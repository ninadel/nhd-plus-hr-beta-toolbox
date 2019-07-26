# NHD Plus HR Tributary Finder v5
# Author: Nina del Rosario
# Last updated: 5/2/19
# Dataset description: https://www.usgs.gov/core-science-systems/ngp/national-hydrography/nhdplus-high-resolution
# Status: Revising from v4 (integrating all parameters, adding pre-checks, adding documentation notes)
#
# The purpose of this script is to select a tributary stream network based on a stream shapefile of starting features.
#
# The input parameters are:
#   parameter_output_location - workspace where results will be saved
#   parameter_gdb_location - geodatabase location of NHD Plus HR data
#   parameter_start_feature - linear feature class or shapefile of streams
#   parameter_all_levels - search tributaries in all StreamLevels?
#   parameter_max_level - if parameter_all_levels is false, what is the highest StreamLevel to include?
#   parameter_dissolve_streams - should stream segments be dissolved into streams (dissolved based on LevelPathI)?
#
# Requirements:
# parameter_gdb_location must point to a GDB from the NHD Plus HR data dataset (unzipped vector data)
# parameter_gdb_location must have a NHDPlusFlowlineVAA file geodatabase table
# NHDPlusFlowlineVAA must have populated data in the following fields:
#   HydroSeq, LevelPathI, TerminalPa, UpLevelPat, UpHydroSeq, DnLevel, DnLevelPat, DnHydroSeq
#   Datasets prior to NHD Plus HR have a few of the above fields unpopulated
# parameter_start_feature must have originated from the same dataset as parameter_gdb_location (NHD Plus HR)
#   finding tributaries will be dependent on selecting segments in parameter_gdb_location/Hydrography/NHDFlowline which coincide (share a line segment) with parameter_start_feature
# parameter_start_feature must have an overlapping extent with parameter_gdb_location/Hydrography/NHDFlowline
#
# This script will generate:
#   A folder in the workspace with the name NHDPLUS_H_[HUC4]_HU4_GDD_RESULT where HUC4 is the 4-digit HUC4 from parameter_gdb_location
#   A geodatabase in the above folder with the name NHDPLUS_H_[HUC4]_HU4_GDD_RESULT.gdb where HUC4 is the 4-digit HUC4 from parameter_gdb_location
#   A feature class in the above geodatabase named StartFeatures_Segments
#   A feature class in the above geodatabase named StartFeatures_Streams  (if parameter_dissolve_streams is true)
#   A feature dataset in the above geodatabase named Tributaries (if tributaries are found)
#   A feature class in the above dataset named Tributaries_Segments
#   A feature class in the above dataset named Tributaries_Segments (if parameter_dissolve_streams is true)
#   The feature classes generated will have added fields based on vaa_segment_fields, fcode_gnisid_fields, and fcode_pathid_fields

import arcpy, os, time

### START GLOBAL PARAMETERS ###
parameter_output_location = 'C:/Workspace/'
parameter_gdb_location = 'E:/GCMRC/NHD Plus HR Process Datasets/00 Original Files/NHDPLUS_H_1507_HU4_GDB/NHDPLUS_H_1507_HU4_GDB.gdb'
parameter_start_feature = 'E:/GCMRC/NHD Plus HR Process Datasets/Basin 15 Start Features/start_features_1507.shp'
parameter_all_levels = False
parameter_max_level = 7
parameter_dissolve_streams = True

arcpy.env.workspace = parameter_output_location

original_dataset_name = 'Hydrography'
original_nhdflowline_name = 'NHDFlowline'
original_vaatable_name = 'NHDPlusFlowlineVAA'

result_suffix = '_RESULT'
result_dataset_name = 'Tributaries'
result_startfeatures_segments_fcname = 'StartFeatures_Segments'
result_startfeatures_dissolved_fcname = 'StartFeatures_Streams'
result_tributaries_segments_fcname = 'Tributaries_Segments'
result_tributaries_dissolved_fcname = 'Tributaries_Streams'

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

### END GLOBAL PARAMETERS ###
### START FUNCTIONS ###

# given a file or feature class name, returns the path
def get_location(parent, fname, extension = '', dir_slash = '/'):
    location = parent + dir_slash + fname + extension
    return location

# given a path, returns a feature class name (strips file extension if there is one)
def get_fname(location):
    fname = location[location.rfind('/') + 1::]
    if '.' in fname:
        fname = fname[0:fname.rfind('.')]
    return fname

# given a feature class, returns a list of NHDPlusIDs
def get_nhdplusids(fc):
    ids = []
    with arcpy.da.SearchCursor(fc, ['NHDPlusID']) as s_cur:
        for row in s_cur:
            ids.append(int(row[0]))
    return ids

# takes start features, finds matching features in input feature class
def find_start_features(inputfc_location, startfeatures_location, output_location):
    inputfc_name = get_fname(inputfc_location)
    arcpy.MakeFeatureLayer_management(
        in_features=inputfc_location,
        out_layer=inputfc_name)
    ## test case - no start features
    arcpy.SelectLayerByLocation_management(
        in_layer=inputfc_name,
        overlap_type='SHARE_A_LINE_SEGMENT_WITH',
        select_features=startfeatures_location)
    ## test case - if there are start features
    if int(arcpy.GetCount_management(inputfc_name)[0]) > 0:
        start_nhdplusids = get_nhdplusids(inputfc_name)
    else:
        start_nhdplusids = []
    arcpy.SelectLayerByAttribute_management(
        in_layer_or_view=inputfc_name,
        selection_type="CLEAR_SELECTION")
    return start_nhdplusids

# exports features matching NHDPlusIDs to GDB
def export_start_features(inputfc_location, start_nhdplusid_list, output_location):
    inputfc_name = get_fname(inputfc_location)
    outputfile_name = get_fname(output_location)
    arcpy.SelectLayerByAttribute_management(
        in_layer_or_view=inputfc_name,
        selection_type="CLEAR_SELECTION")
    start_nhdplusid_list_str = '(' + ', '.join([str(int(i)) for i in start_nhdplusid_list]) + ')'
    where_clause_str = 'NHDPlusID IN ' + start_nhdplusid_list_str
    arcpy.SelectLayerByAttribute_management(
        in_layer_or_view=inputfc_name,
        selection_type="NEW_SELECTION",
        where_clause=where_clause_str)
    arcpy.CopyFeatures_management(
        in_features=inputfc_name,
        out_feature_class=output_location)
    arcpy.SelectLayerByAttribute_management(
        in_layer_or_view=inputfc_name,
        selection_type="CLEAR_SELECTION")
    print(outputfile_name + ' created successfully')


# given NHDPlusIDs of start features, looks at values in vaa table and returns 3 lists:
# start_features_hydroseq_list: list of HydroSeq values for start features
# vaa_path_list: list of LevelPathI where LevelPathI and DnLevelPat are different (not continuation) and item format = [StreamLeve, LevelPathI, DnLevelPat]
# vaa_hydroseq_list: list of HydroSeq where LevelPathI and DnLevelPat are different (not continuation) and item format where = [StreamLeve, LevelPathI, DnLevelPat, DnHydroSeq]
def get_vaa_lists(fc, table_location, start_ids, all_levels, max_level):
    table_name = get_fname(table_location)
    arcpy.SelectLayerByAttribute_management(
        in_layer_or_view=fc,
        selection_type="CLEAR_SELECTION")
    arcpy.AddJoin_management(
        in_layer_or_view=fc,
        in_field="NHDPlusID",
        join_table=table_location,
        join_field="NHDPlusID",
        join_type="KEEP_COMMON")
    vaa_path_list = []
    vaa_hydroseq_list = []
    start_features_hydroseq_list = []
    with arcpy.da.SearchCursor(fc,
                               ['{0}.StreamLeve'.format(table_name),
                                '{0}.NHDPlusID'.format(table_name),
                                '{0}.HydroSeq'.format(table_name),
                                '{0}.LevelPathI'.format(table_name),
                                '{0}.DnLevelPat'.format(table_name),
                                '{0}.DnHydroSeq'.format(table_name)]) as s_cur:
        for row in s_cur:
            StreamLeve = row[0]
            NHDPlusID = row[1]
            HydroSeq = row[2]
            LevelPathI = row[3]
            DnLevelPat = row[4]
            DnHydroSeq = row[5]
            if all_levels or (not all_levels and StreamLeve <= max_level):
                if int(NHDPlusID) in start_ids:
                    start_features_hydroseq_list.append(HydroSeq)
                if LevelPathI != DnLevelPat:
                    vaa_paths_row = [StreamLeve, LevelPathI, DnLevelPat]
                    if vaa_paths_row not in vaa_path_list:
                        vaa_path_list.append(vaa_paths_row)
                    vaa_hydroseq_row = [StreamLeve, LevelPathI, DnLevelPat, DnHydroSeq]
                    if vaa_hydroseq_row not in vaa_hydroseq_list:
                        vaa_hydroseq_list.append(vaa_hydroseq_row)
    arcpy.RemoveJoin_management(in_layer_or_view=fc)
    return start_features_hydroseq_list, vaa_path_list, vaa_hydroseq_list

# finds a list of starting tributaries: LevelPathI that have a DnHydroSeq in start_hydroseq_list
def get_starting_tributaries(start_hydroseq_list, vaa_hydroseq_list):
    # vaa_hydroseq_row = [StreamLeve, LevelPathI, DnLevelPat, DnHydroSeq]
    path_id_list = [i[1] for i in list(filter(lambda x: x[3] in start_hydroseq_list, vaa_hydroseq_list))]
    return path_id_list

# finds a list of primary tributaries for tributary_path_id_list
def get_primary_tributaries_from_path(tributary_path_id_list, vaa_path_list):
    # vaa_path row = [StreamLeve, LevelPathI, DnLevelPat, DnHydroSeq]
    path_id_list = [i[1] for i in list(filter(lambda x: x[2] in tributary_path_id_list, vaa_path_list))]
    return path_id_list

# finds all upstream tributaries from starting_tributaries
def get_all_tributaries_from_path(starting_tributaries, downstream_path_list):
    # copy starting_tributaries list
    input_features = starting_tributaries[:]
    # copy starting_tributaries list
    path_id_list = starting_tributaries[:]
    continue_search = True
    while continue_search:
        input_features = get_primary_tributaries_from_path(input_features, downstream_path_list)
        if len(input_features) == 0:
            continue_search = False
        else:
            path_id_list.extend(input_features)
    return path_id_list

# exports tributary segments to output dataset
def export_matching_paths(inputfc, vaa_table_location, all_tributaries_path_list, output_location):
    all_tributaries_path_list_str = '(' + ', '.join([str(int(i)) for i in all_tributaries_path_list]) + ')'
    arcpy.AddJoin_management(
        in_layer_or_view=inputfc,
        in_field="NHDPlusID",
        join_table=vaa_table_location,
        join_field="NHDPlusID",
        join_type="KEEP_COMMON")
    vaa_table_name = vaa_table_location[vaa_table_location.rfind('/') + 1::]
    where_clause_str = vaa_table_name + '.LevelPathI IN ' + all_tributaries_path_list_str
    arcpy.SelectLayerByAttribute_management(
        in_layer_or_view=inputfc,
        selection_type="NEW_SELECTION",
        where_clause=where_clause_str)
    arcpy.RemoveJoin_management(
        in_layer_or_view=inputfc)
    arcpy.CopyFeatures_management(
        in_features=inputfc,
        out_feature_class=output_location)
    print(output_location + ' created successfully')

# adds fields to fc
def add_fields(fc, field_list):
    for field in field_list:
        arcpy.AddField_management(
            in_table=fc,
            field_name=field[0],
            field_type=field[1],
            field_alias=field[2]
        )
        print(field[0] + ' field added successfully')
        # pause is inserted to avoid errors
        time.sleep(6)

# copy values from vaa_table_location to fc
def copy_vaa_values(fc, vaa_table_location, vaa_fields):
    vaa_table_name = vaa_table_location[vaa_table_location.rfind('/') + 1::]
    arcpy.AddJoin_management(
        in_layer_or_view=fc,
        in_field="NHDPlusID",
        join_table=vaa_table_location,
        join_field="NHDPlusID",
        join_type="KEEP_COMMON")
    for field in vaa_fields:
        fieldname = field[0]
        arcpy.CalculateField_management(
            in_table=fc,
            field=fieldname,
            expression='[' + vaa_table_name + '.{0}]'.format(field[0]))
        print(field[0] + ' calculated for ' + fc)
    arcpy.RemoveJoin_management(
        in_layer_or_view=fc)

# takes a list and formats it to a string for use in SelectLayerByAttribute_management where_clause
def get_list_string(list, quoteitems = False):
    list_string = '('
    for item in list:
        if quoteitems:
            list_string = list_string + "'" + str(item) + "', "
        else:
            list_string = list_string + str(item) + ", "
    list_string = list_string[0:-2] + ')'
    return (list_string, len(list))

# function for retrieving list using SearchCursor
def get_cursor_list(fc, fields, unique = True):
    cursor_list = []
    with arcpy.da.SearchCursor(fc, fields) as s_cur:
        for row in s_cur:
            if unique and row not in cursor_list:
                cursor_list.append(row)
            else:
                cursor_list.append(row)
    return cursor_list

# calculates gfcode_fields for fc
def process_gfcode_fields(fc, gfcode_fields):
    print('Processing G FCode fields for ' + fc)
    cursor_list = get_cursor_list(fc, ['FCode', 'GNIS_ID', 'LevelPathI'])
    for field in gfcode_fields:
        fieldname = field[0]
        nullgnisid_pathid_list = []
        pathid_list = []
        gnisid_list = []
        print('Processing field ' + field[0])
        fcode_value = int(fieldname[1::])
        matching_fcode_list = list(filter(lambda x: x[0] == fcode_value, cursor_list))
        for row in matching_fcode_list:
            gnisid = str(row[1])
            pathid = int(row[2])
            if gnisid == 'None':
                nullgnisid_pathid_list.append(pathid)
            else:
                gnisid_list.append(gnisid)
                pathid_list.append(pathid)
        if len(nullgnisid_pathid_list) > 0:
            arcpy.SelectLayerByAttribute_management(
                in_layer_or_view=fc,
                selection_type="NEW_SELECTION",
                where_clause="GNIS_ID IS NULL AND LevelPathI IN {0}".format(
                    get_list_string(nullgnisid_pathid_list)[0]))
            arcpy.CalculateField_management(
                in_table=fc,
                field=fieldname,
                expression=1)
        if len(gnisid_list) > 0:
            arcpy.SelectLayerByAttribute_management(
                in_layer_or_view=fc,
                selection_type="NEW_SELECTION",
                where_clause="GNIS_ID IN {0} AND LevelPathI IN {1}".format(get_list_string(gnisid_list, True)[0],
                                                                           get_list_string(pathid_list)[0]))
            arcpy.CalculateField_management(
                in_table=fc,
                field=fieldname,
                expression=1)
    arcpy.SelectLayerByAttribute_management(
        in_layer_or_view=fc,
        selection_type="CLEAR_SELECTION")

# calculates pfcode_fields for fc
def process_pfcode_fields(fc, pfcode_fields):
    print('Processing P FCode fields for ' + fc)
    cursor_list = get_cursor_list(fc, ['FCode', 'LevelPathI'])
    for field in pfcode_fields:
        fieldname = field[0]
        pathid_list = []
        print('Processing field ' + field[0])
        fcode_value = int(field[0][1::])
        matching_fcode_list = list(filter(lambda x: x[0] == fcode_value, cursor_list))
        for row in matching_fcode_list:
            pathid = int(row[1])
            pathid_list.append(pathid)
        if len(pathid_list) > 0:
            arcpy.SelectLayerByAttribute_management(
                in_layer_or_view=fc,
                selection_type="NEW_SELECTION",
                where_clause="LevelPathI IN {0}".format(get_list_string(pathid_list)[0]))
            arcpy.CalculateField_management(
                in_table=fc,
                field=fieldname,
                expression = 1)
    arcpy.SelectLayerByAttribute_management(
        in_layer_or_view=fc,
        selection_type="CLEAR_SELECTION")

### END FUNCTIONS ###
### START PROCESSING ###
### Processing Phase 1: Prepare files
print('Processing Phase 0: Create local parameters')

# retrieve path based on parameter_gdb_location and dataset name
original_dataset_location = get_location(parameter_gdb_location, original_dataset_name)
# retrieve path based on parameter_gdb_location and fc name
original_nhdflowline_location = get_location(original_dataset_location, original_nhdflowline_name)
# retrieve path based on parameter_gdb_location and table name
original_vaatable_location = get_location(parameter_gdb_location, original_vaatable_name)
# takes the rootname of parameter_gdb_location and
gdb_original_rootname = get_fname(parameter_gdb_location)
# get name of result directory
result_rootname = gdb_original_rootname + result_suffix
# get pathname of result directory
result_subdir_location = get_location(arcpy.env.workspace, result_rootname)
# determine path of result directory
result_gdb_location = get_location(result_subdir_location, result_rootname, '.gdb')
# determine name of result geodatabase
result_gdb_filename = get_fname(result_gdb_location)
# get pathnames of result feature classes
result_dataset_location = get_location(result_gdb_location, result_dataset_name)
result_startfeatures_segments_location = get_location(result_gdb_location, result_startfeatures_segments_fcname)
result_startfeatures_dissolved_location = get_location(result_gdb_location, result_startfeatures_dissolved_fcname)
result_tributaries_segments_location = get_location(result_dataset_location, result_tributaries_segments_fcname)
result_tributaries_dissolved_location = get_location(result_dataset_location, result_tributaries_dissolved_fcname)

### Processing Phase 1: Pre-tests
print('Processing Phase 1: Pre-tests')
# do usable start features exist
start_nhdplusids = find_start_features(original_nhdflowline_location, parameter_start_feature, result_startfeatures_segments_location)
# if there are usable start features
if len(start_nhdplusids) > 0:
    # find tributaries that match parameters, if any
    vaa_lists = get_vaa_lists(original_nhdflowline_name, original_vaatable_location, start_nhdplusids, parameter_all_levels,
                              parameter_max_level)
    start_features_hydroseq_list = vaa_lists[0]
    vaa_path_id_list = vaa_lists[1]
    vaa_hydroseq_list = vaa_lists[2]
    starting_tributaries_paths = get_starting_tributaries(start_features_hydroseq_list, vaa_hydroseq_list)
    all_tributaries_paths = get_all_tributaries_from_path(starting_tributaries_paths, vaa_path_id_list)
    # if tributaries exist
    if len(all_tributaries_paths) > 0:
        ### Processing Phase 2: Prepare files
        print('Processing Phase 2: Prepare files')
        os.mkdir(result_subdir_location)
        arcpy.CreateFileGDB_management(
            out_folder_path=result_subdir_location,
            out_name=result_gdb_filename,
            out_version="CURRENT")
        print(result_gdb_filename + ' created')
        arcpy.CreateFeatureDataset_management(
            out_dataset_path=result_gdb_location,
            out_name=result_dataset_name,
            spatial_reference=original_dataset_location)
        print(result_dataset_name + ' dataset created')
        ### Processing Phase 3: Export Tributaries
        print('Processing Phase 3: Export Start Features and Tributaries')
        # TEST DISABLED
        # export_start_features(original_nhdflowline_location, start_nhdplusids, result_startfeatures_segments_location)
        export_matching_paths(original_nhdflowline_name, original_vaatable_location, all_tributaries_paths,
                              result_tributaries_segments_location)
        ### Processing Phase 4: Add fields
        print('Processing Phase 4: Add fields')
        # TEST DISABLED
        # add_fields(result_startfeatures_segments_fcname, vaa_segment_fields)
        # add_fields(result_startfeatures_segments_fcname, fcode_gnisid_fields)
        # add_fields(result_startfeatures_segments_fcname, fcode_pathid_fields)
        add_fields(result_tributaries_segments_fcname, vaa_segment_fields)
        add_fields(result_tributaries_segments_fcname, fcode_gnisid_fields)
        add_fields(result_tributaries_segments_fcname, fcode_pathid_fields)
        ### Processing Phase 5: Process fields
        print('Processing Phase 5: Process fields')
        # TEST DISABLED
        # copy_vaa_values(result_startfeatures_segments_fcname, original_vaatable_location, vaa_segment_fields)
        # process_gfcode_fields(result_startfeatures_segments_fcname, fcode_gnisid_fields)
        # process_pfcode_fields(result_startfeatures_segments_fcname, fcode_pathid_fields)
        copy_vaa_values(result_tributaries_segments_fcname, original_vaatable_location, vaa_segment_fields)
        process_gfcode_fields(result_tributaries_segments_fcname, fcode_gnisid_fields)
        process_pfcode_fields(result_tributaries_segments_fcname, fcode_pathid_fields)
        if parameter_dissolve_streams:
            ### Processing Phase 6: Dissolve to streams
            print('Processing Phase 6: Dissolve to streams')
            # TEST DISABLED
            # arcpy.SelectLayerByAttribute_management(
            #     in_layer_or_view=result_startfeatures_segments_fcname,
            #     selection_type="CLEAR_SELECTION")
            # arcpy.Dissolve_management(
            #     in_features=result_startfeatures_segments_fcname,
            #     out_feature_class=result_startfeatures_dissolved_location,
            #     dissolve_field=dissolve_fields)
            arcpy.SelectLayerByAttribute_management(
                in_layer_or_view=result_tributaries_segments_fcname,
                selection_type="CLEAR_SELECTION")
            arcpy.Dissolve_management(
                in_features=result_tributaries_segments_fcname,
                out_feature_class=result_tributaries_dissolved_location,
                dissolve_field=dissolve_fields)
    else:
        print('Checks complete - No tributaries found')
else:
    print('Checks complete - No matching start features found')
### END PROCESSING ###