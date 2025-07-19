
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objs as go

st.set_page_config(page_title='Prediksi Saham KINO', layout='centered')

st.title("📈 Prediksi Harga Saham PT KINO Indonesia (KINO.JK)")
st.markdown("Aplikasi ini menampilkan hasil prediksi harga saham PT. KINO INDONESIA Tbk menggunakan model GRU.")

data = pd.read_csv('hasil_prediksi.csv')

with st.expander("📊 Lihat Data"):
    st.dataframe(data.tail(10))

data['Date'] = pd.to_datetime(data['Date'])

# Pastikan kolom penting ada
required_columns = ['Date', 'Actual', 'Predicted']
if not all(col in data.columns for col in required_columns):
    st.error("❌ Kolom 'Date', 'Actual', atau 'Predicted' tidak ditemukan di CSV.")
    st.write("Kolom yang ditemukan:", data.columns.tolist())
    st.stop()

# Default: prediksi terakhir
default_date = data['Date'].iloc[-1]

# Pilihan tanggal interaktif
selected_date = st.date_input("📅 Pilih tanggal untuk ditandai:", default_date,
                              min_value=data['Date'].min(),
                              max_value=data['Date'].max())

# Jika tanggal yang dipilih tidak pas, cari yang paling dekat
if selected_date not in data['Date'].values:
    selected_date = data['Date'].iloc[(data['Date'] - pd.to_datetime(selected_date)).abs().argmin()]

# Data untuk marker merah (pada prediksi)
y_marker = data.loc[data['Date'] == selected_date, 'Predicted'].values[0]

# Plot interaktif
fig = go.Figure()

# Garis aktual & prediksi
fig.add_trace(go.Scatter(x=data['Date'], y=data['Actual'], mode='lines', name='Aktual', line=dict(color='blue')))
fig.add_trace(go.Scatter(x=data['Date'], y=data['Predicted'], mode='lines', name='Prediksi', line=dict(color='red')))

# Garis vertikal putus-putus
fig.add_shape(
    type="line",
    x0=selected_date,
    y0=data['Predicted'].min(),
    x1=selected_date,
    y1=data['Predicted'].max(),
    line=dict(color="red", width=2, dash="dash"),
)

# Titik merah di garis prediksi
fig.add_trace(go.Scatter(
    x=[selected_date],
    y=[y_marker],
    mode='markers',
    name='Titik yang Dipilih',
    marker=dict(color='red', size=10)
))

# Layout: tampilkan bulan saja di sumbu X
fig.update_layout(
    title="Visualisasi Prediksi Harga Saham",
    xaxis_title="Tanggal",
    yaxis_title="Harga Saham",
    showlegend=True,
    xaxis=dict(
        tickformat='%b %Y',
        tickangle=-45,
        dtick="M1"  # 1 bulan
    )
)

# Tampilkan chart
st.plotly_chart(fig, use_container_width=True)
st.caption("🧠 Model yang digunakan: Gated Recurrent Unit (GRU) | Dataset: KINO.JK")

# Kesimpulan sederhana
if data['Predicted'].iloc[-1] > data['Actual'].iloc[-2]:
    st.success("Harga diprediksi **naik** dalam waktu dekat 📈")
else:
    st.error("Harga diprediksi **turun** dalam waktu dekat 📉")



# Tombol download
csv = data.to_csv(index=False).encode('utf-8')
st.download_button("📥 Download Hasil Prediksi (CSV)", data=csv, file_name="hasil_prediksi.csv", mime="text/csv")

