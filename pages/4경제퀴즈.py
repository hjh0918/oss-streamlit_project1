'''
import streamlit as st
import time

# 로그인 체크
if not st.session_state.get('login', False):
    st.warning("로그인이 필요한 페이지입니다. 홈으로 이동해주세요.")
    st.stop()

# 사이드바 설정
st.sidebar.info(f"👤 접속 중: {st.session_state.current_user}")

st.title("🧠 경제 상식 OX 퀴즈")

# [과제 요건 3] 캐싱 기능
@st.cache_data
def get_quiz_data():
    time.sleep(0.5) # 로딩 시뮬레이션
    return [
        {"q": "기준 금리가 오르면 대출 이자 부담도 늘어난다.", "a": "O"},
        {"q": "인플레이션은 물가가 하락하는 현상을 말한다.", "a": "X"}
    ]

quizzes = get_quiz_data()
with st.form("quiz"):
    # ... (기존 퀴즈 로직 동일) ...
    st.form_submit_button("제출")

# 퀴즈 페이지 마지막 부분에 추가
'''

import streamlit as st
import json
import time
import random
from utils import load_ledger, show_sidebar

if not st.session_state.get('login', False):
    st.warning("로그인이 필요합니다.")
    st.stop()

#st.sidebar.info(f"👤 접속 중: {st.session_state.current_user}")
show_sidebar()
st.title("🧠 경제 & 금융 상식 퀴즈")

QUIZ_FILES = {
    "🟢 하 (입문)": "data/quiz_easy.json",
    "🟡 중 (기본)": "data/quiz_medium.json",
    "🔴 상 (심화)": "data/quiz_hard.json",
}

@st.cache_data
def load_quiz(filepath):
    """캐싱 이유: 100개짜리 JSON을 매번 읽으면 느리므로 한 번만 읽고 재사용"""
    time.sleep(1)
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

st.subheader("📊 난이도를 선택하세요")
difficulty = st.radio(
    "난이도", list(QUIZ_FILES.keys()),
    horizontal=True, label_visibility="collapsed"
)

desc = {
    "🟢 하 (입문)": "일상적인 경제/금융 기초 상식 문제입니다.",
    "🟡 중 (기본)": "경제 원리와 금융 개념을 묻는 문제입니다.",
    "🔴 상 (심화)": "전문적인 경제/금융 지식이 필요한 문제입니다.",
}
st.info(desc[difficulty])

with st.spinner("퀴즈 데이터 로딩 중..."):
    try:
        all_quizzes = load_quiz(QUIZ_FILES[difficulty])
        st.success(f"✅ {len(all_quizzes)}개 문항 로드 완료 (캐싱 활성화)")
    except FileNotFoundError:
        st.error(f"❌ 파일을 찾을 수 없습니다.")
        st.stop()

if st.session_state.get('current_difficulty') != difficulty:
    st.session_state.current_difficulty = difficulty
    st.session_state.random_quizzes = random.sample(all_quizzes, 20)
    st.session_state.quiz_submitted = False

with st.form("quiz_form"):
    st.subheader("📝 랜덤 20문제")
    user_answers = []
    for i, q_item in enumerate(st.session_state.random_quizzes):
        st.write(f"**Q{i+1}. [{q_item['category']}] {q_item['q']}**")
        ans = st.radio(
            f"선택 {i}", ["O", "X"],
            key=f"quiz_{difficulty}_{i}",
            horizontal=True,
            label_visibility="collapsed"
        )
        user_answers.append(ans)
        st.divider()

    if st.form_submit_button("결과 제출"):
        correct = sum(
            1 for i, q in enumerate(st.session_state.random_quizzes)
            if user_answers[i] == q['a']
        )
        final_score = int((correct / 20) * 100)
        st.session_state.quiz_score = final_score
        st.session_state.quiz_difficulty = difficulty
        st.session_state.quiz_done = True

        st.write(f"## 🎯 점수: {final_score}점 ({correct}/20 정답)")
        st.progress(correct / 20)

        if correct == 20:
            st.balloons()
            st.success("완벽합니다! 🎉")
        elif correct >= 10:
            st.info("절반 이상 맞혔어요! 조금만 더 공부해봐요.")
        else:
            st.warning("틀린 문제를 복습해보세요!")

        st.subheader("📋 정답 확인")
        for i, q in enumerate(st.session_state.random_quizzes):
            icon = "✅" if user_answers[i] == q['a'] else "❌"
            st.write(f"{icon} **Q{i+1}.** {q['q']}  →  정답: **{q['a']}**")

if st.button("🔀 새로운 문제 뽑기"):
    st.session_state.random_quizzes = random.sample(all_quizzes, 20)
    st.rerun()