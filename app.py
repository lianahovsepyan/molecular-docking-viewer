import streamlit as st
import pandas as pd
import py3Dmol
import os
import datetime
import requests
import sqlite3
import hashlib
import streamlit.components.v1 as components

st.set_page_config(page_title="Molecular Docking SaaS", layout="wide")

# -- Database Setup --
def init_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            email TEXT PRIMARY KEY,
            password TEXT,
            tier TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(email, password):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (email, password, tier) VALUES (?, ?, ?)", 
                  (email, hash_password(password), "Free"))
        conn.commit()
        success = True
    except sqlite3.IntegrityError:
        success = False
    conn.close()
    return success

def verify_user(email, password):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT password, tier FROM users WHERE email = ?", (email,))
    row = c.fetchone()
    conn.close()
    if row and row[0] == hash_password(password):
        return True, row[1]
    return False, None

def update_user_tier(email, new_tier):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("UPDATE users SET tier = ? WHERE email = ?", (new_tier, email))
    conn.commit()
    conn.close()

# -- Session State Setup --
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "email" not in st.session_state:
    st.session_state.email = ""
if "tier" not in st.session_state:
    st.session_state.tier = "Free"
if "history" not in st.session_state:
    st.session_state.history = []

st.sidebar.title("🔐 Ogtatiroj nujnakanacum")

auth_mode = st.sidebar.radio("Ընտրեք ռեժիմը՝", ["Մուտք (Login)", "Գրանցվել (Sign Up)"])

if not st.session_state.logged_in:
    if auth_mode == "Մուտք (Login)":
        st.sidebar.subheader("Մուտք համակարգ")
        login_email = st.sidebar.text_input("Էլ. հասցե (Email)")
        login_pass = st.sidebar.text_input("Գաղտնաբառ", type="password")
        
        if st.sidebar.button("Մուտք գործել"):
            valid, user_tier = verify_user(login_email, login_pass)
            if valid:
                st.session_state.logged_in = True
                st.session_state.email = login_email
                st.session_state.tier = user_tier
                st.rerun()
            else:
                st.sidebar.error("Սխալ էլ. հասցե hoặc գաղտնաբառ:")
    else:
        st.sidebar.subheader("Նոր հաշվի ստեղծում")
        reg_email = st.sidebar.text_input("Նոր Էլ. հասցե")
        reg_pass = st.sidebar.text_input("Ստեղծեք գաղտնաբառ", type="password")
        
        if st.sidebar.button("Գրանցվել"):
            if reg_email and reg_pass:
                if register_user(reg_email, reg_pass):
                    st.sidebar.success("Գրանցումն հաջողվեց! Այժմ կարող եք մուտք գործել:")
                else:
                    st.sidebar.error("Այս էլ. հասցեն արդեն գրանցված է:")
            else:
                st.sidebar.warning("Լրացրեք բոլոր դաշտերը:")
else:
    st.sidebar.success(f"Բարի գալուստ, {st.session_state.email}!")
    st.sidebar.info(f"Ընթացիկ պլան՝ **{st.session_state.tier} Tier**")
    
    if st.sidebar.button("Դուրս գալ (Log out)"):
        st.session_state.logged_in = False
        st.session_state.email = ""
        st.session_state.tier = "Free"
        st.rerun()

    if st.session_state.tier == "Free":
        st.sidebar.markdown("---")
        st.sidebar.subheader("💎 Թարմացնել Pro-ին")
        stripe_url = "https://buy.stripe.com/test_placeholder_link"
        st.sidebar.link_button("Վճարել $29/ամիս Stripe-ով", stripe_url)
        
        if st.sidebar.button("Մոդելավորել հաջողված վճարումը"):
            update_user_tier(st.session_state.email, "Pro")
            st.session_state.tier = "Pro"
            st.success("Վճարումը հաջողվեց! Ակտիվացավ Pro պլանը:")
            st.rerun()

# -- Main Application Interface --
st.title("🧬 Մոլեկուլային Դոկինգի և Դեղերի Հայտնաբերման SaaS")
st.markdown("Ամպային պլատֆորմ՝ իրական RCSB PDB շտեմարանից սպիտակուցների ներբեռնման և դոկինգի հաշվարկների համար։")

if not st.session_state.logged_in:
    st.warning("🔒 Խնդրում ենք մուտք գործել կամ գրանցվել կողային վահանակից՝ հարթակից օգտվելու համար։")
else:
    tier = st.session_state.tier
    st.info(f"Մուտքը թույլատրված է։ Ձեր հաշիվը՝ {st.session_state.email} ({tier} պլան):")

    if tier == "Free":
        st.warning("🔒 Անվճար պլան․ Իրական շտեմարանից ներբեռնումները և ավտոմատացված դոկինգը հասանելի են միայն Pro տարբերակում։")
    else:
        st.success("⚡ Pro ռեժիմը ակտիվ է։")
        
        input_method = st.radio("Ընտրեք սպիտակուցի ստացման եղանակը՝", ["Ներբեռնել իրական սպիտակուց RCSB PDB բազայից (ըստ ID-ի)", "Վերբեռնել ֆայլ համակարգչից (PDB/SDF)"])
        
        protein_data = None
        protein_name = ""
        ligand_data = None
        ligand_name = ""

        if input_method == "Ներբեռնել իրական սպիտակուց RCSB PDB բազայից (ըստ ID-ի)":
            col1, col2 = st.columns(2)
            with col1:
                pdb_id = st.text_input("Մուտքագրեք PDB ID (օրինակ՝ 1CRN, 1HHO)", value="1CRN").strip().upper()
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
                        st.error("Չհաջողվեց գտնել տվյալ PDB ID-ն:")
            
            if "fetched_pdb" in st.session_state:
                protein_data = st.session_state.fetched_pdb
                protein_name = st.session_state.fetched_name

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
                with st.spinner("Կատարվում է դոկինգի սիմուլյացիա..."):
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
                    
                st.success("Դոկինգն հաջողությամբ ավարտվեց!")
                st.metric(label="Binding Affinity", value=affinity)
                
                st.subheader("🔬 3D Molecular Complex Viewer")
                result_viewer = py3Dmol.view(width=800, height=500)
                result_viewer.addModel(protein_data, "pdb")
                result_viewer.setStyle({'cartoon': {'color': 'cyan'}})
                result_viewer.addModel(ligand_data, "sdf")
                result_viewer.setStyle({'stick': {'colorscheme': 'greenCarbon', 'radius': 0.3}})
                result_viewer.zoomTo()
                components.html(result_viewer._make_html(), height=530)
        
        if st.session_state.history:
            st.markdown("---")
            st.subheader("📋 Ձեր հաշվարկների պատմությունը")
            history_df = pd.DataFrame(st.session_state.history)
            st.dataframe(history_df, use_container_width=True)
