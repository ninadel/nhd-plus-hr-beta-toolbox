import logging
import arcpy

def message(message):

    arcpy.AddMessage(message)
    logging.info(message)

def error(message):

    arcpy.AddError(message)
    logging.error(message, exc_info=True)
