import string

import sys
import os
sys.path.insert(0, os.getcwd() + '/Web')
import constants




'''
html templates used by foxy to build the webapp
'''




def get_page_template():
    return string.Template("""
<!DOCTYPE html>
<html lang="en">

    <head>
        <title>foxy</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">

        <link rel="stylesheet" href="./bootstrap.min.css">        
        <link rel="stylesheet" href="jquery.json-view.min.css">
        <link rel="stylesheet" href="foxy_custom.css" type="text/css">

        <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>
        <script src="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
        <script src="./jquery.json-view.min.js"></script>

    </head>

    <body>

        <!-- nav bar -->
        <nav class="navbar navbar-inverse navbar-fixed-top">

            <div class="container-fluid">
                <a href="#" class="navbar-left"><img src="./cf_logo_smallest.png"></a>
                
                <div class="navbar-header">
                    <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#bs-example-navbar-collapse-2">
                        <span class="sr-only">Toggle navigation</span>
                        <span class="icon-bar"></span>
                        <span class="icon-bar"></span>
                        <span class="icon-bar"></span>
                    </button>
                    <a class="navbar-brand" href="#">&nbsp FOXY</a>              
                </div>
        
                <div class="collapse navbar-collapse" id="bs-example-navbar-collapse-2">

                    <!-- search bar -->
                    <!--
                    <form class="navbar-form navbar-center" role="search">
                        <div class="form-group">
                            <input type="text" class="form-control" placeholder="Search">
                        </div>
                        <button type="submit" class="btn btn-default">Submit</button>
                    </form>
                    -->

                    <!-- right-side buttons -->
                    <ul class="nav navbar-nav navbar-right">
                        
                        <li class="dropdown">
                            <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-expanded="false">CONTAINERS <span class="caret"></span></a>
                            <ul class="dropdown-menu" role="menu">
                                $DROPDOWN_ITEMS
                            </ul>
                        </li>

                        <li><a href="#">HELP</a></li>
                    </ul>
                </div>

           </div>
        </nav>


        <div class="content-container">       
            $CONTAINER_PANELS
        </div>

        <!-- put some space at the footer so we can scroll the last panel to the top of the screen -->
        <div class="spacer200"></div>
        <div class="spacer200"></div>
        <div class="spacer200"></div>

    </body>

</html>

        """)




def get_dropdown_item_template():
    return string.Template("""
<li><a href="#$CONTAINER_PANEL_NAME">$CONTAINER_NAME</a></li>
""")




def get_container_panel_template():
    return string.Template(""" 
<div class="anchor" id="$CONTAINER_PANEL_NAME">      
<div class="panel $PANEL_TYPE panel-fluid"> 
    $CONTAINER_PANEL_CONTENTS 
</div>
</div>
<!--<div class="spacer50"></div>-->""")




def get_container_panel_content_template():
    return string.Template("""
<div class="panel-heading">
    <h4>$CONTAINER_NAME</h4>
</div> 
 <div class="panel-body">
    <ul class="nav nav-pills">
        <li class="active"><a href="#$PORTS_DIV_ID" data-toggle="tab" aria-expanded="true">ports</a></li>
        <li class=""><a href="#$INFO_DIV_ID" data-toggle="tab" aria-expanded="false">info</a></li> 
        <a href="#" class="btn $BUTTON_TYPE pull-right">$BUTTON_LABEL Container</a>
    </ul>
    <div class="tab-content"> 
        $TAB_CONTENT
    </div>                 
</div>""")




def get_container_tab_content_template():
    return string.Template("""
<div id="$PORTS_DIV_ID" class="tab-pane fade in active">
    $TABLES
</div>
<div id="$INFO_DIV_ID" class="tab-pane fade">
    <script>
        var json = (function() {
            var json = null;
            $$.ajax({
                'async': false,
                'global': false,
                'url': "$CONTAINER_INFO_URL",
                'dataType': "json",
                'success': function (data) {
                json = data;
                }
            });
            return json;
            })();

        $$('#$INFO_DIV_ID').jsonView(json, { 'collapsed: true' } );
    </script>
</div> """)   




def get_container_port_category_table_template():
    return string.Template("""
<div class="page-header">
    <h4 id="$CATEGORY_NAME">$CATEGORY_NAME</h4>
</div>  
<table class="table table-striped table-hover ">
    <thead>
            <tr>
                <th>NAME</th>
                <th>EXPOSED AS</th>       
                <th>MAPPED AS</th>
                <th>ATTRIBUTES</th>
            </tr>
    </thead>
    <tbody>
        $TABLE_ROWS
    </tbody>
</table> 
<div class="spacer50"></div>""")




def get_container_port_category_table_row_template(port, containerFoxyDataDict):
    foxyPort = get_foxy_port(port)
    foxyPortNameKey = foxyPort + "." + constants.FOXY_PORT_NAME_KEY

    return string.Template("""
<tr>
    <td>""" + containerFoxyDataDict[foxyPortNameKey] + """</td>
    <td>""" + port + """</td>
    <td>""" + containerFoxyDataDict[constants.DOCKER_PORT_KEY][port][constants.DOCKER_PORTS_HOST_IP_KEY] + 
                """ : """ + 
                containerFoxyDataDict[constants.DOCKER_PORT_KEY][port][constants.DOCKER_PORTS_HOST_PORT_KEY] + 
                """</td>
    <td>$ATTRIBUTES </td></tr>""")




# some lists have the '/tcp' tag on the port and some don't 
# until I get around to normalizing the data this kludge will have to do...
def get_foxy_port(port):
    return port.replace(constants.DOCKER_PORTS_VALUE_SUFFIX, '')



