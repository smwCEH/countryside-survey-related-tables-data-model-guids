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


old_areas = os.path.join(renamed_fgdb, 'SCPTDATA')
new_areas = os.path.join(renamed_fgdb, 'AREAS')
old_areas_guid = 'SCPTDATA_GUID'
new_areas_guid = 'AREAS_GUID'
old_areas_data = os.path.join(renamed_fgdb, 'COMPDATA')
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


# Capture end_time
end_time = time.time()
# Report elapsed_time (= end_time - start_time)
print('\n\nIt took {0} to execute this.'.format(hms_string(end_time - start_time)))
# Print script filename, finish date and time
print('\n\nFinished {0} at {1} on {2}.\n'.format(script,
												 datetime.datetime.now().strftime('%H:%M:%S'),
												 datetime.datetime.now().strftime('%Y-%m-%d')))
