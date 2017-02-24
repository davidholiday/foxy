#!/usr/bin/env python

import cherrypy
import foxy
import os
import subprocess
import constants


class Foxy(object):

    @cherrypy.expose
    def index(self):
        foxy.generate_app()
        return file("./Static/index.html")      

    @cherrypy.expose
    def start(self, container):
        output = subprocess.Popen(["docker", "start", container], stdout=subprocess.PIPE).communicate()[0]
        raise cherrypy.HTTPRedirect("/#" + container + constants.PANEL_DIV_ID_SUFFIX)

    @cherrypy.expose
    def stop(self, container):
        output = subprocess.Popen(["docker", "stop", container], stdout=subprocess.PIPE).communicate()[0]
        raise cherrypy.HTTPRedirect("/#" + container + constants.PANEL_DIV_ID_SUFFIX)


if __name__ == '__main__':
    cherrypy.config.update({'server.socket_port': 1701})

    conf = {
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        '/Static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './Static'
        },
        '/Data': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './Data'
        }
    }
    cherrypy.quickstart(Foxy(), '/', conf)
