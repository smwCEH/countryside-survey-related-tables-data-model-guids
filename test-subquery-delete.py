import os
import sys
import platform
import datetime
import time
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


# Define file geodatabase
fgdb = r'E:\CountrysideSurvey\cs2007-wgem-combined-schema\combined-schema-{0}.gdb'.format(datetime.datetime.now().strftime('%Y%m%d'))
print('\n\nfgdb:\t\t\{0}'.format(fgdb))


parent_fc = os.path.join(fgdb, 'WGEM_SCPTDATA')
child_t = os.path.join(fgdb, 'WGEM_COMPDATA')
id_field = 'SCPTDATA_ID'
print('\n\nparent_fc:\t\t{0}\nchild_t:\t\t{1}\nid_field:\t\t{2}'.format(parent_fc,
                                                                        child_t,
                                                                        id_field))
parent_row_count = child_row_count = 0
for parent_row in sorted(arcpy.da.SearchCursor(in_table=parent_fc,
                                               field_names=['OBJECTID', id_field])):
    # print('{0:<6}\t\t{1:>10}'.format(parent_row[0],
    #                                 parent_row[1]))
    parent_row_count += 1
    for child_row in sorted(arcpy.da.SearchCursor(in_table=child_t,
                                                  field_names=['OBJECTID', id_field],
                                                  where_clause='{0} = {1}'.format(arcpy.AddFieldDelimiters(datasource=child_t,
                                                                                                           field=id_field),
                                                                                  parent_row[1]))):
        # print('\t{0:<6}\t{1:>10}'.format(child_row[0],
        #                                  child_row[1]))
        child_row_count +=1
print('parent_row_count:\t\t{0}'.format(parent_row_count))
print('child_row_count:\t\t{0}'.format(child_row_count))


parent_fc = os.path.join(fgdb, 'WGEM_LINEARDATA')
child_t = os.path.join(fgdb, 'WGEM_EVENTDATA')
id_field = 'LINEARDATA_ID'
print('\n\nparent_fc:\t\t{0}\nchild_t:\t\t{1}\nid_field:\t\t{2}'.format(parent_fc,
                                                                        child_t,
                                                                        id_field))
parent_row_count = child_row_count = 0
for parent_row in sorted(arcpy.da.SearchCursor(in_table=parent_fc,
                                               field_names=['OBJECTID', id_field])):
    # print('{0:<6}\t\t{1:>10}'.format(parent_row[0],
    #                                 parent_row[1]))
    parent_row_count += 1
    for child_row in sorted(arcpy.da.SearchCursor(in_table=child_t,
                                                  field_names=['OBJECTID', id_field],
                                                  where_clause='{0} = {1}'.format(arcpy.AddFieldDelimiters(datasource=child_t,
                                                                                                           field=id_field),
                                                                                  parent_row[1]))):
        # print('\t{0:<6}\t{1:>10}'.format(child_row[0],
        #                                  child_row[1]))
        child_row_count +=1
print('parent_row_count:\t\t{0}'.format(parent_row_count))
print('child_row_count:\t\t{0}'.format(child_row_count))


parent_fc = os.path.join(fgdb, 'WGEM_EVENTDATA')
child_t = os.path.join(fgdb, 'WGEM_SEVENTDATA')
id_field = 'EVENTDATA_ID'
print('\n\nparent_fc:\t\t{0}\nchild_t:\t\t{1}\nid_field:\t\t{2}'.format(parent_fc,
                                                                        child_t,
                                                                        id_field))
parent_row_count = child_row_count = 0
for parent_row in sorted(arcpy.da.SearchCursor(in_table=parent_fc,
                                               field_names=['OBJECTID', id_field])):
    # print('{0:<6}\t\t{1:>10}'.format(parent_row[0],
    #                                 parent_row[1]))
    parent_row_count += 1
    for child_row in sorted(arcpy.da.SearchCursor(in_table=child_t,
                                                  field_names=['OBJECTID', id_field],
                                                  where_clause='{0} = {1}'.format(arcpy.AddFieldDelimiters(datasource=child_t,
                                                                                                           field=id_field),
                                                                                  parent_row[1]))):
        # print('\t{0:<6}\t{1:>10}'.format(child_row[0],
        #                                  child_row[1]))
        child_row_count +=1
print('parent_row_count:\t\t{0}'.format(parent_row_count))
print('child_row_count:\t\t{0}'.format(child_row_count))


parent_fc = os.path.join(fgdb, 'WGEM_POINTDATA')
child_t = os.path.join(fgdb, 'WGEM_PCOMPDATA')
id_field = 'POINTDATA_ID'
print('\n\nparent_fc:\t\t{0}\nchild_t:\t\t{1}\nid_field:\t\t{2}'.format(parent_fc,
                                                                        child_t,
                                                                        id_field))
parent_row_count = child_row_count = 0
for parent_row in sorted(arcpy.da.SearchCursor(in_table=parent_fc,
                                               field_names=['OBJECTID', id_field])):
    # print('{0:<6}\t\t{1:>10}'.format(parent_row[0],
    #                                 parent_row[1]))
    parent_row_count += 1
    for child_row in sorted(arcpy.da.SearchCursor(in_table=child_t,
                                                  field_names=['OBJECTID', id_field],
                                                  where_clause='{0} = {1}'.format(arcpy.AddFieldDelimiters(datasource=child_t,
                                                                                                           field=id_field),
                                                                                  parent_row[1]))):
        # print('\t{0:<6}\t{1:>10}'.format(child_row[0],
        #                                  child_row[1]))
        child_row_count +=1
print('parent_row_count:\t\t{0}'.format(parent_row_count))
print('child_row_count:\t\t{0}'.format(child_row_count))







# Capture end_time
end_time = time.time()


# Report elapsed_time (= end_time - start_time)
print('\n\nIt took {0} to execute this.'.format(hms_string(end_time - start_time)))


# Print script filename, finish date and time
print('\n\nFinished {0} at {1} on {2}.\n'.format(script,
                                                 datetime.datetime.now().strftime('%H:%M:%S'),
                                                 datetime.datetime.now().strftime('%Y-%m-%d')))
