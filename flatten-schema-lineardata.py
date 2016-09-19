import os
import sys
import platform
import datetime
import time
import random
import json
import collections


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
    return "{0}:{1:>02}:{2:>05.2f}".format(h, m, s)


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
# print('\n\narcpy Environment variables:')
# environments = arcpy.ListEnvironments()
# for environment in environments:
#     print('\t{0:<30}:\t{1}'.format(environment, arcpy.env[environment]))


# Define ArcSDE path, user and feature dataset for WGEM geodatabase
# arcsde_wgem = r'C:\Users\SMW\AppData\Roaming\ESRI\Desktop10.1\ArcCatalog\Connection to LADB TBB WGEMADMIN.sde'
# arcsde_user_wgem = r'WGEMADMIN'
# arcsde_feature_dataset_wgem = r'ForesterData'
# print('\n\narcsde_wgem:\t\t\t\t\t{0}'.format(arcsde_wgem))
# print('arcsde_user_wgem:\t\t\t\t{0}'.format(arcsde_user_wgem))
# print('arcsde_feature_dataset_wgem:\t{0}'.format(arcsde_feature_dataset_wgem))


# Define out file geodatabase
fgdb = r'E:\CountrysideSurvey\cs2007-wgem-combined-schema\flattened-schema-lineardata-{0}.gdb'.format(datetime.datetime.now().strftime('%Y%m%d'))
print('\n\nfgdb:\t\t\{0}'.format(fgdb))


# Create file geodatabase if it doesn't already exist
if not arcpy.Exists(dataset=fgdb):
    arcpy.CreateFileGDB_management(out_folder_path=os.path.dirname(fgdb),
                                   out_name=os.path.basename(fgdb),
                                   out_version='')


# Define output dataset
fc_out = os.path.join(fgdb, r'lineardata_flattened')
#  Display input and output dataset paths
print('\n\nfc_out:\t\t{0}'.format(fc_out))


# Delete out dataset if it already exists
if arcpy.Exists(fc_out):
    arcpy.Delete_management(in_data=fc_out)


fc_in = r'C:\Users\SMW\AppData\Roaming\ESRI\Desktop10.1\ArcCatalog\Connection to LADB TBB WGEMADMIN.sde\WGEMADMIN.ForesterData\WGEMADMIN.LINEARDATA'
print('\n\nfc_in:\t\t{0}'.format(fc_in))


# Create empty out feature class using in LINEARDATA feature class as a template
desc = arcpy.Describe(fc_in)
dataType = desc.dataType
print('\tdataType:\t\t{0}'.format(dataType))
shapeType = desc.shapeType
print('\tshapeType:\t\t{0}'.format(shapeType))
arcpy.CreateFeatureclass_management(out_path=os.path.dirname(fc_out),
                                    out_name=os.path.basename(fc_out),
                                    geometry_type=shapeType,
                                    template=fc_in,
                                    spatial_reference=arcpy.SpatialReference(27700))


# List fields in out feature class and append to fc_out_fields list
fields = arcpy.ListFields(fc_out)
fc_out_fields = []
for field in fields:
    print('\t{0} is a type of {1} with a length of {2}'.format(field.name,
                                                               field.type,
                                                               field.length))
    fc_out_fields.append(field.name)
fc_out_fields.extend(['BLKDATA_ID', 'CREATE_ID'])
fc_out_fields.extend(['MAPCODE_BD', 'MAPCODE_FO', 'MAPCODE_PH', 'MAPCODE_ST', 'CREATE_ID'])
print('\tfc_out_fields:\t\t{0}'.format(fc_out_fields))
time.sleep(5)
del field, fields


# List fields in EVENTDATA related table
table_in = r'C:\Users\SMW\AppData\Roaming\ESRI\Desktop10.1\ArcCatalog\Connection to LADB TBB WGEMADMIN.sde\WGEMADMIN.EVENTDATA'
print('\n\ntable_in:\t{0}'.format(table_in))
fields = arcpy.ListFields(table_in)
for field in fields:
    if field.name not in fc_out_fields:
        print('\t{0} is a type of {1} with a length of {2}'.format(field.name,
                                                                       field.type,
                                                                       field.length))
        print('\tAdding field {0} to fc_out {1}...'.format(field.name, fc_out))
        arcpy.AddField_management(in_table=fc_out,
                                  field_name=field.name,
                                  field_type=field.type,
                                  field_precision=field.precision,
                                  field_scale=field.scale,
                                  field_length=field.length,
                                  field_alias='',
                                  field_is_nullable=field.isNullable,
                                  field_is_required=field.required,
                                  field_domain=field.domain)
del field, fields


# Delete fc_out_fields
del fc_out_fields


# Add linears to fc_out using arcpy.da.InsertCursor()
cursor = arcpy.da.InsertCursor(fc_out, ['SHAPE@', 'VISIT_STATUS'])
array = arcpy.Array([arcpy.Point(357150, 532150),
                     arcpy.Point(357300, 532300)])
polyline = arcpy.Polyline(array)
cursor.insertRow((polyline, 1))
array = arcpy.Array([arcpy.Point(357150, 532200),
                     arcpy.Point(357300, 532350)])
polyline = arcpy.Polyline(array)
cursor.insertRow((polyline, 2))
array = arcpy.Array([arcpy.Point(357150, 532250),
                     arcpy.Point(357300, 532400)])
polyline = arcpy.Polyline(array)
cursor.insertRow((polyline, 3))
array = arcpy.Array([arcpy.Point(357150, 532300),
                     arcpy.Point(357300, 532450)])
polyline = arcpy.Polyline(array)
cursor.insertRow((polyline, None))
del cursor


# Capture end_time
end_time = time.time()


# Report elapsed_time (= end_time - start_time)
print('\n\nIt took {0} to execute this.'.format(hms_string(end_time - start_time)))


# Print script filename, finish date and time
print('\n\nFinished {0} at {1} on {2}.\n'.format(script,
                                                 datetime.datetime.now().strftime('%H:%M:%S'),
                                                 datetime.datetime.now().strftime('%Y-%m-%d')))
