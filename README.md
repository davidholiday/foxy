# foxy
---
<br>


### what is? 

Foxy is a python-powered dashboard designed to make using [docker](https://www.docker.com) for local development easier. While there are many other dashboards available for docker, they are all focused primarily on the needs of dev-ops personnel running a cluster. A developer using docker to create a sandbox production environment on her workstation has different needs. Foxy meets those needs by providing meaningful information on what containers are available on the system, what ports are available on the containers, links to open any web-accesible services in the container, and the means to start/stop containers from the dashboard. Ports are displayed along with a name indicating what service it's attached to, and may be grouped together in the dash. For example, the Hadoop ecosystem has many constitutent technologies, HDFS, Hadoop, Spark, Yarn, etc., each of which has one or more network ports used to interact with the service. Foxy can group all of the ports for a given service together on the display so you don't have to hunt around for them.  
<br><br>

### how to use? 


#### associate meta-data with a docker file

The first thing you're going to need to do is associate metadata with the docker file you're planning on using to build your container. If you've already got a container(s), you can still use foxy to start, stop, or display the docker inspect report, but you won't be able to view the port resolution tables or have one-click access to available web services. 

Foxy metadata is associated with the *LABEL* tag in a dockerfile. Below is an example of what this might look like for a containerized cloudera cdh stack:

```
LABEL \
      #
      # group jupyter
          foxy.6666.name="notebook" \
          foxy.6666.group="jupyter" \
          foxy.6666.attribute="web" \
      #
      # group HDFS
          foxy.8020.name="NameNode" \
          foxy.8020.group="HDFS" \
      
          foxy.50470.name="NameNode HTTPS UI" \
          foxy.50470.group="HDFS" \
          foxy.50470.attribute="web" \
      
          foxy.50075.name="DataNode UI" \
          foxy.50075.group="HDFS" \
          foxy.50075.attribute="web" \
      #
      # group Yarn
          foxy.8088.name="Resource Manager UI" \
          foxy.8088.group="Yarn" \
          foxy.8088.attribute="web" \
      
          foxy.8042.name="Node Manager" \
          foxy.8042.group="Yarn" \
          foxy.8042.attribute="web" \
      
          foxy.8040.name="Node Manager Localizer" \
          foxy.8040.group="Yarn" \
      #    
      # group Spark
          foxy.4040.name="Local Client Driver HTTP UI" \
          foxy.4040.group="Spark" \
          foxy.4040.attribute="web" \
      #
      # group Hadoop
          foxy.19888.name="MapReduce JobHistory UI" \
          foxy.19888.group="Hadoop" \
          foxy.19888.attribute="web" \
      #
      # group ZooKeeper
          foxy.2181.name="ZooKeeper Client" \
          foxy.2181.group="ZooKeeper" \
      #
      # group Hue
          foxy.8888.name="Server" \
          foxy.8888.group="Hue" \
      #      
      # group Oozie
          foxy.11000.name="Server HTTP interface" \
          foxy.11000.group="Oozie" \
      #   
      # group Other
          foxy.9090.name="Linux Cockpit (todo)" \
          foxy.9090.group="Other" \
       
          foxy.11443.name="Dogtag Port" \
          foxy.11443.group="Other" \
       
          foxy.22.name="ssh" \
          foxy.22.group="Other" 
```
   
In docker files, the ```\``` character denotes a line-continuation and the ```#``` character denotes a commented line. Here's the breakdown of the metadata namespace:

* ```foxy``` is how foxy knows what metadata to parse. This is why you're able to co-locate foxy metadata along with whatever else you might need/want to put into your container. 
* ```name``` is the name you want to associate with this port. You can call it whatever you want.
* ```group``` the group you want to associate this port with. I haven't tested what happens if you try to associate a port with more than one group. It *should* work...
* ```attribute``` allows you to associate a tag with a port. If the attribute is 'web', foxy will automatically render the label as a button whose target is whatever ip:port on your host the port has been associated with. 



#### run foxy
Now that you've created your container, you'll need to fire up foxy. If you don't have the python >=2.7 and cherrypy installed, you'll need to do that first. 

* [Here are the instructions on how to install python](https://www.python.org/downloads/)
* [Here are the instructions on how to install cherrypy](http://docs.cherrypy.org/en/latest/install.html)

Once you everything installed, start foxy by executing the following script:
```
python ../foxy/Web/foxydriver.py
```
then navigate your favorite web browser to [localhost:1701](localhost:1701)

#### use foxy
Foxy will present you with a dashboard with a nav bar on top and a set of panels below; each panel representing a docker container. 

* Containers that are currently running will be highlighted blue wheras stopped containers will be grey.
* Below the container name will be a bar with three buttons. Here you can start/stop the container, view the ports table, or view the results of a ```docker inspect {container-name}``` command.
* If you make an out-of-band change to your docker environment (eg. build another container, remove a container, etc), simply refresh the foxy dash and foxy will pick up the changes. 
<br><br>

### known issues
* the search feature is currently in development and is non-functional.
* foxy needs to be packaged properly so that the user doesn't have to manually install cherrypy.
* if you create metadata for a given port number then don't expose that port, foxy freaks out. so, yeah, don't do that. 
* I'm pretty sure you can only associate one tag with a port.
* None of this has been unit tested.
* Currently you need to start foxy from within the ./foxy directory -- this is probably an artifact of my not having packaged this correctly yet... 
* when you click on the 'help' button nothing happens.

### todo
* add file explorer
* add drag/drop capability to file explorer
* add notification to user when web interfaces are online/go offline 
* add terminal shell


