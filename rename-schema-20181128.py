import os
import sys
import platform
import datetime
import time


import arcpy


# Capture start_time
start_time = time.time()


def hms_string(sec_elapsed):
    """Function to display elapsed time

    Keyword arguments:
    sec_elapsed -- elapsed time in seconds
    """
    h = int(sec_elapsed / (60 * 60))
    m = int((sec_elapsed % (60 * 60)) / 60)
    s = sec_elapsed % 60.
    return "{0}:{1:>02}:{2:>05.2f}".format(h,
                                           m,
                                           s)


# Print Python version, version info, and platform architecture
print('\n\nsys.version:\t\t\t\t\t{0}'.format(sys.version))
print('sys.versioninfo:\t\t\t\t{0}'.format(sys.version_info))
print('platform.architecture():\t\t{0}'.format(platform.architecture()))


# Print script filename, start date and time
script = os.path.basename(__file__)
print('\n\nStarted {0} at {1} on {2}...'.format(script,
                                                datetime.datetime.now().strftime('%H:%M:%S'),
                                                datetime.datetime.now().strftime('%Y-%m-%d')))


# Define NODATA value
NODATA = -9999.0


# Define DEFAULT value as None
DEFAULT = None


# Set arcpy overwrite output to True
arcpy.env.overwriteOutput = True


#  File GDB
combined_fgdb = r'G:\CountrysideSurvey\cs2007-wgem-combined-schema\combined-schema-20181127.gdb'
renamed_fgdb = r'G:\CountrysideSurvey\cs2007-wgem-combined-schema\combined-schema-20181127-renamed.gdb'
print('\n\nCopying combined_fgdb to renamed_fgdb...')
if arcpy.Exists(dataset=renamed_fgdb):
	print('Deleting exising renamed_fgdb...')
	arcpy.Delete_management(in_data=renamed_fgdb)
arcpy.Copy_management(in_data= combined_fgdb,
                      out_data=renamed_fgdb)


#  Blocks
old_blocks = os.path.join(renamed_fgdb, 'BLKDATA')
new_blocks = os.path.join(renamed_fgdb, 'SURVEYSQUARES')
old_blocks_guid = 'BLKDATA_GUID'
new_blocks_guid = 'SURVEYSQUARES_GUID'
print('\n\nRenaming {0} to {1}...'.format(os.path.basename(old_blocks),
                                          os.path.basename(new_blocks)))
arcpy.Rename_management(in_data=old_blocks,
                        out_data=new_blocks)
print('Renaming {0} to {1}...'.format(old_blocks_guid,
                                      new_blocks_guid))
# arcpy.AlterField_management(in_table=new_blocks,
#                             field=old_blocks_guid,
#                             new_field_name=new_blocks_guid,
#                             new_field_alias=new_blocks_guid)
print('\tAdding {0} field...'.format(new_blocks_guid))
arcpy.AddField_management(in_table=new_blocks,
                          field_name=new_blocks_guid,
                          field_type='GUID',
                          field_is_nullable='NULLABLE',
                          field_is_required='REQUIRED')
print('\tCalculating {0} field...'.format(new_blocks_guid))
arcpy.CalculateField_management(in_table=new_blocks,
                                field=new_blocks_guid,
                                expression='!{0}!'.format(old_blocks_guid),
                                expression_type='PYTHON3')
print('\tDeleting {0} field...'.format(old_blocks_guid))
arcpy.DeleteField_management(in_table=new_blocks,
                             drop_field='[\"{0}\"]'.format(old_blocks_guid))


#  Areas
old_areas = os.path.join(renamed_fgdb, 'SCPTDATA')
new_areas = os.path.join(renamed_fgdb, 'AREAS')
old_areas_data = os.path.join(renamed_fgdb, 'COMPDATA')
new_areas_data = os.path.join(renamed_fgdb, 'AREASDATA')
old_areas_guid = 'SCPTDATA_GUID'
new_areas_guid = 'AREAS_GUID'
old_areas_data = os.path.join(renamed_fgdb, 'COMPDATA')
new_areas_data = os.path.join(renamed_fgdb, 'AREASDATA')
old_areas_data_guid = 'COMPDATA_GUID'
new_areas_data_guid = 'AREASDATA_GUID'
print('\n\nDeleting {0}_{1} relationship class...'.format(os.path.basename(old_areas),
                                                          os.path.basename(old_areas_data)))
arcpy.Delete_management(in_data='{0}_{1}'.format(os.path.basename(old_areas),
                                                 os.path.basename(old_areas_data)))
print('Renaming {0} to {1}...'.format(os.path.basename(old_areas),
                                      os.path.basename(new_areas)))
arcpy.Rename_management(in_data=old_areas,
                        out_data=new_areas)
print('Renaming {0} to {1}...'.format(old_areas_guid,
                                      new_areas_guid))
# arcpy.AlterField_management(in_table=new_areas,
#                             field=old_areas_guid,
#                             new_field_name=new_areas_guid,
#                             new_field_alias=new_areas_guid)
print('\tAdding {0} field...'.format(new_areas_guid))
arcpy.AddField_management(in_table=new_areas,
                          field_name=new_areas_guid,
                          field_type='GUID',
                          field_is_nullable='NULLABLE',
                          field_is_required='REQUIRED')
print('\tCalculating {0} field...'.format(new_areas_guid))
arcpy.CalculateField_management(in_table=new_areas,
                                field=new_areas_guid,
                                expression='!{0}!'.format(old_areas_guid),
                                expression_type='PYTHON3')
print('\tDeleting {0} field...'.format(old_areas_guid))
arcpy.DeleteField_management(in_table=new_areas,
                             drop_field='[\"{0}\"]'.format(old_areas_guid))
print('Renaming {0} to {1}...'.format(os.path.basename(old_areas_data),
                                      os.path.basename(new_areas_data)))
arcpy.Rename_management(in_data=old_areas_data,
                        out_data=new_areas_data)
print('Renaming {0} to {1}...'.format(old_areas_guid,
                                      new_areas_guid))
# arcpy.AlterField_management(in_table=new_areas_data,
#                             field=old_areas_guid,
#                             new_field_name=new_areas_guid,
#                             new_field_alias=new_areas_guid)
print('\tAdding {0} field...'.format(new_areas_guid))
arcpy.AddField_management(in_table=new_areas_data,
                          field_name=new_areas_guid,
                          field_type='GUID',
                          field_is_nullable='NULLABLE',
                          field_is_required='REQUIRED')
print('\tCalculating {0} field...'.format(new_areas_guid))
arcpy.CalculateField_management(in_table=new_areas_data,
                                field=new_areas_guid,
                                expression='!{0}!'.format(old_areas_guid),
                                expression_type='PYTHON3')
print('\tDeleting {0} field...'.format(old_areas_guid))
arcpy.DeleteField_management(in_table=new_areas_data,
                             drop_field='[\"{0}\"]'.format(old_areas_guid))
print('Renaming {0} to {1}...'.format(old_areas_data_guid,
                                      new_areas_data_guid))
# arcpy.AlterField_management(in_table=new_areas_data,
#                             field=old_areas_data_guid,
#                             new_field_name=new_areas_data_guid,
#                             new_field_alias=new_areas_data_guid)
print('\tAdding {0} field...'.format(new_areas_data_guid))
arcpy.AddField_management(in_table=new_areas_data,
                          field_name=new_areas_data_guid,
                          field_type='GUID',
                          field_is_nullable='NULLABLE',
                          field_is_required='REQUIRED')
print('\tCalculating {0} field...'.format(new_areas_data_guid))
arcpy.CalculateField_management(in_table=new_areas_data,
                                field=new_areas_data_guid,
                                expression='!{0}!'.format(old_areas_data_guid),
                                expression_type='PYTHON3')
print('\tDeleting {0} field...'.format(old_areas_data_guid))
arcpy.DeleteField_management(in_table=new_areas_data,
                             drop_field='[\"{0}\"]'.format(old_areas_data_guid))
print('Creating {0}_{1} relationship class...'.format(os.path.basename(new_areas),
                                                      os.path.basename(new_areas_data)))
arcpy.CreateRelationshipClass_management(origin_table=new_areas,
                                         destination_table=new_areas_data,
                                         out_relationship_class='{0}_{1}'.format(os.path.basename(new_areas),
                                                                                 os.path.basename(new_areas_data)),
                                         relationship_type='COMPOSITE',
                                         forward_label=os.path.basename(new_areas),
                                         backward_label=os.path.basename(new_areas_data),
                                         message_direction='FORWARD',
                                         cardinality='ONE_TO_MANY',
                                         attributed='NONE',
                                         origin_primary_key=new_areas_guid,
                                         origin_foreign_key=new_areas_guid,
                                         destination_primary_key='',
                                         destination_foreign_key='')


sys.exit()


#  Linears



#  Points
old_points = os.path.join(renamed_fgdb, 'POINTDATA')
new_points = os.path.join(renamed_fgdb, 'POINTS')
old_points_data = os.path.join(renamed_fgdb, 'PCOMPDATA')
new_points_data = os.path.join(renamed_fgdb, 'POINTSDATA')
old_points_guid = 'POINTDATA_GUID'
new_points_guid = 'POINTS_GUID'
old_points_data = os.path.join(renamed_fgdb, 'PCOMPDATA')
new_points_data = os.path.join(renamed_fgdb, 'POINTSDATA')
old_points_data_guid = 'PCOMPDATA_GUID'
new_points_data_guid = 'POINTSDATA_GUID'
print('\n\nDeleting {0}_{1} relationship class...'.format(os.path.basename(old_points),
                                                          os.path.basename(old_points_data)))
arcpy.Delete_management(in_data='{0}_{1}'.format(os.path.basename(old_points),
                                                 os.path.basename(old_points_data)))
print('Renaming {0} to {1}...'.format(os.path.basename(old_points),
                                      os.path.basename(new_points)))
arcpy.Rename_management(in_data=old_points,
                        out_data=new_points)
print('Renaming {0} to {1}...'.format(old_points_guid,
                                      new_points_guid))
# arcpy.AlterField_management(in_table=new_points,
#                             field=old_points_guid,
#                             new_field_name=new_points_guid,
#                             new_field_alias=new_points_guid)
print('\tAdding {0} field...'.format(new_points_guid))
arcpy.AddField_management(in_table=new_points,
                          field_name=new_points_guid,
                          field_type='GUID',
                          field_is_nullable='NULLABLE',
                          field_is_required='REQUIRED')
print('\tCalculating {0} field...'.format(new_points_guid))
arcpy.CalculateField_management(in_table=new_points,
                                field=new_points_guid,
                                expression='!{0}!'.format(old_points_guid),
                                expression_type='PYTHON3')
print('\tDeleting {0} field...'.format(old_points_guid))
arcpy.DeleteField_management(in_table=new_points,
                             drop_field='[\"{0}\"]'.format(old_points_guid))
print('Renaming {0} to {1}...'.format(os.path.basename(old_points_data),
                                      os.path.basename(new_points_data)))
arcpy.Rename_management(in_data=old_points_data,
                        out_data=new_points_data)
print('Renaming {0} to {1}...'.format(old_points_guid,
                                      new_points_guid))
# arcpy.AlterField_management(in_table=new_points_data,
#                             field=old_points_guid,
#                             new_field_name=new_points_guid,
#                             new_field_alias=new_points_guid)
print('\tAdding {0} field...'.format(new_points_guid))
arcpy.AddField_management(in_table=new_points_data,
                          field_name=new_points_guid,
                          field_type='GUID',
                          field_is_nullable='NULLABLE',
                          field_is_required='REQUIRED')
print('\tCalculating {0} field...'.format(new_points_guid))
arcpy.CalculateField_management(in_table=new_points_data,
                                field=new_points_guid,
                                expression='!{0}!'.format(old_points_guid),
                                expression_type='PYTHON3')
print('\tDeleting {0} field...'.format(old_points_guid))
arcpy.DeleteField_management(in_table=new_points_data,
                             drop_field='[\"{0}\"]'.format(old_points_guid))
print('Renaming {0} to {1}...'.format(old_points_data_guid,
                                      new_points_data_guid))
# arcpy.AlterField_management(in_table=new_points_data,
#                             field=old_points_data_guid,
#                             new_field_name=new_points_data_guid,
#                             new_field_alias=new_points_data_guid)
print('\tAdding {0} field...'.format(new_points_data_guid))
arcpy.AddField_management(in_table=new_points_data,
                          field_name=new_points_data_guid,
                          field_type='GUID',
                          field_is_nullable='NULLABLE',
                          field_is_required='REQUIRED')
print('\tCalculating {0} field...'.format(new_points_data_guid))
arcpy.CalculateField_management(in_table=new_points_data,
                                field=new_points_data_guid,
                                expression='!{0}!'.format(old_points_data_guid),
                                expression_type='PYTHON3')
print('\tDeleting {0} field...'.format(old_points_data_guid))
arcpy.DeleteField_management(in_table=new_points_data,
                             drop_field='[\"{0}\"]'.format(old_points_data_guid))
print('Creating {0}_{1} relationship class...'.format(os.path.basename(new_points),
                                                      os.path.basename(new_points_data)))
arcpy.CreateRelationshipClass_management(origin_table=new_points,
                                         destination_table=new_points_data,
                                         out_relationship_class='{0}_{1}'.format(os.path.basename(new_points),
                                                                                 os.path.basename(new_points_data)),
                                         relationship_type='COMPOSITE',
                                         forward_label=os.path.basename(new_points),
                                         backward_label=os.path.basename(new_points_data),
                                         message_direction='FORWARD',
                                         cardinality='ONE_TO_MANY',
                                         attributed='NONE',
                                         origin_primary_key=new_points_guid,
                                         origin_foreign_key=new_points_guid,
                                         destination_primary_key='',
                                         destination_foreign_key='')



# Capture end_time
end_time = time.time()
# Report elapsed_time (= end_time - start_time)
print('\n\nIt took {0} to execute this.'.format(hms_string(end_time - start_time)))
# Print script filename, finish date and time
print('\n\nFinished {0} at {1} on {2}.\n'.format(script,
                                                 datetime.datetime.now().strftime('%H:%M:%S'),
                                                 datetime.datetime.now().strftime('%Y-%m-%d')))
