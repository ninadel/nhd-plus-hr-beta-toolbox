# NHD Plus HR Beta Toolbox (Tributaries Tool)

## Overview
This tool identifies tributary streams within the NHD Plus High Resolution dataset (NHD Plus HR, currently in beta) and exports them to a new results dataset. 
Tributary identification is accomplished by joining the VAA (value-added attribute) table to the NHDFlowline feature class and analyzing the relationships between the different streams. 

Two versions of the tributaries are exported: in the first version the streams segments remain discrete and in the second version the segments are merged into streams. 
The resulting feature classes keep important attribute fields from the originating files and add additional calculated fields. 

For the purposes of these instructions, \[HUC4] represents the Hydrologic Unit Code. These 4-digit codes identify watershed subregions (more information can be found at https://www.usgs.gov/media/images/watershed-boundary-dataset-subregions-map). 

## Data used by this tool

### How to download NHD Plus HR data
The NHD Plus HR dataset can be downloaded from https://viewer.nationalmap.gov/basic/?basemap=b1&category=nhd&title=NHD%20View. 

From this website, datasets can be downloaded using the following steps:
1. Select NHDPlus HR under Product Search Filter
2. Find the region of interest using either the HUC4 number (by selecting Advanced Search Options) or the map tool
3. When the dataset of interest is located, select the Download Vector link (this will download a zip file)
4. The zip file unzips to a geodatabase, which is the main used by the script.

### Files used by the tool
This script uses the NHDFlowline feature class (under the Hydrography dataset) and the table NHDPlusFlowlineVAA.
This script joins NHDFlowline and NHDPlusFlowlineVAA based on the field NHDPlusID.

## Parameters
1. Output folder - this is where results will be saved. 
    * A subfolder named NHDPLUS_H_\[HUC4]_HU4_GDB_RESULT will be created here. 
2. NHDPlus HR geodatabase - this is the geodatabase downloaded from the steps above. 
    * For best results, this geodatabase should be the unmodified version downloaded from the NHD website. 
3. Shapefile of streams to find tributaries for - these linear features must align with streams from the NHDFlowline 
feature class in the above geodatabase
    * For best results, select streams from the NHDFlowline feature class and export them to a shapefile. 
    * These stream(s) can be continuous or discontinuous (example, steam level)
4. Maximum stream level for tributary search - based on stream level, this is the cutoff point for finding tributaries.  
    * For example, if a starting stream had a stream level of 4, setting this parameter to 5 will find the primary 
    tributaries for this stream. Setting this parameter to 6 would find primary and secondary tributaries. 
    * See https://usgs-mrs.cr.usgs.gov/NHDHelp/WebHelp/NHD_Help/Introduction_to_the_NHD/Feature_Attribution/Stream_Levels.htm 
    for a description of stream levels.

## Outputs

### Output files
The following are outputs of this script:
* In the output folder, a subfolder named NHDPLUS_H_\[HUC4]_HU4_GDB_RESULT 
* In this subfolder, a geodatabase named NHDPLUS_H_\[HUC4]_HU4_GDB_RESULT.gdb   
* In the geodatabase, a dataset named Tributaries
* In the Tributaries dataset, a feature classes named Tributaries_Segments and Tributaries_Streams (Tributaries_Streams feature class is the dissolved version of Tributaries_Segments) 

### Output file fields

#### Tributary_Segment fields
In Tributary_Segments, the following fields are copied from NHDFlowline:
* Permanent_Identifier
* FDate
* Resolution
* GNIS_ID
* GNIS_Name
* LengthKM
* ReachCode
* FlowDir
* WBArea_Permanent_Identifier
* FType
* FCode
* MainPath
* InNetwork
* VisibilityFilter
* Shape_Length
* NHDPlusID
* VPUID
* Enabled

In Tributary_Segments, the following fields are copied from NHDPlusFlowlineVAA:
* StreamLeve
* HydroSeq
* LevelPathI
* TerminalPa
* UpLevelSeq
* UpHydroSeq
* DnLevelPat
* DnHydroSeq

In Tributary_Segments, the following fields are calculated:
* G46000 (Description)
* G46003 (Description)
* G46006 (Description)
* G46007 (Description)
* G55800 (Description)
* P46000 (Description)
* P46003 (Description)
* P46006 (Description)
* P46007 (Description)
* P55800 (Description)

#### Tributary_Streams fields
In Tributary_Streams, the following fields are copied from NHDFlowline:

In Tributary_Streams, the following fields are copied from NHDPlusFlowlineVAA:
*

In Tributary_Streams, the following fields are calculated:
*

* tributary segment fields
    * fields copied from NHDFlowline
    * fields copied from VAA table
* tributary stream fields
    * fields copied from NHDFlowline
    * fields copied from VAA table
* G Fcode fields
* P FCode fields, 
example of where P FCode and G FCode fields may differ

## Reference links
* https://www.usgs.gov/media/images/watershed-boundary-dataset-subregions-map
* https://usgs-mrs.cr.usgs.gov/NHDHelp/WebHelp/NHD_Help/Introduction_to_the_NHD/Feature_Attribution/Stream_Levels.htm