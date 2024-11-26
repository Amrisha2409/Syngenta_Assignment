import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Custom CSS for pastel theme
st.markdown(
    """
    <style>
        .main {
            background-color: #f7fce4; /* Light pastel yellow */
        }
        div.stButton > button {
            background-color: #a8d5ba; /* Pastel green */
            color: #ffffff;
            border-radius: 8px;
            border: 1px solid #86c5a6;
        }
        div.stButton > button:hover {
            background-color: #86c5a6; /* Slightly darker green for hover */
        }
        h1 {
            color: #558c8c; /* Soft greenish blue for headers */
        }
        .css-1offfwp a {
            color: #558c8c !important; /* Adjust link colors */
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Title of the Application
st.title("📊 CSV Data Visualizer")

# File Upload
uploaded_file = st.file_uploader("📁 Upload a CSV file", type=["csv"])

if uploaded_file:
    # Read CSV File
    data = pd.read_csv(uploaded_file)
    st.write("### 📝 Data Preview")
    st.dataframe(data)
    
    # Select Columns for Visualization
    columns = data.columns.tolist()
    chart_type = st.selectbox("📈 Select Chart Type", ["Line Chart", "Bar Chart", "Histogram"])
    
    if chart_type in ["Line Chart", "Bar Chart"]:
        x_axis = st.selectbox("🧭 Select X-Axis", columns)
        y_axis = st.multiselect("🧭 Select Y-Axis (Multiple Columns for Bar Chart)", columns)
        if x_axis and y_axis:
            st.write(f"### {chart_type}")
            if chart_type == "Line Chart":
                st.line_chart(data.set_index(x_axis)[y_axis])
            else:
                st.bar_chart(data.set_index(x_axis)[y_axis])
    
    elif chart_type == "Histogram":
        column = st.selectbox("📊 Select Column for Histogram", columns)
        if column:
            st.write("### Histogram")
            fig, ax = plt.subplots()
            ax.hist(data[column].dropna(), bins=20, color='#a8d5ba', edgecolor='black')
            st.pyplot(fig)
