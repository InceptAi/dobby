"""Base class for a App like youtube etc.

"""
from __future__ import division
from copy import deepcopy
from collections import Counter
from enum import Enum, unique

__author__ = """\n""".join(['Vivek Shrivastava (vivek@obiai.tech)'])

@unique
class AppType(Enum):
    UNKNOWN = 0
    BROWSER = 1
    STREAMING_VIDEO = 2
    STREAMING_AUDIO = 3
    VIDEO_CONF = 4
    AUDIO_CONF = 5
    DOWNLOAD = 6 
    FTP = 7
    INTERACTIVE = 8
    GAMING = 9

class NetworkApp(object):
    """
    Base class for a App.
    This list contains all user visible “applications”. Definition of an 
    application is anything that the user can see/interact with. Examples, 
    include Browser, Streaming applications, mobile apps, Nest remote, Alexa, 
    Google Home etc. 


    App: {
        Name appName //Generic name of the app if any
        AppType appType
        Node node  // Node where the application is running.
        Set<Flow> flows // Set of flows representing this application.
    }
    """
    def __init__(self, app_name=None, app_type=AppType.UNKNOWN, nodes=[], flows=[], **attr)
        self.app_type = app_type
        self.app_name = app_name
        self.flows = flows
        self.nodes = nodes
        self.app_metadata.update(attr)

    def add_flows(self, flows):
        self.flows.add(flows) 
    
    def add_nodes(self, nodes):
        self.nodes.add(nodes) 
