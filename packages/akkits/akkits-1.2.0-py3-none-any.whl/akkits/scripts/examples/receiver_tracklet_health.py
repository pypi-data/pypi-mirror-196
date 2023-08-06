"""
A simple script to receive from multiple upstream sources.

Usage:

```shell
$ python3 -m akkits.scripts.examples.receiver_tracklet_health
```
"""
import argparse

import zmq

import akkits


def main(health_sock_addr: str, tracklet_sock_addr: str, poll_timeout: int = 500):
    context = zmq.Context()
    health_receiver = akkits.HealthStatusReceiver(context, health_sock_addr)
    tracklet_receiver = akkits.TrackletReceiver(context, tracklet_sock_addr)

    try:
        poller = zmq.Poller()
        poller.register(health_receiver.socket, zmq.POLLIN)
        poller.register(tracklet_receiver.socket, zmq.POLLIN)
        print("Receiving packets ...")

        while True:
            socks = dict(poller.poll(poll_timeout))
            if health_receiver.socket in socks and socks[health_receiver.socket] == zmq.POLLIN:
                health_status = health_receiver.recv()
                print(f"Health status received: {health_status}\n")
            if tracklet_receiver.socket in socks and socks[tracklet_receiver.socket] == zmq.POLLIN:
                tracklet = tracklet_receiver.recv()
                print(f"Tracklet received: {tracklet}\n")
            if len(socks) == 0:
                print("Timeout")

    except BaseException as e:
        print(f"STOPPING: `examples/receiver_tracklet_health.py`. Encountered {repr(e)}")
    finally:
        health_receiver.socket.close(1)
        tracklet_receiver.socket.close(1)
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
    main(
        health_sock_addr=f"tcp://{args.ip_addr}:7080",
        tracklet_sock_addr=f"tcp://{args.ip_addr}:8050",
    )


if __name__ == "__main__":
    main_cli()
