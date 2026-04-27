import json
import os
import streamlit as st

LEDGER_FILE = "data/ledger_data.json"
USER_FILE = "data/users.json"

@st.cache_data
def load_ledger():
    if not os.path.exists(LEDGER_FILE):
        return []
    with open(LEDGER_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_ledger(data):
    os.makedirs("data", exist_ok=True)
    with open(LEDGER_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    load_ledger.clear()  # ← 캐시 초기화

def load_users():
    if not os.path.exists(USER_FILE):
        return {}
    with open(USER_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def show_sidebar():
    users = load_users()
    user_info = users.get(st.session_state.get('current_user', ''), {})
    name = user_info.get('name', st.session_state.get('current_user', ''))
    uid  = st.session_state.get('current_user', '')

    st.sidebar.markdown(
        f"""
        <div style="background:#f0f2f6; padding:10px 14px; border-radius:10px;
                    border:1px solid #dfe1e5; margin-bottom:8px;">
            <p style="margin:0; font-size:12px; color:#888;">👤 접속 중</p>
            <p style="margin:4px 0 0 0; font-weight:bold; font-size:15px;">
                {name} ({uid})
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.sidebar.button("🚪 로그아웃", use_container_width=True, key="logout_btn"):
        st.session_state.login = False
        st.session_state.current_user = ""
        st.session_state["force_logout"] = True
        try:
            st.switch_page("main.py")
        except:
            st.rerun()