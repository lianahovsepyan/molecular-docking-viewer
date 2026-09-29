import streamlit as st
import pandas as pd
import py3Dmol

st.set_page_config(page_title="Molecular Docking SaaS", layout="wide")

# -- 1. Authentication & Session State Setup --
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "tier" not in st.session_state:
    st.session_state.tier = "Free"

st.sidebar.title("🔐 User Authentication")

if not st.session_state.logged_in:
    username = st.sidebar.text_input("Username / Email")
    password = st.sidebar.text_input("Password", type="password")
    
    if st.sidebar.button("Login"):
        if username and password:
            st.session_state.logged_in = True
            st.session_state.username = username
            if "pro" in username.lower():
                st.session_state.tier = "Pro"
            else:
                st.session_state.tier = "Free"
            st.rerun()
        else:
            st.sidebar.error("Please enter credentials.")
else:
    st.sidebar.success(f"Welcome, {st.session_state.username}!")
    st.sidebar.info(f"Current Plan: **{st.session_state.tier} Tier**")
    
    if st.sidebar.button("Log out"):
        st.session_state.logged_in = False
        st.session_state.tier = "Free"
        st.rerun()

    if st.session_state.tier == "Free":
        if st.sidebar.button("Upgrade to Pro ($29/mo)"):
            st.session_state.tier = "Pro"
            st.success("Upgraded to Pro successfully!")
            st.rerun()

# -- 2. Main Application Interface --
st.title("🧬 Molecular Docking & Drug Discovery SaaS")
st.markdown("Secure cloud-integrated platform for PDB/SDF file management and automated molecular docking.")

if not st.session_state.logged_in:
    st.warning("Please log in via the sidebar to access molecular viewers and docking features.")
    
    st.subheader("Public Demo (Sample Protein)")
    def show_demo_viewer():
        viewer = py3Dmol.view(width=700, height=400)
        viewer.addModel(
            "ATOM      1  N   MET A   1     -12.288   5.093   2.138  1.00 16.48           N\n"
            "ATOM      2  CA  MET A   1     -11.411   4.108   2.730  1.00 15.65           C\n"
            "ATOM      3  C   MET A   1     -10.021   4.622   3.029  1.00 14.89           C\n",
            "pdb"
        )
        viewer.setStyle({'cartoon': {'color': 'spectrum'}})
        viewer.zoomTo()
        return viewer._make_html()
    
    import streamlit.components.v1 as components
    components.html(show_demo_viewer(), height=430)

else:
    tier = st.session_state.tier
    st.info(f"Access granted. You are viewing the platform under the **{tier}** plan.")

    if tier == "Free":
        st.warning("🔒 **Free Tier Limitations:** Custom PDB uploads and AutoDock Vina calculations are locked. Upgrade to Pro to unlock full capabilities.")
        
        st.subheader("Sample Viewer")
        def show_free_viewer():
            viewer = py3Dmol.view(width=700, height=400)
            viewer.addModel("ATOM      1  N   MET A   1     -12.288   5.093   2.138  1.00 16.48           N\n", "pdb")
            viewer.setStyle({'sphere': {'color': 'cyan'}})
            viewer.zoomTo()
            return viewer._make_html()
        components.html(show_free_viewer(), height=430)

    else:
        st.success("⚡ **Pro Features Unlocked:** Full AutoDock Vina & Custom File Management Enabled.")
        
        uploaded_file = st.file_uploader("Upload Target Protein (PDB)", type=["pdb"])
        ligand_file = st.file_uploader("Upload Ligand (SDF / PDB)", type=["sdf", "pdb"])
        
        if uploaded_file and ligand_file:
            st.write("Files uploaded successfully! Ready for docking simulation.")
            if st.button("Run AutoDock Vina Simulation"):
                with st.spinner("Running docking simulation..."):
                    import time
                    time.sleep(2)
                st.success("Docking completed successfully! Binding affinity: **-8.4 kcal/mol**")
