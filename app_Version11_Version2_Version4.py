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

# 自定义CSS样式（再次增大页面主标题的上边距与行高，避免遮挡；新增美化样式）
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        /* 再次下移，确保不被顶部控件遮挡 */
        margin: 4rem 0 1rem 0;
        line-height: 1.3;
        scroll-margin-top: 5rem; /* 锚点跳转时也避免被顶栏遮挡 */
    }
    .sub-header {
        font-size: 1.2rem;
        color: #2ca02c;
        text-align: center;
        margin-bottom: 1.25rem;
    }
    .feature-list {
        font-size: 1.1rem;
        line-height: 2;
        margin-left: 1.5rem;
    }
    .divider {
        margin: 0.75rem 0 1.25rem 0;
        border-top: 1px solid #e6e6e6;
    }
    .preset-question {
        margin: 0.5rem 0;
        padding: 0.5rem;
        border: 1px solid #ddd;
        border-radius: 0.5rem;
        cursor: pointer;
    }
    .preset-question:hover {
        background-color: #f5f5f5;
    }
    /* 主内容整体上边距，给所有页面增加安全空间 */
    .block-container {
        padding-top: 1.75rem;
    }
    /* 问答助手页的小字提示 */
    .qa-tagline {
        text-align: center;
        color: #ff4d4f;
        font-size: 0.95rem;
        font-weight: 600;
        margin: -0.1rem 0 0.75rem 0;
    }
    /* 侧边栏品牌区域：水平居中对齐 */
    .sidebar-brand {
        display: flex;
        align-items: center; /* 垂直居中，确保同一水平面 */
        gap: 8px;
        padding: 10px 6px 2px 6px;
    }
    .sidebar-logo {
        width: """ + str(SIDEBAR_TU_AN_WIDTH) + """px;
        height: auto;
        display: block;
    }
    .sidebar-wenzi {
        width: """ + str(SIDEBAR_WENZI_WIDTH) + """px;
        height: auto;
        display: block;
    }
    .sidebar-brand-spacer {
        height: 0.25rem;
    }
    /* 欢迎页标题图片容器：继续下移一些 */
    .home-title {
        display: flex;
        justify-content: center;
        margin: 2rem 0 1rem 0;
        width: 100%;
        scroll-margin-top: 5rem;
    }
    .home-wenzi {
        width: """ + str(HOME_WENZI_WIDTH) + """px;
        max-width: 85vw;
        height: auto;
        display: block;
    }
    /* —— 问答助手美化 —— */
    .title-divider {
        height: 3px;
        background: linear-gradient(90deg, #1e90ff, #2c7be5);
        border-radius: 2px;
        width: 82%;
        margin: 0.15rem auto 0.9rem auto; /* 紧跟标题并稍作下移 */
    }
    .section-label {
        font-size: 1rem;           /* 调小字号 */
        font-weight: 700;
        color: #334155;            /* 石板灰 */
        margin: 0.25rem 0 0.5rem 0;
        text-align: left;
    }
    .greeting {
        display: inline-flex;
        align-items: center;
        gap: 10px;
        background: #f0f7ff;
        border: 1px solid #d6e6ff;
        color: #0f3e8a;
        padding: 10px 12px;
        border-radius: 12px;
        margin: 0.25rem 0 1.1rem 0;
    }
    .greeting .icon {
        background: #ffd782;
        color: #915c00;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 28px;
        height: 28px;
        border-radius: 6px;
        font-size: 16px;
    }
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
        # 回退方案：若未找到图片，仍给出提示
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

# “🧠 问答助手”页面的侧边栏：操作说明
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
        # 通义千问API调用
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
            "parameters": {
                "result_format": "message"
            }
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
    # 用 wenzi 图片替代“渔康智鉴”文字标题（绝对居中，已下移）
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
    
    # 欢迎页图片区
    try:
        st.image("20250919185006_1543_32.jpg", use_container_width=True)
    except:
        st.info("图片加载失败，请确保图片文件存在")
    
    # 功能简介
    st.markdown("### 功能介绍")
    features = [
        "鱼类疾病智能识别与诊断",
        "养殖数据可视化分析",
        "个性化治疗建议与预防措施",
        "鱼类健康知识问答"
    ]
    for feature in features:
        st.markdown(f"- **{feature}**")
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    # 技术说明
    st.markdown("### 技术架构")
    st.markdown("""
    本系统采用先进的深度学习技术和生成式人工智能模型，结合专业鱼类疾病知识库，
    为鱼类养殖提供全方位的智能支持。
    """)

elif page == PAGE_CAPTURE:
    # 新增页面：📸开始识别 —— 页面内部只有一句话
    st.write("模型正在加载中......")

elif page == PAGE_DATA:
    # 页面主标题：带表情，并使用更大的上边距样式（避免遮挡）
    st.markdown('<h1 class="main-header">🔍 数据查询</h1>', unsafe_allow_html=True)
    
    # 读取数据
    try:
        df = pd.read_excel("data.xlsx")
        st.success("数据加载成功！")
        
        # 显示原始数据
        st.subheader("原始数据")
        st.dataframe(df, use_container_width=True)
        
        # 提取数据用于图表
        categories = df.columns[1:]
        values = df.iloc[0, 1:].values
        
        # 创建图表
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("鱼类健康状况分布（柱状图）")
            chart_data = pd.DataFrame({
                '类别': categories,
                '数量': values
            })
            st.bar_chart(chart_data.set_index('类别'), use_container_width=True)
            
            # 数值标签
            for category, value in zip(categories, values):
                st.write(f"{category}: {value}")
        
        with col2:
            st.subheader("鱼类健康状况分布（饼图）")
            try:
                import plotly.express as px
                fig = px.pie(
                    values=values, 
                    names=categories,
                    title='鱼类健康状况分布'
                )
                st.plotly_chart(fig, use_container_width=True)
            except ImportError:
                st.info("饼图需要 plotly 库支持。请在 requirements.txt 中添加 'plotly>=5.15.0'")
                
    except Exception as e:
        st.error(f"数据加载失败: {str(e)}")
        st.info("请确保 data.xlsx 文件存在于当前目录中")

elif page == PAGE_QA:
    # 页面主标题：改为“🧠渔康智鉴AI助手”，并使用更大的上边距样式（避免遮挡）
    st.markdown('<h1 class="main-header">🧠渔康智鉴AI助手</h1>', unsafe_allow_html=True)
    # 蓝色分界线
    st.markdown('<div class="title-divider"></div>', unsafe_allow_html=True)
    # 标题正下方的小字说明（延续之前需求）
    st.markdown('<div class="qa-tagline">🐟 一位资深的水产养殖专家，能助您解决各类养殖问题 🐟</div>', unsafe_allow_html=True)

    # 调整：将示例问题标题调小
    st.markdown('<h4 class="section-label">试试这些常见问题：</h4>', unsafe_allow_html=True)

    # 预设问题
    col1, col2 = st.columns(2)
    with col1:
        if st.button("草鱼患溃疡病如何治疗？", key="q1"):
            question = "草鱼患溃疡病如何治疗？"
            st.session_state.messages.append({"role": "user", "content": question})
            with st.spinner("思考中..."):
                answer = call_qwen_api(question)
                st.session_state.messages.append({"role": "assistant", "content": answer})
        if st.button("鲢鱼同时患眼部病变、鳍部病变如何治疗？", key="q2"):
            question = "鲢鱼同时患眼部病变、鳍部病变如何治疗？"
            st.session_state.messages.append({"role": "user", "content": question})
            with st.spinner("思考中..."):
                answer = call_qwen_api(question)
                st.session_state.messages.append({"role": "assistant", "content": answer})
    with col2:
        if st.button("幼苗期鳙鱼患溃疡病如何治疗？", key="q3"):
            question = "幼苗期鳙鱼患溃疡病如何治疗？"
            st.session_state.messages.append({"role": "user", "content": question})
            with st.spinner("思考中..."):
                answer = call_qwen_api(question)
                st.session_state.messages.append({"role": "assistant", "content": answer})
        if st.button("当鱼出现腐烂鳃时如何快速治疗？", key="q4"):
            question = "当鱼出现腐烂鳃时如何快速治疗？"
            st.session_state.messages.append({"role": "user", "content": question})
            with st.spinner("思考中..."):
                answer = call_qwen_api(question)
                st.session_state.messages.append({"role": "assistant", "content": answer})

    # 问候语（示例页面风格）
    st.markdown(
        '<div class="greeting"><span class="icon">📘</span>'
        '<span>你好，我是关于鱼类养殖知识的问答助手。有什么可以帮助到你？🥰</span></div>',
        unsafe_allow_html=True
    )

    # 初始化会话状态
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # 对话记录
    st.markdown("### 对话记录")
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # 用户输入
    if prompt := st.chat_input("请输入您的问题..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        # 调用大模型API
        with st.chat_message("assistant"):
            with st.spinner("思考中..."):
                answer = call_qwen_api(prompt)
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
    
    # 重置会话按钮
    if st.button("重置会话"):
        st.session_state.messages = []
        st.rerun()