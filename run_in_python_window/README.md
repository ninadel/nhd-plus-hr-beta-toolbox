# NHD Plus HR Tributary Finder v5
Author: Nina del Rosario

Last updated: 5/2/19

Dataset description: https://www.usgs.gov/core-science-systems/ngp/national-hydrography/nhdplus-high-resolution

Status: Revising from v4 (integrating all parameters, adding pre-checks, adding documentation notes)

## Purpose
The purpose of this script is to select a tributary stream network based on a stream shapefile of starting features.

## Parameters
The input parameters are:
* parameter_output_location - workspace where results will be saved
* parameter_gdb_location - geodatabase location of NHD Plus HR data
* parameter_start_feature - linear feature class or shapefile of streams
* parameter_all_levels - search tributaries in all StreamLevels?
* parameter_max_level - if parameter_all_levels is false, what is the highest StreamLevel to include?
* parameter_dissolve_streams - should stream segments be dissolved into streams (dissolved based on LevelPathI)?

## Requirements
* parameter_gdb_location must point to a GDB from the NHD Plus HR data dataset (unzipped vector data)
* parameter_gdb_location must have a NHDPlusFlowlineVAA file geodatabase table
* NHDPlusFlowlineVAA must have populated data in the following fields: HydroSeq, LevelPathI, TerminalPa, UpLevelPat, UpHydroSeq, DnLevel, DnLevelPat, DnHydroSeq
* Datasets prior to NHD Plus HR have a few of the above fields unpopulated
* parameter_start_feature must have originated from the same dataset as parameter_gdb_location (NHD Plus HR)
* finding tributaries will be dependent on selecting segments in parameter_gdb_location/Hydrography/NHDFlowline which coincide (share a line segment) with parameter_start_feature
* parameter_start_feature must have an overlapping extent with parameter_gdb_location/Hydrography/NHDFlowline

## Outputs
This script will generate:
* A folder in the workspace with the name 'NHDPLUS_H_[HUC4]\_HU4_GDD_RESULT' where HUC4 is the 4-digit HUC4 from parameter_gdb_location
* A geodatabase in the above folder with the name NHDPLUS_H_[HUC4]\_HU4_GDD_RESULT.gdb where HUC4 is the 4-digit HUC4 from parameter_gdb_location
* A feature class in the above geodatabase named StartFeatures_Segments
* A feature class in the above geodatabase named StartFeatures_Streams  (if parameter_dissolve_streams is true)
* A feature dataset in the above geodatabase named Tributaries (if tributaries are found)
* A feature class in the above dataset named Tributaries_Segments
* A feature class in the above dataset named Tributaries_Segments (if parameter_dissolve_streams is true)
* The feature classes generated will have added fields based on vaa_segment_fields, fcode_gnisid_fields, and fcode_pathid_fields
