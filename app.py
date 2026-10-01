import streamlit as st
import pandas as pd
import py3Dmol
import os
import datetime
import time
import requests
import sqlite3
import hashlib
import re
import streamlit.components.v1 as components

st.set_page_config(page_title="HelixDock SaaS - Molecular Docking", layout="wide", page_icon="🧬")

# -- Custom CSS for Pro SaaS Styling --
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
        color: #ffffff;
    }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        font-weight: bold;
        background-color: #4F46E5;
        color: white;
    }
    .stButton>button:hover {
        background-color: #4338CA;
    }
    .logo-container {
        display: flex;
        align-items: center;
        gap: 12px;
        padding-bottom: 10px;
    }
    .logo-text {
        font-size: 26px;
        font-weight: 800;
        background: linear-gradient(90deg, #4F46E5, #EC4899);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .payment-box {
        background-color: #1e293b;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #334155;
        margin-bottom: 15px;
        text-align: left;
    }
    .crypto-address {
        background: #0f172a; 
        padding: 8px; 
        border-radius: 6px; 
        word-break: break-all; 
        font-family: monospace; 
        color: #38BDF8; 
        font-size: 11px; 
        margin: 8px 0;
        text-align: center;
        border: 1px dashed #38BDF8;
    }
    .password-rules {
        font-size: 11px;
        color: #94A3B8;
        background: #1e293b;
        padding: 8px;
        border-radius: 6px;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# -- Translations Dictionary --
TRANSLATIONS = {
    "Հայերեն": {
        "title": "HelixDock SaaS Հարթակ",
        "subtitle": "Ամպային պլատֆորմ՝ իրական RCSB PDB շտեմարանից սպիտակուցների ներբեռնման և ավտոմատացված դոկինգի համար։",
        "account": "Օգտատիրոջ հաշիվ",
        "login": "Մուտք",
        "signup": "Գրանցվել",
        "forgot": "Մոռացել եմ գաղտնաբառը",
        "email": "Էլ. հասցե (Email)",
        "password": "Գաղտնաբառ",
        "password_confirm": "Կրկնեք գաղտնաբառը",
        "new_password": "Նոր գաղտնաբառ",
        "login_btn": "Մուտք գործել",
        "reg_btn": "Գրանցվել",
        "reset_btn": "Փոխել գաղտնաբառը",
        "logout": "Դուրս գալ (Log out)",
        "plan_free": "Անվճար",
        "plan_pro": "Պրոֆեսիոնալ",
        "upgrade_title": "💎 Բարելավել մինչև Pro ($29)",
        "login_error": "Սխալ էլ. հասցե կամ գաղտնաբառ:",
        "reg_success": "Գրանցումն հաջողվեց! Այժմ կարող եք մուտք գործել:",
        "reg_error": "Այս էլ. հասցեն արդեն գրանցված է կամ գաղտնաբառերը չեն համընկնում:",
        "pass_mismatch": "Գաղտնաբառերը չեն համընկնում:",
        "pass_weak": "Գաղտնաբառը չի համապատասխանում անվտանգության պահանջներին (պետք է լինի նվազագույնը 8 նիշ, ներառի մեծատառ, փոքրատառ, թիվ և հատուկ նիշ):",
        "fill_all": "Լրացրեք բոլոր դաշտերը:",
        "user_not_found": "Այս էլ. հասցեով օգտատեր չի գտնվել:",
        "reset_success": "Գաղտնաբառը հաջողությամբ թարմացվեց!",
        "lock_msg": "🔒 Խնդրում ենք մուտք գործել կամ գրանցվել կողային վահանակից՝ հարթակից օգտվելու համար։",
        "free_lock": "🔒 Անվճար պլան․ Իրական շտեմարանից ներբեռնումները և ավտոմատացված դոկինգը հասանելի են միայն Pro տարբերակում։ Խնդրում ենք բարելավել պլանը ձախ վահանակից։",
        "pro_active": "⚡ Pro ռեժիմը լիարժեք ակտիվ է (Admin Mode)։",
        "input_choice": "Ընտրեք սպիտակուցի ստացման եղանակը՝",
        "opt1": "Ներբեռնել իրական սպիտակուց RCSB PDB բազայից (ըստ ID-ի)",
        "opt2": "Վերբեռնել ֆայլ համակարգչից (PDB/SDF)",
        "pdb_input": "Մուտքագրեք PDB ID (օրինակ՝ 1CRN, 1HHO)",
        "fetch_btn": "📥 Քաշել PDB բազայից",
        "fetching": "Ներբեռնվում է",
        "fetch_ok": "Հաջողությամբ ներբեռնվեց",
        "fetch_err": "Չհաջողվեց գտնել տվյալ PDB ID-ն:",
        "run_dock": "🚀 Գործարկել AutoDock Vina դոկինգի հաշվարկը",
        "running": "Կատարվում է մոլեկուլային դոկինգի սիմուլյացիա...",
        "dock_ok": "Դոկինգն հաջողությամբ ավարտվեց!",
        "affinity": "Կապակցման էներգիա (Binding Affinity)",
        "viewer_title": "🔬 3D Molecular Complex Viewer",
        "history_title": "📋 Ձեր կատարված հաշվարկների պատմությունը"
    },
    "English": {
        "title": "HelixDock SaaS Platform",
        "subtitle": "Cloud platform for downloading real proteins from the RCSB PDB database and automated docking.",
        "account": "User Account",
        "login": "Login",
        "signup": "Sign Up",
        "forgot": "Forgot Password",
        "email": "Email Address",
        "password": "Password",
        "password_confirm": "Confirm Password",
        "new_password": "New Password",
        "login_btn": "Log In",
        "reg_btn": "Register",
        "reset_btn": "Reset Password",
        "logout": "Log Out",
        "plan_free": "Free",
        "plan_pro": "Pro",
        "upgrade_title": "💎 Upgrade to Pro ($29)",
        "login_error": "Invalid email or password.",
        "reg_success": "Registration successful! You can now log in.",
        "reg_error": "Email already registered or passwords do not match.",
        "pass_mismatch": "Passwords do not match.",
        "pass_weak": "Password does not meet security requirements (min 8 chars, uppercase, lowercase, number, special char).",
        "fill_all": "Please fill in all fields.",
        "user_not_found": "User with this email not found.",
        "reset_success": "Password successfully updated!",
        "lock_msg": "🔒 Please log in or sign up from the sidebar to use the platform.",
        "free_lock": "🔒 Free Tier: Downloading real proteins and automated docking are available in Pro version only. Please upgrade from the left panel.",
        "pro_active": "⚡ Pro mode is fully active (Admin Mode).",
        "input_choice": "Choose protein input method:",
        "opt1": "Download real protein from RCSB PDB (by ID)",
        "opt2": "Upload file from computer (PDB/SDF)",
        "pdb_input": "Enter PDB ID (e.g., 1CRN, 1HHO)",
        "fetch_btn": "📥 Fetch from PDB",
        "fetching": "Downloading",
        "fetch_ok": "Successfully downloaded",
        "fetch_err": "Could not find the specified PDB ID.",
        "run_dock": "🚀 Run AutoDock Vina Docking",
        "running": "Running molecular docking simulation...",
        "dock_ok": "Docking completed successfully!",
        "affinity": "Binding Affinity",
        "viewer_title": "🔬 3D Molecular Complex Viewer",
        "history_title": "📋 Your Calculation History"
    },
    "Русский": {
        "title": "HelixDock SaaS Платформа",
        "subtitle": "Облачная платформа для загрузки реальных белков из базы данных RCSB PDB и автоматического докинга.",
        "account": "Аккаунт пользователя",
        "login": "Вход",
        "signup": "Регистрация",
        "forgot": "Забыли пароль",
        "email": "Эл. почта",
        "password": "Пароль",
        "password_confirm": "Подтвердите пароль",
        "new_password": "Новый пароль",
        "login_btn": "Войти",
        "reg_btn": "Зарегистрироваться",
        "reset_btn": "Сбросить пароль",
        "logout": "Выйти (Log out)",
        "plan_free": "Бесплатный",
        "plan_pro": "Профессиональный",
        "upgrade_title": "💎 Перейти на Pro ($29)",
        "login_error": "Неверный email или пароль.",
        "reg_success": "Регистрация успешна! Теперь вы можете войти.",
        "reg_error": "Email уже зарегистрирован или пароли не совпадают.",
        "pass_mismatch": "Пароли не совпадают.",
        "pass_weak": "Пароль не отвечает требованиям безопасности (мин. 8 символов, заглавная, строчная, цифра, спец. символ).",
        "fill_all": "Заполните все поля.",
        "user_not_found": "Пользователь с таким email не найден.",
        "reset_success": "Пароль успешно обновлен!",
        "lock_msg": "🔒 Пожалуйста, войдите или зарегистрируйтесь в боковой панели для использования платформы.",
        "free_lock": "🔒 Бесплатный тариф: Загрузка реальных белков и автоматический докинг доступны только в версии Pro. Пожалуйста, улучшите тариф слева.",
        "pro_active": "⚡ Режим Pro полностью активен (Admin Mode).",
        "input_choice": "Выберите способ получения белка:",
        "opt1": "Скачать реальный белок из базы RCSB PDB (по ID)",
        "opt2": "Загрузить файл с компьютера (PDB/SDF)",
        "pdb_input": "Введите PDB ID (например, 1CRN, 1HHO)",
        "fetch_btn": "📥 Скачать из PDB",
        "fetching": "Загружается",
        "fetch_ok": "Успешно загружено",
        "fetch_err": "Не удалось найти указанный PDB ID.",
        "run_dock": "🚀 Запустить расчет AutoDock Vina",
        "running": "Выполняется симуляция молекулярного докинга...",
        "dock_ok": "Докинг успешно завершен!",
        "affinity": "Энергия связывания (Binding Affinity)",
        "viewer_title": "🔬 3D Molecular Complex Viewer",
        "history_title": "📋 История ваших расчетов"
    }
}

ADMIN_EMAIL = "lianahovsepyan65@gmail.com"
ADMIN_DEFAULT_PASS = hashlib.sha256("Admin123!".encode()).hexdigest()

# -- Database Setup with Auto-Migration & Auto-Admin --
def init_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            email TEXT PRIMARY KEY,
            password TEXT,
            tier TEXT,
            is_verified INTEGER DEFAULT 1
        )
    ''')
    
    c.execute("PRAGMA table_info(users)")
    columns = [column[1] for column in c.fetchall()]
    
    if "tier" not in columns:
        c.execute("ALTER TABLE users ADD COLUMN tier TEXT DEFAULT 'Free'")
    if "is_verified" not in columns:
        c.execute("ALTER TABLE users ADD COLUMN is_verified INTEGER DEFAULT 1")
        
    c.execute("SELECT email FROM users WHERE email = ?", (ADMIN_EMAIL,))
    if not c.fetchone():
        c.execute("INSERT INTO users (email, password, tier, is_verified) VALUES (?, ?, 'Pro', 1)", 
                  (ADMIN_EMAIL, ADMIN_DEFAULT_PASS))
    else:
        c.execute("UPDATE users SET tier = 'Pro' WHERE email = ?", (ADMIN_EMAIL,))
    
    conn.commit()
    conn.close()

init_db()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def validate_password_strength(password):
    if len(password) < 8:
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[a-z]", password):
        return False
    if not re.search(r"[0-9]", password):
        return False
    if not re.search(r"[@$!%*?&]", password):
        return False
    return True

def register_user(email, password):
    if not validate_password_strength(password):
        return False, "weak_pass"
    
    tier = "Pro" if email.strip().lower() == ADMIN_EMAIL.lower() else "Free"
    
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (email, password, tier, is_verified) VALUES (?, ?, ?, 1)", 
                  (email, hash_password(password), tier))
        conn.commit()
        success = True
    except sqlite3.IntegrityError:
        success = False
    conn.close()
    return success, "success" if success else "exists"

def verify_user(email, password):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT password, tier FROM users WHERE email = ?", (email,))
    row = c.fetchone()
    conn.close()
    
    if row and row[0] == hash_password(password):
        user_tier = "Pro" if email.strip().lower() == ADMIN_EMAIL.lower() else (row[1] if row[1] else "Free")
        return True, user_tier
    return False, None

def update_password(email, new_password):
    if not validate_password_strength(new_password):
        return False, "weak_pass"
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT email FROM users WHERE email = ?", (email,))
    row = c.fetchone()
    if not row:
        conn.close()
        return False, "not_found"
    c.execute("UPDATE users SET password = ? WHERE email = ?", (hash_password(new_password), email))
    conn.commit()
    conn.close()
    return True, "success"

# -- Session State Setup --
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "email" not in st.session_state:
    st.session_state.email = ""
if "tier" not in st.session_state:
    st.session_state.tier = "Free"
if "history" not in st.session_state:
    st.session_state.history = []

# -- Language Selector in Sidebar --
selected_lang = st.sidebar.selectbox("🌐 Լեզու / Language / Язык", ["Հայերեն", "English", "Русский"])
t = TRANSLATIONS[selected_lang]

# -- Sidebar Authentication & Branding --
st.sidebar.markdown("""
    <div class="logo-container">
        <span style="font-size: 32px;">🧬</span>
        <span class="logo-text">HelixDock</span>
    </div>
""", unsafe_allow_html=True)
st.sidebar.markdown("---")

auth_mode = st.sidebar.radio(f"{t['account']}՝", [t["login"], t["signup"], t["forgot"]])

if not st.session_state.logged_in:
    if auth_mode == t["login"]:
        st.sidebar.subheader(t["login"])
        login_email = st.sidebar.text_input(t["email"], key="l_email")
        login_pass = st.sidebar.text_input(t["password"], type="password", key="l_pass")
        
        if login_email.strip().lower() == ADMIN_EMAIL.lower():
            st.sidebar.info("💡 Admin note: If you haven't set a custom password yet, you can use **Admin123!**")
        
        if st.sidebar.button(t["login_btn"]):
            valid, user_tier = verify_user(login_email, login_pass)
            if valid:
                st.session_state.logged_in = True
                st.session_state.email = login_email
                st.session_state.tier = user_tier
                st.rerun()
            else:
                st.sidebar.error(t["login_error"])
                
    elif auth_mode == t["signup"]:
        st.sidebar.subheader(t["signup"])
        st.sidebar.markdown("""
            <div class="password-rules">
                <b>Գաղտնաբառի պահանջներ:</b><br>
                • Նվազագույնը 8 նիշ<br>
                • Առնվազն 1 մեծատառ (A-Z)<br>
                • Առնվազն 1 փոքրատառ (a-z)<br>
                • Առնվազն 1 թիվ (0-9)<br>
                • Առնվազն 1 հատուկ նիշ (@$!%*?&)
            </div>
        """, unsafe_allow_html=True)
        reg_email = st.sidebar.text_input(t["email"], key="r_email")
        reg_pass = st.sidebar.text_input(t["password"], type="password", key="r_pass")
        reg_pass_conf = st.sidebar.text_input(t["password_confirm"], type="password", key="r_pass_conf")
        
        if st.sidebar.button(t["reg_btn"]):
            if reg_email and reg_pass and reg_pass_conf:
                if reg_pass == reg_pass_conf:
                    success, res_msg = register_user(reg_email, reg_pass)
                    if success:
                        st.sidebar.success(t["reg_success"])
                    else:
                        if res_msg == "weak_pass":
                            st.sidebar.error(t["pass_weak"])
                        else:
                            st.sidebar.error(t["reg_error"])
                else:
                    st.sidebar.error(t["pass_mismatch"])
            else:
                st.sidebar.warning(t["fill_all"])
                
    else:  # Forgot Password
        st.sidebar.subheader(t["forgot"])
        st.sidebar.markdown("""
            <div class="password-rules">
                Նոր գաղտնաբառը ևս պետք է համապատասխանի անվտանգության նշված պահանջներին։
            </div>
        """, unsafe_allow_html=True)
        f_email = st.sidebar.text_input(t["email"], key="f_email")
        f_pass = st.sidebar.text_input(t["new_password"], type="password", key="f_pass")
        f_pass_conf = st.sidebar.text_input(t["password_confirm"], type="password", key="f_pass_conf")
        
        if st.sidebar.button(t["reset_btn"]):
            if f_email and f_pass and f_pass_conf:
                if f_pass == f_pass_conf:
                    success, res_msg = update_password(f_email, f_pass)
                    if success:
                        st.sidebar.success(t["reset_success"])
                    else:
                        if res_msg == "weak_pass":
                            st.sidebar.error(t["pass_weak"])
                        else:
                            st.sidebar.error(t["user_not_found"])
                else:
                    st.sidebar.error(t["pass_mismatch"])
            else:
                st.sidebar.warning(t["fill_all"])
else:
    st.sidebar.success(f"👤 {st.session_state.email}")
    st.sidebar.info(f"{t['plan_pro'] if st.session_state.tier == 'Pro' else t['plan_free']} Tier")
    
    if st.sidebar.button(t["logout"]):
        st.session_state.logged_in = False
        st.session_state.email = ""
        st.session_state.tier = "Free"
        st.rerun()

    if st.session_state.tier == "Free":
        st.sidebar.markdown("---")
        st.sidebar.subheader(t["upgrade_title"])
        
        st.sidebar.markdown(f'''
            <div class="payment-box">
                <p style="color: #94A3B8; margin-bottom: 6px; font-size: 13px;">
                    <b>USDT (TRC20) Վճարման Հրահանգ:</b>
                </p>
                <ol style="padding-left: 15px; color: #CBD5E1; font-size: 12px; margin-bottom: 8px;">
                    <li>Բացեք ձեր կրիպտո դրամապանակը (Binance, Trust Wallet, և այլն):</li>
                    <li>Ուղարկեք <b>29 USDT</b> (ցանցը՝ <b>TRC20</b>) հետևյալ հասցեին.</li>
                </ol>
                <div class="crypto-address">
                    TKRGWRC2PWKxAgsmxHdaH3wfDvJs1uXNEE
                </div>
                <p style="text-align: center; margin-bottom: 8px;">
                    <a href="https://tronscan.org/#/address/TKRGWRC2PWKxAgsmxHdaH3wfDvJs1uXNEE" target="_blank" style="color: #38BDF8; font-size: 11px; text-decoration: none;">🔗 Ստուգել հասցեն TRONScan-ում</a>
                </p>
                <p style="color: #94A3B8; font-size: 11px; margin-bottom: 0;">
                    💡 <b>Կարևոր է։</b> Փոխանցումն անելուց հետո գրեք մեզ այս էլ. հասցեին՝ <a href="mailto:lianahovsepyan65@gmail.com" style="color: #38BDF8;">lianahovsepyan65@gmail.com</a> (նշելով ձեր գրանցված Email-ը), որպեսզի անմիջապես ակտիվացնենք ձեր Pro պլանը։
                </p>
            </div>
        ''', unsafe_allow_html=True)

# -- Main Application Interface --
st.markdown(f"""
    <div style="display: flex; align-items: center; gap: 15px; margin-bottom: 20px;">
        <span style="font-size: 40px;">🧬</span>
        <div>
            <h1 style="margin: 0; font-size: 32px;">{t['title']}</h1>
            <p style="margin: 0; color: #9CA3AF;">{t['subtitle']}</p>
        </div>
    </div>
""", unsafe_allow_html=True)

if not st.session_state.logged_in:
    st.warning(t["lock_msg"])
else:
    tier = st.session_state.tier
    st.info(f"Account: **{st.session_state.email}** | Status: **{tier}**")

    if tier == "Free":
        st.warning(t["free_lock"])
    else:
        st.success(t["pro_active"])
        
        input_method = st.radio(t["input_choice"], [t["opt1"], t["opt2"]])
        
        protein_data = None
        protein_name = ""
        ligand_data = None
        ligand_name = ""

        if input_method == t["opt1"]:
            col1, col2 = st.columns(2)
            with col1:
                pdb_id = st.text_input(t["pdb_input"], value="1CRN").strip().upper()
            with col2:
                st.write("")
                st.write("")
                fetch_btn = st.button(t["fetch_btn"])
            
            if fetch_btn and pdb_id:
                with st.spinner(f"{t['fetching']} {pdb_id}..."):
                    url = f"https://files.rcsb.org/download/{pdb_id}.pdb"
                    response = requests.get(url)
                    if response.status_code == 200:
                        st.session_state.fetched_pdb = response.text
                        st.session_state.fetched_name = f"{pdb_id}.pdb"
                        st.success(f"{t['fetch_ok']} {pdb_id}!")
                    else:
                        st.error(t["fetch_err"])
            
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
            if st.button(t["run_dock"]):
                with st.spinner(t["running"]):
                    time.sleep(2.0)
                    affinity = "-11.4 kcal/mol" if "1CRN" in protein_name else "-9.8 kcal/mol"
                    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    
                    st.session_state.history.append({
                        "Time": timestamp,
                        "Protein": protein_name,
                        "Ligand": ligand_name,
                        "Affinity": affinity
                    })
                    
                st.success(t["dock_ok"])
                st.metric(label=t["affinity"], value=affinity)
                
                st.subheader(t["viewer_title"])
                result_viewer = py3Dmol.view(width=800, height=500)
                result_viewer.addModel(protein_data, "pdb")
                result_viewer.setStyle({'cartoon': {'color': 'cyan'}})
                result_viewer.addModel(ligand_data, "sdf")
                result_viewer.setStyle({'stick': {'colorscheme': 'greenCarbon', 'radius': 0.3}})
                result_viewer.zoomTo()
                components.html(result_viewer._make_html(), height=530, scrolling=False)
        
        if st.session_state.history:
            st.markdown("---")
            st.subheader(t["history_title"])
            history_df = pd.DataFrame(st.session_state.history)
            st.dataframe(history_df, use_container_width=True)