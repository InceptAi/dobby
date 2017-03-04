"""Base class for a node.
Node: A device that has multiple endpoints, such as a smartphone, laptop, a 
network router, gateway, cable modem etc. A node can either route or bridge packets 
or generate/consume them (via applications) or both.
"""
from __future__ import division
from copy import deepcopy
from collections import Counter
from enum import Enum, unique
import uuid

__author__ = """\n""".join(['Vivek Shrivastava (vivek@obiai.tech)'])

@unique
class NodeType(Enum):
  UNKNOWN = 0
  WIRELESS_ROUTER = 1
  BRIDGE = 2
  MODEM = 3
  SMARTPHONE = 4
  LAPTOP = 5
  TABLET = 6
  THERMOSTAT = 7
  CAMERA = 8
  GENERIC_IOT = 9
  SETTOPBOX = 10
  SERVER = 11
  DESKTOP = 12
  WIRELESS_CLIENT = 13
  ALL_GENERIC = 14

class Node(object):
    """
    Base class for a network node.

    Node: {
      Uint64 nodeId // Primary key: an ID for this node. Can be a random UUID.
        Endpoint endpoints[]  // a list of endpoints.
        InternalEdge internalEdges[] // list of internal edges bet endpoints above.
        // used to represent routing, bridging, firewalling,
        // port forwarding and other functionality between
        // two network interfaces belonging to the same Node.
        NodeType nodeType
        String nodeName // User visible name for this node:
        // Example: "Vivek's macbook".
        Apps appList[]; // A list of apps running on this node (optional).

    }
    """
    def __init__(self, endpoints=[], node_type=NodeType.UNKNOWN, node_name=None,
                 app_list=[], flow_list=[], **kwargs)
        #Generate a random uuid
        self.node_id = uuid.uuid4()
        self.node_type = node_type
        self.node_name = node_name
        self.endpoints = endpoints
        self.apps = app_list
        self.flows = flow_list
        self.update(kwargs)

    def add_endpoint(self, endpoints):
        self.endpoints.add(endpoints)

    def add_flows(self, flows):
        self.flows.add(endpoints)
