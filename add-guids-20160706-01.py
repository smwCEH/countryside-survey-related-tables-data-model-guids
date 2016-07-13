import os
import sys
import platform
import datetime
import time


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


# Define ArcSDE path
# arcsde = r'Database Connections\Connection to LADB FEGEN2 CS2007_ADMIN.sde'
arcsde = r'C:\Users\SMW\AppData\Roaming\ESRI\Desktop10.1\ArcCatalog\Connection to LADB FEGEN2 CS2007_ADMIN.sde'
print('\n\narcsde:\t\t{}'.format(arcsde))


# Define ArcSDE user
arcsde_user = r'CS2007_ADMIN'
print('\n\narcsde_user:\t\t{}'.format(arcsde_user))


# Define file geodatabase
fgdb = r'E:\CountrysideSurvey\esri-uk\guids\guids-{}.gdb'.format(datetime.datetime.now().strftime('%Y%m%d'))
print('\n\nfgdb:\t\t\{}'.format(fgdb))


# Create file geodatabase if it doesn't exist
if not arcpy.Exists(dataset=fgdb):
    arcpy.CreateFileGDB_management(out_folder_path=os.path.dirname(fgdb),
                                   out_name=os.path.basename(fgdb),
                                   out_version='')


# Define dictionary to hold CS ArcSDE feature classes and tables
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
data_dictionary['POINTDATA'] = {}
data_dictionary['LINEARDATA'] = {}
# Add second level dictionary item in_fc
data_dictionary['BLKDATA']['in_fc'] = os.path.join(arcsde, r'CS2007_ADMIN.ForesterData\CS2007_ADMIN.BLKDATA')
data_dictionary['SCPTDATA']['in_fc'] = os.path.join(arcsde, r'CS2007_ADMIN.ForesterData\CS2007_ADMIN.SCPTDATA')
data_dictionary['POINTDATA']['in_fc'] = os.path.join(arcsde, r'CS2007_ADMIN.ForesterData\CS2007_ADMIN.POINTDATA')
data_dictionary['LINEARDATA']['in_fc'] = os.path.join(arcsde, r'CS2007_ADMIN.ForesterData\CS2007_ADMIN.LINEARDATA')
# Add second level dictionary items out_fc and guid_field (derived from second level dictionary item in_fc)
for key in data_dictionary.keys():
    print(key)
    out_fc = os.path.join(fgdb, os.path.basename(data_dictionary[key]['in_fc']).split(arcsde_user + '.', 1)[1])
    data_dictionary[key]['out_fc'] = out_fc
    guid_field = os.path.basename(data_dictionary[key]['in_fc']).split(arcsde_user + '.', 1)[1] + '_GUID'
    data_dictionary[key]['guid_field'] = guid_field
# Display dictionary
for key in data_dictionary.keys():
    print(key)
    print('\t', data_dictionary[key])
    print('\t\t', data_dictionary[key]['in_fc'])
    print('\t\t', data_dictionary[key]['out_fc'])
    print('\t\t', data_dictionary[key]['guid_field'])


# Derive list of feature classes from dictionary
feature_class_list = list(data_dictionary.keys())
print('\n\nfeature_class_list:\t\t{}'.format(feature_class_list))


skip_copy_feature_classes = False


if not skip_copy_feature_classes:
    # Copy CS ArcSDE feature classes to file geodatabase
    print('\n\nCopying feature classes...')
    for feature_class in feature_class_list:
        print('\tin_feature_class:\t\t{}'.format(feature_class))
        desc = arcpy.Describe(value=data_dictionary[feature_class]['in_fc'])
        print('\t\tshapeType:\t\t{}'.format(desc.shapeType))
        result = arcpy.GetCount_management(in_rows=data_dictionary[feature_class]['in_fc'])
        count = int(result.getOutput(0))
        print('\t\tcount:\t\t{}'.format(count))
        print('\tout_feature_class:\t\t{}'.format(data_dictionary[feature_class]['out_fc']))
        if arcpy.Exists(dataset=data_dictionary[feature_class]['out_fc']):
            arcpy.Delete_management(in_data=data_dictionary[feature_class]['out_fc'],
                                    data_type='')
        arcpy.Copy_management(in_data=data_dictionary[feature_class]['in_fc'],
                              out_data=data_dictionary[feature_class]['out_fc'],
                              data_type='')
    print('Copied feature classes.')


sys.exit()


skip_add_guids = True


if not skip_add_guids:
    # Add GUID field to file geodatabase feature classes
    print('\n\nAdding GUID fields to feature classes...')
    for in_feature_class in [BLKDATA, SCPTDATA, POINTDATA, LINEARDATA]:
        # for in_feature_class in [BLKDATA]:
        print('\tin_feature_class:\t\t{}'.format(in_feature_class))
        out_feature_class = os.path.basename(in_feature_class).split(arcsde_user + '.', 1)[1]
        out_feature_class = os.path.join(fgdb, out_feature_class)
        print('\tout_feature_class:\t\t{}'.format(out_feature_class))

        guid_field_name = os.path.basename(in_feature_class).split(arcsde_user + '.', 1)[1] + '_GUID'
        print('\tguid_field_name:\t\t{}'.format(guid_field_name))
        field_list = arcpy.ListFields(dataset=in_feature_class,
                                      wild_card=guid_field_name,
                                      field_type='All')
        print('\tfield_list:\t\t{}'.format(field_list))
        for field in field_list:
            print('\t\t{} is a {} field'.format(field.name, field.type))
            if field.name == guid_field_name:
                print('\tDeleting existing GUID field {}...'.format(guid_field_name))
                arcpy.DeleteField_management(in_table=in_feature_class,
                                             drop_field=list(guid_field_name))
                print('\tDeleted existing GUID field {}.'.format(guid_field_name))
        print('\tAdding GUID field {}...'.format(guid_field_name))
        arcpy.AddField_management(in_table=out_feature_class,
                                  field_name=guid_field_name,
                                  field_type='GUID',
                                  field_precision='#',
                                  field_scale='#',
                                  field_length='#',
                                  field_alias='#',
                                  field_is_nullable='NON_NULLABLE',
                                  field_is_required='REQUIRED',
                                  field_domain='#')
        # arcpy.AddField_management("E:/CountrysideSurvey/esri-uk/guids/guids-20160712.gdb/SCPTDATA","SCPTDATA_GUID","GUID","#","#","#","#","NULLABLE","REQUIRED","#")
        # arcpy.AddField_management("E:/CountrysideSurvey/esri-uk/guids/guids-20160712.gdb/POINTDATA","POINTDATA_GUID","GUID","#","#","#","#","NULLABLE","REQUIRED","#")
        # arcpy.AddField_management("E:/CountrysideSurvey/esri-uk/guids/guids-20160712.gdb/LINEARDATA","LINEARDATA_GUID","GUID","#","#","#","#","NULLABLE","REQUIRED","#")
        print('\tAdded GUID field {}.'.format(guid_field_name))
        print('\tCalculating GUID field {}...'.format(guid_field_name))
        code_block = '''def GUID():
            import uuid
            return \'{\' + str(uuid.uuid4()) + \'}\''''
        arcpy.CalculateField_management(in_table=out_feature_class,
                                        field=guid_field_name,
                                        expression='GUID()',
                                        expression_type='PYTHON',
                                        code_block=code_block)
        print('\tCalculated GUID field {}.'.format(guid_field_name))
    print('Added GUID fields to feature classes.')
    skip_copy_tables = False


sys.exit()


if not skip_copy_tables:
    # Copy CS ArcSDE tables to file geodatabase
    print('\n\nCopying tables...')
    for in_table in [COMPDATA, PCOMPDATA, EVENTDATA, SEVENTDATA]:
        print('\tin_table:\t\t{}'.format(in_table))
        desc = arcpy.Describe(value=in_table)
        if desc.hasOID:
            print('\t\tOIDFieldName:\t\t{}'.format(desc.OIDFieldName))
        result = arcpy.GetCount_management(in_rows=in_table)
        count = int(result.getOutput(0))
        print('\t\tcount:\t\t{}'.format(count))
        out_table = os.path.basename(in_table).split(arcsde_user + '.', 1)[1]
        out_table = os.path.join(fgdb, out_table)
        print('\tout_table:\t\t{}'.format(out_table))
        if arcpy.Exists(dataset=out_table):
            arcpy.Delete_management(in_data=out_table,
                                    data_type='')
        arcpy.CopyRows_management(in_rows=in_table,
                                  out_table=out_table,
                                  config_keyword='')
    print('Copied tables.')
















# Capture end_time
end_time = time.time()


# Report elapsed_time (= end_time - start_time)
print('\n\nIt took {} to execute this.'.format(hms_string(end_time - start_time)))
print('\n\nDone.\n')
