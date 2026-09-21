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
    "label": "Red Hat OpenShift AI – Architektura řešení (vrstvy 4–7)\nAI Appliance pro air-gap prostředí",
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
    filename="diagrams/mo_arch_upper",
    show=False,
    direction="TB",
    graph_attr=graph_attr,
    node_attr=node_attr,
    edge_attr=edge_attr,
    outformat="png",
):

    with Cluster("Vrstva 7 – AI Gateway / MaaS                                                             GA",
                 graph_attr=layer_style("#FCE4EC", "#CC0000")):
        gw7_1 = Custom("MaaS\nGovernance", icon("gateway"))
        gw7_2 = Custom("API Gateway\nKuadrant+Envoy", icon("api"))
        gw7_3 = Custom("OIDC / SSO\nRHBK", icon("sso"))
        gw7_4 = Custom("Rate Limiting\nToken kvóty", icon("secured"))

    with Cluster("Vrstva 6 – Inteligentní routing                                                           TP",
                 graph_attr=layer_style("#FFF3E0", "#E65100")):
        rt6_1 = Custom("llm-d\nKV-cache routing", icon("load_balancer"))
        rt6_2 = Custom("Sémantický router\n(upstream)", icon("network"))
        rt6_3 = Custom("Prioritní\nflow control", icon("secured"))
        rt6_4 = Custom("SLO-aware\nadmission", icon("management"))

    with Cluster("Vrstva 5 – Inference runtime                                                             GA",
                 graph_attr=layer_style("#E8F5E9", "#2E7D32")):
        inf5_1 = Custom("vLLM\nInference", icon("ai_ml"))
        inf5_2 = Custom("NeMo\nGuardrails", icon("secured"))
        inf5_3 = Custom("KServe\nModel Serving", icon("containerized_app"))
        inf5_4 = Custom("ModelCar\nOCI delivery", icon("container_registry"))

    with Cluster("Vrstva 4 – AI platforma (RHOAI)                                                       GA",
                 graph_attr=layer_style("#E3F2FD", "#1565C0")):
        ai4_1 = Custom("OpenShift AI\nRHOAI", icon("openshift_ai"))
        ai4_2 = Custom("MLflow\nTracking", icon("data"))
        ai4_3 = Custom("OGX / Llama Stack\nRAG & Agents", icon("microservices"))
        ai4_4 = Custom("Model\nCatalog", icon("catalog"))

    gw7_1 >> Edge(color="#CC0000") >> rt6_1
    rt6_1 >> Edge(color="#E65100") >> inf5_1
    inf5_1 >> Edge(color="#2E7D32") >> ai4_1
