#!/usr/bin/env python3
__author__ = "smw"
__email__ = "smw@ceh.ac.uk"


import os
import sys
import time
import datetime
import pprint


import arcpy


print('\n\n{}'.format(sys.version))


aprx = r'E:\CountrysideSurvey\cs2007-wgem-combined-schema\update-arcgis-pro-project\combined-schema-20161018-project.aprx'
print('\n\naprx:\t\t{0}'.format(aprx))


new_fgdb = r'E:\CountrysideSurvey\cs2007-wgem-combined-schema\update-arcgis-pro-project\combined-schema-new.gdb'
print('\n\nnew_fgdb:\t\t{0}'.format(new_fgdb))


new_aprx = r'E:\CountrysideSurvey\cs2007-wgem-combined-schema\update-arcgis-pro-project\combined-schema-{0}-project.aprx'.format(datetime.datetime.now().strftime('%Y%m%d'))
print('\n\nnew_aprx:\t\t{0}'.format(new_aprx))


print('\n\nOpening project...')
project = arcpy.mp.ArcGISProject(aprx)
print('\tproject.filePath:\t\t{0}'.format(project.filePath))
print('\tproject.dateSaved:\t\t{0}'.format(project.dateSaved))
print('\tproject.version:\t\t{0}'.format(project.version))


print('\n\nLooping through maps...')
maps = project.listMaps()
for map in maps:
    print('\tmap.name:\t\t{0}'.format(map.name))
    print('\tmap.mapType:\t{0}'.format(map.mapType))
    def_cam = map.defaultCamera
    print('\tdef_cam.getExtent():\t\t{0}'.format(def_cam.getExtent()))
    del def_cam
    #
    print('\t\tLooping through layers...')
    layers = map.listLayers()
    for layer in layers:
        print('\t\t\tlayer.name:\t\t{0}'.format(layer.name))
        con_prop = layer.connectionProperties
        print('\t\t\t\tlayer.connectionProperties:\t\t{0}'.format(con_prop))
        if con_prop != None:
            print('\t\t\t\tworkspace_factory:\t\t{0}'.format(con_prop['workspace_factory']))
            print('\t\t\t\tdataset:\t\t{0}'.format(con_prop['dataset']))
            print('\t\t\t\tdatabase:\t\t{0}'.format(con_prop['connection_info']['database']))
            print('\t\t\t\tUpdating database...')
            con_prop['connection_info']['database'] = new_fgdb
            layer.connectionProperties = con_prop
            print('\t\t\t\tUpdated database.')
        del con_prop
    #
    print('\t\tLooping through tables...')
    tables = map.listTables()
    for table in tables:
        print('\t\t\ttable:\t\t\t{0}'.format(table))
        con_prop = table.connectionProperties
        print('\t\t\t\ttable.connectionProperties:\t\t{0}'.format(con_prop))
        if con_prop != None:
            print('\t\t\t\tworkspace_factory:\t\t{0}'.format(con_prop['workspace_factory']))
            print('\t\t\t\tdataset:\t\t{0}'.format(con_prop['dataset']))
            print('\t\t\t\tdatabase:\t\t{0}'.format(con_prop['connection_info']['database']))
            print('\t\t\t\tUpdating database...')
            con_prop['connection_info']['database'] = new_fgdb
            table.connectionProperties = con_prop
            print('\t\t\t\tUpdated database.')
        del con_prop


print('\n\nLooping through layouts...')
layouts = project.listLayouts()
for layout in layouts:
    print('\tlayout.name:\t\t'.format(layout.name))


print('\n\nSaving a copy of the ArcGIS Pro project...')
project.saveACopy(new_aprx)
print('Saved a copy of the ArcGIS Pro Project.')
del project
new_project = arcpy.mp.ArcGISProject(new_aprx)
print('\tnew_project.filePath:\t\t\t{0}'.format(new_project.filePath))
print('\tnew_project.dateSaved:\t\t\t{0}'.format(new_project.dateSaved))
print('\tnew_project.version:\t\t\t{0}'.format(new_project.version))


map = new_project.listMaps()[0]
print('\tmap.name:\t\t\t\t\t\t{0}'.format(map.name))
def_cam = map.defaultCamera
print('\tdef_cam.getExtent():\t\t\t{0}'.format(def_cam.getExtent()))
new_extent = arcpy.Extent(XMin=0.0, YMin=0.0, XMax=700000.0, YMax=1300000.0)
map.defaultCamera.setExtent(new_extent)
print('\tmap.defaultCamera.getExtent():\t{0}'.format(map.defaultCamera.getExtent()))
new_project.save()
print('\tnew_project.filePath:\t\t\t{0}'.format(new_project.filePath))
print('\tnew_project.dateSaved:\t\t\t{0}'.format(new_project.dateSaved))
print('\tnew_project.version:\t\t\t{0}'.format(new_project.version))









del new_project

