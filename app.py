import streamlit as st
import random
import json
import gspread

# --- 1. スプレッドシートの準備 ---
# Streamlitの金庫（Secrets）から合鍵を取り出して辞書に変換
credentials_dict = json.loads(st.secrets["gcp_service_account_json"])
# 合鍵を使ってGoogleにログイン
gc = gspread.service_account_from_dict(credentials_dict)
# スプレッドシートを開く（名前が違う場合はここを変更！）
sh = gc.open("menu_data") 
# 最初のシートを選ぶ
worksheet = sh.sheet1

# アプリのタイトル
st.title("わが家の献立ルーレット 3.0 🍽️")

# --- 2. メニューを読み込む関数 ---
def load_menus():
    # A列のすべての値を取得（1行目の見出しは省く）
    records = worksheet.col_values(1)
    if len(records) > 1:
        return records[1:]
    else:
        return []

# アプリ起動時にメニューを読み込む
if 'menu_list' not in st.session_state:
    st.session_state.menu_list = load_menus()

# --- 3. メニューを追加する機能 ---
st.subheader("📝 レパートリーを増やす")
new_menu = st.text_input("新しい献立の名前を入力してください")

if st.button("リストに追加する"):
    if new_menu:
        # スプレッドシートの一番下に書き込む！
        worksheet.append_row([new_menu])
        # 画面のリストも更新する
        st.session_state.menu_list.append(new_menu)
        st.success(f"「{new_menu}」をスプレッドシートに保存しました！")
    else:
        st.error("献立名を入力してください")

# --- 4. ルーレットを回す機能 ---
st.subheader("🎲 今日は何を食べる？")
if st.button("ルーレットを回す！"):
    if len(st.session_state.menu_list) > 0:
        chosen = random.choice(st.session_state.menu_list)
        st.header(f"今日は「{chosen}」に決定！")
        st.balloons()
    else:
        st.warning("メニューがありません。追加してください！")

# --- 現在のリストを確認（おまけ） ---
with st.expander("現在のレパートリーを確認する"):
    st.write(st.session_state.menu_list)