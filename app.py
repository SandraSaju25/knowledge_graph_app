import streamlit as st 
import streamlit.components.v1 as components  # For embedding custom HTML
from generate_knowledge_graph import generate_knowledge_graph

# Set up streamlit app configuration
st.set_page_config(
    page_icon=None,
    layout="wide",
    initial_sidebar_state="auto",
    menu_items=None,
)

# Set the title of the app
st.title("Knowledge Graph From Text")

# Sidebar section for user input method
st.sidebar.title("Input Document")
input_method = st.sidebar.radio(
    "Choose an input method:",
    ["Upload a file", "Enter a text"],
)

# Case 1: User uploads a file
if input_method == "Upload a file":
    # File uploader widget in the sidebar
    uploaded_file = st.sidebar.file_uploader(label="Upload file", type=["pdf", "docx", "txt"])

    if uploaded_file is not None:
        # Read the uploaded file content and decode it as utf-8
        text = uploaded_file.read().decode("utf-8")

        # Button to generate the knowledge graph
        if st.sidebar.button("Generate Knowledge Graph"):
            with st.spinner("Generating knowledge graph..."):
                net = generate_knowledge_graph(text)
                st.success("Knowledge graph generated successfully!")

                # Save the knowledge graph as an HMTL file
                output_file = "knowledge_graph.html"
                net.save_graph(output_file)

                # Open the HTML file and display it within the streamlit app
                HtmlFile = open(output_file, "r", encoding="utf-8")
                components.html(HtmlFile.read(), height=1000)

# Case 2: User enters a text
else:
    # Text area widget in the sidebar
    text = st.sidebar.text_area("Enter text", height=300)

    if text:
        if st.sidebar.button("Generate Knowledge Graph"):
            with st.spinner("Generating knowledge graph..."):
                net = generate_knowledge_graph(text)
                st.success("Knowledge graph generated successfully!")

                # Save the knowledge graph as an HMTL file
                output_file = "knowledge_graph.html"
                net.save_graph(output_file)

                # Open the HTML file and display it within the streamlit app
                HtmlFile = open(output_file, "r", encoding="utf-8")
                components.html(HtmlFile.read(), height=1000)



            