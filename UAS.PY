import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Fungsi untuk menghitung EOQ dan ROP
def calculate_eoq_rop(daily_demand, ordering_cost, holding_cost, lead_time, shelf_life):
    eoq = np.sqrt((2 * daily_demand * ordering_cost) / holding_cost)
    rop = daily_demand * lead_time
    stock_out_time = shelf_life / daily_demand
    order_frequency = (30 / (eoq / daily_demand))
    total_inventory_cost = (holding_cost * (eoq / 2)) + (ordering_cost * order_frequency)
    
    return eoq, rop, stock_out_time, order_frequency, total_inventory_cost

# Fungsi untuk memeriksa keamanan EOQ
def is_eoq_safe(eoq, daily_demand, shelf_life):
    return eoq <= (daily_demand * shelf_life)

# Fungsi untuk membuat grafik stok
def plot_stock_graph(daily_demand, rop, shelf_life):
    days = np.arange(0, 10)
    stock_levels = np.maximum(0, shelf_life * daily_demand - daily_demand * days)
    
    plt.figure(figsize=(10, 5))
    plt.plot(days, stock_levels, marker='o', label='Level Stok')
    plt.axhline(y=rop, color='r', linestyle='--', label='Reorder Point (ROP)')
    plt.title('Grafik Level Stok Selama 10 Hari')
    plt.xlabel('Hari')
    plt.ylabel('Level Stok (unit)')
    plt.fill_between(days, stock_levels, 0, where=(stock_levels < rop), color='red', alpha=0.3)
    plt.fill_between(days, stock_levels, 0, where=(stock_levels >= rop) & (stock_levels < (shelf_life * daily_demand)), color='yellow', alpha=0.3)
    plt.fill_between(days, stock_levels, 0, where=(stock_levels >= (shelf_life * daily_demand)), color='green', alpha=0.3)
    plt.legend()
    plt.grid()
    st.pyplot(plt)

# Desain UI
st.title("📦 Kalkulator EOQ dan ROP untuk Produk Cepat Rusak 🍊🧃")
st.markdown("### Masukkan Data Berikut:")

# Input Form
with st.form(key='input_form'):
    daily_demand = st.number_input("Permintaan Harian (unit per hari)", min_value=1)
    ordering_cost = st.number_input("Biaya Pemesanan (Rp per order)", min_value=1)
    holding_cost = st.number_input("Biaya Penyimpanan (Rp per unit per hari)", min_value=1)
    lead_time = st.number_input("Lead Time (hari)", min_value=1)
    shelf_life = st.number_input("Umur Simpan Maksimum (hari)", min_value=1)
    
    submit_button = st.form_submit_button("Hitung")

# Output
if submit_button:
    eoq, rop, stock_out_time, order_frequency, total_inventory_cost = calculate_eoq_rop(
        daily_demand, ordering_cost, holding_cost, lead_time, shelf_life
    )
    
    st.markdown("### Hasil Perhitungan:")
    st.write(f"**EOQ (Economic Order Quantity):** {eoq:.2f} unit")
    st.write(f"**Reorder Point (ROP):** {rop:.2f} unit")
    st.write(f"**Waktu Habisnya Stok:** {stock_out_time:.2f} hari")
    st.write(f"**Frekuensi Pemesanan per Bulan:** {order_frequency:.2f} kali")
    st.write(f"**Total Biaya Persediaan per Bulan:** Rp {total_inventory_cost:.2f}")
    
    if is_eoq_safe(eoq, daily_demand, shelf_life):
        st.success("EOQ aman terhadap umur simpan.")
    else:
        st.warning("⚠️ Peringatan: EOQ lebih besar dari D × umur simpan!")
    
    # Visualisasi
    plot_stock_graph(daily_demand, rop, shelf_life)

# Footer
st.markdown("---")
st.markdown("Dibuat oleh Mahasiswa Teknik Informatika untuk UMKM")
