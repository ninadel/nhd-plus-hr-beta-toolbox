import os

# cross_section_increment_info = {'MILE'      :  {'output fields' : ['RiverMile', 'StartFeet', 'EndFeet'],
#                                            'reference layer' : r'RiverMile_100thMile',
#                                            'reference fields' : ['RIVERMILE_100THS', 'StartFeet', 'EndFeet']},
#                              'KILOMETER' : {'output fields' : ['RiverKM','StartMeter', 'EndMeter'],
#                                             'reference layer' : r'RiverMile_100thKM',
#                                             'reference fields' : ['KM100THS', 'STARTKM100', 'ENDKM100TH']}}
#
# river_discharge_layers = {8000 : r'Modeled_Shoreline_8k',
#                           10000 : r'Modeled_Shoreline_10k',
#                           12000 : r'Modeled_Shoreline_12k',
#                           14000 : r'Modeled_Shoreline_14k',
#                           16000 : r'Modeled_Shoreline_16k',
#                           18000 : r'Modeled_Shoreline_18k',
#                           20000 : r'Modeled_Shoreline_20k',
#                           25000 : r'Modeled_Shoreline_25k',
#                           31000 : r'Modeled_Shoreline_31k',
#                           41000 : r'Modeled_Shoreline_41k',
#                           45000 : r'Modeled_Shoreline_45k'}
#
# river_discharges = [8000,
#                     10000,
#                     12000,
#                     14000,
#                     16000,
#                     18000,
#                     20000,
#                     25000,
#                     31000,
#                     41000,
#                     45000]
#
# distance_units = ['KILOMETER',
#                   'MILE']
#
# increment_distances = [1,
#                        1/10.0,
#                        1/100.0]
#
# feet_in_mile = 5280
# meters_in_kilometer = 1000
#
# input_reference_geodatabase = r'P:\DASA\GIS\Projects\Physical\cross-sections\data\wrk\river_reference_data.gdb'
# input_template_cross_section_feature_class = os.path.join(input_reference_geodatabase,'cross_section_template')
