"""Base class for a network endpoint.

This EndPoint class denotes a network endpoint or an endpoint.
This is a network interface capable of sending and/or receiving network traffic. 
It represents a physical layer connection to another network interface. 
Examples include a wifi network interface, ethernet, p2p links, cable modem's Docsis interface, etc. 
In a graph, this represents a vertex capable of having edges to other endpoints.

"""
from __future__ import division
from copy import deepcopy
from collections import Counter

__author__ = """\n""".join(['Vivek Shrivastava (vivek@obiai.tech)'])


class EndPoint(object):
    """
    Base class for network endpoints.
    Endpoint : {
      PhyAddress phyAddress   // uint64 (should be enough to hold any address)
      PhyModel phyModel   // Reference to an instance of a physical layer network model.
      IpAddress ipAddress // optional field, can be null if non-existent. This includes a 
                          // Netmask and a Router/Gateway address.
      Edge edges[]      // List of links from this endpoint.
    }


    Parameters
    ----------
    phyAddress : input physical address (of class PhyAddress)

    phyModel : input model for the physical layer
    ipAddress : ipAddress of the device if present
    attr : keyword arguments, optional (default= no attributes)
        Attributes to add to graph as key=value pairs.
    """
    def __init__(self, phy_address, phy_model, ip_address, **attr)
        self.phy_address = phy_address
        self.phy_model = phy_model
        self.ip_address = ip_address
        self.links = []


    def add_link(self, link):
        self.links.add(link) 

