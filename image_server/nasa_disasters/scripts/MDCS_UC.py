# ------------------------------------------------------------------------------
# Copyright 2013 Esri
# Modifications Copyright 2021 Alaska Satellite Facility
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ------------------------------------------------------------------------------
# Name: MDCS_UC.py
# Description: A class to implement all user functions or to extend the built in MDCS functions/commands chain.
# Version: 20201230
# Requirements: ArcGIS 10.1 SP1
# Author: Esri Imagery Workflows team
# ------------------------------------------------------------------------------
#!/usr/bin/env python
import os
import sys
import arcpy


class UserCode:

    def __init__(self):
        pass    # initialize variables that need to be shared between multiple user commands.

    def sample00(self, data):
        base = data['base']         # using Base class for its XML specific common functions. (getXMLXPathValue, getXMLNodeValue, getXMLNode)
        xmlDOM = data['mdcs']       # access to MDCS config file
        command_used = base.getXMLNodeValue(xmlDOM, 'Command')
        workspace = data['workspace']
        md = data['mosaicdataset']
        log = data['log']
        log.Message('%s\\%s' % (workspace, md), 0)
        return True

    def sample01(self, data):
        log = data['log']           # How to use logging within the user function.
        log.Message('hello world', 0)
        return True

    def sample02(self, data):
        log = data['log']           # How to use logging within the user function.
        log.Message('Returning multiple values', 0)
        data['useResponse'] = True
        data['response'] = ['msg0', 'msg1', 'msg2']
        data['status'] = True   # overall function status
        return True    # True must be returned if data['useResponse'] is required. data['response'] can be used to return multiple values.

    def customCV(self, data):
        workspace = data['workspace']
        md = data['mosaicdataset']
        ds = os.path.join(workspace, md)
        ds_cursor = arcpy.UpdateCursor(ds)
        if (ds_cursor is not None):
            print ('Calculating values..')
            row = ds_cursor.next()
            while(row is not None):
                row.setValue('MinPS', 0)
                row.setValue('MaxPS', 300)
                WRS_Path = row.getValue('WRS_Path')
                WRS_Row = row.getValue('WRS_Row')
                if (WRS_Path is not None and
                        WRS_Row is not None):
                    PR = (WRS_Path * 1000) + WRS_Row
                    row.setValue('PR', PR)
                AcquisitionData = row.getValue('AcquisitionDate')
                if (AcquisitionData is not None):
                    AcquisitionData = str(AcquisitionData).replace('-', '/')
                    day = int(AcquisitionData.split()[0].split('/')[1])
                    row.setValue('Month', day)
                grp_name = row.getValue('GroupName')
                if (grp_name is not None):
                    CMAX_INDEX = 16
                    if (len(grp_name) >= CMAX_INDEX):
                        row.setValue('DayOfYear', int(grp_name[13:CMAX_INDEX]))
                        row.setValue('Name', grp_name.split('_')[0] + '_' + row.getValue('Tag'))
                ds_cursor.updateRow(row)
                row = ds_cursor.next()
            del ds_cursor
        return True

    def UpdateTagField(self, data):
        workspace = data['workspace']
        md = data['mosaicdataset']
        ds = os.path.join(workspace, md)
        ds_cursor = arcpy.UpdateCursor(ds)
        if (ds_cursor is not None):
            print ('Updating Tag values..')
            row = ds_cursor.next()
            while(row is not None):
                tag = row.getValue('Tag')
                if (tag is not None):
                    row.setValue('Tag', 'VV,VH')
                ds_cursor.updateRow(row)
                row = ds_cursor.next()
            del ds_cursor
        return True

    def UpdateNameField(self, data):
        log = data['log']
        workspace = data['workspace']
        md = data['mosaicdataset']
        ds = os.path.join(workspace, md)
        ds_cursor = arcpy.da.UpdateCursor(ds, ["Name", "GroupName",
                                               "Tag", "MaxPS"])  # https://pro.arcgis.com/en/pro-app/latest/arcpy/data-access/updatecursor-class.htm
        if (ds_cursor is not None):
            log.Message('Updating Name Values..', 0)
            for row in ds_cursor:
                try:
                    ## NameField = row[0]
                    GroupField = row[1]
                    TagField = row[2]
                    if (TagField is not None):
                        TagField = "VV,VH"
                    ## lstNameField = NameField.split(';')
                    lstTagField = TagField.split(',')
                    newNameField = GroupField + "_" + lstTagField[0] + ';' + GroupField + "_" + lstTagField[1]
                    row[0] = newNameField
                    row[2] = TagField
                    row[3] = 310
                    ds_cursor.updateRow(row)
                    log.Message("{} updated".format(newNameField), 0)
                except Exception as exp:
                    log.Message(str(exp), 2)
            del ds_cursor
        return True