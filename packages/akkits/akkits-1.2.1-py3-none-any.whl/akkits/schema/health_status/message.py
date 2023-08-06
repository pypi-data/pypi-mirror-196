from time import time
from typing import Any, Dict

import flatbuffers

from akkits.schema.health_status import AlgoStatus, DeviceStatus, HealthStatus, SensorStatus


def build(
    device_status: int = DeviceStatus.DeviceStatus.Normal,
    algo_status: int = AlgoStatus.AlgoStatus.Normal,
    sensor_status: int = SensorStatus.SensorStatus.Normal,
) -> bytearray:
    """Builds the health status message buffer.

    Args:
        device_status (int, optional): Device status. Defaults to :py:data:`akkits.DeviceStatus.Normal`.
        algo_status (int, optional): Algorithm status. Defaults to :py:data:`akkits.AlgoStatus.Normal`.
        sensor_status (int, optional): Sensor status. Defaults to :py:data:`akkits.SensorStatus.Normal`.

    Returns:
        buffer (bytearray): Message buffer.
    """
    builder = flatbuffers.Builder(0)

    HealthStatus.Start(builder)
    HealthStatus.AddUnixtsMs(builder, time() * 1000.0)
    HealthStatus.AddDeviceStatus(builder, device_status)
    HealthStatus.AddAlgoStatus(builder, algo_status)
    HealthStatus.AddSensorStatus(builder, sensor_status)
    root = HealthStatus.End(builder)

    _ = builder.Finish(root)
    buf = builder.Output()

    return buf


def decode(buf: bytearray) -> Dict[str, Any]:
    """Decodes the message buffer.

    Args:
        buf (bytearray): Message buffer.

    Returns:
        data (Dict[str, Any]): A dictionary with keys:
            "unixts_ms",
            "device_status",
            "algo_status",
            "sensor_status"
    """
    root = HealthStatus.HealthStatus.GetRootAs(buf, 0)
    output_dict = {
        "unixts_ms": root.UnixtsMs(),
        "device_status": root.DeviceStatus(),
        "algo_status": root.AlgoStatus(),
        "sensor_status": root.SensorStatus(),
    }
    return output_dict
