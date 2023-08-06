"""
A simple script to send tracklet messages.

Usage:

```shell
$ python3 -m akkits.scripts.examples.sender_tracklet
```
"""
import argparse
from time import sleep, time

import numpy as np
import zmq

import akkits

UINT16_MAX = np.iinfo(np.uint16).max


def main(sock_addr: str, frequency: int = 10):
    context = zmq.Context()
    sender = akkits.TrackletSender(context, sock_addr)

    try:
        i = 0
        while True:
            if frequency > 0:
                sleep(1 / frequency)
            sender.send(
                frame_id=i % UINT16_MAX,
                lidar_timestamp=1.6,
                unix_timestamp=time() * 1000.0,
                track_ids=[3, 2],
                class_ids=[1, 0],
                confidences=[0.8, 0.9],
                zone_ids=[[0, 1], [2]],
                positions=[[1.2, 2.2, 3.2], [0.5, 1.8, 0.7]],
                velocities=[[0.2, 0.2, 0.2], [1.5, 2.8, 2.7]],
                dimensions=[[8.2, 7.2, 6.2], [5.5, 4.8, 3.7]],
                yaws=[1.5, 2.7],
            )
            print("Tracklet sent")
            i += 1

    except BaseException as e:
        print(f"STOPPING: `examples/sender_tracklet.py`. Encountered {repr(e)}")
    finally:
        sender.socket.close(1)
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
    args = parser.parse_args()
    main(sock_addr=f"tcp://{args.ip_addr}:8050")


if __name__ == "__main__":
    main_cli()
