import streamlit as st # pyright: ignore[reportMissingImports]
import pandas as pd

st.set_page_config(page_title="Production Dashboard", layout="wide")

st.title("Production Planning Dashboard")

uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    # remove hidden spaces
    df.columns = df.columns.str.strip()

    st.write("Column names in your file:")
    st.write(df.columns)

    st.dataframe(df)

    # ---- Auto detect Ordered column ----
    ordered_column = None
    for col in df.columns:
        if "ordered" in col.lower():
            ordered_column = col
            break

    if uploaded_file:
        df: pd.DataFrame = pd.read_excel(uploaded_file)
        df.columns = df.columns.str.strip()

        total_ordered = df["Forecast/MTS"].sum()
        st.metric("Total Ordered", f"{total_ordered:,.0f}") 
         # Group by month
    
        monthly = df.groupby("Month")["Forecast/MTS"].sum()

        st.subheader("Monthly Order Trend")
        st.line_chart(monthly)
         # --- CHANGE column names if needed ---

        ordered_col = "Forecast/MTS"
        finished_col = "Finished"
        backlog_col = "Backlog"

        total_ordered = df[ordered_col].sum()
        total_finished = df[finished_col].sum()
        total_backlog = df[backlog_col].sum()

        fill_rate = (total_finished / total_ordered) * 100
        late_percent = (total_backlog / total_ordered) * 100
 
        col1, col2, col3 = st.columns(3)

        col1.metric("Total Ordered", f"{total_ordered:,.0f}")
        col2.metric("Fill Rate %", f"{fill_rate:.2f}%")
        col3.metric("Late %", f"{late_percent:.2f}%")
   
    # 🔹 Change if your column names are different
    product_col = "Product"
    month_col = "Month"
    foracast_col = "Forecast/MTS"
    ordered_col = "Ordered"
    finished_col = "Finished"

    # Group by Product + Month
    summary = (
        df.groupby([product_col, month_col])[[ordered_col, foracast_col, finished_col]]
        .sum()
        .reset_index()
    )

    # 🔥 Calculate Open Demand
    summary["Open Demand"] = ((summary[ordered_col])+(summary[foracast_col]))-summary[finished_col]

    # Show table
    st.subheader("Open Demand per Product per Month")
    st.dataframe(summary)

    # 🔥 Pivot for graph
    pivot = summary.pivot(index=month_col, columns=product_col, values="Open Demand")

    st.subheader("Open Demand Trend by Product")
    st.line_chart(pivot)
 