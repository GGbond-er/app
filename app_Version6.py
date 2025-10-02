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
        margin: 0.5rem 0 0.25rem 0;
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
    /* 让主容器更贴近页面顶端 */
    .block-container {
        padding-top: 0.75rem;
    }
    /* 问答助手页的小字提示（示意图样式：居中、红色、略加粗） */
    .qa-tagline {
        text-align: center;
        color: #ff4d4f;
        font-size: 0.95rem;
        font-weight: 600;
        margin: 0 0 1rem 0;
    }
    /* 侧边栏品牌区域：与示意图一致，水平居中对齐 */
    .sidebar-brand {
        display: flex;
        align-items: center;
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
    /* 欢迎页标题图片：绝对居中 */
    .home-title {
        display: flex;
        justify-content: center;
        margin: 0.25rem 0 1rem 0;
        width: 100%;
    }
    .home-wenzi {
        width: """ + str(HOME_WENZI_WIDTH) + """px;
        max-width: 85vw;
        height: auto;
        display: block;
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

page = st.sidebar.radio("选择页面", ["欢迎", "数据查询", "问答助手"])

# 调用大模型API的函数
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
if page == "欢迎":
    # 用 wenzi 图片替代“渔康智鉴”文字标题（绝对居中）
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
    
    # 欢迎页图片区（修复弃用参数，使用 use_container_width）
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

elif page == "数据查询":
    st.markdown('<h1 class="main-header">数据查询</h1>', unsafe_allow_html=True)
    
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

elif page == "问答助手":
    st.markdown('<h1 class="main-header">问答助手</h1>', unsafe_allow_html=True)
    # 标题正下方的小字说明（示意图）
    st.markdown('<div class="qa-tagline">🐟 一位资深的水产养殖专家，能助您解决各类养殖问题 🐟</div>', unsafe_allow_html=True)
    
    # 初始化会话状态
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # 预设问题
    st.markdown("### 试试这些常见问题：")
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