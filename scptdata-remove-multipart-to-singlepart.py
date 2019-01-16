import os
import sys
import platform
import datetime
import time
import random
import json
import collections


import arcpy


import uuid


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
	return "{0:>02}:{1:>02}:{2:>05.2f}".format(h, m, s)


def create_dummy_guid(value):
	if not isinstance(value, str):
		value = str(value)
	return '{0}{1}{2}-{3}-{3}-{3}-{4}{5}'.format('{',
	                                          str(0) * (8 - len(value)),
	                                          value,
	                                          str(0) * 4,
	                                          str(0) * 12,
	                                          '}')


# Print Python version, version info, and platform architecture
print('\n\nsys.version:\t\t\t\t\t{0}'.format(sys.version))
print('sys.versioninfo:\t\t\t\t{0}'.format(sys.version_info))
print('platform.architecture():\t\t{0}'.format(platform.architecture()))


# Get ArcGIS installation information
print('\n\nArcGIS installation information:')
d = arcpy.GetInstallInfo()
for key, value in list(d.items()):
    # Print a formatted string of the install key and its value
    #
    print('\t{:<13}: {}'.format(key, value))


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


blkdata = 'BLKDATA'
scptdata = 'SCPTDATA'
compdata = 'COMPDATA'
relationship_class = 'SCPTDATA_COMPDATA'


scptdata_guid_field = scptdata.upper() + '_GUID'
print('\n\nscptdata_guid_field:\t{0}'.format(scptdata_guid_field))


compdata_guid_field = compdata.upper() + '_GUID'
print('\n\ncompdata_guid_field:\t{0}'.format(compdata_guid_field))


duplicate_field = 'duplicate'
print('\n\nduplicate_field:\t{0}'.format(duplicate_field))


# print('\n\nGenerating dummy guids list...')
# dummy_guid_list = [create_dummy_guid(g) for g in range(0, 101)]
# # reverse the order of the list so can use with pop()
# dummy_guid_list = dummy_guid_list[::-1]
# # for dummy_guid in dummy_guid_list:
# # 	print(dummy_guid)
# print('Generated dummy guids list.')


# print('\n\nGenerating unique guid...')
# while True:
# 	# thing1 = uuid.uuid4()
# 	# print(thing1)
# 	# print(thing1 in scptdata_singlepart_unique_guids)
# 	# if not thing1 in scptdata_singlepart_unique_guids:
# 	# 	print('breaking...')
# 	# 	break
# 	thing1 = create_dummy_guid(random.randint(0,102))
# 	print('{0}'.format(thing1))
# 	print('\t{0}'.format(thing1 in dummy_guid_list))
# 	if not thing1 in dummy_guid_list:
# 		print('\t\tbreaking...')
# 		break
# print('thing1:\t{0}'.format(thing1))
# print('thing1 in dummy_guid_list:\t{0}'.format(thing1 in dummy_guid_list))


data_workspace = r'G:\CountrysideSurvey\cs2007-wgem-combined-schema\multipart-scptdata-20190109.gdb'
print('\n\ndata_workspace:\t{0}'.format(data_workspace))


arcpy.env.workspace = data_workspace
print('\n\narcpy.env.workspace:\t{0}'.format(arcpy.env.workspace))


# print('Feature classes:')
# featureclasses = arcpy.ListFeatureClasses(wild_card='',
#                                           feature_type='All',
#                                           feature_dataset='')
# for featureclass in featureclasses:
# 	print('\t{0}'.format(featureclass))
# tables = arcpy.ListTables(wild_card='',
#                           table_type='All')
# print('Tables:')
# for table in tables:
# 	print('\t{0}'.format(table))
# print('Relationship class {0}:'.format(relationship_class))
# desc = arcpy.Describe('SCPTDATA_COMPDATA')
# print('\t{0:25}:\t{1}'.format('Origin Class Names', desc.originClassNames))
# print('\t{0:25}:\t{1}'.format('Destination Class Names', desc.destinationClassNames))
# print('\t{0:25}:\t{1}'.format('Forward Path Label', desc.forwardPathLabel))
# print('\t{0:25}:\t{1}'.format('Backward Path Label', desc.backwardPathLabel))
# print('\t{0:25}:\t{1}'.format('Notification Direction', desc.notification))
# print('\t{0:25}:\t{1}'.format('Cardinality', desc.cardinality))
# print('\t{0:25}:\t{1}'.format('Is Attributed', desc.isAttributed))
# print('\t{0:25}:\t{1}'.format('Origin Class Keys', desc.originClassKeys))
# print('\t{0:25}:\t{1}'.format('Destination Class Keys', desc.destinationClassKeys))
# print('\t{0:25}:\t{1}'.format('Class key', desc.classKey))
# print('\t{0:25}:\t{1}'.format('Is Composite', desc.isComposite))
# print('\t{0:25}:\t{1}'.format('Is Reflexive', desc.isReflexive))
# print('\t{0:25}:\t{1}'.format('Key Type', desc.keyType))
# print('\t{0:25}:\t{1}'.format('Attachment Relationship', desc.isAttachmentRelationship))


scratch_workspace = r'G:\CountrysideSurvey\cs2007-wgem-combined-schema\multipart-scptdata-scratch-{0}.gdb'.format(datetime.datetime.now().strftime('%Y%m%d'))
print('\n\nscratch_workspace:\t{0}'.format(scratch_workspace))


create_scratch_workspace = False


if create_scratch_workspace:
	if arcpy.Exists(dataset=scratch_workspace):
		print('\tDeleting scratch_workspace...')
		arcpy.Delete_management(in_data=scratch_workspace,
		                        data_type='')
		print('\tDeleted scratch_workspace.')
	print('\tCreating_scratch_workspace...')
	arcpy.CreateFileGDB_management(out_folder_path=os.path.dirname(scratch_workspace),
	                               out_name=os.path.basename(scratch_workspace),
	                               out_version='CURRENT')
	print('\tCreated scratch_workspace.')


copy_datasets = False


if copy_datasets:
	print('\n\nCopying datasets to scratch workspace...')
	# for dataset in [blkdata, scptdata, compdata, relationship_class]:
	# Note (from ArcPy tool reference): "Any data dependent on the input is also copied.  For example, copying a
	# feature class or table that is part of a relationship class also copies the relationship class."
	for dataset in [blkdata, scptdata]:
		print('\tdataset:\t{0}'.format(dataset))
		out_dataset = os.path.join(scratch_workspace, dataset)
		print('\tout_dataset:\t{0}'.format(out_dataset))
		if arcpy.Exists(dataset=out_dataset):
			print('\t\tDeleting out_dataset...')
			arcpy.Delete_management(out_dataset)
			print('\t\tDeleted out_dataset.')
		arcpy.Copy_management(in_data=dataset,
		                      out_data=out_dataset)
	print('Copied datasets to scratch workspace.')


arcpy.env.workspace = scratch_workspace
print('\n\narcpy.env.workspace:\t{0}'.format(arcpy.env.workspace))


print('Feature classes:')
featureclasses = arcpy.ListFeatureClasses(wild_card='',
                                          feature_type='All',
                                          feature_dataset='')
for featureclass in featureclasses:
	print('\t{0}'.format(featureclass))


print('Tables:')
tables = arcpy.ListTables(wild_card='',
                          table_type='All')
for table in tables:
	print('\t{0}'.format(table))



print('Relationship classes:')
for featureclass in featureclasses:
	desc = arcpy.Describe(featureclass)
	if len(desc.relationshipClassNames) > 0:
		print('\t{0}'.format(desc.relationshipClassNames))


# if arcpy.Exists(relationship_class):
# 	print('Relationship class {0}:'.format(relationship_class))
# 	desc = arcpy.Describe('SCPTDATA_COMPDATA')
# 	print('\t{0:25}:\t{1}'.format('Origin Class Names', desc.originClassNames))
# 	print('\t{0:25}:\t{1}'.format('Destination Class Names', desc.destinationClassNames))
# 	print('\t{0:25}:\t{1}'.format('Forward Path Label', desc.forwardPathLabel))
# 	print('\t{0:25}:\t{1}'.format('Backward Path Label', desc.backwardPathLabel))
# 	print('\t{0:25}:\t{1}'.format('Notification Direction', desc.notification))
# 	print('\t{0:25}:\t{1}'.format('Cardinality', desc.cardinality))
# 	print('\t{0:25}:\t{1}'.format('Is Attributed', desc.isAttributed))
# 	print('\t{0:25}:\t{1}'.format('Origin Class Keys', desc.originClassKeys))
# 	print('\t{0:25}:\t{1}'.format('Destination Class Keys', desc.destinationClassKeys))
# 	print('\t{0:25}:\t{1}'.format('Class key', desc.classKey))
# 	print('\t{0:25}:\t{1}'.format('Is Composite', desc.isComposite))
# 	print('\t{0:25}:\t{1}'.format('Is Reflexive', desc.isReflexive))
# 	print('\t{0:25}:\t{1}'.format('Key Type', desc.keyType))
# 	print('\t{0:25}:\t{1}'.format('Attachment Relationship', desc.isAttachmentRelationship))


if arcpy.Exists(dataset=relationship_class):
	print('\n\nDeleting relationship class...')
	arcpy.Delete_management(in_data=relationship_class)
	print('Deleted relationship class.')


scptdata_records = arcpy.GetCount_management(in_rows=scptdata)[0]
print('\n\nscptdata_records:\t{0}'.format(scptdata_records))


scptdata_singlepart = scptdata + '_singlepart'
# scptdata_singlepart = 'in_memory/' + scptdata + '_singlepart'
print('\n\nscptdata_singlepart:\t{0}'.format(scptdata_singlepart))
if arcpy.Exists(dataset=scptdata_singlepart):
	arcpy.Delete_management(in_data=scptdata_singlepart)
print('\n\nExploding multipart {0} to singlepart {1}...'.format(scptdata, scptdata_singlepart))
arcpy.MultipartToSinglepart_management(in_features=scptdata,
                                       out_feature_class=scptdata_singlepart)
print('Exploded multipart {0} to singlepart {1}.'.format(scptdata, scptdata_singlepart))


scptdata_singlepart_records = arcpy.GetCount_management(in_rows=scptdata_singlepart)[0]
print('\n\nscptdata_singlepart_records:\t{0}'.format(scptdata_singlepart_records))
print('additional polygons:\t{0}'.format(int(scptdata_singlepart_records) - int(scptdata_records)))


print('\n\nGenerating list of unique SCPTDATA_GUIDs from scptdata_singlepart...')
scptdata_singlepart_unique_guids = set(row[0] for row in arcpy.da.SearchCursor(in_table=scptdata_singlepart,
                                                                               field_names=scptdata_guid_field))
print(scptdata_singlepart_unique_guids)
print(len(scptdata_singlepart_unique_guids))
print('Generated list of unique SCPTDATA_GUIDs from scptdata_singlepart.')


compdata_records = arcpy.GetCount_management(in_rows=compdata)[0]
print('\n\ncompdata_records:\t{0}'.format(compdata_records))


compdata_singlepart = compdata + '_singlepart'
# compdata_singlepart = 'in_memory/' + compdata + '_singlepart'
print('\n\ncompdata_singlepart:\t{0}'.format(compdata_singlepart))
if arcpy.Exists(compdata_singlepart):
	arcpy.Delete_management(in_data=compdata_singlepart)
print('\n\nCopying compdata table to compdata_singlepart table...')
arcpy.Copy_management(in_data=compdata,
                      out_data=compdata_singlepart)
print('Copied compdata table to compdata_singlepart table.')


compdata_singlepart_records = arcpy.GetCount_management(in_rows=compdata_singlepart)[0]
print('\n\ncompdata_singlepart_records:\t{0}'.format(compdata_singlepart_records))
print('additional rows:\t{0}'.format(int(compdata_singlepart_records) - int(compdata_records)))


print('\n\nGenerating list of unique COMPDATA_GUIDs from compdata_singlepart...')
compdata_singlepart_unique_guids = set(row[0] for row in arcpy.da.SearchCursor(in_table=compdata_singlepart,
                                                                               field_names='COMPDATA_GUID'))
print(compdata_singlepart_unique_guids)
print(len(compdata_singlepart_unique_guids))
print('Generated list of unique COMPDATA_GUIDs from compdata_singlepart.')


print('\n\nAdding duplicate field to scptdata_singlepart...')
arcpy.AddField_management(in_table=scptdata_singlepart,
                          field_name=duplicate_field,
                          field_type='SHORT',
                          field_precision='',
                          field_scale='',
                          field_length='',
                          field_alias='',
                          field_is_nullable='NULLABLE',
                          field_is_required='NON_REQUIRED',
                          field_domain='')
print('Added duplicate field to scptdata_singlepart.')


print('\n\nCalculating duplicate field in scptdata_singlepart...')
expression = 'is_duplicate(!{0}!)'.format(scptdata_guid_field)
print('\texpression:\n\t\t{0}'.format(expression))
code_block = '''unique_list = []
def is_duplicate(in_value):
	unique_list.append(in_value)
	return unique_list.count(in_value)
'''
print('\tcode_block:\n\t\t{0}'.format(code_block.replace('\n', '\n\t\t')))
arcpy.CalculateField_management(in_table=scptdata_singlepart,
                                field=duplicate_field,
                                expression=expression,
                                expression_type='PYTHON',
                                code_block=code_block)
print('Calculated duplicate field in scptdata_singlepart.')


print('\n\nLooping to get GUIDs of multipart polygons...')
multipart_guids_list = []
where_clause = '{0} > 1'.format(arcpy.AddFieldDelimiters(datasource=scptdata_singlepart,
                                                         field=duplicate_field))
print('\twhere_clause:\t{0}'.format(where_clause))
sql_clause = (None, 'ORDER BY {0}, {1}'.format(scptdata_guid_field,
                                               duplicate_field))
print('\tsql_clause:\t{0}'.format(sql_clause))
count = 0
with arcpy.da.SearchCursor(in_table=scptdata_singlepart,
                           field_names=['OBJECTID', 'ORIG_FID', scptdata_guid_field, duplicate_field],
                           where_clause=where_clause,
                           spatial_reference='',
                           explode_to_points='',
                           sql_clause=sql_clause) as cursor:
	print('\t{0:<12}\t{1:>12}\t{2:>12}\t{3:>36}\t{4:>12}'.format('COUNT',
	                                                             'OBJECTID',
	                                                             'ORIG_FID',
	                                                             scptdata_guid_field,
	                                                             duplicate_field))
	for row in cursor:
		print('\t{0:<12}\t{1:>12}\t{2:>12}\t{3:>36}\t{4:>12}'.format(count,
		                                                             row[0],
		                                                             row[1],
		                                                             row[2],
		                                                             row[3]))
		count += 1
		multipart_guids_list.append(row[2])
print('Looped to get GUIDs of multipart polygons.')
print(multipart_guids_list)
print(len(multipart_guids_list))
unique_multipart_guids_list = list(set(multipart_guids_list))
print(unique_multipart_guids_list)
print(len(unique_multipart_guids_list))


scptdata_singlepart_fields = [f.name for f in arcpy.ListFields(dataset=scptdata_singlepart,
                                                               wild_card=None,
                                                               field_type='All')]
print('\n\nscptdata_singlepart_fields:\t{0}'.format(scptdata_singlepart_fields))


scptdata_singlepart_guid_field_index = scptdata_singlepart_fields.index(scptdata_guid_field)
print('scptdata_singlepart_guid_field_index:\t{0}'.format(scptdata_singlepart_guid_field_index))
scptdata_singlepart_duplicate_field_index = scptdata_singlepart_fields.index(duplicate_field)
print('scptdata_singlepart_duplicate_field_index:\t{0}'.format(scptdata_singlepart_duplicate_field_index))


compdata_singlepart_fields = [f.name for f in arcpy.ListFields(dataset=compdata_singlepart,
                                                               wild_card=None,
                                                               field_type='All')]
print('\n\ncompdata_singlepart_fields:\t{0}'.format(compdata_singlepart_fields))


compdata_singlepart_guid_field_index = compdata_singlepart_fields.index(compdata_guid_field)
print('compdata_singlepart_guid_field_index:\t{0}'.format(compdata_singlepart_guid_field_index))


print('\n\nLooping...')
multipart_guid_count = 1
for multipart_guid in unique_multipart_guids_list:
# for multipart_guid in unique_multipart_guids_list[:3]:
	print('\tmultipart_guid [{0} of {1}]:\t{2}'.format(multipart_guid_count,
	                                                       len(unique_multipart_guids_list),
	                                                       multipart_guid))
	#
	print('\t\tDoing scptdata_singlepart UpdateCursor...')
	scptdata_singlepart_updatecursor_where_clause = '{0} = \'{1}\''.format(arcpy.AddFieldDelimiters(datasource=scptdata_singlepart,
	                                                                                                field=scptdata_guid_field),
	                                                                       multipart_guid)
	print('\t\t\tscptdata_singlepart_updatecursor_where_clause:\t{0}'.format(scptdata_singlepart_updatecursor_where_clause))
	with arcpy.da.UpdateCursor(in_table=scptdata_singlepart,
	                           field_names='*',
	                           where_clause=scptdata_singlepart_updatecursor_where_clause,
	                           spatial_reference=None,
	                           explode_to_points=False,
	                           sql_clause=(None, None)) as scptdata_singlepart_updatecursor:
		for scptdata_singlepart_row in scptdata_singlepart_updatecursor:
			print('\t\t\t\t{0}'.format(',\t'.join(scptdata_singlepart_fields)))
			print('\t\t\t\t{0}'.format(',\t'.join(map(str, scptdata_singlepart_row))))
			#
			duplicate = scptdata_singlepart_row[scptdata_singlepart_duplicate_field_index]
			print('\t\t\t\tduplicate:\t{0}'.format(duplicate))
			#
			if duplicate > 1:
				#
				while True:
					new_guid = '{0}{1}{2}'.format('{',
					                              str(uuid.uuid4()).upper(),  #  Convert GUID to str and then ensure alphabetic characters are UPPER-CASE!  See:  https://community.esri.com/thread/210223-guid-feature-type-uppercase-by-default-on-fgdb
					                              '}')
					if not new_guid in scptdata_singlepart_unique_guids:
						scptdata_singlepart_unique_guids.add(new_guid)
						break
				print('\t\t\t\t\tnew_guid:\t{0}'.format(new_guid))
				#
				scptdata_singlepart_row[scptdata_singlepart_guid_field_index] = new_guid
				scptdata_singlepart_updatecursor.updateRow(scptdata_singlepart_row)
				print('\t\t\t\t\t{0}'.format(',\t'.join(scptdata_singlepart_fields)))
				print('\t\t\t\t\t{0}'.format(',\t'.join(map(str, scptdata_singlepart_row))))
				#
				compdata_singlepart_tableview = compdata_singlepart + '_tableview'
				print('\t\t\t\t\t\tcompdata_singlepart_tableview:\t{0}'.format(compdata_singlepart_tableview))
				compdata_singlepart_tableview_where_clause = '{0} = \'{1}\''.format(arcpy.AddFieldDelimiters(datasource=compdata_singlepart,
				                                                                                             field=scptdata_guid_field),
				                                                                    multipart_guid)
				print('\t\t\t\t\t\tcompdata_singlepart_tableview_where_clause:\t{0}'.format(compdata_singlepart_tableview_where_clause))
				print('\t\t\t\t\t\tCreating compdata_singlepart_tableview...')
				if arcpy.Exists(compdata_singlepart_tableview):
					arcpy.Delete_management(in_data=compdata_singlepart_tableview)
				arcpy.MakeTableView_management(in_table=compdata_singlepart,
				                               out_view=compdata_singlepart_tableview,
				                               where_clause=compdata_singlepart_tableview_where_clause,
				                               workspace='',
				                               field_info='')
				print('\t\t\t\t\t\tCreated compdata_singlepart_tableview.')
				print('\t\t\t\t\t\tCopying compdata_singlepart_tableview to temporary table...')
				compdata_singlepart_tableview_temp_table = 'in_memory/temp_table_{0}'.format(multipart_guid.replace('{', '').replace('}', '').replace('-', '_'))
				print('\t\t\t\t\t\tcompdata_singlepart_tableview_temp_table:\t{0}'.format(compdata_singlepart_tableview_temp_table))
				if arcpy.Exists(compdata_singlepart_tableview_temp_table):
					arcpy.Delete_management(in_data=compdata_singlepart_tableview_temp_table)
				arcpy.CopyRows_management(in_rows=compdata_singlepart_tableview,
				                          out_table= compdata_singlepart_tableview_temp_table,
				                          config_keyword='')
				print('\t\t\t\t\t\tCopied compdata_singlepart_tableview to temporary table.')
				#
				with arcpy.da.SearchCursor(in_table=compdata_singlepart_tableview_temp_table,
				                           field_names='*',
				                           where_clause=None,
				                           spatial_reference=None,
				                           explode_to_points=False,
				                           sql_clause=(None, None)) as temp_cursor:
					print('\t\t\t\t\t\t{0}'.format(',\t'.join(compdata_singlepart_fields)))
					for temp_row in temp_cursor:
						print('\t\t\t\t\t\t{0}'.format(temp_row))
				#
				print('\t\t\t\t\t\tUpdating guid in compdata_singlepart_tableview_temp_table...')
				compdata_singlepart_tableview_temp_table_expression = '\'{1}\''.format(scptdata_guid_field,
				                                                                       new_guid)
				print('\t\t\t\t\t\tcompdata_singlepart_tableview_temp_table_expression:\t{0}'.format(compdata_singlepart_tableview_temp_table_expression))
				arcpy.CalculateField_management(in_table=compdata_singlepart_tableview_temp_table,
				                                field=scptdata_guid_field,
				                                expression=compdata_singlepart_tableview_temp_table_expression,
				                                expression_type='PYTHON',
				                                code_block=None)
				print('\t\t\t\t\t\tUpdated guid in compdata_singlepart_tableview_temp_table.')
				#
				print('\t\t\t\t\t\tDoing compdata_singlepart UpdateCursor...')
				with arcpy.da.UpdateCursor(in_table=compdata_singlepart_tableview_temp_table,
				                           field_names='*',
				                           where_clause=None,
				                           spatial_reference=None,
				                           explode_to_points=False,
				                           sql_clause=(None, None)) as compdata_singlepart_updatecursor:
					for compdata_singlepart_row in compdata_singlepart_updatecursor:
						print('\t\t\t\t\t\t\t{0}'.format(',\t'.join(compdata_singlepart_fields)))
						print('\t\t\t\t\t\t\t{0}'.format(',\t'.join(map(str, compdata_singlepart_row))))

						while True:
							new_compdata_guid = '{0}{1}{2}'.format('{',
							                                       str(uuid.uuid4()).upper(),  #  Convert GUID to str and then ensure alphabetic characters are UPPER-CASE!  See:  https://community.esri.com/thread/210223-guid-feature-type-uppercase-by-default-on-fgdb
																   '}')
							if not new_compdata_guid in compdata_singlepart_unique_guids:
								compdata_singlepart_unique_guids.add(new_compdata_guid)
								break
						print('\t\t\t\t\t\t\tnew_compdata_guid:\t{0}'.format(new_compdata_guid))

						compdata_singlepart_row[compdata_singlepart_guid_field_index] = new_compdata_guid
						compdata_singlepart_updatecursor.updateRow(compdata_singlepart_row)
						print('\t\t\t\t\t\t\t{0}'.format(',\t'.join(compdata_singlepart_fields)))
						print('\t\t\t\t\t\t\t{0}'.format(',\t'.join(map(str, compdata_singlepart_row))))
				print('\t\t\t\t\t\tDone compdata_singlepart UpdateCursor.')
				#
				print('\t\t\t\t\t\tAppending compdata_singlepart_tableview_temp_table to compdata_singlepart...')
				before_count = arcpy.GetCount_management(in_rows=compdata_singlepart)[0]
				print('\t\t\t\t\t\t\tbefore_count:\t{0}'.format(before_count))
				arcpy.Append_management(inputs=[compdata_singlepart_tableview_temp_table],
				                        target=compdata_singlepart,
				                        schema_type='TEST',
				                        field_mapping=None,
				                        subtype=None,
				                        expression=''
										)
				after_count = arcpy.GetCount_management(in_rows=compdata_singlepart)[0]
				print('\t\t\t\t\t\t\tafter_count:\t{0}'.format(after_count))
				print('\t\t\t\t\t\tAppended compdata_singlepart_tableview_temp_table to compdata_singlepart.')
				#
				print('\t\t\t\t\t\tDeleting compdata_singlepart_tableview_temp_table...')
				arcpy.Delete_management(in_data=compdata_singlepart_tableview_temp_table)
				print('\t\t\t\t\t\tDeleted compdata_singlepart_tableview_temp_table.')
				#
				print('\t\t\t\t\t\tDeleting compdata_singlepart_tableview...')
				arcpy.Delete_management(in_data=compdata_singlepart_tableview)
				print('\t\t\t\t\t\tDeleted compdata_singlepart_tableview.')
	#
	print('\t\tDone scptdata_singlepart UpdateCursor.')
	#
	multipart_guid_count += 1
	#
print('Looped.')


relationship_class_origin_table = scptdata
relationship_class_destination_table = compdata
relationship_class_out_relationship_class = '{0}_{1}'.format(scptdata,
                                                             compdata)
print('\n\nCreating relationship class {0}...'.format(relationship_class_out_relationship_class))
relationship_class_relationship_type = 'COMPOSITE'
relationship_class_forward_label = scptdata
relationship_class_backward_label = compdata
relationship_class_message_direction = 'FORWARD'
relationship_class_cardinality = 'ONE_TO_MANY'
relationship_class_attributed = 'NONE'
relationship_class_origin_primary_key = scptdata_guid_field
relationship_class_origin_foreign_key = scptdata_guid_field
relationship_class_destination_primary_key = ''
relationship_class_destination_foreign_key = ''
arcpy.CreateRelationshipClass_management(origin_table=relationship_class_origin_table,
                                         destination_table=relationship_class_destination_table,
                                         out_relationship_class=relationship_class_out_relationship_class,
                                         relationship_type=relationship_class_relationship_type,
                                         forward_label=relationship_class_forward_label,
                                         backward_label=relationship_class_backward_label,
                                         message_direction=relationship_class_message_direction,
                                         cardinality=relationship_class_cardinality,
                                         attributed=relationship_class_attributed,
                                         origin_primary_key=relationship_class_origin_primary_key,
                                         origin_foreign_key=relationship_class_origin_foreign_key,
                                         destination_primary_key=relationship_class_destination_primary_key,
                                         destination_foreign_key=relationship_class_destination_foreign_key)
print('Created relationship class {0}.'.format(relationship_class_out_relationship_class))


relationship_class_origin_table = scptdata_singlepart
relationship_class_destination_table = compdata_singlepart
relationship_class_out_relationship_class = '{0}_{1}'.format(scptdata_singlepart,
                                                             compdata_singlepart)
print('\n\nCreating relationship class {0}...'.format(relationship_class_out_relationship_class))
relationship_class_relationship_type = 'COMPOSITE'
relationship_class_forward_label = scptdata_singlepart
relationship_class_backward_label = compdata_singlepart
relationship_class_message_direction = 'FORWARD'
relationship_class_cardinality = 'ONE_TO_MANY'
relationship_class_attributed = 'NONE'
relationship_class_origin_primary_key = scptdata_guid_field
relationship_class_origin_foreign_key = scptdata_guid_field
relationship_class_destination_primary_key = ''
relationship_class_destination_foreign_key = ''
arcpy.CreateRelationshipClass_management(origin_table=relationship_class_origin_table,
                                         destination_table=relationship_class_destination_table,
                                         out_relationship_class=relationship_class_out_relationship_class,
                                         relationship_type=relationship_class_relationship_type,
                                         forward_label=relationship_class_forward_label,
                                         backward_label=relationship_class_backward_label,
                                         message_direction=relationship_class_message_direction,
                                         cardinality=relationship_class_cardinality,
                                         attributed=relationship_class_attributed,
                                         origin_primary_key=relationship_class_origin_primary_key,
                                         origin_foreign_key=relationship_class_origin_foreign_key,
                                         destination_primary_key=relationship_class_destination_primary_key,
                                         destination_foreign_key=relationship_class_destination_foreign_key)
print('Created relationship class {0}.'.format(relationship_class_out_relationship_class))


print('\n\nFeature classes:')
featureclasses = arcpy.ListFeatureClasses(wild_card='',
                                          feature_type='All',
                                          feature_dataset='')
for featureclass in featureclasses:
	print('\t{0}'.format(featureclass))


print('Tables:')
tables = arcpy.ListTables(wild_card='',
                          table_type='All')
for table in tables:
	print('\t{0}'.format(table))


print('Relationship classes:')
for featureclass in featureclasses:
	desc = arcpy.Describe(featureclass)
	if len(desc.relationshipClassNames) > 0:
		print('\t{0}'.format(desc.relationshipClassNames))


# Capture end_time
end_time = time.time()
# Report elapsed_time (= end_time - start_time)
print('\n\nIt took {0} to execute this.'.format(hms_string(end_time - start_time)))
# Print script filename, finish date and time
print('\n\nFinished {0} at {1} on {2}.\n'.format(script,
												 datetime.datetime.now().strftime('%H:%M:%S'),
												 datetime.datetime.now().strftime('%Y-%m-%d')))
