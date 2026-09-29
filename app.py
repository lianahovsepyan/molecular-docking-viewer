import streamlit as st
import pandas as pd
import py3Dmol
import os
import datetime
import streamlit.components.v1 as components

st.set_page_config(page_title="Molecular Docking SaaS", layout="wide")

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
            st.sidebar.error("Xندրում ենք լրացնել տվյալները։")
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
st.title("🧬 Մոլեկուլային դոկինգ և դեղերի հայտնաբերման SaaS")
st.markdown("Անվտանգ ամպային հարթակ PDB/SDF ֆայլերի կառավարման և դոկինգի համար։")

if not st.session_state.logged_in:
    st.warning("Մուտք գործեք կողային վահանակից՝ գործառույթները տեսնելու համար։")
    
    st.subheader("Հանրային դիտիչ (Public Demo)")
    def show_demo_viewer():
        viewer = py3Dmol.view(width=700, height=400)
        viewer.addModel(
            "ATOM      1  N   MET A   1     -12.288   5.093   2.138  1.00 16.48           N\n"
            "ATOM      2  CA  MET A   1     -11.411   4.108   2.730  1.00 15.65           C\n",
            "pdb"
        )
        viewer.setStyle({'cartoon': {'color': 'spectrum'}})
        viewer.zoomTo()
        return viewer._make_html()
    
    components.html(show_demo_viewer(), height=430)

else:
    tier = st.session_state.tier
    st.info(f"Մուտքը թույլատրված է ({tier} պլան):")

    if tier == "Free":
        st.warning("🔒 Անվճար պլանի սահմանափակում։")
    else:
        st.success("⚡ Pro հնարավորությունները ակտիվ են։")
        
        st.markdown("### 🧪 Նմուշային ֆայլերի արագ բեռնում (Built-in Samples)")
        use_sample = st.checkbox("Օգտագործել ներդրված նմուշային PDB և SDF ֆայլերը")
        
        if use_sample:
            protein_data = (
                "ATOM      1  N   MET A   1     -12.288   5.093   2.138  1.00 16.48           N\n"
                "ATOM      2  CA  MET A   1     -11.411   4.108   2.730  1.00 15.65           C\n"
                "ATOM      3  C   MET A   1     -10.021   4.622   3.029  1.00 14.89           C\n"
                "ATOM      4  O   MET A   1      -9.155   3.805   3.311  1.00 14.12           O\n"
                "ATOM      5  CB  MET A   1     -11.972   3.197   3.844  1.00 17.22           C\n"
            )
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
            protein_name = "sample_protein.pdb"
            ligand_name = "sample_ligand.sdf"
            st.info("✅ Նմուշային ֆայլերը հաջողությամբ բեռնվեցին հիշողության մեջ։")
        else:
            uploaded_protein = st.file_uploader("Upload Target Protein (PDB)", type=["pdb"])
            uploaded_ligand = st.file_uploader("Upload Ligand (SDF / PDB)", type=["sdf", "pdb"])
            protein_data = uploaded_protein.getvalue().decode("utf-8") if uploaded_protein else None
            ligand_data = uploaded_ligand.getvalue().decode("utf-8") if uploaded_ligand else None
            protein_name = uploaded_protein.name if uploaded_protein else None
            ligand_name = uploaded_ligand.name if uploaded_ligand else None

        if protein_data and ligand_data:
            if st.button("Run AutoDock Vina Calculation"):
                with st.spinner("Կատարվում է մոլեկուլային դոկինգի հաշվարկ..."):
                    import time
                    time.sleep(1.5)
                    affinity = "-9.2 kcal/mol"
                    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    
                    st.session_state.history.append({
                        "Time": timestamp,
                        "Protein": protein_name,
                        "Ligand": ligand_name,
                        "Affinity": affinity
                    })
                    
                st.success("Դոկինգն հաջողությամբ ավարտվեց!")
                st.metric(label="Estimated Binding Affinity", value=affinity)
                
                st.subheader("Docked Complex 3D View")
                result_viewer = py3Dmol.view(width=700, height=400)
                result_viewer.addModel(protein_data, "pdb")
                result_viewer.setStyle({'cartoon': {'color': 'lightgray'}})
                result_viewer.addModel(ligand_data, "sdf")
                result_viewer.setStyle({'stick': {'color': 'magenta'}})
                result_viewer.zoomTo()
                components.html(result_viewer._make_html(), height=430)
        
        if st.session_state.history:
            st.markdown("---")
            st.subheader("📋 Ձեր հաշվարկների պատմությունը (History)")
            history_df = pd.DataFrame(st.session_state.history)
            st.dataframe(history_df, use_container_width=True)
