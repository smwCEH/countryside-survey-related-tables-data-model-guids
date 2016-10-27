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
    print('\tlayout.name:\t\t\t{0}'.format(layout.name))
    print('\tlayout.pageHeight:\t\t{0}'.format(layout.pageHeight))
    print('\tlayout.pageWidth:\t\t{0}'.format(layout.pageWidth))
    print('\tlayout.pageUnits:\t\t{0}'.format(layout.pageUnits))
    for element in layout.listElements("MAPFRAME_ELEMENT"):
        print('\t\telement.name:\t\t\t\t{0}'.format(element.name))
        print('\t\telement.type:\t\t\t\t{0}'.format(element.type))
        print('\t\telement.elementHeight:\t\t{0}'.format(element.elementHeight))
        print('\t\telement.elementWidth:\t\t{0}'.format(element.elementWidth))
        print('\t\telement.elementPositionX:\t{0}'.format(element.elementPositionX))
        print('\t\telement.elementPositionY:\t{0}'.format(element.elementPositionY))
        print('\t\telement.elementRotation:\t{0}'.format(element.elementRotation))
        print('\t\telement.visble:\t\t\t\t{0}'.format(element.visible))
        #
        camera = element.camera
        print('\t\tcaemra.mode:\t\t{0}'.format(camera.mode))
        print('\t\tcaemra.scale:\t\t{0}'.format(camera.scale))
        print('\t\tcaemra.X:\t\t\t{0}'.format(camera.X))
        print('\t\tcaemra.Y:\t\t\t{0}'.format(camera.Y))
        print('\t\tcamera.getExtent():\t{0}'.format(camera.getExtent()))

        # Change extent using camera setExtent() method
        # new_extent = arcpy.Extent(0.0, 0.0, 700000.0, 1300000.0)
        # element.camera.setExtent(new_extent)        
        # Alternatively, change extent by updating camera X and position and scale
        element.camera.X = 342500
        element.camera.Y = 457500
        element.camera.scale = 10000
        print('\t\telement.camera.mode:\t\t{0}'.format(element.camera.mode))
        print('\t\telement.camera.scale:\t\t{0}'.format(element.camera.scale))
        print('\t\telement.camera.X:\t\t\t{0}'.format(element.camera.X))
        print('\t\telement.camera.Y:\t\t\t{0}'.format(element.camera.Y))
        print('\t\telement.camera.getExtent():\t{0}'.format(element.camera.getExtent()))
        # Or use bookmarks (if they've been set) and the map frame element zoomToBookMark() method 
        bookmarks = element.map.listBookmarks()
        for bookmark in bookmarks:
            print('\t\tbookmark.map.name:\t\t{0}'.format(bookmark.map.name))
            print('\t\tbookmark.hasThumbnail:\t{0}'.format(bookmark.hasThumbnail))
            print('\t\tbookmark.name:\t\t\t{0}'.format(bookmark.name))
            element.zoomToBookmark(bookmark)
            pdf = os.path.join(r'E:\CountrysideSurvey\cs2007-wgem-combined-schema\update-arcgis-pro-project', bookmark.name + r'.pdf')
            print('\t\tExporting to PDF {0}...'.format(pdf))
            layout.exportToPDF(out_pdf=pdf,
                               resolution=300,
                               image_quality='BEST',
                               compress_vector_graphics=True,
                               image_compression='ADAPTIVE',
                               embed_fonts=True,
                               layers_attributes='LAYERS_ONLY',
                               georef_info=True,
                               jpeg_compression_quality=100,
                               clip_to_elements=False)
            print('\t\tExported to PDF {0}.'.format(pdf))




print('\n\nSaving a copy of the ArcGIS Pro project...')
project.saveACopy(new_aprx)
print('Saved a copy of the ArcGIS Pro Project.')
del project
new_project = arcpy.mp.ArcGISProject(new_aprx)
print('\tnew_project.filePath:\t\t\t{0}'.format(new_project.filePath))
print('\tnew_project.dateSaved:\t\t\t{0}'.format(new_project.dateSaved))
print('\tnew_project.version:\t\t\t{0}'.format(new_project.version))


#map = new_project.listMaps()[0]
#print('\tmap.name:\t\t\t\t\t\t{0}'.format(map.name))
#def_cam = map.defaultCamera
#print('\tdef_cam.getExtent():\t\t\t{0}'.format(def_cam.getExtent()))
#new_extent = arcpy.Extent(XMin=0.0, YMin=0.0, XMax=700000.0, YMax=1300000.0)
#map.defaultCamera.setExtent(new_extent)
#print('\tmap.defaultCamera.getExtent():\t{0}'.format(map.defaultCamera.getExtent()))
#new_project.save()
#print('\tnew_project.filePath:\t\t\t{0}'.format(new_project.filePath))
#print('\tnew_project.dateSaved:\t\t\t{0}'.format(new_project.dateSaved))
#print('\tnew_project.version:\t\t\t{0}'.format(new_project.version))


del new_project

