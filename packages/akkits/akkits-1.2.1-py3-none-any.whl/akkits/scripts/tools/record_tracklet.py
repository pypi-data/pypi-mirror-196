"""
A simple script to receive tracklet messages and save the message in pkl format.

Usage:

```shell
$ python3 -m akkits.scripts.tools.record_tracklet
```
"""
import argparse
import os
import pickle

import zmq

import akkits


def main(sock_addr: str, output_dir: str):
    context = zmq.Context()
    receiver = akkits.TrackletReceiver(context, sock_addr)
    print("Receiving packets ...")
    pkl_file = None
    try:
        if output_dir == "":
            dir_name = os.path.dirname(__file__)
            pkl_file = open(os.path.join(dir_name, "../sample_data/sample_tracklet.pkl"), "wb")
        else:
            pkl_file = open(os.path.join(output_dir, "sample_tracklet.pkl"), "wb")
        while True:
            binary_tracklet = receiver.socket.recv()
            pickle.dump(binary_tracklet, pkl_file)

            print("Received packet ...")

    except BaseException as e:
        print(f"STOPPING: `akkits/scripts/tools/record_tracklet.py`. Encountered {repr(e)}")
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
        default="",
        help=f"str: Directory to store the tracklet data.",
    )
    args = parser.parse_args()
    main(sock_addr=f"tcp://{args.ip_addr}:8050", output_dir=args.output_dir)


if __name__ == "__main__":
    main_cli()
