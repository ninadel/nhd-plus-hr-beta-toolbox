# NHD Plus HR Tools / Tributaries
# Author: Nina del Rosario (nina.del@gmail.com)
# Last updated: 12/11/2019
# NHD Plus HR description: https://www.usgs.gov/core-science-systems/ngp/national-hydrography/nhdplus-high-resolution

import arcpy
import os
import time
import config

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
def find_start_features(inputfc_location, startfeatures_location):
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
    start_feature_count_str = arcpy.GetCount_management(inputfc_name)[0]
    if int(start_feature_count_str) > 0:
        start_nhdplusids = get_nhdplusids(inputfc_name)
        arcpy.AddMessage('Feedback: ' + start_feature_count_str + ' features found. (Check?)')
    else:
        start_nhdplusids = []
    arcpy.SelectLayerByAttribute_management(
        in_layer_or_view=inputfc_name,
        selection_type="CLEAR_SELECTION")
    return start_nhdplusids

# exports features matching NHDPlusIDs to GDB
# def export_start_features(inputfc_location, start_nhdplusid_list, output_location):
#     inputfc_name = get_fname(inputfc_location)
#     outputfile_name = get_fname(output_location)
#     arcpy.SelectLayerByAttribute_management(
#         in_layer_or_view=inputfc_name,
#         selection_type="CLEAR_SELECTION")
#     start_nhdplusid_list_str = '(' + ', '.join([str(int(i)) for i in start_nhdplusid_list]) + ')'
#     where_clause_str = 'NHDPlusID IN ' + start_nhdplusid_list_str
#     arcpy.SelectLayerByAttribute_management(
#         in_layer_or_view=inputfc_name,
#         selection_type="NEW_SELECTION",
#         where_clause=where_clause_str)
#     arcpy.CopyFeatures_management(
#         in_features=inputfc_name,
#         out_feature_class=output_location)
#     arcpy.SelectLayerByAttribute_management(
#         in_layer_or_view=inputfc_name,
#         selection_type="CLEAR_SELECTION")
#     arcpy.AddMessage(outputfile_name + ' created successfully')


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
    # ERROR
    # result_segment_count = arcpy.GetCount_management(config.result_tributaries_segments_fcname)[0]
    # arcpy.AddMessage(
    #     'Feedback: ' +
    #     result_segment_count +
    #     ' tributary segments found. Segments exported to ' +
    #     config.result_tributaries_segments_fcname +
    #     '.')

# adds fields to fc
def add_fields(fc, field_list):
    for field in field_list:
        arcpy.AddField_management(
            in_table=fc,
            field_name=field[0],
            field_type=field[1],
            field_alias=field[2]
        )
        arcpy.AddMessage(field[0] + ' field added.')
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
        arcpy.AddMessage(field[0] + ' calculated.')
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
    arcpy.AddMessage('Processing G FCode fields for ' + fc)
    cursor_list = get_cursor_list(fc, ['FCode', 'GNIS_ID', 'LevelPathI'])
    for field in gfcode_fields:
        fieldname = field[0]
        nullgnisid_pathid_list = []
        pathid_list = []
        gnisid_list = []
        arcpy.AddMessage('Processing field ' + field[0])
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
    arcpy.AddMessage('Processing P FCode fields for ' + fc)
    cursor_list = get_cursor_list(fc, ['FCode', 'LevelPathI'])
    for field in pfcode_fields:
        fieldname = field[0]
        pathid_list = []
        arcpy.AddMessage('Processing field ' + field[0])
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

def start(parameters):
    arcpy.AddMessage('Feedback: Input parameter: Workspace: ' + arcpy.env.workspace)
    arcpy.AddMessage('Feedback: Input parameter: GDB location: ' + parameters["gdb_location"])
    arcpy.AddMessage('Feedback: Input parameter: Start features: ' + parameters["start_features"])
    arcpy.AddMessage('Feedback: Input parameter: Stream level: ' + str(parameters["max_level"]))
    ### START PROCESSING ###
    ### Processing Phase 0: Create local parameters
    arcpy.env.workspace = parameters["output_folder"]
    # retrieve path based on parameter_gdb_location and dataset name
    original_dataset_location = get_location(parameters["gdb_location"], config.original_dataset_name)
    # retrieve path based on parameter_gdb_location and fc name
    original_nhdflowline_location = get_location(original_dataset_location, config.original_nhdflowline_name)
    # retrieve path based on + and table name
    original_vaatable_location = get_location(parameters["gdb_location"], config.original_vaatable_name)
    # takes the rootname of parameter_gdb_location and
    gdb_original_rootname = get_fname(parameters["gdb_location"])
    # get name of result directory
    result_rootname = gdb_original_rootname + config.result_suffix
    # get pathname of result directory
    result_subdir_location = get_location(arcpy.env.workspace, result_rootname)
    # determine path of result directory
    result_gdb_location = get_location(result_subdir_location, result_rootname, '.gdb')
    # determine name of result geodatabase
    result_gdb_filename = get_fname(result_gdb_location)
    # get pathnames of result feature classes
    result_dataset_location = get_location(result_gdb_location, config.result_dataset_name)
    result_tributaries_segments_location = get_location(result_dataset_location, config.result_tributaries_segments_fcname)
    result_tributaries_dissolved_location = get_location(result_dataset_location, config.result_tributaries_dissolved_fcname)
    ### Processing Phase 1: Pre-tests
    arcpy.AddMessage('Cross checking start features...')
    # do usable start features exist
    start_nhdplusids = find_start_features(original_nhdflowline_location, parameters["start_features"])
    # if there are usable start features
    if len(start_nhdplusids) > 0:
        # find tributaries that match parameters, if any
        arcpy.AddMessage('Searching for tributaries to stream level ' + str(parameters["max_level"]) + "...")
        vaa_lists = get_vaa_lists(config.original_nhdflowline_name, original_vaatable_location, start_nhdplusids, config.result_all_levels,
                                  parameters["max_level"])
        start_features_hydroseq_list = vaa_lists[0]
        vaa_path_id_list = vaa_lists[1]
        vaa_hydroseq_list = vaa_lists[2]
        arcpy.AddMessage(str(len(vaa_path_id_list)) + ' tributaries found')
        starting_tributaries_paths = get_starting_tributaries(start_features_hydroseq_list, vaa_hydroseq_list)
        all_tributaries_paths = get_all_tributaries_from_path(starting_tributaries_paths, vaa_path_id_list)
        # if tributaries exist
        if len(all_tributaries_paths) > 0:
            ### Processing Phase 2: Prepare files
            os.mkdir(result_subdir_location)
            # add message
            arcpy.AddMessage('Feedback: ' + result_rootname + 'directory created')
            arcpy.CreateFileGDB_management(
                out_folder_path=result_subdir_location,
                out_name=result_gdb_filename,
                out_version="CURRENT")
            arcpy.AddMessage(result_gdb_filename + ' geodatabase created')
            arcpy.CreateFeatureDataset_management(
                out_dataset_path=result_gdb_location,
                out_name=config.result_dataset_name,
                spatial_reference=original_dataset_location)
            arcpy.AddMessage('Feedback: ' + config.result_dataset_name + ' dataset created')
            ### Processing Phase 3: Export Tributaries
            arcpy.AddMessage('Feedback: Exporting tributaries...')
            export_matching_paths(config.original_nhdflowline_name, original_vaatable_location, all_tributaries_paths,
                                  result_tributaries_segments_location)
            # add message
            ### Processing Phase 4: Add fields
            arcpy.AddMessage('Feedback: Adding fields...')
            add_fields(result_tributaries_segments_location, config.vaa_segment_fields)
            add_fields(result_tributaries_segments_location, config.fcode_gnisid_fields)
            add_fields(result_tributaries_segments_location, config.fcode_pathid_fields)
            arcpy.MakeFeatureLayer_management(result_tributaries_segments_location, "result_tributaries_segments_lyr")
            ### Processing Phase 5: Process fields
            arcpy.AddMessage('Feedback: Calculating fields...')
            copy_vaa_values("result_tributaries_segments_lyr", original_vaatable_location, config.vaa_segment_fields)
            process_gfcode_fields("result_tributaries_segments_lyr", config.fcode_gnisid_fields)
            process_pfcode_fields("result_tributaries_segments_lyr", config.fcode_pathid_fields)
            if config.result_dissolve:
                ### Processing Phase 6: Dissolve to streams
                arcpy.AddMessage('Feedback: Dissolving segments to streams...')
                arcpy.SelectLayerByAttribute_management(
                    in_layer_or_view="result_tributaries_segments_lyr",
                    selection_type="CLEAR_SELECTION")
                arcpy.Dissolve_management(
                    in_features=result_tributaries_segments_location,
                    out_feature_class=result_tributaries_dissolved_location,
                    dissolve_field=config.dissolve_fields)
                # add message
                # result_stream_count = arcpy.GetCount_management(config.result_tributaries_dissolved_fcname)[0]
                # arcpy.AddMessage('Feedback: Segments dissolved to ' +
                #                  result_stream_count +
                #                  ' streams. Streams exported to '
                #                  + config.result_tributaries_dissolved_fcname)
                # COMPLETE
        else:
            arcpy.AddMessage('Checks complete - No tributaries found')
    else:
        arcpy.AddMessage('Checks complete - No matching start features found')
    ### END PROCESSING ###

### TEST IN ARCPY ###

# nice_params = {
#     "output_folder": 'C:/Workspace/',
#     "gdb_location": 'D:/GCMRC/NHD Plus HR Process Datasets/00 Original Files/NHDPLUS_H_1501_HU4_GDB/NHDPLUS_H_1501_HU4_GDB.gdb',
#     "start_features": 'D:/GCMRC/NHD Plus HR Process Datasets/Basin 15 Start Features/start_features_1501.shp',
#     "max_level": 7
# }
#
# start(nice_params)