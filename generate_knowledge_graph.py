from langchain_experimental.graph_transformers import LLMGraphTransformer
from langchain_core.documents import Document 
from langchain_openai import ChatOpenAI

from pyvis.network import Network
from dotenv import load_dotenv
import os
import asyncio

# Load .env file
load_dotenv()

# Get API key from environment variable
api_key = os.getenv("OPENAI_API_KEY")

# Initialize LLM instance
llm = ChatOpenAI(
    model_name="gpt-4o",
    openai_api_key=api_key,
    temperature=0,
)

# Initialize graph transformer instance
graph_transformer = LLMGraphTransformer(
    llm=llm,
)

# Extract graph data from input text
async def extract_graph_data(text: str) -> list:
    """
    Asynchronously extract graph data from input text using the graph transformer.

    Args:
        text (str): Input text to be processed into knowledge graph.
    
    Returns:
        list: A list of GraphDocument objects containing nodes and relationships.
    """
    documents = [Document(page_content=text)]
    graph_docs = await graph_transformer.aconvert_to_graph_documents(documents)
    return graph_docs

# Visualize knowledge graph
def visualize_graph(graph_docs: list) -> Network | None:
    """
    Visualizes a knowledge graph using PyVis based on the extracted graph documents.

    Args:
        graph_docs (list): A list of documents containing nodes and relationships.

    Returns:
        Network: A network object containing the graph object
    """
    # Create network
    net = Network(
        height="1200px",
        width="100%",
        directed=True,
        notebook=False,
        bgcolor="#222222",
        font_color="white",
        filter_menu=True,
        cdn_resources="remote",
    )

    nodes = graph_docs[0].nodes
    relationships = graph_docs[0].relationships

    # Build lookup for valid nodes
    node_dict = {node.id: node for node in nodes}

    # Filter out invalid edges and collect valid node IDs
    valid_edges = []
    valid_node_ids = set()
    for rel in relationships:
        if rel.source.id in node_dict and rel.target.id in node_dict:
            valid_edges.append(rel)
            valid_node_ids.update([rel.source.id, rel.target.id])

    # Add valid nodes to the graph
    for node_id in valid_node_ids:
        node = node_dict[node_id]
        try:
            net.add_node(node.id, label=node.id, title=node.type, group=node.type)
        except:
            continue  # Skip node if error occurs

    # Add valid edges to the graph
    for rel in valid_edges:
        try:
            net.add_edge(rel.source.id, rel.target.id, label=rel.type.lower())
        except:
            continue  # Skip edge if error occurs

    # Configure graph layout and physics
    net.set_options("""
        {
            "physics": {
                "forceAtlas2Based": {
                    "gravitationalConstant": -100,
                    "centralGravity": 0.01,
                    "springLength": 200,
                    "springConstant": 0.08
                },
                "minVelocity": 0.75,
                "solver": "forceAtlas2Based"
            }
        }
    """)

    output_file = "knowledge_graph.html"
    try:
        net.save_graph(output_file)
        print(f"Graph saved to {os.path.abspath(output_file)}")
        return net
    except Exception as e:
        print(f"Error saving graph: {e}")
        return None

def generate_knowledge_graph(text: str) -> Network | None:
    """
    Generates and visualizes a knowledge graph from input text

    Args:
        text (str): Input text to generate knowledge graph.

    Returns:
        Network: The visualized network graph object.
    """
    graph_docs = asyncio.run(extract_graph_data(text))
    net = visualize_graph(graph_docs)
    return net

