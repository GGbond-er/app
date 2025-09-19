import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import requests
import json
import os

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
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #2ca02c;
        text-align: center;
        margin-bottom: 2rem;
    }
    .feature-list {
        font-size: 1.2rem;
        line-height: 2;
        margin-left: 1.5rem;
    }
    .divider {
        margin: 2rem 0;
        border-top: 1px solid #ddd;
    }
    .tagline {
        font-size: 1.5rem;
        text-align: center;
        font-weight: bold;
        margin: 2rem 0;
        color: #333;
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
</style>
""", unsafe_allow_html=True)

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

# 侧边栏导航
st.sidebar.title("导航")
page = st.sidebar.radio("选择页面", ["欢迎", "数据查询", "问答助手"])

# 主内容区域
if page == "欢迎":
    # 标题
    st.markdown('<h1 class="main-header">渔康智鉴</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">基于深度学习和生成式人工智能的多维度鱼类养殖助手</p>', unsafe_allow_html=True)
    
    # 显示图片 - 已替换为您提供的图片
    try:
        st.image("20250919185006_1543_32.jpg", use_column_width=True)
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
    
    # 分隔线
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
        st.dataframe(df)
        
        # 提取数据用于图表
        categories = df.columns[1:]
        values = df.iloc[0, 1:].values
        
        # 创建图表
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("鱼类健康状况分布（柱状图）")
            # 使用 Streamlit 内置图表
            chart_data = pd.DataFrame({
                '类别': categories,
                '数量': values
            })
            st.bar_chart(chart_data.set_index('类别'))
            
            # 添加数值标签
            for i, (category, value) in enumerate(zip(categories, values)):
                st.write(f"{category}: {value}")
        
        with col2:
            st.subheader("鱼类健康状况分布（饼图）")
            # 使用 Streamlit 的 plotly 图表
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
    
    # 初始化会话状态
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # 显示预设问题按钮
    st.markdown("### 试试这些常见问题：")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("草鱼患溃疡病如何治疗？", key="q1"):
            question = "草鱼患溃疡病如何治疗？"
            st.session_state.messages.append({"role": "user", "content": question})
            # 调用大模型API获取答案
            with st.spinner("思考中..."):
                answer = call_qwen_api(question)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            
        if st.button("鲢鱼同时患眼部病变、鳍部病变如何治疗？", key="q2"):
            question = "鲢鱼同时患眼部病变、鳍部病变如何治疗？"
            st.session_state.messages.append({"role": "user", "content": question})
            # 调用大模型API获取答案
            with st.spinner("思考中..."):
                answer = call_qwen_api(question)
                st.session_state.messages.append({"role": "assistant", "content": answer})
    
    with col2:
        if st.button("幼苗期鳙鱼患溃疡病如何治疗？", key="q3"):
            question = "幼苗期鳙鱼患溃疡病如何治疗？"
            st.session_state.messages.append({"role": "user", "content": question})
            # 调用大模型API获取答案
            with st.spinner("思考中..."):
                answer = call_qwen_api(question)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            
        if st.button("当鱼出现腐烂鳃时如何快速治疗？", key="q4"):
            question = "当鱼出现腐烂鳃时如何快速治疗？"
            st.session_state.messages.append({"role": "user", "content": question})
            # 调用大模型API获取答案
            with st.spinner("思考中..."):
                answer = call_qwen_api(question)
                st.session_state.messages.append({"role": "assistant", "content": answer})
    
    # 显示聊天记录
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