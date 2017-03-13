"""Base class for a network endpoint.

This EndPoint class denotes a network endpoint or an endpoint.
This is a network interface capable of sending and/or receiving network traffic.
It represents a physical layer connection to another network interface.
Examples include a wifi network interface, ethernet, p2p links, cable modem's Docsis interface, etc.
In a graph, this represents a vertex capable of having edges to other endpoints.

"""
import dobby.nwmodel.phymodel as phymodel

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
    def __init__(self, phy_address=None, phy_model=None, ip_info=None, node_id=None, **kwargs):
        self.phy_address = phy_address
        self.phy_model = phy_model
        self.ip_infos = {}
        if ip_info:
            self.ip_infos[str(ip_info.ipv4address)] = ip_info
        self.node_id = node_id
        self.edges = []
        self.__dict__.update(kwargs)

    def add_link(self, edge):
        self.edges.add(edge)

    def add_or_update_ip_info(self, ip_info):
        self.ip_infos[str(ip_info.ipv4address)] = ip_info

    def update_node_info(self, node_id):
        self.node_id = node_id

    def update_phy_model(self, phy_model):
        self.phy_model = phy_model

    def update_phy_address(self, phy_address):
        self.phy_address = phy_address
