"""
A simple script to receive health status messages.

Usage:

```shell
$ python3 -m akkits.scripts.examples.receiver_health
```
"""
import argparse

import zmq

import akkits


def main(sock_addr: str):
    context = zmq.Context()
    receiver = akkits.HealthStatusReceiver(context, sock_addr)
    print("Receiving packets ...")

    try:
        while True:
            # `recv()` returns a dictionary that looks like this:
            # {
            #     "unixts_ms": 1661325459187.7039,
            #     "device_status": 0,
            #     "algo_status": 1,
            #     "sensor_status": 1,
            # }
            health_status = receiver.recv()
            print(f"Packet received: {health_status}")

    except BaseException as e:
        print(f"STOPPING: `examples/receiver_health.py`. Encountered {repr(e)}")
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
    main(sock_addr=f"tcp://{args.ip_addr}:7080")


if __name__ == "__main__":
    main_cli()
