import arcpy

from tools.TributaryFinder import TributaryFinder

class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "NHD Plus HR Toolbox"
        self.alias = "NHD Plus HR Toolbox Alias?"

        # List of tool classes associated with this toolbox
        self.tools = [TributaryFinder]


class TributaryFinder(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "NHD Plus HR Tributary Finder"
        self.description = ""
        self.canRunInBackground = True

    def getParameterInfo(self):
        """Define parameter definitions"""

        # First parameter
        parameter_output_location = arcpy.Parameter(
            displayName="parameter_output_location displayname",
            name="parameter_output_location name",
            datatype="GPFeatureLayer",
            parameterType="Required",
            direction="Input")

        parameter_gdb_location = arcpy.Parameter(
            displayName="parameter_gdb_location displayname",
            name="parameter_gdb_location name",
            datatype="GPFeatureLayer",
            parameterType="Required",
            direction="Input")

        parameter_start_feature = arcpy.Parameter(
            displayName="parameter_start_feature displayname",
            name="parameter_start_feature name",
            datatype="GPFeatureLayer",
            parameterType="Required",
            direction="Input")

        parameter_all_levels = arcpy.Parameter(
            displayName="parameter_all_levels displayname",
            name="parameter_all_levels name",
            datatype="GPFeatureLayer",
            parameterType="Required",
            direction="Input")

        parameter_max_level = arcpy.Parameter(
            displayName="parameter_max_level displayname",
            name="parameter_max_level name",
            datatype="GPFeatureLayer",
            parameterType="Required",
            direction="Input")

        parameter_dissolve_streams = arcpy.Parameter(
            displayName="parameter_dissolve_streams displayname",
            name="parameter_all_levels name",
            datatype="GPFeatureLayer",
            parameterType="Required",
            direction="Input")

        params = [parameter_output_location, parameter_gdb_location, parameter_start_feature, parameter_all_levels, parameter_max_level, parameter_dissolve_streams]
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        return
