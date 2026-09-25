import streamlit as st
import py3Dmol
import streamlit.components.v1 as components

st.set_page_config(page_title="PyMOL-style Docking Studio", layout="wide")

st.title("🧬 PyMOL-style Molecular Docking Studio")
st.sidebar.header("Կառավարման վահանակ")

# Load PDB file
try:
    with open("protein_clean.pdb", "r") as f:
        pdb_data = f.read()
except FileNotFoundError:
    st.error("Չհաջողվեց գտնել protein_clean.pdb ֆայլը այս պանակում։")
    st.stop()

# Sidebar controls
style = st.sidebar.selectbox(
    "Սպիտակուցի ոճը (Representation)",
    ["cartoon", "surface", "ball+stick", "licorice", "spacefill"]
)

color_scheme = st.sidebar.selectbox(
    "Սպիտակուցի գունավորում",
    ["chain", "spectrum", "element", "ss"]
)

show_ligand = st.sidebar.checkbox("Ցույց տալ լիգանդը (դեղին)", value=True)
spin = st.sidebar.checkbox("Պտտել մոդելը (Spin)", value=False)

st.subheader("Սպիտակուց-լիգանդ համալիրի 3D տեսք")

view = py3Dmol.view(width=800, height=600)
view.addModel(pdb_data, "pdb")

# 1. Apply main style to the whole structure
if style == "cartoon":
    view.setStyle({'cartoon': {'color': color_scheme}})
elif style == "surface":
    view.addSurface(py3Dmol.VDW, {'opacity': 0.7, 'color': color_scheme})
elif style == "ball+stick":
    view.setStyle({'stick': {}, 'sphere': {'scale': 0.3}})
elif style == "licorice":
    view.setStyle({'licorice': {}})
elif style == "spacefill":
    view.setStyle({'sphere': {}})

# 2. Highlight Ligand / Heteroatoms in distinct Yellow color securely
if show_ligand:
    view.addStyle({'hetflag': True}, {
        'stick': {'colorscheme': 'yellowCarbon', 'radius': 0.3},
        'sphere': {'scale': 0.4, 'color': 'gold'}
    })

view.zoomTo()
if spin:
    view.spin(True)
else:
    view.spin(False)

components.html(view._make_html(), height=600, width=800)
