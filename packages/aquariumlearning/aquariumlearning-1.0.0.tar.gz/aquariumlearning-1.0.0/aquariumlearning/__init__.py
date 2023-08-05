# Only expose public API

from .util import (
    PrimaryTaskTypes as PrimaryTaskTypes,
    InstanceSegInstance as InstanceSegInstance,
    check_if_update_needed,
)

from .client import (
    Client as Client,
    LabelClassMap as LabelClassMap,
    ClassMapEntry as ClassMapEntry,
    ClassMapUpdateEntry as ClassMapUpdateEntry,
    CustomMetricsDefinition as CustomMetricsDefinition,
    StratifiedMetricsDefinition as StratifiedMetricsDefinition,
    orig_label_color_list as orig_label_color_list,
    tableau_colors as tableau_colors,
    turbo_rgb as turbo_rgb,
    viridis_rgb as viridis_rgb,
)
from .collection_client import CollectionClient as CollectionClient
from .coordinate_frames import (
    CoordinateFrame2D as CoordinateFrame2D,
    CoordinateFrame3D as CoordinateFrame3D,
)
from .datasets_2 import (
    LabeledDataset as LabeledDataset,
    InferenceSet as InferenceSet,
    UnlabeledDataset as UnlabeledDataset,
    UnlabeledDatasetV2 as UnlabeledDatasetV2,
)
from .frames_2 import (
    GeoData as GeoData,
    UserMetadataEntry as UserMetadataEntry,
    LabeledFrame as LabeledFrame,
    ModifiedLabeledFrame as ModifiedLabeledFrame,
    InferenceFrame as InferenceFrame,
    UnlabeledFrame as UnlabeledFrame,
    UnlabeledFrameV2 as UnlabeledFrameV2,
)
from .labels_2 import (
    Bbox2DLabel as Bbox2DLabel,
    LineSegment2DLabel as LineSegment2DLabel,
    Keypoint2DLabel as Keypoint2DLabel,
    PolygonList2DLabel as PolygonList2DLabel,
    Semseg2DLabel as Semseg2DLabel,
    InstanceSeg2DLabel as InstanceSeg2DLabel,
    Classification2DLabel as Classification2DLabel,
    Classification3DLabel as Classification3DLabel,
    Cuboid3DLabel as Cuboid3DLabel,
    TextTokenLabel as TextTokenLabel,
)
from .modified_labels import (
    ModifiedBbox2DLabel as ModifiedBbox2DLabel,
    ModifiedLineSegment2DLabel as ModifiedLineSegment2DLabel,
    ModifiedKeypoint2DLabel as ModifiedKeypoint2DLabel,
    ModifiedPolygonList2DLabel as ModifiedPolygonList2DLabel,
    ModifiedSemseg2DLabel as ModifiedSemseg2DLabel,
    ModifiedInstanceSeg2DLabel as ModifiedInstanceSeg2DLabel,
    ModifiedClassification2DLabel as ModifiedClassification2DLabel,
    ModifiedClassification3DLabel as ModifiedClassification3DLabel,
    ModifiedCuboid3DLabel as ModifiedCuboid3DLabel,
    ModifiedTextTokenLabel as ModifiedTextTokenLabel,
)
from .inferences_2 import (
    Bbox2DInference as Bbox2DInference,
    LineSegment2DInference as LineSegment2DInference,
    Keypoint2DInference as Keypoint2DInference,
    PolygonList2DInference as PolygonList2DInference,
    Semseg2DInference as Semseg2DInference,
    InstanceSeg2DInference as InstanceSeg2DInference,
    Classification2DInference as Classification2DInference,
    Classification3DInference as Classification3DInference,
    Cuboid3DInference as Cuboid3DInference,
    TextTokenInference as TextTokenInference,
)
from .sensor_data import (
    Image as Image,
    ImageOverlay as ImageOverlay,
    Text as Text,
    PointCloudPCD as PointCloudPCD,
    PointCloudBins as PointCloudBins,
    Obj as Obj,
    Audio as Audio,
    Video as Video,
)

from .segments import (
    SegmentManager as SegmentManager,
    Segment as Segment,
    SegmentElement as SegmentElement,
)
from .metrics_manager import MetricsManager as MetricsManager
from .work_queues import (
    WorkQueueManager as WorkQueueManager,
    WorkQueue as WorkQueue,
    WorkQueueElement as WorkQueueElement,
)

# TODO: Avoid duplicating here while still getting nice autodoc?
__all__ = [
    "Client",
    "PrimaryTaskTypes",
    "LabeledDataset",
    "InferenceSet",
    "UnlabeledDataset",
    "UnlabeledDatasetV2",
    "UserMetadataEntry",
    "GeoData",
    "LabeledFrame",
    "ModifiedLabeledFrame",
    "InferenceFrame",
    "UnlabeledFrame",
    "UnlabeledFrameV2",
    "Bbox2DLabel",
    "LineSegment2DLabel",
    "Keypoint2DLabel",
    "PolygonList2DLabel",
    "Semseg2DLabel",
    "InstanceSegInstance",
    "InstanceSeg2DLabel",
    "Classification2DLabel",
    "Classification3DLabel",
    "Cuboid3DLabel",
    "TextTokenLabel",
    "ModifiedBbox2DLabel",
    "ModifiedLineSegment2DLabel",
    "ModifiedKeypoint2DLabel",
    "ModifiedPolygonList2DLabel",
    "ModifiedSemseg2DLabel",
    "ModifiedInstanceSeg2DLabel",
    "ModifiedClassification2DLabel",
    "ModifiedClassification3DLabel",
    "ModifiedCuboid3DLabel",
    "ModifiedTextTokenLabel",
    "Bbox2DInference",
    "LineSegment2DInference",
    "Keypoint2DInference",
    "PolygonList2DInference",
    "Semseg2DInference",
    "InstanceSeg2DInference",
    "Classification2DInference",
    "Classification3DInference",
    "Cuboid3DInference",
    "TextTokenInference",
    "Image",
    "ImageOverlay",
    "Text",
    "PointCloudPCD",
    "PointCloudBins",
    "Obj",
    "Audio",
    "Video",
    "CoordinateFrame2D",
    "CoordinateFrame3D",
    "LabelClassMap",
    "ClassMapEntry",
    "ClassMapUpdateEntry",
    "CustomMetricsDefinition",
    "StratifiedMetricsDefinition",
    "orig_label_color_list",
    "tableau_colors",
    "turbo_rgb",
    "viridis_rgb",
    "CollectionClient",
    "MetricsManager",
    "SegmentManager",
    "Segment",
    "SegmentElement",
    "WorkQueueManager",
    "WorkQueue",
    "WorkQueueElement",
]

check_if_update_needed()
