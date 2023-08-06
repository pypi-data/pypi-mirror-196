"""
A script to mock various health status messages.

Usage:

```shell
# All status Normal
$ python3 src/akkits/scripts/mock/faulty_fusion_controller.py

# Set one or more status
$ python3 src/akkits/scripts/mock/faulty_fusion_controller.py --device_status 1
$ python3 src/akkits/scripts/mock/faulty_fusion_controller.py --algo_status 1
$ python3 src/akkits/scripts/mock/faulty_fusion_controller.py --sensor_status 1
$ python3 src/akkits/scripts/mock/faulty_fusion_controller.py --device_status 1 --algo_status 1
$ python3 src/akkits/scripts/mock/faulty_fusion_controller.py --device_status 2 --algo_status 1 --sensor_status 2
```
"""
import argparse
from time import sleep

import zmq

import akkits
from akkits.utils import _Inspect


def main(
    sock_addr: str,
    device_status: int,
    algo_status: int,
    sensor_status: int,
    frequency: int = 1,
):
    context = zmq.Context()
    sender = akkits.HealthStatusSender(context, sock_addr)

    try:
        while True:
            if frequency > 0:
                sleep(1 / frequency)
            sender.send(device_status, algo_status, sensor_status)
            print("Health status sent")

    except BaseException as e:
        print(f"STOPPING: `mock/faulty_fusion_controller.py`. Encountered {repr(e)}")
    finally:
        sender.socket.close(1)
        context.term()


def main_cli():
    args = vars(parse_args())
    main(sock_addr=f"tcp://{args.pop('ip_addr')}:7080", **args)


def parse_args() -> argparse.Namespace:
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
        "--device_status",
        type=int,
        default=akkits.DeviceStatus.Normal,
        choices=_Inspect(akkits.DeviceStatus).attributes.values(),
        help=f"int: DeviceStatus.",
    )
    parser.add_argument(
        "--algo_status",
        type=int,
        default=akkits.AlgoStatus.Normal,
        choices=_Inspect(akkits.AlgoStatus).attributes.values(),
        help=f"int: AlgoStatus.",
    )
    parser.add_argument(
        "--sensor_status",
        type=int,
        default=akkits.SensorStatus.Normal,
        choices=_Inspect(akkits.SensorStatus).attributes.values(),
        help=f"int: SensorStatus.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    main_cli()
