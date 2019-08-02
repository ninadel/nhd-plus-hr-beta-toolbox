import arcpy

required_boolean_parameter = arcpy.Parameter(datatype = 'GPBoolean',
                                             parameterType = 'Required',
                                             direction = 'Input')

optional_double_parameter = arcpy.Parameter(datatype = 'GPDouble',
                                            parameterType = 'Optional',
                                            direction = 'Input')



river_increment_unit = arcpy.Parameter(displayName = 'River Increment Unit',
                                       name = 'river_increment_unit',
                                       datatype = 'GPString',
                                       parameterType = 'Required',
                                       direction = 'Input')

cross_section_increment_distance = arcpy.Parameter(displayName = 'Cross Section Increment Distance',
                                                   name = 'cross_section_increment',
                                                   datatype = 'GPDouble',
                                                   parameterType = 'Required',
                                                   direction = 'Input')

output_folder = arcpy.Parameter(displayName = 'Output Folder',
                                          name = 'output_folder',
                                          datatype = 'DEFolder',
                                          parameterType = 'Required',
                                          direction = 'Input')

output_filename = arcpy.Parameter(displayName = 'Output File Name',
                                  name = 'output_file_name',
                                  datatype = 'GPString',
                                  parameterType = 'Required',
                                  direction = 'Input')

perform_qa = arcpy.Parameter(displayName = 'Flag Cross Sections For QA',
                             name = 'flag_for_qa',
                             datatype = 'GPBoolean',
                             parameterType = 'Required',
                             direction = 'Input')
