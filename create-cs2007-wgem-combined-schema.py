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
sde_dictionary['CS_ORIGINAL'] = {}
sde_dictionary['CS_ORIGINAL']['connection_file'] = r'C:\Users\SMW\AppData\Roaming\ESRI\Desktop10.1\ArcCatalog\Connection to LADB FEGEN CSADMIN.sde'
sde_dictionary['CS_ORIGINAL']['user'] = r'CSADMIN'
sde_dictionary['CS_ORIGINAL']['FeatureDataset'] = None
sde_dictionary['CS_ORIGINAL']['copy_datasets'] = ['POINTDATA', 'PCOMPDATA']
sde_dictionary['CS_RESTORED'] = {}
sde_dictionary['CS_RESTORED']['connection_file'] = r'C:\Users\SMW\AppData\Roaming\ESRI\Desktop10.1\ArcCatalog\Connection to LADB FEGEN2 CS2007_ADMIN.sde'
sde_dictionary['CS_RESTORED']['user'] = r'CS2007_ADMIN'
sde_dictionary['CS_RESTORED']['FeatureDataset'] = r'ForesterData'
sde_dictionary['CS_RESTORED']['copy_datasets'] = ['BLKDATA', 'SCPTDATA', 'COMPDATA', 'LINEARDATA', 'EVENTDATA', 'SEVENTDATA']
sde_dictionary['WGEM'] = {}
sde_dictionary['WGEM']['connection_file'] = r'C:\Users\SMW\AppData\Roaming\ESRI\Desktop10.1\ArcCatalog\Connection to LADB TBB WGEMADMIN.sde'
sde_dictionary['WGEM']['user'] = r'WGEMADMIN'
sde_dictionary['WGEM']['FeatureDataset'] = r'ForesterData'
sde_dictionary['WGEM']['copy_datasets'] = ['BLKDATA', 'SCPTDATA', 'COMPDATA', 'LINEARDATA', 'EVENTDATA', 'SEVENTDATA', 'POINTDATA', 'PCOMPDATA']
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
for dataset in data_dictionary.keys():
    if dataset in ('SCPTDATA', 'POINTDATA', 'LINEARDATA'):      # Ignore EVENTDATA related table as will queried as the related table of the LINEARDATA feature class
        field_alias_dictionary[dataset] = {}
        print('\t#\n\tdataset:\t\t{0}'.format(dataset))
        search_cursor_fields = ['TABLENAME', 'ITEMNAME', 'DESCRIPTION']
        print('\t\tsearch_cursor_fields:\t\t{0}'.format(search_cursor_fields))
        where_clause = '{0} = {1}'.format(arcpy.AddFieldDelimiters(sm_table_item_table, 'TABLENAME'),
                                          '\'' + dataset + '\'')
        print('\t\twhere_clause:\t\t{0}'.format(where_clause))
        with arcpy.da.SearchCursor(in_table=sm_table_item_table,
                                   field_names=search_cursor_fields,
                                   where_clause=where_clause) as search_cursor:
            for search_row in search_cursor:
                print('\t\t\t{0}\t\t{1}\t\t{2}'.format(search_row[0],
                                                       search_row[1],
                                                       search_row[2]))
                field_alias_dictionary[dataset][search_row[1]]= search_row[2]
        del search_cursor, search_cursor_fields
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
                print('\t\t\t{0}\t\t{1}\t\t{2}'.format(search_row[0],
                                                       search_row[1],
                                                       search_row[2]))
                field_alias_dictionary[related_table][search_row[1]] = search_row[2]
        del search_cursor, search_cursor_fields
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
                print('\t\t\t{0}\t\t{1}\t\t{2}'.format(search_row[0],
                                                       search_row[1],
                                                       search_row[2]))
                field_alias_dictionary[related_table][search_row[1]]= search_row[2]
        del search_cursor, search_cursor_fields
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


# Create combined file geodatabase if it doesn't already exist
print('\n\nCreating combined file geodatabase...')
fgdb = r'E:\CountrysideSurvey\cs2007-wgem-combined-schema\combined-schema-{0}.gdb'.format(datetime.datetime.now().strftime('%Y%m%d'))
print('\tfgdb:\t\t\{0}'.format(fgdb))
if not arcpy.Exists(dataset=fgdb):
    arcpy.CreateFileGDB_management(out_folder_path=os.path.dirname(fgdb),
                                   out_name=os.path.basename(fgdb),
                                   out_version='')
print('Created combined file geodatabase.')


# Create temporary SDE file geodatabases if they don't already exist
print('\n\nCreating temporary SDE file geodatabases...')
for sde in sde_dictionary.keys():
    print('\t{0}'.format(sde))
    temp_fgdb = os.path.join(os.path.dirname(fgdb),
                             os.path.splitext(os.path.basename(fgdb))[0] + '-' + str(sde).lower() + '.gdb')
    print('\t\ttemp_fgdb:\t\t{0}'.format(temp_fgdb))
    if not arcpy.Exists(dataset=temp_fgdb):
        arcpy.CreateFileGDB_management(out_folder_path=os.path.dirname(temp_fgdb),
                                       out_name=os.path.basename(temp_fgdb),
                                       out_version='')
print('Created temporary SDE file geodatabases.')


copy_datasets = True


if copy_datasets:
    print('\n\nCopying datasets...')
    # Loop through SDE geodatabases
    for sde in sde_dictionary.keys():
    # for sde in ['CS_ORIGINAL']:
        print('\t{0}'.format(sde))
        temp_fgdb = os.path.join(os.path.dirname(fgdb),
                                 os.path.splitext(os.path.basename(fgdb))[0] + '-' + str(sde).lower() + '.gdb')
        # Set arcpy.env.workspace to temporary SDE file geodatabase
        arcpy.env.workspace = temp_fgdb
        print('\t\tarcpy.env.workspace:\t\t{0}'.format(arcpy.env.workspace))
        # Loop through feature classes and related tables
        for dataset in sde_dictionary[sde]['copy_datasets']:
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
            dataset_out = dataset + '_' + sde
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
            # Delete non-Welsh data from the WGEM feature classes
            if sde == 'WGEM' and dataset in ('BLKDATA', 'SCPTDATA', 'LINEARDATA', 'POINTDATA'):
                print('\t\t\tRemoving non-Welsh data from feature class...')
                result = arcpy.GetCount_management(in_rows=dataset_out)
                count = int(result.getOutput(0))
                print('\t\t\t\tCount:\t\t{0}'.format(count))
                fl_bng_100km = 'fl_bng_100km'
                where_clause = '{0} in (\'SG\', \'SH\', \'SJ\', \'SM\', \'SN\', \'SO\', \'SR\', \'SS\', \'ST\')'.format(arcpy.AddFieldDelimiters(datasource=bng_100km,
                                                                                                                                                 field='OS_TILE'))
                print('\t\t\t\twhere_clause:\t\t{0}'.format(where_clause))
                arcpy.MakeFeatureLayer_management(in_features=bng_100km,
                                                  out_layer=fl_bng_100km,
                                                  where_clause=where_clause)
                result = arcpy.GetCount_management(in_rows=fl_bng_100km)
                count = int(result.getOutput(0))
                print('\t\t\t\tCount:\t\t{0}'.format(count))
                featurelayer = 'featurelayer'
                arcpy.MakeFeatureLayer_management(in_features=dataset_out,
                                                  out_layer= featurelayer)
                arcpy.SelectLayerByLocation_management(in_layer=featurelayer,
                                                       overlap_type='INTERSECT',
                                                       select_features=fl_bng_100km,
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
            # Delete non-Welsh data from the WGEM tables
            if sde == 'WGEM' and dataset in ('COMPDATA', 'EVENTDATA', 'SEVENTDATA', 'PCOMPDATA'):
                print('\t\t\tRemoving non-Welsh data from table...')
                result = arcpy.GetCount_management(in_rows=dataset_out)
                count = int(result.getOutput(0))
                print('\t\t\t\tCount:\t\t{0}'.format(count))
                tableview = 'tableview'
                parent_table = data_dictionary[dataset]['parent_table']
                print('\t\t\t\tparent_table:\t\t{0}'.format(parent_table))
                id_field = data_dictionary[parent_table]['id_field']
                where_clause = '{0} NOT IN (SELECT {1} FROM {2})'.format(arcpy.AddFieldDelimiters(datasource=dataset_out,
                                                                                                  field=id_field),
                                                                         arcpy.AddFieldDelimiters(datasource=parent_table + '_' + sde,
                                                                                                  field=id_field),
                                                                         parent_table + '_' + sde)
                print('\t\t\t\twhere_clause:\t\t{0}'.format(where_clause))
                arcpy.MakeTableView_management(in_table=dataset_out,
                                               out_view=tableview,
                                               where_clause=where_clause)
                result = arcpy.GetCount_management(in_rows=tableview)
                count = int(result.getOutput(0))
                print('\t\t\t\tCount:\t\t{0}'.format(count))
                arcpy.DeleteRows_management(in_rows=tableview)
                arcpy.SelectLayerByAttribute_management(in_layer_or_view=tableview,
                                                        selection_type='CLEAR_SELECTION')
                result = arcpy.GetCount_management(in_rows=dataset_out)
                count = int(result.getOutput(0))
                print('\t\t\t\tCount:\t\t{0}'.format(count))
                print('\t\t\tRemoved non-Welsh data from table.')
            # Set VISIT_STATUS and REASON_FOR_CHANGE to Null in SCPTDATA and POINTDATA feature class and EVENTDATA related table
            if dataset in ('SCPTDATA', 'POINTDATA', 'EVENTDATA'):
                for null_field in ('VISIT_STATUS', 'REASON_FOR_CHANGE'):
                    print('\t\t\tSetting {0} to <Null> in {1} {2}...'.format(null_field,
                                                                             dataset_out,
                                                                             data_dictionary[dataset]['type'].lower()))
                    arcpy.CalculateField_management(in_table=dataset_out,
                                                    field=null_field,
                                                    expression='None',
                                                    expression_type='PYTHON',
                                                    code_block='')
                    print('\t\t\tSet {0} to <Null> in {1} {2}.'.format(null_field,
                                                                           dataset_out,
                                                                           data_dictionary[dataset]['type'].lower()))
            # Add any additional fields to feature classes and related tables
            print('\t\t\tAdding additional fields...')
            # Add Point_Proximity field to POINTDATA feature class
            if dataset == 'POINTDATA':
                print('\t\t\t\tAdding Point_Proximity field to POINTDATA feature class...')
                arcpy.AddField_management(in_table=dataset_out,
                                          field_name='Point_Proximity',
                                          field_type='TEXT',
                                          field_precision='',
                                          field_scale='',
                                          field_length=10,
                                          field_alias='Point Proximity',
                                          field_is_nullable='NULLABLE',
                                          field_is_required='NON_REQUIRED',
                                          field_domain='')
                print('\t\t\t\tAdded Point_Proximity field to POINTDATA feature class.')
            # Add Polygon_Area field to SCPTDATA feature class
            if dataset == 'SCPTDATA':
                print('\t\t\t\tAdding Polygon_Area field to SCPTDATA feature class...')
                arcpy.AddField_management(in_table=dataset_out,
                                          field_name='Polygon_Area',
                                          field_type='FLOAT',
                                          field_precision=12,
                                          field_scale=3,
                                          field_length='',
                                          field_alias='Polygon Area',
                                          field_is_nullable='NULLABLE',
                                          field_is_required='NON_REQUIRED',
                                          field_domain='')
                print('\t\t\t\tAdded Polygon_Area field to SCPTDATA feature class.')
                print('\t\t\t\t\tCalculating Polygon_Area...')
                arcpy.CalculateField_management(in_table=dataset_out,
                                                field='Polygon_Area',
                                                expression='!shape.area@SQUAREMETERS!',
                                                expression_type='PYTHON',
                                                code_block='#')
                print('\t\t\t\t\tCalculated Polygon_Area.')
            # Add Linear_Length field to LINEARDATA feature class
            if dataset == 'LINEARDATA':
                print('\t\t\t\tAdding Linear_Length field to LINEARDATA feature class...')
                arcpy.AddField_management(in_table=dataset_out,
                                          field_name='Linear_Length',
                                          field_type='FLOAT',
                                          field_precision=12,
                                          field_scale=3,
                                          field_length='',
                                          field_alias='Linear Length',
                                          field_is_nullable='NULLABLE',
                                          field_is_required='NON_REQUIRED',
                                          field_domain='')
                print('\t\t\t\tAdded Linear_Length field to LINEARDATA feature class.')
                print('\t\t\t\t\tCalculating Linear_Length...')
                arcpy.CalculateField_management(in_table=dataset_out,
                                                field='Linear_Length',
                                                expression='!shape.length@METERS!',
                                                expression_type='PYTHON',
                                                code_block='#')
                print('\t\t\t\t\tCalculated Linear_Length.')
            # Add CONDITION, DISEASE_SIGNS and HABITAT_BOXES fields to PCOMPDATA related table
            if dataset == 'PCOMPDATA':
                field_names = [f.name for f in arcpy.ListFields(dataset=dataset_out)]
                if 'CONDITION' not in field_names:
                    print('\t\t\t\tAdding CONDITION field to PCOMPDATA related table...')
                    arcpy.AddField_management(in_table=dataset_out,
                                              field_name='CONDITION',
                                              field_type='SHORT',
                                              field_precision=3,
                                              field_scale='',
                                              field_length='',
                                              field_alias='Condition',
                                              field_is_nullable='NULLABLE',
                                              field_is_required='NON_REQUIRED',
                                              field_domain='')
                    print('\t\t\t\tAdded CONDITION field to PCOMPDATA feature class.')
                if 'DISEASE_SIGNS' not in field_names:
                    print('\t\t\t\tAdding DISEASE_SIGNS field to PCOMPDATA related table...')
                    arcpy.AddField_management(in_table=dataset_out,
                                              field_name='DISEASE_SIGNS',
                                              field_type='SHORT',
                                              field_precision=3,
                                              field_scale='',
                                              field_length='',
                                              field_alias='Signs of disease',
                                              field_is_nullable='NULLABLE',
                                              field_is_required='NON_REQUIRED',
                                              field_domain='')
                    print('\t\t\t\tAdded DISEASE_SIGNS field to PCOMPDATA feature class.')
                if 'HABITAT_BOXES' not in field_names:
                    print('\t\t\t\tAdding HABITAT_BOXES field to PCOMPDATA related table...')
                    arcpy.AddField_management(in_table=dataset_out,
                                              field_name='HABITAT_BOXES',
                                              field_type='SHORT',
                                              field_precision=3,
                                              field_scale='',
                                              field_length='',
                                              field_alias='Habitat boxes',
                                              field_is_nullable='NULLABLE',
                                              field_is_required='NON_REQUIRED',
                                              field_domain='')
                    print('\t\t\t\tAdded HABITAT_BOXES field to PCOMPDATA feature class.')
            # Add Editor and Date of edit fields to BLKDATA feature class
            print('\t\t\t\tAdding Editor and Date of Edit fields to {0}...'.format(dataset_out))
            arcpy.AddField_management(in_table=dataset_out,
                                      field_name='EDITOR',
                                      field_type='TEXT',
                                      field_precision='',
                                      field_scale='',
                                      field_length=25,
                                      field_alias='Editor',
                                      field_is_nullable='NULLABLE',
                                      field_is_required='NON_REQUIRED',
                                      field_domain='')
            arcpy.AddField_management(in_table=dataset_out,
                                      field_name='DATE_OF_EDIT',
                                      field_type='DATE',
                                      field_precision='',
                                      field_scale='',
                                      field_length='',
                                      field_alias='Date of edit',
                                      field_is_nullable='NULLABLE',
                                      field_is_required='NON_REQUIRED',
                                      field_domain='')
            print('\t\t\t\tAdded Editor and Date of Edit fields to {0}.'.format(dataset_out))
            print('\t\t\tAdded additional fields.')
            # Add field aliases
            print('\t\t\tAdding field aliases...')
            field_names = arcpy.ListFields(dataset=dataset_out)
            for field in field_names:
                if field.name not in ['OBJECTID', 'SHAPE', 'SHAPE.AREA', 'SHAPE.LEN'] and field.aliasName == field.name:
                    print('\t\t\t\t{0} is a type of {1} with a length of {2}'.format(field.name,
                                                                                   field.type,
                                                                                   field.length))
                    field_alias = field_alias_dictionary.get(dataset, {}).get(field.name, DEFAULT)
                    if field_alias is not None:
                        print('\t\t\t\tfield_alias:\t\t{0}'.format(field_alias))
                        arcpy.AlterField_management(in_table=dataset_out,
                                                    field=field.name,
                                                    new_field_alias=field_alias)
            print('\t\t\tAdded field aliases.')
    print('Copied datasets.')


add_guids = True


if add_guids:
    print('\n\nAdding GUID fields to feature classes and related tables...')
    # Loop through SDE geodatabases
    for sde in sde_dictionary.keys():
    # for sde in ['CS_ORIGINAL']:
        print('\t{0}'.format(sde))
        temp_fgdb = os.path.join(os.path.dirname(fgdb),
                                 os.path.splitext(os.path.basename(fgdb))[0] + '-' + str(sde).lower() + '.gdb')
        # Set arcpy.env.workspace to temporary SDE file geodatabase
        arcpy.env.workspace = temp_fgdb
        print('\t\tarcpy.env.workspace:\t\t{0}'.format(arcpy.env.workspace))
        # Loop through feature classes and related tables
        for dataset in sde_dictionary[sde]['copy_datasets']:
            print('\t\t{0}'.format(dataset))
            # Define out dataset
            dataset_out = dataset + '_' + sde
            print('\t\t\tdataset_out:\t\t{0}'.format(dataset_out))
            # Define GUID field
            guid_field = data_dictionary[dataset]['guid_field']
            print('\t\t\tguid_field:\t\t{0}'.format(guid_field))
            # Add GUID field to output dataset if it doesn't already exist (Note: cannot delete required fields including GUIDs)
            if not arcpy.ListFields(dataset=dataset_out,
                                    wild_card=guid_field):
                print('\t\t\tAdding GUID field {0} to out {1} {2}...'.format(guid_field,
                                                                             data_dictionary[dataset]['type'].lower(),
                                                                             dataset_out))
                arcpy.AddField_management(in_table=dataset_out,
                                          field_name=guid_field,
                                          field_type='GUID',
                                          field_precision='#',
                                          field_scale='#',
                                          field_length='#',
                                          field_alias='#',
                                          field_is_nullable='NULLABLE',  # field_is_nullable='NULLABLE',
                                          field_is_required='REQUIRED',
                                          field_domain='#')
                print('\t\t\tAdded GUID field {0} to out {1} {2}.'.format(guid_field,
                                                                          data_dictionary[dataset]['type'].lower(),
                                                                          dataset_out))
            print('\t\t\tCalculating GUID field {0} in out {1} {2}...'.format(guid_field,
                                                                              data_dictionary[dataset]['type'].lower(),
                                                                              dataset_out))
            code_block = '''def GUID():
                import uuid
                return \'{\' + str(uuid.uuid4()) + \'}\''''
            arcpy.CalculateField_management(in_table=dataset_out,
                                            field=guid_field,
                                            expression='GUID()',
                                            expression_type='PYTHON',
                                            code_block=code_block)
            print('\t\t\tCalculated GUID field {0} in out {1} {2}.'.format(guid_field,
                                                                           data_dictionary[dataset]['type'].lower(),
                                                                           dataset_out))
            # Add attribute index to newly added GUID field
            print('\t\t\tAdding attribute index to GUID field {0} in out {1} {2}...'.format(guid_field,
                                                                                            data_dictionary[dataset]['type'].lower(),
                                                                                            dataset_out))
            index_name = guid_field + '_IDX'
            if len(arcpy.ListIndexes(dataset=dataset_out,
                                     wild_card=index_name)) > 0:
                print('\t\t\t\tDeleting attribute index {0} in out {1} {2}...'.format(index_name,
                                                                                      data_dictionary[dataset]['type'].lower(),
                                                                                      dataset_out))
                arcpy.RemoveIndex_management(in_table=dataset_out,
                                             index_name=index_name)
                print('\t\t\t\tDeleted attribute index {0} in out {1} {2}.'.format(index_name,
                                                                                   data_dictionary[dataset]['type'].lower(),
                                                                                   dataset_out))
            arcpy.AddIndex_management(in_table=dataset_out,
                                      fields=guid_field,
                                      index_name=index_name,
                                      unique='UNIQUE',
                                      ascending='NON_ASCENDING')
            print('\t\t\tAdded attribute index to GUID field {0} in out {1} {2}.'.format(guid_field,
                                                                                         data_dictionary[dataset]['type'].lower(),
                                                                                         dataset_out))
        # Join GUIDs to related table
        print('\t\tJoining GUID fields to related tables...')
        related_tables = sde_dictionary[sde]['copy_datasets']
        print('\t\trelated_tables:\t\t{0}'.format(related_tables))
        parent_tables = ['BLKDATA', 'SCPTDATA', 'LINEARDATA', 'POINTDATA']
        for parent_table in parent_tables:
            if parent_table in related_tables:
                related_tables.remove(parent_table)
        print('\t\trelated_tables:\t\t{0}'.format(related_tables))
        for related_table in related_tables:
            print('\t\t\trelated_table:\t\t{0}'.format(related_table))
            in_data = related_table + '_' + sde
            print('\t\t\t\tin_data:\t\t{0}'.format(in_data))
            parent_table = data_dictionary[related_table]['parent_table']
            in_field = data_dictionary[parent_table]['id_field']
            print('\t\t\t\tin_field:\t\t{0}'.format(in_field))
            join_table = parent_table + '_' + sde
            print('\t\t\t\tjoin_table:\t\t{0}'.format(join_table))
            join_field = data_dictionary[parent_table]['id_field']
            print('\t\t\t\tjoin_field:\t\t{0}'.format(join_field))
            fields = [data_dictionary[parent_table]['guid_field']]
            print('\t\t\t\tfields:\t\t{0}'.format(fields))
            arcpy.JoinField_management(in_data=in_data,
                                       in_field=in_field,
                                       join_table=join_table,
                                       join_field=join_field,
                                       fields=fields)
            print('\t\t\tAdded GUID field to related tables.')
            #
            # Add attribute index to newly joined GUID field
            for field in fields:
                print('\t\t\t\tAdding attribute index to field {0} in {1} {2}...'.format(field,
                                                                                       data_dictionary[related_table]['type'].lower(),
                                                                                       in_data))
                index_name = field + '_IDX'
                if len(arcpy.ListIndexes(dataset=in_data,
                                         wild_card=index_name)) > 0:
                    print('\t\t\t\t\tDeleting attribute index {0} in {1} {2}...'.format(index_name,
                                                                                      data_dictionary[related_table]['type'].lower(),
                                                                                      in_data))
                    arcpy.RemoveIndex_management(in_table=in_data,
                                                 index_name=index_name)
                    print('\t\t\t\t\tDeleted attribute index {0} in {1} {2}.'.format(index_name,
                                                                                   data_dictionary[related_table]['type'].lower(),
                                                                                   in_data))
                arcpy.AddIndex_management(in_table=in_data,
                                          fields=field,
                                          index_name=index_name,
                                          unique='UNIQUE',
                                          ascending='NON_ASCENDING')
                print('\t\t\t\tAdded attribute index to field {0} in {1} {2}.'.format(field,
                                                                                    data_dictionary[related_table]['type'].lower(),
                                                                                    in_data))
        # del index_name, guid_field, id_field, related_table_out, related_table, dataset_out, dataset, datasets
        print('\t\tJoined GUID fields to related tables.')
    print('Added GUID fields to feature classes and related tables.')


check_guids = True


if check_guids:
    # Checking GUID fields in related file geodatabase datasets
    print('\n\nChecking GUID fields in related datasets...')
    # Set sample size
    sample_size = 10
    print('\tsample_size:\t\t{0}'.format(sample_size))
    # Loop through SDE geodatabases
    for sde in sde_dictionary.keys():
    # for sde in ['CS_ORIGINAL']:
        print('\t{0}'.format(sde))
        temp_fgdb = os.path.join(os.path.dirname(fgdb),
                                 os.path.splitext(os.path.basename(fgdb))[0] + '-' + str(sde).lower() + '.gdb')
        # Set arcpy.env.workspace to temporary SDE file geodatabase
        arcpy.env.workspace = temp_fgdb
        print('\t\tarcpy.env.workspace:\t\t{0}'.format(arcpy.env.workspace))
        # Loop through feature classes and related tables
        print(sde_dictionary[sde])
        parent_tables = sde_dictionary[sde]['copy_datasets']
        print('\t\tparent_tables:\t\t{0}'.format(parent_tables))
        child_tables = ['BLKDATA', 'COMPDATA', 'SEVENTDATA', 'PCOMPDATA']
        for child_table in child_tables:
            if child_table in parent_tables:
                parent_tables.remove(child_table)
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
            random_ids = sorted(random_ids, key=int, reverse=False)
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
                if count != row_count:
                    sys.exit('\n\ncount != row_count!!!\n\n')
    print('Checked GUID fields in related datasets.')







# Capture end_time
end_time = time.time()


# Report elapsed_time (= end_time - start_time)
print('\n\nIt took {0} to execute this.'.format(hms_string(end_time - start_time)))


# Print script filename, finish date and time
print('\n\nFinished {0} at {1} on {2}.\n'.format(script,
                                                 datetime.datetime.now().strftime('%H:%M:%S'),
                                                 datetime.datetime.now().strftime('%Y-%m-%d')))


sys.exit()


create_relationship_classes = True


if create_relationship_classes:
    # Add relationship classes
    print('\n\nCreating relationship classes...')
    for dataset in data_dictionary.keys():
        print('\tdataset:\t\t{0}'.format(dataset))
        # Define output dataset
        dataset_out = os.path.join(fgdb, dataset)
        print('\t\tdataset_out:\t\t{0}'.format(dataset_out))
        # Get related table from data dictionary
        related_table = data_dictionary[dataset]['related_table']
        print('\t\trelated_table:\t\t{0}'.format(related_table))
        # Get related table from data dictionary
        guid_field = data_dictionary[dataset]['guid_field']
        print('\t\tguid_field:\t\t\t{0}'.format(guid_field))
        # Define output related table path
        related_table_out = os.path.join(fgdb, related_table)
        print('\t\trelated_table_out:\t\t{0}'.format(related_table_out))
        #  Create relationship class
        print('\t\tCreating relationship class...')
        print('\t\t\torigin_table:\t\t\t\t{0}'.format(dataset_out))
        print('\t\t\tdestination_table:\t\t\t{0}'.format(related_table_out))
        out_relationship_class = os.path.basename(dataset_out) + '_' + os.path.basename(related_table_out)
        print('\t\t\tout_relationship_class:\t\t{0}'.format(out_relationship_class))
        relationship_type = 'COMPOSITE'
        print('\t\t\trelationship_type:\t\t\t{0}'.format(relationship_type))
        forward_label = os.path.basename(dataset_out)
        print('\t\t\tforward_label:\t\t\t\t{0}'.format(forward_label))
        backward_label = os.path.basename(related_table_out)
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
        # desc = arcpy.Describe(value=os.path.join(fgdb, out_relationship_class))
        # print('desc.name:\t\t{0}'.format(desc.name))
        # if hasattr(desc, 'name'):
        #     print('\t\t\tDeleting existing relationship class {0}...'.format(out_relationship_class))
        #     arcpy.Delete_management(in_data=os.path.join(fgdb, out_relationship_class))
        #     print('\t\t\tDeleted existing relationship class {0}.'.format(out_relationship_class))
        if arcpy.Exists(dataset=os.path.join(fgdb, out_relationship_class)):
            print('\t\t\tDeleting existing relationship class {0}...'.format(out_relationship_class))
            arcpy.Delete_management(in_data=os.path.join(fgdb, out_relationship_class))
            print('\t\t\tDeleted existing relationship class {0}.'.format(out_relationship_class))
        arcpy.CreateRelationshipClass_management(origin_table=dataset_out,
                                                 destination_table=related_table_out,
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
    #
    print('Creating relationship classes...')


copy_domains = True


# TODO - re-create domains from WGEM schema to get must up-to-date values for selected fields
# TODO - (e.g. PRIMARY_QUALIFYER values of Burnt Vegetation (< 2 years) and Burnt Vegetation (< 2 years) instead of Burnt Vegetation) and additional values of Lowland Marshy Grassland and Calaminaria Grassland)
# TODO - (e.g. SWARD_COVER, SWARD_HEIGHT, SWARD_VARIATION and TUSSOCKINESS which aren't CS fields but are WGEM fields)


if copy_domains:
    print('\n\nCopying domains and applying to fields...')
    #
    # Define domain tables code and description fields
    code_field = 'Code'
    print('\tcode_field:\t\t\t\t{0}'.format(code_field))
    description_field = 'Description'
    print('\tdescription_field:\t\t{0}'.format(description_field))
    # # Define in file geodatabase from which to copy domains
    # # This file geodatabase was created from an XML Workspace document created from the CS ArcSDE geodatabase
    fgdb_in = r'E:\CountrysideSurvey\esri-uk\domains\domains.gdb'
    print('\tfgdb_in:\t\t{0}'.format(fgdb_in))
    # Define temporary file geodatabase
    fgdb_temp = os.path.dirname(fgdb_in)
    fgdb_temp = os.path.join(fgdb_temp, r'temporary_domain_tables' + r'.gdb')
    print('\t\tfgdb_temp:\t\t{0}'.format(fgdb_temp))
    # Create temporary file geodatabase
    if arcpy.Exists(fgdb_temp):
        print('\t\tDeleting fgdb_temp {0}...'.format(fgdb_temp))
        arcpy.Delete_management(fgdb_temp)
        print('\t\tDeleted fgdb_temp {0}.'.format(fgdb_temp))
    print('\tCreating fgdb_temp {0}...'.format(fgdb_temp))
    arcpy.CreateFileGDB_management(out_folder_path=os.path.dirname(fgdb_temp),
                                   out_name=os.path.basename(fgdb_temp),
                                   out_version='CURRENT')
    print('\t\tCreated fgdb_temp {0}.'.format(fgdb_temp))
    # Get a list of domains from the in file geodatabase
    domains = arcpy.da.ListDomains(fgdb_in)
    # Loop through list of domains in the in file geodatabase
    for domain in domains:
        # Only get CS 2007 domains
        if domain.name.startswith('CS2007_'):
            # Print out domain name and type
            print('\t#\n\tDomain {0} is of type {1}'.format(domain.name,
                                                            domain.domainType))
            # Print out domain values
            if domain.domainType == 'CodedValue':
                coded_values = domain.codedValues
                for val, desc in coded_values.items():
                    print('\t\t{0} : {1}'.format(val, desc))
            elif domain.domainType == 'Range':
                print('\t\tMin: {0}'.format(domain.range[0]))
                print('\t\tMax: {0}'.format(domain.range[1]))
            # Convert domain to a table in temporary fgdb
            print('\tConverting domain to table in temporary file geodatabase...')
            table_out = domain.name + '_table'
            table_out = os.path.join(fgdb_temp, table_out)
            print('\t\ttable_out:\t\t\t\t{0}'.format(table_out))
            arcpy.DomainToTable_management(in_workspace=fgdb_in,
                                           domain_name=domain.name,
                                           out_table=table_out,
                                           code_field=code_field,
                                           description_field=description_field,
                                           configuration_keyword='')
            print('\tConverted domain to table in temporary file geodatabase.')
            # Add additional HABT_CODES to the CS2007_HABT_CODE table
            if domain.name == 'CS2007_HABT_CODE':
                print('\t#\n\tAdding additional domain values to {0} table...'.format(table_out))
                habt_code_table = arcsde_cs_restored + '\\' +\
                                  arcsde_user_cs_restored + '.' + 'HABITATS'
                print('\t\thabt_code_table:\t\t{0}'.format(habt_code_table))
                a = list(range(10070, 10077))
                b = list(range(601, 613))
                missing_values = a + b
                for missing_value in missing_values:
                    if missing_values.index(missing_value) == 0:
                        missing_values_string = '(\'' + str(missing_value) + '\''
                    elif missing_values.index(missing_value) == (len(missing_values) - 1):
                        missing_values_string += ', \'' + str(missing_value) + '\')'
                    else:
                        missing_values_string += ', \'' + str(missing_value) + '\''
                print('\t\tmissing_values_string:\t\t{0}'.format(missing_values_string))
                where_clause = '{0} IN {1}'.format(arcpy.AddFieldDelimiters(habt_code_table, 'HABT_CODE'),
                                                   missing_values_string)
                print('\t\twhere_clause:\t\t{0}'.format(where_clause))
                search_cursor_fields = ['HABT_CODE', 'HABITAT_NAME']
                print('\t\tsearch_cursor_fields:\t\t{0}'.format(search_cursor_fields))
                print('\t\tMissing codes and descriptions:')
                with arcpy.da.SearchCursor(in_table=habt_code_table,
                                           field_names=search_cursor_fields,
                                           where_clause=where_clause) as search_cursor:
                    insert_cursor_fields = ['Code', 'Description']
                    print('\t\tinsert_cursor_fields:\t\t{0}'.format(insert_cursor_fields))
                    insert_cursor = arcpy.da.InsertCursor(in_table=table_out,
                                                          field_names=insert_cursor_fields)
                    for search_row in search_cursor:
                        print('\t\t\t{0}:\t\t{1}'.format(search_row[0], search_row[1]))
                        insert_cursor.insertRow((search_row[0], search_row[1]))
                del insert_cursor, insert_cursor_fields
                del search_row, search_cursor, search_cursor_fields
                print('\tAdded additional domain values to {0} table.'.format(table_out))
            # Add additional SPECIES to the CS2007_SPECIES table
            if domain.name == 'CS2007_SPECIES':
                print('\t#\n\tAdding additional domain values to {0} table...'.format(table_out))
                fecodes_table = arcsde_cs_restored + '\\' + \
                                arcsde_user_cs_restored + '.' + 'FECODES'
                print('\t\tfecodes_table:\t\t{0}'.format(fecodes_table))
                where_clause = '{0} = {1}'.format(arcpy.AddFieldDelimiters(fecodes_table, 'COLUMN_NAME'),
                                                  '\'SPECIES\'')
                print('\t\twhere_clause:\t\t{0}'.format(where_clause))
                search_cursor_fields = ['COLUMN_NAME', 'CODE', 'DESCRIPTION']
                print('\t\tsearch_cursor_fields:\t\t{0}'.format(search_cursor_fields))
                species_count = 0
                print('\t\tMissing codes and descriptions:')
                with arcpy.da.SearchCursor(in_table=fecodes_table,
                                           field_names=search_cursor_fields,
                                           where_clause=where_clause) as search_cursor:
                    insert_cursor_fields = ['Code', 'Description']
                    print('\t\tinsert_cursor_fields:\t\t{0}'.format(insert_cursor_fields))
                    insert_cursor = arcpy.da.InsertCursor(in_table=table_out,
                                                          field_names=insert_cursor_fields)
                    for search_row in search_cursor:
                        print('\t\t\t{0}:\t\t{1}'.format(search_row[1], search_row[2]))
                        insert_cursor.insertRow((search_row[1], search_row[2]))
                del insert_cursor, insert_cursor_fields
                del search_row, search_cursor, search_cursor_fields
                print('\tAdded additional domain values to {0} table.'.format(table_out))

            # Delete identical records in the temporary domain fgdb table
            print('\tDeleting any identical records in the {0} table...'.format(table_out))
            arcpy.DeleteIdentical_management(in_dataset=table_out,
                                             fields=['Code', 'Description'])
            print('\tDeleted any identical records in the {0} table.'.format(table_out))
            # Convert table to domain in the out file geodatabase
            field_name = domain.name.replace('CS2007_', '')
            print('\t\tfield_name:\t\t{0}'.format(field_name))
            print('\tConverting table to domain in the out file geodatabase...')
            existing_domains_list = arcpy.Describe(fgdb).domains
            print('\t\texisiting_domains_list:\t\t{0}'.format(existing_domains_list))
            if domain.name in existing_domains_list:
                print('\t\t\tDeleting existing domain {0} in file geodatabase...'.format(domain.name))
                tables = ['SCPTDATA', 'LINEARDATA', 'POINTDATA', 'COMPDATA', 'EVENTDATA', 'SEVENTDATA', 'PCOMPDATA']
                for table in tables:
                    print('\t\t\ttable:\t\t{0}'.format(table))
                    fields = arcpy.ListFields(os.path.join(fgdb, table))
                    for field in fields:
                        delete = 'Delete domain' if field_name == field.name else 'Do not delete domain'
                        if delete == 'Delete domain':
                            print('\t\t\t\tRemoving domain {0} from field {1}...'.format(domain.name,
                                                                                         field.name))
                            arcpy.RemoveDomainFromField_management(in_table=os.path.join(fgdb, table),
                                                                   field_name=field_name,
                                                                   subtype_code='')
                            print('\t\t\t\tRemoved domain {0} from field {1}.'.format(domain.name,
                                                                                     field.name))
                del tables
                arcpy.DeleteDomain_management(in_workspace=fgdb,
                                              domain_name=domain.name)
                print('\t\t\tDeleted existing domain {0} in file geodatabase.'.format(domain.name))
            domain_description = domain.name.replace('_', ' ') + ' domain'
            print('\t\tdomain_description:\t\t{0}'.format(domain_description))
            arcpy.TableToDomain_management(in_table=table_out,
                                           code_field=code_field,
                                           description_field=description_field,
                                           in_workspace=fgdb,
                                           domain_name=domain.name,
                                           domain_description=domain_description,
                                           update_option='REPLACE')
            print('\tConverted table to domain in the out file geodatabase.')
            # Assign domain to field
            print('\tAssigning domain to a field ...')
#            field_name = domain.name.replace('CS2007_', '')
#            print('\t\tfield_name:\t\t{0}'.format(field_name))
            arcpy.env.workspace = fgdb
            # tables = arcpy.ListTables()
            tables = ['SCPTDATA', 'LINEARDATA', 'POINTDATA', 'COMPDATA', 'EVENTDATA', 'SEVENTDATA', 'PCOMPDATA']
            for table in tables:
                print('\t\t\ttable:\t\t{0}'.format(table))
                fields = arcpy.ListFields(os.path.join(fgdb, table))
                for field in fields:
                    assign = 'Assign domain' if field_name == field.name else 'Do not assign domain'
                    if assign == 'Assign domain':
                        print('\t\t\t\t{0} is a type of {1}\t\t{2}'.format(field.name,
                                                                            field.type,
                                                                            assign))
                        arcpy.AssignDomainToField_management(in_table=os.path.join(fgdb, table),
                                                             field_name=field_name,
                                                             domain_name=domain.name,
                                                             subtype_code='')
            print('\tAssigned domain to a field.')
    #
    # Add domains from WGEM project
    print('\n\nAdding domains from the WGEM project...')
    fecodes_table = r'C:\Users\SMW\AppData\Roaming\ESRI\Desktop10.1\ArcCatalog\Connection to LADB TBB WGEMADMIN.sde\WGEMADMIN.FECODES'
    search_cursor_fields = ['COLUMN_NAME', 'CODE', 'DESCRIPTION']
    for column_name in ['LUSE', 'CONDITION', 'DISEASE_SIGNS', 'HABITAT_BOXES']:
        print('\t#\n\tcolumn_name:\t\t{0}'.format(column_name))
        #
        domain = 'GMEP13_' + column_name
        print('\t\tdomain:\t\t{0}'.format(domain))
        #
        where_clause = u'{0} = \'{1}\''.format(arcpy.AddFieldDelimiters(fecodes_table, 'COLUMN_NAME'),
                                           column_name)
        print('\t\t\twhere_clause:\t\t{0}'.format(where_clause))
        wgem_table = os.path.join(fgdb_temp, 'WGEM_' + column_name)
        print('\t\t\twgem_table:\t\t{0}'.format(wgem_table))
        if arcpy.Exists(wgem_table):
            print('\t\t\t\t\tDeleting wgem_table {0}...'.format(wgem_table))
            arcpy.Delete_management(wgem_table)
            print('\t\t\t\t\tDeleted wgem_table {0}.'.format(wgem_table))
        print('\t\t\t\tCreating wgem_table {0}...'.format(wgem_table))
        arcpy.CreateTable_management(out_path=os.path.dirname(wgem_table),
                                     out_name=os.path.basename(wgem_table))
        print('\t\t\t\t\tAdding fields to wgem_table {0}...'.format(wgem_table))
        arcpy.AddField_management(in_table=wgem_table,
                                  field_name=code_field,
                                  field_type='TEXT',
                                  field_length=10)
        arcpy.AddField_management(in_table=wgem_table,
                                  field_name=description_field,
                                  field_type='TEXT',
                                  field_length=40)
        print('\t\t\t\t\tAdded fields to wgem_table {0}.'.format(wgem_table))
        print('\t\t\t\tCreated wgem_table {0}.'.format(wgem_table))
        print('\t\t\tUsing arcpy.da cursors to find values and add to wgem_table...')
        print('\t\t\t{0:<20}\t{1:<20}\t{2:<20}'.format(search_cursor_fields[0],
                                                   search_cursor_fields[1],
                                                   search_cursor_fields[2]))
        insert_cursor_fields = ['CODE', 'DESCRIPTION']
        insert_cursor = arcpy.da.InsertCursor(in_table=wgem_table,
                                              field_names=insert_cursor_fields)
        with arcpy.da.SearchCursor(in_table=fecodes_table,
                                   field_names=search_cursor_fields,
                                   where_clause=where_clause) as search_cursor:
            for search_row in search_cursor:
                print('\t\t\t{0:<20}\t{1:<20}\t{2:<20}'.format(search_row[0],
                                                           search_row[1],
                                                           search_row[2]))
                insert_cursor.insertRow((search_row[1],
                                         search_row[2]))
        del insert_cursor
        del search_row, search_cursor
        print('\t\t\tUsed arcpy.da cursors to find values and add to wgem_table.')
        #
        print('\t\t\tConverting table to domain in the out file geodatabase...')
        existing_domains_list = arcpy.Describe(fgdb).domains
        print('\t\t\t\texisiting_domains_list:\t\t{0}'.format(existing_domains_list))
        if domain in existing_domains_list:
            print('\t\t\t\t\tDeleting existing domain {0} in file geodatabase...'.format(domain))
            tables = ['SCPTDATA', 'LINEARDATA', 'POINTDATA', 'COMPDATA', 'EVENTDATA', 'SEVENTDATA', 'PCOMPDATA']
            for table in tables:
                print('\t\t\t\t\t\ttable:\t\t{0}'.format(table))
                fields = arcpy.ListFields(os.path.join(fgdb, table))
                for field in fields:
                    delete = 'Delete domain' if column_name == field.name else 'Do not delete domain'
                    if delete == 'Delete domain':
                        print('\t\t\t\t\t\t\tRemoving domain {0} from field {1}...'.format(domain,
                                                                                     column_name))
                        arcpy.RemoveDomainFromField_management(in_table=os.path.join(fgdb, table),
                                                               field_name=column_name,
                                                               subtype_code='')
                        print('\t\t\t\t\t\t\tRemoved domain {0} from field {1}.'.format(domain,
                                                                                 column_name))
            del tables
            arcpy.DeleteDomain_management(in_workspace=fgdb,
                                          domain_name=domain)
            print('\t\t\t\t\tDeleted existing domain {0} in file geodatabase.'.format(domain))
        domain_description = domain.replace('_', ' ') + ' domain'
        print('\t\t\t\tdomain_description:\t\t{0}'.format(domain_description))
        arcpy.TableToDomain_management(in_table=wgem_table,
                                       code_field=code_field,
                                       description_field=description_field,
                                       in_workspace=fgdb,
                                       domain_name=domain,
                                       domain_description=domain_description,
                                       update_option='REPLACE')
        print('\t\t\tConverted table to domain in the out file geodatabase.')
        #
        # Assign domain to field
        print('\t\t\tAssigning domain to a field ...')
        field_name = column_name
        print('\t\t\t\tfield_name:\t\t{0}'.format(field_name))
        arcpy.env.workspace = fgdb
        # tables = arcpy.ListTables()
        tables = ['SCPTDATA', 'LINEARDATA', 'POINTDATA', 'COMPDATA', 'EVENTDATA', 'SEVENTDATA', 'PCOMPDATA']
        for table in tables:
            print('\t\t\t\t\ttable:\t\t{0}'.format(table))
            fields = arcpy.ListFields(os.path.join(fgdb, table))
            for field in fields:
                assign = 'Assign domain' if field_name == field.name else 'Do not assign domain'
                if assign == 'Assign domain':
                    print('\t\t\t\t\t\t{0} is a type of {1}\t\t{2}'.format(field.name,
                                                                        field.type,
                                                                        assign))
                    arcpy.AssignDomainToField_management(in_table=os.path.join(fgdb, table),
                                                         field_name=field_name,
                                                         domain_name=domain,
                                                         subtype_code='')
        print('\t\t\tAssigned domain to a field.')
    print('Added domains from the WGEM project.')
    #
    print('\n\nCopied domains and applied to fields.')


# Capture end_time
end_time = time.time()


# Report elapsed_time (= end_time - start_time)
print('\n\nIt took {0} to execute this.'.format(hms_string(end_time - start_time)))


# Print script filename, finish date and time
print('\n\nFinished {0} at {1} on {2}.\n'.format(script,
                                                 datetime.datetime.now().strftime('%H:%M:%S'),
                                                 datetime.datetime.now().strftime('%Y-%m-%d')))
