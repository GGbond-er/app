import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import requests
import json
import os

# 检查是否在 Streamlit Cloud 上运行
ON_STREAMLIT_CLOUD = os.getenv('IS_STREAMLIT_CLOUD') is not None

# 设置中文字体支持 - 仅当不在 Streamlit Cloud 上运行时才设置
if not ON_STREAMLIT_CLOUD:
    try:
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
        plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    except:
        pass  # 如果字体设置失败，继续执行

# 设置页面配置
st.set_page_config(
    page_title="鱼疾智鉴",
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

# 侧边栏导航
st.sidebar.title("导航")
page = st.sidebar.radio("选择页面", ["欢迎", "数据查询", "问答助手"])

# 主内容区域
if page == "欢迎":
    # 标题
    st.markdown('<h1 class="main-header">鱼疾智鉴</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">基于深度学习和生成式人工智能的多维度鱼类养殖助手</p>', unsafe_allow_html=True)
    
    # 显示图片
    try:
        st.image("5fee78b75940ba154c648cdd715ec0d0.jpg", use_column_width=True)
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
            fig, ax = plt.subplots(figsize=(10, 6))
            bars = ax.bar(categories, values, color=['green', 'red', 'orange', 'blue', 'purple'])
            ax.set_ylabel('数量')
            ax.set_title('鱼类健康状况分布')
            plt.xticks(rotation=45)
            
            # 在柱子上添加数值标签
            for bar, value in zip(bars, values):
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2, height + 0.5,
                        f'{int(value)}', ha='center', va='bottom', fontsize=10)
            
            # 调整布局以确保标签可见
            plt.tight_layout()
            st.pyplot(fig)
        
        with col2:
            st.subheader("鱼类健康状况分布（饼图）")
            fig, ax = plt.subplots(figsize=(8, 8))
            wedges, texts, autotexts = ax.pie(values, labels=categories, autopct='%1.1f%%', startangle=90)
            
            # 设置饼图标签样式
            for text in texts:
                text.set_fontsize(10)
            for autotext in autotexts:
                autotext.set_fontsize(10)
                autotext.set_color('white')
                autotext.set_weight('bold')
            
            ax.axis('equal')  # 保持圆形
            plt.tight_layout()
            st.pyplot(fig)
            
    except Exception as e:
        st.error(f"数据加载失败: {str(e)}")
        st.info("请确保data.xlsx文件存在于当前目录中")

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
            st.session_state.messages.append({"role": "user", "content": "草鱼患溃疡病如何治疗？"})
            # 自动回答
            st.session_state.messages.append({"role": "assistant", "content": "草鱼溃疡病治疗建议：1. 隔离病鱼；2. 使用5%盐水浸泡10-15分钟；3. 水体内添加适量抗生素；4. 改善水质，增加氧气供应。"})
            
        if st.button("鲢鱼同时患眼部病变、鳍部病变如何治疗？", key="q2"):
            st.session_state.messages.append({"role": "user", "content": "鲢鱼同时患眼部病变、鳍部病变如何治疗？"})
            # 自动回答
            st.session_state.messages.append({"role": "assistant", "content": "鲢鱼眼部和鳍部病变综合治疗：1. 使用0.3-0.5mg/L的二氧化氯全池泼洒；2. 饲料中添加维生素C和抗生素；3. 提高水温至适宜范围；4. 定期换水保持水质清洁。"})
    
    with col2:
        if st.button("幼苗期鳙鱼患溃疡病如何治疗？", key="q3"):
            st.session_state.messages.append({"role": "user", "content": "幼苗期鳙鱼患溃疡病如何治疗？"})
            # 自动回答
            st.session_state.messages.append({"role": "assistant", "content": "幼苗期鳙鱼溃疡病需谨慎处理：1. 使用低浓度(3%)盐水短时间浸泡；2. 水体内添加专用鱼药，按说明减半使用；3. 增加水体溶氧量；4. 少量多次投喂高品质饲料。"})
            
        if st.button("当鱼出现腐烂鳃时如何快速治疗？", key="q4"):
            st.session_state.messages.append({"role": "user", "content": "当鱼出现腐烂鳃时如何快速治疗？"})
            # 自动回答
            st.session_state.messages.append({"role": "assistant", "content": "腐烂鳃急效处理：1. 立即隔离病鱼；2. 使用0.5%盐水和适量高锰酸钾溶液浸泡15分钟；3. 全池泼洒杀菌剂；4. 加强过滤系统，增加水体循环。"})
    
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
        
        # 调用通义千问API
        with st.chat_message("assistant"):
            with st.spinner("思考中..."):
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
                        assistant_reply = result["output"]["choices"][0]["message"]["content"]
                        st.markdown(assistant_reply)
                        st.session_state.messages.append({"role": "assistant", "content": assistant_reply})
                    else:
                        st.error("获取回答时出错，请检查API密钥或网络连接")
                        # 提供默认回答
                        default_reply = "根据您的问题，建议采取以下措施：1. 隔离患病鱼类；2. 改善水质条件；3. 使用适当的鱼类药物治疗；4. 咨询专业鱼类疾病专家获取具体治疗方案。"
                        st.markdown(default_reply)
                        st.session_state.messages.append({"role": "assistant", "content": default_reply})
                        
                except Exception as e:
                    st.error(f"调用API时出错: {str(e)}")
                    # 模拟回复
                    sample_replies = {
                        "草鱼患溃疡病如何治疗？": "草鱼溃疡病治疗建议：1. 隔离病鱼；2. 使用5%盐水浸泡10-15分钟；3. 水体内添加适量抗生素；4. 改善水质，增加氧气供应。",
                        "鲢鱼同时患眼部病变、鳍部病变如何治疗？": "鲢鱼眼部和鳍部病变综合治疗：1. 使用0.3-0.5mg/L的二氧化氯全池泼洒；2. 饲料中添加维生素C和抗生素；3. 提高水温至适宜范围；4. 定期换水保持水质清洁。",
                        "幼苗期鳙鱼患溃疡病如何治疗？": "幼苗期鳙鱼溃疡病需谨慎处理：1. 使用低浓度(3%)盐水短时间浸泡；2. 水体内添加专用鱼药，按说明减半使用；3. 增加水体溶氧量；4. 少量多次投喂高品质饲料。",
                        "当鱼出现腐烂鳃时如何快速治疗？": "腐烂鳃急效处理：1. 立即隔离病鱼；2. 使用0.5%盐水和适量高锰酸钾溶液浸泡15分钟；3. 全池泼洒杀菌剂；4. 加强过滤系统，增加水体循环。"
                    }
                    
                    if prompt in sample_replies:
                        reply = sample_replies[prompt]
                    else:
                        reply = "根据您的问题，建议采取以下措施：1. 隔离患病鱼类；2. 改善水质条件；3. 使用适当的鱼类药物治疗；4. 咨询专业鱼类疾病专家获取具体治疗方案。"
                    
                    st.markdown(reply)
                    st.session_state.messages.append({"role": "assistant", "content": reply})
    
    # 重置会话按钮 - 使用正确的Streamlit方法
    if st.button("重置会话"):
        st.session_state.messages = []
        st.rerun()  # 使用 st.rerun() 而不是 st.experimental_rerun()