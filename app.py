import streamlit as st
import random
import json
import gspread

# --- 1. スプレッドシートの準備 ---
credentials_dict = json.loads(st.secrets["gcp_service_account_json"])
gc = gspread.service_account_from_dict(credentials_dict)
sh = gc.open("menu_data") 
worksheet = sh.sheet1

# アプリのタイトル
st.title("わが家の献立ルーレット 4.0 🍽️")

# --- 2. メニューを読み込む関数 ---
def load_menus():
    records = worksheet.col_values(1)
    if len(records) > 1:
        return records[1:] # 1行目の見出しを除いて返す
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
        worksheet.append_row([new_menu])
        st.session_state.menu_list.append(new_menu)
        st.success(f"「{new_menu}」を保存しました！")
        st.rerun() # 画面を更新して削除リストにも反映させる
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

# --- 5. メニューを削除する機能 (新機能！) ---
st.subheader("🗑️ レパートリーを整理する")
if len(st.session_state.menu_list) > 0:
    # 削除したいメニューをセレクトボックスで選択
    delete_target = st.selectbox("削除する献立を選んでください", st.session_state.menu_list)
    
    if st.button("選択した献立を削除する"):
        # スプレッドシート上の行番号を計算
        # (リストの順番 0から開始) + (見出しの1行分) + (1から数えるための調整1) = +2
        idx = st.session_state.menu_list.index(delete_target)
        row_to_delete = idx + 2
        
        # Googleスプレッドシートから行を削除
        worksheet.delete_rows(row_to_delete)
        
        # アプリ内のリストからも削除
        st.session_state.menu_list.pop(idx)
        
        st.warning(f"「{delete_target}」を削除しました。")
        # 画面を最新の状態に更新
        st.rerun()
else:
    st.write("削除できるメニューがありません。")

# 現在のリストを確認
with st.expander("現在の全レパートリーを確認"):
    st.write(st.session_state.menu_list)