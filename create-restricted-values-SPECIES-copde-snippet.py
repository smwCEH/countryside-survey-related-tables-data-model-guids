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


print('\n\nCreating Sweet Mapping Arcade code snippet...')


fecodes_table = arcsde + '\\' + arcsde_user + '.' + 'FECODES'
# print('\t#\n\tfecodes_table:\t\t{}'.format(fecodes_table))


fecodes_dependent_table = arcsde + '\\' + arcsde_user + '.' + 'FECODES_DEPENDENT'
# print('\t#\n\tfecodes_dependent_table:\t\t{}'.format(fecodes_dependent_table))


code_snippet_file = 'restricted-values-SPECIES.txt'
code_snippet_file = os.path.join(r'E:\CountrysideSurvey\esri-uk\sweet-mapping\sweet-config-20160817', code_snippet_file)
print('\n\ncode_snippet_file:\t\t{0}'.format(code_snippet_file))
file = open(code_snippet_file, 'w')


snippet_string = 'if (IsEmpty($VALUE)) {\n\treturn true;\n}\n\n'
print('{0}'.format(snippet_string))
file.write(snippet_string)


outer_search_cursor_fields = ['COLUMN_NAME', 'CODE', 'DESCRIPTION']
# print('\t#\n\touter_search_cursor_fields:\t\t{}'.format(outer_search_cursor_fields))
outer_search_cursor_where_clause = '{0} = {1} AND {2} IS NOT NULL'.format(arcpy.AddFieldDelimiters(fecodes_table, 'COLUMN_NAME'),
                                                                          '\'VEGETATION_TYPE\'',
                                                                          arcpy.AddFieldDelimiters(fecodes_table, 'CODE'))
# print('\touter_search_cursor_where_clause:\t\t{}'.format(outer_search_cursor_where_clause))
total_species_count = 0
with arcpy.da.SearchCursor(in_table=fecodes_table,
                           field_names=outer_search_cursor_fields,
                           where_clause=outer_search_cursor_where_clause) as outer_search_cursor:
    for outer_search_cursor_row in outer_search_cursor:
        # print('\t\t{0}\t\t{1}\t\t{2}'.format(outer_search_cursor_row[0],
        #                                      outer_search_cursor_row[1],
        #                                      outer_search_cursor_row[2]))
        inner_search_cursor_fields = ['COLUMN_NAME', 'CODE', 'DEPENDENT_ON_COLUMN_NAME', 'DEPENDENT_ON_CODE']
        # print('\t\tinner_search_cursor_fields:\t\t{}'.format(inner_search_cursor_fields))
        inner_search_cursor_where_clause = '{0} = {1}'.format(arcpy.AddFieldDelimiters(fecodes_table, 'DEPENDENT_ON_CODE'),
                                                              '\'{0}\''.format(outer_search_cursor_row[1]))
        # print('\t\tinner_search_cursor_where_clause:\t\t{}'.format(inner_search_cursor_where_clause))
        with arcpy.da.SearchCursor(in_table=fecodes_dependent_table,
                                   field_names=inner_search_cursor_fields,
                                   where_clause=inner_search_cursor_where_clause) as inner_search_cursor:
            species_count = 0
            for inner_search_cursor_row in inner_search_cursor:
                species_count += 1
                # print('\t\t\t{0}\t\t{1}\t\t{2}\t\t{3}'.format(inner_search_cursor_row[0],
                #                                               inner_search_cursor_row[1],
                #                                               inner_search_cursor_row[2],
                #                                               inner_search_cursor_row[3]))
                if total_species_count == 0:
                    snippet_string = 'if ($Feature.VEGETATION_TYPE == \'{0}\') {1}\n\treturn DECODE($VALUE, \'{2}\', TRUE'.format(outer_search_cursor_row[1],
                                                                                                                                 '{',
                                                                                                                                 str(inner_search_cursor_row[1]))
                if species_count == 1:
                    snippet_string = 'else if ($Feature.VEGETATION_TYPE == \'{0}\') {1}\n\treturn DECODE($VALUE, \'{2}\', TRUE'.format(outer_search_cursor_row[1],
                                                                                                                                      '{',
                                                                                                                                      str(inner_search_cursor_row[1]))
                else:
                    snippet_string += ', \'' + str(inner_search_cursor_row[1]) + '\', TRUE'
            snippet_string += ', FALSE);\n{}\n'.format('}')
            # print('\t\tspecies_count:\t\t{}'.format(species_count))
            total_species_count += species_count
            del species_count
            # print('\t\tsnippet_string:\t\t{}'.format(snippet_string))
            print('{0}'.format(snippet_string))
            file.write(snippet_string)



    del inner_search_cursor_row, inner_search_cursor, inner_search_cursor_where_clause, inner_search_cursor_fields
del outer_search_cursor_row, outer_search_cursor, outer_search_cursor_where_clause, outer_search_cursor_fields
# print('\t#\n\ttotal_species_count:\t\t{}'.format(total_species_count))
del total_species_count


snippet_string = 'else {0}\n\treturn true;\n{1}\n'.format('{', '}')
print('{0}'.format(snippet_string))
file.write(snippet_string)


file.close()


print('\n\nCreated Sweet Mapping Arcade code snippet.')


# Capture end_time
end_time = time.time()


# Report elapsed_time (= end_time - start_time)
print('\n\nIt took {} to execute this.'.format(hms_string(end_time - start_time)))


# Print script filename, finish date and time
print('\n\nFinished {0} at {1} on {2}.\n'.format(script,
                                                 datetime.datetime.now().strftime('%H:%M:%S'),
                                                 datetime.datetime.now().strftime('%Y-%m-%d')))
