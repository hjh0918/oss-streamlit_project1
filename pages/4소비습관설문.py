import streamlit as st
import pandas as pd
from utils import load_ledger, show_sidebar

if not st.session_state.get('login', False):
    st.warning("로그인이 필요합니다.")
    st.stop()

show_sidebar()

st.title("💸 나의 소비습관 진단")
st.write("아래 20가지 질문에 솔직하게 답해주세요. 결과는 5페이지에서 가계부 데이터와 비교할 수 있어요!")

current_user = st.session_state.current_user

QUESTIONS = [
    {"id": 1,  "category": "저축/재무목표", "q": "나는 월급을 받으면 저축을 먼저 하고 남은 돈을 쓴다.",                    "reverse": False},
    {"id": 2,  "category": "저축/재무목표", "q": "나는 최소 3개월치 생활비에 해당하는 비상금을 갖고 있다.",                  "reverse": False},
    {"id": 3,  "category": "저축/재무목표", "q": "나는 구체적인 재무 목표(ex. 내 집 마련, 노후 준비 등)를 세우고 있다.",     "reverse": False},
    {"id": 4,  "category": "저축/재무목표", "q": "갑작스럽게 100만 원의 지출이 생겨도 큰 어려움 없이 감당할 수 있다.",       "reverse": False},
    {"id": 5,  "category": "지출통제",     "q": "나는 물건을 살 때 계획하지 않은 충동구매를 자주 한다.",                    "reverse": True},
    {"id": 6,  "category": "지출통제",     "q": "나는 매달 지출 예산을 미리 세우고 지키려고 노력한다.",                     "reverse": False},
    {"id": 7,  "category": "지출통제",     "q": "나는 가계부나 지출 기록을 꾸준히 작성한다.",                              "reverse": False},
    {"id": 8,  "category": "지출통제",     "q": "나는 월말이 되면 돈이 어디에 쓰였는지 잘 모를 때가 많다.",                 "reverse": True},
    {"id": 9,  "category": "신용/부채관리", "q": "나는 신용카드 대금을 매달 전액 납부한다.",                               "reverse": False},
    {"id": 10, "category": "신용/부채관리", "q": "나는 대출이나 카드값을 연체한 적이 있다.",                               "reverse": True},
    {"id": 11, "category": "신용/부채관리", "q": "나는 내 신용점수가 어느 정도인지 알고 있다.",                             "reverse": False},
    {"id": 12, "category": "신용/부채관리", "q": "나는 할부보다 일시불 결제를 선호한다.",                                  "reverse": False},
    {"id": 13, "category": "재무여유도",   "q": "나는 월말이 되어도 통장에 돈이 남아있는 편이다.",                          "reverse": False},
    {"id": 14, "category": "재무여유도",   "q": "나는 돈 걱정으로 스트레스를 받는 일이 거의 없다.",                         "reverse": False},
    {"id": 15, "category": "재무여유도",   "q": "나는 친구 경조사 등 예상치 못한 지출에도 여유 있게 대응할 수 있다.",         "reverse": False},
    {"id": 16, "category": "재무여유도",   "q": "나는 현재 내 재정 상태에 전반적으로 만족한다.",                            "reverse": False},
    {"id": 17, "category": "소비가치관",   "q": "나는 물건을 살 때 가격 대비 가치를 꼼꼼히 따지는 편이다.",                  "reverse": False},
    {"id": 18, "category": "소비가치관",   "q": "나는 현재의 소비보다 미래를 위한 저축이 더 중요하다고 생각한다.",             "reverse": False},
    {"id": 19, "category": "소비가치관",   "q": "나는 세일이나 할인 행사에 충동적으로 구매하지 않는다.",                     "reverse": False},
    {"id": 20, "category": "소비가치관",   "q": "나는 소득이 늘어나면 저축액도 함께 늘린다.",                              "reverse": False},
]

SCALE = ["1 - 전혀 그렇지 않다", "2 - 그렇지 않다", "3 - 보통이다", "4 - 그렇다", "5 - 매우 그렇다"]

cat_display = {
    "저축/재무목표": "💰 저축/재무목표",
    "지출통제":     "📊 지출통제",
    "신용/부채관리": "💳 신용/부채관리",
    "재무여유도":   "😌 재무여유도",
    "소비가치관":   "🧠 소비가치관"
}

type_colors = {
    "💎 재테크형":       "#4CAF50",
    "⚖️ 균형형":        "#2196F3",
    "🛍️ 소비형":       "#FF9800",
    "⚠️ 과소비 주의형":  "#F44336"
}

# 설문 완료 후 결과 표시 
if st.session_state.get('show_survey_result'):
    pct         = st.session_state.survey_pct
    total_score = st.session_state.survey_score
    cat_avg     = st.session_state.survey_cat_avg
    survey_type = st.session_state.survey_type
    color       = type_colors.get(survey_type, "#888")

    advice_map = {
        "💎 재테크형": [
            "✅ 현재 저축 습관을 꾸준히 유지하세요.",
            "📈 저축한 돈을 예·적금 외에 펀드, ETF 등으로 분산 투자해보세요.",
            "🎯 재무 목표를 더 구체적으로 세우고 점검해보세요."
        ],
        "⚖️ 균형형": [
            "💰 저축률을 5% 정도만 더 올려보세요.",
            "📊 지출 항목 중 가장 큰 비중을 차지하는 것을 점검해보세요.",
            "🗓️ 월말에 가계부를 보며 다음 달 예산을 미리 짜보세요."
        ],
        "🛍️ 소비형": [
            "💡 월급날 저축부터 먼저 하는 '선저축 후소비' 습관을 만들어보세요.",
            "🛒 쇼핑 전 24시간 기다려보는 규칙을 만들어보세요.",
            "📱 통신비, 구독 서비스 등 고정지출을 점검해보세요."
        ],
        "⚠️ 과소비 주의형": [
            "🚨 이번 달 지출 내역을 보고 당장 줄일 수 있는 항목을 찾아보세요.",
            "💳 신용카드 대신 체크카드나 현금을 사용해 지출을 체감해보세요.",
            "🏦 비상금 통장에 최소 50만 원이라도 먼저 만들어보세요.",
            "📋 다음 달은 항목별 예산 한도를 미리 정해두세요."
        ]
    }

    st.divider()
    st.subheader("📊 설문 결과")
    st.metric("총점", f"{total_score}점 / 100점 ({pct}%)")
    st.progress(pct / 100)

    st.subheader("📋 영역별 점수")
    cat_df = pd.DataFrame({
        "영역": [cat_display[c] for c in cat_avg],
        "평균 점수 (5점 만점)": list(cat_avg.values()),
        "상태": ["✅ 양호" if v >= 3.5 else "⚠️ 주의" for v in cat_avg.values()]
    })
    st.dataframe(cat_df, use_container_width=True, hide_index=True)

    st.divider()
    st.subheader("🔍 설문 기반 소비 유형")
    st.markdown(
        f"""
        <div style="background:{color}18; border:2px solid {color};
                    border-radius:14px; padding:24px; text-align:center;
                    margin-bottom:16px;">
            <h2 style="color:{color}; margin:0 0 8px 0;">{survey_type}</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.subheader("💡설문 기반 맞춤 조언")
    for tip in advice_map.get(survey_type, []):
        st.markdown(f"- {tip}")

    st.divider()
    st.info("✅ 설문이 완료되었습니다! 5페이지에서 가계부 데이터와 비교해보세요.")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📊 결과 비교하러 가기", key="go_compare"):
            st.switch_page("pages/5결과비교.py")
    with col2:
        if st.button("🔄 설문 다시 하기", key="redo_survey"):
            st.session_state.show_survey_result = False
            st.session_state.survey_done = False
            st.rerun()

    st.stop()  

# 설문 폼 
st.divider()
st.subheader("📝 소비습관 설문 (20문항)")
st.caption("CFPB 재무웰빙척도 · Dew & Xiao 재무행동척도 · 금감원 금융이해력 조사 기반")

with st.form("survey_form"):
    answers = {}
    current_category = ""

    for q in QUESTIONS:
        if q["category"] != current_category:
            current_category = q["category"]
            category_names = {
                "저축/재무목표": "💰 저축 / 재무 목표",
                "지출통제":     "📊 지출 통제",
                "신용/부채관리": "💳 신용 / 부채 관리",
                "재무여유도":   "😌 재무 여유도",
                "소비가치관":   "🧠 소비 가치관"
            }
            st.subheader(category_names[current_category])

        ans = st.radio(
            f"Q{q['id']}. {q['q']}",
            SCALE,
            key=f"q{q['id']}",
            horizontal=True,
            label_visibility="visible"
        )
        answers[q['id']] = ans

    submitted = st.form_submit_button("📊 결과 분석하기", use_container_width=True)

if submitted:
    total_score = 0
    category_scores = {}

    for q in QUESTIONS:
        raw = int(answers[q['id']][0])
        score = (6 - raw) if q['reverse'] else raw
        total_score += score

        cat = q['category']
        if cat not in category_scores:
            category_scores[cat] = []
        category_scores[cat].append(score)

    cat_avg   = {cat: round(sum(v)/len(v), 1) for cat, v in category_scores.items()}
    max_score = 100
    pct       = int(total_score / max_score * 100)

    if pct >= 80:
        survey_type = "💎 재테크형"
    elif pct >= 65:
        survey_type = "⚖️ 균형형"
    elif pct >= 50:
        survey_type = "🛍️ 소비형"
    else:
        survey_type = "⚠️ 과소비 주의형"

    # 세션 저장 후 rerun
    st.session_state.survey_type         = survey_type
    st.session_state.survey_score        = total_score
    st.session_state.survey_pct          = pct
    st.session_state.survey_cat_avg      = cat_avg
    st.session_state.survey_done         = True
    st.session_state.show_survey_result  = True 
    st.rerun()