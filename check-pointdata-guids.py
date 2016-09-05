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


# Define file geodatabase
# fgdb = r'E:\CountrysideSurvey\esri-uk\guids\guids-{0}-without-nullable-fields.gdb'.format(datetime.datetime.now().strftime('%Y%m%d'))
fgdb = r'E:\CountrysideSurvey\esri-uk\guids\guids-20160902-without-nullable-fields.gdb'
print('\n\nfgdb:\t\t\{0}'.format(fgdb))


# data_dictionary = {}
data_dictionary = collections.OrderedDict()
data_dictionary['SCPTDATA'] = {}
data_dictionary['SCPTDATA']['id_field'] = 'SCPTDATA_ID'
data_dictionary['SCPTDATA']['guid_field'] = 'SCPTDATA_GUID'
data_dictionary['SCPTDATA']['related_table'] = 'COMPDATA'
data_dictionary['POINTDATA'] = {}
data_dictionary['POINTDATA']['id_field'] = 'POINTDATA_ID'
data_dictionary['POINTDATA']['guid_field'] = 'POINTDATA_GUID'
data_dictionary['POINTDATA']['related_table'] = 'PCOMPDATA'
data_dictionary['LINEARDATA'] = {}
data_dictionary['LINEARDATA']['id_field'] = 'LINEARDATA_ID'
data_dictionary['LINEARDATA']['guid_field'] = 'LINEARDATA_GUID'
data_dictionary['LINEARDATA']['related_table'] = 'EVENTDATA'
data_dictionary['EVENTDATA'] = {}
data_dictionary['EVENTDATA']['id_field'] = 'EVENTDATA_ID'
data_dictionary['EVENTDATA']['guid_field'] = 'EVENTDATA_GUID'
data_dictionary['EVENTDATA']['related_table'] = 'SEVENTDATA'
#
# Print data_dictionary
print(json.dumps(data_dictionary,
                 sort_keys=False,
                 indent=4))


check_guids = False


if check_guids:
    # Checking GUID fields in related file geodatabase datasets
    print('\n\nChecking GUID fields in related datasets...')
    #
    # Set sample size
    sample_size = 25
    print('sample_size:\t\t{0}'.format(sample_size))
    #
    for dataset in ['POINTDATA']:
        print('\tdataset:\t\t{0}'.format(dataset))
        #
        # Define output dataset
        dataset_out = os.path.join(fgdb, dataset)
        print('\t\tdataset_out:\t\t{0}'.format(dataset_out))
        #
        # Get ID field name from data dictionary
        id_field = data_dictionary[dataset]['id_field']
        print('\t\tid_field:\t\t{0}'.format(id_field))
        #
        # Get GUID field name from data dictionary
        guid_field = data_dictionary[dataset]['guid_field']
        print('\t\tguid_field:\t\t{0}'.format(guid_field))
        #
        # Get related table from data dictinary
        related_table = data_dictionary[dataset]['related_table']
        related_table = os.path.join(fgdb, related_table)
        print('\t\trelated_table:\t\t{0}'.format(related_table))
        #
        # Get GUIDS from file geodatabase dataset
        object_ids = [r[0] for r in arcpy.da.SearchCursor(in_table=dataset_out,
                                                          field_names=['OID@'])]
        # print('object_ids:\t{0}'.format(object_ids))
        print('\t\tlen(object_ids):\t{0}\n\t\tsample_size:\t{1}'.format(len(object_ids), sample_size))
        random_ids = random.sample(object_ids, sample_size)
        random_ids = sorted(random_ids, key=int, reverse=False)
        # print('\t\trandom_ids:\t{0}'.format(random_ids))
        oid_field = arcpy.Describe(dataset_out).OIDFieldName
        # print('\t\toid_field:\t{0}'.format(oid_field))
        where_clause = '"{0}" IN ({1})'.format(oid_field, ','.join(map(str, random_ids)))
        # print('\t\twhere_clause:\t{0}'.format(where_clause))
        rows = [row for row in arcpy.da.SearchCursor(in_table=dataset_out,
                                                     field_names=['OID@', id_field, guid_field],
                                                     where_clause=where_clause,
                                                     sql_clause=(None, 'ORDER BY ' + id_field + ', ' + guid_field))]
        row_count = len(rows)
        del rows
        print('\t\trow_count:\t\t{0}'.format(row_count))
        if row_count != sample_size:
            sys.exit('\n\nrow count != sample_size!!!\n\n')
        count = 0
        sample_list = []
        with arcpy.da.SearchCursor(in_table=dataset_out,
                                   field_names=['OID@', id_field, guid_field],
                                   where_clause=where_clause,
                                   sql_clause=(None, 'ORDER BY ' + id_field + ', ' + guid_field)) as cursor:
            for row in cursor:
                count += 1
                print('\t\t{0:<4}\t\t{1:>6}\t\t{2:>10}\t\t{3:>36}'.format(count,
                                                                          row[0],
                                                                          row[1],
                                                                          row[2]))
                sample_list.append([row[0], row[1], row[2]])
        # print('\t\tsample_list:\t{0}'.format(sample_list))
        for sample in sample_list:
            # print(sample)
            print('\t\tid:\t\t\t{0}'.format(sample[1]))
            print('\t\tguid:\t\t{0}'.format(sample[2]))
            where_clause = '"{0}" = ({1})'.format(id_field, sample[1])
            # print('\t\twhere_clause:\t{0}'.format(where_clause))
            count = 0
            rows = [row for row in arcpy.da.SearchCursor(in_table=related_table,
                                                         field_names=['OID@', id_field, guid_field],
                                                         where_clause=where_clause,
                                                         sql_clause=(None, 'ORDER BY ' + id_field + ', ' + guid_field))]
            row_count = len(rows)
            print('\t\trow_count:\t\t{0}'.format(row_count))
            del rows
            with arcpy.da.SearchCursor(in_table=related_table,
                                       field_names=['OID@', id_field, guid_field],
                                       where_clause=where_clause,
                                       sql_clause=(None, 'ORDER BY ' + id_field + ', ' + guid_field)) as cursor:
                for row in cursor:
                    count += 1
                    print('\t\trow:\t\t{0}'.format(row))
                    print('\t\trow[2]:\t\t{0}'.format(row[2]))
                    print('\t\tsample[2]:\t{0}'.format(sample[2]))
                    if row[2] == sample[2]:
                        compare = 'Yes'
                    else:
                        compare = 'No'
                    print('\t\t{0:<4}\t\t{1:>6}\t\t{2:>10}\t\t{3:>36}\t\t{4:>3}'.format(count, row[0], row[1], row[2], compare))
            if count != row_count:
                sys.exit('\n\ncount != row_count!!!\n\n')

        #
        time.sleep(1)
        #
    print('\n\nChecked GUID fields in related datasets.')


# Capture end_time
end_time = time.time()


# Report elapsed_time (= end_time - start_time)
print('\n\nIt took {0} to execute this.'.format(hms_string(end_time - start_time)))


# Print script filename, finish date and time
print('\n\nFinished {0} at {1} on {2}.\n'.format(script,
                                                 datetime.datetime.now().strftime('%H:%M:%S'),
                                                 datetime.datetime.now().strftime('%Y-%m-%d')))
