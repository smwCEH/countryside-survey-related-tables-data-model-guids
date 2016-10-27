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


import arcpy


def pprint_fields(table):
    """ pretty print table's fields and their properties """
    def _print(l):
        print("".join(["{:>14}".format(i) for i in l]))
    atts = ['name', 'aliasName', 'type', 'baseName', 'domain',
            'editable', 'isNullable', 'length', 'precision',
            'required', 'scale',]
    _print(atts)
    for f in arcpy.ListFields(table):
        _print(["{:>12}".format(getattr(f, i)) for i in atts])


blkdata = r'E:\CountrysideSurvey\cs2007-wgem-combined-schema\update-arcgis-pro-project\combined-schema-20161017.gdb\BLKDATA'


pprint_fields(blkdata)


