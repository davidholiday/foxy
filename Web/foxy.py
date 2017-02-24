#!/usr/bin/env python

import logging
import argparse
import simplejson as json
import getpass
import subprocess
import socket
import io
import constants
import html_generator
import os
import ast


'''
driver for the foxy web app. main() querries current state of docker and builds the 
appropriate json and html files to render that information in the application.
'''


def generate_app():
    main()


def main():
    setup_logging()
    parser = get_parser()
    parsedArgsDict = parse_args(parser)
    containerNames = get_container_names(parsedArgsDict)
    containerInfoDict = get_container_info_dict(containerNames)
    foxyDataDict = get_foxydata_dict(containerInfoDict)
    make_foxy_files(containerInfoDict, foxyDataDict)


def setup_logging():
    """

    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - [%(levelname)s] [%(threadName)s] (%(module)s:%(lineno)d) %(message)s", )


def get_parser():
    """

    """
    parser = argparse.ArgumentParser(\
        description="creates a dashboard that lists port resolutions for a given docker container.")

    parser.add_argument("-d", \
                        "--%s" % (constants.DASH_NAME_ARG,), \
                        help="the display name for this dashboard instance.")

    parser.add_argument("-c", 
                        "--%s" % (constants.CONTAINER_NAME_ARG,), 
                        help="the name of the container you wish to create a dock for \
                              (default is to list all running containers in the dash).")
    return parser


def parse_args(parser):
    """

    """
    isArgKosher = arg_check(parser, argparse.ArgumentParser)
    if (isArgKosher != True):
        raise ValueError("this method only accepts instances of argparse.ArgumentParser!")

    args = parser.parse_args()
    parsedArgsDict = vars(args)

    if (parsedArgsDict.get(constants.DASH_NAME_ARG)):

        parsedArgsDict[constants.DASH_NAME_ARG] = \
            "%s %s@%s" % (parsedArgsDict.get(constants.DASH_NAME_ARG), getpass.getuser(), socket.gethostname())

    else:
        parsedArgsDict[constants.DASH_NAME_ARG] = \
            "%s %s@%s" % (constants.DEFAULT_DASH_NAME_PREFIX, getpass.getuser(), socket.gethostname())

    return parsedArgsDict


def get_container_names(parsedArgsDict):
    """

    """
    isArgKosher = arg_check(parsedArgsDict, dict)
    if (isArgKosher != True):
        raise ValueError("this method only accepts instances of dict")

    containerNames = list()

    if (parsedArgsDict[constants.CONTAINER_NAME_ARG]):
        containerNames.append(parsedArgsDict[constants.CONTAINER_NAME_ARG])
    else:

        output = subprocess.Popen(["docker", "ps", "-a", "--format", 'table {{.Names}}'], \
                    stdout=subprocess.PIPE).communicate()[0]

        outputList = output.split()
        del outputList[0]
        containerNames = containerNames + outputList

    return containerNames


def get_container_info_dict(containerNames):
    """

    """
    containerInfoDict = dict()
    for containerName in containerNames:
        output = subprocess.Popen(["docker", "inspect", "--format='{{json .}}'", containerName],
            stdout=subprocess.PIPE).communicate()[0]
        # no fucking idea why this suddenly became an issue, but it is so blah. 
        # basically {output} is bookended by single quotes which the json.loads()
        # operation isn't handling well. the following strips the leading and trailing 
        # single quote to facillitate json parsing. 
        # moreover .strip() will probably work here but it's being a butthole 
        # and only removing the leading ' so fuckit I'm doing it the overly 
        # complicated way
        unfunkified_output = ast.literal_eval(output)
        containerInfoDict[containerName] = json.loads(unfunkified_output)
    
    return containerInfoDict


def get_foxydata_dict(containerInfoDict):
    """
    """    
    foxyDataDict = dict()
    for key, valueDict in containerInfoDict.iteritems():

        logging.info("container is: %s"  % (key) )
        #valueDict = json.loads(value)
        metaDataDict = valueDict['Config']['Labels']
        
        portsDict = dict()
        if valueDict['State']['Running'] == True:
            portsDict = valueDict['NetworkSettings']['Ports']

        # because the vals are given to us as lists of dicts and we need them to be dicts
        for k, v in portsDict.iteritems():
            if v is not None:
                portsDict[k] = v[0]


        foxyFilter = constants.TOP_LEVEL_METATDATA_FILTER
        containerFoxyDataDict = filter_by_namespace(metaDataDict, foxyFilter)
        containerFoxyDataDict[constants.DOCKER_PORT_KEY] = portsDict
        foxyDataDict[key] = containerFoxyDataDict

    return foxyDataDict 


def filter_by_namespace(valueDict, filterValue):
    """
    filters foxy metadata by namespace, returns set of <k,v>'s that DO NOT contain the 
    filtered portion of the namespace. 
    """
    return { k[ len(filterValue): ] : v \
                for k, v in valueDict.iteritems() \
                    if k.startswith(filterValue) }


def make_foxy_files(containerInfoDict, foxyDataDict):
    serialize_inner_dict_as_json('info', containerInfoDict)
    serialize_inner_dict_as_json('foxydata', foxyDataDict)

    foxyColorIndex = 0
    containerPanels = []
    for k, v in containerInfoDict.iteritems():

        if v['State']['Running'] == False:
            panelType = "panel-default"
        else:
            panelType = "panel-info"
            #panelType = constants.FOXY_PANEL_COLOR_LIST[foxyColorIndex]
            #
            #foxyColorIndex = (foxyColorIndex + 1) \
            #    if (foxyColorIndex + 1 < len(constants.FOXY_PANEL_COLOR_LIST)) \
            #        else (0)

        containerName = k
        categoryToPortsDict = get_category_to_ports_dict(containerName, foxyDataDict)
        #portToDataDict = foxyDataDict[containerName][constants.DOCKER_PORT_KEY]

        containerPanel = html_generator.get_container_panel(panelType, 
                                                              containerName, 
                                                              categoryToPortsDict, 
                                                              foxyDataDict, 
                                                              containerInfoDict)
        containerPanels.append(containerPanel)

    page = html_generator.get_page(containerInfoDict, containerPanels)
    f = open('./Static/index.html', 'w')
    f.write(page)
    f.close()


def get_category_to_ports_dict(containerName, foxyDataDict):
    containerFoxyDataDict = foxyDataDict[containerName]
    containerPortsDict = containerFoxyDataDict[constants.DOCKER_PORT_KEY]

    categoryToPortsDict = dict()
    for k, v in containerPortsDict.iteritems():
        exposedPort = k.replace(constants.DOCKER_PORTS_VALUE_SUFFIX, '')
        foxyKey = exposedPort + ".group"

        if foxyKey in foxyDataDict[containerName]:
            group = foxyDataDict[containerName][foxyKey]
            #group = str(group)

            if group in categoryToPortsDict:
                categoryToPortsDict[group].append(exposedPort)
            else:
                categoryToPortsDict[group] = [exposedPort]

    return categoryToPortsDict


# assumes dicts of dicts!
def serialize_inner_dict_as_json(filenameSuffix, dictionary):
    
    for k, v in dictionary.iteritems():
        filename = k + "_" + filenameSuffix + ".json"
        v_asJSON = json.dumps(v, ensure_ascii=False)
        dataDirectory = os.getcwd() + constants.RELATIVE_PATH_TO_JSON
        with io.open(dataDirectory + filename, 'w', encoding="utf-8") as outfile:
            outfile.write(unicode(v_asJSON))


def arg_check(arg, clazz):
    """

    """
    return isinstance(arg, clazz)


if __name__ == "__main__": main()




