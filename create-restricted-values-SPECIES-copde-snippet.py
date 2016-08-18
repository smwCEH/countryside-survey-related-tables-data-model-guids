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
    return "{}:{:>02}:{:>05.2f}".format(h, m, s)


# Print Python version, version info, and platform architecture
print('\n\nsys.version:\t\t\t\t\t{}'.format(sys.version))
print('sys.versioninfo:\t\t\t\t{}'.format(sys.version_info))
print('platform.architecture():\t\t{}'.format(platform.architecture()))


# Print script filename, start date and time
script = os.path.basename(__file__)
print('\n\nStarted {0} at {1} on {2}...'.format(script,
                                                datetime.datetime.now().strftime('%H:%M:%S'),
                                                datetime.datetime.now().strftime('%Y-%m-%d')))


# Define NODATA value
NODATA = -9999.0


# Set arcpy overwrite output to True
arcpy.env.overwriteOutput = True
# print('\n\narcpy Environment variables:')
# environments = arcpy.ListEnvironments()
# for environment in environments:
#     print('\t{0:<30}:\t{1}'.format(environment, arcpy.env[environment]))


# Define ArcSDE path
# arcsde = r'Database Connections\Connection to LADB FEGEN2 CS2007_ADMIN.sde'
arcsde = r'C:\Users\SMW\AppData\Roaming\ESRI\Desktop10.1\ArcCatalog\Connection to LADB FEGEN2 CS2007_ADMIN.sde'
print('\n\narcsde:\t\t{}'.format(arcsde))


# Define ArcSDE user
arcsde_user = r'CS2007_ADMIN'
print('\n\narcsde_user:\t\t{}'.format(arcsde_user))


# Define ArcSDE feature dataset
arcsde_fd = r'ForesterData'
print('\n\narcsde_fd:\t\t{}'.format(arcsde_fd))


print('\n\nCreating Sweet Mapping Arcade code snippet...')
fecodes_table = arcsde + '\\' + arcsde_user + '.' + 'FECODES'
print('\n\nfecodes_table:\t\t{}'.format(fecodes_table))
where_clause = '{0} = {1}'.format(arcpy.AddFieldDelimiters(fecodes_table, 'COLUMN_NAME'),
                                  '\'VEGETATION_TYPE\'')
print('\twhere_clause:\t\t{}'.format(where_clause))
search_cursor_fields = ['COLUMN_NAME', 'CODE', 'DESCRIPTION']
print('\tsearch_cursor_fields:\t\t{}'.format(search_cursor_fields))
with arcpy.da.SearchCursor(in_table=fecodes_table,
                           field_names=search_cursor_fields,
                           where_clause=where_clause) as search_cursor:
    for search_row in search_cursor:
        print('\t{0}\t\t{1}\t\t{2}'.format(search_row[0], search_row[1], search_row[2]))
del search_row, search_cursor, search_cursor_fields





print('Created Sweet Mapping Arcade code snippet.')


# Capture end_time
end_time = time.time()


# Report elapsed_time (= end_time - start_time)
print('\n\nIt took {} to execute this.'.format(hms_string(end_time - start_time)))


# Print script filename, finish date and time
print('\n\nFinished {0} at {1} on {2}.\n'.format(script,
                                                 datetime.datetime.now().strftime('%H:%M:%S'),
                                                 datetime.datetime.now().strftime('%Y-%m-%d')))
