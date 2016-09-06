import os
import shutil
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
    return "{0}:{1:>02}:{2:>05.2f}".format(h, m, s)


# Print Python version, version info, and platform architecture
print('\n\nsys.version:\t\t\t\t\t{0}'.format(sys.version))
print('sys.versioninfo:\t\t\t\t{0}'.format(sys.version_info))
print('platform.architecture():\t\t{0}'.format(platform.architecture()))


# Print script filename, start date and time
script = os.path.basename(__file__)
print('\n\nStarted {0} at {1} on {2}...'.format(script,
                                                datetime.datetime.now().strftime('%H:%M:%S'),
                                                datetime.datetime.now().strftime('%Y-%m-%d')))


root_folder = r'E:\CountrysideSurvey\esri-uk\arcpy-mapping'
print('\n\nroot_folder:\t\t{0}'.format(root_folder))


blank_aprx = r'blank-project-with-single-map\blank-project-with-single-map.aprx'
blank_aprx = os.path.join(root_folder, blank_aprx)
print('\n\nblank_aprx:\t\t{0}'.format(blank_aprx))


new_aprx = r'copied-project-with-single-map.aprx'
print('\n\nnew_aprx:\t\t{0}'.format(new_aprx))


new_aprx_folder = os.path.join(root_folder, os.path.splitext(new_aprx)[0])
print('\n\nnew_aprx_folder:\t\t{0}'.format(new_aprx_folder))
if not os.path.exists(new_aprx_folder):
    os.makedirs(new_aprx_folder)


new_aprx = os.path.join(new_aprx_folder, new_aprx)
print('\n\nnew_aprx:\t\t{0}'.format(new_aprx))


if os.path.exists(new_aprx):
    os.remove(new_aprx)


shutil.copyfile(blank_aprx, new_aprx)


aprx = arcpy.mp.ArcGISProject(new_aprx)


default_gdb = r'E:\CountrysideSurvey\esri-uk\guids\guids-20160906-without-nullable-fields.gdb'


aprx.defaultGeodatabase = default_gdb
print('\n\naprx.defaultGeodatabase:\t\t{0}'.format(aprx.defaultGeodatabase))


maps = aprx.listMaps()
for map in maps:
    print('\n\nmap.name:\t\t{0}\t\tmap.mapType:\t\t{1}'.format(map.name, map.mapType))
del map, maps


map = aprx.listMaps('Map')[0]
layer_file = arcpy.mp.LayerFile(r'E:\CountrysideSurvey\esri-uk\arcpy-mapping\layer-files\BLKDATA.lyrx')
map.addLayer(add_layer_or_layerfile=layer_file,
             add_position='TOP')
layer_file = arcpy.mp.LayerFile(r'E:\CountrysideSurvey\esri-uk\arcpy-mapping\layer-files\SCPTDATA.lyrx')
map.addLayer(add_layer_or_layerfile=layer_file,
             add_position='TOP')
layer_file = arcpy.mp.LayerFile(r'E:\CountrysideSurvey\esri-uk\arcpy-mapping\layer-files\LINEARDATA.lyrx')
map.addLayer(add_layer_or_layerfile=layer_file,
             add_position='TOP')
layer_file = arcpy.mp.LayerFile(r'E:\CountrysideSurvey\esri-uk\arcpy-mapping\layer-files\POINTDATA.lyrx')
map.addLayer(add_layer_or_layerfile=layer_file,
             add_position='TOP')


table = arcpy.mp.Table(r'E:\CountrysideSurvey\esri-uk\guids\guids-20160906-without-nullable-fields.gdb\PCOMPDATA')
map.addTable(add_table=table)
table = arcpy.mp.Table(r'E:\CountrysideSurvey\esri-uk\guids\guids-20160906-without-nullable-fields.gdb\EVENTDATA')
map.addTable(add_table=table)
table = arcpy.mp.Table(r'E:\CountrysideSurvey\esri-uk\guids\guids-20160906-without-nullable-fields.gdb\SEVENTDATA')
map.addTable(add_table=table)
table = arcpy.mp.Table(r'E:\CountrysideSurvey\esri-uk\guids\guids-20160906-without-nullable-fields.gdb\COMPDATA')
map.addTable(add_table=table)



# lyts = aprx.listLayouts()
# for lyt in lyts:
#     print(lyt.name)


# lyt = aprx.listLayouts("Map")[0]
# mf = lyt.listElements("mapframe_element", "Map")[0]
# mf.camera.setExtent(arcpy.Extent(0,0,700000,1300000))


# map.camera.setExtent(arcpy.Extent(0.0, 0.0, 700000.0, 1300000.0))


aprx.save()


del aprx





# Capture end_time
end_time = time.time()


# Report elapsed_time (= end_time - start_time)
print('\n\nIt took {0} to execute this.'.format(hms_string(end_time - start_time)))


# Print script filename, finish date and time
print('\n\nFinished {0} at {1} on {2}.\n'.format(script,
                                                 datetime.datetime.now().strftime('%H:%M:%S'),
                                                 datetime.datetime.now().strftime('%Y-%m-%d')))
