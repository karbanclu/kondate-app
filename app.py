import streamlit as st
import random

# アプリのタイトルと説明
st.title("今日の献立ルーレット🍽️")
st.write("ボタンを押すと、今日の献立が決まります！")

# 献立のリスト（後であなたの好きなメニューに変更できます）
menu_list = ["カレーライス", "豚の生姜焼き", "唐揚げ", "ハンバーグ", "焼き魚", "オムライス", "肉じゃが"]

# ボタンが押された時の処理（if文）
if st.button("今日のご飯を決める！"):
    # リストの中からランダムに1つ選ぶ
    chosen_menu = random.choice(menu_list)
    
    # 選ばれたメニューを画面に大きく表示する
    st.success(f"今日は「{chosen_menu}」に決定！")
    
    # おまけ：風船を飛ばす演出
    st.balloons()