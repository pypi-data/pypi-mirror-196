"""
A simple script to send health status messages.

Usage:

```shell
$ python3 -m akkits.scripts.examples.sender_health
```
"""
import argparse
from time import sleep

import zmq

import akkits


def main(sock_addr: str, frequency: int = 1):
    context = zmq.Context()
    sender = akkits.HealthStatusSender(context, sock_addr)

    try:
        while True:
            if frequency > 0:
                sleep(1 / frequency)
            sender.send(akkits.DeviceStatus.None_)
            print("Health status sent")

    except BaseException as e:
        print(f"STOPPING: `examples/sender_health.py`. Encountered {repr(e)}")
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
    main(sock_addr=f"tcp://{args.ip_addr}:7080")


if __name__ == "__main__":
    main_cli()
