import constants
import json

import sys
import os
#sys.path.insert(0, os.getcwd() + '/Templates')
from Templates import templates



'''
methods to generate the static html needed to drive the foxy webapp. 
*NOTE* you should only need to call the get_page method to generate 
the index file.
'''




def get_page(containerInfoDict, containerPanels):

    # dropdown
    dropdownItems = ""
    tags = ""
    for k, v in containerInfoDict.iteritems():
        containerName = k
        containerPanelName = containerName + "_panel"
        dropdownItemTemplate = templates.get_dropdown_item_template()

        dropdownItemContent = dropdownItemTemplate.substitute(CONTAINER_NAME = containerName,
                                                              CONTAINER_PANEL_NAME = containerPanelName)
        
        dropdownItems = dropdownItems + dropdownItemContent
        tags = tags + """ " """ + containerName + """ ", """

    # content panels
    sep = "\n"
    containerPanelString = sep.join(containerPanels) 
    pageTemplate = templates.get_page_template();

    page = pageTemplate.substitute(CONTAINER_PANELS = containerPanelString,
                                   DROPDOWN_ITEMS = dropdownItems,
                                   TAGS = tags)
    
    return page




def get_container_panel(panelType, containerName, categoryToPortsDict, foxyDataDict, containerInfo):
    
    buttonType = ""
    buttonLabel = ""
    
    if containerInfo[containerName]['State']['Running'] == True:
        buttonType = "btn-danger"
        buttonLabel = "Stop"
        buttonURL = "/stop/?container=" + containerName 
    else:
        buttonType = "btn-success"
        buttonLabel = "Start" 
        buttonURL = "/start/?container=" + containerName 

    containerPanelContents = get_container_panel_contents(containerName, 
                                                          categoryToPortsDict, 
                                                          foxyDataDict,
                                                          buttonType,
                                                          buttonLabel,
                                                          buttonURL)

    containerPanelName = containerName + "_panel"
    containerPanelTemplate = templates.get_container_panel_template()
    containerPanel = containerPanelTemplate.substitute(CONTAINER_PANEL_NAME = containerPanelName,
                                                       CONTAINER_PANEL_CONTENTS = containerPanelContents,
                                                       PANEL_TYPE = panelType)
    return containerPanel




def get_container_panel_contents(containerName, 
                                 categoryToPortsDict, 
                                 foxyDataDict, 
                                 buttonType, 
                                 buttonLabel, 
                                 buttonURL):

    containerPanelContentTemplate = templates.get_container_panel_content_template()
    containerPanelTabContent = get_container_tab_content(containerName, categoryToPortsDict, foxyDataDict)

    portsDivID = containerName + "_ports"
    infoDivID = containerName + "_info"

    containerPanelContent = containerPanelContentTemplate.substitute(CONTAINER_NAME = containerName, 
                                                                     TAB_CONTENT = containerPanelTabContent,
                                                                     BUTTON_TYPE = buttonType,
                                                                     BUTTON_LABEL = buttonLabel,
                                                                     BUTTON_URL = buttonURL,
                                                                     PORTS_DIV_ID = portsDivID,
                                                                     INFO_DIV_ID = infoDivID)
    return containerPanelContent




def get_container_tab_content(containerName, categoryToPortsDict, foxyDataDict):
    tables = get_container_port_tables(containerName, categoryToPortsDict, foxyDataDict)
    containerInfoURL = "." + constants.RELATIVE_PATH_TO_JSON + containerName + "_info.json"
    tab_content_template = templates.get_container_tab_content_template()

    portsDivID = containerName + constants.FILE_AND_DIV_PORTS_SUFFIX
    infoDivID = containerName + constants.FILE_AND_DIV_INFO_SUFFIX

    tab_content = tab_content_template.substitute(TABLES = tables, 
                                                  CONTAINER_INFO_URL = containerInfoURL,
                                                  PORTS_DIV_ID = portsDivID,
                                                  INFO_DIV_ID = infoDivID)

    return tab_content




def get_container_port_tables(containerName, categoryToPortsDict, foxyDataDict):
    containerFoxyDataDict = foxyDataDict[containerName]

    returnVal = ""

    for category, portDict in categoryToPortsDict.iteritems():
        portCategoryTable = get_container_port_category_table(category, portDict, containerFoxyDataDict)
        returnVal = returnVal + portCategoryTable

    return returnVal





def get_container_port_category_table(category, portDict, containerFoxyDataDict):
    rows = ""
    for port in portDict:
        portKey = port + constants.DOCKER_PORTS_VALUE_SUFFIX
        rows = rows + get_container_port_category_table_row(portKey, containerFoxyDataDict)
    
    tableTemplate = templates.get_container_port_category_table_template()
    table = tableTemplate.substitute(TABLE_ROWS = rows, CATEGORY_NAME = category)
    return table




def get_container_port_category_table_row(port, containerFoxyDataDict):
    row_template = templates.get_container_port_category_table_row_template(port, containerFoxyDataDict)
    foxyPort = templates.get_foxy_port(port)
    foxyAttributeKey = foxyPort + "." +  constants.FOXY_PORT_ATTRIBUTE_KEY

    if foxyAttributeKey in containerFoxyDataDict:
        attribute = containerFoxyDataDict[foxyAttributeKey]

        html_a_fied_attributes = \
            get_container_port_category_table_row_attribute(attribute, port, containerFoxyDataDict)
        
        row = row_template.substitute(ATTRIBUTES = html_a_fied_attributes)
    else:
        row = row_template.substitute(ATTRIBUTES = '')



    return row



def get_container_port_category_table_row_attribute(attribute, port, containerFoxyDataDict):
    
    returnVal = ""

    if (attribute == constants.FOXY_WEB_ATTRIBUTE):
        hostIP = containerFoxyDataDict[constants.DOCKER_PORT_KEY][port][constants.DOCKER_PORTS_HOST_IP_KEY]
        hostPort = containerFoxyDataDict[constants.DOCKER_PORT_KEY][port][constants.DOCKER_PORTS_HOST_PORT_KEY]
        foxyLink = "http://" + hostIP + ":" + str(hostPort)

        returnVal = returnVal + """<a target="_blank" href=" """ + foxyLink + \
                                """ " style="text-decoration: none"> """ + \
                                """<span class="btn btn btn-success"> """ + \
                                str(attribute) + \
                                """</span></a>"""
    else: 
        returnVal = returnVal + """<span class="label label label-warning">""" + \
                                str(attribute) + \
                                """</span>"""

    return returnVal



