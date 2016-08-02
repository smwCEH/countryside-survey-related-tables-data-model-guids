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


# Define file geodatabase
# fgdb = r'E:\CountrysideSurvey\esri-uk\guids\guids-{}.gdb'.format(datetime.datetime.now().strftime('%Y%m%d'))
# fgdb = r'E:\CountrysideSurvey\esri-uk\guids\guids-20160714.gdb'
# fgdb = r'E:\CountrysideSurvey\esri-uk\guids\guids-20160715.gdb'
# fgdb = r'E:\CountrysideSurvey\esri-uk\guids\guids-{}-with-nullable-fields.gdb'.format(datetime.datetime.now().strftime('%Y%m%d'))
fgdb = r'E:\CountrysideSurvey\esri-uk\guids\guids-{}-without-nullable-fields.gdb'.format(datetime.datetime.now().strftime('%Y%m%d'))
print('\n\nfgdb:\t\t\{}'.format(fgdb))


# Create file geodatabase if it doesn't exist
if not arcpy.Exists(dataset=fgdb):
    arcpy.CreateFileGDB_management(out_folder_path=os.path.dirname(fgdb),
                                   out_name=os.path.basename(fgdb),
                                   out_version='')


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



print(json.dumps(data_dictionary,
                 sort_keys=False,
                 indent=4))


copy_datasets = True


if copy_datasets:
    # Copy CS ArcSDE datasets to file geodatabase datasets
    print('\n\nCopying datasets...')
    #
    # Copy the BLKDATA feature class
    # Define input_dataset
    dataset = r'BLKDATA'
    dataset_in = arcsde + '\\' + arcsde_user + '.' + arcsde_fd + '\\' + dataset
    #Define output dataset
    dataset_out = os.path.join(fgdb, dataset)
    #  Display input and output dataset paths
    print('\t\tdataset_in:\t\t{}'.format(dataset_in))
    print('\t\tdataset_out:\t\t{}'.format(dataset_out))
    # Delete out dataset if it already exists
    if arcpy.Exists(dataset_out):
        arcpy.Delete_management(in_data=dataset_out,
                                data_type='')
    # Create empty feature class
    desc = arcpy.Describe(dataset_in)
    dataType = desc.dataType
    print('\t\t\tdataType:\t\t{}'.format(dataType))
    shapeType = desc.shapeType
    print('\t\t\tshapeType:\t\t{}'.format(shapeType))
    arcpy.CreateFeatureclass_management(out_path=os.path.dirname(dataset_out),
                                        out_name=os.path.basename(dataset_out),
                                        geometry_type=shapeType,
                                        spatial_reference=arcpy.SpatialReference(27700))
    fields = arcpy.ListFields(dataset_out)
    print('\t\tListing fields in out feature class and creating in new feature class...')
    fields = arcpy.ListFields(dataset_in)
    for field in fields:
        if field.name not in ['OBJECTID', 'SHAPE', 'SHAPE.AREA', 'SHAPE.LEN']:
            print('\t\t\t{0} is a type of {1} with a length of {2}'.format(field.name,
                                                                           field.type,
                                                                           field.length))
            arcpy.AddField_management(in_table=dataset_out,
                                      field_name=field.name,
                                      field_type=field.type,
                                      field_precision=field.precision,
                                      field_scale=field.scale,
                                      field_length=field.length,
                                      field_alias=field.aliasName,
                                      field_is_nullable='NULLABLE',  # field_is_nullable=field.isNullable,
                                      field_is_required=field.required,
                                      field_domain=field.domain)
    del field, fields
    print('\t\tListed fields in out feature class and created in new feature class.')
    # Append data from out dataset to new dataset
    print('\t\tAppending rows from in feature class to out feature class...')
    arcpy.Append_management(inputs=[dataset_in],
                            target=dataset_out,
                            schema_type='TEST')
    print('\t\tAppended rows from in feature class to out feature class.')
    #
    # Add Editor and Date of edit fields to BLKDATA feature class
    print('\t\tAdding Editor and Date of Edit fields to {} feature class...'.format(dataset_out))
    arcpy.AddField_management(in_table=dataset_out,
                              field_name='EDITOR',
                              field_type='TEXT',
                              field_precision='',
                              field_scale='',
                              field_length=25,
                              field_alias='',
                              field_is_nullable='NULLABLE',
                              field_is_required='NON_REQUIRED',
                              field_domain='')
    arcpy.AddField_management(in_table=dataset_out,
                              field_name='DATE_OF_EDIT',
                              field_type='DATE',
                              field_precision='',
                              field_scale='',
                              field_length='',
                              field_alias='',
                              field_is_nullable='NULLABLE',
                              field_is_required='NON_REQUIRED',
                              field_domain='')
    print('\t\tAdded Editor and Date of Edit fields to {} feature class.'.format(dataset_out))
    #
    # Copy CS ArcSDE datasets and their related tables
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
        # Create new feature class
        if dataset in ('SCPTDATA', 'POINTDATA', 'LINEARDATA'):      # Only copy feature classes as EVENTDATA related table will be copied as the related table of the LINEARDATA feature class
            #
            #  Delete out dataset if it already exists
            if arcpy.Exists(dataset_out):
                arcpy.Delete_management(in_data=dataset_out,
                                        data_type='')
            #
            # Create empty feature class
            desc = arcpy.Describe(dataset_in)
            dataType = desc.dataType
            print('\t\t\tdataType:\t\t{}'.format(dataType))
            shapeType = desc.shapeType
            print('\t\t\tshapeType:\t\t{}'.format(shapeType))
            arcpy.CreateFeatureclass_management(out_path=os.path.dirname(dataset_out),
                                                out_name=os.path.basename(dataset_out),
                                                geometry_type=shapeType,
                                                spatial_reference=arcpy.SpatialReference(27700))
            fields = arcpy.ListFields(dataset_out)
            # for field in fields:
            #     print('\t\t\t{0} is a type of {1} with a length of {2}'.format(field.name,
            #                                                                    field.type,
            #                                                                    field.length))
            # del field, fields
            #
            # List fields in dataset_in and create fields in dataset_out
            print('\t\tListing fields in out feature class and creating in new feature class...')
            fields = arcpy.ListFields(dataset_in)
            for field in fields:
                if field.name not in ['OBJECTID', 'SHAPE', 'SHAPE.AREA', 'SHAPE.LEN']:
                    print('\t\t\t{0} is a type of {1} with a length of {2}'.format(field.name,
                                                                                   field.type,
                                                                                   field.length))
                    # print('\t\t\t\t{0} {1} nullable'.format(field.name,
                    #                                         'is' if field.isNullable else 'is not'))
                    # print('\t\t\t\t{0} has associated domain {1} ?????'.format(field.name,
                    #                                                      field.domain))
                    # print('\t\t\t\t{0} {1} required'.format(field.name,
                    #                                         'is' if field.required else 'is not'))
                    arcpy.AddField_management(in_table=dataset_out,
                                              field_name=field.name,
                                              field_type=field.type,
                                              field_precision=field.precision,
                                              field_scale=field.scale,
                                              field_length=field.length,
                                              field_alias=field.aliasName,
                                              field_is_nullable='NULLABLE',  # field_is_nullable=field.isNullable,
                                              field_is_required=field.required,
                                              field_domain=field.domain)
            del field, fields
            print('\t\tListed fields in out feature class and created in new feature class.')
            #
            # Append data from out dataset to new dataset
            print('\t\tAppending rows from in feature class to out feature class...')
            arcpy.Append_management(inputs=[dataset_in],
                                    target=dataset_out,
                                    schema_type='TEST')
            print('\t\tAppended rows from in feature class to out feature class.')
            #
            # Add Editor and Date of edit fields to BLKDATA feature class
            print('\t\tAdding Editor and Date of Edit fields to {} feature class...'.format(dataset_out))
            arcpy.AddField_management(in_table=dataset_out,
                                      field_name='EDITOR',
                                      field_type='TEXT',
                                      field_precision='',
                                      field_scale='',
                                      field_length=25,
                                      field_alias='',
                                      field_is_nullable='NULLABLE',
                                      field_is_required='NON_REQUIRED',
                                      field_domain='')
            arcpy.AddField_management(in_table=dataset_out,
                                      field_name='DATE_OF_EDIT',
                                      field_type='DATE',
                                      field_precision='',
                                      field_scale='',
                                      field_length='',
                                      field_alias='',
                                      field_is_nullable='NULLABLE',
                                      field_is_required='NON_REQUIRED',
                                      field_domain='')
            print('\t\tAdded Editor and Date of Edit fields to {} feature class.'.format(dataset_out))
        #
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
        # #
        # # Copy related table
        # arcpy.Copy_management(in_data=related_table_in,
        #                       out_data=related_table_out,
        #                       data_type='')
        #
        # Create empty table
        desc = arcpy.Describe(related_table_in)
        dataType = desc.dataType
        print('\t\t\tdataType:\t\t{}'.format(dataType))
        arcpy.CreateTable_management(out_path=os.path.dirname(related_table_out),
                                     out_name=os.path.basename(related_table_out))
        # fields = arcpy.ListFields(related_table_out)
        # for field in fields:
        #     print('\t\t\t{0} is a type of {1} with a length of {2}'.format(field.name,
        #                                                                    field.type,
        #                                                                    field.length))
        # del field, fields
        #
        # List fields in dataset_in and create fields in dataset_out
        print('\t\tListing fields in out feature class and creating in new feature class...')
        fields = arcpy.ListFields(related_table_in)
        for field in fields:
            if field.name not in ['OBJECTID']:
                print('\t\t\t{0} is a type of {1} with a length of {2}'.format(field.name,
                                                                               field.type,
                                                                               field.length))
                # print('\t\t\t\t{0} {1} nullable'.format(field.name,
                #                                         'is' if field.isNullable else 'is not'))
                # print('\t\t\t\t{0} has associated domain {1} ?????'.format(field.name,
                #                                                      field.domain))
                # print('\t\t\t\t{0} {1} required'.format(field.name,
                #                                         'is' if field.required else 'is not'))
                arcpy.AddField_management(in_table=related_table_out,
                                          field_name=field.name,
                                          field_type=field.type,
                                          field_precision=field.precision,
                                          field_scale=field.scale,
                                          field_length=field.length,
                                          field_alias=field.aliasName,
                                          field_is_nullable='NULLABLE',  # field_is_nullable=field.isNullable,
                                          field_is_required=field.required,
                                          field_domain=field.domain)
        del field, fields
        print('\t\tListed fields in out feature class and created in new feature class.')
        #
        # Append data from out dataset to new dataset
        print('\t\tAppending rows from in related table to out related table...')
        arcpy.Append_management(inputs=[related_table_in],
                                target=related_table_out,
                                schema_type='TEST')
        print('\t\tAppended rows from in related table to out related table.')
        #
        # Add Editor and Date of edit fields to BLKDATA feature class
        print('\t\tAdding Editor and Date of Edit fields to {} feature class...'.format(dataset_out))
        arcpy.AddField_management(in_table=related_table_out,
                                  field_name='EDITOR',
                                  field_type='TEXT',
                                  field_precision='',
                                  field_scale='',
                                  field_length=25,
                                  field_alias='',
                                  field_is_nullable='NULLABLE',
                                  field_is_required='NON_REQUIRED',
                                  field_domain='')
        arcpy.AddField_management(in_table=related_table_out,
                                  field_name='DATE_OF_EDIT',
                                  field_type='DATE',
                                  field_precision='',
                                  field_scale='',
                                  field_length='',
                                  field_alias='',
                                  field_is_nullable='NULLABLE',
                                  field_is_required='NON_REQUIRED',
                                  field_domain='')
        print('\t\tAdded Editor and Date of Edit fields to {} feature class.'.format(dataset_out))
    #
    # Add Point_Proximity field to POINTDATA feature class
    print('\tAdding Point_Proximity field to POINTDATA feature class...')
    arcpy.AddField_management(in_table=os.path.join(fgdb, 'POINTDATA'),
                              field_name='Point_Proximity',
                              field_type='FLOAT',
                              field_precision='',
                              field_scale='',
                              field_length='',
                              field_alias='',
                              field_is_nullable='NULLABLE',
                              field_is_required='NON_REQUIRED',
                              field_domain='')
    print('\tAdding Point_Proximity field to POINTDATA feature class.')
    #
    print('Copied datasets.')


add_guids = True


if add_guids:
    # Add GUID field to file geodatabase datasets
    print('\n\nAdding GUID fields to datasets...')
    #
    # Add GUID field to the BLKDATA feature class
    dataset = r'BLKDATA'
    #Define output dataset
    dataset_out = os.path.join(fgdb, dataset)
    #  Display input and output dataset paths
    print('\t\tdataset_in:\t\t{}'.format(dataset_in))
    print('\t\tdataset_out:\t\t{}'.format(dataset_out))
    # Define GUID field
    guid_field = dataset + '_GUID'
    print('\t\tguid_field:\t\t{}'.format(guid_field))
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
                              field_is_nullable='NULLABLE',  # field_is_nullable='NULLABLE',
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
    # Add attribute index to newly added GUID field
    print('\t\tAdding attribute index to GUID field {}...'.format(guid_field))
    index_name = guid_field + '_IDX'
    if len(arcpy.ListIndexes(dataset=dataset_out,
                             wild_card=index_name)) > 0:
        print('\t\t\tDeleting attribute index {}...'.format(index_name))
        arcpy.RemoveIndex_management(in_table=dataset_out,
                                     index_name=index_name)
        print('\t\t\tDeleted attribute index {}.'.format(index_name))
    arcpy.AddIndex_management(in_table=dataset_out,
                              fields=guid_field,
                              index_name=index_name,
                              unique='UNIQUE',
                              ascending='NON_ASCENDING')
    print('\t\tAdded attribute index to GUID field {}.'.format(guid_field))
    #
    # Add GUID field to datasets defined by data_dictionary
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
                                  field_is_nullable='NULLABLE',  # field_is_nullable='NULLABLE',
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
        # Add attribute index to newly added GUID field
        print('\t\tAdding attribute index to GUID field {}...'.format(guid_field))
        index_name = guid_field + '_IDX'
        if len(arcpy.ListIndexes(dataset=dataset_out,
                                 wild_card=index_name)) > 0:
            print('\t\t\tDeleting attribute index {}...'.format(index_name))
            arcpy.RemoveIndex_management(in_table=dataset_out,
                                         index_name=index_name)
            print('\t\t\tDeleted attribute index {}.'.format(index_name))
        arcpy.AddIndex_management(in_table=dataset_out,
                                  fields=guid_field,
                                  index_name=index_name,
                                  unique='UNIQUE',
                                  ascending='NON_ASCENDING')
        print('\t\tAdded attribute index to GUID field {}.'.format(guid_field))
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
        #
        # Add attribute index to newly joined GUID field
        print('\t\t\tAdding attribute index to GUID field {}...'.format(guid_field))
        index_name = guid_field + '_IDX'
        if len(arcpy.ListIndexes(dataset=related_table_out,
                                 wild_card=index_name)) > 0:
            print('\t\t\t\tDeleting attribute index {}...'.format(index_name))
            arcpy.RemoveIndex_management(in_table=related_table_out,
                                         index_name=index_name)
            print('\t\t\t\tDeleted attribute index {}.'.format(index_name))
        arcpy.AddIndex_management(in_table=related_table_out,
                                  fields=guid_field,
                                  index_name=index_name,
                                  unique='UNIQUE',
                                  ascending='NON_ASCENDING')
        print('\t\t\tAdded attribute index to GUID field {}.'.format(guid_field))
    #
    print('Added GUID fields to datasets.')


check_guids = True


if check_guids:
    # Checking GUID fields in related file geodatabase datasets
    print('\n' * 5 + 'Checking GUID fields in related datasets...')
    #
    # Set sample size
    sample_size = 25
    print('sample_size:\t\t{}'.format(sample_size))
    #
    for dataset in data_dictionary.keys():
    # for dataset in ['SCPTDATA']:
        print('\tdataset:\t\t{}'.format(dataset))
        #
        # Define output dataset
        dataset_out = os.path.join(fgdb, dataset)
        print('\t\tdataset_out:\t\t{}'.format(dataset_out))
        #
        # Get ID field name from data dictionary
        id_field = data_dictionary[dataset]['id_field']
        print('\t\tid_field:\t\t{}'.format(id_field))
        #
        # Get GUID field name from data dictionary
        guid_field = data_dictionary[dataset]['guid_field']
        print('\t\tguid_field:\t\t{}'.format(guid_field))
        #
        # Get related table from data dictinary
        related_table = data_dictionary[dataset]['related_table']
        related_table = os.path.join(fgdb, related_table)
        print('\t\trelated_table:\t\t{}'.format(related_table))
        #
        # Get GUIDS from file geodatabase dataset
        object_ids = [r[0] for r in arcpy.da.SearchCursor(in_table=dataset_out,
                                                          field_names=['OID@'])]
        # print('object_ids:\t{}'.format(object_ids))
        print('\t\tlen(object_ids):\t{0}\n\t\tsample_size:\t{1}'.format(len(object_ids), sample_size))
        random_ids = random.sample(object_ids, sample_size)
        random_ids = sorted(random_ids, key=int, reverse=False)
        # print('\t\trandom_ids:\t{0}'.format(random_ids))
        oid_field = arcpy.Describe(dataset_out).OIDFieldName
        # print('\t\toid_field:\t{0}'.format(oid_field))
        where_clause = '"{0}" IN ({1})'.format(oid_field, ','.join(map(str, random_ids)))
        # print('\t\twhere_clause:\t{}'.format(where_clause))
        rows = [row for row in arcpy.da.SearchCursor(in_table=dataset_out,
                                                     field_names=['OID@', id_field, guid_field],
                                                     where_clause=where_clause,
                                                     sql_clause=(None, 'ORDER BY ' + id_field + ', ' + guid_field))]
        row_count = len(rows)
        del rows
        print('\t\trow_count:\t\t{}'.format(row_count))
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
                print('\t\t{0:<4}\t\t{1:>6}\t\t{2:>10}\t\t{3:>36}'.format(count, row[0], row[1], row[2]))
                sample_list.append([row[0], row[1], row[2]])
        # print('\t\tsample_list:\t{}'.format(sample_list))
        for sample in sample_list:
            # print(sample)
            print('\t\tid:\t\t\t{}'.format(sample[1]))
            print('\t\tguid:\t\t{}'.format(sample[2]))
            where_clause = '"{0}" = ({1})'.format(id_field, sample[1])
            # print('\t\twhere_clause:\t{}'.format(where_clause))
            count = 0
            rows = [row for row in arcpy.da.SearchCursor(in_table=related_table,
                                                         field_names=['OID@', id_field, guid_field],
                                                         where_clause=where_clause,
                                                         sql_clause=(None, 'ORDER BY ' + id_field + ', ' + guid_field))]
            row_count = len(rows)
            print('\t\trow_count:\t\t{}'.format(row_count))
            del rows
            with arcpy.da.SearchCursor(in_table=related_table,
                                       field_names=['OID@', id_field, guid_field],
                                       where_clause=where_clause,
                                       sql_clause=(None, 'ORDER BY ' + id_field + ', ' + guid_field)) as cursor:
                for row in cursor:
                    count += 1
                    print('\t\trow:\t\t{}'.format(row))
                    print('\t\trow[2]:\t\t{}'.format(row[2]))
                    print('\t\tsample[2]:\t{}'.format(sample[2]))
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
    print('\n\nChecked GUID fields in related datasets.' + '\n' * 5)


create_relationship_classes = True


if create_relationship_classes:
    # Add relationship classes
    print('\n\nCreating relationship classes...')
    for dataset in data_dictionary.keys():
        print('\tdataset:\t\t{}'.format(dataset))
        #
        # Define output dataset
        dataset_out = os.path.join(fgdb, dataset)
        print('\t\tdataset_out:\t\t{}'.format(dataset_out))
        #
        # Get related table from data dictionary
        related_table = data_dictionary[dataset]['related_table']
        # print('\t\trelated_table:\t\t{}'.format(related_table))
        #
        # Get related table from data dictionary
        guid_field = data_dictionary[dataset]['guid_field']
        print('\t\tguid_field:\t\t{}'.format(guid_field))
        #
        # Define output related table path
        related_table_out = os.path.join(fgdb, related_table)
        print('\t\trelated_table_out:\t\t{}'.format(related_table_out))
        #
        #  Create relationship class
        print('\t\tCreating relationship class...')
        print('\t\t\torigin_table:\t\t\t\t{}'.format(dataset_out))
        print('\t\t\tdestination_table:\t\t\t{}'.format(related_table_out))
        out_relationship_class = os.path.basename(dataset_out) + '_' + os.path.basename(related_table_out)
        print('\t\t\tout_relationship_class:\t\t{}'.format(out_relationship_class))
        relationship_type = 'COMPOSITE'
        print('\t\t\trelationship_type:\t\t\t{}'.format(relationship_type))
        forward_label = os.path.basename(dataset_out)
        print('\t\t\tforward_label:\t\t\t\t{}'.format(forward_label))
        backward_label = os.path.basename(related_table_out)
        print('\t\t\tbackward_label:\t\t\t\t{}'.format(backward_label))
        message_direction = 'FORWARD'
        print('\t\t\tmessage_direction:\t\t\t{}'.format(message_direction))
        cardinality = 'ONE_TO_MANY'
        print('\t\t\tcardinality:\t\t\t\t{}'.format(cardinality))
        attributed = 'NONE'
        print('\t\t\tattributed:\t\t\t\t\t{}'.format(attributed))
        origin_primary_key = guid_field
        print('\t\t\torigin_primary_key:\t\t\t{}'.format(origin_primary_key))
        origin_foreign_key = ''
        print('\t\t\torigin_foreign_key:\t\t\t{}'.format(origin_foreign_key))
        destination_primary_key = guid_field
        print('\t\t\tdestination_primary_key:\t{}'.format(destination_primary_key))
        destination_foreign_key = ''
        print('\t\t\tdestination_foreign_key:\t{}'.format(destination_foreign_key))
        # desc = arcpy.Describe(value=os.path.join(fgdb, out_relationship_class))
        # print('desc.name:\t\t{}'.format(desc.name))
        # if hasattr(desc, 'name'):
        #     print('\t\t\tDeleting existing relationship class {}...'.format(out_relationship_class))
        #     arcpy.Delete_management(in_data=os.path.join(fgdb, out_relationship_class))
        #     print('\t\t\tDeleted existing relationship class {}.'.format(out_relationship_class))
        if arcpy.Exists(dataset=os.path.join(fgdb, out_relationship_class)):
            print('\t\t\tDeleting existing relationship class {}...'.format(out_relationship_class))
            arcpy.Delete_management(in_data=os.path.join(fgdb, out_relationship_class))
            print('\t\t\tDeleted existing relationship class {}.'.format(out_relationship_class))
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
        print('\t\tCreating relationship class...')
    #
    print('Creating relationship classes...')


copy_domains = True


if copy_domains:
    print('\n\nCopying domains and applying to fields...')
    #
    # Define domain tables code and description fields
    code_field = 'Code'
    print('\tcode_field:\t\t\t\t{}'.format(code_field))
    description_field = 'Description'
    print('\tdescription_field:\t\t{}'.format(description_field))
    # # Define in file geodatabase from which to copy domains
    # # This file geodatabase was created from an XML Workspace document created from the CS ArcSDE geodatabase
    fgdb_in = r'E:\CountrysideSurvey\esri-uk\domains\domains.gdb'
    print('\tfgdb_in:\t\t{}'.format(fgdb_in))
    # Define temporary file geodatabase
    fgdb_temp = os.path.dirname(fgdb_in)
    fgdb_temp = os.path.join(fgdb_temp, r'temporary_domain_tables' + r'.gdb')
    print('\t\tfgdb_temp:\t\t{}'.format(fgdb_temp))
    # Create temporary file geodatabase
    if arcpy.Exists(fgdb_temp):
        print('\t\tDeleting fgdb_temp {}...'.format(fgdb_temp))
        arcpy.Delete_management(fgdb_temp)
        print('\t\tDeleted fgdb_temp {}.'.format(fgdb_temp))
    print('\tCreating fgdb_temp {}...'.format(fgdb_temp))
    arcpy.CreateFileGDB_management(out_folder_path=os.path.dirname(fgdb_temp),
                                   out_name=os.path.basename(fgdb_temp),
                                   out_version='CURRENT')
    print('\t\tCreated fgdb_temp {}.'.format(fgdb_temp))
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
            print('\t\ttable_out:\t\t\t\t{}'.format(table_out))
            arcpy.DomainToTable_management(in_workspace=fgdb_in,
                                           domain_name=domain.name,
                                           out_table=table_out,
                                           code_field=code_field,
                                           description_field=description_field,
                                           configuration_keyword='')
            print('\tConverted domain to table in temporary file geodatabase.')
            # Convert table to domain in the out file geodatabase
            print('\tConverting table to domain in the out file geodatabase...')
            existing_domains_list = arcpy.Describe(fgdb).domains
            print('\t\texisiting_domains_list:\t\t{}'.format(existing_domains_list))
            if domain.name in existing_domains_list:
                print('\t\t\tDeleting existing domain {} in file geodatabase...'.format(domain.name))
                arcpy.DeleteDomain_management(in_workspace=fgdb,
                                              domain_name=domain.name)
                print('\t\t\tDeleted existing domain {} in file geodatabase.'.format(domain.name))
            domain_description = domain.name.replace('_', ' ') + ' domain'
            print('\t\tdomain_description:\t\t{}'.format(domain_description))
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
            field_name = domain.name.replace('CS2007_', '')
            print('\t\tfield_name:\t\t{}'.format(field_name))
            arcpy.env.workspace = fgdb
            # tables = arcpy.ListTables()
            tables = ['SCPTDATA', 'LINEARDATA', 'POINTDATA', 'COMPDATA', 'EVENTDATA', 'SEVENTDATA', 'PCOMPDATA']
            for table in tables:
                print('\t\t\ttable:\t\t{}'.format(table))
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
    fecodes_table = r'C:\Users\SMW\AppData\Roaming\ESRI\Desktop10.1\ArcCatalog\Connection to LADB TBB WGEMADMIN.sde\WGEMADMIN.FECODES'
    searchcursor_fields = ['COLUMN_NAME', 'CODE', 'DESCRIPTION']
    for column_name in ['LUSE', 'CONDITION', 'DISEASE_SIGNS', 'HABITAT_BOXES']:
        print('\n\ncolumn_name:\t\t{}'.format(column_name))
        #
        domain = 'GMEP13_' + column_name
        print('domain:\t\t{}'.format(domain))
        #
        where_clause = u'{0} = \'{1}\''.format(arcpy.AddFieldDelimiters(fecodes_table, 'COLUMN_NAME'),
                                           column_name)
        print('\twhere_clause:\t\t{}'.format(where_clause))
        wgem_table = os.path.join(fgdb_temp, 'WGEM_' + column_name)
        print('\twgem_table:\t\t{}'.format(wgem_table))
        if arcpy.Exists(wgem_table):
            print('\t\t\tDeleting wgem_table {}...'.format(wgem_table))
            arcpy.Delete_management(wgem_table)
            print('\t\t\tDeleted wgem_table {}.'.format(wgem_table))
        print('\t\tCreating wgem_table {}...'.format(wgem_table))
        arcpy.CreateTable_management(out_path=os.path.dirname(wgem_table),
                                     out_name=os.path.basename(wgem_table))
        print('\t\t\tAdding fields to wgem_table {}...'.format(wgem_table))
        arcpy.AddField_management(in_table=wgem_table,
                                  field_name=code_field,
                                  field_type='TEXT',
                                  field_length=10)
        arcpy.AddField_management(in_table=wgem_table,
                                  field_name=description_field,
                                  field_type='TEXT',
                                  field_length=40)
        print('\t\t\tAdded fields to wgem_table {}.'.format(wgem_table))
        print('\t\tCreated wgem_table {}.'.format(wgem_table))
        print('\tUsing arcpy.da cursors to find values and add to wgem_table...')
        print('\t{0:<20}\t{1:<20}\t{2:<20}'.format(searchcursor_fields[0],
                                                   searchcursor_fields[1],
                                                   searchcursor_fields[2]))
        insertcursor_fields = ['CODE', 'DESCRIPTION']
        insert_cursor = arcpy.da.InsertCursor(in_table=wgem_table,
                                              field_names=insertcursor_fields)
        with arcpy.da.SearchCursor(in_table=fecodes_table,
                                   field_names=searchcursor_fields,
                                   where_clause=where_clause) as search_cursor:
            for search_row in search_cursor:
                print('\t{0:<20}\t{1:<20}\t{2:<20}'.format(search_row[0],
                                                           search_row[1],
                                                           search_row[2]))
                insert_cursor.insertRow((search_row[1],
                                         search_row[2]))
        del insert_cursor
        del search_row, search_cursor
        print('\tUsed arcpy.da cursors to find values and add to wgem_table.')
        #
        print('\tConverting table to domain in the out file geodatabase...')
        existing_domains_list = arcpy.Describe(fgdb).domains
        print('\t\texisiting_domains_list:\t\t{}'.format(existing_domains_list))
        if domain in existing_domains_list:
            print('\t\t\tDeleting existing domain {} in file geodatabase...'.format(domain.name))
            arcpy.DeleteDomain_management(in_workspace=fgdb,
                                          domain_name=domain.name)
            print('\t\t\tDeleted existing domain {} in file geodatabase.'.format(domain.name))
        domain_description = domain.replace('_', ' ') + ' domain'
        print('\t\tdomain_description:\t\t{}'.format(domain_description))
        arcpy.TableToDomain_management(in_table=wgem_table,
                                       code_field=code_field,
                                       description_field=description_field,
                                       in_workspace=fgdb,
                                       domain_name=domain,
                                       domain_description=domain_description,
                                       update_option='REPLACE')
        print('\tConverted table to domain in the out file geodatabase.')
        #
        # Assign domain to field
        print('\tAssigning domain to a field ...')
        field_name = column_name
        print('\t\tfield_name:\t\t{}'.format(field_name))
        arcpy.env.workspace = fgdb
        # tables = arcpy.ListTables()
        tables = ['SCPTDATA', 'LINEARDATA', 'POINTDATA', 'COMPDATA', 'EVENTDATA', 'SEVENTDATA', 'PCOMPDATA']
        for table in tables:
            print('\t\t\ttable:\t\t{}'.format(table))
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
    # # Delete temporary file geodatabase used to store intermediate domain tables
    # print('\tDeleting fgdb_temp {}...'.format(fgdb_temp))
    # arcpy.Delete_management(fgdb_temp)
    # print('\tDeleted fgdb_temp {}.'.format(fgdb_temp))
    #
    print('\n\nCopied domains and applied to fields.')


# Capture end_time
end_time = time.time()


# Report elapsed_time (= end_time - start_time)
print('\n\nIt took {} to execute this.'.format(hms_string(end_time - start_time)))


# Print script filename, finish date and time
print('\n\nFinished {0} at {1} on {2}.\n'.format(script,
                                                 datetime.datetime.now().strftime('%H:%M:%S'),
                                                 datetime.datetime.now().strftime('%Y-%m-%d')))
