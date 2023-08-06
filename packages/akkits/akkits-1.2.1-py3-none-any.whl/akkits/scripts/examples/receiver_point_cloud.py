"""
A simple script to receive point cloud data.

Usage:

```shell
$ python3 -m akkits.scripts.examples.receiver_point_cloud
```
"""
import argparse

import zmq

import akkits


def main(sock_addr: str):
    context = zmq.Context()
    receiver = akkits.PointCloudReceiver(context, sock_addr)
    print("Receiving packets ...")

    try:
        while True:
            # `recv()` returns a dictionary that looks like this:
            # {
            #     "frame_id": 42,
            #     "lidarts_ms": 1.6,
            #     "unixts_ms": 8.2,
            #     "point_clouds": [
            #         {
            #             "lidar_sn": 8000,
            #             "attr_column": 1,
            #             "column_count": 4,
            #             "row_count": 1000,
            #             "point_cloud": np.array(
            #                 [
            #                     0.41458163,
            #                     ...,
            #                     0.7410443,
            #                 ],
            #                 dtype=np.float32,
            #             ),
            #         }
            #     ],
            # }
            point_cloud = receiver.recv()
            print(f"Packet received: {point_cloud}")

    except BaseException as e:
        print(f"STOPPING: `examples/receiver_point_cloud.py`. Encountered {repr(e)}")
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
    main(sock_addr=f"tcp://{args.ip_addr}:5558")


if __name__ == "__main__":
    main_cli()
