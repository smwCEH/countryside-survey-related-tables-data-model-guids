import os
import sys
import platform
import datetime
import time
import random


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


# Define file geodatabase
fgdb = r'E:\CountrysideSurvey\esri-uk\guids\guids-{}.gdb'.format(datetime.datetime.now().strftime('%Y%m%d'))
# fgdb = r'E:\CountrysideSurvey\esri-uk\guids\guids-20160714.gdb'
print('\n\nfgdb:\t\t\{}'.format(fgdb))


# Create file geodatabase if it doesn't exist
if not arcpy.Exists(dataset=fgdb):
    arcpy.CreateFileGDB_management(out_folder_path=os.path.dirname(fgdb),
                                   out_name=os.path.basename(fgdb),
                                   out_version='')


# Define dictionary to hold CS ArcSDE feature classes and tables
print('\n\nCreating data dictionary...')
# BLKDATA = os.path.join(arcsde, r'CS2007_ADMIN.ForesterData\CS2007_ADMIN.BLKDATA')
# SCPTDATA = os.path.join(arcsde, r'CS2007_ADMIN.ForesterData\CS2007_ADMIN.SCPTDATA')
# COMPDATA = os.path.join(arcsde, r'CS2007_ADMIN.COMPDATA')
# POINTDATA = os.path.join(arcsde, r'CS2007_ADMIN.ForesterData\CS2007_ADMIN.POINTDATA')
# PCOMPDATA = os.path.join(arcsde, r'CS2007_ADMIN.PCOMPDATA')
# LINEARDATA = os.path.join(arcsde, r'CS2007_ADMIN.ForesterData\CS2007_ADMIN.LINEARDATA')
# EVENTDATA = os.path.join(arcsde, r'CS2007_ADMIN.EVENTDATA')
# SEVENTDATA = os.path.join(arcsde, r'CS2007_ADMIN.SEVENTDATA')
# Create empty dictionary
data_dictionary = {}
# Add first level dictionary items
data_dictionary['BLKDATA'] = {}
data_dictionary['SCPTDATA'] = {}
data_dictionary['COMPDATA'] = {}
data_dictionary['POINTDATA'] = {}
data_dictionary['PCOMPDATA'] = {}
data_dictionary['LINEARDATA'] = {}
data_dictionary['EVENTDATA'] = {}
data_dictionary['SEVENTDATA'] = {}
# Add second level dictionary items for feature classes and tables
data_dictionary['BLKDATA']['in_dataset'] = os.path.join(arcsde, r'CS2007_ADMIN.ForesterData\CS2007_ADMIN.BLKDATA')
data_dictionary['BLKDATA']['type'] = 'feature_class'
data_dictionary['SCPTDATA']['in_dataset'] = os.path.join(arcsde, r'CS2007_ADMIN.ForesterData\CS2007_ADMIN.SCPTDATA')
data_dictionary['SCPTDATA']['type'] = 'feature_class'
data_dictionary['COMPDATA']['in_dataset'] = os.path.join(arcsde, r'CS2007_ADMIN.COMPDATA')
data_dictionary['COMPDATA']['type'] = 'table'
data_dictionary['POINTDATA']['in_dataset'] = os.path.join(arcsde, r'CS2007_ADMIN.ForesterData\CS2007_ADMIN.POINTDATA')
data_dictionary['POINTDATA']['type'] = 'feature_class'
data_dictionary['PCOMPDATA']['in_dataset'] = os.path.join(arcsde, r'CS2007_ADMIN.PCOMPDATA')
data_dictionary['PCOMPDATA']['type'] = 'table'
data_dictionary['LINEARDATA']['in_dataset'] = os.path.join(arcsde, r'CS2007_ADMIN.ForesterData\CS2007_ADMIN.LINEARDATA')
data_dictionary['LINEARDATA']['type'] = 'feature_class'
data_dictionary['EVENTDATA']['in_dataset'] = os.path.join(arcsde, r'CS2007_ADMIN.EVENTDATA')
data_dictionary['EVENTDATA']['type'] = 'table'
data_dictionary['SEVENTDATA']['in_dataset'] = os.path.join(arcsde, r'CS2007_ADMIN.SEVENTDATA')
data_dictionary['SEVENTDATA']['type'] = 'table'
# Add second level dictionary item out feature class and table (derived from second level dictionary item in_fc)
for key in data_dictionary.keys():
    print(key)
    out_fc = os.path.join(fgdb, os.path.basename(data_dictionary[key]['in_dataset']).split(arcsde_user + '.', 1)[1])
    data_dictionary[key]['out_dataset'] = out_fc
# Add second level dictionary item guid field for feature classes (derived from second level dictionary item in_fc)
for key in {k:v for k, v in data_dictionary.items() if v['type'] == 'feature_class'}:
    print(key)
    guid_field = os.path.basename(data_dictionary[key]['in_dataset']).split(arcsde_user + '.', 1)[1] + '_GUID'
    data_dictionary[key]['guid_field'] = guid_field
# Add second level dictionary item guid field for EVENTDATA table
data_dictionary['EVENTDATA']['guid_field'] = 'EVENTDATA_GUID'
# Add second level dictionary items for tables
data_dictionary['COMPDATA']['join_table'] = data_dictionary['SCPTDATA']['out_dataset']
data_dictionary['COMPDATA']['join_field'] = 'SCPTDATA_ID'
data_dictionary['PCOMPDATA']['join_table'] = data_dictionary['POINTDATA']['out_dataset']
data_dictionary['PCOMPDATA']['join_field'] = 'POINTDATA_ID'
data_dictionary['EVENTDATA']['join_table'] = data_dictionary['LINEARDATA']['out_dataset']
data_dictionary['EVENTDATA']['join_field'] = 'LINEARDATA_ID'
data_dictionary['SEVENTDATA']['join_table'] = data_dictionary['EVENTDATA']['out_dataset']
data_dictionary['SEVENTDATA']['join_field'] = 'EVENTDATA_ID'
# Display dictionary
print(data_dictionary)
# for key in data_dictionary.keys():
#     print(key)
#     print('\t', data_dictionary[key])
#     print('\t\t', data_dictionary[key]['in_dataset'])
#     print('\t\t', data_dictionary[key]['out_dataset'])
#     print('\t\t', data_dictionary[key]['guid_field'])
print('Created data dictionary.')


# Derive list of feature classes from the data dictionary
# feature_class_list = list(data_dictionary.keys())
feature_class_dictionary = {k:v for k, v in data_dictionary.items() if v['type'] == 'feature_class'}
feature_class_list = list(feature_class_dictionary.keys())
print('\n\nfeature_class_list:\t\t{}'.format(feature_class_list))
feature_class_list.remove('BLKDATA')
print('feature_class_list:\t\t{}'.format(feature_class_list))


# Derive list of tables from the data dictionary
# feature_class_list = list(data_dictionary.keys())
table_dictionary = {k:v for k, v in data_dictionary.items() if v['type'] == 'table'}
table_list = list(table_dictionary.keys())
print('\n\ntable_list:\t\t{}'.format(table_list))


copy_feature_classes = False


if copy_feature_classes:
    # Copy CS ArcSDE feature classes to file geodatabase feature classes
    print('\n\nCopying feature classes...')
    for feature_class in feature_class_list:
        print('\tfeature_class:\t\t{}'.format(feature_class))
        desc = arcpy.Describe(value=data_dictionary[feature_class]['in_dataset'])
        print('\t\tshapeType:\t\t{}'.format(desc.shapeType))
        result = arcpy.GetCount_management(in_rows=data_dictionary[feature_class]['in_dataset'])
        count = int(result.getOutput(0))
        print('\t\tcount:\t\t{}'.format(count))
        print('\t\tout_feature_class:\t\t{}'.format(data_dictionary[feature_class]['out_dataset']))
        if arcpy.Exists(dataset=data_dictionary[feature_class]['out_dataset']):
            arcpy.Delete_management(in_data=data_dictionary[feature_class]['out_dataset'],
                                    data_type='')
        arcpy.Copy_management(in_data=data_dictionary[feature_class]['in_dataset'],
                              out_data=data_dictionary[feature_class]['out_dataset'],
                              data_type='')
    print('Copied feature classes.')


copy_tables = False


if copy_tables:
    # Copy CS ArcSDE tables to file geodatabase tables
    print('\n\nCopying tables...')
    for table in table_list:
        print('\ttable:\t\t{}'.format(table))
        desc = arcpy.Describe(value=data_dictionary[table]['in_dataset'])
        if desc.hasOID:
            print('\t\tOIDFieldName:\t\t{}'.format(desc.OIDFieldName))
        result = arcpy.GetCount_management(in_rows=data_dictionary[table]['in_dataset'])
        count = int(result.getOutput(0))
        print('\t\tcount:\t\t{}'.format(count))
        print('\t\tout_table:\t\t{}'.format(data_dictionary[table]['out_dataset']))
        if arcpy.Exists(dataset=data_dictionary[table]['out_dataset']):
            arcpy.Delete_management(in_data=data_dictionary[table]['out_dataset'],
                                    data_type='')
        arcpy.CopyRows_management(in_rows=data_dictionary[table]['in_dataset'],
                                  out_table=data_dictionary[table]['out_dataset'],
                                  config_keyword='')
    print('Copied tables.')


add_feature_class_guids = False


if add_feature_class_guids:
    # Add GUID field to file geodatabase feature classes
    print('\n\nAdding GUID fields to feature classes...')
    for feature_class in feature_class_list:
        print('\tfeature_class:\t\t{}'.format(feature_class))
        print('\t\tout_feature_class:\t\t{}'.format(data_dictionary[feature_class]['out_dataset']))
        print('\t\tguid_field:\t\t{}'.format(data_dictionary[feature_class]['guid_field']))
        field_list = arcpy.ListFields(dataset=data_dictionary[feature_class]['out_dataset'],
                                      #wild_card=data_dictionary[feature_class]['guid_field'],
                                      wild_card='*',
                                      field_type='All')
        # print('\tfield_list:\t\t{}'.format(field_list))
        for field in field_list:
            print('\t\t{} is a {} field'.format(field.name, field.type))
            if field.name == data_dictionary[feature_class]['guid_field']:
                print('\tDeleting existing GUID field {}...'.format(data_dictionary[feature_class]['guid_field']))
                arcpy.DeleteField_management(in_table=feature_class,
                                             drop_field=list(data_dictionary[feature_class]['guid_field']))
                print('\tDeleted existing GUID field {}.'.format(data_dictionary[feature_class]['guid_field']))
        print('\tAdding GUID field {}...'.format(data_dictionary[feature_class]['guid_field']))
        # Note that fields with Allow NULL Values = NO can only be added to empty feature classes or tables
        # Therefore, field_is_nullable parameter must be set to 'NULLABLE'
        # See:  http://support.esri.com/technical-article/000010006
        arcpy.AddField_management(in_table=data_dictionary[feature_class]['out_dataset'],
                                  field_name=data_dictionary[feature_class]['guid_field'],
                                  field_type='GUID',
                                  field_precision='#',
                                  field_scale='#',
                                  field_length='#',
                                  field_alias='#',
                                  field_is_nullable='NULLABLE',
                                  field_is_required='REQUIRED',
                                  field_domain='#')
        print('\tAdded GUID field {}.'.format(data_dictionary[feature_class]['guid_field']))
        print('\tCalculating GUID field {}...'.format(data_dictionary[feature_class]['guid_field']))
        code_block = '''def GUID():
            import uuid
            return \'{\' + str(uuid.uuid4()) + \'}\''''
        arcpy.CalculateField_management(in_table=data_dictionary[feature_class]['out_dataset'],
                                        field=data_dictionary[feature_class]['guid_field'],
                                        expression='GUID()',
                                        expression_type='PYTHON',
                                        code_block=code_block)
        print('\tCalculated GUID field {}.'.format(data_dictionary[feature_class]['guid_field']))
    print('Added GUID fields to feature classes.')


add_related_table_guids = False


if add_related_table_guids:
    # Add GUID field to EVENTDATA table
    print('\tAdding GUID field {}...'.format(data_dictionary['EVENTDATA']['guid_field']))
    # Note that fields with Allow NULL Values = NO can only be added to empty feature classes or tables
    # Therefore, field_is_nullable parameter must be set to 'NULLABLE'
    # See:  http://support.esri.com/technical-article/000010006
    arcpy.AddField_management(in_table=data_dictionary['EVENTDATA']['out_dataset'],
                              field_name=data_dictionary['EVENTDATA']['guid_field'],
                              field_type='GUID',
                              field_precision='#',
                              field_scale='#',
                              field_length='#',
                              field_alias='#',
                              field_is_nullable='NULLABLE',
                              field_is_required='REQUIRED',
                              field_domain='#')
    print('\tAdded GUID field {}.'.format(data_dictionary['EVENTDATA']['guid_field']))
    print('\tCalculating GUID field {}...'.format(data_dictionary['EVENTDATA']['guid_field']))
    code_block = '''def GUID():
        import uuid
        return \'{\' + str(uuid.uuid4()) + \'}\''''
    arcpy.CalculateField_management(in_table=data_dictionary['EVENTDATA']['out_dataset'],
                                    field=data_dictionary['EVENTDATA']['guid_field'],
                                    expression='GUID()',
                                    expression_type='PYTHON',
                                    code_block=code_block)
    print('\tCalculated GUID field {}.'.format(data_dictionary['EVENTDATA']['guid_field']))
    # Add GUID field to file geodatabase tables
    print('\n\nAdding GUID fields to tables...')
    for table in table_list:
        print('\ttable:\t\t{}'.format(table))
        print('\t\tin_data={}'.format(data_dictionary[table]['out_dataset']))
        print('\t\tin_field={}'.format(data_dictionary[table]['join_field']))
        print('\t\tjoin_table={}'.format(data_dictionary[table]['join_table']))
        print('\t\tjoin_field={}'.format(data_dictionary[table]['join_field']))
        thing = os.path.basename(data_dictionary[table]['join_table'])
        print('\t\tthing={}'.format(thing))
        print('\t\tfields={}'.format([data_dictionary[thing]['guid_field']]))
        arcpy.JoinField_management(in_data=data_dictionary[table]['out_dataset'],
                                   in_field=data_dictionary[table]['join_field'],
                                   join_table=data_dictionary[table]['join_table'],
                                   join_field=data_dictionary[table]['join_field'],
                                   fields=[data_dictionary[thing]['guid_field']])
    print('Added GUID fields to tables.')


print('\n' * 5)


# See:  http://gis.stackexchange.com/questions/116274/select-random-rows-with-python-in-arcgis

# table = data_dictionary['COMPDATA']['out_dataset']

fc = data_dictionary['POINTDATA']['out_dataset']
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
rt = data_dictionary['PCOMPDATA']['out_dataset']
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
