# NHD Plus HR Beta Toolbox (Tributaries Tool)

## Overview
The purpose of the tool, 

Details about the source dataset, beta version, link

What #### means in these instructions

## Data used by this tool

### How to download NHD Plus HR data
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