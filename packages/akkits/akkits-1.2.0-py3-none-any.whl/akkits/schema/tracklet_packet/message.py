from typing import Any, Dict, List

import flatbuffers
import numpy as np

from akkits.schema.tracklet_packet import BoundingBox, Tracklet, TrackletsPacket, Vector3
from akkits.utils.flatbuffer import vec3_to_np_array


def build(
    frame_id: int,
    lidar_timestamp: float,
    unix_timestamp: float,
    track_ids: List[int],
    class_ids: List[int],
    confidences: List[float],
    zone_ids: List[List[int]],
    positions: List[List[float]],
    velocities: List[List[float]],
    dimensions: List[List[float]],
    yaws: List[float],
) -> bytearray:
    """Builds the tracklet packet message buffer.

    Args:
        frame_id (int): Frame ID.
        lidar_timestamp (float): Timestamp from LiDAR.
        unix_timestamp (float): Timestamp from sensor interface.
        track_ids (List[int]): List of object track ID.
        class_ids (List[int]): List of object class ID.
        confidences (List[float]): List of object confidence.
        zone_ids (List[List[int]]): List of object zone ID.
        positions (List[List[float]]): List of object position.
        velocities (List[List[float]]): List of object velocity.
        dimensions (List[List[float]]): List of object / bounding box dimension.
        yaws (List[float]): List of object yaw angle.

    Returns:
        buffer (bytearray): Message buffer.
    """
    if not (
        len(track_ids)
        == len(class_ids)
        == len(confidences)
        == len(zone_ids)
        == len(positions)
        == len(velocities)
        == len(dimensions)
        == len(yaws)
    ):
        raise ValueError(
            f"""Inconsistent list lengths:
    len(track_ids) = {len(track_ids)}
    len(class_ids) = {len(class_ids)}
    len(confidences) = {len(confidences)}
    len(zone_ids) = {len(zone_ids)}
    len(positions) = {len(positions)}
    len(velocities) = {len(velocities)}
    len(dimensions) = {len(dimensions)}
    len(yaws) = {len(yaws)}
    """
        )
    object_count = len(track_ids)
    builder = flatbuffers.Builder(0)

    tracklet_offs = []
    for i in range(object_count):
        # BoundingBox
        BoundingBox.Start(builder)
        BoundingBox.AddPosition(builder, Vector3.CreateVector3(builder, *positions[i]))
        BoundingBox.AddVelocity(builder, Vector3.CreateVector3(builder, *velocities[i]))
        BoundingBox.AddDimension(builder, Vector3.CreateVector3(builder, *dimensions[i]))
        BoundingBox.AddYaw(builder, yaws[i])
        bbox_off = BoundingBox.End(builder)

        # Zone IDs
        zone_id = zone_ids[i]
        if isinstance(zone_id, np.ndarray):
            zone_ids_off = builder.CreateNumpyVector(zone_id.astype(np.uint16))
        else:
            Tracklet.StartZoneIdsVector(builder, numElems=len(zone_id))
            for _id in reversed(zone_id):
                builder.PrependUint16(_id)
            zone_ids_off = builder.EndVector()

        Tracklet.Start(builder)
        Tracklet.AddTrackId(builder, track_ids[i])
        Tracklet.AddClassId(builder, class_ids[i])
        Tracklet.AddConfidence(builder, confidences[i])
        Tracklet.AddBbox(builder, bbox_off)
        Tracklet.AddZoneIds(builder, zone_ids_off)
        tracklet_offs.append(Tracklet.End(builder))

    TrackletsPacket.StartTrackletsVector(builder, numElems=object_count)
    for offset in reversed(tracklet_offs):
        builder.PrependUOffsetTRelative(offset)
    tracklets_offset = builder.EndVector()

    TrackletsPacket.Start(builder)
    TrackletsPacket.AddFrameId(builder, frame_id)
    TrackletsPacket.AddCount(builder, object_count)
    TrackletsPacket.AddLidartsMs(builder, lidar_timestamp)
    TrackletsPacket.AddUnixtsMs(builder, unix_timestamp)
    TrackletsPacket.AddTracklets(builder, tracklets_offset)
    root = TrackletsPacket.End(builder)

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
            "count",
            "lidarts_ms",
            "unixts_ms",
            "tracklets"
    """
    root = TrackletsPacket.TrackletsPacket.GetRootAs(buf, 0)

    tracklets = []
    for i in range(root.TrackletsLength()):
        tracklet = root.Tracklets(i)
        bbox = tracklet.Bbox()
        tracklets.append(
            {
                "track_id": tracklet.TrackId(),
                "class_id": tracklet.ClassId(),
                "confidence": tracklet.Confidence(),
                "bbox": {
                    "position": vec3_to_np_array(bbox.Position()),
                    "velocity": vec3_to_np_array(bbox.Velocity()),
                    "dimension": vec3_to_np_array(bbox.Dimension()),
                    "yaw": bbox.Yaw(),
                },
                "zone_ids": tracklet.ZoneIdsAsNumpy(),
            }
        )
    output_dict = {
        "frame_id": root.FrameId(),
        "count": root.Count(),
        "lidarts_ms": root.LidartsMs(),
        "unixts_ms": root.UnixtsMs(),
        "tracklets": tracklets,
    }
    return output_dict
