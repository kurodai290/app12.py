import streamlit as st
import pandas as pd
import random

# アプリの設定
st.set_page_config(page_title="JAPAN GUESSER 100", layout="centered")
st.title("🗺️ 【位置当てゲーム：JAPAN GUESSER 100】")
st.caption("URLチェック強化版。全問正解を目指してピンを刺せ！")

# 1. CSVデータファイルの読み込み
@st.cache_data
def load_quiz_data():
    try:
        # UTF-8でCSVを読み込む
        df = pd.read_csv("quiz_data.csv", encoding="utf-8")
        return df.to_dict(orient="records")
    except Exception as e:
        st.error(f"⚠️ quiz_data.csv の読み込みに失敗しました: {e}")
        return []

all_questions = load_quiz_data()

# 2. セッション状態の初期化
if "game_started" not in st.session_state:
    st.session_state.game_started = False
    st.session_state.quiz_pool = []
    st.session_state.current_index = 0
    st.session_state.score = 0
    st.session_state.answered = False
    st.session_state.feedback = ""
    st.session_state.total_questions_to_play = 100

# 3. ゲーム開始・リセット関数
def start_new_marathon():
    if not all_questions:
        return
    shuffled = all_questions.copy()
    random.shuffle(shuffled)
    
    limit = min(st.session_state.total_questions_to_play, len(shuffled))
    st.session_state.quiz_pool = shuffled[:limit]
    
    st.session_state.current_index = 0
    st.session_state.score = 0
    st.session_state.answered = False
    st.session_state.feedback = ""
    st.session_state.game_started = True

# --- 画面レイアウト ---
if not st.session_state.game_started:
    st.subheader("🏁 ジオゲッサー・日本百人組手")
    st.write(f"現在、データベースには **{len(all_questions)}問** のスポットが登録されています。")
    
    max_available = min(100, len(all_questions)) if all_questions else 10
    st.session_state.total_questions_to_play = st.slider("何問挑戦しますか？", 5, max_available, min(100, max_available))
    
    if st.button("🚀 マラソンを開始する", use_container_width=True):
        start_new_marathon()
        st.rerun()

else:
    pool = st.session_state.quiz_pool
    idx = st.session_state.current_index
    total_q = len(pool)
    
    # サイドバー情報
    st.sidebar.header("📊 マラソン状況")
    st.sidebar.metric("現在のスコア", f"{st.session_state.score} 点")
    st.sidebar.metric("進行状況", f"{idx + 1} / {total_q} 問目")
    st.sidebar.progress(int(((idx) / total_q) * 100), text="走破率")
    
    if st.sidebar.button("🚪 タイトルに戻る"):
        st.session_state.game_started = False
        st.rerun()

    # 全問終了判定
    if idx >= total_q:
        max_score = total_q * 100
        st.success(f"🎉 完走おめでとうございます！最終スコア: {st.session_state.score} / {max_score} 点")
        
        accuracy = (st.session_state.score / max_score) * 100
        if accuracy == 100:
            st.title("👑 ランク：日本地理の神")
        elif accuracy >= 80:
            st.title("🚗 ランク：一流ドライバー")
        elif accuracy >= 50:
            st.title("🚲 ランク：一般旅行者")
        else:
            st.title("🚶 ランク：方向音痴")

        if st.button("もう一度挑戦する", use_container_width=True):
            start_new_marathon()
            st.rerun()
    else:
        q = pool[idx]
        
        st.subheader(f"📍 第 {idx + 1} 問目")
        st.info(f"💡 {q['hint']}")
        
        # --- 画像判定ロジックの強化（余白削除のクレンジング追加） ---
        raw_url = str(q.get("image_url", "")).strip()
        
        if pd.notna(q.get("image_url")) and (raw_url.startswith("http://") or raw_url.startswith("https://")):
            try:
                st.image(raw_url, caption="この場所はどこ？", use_container_width=True)
            except Exception as img_err:
                st.error("⚠️ 画像の描写処理でエラーが発生しました。テキストヒントから推測してください。")
                st.caption(f"システム理由: {img_err}")
        else:
            # URLが壊れている、または認識されなかった場合のフォールバック（強制停止を防ぐ）
            st.warning("⚠️ CSVに有効なインターネット画像URL（https://...）が登録されていません。テキストヒントのみで勝負です！")
            st.caption(f"登録されていた値: {raw_url}")
        
        # 選択肢の構築
        choices = [q["choice1"], q["choice2"], q["choice3"], q["choice4"], q["choice5"]]
        choices = [c for c in choices if pd.notna(c)]
        
        # 回答フォーム
        with st.form(key=f"guess_form_{idx}"):
            user_guess = st.selectbox("ここだと思う都道府県を選んでください：", choices)
            submit_button = st.form_submit_button(label="📍 ここにピンを刺す（回答）")
            
        if submit_button and not st.session_state.answered:
            st.session_state.answered = True
            if user_guess == q["correct_pref"]:
                st.session_state.score += 100
                st.session_state.feedback = f"🎯 正解！+100ポイント！\n\n{q['description']}"
            else:
                st.session_state.feedback = f"❌ 残念！あなたの予想: {user_guess} ➔ 正解: {q['correct_pref']}\n\n{q['description']}"
            st.rerun()

        # 回答後のフィードバック表示
        if st.session_state.answered:
            if "🎯" in st.session_state.feedback:
                st.success(st.session_state.feedback)
            else:
                st.error(st.session_state.feedback)
                
            if st.button("次の問題へ ➔", use_container_width=True):
                st.session_state.answered = False
                st.session_state.feedback = ""
                st.session_state.current_index += 1
                st.rerun()
