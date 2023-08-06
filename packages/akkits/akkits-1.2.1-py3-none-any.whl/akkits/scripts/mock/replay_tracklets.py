"""
A simple script to send tracklet messages by replaying from
tests/test_data/sample_tracklet.pkl.

Usage:

```shell
$ python3 -m akkits.scripts.mock.replay_tracklets
```
"""
import argparse
import os
import pickle
from time import sleep

import numpy as np
import zmq

import akkits

# from akkits.schema.tracklet_packet.message import decode as decode_tracklet

UINT16_MAX = np.iinfo(np.uint16).max


def main(sock_addr: str, frequency: int = 10, output_dir: str = ""):
    context = zmq.Context()
    sender = akkits.TrackletSender(context, sock_addr)
    try:
        if output_dir == "":
            dir_name = os.path.dirname(__file__)
            pkl_file = open(os.path.join(dir_name, "sample_data/sample_tracklet.pkl"), "rb")
        else:
            pkl_file = open(os.path.join(output_dir, "sample_tracklet.pkl"), "rb")
        i = 0
        while True:
            if frequency > 0:
                sleep(1 / frequency)

            binary = pickle.load(pkl_file)
            # message = decode_tracklet(binary)
            sender.socket.send(binary)
            print("Tracklet sent ")
            i += 1

    except BaseException as e:
        print(f"STOPPING: `akkits/scripts/mock/replay_trackets.py`. Encountered {repr(e)}")
    finally:
        sender.socket.close(1)
        context.term()
        pkl_file.close()


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
        default="",
        help=f"str: Directory to store the tracklet data.",
    )
    args = parser.parse_args()
    main(sock_addr=f"tcp://{args.ip_addr}:8050", output_dir=args.output_dir)


if __name__ == "__main__":
    main_cli()
