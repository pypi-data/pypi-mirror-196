import hashlib
import logging
import os
import pickle
import shutil
import subprocess
import traceback
from datetime import datetime, timezone
from os.path import abspath, isdir, join, splitext
from pprint import pformat
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple

import numpy as np
import srsly
from srsly.util import JSONInput, JSONOutput
from tqdm import tqdm

logger = logging.getLogger(__name__)


def load_pickle(file_path: str):
    with open(file_path, "rb") as f:
        return pickle.load(f)


def dump_pickle(out_path: str, obj: Any):
    with open(out_path, "wb") as f:
        pickle.dump(obj, f)


def read_json(path: str) -> JSONOutput:
    """Reads a JSON file.

    Args:
        path (str): Path to the file.

    Returns:
        data (JSONOutput): The data.
    """
    return srsly.read_json(path)


def dump_json(data: JSONInput, path: str, **kwargs) -> str:
    """Writes a JSON file.

    Args:
        data (JSONInput): The data.
        path (str): Path to the file.
        **kwargs: Other keyword arguments to pass into `srsly.write_json`.

    Returns:
        path (str): Path to the file.
    """
    srsly.write_json(path, data, **kwargs)
    return path


def read_yaml(path: str) -> JSONOutput:
    """Reads a YAML file.

    Args:
        path (str): Path to the file.

    Returns:
        data (JSONOutput): The data.
    """
    return srsly.read_yaml(path)


def dump_yaml(data: JSONInput, path: str, **kwargs) -> str:
    """Writes a YAML file.

    Args:
        data (JSONInput): The data.
        path (str): Path to the file.
        **kwargs: Other keyword arguments to pass into `srsly.write_yaml`.

    Returns:
        path (str): Path to the file.
    """
    srsly.write_yaml(path, data, **kwargs)
    return path


def read_file(path, rstrip: bool = True):
    with open(path, "r") as f:
        data = [line.rstrip() if rstrip else line for line in f.readlines()]
    return data


def dumps_file(string, path, utf8=True, lf_newline=True):
    encoding = "utf8" if utf8 else None
    newline = "\n" if lf_newline else None
    with open(path, "w", encoding=encoding, newline=newline) as f:
        f.write(string)
    return path


def listdir_full(path: str):
    return [join(path, directory) for directory in os.listdir(path)]


def subprocess_check_output(
    cmd: str, log_fn: Callable = logger.debug, **kwargs
) -> Tuple[str, bool]:
    """A simple wrapper for `subprocess.check_output()`.

    The following arguments are set when calling `subprocess.check_output()`:
        - `shell = True`
        - `universal_newlines = True`
        - `stderr = subprocess.STDOUT`

    Args:
        cmd (str): Command to execute.
        log_fn (Callable, optional): A callable for logging. Defaults to `logger.debug`.

    Returns:
        outputs (str): Outputs from command execution (stdout and stderr).
        success (bool): True if no errors occurred.
    """
    try:
        outputs = subprocess.check_output(
            cmd,
            shell=True,
            universal_newlines=True,
            stderr=subprocess.STDOUT,
            **kwargs,
        )
    except subprocess.CalledProcessError as e:
        outputs = repr(e)
        success = False
    else:
        success = True
    log_fn(f"Command:\n'{cmd}'\nOutput:\n'{outputs.strip()}'")
    return outputs, success


def get_git_revision_hash(short: bool = True) -> str:
    # https://stackoverflow.com/a/66292983
    cmd = ["git", "rev-parse", "HEAD"]
    if short:
        cmd.insert(2, "--short")
    try:
        hash_val = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        hash_val = str(hash_val, "utf-8").strip()
    except subprocess.CalledProcessError as e:
        hash_val = "Unknown"
        logger.warning(
            f"Unable to get git revision hash, are you in a git directory? \n{e.output.decode('utf8')}"
        )
    return hash_val


def rmtree_if_exists(path: str):
    try:
        shutil.rmtree(path)
    except FileNotFoundError:
        pass


def rm_if_exists(path: str):
    try:
        os.remove(path)
    except FileNotFoundError:
        pass


def set_root_logger_level(
    logging_level: str,
    logging_fmt: str = "%(levelname)s:%(name)s:%(message)s",
    logging_filepath: Optional[str] = None,
    logging_level_tf: Optional[str] = None,
):
    formatter = logging.Formatter(logging_fmt)
    root_logger = logging.getLogger()
    root_logger.setLevel(logging_level)
    root_logger.addHandler(TqdmLoggingHandler())

    if logging_filepath is not None:
        file_handler = logging.FileHandler(logging_filepath)
        file_handler.setFormatter(formatter)
        logging.info(f"Writing logs to: {logging_filepath}")
        root_logger.addHandler(file_handler)

    try:
        root_handler = root_logger.handlers[0]
        root_handler.setFormatter(formatter)
    except IndexError:
        logging.warning("Failed to retrieve root handler, using `basicConfig()`.")
        logging.basicConfig(
            level=logging_level,
            format=logging_fmt,
            handlers=[TqdmLoggingHandler(), file_handler],
        )

    if isinstance(logging_level_tf, str):
        import tensorflow as tf

        tf.get_logger().setLevel(logging_level_tf)

    # Log timestamp
    # https://stackoverflow.com/a/25887393
    logging.info(f"Timestamp: {datetime.now().strftime('%Y/%m/%d %H:%M:%S')}")
    logging.info(f"Timestamp (ISO): {datetime.now(timezone.utc).astimezone().isoformat()}\n")


class TqdmLoggingHandler(logging.Handler):
    """Logging handler that plays nice with tqdm.

    https://stackoverflow.com/a/38739634
    """

    def emit(self, record):
        try:
            msg = self.format(record)
            tqdm.write(msg)
            self.flush()
        except Exception:
            self.handleError(record)


def hash_string_blake2b(string: str, digest_size: int = 8) -> str:
    hasher = hashlib.blake2b(digest_size=digest_size)
    hasher.update(string.encode())
    return hasher.hexdigest()


def find_files(
    directory: str,
    file_ext: Iterable[str],
    max_level: int = -1,
) -> List[str]:
    """
    Recursively lists all the files with matching extension(s) in a directory.

    Args:
        directory (str): The directory path.
        file_ext (Iterable[str]): A list of file extensions to search for.
        max_level (int, optional): Maximum recursion / directory depth. `max_level` < 0 implies no limit.
            Defaults to -1 (no limit).

    Raises:
        OSError: If `directory` is not a directory.

    Returns:
        matched_files (List[str]): A list of label file paths.
    """
    if not isinstance(file_ext, (list, tuple, set)):
        raise TypeError(
            f"`file_ext` must be one of (list, tuple, set), received: {type(file_ext)}"
        )
    file_ext = set(file_ext)

    def _match_file(file_path: str) -> bool:
        return splitext(file_path)[1] in file_ext

    if not isdir(directory):
        raise OSError(f"Not a directory: {directory}")

    directory = abspath(directory)
    matched_files = []
    for root, dirs, files in os.walk(directory, topdown=True):
        if max_level > 0 and root.count(os.sep) - directory.count(os.sep) > max_level:
            del dirs[:]
        else:
            dirs.sort()
            # Filter files
            files = [join(root, f) for f in sorted(files)]
            matched_files += filter(_match_file, files)
    return matched_files


def error_tb_mssg(
    e: Exception,
    name: str,
    log_vars: Dict[str, Any],
) -> str:
    """Returns an error message with traceback for use with try...except.

    Args:
        e (Exception): The exception.
        name (str): Name of the process / program.
        log_vars (Dict[str, Any]): Variables to log.

    Returns:
        message (str): Error message.
    """
    log_vars = {
        k: {"type": type(v), "shape": v.shape, "dtype": v.dtype}
        if isinstance(v, np.ndarray)
        else v
        for k, v in log_vars.items()
    }
    return (
        f"STOPPING {name}. Encountered: {repr(e)}\n"
        f"Traceback: {''.join(traceback.format_tb(e.__traceback__))}\n"
        f"vars: {pformat(log_vars)}"
    )


def print_to_file(out: Any, out_filepath: str):
    out = str(out)
    if out_filepath != "":
        with open(out_filepath, "a") as f:
            print(out, file=f)
    print(out)
