import streamlit as st
import pandas as pd
import joblib

st.set_page_config(page_title="腐蚀速率预测界面", layout="wide")

# 页面标题
st.markdown("<h1 style='text-align: center; color: black;'>腐蚀速率预测</h1>", unsafe_allow_html=True)
st.markdown("<div style='background-color: blue; height: 5px;'></div>", unsafe_allow_html=True)
st.markdown("---")  # 添加分隔线

# 输入参数部分
st.subheader("输入参数")
model_file = st.file_uploader("上传模型文件 (pkl)", type=["pkl"])

# 使用标签选择输入方式
input_method = st.radio("选择输入方式", ["单点预测", "批量输入"])

input_data = {}
parameters = [
    '环境电阻率（Ω·m）', '环境Ph', '工作面面积（cm2）', '时长（d）',
    '通电电位最大值（VCSE）', '通电电位最小值（VCSE）', '通电电位平均值（VCSE）',
    '断电电位最大值（VCSE）', '断电电位最小值（VCSE）', '断电电位平均值（VCSE）',
    '断电电位正于阴极保护准则比例', '断电电位正于阴极保护准则+50mV比例',
    '断电电位正于阴极保护准则+100mV比例', '断电电位正于阴极保护准则+850mV比例',
    '交流电压最大值（V）', '交流电压最小值（V）', '交流电压平均值（V）',
    '交流电流密度最大值（A/m2）', '交流电流密度最小值（A/m2）', '交流电流密度平均值（A/m2）',
    '直流电流密度平均值（A/m2）'
]

# 设置默认值
default_values = {
    '环境电阻率（Ω·m）': 50.0,
    '环境Ph': 7.5,
    '工作面面积（cm2）': 1.0,
    '时长（d）': 180.0,
    '通电电位最大值（VCSE）': -1.2,
    '通电电位最小值（VCSE）': -1.2,
    '通电电位平均值（VCSE）': -1.2,
    '断电电位最大值（VCSE）': -1.0,
    '断电电位最小值（VCSE）': -1.0,
    '断电电位平均值（VCSE）': -1.0,
    '断电电位正于阴极保护准则比例': 0.1,
    '断电电位正于阴极保护准则+50mV比例': 0.0,
    '断电电位正于阴极保护准则+100mV比例': 0.0,
    '断电电位正于阴极保护准则+850mV比例': 0.0,
    '交流电压最大值（V）': 4.0,
    '交流电压最小值（V）': 0.0,
    '交流电压平均值（V）': 1.0,
    '交流电流密度最大值（A/m2）': 30.0,
    '交流电流密度最小值（A/m2）': 0.0,
    '交流电流密度平均值（A/m2）': 10.0,
    '直流电流密度平均值（A/m2）': 0.1
}

if input_method == "单点预测":
    cols = st.columns(7, gap="large")  # 增大行与行、列与列之间的间距
    for i, param in enumerate(parameters):
        with cols[i % 7]:  # 将输入框放置在对应的列中
            if param in [
                '断电电位正于阴极保护准则比例',
                '断电电位正于阴极保护准则+50mV比例',
                '断电电位正于阴极保护准则+100mV比例',
                '断电电位正于阴极保护准则+850mV比例'
            ]:
                input_data[param] = st.number_input(param, format="%.4f", value=default_values[param],
                                                      min_value=0.0, max_value=1.0, step=0.01)
            else:
                input_data[param] = st.number_input(param, format="%.4f", value=default_values[param])

    # 注意事项和预测按钮在同一行

    st.markdown("<p style='color: red;'>注意：开始预测前请确保输入数据的单位与标注单位一致，否则可能导致预测结果出现较大偏差。</p>", unsafe_allow_html=True)


    if st.button("开始预测"):
            if model_file is not None:
                model = joblib.load(model_file)  # 确保模型在此加载
                input_df = pd.DataFrame([input_data])  # 确保是二维数据框
                prediction = model.predict(input_df)
                st.subheader("预测结果")

                # 显示预测结果
                st.markdown(f"<h2 style='text-align: left;'>腐蚀速率预测值: {prediction[0]:.4f}</h2>",
                            unsafe_allow_html=True)

                # 创建结果 DataFrame，并确保有表头
                result_df = pd.DataFrame(input_data, index=[0])  # 转换为 DataFrame
                result_df["预测值"] = prediction[0]  # 将预测值添加到 DataFrame 中

                # 显示预测结果
                st.dataframe(
                    result_df.style.set_table_attributes("style='width:100%; background-color: lightgrey;'"))  # 表格铺满屏幕

            else:
                st.error("请先上传模型文件。")

elif input_method == "批量输入":
    uploaded_file = st.file_uploader("上传包含输入参数的Excel文件", type=["xlsx"])
    if uploaded_file is not None:
        input_df = pd.read_excel(uploaded_file)  # 读取Excel文件
        if model_file is not None:
            model = joblib.load(model_file)  # 加载模型
            predictions = model.predict(input_df)  # 进行批量预测

            # 创建结果 DataFrame，并将预测值添加到原始输入数据中
            input_df["预测值"] = predictions

            # 显示预测结果
            st.subheader("批量预测结果")
            st.dataframe(
                input_df.style.set_table_attributes("style='width:100%; background-color: lightgrey;'"))  # 表格铺满屏幕
        else:
            st.error("请先上传模型文件。")

# 结束
st.markdown("---")  # 添加分隔线
