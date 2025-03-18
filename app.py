import streamlit as st
import pandas as pd
import plotly.express as px

# Page Setup
st.set_page_config(page_title="Warehouse Management System (WMS)", layout="wide")

st.title("📦 Warehouse Management System (WMS) Dashboard")

# File uploader
uploaded_file = st.file_uploader("📂 Upload Inventory File (Excel)", type=["xlsx"])

if uploaded_file:
    df_inventory = pd.read_excel(uploaded_file)
    
    st.write("### 🗂️ Inventory Data Preview")
    st.dataframe(df_inventory)

    # ---- 🏆 KEY METRICS ----
    total_stock = df_inventory["Opening Stock"].sum()
    buffer_stock = df_inventory["Buffer Stock"].sum()
    low_stock_items = df_inventory[df_inventory["Opening Stock"] < df_inventory["Buffer Stock"]].shape[0]
    out_of_stock = df_inventory[df_inventory["Opening Stock"] == 0].shape[0]
    overstocked_items = df_inventory[df_inventory["Opening Stock"] > (df_inventory["Buffer Stock"] * 2)].shape[0]
    fast_moving_skus = df_inventory[df_inventory["Opening Stock"] < (df_inventory["Buffer Stock"] * 1.5)].shape[0]  # Fast-moving if close to buffer

    # Show Metrics in Boxes
    col1, col2, col3 = st.columns(3)
    col1.metric("📦 Total Stock", f"{total_stock:,}", help="Total quantity of items in inventory.")
    col2.metric("🔄 Buffer Stock", f"{buffer_stock:,}", help="Reserved stock to avoid shortages.")
    col3.metric("⚠️ Low Stock Items", f"{low_stock_items}", help="Items below safety stock levels.")

    col4, col5, col6 = st.columns(3)
    col4.metric("❌ Out of Stock", f"{out_of_stock}", help="Items that are currently unavailable.")
    col5.metric("📊 Overstocked Items", f"{overstocked_items}", help="Items with excessive stock.")
    col6.metric("🚀 Fast Moving SKUs", f"{fast_moving_skus}", help="Items selling quickly and need monitoring.")

    # ---- 🔍 STOCK HEALTH ANALYSIS ----
    st.write("## ✅ Inventory Health Check")

    if out_of_stock > 0:
        st.warning(f"⚠️ {out_of_stock} products are **out of stock**! Consider restocking.")
    else:
        st.success("🎉 No out-of-stock items! Your inventory is well-stocked.")

    if low_stock_items > 0:
        st.warning(f"⚠️ {low_stock_items} products are running **low on stock**! Plan your purchases.")
    
    if overstocked_items > 0:
        st.info(f"ℹ️ {overstocked_items} products have **too much stock**. Consider discounting or redistributing.")
    
    if fast_moving_skus > 0:
        st.info(f"🚀 {fast_moving_skus} SKUs are selling fast! Ensure continuous supply.")

    # ---- 📊 STOCK DISTRIBUTION VISUALIZATION ----
    st.write("## 📊 Stock Distribution by Product")
    fig_stock = px.bar(df_inventory, x="Product Name", y="Opening Stock", color="Opening Stock",
                        title="Stock Levels of Different Products", height=400)
    st.plotly_chart(fig_stock, use_container_width=True)

    # ---- ⚠️ LOW STOCK ALERTS ----
    st.write("## ⚠️ Low Stock Alerts")
    low_stock_df = df_inventory[df_inventory["Opening Stock"] < df_inventory["Buffer Stock"]]
    if not low_stock_df.empty:
        st.dataframe(low_stock_df)
    else:
        st.success("✅ No low-stock items! Inventory is in good shape.")

    # ---- 🏢 STOCK ACROSS WAREHOUSES ----
    warehouse_columns = ["BLR7", "BLR8", "BOM5", "BOM7", "CCU1", "CCX1", "DEL4", "DEL5", "DEX3", "PNQ2", "PNQ3", "SDED", "SDEE", "XHJ9"]
    warehouse_stock = df_inventory[warehouse_columns].sum().reset_index()
    warehouse_stock.columns = ["Warehouse", "Total Stock"]

    st.write("## 🏢 Warehouse Stock Levels")
    fig_warehouse = px.bar(warehouse_stock, x="Warehouse", y="Total Stock", color="Total Stock",
                            title="Warehouse-wise Stock Distribution", height=400)
    st.plotly_chart(fig_warehouse, use_container_width=True)
