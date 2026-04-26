import streamlit as st
import pandas as pd
from datetime import date      # ← 추가
from utils import load_ledger, show_sidebar  # ← 이걸로 교체

# 로그인 체크
if not st.session_state.get('login', False):
    st.warning("로그인이 필요합니다.")
    st.stop()

#st.sidebar.info(f"👤 접속 중: {st.session_state.current_user}")
show_sidebar()
st.title("마이 페이지")

# 데이터가 있는지 확인 후 표시
col1, col2 = st.columns(2)

with col1:
    st.subheader("🛍️ 소비 성향")
    user_type = st.session_state.get('user_type', "진단 전")
    st.info(f"당신은 **{user_type}** 입니다.")

with col2:
    st.subheader("🧠 경제 퀴즈 점수")
    score = st.session_state.get('quiz_score', "미응시")
    st.metric(label="최근 퀴즈 점수", value=f"{score}점")

st.divider()

# 종합 평가 (예시)
#if st.session_state.get('quiz_done') and st.session_state.get('user_type'):
#    st.success("✅ 모든 테스트를 완료하셨습니다!")
#    st.write(f"**{st.session_state.current_user}**님은 지식과 습관을 모두 갖추기 위해 노력 중이시군요!")
#else:
#    st.warning("아직 완료하지 않은 테스트가 있습니다. 모든 테스트를 마치고 리포트를 확인하세요.")

# 기존 점수/유형 표시에 추가할 부분

# 가계부 요약 연동
all_data = load_ledger()
my_data = [r for r in all_data if r["user"] == st.session_state.current_user]

# ✅ 바꾼 코드
if my_data:
    df = pd.DataFrame(my_data)
    st.subheader("💰 이번 달 지출 요약")
    this_month = df[(df["year"]==date.today().year) & (df["month"]==date.today().month)]

    if not this_month.empty:
        st.metric("이번 달 총 지출", f"{this_month['amount'].sum():,}원")
        top_cat = this_month.groupby("category")["amount"].sum().idxmax()
        st.info(f"이번 달 지출 1위 항목: **{top_cat}**")
    else:
        st.info("이번 달 지출 내역이 없습니다.")

st.divider()

# ── 회원 탈퇴 ───────────────────────────────────────
with st.expander("⚠️ 회원 탈퇴"):
    st.warning("탈퇴 시 모든 가계부 데이터가 삭제되며 복구할 수 없습니다.")
    confirm = st.text_input("탈퇴하려면 아이디를 입력하세요", key="confirm_delete")

    if st.button("회원 탈퇴", type="primary"):
        if confirm != st.session_state.current_user:
            st.error("❌ 아이디가 일치하지 않습니다.")
        else:
            from utils import load_users, load_ledger, save_ledger
            import json, os

            # 유저 정보 삭제
            users = load_users()
            if st.session_state.current_user in users:
                del users[st.session_state.current_user]
                with open("data/users.json", "w", encoding="utf-8") as f:
                    json.dump(users, f, ensure_ascii=False, indent=2)

            # 가계부 데이터 삭제
            all_data = load_ledger()
            remaining = [r for r in all_data if r["user"] != st.session_state.current_user]
            save_ledger(remaining)

            # 세션 초기화
            st.session_state.login = False
            st.session_state.current_user = ""
            st.session_state["force_logout"] = True
            st.success("✅ 탈퇴가 완료되었습니다.")
            st.switch_page("main.py")