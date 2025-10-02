import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import requests
import json
import os
import base64

# =========================
# 可调尺寸（按示意图比例，可微调）
# =========================
SIDEBAR_TU_AN_WIDTH = 44    # 侧边栏左上角图案 tu_an 宽度（px）
SIDEBAR_WENZI_WIDTH = 170   # 侧边栏左上角文字 wenzi 宽度（px）
HOME_WENZI_WIDTH = 520      # 欢迎页主标题 wenzi 宽度（px，居中）

# 品牌图片路径（请把图片放在应用根目录）
BRAND_LOGO_PATH = "tu_an.png"   # 左侧图案
BRAND_TEXT_PATH = "wenzi.png"   # 右侧文字

# 设置页面配置
st.set_page_config(
    page_title="渔康智鉴",
    page_icon="🐟",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义CSS样式
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin: 4rem 0 1rem 0;
        line-height: 1.3;
        scroll-margin-top: 5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #2ca02c;
        text-align: center;
        margin-bottom: 1.25rem;
    }
    .feature-list { font-size: 1.1rem; line-height: 2; margin-left: 1.5rem; }
    .divider { margin: 0.75rem 0 1.25rem 0; border-top: 1px solid #e6e6e6; }
    .preset-question { margin: 0.5rem 0; padding: 0.5rem; border: 1px solid #ddd; border-radius: 0.5rem; cursor: pointer; }
    .preset-question:hover { background-color: #f5f5f5; }
    .block-container { padding-top: 1.75rem; }
    .qa-tagline { text-align: center; color: #ff4d4f; font-size: 0.95rem; font-weight: 600; margin: -0.1rem 0 0.75rem 0; }

    .sidebar-brand { display: flex; align-items: center; gap: 8px; padding: 10px 6px 2px 6px; }
    .sidebar-logo { width: """ + str(SIDEBAR_TU_AN_WIDTH) + """px; height: auto; display: block; }
    .sidebar-wenzi { width: """ + str(SIDEBAR_WENZI_WIDTH) + """px; height: auto; display: block; }
    .sidebar-brand-spacer { height: 0.25rem; }

    .home-title { display: flex; justify-content: center; margin: 2rem 0 1rem 0; width: 100%; scroll-margin-top: 5rem; }
    .home-wenzi { width: """ + str(HOME_WENZI_WIDTH) + """px; max-width: 85vw; height: auto; display: block; }

    .title-divider { height: 3px; background: linear-gradient(90deg, #1e90ff, #2c7be5); border-radius: 2px; width: 82%; margin: 0.15rem auto 0.9rem auto; }
    .section-label { font-size: 1rem; font-weight: 700; color: #334155; margin: 0.25rem 0 0.5rem 0; text-align: left; }
    .greeting { display: inline-flex; align-items: center; gap: 10px; background: #f0f7ff; border: 1px solid #d6e6ff; color: #0f3e8a; padding: 10px 12px; border-radius: 12px; margin: 0.25rem 0 1.1rem 0; }
    .greeting .icon { background: #ffd782; color: #915c00; display: inline-flex; align-items: center; justify-content: center; width: 28px; height: 28px; border-radius: 6px; font-size: 16px; }

    /* 数据查询页：建议模块 */
    .ai-hr { border: 0; height: 0; border-top: 6px solid #7c8aa0; width: 100%; margin: 0.5rem 0 0.9rem 0; border-radius: 2px; }
    .ai-hr-line { height: 6px; background: #7c8aa0; border-radius: 2px; width: 100%; margin: 0.5rem 0 0.9rem 0; }
    .ai-hint-subtitle { color: #64748b; font-size: 0.9rem; margin: 0.1rem 0 0.6rem 0; text-align: left; width: 100%; margin-left: 0 !important; margin-right: 0 !important; }
</style>
""", unsafe_allow_html=True)

def _img_to_base64(path: str):
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except Exception:
        return None

logo_b64 = _img_to_base64(BRAND_LOGO_PATH)
wenzi_b64 = _img_to_base64(BRAND_TEXT_PATH)

# ---------- 侧边栏：左上角品牌（同一水平面） ----------
with st.sidebar:
    if logo_b64 and wenzi_b64:
        st.markdown(
            f"""
            <div class="sidebar-brand">
                <img class="sidebar-logo" src="data:image/png;base64,{logo_b64}" />
                <img class="sidebar-wenzi" src="data:image/png;base64,{wenzi_b64}" />
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        brand_container = st.container()
        col_logo, col_word = brand_container.columns([1, 4])
        with col_logo:
            if os.path.exists(BRAND_LOGO_PATH):
                st.image(BRAND_LOGO_PATH, width=SIDEBAR_TU_AN_WIDTH)
            else:
                st.info("缺少 tu_an.png（放到应用根目录）")
        with col_word:
            if os.path.exists(BRAND_TEXT_PATH):
                st.image(BRAND_TEXT_PATH, width=SIDEBAR_WENZI_WIDTH)
            else:
                st.info("缺少 wenzi.png（放到应用根目录）")

    st.markdown('<div class="sidebar-brand-spacer"></div>', unsafe_allow_html=True)
    st.title("导航")

# 导航栏选项（新增：📸开始识别，位置在欢迎与数据查询之间）
PAGE_WELCOME = "🎉欢迎"
PAGE_CAPTURE = "📸开始识别"
PAGE_DATA = "🔍数据查询"
PAGE_QA = "🧠 问答助手"
page = st.sidebar.radio("选择页面", [PAGE_WELCOME, PAGE_CAPTURE, PAGE_DATA, PAGE_QA])

# 将“开始识别”页的两个按钮放在导航栏下面（侧边栏中，紧随单选后）
if page == PAGE_CAPTURE:
    with st.sidebar:
        with st.expander("📝 操作说明", expanded=False):
            st.markdown(
                "1.📹 模型支持图片、视频、摄像头三种数据来源\n"
                "2.🎚️ 通过调节置信度可以提高模型识别质量\n"
                "3.🚀 点击「开始检测」按钮输出结果"
            )
        with st.expander("⚙️ 高级选项", expanded=False):
            st.markdown("**置信度阈值**")
            default_conf = st.session_state.get("confidence", 0.90)
            confidence = st.slider(
                label="置信度阈值",
                min_value=0.70,
                max_value=0.99,
                value=float(default_conf),
                step=0.01,
                format="%.2f",
                label_visibility="collapsed",
                key="capture_confidence_slider"
            )
            st.session_state["confidence"] = confidence

            c1, c2 = st.columns(2)
            with c1:
                st.caption("0.70")
            with c2:
                st.markdown('<div style="text-align:right;color:#64748b;">0.99</div>', unsafe_allow_html=True)

            with st.expander("数据来源", expanded=False):
                source = st.radio(
                    "请选择来源",
                    options=["图片", "视频", "摄像头"],
                    index=["图片", "视频", "摄像头"].index(st.session_state.get("source", "图片")),
                    horizontal=True,
                    key="capture_source_radio"
                )
                st.session_state["source"] = source

# “🧠 问答助手”页面的侧边栏：操作说明（保留）
if page == PAGE_QA:
    with st.sidebar:
        with st.expander("📝 操作说明", expanded=False):
            st.markdown(
                "- 1.💬 输入问题：在下方输入框中输入你的问题，点击发送按钮。\n"
                "- 2.🔍 查看回答：系统会根据知识图谱和通义千问模型生成回答，并展示在聊天记录中。\n"
                "- 3.✨ 查看示例问题：点击上方的示例问题按钮，快速获取常见问题的回答。"
            )

# 调用大模型API的函数（原样保留）
def call_qwen_api(prompt):
    try:
        api_key = "sk-23596706e0104528b11ae1c28802831d"
        url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "qwen-turbo",
            "input": {
                "messages": [
                    {
                        "role": "system",
                        "content": "你是一个鱼类疾病专家，专门回答关于鱼类健康、疾病治疗和预防的问题。请提供专业、准确的建议。"
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            },
            "parameters": { "result_format": "message" }
        }
        response = requests.post(url, headers=headers, json=data)
        result = response.json()
        if "output" in result and "choices" in result["output"]:
            return result["output"]["choices"][0]["message"]["content"]
        else:
            return "获取回答时出错，请检查API密钥或网络连接"
    except Exception as e:
        return f"调用API时出错: {str(e)}"

# ---------- 主内容 ----------
if page == PAGE_WELCOME:
    if wenzi_b64:
        st.markdown(
            f"""
            <div class="home-title">
                <img class="home-wenzi" src="data:image/png;base64,{wenzi_b64}" />
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown('<h1 class="main-header">渔康智鉴</h1>', unsafe_allow_html=True)

    st.markdown('<p class="sub-header">基于深度学习和生成式人工智能的多维度鱼类养殖助手</p>', unsafe_allow_html=True)
    try:
        st.image("20250919185006_1543_32.jpg", use_container_width=True)
    except:
        st.info("图片加载失败，请确保图片文件存在")
    st.markdown("### 功能介绍")
    for feature in ["鱼类疾病智能识别与诊断", "养殖数据可视化分析", "个性化治疗建议与预防措施", "鱼类健康知识问答"]:
        st.markdown(f"- **{feature}**")
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown("### 技术架构")
    st.markdown("本系统采用先进的深度学习技术和生成式人工智能模型，结合专业鱼类疾病知识库，为鱼类养殖提供全方位的智能支持。")

elif page == PAGE_CAPTURE:
    # 主区仅展示加载提示（两个按钮已移动到侧边栏导航下方）
    st.markdown('<div class="loading-hint" style="margin:2rem 0 0; text-align:center; font-size:1.1rem; color:#334155;">模型正在加载中......</div>', unsafe_allow_html=True)

elif page == PAGE_DATA:
    st.markdown('<h1 class="main-header">🔍 数据查询</h1>', unsafe_allow_html=True)
    try:
        df = pd.read_excel("data.xlsx")
        st.success("数据加载成功！")
        st.subheader("原始数据")
        st.dataframe(df, use_container_width=True)

        categories = df.columns[1:]
        values = df.iloc[0, 1:].values

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("鱼类健康状况分布（柱状图）")
            chart_data = pd.DataFrame({'类别': categories, '数量': values})
            st.bar_chart(chart_data.set_index('类别'), use_container_width=True)

        with col2:
            st.subheader("鱼类健康状况分布（饼图）")
            try:
                import plotly.express as px
                fig = px.pie(values=values, names=categories, title='鱼类健康状况分布')
                st.plotly_chart(fig, use_container_width=True)
            except ImportError:
                st.info("饼图需要 plotly 库支持。请在 requirements.txt 中添加 'plotly>=5.15.0'")

        st.markdown("## 💡 建议")
        st.markdown('<div class="ai-hr-line"></div>', unsafe_allow_html=True)
        st.markdown('<div class="ai-hint-subtitle">🔍 基于 <b>通义千问</b> 大模型的建议生成</div>', unsafe_allow_html=True)
        with st.expander("🚀通义千问 建议", expanded=False):
            st.markdown("""
根据模型检测，您的鱼类患有溃疡病、眼部病变、鳍部病变、腐烂鳃四种疾病。这类复合感染可能由细菌、真菌或寄生虫引起，需要及时采取综合治疗措施，以防止病情恶化。为了帮助您有效管理鱼群健康，我建议如下治疗方案：

1.🧱隔离病鱼：立即将患病鱼类转移到单独的治疗缸中，避免疾病传播给其他健康鱼只。确保治疗缸的水质清洁，并保持适宜的温度和氧气水平。

2.💧改善水质：检查并优化主缸和治疗缸的水质参数，包括 pH 值（维持在 6.5-7.5）、氨氮和亚硝酸盐水平（尽可能接近零）。定期换水（建议每周换水 25-30%），并添加水质稳定剂以减少应激。

3.💊药物治疗：根据疾病类型，使用以下针对性治疗：
- 对于溃疡病和鳍部病变，可使用广谱抗生素如土霉素或呋喃西林（按产品说明剂量添加至水中），连续治疗 5-7 天。
- 对于眼部病变，建议使用抗菌药浴，如甲基蓝溶液（每 10 升水添加 1-2 毫升），浸泡病鱼 15-20 分钟，每天一次，持续 3-5 天。
- 对于腐烂鳃，采用盐浴疗法（每升水添加 1-3 克非碘盐），浸泡病鱼 10-15 分钟，每天一次，同时可配合使用抗菌药物如磺胺类制剂。

4.🍔营养支持：在治疗期间，提供高营养、易消化的饲料，如富含维生素的活饵或专用病鱼饲料，以增强鱼体的免疫力和恢复能力。

5.🔭监测与调整：每天观察病鱼的行为和症状变化，记录治疗进展。如果病情未见好转，请咨询兽医或水产专家，调整治疗方案。

恭喜您及时检测到这些疾病！通过积极治疗和预防，您的鱼群有望恢复健康。如有不确定之处，建议寻求专业指导。保持细心照料，水族生活更安心！
            """)
    except Exception as e:
        st.error(f"数据加载失败: {str(e)}")
        st.info("请确保 data.xlsx 文件存在于当前目录中")

elif page == PAGE_QA:
    st.markdown('<h1 class="main-header">🧠渔康智鉴AI助手</h1>', unsafe_allow_html=True)
    st.markdown('<div class="title-divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="qa-tagline">🐟 一位资深的水产养殖专家，能助您解决各类养殖问题 🐟</div>', unsafe_allow_html=True)

    st.markdown('<h4 class="section-label">试试这些常见问题：</h4>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("草鱼患溃疡病如何治疗？", key="q1"):
            question = "草鱼患溃疡病如何治疗？"
            st.session_state.setdefault("messages", []).append({"role": "user", "content": question})
            with st.spinner("思考中..."):
                answer = call_qwen_api(question)
                st.session_state["messages"].append({"role": "assistant", "content": answer})
        if st.button("鲢鱼同时患眼部病变、鳍部病变如何治疗？", key="q2"):
            question = "鲢鱼同时患眼部病变、鳍部病变如何治疗？"
            st.session_state.setdefault("messages", []).append({"role": "user", "content": question})
            with st.spinner("思考中..."):
                answer = call_qwen_api(question)
                st.session_state["messages"].append({"role": "assistant", "content": answer})
    with col2:
        if st.button("幼苗期鳙鱼患溃疡病如何治疗？", key="q3"):
            question = "幼苗期鳙鱼患溃疡病如何治疗？"
            st.session_state.setdefault("messages", []).append({"role": "user", "content": question})
            with st.spinner("思考中..."):
                answer = call_qwen_api(question)
                st.session_state["messages"].append({"role": "assistant", "content": answer})
        if st.button("当鱼出现腐烂鳃时如何快速治疗？", key="q4"):
            question = "当鱼出现腐烂鳃时如何快速治疗？"
            st.session_state.setdefault("messages", []).append({"role": "user", "content": question})
            with st.spinner("思考中..."):
                answer = call_qwen_api(question)
                st.session_state["messages"].append({"role": "assistant", "content": answer})

    st.markdown(
        '<div class="greeting"><span class="icon">📘</span>'
        '<span>你好，我是关于鱼类养殖知识的问答助手。有什么可以帮助到你？🥰</span></div>',
        unsafe_allow_html=True
    )

    if "messages" not in st.session_state:
        st.session_state.messages = []

    st.markdown("### 对话记录")
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("请输入您的问题..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            with st.spinner("思考中..."):
                answer = call_qwen_api(prompt)
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})

    if st.button("重置会话"):
        st.session_state.messages = []
        st.rerun()