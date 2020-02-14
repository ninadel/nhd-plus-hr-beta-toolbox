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

### FCodes
Information about FCodes can be found at https://nhd.usgs.gov/userGuide/Robohelpfiles/NHD_User_Guide/Feature_Catalog/Hydrography_Dataset/NHDFlowline/NHDFlowline.htm. 

The following FCodes are used by this script to classify stream segments: 
* 46000 - STREAM/RIVER, feature type only: no attributes
* 46003 - STREAM/RIVER, Hydrographic Category|intermittent
* 46006 - STREAM/RIVER, Hydrographic Category|perennial
* 46007 - STREAM/RIVER, Hydrographic Category|ephemeral
* 55800 - ARTIFICIAL PATH, feature type only: no attributes

## Parameters
1. Output folder - this is where results will be saved. 
    * A subfolder named NHDPLUS_H_\[HUC4]_HU4_GDB_RESULT will be created here. 
2. NHDPlus HR geodatabase - this is the geodatabase downloaded from the NHD website using the steps above. 
    * For best results, this geodatabase should be the unmodified version downloaded from the NHD website. 
3. Shapefile of streams to find tributaries for - these linear features must align with streams from the NHDFlowline 
feature class in the above geodatabase
    * For best results, select streams of interest from the NHDFlowline feature class and export them 
    to a shapefile. This will ensure that the shapefile and the geodatabase align because they came from the same data source.
    * These stream(s) can be continuous or discontinuous. For example, it is possible to run this script on two different streams 
    that are disconnected but both in the same watershed subregion. 
4. Maximum stream level for tributary search - based on stream level, this is the cutoff point for finding tributaries.  
    * For example, if a starting stream had a stream level of 4, setting this parameter to 5 will find the primary 
    tributaries for this stream. Setting this parameter to 6 would find primary and secondary tributaries. 
    * See https://usgs-mrs.cr.usgs.gov/NHDHelp/WebHelp/NHD_Help/Introduction_to_the_NHD/Feature_Attribution/Stream_Levels.htm 
    for an explanation of stream levels.

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
* G46000 - this field will have the value of 1 if the collection of segments that share the same combination of GNIS_ID and LevelPathI contain at least one segment with the FCode 46000. 
* G46003 - this field will have the value of 1 if the collection of segments that share the same combination of GNIS_ID and LevelPathI contain at least one segment with the FCode 46003. 
* G46006 - this field will have the value of 1 if the collection of segments that share the same combination of GNIS_ID and LevelPathI contain at least one segment with the FCode 46006. 
* G46007 - this field will have the value of 1 if the collection of segments that share the same combination of GNIS_ID and LevelPathI contain at least one segment with the FCode 46007. 
* G55800 - this field will have the value of 1 if the collection of segments that share the same combination of GNIS_ID and LevelPathI contain at least one segment with the FCode 55800. 
* P46000 - this field will have the value of 1 if the collection of segments that share the same LevelPathI contain at least one segment with the FCode 46000. 
* P46003 - this field will have the value of 1 if the collection of segments that share the same LevelPathI contain at least one segment with the FCode 46003. 
* P46006 - this field will have the value of 1 if the collection of segments that share the same LevelPathI contain at least one segment with the FCode 46006. 
* P46007 - this field will have the value of 1 if the collection of segments that share the same LevelPathI contain at least one segment with the FCode 46007. 
* P55800 - this field will have the value of 1 if the collection of segments that share the same LevelPathI contain at least one segment with the FCode 55800. 

There is a subtle difference between the fields above with the prefix G and the fields above with the prefix P. 
It is possible to have a physically continuous stream which has more than one GNIS_ID value 
(for example, the stream may have portions with different names or named and unnamed portions).
If interested in a portion of a stream that shares the same name, use fields with the prefix G. 
If interested in a physically continuous stream regardless of name, use fields with the prefix P. 

These calculated fields are useful for filtering streams by FCode type. For example, to exclude 
streams that do not contain perennial segments, select features that have a P46006 value of 1 (FCode 46006 = perennial). 

#### Tributary_Streams fields (dissolved)
* To generate the Tributary_Streams feature class, the Tributary_Segments feature class is dissolved on the following fields:
    * GNIS_ID
    * GNIS_Name
    * StreamLeve
    * LevelPathI
    * G46000
    * G46003
    * G46006
    * G46007
    * G55800
    * P46000
    * P46003
    * P46006
    * P46007
    * P55800

## Reference links
* https://www.usgs.gov/media/images/watershed-boundary-dataset-subregions-map
* https://nhd.usgs.gov/userGuide/Robohelpfiles/NHD_User_Guide/Feature_Catalog/Hydrography_Dataset/NHDFlowline/NHDFlowline.htm
* https://usgs-mrs.cr.usgs.gov/NHDHelp/WebHelp/NHD_Help/Introduction_to_the_NHD/Feature_Attribution/Stream_Levels.htm
