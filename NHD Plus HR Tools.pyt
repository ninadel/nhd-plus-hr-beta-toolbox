import arcpy
import tool

class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "NHD Plus HR Tools"
        self.alias = ""

        # List of tool classes associated with this toolbox
        self.tools = [Tributaries]


class Tributaries(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Tributaries"
        self.description = ""
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""

        output_folder = arcpy.Parameter(displayName = 'Output Folder',
                                 name = 'output_folder',
                                 datatype = 'DEFolder',
                                 parameterType = 'Required',
                                 direction = 'Input')

        gdb_location = arcpy.Parameter(
            displayName="GDB Location",
            name="gdb_location",
            datatype="DEWorkspace",
            parameterType="Required",
            direction="Input")

        start_features = arcpy.Parameter(displayName = 'Start Features',
                                 name = 'start_features',
                                 datatype = 'DEShapefile',
                                 parameterType = 'Required',
                                 direction = 'Input')

        max_level = arcpy.Parameter(displayName = 'Max stream level',
                                 name = 'max_level',
                                 datatype = 'GPLong',
                                 parameterType = 'Required',
                                 direction = 'Input')

        params = [output_folder, gdb_location, start_features, max_level]
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
        output_folder = parameters[0].valueAsText
        gdb_location = parameters[1].valueAsText
        start_features = parameters[2].valueAsText
        max_level = parameters[3].valueAsText

        nice_params = {
            "output_folder": parameters[0].valueAsText.replace("\\", "/"),
            "gdb_location": parameters[1].valueAsText.replace("\\", "/"),
            "start_features": parameters[2].valueAsText.replace("\\", "/"),
            "max_level": int(parameters[3].valueAsText)
        }

        tool.start(nice_params)