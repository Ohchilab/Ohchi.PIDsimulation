import streamlit as st
from control.matlab import *
import matplotlib.pyplot as plt
import numpy as np

st.title("PID制御シミュレーション")

# Kp = 2
# Ki = 0
# Kd = 0

Kp = st.number_input('Kp',min_value=0.00,value=1.00)
Ki = st.number_input('Ki',min_value=0.00)
Kd = st.number_input('Kd',min_value=0.00)

with st.expander('制御対象の伝達関数'):
        st.latex("\\frac{k}{ms^2+cs+1}")
        Pa = st.number_input('m')
        Pb = st.number_input('c',value=1.00)
        Pc = st.number_input('k',value=1.00)
        

P =tf(Pc,[Pa, Pb, 1])

C =tf([Kd, Kp, Ki],[1, 0])

Gyr = feedback(P*C, 1)

with st.expander("制御対象のステップ応答"):
	st.text(f"m={Pa},c={Pb},k={Pc}")
	y, t = step(P, np.arange(0, 10 , 0.01))
	fig, ax = plt.subplots(figsize=(3, 2.3))
	ax.plot(t,y)
	ax.set_xlabel('t')
	ax.set_ylabel('y')
	ax.grid(ls=':')
	st.pyplot(fig)

with st.expander("制御系のステップ応答"):
	st.text(f"Kp={Kp},Ki={Ki},Kd={Kd}")
	st.text(f"m={Pa},c={Pb},k={Pc}")
	y, t = step(Gyr, np.arange(0, 10 , 0.01))
	fig, ax = plt.subplots(figsize=(3, 2.3))
	ax.plot(t,y)
	ax.set_xlabel('t')
	ax.set_ylabel('y')
	ax.grid(ls=':')
	st.pyplot(fig)

# フィードバック制御
with st.expander("制御シミュレーション"):
	L = st.number_input('目標値',value=1)
	st.text(f"Kp={Kp},Ki={Ki},Kd={Kd}")
	st.text(f"m={Pa},c={Pb},k={Pc}")
	t = np.linspace(0, 100, 1000)
	y, t = step(L*Gyr, t)
	fig, ax = plt.subplots(figsize=(3, 2.3))
	ax.plot(t,y)
	ax.set_xlabel('t')
	ax.set_ylabel('y')
	ax.grid(ls=':')
	plt.axhline(L, color="b", linestyle="--")
	st.pyplot(fig)