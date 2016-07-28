import os
import sys


import arcpy


# Define in file geodatabase
fgdb_in = r'E:\CountrysideSurvey\esri-uk\domains\domains.gdb'
print('\n\nfgdb_in:\t\t{}'.format(fgdb_in))


# Define temporary file geodatabase
fgdb_temp = os.path.dirname(fgdb_in)
fgdb_temp = os.path.join(fgdb_temp, r'temporary_domain_tables' + r'.gdb')
print('\n\nfgdb_temp:\t\t{}'.format(fgdb_temp))


# Create temporary file geodatabase
if arcpy.Exists(fgdb_temp):
    print('\tDeleting fgdb_temp {}...'.format(fgdb_temp))
    arcpy.Delete_management(fgdb_temp)
    print('\tDeleted fgdb_temp {}.'.format(fgdb_temp))
print('\tCreating fgdb_temp {}...'.format(fgdb_temp))
arcpy.CreateFileGDB_management(out_folder_path=os.path.dirname(fgdb_temp),
                               out_name=os.path.basename(fgdb_temp),
                               out_version='CURRENT')
print('\tCreated fgdb_temp {}.'.format(fgdb_temp))


# Define out file geodatabase
fgdb_out = r'E:\CountrysideSurvey\esri-uk\guids\guids-20160727-without-nullable-fields.gdb'
print('\n\nfgdb_out:\t\t{}'.format(fgdb_out))


# Get a list of domains from the in file geodatabase
domains = arcpy.da.ListDomains(fgdb_in)


# Loop through list of domains
for domain in domains:
    # Only get CS 2007 domains
    if domain.name.startswith('CS2007_'):
        # Print out domain name and type
        print('\n\nDomain {0} is of type {1}'.format(domain.name,
                                                domain.domainType))
        #
        # Print out domain values
        if domain.domainType == 'CodedValue':
            coded_values = domain.codedValues
            for val, desc in coded_values.items():
                print('\t{0} : {1}'.format(val, desc))
        elif domain.domainType == 'Range':
            print('\tMin: {0}'.format(domain.range[0]))
            print('\tMax: {0}'.format(domain.range[1]))
        #
        # Convert domain to a table in temporary fgdb
        print('Converting domain to table in temporary file geodatabase...')
        table_out = domain.name + '_table'
        table_out = os.path.join(fgdb_temp, table_out)
        print('\ttable_out:\t\t\t\t{}'.format(table_out))
        code_field = 'Code'
        print('\tcode_field:\t\t\t\t{}'.format(code_field))
        description_field = 'Description'
        print('\tdescription_field:\t\t{}'.format(description_field))
        arcpy.DomainToTable_management(in_workspace=fgdb_in,
                                       domain_name=domain.name,
                                       out_table=table_out,
                                       code_field=code_field,
                                       description_field=description_field,
                                       configuration_keyword='')
        print('Converted domain to table in temporary file geodatabase.')
        #
        # Convert table to domain in the out file geodatabase
        print('Converting table to domain in the out file geodatabase...')
        domain_description = domain.name.replace('_', ' ') + ' domain'
        print('domain_description:\t\t{}'.format(domain_description))
        arcpy.TableToDomain_management(in_table=table_out,
                                       code_field=code_field,
                                       description_field=description_field,
                                       in_workspace=fgdb_out,
                                       domain_name=domain.name,
                                       domain_description=domain_description,
                                       update_option='REPLACE')
        print('Converted table to domain in the out file geodatabase.')
        #
        # Assign domain to field
        # arcpy.AssignDomainToField_management(in_table=,
        #                                      field_name=,
        #                                      domain_name=,
        #                                      subtype_code=)






sys.exit()


# Delete temporary file geodatabase
print('\tDeleting fgdb_temp {}...'.format(fgdb_temp))
arcpy.Delete_management(fgdb_temp)
print('\tDeleted fgdb_temp {}.'.format(fgdb_temp))

