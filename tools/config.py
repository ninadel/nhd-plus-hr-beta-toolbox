# names of objects in the NHD dataset that are used by this tool
# names of objects in the NHD dataset that are used by this tool
original_dataset_name = 'Hydrography'
original_nhdflowline_name = 'NHDFlowline'
original_vaatable_name = 'NHDPlusFlowlineVAA'

# names of resulting objects
# these may become user defined parameters in the future
result_suffix = '_RESULT'
result_dataset_name = 'Tributaries'
result_startfeatures_segments_fcname = 'StartFeatures_Segments'
result_startfeatures_dissolved_fcname = 'StartFeatures_Streams'
result_tributaries_segments_fcname = 'Tributaries_Segments'
result_tributaries_dissolved_fcname = 'Tributaries_Streams'

# fields from NHDPlusFlowlineVAA that are used in filtering and aggregation
vaa_segment_fields = [
    # [FieldName, FieldDataType, FieldAlias]
    ['StreamLeve', "SHORT", 'StreamLevel'],
    ['HydroSeq', "DOUBLE", 'HydrologicSequence'],
    ['LevelPathI', "DOUBLE", 'LevelPathIdentifier'],
    ['TerminalPa', "DOUBLE", 'TerminalPathIdentifier'],
    ['UpLevelPat', "DOUBLE", 'UpstreamMainPathLevelPathID'],
    ['UpHydroSeq', "DOUBLE", 'UpstreamMainPathHydroSeq'],
    ['DnLevel', "SHORT", 'DownstreamMainPathStreamLevel'],
    ['DnLevelPat', "DOUBLE", 'DownstreamMainPathLevelPathID'],
    ['DnHydroSeq', "DOUBLE", 'DownstreamMainPathHydroSeq']
]

# names of created result fields
fcode_gnisid_fields = [
    ['G46000', "SHORT", 'GNISID_ContainsFCode46000'],
    ['G46003', "SHORT", 'GNISID_ContainsFCode46003'],
    ['G46006', "SHORT", 'GNISID_ContainsFCode46006'],
    ['G46007', "SHORT", 'GNISID_ContainsFCode46007'],
    ['G55800', "SHORT", 'GNISID_ContainsFCode55800']
]

fcode_pathid_fields = [
    ['P46000', "SHORT", 'Path_ContainsFCode46000'],
    ['P46003', "SHORT", 'Path_ContainsFCode46003'],
    ['P46006', "SHORT", 'Path_ContainsFCode46006'],
    ['P46007', "SHORT", 'Path_ContainsFCode46007'],
    ['P55800', "SHORT", 'Path_ContainsFCode55800']
]

# names of fields that are dissolved on
dissolve_fields = [
    'GNIS_ID',
    'GNIS_Name',
    'StreamLeve',
    'LevelPathI',
    'G46000',
    'G46003',
    'G46006',
    'G46007',
    'G55800',
    'P46000',
    'P46003',
    'P46006',
    'P46007',
    'P55800'
]