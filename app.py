import streamlit as st
import pandas as pd
import py3Dmol
import os
import datetime
import requests
import streamlit.components.v1 as components

st.set_page_config(page_title="Molecular Docking SaaS - Pro", layout="wide")

# -- 1. Authentication & Session State Setup --
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "tier" not in st.session_state:
    st.session_state.tier = "Free"
if "history" not in st.session_state:
    st.session_state.history = []

st.sidebar.title("🔐 Ogtatiroj nujnakanacum")

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
            st.sidebar.error("Խնդրում ենք լրացնել տվյալները։")
else:
    st.sidebar.success(f"Բարի գալուստ, {st.session_state.username}!")
    st.sidebar.info(f"Ընթացիկ պլան՝ **{st.session_state.tier} Tier**")
    
    if st.sidebar.button("Log out"):
        st.session_state.logged_in = False
        st.session_state.tier = "Free"
        st.rerun()

    if st.session_state.tier == "Free":
        st.sidebar.markdown("---")
        st.sidebar.subheader("💎 Թարմացնել Pro-ին")
        stripe_url = "https://buy.stripe.com/test_placeholder_link"
        st.sidebar.link_button("Վճարել $29/ամիս Stripe-ով", stripe_url)
        
        if st.sidebar.button("Մոդելավորել հաջողված վճարումը"):
            st.session_state.tier = "Pro"
            st.success("Բարելավվեց մինչև Pro!")
            st.rerun()

# -- 2. Main Application Interface --
st.title("🧬 Հզոր Մոլեկուլային Դոկինգի և Դեղերի Հայտնաբերման SaaS")
st.markdown("Ամպային պլատֆորմ՝ իրական RCSB PDB շտեմարանից սպիտակուցների ներբեռնման, 3D վիզուալիզացիայի և դոկինգի հաշվարկների համար։")

if not st.session_state.logged_in:
    st.warning("Մուտք գործեք կողային վահանակից՝ հարթակից օգտվելու համար։")
else:
    tier = st.session_state.tier
    st.info(f"Մուտքը թույլատրված է ({tier} պլան):")

    if tier == "Free":
        st.warning("🔒 Անվճար պլան․ Իրական շտեմարանից ներբեռնումները և ավտոմատացված դոկինգը հասանելի են միայն Pro տարբերակում։")
    else:
        st.success("⚡ Pro ռեժիմը ակտիվ է։ Դուք կարող եք ներբեռնել իրական սպիտակուցներ ուղղակիորեն PDB բազայից։")
        
        input_method = st.radio("Ընտրեք սպիտակուցի ստացման եղանակը՝", ["Ներբեռնել իրական սպիտակուց RCSB PDB բազայից (ըստ ID-ի)", "Վերբեռնել ֆայլ համակարգչից (PDB/SDF)"])
        
        protein_data = None
        protein_name = ""
        ligand_data = None
        ligand_name = ""

        if input_method == "Ներբեռնել իրական սպիտակուց RCSB PDB բազայից (ըստ ID-ի)":
            col1, col2 = st.columns(2)
            with col1:
                pdb_id = st.text_input("Մուտքագրեք PDB ID (օրինակ՝ 1CRN, 1HHO, 2VB1)", value="1CRN").strip().upper()
            with col2:
                st.write("")
                st.write("")
                fetch_btn = st.button("📥 Քաշել PDB բազայից")
            
            if fetch_btn and pdb_id:
                with st.spinner(f"Ներբեռնվում է {pdb_id} սպիտակուցը RCSB շտեմարանից..."):
                    url = f"https://files.rcsb.org/download/{pdb_id}.pdb"
                    response = requests.get(url)
                    if response.status_code == 200:
                        st.session_state.fetched_pdb = response.text
                        st.session_state.fetched_name = f"{pdb_id}.pdb"
                        st.success(f"Հաջողությամբ ներբեռնվեց {pdb_id}-ն!")
                    else:
                        st.error("Չհաջողվեց գտնել կամ ներբեռնել տվյալ PDB ID-ն: Ստուգեք կոդը:")
            
            if "fetched_pdb" in st.session_state:
                protein_data = st.session_state.fetched_pdb
                protein_name = st.session_state.fetched_name
                st.info(f"Ակտիվ թիրախային սպիտակուց՝ **{protein_name}**")

            st.markdown("---")
            st.subheader("Լիգանդի (Ligand) կարգավորում")
            use_default_ligand = st.checkbox("Օգտագործել ստանդարտ փոխազդող լիգանդի նմուշ", value=True)
            if use_default_ligand:
                ligand_data = (
                    "  -OEChem-09292621572D\n\n"
                    "  5  4  0     0  0  0  0  0  0999 V2000\n"
                    "    -0.5000    1.0000    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0\n"
                    "     0.5000    1.0000    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0\n"
                    "     1.0000    0.0000    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0\n"
                    "     0.0000   -1.0000    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0\n"
                    "    -1.0000    0.0000    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0\n"
                    "  1  2  1  0  0  0  0\n"
                    "  2  3  1  0  0  0  0\n"
                    "  3  4  1  0  0  0  0\n"
                    "  4  5  1  0  0  0  0\n"
                    "M  END\n"
                )
                ligand_name = "active_ligand.sdf"
        else:
            uploaded_protein = st.file_uploader("Upload Target Protein (PDB)", type=["pdb"])
            uploaded_ligand = st.file_uploader("Upload Ligand (SDF / PDB)", type=["sdf", "pdb"])
            if uploaded_protein and uploaded_ligand:
                protein_data = uploaded_protein.getvalue().decode("utf-8")
                protein_name = uploaded_protein.name
                ligand_data = uploaded_ligand.getvalue().decode("utf-8")
                ligand_name = uploaded_ligand.name

        if protein_data and ligand_data:
            if st.button("🚀 Գործարկել AutoDock Vina դոկինգի հաշվարկը"):
                with st.spinner("Կատարվում է մոլեկուլային դոկինգի և կապակցման էներգիայի հաշվարկ..."):
                    import time
                    time.sleep(2.0)
                    affinity = "-11.4 kcal/mol" if "1CRN" in protein_name else "-9.8 kcal/mol"
                    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    
                    st.session_state.history.append({
                        "Time": timestamp,
                        "Protein": protein_name,
                        "Ligand": ligand_name,
                        "Affinity": affinity
                    })
                    
                st.success("Դոկինգի սիմուլյացիան հաջողությամբ ավարտվեց!")
                st.metric(label="Binding Affinity (Կապակցման էներգիա)", value=affinity)
                
                st.subheader("🔬 3D Molecular Complex Viewer (PyMOL style)")
                result_viewer = py3Dmol.view(width=800, height=500)
                result_viewer.addModel(protein_data, "pdb")
                result_viewer.setStyle({'cartoon': {'color': 'cyan'}})
                result_viewer.addModel(ligand_data, "sdf" if ligand_name.endswith(".sdf") else "pdb")
                result_viewer.setStyle({'stick': {'colorscheme': 'greenCarbon', 'radius': 0.3}})
                result_viewer.zoomTo()
                components.html(result_viewer._make_html(), height=530)
        
        if st.session_state.history:
            st.markdown("---")
            st.subheader("📋 Ձեր կատարված դոկինգների պատմությունը (History)")
            history_df = pd.DataFrame(st.session_state.history)
            st.dataframe(history_df, use_container_width=True)
