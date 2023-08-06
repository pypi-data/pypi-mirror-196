"""
A simple script to send point cloud data.

Usage:

```shell
$ python3 -m akkits.scripts.examples.sender_point_cloud
```
"""
import argparse
from time import sleep

import numpy as np
import zmq

import akkits

UINT16_MAX = np.iinfo(np.uint16).max


def main(sock_addr: str, frequency: int = 10):
    context = zmq.Context()
    sender = akkits.PointCloudSender(context, sock_addr)

    try:
        i = 0
        while True:
            if frequency > 0:
                sleep(1 / frequency)
            sender.send(
                frame_id=i,
                lidar_timestamp=1.6,
                unix_timestamp=8.2,
                lidars_sn=[8000],
                attr_columns=[akkits.AttrType.Range],
                point_clouds=[np.random.rand(1000, 4)],
            )
            print(f"Point cloud sent: Frame ID = {i}")
            i = (i + 1) % UINT16_MAX

    except BaseException as e:
        print(f"STOPPING: `examples/sender_point_cloud.py`. Encountered {repr(e)}")
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
    main(sock_addr=f"tcp://{args.ip_addr}:5558")


if __name__ == "__main__":
    main_cli()
