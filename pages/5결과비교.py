import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date
from utils import load_ledger, show_sidebar

if not st.session_state.get('login', False):
    st.warning("로그인이 필요합니다.")
    st.stop()

show_sidebar()

st.title("📊 종합 결과 비교")
st.write("소비습관 설문 결과와 실제 가계부 데이터 기반 분석을 비교해드려요!")

current_user = st.session_state.current_user

survey_done  = st.session_state.get('survey_done', False)
ledger_done  = st.session_state.get('user_type', None)

# 완료 여부 확인
col1, col2 = st.columns(2)
with col1:
    if survey_done:
        st.success("✅ 소비습관 설문 완료")
    else:
        st.warning("⚠️ 소비습관 설문 미완료")
        if st.button("💸 설문하러 가기", use_container_width=True):
            st.switch_page("pages/4소비습관설문.py")

with col2:
    if ledger_done:
        st.success("✅ 가계부 소비성향 분석 완료")
    else:
        st.warning("⚠️ 소비성향 분석 미완료")
        if st.button("🛍️ 소비성향 분석하러 가기", use_container_width=True):
            st.switch_page("pages/3소비성향.py")

st.divider()

# 둘 다 완료된 경우 비교 
if survey_done and ledger_done:

    survey_type = st.session_state.get('survey_type', '-')
    ledger_type = st.session_state.get('user_type', '-')
    survey_pct  = st.session_state.get('survey_pct', 0)
    cat_avg     = st.session_state.get('survey_cat_avg', {})

    # 두 결과 나란히 비교 
    st.subheader("🔍 소비 유형 비교")

    col1, col2 = st.columns(2)

    type_colors = {
        "💎 재테크형":    "#4CAF50",
        "⚖️ 균형형":     "#2196F3",
        "🛍️ 소비형":    "#FF9800",
        "⚠️ 과소비 주의형": "#F44336"
    }

    survey_color = type_colors.get(survey_type, "#888")
    ledger_color = type_colors.get(ledger_type, "#888")

    with col1:
        st.markdown(
            f"""
            <div style="background:{survey_color}18; border:2px solid {survey_color};
                        border-radius:14px; padding:20px; text-align:center;">
                <p style="margin:0; font-size:13px; color:#888;">📝 설문 기반 소비 유형</p>
                <h2 style="margin:8px 0 0 0; color:{survey_color};">{survey_type}</h2>
                <p style="margin:4px 0 0 0; font-size:13px; color:#666;">설문 점수: {survey_pct}점</p>
            </div>
            """, unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f"""
            <div style="background:{ledger_color}18; border:2px solid {ledger_color};
                        border-radius:14px; padding:20px; text-align:center;">
                <p style="margin:0; font-size:13px; color:#888;">📒 가계부 데이터 기반 소비 유형</p>
                <h2 style="margin:8px 0 0 0; color:{ledger_color};">{ledger_type}</h2>
                <p style="margin:4px 0 0 0; font-size:13px; color:#666;">실제 지출 데이터 기반</p>
            </div>
            """, unsafe_allow_html=True
        )

    st.divider()

    # 일치/불일치 메시지 
    if survey_type == ledger_type:
        st.success(
            f"✅ 두 결과가 일치해요! **{survey_type}**\n\n"
            "본인의 소비 습관을 정확하게 인식하고 있어요. 현재 습관을 꾸준히 유지해보세요!"
        )
    else:
        st.warning(
            f"⚠️ 두 결과가 다르게 나왔어요!\n\n"
            f"설문에서는 **{survey_type}** 이지만 실제 가계부 데이터는 **{ledger_type}** 이에요.\n\n"
            "생각과 실제 소비 사이에 차이가 있어요. 가계부를 꾸준히 기록하며 지출을 점검해보세요!"
        )

    st.divider()

    # 설문 영역별 점수 차트 
    if cat_avg:
        st.subheader("📋 소비습관 영역별 점수")

        cat_display = {
            "저축/재무목표": "💰 저축/재무목표",
            "지출통제":     "📊 지출통제",
            "신용/부채관리": "💳 신용/부채관리",
            "재무여유도":   "😌 재무여유도",
            "소비가치관":   "🧠 소비가치관"
        }

        cat_df = pd.DataFrame({
            "영역": [cat_display.get(c, c) for c in cat_avg],
            "내 점수": list(cat_avg.values()),
            "권장 점수": [3.5] * len(cat_avg)
        })

        fig = px.bar(
            cat_df,
            x="영역",
            y=["내 점수", "권장 점수"],
            barmode="group",
            color_discrete_map={"내 점수": "#636EFA", "권장 점수": "#EF553B"},
            labels={"value": "점수 (5점 만점)", "variable": "구분"}
        )
        fig.update_layout(yaxis_range=[0, 5])
        st.plotly_chart(fig, use_container_width=True)

        # 개선 필요 영역
        weak_cats = [cat_display.get(c, c) for c, v in cat_avg.items() if v < 3.5]
        if weak_cats:
            st.subheader("💡 개선이 필요한 영역")
            for cat in weak_cats:
                st.markdown(f"- **{cat}** — 평균 점수가 낮아요. 집중적으로 개선해보세요!")
        else:
            st.success("✅ 모든 영역에서 양호한 점수를 받았어요!")

    st.divider()

    # 이번 달 가계부 요약 
    st.subheader("💰 이번 달 지출 현황")

    all_data = load_ledger()
    my_data  = [r for r in all_data if r["user"] == current_user]

    if my_data:
        df = pd.DataFrame(my_data)
        this_month = df[
            (df["year"]  == date.today().year) &
            (df["month"] == date.today().month)
        ]
        if not this_month.empty:
            total = int(this_month["amount"].sum())
            top_cat = this_month.groupby("category")["amount"].sum().idxmax()
            col1, col2 = st.columns(2)
            with col1:
                st.metric("이번 달 총 지출", f"{total:,}원")
            with col2:
                st.metric("지출 1위 항목", top_cat)
        else:
            st.info("이번 달 가계부 데이터가 없어요.")
    else:
        st.info("가계부 데이터가 없어요. 가계부를 먼저 작성해주세요!")

    st.divider()

    # 종합 조언 
    st.subheader("🎯 종합 조언")

    if survey_type == ledger_type and "재테크형" in survey_type:
        st.success("완벽해요! 생각과 행동이 일치하는 재테크형입니다. 투자 다변화를 고려해보세요.")
    elif survey_type == ledger_type and "균형형" in survey_type:
        st.info("좋아요! 균형잡힌 소비를 하고 있어요. 저축률을 조금만 더 올려보세요.")
    elif survey_type != ledger_type:
        st.warning(
            "설문과 실제 데이터가 다르게 나왔어요. "
            "가계부를 꾸준히 작성하면서 실제 지출 패턴을 파악하고 "
            "소비 습관을 개선해나가는 것을 목표로 해보세요!"
        )

    # 다시 분석하기 버튼
    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        if st.button("💸 설문 다시 하기", use_container_width=True):
            st.session_state.survey_done = False
            st.switch_page("pages/4소비습관설문.py")
    with col2:
        if st.button("🛍️ 소비성향 다시 분석", use_container_width=True):
            st.switch_page("pages/3소비성향.py")

# 둘 중 하나만 완료된 경우 
elif survey_done and not ledger_done:
    st.info("📒 가계부 소비성향 분석을 완료하면 비교 결과를 볼 수 있어요!")
elif not survey_done and ledger_done:
    st.info("💸 소비습관 설문을 완료하면 비교 결과를 볼 수 있어요!")
else:
    st.info("💡 소비습관 설문과 가계부 소비성향 분석을 모두 완료하면 비교 결과를 볼 수 있어요!")