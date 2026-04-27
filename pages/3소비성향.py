import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_ledger, show_sidebar, save_ledger

# 로그인 체크
if not st.session_state.get('login', False):
    st.warning("로그인이 필요합니다.")
    st.stop()

show_sidebar()

st.title("🛍️ 나의 소비 성향 분석")
current_user = st.session_state.current_user

# 가계부 데이터 불러오기
all_data = load_ledger()
my_data = [r for r in all_data if r["user"] == current_user]

if not my_data:
    st.warning("⚠️ 가계부 데이터가 없습니다. 먼저 가계부에서 지출을 입력해주세요!")
    st.stop()

df = pd.DataFrame(my_data)

# 분석 기간 선택
st.subheader("📅 분석 기간 선택")
col1, col2 = st.columns(2)
with col1:
    years = sorted(df["year"].unique(), reverse=True)
    sel_year = st.selectbox("연도", years)
with col2:
    months = sorted(df[df["year"] == sel_year]["month"].unique())
    sel_month = st.selectbox("월", months)

filtered = df[(df["year"] == sel_year) & (df["month"] == sel_month)]

if filtered.empty:
    st.info("선택한 기간의 데이터가 없습니다.")
    st.stop()

st.divider()

# 월 소득 입력
st.subheader("💰 이번 달 소득 입력")
st.caption("저축률 계산을 위해 세후 실수령액을 입력해주세요.")

default_income = st.session_state.get('monthly_income', 2500000)
monthly_income = st.number_input("월 소득 (원)", min_value=0, step=100000, value=default_income)
st.session_state.monthly_income = monthly_income

st.divider()

# 카테고리별 지출 계산
total = filtered["amount"].sum()
by_cat = filtered.groupby("category")["amount"].sum()

def get_amt(cat):
    return by_cat.get(cat, 0)

# 50/30/20 그룹핑
ESSENTIAL = ["식비", "교통비", "주거비", "의료비", "통신비", "교육비"]
LEISURE   = ["여가/취미", "쇼핑/의류", "기타"]
SAVING    = ["저축/투자"]

essential_amt = sum(get_amt(c) for c in ESSENTIAL)
leisure_amt   = sum(get_amt(c) for c in LEISURE)
saving_amt    = get_amt("저축/투자")

# 소득 대비 비율 (소득 입력 시)
income_base = monthly_income if monthly_income > 0 else total

saving_rate    = saving_amt    / income_base * 100
essential_rate = essential_amt / income_base * 100
leisure_rate   = leisure_amt   / income_base * 100

# 총지출 대비 비율
food_rate    = get_amt("식비")    / total * 100 if total > 0 else 0
housing_rate = get_amt("주거비")  / income_base * 100 if income_base > 0 else 0

# 핵심 지표 카드
st.subheader(f"📊 {sel_year}년 {sel_month}월 핵심 지표")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("이번 달 총 지출", f"{total:,}원")
with col2:
    st.metric(
        "저축률",
        f"{saving_rate:.1f}%",
        delta="권장 20% 이상" if saving_rate < 20 else "✅ 달성"
    )
with col3:
    st.metric(
        "식비 비율 (엥겔지수)",
        f"{food_rate:.1f}%",
        delta="권장 15% 이하" if food_rate > 15 else "✅ 양호"
    )
with col4:
    st.metric(
        "주거비 비율",
        f"{housing_rate:.1f}%",
        delta="권장 30% 이하" if housing_rate > 30 else "✅ 양호"
    )
    
st.caption("💡 저축률·주거비·필수지출·여가 비율은 소득 기준 / 식비(엥겔지수)는 총지출 기준")
st.divider()

# 50/30/20 법칙 비교
st.subheader("📐 50/30/20 법칙으로 본 내 지출")
st.caption("소득 기준 권장: 필수지출 50% 이하 / 여가·욕구 30% 이하 / 저축·투자 20% 이상")

compare_data = {
    "항목":        ["✅ 필수지출", "🎯 여가/욕구", "💰 저축/투자"],
    "내 비율(%)":  [round(essential_rate,1), round(leisure_rate,1), round(saving_rate,1)],
    "권장 비율(%)": [50, 30, 20],
    "상태":        [
        "✅ 양호" if essential_rate <= 50 else "⚠️ 초과",
        "✅ 양호" if leisure_rate   <= 30 else "⚠️ 초과",
        "✅ 달성" if saving_rate    >= 20 else "⚠️ 미달",
    ]
}
compare_df = pd.DataFrame(compare_data)
st.dataframe(compare_df, use_container_width=True, hide_index=True)

# 막대 차트 비교
fig = px.bar(
    compare_df,
    x="항목",
    y=["내 비율(%)", "권장 비율(%)"],
    barmode="group",
    color_discrete_map={"내 비율(%)": "#636EFA", "권장 비율(%)": "#EF553B"},
    labels={"value": "비율 (%)", "variable": "구분"}
)

max_val = max(essential_rate, leisure_rate, saving_rate, 100)
fig.update_layout(yaxis_range=[0, max_val + 10])
st.plotly_chart(fig, use_container_width=True)


st.divider()

# 소비 유형 판별
st.subheader("🔍 나의 소비 유형 진단")

# 점수 계산 (총 10점)
score = 0

# 저축률 (4점)
if saving_rate >= 30:   score += 4
elif saving_rate >= 20: score += 3
elif saving_rate >= 10: score += 2
elif saving_rate >= 5:  score += 1

# 필수지출 비율 (2점)
if essential_rate <= 50:   score += 2
elif essential_rate <= 60: score += 1

# 여가/쇼핑 비율 (2점)
if leisure_rate <= 20:   score += 2
elif leisure_rate <= 30: score += 1

# 엥겔지수 식비 (1점)
if food_rate <= 15: score += 1

# 주거비 (1점)
if housing_rate <= 30: score += 1

# 유형 결정
if score >= 8:
    user_type = "💎 재테크형"
    color     = "#4CAF50"
    summary   = "저축률이 높고 지출이 균형 잡혀 있어요!"
    advice    = [
        "✅ 현재 저축 습관을 꾸준히 유지하세요.",
        "📈 저축한 돈을 예·적금 외에 펀드, ETF 등으로 분산 투자해보세요.",
        "🎯 재무 목표(내 집 마련, 노후 준비 등)를 구체적으로 세워보세요."
    ]
elif score >= 6:
    user_type = "⚖️ 균형형"
    color     = "#2196F3"
    summary   = "50/30/20 법칙에 가까운 건강한 소비 패턴이에요."
    advice    = [
        "💰 저축률을 5% 정도만 더 올려보세요.",
        "📊 지출 항목 중 가장 큰 비중을 차지하는 것을 점검해보세요.",
        "🗓️ 월말에 가계부를 보며 다음 달 예산을 미리 짜보세요."
    ]
elif score >= 4:
    user_type = "🛍️ 소비형"
    color     = "#FF9800"
    summary   = "여가·쇼핑 지출이 많거나 저축이 다소 부족해요."
    advice    = [
        "💡 월급날 저축부터 먼저 하는 '선저축 후소비' 습관을 만들어보세요.",
        "🛒 쇼핑 전 24시간 기다려보는 규칙을 만들어보세요.",
        "📱 통신비, 구독 서비스 등 고정지출을 점검해보세요."
    ]
else:
    user_type = "⚠️ 과소비 주의형"
    color     = "#F44336"
    summary   = "지출이 소득을 위협할 수 있어요. 지금 바로 점검이 필요해요!"
    advice    = [
        "🚨 이번 달 지출 내역을 보고 당장 줄일 수 있는 항목을 찾아보세요.",
        "💳 신용카드 대신 체크카드나 현금을 사용해 지출을 체감해보세요.",
        "🏦 비상금 통장에 최소 50만 원이라도 먼저 만들어보세요.",
        "📋 다음 달은 항목별 예산 한도를 미리 정해두세요."
    ]

# 유형 카드
st.markdown(
    f"""
    <div style="background:{color}18; border:2px solid {color};
                border-radius:14px; padding:24px; text-align:center;
                margin-bottom:16px;">
        <h2 style="color:{color}; margin:0 0 8px 0;">{user_type}</h2>
        <p style="font-size:17px; margin:0; color:#333;">{summary}</p>
    </div>
    """,
    unsafe_allow_html=True
)

# 맞춤 조언
st.subheader("💡가계부 기반 맞춤 소비 조언")
for tip in advice:
    st.markdown(f"- {tip}")

# 세션 저장 (my_status 연동)
st.session_state.user_type = user_type

st.divider()

# 계정과목별 상세 내역
st.subheader("📋 계정과목별 지출 상세")

rows = []
for cat, amt in by_cat.items():
    pct_total  = amt / total * 100 if total > 0 else 0
    pct_income = amt / income_base * 100 if income_base > 0 else 0

    # 항목별 권장 기준
    if cat == "식비":
        status = "✅" if pct_total <= 15 else "⚠️"
        guide  = "총지출의 15% 이하 권장"
    elif cat == "주거비":
        status = "✅" if pct_income <= 30 else "⚠️"
        guide  = "소득의 30% 이하 권장"
    elif cat == "저축/투자":
        status = "✅" if pct_income >= 20 else "⚠️"
        guide  = "소득의 20% 이상 권장"
    elif cat in ["여가/취미", "쇼핑/의류"]:
        status = "✅" if pct_income <= 15 else "⚠️"
        guide  = "소득의 15% 이하 권장"
    else:
        status = "✅"
        guide  = "-"

    rows.append({
        "계정과목": cat,
        "금액 (원)": f"{amt:,}",
        "총지출 대비": f"{pct_total:.1f}%",
        "소득 대비": f"{pct_income:.1f}%",
        "권장 기준": guide,
        "상태": status
    })

detail_df = pd.DataFrame(rows)
st.dataframe(detail_df, use_container_width=True, hide_index=True)

# 파이 차트
st.subheader("🥧 지출 구성 비율")
pie_fig = px.pie(
    values=by_cat.values,
    names=by_cat.index,
    hole=0.4,
)
pie_fig.update_traces(textposition='inside', textinfo='percent+label')
st.plotly_chart(pie_fig, use_container_width=True)