import os
import arcpy
import reporting

def execute(output_file_path,
            input_template_cross_section_feature_class,
            fields_to_add):    

    # validation
    validate(output_file_path)

    # add .shp extension if output file path does not currently have it
    output_file_path = verify_shapefile_input_has_correct_extension(output_file_path)

    # define temp output file path
    in_memory_feature_class = r'in_memory\%s' % os.path.splitext(os.path.basename(output_file_path))[0]

    # delete in memory feature class if it exists
    if arcpy.Exists(in_memory_feature_class):
        arcpy.Delete_management(in_memory_feature_class)

    # copy template feature class to output file location
    arcpy.CopyFeatures_management(input_template_cross_section_feature_class,
                                  in_memory_feature_class)

    # add the necessary fields to the copied feature class
    for field_name in fields_to_add:
        arcpy.AddField_management(in_memory_feature_class,
                                  field_name,
                                  'DOUBLE')   

    return in_memory_feature_class

def validate(file_path):

    # verify the provided output folder exists
    if not os.path.isdir(os.path.dirname(file_path)):
        reporting.error('The provided output folder: %s does not exist. Please provide an existing folder for the Output Folder.' % os.path.dirname(file_path))
        raise arcpy.ExecuteError

    # verify that the output file path does not already exist
    if os.path.isfile(file_path):
        reporting.error('The provided output file name: %s already exists. Please provide an output file name for the Output Folder.' % file_path)
        raise arcpy.ExecuteError  

def verify_shapefile_input_has_correct_extension(file_path):
    
    # verify that output file name has the .shp extension
    if os.path.splitext(os.path.basename(file_path))[1] != '.shp':
        output_file_name = os.path.splitext(os.path.basename(file_path))[0] + '.shp'
        file_path = os.path.join(os.path.dirname(file_path), output_file_name)

    return file_path


