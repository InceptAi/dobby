import enum
__author__ = """\n""".join(['Vivek Shrivastava (vivek@obiai.tech)'])


MAX_STATS_LENGTH = 20


@enum.unique
class EdgeType(enum.Enum):
    UNKNOWN = 0
    PHYSICAL = 1
    BRIDGE = 2
    VIRTUAL = 3

def find_metrics(metrics_queue, ts):
    for metrics in list(reversed(metrics_queue)):
        if (ts <= metrics.start_ts and ts < metrics.end_ts):
            return metrics
    return None

class Edge(object):
    """
    Base class for edges in our model.
    Edge : {
      Edge {
        Endpoint A   // Pointer or reference to Endpoint labelled "A"
        Endpoint B   // Pointer or reference to Endpoint labelled "B"
        EdgeType edgeType // Type of edge -- by default set to PHYSICAL
        LinkMetrics AtoB  // link metrics for the traffic from A to B
        LinkMetrics BtoA  // link metrics for the traffic from B to A
        Metrics avgRTT, avgLatency, avgLoss // direction-less link metrics.
        PhyModel phyModel = if (A.phyModel.type == B.phyModel.type) ? A.phyModel : BRIDGE
        phyModel.mtu = min(A.phyModel.mtu, B.phyModel.mtu)
      }

    Parameters
    ----------
    See above
    attr : keyword arguments, optional (default= no attributes)
        Attributes to add to graph as key=value pairs.
    """
    def __init__(self, endpoint_a, endpoint_b, edge_type=EdgeType.UNKNOWN,
                 edge_metrics=None, edge_metrics_ab=None, edge_metrics_ba=None, **kwargs):
        self.endpoint_a = endpoint_a
        self.endpoint_b = endpoint_b
        self.edge_type = edge_type
        self.edge_metrics = edge_metrics
        self.edge_metrics_ab = edge_metrics_ab
        self.edge_metrics_ba = edge_metrics_ba
        self.__dict__.update(kwargs)


    def update_undirected_metrics(self, metrics):
        self.edge_metrics = metrics

    def update_metrics_ab(self, metrics_ab):
        self.edge_metrics_ab = metrics_ab

    def update_metrics_ba(self, metrics_ba):
        self.edge_metrics_ba = metrics_ba
