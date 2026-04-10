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
st.title("わが家の献立ルーレット 5.0 🍽️")

# --- 2. 状態の初期化 ---
def load_menus():
    records = worksheet.col_values(1)
    if len(records) > 1:
        return records[1:]
    else:
        return []

if 'menu_list' not in st.session_state:
    st.session_state.menu_list = load_menus()

# ★新しく「前回選ばれたメニュー」を記憶する箱を用意
if 'last_chosen' not in st.session_state:
    st.session_state.last_chosen = None

# --- 3. メニューを追加する機能 ---
st.subheader("📝 レパートリーを増やす")
new_menu = st.text_input("新しい献立の名前を入力してください")

if st.button("リストに追加する"):
    if new_menu:
        worksheet.append_row([new_menu])
        st.session_state.menu_list.append(new_menu)
        st.success(f"「{new_menu}」を保存しました！")
        st.rerun()
    else:
        st.error("献立名を入力してください")

# --- 4. ルーレットを回す機能 (★ここが進化！) ---
st.subheader("🎲 今日は何を食べる？")
if st.button("ルーレットを回す！"):
    menu_count = len(st.session_state.menu_list)
    
    if menu_count > 1:
        # 候補リストから「前回選ばれたメニュー」を除外する
        available_menus = [m for m in st.session_state.menu_list if m != st.session_state.last_chosen]
        
        # 除外した後のリストからランダムに選ぶ
        chosen = random.choice(available_menus)
        
        # 今回選ばれたメニューを「前回出たメニュー」として新しく記憶させる
        st.session_state.last_chosen = chosen 
        
        st.header(f"今日は「{chosen}」に決定！")
        st.balloons()
        
    elif menu_count == 1:
        # メニューが1つしかない場合はそれをそのまま出す
        chosen = st.session_state.menu_list[0]
        st.header(f"今日は「{chosen}」に決定！")
        st.balloons()
        
    else:
        st.warning("メニューがありません。追加してください！")

# --- 5. メニューを削除する機能 ---
st.subheader("🗑️ レパートリーを整理する")
if len(st.session_state.menu_list) > 0:
    delete_target = st.selectbox("削除する献立を選んでください", st.session_state.menu_list)
    
    if st.button("選択した献立を削除する"):
        idx = st.session_state.menu_list.index(delete_target)
        row_to_delete = idx + 2
        worksheet.delete_rows(row_to_delete)
        st.session_state.menu_list.pop(idx)
        
        # ★もし「前回選んだメニュー」を削除した場合は、記憶をリセットする
        if st.session_state.last_chosen == delete_target:
            st.session_state.last_chosen = None
            
        st.warning(f"「{delete_target}」を削除しました。")
        st.rerun()
else:
    st.write("削除できるメニューがありません。")

# 現在のリストを確認
with st.expander("現在の全レパートリーを確認"):
    st.write(st.session_state.menu_list)