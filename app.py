import streamlit as st
import pandas as pd
import os

# Load or initialize inventory
file_path = "stationery_inventory.csv"
if os.path.exists(file_path):
    inventory = pd.read_csv(file_path)
else:
    inventory = pd.DataFrame(columns=["ItemID", "ItemName", "Quantity", "BuyingPrice", "SellingPrice"])

# View Inventory
st.title("📦 Stationery Shop Inventory Management")

st.subheader("📋 Current Inventory")
st.dataframe(inventory)

# Add New Item
st.subheader("➕ Add New Item")
with st.form("add_item_form"):
    new_id = st.text_input("Item ID")
    new_name = st.text_input("Item Name")
    new_qty = st.number_input("Quantity", min_value=0, step=1)
    buy_price = st.number_input("Buying Price", min_value=0.0, step=0.1)
    sell_price = st.number_input("Selling Price", min_value=0.0, step=0.1)
    add_btn = st.form_submit_button("Add Item")

if add_btn:
    if new_id in inventory["ItemID"].values:
        st.warning("Item ID already exists!")
    else:
        new_row = pd.DataFrame([{
            "ItemID": new_id,
            "ItemName": new_name,
            "Quantity": new_qty,
            "BuyingPrice": buy_price,
            "SellingPrice": sell_price
        }])
        inventory = pd.concat([inventory, new_row], ignore_index=True)
        st.success("Item added successfully!")

# Update Stock
st.subheader("🔄 Update Stock")
with st.form("update_stock_form"):
    update_id = st.text_input("Enter Item ID to update")
    add_qty = st.number_input("Add Quantity", min_value=0, step=1)
    update_btn = st.form_submit_button("Update Stock")

if update_btn:
    if update_id in inventory["ItemID"].values:
        inventory.loc[inventory["ItemID"] == update_id, "Quantity"] += add_qty
        st.success("Stock updated.")
    else:
        st.error("Item ID not found!")

# Sell Item
st.subheader("🛒 Sell Item")
with st.form("sell_item_form"):
    sell_id = st.text_input("Enter Item ID to sell")
    sell_qty = st.number_input("Sell Quantity", min_value=0, step=1)
    sell_btn = st.form_submit_button("Sell")

if sell_btn:
    if sell_id in inventory["ItemID"].values:
        current_qty = inventory.loc[inventory["ItemID"] == sell_id, "Quantity"].values[0]
        if current_qty >= sell_qty:
            inventory.loc[inventory["ItemID"] == sell_id, "Quantity"] -= sell_qty
            total_price = inventory.loc[inventory["ItemID"] == sell_id, "SellingPrice"].values[0] * sell_qty
            st.success(f"Sold {sell_qty} units. Total price: Rs. {total_price}")
        else:
            st.warning("Not enough stock!")
    else:
        st.error("Item ID not found!")

# Save Inventory
if st.button("💾 Save Inventory"):
    inventory.to_csv(file_path, index=False)
    st.success("Inventory saved to CSV!")

