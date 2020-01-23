# NHD Plus HR Beta Toolbox (Tributaries Tool)

## Overview
This tool identifies tributary streams within the NHD Plus High Resolution dataset (NHD Plus HR, currently in beta) and exports them to a new results dataset. 
Tributary identification is accomplished by joining the VAA (value-added attribute) table to the NHDFlowline feature class and analyzing the relationships between the different streams. 

Two versions of the tributaries are exported: in the first version the streams segments remain discrete and in the second version the segments are merged into streams. 
The resulting feature classes keep important attribute fields from the originating files and add additional calculated fields. 

For the purposes of these instructions, #### represents the HUC4 (Hydrologic Unit Code), which will vary with each watershed. 

## Data used by this tool

### How to download NHD Plus HR data
The NHD Plus HR dataset can be downloaded from https://viewer.nationalmap.gov/basic/?basemap=b1&category=nhd&title=NHD%20View. 

Go to national map website,
search for data for region of interest (using code or map),
download vector file (zip), unzip

### Files used by the tool
NHDFlowline, feature class, 
VAA table, join on NHDPlusID field, where to find more information on VAA

## Parameters
* Output folder, 
subdir created
* GDB location, 
should be unmodified from GDB downloaded from TNM
* Start features, 
derived from NHD flowline and must align, 
how to create start features, 
can be continuous or discontinuous, 
how to create a start feature shapefile (join VAA table using NHDPlusID)
* Max level, 
stream level concept, 
link to USGS docs, 
examples (single stream to find primary and secondary tributaries, multi stream with different levels)

## Outputs

### Output files
* Folder
* Dataset
* Segment feature class
* Stream feature class, dissolved based on these fields...

### Output file fields
* tributary segment fields
    * fields copied from NHDFlowline
    * fields copied from VAA table
* tributary stream fields
    * fields copied from NHDFlowline
    * fields copied from VAA table
* G Fcode fields
* P FCode fields, 
example of where P FCode and G FCode fields may differ

## Sample data
Where to find sample data