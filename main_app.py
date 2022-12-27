import streamlit as st#streamlitをインポート
from control.matlab import *#controlモジュールのmatlabをインポート
import matplotlib.pyplot as plt#matplotlibのpyplotをインポート
import numpy as np#numpyをインポート

st.title("PID制御シミュレーション")#大きな文字でPID制御シミュレーションと表示

Kp = st.number_input('Kp',min_value=0.00,value=1.00)#最小値0.00,初期値1.00の数字を入力する場所を作成
Ki = st.number_input('Ki',min_value=0.00)
Kd = st.number_input('Kd',min_value=0.00)

#制御対象の伝達関数
with st.expander('制御対象の伝達関数'):#クリックすると開くところを作成↓中身
        st.latex("\\frac{k}{ms^2+cs+1}")#latexのやつ
        Pa = st.number_input('m')
        Pb = st.number_input('c',value=1.00)
        Pc = st.number_input('k',value=1.00)
        #ここまで制御対象の伝達関数の中身

P =tf(Pc,[Pa, Pb, 1])#tf(A,[B,C,D])で伝達関数(A)/(Bs^2+Cs+D),matlabの関数です
C =tf([Kd, Kp, Ki],[1, 0])#伝達関数Kds+Kp+Ki/s
Gyr = feedback(P*C, 1)#PとCの閉ループ系,matlabの関数

#シミュレーション時間設定
with st.expander("シミュレーション時間"):
	T1 = st.number_input('制御対象のステップ応答',value=10)
	T2 = st.number_input('制御系のステップ応答',value=10)
	T3 = st.number_input('制御シミュレーション',value=100)
	
#制御対象のステップ応答
with st.expander("制御対象のステップ応答"):#クリックすると開くところを作成↓中身
	st.text(f"m={Pa},c={Pb},k={Pc}")
	y, t = step(P, np.arange(0, T1 , 0.01))#Pのステップ応答
	fig, ax = plt.subplots(figsize=(3, 2.3))#グラフの縦横比を3:2.3に
	ax.plot(t,y)
	ax.set_xlabel('t')#x軸ラベルをtに
	ax.set_ylabel('y')#y軸ラベルをyに
	ax.grid(ls=':')
	st.pyplot(fig)
	#ここまで制御対象のステップ応答の中身

#制御系のステップ応答
with st.expander("制御系のステップ応答"):
	st.text(f"Kp={Kp},Ki={Ki},Kd={Kd}")
	st.text(f"m={Pa},c={Pb},k={Pc}")
	y, t = step(Gyr, np.arange(0, T2 , 0.01))
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
	t = np.linspace(0, T3, 1000)
	y, t = step(L*Gyr, t)#制御系のステップ応答を目標値倍する
	fig, ax = plt.subplots(figsize=(3, 2.3))
	ax.plot(t,y)
	ax.set_xlabel('t')
	ax.set_ylabel('y')
	ax.grid(ls=':')
	plt.axhline(L, color="b", linestyle="--")
	st.pyplot(fig)
