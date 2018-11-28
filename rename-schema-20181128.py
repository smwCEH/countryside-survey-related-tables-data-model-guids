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


combined_fgdb = r'G:\CountrysideSurvey\cs2007-wgem-combined-schema\combined-schema-20181127.gdb'


renamed_fgdb = r'G:\CountrysideSurvey\cs2007-wgem-combined-schema\combined-schema-20181127-renamed.gdb'


print('\n\nCopying combined_fgdb to renamed_fgdb...')
if arcpy.Exists(dataset=renamed_fgdb):
	print('Deleting exising renamed_fgdb...')
	arcpy.Delete_management(in_data=renamed_fgdb)
arcpy.Copy_management(in_data= combined_fgdb,
                      out_data=renamed_fgdb)


print('\n\nRenaming blocks...')
old_blocks = os.path.join(renamed_fgdb, 'BLKDATA')
new_blocks = os.path.join(renamed_fgdb, 'SURVEYSQUARES')
arcpy.Rename_management(in_data=old_blocks,
                        out_data=new_blocks)


print('\n\nRenaming blocks GUID...')
arcpy.AlterField_management(in_table=new_blocks,
                            field='BLKDATA_GUID',
                            new_field_name='SURVEYSQUARES_GUID',
                            new_field_alias='SURVEYSQUARES_GUID')


# print('\n\nRenaming areas...')
# old_areas = os.path.join(renamed_fgdb, 'SCPTDATA')
# new_areas = os.path.join(renamed_fgdb, 'AREAS')
# arcpy.Rename_management(in_data=old_areas,
#                         out_data=new_areas)









# Capture end_time
end_time = time.time()
# Report elapsed_time (= end_time - start_time)
print('\n\nIt took {0} to execute this.'.format(hms_string(end_time - start_time)))
# Print script filename, finish date and time
print('\n\nFinished {0} at {1} on {2}.\n'.format(script,
                                                 datetime.datetime.now().strftime('%H:%M:%S'),
                                                 datetime.datetime.now().strftime('%Y-%m-%d')))
