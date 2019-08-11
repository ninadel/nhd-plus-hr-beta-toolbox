import arcpy
import arguments
import config
import os
import math
import methods.initialization
import methods.quality_assurance

class TributaryFinder(object):

    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "NHD Plus HR Tributary Finder"
        self.description = ""
        self.canRunInBackground = True
        self.params = arcpy.GetParameterInfo()

    def getParameterInfo(self):
        """Define parameter definitions"""
        param0 = arguments.arcpy_parameter.required_max_level
        # param1
        # param2

        params = [
            param0]

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
