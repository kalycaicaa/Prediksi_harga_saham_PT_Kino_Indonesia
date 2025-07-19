
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title='Prediksi Saham KINO', layout='centered')

st.title("📈 Prediksi Harga Saham PT KINO Indonesia (KINO.JK)")
st.markdown("Aplikasi ini menampilkan hasil prediksi harga saham KINO menggunakan model GRU.")

data = pd.read_csv('hasil_prediksi.csv')

with st.expander("📊 Lihat Data"):
    st.dataframe(data.tail(10))

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(data['Date'], data['Actual'], label='Aktual', color='blue')
ax.plot(data['Date'], data['Predicted'], label='Prediksi', color='red')
ax.set_title('Prediksi vs Aktual Harga Saham')
ax.set_xlabel('Tanggal')
ax.set_ylabel('Harga Saham')
ax.legend()
st.pyplot(fig)

# Kesimpulan sederhana
if data['Predicted'].iloc[-1] > data['Actual'].iloc[-1]:
    st.success("Harga diprediksi **naik** dalam waktu dekat 📈")
else:
    st.error("Harga diprediksi **turun** dalam waktu dekat 📉")

# Tombol download
csv = data.to_csv(index=False).encode('utf-8')
st.download_button("📥 Download Hasil Prediksi (CSV)", data=csv, file_name="hasil_prediksi.csv", mime="text/csv")
