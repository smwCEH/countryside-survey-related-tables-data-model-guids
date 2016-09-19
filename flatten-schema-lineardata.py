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


# # Define ArcSDE path and user for original CS2007 geodatabase
# arcsde_cs_original = r'C:\Users\SMW\AppData\Roaming\ESRI\Desktop10.1\ArcCatalog\Connection to LADB FEGEN CSADMIN.sde'
# arcsde_user_cs_original = r'CSADMIN'
# print('\n\narcsde_cs_original:\t\t{0}'.format(arcsde_cs_original))
# print('arcsde_user_cs_original:\t\t{0}'.format(arcsde_user_cs_original))
#
#
# # Define ArcSDE path, user and feature dataset for restored CS2007 geodatabase
# arcsde_cs_restored = r'C:\Users\SMW\AppData\Roaming\ESRI\Desktop10.1\ArcCatalog\Connection to LADB FEGEN2 CS2007_ADMIN.sde'
# arcsde_user_cs_restored = r'CS2007_ADMIN'
# arcsde_feature_dataset_cs_restored = r'ForesterData'
# print('\n\narcsde_cs_restored:\t\t{0}'.format(arcsde_cs_restored))
# print('arcsde_user_cs_restored:\t\t{0}'.format(arcsde_user_cs_restored))
# print('arcsde_feature_dataset_cs_restored:\t\t{0}'.format(arcsde_feature_dataset_cs_restored))
#
#
# # Define ArcSDE path, user and feature dataset for WGEM geodatabase
# arcsde_cs_restored = r'C:\Users\SMW\AppData\Roaming\ESRI\Desktop10.1\ArcCatalog\Connection to LADB TBB WGEMADMIN.sde'
# arcsde_user_cs_restored = r'WGEMADMIN'
# arcsde_feature_dataset_cs_restored = r'ForesterData'
# print('\n\narcsde_cs_restored:\t\t{0}'.format(arcsde_cs_restored))
# print('arcsde_user_cs_restored:\t\t{0}'.format(arcsde_user_cs_restored))
# print('arcsde_feature_dataset_cs_restored:\t\t{0}'.format(arcsde_feature_dataset_cs_restored))























# Capture end_time
end_time = time.time()


# Report elapsed_time (= end_time - start_time)
print('\n\nIt took {0} to execute this.'.format(hms_string(end_time - start_time)))


# Print script filename, finish date and time
print('\n\nFinished {0} at {1} on {2}.\n'.format(script,
                                                 datetime.datetime.now().strftime('%H:%M:%S'),
                                                 datetime.datetime.now().strftime('%Y-%m-%d')))
