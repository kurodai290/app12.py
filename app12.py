import streamlit as st
import pandas as pd
import random

# アプリの設定
st.set_page_config(page_title="JAPAN GUESSER 100", layout="centered")
st.title("🗺️ 【位置当てゲーム：JAPAN GUESSER 100】")
st.caption("登録された大量のデータからランダムに出題！全問正解を目指せ！")

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
    st.session_state.total_questions_to_play = 100  # ここでプレイする総問題数を指定可能

# 3. ゲーム開始・リセット関数
def start_new_marathon():
    if not all_questions:
        return
    # CSVにある全ての問題をシャッフル
    shuffled = all_questions.copy()
    random.shuffle(shuffled)
    
    # 指定した問題数（例：100問）をプールにセット（CSVの総数が足りない場合は全数）
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
    
    # プレイ問数の選択（最大100問など）
    max_available = min(100, len(all_questions)) if all_questions else 10
    st.session_state.total_questions_to_play = st.slider("何問挑戦しますか？", 5, max_available, min(100, max_available))
    
    if st.button("🚀 マラソンを開始する", use_container_width=True):
        start_new_marathon()
        st.rerun()

else:
    # 進行度の計算
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

    # ゲームオーバー（全問終了）判定
    if idx >= total_q:
        max_score = total_q * 100
        st.success(f"🎉 完走おめでとうございます！最終スコア: {st.session_state.score} / {max_score} 点")
        
        # ランク評価
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
        # 現在の問題データを取得
        q = pool[idx]
        
        st.subheader(f"📍 第 {idx + 1} 問目")
        st.info(f"💡 {q['hint']}")
        
        # 画像の表示（URLエラー対策付き）
        try:
            st.image(q["image_url"], caption="この場所はどこ？", use_container_width=True)
        except:
            st.warning("⚠️ 画像の読み込みに失敗しました。ヒントと選択肢から推理してください。")
        
        # 選択肢をリスト化
        choices = [q["choice1"], q["choice2"], q["choice3"], q["choice4"], q["choice5"]]
        # 空白データを排除
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
