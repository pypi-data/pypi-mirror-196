from typing import Any, Dict, List

import flatbuffers
import numpy as np

from akkits.schema.point_cloud import AttrType, PointCloud, PointCloudPacket


def build(
    frame_id: int,
    lidar_timestamp: float,
    unix_timestamp: float,
    lidars_sn: List[int],
    attr_columns: List[int],
    point_clouds: List[np.ndarray],
) -> bytearray:
    """Builds the point cloud data message buffer.

    Args:
        frame_id (int): Frame ID.
        lidar_timestamp (float): Timestamp from LiDAR.
        unix_timestamp (float): Timestamp from sensor interface.
        lidars_sn (List[int]): List of LiDAR serial number.
        attr_columns (List[int]): List of attribute type: :py:class:`akkits.AttrType`.
        point_clouds (List[np.ndarray]): List of point cloud NumPy array.

    Returns:
        buffer (bytearray): Message buffer.
    """
    if not (len(lidars_sn) == len(attr_columns) == len(point_clouds)):
        raise ValueError(
            f"""Inconsistent list lengths:
    len(lidars_sn) = {len(lidars_sn)}
    len(attr_columns) = {len(attr_columns)}
    len(point_clouds) = {len(point_clouds)}
    """
        )
    if any(pc.ndim != 2 for pc in point_clouds):
        raise ValueError(
            "All point cloud arrays must be rank 2, received: "
            f"{[pc.ndim for pc in point_clouds]}."
        )

    builder = flatbuffers.Builder(0)

    point_cloud_offs = []
    for i in range(len(point_clouds)):
        point_cloud = point_clouds[i]
        attr = attr_columns[i]
        row_count, col_count = point_cloud.shape
        if col_count == 3 and attr != AttrType.AttrType.NoAttr:
            raise ValueError(
                "If point cloud data have 3 columns, then AttrType must be NoAttr. "
                f"Received point cloud with shape {point_cloud.shape} and"
                f"AttrType {attr}"
            )
        if col_count != 3 and attr == AttrType.AttrType.NoAttr:
            raise ValueError(
                "If point cloud data have more than 3 columns, then AttrType cannot be NoAttr. "
                f"Received point cloud with shape {point_cloud.shape} and"
                f"AttrType {attr}"
            )

        pc_off = builder.CreateNumpyVector(point_cloud.reshape(-1).astype(np.float32))
        PointCloud.Start(builder)
        PointCloud.AddLidarSn(builder, lidars_sn[i])
        PointCloud.AddAttrColumn(builder, attr)
        PointCloud.AddColumnCount(builder, col_count)
        PointCloud.AddRowCount(builder, row_count)
        PointCloud.AddPointCloud(builder, pc_off)
        point_cloud_offs.append(PointCloud.End(builder))

    PointCloudPacket.StartPointCloudsVector(builder, numElems=len(point_clouds))
    for offset in reversed(point_cloud_offs):
        builder.PrependUOffsetTRelative(offset)
    point_clouds_offset = builder.EndVector()

    PointCloudPacket.Start(builder)
    PointCloudPacket.AddFrameId(builder, frame_id)
    PointCloudPacket.AddLidartsMs(builder, lidar_timestamp)
    PointCloudPacket.AddUnixtsMs(builder, unix_timestamp)
    PointCloudPacket.AddPointClouds(builder, point_clouds_offset)
    root = PointCloudPacket.End(builder)

    _ = builder.Finish(root)
    buf = builder.Output()

    return buf


def decode(buf: bytearray) -> Dict[str, Any]:
    """Decodes the message buffer.

    Args:
        buf (bytearray): Message buffer.

    Returns:
        data (Dict[str, Any]): A dictionary with keys:
            "frame_id",
            "lidarts_ms",
            "unixts_ms",
            "point_clouds"
    """
    root = PointCloudPacket.PointCloudPacket.GetRootAs(buf, 0)
    point_clouds = []
    for i in range(root.PointCloudsLength()):
        point_cloud = root.PointClouds(i)
        point_clouds.append(
            {
                "lidar_sn": point_cloud.LidarSn(),
                "attr_column": point_cloud.AttrColumn(),
                "column_count": point_cloud.ColumnCount(),
                "row_count": point_cloud.RowCount(),
                "point_cloud": point_cloud.PointCloudAsNumpy(),
            }
        )
    output_dict = {
        "frame_id": root.FrameId(),
        "lidarts_ms": root.LidartsMs(),
        "unixts_ms": root.UnixtsMs(),
        "point_clouds": point_clouds,
    }
    return output_dict
