"""
A simple script to record point cloud from Fusion Box.

If `.pkl` file format is selected, the entire point cloud
message will be stored.

If `.bin` file format is selected, only the point cloud field
is stored as "<f" float binary.

Usage:

```shell
$ python3 -m akkits.scripts.tools.record_point_cloud
```

# specifying the output directory and file format
```
$ python3 -m akkits.scripts.tools.record_point_cloud \
    --output_dir <path/to/directory> \
    --ext <.pkl/or/.bin>
```

# recording data from remote machines
```
$ python3 tools/record_point_cloud.py \
    --ip_addr <remote/host/ip>
```
"""
import argparse
import os
import pickle

import numpy as np
import zmq

import akkits


def main(sock_addr: str, output_dir: str, ext: str):

    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)

    context = zmq.Context()
    receiver = akkits.PointCloudReceiver(context, sock_addr)

    output_file = None

    print("Receiving packets ...")
    try:
        while True:
            point_cloud_msg = receiver.recv()
            if ext == ".pkl":
                if output_file is None:
                    output_file = open(
                        os.path.join(output_dir, f"{np.uint64(point_cloud_msg['unixts_ms'])}.pkl"),
                        "wb",
                    )
                pickle.dump(point_cloud_msg, output_file)

            elif ext == ".bin":
                # print(point_cloud_msg)
                point_cloud_data = point_cloud_msg["point_clouds"][0]["point_cloud"]

                if output_file is None:
                    with open(
                        os.path.join(
                            output_dir, f"{np.uint64(point_cloud_msg['unixts_ms'])}_metadata.txt"
                        ),
                        "w+",
                    ) as metadata_file:
                        attr_column = point_cloud_msg["point_clouds"][0]["attr_column"]
                        column_count = point_cloud_msg["point_clouds"][0]["column_count"]
                        metadata_str = (
                            f"attr_column:{attr_column}\n"
                            + f"column_count:{column_count}\n"
                            + f"data_type:float32\n"
                        )
                        metadata_file.write(metadata_str)
                output_file = os.path.join(
                    output_dir, f"{np.uint64(point_cloud_msg['unixts_ms'])}.bin"
                )
                point_cloud_data.tofile(output_file)
            else:
                raise ValueError(f"File extension format {ext} storage is not supported.")

            print("Received packet ...")

    except BaseException as e:
        print(f"STOPPING: `akkits/scripts/tools/record_point_cloud.py`. Encountered {repr(e)}")
    finally:
        receiver.socket.close(1)
        context.term()


def main_cli():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--ip_addr",
        type=str,
        default="127.0.0.1",
        help=f"str: Host IP address.",
    )
    parser.add_argument(
        "--output_dir",
        type=str,
        default="./artifacts",
        help=f"str: Directory to store the point cloud data.",
    )
    parser.add_argument(
        "--ext",
        type=str,
        default=".pkl",
        help=f"str: Supported two storage type based on file extension: `.pkl` (Default) and `.bin`.",
    )
    args = parser.parse_args()
    main(sock_addr=f"tcp://{args.ip_addr}:5558", output_dir=args.output_dir, ext=args.ext)


if __name__ == "__main__":
    main_cli()
