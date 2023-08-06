"""
A simple script to receive tracklet messages.

Usage:

```shell
$ python3 -m akkits.scripts.examples.receiver_tracklet
```
"""
import argparse

import zmq

import akkits


def main(sock_addr: str):
    context = zmq.Context()
    receiver = akkits.TrackletReceiver(context, sock_addr)
    print("Receiving packets ...")

    try:
        while True:
            # `recv()` returns a dictionary that looks like this:
            # {
            #     "frame_id": 290,
            #     "count": 2,
            #     "lidarts_ms": 1.6,
            #     "unixts_ms": 1661331594186.1365,
            #     "tracklets": [
            #         {
            #             "track_id": 3,
            #             "class_id": 1,
            #             "confidence": 0.800000011920929,
            #             "bbox": {
            #                 "position": np.array([1.2, 2.2, 3.2], dtype=float32),
            #                 "velocity": np.array([0.2, 0.2, 0.2], dtype=float32),
            #                 "dimension": np.array([8.2, 7.2, 6.2], dtype=float32),
            #                 "yaw": 1.5,
            #             },
            #             "zone_ids": np.array([0, 1], dtype=uint16),
            #         },
            #         ...
            #     ],
            # }
            tracklet = receiver.recv()
            print(f"Packet received: {tracklet}\n")

    except BaseException as e:
        print(f"STOPPING: `examples/receiver_tracklet.py`. Encountered {repr(e)}")
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
    args = parser.parse_args()
    main(sock_addr=f"tcp://{args.ip_addr}:8050")


if __name__ == "__main__":
    main_cli()
