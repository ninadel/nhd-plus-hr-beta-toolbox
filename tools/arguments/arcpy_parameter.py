import arcpy

#   required_gdb_location - geodatabase location of NHD Plus HR data
required_gdb_location = arcpy.Parameter(
    displayName="NHD Geodatabase File",
    name="nhd_geodatabase_file",
    datatype="DEWorkspace",
    parameterType="Required",
    direction="Input")

#   required_start_feature = the stream feature for which tributaries will be found
required_start_stream_linear_feature = arcpy.Parameter(
    displayName="Start stream linear feature",
    name="start_stream_linear_feature",
    datatype="GPLayer",
    parameterType="Required",
    direction="Input")

#   output_folder - folder where results will be saved
output_folder = arcpy.Parameter(
    displayName = 'Output Folder',
    name = 'output_folder',
    datatype = 'DEFolder',
    parameterType = 'Required',
    direction = 'Input')

#   all_levels - TBD

#   max_level - TBD

#   dissolve_streams - TBD

# COPIED FROM vaa_tributary_finder
#   parameter_start_feature - linear feature class or shapefile of streams
#   parameter_all_levels - search tributaries in all StreamLevels?
#   parameter_max_level - if parameter_all_levels is false, what is the highest StreamLevel to include?
#   parameter_dissolve_streams - should stream segments be dissolved into streams (dissolved based on LevelPathI)?

# COPIED FROM vaa_tributary_finder
# ### START GLOBAL PARAMETERS ###
# parameter_output_location = 'C:/Workspace/'
# parameter_gdb_location = 'E:/GCMRC/NHD Plus HR Process Datasets/00 Original Files/NHDPLUS_H_1507_HU4_GDB/NHDPLUS_H_1507_HU4_GDB.gdb'
# parameter_start_feature = 'E:/GCMRC/NHD Plus HR Process Datasets/Basin 15 Start Features/start_features_1507.shp'
# parameter_all_levels = False
# parameter_max_level = 7
# parameter_dissolve_streams = True
#
# arcpy.env.workspace = parameter_output_location

# COPIED FROM cross-section-demo
# required_boolean_parameter = arcpy.Parameter(datatype = 'GPBoolean',
#                                              parameterType = 'Required',
#                                              direction = 'Input')
#
# optional_double_parameter = arcpy.Parameter(datatype = 'GPDouble',
#                                             parameterType = 'Optional',
#                                             direction = 'Input')
#
#
#
# river_increment_unit = arcpy.Parameter(displayName = 'River Increment Unit',
#                                        name = 'river_increment_unit',
#                                        datatype = 'GPString',
#                                        parameterType = 'Required',
#                                        direction = 'Input')
#
# cross_section_increment_distance = arcpy.Parameter(displayName = 'Cross Section Increment Distance',
#                                                    name = 'cross_section_increment',
#                                                    datatype = 'GPDouble',
#                                                    parameterType = 'Required',
#                                                    direction = 'Input')
#
#
# output_filename = arcpy.Parameter(displayName = 'Output File Name',
#                                   name = 'output_file_name',
#                                   datatype = 'GPString',
#                                   parameterType = 'Required',
#                                   direction = 'Input')
#
# perform_qa = arcpy.Parameter(displayName = 'Flag Cross Sections For QA',
#                              name = 'flag_for_qa',
#                              datatype = 'GPBoolean',
#                              parameterType = 'Required',
#                              direction = 'Input')

# COPIED FROM NHD Plus HR Tributary Finder.pyt
# """Define parameter definitions"""
#
# # First parameter
# parameter_output_location = arcpy.Parameter(
#     displayName="parameter_output_location displayname",
#     name="parameter_output_location name",
#     datatype="GPFeatureLayer",
#     parameterType="Required",
#     direction="Input")
#
#
# parameter_start_feature = arcpy.Parameter(
#     displayName="parameter_start_feature displayname",
#     name="parameter_start_feature name",
#     datatype="GPFeatureLayer",
#     parameterType="Required",
#     direction="Input")
#
# parameter_all_levels = arcpy.Parameter(
#     displayName="parameter_all_levels displayname",
#     name="parameter_all_levels name",
#     datatype="GPFeatureLayer",
#     parameterType="Required",
#     direction="Input")
#
# parameter_max_level = arcpy.Parameter(
#     displayName="parameter_max_level displayname",
#     name="parameter_max_level name",
#     datatype="GPFeatureLayer",
#     parameterType="Required",
#     direction="Input")
#
# parameter_dissolve_streams = arcpy.Parameter(
#     displayName="parameter_dissolve_streams displayname",
#     name="parameter_all_levels name",
#     datatype="GPFeatureLayer",
#     parameterType="Required",
#     direction="Input")
