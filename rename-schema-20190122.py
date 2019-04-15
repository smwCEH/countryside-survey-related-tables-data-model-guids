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
	return "{0}:{1:>02}:{2:>05.2f}".format(h,
										   m,
										   s)


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


# combined_fgdb = r'G:\CountrysideSurvey\cs2007-wgem-combined-schema\combined-schema-20181127.gdb'
# combined_fgdb = r'G:\CountrysideSurvey\cs2007-wgem-combined-schema\combined-schema-20181129.gdb'
combined_fgdb = r'G:\CountrysideSurvey\cs2007-wgem-combined-schema\combined-schema-20181129-copy-converted-to-singlepart-20190117.gdb'


# renamed_fgdb = r'G:\CountrysideSurvey\cs2007-wgem-combined-schema\combined-schema-20181127-renamed.gdb'
# renamed_fgdb = r'G:\CountrysideSurvey\cs2007-wgem-combined-schema\combined-schema-20181129-renamed.gdb'
renamed_fgdb = r'G:\CountrysideSurvey\cs2007-wgem-combined-schema\combined-schema-20190121-renamed.gdb'


old_blocks = os.path.join(renamed_fgdb, 'BLKDATA')
new_blocks = os.path.join(renamed_fgdb, 'SURVEYSQUARES')
old_blocks_guid = 'BLKDATA_GUID'
new_blocks_guid = 'SURVEYSQUARES_GUID'


old_areas = os.path.join(renamed_fgdb, 'SCPTDATA_singlepart')
new_areas = os.path.join(renamed_fgdb, 'AREAS')
old_areas_guid = 'SCPTDATA_GUID'
new_areas_guid = 'AREAS_GUID'
old_areas_data = os.path.join(renamed_fgdb, 'COMPDATA_singlepart')
new_areas_data = os.path.join(renamed_fgdb, 'AREASDATA')
old_areas_data_guid = 'COMPDATA_GUID'
new_areas_data_guid = 'AREASDATA_GUID'


old_linears = os.path.join(renamed_fgdb, 'LINEARDATA')
new_linears = os.path.join(renamed_fgdb, 'LINEARS')
old_linears_guid = 'LINEARDATA_GUID'
new_linears_guid = 'LINEARS_GUID'
old_linears_data = os.path.join(renamed_fgdb, 'EVENTDATA')
new_linears_data = os.path.join(renamed_fgdb, 'EVENTSDATA')
old_linears_data_guid = 'EVENTDATA_GUID'
new_linears_data_guid = 'EVENTSDATA_GUID'
old_linears_species_data = os.path.join(renamed_fgdb, 'SEVENTDATA')
new_linears_species_data = os.path.join(renamed_fgdb, 'SEVENTSDATA')
old_linears_species_data_guid = 'SEVENTDATA_GUID'
new_linears_species_data_guid = 'SEVENTSDATA_GUID'


old_points = os.path.join(renamed_fgdb, 'POINTDATA')
new_points = os.path.join(renamed_fgdb, 'POINTS')
old_points_data = os.path.join(renamed_fgdb, 'PCOMPDATA')
new_points_data = os.path.join(renamed_fgdb, 'POINTSDATA')
old_points_guid = 'POINTDATA_GUID'
new_points_guid = 'POINTS_GUID'
old_points_data = os.path.join(renamed_fgdb, 'PCOMPDATA')
new_points_data = os.path.join(renamed_fgdb, 'POINTSDATA')
old_points_data_guid = 'PCOMPDATA_GUID'
new_points_data_guid = 'POINTSDATA_GUID'


do_fgdb = True
do_blocks = True
do_areas = True
do_linears = True
do_points = True


#  File GDB
if do_fgdb:
	print('\n\nCopying combined_fgdb to renamed_fgdb...')
	if arcpy.Exists(dataset=renamed_fgdb):
		print('\tDeleting exising renamed_fgdb...')
		arcpy.Delete_management(in_data=renamed_fgdb)
	arcpy.Copy_management(in_data= combined_fgdb,
						  out_data=renamed_fgdb)


#  Survey Squares
if do_blocks:
	print('\n\nRenaming {0} to {1}...'.format(os.path.basename(old_blocks),
											  os.path.basename(new_blocks)))
	arcpy.Rename_management(in_data=old_blocks,
							out_data=new_blocks)
	print('\tRenaming {0} to {1}...'.format(old_blocks_guid,
										  new_blocks_guid))
	# arcpy.AlterField_management(in_table=new_blocks,
	#                             field=old_blocks_guid,
	#                             new_field_name=new_blocks_guid,
	#                             new_field_alias=new_blocks_guid)
	print('\t\tAdding {0} field...'.format(new_blocks_guid))
	arcpy.AddField_management(in_table=new_blocks,
							  field_name=new_blocks_guid,
							  field_type='GUID',
							  field_is_nullable='NULLABLE',
							  field_is_required='REQUIRED')
	print('\t\tCalculating {0} field...'.format(new_blocks_guid))
	arcpy.CalculateField_management(in_table=new_blocks,
									field=new_blocks_guid,
									expression='!{0}!'.format(old_blocks_guid),
									expression_type='PYTHON3')
	print('\t\tDeleting {0} field...'.format(old_blocks_guid))
	arcpy.DeleteField_management(in_table=new_blocks,
								 drop_field=old_blocks_guid)


#  Areas
if do_areas:
	print('\n\nDeleting {0}_{1} relationship class...'.format(os.path.basename(old_areas),
															  os.path.basename(old_areas_data)))
	relationship_class = os.path.join(renamed_fgdb, '{0}_{1}'.format(os.path.basename(old_areas),
																				os.path.basename(old_areas_data)))
	if not arcpy.Exists(relationship_class):
		sys.exit('relationship_class {0} doesn\'t exist!!!'.format(relationship_class))
	else:
		arcpy.Delete_management(in_data=relationship_class)
	del relationship_class
	print('Renaming {0} to {1}...'.format(os.path.basename(old_areas),
										  os.path.basename(new_areas)))
	arcpy.Rename_management(in_data=old_areas,
							out_data=new_areas)
	print('\tRenaming {0} to {1}...'.format(old_areas_guid,
										  new_areas_guid))
	# arcpy.AlterField_management(in_table=new_areas,
	#                             field=old_areas_guid,
	#                             new_field_name=new_areas_guid,
	#                             new_field_alias=new_areas_guid)
	print('\t\tAdding {0} field...'.format(new_areas_guid))
	arcpy.AddField_management(in_table=new_areas,
							  field_name=new_areas_guid,
							  field_type='GUID',
							  field_is_nullable='NULLABLE',
							  field_is_required='REQUIRED')
	print('\t\tCalculating {0} field...'.format(new_areas_guid))
	arcpy.CalculateField_management(in_table=new_areas,
									field=new_areas_guid,
									expression='!{0}!'.format(old_areas_guid),
									expression_type='PYTHON3')
	print('\t\tDeleting {0} field...'.format(old_areas_guid))
	arcpy.DeleteField_management(in_table=new_areas,
								 drop_field=old_areas_guid)
	print('Renaming {0} to {1}...'.format(os.path.basename(old_areas_data),
										  os.path.basename(new_areas_data)))
	arcpy.Rename_management(in_data=old_areas_data,
							out_data=new_areas_data)
	print('\tRenaming {0} to {1}...'.format(old_areas_guid,
										  new_areas_guid))
	# arcpy.AlterField_management(in_table=new_areas_data,
	#                             field=old_areas_guid,
	#                             new_field_name=new_areas_guid,
	#                             new_field_alias=new_areas_guid)
	print('\t\tAdding {0} field...'.format(new_areas_guid))
	arcpy.AddField_management(in_table=new_areas_data,
							  field_name=new_areas_guid,
							  field_type='GUID',
							  field_is_nullable='NULLABLE',
							  field_is_required='REQUIRED')
	print('\t\tCalculating {0} field...'.format(new_areas_guid))
	arcpy.CalculateField_management(in_table=new_areas_data,
									field=new_areas_guid,
									expression='!{0}!'.format(old_areas_guid),
									expression_type='PYTHON3')
	print('\t\tDeleting {0} field...'.format(old_areas_guid))
	arcpy.DeleteField_management(in_table=new_areas_data,
								 drop_field=old_areas_guid)
	print('\tRenaming {0} to {1}...'.format(old_areas_data_guid,
										  new_areas_data_guid))
	# arcpy.AlterField_management(in_table=new_areas_data,
	#                             field=old_areas_data_guid,
	#                             new_field_name=new_areas_data_guid,
	#                             new_field_alias=new_areas_data_guid)
	print('\t\tAdding {0} field...'.format(new_areas_data_guid))
	arcpy.AddField_management(in_table=new_areas_data,
							  field_name=new_areas_data_guid,
							  field_type='GUID',
							  field_is_nullable='NULLABLE',
							  field_is_required='REQUIRED')
	print('\t\tCalculating {0} field...'.format(new_areas_data_guid))
	arcpy.CalculateField_management(in_table=new_areas_data,
									field=new_areas_data_guid,
									expression='!{0}!'.format(old_areas_data_guid),
									expression_type='PYTHON3')
	print('\t\tDeleting {0} field...'.format(old_areas_data_guid))
	arcpy.DeleteField_management(in_table=new_areas_data,
								 drop_field=old_areas_data_guid)
	print('\tAdding new fields to {0}...'.format(os.path.basename(new_areas_data)))
	new_fields = {}
	new_fields['MOSAIC_AREA'] = {'field_type': 'SHORT',
	                             'field_alias': 'Mosaic Area',
	                             'field_is_nullable': 'NULLABLE',
	                             'field_is_required': 'NON_REQUIRED'}
	new_fields['AREAS_BROAD_HABITAT'] = {'field_type': 'SHORT',
	                                     'field_alias': 'Area Broad Habitat',
	                                     'field_is_nullable': 'NULLABLE',
	                                     'field_is_required': 'NON_REQUIRED'}
	new_fields['MOSAIC_BROAD_HABITAT'] = {'field_type': 'SHORT',
	                                      'field_alias': 'Mosaic Broad Habitat',
	                                      'field_is_nullable': 'NULLABLE',
	                                      'field_is_required': 'NON_REQUIRED'}
	for field in ['MOSAIC_AREA', 'AREAS_BROAD_HABITAT', 'MOSAIC_BROAD_HABITAT']:
		print('\t\tAdding {0} field...'.format(field))
		try:
			arcpy.AddField_management(in_table=new_areas_data,
			                          field_name=field,
			                          field_type=new_fields[field]['field_type'],
			                          field_alias=new_fields[field]['field_alias'],
			                          field_is_nullable=new_fields[field]['field_is_nullable'],
			                          field_is_required = new_fields[field]['field_is_required'])
		except:
			sys.exit('Failed to add field {0} to table {1}!!!'.format(field,
			                                                          os.path.basename(new_areas_data)))
		domain = 'BROAD_HABITAT'
		if field in ['AREAS_BROAD_HABITAT', 'MOSAIC_BROAD_HABITAT']:
			print('\t\t\tAdding {0} domain to field {1}...'.format(domain, field))
			try:
				arcpy.AssignDomainToField_management(in_table=new_areas_data,
				                                     field_name=field,
				                                     domain_name=domain)
			except:
				sys.exit('Failed to add domain {0} to field {1}!!!'.format(domain,
				                                                           field))
		del domain
	print('Creating {0}_{1} relationship class...'.format(os.path.basename(new_areas),
	                                                      os.path.basename(new_areas_data)))
	arcpy.CreateRelationshipClass_management(origin_table=new_areas,
											 destination_table=new_areas_data,
											 out_relationship_class=os.path.join(renamed_fgdb, '{0}_{1}'.format(os.path.basename(new_areas),
																												os.path.basename(new_areas_data))),
											 relationship_type='COMPOSITE',
											 forward_label=os.path.basename(new_areas),
											 backward_label=os.path.basename(new_areas_data),
											 message_direction='FORWARD',
											 cardinality='ONE_TO_MANY',
											 attributed='NONE',
											 origin_primary_key=new_areas_guid,
											 origin_foreign_key=new_areas_guid,
											 destination_primary_key='',
											 destination_foreign_key='')


#  Linears
if do_linears:
	print('\n\nDeleting {0}_{1} relationship class...'.format(os.path.basename(old_linears_data),
	                                                          os.path.basename(old_linears_species_data)))
	relationship_class = os.path.join(renamed_fgdb, '{0}_{1}'.format(os.path.basename(old_linears_data),
	                                                                 os.path.basename(old_linears_species_data)))
	if not arcpy.Exists(relationship_class):
		sys.exit('relationship_class {0} doesn\'t exist!!!'.format(relationship_class))
	else:
		arcpy.Delete_management(in_data=relationship_class)
	del relationship_class
	print('Deleting {0}_{1} relationship class...'.format(os.path.basename(old_linears),
	                                                      os.path.basename(old_linears_data)))
	relationship_class = os.path.join(renamed_fgdb, '{0}_{1}'.format(os.path.basename(old_linears),
	                                                                 os.path.basename(old_linears_data)))
	if not arcpy.Exists(relationship_class):
		sys.exit('relationship_class {0} doesn\'t exist!!!'.format(relationship_class))
	else:
		arcpy.Delete_management(in_data=relationship_class)
	del relationship_class
	print('Renaming {0} to {1}...'.format(os.path.basename(old_linears),
	                                      os.path.basename(new_linears)))
	arcpy.Rename_management(in_data=old_linears,
							out_data=new_linears)
	print('\tRenaming {0} to {1}...'.format(old_linears_guid,
	                                      new_linears_guid))
	# arcpy.AlterField_management(in_table=new_linears,
	#                             field=old_linears_guid,
	#                             new_field_name=new_linears_guid,
	#                             new_field_alias=new_linears_guid)
	print('\t\tAdding {0} field...'.format(new_linears_guid))
	arcpy.AddField_management(in_table=new_linears,
							  field_name=new_linears_guid,
							  field_type='GUID',
							  field_is_nullable='NULLABLE',
							  field_is_required='REQUIRED')
	print('\t\tCalculating {0} field...'.format(new_linears_guid))
	arcpy.CalculateField_management(in_table=new_linears,
									field=new_linears_guid,
									expression='!{0}!'.format(old_linears_guid),
									expression_type='PYTHON3')
	print('\t\tDeleting {0} field...'.format(old_linears_guid))
	arcpy.DeleteField_management(in_table=new_linears,
								 drop_field=old_linears_guid)
	print('Renaming {0} to {1}...'.format(os.path.basename(old_linears_data),
	                                      os.path.basename(new_linears_data)))
	arcpy.Rename_management(in_data=old_linears_data,
							out_data=new_linears_data)
	print('\tRenaming {0} to {1}...'.format(old_linears_guid,
	                                      new_linears_guid))
	# arcpy.AlterField_management(in_table=new_linears_data,
	#                             field=old_linears_guid,
	#                             new_field_name=new_linears_guid,
	#                             new_field_alias=new_linears_guid)
	print('\t\tAdding {0} field...'.format(new_linears_guid))
	arcpy.AddField_management(in_table=new_linears_data,
							  field_name=new_linears_guid,
							  field_type='GUID',
							  field_is_nullable='NULLABLE',
							  field_is_required='REQUIRED')
	print('\t\tCalculating {0} field...'.format(new_linears_guid))
	arcpy.CalculateField_management(in_table=new_linears_data,
									field=new_linears_guid,
									expression='!{0}!'.format(old_linears_guid),
									expression_type='PYTHON3')
	print('\t\tDeleting {0} field...'.format(old_linears_guid))
	arcpy.DeleteField_management(in_table=new_linears_data,
								 drop_field=old_linears_guid)
	print('\tRenaming {0} to {1}...'.format(old_linears_data_guid,
	                                      new_linears_data_guid))
	# arcpy.AlterField_management(in_table=new_linears_data,
	#                             field=old_linears_data_guid,
	#                             new_field_name=new_linears_data_guid,
	#                             new_field_alias=new_linears_data_guid)
	print('\t\tAdding {0} field...'.format(new_linears_data_guid))
	arcpy.AddField_management(in_table=new_linears_data,
							  field_name=new_linears_data_guid,
							  field_type='GUID',
							  field_is_nullable='NULLABLE',
							  field_is_required='REQUIRED')
	print('\t\tCalculating {0} field...'.format(new_linears_data_guid))
	arcpy.CalculateField_management(in_table=new_linears_data,
									field=new_linears_data_guid,
									expression='!{0}!'.format(old_linears_data_guid),
									expression_type='PYTHON3')
	print('\t\tDeleting {0} field...'.format(old_linears_data_guid))
	arcpy.DeleteField_management(in_table=new_linears_data,
								 drop_field=old_linears_data_guid)
	print('Renaming {0} to {1}...'.format(os.path.basename(old_linears_species_data),
	                                      os.path.basename(new_linears_species_data)))
	arcpy.Rename_management(in_data=old_linears_species_data,
							out_data=new_linears_species_data)
	print('\tRenaming {0} to {1}...'.format(old_linears_species_data_guid,
	                                        new_linears_species_data_guid))
	# arcpy.AlterField_management(in_table=new_linears_species_data,
	#                             field=old_linears_species_data_guid,
	#                             new_field_name=new_linears_speies_data_guid,
	#                             new_field_alias=new_linears_species_data_guid)
	print('\t\tAdding {0} field...'.format(new_linears_data_guid))
	arcpy.AddField_management(in_table=new_linears_species_data,
							  field_name=new_linears_data_guid,
							  field_type='GUID',
							  field_is_nullable='NULLABLE',
							  field_is_required='REQUIRED')
	print('\t\tCalculating {0} field...'.format(new_linears_data_guid))
	arcpy.CalculateField_management(in_table=new_linears_species_data,
									field=new_linears_data_guid,
									expression='!{0}!'.format(old_linears_data_guid),
									expression_type='PYTHON3')
	print('\t\tDeleting {0} field...'.format(old_linears_data_guid))
	arcpy.DeleteField_management(in_table=new_linears_species_data,
								 drop_field=old_linears_data_guid)
	print('\tRenaming {0} to {1}...'.format(old_linears_species_data_guid,
	                                        new_linears_species_data_guid))
	# arcpy.AlterField_management(in_table=new_linears_species_data,
	#                             field=old_linears_data_guid,
	#                             new_field_name=new_linears_data_guid,
	#                             new_field_alias=new_linears_data_guid)
	print('\t\tAdding {0} field...'.format(new_linears_species_data_guid))
	arcpy.AddField_management(in_table=new_linears_species_data,
							  field_name=new_linears_species_data_guid,
							  field_type='GUID',
							  field_is_nullable='NULLABLE',
							  field_is_required='REQUIRED')
	print('\t\tCalculating {0} field...'.format(new_linears_species_data_guid))
	arcpy.CalculateField_management(in_table=new_linears_species_data,
									field=new_linears_species_data_guid,
									expression='!{0}!'.format(old_linears_species_data_guid),
									expression_type='PYTHON3')
	print('\t\tDeleting {0} field...'.format(old_linears_species_data_guid))
	arcpy.DeleteField_management(in_table=new_linears_species_data,
								 drop_field=old_linears_species_data_guid)
	print('Creating {0}_{1} relationship class...'.format(os.path.basename(new_linears),
	                                                      os.path.basename(new_linears_data)))
	arcpy.CreateRelationshipClass_management(origin_table=new_linears,
											 destination_table=new_linears_data,
											 out_relationship_class=os.path.join(renamed_fgdb, '{0}_{1}'.format(os.path.basename(new_linears),
																												os.path.basename(new_linears_data))),
											 relationship_type='COMPOSITE',
											 forward_label=os.path.basename(new_linears),
											 backward_label=os.path.basename(new_linears_data),
											 message_direction='FORWARD',
											 cardinality='ONE_TO_MANY',
											 attributed='NONE',
											 origin_primary_key=new_linears_guid,
											 origin_foreign_key=new_linears_guid,
											 destination_primary_key='',
											 destination_foreign_key='')
	print('Creating {0}_{1} relationship class...'.format(os.path.basename(new_linears_data),
	                                                      os.path.basename(new_linears_species_data)))
	arcpy.CreateRelationshipClass_management(origin_table=new_linears_data,
											 destination_table=new_linears_species_data,
											 out_relationship_class=os.path.join(renamed_fgdb, '{0}_{1}'.format(os.path.basename(new_linears_data),
																												os.path.basename(new_linears_species_data))),
											 relationship_type='COMPOSITE',
											 forward_label=os.path.basename(new_linears_data),
											 backward_label=os.path.basename(new_linears_species_data),
											 message_direction='FORWARD',
											 cardinality='ONE_TO_MANY',
											 attributed='NONE',
											 origin_primary_key=new_linears_data_guid,
											 origin_foreign_key=new_linears_data_guid,
											 destination_primary_key='',
											 destination_foreign_key='')


#  Points
if do_points:
	print('\n\nDeleting {0}_{1} relationship class...'.format(os.path.basename(old_points),
															  os.path.basename(old_points_data)))
	relationship_class = os.path.join(renamed_fgdb, '{0}_{1}'.format(os.path.basename(old_points),
	                                                                 os.path.basename(old_points_data)))
	if not arcpy.Exists(relationship_class):
		sys.exit('relationship_class {0} doesn\'t exist!!!'.format(relationship_class))
	else:
		arcpy.Delete_management(in_data=relationship_class)
	del relationship_class
	print('Renaming {0} to {1}...'.format(os.path.basename(old_points),
										  os.path.basename(new_points)))
	arcpy.Rename_management(in_data=old_points,
							out_data=new_points)
	print('\tRenaming {0} to {1}...'.format(old_points_guid,
										  new_points_guid))
	# arcpy.AlterField_management(in_table=new_points,
	#                             field=old_points_guid,
	#                             new_field_name=new_points_guid,
	#                             new_field_alias=new_points_guid)
	print('\t\tAdding {0} field...'.format(new_points_guid))
	arcpy.AddField_management(in_table=new_points,
							  field_name=new_points_guid,
							  field_type='GUID',
							  field_is_nullable='NULLABLE',
							  field_is_required='REQUIRED')
	print('\t\tCalculating {0} field...'.format(new_points_guid))
	arcpy.CalculateField_management(in_table=new_points,
									field=new_points_guid,
									expression='!{0}!'.format(old_points_guid),
									expression_type='PYTHON3')
	print('\t\tDeleting {0} field...'.format(old_points_guid))
	arcpy.DeleteField_management(in_table=new_points,
								 drop_field=old_points_guid)
	print('Renaming {0} to {1}...'.format(os.path.basename(old_points_data),
										  os.path.basename(new_points_data)))
	arcpy.Rename_management(in_data=old_points_data,
							out_data=new_points_data)
	print('\tRenaming {0} to {1}...'.format(old_points_guid,
										  new_points_guid))
	# arcpy.AlterField_management(in_table=new_points_data,
	#                             field=old_points_guid,
	#                             new_field_name=new_points_guid,
	#                             new_field_alias=new_points_guid)
	print('\t\tAdding {0} field...'.format(new_points_guid))
	arcpy.AddField_management(in_table=new_points_data,
							  field_name=new_points_guid,
							  field_type='GUID',
							  field_is_nullable='NULLABLE',
							  field_is_required='REQUIRED')
	print('\t\tCalculating {0} field...'.format(new_points_guid))
	arcpy.CalculateField_management(in_table=new_points_data,
									field=new_points_guid,
									expression='!{0}!'.format(old_points_guid),
									expression_type='PYTHON3')
	print('\t\tDeleting {0} field...'.format(old_points_guid))
	arcpy.DeleteField_management(in_table=new_points_data,
								 drop_field=old_points_guid)
	print('\tRenaming {0} to {1}...'.format(old_points_data_guid,
										  new_points_data_guid))
	# arcpy.AlterField_management(in_table=new_points_data,
	#                             field=old_points_data_guid,
	#                             new_field_name=new_points_data_guid,
	#                             new_field_alias=new_points_data_guid)
	print('\t\tAdding {0} field...'.format(new_points_data_guid))
	arcpy.AddField_management(in_table=new_points_data,
							  field_name=new_points_data_guid,
							  field_type='GUID',
							  field_is_nullable='NULLABLE',
							  field_is_required='REQUIRED')
	print('\t\tCalculating {0} field...'.format(new_points_data_guid))
	arcpy.CalculateField_management(in_table=new_points_data,
									field=new_points_data_guid,
									expression='!{0}!'.format(old_points_data_guid),
									expression_type='PYTHON3')
	print('\t\tDeleting {0} field...'.format(old_points_data_guid))
	arcpy.DeleteField_management(in_table=new_points_data,
								 drop_field=old_points_data_guid)
	print('Creating {0}_{1} relationship class...'.format(os.path.basename(new_points),
														  os.path.basename(new_points_data)))
	arcpy.CreateRelationshipClass_management(origin_table=new_points,
											 destination_table=new_points_data,
											 out_relationship_class=os.path.join(renamed_fgdb, '{0}_{1}'.format(os.path.basename(new_points),
																												os.path.basename(new_points_data))),
											 relationship_type='COMPOSITE',
											 forward_label=os.path.basename(new_points),
											 backward_label=os.path.basename(new_points_data),
											 message_direction='FORWARD',
											 cardinality='ONE_TO_MANY',
											 attributed='NONE',
											 origin_primary_key=new_points_guid,
											 origin_foreign_key=new_points_guid,
											 destination_primary_key='',
											 destination_foreign_key='')


copy_domains = True


if copy_domains:
	print('\n\nCopying domains and applying to fields...')
	# Set arcpy.env.workspace to the combined file geodatabase
	arcpy.env.workspace = combined_fgdb
	print('\t#\n\tarcpy.env.workspace:\t\t{0}\n\t#'.format(arcpy.env.workspace))
	# Define in_memory or file geodatabase to store domain tables
	domain_fgdb = os.path.join(os.path.dirname(combined_fgdb),
							   'combined-schema-20181127-domains.gdb'.format(datetime.datetime.now().strftime('%Y%m%d')))
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





# Capture end_time
end_time = time.time()
# Report elapsed_time (= end_time - start_time)
print('\n\nIt took {0} to execute this.'.format(hms_string(end_time - start_time)))
# Print script filename, finish date and time
print('\n\nFinished {0} at {1} on {2}.\n'.format(script,
												 datetime.datetime.now().strftime('%H:%M:%S'),
												 datetime.datetime.now().strftime('%Y-%m-%d')))
