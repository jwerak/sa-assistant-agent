import os
from diagrams import Diagram, Cluster, Edge
from diagrams.custom import Custom

ICON_DIR = os.path.expanduser("~/.agents/skills/generate-diagram/icons")

def icon(name):
    return os.path.join(ICON_DIR, f"{name}.png")

graph_attr = {
    "fontsize": "16",
    "fontname": "Red Hat Display, Overpass, sans-serif",
    "bgcolor": "white",
    "pad": "0.8",
    "nodesep": "0.8",
    "ranksep": "1.2",
    "splines": "ortho",
    "label": "Red Hat OpenShift AI – Air-gap nasazení\nWorkflow přenosu obrazů a modelů do odpojeného prostředí",
    "labelloc": "t",
    "labeljust": "c",
    "fontcolor": "#1A1A1A",
    "dpi": "200",
}

node_attr = {
    "fontsize": "11",
    "fontname": "Red Hat Text, Overpass, sans-serif",
    "fontcolor": "#1A1A1A",
    "imagescale": "true",
    "fixedsize": "true",
    "width": "1.3",
    "height": "1.3",
}

edge_attr = {
    "color": "#6A6E73",
    "fontsize": "9",
    "fontname": "Red Hat Text, Overpass, sans-serif",
    "fontcolor": "#6A6E73",
}

cluster_style = {
    "fontsize": "12",
    "fontname": "Red Hat Display, Overpass, sans-serif",
    "style": "rounded",
    "penwidth": "1.5",
}

with Diagram(
    "",
    filename="diagrams/mo_airgap_flow",
    show=False,
    direction="LR",
    graph_attr=graph_attr,
    node_attr=node_attr,
    edge_attr=edge_attr,
    outformat="png",
):
    # === Online zone ===
    with Cluster("Online zóna (připojená síť)", graph_attr={
        **cluster_style, "bgcolor": "#E3F2FD", "color": "#1565C0",
        "fontcolor": "#1565C0",
    }):
        rh_registry = Custom("Red Hat\nContainer\nCatalog", icon("container_registry"))
        hf_hub = Custom("HuggingFace\n/ Model Hub", icon("ai_ml"))
        oc_mirror = Custom("oc-mirror\n(příprava)", icon("container_platform"))
        modelcar_build = Custom("ModelCar\nOCI build", icon("containerized_app"))

    # === Transfer ===
    with Cluster("Přenosové médium", graph_attr={
        **cluster_style, "bgcolor": "#FFF3E0", "color": "#E65100",
        "fontcolor": "#E65100",
    }):
        media = Custom("Šifrovaný\nUSB / disk", icon("storage"))

    # === Firewall ===
    fw = Custom("Air-gap\nhranice", icon("firewall"))

    # === Offline zone ===
    with Cluster("Odpojené prostředí (air-gap)", graph_attr={
        **cluster_style, "bgcolor": "#FFEBEE", "color": "#EE0000",
        "fontcolor": "#EE0000",
    }):
        with Cluster("Mirror registry", graph_attr={
            **cluster_style, "bgcolor": "#FCE4EC", "color": "#C62828",
            "fontcolor": "#C62828",
        }):
            quay_mirror = Custom("Red Hat Quay\n(lokální)", icon("quay"))
            oc_mirror_load = Custom("oc-mirror\n(import)", icon("container_platform"))

        with Cluster("OpenShift cluster", graph_attr={
            **cluster_style, "bgcolor": "#FFF8E1", "color": "#F57F17",
            "fontcolor": "#F57F17",
        }):
            ocp_cluster = Custom("OpenShift\nPlatform", icon("openshift"))
            rhoai = Custom("OpenShift AI\n(RHOAI)", icon("openshift_ai"))
            kserve = Custom("KServe\nModel Serving", icon("microservices"))
            modelcar_deploy = Custom("ModelCar\ninit-container", icon("containerized_app"))
            gpu_nodes = Custom("GPU Nody\n(B300)", icon("gpu"))

    # === Edges: Online zone ===
    rh_registry >> Edge(label="oc-mirror", color="#1565C0") >> oc_mirror
    hf_hub >> Edge(label="OCI build", color="#1565C0") >> modelcar_build

    # Online → media
    oc_mirror >> Edge(label="tar archiv", color="#E65100") >> media
    modelcar_build >> Edge(label="OCI image", color="#E65100") >> media

    # Media → firewall → offline
    media >> Edge(label="fyzický\npřenos", color="#E65100", penwidth="2") >> fw
    fw >> Edge(color="#EE0000", penwidth="2") >> oc_mirror_load

    # Offline zone
    oc_mirror_load >> Edge(label="push", color="#C62828") >> quay_mirror
    quay_mirror >> Edge(label="operátory\n+ obrazy", color="#EE0000") >> ocp_cluster
    ocp_cluster >> Edge(color="#EE0000") >> rhoai
    rhoai >> Edge(color="#EE0000") >> kserve
    quay_mirror >> Edge(label="ModelCar\nOCI", color="#C62828", style="dashed") >> modelcar_deploy
    modelcar_deploy >> Edge(color="#F57F17") >> kserve
    kserve >> Edge(color="#F57F17") >> gpu_nodes
