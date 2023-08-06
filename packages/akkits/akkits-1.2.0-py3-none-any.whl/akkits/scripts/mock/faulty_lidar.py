"""
A script to mock "sensor lost connection" health status.

Usage:

```shell
$ python3 src/akkits/scripts/mock/faulty_lidar.py
```
"""
import argparse
from multiprocessing import Process
from time import sleep

import zmq

import akkits


def _send_health_status(
    sock_addr: str,
    sink_addr: str,
    poll_timeout: int = 1,
):
    context = zmq.Context()
    sender = akkits.HealthStatusSender(context, sock_addr)
    sink = context.socket(zmq.PULL)
    sensor_status = akkits.SensorStatus.Normal
    try:
        sink.connect(sink_addr)
        poller = zmq.Poller()
        poller.register(sink, zmq.POLLIN)

        while True:
            socks = dict(poller.poll(poll_timeout))
            if sink in socks and socks[sink] == zmq.POLLIN:
                sensor_status = sink.recv_pyobj()
            if sensor_status < 0:
                break
            sleep(1.0 - (poll_timeout / 1000.0))
            sender.send(sensor_status=sensor_status)
    except BaseException as e:
        print(f"STOPPING: _send_health_status. Encountered {repr(e)}")
    finally:
        sender.socket.close(1)
        sink.close(1)
        context.term()


def main(sock_addr: str, sink_addr: str):
    procs = [
        Process(
            target=_send_health_status,
            args=[sock_addr, sink_addr],
            daemon=True,
        ),
    ]

    for process in procs:
        process.start()
        sleep(0.1)
    print("> All mock ZMQ processes launched.")

    context = zmq.Context()
    sink = context.socket(zmq.PUSH)
    sensor_status = akkits.SensorStatus.Normal

    try:
        sink.bind(sink_addr)
        sink.send_pyobj(sensor_status)

        while True:
            if sensor_status == akkits.SensorStatus.Normal:
                input("Enter any key to switch to `SensorStatus.LostConnection`: ")
                sensor_status = akkits.SensorStatus.LostConnection
            else:
                input("Enter any key to switch to `SensorStatus.Normal`: ")
                sensor_status = akkits.SensorStatus.Normal
            sink.send_pyobj(sensor_status)

    except BaseException as e:
        print(f"> STOPPING: `mock/faulty_lidar.py`. Encountered {repr(e)}")
        raise
    finally:
        sink.send_pyobj(-1)
        sink.close(1)
        context.term()
        print("> Stopping processes ...")
        for process in procs:
            process.terminate()
            process.join()
            try:
                process.close()
            except AttributeError:
                # Python < 3.7
                pass
        sleep(1.0)
        print("> Exiting ...")


def main_cli():
    ip_addr = parse_args().ip_addr
    main(sock_addr=f"tcp://{ip_addr}:7080", sink_addr=f"tcp://{ip_addr}:5000")


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
    return parser.parse_args()


if __name__ == "__main__":
    main_cli()
