# import json
# import os
# import streamlit as st

# LEDGER_FILE = "data/ledger_data.json"

# @st.cache_data
# def load_ledger():
#     if not os.path.exists(LEDGER_FILE):
#         return []
#     with open(LEDGER_FILE, "r", encoding="utf-8") as f:
#         return json.load(f)

#####################################################################

# import json
# import os
# import streamlit as st

# LEDGER_FILE = "data/ledger_data.json"
# USER_FILE = "data/users.json"

# @st.cache_data
# def load_ledger():
#     if not os.path.exists(LEDGER_FILE):
#         return []
#     with open(LEDGER_FILE, "r", encoding="utf-8") as f:
#         return json.load(f)

# def load_users():
#     if not os.path.exists(USER_FILE):
#         return {}
#     with open(USER_FILE, "r", encoding="utf-8") as f:
#         return json.load(f)

# def show_sidebar():
#     """모든 페이지에서 공통으로 쓰는 사이드바 - 하단에 유저 정보 + 로그아웃"""
#     users = load_users()
#     user_info = users.get(st.session_state.current_user, {})
#     name = user_info.get('name', st.session_state.current_user)

#     # 사이드바 하단 고정을 위한 빈 공간
#     st.sidebar.markdown("---")
#     st.sidebar.markdown(
#         f"""
#         <div style="position:fixed; bottom:20px; width:230px;
#                     background:#f0f2f6; padding:12px; border-radius:10px;
#                     border:1px solid #dfe1e5;">
#             <p style="margin:0; font-size:13px; color:#555;">👤 접속 중</p>
#             <p style="margin:4px 0 8px 0; font-weight:bold; font-size:15px;">
#                 {name} ({st.session_state.current_user})
#             </p>
#         </div>
#         """,
#         unsafe_allow_html=True
#     )

#     # 로그아웃 버튼 (사이드바 하단)
#     st.sidebar.markdown("<br>" * 8, unsafe_allow_html=True)
#     if st.sidebar.button("🚪 로그아웃", use_container_width=True):
#         # 쿠키 삭제 시도 (main.py에서 cookies가 있을 때만)
#         try:
#             from streamlit_cookies_manager import EncryptedCookieManager
#             cookies = EncryptedCookieManager(prefix="gq_app_", password="gq-secret-key-2024")
#             if cookies.ready():
#                 cookies["logged_in_user"] = ""
#                 cookies.save()
#         except:
#             pass
#         st.session_state.login = False
#         st.session_state.current_user = ""
#         st.switch_page("main.py")

#########################

# import json
# import os
# import streamlit as st

# LEDGER_FILE = "data/ledger_data.json"
# USER_FILE = "data/users.json"

# @st.cache_data
# def load_ledger():
#     if not os.path.exists(LEDGER_FILE):
#         return []
#     with open(LEDGER_FILE, "r", encoding="utf-8") as f:
#         return json.load(f)

# def load_users():
#     if not os.path.exists(USER_FILE):
#         return {}
#     with open(USER_FILE, "r", encoding="utf-8") as f:
#         return json.load(f)

# def show_sidebar():
#     users = load_users()
#     user_info = users.get(st.session_state.get('current_user', ''), {})
#     name = user_info.get('name', st.session_state.get('current_user', ''))
#     uid  = st.session_state.get('current_user', '')

#     # 사이드바 하단에 접속중 박스 + 로그아웃 버튼
#     st.sidebar.markdown(
#         f"""
#         <div style="position:fixed; bottom:70px; width:230px;
#                     background:#f0f2f6; padding:12px; border-radius:10px;
#                     border:1px solid #dfe1e5;">
#             <p style="margin:0; font-size:12px; color:#888;">👤 접속 중</p>
#             <p style="margin:4px 0 0 0; font-weight:bold; font-size:14px;">
#                 {name} ({uid})
#             </p>
#         </div>
#         """,
#         unsafe_allow_html=True
#     )

#     # 로그아웃 버튼 — 접속중 박스 아래 고정
#     st.sidebar.markdown(
#         """
#         <div style="position:fixed; bottom:20px; width:230px;">
#         """,
#         unsafe_allow_html=True
#     )
#     if st.sidebar.button("🚪 로그아웃", use_container_width=True, key="logout_btn"):
#         try:
#             from streamlit_cookies_manager import EncryptedCookieManager
#             cookies = EncryptedCookieManager(prefix="gq_app_", password="gq-secret-key-2024")
#             if cookies.ready():
#                 cookies["logged_in_user"] = ""
#                 cookies.save()
#         except:
#             pass
#         st.session_state.login = False
#         st.session_state.current_user = ""
#         try:
#             st.switch_page("main.py")
#         except:
#             st.rerun()
#     st.sidebar.markdown("</div>", unsafe_allow_html=True)

##################

# import json
# import os
# import streamlit as st

# LEDGER_FILE = "data/ledger_data.json"
# USER_FILE = "data/users.json"

# @st.cache_data
# def load_ledger():
#     if not os.path.exists(LEDGER_FILE):
#         return []
#     with open(LEDGER_FILE, "r", encoding="utf-8") as f:
#         return json.load(f)

# def load_users():
#     if not os.path.exists(USER_FILE):
#         return {}
#     with open(USER_FILE, "r", encoding="utf-8") as f:
#         return json.load(f)

# def show_sidebar():
#     users = load_users()
#     user_info = users.get(st.session_state.get('current_user', ''), {})
#     name = user_info.get('name', st.session_state.get('current_user', ''))
#     uid  = st.session_state.get('current_user', '')

#     # 접속중 표시 — 사이드바 페이지 목록 바로 아래 작게
#     st.sidebar.markdown(
#         f"""
#         <div style="font-size:11px; color:#aaa; margin: 4px 0 0 4px;">
#             👤 {name} ({uid}) 접속 중
#         </div>
#         """,
#         unsafe_allow_html=True
#     )

#     # 빈 공간으로 로그아웃 버튼을 아래로 밀기
#     st.sidebar.markdown("<br>" * 20, unsafe_allow_html=True)

#     # 로그아웃 버튼 — 맨 아래
#     if st.sidebar.button("🚪 로그아웃", use_container_width=True, key="logout_btn"):
#         try:
#             from streamlit_cookies_manager import EncryptedCookieManager
#             cookies = EncryptedCookieManager(prefix="gq_app_", password="gq-secret-key-2024")
#             if cookies.ready():
#                 cookies["logged_in_user"] = ""
#                 cookies.save()
#         except:
#             pass
#         st.session_state.login = False
#         st.session_state.current_user = ""
#         try:
#             st.switch_page("main.py")
#         except:
#             st.rerun()

##########################################

# import json
# import os
# import streamlit as st

# LEDGER_FILE = "data/ledger_data.json"
# USER_FILE = "data/users.json"

# @st.cache_data
# def load_ledger():
#     if not os.path.exists(LEDGER_FILE):
#         return []
#     with open(LEDGER_FILE, "r", encoding="utf-8") as f:
#         return json.load(f)

# def load_users():
#     if not os.path.exists(USER_FILE):
#         return {}
#     with open(USER_FILE, "r", encoding="utf-8") as f:
#         return json.load(f)

# def show_sidebar():
#     users = load_users()
#     user_info = users.get(st.session_state.get('current_user', ''), {})
#     name = user_info.get('name', st.session_state.get('current_user', ''))
#     uid  = st.session_state.get('current_user', '')

#     # 접속중 박스 — 사이드바 상단에 표시
#     st.sidebar.markdown(
#         f"""
#         <div style="background:#f0f2f6; padding:10px 14px; border-radius:10px;
#                     border:1px solid #dfe1e5; margin-bottom:8px;">
#             <p style="margin:0; font-size:12px; color:#888;">👤 접속 중</p>
#             <p style="margin:4px 0 0 0; font-weight:bold; font-size:15px;">
#                 {name} ({uid})
#             </p>
#         </div>
#         """,
#         unsafe_allow_html=True
#     )

#     # 로그아웃 버튼 — 접속중 박스 바로 아래
#     if st.sidebar.button("🚪 로그아웃", use_container_width=True, key="logout_btn"):
#         try:
#             from streamlit_cookies_manager import EncryptedCookieManager
#             cookies = EncryptedCookieManager(prefix="gq_app_", password="gq-secret-key-2024")
#             if cookies.ready():
#                 cookies["logged_in_user"] = ""
#                 cookies.save()
#         except:
#             pass
#         st.session_state.login = False
#         st.session_state.current_user = ""
#         try:
#             st.switch_page("main.py")
#         except:
#             st.rerun()

########################################

# import json
# import os
# import streamlit as st

# LEDGER_FILE = "data/ledger_data.json"
# USER_FILE = "data/users.json"

# @st.cache_data
# def load_ledger():
#     if not os.path.exists(LEDGER_FILE):
#         return []
#     with open(LEDGER_FILE, "r", encoding="utf-8") as f:
#         return json.load(f)

# def load_users():
#     if not os.path.exists(USER_FILE):
#         return {}
#     with open(USER_FILE, "r", encoding="utf-8") as f:
#         return json.load(f)

# def show_sidebar():
#     users = load_users()
#     user_info = users.get(st.session_state.get('current_user', ''), {})
#     name = user_info.get('name', st.session_state.get('current_user', ''))
#     uid  = st.session_state.get('current_user', '')

#     st.sidebar.markdown(
#         f"""
#         <div style="background:#f0f2f6; padding:10px 14px; border-radius:10px;
#                     border:1px solid #dfe1e5; margin-bottom:8px;">
#             <p style="margin:0; font-size:12px; color:#888;">👤 접속 중</p>
#             <p style="margin:4px 0 0 0; font-weight:bold; font-size:15px;">
#                 {name} ({uid})
#             </p>
#         </div>
#         """,
#         unsafe_allow_html=True
#     )

#     if st.sidebar.button("🚪 로그아웃", use_container_width=True, key="logout_btn"):
#         # 세션 초기화
#         st.session_state.login = False
#         st.session_state.current_user = ""
#         st.session_state["force_logout"] = True  # ← main에 쿠키 삭제 신호
#         try:
#             st.switch_page("main.py")
#         except:
#             st.rerun()

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