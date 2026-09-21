import os
from diagrams import Diagram, Cluster, Edge
from diagrams.custom import Custom

ICON_DIR = os.path.expanduser("~/.agents/skills/generate-diagram/icons")

def icon(name):
    return os.path.join(ICON_DIR, f"{name}.png")

graph_attr = {
    "fontsize": "20",
    "fontname": "Red Hat Display, Overpass, sans-serif",
    "bgcolor": "white",
    "pad": "0.5",
    "nodesep": "0.6",
    "ranksep": "0.35",
    "splines": "false",
    "label": "Red Hat OpenShift AI – Architektura řešení (vrstvy 0–3)\nInfrastruktura a platforma",
    "labelloc": "t",
    "labeljust": "c",
    "fontcolor": "#1A1A1A",
    "compound": "true",
    "dpi": "200",
    "size": "11.7,8.3!",
    "ratio": "fill",
}

node_attr = {
    "fontsize": "11",
    "fontname": "Red Hat Text, Overpass, sans-serif",
    "fontcolor": "#1A1A1A",
    "imagescale": "true",
    "fixedsize": "true",
    "width": "1.2",
    "height": "1.2",
}

edge_attr = {
    "color": "#AAAAAA",
    "arrowsize": "0.7",
}

def layer_style(bgcolor, color):
    return {
        "fontsize": "13",
        "fontname": "Red Hat Display, Overpass, sans-serif",
        "style": "rounded,filled",
        "fillcolor": bgcolor,
        "color": color,
        "fontcolor": color,
        "penwidth": "1.5",
        "margin": "18",
    }

with Diagram(
    "",
    filename="diagrams/mo_arch_lower",
    show=False,
    direction="TB",
    graph_attr=graph_attr,
    node_attr=node_attr,
    edge_attr=edge_attr,
    outformat="png",
):

    with Cluster("Vrstva 3 – Observabilita                                                                     GA",
                 graph_attr=layer_style("#F3E5F5", "#7B1FA2")):
        obs3_1 = Custom("Prometheus\nMetriky", icon("opentelemetry"))
        obs3_2 = Custom("Grafana\nDashboards", icon("insights"))
        obs3_3 = Custom("MaaS Usage\nDashboard", icon("management"))
        obs3_4 = Custom("DCGM\nGPU metriky", icon("gpu"))

    with Cluster("Vrstva 2 – Platforma (OCP)                                                                GA",
                 graph_attr=layer_style("#FFEBEE", "#CC0000")):
        plt2_1 = Custom("OpenShift\nPlatform", icon("openshift"))
        plt2_2 = Custom("ACS\nSecurity", icon("acs"))
        plt2_3 = Custom("Quay\nRegistry", icon("quay"))
        plt2_4 = Custom("ACM\nManagement", icon("acm"))

    with Cluster("Vrstva 1 – GPU infrastruktura                                                             GA",
                 graph_attr=layer_style("#E0F2F1", "#00695C")):
        gpu1_1 = Custom("NVIDIA GPU\nOperator", icon("gpu"))
        gpu1_2 = Custom("Kueue\nScheduling", icon("load_balancer"))
        gpu1_3 = Custom("MIG\nPartitioning", icon("microservices"))
        gpu1_4 = Custom("NVLink /\nNVSwitch", icon("network"))

    with Cluster("Vrstva 0 – Hardware                                                                              ",
                 graph_attr=layer_style("#ECEFF1", "#37474F")):
        hw0_1 = Custom("GPU Servery\nNVIDIA B300", icon("server_stack"))
        hw0_2 = Custom("NVMe Storage\nODF", icon("storage"))
        hw0_3 = Custom("Síť\nCisco N9K", icon("network"))
        hw0_4 = Custom("Management\nnody", icon("server"))

    obs3_1 >> Edge(color="#7B1FA2") >> plt2_1
    plt2_1 >> Edge(color="#CC0000") >> gpu1_1
    gpu1_1 >> Edge(color="#00695C") >> hw0_1
