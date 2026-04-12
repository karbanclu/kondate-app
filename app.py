import streamlit as st
import random
import json
import gspread
import urllib.parse

# --- スプレッドシートの準備 ---
credentials_dict = json.loads(st.secrets["gcp_service_account_json"])
gc = gspread.service_account_from_dict(credentials_dict)
sh = gc.open("menu_data") 
worksheet = sh.sheet1

# ★ページ全体のレイアウト設定（スマホでも見やすく）
st.set_page_config(page_title="献立ルーレット", page_icon="🍽️", layout="centered")

# アプリのタイトル
st.title("わが家の献立ルーレット 🍽️")
st.divider() # ★区切り線を追加してスッキリさせる

# --- 状態の初期化 ---
def load_menus():
    records = worksheet.col_values(1)
    if len(records) > 1:
        return records[1:]
    else:
        return []

if 'menu_list' not in st.session_state:
    st.session_state.menu_list = load_menus()

if 'last_chosen' not in st.session_state:
    st.session_state.last_chosen = None

# --- ルーレットを回す機能（メイン機能を一番上に移動！） ---
st.subheader("🎲 今日は何を食べる？")

# ★ボタンを中央寄りに目立たせる工夫
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    roll_button = st.button("ぐるぐる回す！", use_container_width=True) # ボタンを横幅いっぱいに広げる

if roll_button:
    menu_count = len(st.session_state.menu_list)
    
    if menu_count > 1:
        available_menus = [m for m in st.session_state.menu_list if m != st.session_state.last_chosen]
        chosen = random.choice(available_menus)
        st.session_state.last_chosen = chosen 
        
        # ★結果を色付きの枠（st.success）で囲って目立たせる
        st.success(f"## 🎉 今日は「{chosen}」に決定！")
        st.balloons()
        
        search_word = chosen + " レシピ"
        encoded_word = urllib.parse.quote(search_word)
        search_url = f"https://www.google.com/search?q={encoded_word}"
        st.link_button(f"🍳 「{chosen}」のレシピを探す", search_url, use_container_width=True)
        
    elif menu_count == 1:
        chosen = st.session_state.menu_list[0]
        st.success(f"## 🎉 今日は「{chosen}」に決定！")
        st.balloons()
        
        search_word = chosen + " レシピ"
        encoded_word = urllib.parse.quote(search_url)
        st.link_button(f"🍳 「{chosen}」のレシピを探す", search_url, use_container_width=True)
        
    else:
        st.warning("メニューがありません。下の欄から追加してください！")

st.divider() # ★区切り線

# --- メニューを追加・削除する機能（管理機能はまとめて下に） ---
st.subheader("⚙️ メニューの管理")

# ★追加と削除を「タブ」で切り替えられるようにして省スペース化！
tab1, tab2, tab3 = st.tabs(["📝 追加する", "🗑️ 削除する", "📋 全一覧"])

with tab1:
    # ★入力欄とボタンを横並び（7:3の割合）にする
    add_col1, add_col2 = st.columns([7, 3])
    with add_col1:
        new_menu = st.text_input("新しい献立名", label_visibility="collapsed", placeholder="例：肉じゃが")
    with add_col2:
        if st.button("追加", use_container_width=True):
            if new_menu:
                worksheet.append_row([new_menu])
                st.session_state.menu_list.append(new_menu)
                st.rerun()

with tab2:
    if len(st.session_state.menu_list) > 0:
        del_col1, del_col2 = st.columns([7, 3])
        with del_col1:
            delete_target = st.selectbox("削除する献立", st.session_state.menu_list, label_visibility="collapsed")
        with del_col2:
            if st.button("削除", use_container_width=True):
                idx = st.session_state.menu_list.index(delete_target)
                worksheet.delete_rows(idx + 2)
                st.session_state.menu_list.pop(idx)
                if st.session_state.last_chosen == delete_target:
                    st.session_state.last_chosen = None
                st.rerun()
    else:
        st.write("削除できるメニューがありません。")

with tab3:
    st.write("現在登録されているメニュー：", len(st.session_state.menu_list), "種類")
    st.write(", ".join(st.session_state.menu_list)) # リストを横並びの文字で表示してスッキリさせる