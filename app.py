import streamlit as st
import random

# アプリのタイトル
st.title("わが家の献立ルーレット 2.0 🍽️")

# --- 1. 献立リストを「覚える」ための準備 ---
# アプリが起動したとき、まだリストがなければ初期メニューを作ります
if 'menu_list' not in st.session_state:
    st.session_state.menu_list = ["カレーライス", "豚の生姜焼き", "唐揚げ", "ハンバーグ", "焼き魚"]

# --- 2. メニューを追加する機能 ---
st.subheader("📝 レパートリーを増やす")
# テキスト入力欄
new_menu = st.text_input("新しい献立の名前を入力してください")

if st.button("リストに追加する"):
    if new_menu: # 何か文字が入っていたら
        # session_state の中のリストに名前を追加
        st.session_state.menu_list.append(new_menu)
        st.success(f"「{new_menu}」を追加しました！")
    else:
        st.error("献立名を入力してください")

# --- 3. ルーレットを回す機能 ---
st.subheader("🎲 今日は何を食べる？")
if st.button("ルーレットを回す！"):
    # 覚えさせてあるリストの中からランダムに選ぶ
    chosen = random.choice(st.session_state.menu_list)
    st.header(f"今日は「{chosen}」に決定！")
    st.balloons()

# --- 4. 現在のリストを確認（おまけ） ---
with st.expander("現在のレパートリーを確認する"):
    st.write(st.session_state.menu_list)