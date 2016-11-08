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


# Define sde dictionary for holding ArcSDE parameters
sde_dictionary = collections.OrderedDict()
# sde_dictionary['CS_ORIGINAL'] = {}
# sde_dictionary['CS_ORIGINAL']['connection_file'] = r'C:\Users\SMW\AppData\Roaming\ESRI\Desktop10.1\ArcCatalog\Connection to LADB FEGEN CSADMIN.sde'
# sde_dictionary['CS_ORIGINAL']['user'] = r'CSADMIN'
# sde_dictionary['CS_ORIGINAL']['FeatureDataset'] = None
# sde_dictionary['CS_ORIGINAL']['datasets_to_copy'] = ['POINTDATA', 'PCOMPDATA']
sde_dictionary['CS_RESTORED'] = {}
sde_dictionary['CS_RESTORED']['connection_file'] = r'C:\Users\SMW\AppData\Roaming\ESRI\Desktop10.1\ArcCatalog\Connection to LADB FEGEN2 CS2007_ADMIN.sde'
sde_dictionary['CS_RESTORED']['user'] = r'CS2007_ADMIN'
sde_dictionary['CS_RESTORED']['FeatureDataset'] = r'ForesterData'
sde_dictionary['CS_RESTORED']['datasets_to_copy'] = ['BLKDATA', 'SCPTDATA', 'COMPDATA', 'LINEARDATA', 'EVENTDATA', 'SEVENTDATA', 'POINTDATA', 'PCOMPDATA']
sde_dictionary['WGEM'] = {}
sde_dictionary['WGEM']['connection_file'] = r'C:\Users\SMW\AppData\Roaming\ESRI\Desktop10.1\ArcCatalog\Connection to LADB TBB WGEMADMIN.sde'
sde_dictionary['WGEM']['user'] = r'WGEMADMIN'
sde_dictionary['WGEM']['FeatureDataset'] = r'ForesterData'
sde_dictionary['WGEM']['datasets_to_copy'] = ['BLKDATA', 'SCPTDATA', 'COMPDATA', 'LINEARDATA', 'EVENTDATA', 'SEVENTDATA', 'POINTDATA', 'PCOMPDATA']
#
# Print sde_dictionary
print('\n\nsde_dictionary:\n{0}'.format(json.dumps(sde_dictionary,
                                                   sort_keys=False,
                                                   indent=4)))
# Define data dictionary for holding feature class and related table parameters
data_dictionary = collections.OrderedDict()
data_dictionary['BLKDATA'] = {}
data_dictionary['BLKDATA']['type'] = 'Feature Class'
data_dictionary['BLKDATA']['id_field'] = 'BLKDATA_ID'
data_dictionary['BLKDATA']['guid_field'] = 'BLKDATA_GUID'
data_dictionary['BLKDATA']['child_table'] = None
data_dictionary['BLKDATA']['parent_table'] = None
data_dictionary['BLKDATA']['drop_fields'] = ['EXTENT', 'FOREST', 'CREATE_ID']
data_dictionary['SCPTDATA'] = {}
data_dictionary['SCPTDATA']['type'] = 'Feature Class'
data_dictionary['SCPTDATA']['id_field'] = 'SCPTDATA_ID'
data_dictionary['SCPTDATA']['guid_field'] = 'SCPTDATA_GUID'
data_dictionary['SCPTDATA']['drop_fields'] = ['SCPT', 'FORP', 'COVA', 'COFC', 'HABT', 'AMAW', 'SOIL', 'TCON', 'TRGH', 'TSLP',
                                              'CULT', 'GRAZED_SWARD', 'CANOPY_FRAGMENTATION', 'MAPCODE_AG', 'MAPCODE_FO', 'MAPCODE_PH', 'MAPCODE_ST', 'MAPCODE_HA', 'CPMT', 'BLK',
                                              'FOREST', 'ALTD', 'THIN_STATUS', 'INVALID_THIN', 'CPTDATA_ID', 'THINCOUPE_ID', 'CREATE_ID', 'CANOPY_COVERP', 'NATIVE_SPIS_IN_CANOPYP', 'SEMI_NATURALP',
                                              'PLANTEDP', 'POACHED_GROUND', 'SPATIAL_ERROR']
data_dictionary['SCPTDATA']['child_table'] = 'COMPDATA'
data_dictionary['SCPTDATA']['parent_table'] = None
data_dictionary['COMPDATA'] = {}
data_dictionary['COMPDATA']['type'] = 'Table'
data_dictionary['COMPDATA']['id_field'] = 'COMPDATA_ID'
data_dictionary['COMPDATA']['guid_field'] = 'COMPDATA_GUID'
data_dictionary['COMPDATA']['drop_fields'] = ['SCPT', 'SPIS', 'ORIG', 'PROP', 'ROTN', 'MIXT', 'MODEL', 'STOP', 'FCST', 'EXTLUSE',
                                              'HABT_CONDITION', 'LANDSCAPE_TYPE', 'STRUCTURE', 'BARK_STRIP_FRAYING', 'CPMT', 'PLYR', 'STOCK', 'SDATE', 'DISP', 'BLK',
                                              'FOREST', 'STRY', 'YLDC', 'SPNUM', 'THCY', 'DFST', 'DNXT', 'VOLP', 'VOLT', 'DBHP',
                                              'CREATE_ID', 'COMP_NUM', 'SPACING', 'WHCL', 'DBH_CLASS', 'FIRST_GRADEP', 'SECOND_GRADEP', 'THIRD_GRADEP', 'WOODLAND_LOSS_TYPE', 'WOODLAND_LOSS_CAUSE',
                                              'BROWSING_RATE', 'BROWSELINE', 'BASAL_SHOOTS']
data_dictionary['COMPDATA']['child_table'] = None
data_dictionary['COMPDATA']['parent_table'] = 'SCPTDATA'
data_dictionary['LINEARDATA'] = {}
data_dictionary['LINEARDATA']['type'] = 'Feature Class'
data_dictionary['LINEARDATA']['id_field'] = 'LINEARDATA_ID'
data_dictionary['LINEARDATA']['guid_field'] = 'LINEARDATA_GUID'
data_dictionary['LINEARDATA']['drop_fields'] = ['BLKDATA_ID', 'CREATE_ID']
data_dictionary['LINEARDATA']['child_table'] = 'EVENTDATA'
data_dictionary['LINEARDATA']['parent_table'] = None
data_dictionary['EVENTDATA'] = {}
data_dictionary['EVENTDATA']['type'] = 'Table'
data_dictionary['EVENTDATA']['id_field'] = 'EVENTDATA_ID'
data_dictionary['EVENTDATA']['guid_field'] = 'EVENTDATA_GUID'
data_dictionary['EVENTDATA']['drop_fields'] = ['MAPCODE_BD', 'MAPCODE_FO', 'MAPCODE_PH', 'MAPCODE_ST', 'CREATE_ID']
data_dictionary['EVENTDATA']['child_table'] = 'SEVENTDATA'
data_dictionary['EVENTDATA']['parent_table'] = 'LINEARDATA'
data_dictionary['SEVENTDATA'] = {}
data_dictionary['SEVENTDATA']['type'] = 'Table'
data_dictionary['SEVENTDATA']['id_field'] = 'SEVENTDATA_ID'
data_dictionary['SEVENTDATA']['guid_field'] = 'SEVENTDATA_GUID'
data_dictionary['SEVENTDATA']['drop_fields'] = ['CREATE_ID']
data_dictionary['SEVENTDATA']['child_table'] = None
data_dictionary['SEVENTDATA']['parent_table'] = 'EVENTDATA'
data_dictionary['POINTDATA'] = {}
data_dictionary['POINTDATA']['type'] = 'Feature Class'
data_dictionary['POINTDATA']['id_field'] = 'POINTDATA_ID'
data_dictionary['POINTDATA']['guid_field'] = 'POINTDATA_GUID'
data_dictionary['POINTDATA']['drop_fields'] = ['MAPCODE_AG', 'MAPCODE_FO', 'MAPCODE_PH', 'MAPCODE_ST', 'CREATE_ID', 'CPTDATA_ID']
data_dictionary['POINTDATA']['child_table'] = 'PCOMPDATA'
data_dictionary['POINTDATA']['parent_table'] = None
data_dictionary['PCOMPDATA'] = {}
data_dictionary['PCOMPDATA']['type'] = 'Table'
data_dictionary['PCOMPDATA']['id_field'] = 'PCOMPDATA_ID'
data_dictionary['PCOMPDATA']['guid_field'] = 'PCOMPDATA_GUID'
data_dictionary['PCOMPDATA']['drop_fields'] = ['CREATE_ID']
data_dictionary['PCOMPDATA']['child_table'] = None
data_dictionary['PCOMPDATA']['parent_table'] = 'POINTDATA'
#
# Print data_dictionary
print('\n\ndata_dictionary:\n{0}'.format(json.dumps(data_dictionary,
                                                    sort_keys=False,
                                                    indent=4)))


# Dictionary to allow conversion between arcpy.Field type and arcpy.AddField type
arcgis_field_dictionary = {'Blob': 'BLOB',
                           'Date': 'DATE',
                           'Double': 'DOUBLE',
                           'Geometry': '',
                           'Guid': 'GUID',
                           'Integer': 'LONG',
                           'OID': '',
                           'Raster': 'RASTER',
                           'Single': 'FLOAT',
                           'SmallInteger': 'SHORT',
                           'String': 'TEXT'}


# Create dictionary to hold field aliases
# Field aliases held in CS2007_ADMIN.SM_TABLE_ITEM table
print('\n\nCreating dictionary to hold field aliases...')
#
field_alias_dictionary = collections.OrderedDict()
field_alias_dictionary['BLKDATA'] = {}
field_alias_dictionary['BLKDATA']['BLK'] = 'CS Square'
# sm_table_item_table = arcsde_cs_restored + '\\' +\
#                       arcsde_user_cs_restored + '.' + 'SM_TABLE_ITEM'
sm_table_item_table = sde_dictionary['CS_RESTORED']['connection_file'] + '\\' +\
                      sde_dictionary['CS_RESTORED']['user'] + '.' + 'SM_TABLE_ITEM'
print('\t#\n\tsm_table_item_table:\t\t{0}'.format(sm_table_item_table))
search_cursor_fields = ['TABLENAME', 'ITEMNAME', 'DESCRIPTION']
print('\tsearch_cursor_fields:\t\t{0}'.format(search_cursor_fields))
for dataset in data_dictionary.keys():
    if dataset in ('SCPTDATA', 'POINTDATA', 'LINEARDATA'):      # Ignore EVENTDATA related table as will queried as the related table of the LINEARDATA feature class
        field_alias_dictionary[dataset] = {}
        print('\t#\n\tdataset:\t\t{0}'.format(dataset))
        where_clause = '{0} = {1}'.format(arcpy.AddFieldDelimiters(sm_table_item_table, 'TABLENAME'),
                                          '\'' + dataset + '\'')
        print('\t\twhere_clause:\t\t{0}'.format(where_clause))
        with arcpy.da.SearchCursor(in_table=sm_table_item_table,
                                   field_names=search_cursor_fields,
                                   where_clause=where_clause) as search_cursor:
            for search_row in search_cursor:
                alias = search_row[1] if search_row[1] == 'ORIGINAL_ID' else search_row[2]
                print('\t\t\t{0}\t\t{1}\t\t{2}'.format(search_row[0],
                                                       search_row[1],
                                                       alias))
                field_alias_dictionary[dataset][search_row[1]]= alias
                del alias
        del search_cursor
        related_table = data_dictionary[dataset]['child_table']
        print('\t\trelated_table:\t\t{0}'.format(related_table))
        field_alias_dictionary[related_table] = {}
        where_clause = '{0} = {1}'.format(arcpy.AddFieldDelimiters(sm_table_item_table, 'TABLENAME'),
                                          '\'' + related_table + '\'')
        print('\t\twhere_clause:\t\t{0}'.format(where_clause))
        with arcpy.da.SearchCursor(in_table=sm_table_item_table,
                                   field_names=search_cursor_fields,
                                   where_clause=where_clause) as search_cursor:
            for search_row in search_cursor:
                alias = search_row[1] if search_row[1] == 'ORIGINAL_ID' else search_row[2]
                print('\t\t\t{0}\t\t{1}\t\t{2}'.format(search_row[0],
                                                       search_row[1],
                                                       alias))
                field_alias_dictionary[related_table][search_row[1]] = alias
                del alias
        del search_cursor
    if dataset in ('EVENTDATA'):  # Get SEVENTDATA
        related_table = data_dictionary[dataset]['child_table']
        print('\t\trelated_table:\t\t{0}'.format(related_table))
        field_alias_dictionary[related_table] = {}
        search_cursor_fields = ['TABLENAME', 'ITEMNAME', 'DESCRIPTION']
        print('\t\tsearch_cursor_fields:\t\t{0}'.format(search_cursor_fields))
        where_clause = '{0} = {1}'.format(arcpy.AddFieldDelimiters(sm_table_item_table, 'TABLENAME'),
                                          '\'' + related_table + '\'')
        print('\t\twhere_clause:\t\t{0}'.format(where_clause))
        with arcpy.da.SearchCursor(in_table=sm_table_item_table,
                                   field_names=search_cursor_fields,
                                   where_clause=where_clause) as search_cursor:
            for search_row in search_cursor:
                alias = search_row[1] if search_row[1] == 'ORIGINAL_ID' else search_row[2]
                print('\t\t\t{0}\t\t{1}\t\t{2}'.format(search_row[0],
                                                       search_row[1],
                                                       alias))
                field_alias_dictionary[related_table][search_row[1]]= alias
                del alias
        del search_cursor
del search_cursor_fields
# Print out field_alias_dictionary
print('\t#\n\t{0}'.format(field_alias_dictionary))
# Print out lower level dictionaries for each dataset and related table
print('\t#\n\tfield_alias_dictionary[\'BLKDATA\']:\n\t{0}'.format(field_alias_dictionary['BLKDATA']))
print('\tfield_alias_dictionary[\'SCPTDATA\']:\n\t{0}'.format(field_alias_dictionary['SCPTDATA']))
print('\tfield_alias_dictionary[\'COMPDATA\']:\n\t{0}'.format(field_alias_dictionary['COMPDATA']))
print('\tfield_alias_dictionary[\'POINTDATA\']:\n\t{0}'.format(field_alias_dictionary['POINTDATA']))
print('\tfield_alias_dictionary[\'PCOMPDATA\']:\n\t{0}'.format(field_alias_dictionary['PCOMPDATA']))
print('\tfield_alias_dictionary[\'LINEARDATA\']:\n\t{0}'.format(field_alias_dictionary['LINEARDATA']))
print('\tfield_alias_dictionary[\'EVENTDATA\']:\n\t{0}'.format(field_alias_dictionary['EVENTDATA']))
print('\tfield_alias_dictionary[\'SEVENTDATA\']:\n\t{0}'.format(field_alias_dictionary['SEVENTDATA']))
# Print out selected field aliases
alias = field_alias_dictionary.get('BLKDATA', {}).get('BLK', DEFAULT)
print('\t#\n\t{0}'.format(alias))
alias = field_alias_dictionary.get('SCPTDATA', {}).get('BROAD_HABITAT', DEFAULT)
print('\t{0}'.format(alias))
alias = field_alias_dictionary.get('COMPDATA', {}).get('ROAD_VERGE_A', DEFAULT)
print('\t{0}'.format(alias))
alias = field_alias_dictionary.get('POINTDATA', {}).get('VISIT_STATUS', DEFAULT)
print('\t{0}'.format(alias))
alias = field_alias_dictionary.get('PCOMPDATA', {}).get('HABT_CODE', DEFAULT)
print('\t{0}'.format(alias))
alias = field_alias_dictionary.get('LINEARDATA', {}).get('HABT_CODE', DEFAULT)
print('\t{0}'.format(alias))
alias = field_alias_dictionary.get('EVENTDATA', {}).get('HEVENT_FROM', DEFAULT)
print('\t{0}'.format(alias))
alias = field_alias_dictionary.get('SEVENTDATA', {}).get('VEGETATION_TYPE', DEFAULT)
print('\t{0}'.format(alias))
alias = field_alias_dictionary.get('PCOMPDATA', {}).get('CHEESY_PEAS', DEFAULT)
print('\t{0}'.format(alias))
#
print('\t#\nCreated dictionary to hold field aliases.')


# Define BritishNationalGrid_100km feature class
bng_100km = r'C:\Users\SMW\AppData\Roaming\ESRI\Desktop10.1\ArcCatalog\Connection to LADB CEHCORP CORPADMIN.sde\CORPADMIN.BritishNationalGrid_100km'
print('\n\nbng_100km:\t\t{0}'.format(bng_100km))


# Define CS_RESTORED BLKDATA feature class
cs_restored_blkdata = r'C:\Users\SMW\AppData\Roaming\ESRI\Desktop10.1\ArcCatalog\Connection to LADB FEGEN2 CS2007_ADMIN.sde\CS2007_ADMIN.ForesterData\CS2007_ADMIN.BLKDATA'
print('\n\ncs_restored_blkdata:\t\t{0}'.format(cs_restored_blkdata))


# Create combined file geodatabase if it doesn't already exist
print('\n\nCreating combined file geodatabase...')
combined_fgdb = r'E:\CountrysideSurvey\cs2007-wgem-combined-schema\combined-schema-{0}.gdb'.format(datetime.datetime.now().strftime('%Y%m%d'))
print('\tcombined_fgdb:\t\t\{0}'.format(combined_fgdb))
if not arcpy.Exists(dataset=combined_fgdb):
    arcpy.CreateFileGDB_management(out_folder_path=os.path.dirname(combined_fgdb),
                                   out_name=os.path.basename(combined_fgdb),
                                   out_version='')
print('Created combined file geodatabase.')


# Create temporary SDE file geodatabases if they don't already exist
print('\n\nCreating temporary SDE file geodatabases...')
for sde in sde_dictionary.keys():
    print('\t{0}'.format(sde))
    temp_fgdb = os.path.join(os.path.dirname(combined_fgdb),
                             os.path.splitext(os.path.basename(combined_fgdb))[0] + '-' + str(sde).lower() + '.gdb')
    print('\t\ttemp_fgdb:\t\t{0}'.format(temp_fgdb))
    if not arcpy.Exists(dataset=temp_fgdb):
        arcpy.CreateFileGDB_management(out_folder_path=os.path.dirname(temp_fgdb),
                                       out_name=os.path.basename(temp_fgdb),
                                       out_version='')
print('Created temporary SDE file geodatabases.')


# Delete in_memory workspace contents
print('\n\nDeleting contents of in_memory workspace...')
arcpy.Delete_management(in_data='in_memory')
print('Deleted contents of in_memory workspace.')


# Get list, from a CSV file, of CS squares to extract from the restored SDE geodatabase
# Snippet from http://stackoverflow.com/questions/16268174/reading-rows-of-csv-file-into-string-in-python
print('\n\nGetting list of CS survey squares to copy from restore schema...')
restored_squares_csv = r'E:\CountrysideSurvey\cs2007-wgem-combined-schema\Sqs_CS_GMEP-from-clamw-20161107.csv'
print('\trestored_squares_csv:\t\t{0}'.format(restored_squares_csv))
import csv
with open(restored_squares_csv, 'r') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    # Skip the first, header, line
    next(spamreader)
    restored_squares_list = []
    for row in spamreader:
        # print(row[0])
        restored_squares_list.append(str(row[0]))
        # print(', '.join(row))
print('\trestored_squares_list:\t\t{0}'.format(restored_squares_list))
restored_squares_string = ', '.join(restored_squares_list)
print('\trestored_squares_string:\t{0}'.format(restored_squares_string))
del spamreader, csvfile


copy_datasets = True


if copy_datasets:
    print('\n\nCopying datasets...')
    # Loop through SDE geodatabases
    for sde in sde_dictionary.keys():
        print('\t{0}'.format(sde))
        temp_fgdb = os.path.join(os.path.dirname(combined_fgdb),
                                 os.path.splitext(os.path.basename(combined_fgdb))[0] + '-' + str(sde).lower() + '.gdb')
        ## Set arcpy.env.workspace to temporary SDE file geodatabase
        # arcpy.env.workspace = temp_fgdb
        # Set arcpy.env.workspace to the in_memory workspace
        arcpy.env.workspace = 'in_memory'
        print('\t\tarcpy.env.workspace:\t\t{0}'.format(arcpy.env.workspace))
        # Loop through feature classes and related tables
        for dataset in sde_dictionary[sde]['datasets_to_copy']:
            print('\t\t{0}'.format(dataset))
            # Define in dataset
            if sde_dictionary[sde]['FeatureDataset'] == None:
                dataset_in = sde_dictionary[sde]['connection_file'] +\
                             '\\' +\
                             dataset
            elif data_dictionary[dataset]['type'] == 'Table':
                dataset_in = sde_dictionary[sde]['connection_file'] +\
                             '\\' +\
                             dataset
            elif data_dictionary[dataset]['type'] == 'Feature Class':
                dataset_in = sde_dictionary[sde]['connection_file'] +\
                             '\\' +\
                             sde_dictionary[sde]['user'] +\
                             '.' +\
                             sde_dictionary[sde]['FeatureDataset'] +\
                             '\\' +\
                             dataset
            else:
                sys.exit('\n\nNot coded for!!!\nCannot determine dataset_in!!!\n')
            print('\t\t\tdataset_in:\t\t\t{0}'.format(dataset_in))
            desc = arcpy.Describe(dataset_in)
            dataType = desc.dataType
            print('\t\t\tdataType:\t\t\t{0}'.format(dataType))
            try:
                shapeType = desc.shapeType
            except AttributeError:
                shapeType = None
            print('\t\t\tshapeType:\t\t\t{0}'.format(shapeType))
            # Define out dataset
            dataset_out = os.path.join(arcpy.env.workspace,
                                       dataset + '_' + sde)
            print('\t\t\tdataset_out:\t\t{0}'.format(dataset_out))
            # Delete out dataset if it already exists
            if arcpy.Exists(dataset=dataset_out):
                arcpy.Delete_management(in_data=dataset_out,
                                        data_type=data_dictionary[dataset]['type'])
            # Create empty out dataset using in dataset as a template
            if data_dictionary[dataset]['type'] == 'Feature Class':
                # Create empty feature class
                arcpy.CreateFeatureclass_management(out_path=os.path.dirname(dataset_out),
                                                    out_name=os.path.basename(dataset_out),
                                                    geometry_type=shapeType,
                                                    template=dataset_in,
                                                    spatial_reference=arcpy.SpatialReference(27700))
            elif data_dictionary[dataset]['type'] == 'Table':
                # Create empty table
                arcpy.CreateTable_management(out_path=os.path.dirname(dataset_out),
                                             out_name=os.path.basename(dataset_out),
                                             template=dataset_in)
            else:
                sys.exit('\n\nNot coded for!!!Create table isn\'t FeatureClass or Table!!!\n')
            # Delete non-CS2007 fields
            print('\t\t\tDeleting non-CS2007 fields from out {0} {1}...'.format(data_dictionary[dataset]['type'].lower(),
                                                                                dataset_out))
            print('\t\t\t\tdrop_fields:\t\t{0}'.format(data_dictionary[dataset]['drop_fields']))
            arcpy.DeleteField_management(in_table=dataset_out,
                                         drop_field=data_dictionary[dataset]['drop_fields'])
            print('\t\t\tDeleted non-CS2007 fields from out {0} {1}.'.format(data_dictionary[dataset]['type'].lower(),
                                                                             dataset_out))

            # Append data from in dataset to out dataset
            print('\t\t\tAppending rows from in {0} {1} to out {0} {2}...'.format(data_dictionary[dataset]['type'].lower(),
                                                                                  dataset_in,
                                                                                  dataset_out))
            arcpy.Append_management(inputs=[dataset_in],
                                    target=dataset_out,
                                    schema_type='NO_TEST')
            print('\t\t\tAppended rows from in {0} {1} to out {0} {2}...'.format(data_dictionary[dataset]['type'].lower(),
                                                                                 dataset_in,
                                                                                 dataset_out))
            result = arcpy.GetCount_management(dataset_out)
            count = int(result.getOutput(0))
            print('\t\t\tCount:\t\t{0}'.format(count))
            # Delete non-Summer 2016 Pilot squares from the CS_RESTORED feature classes or non-Welsh data from the WGEM feature classes
            if sde == 'CS_RESTORED':
                print('\t\t\tRemoving non-Summer 2016 Pilot data from feature class...')
                intersect_fc = cs_restored_blkdata
                intersect_layer = 'fl_cs_restored_blkdata'
                where_clause = '{0} IN ({1})'.format(arcpy.AddFieldDelimiters(datasource=intersect_fc,
                                                                                  field='BLK'),
                                                       restored_squares_string)
            elif sde == 'WGEM':# and dataset in ('BLKDATA', 'SCPTDATA', 'LINEARDATA', 'POINTDATA'):
                print('\t\t\tRemoving non-Welsh data from feature class...')
                intersect_fc = bng_100km
                intersect_layer = 'fl_bng_100km'
                where_clause = '{0} IN (\'SG\', \'SH\', \'SJ\', \'SM\', \'SN\', \'SO\', \'SR\', \'SS\', \'ST\')'.format(arcpy.AddFieldDelimiters(datasource=intersect_fc,
                                                                                                                                                 field='OS_TILE'))
            else:
                sys.exit('\n\nPython script not coded for sde {0}\n\n'.format(sde))
            print('\t\t\t\tintersect_fc:\t\t{0}'.format(intersect_fc))
            print('\t\t\t\tintersect_layer:\t{0}'.format(intersect_layer))
            print('\t\t\t\twhere_clause:\t\t{0}'.format(where_clause))
            if dataset in ('BLKDATA', 'SCPTDATA', 'LINEARDATA', 'POINTDATA'):
                # result = arcpy.GetCount_management(in_rows=dataset_out)
                # count = int(result.getOutput(0))
                # print('\t\t\t\tCount:\t\t{0}'.format(count))
                arcpy.MakeFeatureLayer_management(in_features=intersect_fc,
                                                  out_layer=intersect_layer,
                                                  where_clause=where_clause)
                result = arcpy.GetCount_management(in_rows=intersect_layer)
                count = int(result.getOutput(0))
                print('\t\t\t\tCount:\t\t\t\t{0}'.format(count))
                featurelayer = 'featurelayer'
                if arcpy.Exists(featurelayer):
                    arcpy.Delete_management(featurelayer)
                arcpy.MakeFeatureLayer_management(in_features=dataset_out,
                                                  out_layer=featurelayer)
                arcpy.SelectLayerByLocation_management(in_layer=featurelayer,
                                                       overlap_type='INTERSECT',
                                                       select_features=intersect_layer,
                                                       selection_type='NEW_SELECTION',
                                                       invert_spatial_relationship='INVERT')
                result = arcpy.GetCount_management(in_rows=featurelayer)
                count = int(result.getOutput(0))
                print('\t\t\t\tCount:\t\t{0}'.format(count))
                arcpy.DeleteFeatures_management(in_features=featurelayer)
                arcpy.SelectLayerByAttribute_management(in_layer_or_view=featurelayer,
                                                        selection_type='CLEAR_SELECTION')
                result = arcpy.GetCount_management(in_rows=dataset_out)
                count = int(result.getOutput(0))
                print('\t\t\t\tCount:\t\t{0}'.format(count))
                # Recalculate the feature class extent
                print('\t\t\t\tRe-calculating the extent of feature class {0}...'.format(dataset_out))
                arcpy.RecalculateFeatureClassExtent_management(in_features=dataset_out)
                print('\t\t\t\tRe-calculated the extent of feature class {0}.'.format(dataset_out))
                print('\t\t\tRemoved non-Welsh data from feature class.')

            # Delete non-Summer 2016 Pilot squares from the CS_RESTORED tables or non-Welsh data from the WGEM tables
            # if sde == 'WGEM' and dataset in ('COMPDATA', 'EVENTDATA', 'SEVENTDATA', 'PCOMPDATA'):
            #     print('\t\t\tRemoving non-Welsh data from table...')
            #     result = arcpy.GetCount_management(in_rows=dataset_out)
            #     count = int(result.getOutput(0))
            #     print('\t\t\t\tCount:\t\t{0}'.format(count))
            #     tableview = 'tableview'
            #     parent_table = arcpy.env.workspace + '\\' + data_dictionary[dataset]['parent_table'] + '_' + sde
            #     print('\t\t\t\tparent_table:\t\t{0}'.format(parent_table))
            #     id_field = data_dictionary[data_dictionary[dataset]['parent_table']]['id_field']
            #     print('\t\t\t\tid_field:\t\t\t{0}'.format(id_field))
            #     # Can't use subqueries (to select values in one table based upon values in another) with in_memory feature classes and tables
            #     # So creating table view using a where clause based upon unique values in the parent table obtained using an arcpy.da.SearchCursor
            #     values = [row[0]for row in arcpy.da.SearchCursor(in_table=parent_table,
            #                                                       field_names=id_field)]
            #     unique_values = set(values)
            #     print('\t\t\t\tunique_values:\t\t{0}'.format(unique_values))
            #     print('\t\t\t\tnumber of unique_values:\t\t{0}'.format(len(unique_values)))
            #     where_clause = '{0} NOT IN ({1})'.format(arcpy.AddFieldDelimiters(datasource=dataset_out,
            #                                                                   field=id_field),
            #                                          ','.join(map(str, unique_values)))
            #     print('\t\t\t\twhere_clause:\t\t{0}'.format(where_clause))
            #     arcpy.MakeTableView_management(in_table=dataset_out,
            #                                    out_view=tableview,
            #                                    where_clause=where_clause)
            #     result = arcpy.GetCount_management(in_rows=tableview)
            #     count = int(result.getOutput(0))
            #     print('\t\t\t\tCount:\t\t{0}'.format(count))
            #     arcpy.DeleteRows_management(in_rows=tableview)
            #     arcpy.SelectLayerByAttribute_management(in_layer_or_view=tableview,
            #                                             selection_type='CLEAR_SELECTION')
            #     result = arcpy.GetCount_management(in_rows=dataset_out)
            #     count = int(result.getOutput(0))
            #     print('\t\t\t\tCount:\t\t{0}'.format(count))
            #     print('\t\t\tRemoved non-Welsh data from table.')
            # # Set VISIT_STATUS and REASON_FOR_CHANGE to Null in SCPTDATA and POINTDATA feature class and EVENTDATA related table
            # if dataset in ('SCPTDATA', 'POINTDATA', 'EVENTDATA'):
            #     for null_field in ('VISIT_STATUS', 'REASON_FOR_CHANGE'):
            #         print('\t\t\tSetting {0} to <Null> in {1} {2}...'.format(null_field,
            #                                                                  dataset_out,
            #                                                                  data_dictionary[dataset]['type'].lower()))
            #         arcpy.CalculateField_management(in_table=dataset_out,
            #                                         field=null_field,
            #                                         expression='None',
            #                                         expression_type='PYTHON',
            #                                         code_block='')
            #         print('\t\t\tSet {0} to <Null> in {1} {2}.'.format(null_field,
            #                                                                dataset_out,
            #                                                                data_dictionary[dataset]['type'].lower()))
            # # Add any additional fields to feature classes and related tables
            # print('\t\t\tAdding additional fields...')
            # # Add Point_Proximity field to POINTDATA feature class
            # if dataset == 'POINTDATA':
            #     print('\t\t\t\tAdding Point_Proximity field to POINTDATA feature class...')
            #     arcpy.AddField_management(in_table=dataset_out,
            #                               field_name='Point_Proximity',
            #                               field_type='TEXT',
            #                               field_precision='',
            #                               field_scale='',
            #                               field_length=10,
            #                               field_alias='Point Proximity',
            #                               field_is_nullable='NULLABLE',
            #                               field_is_required='NON_REQUIRED',
            #                               field_domain='')
            #     print('\t\t\t\tAdded Point_Proximity field to POINTDATA feature class.')
            # # Add Polygon_Area field to SCPTDATA feature class
            # if dataset == 'SCPTDATA':
            #     print('\t\t\t\tAdding Polygon_Area field to SCPTDATA feature class...')
            #     arcpy.AddField_management(in_table=dataset_out,
            #                               field_name='Polygon_Area',
            #                               field_type='FLOAT',
            #                               field_precision=12,
            #                               field_scale=3,
            #                               field_length='',
            #                               field_alias='Polygon Area',
            #                               field_is_nullable='NULLABLE',
            #                               field_is_required='NON_REQUIRED',
            #                               field_domain='')
            #     print('\t\t\t\tAdded Polygon_Area field to SCPTDATA feature class.')
            #     print('\t\t\t\t\tCalculating Polygon_Area...')
            #     arcpy.CalculateField_management(in_table=dataset_out,
            #                                     field='Polygon_Area',
            #                                     expression='!shape.area@SQUAREMETERS!',
            #                                     expression_type='PYTHON',
            #                                     code_block='#')
            #     print('\t\t\t\t\tCalculated Polygon_Area.')
            # # Add Linear_Length field to LINEARDATA feature class
            # if dataset == 'LINEARDATA':
            #     print('\t\t\t\tAdding Linear_Length field to LINEARDATA feature class...')
            #     arcpy.AddField_management(in_table=dataset_out,
            #                               field_name='Linear_Length',
            #                               field_type='FLOAT',
            #                               field_precision=12,
            #                               field_scale=3,
            #                               field_length='',
            #                               field_alias='Linear Length',
            #                               field_is_nullable='NULLABLE',
            #                               field_is_required='NON_REQUIRED',
            #                               field_domain='')
            #     print('\t\t\t\tAdded Linear_Length field to LINEARDATA feature class.')
            #     print('\t\t\t\t\tCalculating Linear_Length...')
            #     arcpy.CalculateField_management(in_table=dataset_out,
            #                                     field='Linear_Length',
            #                                     expression='!shape.length@METERS!',
            #                                     expression_type='PYTHON',
            #                                     code_block='#')
            #     print('\t\t\t\t\tCalculated Linear_Length.')
            # # Add CONDITION, DISEASE_SIGNS and HABITAT_BOXES fields to PCOMPDATA related table
            # if dataset == 'PCOMPDATA':
            #     field_names = [f.name for f in arcpy.ListFields(dataset=dataset_out)]
            #     if 'CONDITION' not in field_names:
            #         print('\t\t\t\tAdding CONDITION field to PCOMPDATA related table...')
            #         arcpy.AddField_management(in_table=dataset_out,
            #                                   field_name='CONDITION',
            #                                   field_type='SHORT',
            #                                   field_precision=3,
            #                                   field_scale='',
            #                                   field_length='',
            #                                   field_alias='Condition',
            #                                   field_is_nullable='NULLABLE',
            #                                   field_is_required='NON_REQUIRED',
            #                                   field_domain='')
            #         print('\t\t\t\tAdded CONDITION field to PCOMPDATA feature class.')
            #     if 'DISEASE_SIGNS' not in field_names:
            #         print('\t\t\t\tAdding DISEASE_SIGNS field to PCOMPDATA related table...')
            #         arcpy.AddField_management(in_table=dataset_out,
            #                                   field_name='DISEASE_SIGNS',
            #                                   field_type='SHORT',
            #                                   field_precision=3,
            #                                   field_scale='',
            #                                   field_length='',
            #                                   field_alias='Signs of disease',
            #                                   field_is_nullable='NULLABLE',
            #                                   field_is_required='NON_REQUIRED',
            #                                   field_domain='')
            #         print('\t\t\t\tAdded DISEASE_SIGNS field to PCOMPDATA feature class.')
            #     if 'HABITAT_BOXES' not in field_names:
            #         print('\t\t\t\tAdding HABITAT_BOXES field to PCOMPDATA related table...')
            #         arcpy.AddField_management(in_table=dataset_out,
            #                                   field_name='HABITAT_BOXES',
            #                                   field_type='SHORT',
            #                                   field_precision=3,
            #                                   field_scale='',
            #                                   field_length='',
            #                                   field_alias='Habitat boxes',
            #                                   field_is_nullable='NULLABLE',
            #                                   field_is_required='NON_REQUIRED',
            #                                   field_domain='')
            #         print('\t\t\t\tAdded HABITAT_BOXES field to PCOMPDATA feature class.')
            # # Add Editor and Date of edit fields to BLKDATA feature class
            # print('\t\t\t\tAdding Editor and Date of Edit fields to {0}...'.format(dataset_out))
            # arcpy.AddField_management(in_table=dataset_out,
            #                           field_name='EDITOR',
            #                           field_type='TEXT',
            #                           field_precision='',
            #                           field_scale='',
            #                           field_length=25,
            #                           field_alias='Editor',
            #                           field_is_nullable='NULLABLE',
            #                           field_is_required='NON_REQUIRED',
            #                           field_domain='')
            # arcpy.AddField_management(in_table=dataset_out,
            #                           field_name='DATE_OF_EDIT',
            #                           field_type='DATE',
            #                           field_precision='',
            #                           field_scale='',
            #                           field_length='',
            #                           field_alias='Date of edit',
            #                           field_is_nullable='NULLABLE',
            #                           field_is_required='NON_REQUIRED',
            #                           field_domain='')
            # print('\t\t\t\tAdded Editor and Date of Edit fields to {0}.'.format(dataset_out))
            # print('\t\t\tAdded additional fields.')
            # # Add field aliases
            # print('\t\t\tAdding field aliases...')
            # field_names = arcpy.ListFields(dataset=dataset_out)
            # for field in field_names:
            #     if field.name not in ['OBJECTID', 'SHAPE', 'SHAPE.AREA', 'SHAPE.LEN'] and field.aliasName == field.name:
            #         print('\t\t\t\t{0} is a type of {1} with a length of {2}'.format(field.name,
            #                                                                        field.type,
            #                                                                        field.length))
            #         field_alias = field_alias_dictionary.get(dataset, {}).get(field.name, DEFAULT)
            #         if field_alias is not None:
            #             print('\t\t\t\tfield_alias:\t\t{0}'.format(field_alias))
            #             # Can't seem to replace upper-case alias name with lower-case, so replace alias name with dummy alias before setting to lower-case alias!
            #             # print('in_table={0}\tfield={1}\tnew_field_alias={2}'.format(dataset_out, field.name, field_alias))
            #             if field.name.upper() in ['USE', 'SPECIES', 'PROPORTION', 'HEIGHT', 'CONDITION', 'WIDTH', 'TUSSOCKINESS']:
            #                 # print('Setting cheesey alias...')
            #                 arcpy.AlterField_management(in_table=dataset_out,
            #                                             field=field.name,
            #                                             new_field_alias='CHEESE')
            #                 # print('Set cheesey alias.')
            #             # print('new_field_alias={0}'.format(field_alias))
            #             arcpy.AlterField_management(in_table=dataset_out,
            #                                         field=field.name,
            #                                         new_field_alias=field_alias)
            # print('\t\t\tAdded field aliases.')
            # # Add GUID field to output dataset if it doesn't already exist (Note: cannot delete required fields including GUIDs)
            # guid_field = data_dictionary[dataset]['guid_field']
            # print('\t\t\tguid_field:\t\t{0}'.format(guid_field))
            # if not arcpy.ListFields(dataset=dataset_out,
            #                         wild_card=guid_field):
            #     print('\t\t\tAdding GUID field {0} to out {1} {2}...'.format(guid_field,
            #                                                                  data_dictionary[dataset]['type'].lower(),
            #                                                                  dataset_out))
            #     arcpy.AddField_management(in_table=dataset_out,
            #                               field_name=guid_field,
            #                               field_type='GUID',
            #                               field_precision='#',
            #                               field_scale='#',
            #                               field_length='#',
            #                               field_alias='#',
            #                               field_is_nullable='NULLABLE',  # field_is_nullable='NULLABLE',
            #                               field_is_required='REQUIRED',
            #                               field_domain='#')
            #     print('\t\t\tAdded GUID field {0} to out {1} {2}.'.format(guid_field,
            #                                                               data_dictionary[dataset]['type'].lower(),
            #                                                               dataset_out))
            # print('\t\t\tCalculating GUID field {0} in out {1} {2}...'.format(guid_field,
            #                                                                   data_dictionary[dataset]['type'].lower(),
            #                                                                   dataset_out))
            # code_block = '''def GUID():
            #     import uuid
            #     return \'{\' + str(uuid.uuid4()) + \'}\''''
            # arcpy.CalculateField_management(in_table=dataset_out,
            #                                 field=guid_field,
            #                                 expression='GUID()',
            #                                 expression_type='PYTHON',
            #                                 code_block=code_block)
            # print('\t\t\tCalculated GUID field {0} in out {1} {2}.'.format(guid_field,
            #                                                                data_dictionary[dataset]['type'].lower(),
            #                                                                dataset_out))
            #             # # Copy GUID from parent table to child table based upon CS2007 id field
            # if data_dictionary[dataset]['parent_table'] != None:
            #     print('\t\t\tJoining GUID fields to related tables...')
            #     in_data = dataset_out
            #     print('\t\t\t\tin_data:\t\t{0}'.format(in_data))
            #     parent_table = data_dictionary[dataset]['parent_table']
            #     in_field = data_dictionary[parent_table]['id_field']
            #     print('\t\t\t\tin_field:\t\t{0}'.format(in_field))
            #     join_table = parent_table + '_' + sde
            #     print('\t\t\t\tjoin_table:\t\t{0}'.format(join_table))
            #     join_field = data_dictionary[parent_table]['id_field']
            #     print('\t\t\t\tjoin_field:\t\t{0}'.format(join_field))
            #     fields = [data_dictionary[parent_table]['guid_field']]
            #     print('\t\t\t\tfields:\t\t\t{0}'.format(fields))
            #     arcpy.JoinField_management(in_data=in_data,
            #                                in_field=in_field,
            #                                join_table=join_table,
            #                                join_field=join_field,
            #                                fields=fields)
            #     print('\t\t\tAdded GUID field to related tables.')
            # # Copy in_memory dataset to file geodatabase
            # print('\t\t\tCopying in_memory dataset to file geodatabase...')
            # out_data = os.path.join(temp_fgdb, dataset + '_' + sde)
            # print('\t\t\t\tout_data:\t\t{0}'.format(out_data))
            # if arcpy.Exists(dataset=out_data):
            #     print('\t\t\t\t\tDeleting out_data {0}...'.format(out_data))
            #     arcpy.Delete_management(in_data=out_data)
            #     print('\t\t\t\t\tDeleted out_data {0}.'.format(out_data))
            # if data_dictionary[dataset]['type'] == 'Feature Class':
            #     arcpy.CopyFeatures_management(in_features=dataset_out,
            #                                   out_feature_class=out_data)
            # elif data_dictionary[dataset]['type'] == 'Table':
            #     # Create empty table
            #     arcpy.CopyRows_management(in_rows=dataset_out,
            #                               out_table=out_data)
            # else:
            #     sys.exit('\n\nNot coded for!!!Create table isn\'t FeatureClass or Table!!!\n')
            # print('\t\t\tCopied in_memory dataset to file geodatabase.')
            # # Cannot create attribute indexes on in_memory feature classes or tables
            # # so add attribute index to GUID fields in the copied file geodatabase feature class or table
            # guid_fields = arcpy.ListFields(dataset=out_data,
            #                                wild_card='',
            #                                field_type='GUID')
            # for guid_field in guid_fields:
            #     print('\t\t\tAdding attribute index to GUID field {0} in out {1} {2}...'.format(guid_field.name,
            #                                                                                     data_dictionary[dataset]['type'].lower(),
            #                                                                                     out_data))
            #     index_name = guid_field.name + '_IDX'
            #     if len(arcpy.ListIndexes(dataset=out_data,
            #                              wild_card=index_name)) > 0:
            #         print('\t\t\t\tDeleting attribute index {0} in out {1} {2}...'.format(index_name,
            #                                                                               data_dictionary[dataset]['type'].lower(),
            #                                                                               out_data))
            #         arcpy.RemoveIndex_management(in_table=out_data,
            #                                      index_name=index_name)
            #         print('\t\t\t\tDeleted attribute index {0} in out {1} {2}.'.format(index_name,
            #                                                                            data_dictionary[dataset]['type'].lower(),
            #                                                                            out_data))
            #     arcpy.AddIndex_management(in_table=out_data,
            #                               fields=guid_field.name,
            #                               index_name=index_name,
            #                               unique='UNIQUE',
            #                               ascending='NON_ASCENDING')
            #     print('\t\t\tAdded attribute index to GUID field {0} in out {1} {2}.'.format(guid_field.name,
            #                                                                                  data_dictionary[dataset]['type'].lower(),
            #                                                                                  out_data))
    print('Copied datasets.')


del copy_datasets


sys.exit()


# Delete in_memory workspace contents
print('\n\nDeleting contents of in_memory workspace...')
arcpy.Delete_management(in_data='in_memory')
print('Deleted contents of in_memory workspace.')


check_guids = True


if check_guids:
    # Checking GUID fields in related file geodatabase datasets
    print('\n\nChecking GUID fields in related datasets...')
    # Set sample size
    sample_size = 25
    print('\tsample_size:\t\t{0}'.format(sample_size))
    # Loop through SDE geodatabases
    for sde in sde_dictionary.keys():
        print('\t{0}'.format(sde))
        temp_fgdb = os.path.join(os.path.dirname(combined_fgdb),
                                 os.path.splitext(os.path.basename(combined_fgdb))[0] + '-' + str(sde).lower() + '.gdb')
        # Set arcpy.env.workspace to temporary SDE file geodatabase
        arcpy.env.workspace = temp_fgdb
        del temp_fgdb
        print('\t\tarcpy.env.workspace:\t\t{0}'.format(arcpy.env.workspace))
        # Loop through feature classes and related tables
        print(sde_dictionary[sde])
        parent_tables = sde_dictionary[sde]['datasets_to_copy'].copy()
        # print('\t\tparent_tables:\t\t{0}'.format(parent_tables))
        child_tables = ['BLKDATA', 'COMPDATA', 'SEVENTDATA', 'PCOMPDATA']
        for child_table in child_tables:
            if child_table in parent_tables:
                parent_tables.remove(child_table)
        del child_table, child_tables
        print('\t\tparent_tables:\t\t{0}'.format(parent_tables))
        for parent_table in parent_tables:
            print('\t\t{0}'.format(parent_table))
            # Define out dataset
            dataset_out = parent_table + '_' + sde
            print('\t\t\tdataset_out:\t\t{0}'.format(dataset_out))
            # Define ID field
            id_field = data_dictionary[parent_table]['id_field']
            print('\t\t\tid_field:\t\t\t{0}'.format(id_field))
            # Define GUID field
            guid_field = data_dictionary[parent_table]['guid_field']
            print('\t\t\tguid_field:\t\t\t{0}'.format(guid_field))
            # Define child table
            child_table = data_dictionary[parent_table]['child_table']
            child_table = child_table + '_' + sde
            print('\t\t\tchild_table:\t\t{0}'.format(child_table))
            # Get GUIDS from file geodatabase dataset
            object_ids = [r[0] for r in arcpy.da.SearchCursor(in_table=dataset_out,
                                                              field_names=['OID@'])]
            # print('object_ids:\t{0}'.format(object_ids))
            print('\t\t\tlen(object_ids):\t{0}\n\t\t\tsample_size:\t\t{1}'.format(len(object_ids), sample_size))
            random_ids = random.sample(object_ids, sample_size)
            random_ids = sorted(random_ids,
                                key=int,
                                reverse=False)
            # print('\t\trandom_ids:\t{0}'.format(random_ids))
            oid_field = arcpy.Describe(dataset_out).OIDFieldName
            # print('\t\toid_field:\t{0}'.format(oid_field))
            where_clause = '"{0}" IN ({1})'.format(oid_field, ','.join(map(str, random_ids)))
            print('\t\t\twhere_clause:\t{0}'.format(where_clause))
            rows = [row for row in arcpy.da.SearchCursor(in_table=dataset_out,
                                                         field_names=['OID@', id_field, guid_field],
                                                         where_clause=where_clause,
                                                         sql_clause=(None, 'ORDER BY ' + id_field + ', ' + guid_field))]
            row_count = len(rows)
            del rows
            print('\t\t\trow_count:\t\t\t{0}'.format(row_count))
            if row_count != sample_size:
                sys.exit('\n\nrow count != sample_size!!!\n\n')
            del row_count
            count = 0
            sample_list = []
            with arcpy.da.SearchCursor(in_table=dataset_out,
                                       field_names=['OID@', id_field, guid_field],
                                       where_clause=where_clause,
                                       sql_clause=(None, 'ORDER BY ' + id_field + ', ' + guid_field)) as cursor:
                for row in cursor:
                    count += 1
                    print('\t\t\t{0:<4}\t\t{1:>6}\t\t{2:>10}\t\t{3:>36}'.format(count,
                                                                              row[0],
                                                                              row[1],
                                                                              row[2]))
                    sample_list.append([row[0], row[1], row[2]])
            del row, cursor, count
            # print('\t\tsample_list:\t{0}'.format(sample_list))
            for sample in sample_list:
                # print(sample)
                print('\t\t\tid:\t\t\t{0}'.format(sample[1]))
                print('\t\t\tguid:\t\t{0}'.format(sample[2]))
                where_clause = '"{0}" = ({1})'.format(id_field, sample[1])
                print('\t\t\twhere_clause:\t\t{0}'.format(where_clause))
                count = 0
                rows = [row for row in arcpy.da.SearchCursor(in_table=child_table,
                                                             field_names=['OID@', id_field, guid_field],
                                                             where_clause=where_clause,
                                                             sql_clause=(None, 'ORDER BY ' + id_field + ', ' + guid_field))]
                row_count = len(rows)
                print('\t\t\trow_count:\t\t{0}'.format(row_count))
                del rows
                if row_count > 0:
                    with arcpy.da.SearchCursor(in_table=child_table,
                                               field_names=['OID@', id_field, guid_field],
                                               where_clause=where_clause,
                                               sql_clause=(None, 'ORDER BY ' + id_field + ', ' + guid_field)) as cursor:
                        for row in cursor:
                            count += 1
                            print('\t\t\trow:\t\t{0}'.format(row))
                            print('\t\t\trow[2]:\t\t{0}'.format(row[2]))
                            print('\t\t\tsample[2]:\t{0}'.format(sample[2]))
                            if row[2] == sample[2]:
                                compare = 'Yes'
                            else:
                                compare = 'No'
                            print('\t\t\t{0:<4}\t\t{1:>6}\t\t{2:>10}\t\t{3:>36}\t\t{4:>3}'.format(count, row[0], row[1], row[2], compare))
                        del row
                    del cursor
                if count != row_count:
                    sys.exit('\n\ncount != row_count!!!\n\n')
                del where_clause, count, row_count
            del dataset_out, id_field, guid_field, child_table, object_ids, random_ids, oid_field, sample_list
        del parent_tables, parent_table
    del sde
    del sample_size
    print('Checked GUID fields in related datasets.')


del check_guids


append_datasets = True


if append_datasets:
    print('\n\nAppending datasets into single file geodatabase...')
    # Create empty feature classes and related tables in the combined file geodatabase
    print('\tCreating empty feature classes and related tables in the combined file geodatabase...')
    sde = 'WGEM'
    for dataset in sde_dictionary[sde]['datasets_to_copy']:
        print('\t\tdataset:\t\t{0}'.format(dataset))
        dataset_out = os.path.join(combined_fgdb, dataset)
        print('\t\t\tdataset_out:\t\t{0}'.format(dataset_out))
        dataset_template = os.path.join(os.path.join(os.path.dirname(combined_fgdb),
                                                     os.path.splitext(os.path.basename(combined_fgdb))[0] + '-' + str(sde).lower() + '.gdb'),
                                        dataset + '_' + sde)
        print('\t\t\tdataset_template:\t\t{0}'.format(dataset_template))
        desc = arcpy.Describe(dataset_template)
        data_type = desc.dataType
        print('\t\t\tdata_type:\t\t\t{0}'.format(data_type))
        try:
            shape_type = desc.shapeType
        except AttributeError:
            shape_type = None
        print('\t\t\tshape_type:\t\t\t{0}'.format(shape_type))
        if arcpy.Exists(dataset_out):
            arcpy.Delete_management(dataset_out)
        if data_dictionary[dataset]['type'] == 'Feature Class':
            # Create empty feature class
            arcpy.CreateFeatureclass_management(out_path=os.path.dirname(dataset_out),
                                                out_name=os.path.basename(dataset_out),
                                                geometry_type=shape_type,
                                                template=dataset_template,
                                                spatial_reference=arcpy.SpatialReference(27700))
        elif data_dictionary[dataset]['type'] == 'Table':
            # Create empty table
            arcpy.CreateTable_management(out_path=os.path.dirname(dataset_out),
                                         out_name=os.path.basename(dataset_out),
                                         template=dataset_template)
        else:
            sys.exit('\n\nNot coded for!!!Create table isn\'t FeatureClass or Table!!!\n')
        del dataset_out, dataset_template, desc, data_type, shape_type
    del sde
    print('\tCreated empty feature classes and related tables in the combined file geodatabase.')
    # Append feature classes and tables into empty feature classes and tables in the combined file geodatabase
    for sde in sde_dictionary.keys():
        print('\t{0}'.format(sde))
        temp_fgdb = os.path.join(os.path.dirname(combined_fgdb),
                                 os.path.splitext(os.path.basename(combined_fgdb))[0] + '-' + str(sde).lower() + '.gdb')
        print('\ttemp_fgdb:\t\t{0}'.format(temp_fgdb))
        # Loop through feature classes and related tables
        for dataset in sde_dictionary[sde]['datasets_to_copy']:
            print('\t\t{0}'.format(dataset))
            # Define in dataset
            dataset_in = os.path.join(temp_fgdb,
                                      dataset + '_' + sde)
            print('\t\t\tdataset_in:\t\t{0}'.format(dataset_in))
            result = arcpy.GetCount_management(dataset_in)
            count = int(result.getOutput(0))
            print('\t\t\tCount:\t\t{0}'.format(count))
            del result, count
            dataset_out = os.path.join(combined_fgdb, dataset)
            print('\t\t\tdataset_out:\t\t{0}'.format(dataset_out))
            # Append data from in dataset to out dataset
            print('\t\t\tAppending rows from in {0} {1} to out {0} {2}...'.format(data_dictionary[dataset]['type'].lower(),
                                                                                  dataset_in,
                                                                                  dataset_out))
            arcpy.Append_management(inputs=[dataset_in],
                                    target=dataset_out,
                                    schema_type='NO_TEST')
            print('\t\t\tAppended rows from in {0} {1} to out {0} {2}...'.format(data_dictionary[dataset]['type'].lower(),
                                                                                 dataset_in,
                                                                                 dataset_out))
            result = arcpy.GetCount_management(dataset_out)
            count = int(result.getOutput(0))
            print('\t\t\tCount:\t\t{0}'.format(count))
            del result, count
            del dataset_in, dataset_out
        del temp_fgdb
    del sde
    print('Appended datasets into single file geodatabase.')


del append_datasets


create_relationship_classes = True


if create_relationship_classes:
    # Add relationship classes
    print('\n\nCreating relationship classes...')
    # Set arcpy.env.workspace to the combined file geodatabase
    arcpy.env.workspace = combined_fgdb
    print('\t#\n\tarcpy.env.workspace:\t\t{0}\n\t#'.format(arcpy.env.workspace))
    # Loop though parent tables to create relationship classes for child tables
    for dataset in ['SCPTDATA', 'LINEARDATA', 'EVENTDATA', 'POINTDATA']:
        print('\tdataset:\t\t\t{0}'.format(dataset))
        # Define output dataset
        dataset_out = os.path.join(combined_fgdb, dataset)
        print('\t\tdataset_out:\t\t\t{0}'.format(dataset_out))
        # Get related table from data dictionary
        child_table = data_dictionary[dataset]['child_table']
        print('\t\tchild_table:\t\t\t{0}'.format(child_table))
        # Get related table from data dictionary
        guid_field = data_dictionary[dataset]['guid_field']
        print('\t\tguid_field:\t\t\t{0}'.format(guid_field))
        # Define output related table path
        child_table_out = os.path.join(combined_fgdb, child_table)
        print('\t\tchild_table_out:\t\t{0}'.format(child_table_out))
        #  Define relationship class parameters
        print('\t\tCreating relationship class...')
        print('\t\t\torigin_table:\t\t\t\t{0}'.format(dataset_out))
        print('\t\t\tdestination_table:\t\t\t{0}'.format(child_table_out))
        out_relationship_class = os.path.basename(dataset_out) + '_' + os.path.basename(child_table_out)
        print('\t\t\tout_relationship_class:\t\t{0}'.format(out_relationship_class))
        relationship_type = 'COMPOSITE'
        print('\t\t\trelationship_type:\t\t\t{0}'.format(relationship_type))
        forward_label = os.path.basename(dataset_out)
        print('\t\t\tforward_label:\t\t\t\t{0}'.format(forward_label))
        backward_label = os.path.basename(child_table_out)
        print('\t\t\tbackward_label:\t\t\t\t{0}'.format(backward_label))
        message_direction = 'FORWARD'
        print('\t\t\tmessage_direction:\t\t\t{0}'.format(message_direction))
        cardinality = 'ONE_TO_MANY'
        print('\t\t\tcardinality:\t\t\t\t{0}'.format(cardinality))
        attributed = 'NONE'
        print('\t\t\tattributed:\t\t\t\t\t{0}'.format(attributed))
        origin_primary_key = guid_field
        print('\t\t\torigin_primary_key:\t\t\t{0}'.format(origin_primary_key))
        origin_foreign_key = guid_field
        print('\t\t\torigin_foreign_key:\t\t\t{0}'.format(origin_foreign_key))
        destination_primary_key = ''
        print('\t\t\tdestination_primary_key:\t{0}'.format(destination_primary_key))
        destination_foreign_key = ''
        print('\t\t\tdestination_foreign_key:\t{0}'.format(destination_foreign_key))
        # Delete relationship class if it already exists
        if arcpy.Exists(dataset=os.path.join(combined_fgdb, out_relationship_class)):
            print('\t\t\tDeleting existing relationship class {0}...'.format(out_relationship_class))
            arcpy.Delete_management(in_data=os.path.join(combined_fgdb, out_relationship_class))
            print('\t\t\tDeleted existing relationship class {0}.'.format(out_relationship_class))
        # Create relationship class
        arcpy.CreateRelationshipClass_management(origin_table=dataset_out,
                                                 destination_table=child_table_out,
                                                 out_relationship_class=out_relationship_class,
                                                 relationship_type=relationship_type,
                                                 forward_label=forward_label,
                                                 backward_label=backward_label,
                                                 message_direction=message_direction,
                                                 cardinality=cardinality,
                                                 attributed=attributed,
                                                 origin_primary_key=origin_primary_key,
                                                 origin_foreign_key=origin_foreign_key,
                                                 destination_primary_key=destination_primary_key,
                                                 destination_foreign_key=destination_foreign_key)
        print('\t\tCreated relationship class.')
    del destination_foreign_key, destination_primary_key, origin_foreign_key, origin_primary_key
    del attributed, cardinality, message_direction, backward_label, forward_label
    del relationship_type, out_relationship_class, child_table_out, guid_field, child_table, dataset_out
    print('Created relationship classes.')


del create_relationship_classes


copy_domains = True


if copy_domains:
    print('\n\nCopying domains and applying to fields...')
    # Set arcpy.env.workspace to the combined file geodatabase
    arcpy.env.workspace = combined_fgdb
    print('\t#\n\tarcpy.env.workspace:\t\t{0}\n\t#'.format(arcpy.env.workspace))
    # Define in_memory or file geodatabase to store domain tables
    domain_fgdb = os.path.join(os.path.dirname(combined_fgdb),
                               'combined-schema-{0}-domains.gdb'.format(datetime.datetime.now().strftime('%Y%m%d')))
    # domain_fgdb = 'in_memory'
    print('\tdomain_fgdb:\t\t\t{0}'.format(domain_fgdb))
    # Create temporary file geodatabase if required
    if domain_fgdb == 'in_memory':
        print('\tUsing in_memory workspace to store domain tables.')
    else:
        print('\tUsing file geodatabase to store domain_tables.')
        if arcpy.Exists(domain_fgdb):
            print('\t\tDeleting domain_fgdb {0}...'.format(domain_fgdb))
            arcpy.Delete_management(domain_fgdb)
            print('\t\tDeleted domain_fgdb {0}.'.format(domain_fgdb))
        print('\tCreating domain_fgdb {0}...'.format(domain_fgdb))
        arcpy.CreateFileGDB_management(out_folder_path=os.path.dirname(domain_fgdb),
                                       out_name=os.path.basename(domain_fgdb),
                                       out_version='CURRENT')
        print('\tCreated domain_fgdb {0}.'.format(domain_fgdb))
    # Define FECODES table
    fecodes_table = os.path.join(sde_dictionary['WGEM']['connection_file'],
                                 r'FECODES')
    print('\t#\n\tfecodes_table:\t\t{0}'.format(fecodes_table))
    fecodes_table_field = r'COLUMN_NAME'
    print('\tfecodes_table_field:\t\t{0}'.format(fecodes_table_field))
    # Get COLUMN_NAMES from FECODES table
    column_names = [row[0] for row in arcpy.da.SearchCursor(fecodes_table, fecodes_table_field)]
    del fecodes_table_field
    unique_column_names = sorted(set(column_names))
    del column_names
    print('\tunique_column_names:\t\t{0}'.format(unique_column_names))
    print(len(unique_column_names))
    domain_code_field = 'CODE'
    domain_description_field = 'DESCRIPTION'
    domain_fields = []
    domain_fields.append(domain_code_field)
    domain_fields.append(domain_description_field)
    print('\tdomain_fields:\t\t{0}'.format(domain_fields))
    # Loop though unique COLUMN_NAMES to create domain tables
    for column_name in unique_column_names:
        print('\t#\n\tcolumn_name:\t\t{0}'.format(column_name))
        # Define domain table
        domain_table = os.path.join(domain_fgdb,
                                    column_name)
        print('\t\tdomain_table:\t\t{0}'.format(domain_table))
        if arcpy.Exists(domain_table):
            arcpy.Delete_management(domain_table)
        arcpy.CreateTable_management(out_path=domain_fgdb,
                                     out_name=column_name)
        print('\t\t\tGetting field characteristics...')
        field_type_list = []
        field_length = int(NODATA)
        for table in ['SCPTDATA', 'LINEARDATA', 'POINTDATA', 'COMPDATA', 'EVENTDATA', 'SEVENTDATA', 'PCOMPDATA']:
            print('\t\t\t\ttable:\t\t{0}'.format(table))
            list_fields = arcpy.ListFields(dataset=os.path.join(combined_fgdb,
                                                                table),
                                           wild_card=column_name)
            if len(list_fields) > 0:
                for list_field in list_fields:
                    print('\t\t\t\t\t{0}\t{1}\t{2}'.format(list_field.name,
                                                         list_field.type,
                                                         list_field.length))
                    field_type_list.append(arcgis_field_dictionary[list_field.type])
                    if list_field.type == 'String':
                        field_length = max(field_length, list_field.length)
                del list_field
            del list_fields
        field_types = set(field_type_list)
        del field_type_list
        print('\t\t\t\tfield_types:\t\t{0}'.format(field_types))
        if len(field_types) != 1:
            sys.exit()
        if field_length > int(NODATA):
            print('\t\t\t\tfield_length:\t\t{0}'.format(field_length))
        print('\t\t\tGot field characteristics.')
        field_length_addfield = field_length if list(field_types)[0] == 'TEXT' else None
        del field_length
        arcpy.AddField_management(in_table=domain_table,
                                  field_name='CODE',
                                  field_type=list(field_types)[0],
                                  field_length=field_length_addfield)
        arcpy.AddField_management(in_table=domain_table,
                                  field_name='DESCRIPTION',
                                  field_type='TEXT',
                                  field_length=40)
        del field_types, field_length_addfield
        # Create InsertCursor to add rows to domain table
        insert_cursor = arcpy.da.InsertCursor(domain_table,
                                              domain_fields)
        # Use a SearchCursor to loop through domain values for each column and add rows to domain table
        expression = u'{0} = \'{1}\''.format('COLUMN_NAME',
                                             column_name)
        print('\t\texpression:\t\t{0}'.format(expression))
        sql_clause = (None, 'ORDER BY CODE, DESCRIPTION')
        print('\t\tsql_clause:\t\t{0}'.format(sql_clause))
        for row in arcpy.da.SearchCursor(in_table=fecodes_table,
                                         field_names=domain_fields,
                                         where_clause=expression,
                                         sql_clause=sql_clause):
            print('\t\t\t{0}\t\t{1}'.format(row[0],
                                            row[1]))
            insert_cursor.insertRow((row[0], row[1]))
        del insert_cursor, expression, sql_clause, row
        # Delete any identical records in the domain table
        print('\t\tDeleting any identical records in the {0} table...'.format(domain_table))
        arcpy.DeleteIdentical_management(in_dataset=domain_table,
                                         fields=['Code', 'Description'])
        print('\t\tDeleted any identical records in the {0} table.'.format(domain_table))
        # Add domain to combined file geodatabase
        domain_description = column_name + ' domain'
        print('\t\tdomain_description:\t\t{0}'.format(domain_description))
        print('\t\tAdding {0} domain to combined file geodatabase {1}...'.format(column_name,
                                                                                 combined_fgdb))
        arcpy.TableToDomain_management(in_table=domain_table,
                                       code_field=domain_code_field,
                                       description_field=domain_description_field,
                                       in_workspace=combined_fgdb,
                                       domain_name=column_name,
                                       domain_description=domain_description,
                                       update_option='REPLACE')
        del domain_table, domain_description
        print('\t\tAdded {0} domain to combined file geodatabase {1}.'.format(column_name,
                                                                            combined_fgdb))
        # Assign domain to field
        print('\t\tAssigning domain to fields...')
        tables = ['SCPTDATA', 'LINEARDATA', 'POINTDATA', 'COMPDATA', 'EVENTDATA', 'SEVENTDATA', 'PCOMPDATA']
        for table in tables:
            print('\t\t\ttable:\t\t{0}'.format(table))
            fields = arcpy.ListFields(os.path.join(combined_fgdb,
                                                   table))
            for field in fields:
                assign = 'Assign domain' if column_name == field.name else 'Do not assign domain'
                if assign == 'Assign domain':
                    print('\t\t\t\t{0} is a type of {1}\t\t{2}'.format(field.name,
                                                                       field.type,
                                                                       assign))
                    arcpy.AssignDomainToField_management(in_table=os.path.join(combined_fgdb, table),
                                                         field_name=column_name,
                                                         domain_name=column_name,
                                                         subtype_code='')
                del assign
            del field, fields
        print('\t\tAssigned domain to fields.')
        del table, tables
    del domain_code_field, domain_description_field, domain_fields
    del column_name, unique_column_names
    del fecodes_table
    # Define HABITATS table - for Primary Attribute (HABT_CODE) field
    habitats_table = os.path.join(sde_dictionary['WGEM']['connection_file'],
                                  'HABITATS')
    print('\t#\n\thabitats_table:\t\t{0}'.format(habitats_table))
    domain_code_field = 'HABT_CODE'
    domain_description_field = 'HABITAT_NAME'
    domain_fields = []
    domain_fields.append(domain_code_field)
    domain_fields.append(domain_description_field)
    print('\tdomain_fields:\t\t{0}'.format(domain_fields))
    # Define domain table
    domain_table = os.path.join(domain_fgdb,
                                domain_code_field)
    print('\t\tdomain_table:\t\t{0}'.format(domain_table))
    if arcpy.Exists(domain_table):
        arcpy.Delete_management(domain_table)
    arcpy.CreateTable_management(out_path=domain_fgdb,
                                 out_name=domain_code_field)
    print('\t\t\tGetting field characteristics...')
    field_type_list = []
    field_length = int(NODATA)
    for table in ['SCPTDATA', 'LINEARDATA', 'POINTDATA', 'COMPDATA', 'EVENTDATA', 'SEVENTDATA', 'PCOMPDATA']:
        print('\t\t\t\ttable:\t\t{0}'.format(table))
        list_fields = arcpy.ListFields(dataset=os.path.join(combined_fgdb,
                                                            table),
                                       wild_card=domain_code_field)
        if len(list_fields) > 0:
            for list_field in list_fields:
                print('\t\t\t\t\t{0}\t{1}\t{2}'.format(list_field.name,
                                                     list_field.type,
                                                     list_field.length))
                field_type_list.append(arcgis_field_dictionary[list_field.type])
                if list_field.type == 'String':
                    field_length = max(field_length, list_field.length)
            del list_field
        del list_fields
    field_types = set(field_type_list)
    del field_type_list
    print('\t\t\t\tfield_types:\t\t{0}'.format(field_types))
    if len(field_types) != 1:
        sys.exit()
    if field_length > int(NODATA):
        print('\t\t\t\tfield_length:\t\t{0}'.format(field_length))
    print('\t\t\tGot field characteristics.')
    field_length_addfield = field_length if list(field_types)[0] == 'TEXT' else None
    del field_length
    arcpy.AddField_management(in_table=domain_table,
                              field_name='CODE',
                              field_type=list(field_types)[0],
                              field_length=field_length_addfield)
    arcpy.AddField_management(in_table=domain_table,
                              field_name='DESCRIPTION',
                              field_type='TEXT',
                              field_length=255)
    del field_types, field_length_addfield
    # Create InsertCursor to add rows to domain table
    insert_cursor = arcpy.da.InsertCursor(domain_table,
                                          ['CODE', 'DESCRIPTION'])
    # Use a SearchCursor to loop through domain values for the HABITAT_NAME column and add rows to domain table
    sql_clause = (None, 'ORDER BY {0}, {1}'.format(domain_code_field,
                                                   domain_description_field))
    print('\t\tsql_clause:\t\t{0}'.format(sql_clause))
    for row in arcpy.da.SearchCursor(in_table=habitats_table,
                                     field_names=domain_fields,
                                     sql_clause=sql_clause):
        print('\t\t\t{0}\t\t{1}'.format(row[0],
                                        row[1]))
        insert_cursor.insertRow((row[0], row[1]))
    del insert_cursor, sql_clause, row
    # Delete any identical records in the domain table
    print('\t\tDeleting any identical records in the {0} table...'.format(domain_table))
    arcpy.DeleteIdentical_management(in_dataset=domain_table,
                                     fields=['Code', 'Description'])
    print('\t\tDeleted any identical records in the {0} table.'.format(domain_table))
    # Add domain to combined file geodatabase
    domain_description = domain_code_field + ' domain'
    print('\t\tdomain_description:\t\t{0}'.format(domain_description))
    print('\t\tAdding {0} domain to combined file geodatabase {1}...'.format(domain_code_field,
                                                                             combined_fgdb))
    arcpy.TableToDomain_management(in_table=domain_table,
                                   code_field='CODE',
                                   description_field='DESCRIPTION',
                                   in_workspace=combined_fgdb,
                                   domain_name=domain_code_field,
                                   domain_description=domain_description,
                                   update_option='REPLACE')
    del domain_table, domain_description
    print('\t\tAdded {0} domain to combined file geodatabase {1}.'.format(domain_code_field,
                                                                          combined_fgdb))
    # Assign domain to field
    print('\t\tAssigning domain to fields...')
    tables = ['SCPTDATA', 'LINEARDATA', 'POINTDATA', 'COMPDATA', 'EVENTDATA', 'SEVENTDATA', 'PCOMPDATA']
    for table in tables:
        print('\t\t\ttable:\t\t{0}'.format(table))
        fields = arcpy.ListFields(os.path.join(combined_fgdb,
                                               table))
        for field in fields:
            assign = 'Assign domain' if domain_code_field == field.name else 'Do not assign domain'
            if assign == 'Assign domain':
                print('\t\t\t\t{0} is a type of {1}\t\t{2}'.format(field.name,
                                                                   field.type,
                                                                   assign))
                arcpy.AssignDomainToField_management(in_table=os.path.join(combined_fgdb, table),
                                                     field_name=domain_code_field,
                                                     domain_name=domain_code_field,
                                                     subtype_code='')
            del assign
        del field, fields
    print('\t\tAssigned domain to fields.')
    del table, tables
    del domain_code_field, domain_description_field, domain_fields
    del habitats_table
    #
    del domain_fgdb
    #
    print('\t#\nCopied domains and applied to fields.')


del copy_domains


# Capture end_time
end_time = time.time()
# Report elapsed_time (= end_time - start_time)
print('\n\nIt took {0} to execute this.'.format(hms_string(end_time - start_time)))
# Print script filename, finish date and time
print('\n\nFinished {0} at {1} on {2}.\n'.format(script,
                                                 datetime.datetime.now().strftime('%H:%M:%S'),
                                                 datetime.datetime.now().strftime('%Y-%m-%d')))
