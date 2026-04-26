# import streamlit as st
# import json
# import os
# import random
# import pandas as pd
# from datetime import date
# from streamlit_cookies_manager import EncryptedCookieManager

# USER_FILE = "data/users.json"

# cookies = EncryptedCookieManager(prefix="gq_app_", password="gq-secret-key-2024")
# if not cookies.ready():
#     st.stop()

# def load_users():
#     os.makedirs("data", exist_ok=True)
#     if not os.path.exists(USER_FILE):
#         return {}
#     with open(USER_FILE, "r", encoding="utf-8") as f:
#         return json.load(f)

# def save_users(users):
#     os.makedirs("data", exist_ok=True)
#     with open(USER_FILE, "w", encoding="utf-8") as f:
#         json.dump(users, f, ensure_ascii=False, indent=2)

# st.set_page_config(page_title="경제 나침반", layout="wide")

# if 'login' not in st.session_state:
#     st.session_state.login = False
# if 'current_user' not in st.session_state:
#     st.session_state.current_user = ""

# # ── 로그아웃 신호 감지 → 쿠키 삭제 ────────────────
# if st.session_state.get("force_logout"):
#     cookies["logged_in_user"] = ""
#     cookies.save()
#     st.session_state["force_logout"] = False

# # ── 쿠키로 자동 로그인 복구 ────────────────────────
# if not st.session_state.login:
#     saved_user = cookies.get("logged_in_user", "")
#     if saved_user:
#         users = load_users()
#         if saved_user in users:
#             st.session_state.login = True
#             st.session_state.current_user = saved_user
#             st.rerun()

# # ── 첫 화면 학번/이름 표시 ─────────────────────────
# st.markdown("""
#     <div style="background-color:#f0f2f6; padding:15px; border-radius:10px; 
#                 border:1px solid #dfe1e5; margin-bottom:20px;">
#         <h3 style="margin:0; color:#31333f;">과제 제출자</h3>
#         <p style="margin:0; font-size:16px;"><b>학번:</b> 2021204080</p>
#         <p style="margin:0; font-size:16px;"><b>이름:</b> 허재호</p>
#     </div>
# """, unsafe_allow_html=True)

# #💰
# # ── 로그인 전 화면 ──────────────────────────────────
# if not st.session_state.login:
#     st.title("MoneyLog")
#     tab1, tab2, tab3 = st.tabs(["🔒 로그인", "📝 회원가입", "🔑 아이디/비밀번호 찾기"])

#     with tab1:
#         st.subheader("로그인")
#         login_id = st.text_input("아이디", key="login_id")
#         login_pw = st.text_input("비밀번호", type="password", key="login_pw")

#         if st.button("로그인하기"):
#             users = load_users()
#             if login_id not in users:
#                 st.error("❌ 등록되지 않은 아이디입니다.")
#             elif users[login_id]["password"] != login_pw:
#                 st.error("❌ 비밀번호가 일치하지 않습니다.")
#             else:
#                 st.session_state.login = True
#                 st.session_state.current_user = login_id
#                 cookies["logged_in_user"] = login_id
#                 cookies.save()
#                 st.success(f"✅ {users[login_id]['name']}님, 환영합니다!")
#                 st.rerun()

#     with tab2:
#         st.subheader("새 계정 만들기")
#         new_id       = st.text_input("아이디", key="new_id")
#         new_name     = st.text_input("이름", key="new_name")
#         new_hint     = st.text_input("힌트 질문 (예: 내 고향은?)", key="new_hint")
#         new_hint_ans = st.text_input("힌트 답변", key="new_hint_ans")
#         new_pw       = st.text_input("비밀번호", type="password", key="new_pw")
#         new_pw2      = st.text_input("비밀번호 확인", type="password", key="new_pw2")

#         if st.button("회원가입 완료"):
#             users = load_users()
#             if not all([new_id, new_name, new_hint, new_hint_ans, new_pw]):
#                 st.warning("⚠️ 모든 항목을 입력해주세요.")
#             elif new_id in users:
#                 st.error("❌ 이미 가입된 아이디입니다.")
#             elif new_pw != new_pw2:
#                 st.error("❌ 비밀번호가 일치하지 않습니다.")
#             else:
#                 users[new_id] = {
#                     "name": new_name,
#                     "password": new_pw,
#                     "hint_q": new_hint,
#                     "hint_a": new_hint_ans
#                 }
#                 save_users(users)
#                 st.success("✅ 회원가입 완료! 로그인 탭에서 로그인하세요.")

#     with tab3:
#         st.subheader("🔑 아이디/비밀번호 찾기")
#         find_tab1, find_tab2 = st.tabs(["아이디 찾기", "비밀번호 찾기"])

#         with find_tab1:
#             find_name = st.text_input("가입 시 입력한 이름", key="find_name")
#             if st.button("아이디 찾기"):
#                 users = load_users()
#                 found = [uid for uid, info in users.items() if info["name"] == find_name]
#                 if found:
#                     st.success(f"✅ 가입된 아이디: **{', '.join(found)}**")
#                 else:
#                     st.error("❌ 해당 이름으로 가입된 계정이 없습니다.")

#         with find_tab2:
#             find_id = st.text_input("아이디", key="find_id")
#             if st.button("힌트 질문 불러오기"):
#                 users = load_users()
#                 if find_id in users:
#                     st.session_state.hint_q = users[find_id]["hint_q"]
#                 else:
#                     st.error("❌ 등록되지 않은 아이디입니다.")

#             if 'hint_q' in st.session_state:
#                 st.info(f"힌트 질문: **{st.session_state.hint_q}**")
#                 find_hint_ans = st.text_input("힌트 답변 입력", key="find_hint_ans")
#                 if st.button("비밀번호 확인"):
#                     users = load_users()
#                     if find_id in users and users[find_id]["hint_a"] == find_hint_ans:
#                         st.success(f"✅ 비밀번호는: **{users[find_id]['password']}**")
#                     else:
#                         st.error("❌ 힌트 답변이 틀렸습니다.")

# # ── 로그인 후 메인 대시보드 ────────────────────────
# else:
#     from utils import show_sidebar, load_ledger
#     show_sidebar()

#     users = load_users()
#     user_info = users.get(st.session_state.current_user, {})
#     name = user_info.get('name', '')

#     st.title("🏠 메인 대시보드")
#     st.write(f"안녕하세요, **{name}**님! 환영합니다! ")

#     st.divider()

#     # ── 오늘의 경제 한마디 ──────────────────────────
#     quotes = [
#         ("💬 \"복리는 세계 8번째 불가사의다. 이해하는 자는 이익을 얻고, 이해 못하는 자는 이자를 낸다.\"", "- 알버트 아인슈타인"),
#         ("💬 \"주식시장은 인내심 없는 사람의 돈을 인내심 있는 사람에게 이전시키는 장치다.\"", "- 워런 버핏"),
#         ("💬 \"돈을 버는 것보다 돈을 관리하는 것이 더 중요하다.\"", "- 앤드루 카네기"),
#         ("💬 \"지출을 소득 수준 이하로 유지하는 것이 재정적 성공의 핵심이다.\"", "- 토마스 스탠리"),
#         ("💬 \"부자가 되고 싶다면 부자가 하는 행동을 하라.\"", "- 벤자민 프랭클린"),
#         ("💬 \"저축은 수입과 지출의 차이가 아니라 습관이다.\"", "- 존 템플턴"),
#         ("💬 \"가계부를 쓰는 것은 돈을 다스리는 첫걸음이다.\"", "- 재무 격언"),
#         ("💬 \"작은 지출을 조심하라. 작은 구멍이 큰 배를 침몰시킨다.\"", "- 벤자민 프랭클린"),
#         ("💬 \"월급날 남은 돈을 저축하지 말고, 저축하고 남은 돈을 써라.\"", "- 워런 버핏"),
#         ("💬 \"돈은 감정이 아니라 계획으로 관리해야 한다.\"", "- 데이브 램지"),
#         ("💬 \"부자는 자산이 일하게 하고, 가난한 사람은 자신이 일한다.\"", "- 로버트 기요사키"),
#     ]
#     quote, author = random.choice(quotes)
#     st.markdown(
#         f"""
#         <div style="background:#f8f9fa; border-left:4px solid #4CAF50;
#                     padding:16px 20px; border-radius:8px; margin-bottom:16px;">
#             <p style="font-size:16px; margin:0; color:#333;">{quote}</p>
#             <p style="font-size:13px; margin:8px 0 0 0; color:#888;">{author}</p>
#         </div>
#         """,
#         unsafe_allow_html=True
#     )

#     st.divider()

#     # ── 나의 활동 요약 ───────────────────────────────
#     st.subheader("📋 나의 활동 요약")
#     col1, col2, col3 = st.columns(3)

#     with col1:
#         quiz_score = st.session_state.get('quiz_score', None)
#         if quiz_score is not None:
#             st.metric("🧠 최근 퀴즈 점수", f"{quiz_score}점")
#         else:
#             st.metric("🧠 최근 퀴즈 점수", "미응시")

#     with col2:
#         user_type = st.session_state.get('user_type', None)
#         if user_type:
#             st.metric("🛍️ 소비 성향", user_type)
#         else:
#             st.metric("🛍️ 소비 성향", "진단 전")

#     with col3:
#         all_data = load_ledger()
#         my_data = [r for r in all_data if r["user"] == st.session_state.current_user]
#         if my_data:
#             df = pd.DataFrame(my_data)
#             this_month = df[
#                 (df["year"] == date.today().year) &
#                 (df["month"] == date.today().month)
#             ]
#             total = int(this_month["amount"].sum())
#             st.metric("💰 이번 달 총 지출", f"{total:,}원")
#         else:
#             st.metric("💰 이번 달 총 지출", "기록 없음")

#     st.divider()

#     # ── 빠른 이동 버튼 ──────────────────────────────
#     st.subheader("🚀 빠른 이동")
#     col1, col2, col3, col4 = st.columns(4)

#     with col1:
#         if st.button("📊 마이페이지", use_container_width=True):
#             st.switch_page("pages/1마이페이지.py")
#     with col2:
#         if st.button("📒 가계부 작성", use_container_width=True):
#             st.switch_page("pages/2가계부.py")
#     with col3:
#         if st.button("🛍️ 소비 성향 진단", use_container_width=True):
#             st.switch_page("pages/3소비성향.py")
#     with col4:
#         if st.button("🧠 경제 퀴즈 풀기", use_container_width=True):
#             st.switch_page("pages/4경제퀴즈.py")

import streamlit as st
import json
import os
import random
import pandas as pd
from datetime import date
from streamlit_cookies_manager import EncryptedCookieManager

USER_FILE = "data/users.json"

cookies = EncryptedCookieManager(prefix="gq_app_", password="gq-secret-key-2024")
if not cookies.ready():
    st.stop()

def load_users():
    os.makedirs("data", exist_ok=True)
    if not os.path.exists(USER_FILE):
        return {}
    with open(USER_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_users(users):
    os.makedirs("data", exist_ok=True)
    with open(USER_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)

st.set_page_config(page_title="MoneyLog", layout="wide")

if 'login' not in st.session_state:
    st.session_state.login = False
if 'current_user' not in st.session_state:
    st.session_state.current_user = ""
if 'show_login' not in st.session_state:
    st.session_state.show_login = False

# ── 로그아웃 신호 감지 → 쿠키 삭제 ────────────────
if st.session_state.get("force_logout"):
    cookies["logged_in_user"] = ""
    cookies.save()
    st.session_state["force_logout"] = False

# ── 쿠키로 자동 로그인 복구 ────────────────────────
if not st.session_state.login and not st.session_state.get('show_login'):
    saved_user = cookies.get("logged_in_user", "")
    if saved_user:
        users = load_users()
        if saved_user in users:
            st.session_state.login = True
            st.session_state.current_user = saved_user
            st.rerun()

# ── 첫 화면 학번/이름 표시 ─────────────────────────
st.markdown("""
    <div style="background-color:#f0f2f6; padding:15px; border-radius:10px; 
                border:1px solid #dfe1e5; margin-bottom:20px;">
        <h3 style="margin:0; color:#31333f;">과제 제출자</h3>
        <p style="margin:0; font-size:16px;"><b>학번:</b> 2021204080</p>
        <p style="margin:0; font-size:16px;"><b>이름:</b> 허재호</p>
    </div>
""", unsafe_allow_html=True)

# ── 로그인 전 화면 ──────────────────────────────────
if not st.session_state.login:
    st.title("MoneyLog")

    # 회원가입 완료 후 로그인 화면으로 전환
    # 회원가입 완료 후 로그인 화면으로 전환
    if st.session_state.show_login:
        st.success("✅ 회원가입이 완료되었습니다! 로그인해주세요.")
        st.subheader("로그인")
        login_id = st.text_input("아이디", key="login_id")
        login_pw = st.text_input("비밀번호", type="password", key="login_pw")

        if st.button("로그인하기"):
            users = load_users()
            if login_id not in users:
                st.error("❌ 등록되지 않은 아이디입니다.")
            elif users[login_id]["password"] != login_pw:
                st.error("❌ 비밀번호가 일치하지 않습니다.")
            else:
                st.session_state.login = True
                st.session_state.current_user = login_id
                st.session_state.show_login = False  # ← 로그인 성공 시에만 False
                cookies["logged_in_user"] = login_id
                cookies.save()
                st.rerun()

        if st.button("← 돌아가기"):
            st.session_state.show_login = False
            st.rerun()

    # 일반 탭 화면
    else:
        tab1, tab2, tab3 = st.tabs(["🔒 로그인", "📝 회원가입", "🔑 아이디/비밀번호 찾기"])

        with tab1:
            st.subheader("로그인")
            login_id = st.text_input("아이디", key="login_id")
            login_pw = st.text_input("비밀번호", type="password", key="login_pw")

            if st.button("로그인하기"):
                users = load_users()
                if login_id not in users:
                    st.error("❌ 등록되지 않은 아이디입니다.")
                elif users[login_id]["password"] != login_pw:
                    st.error("❌ 비밀번호가 일치하지 않습니다.")
                else:
                    st.session_state.login = True
                    st.session_state.current_user = login_id
                    cookies["logged_in_user"] = login_id
                    cookies.save()
                    st.success(f"✅ {users[login_id]['name']}님, 환영합니다!")
                    st.rerun()

        with tab2:
            st.subheader("새 계정 만들기")
            new_id       = st.text_input("아이디", key="new_id")
            new_name     = st.text_input("이름", key="new_name")
            new_hint     = st.text_input("힌트 질문 (예: 내 고향은?)", key="new_hint")
            new_hint_ans = st.text_input("힌트 답변", key="new_hint_ans")
            new_pw       = st.text_input("비밀번호", type="password", key="new_pw")
            new_pw2      = st.text_input("비밀번호 확인", type="password", key="new_pw2")

            if st.button("회원가입 완료"):
                users = load_users()
                if not all([new_id, new_name, new_hint, new_hint_ans, new_pw]):
                    st.warning("⚠️ 모든 항목을 입력해주세요.")
                elif new_id in users:
                    st.error("❌ 이미 가입된 아이디입니다.")
                elif new_pw != new_pw2:
                    st.error("❌ 비밀번호가 일치하지 않습니다.")
                else:
                    users[new_id] = {
                        "name": new_name,
                        "password": new_pw,
                        "hint_q": new_hint,
                        "hint_a": new_hint_ans
                    }
                    save_users(users)
                    cookies["logged_in_user"] = ""  # ← 추가: 쿠키 삭제
                    cookies.save()                  # ← 추가: 쿠키 저장
                    st.session_state.login = False  # ← 추가: 로그인 상태 초기화
                    st.session_state.current_user = "" 
                    st.session_state.show_login = True  # ← 로그인 화면으로 전환
                    st.rerun()

        with tab3:
            st.subheader("🔑 아이디/비밀번호 찾기")
            find_tab1, find_tab2 = st.tabs(["아이디 찾기", "비밀번호 찾기"])

            with find_tab1:
                find_name = st.text_input("가입 시 입력한 이름", key="find_name")
                if st.button("아이디 찾기"):
                    users = load_users()
                    found = [uid for uid, info in users.items() if info["name"] == find_name]
                    if found:
                        st.success(f"✅ 가입된 아이디: **{', '.join(found)}**")
                    else:
                        st.error("❌ 해당 이름으로 가입된 계정이 없습니다.")

            with find_tab2:
                find_id = st.text_input("아이디", key="find_id")
                if st.button("힌트 질문 불러오기"):
                    users = load_users()
                    if find_id in users:
                        st.session_state.hint_q = users[find_id]["hint_q"]
                    else:
                        st.error("❌ 등록되지 않은 아이디입니다.")

                if 'hint_q' in st.session_state:
                    st.info(f"힌트 질문: **{st.session_state.hint_q}**")
                    find_hint_ans = st.text_input("힌트 답변 입력", key="find_hint_ans")
                    if st.button("비밀번호 확인"):
                        users = load_users()
                        if find_id in users and users[find_id]["hint_a"] == find_hint_ans:
                            st.success(f"✅ 비밀번호는: **{users[find_id]['password']}**")
                        else:
                            st.error("❌ 힌트 답변이 틀렸습니다.")

# ── 로그인 후 메인 대시보드 ────────────────────────
else:
    from utils import show_sidebar, load_ledger
    show_sidebar()

    users = load_users()
    user_info = users.get(st.session_state.current_user, {})
    name = user_info.get('name', '')

    st.title("🏠 메인 대시보드")
    st.write(f"안녕하세요, **{name}**님! 환영합니다!")

    st.divider()

    # ── 오늘의 경제 한마디 ──────────────────────────
    quotes = [
        ("💬 \"복리는 세계 8번째 불가사의다. 이해하는 자는 이익을 얻고, 이해 못하는 자는 이자를 낸다.\"", "- 알버트 아인슈타인"),
        ("💬 \"주식시장은 인내심 없는 사람의 돈을 인내심 있는 사람에게 이전시키는 장치다.\"", "- 워런 버핏"),
        ("💬 \"돈을 버는 것보다 돈을 관리하는 것이 더 중요하다.\"", "- 앤드루 카네기"),
        ("💬 \"지출을 소득 수준 이하로 유지하는 것이 재정적 성공의 핵심이다.\"", "- 토마스 스탠리"),
        ("💬 \"부자가 되고 싶다면 부자가 하는 행동을 하라.\"", "- 벤자민 프랭클린"),
        ("💬 \"저축은 수입과 지출의 차이가 아니라 습관이다.\"", "- 존 템플턴"),
        ("💬 \"가계부를 쓰는 것은 돈을 다스리는 첫걸음이다.\"", "- 재무 격언"),
        ("💬 \"작은 지출을 조심하라. 작은 구멍이 큰 배를 침몰시킨다.\"", "- 벤자민 프랭클린"),
        ("💬 \"월급날 남은 돈을 저축하지 말고, 저축하고 남은 돈을 써라.\"", "- 워런 버핏"),
        ("💬 \"돈은 감정이 아니라 계획으로 관리해야 한다.\"", "- 데이브 램지"),
        ("💬 \"부자는 자산이 일하게 하고, 가난한 사람은 자신이 일한다.\"", "- 로버트 기요사키"),
    ]
    quote, author = random.choice(quotes)
    st.markdown(
        f"""
        <div style="background:#f8f9fa; border-left:4px solid #4CAF50;
                    padding:16px 20px; border-radius:8px; margin-bottom:16px;">
            <p style="font-size:16px; margin:0; color:#333;">{quote}</p>
            <p style="font-size:13px; margin:8px 0 0 0; color:#888;">{author}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    # ── 나의 활동 요약 ───────────────────────────────
    st.subheader("📋 나의 활동 요약")
    col1, col2, col3 = st.columns(3)

    with col1:
        quiz_score = st.session_state.get('quiz_score', None)
        if quiz_score is not None:
            st.metric("🧠 최근 퀴즈 점수", f"{quiz_score}점")
        else:
            st.metric("🧠 최근 퀴즈 점수", "미응시")

    with col2:
        user_type = st.session_state.get('user_type', None)
        if user_type:
            st.metric("🛍️ 소비 성향", user_type)
        else:
            st.metric("🛍️ 소비 성향", "진단 전")

    with col3:
        all_data = load_ledger()
        my_data = [r for r in all_data if r["user"] == st.session_state.current_user]
        if my_data:
            df = pd.DataFrame(my_data)
            this_month = df[
                (df["year"] == date.today().year) &
                (df["month"] == date.today().month)
            ]
            total = int(this_month["amount"].sum())
            st.metric("💰 이번 달 총 지출", f"{total:,}원")
        else:
            st.metric("💰 이번 달 총 지출", "기록 없음")

    st.divider()

    # ── 빠른 이동 버튼 ──────────────────────────────
    st.subheader("🚀 빠른 이동")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("📊 마이페이지", use_container_width=True):
            st.switch_page("pages/1마이페이지.py")
    with col2:
        if st.button("📒 가계부 작성", use_container_width=True):
            st.switch_page("pages/2가계부.py")
    with col3:
        if st.button("🛍️ 소비 성향 진단", use_container_width=True):
            st.switch_page("pages/3소비성향.py")
    with col4:
        if st.button("🧠 경제 퀴즈 풀기", use_container_width=True):
            st.switch_page("pages/4경제퀴즈.py")