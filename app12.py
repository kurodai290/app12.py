import streamlit as st
import random

# アプリの設定
st.set_page_config(page_title="JAPAN GUESSER MULTI", layout="centered")
st.title("🗺️ 【位置当て対戦ゲーム：JAPAN GUESSER MULTI】")
st.caption("同じ画面で交代で遊ぶローカルマルチプレイ対応版！友達や家族と地理力を競おう！")

# 1. 画像データ（Base64テキスト形式で内蔵・通信エラーゼロ）
FUJI_IMG = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAKAAAABgCAYAAACIv69QAAAABmJLR0QA/wD/AP+gvaeTAAAAdklEQVR4nO3BMQEAAADCoPVPbQ0PoAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHwMGbYAAf39Y7gAAAAAElFTkSuQmCC"
KINKAKU_IMG = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAKAAAABgCAYAAACIv69QAAAABmJLR0QA/wD/AP+gvaeTAAAAdklEQVR4nO3BMQEAAADCoPVPbQ0PoAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHwMGbYAAf39Y7gAAAAAElFTkSuQmCC"
SAKYU_IMG = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAKAAAABgCAYAAACIv69QAAAABmJLR0QA/wD/AP+gvaeTAAAAdklEQVR4nO3BMQEAAADCoPVPbQ0PoAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHwMGbYAAf39Y7gAAAAAElFTkSuQmCC"
HOKKAIDO_IMG = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAKAAAABgCAYAAACIv69QAAAABmJLR0QA/wD/AP+gvaeTAAAAdklEQVR4nO3BMQEAAADCoPVPbQ0PoAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHwMGbYAAf39Y7gAAAAAElFTkSuQmCC"
OKINAWA_IMG = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAKAAAABgCAYAAACIv69QAAAABmJLR0QA/wD/AP+gvaeTAAAAdklEQVR4nO3BMQEAAADCoPVPbQ0PoAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHwMGbYAAf39Y7gAAAAAElFTkSuQmCC"

@st.cache_data
def get_quiz_data():
    return [
        {"id": 1, "hint": "非常に有名な日本のシンボルです。山頂の雪と周りの自然が特徴です。", "image_data": FUJI_IMG, "correct_pref": "静岡県", "choices": ["北海道", "東京都", "静岡県", "京都府", "沖縄県"], "description": "富士山（静岡県・山梨県）でした！"},
        {"id": 2, "hint": "歴史的な建造物（お寺）です。建物全体が金箔で覆われています。", "image_data": KINKAKU_IMG, "correct_pref": "京都府", "choices": ["奈良県", "京都府", "石川県", "広島県", "東京都"], "description": "金閣寺（京都府）でした！"},
        {"id": 3, "hint": "青い海と白い砂漠のような景色、そして歩いている動物に注目してください。", "image_data": SAKYU_IMG, "correct_pref": "鳥取県", "choices": ["千葉県", "鳥取県", "鹿児島県", "沖縄県", "香川県"], "description": "鳥取砂丘でした！"},
        {"id": 4, "hint": "日本最北端の大地です。広大な大自然と冬の雪景色が有名です。", "image_data": HOKKAIDO_IMG, "correct_pref": "北海道", "choices": ["北海道", "青森県", "岩手県", "秋田県", "新潟県"], "description": "北海道の広大な雪景色でした！"},
        {"id": 5, "hint": "透明度の高い透き通った海と、白い砂浜が広がる南国のリゾート地です。", "image_data": OKINAWA_IMG, "correct_pref": "沖縄県", "choices": ["鹿児島県", "宮崎県", "沖縄県", "長崎県", "高知県"], "description": "沖縄県のエメラルドグリーンの海でした！"}
    ]

all_questions = get_quiz_data()

# 2. セッション状態（マルチプレイ対応）の初期化
if "game_started" not in st.session_state:
    st.session_state.game_started = False
    st.session_state.quiz_pool = []
    st.session_state.current_index = 0
    st.session_state.num_players = 1
    st.session_state.player_names = []
    st.session_state.player_scores = {}
    st.session_state.player_turn_idx = 0  # 誰の番かを表すインデックス
    st.session_state.answered = False
    st.session_state.feedback = ""

# 3. ゲームリセット・開始処理
def start_multi_game():
    shuffled = all_questions.copy()
    random.shuffle(shuffled)
    
    # 参加プレイヤー人数分の問題、または全問をプールに格納
    st.session_state.quiz_pool = shuffled
    st.session_state.current_index = 0
    st.session_state.player_turn_idx = 0
    st.session_state.answered = False
    st.session_state.feedback = ""
    
    # スコア初期化
    st.session_state.player_scores = {name: 0 for name in st.session_state.player_names}
    st.session_state.game_started = True

# --- 画面レイアウト ---
if not st.session_state.game_started:
    st.subheader("👥 対戦設定")
    
    # 人数選択
    num_players = st.slider("プレイ人数を選んでください", 1, 4, 2)
    
    # 名前の入力フォーム
    player_names = []
    for i in range(num_players):
        name = st.text_input(f"プレイヤー {i+1} の名前", f"プレイヤー {i+1}", key=f"pname_{i}")
        player_names.append(name)
        
    if st.button("🚀 ゲームを開始する", use_container_width=True):
        st.session_state.num_players = num_players
        st.session_state.player_names = player_names
        start_multi_game()
        st.rerun()

else:
    pool = st.session_state.quiz_pool
    idx = st.session_state.current_index
    total_q = len(pool)
    
    # 現在の解答担当プレイヤーの特定
    current_player = st.session_state.player_names[st.session_state.player_turn_idx]
    
    # サイドバー：現在のスコアボード一覧表示
    st.sidebar.header("📊 スコアボード")
    for name in st.session_state.player_names:
        st.sidebar.write(f"👤 {name} : **{st.session_state.player_scores[name]} 点**")
        
    st.sidebar.write("---")
    st.sidebar.write(f"進行状況: {idx + 1} / {total_q} 問目")
    
    if st.sidebar.button("🚪 タイトルに戻る"):
        st.session_state.game_started = False
        st.rerun()

    # 全問終了（ゲームオーバー）判定
    if idx >= total_q:
        st.success("🎉 全ての問題が終了しました！最終結果の発表です！")
        
        # スコア順に並び替え
        sorted_scores = sorted(st.session_state.player_scores.items(), key=lambda x: x[1], reverse=True)
        
        st.subheader("🏆 最終ランキング 🏆")
        for rank, (name, score) in enumerate(sorted_scores, 1):
            if rank == 1:
                st.title(f"🥇 優勝: {name} ({score}点)")
            elif rank == 2:
                st.subheader(f"🥈 第2位: {name} ({score}点)")
            else:
                st.write(f"🥉 第{rank}位: {name} ({score}点)")
                
        if st.button("もう一度同じメンバーで遊ぶ", use_container_width=True):
            start_multi_game()
            st.rerun()
    else:
        q = pool[idx]
        
        # 手番プレイヤーの目立つ表示
        st.markdown(f"### 📢 現在の手番: **{current_player}** さんの番です！")
        st.info(f"💡 ヒント: {q['hint']}")
        
        # 内蔵データから画像表示
        st.image(q["image_data"], caption="地形・環境のヒント", use_container_width=True)
        
        # 回答フォーム
        with st.form(key=f"guess_form_{idx}_{st.session_state.player_turn_idx}"):
            user_guess = st.selectbox(f"{current_player} さんの予想（都道府県）：", q["choices"])
            submit_button = st.form_submit_button(label="📍 ここにピンを刺す（回答）")
            
        if submit_button and not st.session_state.answered:
            st.session_state.answered = True
            if user_guess == q["correct_pref"]:
                st.session_state.player_scores[current_player] += 100
                st.session_state.feedback = f"🎯 正解！ **{current_player}** さんに +100ポイント！\n\n{q['description']}"
            else:
                st.session_state.feedback = f"❌ 残念！ **{current_player}** さんの予想: {user_guess} ➔ 正解: {q['correct_pref']}\n\n{q['description']}"
            st.rerun()

        # 回答後の処理
        if st.session_state.answered:
            if "🎯" in st.session_state.feedback:
                st.success(st.session_state.feedback)
            else:
                st.error(st.session_state.feedback)
                
            if st.button("次の問題へ ➔", use_container_width=True):
                st.session_state.answered = False
                st.session_state.feedback = ""
                
                # 次のプレイヤーに手番を交代（人数で割った余りでループ）
                st.session_state.player_turn_idx = (st.session_state.player_turn_idx + 1) % st.session_state.num_players
                # 次の問題に進む
                st.session_state.current_index += 1
                st.rerun()
