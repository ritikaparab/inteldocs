import fitz  # PyMuPDF for PDF extraction
import spacy  # NLP for Named Entity Recognition (NER)
import networkx as nx  # Graph generation
from pyvis.network import Network  # Visualization
from tkinter import Tk, filedialog

# Step 1: Select PDF File
def select_pdf():
    root = Tk()
    root.withdraw()  # Hide the GUI window
    file_path = filedialog.askopenfilename(title="Select a PDF File", filetypes=[("PDF Files", "*.pdf")])
    return file_path

pdf_path = select_pdf()
if not pdf_path:
    print("❌ No PDF selected. Exiting...")
    exit()

# Step 2: Extract Text from PDF
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)  # Open PDF
    text = ""
    for page in doc:
        text += page.get_text("text") + "\n"  # Extract text from pages
    return text.strip()

document_text = extract_text_from_pdf(pdf_path)
print("✔ PDF text extracted successfully!")

# Step 3: Load spaCy NLP Model
nlp = spacy.load("en_core_web_sm")

# Step 4: Extract Entities Using spaCy
def extract_entities(text):
    doc = nlp(text)
    entities = {}  # Dictionary to store entity relationships
    for ent in doc.ents:
        if ent.label_ not in entities:
            entities[ent.label_] = set()
        entities[ent.label_].add(ent.text)
    return entities

entities = extract_entities(document_text)

# Step 5: Create a Knowledge Graph
G = nx.Graph()

# Add Nodes for Entities
for entity_type, entity_names in entities.items():
    for name in entity_names:
        G.add_node(name, label=entity_type)

# Add Edges (Connecting related entities)
for entity_type, entity_names in entities.items():
    entity_list = list(entity_names)
    for i in range(len(entity_list)):
        for j in range(i + 1, len(entity_list)):
            G.add_edge(entity_list[i], entity_list[j])

# Step 6: Visualize the Knowledge Graph
graph_vis = Network(notebook=True, height="600px", width="100%", bgcolor="#222222", font_color="white")

for node in G.nodes:
    graph_vis.add_node(node, label=node, title=node, color="skyblue")

for edge in G.edges:
    graph_vis.add_edge(edge[0], edge[1])

# Save and display the graph
output_file = "knowledge_graph.html"
graph_vis.show(output_file)

print(f"✔ Knowledge graph generated! Open '{output_file}' in your browser.")
