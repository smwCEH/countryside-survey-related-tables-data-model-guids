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


# Define NODATA value
NODATA = -9999.0


# Set arcpy overwrite output to True
arcpy.env.overwriteOutput = True
print('\n\narcpy Environment variables:')
environments = arcpy.ListEnvironments()
for environment in environments:
    print('\t{0:<30}:\t{1}'.format(environment, arcpy.env[environment]))


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


# Define file geodatabase
fgdb = r'E:\CountrysideSurvey\esri-uk\guids\guids-{}.gdb'.format(datetime.datetime.now().strftime('%Y%m%d'))
# fgdb = r'E:\CountrysideSurvey\esri-uk\guids\guids-20160714.gdb'
print('\n\nfgdb:\t\t\{}'.format(fgdb))


# Create file geodatabase if it doesn't exist
if not arcpy.Exists(dataset=fgdb):
    arcpy.CreateFileGDB_management(out_folder_path=os.path.dirname(fgdb),
                                   out_name=os.path.basename(fgdb),
                                   out_version='')


# data_dictionary = {}
data_dictionary = collections.OrderedDict()
data_dictionary['SCPTDATA'] = {}
data_dictionary['SCPTDATA']['id_field'] =         'SCPTDATA_ID'
data_dictionary['SCPTDATA']['guid_field'] =       'SCPTDATA_GUID'
data_dictionary['SCPTDATA']['related_table'] =    'COMPDATA'
data_dictionary['POINTDATA'] = {}
data_dictionary['POINTDATA']['id_field'] =        'POINTDATA_ID'
data_dictionary['POINTDATA']['guid_field'] =      'POINTDATA_GUID'
data_dictionary['POINTDATA']['related_table'] =   'PCOMPDATA'
data_dictionary['LINEARDATA'] = {}
data_dictionary['LINEARDATA']['id_field'] =       'LINEARDATA_ID'
data_dictionary['LINEARDATA']['guid_field'] =     'LINEARDATA_GUID'
data_dictionary['LINEARDATA']['related_table'] =  'EVENTDATA'
data_dictionary['EVENTDATA'] = {}
data_dictionary['EVENTDATA']['id_field'] =        'EVENTDATA_ID'
data_dictionary['EVENTDATA']['guid_field'] =      'EVENTDATA_GUID'
data_dictionary['EVENTDATA']['related_table'] =   'SEVENTDATA'



print(json.dumps(data_dictionary,
                 sort_keys=False,
                 indent=4))


copy_datasets = False


if copy_datasets:
    # Copy CS ArcSDE datasets to file geodatabase datasets
    print('\n\nCopying datasets...')
    for dataset in data_dictionary.keys():
        print('\tdataset:\t\t{}'.format(dataset))
        #
        # Define input dataset
        if dataset in ('SCPTDATA', 'POINTDATA', 'LINEARDATA'):
            dataset_in = arcsde + '\\' + arcsde_user + '.' + arcsde_fd + '\\' + dataset
        elif dataset in ('EVENTDATA'):
            dataset_in = arcsde + '\\' + arcsde_user +'.' + dataset
        else:
            sys.exit('\n\ndataset {} not coded for!!!\n\n'.format(dataset))
        #
        # Define output dataset
        dataset_out = os.path.join(fgdb, dataset)
        #
        #  Display input and output dataset paths
        print('\t\tdataset_in:\t\t{}'.format(dataset_in))
        print('\t\tdataset_out:\t\t{}'.format(dataset_out))
        #
        #  Delete out dataset if it already exists
        if dataset in ('SCPTDATA', 'POINTDATA', 'LINEARDATA'):      # Only copy feature classes as EVENTDATA related table will be copied as the related table of the LINEARDATA feature class
            if arcpy.Exists(dataset_out):
                arcpy.Delete_management(in_data=dataset_out,
                                        data_type='')
            #
            # Copy dataset
            arcpy.Copy_management(in_data=dataset_in,
                                  out_data=dataset_out,
                                  data_type='')
        #
        # Copy related table
        # Get related table from data dictionary
        related_table = data_dictionary[dataset]['related_table']
        print('\t\trelated_table:\t\t{}'.format(related_table))
        #
        #  Define input related table
        related_table_in = arcsde + '\\' + arcsde_user +'.' + related_table
        #
        #  Define output related table
        related_table_out = os.path.join(fgdb, related_table)
        #
        # Display input and output related table paths
        print('\t\t\trelated_table_in:\t\t{}'.format(related_table_in))
        print('\t\t\trelated_table_out:\t\t{}'.format(related_table_out))
        #
        #  Delete out related table if it already exists
        if arcpy.Exists(related_table_out):
            arcpy.Delete_management(in_data=related_table_out,
                                    data_type='')
        #
        # Copy related table
        arcpy.Copy_management(in_data=related_table_in,
                              out_data=related_table_out,
                              data_type='')
    print('Copied datasets.')


add_guids = False


if add_guids:
    # Add GUID field to file geodatabase datasets
    print('\n\nAdding GUID fields to datasets...')
    for dataset in data_dictionary.keys():
        print('\tdataset:\t\t{}'.format(dataset))
        #
        # Define output dataset
        dataset_out = os.path.join(fgdb, dataset)
        print('\t\tdataset_out:\t\t{}'.format(dataset_out))
        #
        # Get GUID field name from data dictionary
        guid_field = data_dictionary[dataset]['guid_field']
        print('\t\tguid_field:\t\t{}'.format(guid_field))
        #
        # Add GUID field to output dataset
        print('\t\tAdding GUID field {}...'.format(guid_field))
        # Note that fields with Allow NULL Values = NO can only be added to empty feature classes or tables
        # Therefore, field_is_nullable parameter must be set to 'NULLABLE'
        # See:  http://support.esri.com/technical-article/000010006
        arcpy.AddField_management(in_table=dataset_out,
                                  field_name=guid_field,
                                  field_type='GUID',
                                  field_precision='#',
                                  field_scale='#',
                                  field_length='#',
                                  field_alias='#',
                                  field_is_nullable='NULLABLE',
                                  field_is_required='REQUIRED',
                                  field_domain='#')
        print('\t\tAdded GUID field {}.'.format(guid_field))
        print('\t\tCalculating GUID field {}...'.format(guid_field))
        code_block = '''def GUID():
            import uuid
            return \'{\' + str(uuid.uuid4()) + \'}\''''
        arcpy.CalculateField_management(in_table=dataset_out,
                                        field=guid_field,
                                        expression='GUID()',
                                        expression_type='PYTHON',
                                        code_block=code_block)
        print('\t\tCalculated GUID field {}.'.format(guid_field))
        #
        # Join GUIDs to related table
        # Get related table from data dictionary
        related_table = data_dictionary[dataset]['related_table']
        print('\t\trelated_table:\t\t{}'.format(related_table))
        #
        #  Define output related table path
        related_table_out = os.path.join(fgdb, related_table)
        print('\t\t\trelated_table_out:\t\t{}'.format(related_table_out))
        #
        # Get ID field from data dictionary
        id_field = data_dictionary[dataset]['id_field']
        print('\t\t\tid_field:\t\t{}'.format(id_field))
        #
        # Add GUID field to file geodatabase tables
        print('\t\t\tAdding GUID field to related table...')
        print('\t\t\t\tin_data={}'.format(related_table_out))
        print('\t\t\t\tin_field={}'.format(id_field))
        print('\t\t\t\tjoin_table={}'.format(dataset_out))
        print('\t\t\t\tjoin_field={}'.format(id_field))
        print('\t\t\t\tfields={}'.format([guid_field]))
        arcpy.JoinField_management(in_data=related_table_out,
                                   in_field=id_field,
                                   join_table=dataset_out,
                                   join_field=id_field,
                                   fields=[guid_field])
        print('\t\t\tAdded GUID fields to related tables.')

    print('Added GUID fields to datasets.')


print('\n' * 5)


# See:  http://gis.stackexchange.com/questions/116274/select-random-rows-with-python-in-arcgis
# fc = data_dictionary['POINTDATA']['out_dataset']
fc = r'E:\CountrysideSurvey\esri-uk\guids\guids-20160715.gdb\POINTDATA'
object_ids = [r[0] for r in arcpy.da.SearchCursor(in_table=fc,
                                                  field_names=['OID@'])]
# print('object_ids:\t{}'.format(object_ids))
sample_size = int(len(object_ids) / 100)
print('\nlen(object_ids):\t{0}\nsample_size:\t{1}'.format(len(object_ids), sample_size))
random_ids = random.sample(object_ids, sample_size)
random_ids = sorted(random_ids, key=int, reverse=False)
print('random_ids:\t{0}'.format(random_ids))
oid_field = arcpy.Describe(fc).OIDFieldName
print('oid_field:\t{0}'.format(oid_field))
where_clause = '"{0}" IN ({1})'.format(oid_field, ','.join(map(str, random_ids)))
print('where_clause:\t{}'.format(where_clause))
# arcpy.MakeFeatureLayer_management(in_features=fc,
#                                   out_layer='fc_layer',
#                                   where_clause=where_clause)
count = 0
id_list = []
with arcpy.da.SearchCursor(in_table=fc,
                           field_names=['OID@', 'POINTDATA_ID', 'POINTDATA_GUID'],
                           where_clause=where_clause,
                           sql_clause=(None, 'ORDER BY POINTDATA_ID, POINTDATA_GUID')) as cursor:
    for row in cursor:
        count += 1
        print('\t{0:<4}\t\t{1:>6}\t\t{2:>8}\t\t{3:>36}'.format(count, row[0], row[1], row[2]))
        id_list.append(row[1])
print('id_list:\t{}'.format(id_list))
where_clause = '"{0}" IN ({1})'.format('POINTDATA_ID', ','.join(map(str, id_list)))
print('where_clause:\t{}'.format(where_clause))
# rt = data_dictionary['PCOMPDATA']['out_dataset']
rt = r'E:\CountrysideSurvey\esri-uk\guids\guids-20160715.gdb\PCOMPDATA'
count = 0
with arcpy.da.SearchCursor(in_table=rt,
                           field_names=['OID@', 'POINTDATA_ID', 'POINTDATA_GUID'],
                           where_clause=where_clause,
                           sql_clause=(None, 'ORDER BY POINTDATA_ID, POINTDATA_GUID')) as cursor:
    for row in cursor:
        count += 1
        print('\t{0:<4}\t\t{1:>6}\t\t{2:>8}\t\t{3:>36}'.format(count, row[0], row[1], row[2]))





# Capture end_time
end_time = time.time()


# Report elapsed_time (= end_time - start_time)
print('\n\nIt took {} to execute this.'.format(hms_string(end_time - start_time)))
print('\n\nDone.\n')
