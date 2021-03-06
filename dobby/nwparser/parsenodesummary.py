"""Base class for parsing summaries generated by click.
"""
import copy

import dobby.nwinfo.networksummary as networksummary
import dobby.nwmodel.endpoint as endpointmodel
import dobby.nwmodel.node as nodemodel
import dobby.nwmodel.ipinfo as ipinfo
import dobby.nwmodel.phymodel as phymodel
import dobby.nwmetrics.metrics as metrics
import dobby.utils.util as util

__author__ = """\n""".join(['Vivek Shrivastava (vivek@obiai.tech)'])

class ParseNodeSummary(object):
    """Parses node summary generated by click
    """
    def parse_summary(self, node_json, network_summary=None):
        # Create an empty summary if none was provided
        if not network_summary:
            network_summary = networksummary.NetworkSummary()
        else:
            network_summary = copy.copy(network_summary)
        #Iterate and update the endpoint stats
        for json_node in node_json['nodes']['node']:
            mac = json_node.get('@ether', None)
            vendor = json_node.get('@vendor', None)
            phy_addr = phymodel.PhysicalAddress(phy_address=mac, vendor=vendor)
            # See if this endpoint exists
            endpoint = network_summary.mac_to_endpoints.get(str(phy_addr), None)
            if endpoint:
                #Endpoint exists. Just update the vendor
                endpoint.phy_address.update_vendor(vendor)
            else:
                endpoint = endpointmodel.EndPoint(phy_addr)
                network_summary.mac_to_endpoints[str(phy_addr)] = endpoint
            # Check if a corresponding node exists
            if endpoint.node_id:
                node = network_summary.nodes.get(endpoint.node_id, None)
            else:
                # Create a node
                node = nodemodel.Node(endpoints=[endpoint], node_type=nodemodel.NodeType.UNKNOWN)
                endpoint.node_id = node.node_id
                network_summary.nodes[node.node_id] = node

            if json_node.get('ip', None):
                if (type(json_node['ip']) == dict):
                    ips_to_process = [json_node['ip']]
                else:
                    ips_to_process = json_node['ip']
                assert(type(ips_to_process) == list)
                for ip in ips_to_process:
                    ip_info = ipinfo.IPInfo(ipv4address=ip['@addr'], hostname=ip.get('hostname', None))
                    if node.node_type == nodemodel.NodeType.WIRELESS_ROUTER:
                        # Create an endpoint with ip_info -- assign it to the endpoint above if not AP
                        # TODO remove this hack -- IP-->MAC should be derived from ARP requests
                        ip_endpoint = endpointmodel.EndPoint(ip_info=ip_info)
                        ip_node = nodemodel.Node(endpoints=[ip_endpoint], node_type=nodemodel.NodeType.CLOUD_IP)
                        ip_endpoint.node_id = ip_node.node_id
                        network_summary.ip_to_endpoints[str(ip_info.ipv4address)] = ip_endpoint
                        network_summary.nodes[ip_node.node_id] = ip_node
                    else:
                        # Add to the MAC endpoint above
                        endpoint.add_or_update_ip_info(ip_info=ip_info)
                        network_summary.ip_to_endpoints[str(ip_info.ipv4address)] = endpoint
        return network_summary
