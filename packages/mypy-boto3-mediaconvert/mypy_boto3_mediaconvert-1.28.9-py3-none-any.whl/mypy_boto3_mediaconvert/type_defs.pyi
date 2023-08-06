"""
Type annotations for mediaconvert service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediaconvert/type_defs/)

Usage::

    ```python
    from mypy_boto3_mediaconvert.type_defs import AacSettingsOutputTypeDef

    data: AacSettingsOutputTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence

from .literals import (
    AacAudioDescriptionBroadcasterMixType,
    AacCodecProfileType,
    AacCodingModeType,
    AacRateControlModeType,
    AacRawFormatType,
    AacSpecificationType,
    AacVbrQualityType,
    Ac3BitstreamModeType,
    Ac3CodingModeType,
    Ac3DynamicRangeCompressionLineType,
    Ac3DynamicRangeCompressionProfileType,
    Ac3DynamicRangeCompressionRfType,
    Ac3LfeFilterType,
    Ac3MetadataControlType,
    AccelerationModeType,
    AccelerationStatusType,
    AdvancedInputFilterAddTextureType,
    AdvancedInputFilterSharpenType,
    AdvancedInputFilterType,
    AfdSignalingType,
    AlphaBehaviorType,
    AncillaryConvert608To708Type,
    AncillaryTerminateCaptionsType,
    AntiAliasType,
    AudioChannelTagType,
    AudioCodecType,
    AudioDefaultSelectionType,
    AudioDurationCorrectionType,
    AudioLanguageCodeControlType,
    AudioNormalizationAlgorithmControlType,
    AudioNormalizationAlgorithmType,
    AudioNormalizationLoudnessLoggingType,
    AudioNormalizationPeakCalculationType,
    AudioSelectorTypeType,
    AudioTypeControlType,
    Av1AdaptiveQuantizationType,
    Av1BitDepthType,
    Av1FramerateControlType,
    Av1FramerateConversionAlgorithmType,
    Av1SpatialAdaptiveQuantizationType,
    AvcIntraClassType,
    AvcIntraFramerateControlType,
    AvcIntraFramerateConversionAlgorithmType,
    AvcIntraInterlaceModeType,
    AvcIntraScanTypeConversionModeType,
    AvcIntraSlowPalType,
    AvcIntraTelecineType,
    AvcIntraUhdQualityTuningLevelType,
    BandwidthReductionFilterSharpeningType,
    BandwidthReductionFilterStrengthType,
    BillingTagsSourceType,
    BurninSubtitleAlignmentType,
    BurninSubtitleApplyFontColorType,
    BurninSubtitleBackgroundColorType,
    BurninSubtitleFallbackFontType,
    BurninSubtitleFontColorType,
    BurninSubtitleOutlineColorType,
    BurninSubtitleShadowColorType,
    BurnInSubtitleStylePassthroughType,
    BurninSubtitleTeletextSpacingType,
    CaptionDestinationTypeType,
    CaptionSourceConvertPaintOnToPopOnType,
    CaptionSourceTypeType,
    CmafClientCacheType,
    CmafCodecSpecificationType,
    CmafEncryptionTypeType,
    CmafImageBasedTrickPlayType,
    CmafInitializationVectorInManifestType,
    CmafIntervalCadenceType,
    CmafKeyProviderTypeType,
    CmafManifestCompressionType,
    CmafManifestDurationFormatType,
    CmafMpdManifestBandwidthTypeType,
    CmafMpdProfileType,
    CmafPtsOffsetHandlingForBFramesType,
    CmafSegmentControlType,
    CmafSegmentLengthControlType,
    CmafStreamInfResolutionType,
    CmafTargetDurationCompatibilityModeType,
    CmafVideoCompositionOffsetsType,
    CmafWriteDASHManifestType,
    CmafWriteHLSManifestType,
    CmafWriteSegmentTimelineInRepresentationType,
    CmfcAudioDurationType,
    CmfcAudioTrackTypeType,
    CmfcDescriptiveVideoServiceFlagType,
    CmfcIFrameOnlyManifestType,
    CmfcKlvMetadataType,
    CmfcManifestMetadataSignalingType,
    CmfcScte35EsamType,
    CmfcScte35SourceType,
    CmfcTimedMetadataBoxVersionType,
    CmfcTimedMetadataType,
    ColorMetadataType,
    ColorSpaceConversionType,
    ColorSpaceType,
    ColorSpaceUsageType,
    ContainerTypeType,
    CopyProtectionActionType,
    DashIsoGroupAudioChannelConfigSchemeIdUriType,
    DashIsoHbbtvComplianceType,
    DashIsoImageBasedTrickPlayType,
    DashIsoIntervalCadenceType,
    DashIsoMpdManifestBandwidthTypeType,
    DashIsoMpdProfileType,
    DashIsoPlaybackDeviceCompatibilityType,
    DashIsoPtsOffsetHandlingForBFramesType,
    DashIsoSegmentControlType,
    DashIsoSegmentLengthControlType,
    DashIsoVideoCompositionOffsetsType,
    DashIsoWriteSegmentTimelineInRepresentationType,
    DashManifestStyleType,
    DecryptionModeType,
    DeinterlaceAlgorithmType,
    DeinterlacerControlType,
    DeinterlacerModeType,
    DescribeEndpointsModeType,
    DolbyVisionLevel6ModeType,
    DolbyVisionMappingType,
    DolbyVisionProfileType,
    DropFrameTimecodeType,
    DvbddsHandlingType,
    DvbSubSubtitleFallbackFontType,
    DvbSubtitleAlignmentType,
    DvbSubtitleApplyFontColorType,
    DvbSubtitleBackgroundColorType,
    DvbSubtitleFontColorType,
    DvbSubtitleOutlineColorType,
    DvbSubtitleShadowColorType,
    DvbSubtitleStylePassthroughType,
    DvbSubtitleTeletextSpacingType,
    DvbSubtitlingTypeType,
    Eac3AtmosCodingModeType,
    Eac3AtmosDialogueIntelligenceType,
    Eac3AtmosDownmixControlType,
    Eac3AtmosDynamicRangeCompressionLineType,
    Eac3AtmosDynamicRangeCompressionRfType,
    Eac3AtmosDynamicRangeControlType,
    Eac3AtmosMeteringModeType,
    Eac3AtmosStereoDownmixType,
    Eac3AtmosSurroundExModeType,
    Eac3AttenuationControlType,
    Eac3BitstreamModeType,
    Eac3CodingModeType,
    Eac3DcFilterType,
    Eac3DynamicRangeCompressionLineType,
    Eac3DynamicRangeCompressionRfType,
    Eac3LfeControlType,
    Eac3LfeFilterType,
    Eac3MetadataControlType,
    Eac3PassthroughControlType,
    Eac3PhaseControlType,
    Eac3StereoDownmixType,
    Eac3SurroundExModeType,
    Eac3SurroundModeType,
    EmbeddedConvert608To708Type,
    EmbeddedTerminateCaptionsType,
    EmbeddedTimecodeOverrideType,
    F4vMoovPlacementType,
    FileSourceConvert608To708Type,
    FileSourceTimeDeltaUnitsType,
    FontScriptType,
    H264AdaptiveQuantizationType,
    H264CodecLevelType,
    H264CodecProfileType,
    H264DynamicSubGopType,
    H264EntropyEncodingType,
    H264FieldEncodingType,
    H264FlickerAdaptiveQuantizationType,
    H264FramerateControlType,
    H264FramerateConversionAlgorithmType,
    H264GopBReferenceType,
    H264GopSizeUnitsType,
    H264InterlaceModeType,
    H264ParControlType,
    H264QualityTuningLevelType,
    H264RateControlModeType,
    H264RepeatPpsType,
    H264ScanTypeConversionModeType,
    H264SceneChangeDetectType,
    H264SlowPalType,
    H264SpatialAdaptiveQuantizationType,
    H264SyntaxType,
    H264TelecineType,
    H264TemporalAdaptiveQuantizationType,
    H264UnregisteredSeiTimecodeType,
    H265AdaptiveQuantizationType,
    H265AlternateTransferFunctionSeiType,
    H265CodecLevelType,
    H265CodecProfileType,
    H265DynamicSubGopType,
    H265FlickerAdaptiveQuantizationType,
    H265FramerateControlType,
    H265FramerateConversionAlgorithmType,
    H265GopBReferenceType,
    H265GopSizeUnitsType,
    H265InterlaceModeType,
    H265ParControlType,
    H265QualityTuningLevelType,
    H265RateControlModeType,
    H265SampleAdaptiveOffsetFilterModeType,
    H265ScanTypeConversionModeType,
    H265SceneChangeDetectType,
    H265SlowPalType,
    H265SpatialAdaptiveQuantizationType,
    H265TelecineType,
    H265TemporalAdaptiveQuantizationType,
    H265TemporalIdsType,
    H265TilesType,
    H265UnregisteredSeiTimecodeType,
    H265WriteMp4PackagingTypeType,
    HDRToSDRToneMapperType,
    HlsAdMarkersType,
    HlsAudioOnlyContainerType,
    HlsAudioOnlyHeaderType,
    HlsAudioTrackTypeType,
    HlsCaptionLanguageSettingType,
    HlsCaptionSegmentLengthControlType,
    HlsClientCacheType,
    HlsCodecSpecificationType,
    HlsDescriptiveVideoServiceFlagType,
    HlsDirectoryStructureType,
    HlsEncryptionTypeType,
    HlsIFrameOnlyManifestType,
    HlsImageBasedTrickPlayType,
    HlsInitializationVectorInManifestType,
    HlsIntervalCadenceType,
    HlsKeyProviderTypeType,
    HlsManifestCompressionType,
    HlsManifestDurationFormatType,
    HlsOfflineEncryptedType,
    HlsOutputSelectionType,
    HlsProgramDateTimeType,
    HlsProgressiveWriteHlsManifestType,
    HlsSegmentControlType,
    HlsSegmentLengthControlType,
    HlsStreamInfResolutionType,
    HlsTargetDurationCompatibilityModeType,
    HlsTimedMetadataId3FrameType,
    ImscAccessibilitySubsType,
    ImscStylePassthroughType,
    InputDeblockFilterType,
    InputDenoiseFilterType,
    InputFilterEnableType,
    InputPolicyType,
    InputPsiControlType,
    InputRotateType,
    InputSampleRangeType,
    InputScanTypeType,
    InputTimecodeSourceType,
    JobPhaseType,
    JobStatusType,
    JobTemplateListByType,
    LanguageCodeType,
    M2tsAudioBufferModelType,
    M2tsAudioDurationType,
    M2tsBufferModelType,
    M2tsDataPtsControlType,
    M2tsEbpAudioIntervalType,
    M2tsEbpPlacementType,
    M2tsEsRateInPesType,
    M2tsForceTsVideoEbpOrderType,
    M2tsKlvMetadataType,
    M2tsNielsenId3Type,
    M2tsPcrControlType,
    M2tsRateModeType,
    M2tsScte35SourceType,
    M2tsSegmentationMarkersType,
    M2tsSegmentationStyleType,
    M3u8AudioDurationType,
    M3u8DataPtsControlType,
    M3u8NielsenId3Type,
    M3u8PcrControlType,
    M3u8Scte35SourceType,
    MotionImageInsertionModeType,
    MotionImagePlaybackType,
    MovClapAtomType,
    MovCslgAtomType,
    MovMpeg2FourCCControlType,
    MovPaddingControlType,
    MovReferenceType,
    Mp3RateControlModeType,
    Mp4CslgAtomType,
    Mp4FreeSpaceBoxType,
    Mp4MoovPlacementType,
    MpdAccessibilityCaptionHintsType,
    MpdAudioDurationType,
    MpdCaptionContainerTypeType,
    MpdKlvMetadataType,
    MpdManifestMetadataSignalingType,
    MpdScte35EsamType,
    MpdScte35SourceType,
    MpdTimedMetadataBoxVersionType,
    MpdTimedMetadataType,
    Mpeg2AdaptiveQuantizationType,
    Mpeg2CodecLevelType,
    Mpeg2CodecProfileType,
    Mpeg2DynamicSubGopType,
    Mpeg2FramerateControlType,
    Mpeg2FramerateConversionAlgorithmType,
    Mpeg2GopSizeUnitsType,
    Mpeg2InterlaceModeType,
    Mpeg2IntraDcPrecisionType,
    Mpeg2ParControlType,
    Mpeg2QualityTuningLevelType,
    Mpeg2RateControlModeType,
    Mpeg2ScanTypeConversionModeType,
    Mpeg2SceneChangeDetectType,
    Mpeg2SlowPalType,
    Mpeg2SpatialAdaptiveQuantizationType,
    Mpeg2SyntaxType,
    Mpeg2TelecineType,
    Mpeg2TemporalAdaptiveQuantizationType,
    MsSmoothAudioDeduplicationType,
    MsSmoothFragmentLengthControlType,
    MsSmoothManifestEncodingType,
    MxfAfdSignalingType,
    MxfProfileType,
    MxfXavcDurationModeType,
    NielsenActiveWatermarkProcessTypeType,
    NielsenSourceWatermarkStatusTypeType,
    NielsenUniqueTicPerAudioTrackTypeType,
    NoiseFilterPostTemporalSharpeningStrengthType,
    NoiseFilterPostTemporalSharpeningType,
    NoiseReducerFilterType,
    OrderType,
    OutputGroupTypeType,
    OutputSdtType,
    PadVideoType,
    PresetListByType,
    PricingPlanType,
    ProresChromaSamplingType,
    ProresCodecProfileType,
    ProresFramerateControlType,
    ProresFramerateConversionAlgorithmType,
    ProresInterlaceModeType,
    ProresParControlType,
    ProresScanTypeConversionModeType,
    ProresSlowPalType,
    ProresTelecineType,
    QueueListByType,
    QueueStatusType,
    RenewalTypeType,
    RequiredFlagType,
    ReservationPlanStatusType,
    RespondToAfdType,
    RuleTypeType,
    S3ObjectCannedAclType,
    S3ServerSideEncryptionTypeType,
    SampleRangeConversionType,
    ScalingBehaviorType,
    SccDestinationFramerateType,
    SimulateReservedQueueType,
    SrtStylePassthroughType,
    StatusUpdateIntervalType,
    TeletextPageTypeType,
    TimecodeBurninPositionType,
    TimecodeSourceType,
    TimedMetadataType,
    TtmlStylePassthroughType,
    TypeType,
    Vc3ClassType,
    Vc3FramerateControlType,
    Vc3FramerateConversionAlgorithmType,
    Vc3InterlaceModeType,
    Vc3ScanTypeConversionModeType,
    Vc3SlowPalType,
    Vc3TelecineType,
    VchipActionType,
    VideoCodecType,
    VideoTimecodeInsertionType,
    Vp8FramerateControlType,
    Vp8FramerateConversionAlgorithmType,
    Vp8ParControlType,
    Vp8QualityTuningLevelType,
    Vp9FramerateControlType,
    Vp9FramerateConversionAlgorithmType,
    Vp9ParControlType,
    Vp9QualityTuningLevelType,
    WatermarkingStrengthType,
    WavFormatType,
    WebvttAccessibilitySubsType,
    WebvttStylePassthroughType,
    Xavc4kIntraCbgProfileClassType,
    Xavc4kIntraVbrProfileClassType,
    Xavc4kProfileBitrateClassType,
    Xavc4kProfileCodecProfileType,
    Xavc4kProfileQualityTuningLevelType,
    XavcAdaptiveQuantizationType,
    XavcEntropyEncodingType,
    XavcFlickerAdaptiveQuantizationType,
    XavcFramerateControlType,
    XavcFramerateConversionAlgorithmType,
    XavcGopBReferenceType,
    XavcHdIntraCbgProfileClassType,
    XavcHdProfileBitrateClassType,
    XavcHdProfileQualityTuningLevelType,
    XavcHdProfileTelecineType,
    XavcInterlaceModeType,
    XavcProfileType,
    XavcSlowPalType,
    XavcSpatialAdaptiveQuantizationType,
    XavcTemporalAdaptiveQuantizationType,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict

__all__ = (
    "AacSettingsOutputTypeDef",
    "AacSettingsTypeDef",
    "Ac3SettingsOutputTypeDef",
    "Ac3SettingsTypeDef",
    "AccelerationSettingsOutputTypeDef",
    "AccelerationSettingsTypeDef",
    "AdvancedInputFilterSettingsOutputTypeDef",
    "AdvancedInputFilterSettingsTypeDef",
    "AiffSettingsOutputTypeDef",
    "AiffSettingsTypeDef",
    "AllowedRenditionSizeOutputTypeDef",
    "AllowedRenditionSizeTypeDef",
    "AncillarySourceSettingsOutputTypeDef",
    "AncillarySourceSettingsTypeDef",
    "AssociateCertificateRequestRequestTypeDef",
    "AudioChannelTaggingSettingsOutputTypeDef",
    "AudioChannelTaggingSettingsTypeDef",
    "Eac3AtmosSettingsOutputTypeDef",
    "Eac3SettingsOutputTypeDef",
    "Mp2SettingsOutputTypeDef",
    "Mp3SettingsOutputTypeDef",
    "OpusSettingsOutputTypeDef",
    "VorbisSettingsOutputTypeDef",
    "WavSettingsOutputTypeDef",
    "Eac3AtmosSettingsTypeDef",
    "Eac3SettingsTypeDef",
    "Mp2SettingsTypeDef",
    "Mp3SettingsTypeDef",
    "OpusSettingsTypeDef",
    "VorbisSettingsTypeDef",
    "WavSettingsTypeDef",
    "AudioNormalizationSettingsOutputTypeDef",
    "AudioNormalizationSettingsTypeDef",
    "AudioSelectorGroupOutputTypeDef",
    "AudioSelectorGroupTypeDef",
    "HlsRenditionGroupSettingsOutputTypeDef",
    "HlsRenditionGroupSettingsTypeDef",
    "ForceIncludeRenditionSizeOutputTypeDef",
    "MinBottomRenditionSizeOutputTypeDef",
    "MinTopRenditionSizeOutputTypeDef",
    "ForceIncludeRenditionSizeTypeDef",
    "MinBottomRenditionSizeTypeDef",
    "MinTopRenditionSizeTypeDef",
    "Av1QvbrSettingsOutputTypeDef",
    "Av1QvbrSettingsTypeDef",
    "AvailBlankingOutputTypeDef",
    "AvailBlankingTypeDef",
    "AvcIntraUhdSettingsOutputTypeDef",
    "AvcIntraUhdSettingsTypeDef",
    "BandwidthReductionFilterOutputTypeDef",
    "BandwidthReductionFilterTypeDef",
    "BurninDestinationSettingsOutputTypeDef",
    "BurninDestinationSettingsTypeDef",
    "CancelJobRequestRequestTypeDef",
    "DvbSubDestinationSettingsOutputTypeDef",
    "EmbeddedDestinationSettingsOutputTypeDef",
    "ImscDestinationSettingsOutputTypeDef",
    "SccDestinationSettingsOutputTypeDef",
    "SrtDestinationSettingsOutputTypeDef",
    "TeletextDestinationSettingsOutputTypeDef",
    "TtmlDestinationSettingsOutputTypeDef",
    "WebvttDestinationSettingsOutputTypeDef",
    "DvbSubDestinationSettingsTypeDef",
    "EmbeddedDestinationSettingsTypeDef",
    "ImscDestinationSettingsTypeDef",
    "SccDestinationSettingsTypeDef",
    "SrtDestinationSettingsTypeDef",
    "TeletextDestinationSettingsTypeDef",
    "TtmlDestinationSettingsTypeDef",
    "WebvttDestinationSettingsTypeDef",
    "CaptionSourceFramerateOutputTypeDef",
    "CaptionSourceFramerateTypeDef",
    "DvbSubSourceSettingsOutputTypeDef",
    "EmbeddedSourceSettingsOutputTypeDef",
    "TeletextSourceSettingsOutputTypeDef",
    "TrackSourceSettingsOutputTypeDef",
    "WebvttHlsSourceSettingsOutputTypeDef",
    "DvbSubSourceSettingsTypeDef",
    "EmbeddedSourceSettingsTypeDef",
    "TeletextSourceSettingsTypeDef",
    "TrackSourceSettingsTypeDef",
    "WebvttHlsSourceSettingsTypeDef",
    "OutputChannelMappingOutputTypeDef",
    "OutputChannelMappingTypeDef",
    "ClipLimitsOutputTypeDef",
    "ClipLimitsTypeDef",
    "CmafAdditionalManifestOutputTypeDef",
    "CmafAdditionalManifestTypeDef",
    "SpekeKeyProviderCmafOutputTypeDef",
    "StaticKeyProviderOutputTypeDef",
    "SpekeKeyProviderCmafTypeDef",
    "StaticKeyProviderTypeDef",
    "CmafImageBasedTrickPlaySettingsOutputTypeDef",
    "CmafImageBasedTrickPlaySettingsTypeDef",
    "CmfcSettingsOutputTypeDef",
    "CmfcSettingsTypeDef",
    "Hdr10MetadataOutputTypeDef",
    "Hdr10MetadataTypeDef",
    "F4vSettingsOutputTypeDef",
    "M3u8SettingsOutputTypeDef",
    "MovSettingsOutputTypeDef",
    "Mp4SettingsOutputTypeDef",
    "MpdSettingsOutputTypeDef",
    "F4vSettingsTypeDef",
    "M3u8SettingsTypeDef",
    "MovSettingsTypeDef",
    "Mp4SettingsTypeDef",
    "MpdSettingsTypeDef",
    "HopDestinationTypeDef",
    "ResponseMetadataTypeDef",
    "ReservationPlanSettingsTypeDef",
    "DashAdditionalManifestOutputTypeDef",
    "DashAdditionalManifestTypeDef",
    "SpekeKeyProviderOutputTypeDef",
    "SpekeKeyProviderTypeDef",
    "DashIsoImageBasedTrickPlaySettingsOutputTypeDef",
    "DashIsoImageBasedTrickPlaySettingsTypeDef",
    "DeinterlacerOutputTypeDef",
    "DeinterlacerTypeDef",
    "DeleteJobTemplateRequestRequestTypeDef",
    "DeletePresetRequestRequestTypeDef",
    "DeleteQueueRequestRequestTypeDef",
    "PaginatorConfigTypeDef",
    "DescribeEndpointsRequestRequestTypeDef",
    "EndpointTypeDef",
    "DisassociateCertificateRequestRequestTypeDef",
    "DolbyVisionLevel6MetadataOutputTypeDef",
    "DolbyVisionLevel6MetadataTypeDef",
    "DvbNitSettingsOutputTypeDef",
    "DvbNitSettingsTypeDef",
    "DvbSdtSettingsOutputTypeDef",
    "DvbSdtSettingsTypeDef",
    "DvbTdtSettingsOutputTypeDef",
    "DvbTdtSettingsTypeDef",
    "EsamManifestConfirmConditionNotificationOutputTypeDef",
    "EsamManifestConfirmConditionNotificationTypeDef",
    "EsamSignalProcessingNotificationOutputTypeDef",
    "EsamSignalProcessingNotificationTypeDef",
    "ExtendedDataServicesOutputTypeDef",
    "ExtendedDataServicesTypeDef",
    "FrameCaptureSettingsOutputTypeDef",
    "FrameCaptureSettingsTypeDef",
    "GetJobRequestRequestTypeDef",
    "GetJobTemplateRequestRequestTypeDef",
    "PolicyOutputTypeDef",
    "GetPresetRequestRequestTypeDef",
    "GetQueueRequestRequestTypeDef",
    "H264QvbrSettingsOutputTypeDef",
    "H264QvbrSettingsTypeDef",
    "H265QvbrSettingsOutputTypeDef",
    "H265QvbrSettingsTypeDef",
    "Hdr10PlusOutputTypeDef",
    "Hdr10PlusTypeDef",
    "HlsAdditionalManifestOutputTypeDef",
    "HlsAdditionalManifestTypeDef",
    "HlsCaptionLanguageMappingOutputTypeDef",
    "HlsCaptionLanguageMappingTypeDef",
    "HlsImageBasedTrickPlaySettingsOutputTypeDef",
    "HlsImageBasedTrickPlaySettingsTypeDef",
    "HlsSettingsOutputTypeDef",
    "HopDestinationOutputTypeDef",
    "Id3InsertionOutputTypeDef",
    "Id3InsertionTypeDef",
    "InsertableImageOutputTypeDef",
    "InsertableImageTypeDef",
    "InputClippingOutputTypeDef",
    "InputClippingTypeDef",
    "InputDecryptionSettingsOutputTypeDef",
    "InputDecryptionSettingsTypeDef",
    "InputVideoGeneratorOutputTypeDef",
    "RectangleOutputTypeDef",
    "RectangleTypeDef",
    "InputVideoGeneratorTypeDef",
    "JobMessagesTypeDef",
    "KantarWatermarkSettingsOutputTypeDef",
    "NielsenConfigurationOutputTypeDef",
    "NielsenNonLinearWatermarkSettingsOutputTypeDef",
    "TimecodeConfigOutputTypeDef",
    "KantarWatermarkSettingsTypeDef",
    "NielsenConfigurationTypeDef",
    "NielsenNonLinearWatermarkSettingsTypeDef",
    "TimecodeConfigTypeDef",
    "QueueTransitionTypeDef",
    "TimingTypeDef",
    "WarningGroupTypeDef",
    "ListJobTemplatesRequestRequestTypeDef",
    "ListJobsRequestRequestTypeDef",
    "ListPresetsRequestRequestTypeDef",
    "ListQueuesRequestRequestTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ResourceTagsTypeDef",
    "M2tsScte35EsamOutputTypeDef",
    "M2tsScte35EsamTypeDef",
    "MotionImageInsertionFramerateOutputTypeDef",
    "MotionImageInsertionOffsetOutputTypeDef",
    "MotionImageInsertionFramerateTypeDef",
    "MotionImageInsertionOffsetTypeDef",
    "Mpeg2SettingsOutputTypeDef",
    "Mpeg2SettingsTypeDef",
    "MsSmoothAdditionalManifestOutputTypeDef",
    "MsSmoothAdditionalManifestTypeDef",
    "MxfXavcProfileSettingsOutputTypeDef",
    "MxfXavcProfileSettingsTypeDef",
    "NexGuardFileMarkerSettingsOutputTypeDef",
    "NexGuardFileMarkerSettingsTypeDef",
    "NoiseReducerFilterSettingsOutputTypeDef",
    "NoiseReducerFilterSettingsTypeDef",
    "NoiseReducerSpatialFilterSettingsOutputTypeDef",
    "NoiseReducerTemporalFilterSettingsOutputTypeDef",
    "NoiseReducerSpatialFilterSettingsTypeDef",
    "NoiseReducerTemporalFilterSettingsTypeDef",
    "VideoDetailTypeDef",
    "PolicyTypeDef",
    "ProresSettingsOutputTypeDef",
    "ProresSettingsTypeDef",
    "ReservationPlanTypeDef",
    "S3DestinationAccessControlOutputTypeDef",
    "S3DestinationAccessControlTypeDef",
    "S3EncryptionSettingsOutputTypeDef",
    "S3EncryptionSettingsTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TimecodeBurninOutputTypeDef",
    "TimecodeBurninTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "Vc3SettingsOutputTypeDef",
    "Vc3SettingsTypeDef",
    "Vp8SettingsOutputTypeDef",
    "Vp9SettingsOutputTypeDef",
    "Vp8SettingsTypeDef",
    "Vp9SettingsTypeDef",
    "Xavc4kIntraCbgProfileSettingsOutputTypeDef",
    "Xavc4kIntraCbgProfileSettingsTypeDef",
    "Xavc4kIntraVbrProfileSettingsOutputTypeDef",
    "Xavc4kIntraVbrProfileSettingsTypeDef",
    "Xavc4kProfileSettingsOutputTypeDef",
    "Xavc4kProfileSettingsTypeDef",
    "XavcHdIntraCbgProfileSettingsOutputTypeDef",
    "XavcHdIntraCbgProfileSettingsTypeDef",
    "XavcHdProfileSettingsOutputTypeDef",
    "XavcHdProfileSettingsTypeDef",
    "AudioCodecSettingsOutputTypeDef",
    "AudioCodecSettingsTypeDef",
    "AutomatedAbrRuleOutputTypeDef",
    "AutomatedAbrRuleTypeDef",
    "Av1SettingsOutputTypeDef",
    "Av1SettingsTypeDef",
    "AvcIntraSettingsOutputTypeDef",
    "AvcIntraSettingsTypeDef",
    "CaptionDestinationSettingsOutputTypeDef",
    "CaptionDestinationSettingsTypeDef",
    "FileSourceSettingsOutputTypeDef",
    "FileSourceSettingsTypeDef",
    "ChannelMappingOutputTypeDef",
    "ChannelMappingTypeDef",
    "CmafEncryptionSettingsOutputTypeDef",
    "CmafEncryptionSettingsTypeDef",
    "ColorCorrectorOutputTypeDef",
    "VideoSelectorOutputTypeDef",
    "ColorCorrectorTypeDef",
    "VideoSelectorTypeDef",
    "CreateQueueRequestRequestTypeDef",
    "UpdateQueueRequestRequestTypeDef",
    "DashIsoEncryptionSettingsOutputTypeDef",
    "HlsEncryptionSettingsOutputTypeDef",
    "MsSmoothEncryptionSettingsOutputTypeDef",
    "DashIsoEncryptionSettingsTypeDef",
    "HlsEncryptionSettingsTypeDef",
    "MsSmoothEncryptionSettingsTypeDef",
    "DescribeEndpointsRequestDescribeEndpointsPaginateTypeDef",
    "ListJobTemplatesRequestListJobTemplatesPaginateTypeDef",
    "ListJobsRequestListJobsPaginateTypeDef",
    "ListPresetsRequestListPresetsPaginateTypeDef",
    "ListQueuesRequestListQueuesPaginateTypeDef",
    "DescribeEndpointsResponseTypeDef",
    "DolbyVisionOutputTypeDef",
    "DolbyVisionTypeDef",
    "EsamSettingsOutputTypeDef",
    "EsamSettingsTypeDef",
    "GetPolicyResponseTypeDef",
    "PutPolicyResponseTypeDef",
    "H264SettingsOutputTypeDef",
    "H264SettingsTypeDef",
    "H265SettingsOutputTypeDef",
    "H265SettingsTypeDef",
    "OutputSettingsOutputTypeDef",
    "TimedMetadataInsertionOutputTypeDef",
    "TimedMetadataInsertionTypeDef",
    "ImageInserterOutputTypeDef",
    "ImageInserterTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "M2tsSettingsOutputTypeDef",
    "M2tsSettingsTypeDef",
    "MotionImageInserterOutputTypeDef",
    "MotionImageInserterTypeDef",
    "MxfSettingsOutputTypeDef",
    "MxfSettingsTypeDef",
    "PartnerWatermarkingOutputTypeDef",
    "PartnerWatermarkingTypeDef",
    "NoiseReducerOutputTypeDef",
    "NoiseReducerTypeDef",
    "OutputDetailTypeDef",
    "PutPolicyRequestRequestTypeDef",
    "QueueTypeDef",
    "S3DestinationSettingsOutputTypeDef",
    "S3DestinationSettingsTypeDef",
    "XavcSettingsOutputTypeDef",
    "XavcSettingsTypeDef",
    "AutomatedAbrSettingsOutputTypeDef",
    "AutomatedAbrSettingsTypeDef",
    "CaptionDescriptionOutputTypeDef",
    "CaptionDescriptionPresetOutputTypeDef",
    "CaptionDescriptionPresetTypeDef",
    "CaptionSourceSettingsOutputTypeDef",
    "CaptionSourceSettingsTypeDef",
    "RemixSettingsOutputTypeDef",
    "RemixSettingsTypeDef",
    "ContainerSettingsOutputTypeDef",
    "ContainerSettingsTypeDef",
    "VideoPreprocessorOutputTypeDef",
    "VideoPreprocessorTypeDef",
    "OutputGroupDetailTypeDef",
    "CreateQueueResponseTypeDef",
    "GetQueueResponseTypeDef",
    "ListQueuesResponseTypeDef",
    "UpdateQueueResponseTypeDef",
    "DestinationSettingsOutputTypeDef",
    "DestinationSettingsTypeDef",
    "VideoCodecSettingsOutputTypeDef",
    "VideoCodecSettingsTypeDef",
    "AutomatedEncodingSettingsOutputTypeDef",
    "AutomatedEncodingSettingsTypeDef",
    "CaptionSelectorOutputTypeDef",
    "CaptionSelectorTypeDef",
    "AudioDescriptionOutputTypeDef",
    "AudioSelectorOutputTypeDef",
    "AudioDescriptionTypeDef",
    "AudioSelectorTypeDef",
    "CmafGroupSettingsOutputTypeDef",
    "DashIsoGroupSettingsOutputTypeDef",
    "FileGroupSettingsOutputTypeDef",
    "HlsGroupSettingsOutputTypeDef",
    "MsSmoothGroupSettingsOutputTypeDef",
    "CmafGroupSettingsTypeDef",
    "DashIsoGroupSettingsTypeDef",
    "FileGroupSettingsTypeDef",
    "HlsGroupSettingsTypeDef",
    "MsSmoothGroupSettingsTypeDef",
    "VideoDescriptionOutputTypeDef",
    "VideoDescriptionTypeDef",
    "InputOutputTypeDef",
    "InputTemplateOutputTypeDef",
    "InputTemplateTypeDef",
    "InputTypeDef",
    "OutputGroupSettingsOutputTypeDef",
    "OutputGroupSettingsTypeDef",
    "OutputTypeDef",
    "PresetSettingsOutputTypeDef",
    "PresetSettingsTypeDef",
    "OutputGroupOutputTypeDef",
    "OutputGroupTypeDef",
    "PresetTypeDef",
    "CreatePresetRequestRequestTypeDef",
    "UpdatePresetRequestRequestTypeDef",
    "JobSettingsOutputTypeDef",
    "JobTemplateSettingsOutputTypeDef",
    "JobSettingsTypeDef",
    "JobTemplateSettingsTypeDef",
    "CreatePresetResponseTypeDef",
    "GetPresetResponseTypeDef",
    "ListPresetsResponseTypeDef",
    "UpdatePresetResponseTypeDef",
    "JobTypeDef",
    "JobTemplateTypeDef",
    "CreateJobRequestRequestTypeDef",
    "CreateJobTemplateRequestRequestTypeDef",
    "UpdateJobTemplateRequestRequestTypeDef",
    "CreateJobResponseTypeDef",
    "GetJobResponseTypeDef",
    "ListJobsResponseTypeDef",
    "CreateJobTemplateResponseTypeDef",
    "GetJobTemplateResponseTypeDef",
    "ListJobTemplatesResponseTypeDef",
    "UpdateJobTemplateResponseTypeDef",
)

AacSettingsOutputTypeDef = TypedDict(
    "AacSettingsOutputTypeDef",
    {
        "AudioDescriptionBroadcasterMix": AacAudioDescriptionBroadcasterMixType,
        "Bitrate": int,
        "CodecProfile": AacCodecProfileType,
        "CodingMode": AacCodingModeType,
        "RateControlMode": AacRateControlModeType,
        "RawFormat": AacRawFormatType,
        "SampleRate": int,
        "Specification": AacSpecificationType,
        "VbrQuality": AacVbrQualityType,
    },
)

AacSettingsTypeDef = TypedDict(
    "AacSettingsTypeDef",
    {
        "AudioDescriptionBroadcasterMix": AacAudioDescriptionBroadcasterMixType,
        "Bitrate": int,
        "CodecProfile": AacCodecProfileType,
        "CodingMode": AacCodingModeType,
        "RateControlMode": AacRateControlModeType,
        "RawFormat": AacRawFormatType,
        "SampleRate": int,
        "Specification": AacSpecificationType,
        "VbrQuality": AacVbrQualityType,
    },
    total=False,
)

Ac3SettingsOutputTypeDef = TypedDict(
    "Ac3SettingsOutputTypeDef",
    {
        "Bitrate": int,
        "BitstreamMode": Ac3BitstreamModeType,
        "CodingMode": Ac3CodingModeType,
        "Dialnorm": int,
        "DynamicRangeCompressionLine": Ac3DynamicRangeCompressionLineType,
        "DynamicRangeCompressionProfile": Ac3DynamicRangeCompressionProfileType,
        "DynamicRangeCompressionRf": Ac3DynamicRangeCompressionRfType,
        "LfeFilter": Ac3LfeFilterType,
        "MetadataControl": Ac3MetadataControlType,
        "SampleRate": int,
    },
)

Ac3SettingsTypeDef = TypedDict(
    "Ac3SettingsTypeDef",
    {
        "Bitrate": int,
        "BitstreamMode": Ac3BitstreamModeType,
        "CodingMode": Ac3CodingModeType,
        "Dialnorm": int,
        "DynamicRangeCompressionLine": Ac3DynamicRangeCompressionLineType,
        "DynamicRangeCompressionProfile": Ac3DynamicRangeCompressionProfileType,
        "DynamicRangeCompressionRf": Ac3DynamicRangeCompressionRfType,
        "LfeFilter": Ac3LfeFilterType,
        "MetadataControl": Ac3MetadataControlType,
        "SampleRate": int,
    },
    total=False,
)

AccelerationSettingsOutputTypeDef = TypedDict(
    "AccelerationSettingsOutputTypeDef",
    {
        "Mode": AccelerationModeType,
    },
)

AccelerationSettingsTypeDef = TypedDict(
    "AccelerationSettingsTypeDef",
    {
        "Mode": AccelerationModeType,
    },
)

AdvancedInputFilterSettingsOutputTypeDef = TypedDict(
    "AdvancedInputFilterSettingsOutputTypeDef",
    {
        "AddTexture": AdvancedInputFilterAddTextureType,
        "Sharpening": AdvancedInputFilterSharpenType,
    },
)

AdvancedInputFilterSettingsTypeDef = TypedDict(
    "AdvancedInputFilterSettingsTypeDef",
    {
        "AddTexture": AdvancedInputFilterAddTextureType,
        "Sharpening": AdvancedInputFilterSharpenType,
    },
    total=False,
)

AiffSettingsOutputTypeDef = TypedDict(
    "AiffSettingsOutputTypeDef",
    {
        "BitDepth": int,
        "Channels": int,
        "SampleRate": int,
    },
)

AiffSettingsTypeDef = TypedDict(
    "AiffSettingsTypeDef",
    {
        "BitDepth": int,
        "Channels": int,
        "SampleRate": int,
    },
    total=False,
)

AllowedRenditionSizeOutputTypeDef = TypedDict(
    "AllowedRenditionSizeOutputTypeDef",
    {
        "Height": int,
        "Required": RequiredFlagType,
        "Width": int,
    },
)

AllowedRenditionSizeTypeDef = TypedDict(
    "AllowedRenditionSizeTypeDef",
    {
        "Height": int,
        "Required": RequiredFlagType,
        "Width": int,
    },
    total=False,
)

AncillarySourceSettingsOutputTypeDef = TypedDict(
    "AncillarySourceSettingsOutputTypeDef",
    {
        "Convert608To708": AncillaryConvert608To708Type,
        "SourceAncillaryChannelNumber": int,
        "TerminateCaptions": AncillaryTerminateCaptionsType,
    },
)

AncillarySourceSettingsTypeDef = TypedDict(
    "AncillarySourceSettingsTypeDef",
    {
        "Convert608To708": AncillaryConvert608To708Type,
        "SourceAncillaryChannelNumber": int,
        "TerminateCaptions": AncillaryTerminateCaptionsType,
    },
    total=False,
)

AssociateCertificateRequestRequestTypeDef = TypedDict(
    "AssociateCertificateRequestRequestTypeDef",
    {
        "Arn": str,
    },
)

AudioChannelTaggingSettingsOutputTypeDef = TypedDict(
    "AudioChannelTaggingSettingsOutputTypeDef",
    {
        "ChannelTag": AudioChannelTagType,
    },
)

AudioChannelTaggingSettingsTypeDef = TypedDict(
    "AudioChannelTaggingSettingsTypeDef",
    {
        "ChannelTag": AudioChannelTagType,
    },
    total=False,
)

Eac3AtmosSettingsOutputTypeDef = TypedDict(
    "Eac3AtmosSettingsOutputTypeDef",
    {
        "Bitrate": int,
        "BitstreamMode": Literal["COMPLETE_MAIN"],
        "CodingMode": Eac3AtmosCodingModeType,
        "DialogueIntelligence": Eac3AtmosDialogueIntelligenceType,
        "DownmixControl": Eac3AtmosDownmixControlType,
        "DynamicRangeCompressionLine": Eac3AtmosDynamicRangeCompressionLineType,
        "DynamicRangeCompressionRf": Eac3AtmosDynamicRangeCompressionRfType,
        "DynamicRangeControl": Eac3AtmosDynamicRangeControlType,
        "LoRoCenterMixLevel": float,
        "LoRoSurroundMixLevel": float,
        "LtRtCenterMixLevel": float,
        "LtRtSurroundMixLevel": float,
        "MeteringMode": Eac3AtmosMeteringModeType,
        "SampleRate": int,
        "SpeechThreshold": int,
        "StereoDownmix": Eac3AtmosStereoDownmixType,
        "SurroundExMode": Eac3AtmosSurroundExModeType,
    },
)

Eac3SettingsOutputTypeDef = TypedDict(
    "Eac3SettingsOutputTypeDef",
    {
        "AttenuationControl": Eac3AttenuationControlType,
        "Bitrate": int,
        "BitstreamMode": Eac3BitstreamModeType,
        "CodingMode": Eac3CodingModeType,
        "DcFilter": Eac3DcFilterType,
        "Dialnorm": int,
        "DynamicRangeCompressionLine": Eac3DynamicRangeCompressionLineType,
        "DynamicRangeCompressionRf": Eac3DynamicRangeCompressionRfType,
        "LfeControl": Eac3LfeControlType,
        "LfeFilter": Eac3LfeFilterType,
        "LoRoCenterMixLevel": float,
        "LoRoSurroundMixLevel": float,
        "LtRtCenterMixLevel": float,
        "LtRtSurroundMixLevel": float,
        "MetadataControl": Eac3MetadataControlType,
        "PassthroughControl": Eac3PassthroughControlType,
        "PhaseControl": Eac3PhaseControlType,
        "SampleRate": int,
        "StereoDownmix": Eac3StereoDownmixType,
        "SurroundExMode": Eac3SurroundExModeType,
        "SurroundMode": Eac3SurroundModeType,
    },
)

Mp2SettingsOutputTypeDef = TypedDict(
    "Mp2SettingsOutputTypeDef",
    {
        "Bitrate": int,
        "Channels": int,
        "SampleRate": int,
    },
)

Mp3SettingsOutputTypeDef = TypedDict(
    "Mp3SettingsOutputTypeDef",
    {
        "Bitrate": int,
        "Channels": int,
        "RateControlMode": Mp3RateControlModeType,
        "SampleRate": int,
        "VbrQuality": int,
    },
)

OpusSettingsOutputTypeDef = TypedDict(
    "OpusSettingsOutputTypeDef",
    {
        "Bitrate": int,
        "Channels": int,
        "SampleRate": int,
    },
)

VorbisSettingsOutputTypeDef = TypedDict(
    "VorbisSettingsOutputTypeDef",
    {
        "Channels": int,
        "SampleRate": int,
        "VbrQuality": int,
    },
)

WavSettingsOutputTypeDef = TypedDict(
    "WavSettingsOutputTypeDef",
    {
        "BitDepth": int,
        "Channels": int,
        "Format": WavFormatType,
        "SampleRate": int,
    },
)

Eac3AtmosSettingsTypeDef = TypedDict(
    "Eac3AtmosSettingsTypeDef",
    {
        "Bitrate": int,
        "BitstreamMode": Literal["COMPLETE_MAIN"],
        "CodingMode": Eac3AtmosCodingModeType,
        "DialogueIntelligence": Eac3AtmosDialogueIntelligenceType,
        "DownmixControl": Eac3AtmosDownmixControlType,
        "DynamicRangeCompressionLine": Eac3AtmosDynamicRangeCompressionLineType,
        "DynamicRangeCompressionRf": Eac3AtmosDynamicRangeCompressionRfType,
        "DynamicRangeControl": Eac3AtmosDynamicRangeControlType,
        "LoRoCenterMixLevel": float,
        "LoRoSurroundMixLevel": float,
        "LtRtCenterMixLevel": float,
        "LtRtSurroundMixLevel": float,
        "MeteringMode": Eac3AtmosMeteringModeType,
        "SampleRate": int,
        "SpeechThreshold": int,
        "StereoDownmix": Eac3AtmosStereoDownmixType,
        "SurroundExMode": Eac3AtmosSurroundExModeType,
    },
    total=False,
)

Eac3SettingsTypeDef = TypedDict(
    "Eac3SettingsTypeDef",
    {
        "AttenuationControl": Eac3AttenuationControlType,
        "Bitrate": int,
        "BitstreamMode": Eac3BitstreamModeType,
        "CodingMode": Eac3CodingModeType,
        "DcFilter": Eac3DcFilterType,
        "Dialnorm": int,
        "DynamicRangeCompressionLine": Eac3DynamicRangeCompressionLineType,
        "DynamicRangeCompressionRf": Eac3DynamicRangeCompressionRfType,
        "LfeControl": Eac3LfeControlType,
        "LfeFilter": Eac3LfeFilterType,
        "LoRoCenterMixLevel": float,
        "LoRoSurroundMixLevel": float,
        "LtRtCenterMixLevel": float,
        "LtRtSurroundMixLevel": float,
        "MetadataControl": Eac3MetadataControlType,
        "PassthroughControl": Eac3PassthroughControlType,
        "PhaseControl": Eac3PhaseControlType,
        "SampleRate": int,
        "StereoDownmix": Eac3StereoDownmixType,
        "SurroundExMode": Eac3SurroundExModeType,
        "SurroundMode": Eac3SurroundModeType,
    },
    total=False,
)

Mp2SettingsTypeDef = TypedDict(
    "Mp2SettingsTypeDef",
    {
        "Bitrate": int,
        "Channels": int,
        "SampleRate": int,
    },
    total=False,
)

Mp3SettingsTypeDef = TypedDict(
    "Mp3SettingsTypeDef",
    {
        "Bitrate": int,
        "Channels": int,
        "RateControlMode": Mp3RateControlModeType,
        "SampleRate": int,
        "VbrQuality": int,
    },
    total=False,
)

OpusSettingsTypeDef = TypedDict(
    "OpusSettingsTypeDef",
    {
        "Bitrate": int,
        "Channels": int,
        "SampleRate": int,
    },
    total=False,
)

VorbisSettingsTypeDef = TypedDict(
    "VorbisSettingsTypeDef",
    {
        "Channels": int,
        "SampleRate": int,
        "VbrQuality": int,
    },
    total=False,
)

WavSettingsTypeDef = TypedDict(
    "WavSettingsTypeDef",
    {
        "BitDepth": int,
        "Channels": int,
        "Format": WavFormatType,
        "SampleRate": int,
    },
    total=False,
)

AudioNormalizationSettingsOutputTypeDef = TypedDict(
    "AudioNormalizationSettingsOutputTypeDef",
    {
        "Algorithm": AudioNormalizationAlgorithmType,
        "AlgorithmControl": AudioNormalizationAlgorithmControlType,
        "CorrectionGateLevel": int,
        "LoudnessLogging": AudioNormalizationLoudnessLoggingType,
        "PeakCalculation": AudioNormalizationPeakCalculationType,
        "TargetLkfs": float,
        "TruePeakLimiterThreshold": float,
    },
)

AudioNormalizationSettingsTypeDef = TypedDict(
    "AudioNormalizationSettingsTypeDef",
    {
        "Algorithm": AudioNormalizationAlgorithmType,
        "AlgorithmControl": AudioNormalizationAlgorithmControlType,
        "CorrectionGateLevel": int,
        "LoudnessLogging": AudioNormalizationLoudnessLoggingType,
        "PeakCalculation": AudioNormalizationPeakCalculationType,
        "TargetLkfs": float,
        "TruePeakLimiterThreshold": float,
    },
    total=False,
)

AudioSelectorGroupOutputTypeDef = TypedDict(
    "AudioSelectorGroupOutputTypeDef",
    {
        "AudioSelectorNames": List[str],
    },
)

AudioSelectorGroupTypeDef = TypedDict(
    "AudioSelectorGroupTypeDef",
    {
        "AudioSelectorNames": Sequence[str],
    },
    total=False,
)

HlsRenditionGroupSettingsOutputTypeDef = TypedDict(
    "HlsRenditionGroupSettingsOutputTypeDef",
    {
        "RenditionGroupId": str,
        "RenditionLanguageCode": LanguageCodeType,
        "RenditionName": str,
    },
)

HlsRenditionGroupSettingsTypeDef = TypedDict(
    "HlsRenditionGroupSettingsTypeDef",
    {
        "RenditionGroupId": str,
        "RenditionLanguageCode": LanguageCodeType,
        "RenditionName": str,
    },
    total=False,
)

ForceIncludeRenditionSizeOutputTypeDef = TypedDict(
    "ForceIncludeRenditionSizeOutputTypeDef",
    {
        "Height": int,
        "Width": int,
    },
)

MinBottomRenditionSizeOutputTypeDef = TypedDict(
    "MinBottomRenditionSizeOutputTypeDef",
    {
        "Height": int,
        "Width": int,
    },
)

MinTopRenditionSizeOutputTypeDef = TypedDict(
    "MinTopRenditionSizeOutputTypeDef",
    {
        "Height": int,
        "Width": int,
    },
)

ForceIncludeRenditionSizeTypeDef = TypedDict(
    "ForceIncludeRenditionSizeTypeDef",
    {
        "Height": int,
        "Width": int,
    },
    total=False,
)

MinBottomRenditionSizeTypeDef = TypedDict(
    "MinBottomRenditionSizeTypeDef",
    {
        "Height": int,
        "Width": int,
    },
    total=False,
)

MinTopRenditionSizeTypeDef = TypedDict(
    "MinTopRenditionSizeTypeDef",
    {
        "Height": int,
        "Width": int,
    },
    total=False,
)

Av1QvbrSettingsOutputTypeDef = TypedDict(
    "Av1QvbrSettingsOutputTypeDef",
    {
        "QvbrQualityLevel": int,
        "QvbrQualityLevelFineTune": float,
    },
)

Av1QvbrSettingsTypeDef = TypedDict(
    "Av1QvbrSettingsTypeDef",
    {
        "QvbrQualityLevel": int,
        "QvbrQualityLevelFineTune": float,
    },
    total=False,
)

AvailBlankingOutputTypeDef = TypedDict(
    "AvailBlankingOutputTypeDef",
    {
        "AvailBlankingImage": str,
    },
)

AvailBlankingTypeDef = TypedDict(
    "AvailBlankingTypeDef",
    {
        "AvailBlankingImage": str,
    },
    total=False,
)

AvcIntraUhdSettingsOutputTypeDef = TypedDict(
    "AvcIntraUhdSettingsOutputTypeDef",
    {
        "QualityTuningLevel": AvcIntraUhdQualityTuningLevelType,
    },
)

AvcIntraUhdSettingsTypeDef = TypedDict(
    "AvcIntraUhdSettingsTypeDef",
    {
        "QualityTuningLevel": AvcIntraUhdQualityTuningLevelType,
    },
    total=False,
)

BandwidthReductionFilterOutputTypeDef = TypedDict(
    "BandwidthReductionFilterOutputTypeDef",
    {
        "Sharpening": BandwidthReductionFilterSharpeningType,
        "Strength": BandwidthReductionFilterStrengthType,
    },
)

BandwidthReductionFilterTypeDef = TypedDict(
    "BandwidthReductionFilterTypeDef",
    {
        "Sharpening": BandwidthReductionFilterSharpeningType,
        "Strength": BandwidthReductionFilterStrengthType,
    },
    total=False,
)

BurninDestinationSettingsOutputTypeDef = TypedDict(
    "BurninDestinationSettingsOutputTypeDef",
    {
        "Alignment": BurninSubtitleAlignmentType,
        "ApplyFontColor": BurninSubtitleApplyFontColorType,
        "BackgroundColor": BurninSubtitleBackgroundColorType,
        "BackgroundOpacity": int,
        "FallbackFont": BurninSubtitleFallbackFontType,
        "FontColor": BurninSubtitleFontColorType,
        "FontOpacity": int,
        "FontResolution": int,
        "FontScript": FontScriptType,
        "FontSize": int,
        "HexFontColor": str,
        "OutlineColor": BurninSubtitleOutlineColorType,
        "OutlineSize": int,
        "ShadowColor": BurninSubtitleShadowColorType,
        "ShadowOpacity": int,
        "ShadowXOffset": int,
        "ShadowYOffset": int,
        "StylePassthrough": BurnInSubtitleStylePassthroughType,
        "TeletextSpacing": BurninSubtitleTeletextSpacingType,
        "XPosition": int,
        "YPosition": int,
    },
)

BurninDestinationSettingsTypeDef = TypedDict(
    "BurninDestinationSettingsTypeDef",
    {
        "Alignment": BurninSubtitleAlignmentType,
        "ApplyFontColor": BurninSubtitleApplyFontColorType,
        "BackgroundColor": BurninSubtitleBackgroundColorType,
        "BackgroundOpacity": int,
        "FallbackFont": BurninSubtitleFallbackFontType,
        "FontColor": BurninSubtitleFontColorType,
        "FontOpacity": int,
        "FontResolution": int,
        "FontScript": FontScriptType,
        "FontSize": int,
        "HexFontColor": str,
        "OutlineColor": BurninSubtitleOutlineColorType,
        "OutlineSize": int,
        "ShadowColor": BurninSubtitleShadowColorType,
        "ShadowOpacity": int,
        "ShadowXOffset": int,
        "ShadowYOffset": int,
        "StylePassthrough": BurnInSubtitleStylePassthroughType,
        "TeletextSpacing": BurninSubtitleTeletextSpacingType,
        "XPosition": int,
        "YPosition": int,
    },
    total=False,
)

CancelJobRequestRequestTypeDef = TypedDict(
    "CancelJobRequestRequestTypeDef",
    {
        "Id": str,
    },
)

DvbSubDestinationSettingsOutputTypeDef = TypedDict(
    "DvbSubDestinationSettingsOutputTypeDef",
    {
        "Alignment": DvbSubtitleAlignmentType,
        "ApplyFontColor": DvbSubtitleApplyFontColorType,
        "BackgroundColor": DvbSubtitleBackgroundColorType,
        "BackgroundOpacity": int,
        "DdsHandling": DvbddsHandlingType,
        "DdsXCoordinate": int,
        "DdsYCoordinate": int,
        "FallbackFont": DvbSubSubtitleFallbackFontType,
        "FontColor": DvbSubtitleFontColorType,
        "FontOpacity": int,
        "FontResolution": int,
        "FontScript": FontScriptType,
        "FontSize": int,
        "Height": int,
        "HexFontColor": str,
        "OutlineColor": DvbSubtitleOutlineColorType,
        "OutlineSize": int,
        "ShadowColor": DvbSubtitleShadowColorType,
        "ShadowOpacity": int,
        "ShadowXOffset": int,
        "ShadowYOffset": int,
        "StylePassthrough": DvbSubtitleStylePassthroughType,
        "SubtitlingType": DvbSubtitlingTypeType,
        "TeletextSpacing": DvbSubtitleTeletextSpacingType,
        "Width": int,
        "XPosition": int,
        "YPosition": int,
    },
)

EmbeddedDestinationSettingsOutputTypeDef = TypedDict(
    "EmbeddedDestinationSettingsOutputTypeDef",
    {
        "Destination608ChannelNumber": int,
        "Destination708ServiceNumber": int,
    },
)

ImscDestinationSettingsOutputTypeDef = TypedDict(
    "ImscDestinationSettingsOutputTypeDef",
    {
        "Accessibility": ImscAccessibilitySubsType,
        "StylePassthrough": ImscStylePassthroughType,
    },
)

SccDestinationSettingsOutputTypeDef = TypedDict(
    "SccDestinationSettingsOutputTypeDef",
    {
        "Framerate": SccDestinationFramerateType,
    },
)

SrtDestinationSettingsOutputTypeDef = TypedDict(
    "SrtDestinationSettingsOutputTypeDef",
    {
        "StylePassthrough": SrtStylePassthroughType,
    },
)

TeletextDestinationSettingsOutputTypeDef = TypedDict(
    "TeletextDestinationSettingsOutputTypeDef",
    {
        "PageNumber": str,
        "PageTypes": List[TeletextPageTypeType],
    },
)

TtmlDestinationSettingsOutputTypeDef = TypedDict(
    "TtmlDestinationSettingsOutputTypeDef",
    {
        "StylePassthrough": TtmlStylePassthroughType,
    },
)

WebvttDestinationSettingsOutputTypeDef = TypedDict(
    "WebvttDestinationSettingsOutputTypeDef",
    {
        "Accessibility": WebvttAccessibilitySubsType,
        "StylePassthrough": WebvttStylePassthroughType,
    },
)

DvbSubDestinationSettingsTypeDef = TypedDict(
    "DvbSubDestinationSettingsTypeDef",
    {
        "Alignment": DvbSubtitleAlignmentType,
        "ApplyFontColor": DvbSubtitleApplyFontColorType,
        "BackgroundColor": DvbSubtitleBackgroundColorType,
        "BackgroundOpacity": int,
        "DdsHandling": DvbddsHandlingType,
        "DdsXCoordinate": int,
        "DdsYCoordinate": int,
        "FallbackFont": DvbSubSubtitleFallbackFontType,
        "FontColor": DvbSubtitleFontColorType,
        "FontOpacity": int,
        "FontResolution": int,
        "FontScript": FontScriptType,
        "FontSize": int,
        "Height": int,
        "HexFontColor": str,
        "OutlineColor": DvbSubtitleOutlineColorType,
        "OutlineSize": int,
        "ShadowColor": DvbSubtitleShadowColorType,
        "ShadowOpacity": int,
        "ShadowXOffset": int,
        "ShadowYOffset": int,
        "StylePassthrough": DvbSubtitleStylePassthroughType,
        "SubtitlingType": DvbSubtitlingTypeType,
        "TeletextSpacing": DvbSubtitleTeletextSpacingType,
        "Width": int,
        "XPosition": int,
        "YPosition": int,
    },
    total=False,
)

EmbeddedDestinationSettingsTypeDef = TypedDict(
    "EmbeddedDestinationSettingsTypeDef",
    {
        "Destination608ChannelNumber": int,
        "Destination708ServiceNumber": int,
    },
    total=False,
)

ImscDestinationSettingsTypeDef = TypedDict(
    "ImscDestinationSettingsTypeDef",
    {
        "Accessibility": ImscAccessibilitySubsType,
        "StylePassthrough": ImscStylePassthroughType,
    },
    total=False,
)

SccDestinationSettingsTypeDef = TypedDict(
    "SccDestinationSettingsTypeDef",
    {
        "Framerate": SccDestinationFramerateType,
    },
    total=False,
)

SrtDestinationSettingsTypeDef = TypedDict(
    "SrtDestinationSettingsTypeDef",
    {
        "StylePassthrough": SrtStylePassthroughType,
    },
    total=False,
)

TeletextDestinationSettingsTypeDef = TypedDict(
    "TeletextDestinationSettingsTypeDef",
    {
        "PageNumber": str,
        "PageTypes": Sequence[TeletextPageTypeType],
    },
    total=False,
)

TtmlDestinationSettingsTypeDef = TypedDict(
    "TtmlDestinationSettingsTypeDef",
    {
        "StylePassthrough": TtmlStylePassthroughType,
    },
    total=False,
)

WebvttDestinationSettingsTypeDef = TypedDict(
    "WebvttDestinationSettingsTypeDef",
    {
        "Accessibility": WebvttAccessibilitySubsType,
        "StylePassthrough": WebvttStylePassthroughType,
    },
    total=False,
)

CaptionSourceFramerateOutputTypeDef = TypedDict(
    "CaptionSourceFramerateOutputTypeDef",
    {
        "FramerateDenominator": int,
        "FramerateNumerator": int,
    },
)

CaptionSourceFramerateTypeDef = TypedDict(
    "CaptionSourceFramerateTypeDef",
    {
        "FramerateDenominator": int,
        "FramerateNumerator": int,
    },
    total=False,
)

DvbSubSourceSettingsOutputTypeDef = TypedDict(
    "DvbSubSourceSettingsOutputTypeDef",
    {
        "Pid": int,
    },
)

EmbeddedSourceSettingsOutputTypeDef = TypedDict(
    "EmbeddedSourceSettingsOutputTypeDef",
    {
        "Convert608To708": EmbeddedConvert608To708Type,
        "Source608ChannelNumber": int,
        "Source608TrackNumber": int,
        "TerminateCaptions": EmbeddedTerminateCaptionsType,
    },
)

TeletextSourceSettingsOutputTypeDef = TypedDict(
    "TeletextSourceSettingsOutputTypeDef",
    {
        "PageNumber": str,
    },
)

TrackSourceSettingsOutputTypeDef = TypedDict(
    "TrackSourceSettingsOutputTypeDef",
    {
        "TrackNumber": int,
    },
)

WebvttHlsSourceSettingsOutputTypeDef = TypedDict(
    "WebvttHlsSourceSettingsOutputTypeDef",
    {
        "RenditionGroupId": str,
        "RenditionLanguageCode": LanguageCodeType,
        "RenditionName": str,
    },
)

DvbSubSourceSettingsTypeDef = TypedDict(
    "DvbSubSourceSettingsTypeDef",
    {
        "Pid": int,
    },
    total=False,
)

EmbeddedSourceSettingsTypeDef = TypedDict(
    "EmbeddedSourceSettingsTypeDef",
    {
        "Convert608To708": EmbeddedConvert608To708Type,
        "Source608ChannelNumber": int,
        "Source608TrackNumber": int,
        "TerminateCaptions": EmbeddedTerminateCaptionsType,
    },
    total=False,
)

TeletextSourceSettingsTypeDef = TypedDict(
    "TeletextSourceSettingsTypeDef",
    {
        "PageNumber": str,
    },
    total=False,
)

TrackSourceSettingsTypeDef = TypedDict(
    "TrackSourceSettingsTypeDef",
    {
        "TrackNumber": int,
    },
    total=False,
)

WebvttHlsSourceSettingsTypeDef = TypedDict(
    "WebvttHlsSourceSettingsTypeDef",
    {
        "RenditionGroupId": str,
        "RenditionLanguageCode": LanguageCodeType,
        "RenditionName": str,
    },
    total=False,
)

OutputChannelMappingOutputTypeDef = TypedDict(
    "OutputChannelMappingOutputTypeDef",
    {
        "InputChannels": List[int],
        "InputChannelsFineTune": List[float],
    },
)

OutputChannelMappingTypeDef = TypedDict(
    "OutputChannelMappingTypeDef",
    {
        "InputChannels": Sequence[int],
        "InputChannelsFineTune": Sequence[float],
    },
    total=False,
)

ClipLimitsOutputTypeDef = TypedDict(
    "ClipLimitsOutputTypeDef",
    {
        "MaximumRGBTolerance": int,
        "MaximumYUV": int,
        "MinimumRGBTolerance": int,
        "MinimumYUV": int,
    },
)

ClipLimitsTypeDef = TypedDict(
    "ClipLimitsTypeDef",
    {
        "MaximumRGBTolerance": int,
        "MaximumYUV": int,
        "MinimumRGBTolerance": int,
        "MinimumYUV": int,
    },
    total=False,
)

CmafAdditionalManifestOutputTypeDef = TypedDict(
    "CmafAdditionalManifestOutputTypeDef",
    {
        "ManifestNameModifier": str,
        "SelectedOutputs": List[str],
    },
)

CmafAdditionalManifestTypeDef = TypedDict(
    "CmafAdditionalManifestTypeDef",
    {
        "ManifestNameModifier": str,
        "SelectedOutputs": Sequence[str],
    },
    total=False,
)

SpekeKeyProviderCmafOutputTypeDef = TypedDict(
    "SpekeKeyProviderCmafOutputTypeDef",
    {
        "CertificateArn": str,
        "DashSignaledSystemIds": List[str],
        "HlsSignaledSystemIds": List[str],
        "ResourceId": str,
        "Url": str,
    },
)

StaticKeyProviderOutputTypeDef = TypedDict(
    "StaticKeyProviderOutputTypeDef",
    {
        "KeyFormat": str,
        "KeyFormatVersions": str,
        "StaticKeyValue": str,
        "Url": str,
    },
)

SpekeKeyProviderCmafTypeDef = TypedDict(
    "SpekeKeyProviderCmafTypeDef",
    {
        "CertificateArn": str,
        "DashSignaledSystemIds": Sequence[str],
        "HlsSignaledSystemIds": Sequence[str],
        "ResourceId": str,
        "Url": str,
    },
    total=False,
)

StaticKeyProviderTypeDef = TypedDict(
    "StaticKeyProviderTypeDef",
    {
        "KeyFormat": str,
        "KeyFormatVersions": str,
        "StaticKeyValue": str,
        "Url": str,
    },
    total=False,
)

CmafImageBasedTrickPlaySettingsOutputTypeDef = TypedDict(
    "CmafImageBasedTrickPlaySettingsOutputTypeDef",
    {
        "IntervalCadence": CmafIntervalCadenceType,
        "ThumbnailHeight": int,
        "ThumbnailInterval": float,
        "ThumbnailWidth": int,
        "TileHeight": int,
        "TileWidth": int,
    },
)

CmafImageBasedTrickPlaySettingsTypeDef = TypedDict(
    "CmafImageBasedTrickPlaySettingsTypeDef",
    {
        "IntervalCadence": CmafIntervalCadenceType,
        "ThumbnailHeight": int,
        "ThumbnailInterval": float,
        "ThumbnailWidth": int,
        "TileHeight": int,
        "TileWidth": int,
    },
    total=False,
)

CmfcSettingsOutputTypeDef = TypedDict(
    "CmfcSettingsOutputTypeDef",
    {
        "AudioDuration": CmfcAudioDurationType,
        "AudioGroupId": str,
        "AudioRenditionSets": str,
        "AudioTrackType": CmfcAudioTrackTypeType,
        "DescriptiveVideoServiceFlag": CmfcDescriptiveVideoServiceFlagType,
        "IFrameOnlyManifest": CmfcIFrameOnlyManifestType,
        "KlvMetadata": CmfcKlvMetadataType,
        "ManifestMetadataSignaling": CmfcManifestMetadataSignalingType,
        "Scte35Esam": CmfcScte35EsamType,
        "Scte35Source": CmfcScte35SourceType,
        "TimedMetadata": CmfcTimedMetadataType,
        "TimedMetadataBoxVersion": CmfcTimedMetadataBoxVersionType,
        "TimedMetadataSchemeIdUri": str,
        "TimedMetadataValue": str,
    },
)

CmfcSettingsTypeDef = TypedDict(
    "CmfcSettingsTypeDef",
    {
        "AudioDuration": CmfcAudioDurationType,
        "AudioGroupId": str,
        "AudioRenditionSets": str,
        "AudioTrackType": CmfcAudioTrackTypeType,
        "DescriptiveVideoServiceFlag": CmfcDescriptiveVideoServiceFlagType,
        "IFrameOnlyManifest": CmfcIFrameOnlyManifestType,
        "KlvMetadata": CmfcKlvMetadataType,
        "ManifestMetadataSignaling": CmfcManifestMetadataSignalingType,
        "Scte35Esam": CmfcScte35EsamType,
        "Scte35Source": CmfcScte35SourceType,
        "TimedMetadata": CmfcTimedMetadataType,
        "TimedMetadataBoxVersion": CmfcTimedMetadataBoxVersionType,
        "TimedMetadataSchemeIdUri": str,
        "TimedMetadataValue": str,
    },
    total=False,
)

Hdr10MetadataOutputTypeDef = TypedDict(
    "Hdr10MetadataOutputTypeDef",
    {
        "BluePrimaryX": int,
        "BluePrimaryY": int,
        "GreenPrimaryX": int,
        "GreenPrimaryY": int,
        "MaxContentLightLevel": int,
        "MaxFrameAverageLightLevel": int,
        "MaxLuminance": int,
        "MinLuminance": int,
        "RedPrimaryX": int,
        "RedPrimaryY": int,
        "WhitePointX": int,
        "WhitePointY": int,
    },
)

Hdr10MetadataTypeDef = TypedDict(
    "Hdr10MetadataTypeDef",
    {
        "BluePrimaryX": int,
        "BluePrimaryY": int,
        "GreenPrimaryX": int,
        "GreenPrimaryY": int,
        "MaxContentLightLevel": int,
        "MaxFrameAverageLightLevel": int,
        "MaxLuminance": int,
        "MinLuminance": int,
        "RedPrimaryX": int,
        "RedPrimaryY": int,
        "WhitePointX": int,
        "WhitePointY": int,
    },
    total=False,
)

F4vSettingsOutputTypeDef = TypedDict(
    "F4vSettingsOutputTypeDef",
    {
        "MoovPlacement": F4vMoovPlacementType,
    },
)

M3u8SettingsOutputTypeDef = TypedDict(
    "M3u8SettingsOutputTypeDef",
    {
        "AudioDuration": M3u8AudioDurationType,
        "AudioFramesPerPes": int,
        "AudioPids": List[int],
        "DataPTSControl": M3u8DataPtsControlType,
        "MaxPcrInterval": int,
        "NielsenId3": M3u8NielsenId3Type,
        "PatInterval": int,
        "PcrControl": M3u8PcrControlType,
        "PcrPid": int,
        "PmtInterval": int,
        "PmtPid": int,
        "PrivateMetadataPid": int,
        "ProgramNumber": int,
        "Scte35Pid": int,
        "Scte35Source": M3u8Scte35SourceType,
        "TimedMetadata": TimedMetadataType,
        "TimedMetadataPid": int,
        "TransportStreamId": int,
        "VideoPid": int,
    },
)

MovSettingsOutputTypeDef = TypedDict(
    "MovSettingsOutputTypeDef",
    {
        "ClapAtom": MovClapAtomType,
        "CslgAtom": MovCslgAtomType,
        "Mpeg2FourCCControl": MovMpeg2FourCCControlType,
        "PaddingControl": MovPaddingControlType,
        "Reference": MovReferenceType,
    },
)

Mp4SettingsOutputTypeDef = TypedDict(
    "Mp4SettingsOutputTypeDef",
    {
        "AudioDuration": CmfcAudioDurationType,
        "CslgAtom": Mp4CslgAtomType,
        "CttsVersion": int,
        "FreeSpaceBox": Mp4FreeSpaceBoxType,
        "MoovPlacement": Mp4MoovPlacementType,
        "Mp4MajorBrand": str,
    },
)

MpdSettingsOutputTypeDef = TypedDict(
    "MpdSettingsOutputTypeDef",
    {
        "AccessibilityCaptionHints": MpdAccessibilityCaptionHintsType,
        "AudioDuration": MpdAudioDurationType,
        "CaptionContainerType": MpdCaptionContainerTypeType,
        "KlvMetadata": MpdKlvMetadataType,
        "ManifestMetadataSignaling": MpdManifestMetadataSignalingType,
        "Scte35Esam": MpdScte35EsamType,
        "Scte35Source": MpdScte35SourceType,
        "TimedMetadata": MpdTimedMetadataType,
        "TimedMetadataBoxVersion": MpdTimedMetadataBoxVersionType,
        "TimedMetadataSchemeIdUri": str,
        "TimedMetadataValue": str,
    },
)

F4vSettingsTypeDef = TypedDict(
    "F4vSettingsTypeDef",
    {
        "MoovPlacement": F4vMoovPlacementType,
    },
    total=False,
)

M3u8SettingsTypeDef = TypedDict(
    "M3u8SettingsTypeDef",
    {
        "AudioDuration": M3u8AudioDurationType,
        "AudioFramesPerPes": int,
        "AudioPids": Sequence[int],
        "DataPTSControl": M3u8DataPtsControlType,
        "MaxPcrInterval": int,
        "NielsenId3": M3u8NielsenId3Type,
        "PatInterval": int,
        "PcrControl": M3u8PcrControlType,
        "PcrPid": int,
        "PmtInterval": int,
        "PmtPid": int,
        "PrivateMetadataPid": int,
        "ProgramNumber": int,
        "Scte35Pid": int,
        "Scte35Source": M3u8Scte35SourceType,
        "TimedMetadata": TimedMetadataType,
        "TimedMetadataPid": int,
        "TransportStreamId": int,
        "VideoPid": int,
    },
    total=False,
)

MovSettingsTypeDef = TypedDict(
    "MovSettingsTypeDef",
    {
        "ClapAtom": MovClapAtomType,
        "CslgAtom": MovCslgAtomType,
        "Mpeg2FourCCControl": MovMpeg2FourCCControlType,
        "PaddingControl": MovPaddingControlType,
        "Reference": MovReferenceType,
    },
    total=False,
)

Mp4SettingsTypeDef = TypedDict(
    "Mp4SettingsTypeDef",
    {
        "AudioDuration": CmfcAudioDurationType,
        "CslgAtom": Mp4CslgAtomType,
        "CttsVersion": int,
        "FreeSpaceBox": Mp4FreeSpaceBoxType,
        "MoovPlacement": Mp4MoovPlacementType,
        "Mp4MajorBrand": str,
    },
    total=False,
)

MpdSettingsTypeDef = TypedDict(
    "MpdSettingsTypeDef",
    {
        "AccessibilityCaptionHints": MpdAccessibilityCaptionHintsType,
        "AudioDuration": MpdAudioDurationType,
        "CaptionContainerType": MpdCaptionContainerTypeType,
        "KlvMetadata": MpdKlvMetadataType,
        "ManifestMetadataSignaling": MpdManifestMetadataSignalingType,
        "Scte35Esam": MpdScte35EsamType,
        "Scte35Source": MpdScte35SourceType,
        "TimedMetadata": MpdTimedMetadataType,
        "TimedMetadataBoxVersion": MpdTimedMetadataBoxVersionType,
        "TimedMetadataSchemeIdUri": str,
        "TimedMetadataValue": str,
    },
    total=False,
)

HopDestinationTypeDef = TypedDict(
    "HopDestinationTypeDef",
    {
        "Priority": int,
        "Queue": str,
        "WaitMinutes": int,
    },
    total=False,
)

ResponseMetadataTypeDef = TypedDict(
    "ResponseMetadataTypeDef",
    {
        "RequestId": str,
        "HostId": str,
        "HTTPStatusCode": int,
        "HTTPHeaders": Dict[str, str],
        "RetryAttempts": int,
    },
)

ReservationPlanSettingsTypeDef = TypedDict(
    "ReservationPlanSettingsTypeDef",
    {
        "Commitment": Literal["ONE_YEAR"],
        "RenewalType": RenewalTypeType,
        "ReservedSlots": int,
    },
)

DashAdditionalManifestOutputTypeDef = TypedDict(
    "DashAdditionalManifestOutputTypeDef",
    {
        "ManifestNameModifier": str,
        "SelectedOutputs": List[str],
    },
)

DashAdditionalManifestTypeDef = TypedDict(
    "DashAdditionalManifestTypeDef",
    {
        "ManifestNameModifier": str,
        "SelectedOutputs": Sequence[str],
    },
    total=False,
)

SpekeKeyProviderOutputTypeDef = TypedDict(
    "SpekeKeyProviderOutputTypeDef",
    {
        "CertificateArn": str,
        "ResourceId": str,
        "SystemIds": List[str],
        "Url": str,
    },
)

SpekeKeyProviderTypeDef = TypedDict(
    "SpekeKeyProviderTypeDef",
    {
        "CertificateArn": str,
        "ResourceId": str,
        "SystemIds": Sequence[str],
        "Url": str,
    },
    total=False,
)

DashIsoImageBasedTrickPlaySettingsOutputTypeDef = TypedDict(
    "DashIsoImageBasedTrickPlaySettingsOutputTypeDef",
    {
        "IntervalCadence": DashIsoIntervalCadenceType,
        "ThumbnailHeight": int,
        "ThumbnailInterval": float,
        "ThumbnailWidth": int,
        "TileHeight": int,
        "TileWidth": int,
    },
)

DashIsoImageBasedTrickPlaySettingsTypeDef = TypedDict(
    "DashIsoImageBasedTrickPlaySettingsTypeDef",
    {
        "IntervalCadence": DashIsoIntervalCadenceType,
        "ThumbnailHeight": int,
        "ThumbnailInterval": float,
        "ThumbnailWidth": int,
        "TileHeight": int,
        "TileWidth": int,
    },
    total=False,
)

DeinterlacerOutputTypeDef = TypedDict(
    "DeinterlacerOutputTypeDef",
    {
        "Algorithm": DeinterlaceAlgorithmType,
        "Control": DeinterlacerControlType,
        "Mode": DeinterlacerModeType,
    },
)

DeinterlacerTypeDef = TypedDict(
    "DeinterlacerTypeDef",
    {
        "Algorithm": DeinterlaceAlgorithmType,
        "Control": DeinterlacerControlType,
        "Mode": DeinterlacerModeType,
    },
    total=False,
)

DeleteJobTemplateRequestRequestTypeDef = TypedDict(
    "DeleteJobTemplateRequestRequestTypeDef",
    {
        "Name": str,
    },
)

DeletePresetRequestRequestTypeDef = TypedDict(
    "DeletePresetRequestRequestTypeDef",
    {
        "Name": str,
    },
)

DeleteQueueRequestRequestTypeDef = TypedDict(
    "DeleteQueueRequestRequestTypeDef",
    {
        "Name": str,
    },
)

PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef",
    {
        "MaxItems": int,
        "PageSize": int,
        "StartingToken": str,
    },
    total=False,
)

DescribeEndpointsRequestRequestTypeDef = TypedDict(
    "DescribeEndpointsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "Mode": DescribeEndpointsModeType,
        "NextToken": str,
    },
    total=False,
)

EndpointTypeDef = TypedDict(
    "EndpointTypeDef",
    {
        "Url": str,
    },
)

DisassociateCertificateRequestRequestTypeDef = TypedDict(
    "DisassociateCertificateRequestRequestTypeDef",
    {
        "Arn": str,
    },
)

DolbyVisionLevel6MetadataOutputTypeDef = TypedDict(
    "DolbyVisionLevel6MetadataOutputTypeDef",
    {
        "MaxCll": int,
        "MaxFall": int,
    },
)

DolbyVisionLevel6MetadataTypeDef = TypedDict(
    "DolbyVisionLevel6MetadataTypeDef",
    {
        "MaxCll": int,
        "MaxFall": int,
    },
    total=False,
)

DvbNitSettingsOutputTypeDef = TypedDict(
    "DvbNitSettingsOutputTypeDef",
    {
        "NetworkId": int,
        "NetworkName": str,
        "NitInterval": int,
    },
)

DvbNitSettingsTypeDef = TypedDict(
    "DvbNitSettingsTypeDef",
    {
        "NetworkId": int,
        "NetworkName": str,
        "NitInterval": int,
    },
    total=False,
)

DvbSdtSettingsOutputTypeDef = TypedDict(
    "DvbSdtSettingsOutputTypeDef",
    {
        "OutputSdt": OutputSdtType,
        "SdtInterval": int,
        "ServiceName": str,
        "ServiceProviderName": str,
    },
)

DvbSdtSettingsTypeDef = TypedDict(
    "DvbSdtSettingsTypeDef",
    {
        "OutputSdt": OutputSdtType,
        "SdtInterval": int,
        "ServiceName": str,
        "ServiceProviderName": str,
    },
    total=False,
)

DvbTdtSettingsOutputTypeDef = TypedDict(
    "DvbTdtSettingsOutputTypeDef",
    {
        "TdtInterval": int,
    },
)

DvbTdtSettingsTypeDef = TypedDict(
    "DvbTdtSettingsTypeDef",
    {
        "TdtInterval": int,
    },
    total=False,
)

EsamManifestConfirmConditionNotificationOutputTypeDef = TypedDict(
    "EsamManifestConfirmConditionNotificationOutputTypeDef",
    {
        "MccXml": str,
    },
)

EsamManifestConfirmConditionNotificationTypeDef = TypedDict(
    "EsamManifestConfirmConditionNotificationTypeDef",
    {
        "MccXml": str,
    },
    total=False,
)

EsamSignalProcessingNotificationOutputTypeDef = TypedDict(
    "EsamSignalProcessingNotificationOutputTypeDef",
    {
        "SccXml": str,
    },
)

EsamSignalProcessingNotificationTypeDef = TypedDict(
    "EsamSignalProcessingNotificationTypeDef",
    {
        "SccXml": str,
    },
    total=False,
)

ExtendedDataServicesOutputTypeDef = TypedDict(
    "ExtendedDataServicesOutputTypeDef",
    {
        "CopyProtectionAction": CopyProtectionActionType,
        "VchipAction": VchipActionType,
    },
)

ExtendedDataServicesTypeDef = TypedDict(
    "ExtendedDataServicesTypeDef",
    {
        "CopyProtectionAction": CopyProtectionActionType,
        "VchipAction": VchipActionType,
    },
    total=False,
)

FrameCaptureSettingsOutputTypeDef = TypedDict(
    "FrameCaptureSettingsOutputTypeDef",
    {
        "FramerateDenominator": int,
        "FramerateNumerator": int,
        "MaxCaptures": int,
        "Quality": int,
    },
)

FrameCaptureSettingsTypeDef = TypedDict(
    "FrameCaptureSettingsTypeDef",
    {
        "FramerateDenominator": int,
        "FramerateNumerator": int,
        "MaxCaptures": int,
        "Quality": int,
    },
    total=False,
)

GetJobRequestRequestTypeDef = TypedDict(
    "GetJobRequestRequestTypeDef",
    {
        "Id": str,
    },
)

GetJobTemplateRequestRequestTypeDef = TypedDict(
    "GetJobTemplateRequestRequestTypeDef",
    {
        "Name": str,
    },
)

PolicyOutputTypeDef = TypedDict(
    "PolicyOutputTypeDef",
    {
        "HttpInputs": InputPolicyType,
        "HttpsInputs": InputPolicyType,
        "S3Inputs": InputPolicyType,
    },
)

GetPresetRequestRequestTypeDef = TypedDict(
    "GetPresetRequestRequestTypeDef",
    {
        "Name": str,
    },
)

GetQueueRequestRequestTypeDef = TypedDict(
    "GetQueueRequestRequestTypeDef",
    {
        "Name": str,
    },
)

H264QvbrSettingsOutputTypeDef = TypedDict(
    "H264QvbrSettingsOutputTypeDef",
    {
        "MaxAverageBitrate": int,
        "QvbrQualityLevel": int,
        "QvbrQualityLevelFineTune": float,
    },
)

H264QvbrSettingsTypeDef = TypedDict(
    "H264QvbrSettingsTypeDef",
    {
        "MaxAverageBitrate": int,
        "QvbrQualityLevel": int,
        "QvbrQualityLevelFineTune": float,
    },
    total=False,
)

H265QvbrSettingsOutputTypeDef = TypedDict(
    "H265QvbrSettingsOutputTypeDef",
    {
        "MaxAverageBitrate": int,
        "QvbrQualityLevel": int,
        "QvbrQualityLevelFineTune": float,
    },
)

H265QvbrSettingsTypeDef = TypedDict(
    "H265QvbrSettingsTypeDef",
    {
        "MaxAverageBitrate": int,
        "QvbrQualityLevel": int,
        "QvbrQualityLevelFineTune": float,
    },
    total=False,
)

Hdr10PlusOutputTypeDef = TypedDict(
    "Hdr10PlusOutputTypeDef",
    {
        "MasteringMonitorNits": int,
        "TargetMonitorNits": int,
    },
)

Hdr10PlusTypeDef = TypedDict(
    "Hdr10PlusTypeDef",
    {
        "MasteringMonitorNits": int,
        "TargetMonitorNits": int,
    },
    total=False,
)

HlsAdditionalManifestOutputTypeDef = TypedDict(
    "HlsAdditionalManifestOutputTypeDef",
    {
        "ManifestNameModifier": str,
        "SelectedOutputs": List[str],
    },
)

HlsAdditionalManifestTypeDef = TypedDict(
    "HlsAdditionalManifestTypeDef",
    {
        "ManifestNameModifier": str,
        "SelectedOutputs": Sequence[str],
    },
    total=False,
)

HlsCaptionLanguageMappingOutputTypeDef = TypedDict(
    "HlsCaptionLanguageMappingOutputTypeDef",
    {
        "CaptionChannel": int,
        "CustomLanguageCode": str,
        "LanguageCode": LanguageCodeType,
        "LanguageDescription": str,
    },
)

HlsCaptionLanguageMappingTypeDef = TypedDict(
    "HlsCaptionLanguageMappingTypeDef",
    {
        "CaptionChannel": int,
        "CustomLanguageCode": str,
        "LanguageCode": LanguageCodeType,
        "LanguageDescription": str,
    },
    total=False,
)

HlsImageBasedTrickPlaySettingsOutputTypeDef = TypedDict(
    "HlsImageBasedTrickPlaySettingsOutputTypeDef",
    {
        "IntervalCadence": HlsIntervalCadenceType,
        "ThumbnailHeight": int,
        "ThumbnailInterval": float,
        "ThumbnailWidth": int,
        "TileHeight": int,
        "TileWidth": int,
    },
)

HlsImageBasedTrickPlaySettingsTypeDef = TypedDict(
    "HlsImageBasedTrickPlaySettingsTypeDef",
    {
        "IntervalCadence": HlsIntervalCadenceType,
        "ThumbnailHeight": int,
        "ThumbnailInterval": float,
        "ThumbnailWidth": int,
        "TileHeight": int,
        "TileWidth": int,
    },
    total=False,
)

HlsSettingsOutputTypeDef = TypedDict(
    "HlsSettingsOutputTypeDef",
    {
        "AudioGroupId": str,
        "AudioOnlyContainer": HlsAudioOnlyContainerType,
        "AudioRenditionSets": str,
        "AudioTrackType": HlsAudioTrackTypeType,
        "DescriptiveVideoServiceFlag": HlsDescriptiveVideoServiceFlagType,
        "IFrameOnlyManifest": HlsIFrameOnlyManifestType,
        "SegmentModifier": str,
    },
)

HopDestinationOutputTypeDef = TypedDict(
    "HopDestinationOutputTypeDef",
    {
        "Priority": int,
        "Queue": str,
        "WaitMinutes": int,
    },
)

Id3InsertionOutputTypeDef = TypedDict(
    "Id3InsertionOutputTypeDef",
    {
        "Id3": str,
        "Timecode": str,
    },
)

Id3InsertionTypeDef = TypedDict(
    "Id3InsertionTypeDef",
    {
        "Id3": str,
        "Timecode": str,
    },
    total=False,
)

InsertableImageOutputTypeDef = TypedDict(
    "InsertableImageOutputTypeDef",
    {
        "Duration": int,
        "FadeIn": int,
        "FadeOut": int,
        "Height": int,
        "ImageInserterInput": str,
        "ImageX": int,
        "ImageY": int,
        "Layer": int,
        "Opacity": int,
        "StartTime": str,
        "Width": int,
    },
)

InsertableImageTypeDef = TypedDict(
    "InsertableImageTypeDef",
    {
        "Duration": int,
        "FadeIn": int,
        "FadeOut": int,
        "Height": int,
        "ImageInserterInput": str,
        "ImageX": int,
        "ImageY": int,
        "Layer": int,
        "Opacity": int,
        "StartTime": str,
        "Width": int,
    },
    total=False,
)

InputClippingOutputTypeDef = TypedDict(
    "InputClippingOutputTypeDef",
    {
        "EndTimecode": str,
        "StartTimecode": str,
    },
)

InputClippingTypeDef = TypedDict(
    "InputClippingTypeDef",
    {
        "EndTimecode": str,
        "StartTimecode": str,
    },
    total=False,
)

InputDecryptionSettingsOutputTypeDef = TypedDict(
    "InputDecryptionSettingsOutputTypeDef",
    {
        "DecryptionMode": DecryptionModeType,
        "EncryptedDecryptionKey": str,
        "InitializationVector": str,
        "KmsKeyRegion": str,
    },
)

InputDecryptionSettingsTypeDef = TypedDict(
    "InputDecryptionSettingsTypeDef",
    {
        "DecryptionMode": DecryptionModeType,
        "EncryptedDecryptionKey": str,
        "InitializationVector": str,
        "KmsKeyRegion": str,
    },
    total=False,
)

InputVideoGeneratorOutputTypeDef = TypedDict(
    "InputVideoGeneratorOutputTypeDef",
    {
        "Duration": int,
    },
)

RectangleOutputTypeDef = TypedDict(
    "RectangleOutputTypeDef",
    {
        "Height": int,
        "Width": int,
        "X": int,
        "Y": int,
    },
)

RectangleTypeDef = TypedDict(
    "RectangleTypeDef",
    {
        "Height": int,
        "Width": int,
        "X": int,
        "Y": int,
    },
    total=False,
)

InputVideoGeneratorTypeDef = TypedDict(
    "InputVideoGeneratorTypeDef",
    {
        "Duration": int,
    },
    total=False,
)

JobMessagesTypeDef = TypedDict(
    "JobMessagesTypeDef",
    {
        "Info": List[str],
        "Warning": List[str],
    },
)

KantarWatermarkSettingsOutputTypeDef = TypedDict(
    "KantarWatermarkSettingsOutputTypeDef",
    {
        "ChannelName": str,
        "ContentReference": str,
        "CredentialsSecretName": str,
        "FileOffset": float,
        "KantarLicenseId": int,
        "KantarServerUrl": str,
        "LogDestination": str,
        "Metadata3": str,
        "Metadata4": str,
        "Metadata5": str,
        "Metadata6": str,
        "Metadata7": str,
        "Metadata8": str,
    },
)

NielsenConfigurationOutputTypeDef = TypedDict(
    "NielsenConfigurationOutputTypeDef",
    {
        "BreakoutCode": int,
        "DistributorId": str,
    },
)

NielsenNonLinearWatermarkSettingsOutputTypeDef = TypedDict(
    "NielsenNonLinearWatermarkSettingsOutputTypeDef",
    {
        "ActiveWatermarkProcess": NielsenActiveWatermarkProcessTypeType,
        "AdiFilename": str,
        "AssetId": str,
        "AssetName": str,
        "CbetSourceId": str,
        "EpisodeId": str,
        "MetadataDestination": str,
        "SourceId": int,
        "SourceWatermarkStatus": NielsenSourceWatermarkStatusTypeType,
        "TicServerUrl": str,
        "UniqueTicPerAudioTrack": NielsenUniqueTicPerAudioTrackTypeType,
    },
)

TimecodeConfigOutputTypeDef = TypedDict(
    "TimecodeConfigOutputTypeDef",
    {
        "Anchor": str,
        "Source": TimecodeSourceType,
        "Start": str,
        "TimestampOffset": str,
    },
)

KantarWatermarkSettingsTypeDef = TypedDict(
    "KantarWatermarkSettingsTypeDef",
    {
        "ChannelName": str,
        "ContentReference": str,
        "CredentialsSecretName": str,
        "FileOffset": float,
        "KantarLicenseId": int,
        "KantarServerUrl": str,
        "LogDestination": str,
        "Metadata3": str,
        "Metadata4": str,
        "Metadata5": str,
        "Metadata6": str,
        "Metadata7": str,
        "Metadata8": str,
    },
    total=False,
)

NielsenConfigurationTypeDef = TypedDict(
    "NielsenConfigurationTypeDef",
    {
        "BreakoutCode": int,
        "DistributorId": str,
    },
    total=False,
)

NielsenNonLinearWatermarkSettingsTypeDef = TypedDict(
    "NielsenNonLinearWatermarkSettingsTypeDef",
    {
        "ActiveWatermarkProcess": NielsenActiveWatermarkProcessTypeType,
        "AdiFilename": str,
        "AssetId": str,
        "AssetName": str,
        "CbetSourceId": str,
        "EpisodeId": str,
        "MetadataDestination": str,
        "SourceId": int,
        "SourceWatermarkStatus": NielsenSourceWatermarkStatusTypeType,
        "TicServerUrl": str,
        "UniqueTicPerAudioTrack": NielsenUniqueTicPerAudioTrackTypeType,
    },
    total=False,
)

TimecodeConfigTypeDef = TypedDict(
    "TimecodeConfigTypeDef",
    {
        "Anchor": str,
        "Source": TimecodeSourceType,
        "Start": str,
        "TimestampOffset": str,
    },
    total=False,
)

QueueTransitionTypeDef = TypedDict(
    "QueueTransitionTypeDef",
    {
        "DestinationQueue": str,
        "SourceQueue": str,
        "Timestamp": datetime,
    },
)

TimingTypeDef = TypedDict(
    "TimingTypeDef",
    {
        "FinishTime": datetime,
        "StartTime": datetime,
        "SubmitTime": datetime,
    },
)

WarningGroupTypeDef = TypedDict(
    "WarningGroupTypeDef",
    {
        "Code": int,
        "Count": int,
    },
)

ListJobTemplatesRequestRequestTypeDef = TypedDict(
    "ListJobTemplatesRequestRequestTypeDef",
    {
        "Category": str,
        "ListBy": JobTemplateListByType,
        "MaxResults": int,
        "NextToken": str,
        "Order": OrderType,
    },
    total=False,
)

ListJobsRequestRequestTypeDef = TypedDict(
    "ListJobsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
        "Order": OrderType,
        "Queue": str,
        "Status": JobStatusType,
    },
    total=False,
)

ListPresetsRequestRequestTypeDef = TypedDict(
    "ListPresetsRequestRequestTypeDef",
    {
        "Category": str,
        "ListBy": PresetListByType,
        "MaxResults": int,
        "NextToken": str,
        "Order": OrderType,
    },
    total=False,
)

ListQueuesRequestRequestTypeDef = TypedDict(
    "ListQueuesRequestRequestTypeDef",
    {
        "ListBy": QueueListByType,
        "MaxResults": int,
        "NextToken": str,
        "Order": OrderType,
    },
    total=False,
)

ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "Arn": str,
    },
)

ResourceTagsTypeDef = TypedDict(
    "ResourceTagsTypeDef",
    {
        "Arn": str,
        "Tags": Dict[str, str],
    },
)

M2tsScte35EsamOutputTypeDef = TypedDict(
    "M2tsScte35EsamOutputTypeDef",
    {
        "Scte35EsamPid": int,
    },
)

M2tsScte35EsamTypeDef = TypedDict(
    "M2tsScte35EsamTypeDef",
    {
        "Scte35EsamPid": int,
    },
    total=False,
)

MotionImageInsertionFramerateOutputTypeDef = TypedDict(
    "MotionImageInsertionFramerateOutputTypeDef",
    {
        "FramerateDenominator": int,
        "FramerateNumerator": int,
    },
)

MotionImageInsertionOffsetOutputTypeDef = TypedDict(
    "MotionImageInsertionOffsetOutputTypeDef",
    {
        "ImageX": int,
        "ImageY": int,
    },
)

MotionImageInsertionFramerateTypeDef = TypedDict(
    "MotionImageInsertionFramerateTypeDef",
    {
        "FramerateDenominator": int,
        "FramerateNumerator": int,
    },
    total=False,
)

MotionImageInsertionOffsetTypeDef = TypedDict(
    "MotionImageInsertionOffsetTypeDef",
    {
        "ImageX": int,
        "ImageY": int,
    },
    total=False,
)

Mpeg2SettingsOutputTypeDef = TypedDict(
    "Mpeg2SettingsOutputTypeDef",
    {
        "AdaptiveQuantization": Mpeg2AdaptiveQuantizationType,
        "Bitrate": int,
        "CodecLevel": Mpeg2CodecLevelType,
        "CodecProfile": Mpeg2CodecProfileType,
        "DynamicSubGop": Mpeg2DynamicSubGopType,
        "FramerateControl": Mpeg2FramerateControlType,
        "FramerateConversionAlgorithm": Mpeg2FramerateConversionAlgorithmType,
        "FramerateDenominator": int,
        "FramerateNumerator": int,
        "GopClosedCadence": int,
        "GopSize": float,
        "GopSizeUnits": Mpeg2GopSizeUnitsType,
        "HrdBufferFinalFillPercentage": int,
        "HrdBufferInitialFillPercentage": int,
        "HrdBufferSize": int,
        "InterlaceMode": Mpeg2InterlaceModeType,
        "IntraDcPrecision": Mpeg2IntraDcPrecisionType,
        "MaxBitrate": int,
        "MinIInterval": int,
        "NumberBFramesBetweenReferenceFrames": int,
        "ParControl": Mpeg2ParControlType,
        "ParDenominator": int,
        "ParNumerator": int,
        "QualityTuningLevel": Mpeg2QualityTuningLevelType,
        "RateControlMode": Mpeg2RateControlModeType,
        "ScanTypeConversionMode": Mpeg2ScanTypeConversionModeType,
        "SceneChangeDetect": Mpeg2SceneChangeDetectType,
        "SlowPal": Mpeg2SlowPalType,
        "Softness": int,
        "SpatialAdaptiveQuantization": Mpeg2SpatialAdaptiveQuantizationType,
        "Syntax": Mpeg2SyntaxType,
        "Telecine": Mpeg2TelecineType,
        "TemporalAdaptiveQuantization": Mpeg2TemporalAdaptiveQuantizationType,
    },
)

Mpeg2SettingsTypeDef = TypedDict(
    "Mpeg2SettingsTypeDef",
    {
        "AdaptiveQuantization": Mpeg2AdaptiveQuantizationType,
        "Bitrate": int,
        "CodecLevel": Mpeg2CodecLevelType,
        "CodecProfile": Mpeg2CodecProfileType,
        "DynamicSubGop": Mpeg2DynamicSubGopType,
        "FramerateControl": Mpeg2FramerateControlType,
        "FramerateConversionAlgorithm": Mpeg2FramerateConversionAlgorithmType,
        "FramerateDenominator": int,
        "FramerateNumerator": int,
        "GopClosedCadence": int,
        "GopSize": float,
        "GopSizeUnits": Mpeg2GopSizeUnitsType,
        "HrdBufferFinalFillPercentage": int,
        "HrdBufferInitialFillPercentage": int,
        "HrdBufferSize": int,
        "InterlaceMode": Mpeg2InterlaceModeType,
        "IntraDcPrecision": Mpeg2IntraDcPrecisionType,
        "MaxBitrate": int,
        "MinIInterval": int,
        "NumberBFramesBetweenReferenceFrames": int,
        "ParControl": Mpeg2ParControlType,
        "ParDenominator": int,
        "ParNumerator": int,
        "QualityTuningLevel": Mpeg2QualityTuningLevelType,
        "RateControlMode": Mpeg2RateControlModeType,
        "ScanTypeConversionMode": Mpeg2ScanTypeConversionModeType,
        "SceneChangeDetect": Mpeg2SceneChangeDetectType,
        "SlowPal": Mpeg2SlowPalType,
        "Softness": int,
        "SpatialAdaptiveQuantization": Mpeg2SpatialAdaptiveQuantizationType,
        "Syntax": Mpeg2SyntaxType,
        "Telecine": Mpeg2TelecineType,
        "TemporalAdaptiveQuantization": Mpeg2TemporalAdaptiveQuantizationType,
    },
    total=False,
)

MsSmoothAdditionalManifestOutputTypeDef = TypedDict(
    "MsSmoothAdditionalManifestOutputTypeDef",
    {
        "ManifestNameModifier": str,
        "SelectedOutputs": List[str],
    },
)

MsSmoothAdditionalManifestTypeDef = TypedDict(
    "MsSmoothAdditionalManifestTypeDef",
    {
        "ManifestNameModifier": str,
        "SelectedOutputs": Sequence[str],
    },
    total=False,
)

MxfXavcProfileSettingsOutputTypeDef = TypedDict(
    "MxfXavcProfileSettingsOutputTypeDef",
    {
        "DurationMode": MxfXavcDurationModeType,
        "MaxAncDataSize": int,
    },
)

MxfXavcProfileSettingsTypeDef = TypedDict(
    "MxfXavcProfileSettingsTypeDef",
    {
        "DurationMode": MxfXavcDurationModeType,
        "MaxAncDataSize": int,
    },
    total=False,
)

NexGuardFileMarkerSettingsOutputTypeDef = TypedDict(
    "NexGuardFileMarkerSettingsOutputTypeDef",
    {
        "License": str,
        "Payload": int,
        "Preset": str,
        "Strength": WatermarkingStrengthType,
    },
)

NexGuardFileMarkerSettingsTypeDef = TypedDict(
    "NexGuardFileMarkerSettingsTypeDef",
    {
        "License": str,
        "Payload": int,
        "Preset": str,
        "Strength": WatermarkingStrengthType,
    },
    total=False,
)

NoiseReducerFilterSettingsOutputTypeDef = TypedDict(
    "NoiseReducerFilterSettingsOutputTypeDef",
    {
        "Strength": int,
    },
)

NoiseReducerFilterSettingsTypeDef = TypedDict(
    "NoiseReducerFilterSettingsTypeDef",
    {
        "Strength": int,
    },
    total=False,
)

NoiseReducerSpatialFilterSettingsOutputTypeDef = TypedDict(
    "NoiseReducerSpatialFilterSettingsOutputTypeDef",
    {
        "PostFilterSharpenStrength": int,
        "Speed": int,
        "Strength": int,
    },
)

NoiseReducerTemporalFilterSettingsOutputTypeDef = TypedDict(
    "NoiseReducerTemporalFilterSettingsOutputTypeDef",
    {
        "AggressiveMode": int,
        "PostTemporalSharpening": NoiseFilterPostTemporalSharpeningType,
        "PostTemporalSharpeningStrength": NoiseFilterPostTemporalSharpeningStrengthType,
        "Speed": int,
        "Strength": int,
    },
)

NoiseReducerSpatialFilterSettingsTypeDef = TypedDict(
    "NoiseReducerSpatialFilterSettingsTypeDef",
    {
        "PostFilterSharpenStrength": int,
        "Speed": int,
        "Strength": int,
    },
    total=False,
)

NoiseReducerTemporalFilterSettingsTypeDef = TypedDict(
    "NoiseReducerTemporalFilterSettingsTypeDef",
    {
        "AggressiveMode": int,
        "PostTemporalSharpening": NoiseFilterPostTemporalSharpeningType,
        "PostTemporalSharpeningStrength": NoiseFilterPostTemporalSharpeningStrengthType,
        "Speed": int,
        "Strength": int,
    },
    total=False,
)

VideoDetailTypeDef = TypedDict(
    "VideoDetailTypeDef",
    {
        "HeightInPx": int,
        "WidthInPx": int,
    },
)

PolicyTypeDef = TypedDict(
    "PolicyTypeDef",
    {
        "HttpInputs": InputPolicyType,
        "HttpsInputs": InputPolicyType,
        "S3Inputs": InputPolicyType,
    },
    total=False,
)

ProresSettingsOutputTypeDef = TypedDict(
    "ProresSettingsOutputTypeDef",
    {
        "ChromaSampling": ProresChromaSamplingType,
        "CodecProfile": ProresCodecProfileType,
        "FramerateControl": ProresFramerateControlType,
        "FramerateConversionAlgorithm": ProresFramerateConversionAlgorithmType,
        "FramerateDenominator": int,
        "FramerateNumerator": int,
        "InterlaceMode": ProresInterlaceModeType,
        "ParControl": ProresParControlType,
        "ParDenominator": int,
        "ParNumerator": int,
        "ScanTypeConversionMode": ProresScanTypeConversionModeType,
        "SlowPal": ProresSlowPalType,
        "Telecine": ProresTelecineType,
    },
)

ProresSettingsTypeDef = TypedDict(
    "ProresSettingsTypeDef",
    {
        "ChromaSampling": ProresChromaSamplingType,
        "CodecProfile": ProresCodecProfileType,
        "FramerateControl": ProresFramerateControlType,
        "FramerateConversionAlgorithm": ProresFramerateConversionAlgorithmType,
        "FramerateDenominator": int,
        "FramerateNumerator": int,
        "InterlaceMode": ProresInterlaceModeType,
        "ParControl": ProresParControlType,
        "ParDenominator": int,
        "ParNumerator": int,
        "ScanTypeConversionMode": ProresScanTypeConversionModeType,
        "SlowPal": ProresSlowPalType,
        "Telecine": ProresTelecineType,
    },
    total=False,
)

ReservationPlanTypeDef = TypedDict(
    "ReservationPlanTypeDef",
    {
        "Commitment": Literal["ONE_YEAR"],
        "ExpiresAt": datetime,
        "PurchasedAt": datetime,
        "RenewalType": RenewalTypeType,
        "ReservedSlots": int,
        "Status": ReservationPlanStatusType,
    },
)

S3DestinationAccessControlOutputTypeDef = TypedDict(
    "S3DestinationAccessControlOutputTypeDef",
    {
        "CannedAcl": S3ObjectCannedAclType,
    },
)

S3DestinationAccessControlTypeDef = TypedDict(
    "S3DestinationAccessControlTypeDef",
    {
        "CannedAcl": S3ObjectCannedAclType,
    },
    total=False,
)

S3EncryptionSettingsOutputTypeDef = TypedDict(
    "S3EncryptionSettingsOutputTypeDef",
    {
        "EncryptionType": S3ServerSideEncryptionTypeType,
        "KmsEncryptionContext": str,
        "KmsKeyArn": str,
    },
)

S3EncryptionSettingsTypeDef = TypedDict(
    "S3EncryptionSettingsTypeDef",
    {
        "EncryptionType": S3ServerSideEncryptionTypeType,
        "KmsEncryptionContext": str,
        "KmsKeyArn": str,
    },
    total=False,
)

TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "Arn": str,
        "Tags": Mapping[str, str],
    },
)

TimecodeBurninOutputTypeDef = TypedDict(
    "TimecodeBurninOutputTypeDef",
    {
        "FontSize": int,
        "Position": TimecodeBurninPositionType,
        "Prefix": str,
    },
)

TimecodeBurninTypeDef = TypedDict(
    "TimecodeBurninTypeDef",
    {
        "FontSize": int,
        "Position": TimecodeBurninPositionType,
        "Prefix": str,
    },
    total=False,
)

_RequiredUntagResourceRequestRequestTypeDef = TypedDict(
    "_RequiredUntagResourceRequestRequestTypeDef",
    {
        "Arn": str,
    },
)
_OptionalUntagResourceRequestRequestTypeDef = TypedDict(
    "_OptionalUntagResourceRequestRequestTypeDef",
    {
        "TagKeys": Sequence[str],
    },
    total=False,
)

class UntagResourceRequestRequestTypeDef(
    _RequiredUntagResourceRequestRequestTypeDef, _OptionalUntagResourceRequestRequestTypeDef
):
    pass

Vc3SettingsOutputTypeDef = TypedDict(
    "Vc3SettingsOutputTypeDef",
    {
        "FramerateControl": Vc3FramerateControlType,
        "FramerateConversionAlgorithm": Vc3FramerateConversionAlgorithmType,
        "FramerateDenominator": int,
        "FramerateNumerator": int,
        "InterlaceMode": Vc3InterlaceModeType,
        "ScanTypeConversionMode": Vc3ScanTypeConversionModeType,
        "SlowPal": Vc3SlowPalType,
        "Telecine": Vc3TelecineType,
        "Vc3Class": Vc3ClassType,
    },
)

Vc3SettingsTypeDef = TypedDict(
    "Vc3SettingsTypeDef",
    {
        "FramerateControl": Vc3FramerateControlType,
        "FramerateConversionAlgorithm": Vc3FramerateConversionAlgorithmType,
        "FramerateDenominator": int,
        "FramerateNumerator": int,
        "InterlaceMode": Vc3InterlaceModeType,
        "ScanTypeConversionMode": Vc3ScanTypeConversionModeType,
        "SlowPal": Vc3SlowPalType,
        "Telecine": Vc3TelecineType,
        "Vc3Class": Vc3ClassType,
    },
    total=False,
)

Vp8SettingsOutputTypeDef = TypedDict(
    "Vp8SettingsOutputTypeDef",
    {
        "Bitrate": int,
        "FramerateControl": Vp8FramerateControlType,
        "FramerateConversionAlgorithm": Vp8FramerateConversionAlgorithmType,
        "FramerateDenominator": int,
        "FramerateNumerator": int,
        "GopSize": float,
        "HrdBufferSize": int,
        "MaxBitrate": int,
        "ParControl": Vp8ParControlType,
        "ParDenominator": int,
        "ParNumerator": int,
        "QualityTuningLevel": Vp8QualityTuningLevelType,
        "RateControlMode": Literal["VBR"],
    },
)

Vp9SettingsOutputTypeDef = TypedDict(
    "Vp9SettingsOutputTypeDef",
    {
        "Bitrate": int,
        "FramerateControl": Vp9FramerateControlType,
        "FramerateConversionAlgorithm": Vp9FramerateConversionAlgorithmType,
        "FramerateDenominator": int,
        "FramerateNumerator": int,
        "GopSize": float,
        "HrdBufferSize": int,
        "MaxBitrate": int,
        "ParControl": Vp9ParControlType,
        "ParDenominator": int,
        "ParNumerator": int,
        "QualityTuningLevel": Vp9QualityTuningLevelType,
        "RateControlMode": Literal["VBR"],
    },
)

Vp8SettingsTypeDef = TypedDict(
    "Vp8SettingsTypeDef",
    {
        "Bitrate": int,
        "FramerateControl": Vp8FramerateControlType,
        "FramerateConversionAlgorithm": Vp8FramerateConversionAlgorithmType,
        "FramerateDenominator": int,
        "FramerateNumerator": int,
        "GopSize": float,
        "HrdBufferSize": int,
        "MaxBitrate": int,
        "ParControl": Vp8ParControlType,
        "ParDenominator": int,
        "ParNumerator": int,
        "QualityTuningLevel": Vp8QualityTuningLevelType,
        "RateControlMode": Literal["VBR"],
    },
    total=False,
)

Vp9SettingsTypeDef = TypedDict(
    "Vp9SettingsTypeDef",
    {
        "Bitrate": int,
        "FramerateControl": Vp9FramerateControlType,
        "FramerateConversionAlgorithm": Vp9FramerateConversionAlgorithmType,
        "FramerateDenominator": int,
        "FramerateNumerator": int,
        "GopSize": float,
        "HrdBufferSize": int,
        "MaxBitrate": int,
        "ParControl": Vp9ParControlType,
        "ParDenominator": int,
        "ParNumerator": int,
        "QualityTuningLevel": Vp9QualityTuningLevelType,
        "RateControlMode": Literal["VBR"],
    },
    total=False,
)

Xavc4kIntraCbgProfileSettingsOutputTypeDef = TypedDict(
    "Xavc4kIntraCbgProfileSettingsOutputTypeDef",
    {
        "XavcClass": Xavc4kIntraCbgProfileClassType,
    },
)

Xavc4kIntraCbgProfileSettingsTypeDef = TypedDict(
    "Xavc4kIntraCbgProfileSettingsTypeDef",
    {
        "XavcClass": Xavc4kIntraCbgProfileClassType,
    },
    total=False,
)

Xavc4kIntraVbrProfileSettingsOutputTypeDef = TypedDict(
    "Xavc4kIntraVbrProfileSettingsOutputTypeDef",
    {
        "XavcClass": Xavc4kIntraVbrProfileClassType,
    },
)

Xavc4kIntraVbrProfileSettingsTypeDef = TypedDict(
    "Xavc4kIntraVbrProfileSettingsTypeDef",
    {
        "XavcClass": Xavc4kIntraVbrProfileClassType,
    },
    total=False,
)

Xavc4kProfileSettingsOutputTypeDef = TypedDict(
    "Xavc4kProfileSettingsOutputTypeDef",
    {
        "BitrateClass": Xavc4kProfileBitrateClassType,
        "CodecProfile": Xavc4kProfileCodecProfileType,
        "FlickerAdaptiveQuantization": XavcFlickerAdaptiveQuantizationType,
        "GopBReference": XavcGopBReferenceType,
        "GopClosedCadence": int,
        "HrdBufferSize": int,
        "QualityTuningLevel": Xavc4kProfileQualityTuningLevelType,
        "Slices": int,
    },
)

Xavc4kProfileSettingsTypeDef = TypedDict(
    "Xavc4kProfileSettingsTypeDef",
    {
        "BitrateClass": Xavc4kProfileBitrateClassType,
        "CodecProfile": Xavc4kProfileCodecProfileType,
        "FlickerAdaptiveQuantization": XavcFlickerAdaptiveQuantizationType,
        "GopBReference": XavcGopBReferenceType,
        "GopClosedCadence": int,
        "HrdBufferSize": int,
        "QualityTuningLevel": Xavc4kProfileQualityTuningLevelType,
        "Slices": int,
    },
    total=False,
)

XavcHdIntraCbgProfileSettingsOutputTypeDef = TypedDict(
    "XavcHdIntraCbgProfileSettingsOutputTypeDef",
    {
        "XavcClass": XavcHdIntraCbgProfileClassType,
    },
)

XavcHdIntraCbgProfileSettingsTypeDef = TypedDict(
    "XavcHdIntraCbgProfileSettingsTypeDef",
    {
        "XavcClass": XavcHdIntraCbgProfileClassType,
    },
    total=False,
)

XavcHdProfileSettingsOutputTypeDef = TypedDict(
    "XavcHdProfileSettingsOutputTypeDef",
    {
        "BitrateClass": XavcHdProfileBitrateClassType,
        "FlickerAdaptiveQuantization": XavcFlickerAdaptiveQuantizationType,
        "GopBReference": XavcGopBReferenceType,
        "GopClosedCadence": int,
        "HrdBufferSize": int,
        "InterlaceMode": XavcInterlaceModeType,
        "QualityTuningLevel": XavcHdProfileQualityTuningLevelType,
        "Slices": int,
        "Telecine": XavcHdProfileTelecineType,
    },
)

XavcHdProfileSettingsTypeDef = TypedDict(
    "XavcHdProfileSettingsTypeDef",
    {
        "BitrateClass": XavcHdProfileBitrateClassType,
        "FlickerAdaptiveQuantization": XavcFlickerAdaptiveQuantizationType,
        "GopBReference": XavcGopBReferenceType,
        "GopClosedCadence": int,
        "HrdBufferSize": int,
        "InterlaceMode": XavcInterlaceModeType,
        "QualityTuningLevel": XavcHdProfileQualityTuningLevelType,
        "Slices": int,
        "Telecine": XavcHdProfileTelecineType,
    },
    total=False,
)

AudioCodecSettingsOutputTypeDef = TypedDict(
    "AudioCodecSettingsOutputTypeDef",
    {
        "AacSettings": AacSettingsOutputTypeDef,
        "Ac3Settings": Ac3SettingsOutputTypeDef,
        "AiffSettings": AiffSettingsOutputTypeDef,
        "Codec": AudioCodecType,
        "Eac3AtmosSettings": Eac3AtmosSettingsOutputTypeDef,
        "Eac3Settings": Eac3SettingsOutputTypeDef,
        "Mp2Settings": Mp2SettingsOutputTypeDef,
        "Mp3Settings": Mp3SettingsOutputTypeDef,
        "OpusSettings": OpusSettingsOutputTypeDef,
        "VorbisSettings": VorbisSettingsOutputTypeDef,
        "WavSettings": WavSettingsOutputTypeDef,
    },
)

AudioCodecSettingsTypeDef = TypedDict(
    "AudioCodecSettingsTypeDef",
    {
        "AacSettings": AacSettingsTypeDef,
        "Ac3Settings": Ac3SettingsTypeDef,
        "AiffSettings": AiffSettingsTypeDef,
        "Codec": AudioCodecType,
        "Eac3AtmosSettings": Eac3AtmosSettingsTypeDef,
        "Eac3Settings": Eac3SettingsTypeDef,
        "Mp2Settings": Mp2SettingsTypeDef,
        "Mp3Settings": Mp3SettingsTypeDef,
        "OpusSettings": OpusSettingsTypeDef,
        "VorbisSettings": VorbisSettingsTypeDef,
        "WavSettings": WavSettingsTypeDef,
    },
    total=False,
)

AutomatedAbrRuleOutputTypeDef = TypedDict(
    "AutomatedAbrRuleOutputTypeDef",
    {
        "AllowedRenditions": List[AllowedRenditionSizeOutputTypeDef],
        "ForceIncludeRenditions": List[ForceIncludeRenditionSizeOutputTypeDef],
        "MinBottomRenditionSize": MinBottomRenditionSizeOutputTypeDef,
        "MinTopRenditionSize": MinTopRenditionSizeOutputTypeDef,
        "Type": RuleTypeType,
    },
)

AutomatedAbrRuleTypeDef = TypedDict(
    "AutomatedAbrRuleTypeDef",
    {
        "AllowedRenditions": Sequence[AllowedRenditionSizeTypeDef],
        "ForceIncludeRenditions": Sequence[ForceIncludeRenditionSizeTypeDef],
        "MinBottomRenditionSize": MinBottomRenditionSizeTypeDef,
        "MinTopRenditionSize": MinTopRenditionSizeTypeDef,
        "Type": RuleTypeType,
    },
    total=False,
)

Av1SettingsOutputTypeDef = TypedDict(
    "Av1SettingsOutputTypeDef",
    {
        "AdaptiveQuantization": Av1AdaptiveQuantizationType,
        "BitDepth": Av1BitDepthType,
        "FramerateControl": Av1FramerateControlType,
        "FramerateConversionAlgorithm": Av1FramerateConversionAlgorithmType,
        "FramerateDenominator": int,
        "FramerateNumerator": int,
        "GopSize": float,
        "MaxBitrate": int,
        "NumberBFramesBetweenReferenceFrames": int,
        "QvbrSettings": Av1QvbrSettingsOutputTypeDef,
        "RateControlMode": Literal["QVBR"],
        "Slices": int,
        "SpatialAdaptiveQuantization": Av1SpatialAdaptiveQuantizationType,
    },
)

Av1SettingsTypeDef = TypedDict(
    "Av1SettingsTypeDef",
    {
        "AdaptiveQuantization": Av1AdaptiveQuantizationType,
        "BitDepth": Av1BitDepthType,
        "FramerateControl": Av1FramerateControlType,
        "FramerateConversionAlgorithm": Av1FramerateConversionAlgorithmType,
        "FramerateDenominator": int,
        "FramerateNumerator": int,
        "GopSize": float,
        "MaxBitrate": int,
        "NumberBFramesBetweenReferenceFrames": int,
        "QvbrSettings": Av1QvbrSettingsTypeDef,
        "RateControlMode": Literal["QVBR"],
        "Slices": int,
        "SpatialAdaptiveQuantization": Av1SpatialAdaptiveQuantizationType,
    },
    total=False,
)

AvcIntraSettingsOutputTypeDef = TypedDict(
    "AvcIntraSettingsOutputTypeDef",
    {
        "AvcIntraClass": AvcIntraClassType,
        "AvcIntraUhdSettings": AvcIntraUhdSettingsOutputTypeDef,
        "FramerateControl": AvcIntraFramerateControlType,
        "FramerateConversionAlgorithm": AvcIntraFramerateConversionAlgorithmType,
        "FramerateDenominator": int,
        "FramerateNumerator": int,
        "InterlaceMode": AvcIntraInterlaceModeType,
        "ScanTypeConversionMode": AvcIntraScanTypeConversionModeType,
        "SlowPal": AvcIntraSlowPalType,
        "Telecine": AvcIntraTelecineType,
    },
)

AvcIntraSettingsTypeDef = TypedDict(
    "AvcIntraSettingsTypeDef",
    {
        "AvcIntraClass": AvcIntraClassType,
        "AvcIntraUhdSettings": AvcIntraUhdSettingsTypeDef,
        "FramerateControl": AvcIntraFramerateControlType,
        "FramerateConversionAlgorithm": AvcIntraFramerateConversionAlgorithmType,
        "FramerateDenominator": int,
        "FramerateNumerator": int,
        "InterlaceMode": AvcIntraInterlaceModeType,
        "ScanTypeConversionMode": AvcIntraScanTypeConversionModeType,
        "SlowPal": AvcIntraSlowPalType,
        "Telecine": AvcIntraTelecineType,
    },
    total=False,
)

CaptionDestinationSettingsOutputTypeDef = TypedDict(
    "CaptionDestinationSettingsOutputTypeDef",
    {
        "BurninDestinationSettings": BurninDestinationSettingsOutputTypeDef,
        "DestinationType": CaptionDestinationTypeType,
        "DvbSubDestinationSettings": DvbSubDestinationSettingsOutputTypeDef,
        "EmbeddedDestinationSettings": EmbeddedDestinationSettingsOutputTypeDef,
        "ImscDestinationSettings": ImscDestinationSettingsOutputTypeDef,
        "SccDestinationSettings": SccDestinationSettingsOutputTypeDef,
        "SrtDestinationSettings": SrtDestinationSettingsOutputTypeDef,
        "TeletextDestinationSettings": TeletextDestinationSettingsOutputTypeDef,
        "TtmlDestinationSettings": TtmlDestinationSettingsOutputTypeDef,
        "WebvttDestinationSettings": WebvttDestinationSettingsOutputTypeDef,
    },
)

CaptionDestinationSettingsTypeDef = TypedDict(
    "CaptionDestinationSettingsTypeDef",
    {
        "BurninDestinationSettings": BurninDestinationSettingsTypeDef,
        "DestinationType": CaptionDestinationTypeType,
        "DvbSubDestinationSettings": DvbSubDestinationSettingsTypeDef,
        "EmbeddedDestinationSettings": EmbeddedDestinationSettingsTypeDef,
        "ImscDestinationSettings": ImscDestinationSettingsTypeDef,
        "SccDestinationSettings": SccDestinationSettingsTypeDef,
        "SrtDestinationSettings": SrtDestinationSettingsTypeDef,
        "TeletextDestinationSettings": TeletextDestinationSettingsTypeDef,
        "TtmlDestinationSettings": TtmlDestinationSettingsTypeDef,
        "WebvttDestinationSettings": WebvttDestinationSettingsTypeDef,
    },
    total=False,
)

FileSourceSettingsOutputTypeDef = TypedDict(
    "FileSourceSettingsOutputTypeDef",
    {
        "Convert608To708": FileSourceConvert608To708Type,
        "ConvertPaintToPop": CaptionSourceConvertPaintOnToPopOnType,
        "Framerate": CaptionSourceFramerateOutputTypeDef,
        "SourceFile": str,
        "TimeDelta": int,
        "TimeDeltaUnits": FileSourceTimeDeltaUnitsType,
    },
)

FileSourceSettingsTypeDef = TypedDict(
    "FileSourceSettingsTypeDef",
    {
        "Convert608To708": FileSourceConvert608To708Type,
        "ConvertPaintToPop": CaptionSourceConvertPaintOnToPopOnType,
        "Framerate": CaptionSourceFramerateTypeDef,
        "SourceFile": str,
        "TimeDelta": int,
        "TimeDeltaUnits": FileSourceTimeDeltaUnitsType,
    },
    total=False,
)

ChannelMappingOutputTypeDef = TypedDict(
    "ChannelMappingOutputTypeDef",
    {
        "OutputChannels": List[OutputChannelMappingOutputTypeDef],
    },
)

ChannelMappingTypeDef = TypedDict(
    "ChannelMappingTypeDef",
    {
        "OutputChannels": Sequence[OutputChannelMappingTypeDef],
    },
    total=False,
)

CmafEncryptionSettingsOutputTypeDef = TypedDict(
    "CmafEncryptionSettingsOutputTypeDef",
    {
        "ConstantInitializationVector": str,
        "EncryptionMethod": CmafEncryptionTypeType,
        "InitializationVectorInManifest": CmafInitializationVectorInManifestType,
        "SpekeKeyProvider": SpekeKeyProviderCmafOutputTypeDef,
        "StaticKeyProvider": StaticKeyProviderOutputTypeDef,
        "Type": CmafKeyProviderTypeType,
    },
)

CmafEncryptionSettingsTypeDef = TypedDict(
    "CmafEncryptionSettingsTypeDef",
    {
        "ConstantInitializationVector": str,
        "EncryptionMethod": CmafEncryptionTypeType,
        "InitializationVectorInManifest": CmafInitializationVectorInManifestType,
        "SpekeKeyProvider": SpekeKeyProviderCmafTypeDef,
        "StaticKeyProvider": StaticKeyProviderTypeDef,
        "Type": CmafKeyProviderTypeType,
    },
    total=False,
)

ColorCorrectorOutputTypeDef = TypedDict(
    "ColorCorrectorOutputTypeDef",
    {
        "Brightness": int,
        "ClipLimits": ClipLimitsOutputTypeDef,
        "ColorSpaceConversion": ColorSpaceConversionType,
        "Contrast": int,
        "Hdr10Metadata": Hdr10MetadataOutputTypeDef,
        "HdrToSdrToneMapper": HDRToSDRToneMapperType,
        "Hue": int,
        "SampleRangeConversion": SampleRangeConversionType,
        "Saturation": int,
        "SdrReferenceWhiteLevel": int,
    },
)

VideoSelectorOutputTypeDef = TypedDict(
    "VideoSelectorOutputTypeDef",
    {
        "AlphaBehavior": AlphaBehaviorType,
        "ColorSpace": ColorSpaceType,
        "ColorSpaceUsage": ColorSpaceUsageType,
        "EmbeddedTimecodeOverride": EmbeddedTimecodeOverrideType,
        "Hdr10Metadata": Hdr10MetadataOutputTypeDef,
        "PadVideo": PadVideoType,
        "Pid": int,
        "ProgramNumber": int,
        "Rotate": InputRotateType,
        "SampleRange": InputSampleRangeType,
    },
)

ColorCorrectorTypeDef = TypedDict(
    "ColorCorrectorTypeDef",
    {
        "Brightness": int,
        "ClipLimits": ClipLimitsTypeDef,
        "ColorSpaceConversion": ColorSpaceConversionType,
        "Contrast": int,
        "Hdr10Metadata": Hdr10MetadataTypeDef,
        "HdrToSdrToneMapper": HDRToSDRToneMapperType,
        "Hue": int,
        "SampleRangeConversion": SampleRangeConversionType,
        "Saturation": int,
        "SdrReferenceWhiteLevel": int,
    },
    total=False,
)

VideoSelectorTypeDef = TypedDict(
    "VideoSelectorTypeDef",
    {
        "AlphaBehavior": AlphaBehaviorType,
        "ColorSpace": ColorSpaceType,
        "ColorSpaceUsage": ColorSpaceUsageType,
        "EmbeddedTimecodeOverride": EmbeddedTimecodeOverrideType,
        "Hdr10Metadata": Hdr10MetadataTypeDef,
        "PadVideo": PadVideoType,
        "Pid": int,
        "ProgramNumber": int,
        "Rotate": InputRotateType,
        "SampleRange": InputSampleRangeType,
    },
    total=False,
)

_RequiredCreateQueueRequestRequestTypeDef = TypedDict(
    "_RequiredCreateQueueRequestRequestTypeDef",
    {
        "Name": str,
    },
)
_OptionalCreateQueueRequestRequestTypeDef = TypedDict(
    "_OptionalCreateQueueRequestRequestTypeDef",
    {
        "Description": str,
        "PricingPlan": PricingPlanType,
        "ReservationPlanSettings": ReservationPlanSettingsTypeDef,
        "Status": QueueStatusType,
        "Tags": Mapping[str, str],
    },
    total=False,
)

class CreateQueueRequestRequestTypeDef(
    _RequiredCreateQueueRequestRequestTypeDef, _OptionalCreateQueueRequestRequestTypeDef
):
    pass

_RequiredUpdateQueueRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateQueueRequestRequestTypeDef",
    {
        "Name": str,
    },
)
_OptionalUpdateQueueRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateQueueRequestRequestTypeDef",
    {
        "Description": str,
        "ReservationPlanSettings": ReservationPlanSettingsTypeDef,
        "Status": QueueStatusType,
    },
    total=False,
)

class UpdateQueueRequestRequestTypeDef(
    _RequiredUpdateQueueRequestRequestTypeDef, _OptionalUpdateQueueRequestRequestTypeDef
):
    pass

DashIsoEncryptionSettingsOutputTypeDef = TypedDict(
    "DashIsoEncryptionSettingsOutputTypeDef",
    {
        "PlaybackDeviceCompatibility": DashIsoPlaybackDeviceCompatibilityType,
        "SpekeKeyProvider": SpekeKeyProviderOutputTypeDef,
    },
)

HlsEncryptionSettingsOutputTypeDef = TypedDict(
    "HlsEncryptionSettingsOutputTypeDef",
    {
        "ConstantInitializationVector": str,
        "EncryptionMethod": HlsEncryptionTypeType,
        "InitializationVectorInManifest": HlsInitializationVectorInManifestType,
        "OfflineEncrypted": HlsOfflineEncryptedType,
        "SpekeKeyProvider": SpekeKeyProviderOutputTypeDef,
        "StaticKeyProvider": StaticKeyProviderOutputTypeDef,
        "Type": HlsKeyProviderTypeType,
    },
)

MsSmoothEncryptionSettingsOutputTypeDef = TypedDict(
    "MsSmoothEncryptionSettingsOutputTypeDef",
    {
        "SpekeKeyProvider": SpekeKeyProviderOutputTypeDef,
    },
)

DashIsoEncryptionSettingsTypeDef = TypedDict(
    "DashIsoEncryptionSettingsTypeDef",
    {
        "PlaybackDeviceCompatibility": DashIsoPlaybackDeviceCompatibilityType,
        "SpekeKeyProvider": SpekeKeyProviderTypeDef,
    },
    total=False,
)

HlsEncryptionSettingsTypeDef = TypedDict(
    "HlsEncryptionSettingsTypeDef",
    {
        "ConstantInitializationVector": str,
        "EncryptionMethod": HlsEncryptionTypeType,
        "InitializationVectorInManifest": HlsInitializationVectorInManifestType,
        "OfflineEncrypted": HlsOfflineEncryptedType,
        "SpekeKeyProvider": SpekeKeyProviderTypeDef,
        "StaticKeyProvider": StaticKeyProviderTypeDef,
        "Type": HlsKeyProviderTypeType,
    },
    total=False,
)

MsSmoothEncryptionSettingsTypeDef = TypedDict(
    "MsSmoothEncryptionSettingsTypeDef",
    {
        "SpekeKeyProvider": SpekeKeyProviderTypeDef,
    },
    total=False,
)

DescribeEndpointsRequestDescribeEndpointsPaginateTypeDef = TypedDict(
    "DescribeEndpointsRequestDescribeEndpointsPaginateTypeDef",
    {
        "Mode": DescribeEndpointsModeType,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListJobTemplatesRequestListJobTemplatesPaginateTypeDef = TypedDict(
    "ListJobTemplatesRequestListJobTemplatesPaginateTypeDef",
    {
        "Category": str,
        "ListBy": JobTemplateListByType,
        "Order": OrderType,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListJobsRequestListJobsPaginateTypeDef = TypedDict(
    "ListJobsRequestListJobsPaginateTypeDef",
    {
        "Order": OrderType,
        "Queue": str,
        "Status": JobStatusType,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListPresetsRequestListPresetsPaginateTypeDef = TypedDict(
    "ListPresetsRequestListPresetsPaginateTypeDef",
    {
        "Category": str,
        "ListBy": PresetListByType,
        "Order": OrderType,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListQueuesRequestListQueuesPaginateTypeDef = TypedDict(
    "ListQueuesRequestListQueuesPaginateTypeDef",
    {
        "ListBy": QueueListByType,
        "Order": OrderType,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

DescribeEndpointsResponseTypeDef = TypedDict(
    "DescribeEndpointsResponseTypeDef",
    {
        "Endpoints": List[EndpointTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DolbyVisionOutputTypeDef = TypedDict(
    "DolbyVisionOutputTypeDef",
    {
        "L6Metadata": DolbyVisionLevel6MetadataOutputTypeDef,
        "L6Mode": DolbyVisionLevel6ModeType,
        "Mapping": DolbyVisionMappingType,
        "Profile": DolbyVisionProfileType,
    },
)

DolbyVisionTypeDef = TypedDict(
    "DolbyVisionTypeDef",
    {
        "L6Metadata": DolbyVisionLevel6MetadataTypeDef,
        "L6Mode": DolbyVisionLevel6ModeType,
        "Mapping": DolbyVisionMappingType,
        "Profile": DolbyVisionProfileType,
    },
    total=False,
)

EsamSettingsOutputTypeDef = TypedDict(
    "EsamSettingsOutputTypeDef",
    {
        "ManifestConfirmConditionNotification": (
            EsamManifestConfirmConditionNotificationOutputTypeDef
        ),
        "ResponseSignalPreroll": int,
        "SignalProcessingNotification": EsamSignalProcessingNotificationOutputTypeDef,
    },
)

EsamSettingsTypeDef = TypedDict(
    "EsamSettingsTypeDef",
    {
        "ManifestConfirmConditionNotification": EsamManifestConfirmConditionNotificationTypeDef,
        "ResponseSignalPreroll": int,
        "SignalProcessingNotification": EsamSignalProcessingNotificationTypeDef,
    },
    total=False,
)

GetPolicyResponseTypeDef = TypedDict(
    "GetPolicyResponseTypeDef",
    {
        "Policy": PolicyOutputTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PutPolicyResponseTypeDef = TypedDict(
    "PutPolicyResponseTypeDef",
    {
        "Policy": PolicyOutputTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

H264SettingsOutputTypeDef = TypedDict(
    "H264SettingsOutputTypeDef",
    {
        "AdaptiveQuantization": H264AdaptiveQuantizationType,
        "BandwidthReductionFilter": BandwidthReductionFilterOutputTypeDef,
        "Bitrate": int,
        "CodecLevel": H264CodecLevelType,
        "CodecProfile": H264CodecProfileType,
        "DynamicSubGop": H264DynamicSubGopType,
        "EntropyEncoding": H264EntropyEncodingType,
        "FieldEncoding": H264FieldEncodingType,
        "FlickerAdaptiveQuantization": H264FlickerAdaptiveQuantizationType,
        "FramerateControl": H264FramerateControlType,
        "FramerateConversionAlgorithm": H264FramerateConversionAlgorithmType,
        "FramerateDenominator": int,
        "FramerateNumerator": int,
        "GopBReference": H264GopBReferenceType,
        "GopClosedCadence": int,
        "GopSize": float,
        "GopSizeUnits": H264GopSizeUnitsType,
        "HrdBufferFinalFillPercentage": int,
        "HrdBufferInitialFillPercentage": int,
        "HrdBufferSize": int,
        "InterlaceMode": H264InterlaceModeType,
        "MaxBitrate": int,
        "MinIInterval": int,
        "NumberBFramesBetweenReferenceFrames": int,
        "NumberReferenceFrames": int,
        "ParControl": H264ParControlType,
        "ParDenominator": int,
        "ParNumerator": int,
        "QualityTuningLevel": H264QualityTuningLevelType,
        "QvbrSettings": H264QvbrSettingsOutputTypeDef,
        "RateControlMode": H264RateControlModeType,
        "RepeatPps": H264RepeatPpsType,
        "ScanTypeConversionMode": H264ScanTypeConversionModeType,
        "SceneChangeDetect": H264SceneChangeDetectType,
        "Slices": int,
        "SlowPal": H264SlowPalType,
        "Softness": int,
        "SpatialAdaptiveQuantization": H264SpatialAdaptiveQuantizationType,
        "Syntax": H264SyntaxType,
        "Telecine": H264TelecineType,
        "TemporalAdaptiveQuantization": H264TemporalAdaptiveQuantizationType,
        "UnregisteredSeiTimecode": H264UnregisteredSeiTimecodeType,
    },
)

H264SettingsTypeDef = TypedDict(
    "H264SettingsTypeDef",
    {
        "AdaptiveQuantization": H264AdaptiveQuantizationType,
        "BandwidthReductionFilter": BandwidthReductionFilterTypeDef,
        "Bitrate": int,
        "CodecLevel": H264CodecLevelType,
        "CodecProfile": H264CodecProfileType,
        "DynamicSubGop": H264DynamicSubGopType,
        "EntropyEncoding": H264EntropyEncodingType,
        "FieldEncoding": H264FieldEncodingType,
        "FlickerAdaptiveQuantization": H264FlickerAdaptiveQuantizationType,
        "FramerateControl": H264FramerateControlType,
        "FramerateConversionAlgorithm": H264FramerateConversionAlgorithmType,
        "FramerateDenominator": int,
        "FramerateNumerator": int,
        "GopBReference": H264GopBReferenceType,
        "GopClosedCadence": int,
        "GopSize": float,
        "GopSizeUnits": H264GopSizeUnitsType,
        "HrdBufferFinalFillPercentage": int,
        "HrdBufferInitialFillPercentage": int,
        "HrdBufferSize": int,
        "InterlaceMode": H264InterlaceModeType,
        "MaxBitrate": int,
        "MinIInterval": int,
        "NumberBFramesBetweenReferenceFrames": int,
        "NumberReferenceFrames": int,
        "ParControl": H264ParControlType,
        "ParDenominator": int,
        "ParNumerator": int,
        "QualityTuningLevel": H264QualityTuningLevelType,
        "QvbrSettings": H264QvbrSettingsTypeDef,
        "RateControlMode": H264RateControlModeType,
        "RepeatPps": H264RepeatPpsType,
        "ScanTypeConversionMode": H264ScanTypeConversionModeType,
        "SceneChangeDetect": H264SceneChangeDetectType,
        "Slices": int,
        "SlowPal": H264SlowPalType,
        "Softness": int,
        "SpatialAdaptiveQuantization": H264SpatialAdaptiveQuantizationType,
        "Syntax": H264SyntaxType,
        "Telecine": H264TelecineType,
        "TemporalAdaptiveQuantization": H264TemporalAdaptiveQuantizationType,
        "UnregisteredSeiTimecode": H264UnregisteredSeiTimecodeType,
    },
    total=False,
)

H265SettingsOutputTypeDef = TypedDict(
    "H265SettingsOutputTypeDef",
    {
        "AdaptiveQuantization": H265AdaptiveQuantizationType,
        "AlternateTransferFunctionSei": H265AlternateTransferFunctionSeiType,
        "BandwidthReductionFilter": BandwidthReductionFilterOutputTypeDef,
        "Bitrate": int,
        "CodecLevel": H265CodecLevelType,
        "CodecProfile": H265CodecProfileType,
        "DynamicSubGop": H265DynamicSubGopType,
        "FlickerAdaptiveQuantization": H265FlickerAdaptiveQuantizationType,
        "FramerateControl": H265FramerateControlType,
        "FramerateConversionAlgorithm": H265FramerateConversionAlgorithmType,
        "FramerateDenominator": int,
        "FramerateNumerator": int,
        "GopBReference": H265GopBReferenceType,
        "GopClosedCadence": int,
        "GopSize": float,
        "GopSizeUnits": H265GopSizeUnitsType,
        "HrdBufferFinalFillPercentage": int,
        "HrdBufferInitialFillPercentage": int,
        "HrdBufferSize": int,
        "InterlaceMode": H265InterlaceModeType,
        "MaxBitrate": int,
        "MinIInterval": int,
        "NumberBFramesBetweenReferenceFrames": int,
        "NumberReferenceFrames": int,
        "ParControl": H265ParControlType,
        "ParDenominator": int,
        "ParNumerator": int,
        "QualityTuningLevel": H265QualityTuningLevelType,
        "QvbrSettings": H265QvbrSettingsOutputTypeDef,
        "RateControlMode": H265RateControlModeType,
        "SampleAdaptiveOffsetFilterMode": H265SampleAdaptiveOffsetFilterModeType,
        "ScanTypeConversionMode": H265ScanTypeConversionModeType,
        "SceneChangeDetect": H265SceneChangeDetectType,
        "Slices": int,
        "SlowPal": H265SlowPalType,
        "SpatialAdaptiveQuantization": H265SpatialAdaptiveQuantizationType,
        "Telecine": H265TelecineType,
        "TemporalAdaptiveQuantization": H265TemporalAdaptiveQuantizationType,
        "TemporalIds": H265TemporalIdsType,
        "Tiles": H265TilesType,
        "UnregisteredSeiTimecode": H265UnregisteredSeiTimecodeType,
        "WriteMp4PackagingType": H265WriteMp4PackagingTypeType,
    },
)

H265SettingsTypeDef = TypedDict(
    "H265SettingsTypeDef",
    {
        "AdaptiveQuantization": H265AdaptiveQuantizationType,
        "AlternateTransferFunctionSei": H265AlternateTransferFunctionSeiType,
        "BandwidthReductionFilter": BandwidthReductionFilterTypeDef,
        "Bitrate": int,
        "CodecLevel": H265CodecLevelType,
        "CodecProfile": H265CodecProfileType,
        "DynamicSubGop": H265DynamicSubGopType,
        "FlickerAdaptiveQuantization": H265FlickerAdaptiveQuantizationType,
        "FramerateControl": H265FramerateControlType,
        "FramerateConversionAlgorithm": H265FramerateConversionAlgorithmType,
        "FramerateDenominator": int,
        "FramerateNumerator": int,
        "GopBReference": H265GopBReferenceType,
        "GopClosedCadence": int,
        "GopSize": float,
        "GopSizeUnits": H265GopSizeUnitsType,
        "HrdBufferFinalFillPercentage": int,
        "HrdBufferInitialFillPercentage": int,
        "HrdBufferSize": int,
        "InterlaceMode": H265InterlaceModeType,
        "MaxBitrate": int,
        "MinIInterval": int,
        "NumberBFramesBetweenReferenceFrames": int,
        "NumberReferenceFrames": int,
        "ParControl": H265ParControlType,
        "ParDenominator": int,
        "ParNumerator": int,
        "QualityTuningLevel": H265QualityTuningLevelType,
        "QvbrSettings": H265QvbrSettingsTypeDef,
        "RateControlMode": H265RateControlModeType,
        "SampleAdaptiveOffsetFilterMode": H265SampleAdaptiveOffsetFilterModeType,
        "ScanTypeConversionMode": H265ScanTypeConversionModeType,
        "SceneChangeDetect": H265SceneChangeDetectType,
        "Slices": int,
        "SlowPal": H265SlowPalType,
        "SpatialAdaptiveQuantization": H265SpatialAdaptiveQuantizationType,
        "Telecine": H265TelecineType,
        "TemporalAdaptiveQuantization": H265TemporalAdaptiveQuantizationType,
        "TemporalIds": H265TemporalIdsType,
        "Tiles": H265TilesType,
        "UnregisteredSeiTimecode": H265UnregisteredSeiTimecodeType,
        "WriteMp4PackagingType": H265WriteMp4PackagingTypeType,
    },
    total=False,
)

OutputSettingsOutputTypeDef = TypedDict(
    "OutputSettingsOutputTypeDef",
    {
        "HlsSettings": HlsSettingsOutputTypeDef,
    },
)

TimedMetadataInsertionOutputTypeDef = TypedDict(
    "TimedMetadataInsertionOutputTypeDef",
    {
        "Id3Insertions": List[Id3InsertionOutputTypeDef],
    },
)

TimedMetadataInsertionTypeDef = TypedDict(
    "TimedMetadataInsertionTypeDef",
    {
        "Id3Insertions": Sequence[Id3InsertionTypeDef],
    },
    total=False,
)

ImageInserterOutputTypeDef = TypedDict(
    "ImageInserterOutputTypeDef",
    {
        "InsertableImages": List[InsertableImageOutputTypeDef],
        "SdrReferenceWhiteLevel": int,
    },
)

ImageInserterTypeDef = TypedDict(
    "ImageInserterTypeDef",
    {
        "InsertableImages": Sequence[InsertableImageTypeDef],
        "SdrReferenceWhiteLevel": int,
    },
    total=False,
)

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "ResourceTags": ResourceTagsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

M2tsSettingsOutputTypeDef = TypedDict(
    "M2tsSettingsOutputTypeDef",
    {
        "AudioBufferModel": M2tsAudioBufferModelType,
        "AudioDuration": M2tsAudioDurationType,
        "AudioFramesPerPes": int,
        "AudioPids": List[int],
        "Bitrate": int,
        "BufferModel": M2tsBufferModelType,
        "DataPTSControl": M2tsDataPtsControlType,
        "DvbNitSettings": DvbNitSettingsOutputTypeDef,
        "DvbSdtSettings": DvbSdtSettingsOutputTypeDef,
        "DvbSubPids": List[int],
        "DvbTdtSettings": DvbTdtSettingsOutputTypeDef,
        "DvbTeletextPid": int,
        "EbpAudioInterval": M2tsEbpAudioIntervalType,
        "EbpPlacement": M2tsEbpPlacementType,
        "EsRateInPes": M2tsEsRateInPesType,
        "ForceTsVideoEbpOrder": M2tsForceTsVideoEbpOrderType,
        "FragmentTime": float,
        "KlvMetadata": M2tsKlvMetadataType,
        "MaxPcrInterval": int,
        "MinEbpInterval": int,
        "NielsenId3": M2tsNielsenId3Type,
        "NullPacketBitrate": float,
        "PatInterval": int,
        "PcrControl": M2tsPcrControlType,
        "PcrPid": int,
        "PmtInterval": int,
        "PmtPid": int,
        "PrivateMetadataPid": int,
        "ProgramNumber": int,
        "RateMode": M2tsRateModeType,
        "Scte35Esam": M2tsScte35EsamOutputTypeDef,
        "Scte35Pid": int,
        "Scte35Source": M2tsScte35SourceType,
        "SegmentationMarkers": M2tsSegmentationMarkersType,
        "SegmentationStyle": M2tsSegmentationStyleType,
        "SegmentationTime": float,
        "TimedMetadataPid": int,
        "TransportStreamId": int,
        "VideoPid": int,
    },
)

M2tsSettingsTypeDef = TypedDict(
    "M2tsSettingsTypeDef",
    {
        "AudioBufferModel": M2tsAudioBufferModelType,
        "AudioDuration": M2tsAudioDurationType,
        "AudioFramesPerPes": int,
        "AudioPids": Sequence[int],
        "Bitrate": int,
        "BufferModel": M2tsBufferModelType,
        "DataPTSControl": M2tsDataPtsControlType,
        "DvbNitSettings": DvbNitSettingsTypeDef,
        "DvbSdtSettings": DvbSdtSettingsTypeDef,
        "DvbSubPids": Sequence[int],
        "DvbTdtSettings": DvbTdtSettingsTypeDef,
        "DvbTeletextPid": int,
        "EbpAudioInterval": M2tsEbpAudioIntervalType,
        "EbpPlacement": M2tsEbpPlacementType,
        "EsRateInPes": M2tsEsRateInPesType,
        "ForceTsVideoEbpOrder": M2tsForceTsVideoEbpOrderType,
        "FragmentTime": float,
        "KlvMetadata": M2tsKlvMetadataType,
        "MaxPcrInterval": int,
        "MinEbpInterval": int,
        "NielsenId3": M2tsNielsenId3Type,
        "NullPacketBitrate": float,
        "PatInterval": int,
        "PcrControl": M2tsPcrControlType,
        "PcrPid": int,
        "PmtInterval": int,
        "PmtPid": int,
        "PrivateMetadataPid": int,
        "ProgramNumber": int,
        "RateMode": M2tsRateModeType,
        "Scte35Esam": M2tsScte35EsamTypeDef,
        "Scte35Pid": int,
        "Scte35Source": M2tsScte35SourceType,
        "SegmentationMarkers": M2tsSegmentationMarkersType,
        "SegmentationStyle": M2tsSegmentationStyleType,
        "SegmentationTime": float,
        "TimedMetadataPid": int,
        "TransportStreamId": int,
        "VideoPid": int,
    },
    total=False,
)

MotionImageInserterOutputTypeDef = TypedDict(
    "MotionImageInserterOutputTypeDef",
    {
        "Framerate": MotionImageInsertionFramerateOutputTypeDef,
        "Input": str,
        "InsertionMode": MotionImageInsertionModeType,
        "Offset": MotionImageInsertionOffsetOutputTypeDef,
        "Playback": MotionImagePlaybackType,
        "StartTime": str,
    },
)

MotionImageInserterTypeDef = TypedDict(
    "MotionImageInserterTypeDef",
    {
        "Framerate": MotionImageInsertionFramerateTypeDef,
        "Input": str,
        "InsertionMode": MotionImageInsertionModeType,
        "Offset": MotionImageInsertionOffsetTypeDef,
        "Playback": MotionImagePlaybackType,
        "StartTime": str,
    },
    total=False,
)

MxfSettingsOutputTypeDef = TypedDict(
    "MxfSettingsOutputTypeDef",
    {
        "AfdSignaling": MxfAfdSignalingType,
        "Profile": MxfProfileType,
        "XavcProfileSettings": MxfXavcProfileSettingsOutputTypeDef,
    },
)

MxfSettingsTypeDef = TypedDict(
    "MxfSettingsTypeDef",
    {
        "AfdSignaling": MxfAfdSignalingType,
        "Profile": MxfProfileType,
        "XavcProfileSettings": MxfXavcProfileSettingsTypeDef,
    },
    total=False,
)

PartnerWatermarkingOutputTypeDef = TypedDict(
    "PartnerWatermarkingOutputTypeDef",
    {
        "NexguardFileMarkerSettings": NexGuardFileMarkerSettingsOutputTypeDef,
    },
)

PartnerWatermarkingTypeDef = TypedDict(
    "PartnerWatermarkingTypeDef",
    {
        "NexguardFileMarkerSettings": NexGuardFileMarkerSettingsTypeDef,
    },
    total=False,
)

NoiseReducerOutputTypeDef = TypedDict(
    "NoiseReducerOutputTypeDef",
    {
        "Filter": NoiseReducerFilterType,
        "FilterSettings": NoiseReducerFilterSettingsOutputTypeDef,
        "SpatialFilterSettings": NoiseReducerSpatialFilterSettingsOutputTypeDef,
        "TemporalFilterSettings": NoiseReducerTemporalFilterSettingsOutputTypeDef,
    },
)

NoiseReducerTypeDef = TypedDict(
    "NoiseReducerTypeDef",
    {
        "Filter": NoiseReducerFilterType,
        "FilterSettings": NoiseReducerFilterSettingsTypeDef,
        "SpatialFilterSettings": NoiseReducerSpatialFilterSettingsTypeDef,
        "TemporalFilterSettings": NoiseReducerTemporalFilterSettingsTypeDef,
    },
    total=False,
)

OutputDetailTypeDef = TypedDict(
    "OutputDetailTypeDef",
    {
        "DurationInMs": int,
        "VideoDetails": VideoDetailTypeDef,
    },
)

PutPolicyRequestRequestTypeDef = TypedDict(
    "PutPolicyRequestRequestTypeDef",
    {
        "Policy": PolicyTypeDef,
    },
)

QueueTypeDef = TypedDict(
    "QueueTypeDef",
    {
        "Arn": str,
        "CreatedAt": datetime,
        "Description": str,
        "LastUpdated": datetime,
        "Name": str,
        "PricingPlan": PricingPlanType,
        "ProgressingJobsCount": int,
        "ReservationPlan": ReservationPlanTypeDef,
        "Status": QueueStatusType,
        "SubmittedJobsCount": int,
        "Type": TypeType,
    },
)

S3DestinationSettingsOutputTypeDef = TypedDict(
    "S3DestinationSettingsOutputTypeDef",
    {
        "AccessControl": S3DestinationAccessControlOutputTypeDef,
        "Encryption": S3EncryptionSettingsOutputTypeDef,
    },
)

S3DestinationSettingsTypeDef = TypedDict(
    "S3DestinationSettingsTypeDef",
    {
        "AccessControl": S3DestinationAccessControlTypeDef,
        "Encryption": S3EncryptionSettingsTypeDef,
    },
    total=False,
)

XavcSettingsOutputTypeDef = TypedDict(
    "XavcSettingsOutputTypeDef",
    {
        "AdaptiveQuantization": XavcAdaptiveQuantizationType,
        "EntropyEncoding": XavcEntropyEncodingType,
        "FramerateControl": XavcFramerateControlType,
        "FramerateConversionAlgorithm": XavcFramerateConversionAlgorithmType,
        "FramerateDenominator": int,
        "FramerateNumerator": int,
        "Profile": XavcProfileType,
        "SlowPal": XavcSlowPalType,
        "Softness": int,
        "SpatialAdaptiveQuantization": XavcSpatialAdaptiveQuantizationType,
        "TemporalAdaptiveQuantization": XavcTemporalAdaptiveQuantizationType,
        "Xavc4kIntraCbgProfileSettings": Xavc4kIntraCbgProfileSettingsOutputTypeDef,
        "Xavc4kIntraVbrProfileSettings": Xavc4kIntraVbrProfileSettingsOutputTypeDef,
        "Xavc4kProfileSettings": Xavc4kProfileSettingsOutputTypeDef,
        "XavcHdIntraCbgProfileSettings": XavcHdIntraCbgProfileSettingsOutputTypeDef,
        "XavcHdProfileSettings": XavcHdProfileSettingsOutputTypeDef,
    },
)

XavcSettingsTypeDef = TypedDict(
    "XavcSettingsTypeDef",
    {
        "AdaptiveQuantization": XavcAdaptiveQuantizationType,
        "EntropyEncoding": XavcEntropyEncodingType,
        "FramerateControl": XavcFramerateControlType,
        "FramerateConversionAlgorithm": XavcFramerateConversionAlgorithmType,
        "FramerateDenominator": int,
        "FramerateNumerator": int,
        "Profile": XavcProfileType,
        "SlowPal": XavcSlowPalType,
        "Softness": int,
        "SpatialAdaptiveQuantization": XavcSpatialAdaptiveQuantizationType,
        "TemporalAdaptiveQuantization": XavcTemporalAdaptiveQuantizationType,
        "Xavc4kIntraCbgProfileSettings": Xavc4kIntraCbgProfileSettingsTypeDef,
        "Xavc4kIntraVbrProfileSettings": Xavc4kIntraVbrProfileSettingsTypeDef,
        "Xavc4kProfileSettings": Xavc4kProfileSettingsTypeDef,
        "XavcHdIntraCbgProfileSettings": XavcHdIntraCbgProfileSettingsTypeDef,
        "XavcHdProfileSettings": XavcHdProfileSettingsTypeDef,
    },
    total=False,
)

AutomatedAbrSettingsOutputTypeDef = TypedDict(
    "AutomatedAbrSettingsOutputTypeDef",
    {
        "MaxAbrBitrate": int,
        "MaxRenditions": int,
        "MinAbrBitrate": int,
        "Rules": List[AutomatedAbrRuleOutputTypeDef],
    },
)

AutomatedAbrSettingsTypeDef = TypedDict(
    "AutomatedAbrSettingsTypeDef",
    {
        "MaxAbrBitrate": int,
        "MaxRenditions": int,
        "MinAbrBitrate": int,
        "Rules": Sequence[AutomatedAbrRuleTypeDef],
    },
    total=False,
)

CaptionDescriptionOutputTypeDef = TypedDict(
    "CaptionDescriptionOutputTypeDef",
    {
        "CaptionSelectorName": str,
        "CustomLanguageCode": str,
        "DestinationSettings": CaptionDestinationSettingsOutputTypeDef,
        "LanguageCode": LanguageCodeType,
        "LanguageDescription": str,
    },
)

CaptionDescriptionPresetOutputTypeDef = TypedDict(
    "CaptionDescriptionPresetOutputTypeDef",
    {
        "CustomLanguageCode": str,
        "DestinationSettings": CaptionDestinationSettingsOutputTypeDef,
        "LanguageCode": LanguageCodeType,
        "LanguageDescription": str,
    },
)

CaptionDescriptionPresetTypeDef = TypedDict(
    "CaptionDescriptionPresetTypeDef",
    {
        "CustomLanguageCode": str,
        "DestinationSettings": CaptionDestinationSettingsTypeDef,
        "LanguageCode": LanguageCodeType,
        "LanguageDescription": str,
    },
    total=False,
)

CaptionSourceSettingsOutputTypeDef = TypedDict(
    "CaptionSourceSettingsOutputTypeDef",
    {
        "AncillarySourceSettings": AncillarySourceSettingsOutputTypeDef,
        "DvbSubSourceSettings": DvbSubSourceSettingsOutputTypeDef,
        "EmbeddedSourceSettings": EmbeddedSourceSettingsOutputTypeDef,
        "FileSourceSettings": FileSourceSettingsOutputTypeDef,
        "SourceType": CaptionSourceTypeType,
        "TeletextSourceSettings": TeletextSourceSettingsOutputTypeDef,
        "TrackSourceSettings": TrackSourceSettingsOutputTypeDef,
        "WebvttHlsSourceSettings": WebvttHlsSourceSettingsOutputTypeDef,
    },
)

CaptionSourceSettingsTypeDef = TypedDict(
    "CaptionSourceSettingsTypeDef",
    {
        "AncillarySourceSettings": AncillarySourceSettingsTypeDef,
        "DvbSubSourceSettings": DvbSubSourceSettingsTypeDef,
        "EmbeddedSourceSettings": EmbeddedSourceSettingsTypeDef,
        "FileSourceSettings": FileSourceSettingsTypeDef,
        "SourceType": CaptionSourceTypeType,
        "TeletextSourceSettings": TeletextSourceSettingsTypeDef,
        "TrackSourceSettings": TrackSourceSettingsTypeDef,
        "WebvttHlsSourceSettings": WebvttHlsSourceSettingsTypeDef,
    },
    total=False,
)

RemixSettingsOutputTypeDef = TypedDict(
    "RemixSettingsOutputTypeDef",
    {
        "ChannelMapping": ChannelMappingOutputTypeDef,
        "ChannelsIn": int,
        "ChannelsOut": int,
    },
)

RemixSettingsTypeDef = TypedDict(
    "RemixSettingsTypeDef",
    {
        "ChannelMapping": ChannelMappingTypeDef,
        "ChannelsIn": int,
        "ChannelsOut": int,
    },
    total=False,
)

ContainerSettingsOutputTypeDef = TypedDict(
    "ContainerSettingsOutputTypeDef",
    {
        "CmfcSettings": CmfcSettingsOutputTypeDef,
        "Container": ContainerTypeType,
        "F4vSettings": F4vSettingsOutputTypeDef,
        "M2tsSettings": M2tsSettingsOutputTypeDef,
        "M3u8Settings": M3u8SettingsOutputTypeDef,
        "MovSettings": MovSettingsOutputTypeDef,
        "Mp4Settings": Mp4SettingsOutputTypeDef,
        "MpdSettings": MpdSettingsOutputTypeDef,
        "MxfSettings": MxfSettingsOutputTypeDef,
    },
)

ContainerSettingsTypeDef = TypedDict(
    "ContainerSettingsTypeDef",
    {
        "CmfcSettings": CmfcSettingsTypeDef,
        "Container": ContainerTypeType,
        "F4vSettings": F4vSettingsTypeDef,
        "M2tsSettings": M2tsSettingsTypeDef,
        "M3u8Settings": M3u8SettingsTypeDef,
        "MovSettings": MovSettingsTypeDef,
        "Mp4Settings": Mp4SettingsTypeDef,
        "MpdSettings": MpdSettingsTypeDef,
        "MxfSettings": MxfSettingsTypeDef,
    },
    total=False,
)

VideoPreprocessorOutputTypeDef = TypedDict(
    "VideoPreprocessorOutputTypeDef",
    {
        "ColorCorrector": ColorCorrectorOutputTypeDef,
        "Deinterlacer": DeinterlacerOutputTypeDef,
        "DolbyVision": DolbyVisionOutputTypeDef,
        "Hdr10Plus": Hdr10PlusOutputTypeDef,
        "ImageInserter": ImageInserterOutputTypeDef,
        "NoiseReducer": NoiseReducerOutputTypeDef,
        "PartnerWatermarking": PartnerWatermarkingOutputTypeDef,
        "TimecodeBurnin": TimecodeBurninOutputTypeDef,
    },
)

VideoPreprocessorTypeDef = TypedDict(
    "VideoPreprocessorTypeDef",
    {
        "ColorCorrector": ColorCorrectorTypeDef,
        "Deinterlacer": DeinterlacerTypeDef,
        "DolbyVision": DolbyVisionTypeDef,
        "Hdr10Plus": Hdr10PlusTypeDef,
        "ImageInserter": ImageInserterTypeDef,
        "NoiseReducer": NoiseReducerTypeDef,
        "PartnerWatermarking": PartnerWatermarkingTypeDef,
        "TimecodeBurnin": TimecodeBurninTypeDef,
    },
    total=False,
)

OutputGroupDetailTypeDef = TypedDict(
    "OutputGroupDetailTypeDef",
    {
        "OutputDetails": List[OutputDetailTypeDef],
    },
)

CreateQueueResponseTypeDef = TypedDict(
    "CreateQueueResponseTypeDef",
    {
        "Queue": QueueTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetQueueResponseTypeDef = TypedDict(
    "GetQueueResponseTypeDef",
    {
        "Queue": QueueTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListQueuesResponseTypeDef = TypedDict(
    "ListQueuesResponseTypeDef",
    {
        "NextToken": str,
        "Queues": List[QueueTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateQueueResponseTypeDef = TypedDict(
    "UpdateQueueResponseTypeDef",
    {
        "Queue": QueueTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DestinationSettingsOutputTypeDef = TypedDict(
    "DestinationSettingsOutputTypeDef",
    {
        "S3Settings": S3DestinationSettingsOutputTypeDef,
    },
)

DestinationSettingsTypeDef = TypedDict(
    "DestinationSettingsTypeDef",
    {
        "S3Settings": S3DestinationSettingsTypeDef,
    },
    total=False,
)

VideoCodecSettingsOutputTypeDef = TypedDict(
    "VideoCodecSettingsOutputTypeDef",
    {
        "Av1Settings": Av1SettingsOutputTypeDef,
        "AvcIntraSettings": AvcIntraSettingsOutputTypeDef,
        "Codec": VideoCodecType,
        "FrameCaptureSettings": FrameCaptureSettingsOutputTypeDef,
        "H264Settings": H264SettingsOutputTypeDef,
        "H265Settings": H265SettingsOutputTypeDef,
        "Mpeg2Settings": Mpeg2SettingsOutputTypeDef,
        "ProresSettings": ProresSettingsOutputTypeDef,
        "Vc3Settings": Vc3SettingsOutputTypeDef,
        "Vp8Settings": Vp8SettingsOutputTypeDef,
        "Vp9Settings": Vp9SettingsOutputTypeDef,
        "XavcSettings": XavcSettingsOutputTypeDef,
    },
)

VideoCodecSettingsTypeDef = TypedDict(
    "VideoCodecSettingsTypeDef",
    {
        "Av1Settings": Av1SettingsTypeDef,
        "AvcIntraSettings": AvcIntraSettingsTypeDef,
        "Codec": VideoCodecType,
        "FrameCaptureSettings": FrameCaptureSettingsTypeDef,
        "H264Settings": H264SettingsTypeDef,
        "H265Settings": H265SettingsTypeDef,
        "Mpeg2Settings": Mpeg2SettingsTypeDef,
        "ProresSettings": ProresSettingsTypeDef,
        "Vc3Settings": Vc3SettingsTypeDef,
        "Vp8Settings": Vp8SettingsTypeDef,
        "Vp9Settings": Vp9SettingsTypeDef,
        "XavcSettings": XavcSettingsTypeDef,
    },
    total=False,
)

AutomatedEncodingSettingsOutputTypeDef = TypedDict(
    "AutomatedEncodingSettingsOutputTypeDef",
    {
        "AbrSettings": AutomatedAbrSettingsOutputTypeDef,
    },
)

AutomatedEncodingSettingsTypeDef = TypedDict(
    "AutomatedEncodingSettingsTypeDef",
    {
        "AbrSettings": AutomatedAbrSettingsTypeDef,
    },
    total=False,
)

CaptionSelectorOutputTypeDef = TypedDict(
    "CaptionSelectorOutputTypeDef",
    {
        "CustomLanguageCode": str,
        "LanguageCode": LanguageCodeType,
        "SourceSettings": CaptionSourceSettingsOutputTypeDef,
    },
)

CaptionSelectorTypeDef = TypedDict(
    "CaptionSelectorTypeDef",
    {
        "CustomLanguageCode": str,
        "LanguageCode": LanguageCodeType,
        "SourceSettings": CaptionSourceSettingsTypeDef,
    },
    total=False,
)

AudioDescriptionOutputTypeDef = TypedDict(
    "AudioDescriptionOutputTypeDef",
    {
        "AudioChannelTaggingSettings": AudioChannelTaggingSettingsOutputTypeDef,
        "AudioNormalizationSettings": AudioNormalizationSettingsOutputTypeDef,
        "AudioSourceName": str,
        "AudioType": int,
        "AudioTypeControl": AudioTypeControlType,
        "CodecSettings": AudioCodecSettingsOutputTypeDef,
        "CustomLanguageCode": str,
        "LanguageCode": LanguageCodeType,
        "LanguageCodeControl": AudioLanguageCodeControlType,
        "RemixSettings": RemixSettingsOutputTypeDef,
        "StreamName": str,
    },
)

AudioSelectorOutputTypeDef = TypedDict(
    "AudioSelectorOutputTypeDef",
    {
        "AudioDurationCorrection": AudioDurationCorrectionType,
        "CustomLanguageCode": str,
        "DefaultSelection": AudioDefaultSelectionType,
        "ExternalAudioFileInput": str,
        "HlsRenditionGroupSettings": HlsRenditionGroupSettingsOutputTypeDef,
        "LanguageCode": LanguageCodeType,
        "Offset": int,
        "Pids": List[int],
        "ProgramSelection": int,
        "RemixSettings": RemixSettingsOutputTypeDef,
        "SelectorType": AudioSelectorTypeType,
        "Tracks": List[int],
    },
)

AudioDescriptionTypeDef = TypedDict(
    "AudioDescriptionTypeDef",
    {
        "AudioChannelTaggingSettings": AudioChannelTaggingSettingsTypeDef,
        "AudioNormalizationSettings": AudioNormalizationSettingsTypeDef,
        "AudioSourceName": str,
        "AudioType": int,
        "AudioTypeControl": AudioTypeControlType,
        "CodecSettings": AudioCodecSettingsTypeDef,
        "CustomLanguageCode": str,
        "LanguageCode": LanguageCodeType,
        "LanguageCodeControl": AudioLanguageCodeControlType,
        "RemixSettings": RemixSettingsTypeDef,
        "StreamName": str,
    },
    total=False,
)

AudioSelectorTypeDef = TypedDict(
    "AudioSelectorTypeDef",
    {
        "AudioDurationCorrection": AudioDurationCorrectionType,
        "CustomLanguageCode": str,
        "DefaultSelection": AudioDefaultSelectionType,
        "ExternalAudioFileInput": str,
        "HlsRenditionGroupSettings": HlsRenditionGroupSettingsTypeDef,
        "LanguageCode": LanguageCodeType,
        "Offset": int,
        "Pids": Sequence[int],
        "ProgramSelection": int,
        "RemixSettings": RemixSettingsTypeDef,
        "SelectorType": AudioSelectorTypeType,
        "Tracks": Sequence[int],
    },
    total=False,
)

CmafGroupSettingsOutputTypeDef = TypedDict(
    "CmafGroupSettingsOutputTypeDef",
    {
        "AdditionalManifests": List[CmafAdditionalManifestOutputTypeDef],
        "BaseUrl": str,
        "ClientCache": CmafClientCacheType,
        "CodecSpecification": CmafCodecSpecificationType,
        "DashManifestStyle": DashManifestStyleType,
        "Destination": str,
        "DestinationSettings": DestinationSettingsOutputTypeDef,
        "Encryption": CmafEncryptionSettingsOutputTypeDef,
        "FragmentLength": int,
        "ImageBasedTrickPlay": CmafImageBasedTrickPlayType,
        "ImageBasedTrickPlaySettings": CmafImageBasedTrickPlaySettingsOutputTypeDef,
        "ManifestCompression": CmafManifestCompressionType,
        "ManifestDurationFormat": CmafManifestDurationFormatType,
        "MinBufferTime": int,
        "MinFinalSegmentLength": float,
        "MpdManifestBandwidthType": CmafMpdManifestBandwidthTypeType,
        "MpdProfile": CmafMpdProfileType,
        "PtsOffsetHandlingForBFrames": CmafPtsOffsetHandlingForBFramesType,
        "SegmentControl": CmafSegmentControlType,
        "SegmentLength": int,
        "SegmentLengthControl": CmafSegmentLengthControlType,
        "StreamInfResolution": CmafStreamInfResolutionType,
        "TargetDurationCompatibilityMode": CmafTargetDurationCompatibilityModeType,
        "VideoCompositionOffsets": CmafVideoCompositionOffsetsType,
        "WriteDashManifest": CmafWriteDASHManifestType,
        "WriteHlsManifest": CmafWriteHLSManifestType,
        "WriteSegmentTimelineInRepresentation": CmafWriteSegmentTimelineInRepresentationType,
    },
)

DashIsoGroupSettingsOutputTypeDef = TypedDict(
    "DashIsoGroupSettingsOutputTypeDef",
    {
        "AdditionalManifests": List[DashAdditionalManifestOutputTypeDef],
        "AudioChannelConfigSchemeIdUri": DashIsoGroupAudioChannelConfigSchemeIdUriType,
        "BaseUrl": str,
        "DashManifestStyle": DashManifestStyleType,
        "Destination": str,
        "DestinationSettings": DestinationSettingsOutputTypeDef,
        "Encryption": DashIsoEncryptionSettingsOutputTypeDef,
        "FragmentLength": int,
        "HbbtvCompliance": DashIsoHbbtvComplianceType,
        "ImageBasedTrickPlay": DashIsoImageBasedTrickPlayType,
        "ImageBasedTrickPlaySettings": DashIsoImageBasedTrickPlaySettingsOutputTypeDef,
        "MinBufferTime": int,
        "MinFinalSegmentLength": float,
        "MpdManifestBandwidthType": DashIsoMpdManifestBandwidthTypeType,
        "MpdProfile": DashIsoMpdProfileType,
        "PtsOffsetHandlingForBFrames": DashIsoPtsOffsetHandlingForBFramesType,
        "SegmentControl": DashIsoSegmentControlType,
        "SegmentLength": int,
        "SegmentLengthControl": DashIsoSegmentLengthControlType,
        "VideoCompositionOffsets": DashIsoVideoCompositionOffsetsType,
        "WriteSegmentTimelineInRepresentation": DashIsoWriteSegmentTimelineInRepresentationType,
    },
)

FileGroupSettingsOutputTypeDef = TypedDict(
    "FileGroupSettingsOutputTypeDef",
    {
        "Destination": str,
        "DestinationSettings": DestinationSettingsOutputTypeDef,
    },
)

HlsGroupSettingsOutputTypeDef = TypedDict(
    "HlsGroupSettingsOutputTypeDef",
    {
        "AdMarkers": List[HlsAdMarkersType],
        "AdditionalManifests": List[HlsAdditionalManifestOutputTypeDef],
        "AudioOnlyHeader": HlsAudioOnlyHeaderType,
        "BaseUrl": str,
        "CaptionLanguageMappings": List[HlsCaptionLanguageMappingOutputTypeDef],
        "CaptionLanguageSetting": HlsCaptionLanguageSettingType,
        "CaptionSegmentLengthControl": HlsCaptionSegmentLengthControlType,
        "ClientCache": HlsClientCacheType,
        "CodecSpecification": HlsCodecSpecificationType,
        "Destination": str,
        "DestinationSettings": DestinationSettingsOutputTypeDef,
        "DirectoryStructure": HlsDirectoryStructureType,
        "Encryption": HlsEncryptionSettingsOutputTypeDef,
        "ImageBasedTrickPlay": HlsImageBasedTrickPlayType,
        "ImageBasedTrickPlaySettings": HlsImageBasedTrickPlaySettingsOutputTypeDef,
        "ManifestCompression": HlsManifestCompressionType,
        "ManifestDurationFormat": HlsManifestDurationFormatType,
        "MinFinalSegmentLength": float,
        "MinSegmentLength": int,
        "OutputSelection": HlsOutputSelectionType,
        "ProgramDateTime": HlsProgramDateTimeType,
        "ProgramDateTimePeriod": int,
        "ProgressiveWriteHlsManifest": HlsProgressiveWriteHlsManifestType,
        "SegmentControl": HlsSegmentControlType,
        "SegmentLength": int,
        "SegmentLengthControl": HlsSegmentLengthControlType,
        "SegmentsPerSubdirectory": int,
        "StreamInfResolution": HlsStreamInfResolutionType,
        "TargetDurationCompatibilityMode": HlsTargetDurationCompatibilityModeType,
        "TimedMetadataId3Frame": HlsTimedMetadataId3FrameType,
        "TimedMetadataId3Period": int,
        "TimestampDeltaMilliseconds": int,
    },
)

MsSmoothGroupSettingsOutputTypeDef = TypedDict(
    "MsSmoothGroupSettingsOutputTypeDef",
    {
        "AdditionalManifests": List[MsSmoothAdditionalManifestOutputTypeDef],
        "AudioDeduplication": MsSmoothAudioDeduplicationType,
        "Destination": str,
        "DestinationSettings": DestinationSettingsOutputTypeDef,
        "Encryption": MsSmoothEncryptionSettingsOutputTypeDef,
        "FragmentLength": int,
        "FragmentLengthControl": MsSmoothFragmentLengthControlType,
        "ManifestEncoding": MsSmoothManifestEncodingType,
    },
)

CmafGroupSettingsTypeDef = TypedDict(
    "CmafGroupSettingsTypeDef",
    {
        "AdditionalManifests": Sequence[CmafAdditionalManifestTypeDef],
        "BaseUrl": str,
        "ClientCache": CmafClientCacheType,
        "CodecSpecification": CmafCodecSpecificationType,
        "DashManifestStyle": DashManifestStyleType,
        "Destination": str,
        "DestinationSettings": DestinationSettingsTypeDef,
        "Encryption": CmafEncryptionSettingsTypeDef,
        "FragmentLength": int,
        "ImageBasedTrickPlay": CmafImageBasedTrickPlayType,
        "ImageBasedTrickPlaySettings": CmafImageBasedTrickPlaySettingsTypeDef,
        "ManifestCompression": CmafManifestCompressionType,
        "ManifestDurationFormat": CmafManifestDurationFormatType,
        "MinBufferTime": int,
        "MinFinalSegmentLength": float,
        "MpdManifestBandwidthType": CmafMpdManifestBandwidthTypeType,
        "MpdProfile": CmafMpdProfileType,
        "PtsOffsetHandlingForBFrames": CmafPtsOffsetHandlingForBFramesType,
        "SegmentControl": CmafSegmentControlType,
        "SegmentLength": int,
        "SegmentLengthControl": CmafSegmentLengthControlType,
        "StreamInfResolution": CmafStreamInfResolutionType,
        "TargetDurationCompatibilityMode": CmafTargetDurationCompatibilityModeType,
        "VideoCompositionOffsets": CmafVideoCompositionOffsetsType,
        "WriteDashManifest": CmafWriteDASHManifestType,
        "WriteHlsManifest": CmafWriteHLSManifestType,
        "WriteSegmentTimelineInRepresentation": CmafWriteSegmentTimelineInRepresentationType,
    },
    total=False,
)

DashIsoGroupSettingsTypeDef = TypedDict(
    "DashIsoGroupSettingsTypeDef",
    {
        "AdditionalManifests": Sequence[DashAdditionalManifestTypeDef],
        "AudioChannelConfigSchemeIdUri": DashIsoGroupAudioChannelConfigSchemeIdUriType,
        "BaseUrl": str,
        "DashManifestStyle": DashManifestStyleType,
        "Destination": str,
        "DestinationSettings": DestinationSettingsTypeDef,
        "Encryption": DashIsoEncryptionSettingsTypeDef,
        "FragmentLength": int,
        "HbbtvCompliance": DashIsoHbbtvComplianceType,
        "ImageBasedTrickPlay": DashIsoImageBasedTrickPlayType,
        "ImageBasedTrickPlaySettings": DashIsoImageBasedTrickPlaySettingsTypeDef,
        "MinBufferTime": int,
        "MinFinalSegmentLength": float,
        "MpdManifestBandwidthType": DashIsoMpdManifestBandwidthTypeType,
        "MpdProfile": DashIsoMpdProfileType,
        "PtsOffsetHandlingForBFrames": DashIsoPtsOffsetHandlingForBFramesType,
        "SegmentControl": DashIsoSegmentControlType,
        "SegmentLength": int,
        "SegmentLengthControl": DashIsoSegmentLengthControlType,
        "VideoCompositionOffsets": DashIsoVideoCompositionOffsetsType,
        "WriteSegmentTimelineInRepresentation": DashIsoWriteSegmentTimelineInRepresentationType,
    },
    total=False,
)

FileGroupSettingsTypeDef = TypedDict(
    "FileGroupSettingsTypeDef",
    {
        "Destination": str,
        "DestinationSettings": DestinationSettingsTypeDef,
    },
    total=False,
)

HlsGroupSettingsTypeDef = TypedDict(
    "HlsGroupSettingsTypeDef",
    {
        "AdMarkers": Sequence[HlsAdMarkersType],
        "AdditionalManifests": Sequence[HlsAdditionalManifestTypeDef],
        "AudioOnlyHeader": HlsAudioOnlyHeaderType,
        "BaseUrl": str,
        "CaptionLanguageMappings": Sequence[HlsCaptionLanguageMappingTypeDef],
        "CaptionLanguageSetting": HlsCaptionLanguageSettingType,
        "CaptionSegmentLengthControl": HlsCaptionSegmentLengthControlType,
        "ClientCache": HlsClientCacheType,
        "CodecSpecification": HlsCodecSpecificationType,
        "Destination": str,
        "DestinationSettings": DestinationSettingsTypeDef,
        "DirectoryStructure": HlsDirectoryStructureType,
        "Encryption": HlsEncryptionSettingsTypeDef,
        "ImageBasedTrickPlay": HlsImageBasedTrickPlayType,
        "ImageBasedTrickPlaySettings": HlsImageBasedTrickPlaySettingsTypeDef,
        "ManifestCompression": HlsManifestCompressionType,
        "ManifestDurationFormat": HlsManifestDurationFormatType,
        "MinFinalSegmentLength": float,
        "MinSegmentLength": int,
        "OutputSelection": HlsOutputSelectionType,
        "ProgramDateTime": HlsProgramDateTimeType,
        "ProgramDateTimePeriod": int,
        "ProgressiveWriteHlsManifest": HlsProgressiveWriteHlsManifestType,
        "SegmentControl": HlsSegmentControlType,
        "SegmentLength": int,
        "SegmentLengthControl": HlsSegmentLengthControlType,
        "SegmentsPerSubdirectory": int,
        "StreamInfResolution": HlsStreamInfResolutionType,
        "TargetDurationCompatibilityMode": HlsTargetDurationCompatibilityModeType,
        "TimedMetadataId3Frame": HlsTimedMetadataId3FrameType,
        "TimedMetadataId3Period": int,
        "TimestampDeltaMilliseconds": int,
    },
    total=False,
)

MsSmoothGroupSettingsTypeDef = TypedDict(
    "MsSmoothGroupSettingsTypeDef",
    {
        "AdditionalManifests": Sequence[MsSmoothAdditionalManifestTypeDef],
        "AudioDeduplication": MsSmoothAudioDeduplicationType,
        "Destination": str,
        "DestinationSettings": DestinationSettingsTypeDef,
        "Encryption": MsSmoothEncryptionSettingsTypeDef,
        "FragmentLength": int,
        "FragmentLengthControl": MsSmoothFragmentLengthControlType,
        "ManifestEncoding": MsSmoothManifestEncodingType,
    },
    total=False,
)

VideoDescriptionOutputTypeDef = TypedDict(
    "VideoDescriptionOutputTypeDef",
    {
        "AfdSignaling": AfdSignalingType,
        "AntiAlias": AntiAliasType,
        "CodecSettings": VideoCodecSettingsOutputTypeDef,
        "ColorMetadata": ColorMetadataType,
        "Crop": RectangleOutputTypeDef,
        "DropFrameTimecode": DropFrameTimecodeType,
        "FixedAfd": int,
        "Height": int,
        "Position": RectangleOutputTypeDef,
        "RespondToAfd": RespondToAfdType,
        "ScalingBehavior": ScalingBehaviorType,
        "Sharpness": int,
        "TimecodeInsertion": VideoTimecodeInsertionType,
        "VideoPreprocessors": VideoPreprocessorOutputTypeDef,
        "Width": int,
    },
)

VideoDescriptionTypeDef = TypedDict(
    "VideoDescriptionTypeDef",
    {
        "AfdSignaling": AfdSignalingType,
        "AntiAlias": AntiAliasType,
        "CodecSettings": VideoCodecSettingsTypeDef,
        "ColorMetadata": ColorMetadataType,
        "Crop": RectangleTypeDef,
        "DropFrameTimecode": DropFrameTimecodeType,
        "FixedAfd": int,
        "Height": int,
        "Position": RectangleTypeDef,
        "RespondToAfd": RespondToAfdType,
        "ScalingBehavior": ScalingBehaviorType,
        "Sharpness": int,
        "TimecodeInsertion": VideoTimecodeInsertionType,
        "VideoPreprocessors": VideoPreprocessorTypeDef,
        "Width": int,
    },
    total=False,
)

InputOutputTypeDef = TypedDict(
    "InputOutputTypeDef",
    {
        "AdvancedInputFilter": AdvancedInputFilterType,
        "AdvancedInputFilterSettings": AdvancedInputFilterSettingsOutputTypeDef,
        "AudioSelectorGroups": Dict[str, AudioSelectorGroupOutputTypeDef],
        "AudioSelectors": Dict[str, AudioSelectorOutputTypeDef],
        "CaptionSelectors": Dict[str, CaptionSelectorOutputTypeDef],
        "Crop": RectangleOutputTypeDef,
        "DeblockFilter": InputDeblockFilterType,
        "DecryptionSettings": InputDecryptionSettingsOutputTypeDef,
        "DenoiseFilter": InputDenoiseFilterType,
        "DolbyVisionMetadataXml": str,
        "FileInput": str,
        "FilterEnable": InputFilterEnableType,
        "FilterStrength": int,
        "ImageInserter": ImageInserterOutputTypeDef,
        "InputClippings": List[InputClippingOutputTypeDef],
        "InputScanType": InputScanTypeType,
        "Position": RectangleOutputTypeDef,
        "ProgramNumber": int,
        "PsiControl": InputPsiControlType,
        "SupplementalImps": List[str],
        "TimecodeSource": InputTimecodeSourceType,
        "TimecodeStart": str,
        "VideoGenerator": InputVideoGeneratorOutputTypeDef,
        "VideoSelector": VideoSelectorOutputTypeDef,
    },
)

InputTemplateOutputTypeDef = TypedDict(
    "InputTemplateOutputTypeDef",
    {
        "AdvancedInputFilter": AdvancedInputFilterType,
        "AdvancedInputFilterSettings": AdvancedInputFilterSettingsOutputTypeDef,
        "AudioSelectorGroups": Dict[str, AudioSelectorGroupOutputTypeDef],
        "AudioSelectors": Dict[str, AudioSelectorOutputTypeDef],
        "CaptionSelectors": Dict[str, CaptionSelectorOutputTypeDef],
        "Crop": RectangleOutputTypeDef,
        "DeblockFilter": InputDeblockFilterType,
        "DenoiseFilter": InputDenoiseFilterType,
        "DolbyVisionMetadataXml": str,
        "FilterEnable": InputFilterEnableType,
        "FilterStrength": int,
        "ImageInserter": ImageInserterOutputTypeDef,
        "InputClippings": List[InputClippingOutputTypeDef],
        "InputScanType": InputScanTypeType,
        "Position": RectangleOutputTypeDef,
        "ProgramNumber": int,
        "PsiControl": InputPsiControlType,
        "TimecodeSource": InputTimecodeSourceType,
        "TimecodeStart": str,
        "VideoSelector": VideoSelectorOutputTypeDef,
    },
)

InputTemplateTypeDef = TypedDict(
    "InputTemplateTypeDef",
    {
        "AdvancedInputFilter": AdvancedInputFilterType,
        "AdvancedInputFilterSettings": AdvancedInputFilterSettingsTypeDef,
        "AudioSelectorGroups": Mapping[str, AudioSelectorGroupTypeDef],
        "AudioSelectors": Mapping[str, AudioSelectorTypeDef],
        "CaptionSelectors": Mapping[str, CaptionSelectorTypeDef],
        "Crop": RectangleTypeDef,
        "DeblockFilter": InputDeblockFilterType,
        "DenoiseFilter": InputDenoiseFilterType,
        "DolbyVisionMetadataXml": str,
        "FilterEnable": InputFilterEnableType,
        "FilterStrength": int,
        "ImageInserter": ImageInserterTypeDef,
        "InputClippings": Sequence[InputClippingTypeDef],
        "InputScanType": InputScanTypeType,
        "Position": RectangleTypeDef,
        "ProgramNumber": int,
        "PsiControl": InputPsiControlType,
        "TimecodeSource": InputTimecodeSourceType,
        "TimecodeStart": str,
        "VideoSelector": VideoSelectorTypeDef,
    },
    total=False,
)

InputTypeDef = TypedDict(
    "InputTypeDef",
    {
        "AdvancedInputFilter": AdvancedInputFilterType,
        "AdvancedInputFilterSettings": AdvancedInputFilterSettingsTypeDef,
        "AudioSelectorGroups": Mapping[str, AudioSelectorGroupTypeDef],
        "AudioSelectors": Mapping[str, AudioSelectorTypeDef],
        "CaptionSelectors": Mapping[str, CaptionSelectorTypeDef],
        "Crop": RectangleTypeDef,
        "DeblockFilter": InputDeblockFilterType,
        "DecryptionSettings": InputDecryptionSettingsTypeDef,
        "DenoiseFilter": InputDenoiseFilterType,
        "DolbyVisionMetadataXml": str,
        "FileInput": str,
        "FilterEnable": InputFilterEnableType,
        "FilterStrength": int,
        "ImageInserter": ImageInserterTypeDef,
        "InputClippings": Sequence[InputClippingTypeDef],
        "InputScanType": InputScanTypeType,
        "Position": RectangleTypeDef,
        "ProgramNumber": int,
        "PsiControl": InputPsiControlType,
        "SupplementalImps": Sequence[str],
        "TimecodeSource": InputTimecodeSourceType,
        "TimecodeStart": str,
        "VideoGenerator": InputVideoGeneratorTypeDef,
        "VideoSelector": VideoSelectorTypeDef,
    },
    total=False,
)

OutputGroupSettingsOutputTypeDef = TypedDict(
    "OutputGroupSettingsOutputTypeDef",
    {
        "CmafGroupSettings": CmafGroupSettingsOutputTypeDef,
        "DashIsoGroupSettings": DashIsoGroupSettingsOutputTypeDef,
        "FileGroupSettings": FileGroupSettingsOutputTypeDef,
        "HlsGroupSettings": HlsGroupSettingsOutputTypeDef,
        "MsSmoothGroupSettings": MsSmoothGroupSettingsOutputTypeDef,
        "Type": OutputGroupTypeType,
    },
)

OutputGroupSettingsTypeDef = TypedDict(
    "OutputGroupSettingsTypeDef",
    {
        "CmafGroupSettings": CmafGroupSettingsTypeDef,
        "DashIsoGroupSettings": DashIsoGroupSettingsTypeDef,
        "FileGroupSettings": FileGroupSettingsTypeDef,
        "HlsGroupSettings": HlsGroupSettingsTypeDef,
        "MsSmoothGroupSettings": MsSmoothGroupSettingsTypeDef,
        "Type": OutputGroupTypeType,
    },
    total=False,
)

OutputTypeDef = TypedDict(
    "OutputTypeDef",
    {
        "AudioDescriptions": List[AudioDescriptionOutputTypeDef],
        "CaptionDescriptions": List[CaptionDescriptionOutputTypeDef],
        "ContainerSettings": ContainerSettingsOutputTypeDef,
        "Extension": str,
        "NameModifier": str,
        "OutputSettings": OutputSettingsOutputTypeDef,
        "Preset": str,
        "VideoDescription": VideoDescriptionOutputTypeDef,
    },
)

PresetSettingsOutputTypeDef = TypedDict(
    "PresetSettingsOutputTypeDef",
    {
        "AudioDescriptions": List[AudioDescriptionOutputTypeDef],
        "CaptionDescriptions": List[CaptionDescriptionPresetOutputTypeDef],
        "ContainerSettings": ContainerSettingsOutputTypeDef,
        "VideoDescription": VideoDescriptionOutputTypeDef,
    },
)

PresetSettingsTypeDef = TypedDict(
    "PresetSettingsTypeDef",
    {
        "AudioDescriptions": Sequence[AudioDescriptionTypeDef],
        "CaptionDescriptions": Sequence[CaptionDescriptionPresetTypeDef],
        "ContainerSettings": ContainerSettingsTypeDef,
        "VideoDescription": VideoDescriptionTypeDef,
    },
    total=False,
)

OutputGroupOutputTypeDef = TypedDict(
    "OutputGroupOutputTypeDef",
    {
        "AutomatedEncodingSettings": AutomatedEncodingSettingsOutputTypeDef,
        "CustomName": str,
        "Name": str,
        "OutputGroupSettings": OutputGroupSettingsOutputTypeDef,
        "Outputs": List[OutputTypeDef],
    },
)

OutputGroupTypeDef = TypedDict(
    "OutputGroupTypeDef",
    {
        "AutomatedEncodingSettings": AutomatedEncodingSettingsTypeDef,
        "CustomName": str,
        "Name": str,
        "OutputGroupSettings": OutputGroupSettingsTypeDef,
        "Outputs": Sequence[OutputTypeDef],
    },
    total=False,
)

PresetTypeDef = TypedDict(
    "PresetTypeDef",
    {
        "Arn": str,
        "Category": str,
        "CreatedAt": datetime,
        "Description": str,
        "LastUpdated": datetime,
        "Name": str,
        "Settings": PresetSettingsOutputTypeDef,
        "Type": TypeType,
    },
)

_RequiredCreatePresetRequestRequestTypeDef = TypedDict(
    "_RequiredCreatePresetRequestRequestTypeDef",
    {
        "Name": str,
        "Settings": PresetSettingsTypeDef,
    },
)
_OptionalCreatePresetRequestRequestTypeDef = TypedDict(
    "_OptionalCreatePresetRequestRequestTypeDef",
    {
        "Category": str,
        "Description": str,
        "Tags": Mapping[str, str],
    },
    total=False,
)

class CreatePresetRequestRequestTypeDef(
    _RequiredCreatePresetRequestRequestTypeDef, _OptionalCreatePresetRequestRequestTypeDef
):
    pass

_RequiredUpdatePresetRequestRequestTypeDef = TypedDict(
    "_RequiredUpdatePresetRequestRequestTypeDef",
    {
        "Name": str,
    },
)
_OptionalUpdatePresetRequestRequestTypeDef = TypedDict(
    "_OptionalUpdatePresetRequestRequestTypeDef",
    {
        "Category": str,
        "Description": str,
        "Settings": PresetSettingsTypeDef,
    },
    total=False,
)

class UpdatePresetRequestRequestTypeDef(
    _RequiredUpdatePresetRequestRequestTypeDef, _OptionalUpdatePresetRequestRequestTypeDef
):
    pass

JobSettingsOutputTypeDef = TypedDict(
    "JobSettingsOutputTypeDef",
    {
        "AdAvailOffset": int,
        "AvailBlanking": AvailBlankingOutputTypeDef,
        "Esam": EsamSettingsOutputTypeDef,
        "ExtendedDataServices": ExtendedDataServicesOutputTypeDef,
        "Inputs": List[InputOutputTypeDef],
        "KantarWatermark": KantarWatermarkSettingsOutputTypeDef,
        "MotionImageInserter": MotionImageInserterOutputTypeDef,
        "NielsenConfiguration": NielsenConfigurationOutputTypeDef,
        "NielsenNonLinearWatermark": NielsenNonLinearWatermarkSettingsOutputTypeDef,
        "OutputGroups": List[OutputGroupOutputTypeDef],
        "TimecodeConfig": TimecodeConfigOutputTypeDef,
        "TimedMetadataInsertion": TimedMetadataInsertionOutputTypeDef,
    },
)

JobTemplateSettingsOutputTypeDef = TypedDict(
    "JobTemplateSettingsOutputTypeDef",
    {
        "AdAvailOffset": int,
        "AvailBlanking": AvailBlankingOutputTypeDef,
        "Esam": EsamSettingsOutputTypeDef,
        "ExtendedDataServices": ExtendedDataServicesOutputTypeDef,
        "Inputs": List[InputTemplateOutputTypeDef],
        "KantarWatermark": KantarWatermarkSettingsOutputTypeDef,
        "MotionImageInserter": MotionImageInserterOutputTypeDef,
        "NielsenConfiguration": NielsenConfigurationOutputTypeDef,
        "NielsenNonLinearWatermark": NielsenNonLinearWatermarkSettingsOutputTypeDef,
        "OutputGroups": List[OutputGroupOutputTypeDef],
        "TimecodeConfig": TimecodeConfigOutputTypeDef,
        "TimedMetadataInsertion": TimedMetadataInsertionOutputTypeDef,
    },
)

JobSettingsTypeDef = TypedDict(
    "JobSettingsTypeDef",
    {
        "AdAvailOffset": int,
        "AvailBlanking": AvailBlankingTypeDef,
        "Esam": EsamSettingsTypeDef,
        "ExtendedDataServices": ExtendedDataServicesTypeDef,
        "Inputs": Sequence[InputTypeDef],
        "KantarWatermark": KantarWatermarkSettingsTypeDef,
        "MotionImageInserter": MotionImageInserterTypeDef,
        "NielsenConfiguration": NielsenConfigurationTypeDef,
        "NielsenNonLinearWatermark": NielsenNonLinearWatermarkSettingsTypeDef,
        "OutputGroups": Sequence[OutputGroupTypeDef],
        "TimecodeConfig": TimecodeConfigTypeDef,
        "TimedMetadataInsertion": TimedMetadataInsertionTypeDef,
    },
    total=False,
)

JobTemplateSettingsTypeDef = TypedDict(
    "JobTemplateSettingsTypeDef",
    {
        "AdAvailOffset": int,
        "AvailBlanking": AvailBlankingTypeDef,
        "Esam": EsamSettingsTypeDef,
        "ExtendedDataServices": ExtendedDataServicesTypeDef,
        "Inputs": Sequence[InputTemplateTypeDef],
        "KantarWatermark": KantarWatermarkSettingsTypeDef,
        "MotionImageInserter": MotionImageInserterTypeDef,
        "NielsenConfiguration": NielsenConfigurationTypeDef,
        "NielsenNonLinearWatermark": NielsenNonLinearWatermarkSettingsTypeDef,
        "OutputGroups": Sequence[OutputGroupTypeDef],
        "TimecodeConfig": TimecodeConfigTypeDef,
        "TimedMetadataInsertion": TimedMetadataInsertionTypeDef,
    },
    total=False,
)

CreatePresetResponseTypeDef = TypedDict(
    "CreatePresetResponseTypeDef",
    {
        "Preset": PresetTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetPresetResponseTypeDef = TypedDict(
    "GetPresetResponseTypeDef",
    {
        "Preset": PresetTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListPresetsResponseTypeDef = TypedDict(
    "ListPresetsResponseTypeDef",
    {
        "NextToken": str,
        "Presets": List[PresetTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdatePresetResponseTypeDef = TypedDict(
    "UpdatePresetResponseTypeDef",
    {
        "Preset": PresetTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

JobTypeDef = TypedDict(
    "JobTypeDef",
    {
        "AccelerationSettings": AccelerationSettingsOutputTypeDef,
        "AccelerationStatus": AccelerationStatusType,
        "Arn": str,
        "BillingTagsSource": BillingTagsSourceType,
        "ClientRequestToken": str,
        "CreatedAt": datetime,
        "CurrentPhase": JobPhaseType,
        "ErrorCode": int,
        "ErrorMessage": str,
        "HopDestinations": List[HopDestinationOutputTypeDef],
        "Id": str,
        "JobPercentComplete": int,
        "JobTemplate": str,
        "Messages": JobMessagesTypeDef,
        "OutputGroupDetails": List[OutputGroupDetailTypeDef],
        "Priority": int,
        "Queue": str,
        "QueueTransitions": List[QueueTransitionTypeDef],
        "RetryCount": int,
        "Role": str,
        "Settings": JobSettingsOutputTypeDef,
        "SimulateReservedQueue": SimulateReservedQueueType,
        "Status": JobStatusType,
        "StatusUpdateInterval": StatusUpdateIntervalType,
        "Timing": TimingTypeDef,
        "UserMetadata": Dict[str, str],
        "Warnings": List[WarningGroupTypeDef],
    },
)

JobTemplateTypeDef = TypedDict(
    "JobTemplateTypeDef",
    {
        "AccelerationSettings": AccelerationSettingsOutputTypeDef,
        "Arn": str,
        "Category": str,
        "CreatedAt": datetime,
        "Description": str,
        "HopDestinations": List[HopDestinationOutputTypeDef],
        "LastUpdated": datetime,
        "Name": str,
        "Priority": int,
        "Queue": str,
        "Settings": JobTemplateSettingsOutputTypeDef,
        "StatusUpdateInterval": StatusUpdateIntervalType,
        "Type": TypeType,
    },
)

_RequiredCreateJobRequestRequestTypeDef = TypedDict(
    "_RequiredCreateJobRequestRequestTypeDef",
    {
        "Role": str,
        "Settings": JobSettingsTypeDef,
    },
)
_OptionalCreateJobRequestRequestTypeDef = TypedDict(
    "_OptionalCreateJobRequestRequestTypeDef",
    {
        "AccelerationSettings": AccelerationSettingsTypeDef,
        "BillingTagsSource": BillingTagsSourceType,
        "ClientRequestToken": str,
        "HopDestinations": Sequence[HopDestinationTypeDef],
        "JobTemplate": str,
        "Priority": int,
        "Queue": str,
        "SimulateReservedQueue": SimulateReservedQueueType,
        "StatusUpdateInterval": StatusUpdateIntervalType,
        "Tags": Mapping[str, str],
        "UserMetadata": Mapping[str, str],
    },
    total=False,
)

class CreateJobRequestRequestTypeDef(
    _RequiredCreateJobRequestRequestTypeDef, _OptionalCreateJobRequestRequestTypeDef
):
    pass

_RequiredCreateJobTemplateRequestRequestTypeDef = TypedDict(
    "_RequiredCreateJobTemplateRequestRequestTypeDef",
    {
        "Name": str,
        "Settings": JobTemplateSettingsTypeDef,
    },
)
_OptionalCreateJobTemplateRequestRequestTypeDef = TypedDict(
    "_OptionalCreateJobTemplateRequestRequestTypeDef",
    {
        "AccelerationSettings": AccelerationSettingsTypeDef,
        "Category": str,
        "Description": str,
        "HopDestinations": Sequence[HopDestinationTypeDef],
        "Priority": int,
        "Queue": str,
        "StatusUpdateInterval": StatusUpdateIntervalType,
        "Tags": Mapping[str, str],
    },
    total=False,
)

class CreateJobTemplateRequestRequestTypeDef(
    _RequiredCreateJobTemplateRequestRequestTypeDef, _OptionalCreateJobTemplateRequestRequestTypeDef
):
    pass

_RequiredUpdateJobTemplateRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateJobTemplateRequestRequestTypeDef",
    {
        "Name": str,
    },
)
_OptionalUpdateJobTemplateRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateJobTemplateRequestRequestTypeDef",
    {
        "AccelerationSettings": AccelerationSettingsTypeDef,
        "Category": str,
        "Description": str,
        "HopDestinations": Sequence[HopDestinationTypeDef],
        "Priority": int,
        "Queue": str,
        "Settings": JobTemplateSettingsTypeDef,
        "StatusUpdateInterval": StatusUpdateIntervalType,
    },
    total=False,
)

class UpdateJobTemplateRequestRequestTypeDef(
    _RequiredUpdateJobTemplateRequestRequestTypeDef, _OptionalUpdateJobTemplateRequestRequestTypeDef
):
    pass

CreateJobResponseTypeDef = TypedDict(
    "CreateJobResponseTypeDef",
    {
        "Job": JobTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetJobResponseTypeDef = TypedDict(
    "GetJobResponseTypeDef",
    {
        "Job": JobTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListJobsResponseTypeDef = TypedDict(
    "ListJobsResponseTypeDef",
    {
        "Jobs": List[JobTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateJobTemplateResponseTypeDef = TypedDict(
    "CreateJobTemplateResponseTypeDef",
    {
        "JobTemplate": JobTemplateTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetJobTemplateResponseTypeDef = TypedDict(
    "GetJobTemplateResponseTypeDef",
    {
        "JobTemplate": JobTemplateTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListJobTemplatesResponseTypeDef = TypedDict(
    "ListJobTemplatesResponseTypeDef",
    {
        "JobTemplates": List[JobTemplateTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateJobTemplateResponseTypeDef = TypedDict(
    "UpdateJobTemplateResponseTypeDef",
    {
        "JobTemplate": JobTemplateTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
