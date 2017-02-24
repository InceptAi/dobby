#!/usr/bin/env python3
"""Utility class for a network addresses.

This EndPoint class denotes a network endpoint or an endpoint.
This is a network interface capable of sending and/or receiving network traffic. 
It represents a physical layer connection to another network interface. 
Examples include a wifi network interface, ethernet, p2p links, cable modem's Docsis interface, etc. 
In a graph, this represents a vertex capable of having edges to other endpoints.

"""
from __future__ import division
from copy import deepcopy
import ipaddress

__author__ = """\n""".join(['Vivek Shrivastava (vivek@obiai.tech)'])


class IPInfo(object):
    """
    Base class for IPAddress.

    IPInfo : {
      IPv4Address ipv4Address;
      IPv6Address ipv6Address;
      IPv4Address gwv4address;
      IPv6Address gwv6address;
      int netmask; // int is inifinte precision in python 3 -- serves our purpose
    }

    """

    def __init__(self, ipv4address=None, ipv6address=None, gwv4address=None, gwv6address=None, netmask=0, **attr):
        """Initialize an address and its attributes.
        Parameters
        ----------
        ipv4Address : input IPv4 Address 
        ipv6Address : input IPv6 Address
        gwv4address : gateway IPv4 Address
        gwv6address : gateway IPv6 Address
        netmask     : netmask for IP Address, useful for routing
        bitmask     : bitmask for storing misc information like is_routable
        attr : keyword arguments, optional (default= no attributes)
          Attributes to add to graph as key=value pairs.

        """
        self.ip_metadata = {}   
        self.ipv4address = ipaddress.IPv4Address('ipv4address')
        self.ipv6address = ipaddress.IPv6Address('ipv6address')
        self.gwv4address = ipaddress.IPv4Address('gwv4address')
        self.gwv6address = ipaddress.IPv6Address('gwv6address')
        self.netmask = netmask 
        self.ip_metadata.update(attr)

    def update_properties(self, n, **attr):
        """Update IP properties.
        """
        self.ip_metadata.update(attr)


