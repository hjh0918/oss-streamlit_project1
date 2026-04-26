# import streamlit as st
# import json
# import pandas as pd
# from datetime import date
# import os
# from utils import load_ledger  # ← 추가
# import plotly.express as px  # ← 추가
# from utils import load_ledger, show_sidebar


# show_sidebar()
# # 로그인 체크
# if not st.session_state.get('login', False):
#     st.warning("로그인이 필요합니다.")
#     st.stop()

# LEDGER_FILE = "data/ledger_data.json"

# # 계정과목 목록 (사용자가 선택 가능)
# CATEGORIES = ["식비", "교통비", "주거비", "의료비", "교육비", 
#                "여가/취미", "쇼핑/의류", "통신비", "저축/투자", "기타"]

# # ── 데이터 로드/저장 함수 ──────────────────────────
# @st.cache_data
# def load_ledger():
#     """캐싱 이유: JSON을 매번 읽으면 느리므로 한 번만 읽고 재사용"""
#     if not os.path.exists(LEDGER_FILE):
#         return []
#     with open(LEDGER_FILE, "r", encoding="utf-8") as f:
#         return json.load(f)

# def save_ledger(data):
#     os.makedirs("data", exist_ok=True)
#     with open(LEDGER_FILE, "w", encoding="utf-8") as f:
#         json.dump(data, f, ensure_ascii=False, indent=2)
#     # 캐시 초기화 (새 데이터 반영을 위해)
#     load_ledger.clear()

# # ── UI ──────────────────────────────────────────────
# st.title("📒 가계부")
# current_user = st.session_state.current_user

# # 지출 입력 폼
# with st.expander("➕ 지출 추가하기", expanded=True):
#     with st.form("add_expense"):
#         col1, col2 = st.columns(2)
#         with col1:
#             exp_date = st.date_input("날짜", value=date.today())
#             category = st.selectbox("계정과목", CATEGORIES)
#         with col2:
#             amount = st.number_input("금액 (원)", min_value=0, step=1000)
#             memo = st.text_input("메모 (선택)")
        
#         if st.form_submit_button("저장"):
#             record = {
#                 "user": current_user,
#                 "date": str(exp_date),
#                 "year": exp_date.year,
#                 "month": exp_date.month,
#                 "category": category,
#                 "amount": amount,
#                 "memo": memo
#             }
#             all_data = load_ledger()
#             all_data.append(record)
#             save_ledger(all_data)
#             st.success("저장되었습니다!")
#             st.rerun()

# # 내 데이터만 필터링
# all_data = load_ledger()
# my_data = [r for r in all_data if r["user"] == current_user]

# if not my_data:
#     st.info("아직 지출 내역이 없습니다. 위에서 추가해보세요!")
# else:
#     df = pd.DataFrame(my_data)
    
#     # ── 필터: 연도/월 선택 ──
#     st.subheader("📊 지출 분석")
#     col1, col2 = st.columns(2)
#     with col1:
#         years = sorted(df["year"].unique(), reverse=True)
#         sel_year = st.selectbox("연도", years)
#     with col2:
#         months = sorted(df[df["year"]==sel_year]["month"].unique())
#         sel_month = st.selectbox("월", months)
    
#     filtered = df[(df["year"]==sel_year) & (df["month"]==sel_month)]
    
#     # 월별 합계
#     total = filtered["amount"].sum()
#     st.metric(f"{sel_year}년 {sel_month}월 총 지출", f"{total:,}원")
    
#     # 계정과목별 차트
#     by_category = filtered.groupby("category")["amount"].sum().reset_index()
#     st.bar_chart(by_category.set_index("category"))
    
#     # 상세 내역 테이블
#     st.dataframe(
#         filtered[["date","category","amount","memo"]].sort_values("date", ascending=False),
#         use_container_width=True
#     )
    
   
#     # 연간 월별 추이
#     st.subheader(f"📈 {sel_year}년 월별 지출 추이")

#     # 1~12월 전체 틀 만들기 (데이터 없는 달은 0으로 채움)
#     all_months = pd.DataFrame({"month": range(1, 13)})
#     yearly = df[df["year"] == sel_year].groupby("month")["amount"].sum().reset_index()
#     yearly = all_months.merge(yearly, on="month", how="left").fillna(0)
#     yearly["month_label"] = yearly["month"].astype(str) + "월"

#     fig = px.line(
#         yearly,
#         x="month_label",
#         y="amount",
#         markers=True,
#         labels={"month_label": "월", "amount": "지출 금액 (원)"},
#     )
#     fig.update_layout(
#         xaxis=dict(categoryorder="array", categoryarray=[f"{m}월" for m in range(1, 13)]),
#         yaxis_tickformat=",",   # 세로축 천 단위 콤마
#     )
#     st.plotly_chart(fig, use_container_width=True)

import streamlit as st
import pandas as pd
from datetime import date
import plotly.express as px
from utils import load_ledger, save_ledger, show_sidebar

# 로그인 체크
if not st.session_state.get('login', False):
    st.warning("로그인이 필요합니다.")
    st.stop()

show_sidebar()

CATEGORIES = ["식비", "교통비", "주거비", "의료비", "교육비",
               "여가/취미", "쇼핑/의류", "통신비", "저축/투자", "기타"]

st.title("📒 가계부")
current_user = st.session_state.current_user

# ── 지출 추가 ───────────────────────────────────────
with st.expander("➕ 지출 추가하기", expanded=True):
    with st.form("add_expense"):
        col1, col2 = st.columns(2)
        with col1:
            exp_date = st.date_input("날짜", value=date.today())
            category = st.selectbox("계정과목", CATEGORIES)
        with col2:
            amount = st.number_input("금액 (원)", min_value=0, step=1000)
            memo   = st.text_input("메모 (선택)")

        if st.form_submit_button("저장"):
            record = {
                "user":     current_user,
                "date":     str(exp_date),
                "year":     exp_date.year,
                "month":    exp_date.month,
                "category": category,
                "amount":   amount,
                "memo":     memo
            }
            all_data = load_ledger()
            all_data.append(record)
            save_ledger(all_data)
            st.success("저장되었습니다!")
            st.rerun()

# ── 내 데이터 필터링 ────────────────────────────────
all_data = load_ledger()
my_data  = [r for r in all_data if r["user"] == current_user]

if not my_data:
    st.info("아직 지출 내역이 없습니다. 위에서 추가해보세요!")
else:
    df = pd.DataFrame(my_data)
    # 원본 인덱스 보존 (삭제용)
    df["_idx"] = [i for i, r in enumerate(all_data) if r["user"] == current_user]

    # ── 연도/월 선택 ──
    st.subheader("📊 지출 분석")
    col1, col2 = st.columns(2)
    with col1:
        years     = sorted(df["year"].unique(), reverse=True)
        sel_year  = st.selectbox("연도", years)
    with col2:
        months    = sorted(df[df["year"] == sel_year]["month"].unique())
        sel_month = st.selectbox("월", months)

    filtered = df[(df["year"] == sel_year) & (df["month"] == sel_month)]

    # 월 합계
    total = filtered["amount"].sum()
    st.metric(f"{sel_year}년 {sel_month}월 총 지출", f"{total:,}원")

    # 계정과목별 차트
    by_category = filtered.groupby("category")["amount"].sum().reset_index()
    st.bar_chart(by_category.set_index("category"))

    # ── 상세 내역 + 삭제 ────────────────────────────
    st.subheader("📋 지출 내역")
    st.caption("잘못 입력한 항목은 🗑️ 버튼으로 삭제할 수 있어요.")

    for _, row in filtered.sort_values("date", ascending=False).iterrows():
        col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 2, 1])
        with col1:
            st.write(row["date"])
        with col2:
            st.write(row["category"])
        with col3:
            st.write(f"{int(row['amount']):,}원")
        with col4:
            st.write(row["memo"] if row["memo"] else "-")
        with col5:
            if st.button("🗑️", key=f"del_{row['_idx']}"):
                all_data = load_ledger()
                all_data.pop(row["_idx"])
                save_ledger(all_data)
                st.success("삭제되었습니다!")
                st.rerun()

    st.divider()

    # ── 월별 추이 ───────────────────────────────────
    st.subheader(f"📈 {sel_year}년 월별 지출 추이")
    all_months = pd.DataFrame({"month": range(1, 13)})
    yearly     = df[df["year"] == sel_year].groupby("month")["amount"].sum().reset_index()
    yearly     = all_months.merge(yearly, on="month", how="left").fillna(0)
    yearly["month_label"] = yearly["month"].astype(str) + "월"

    fig = px.line(
        yearly, x="month_label", y="amount", markers=True,
        labels={"month_label": "월", "amount": "지출 금액 (원)"}
    )
    fig.update_traces(hovertemplate="%{x}: %{y:,}원<extra></extra>")
    fig.update_layout(
        xaxis=dict(categoryorder="array",
                   categoryarray=[f"{m}월" for m in range(1, 13)]),
        yaxis_tickformat=","
    )
    st.plotly_chart(fig, use_container_width=True)