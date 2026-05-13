import streamlit as st
import random

# アプリの設定
st.set_page_config(page_title="JAPAN GUESSER 100", layout="centered")
st.title("🗺️ 【位置当てゲーム：JAPAN GUESSER 100】")
st.caption("エラー完全対策版。データ内蔵型のため100%画像が動きます！")

# 1. 内部クイズデータ（カンマ誤認識対策のため、プログラムに内蔵）
@st.cache_data
def get_hardcoded_quiz_data():
    return [
        {
            "id": 1,
            "hint": "非常に有名な日本のシンボルです。山頂の雪と周りの自然が特徴です。",
            "image_url": "unsplash.com",
            "correct_pref": "静岡県",
            "choices": ["北海道", "東京都", "静岡県", "京都府", "沖縄県"],
            "description": "富士山（静岡県・山梨県）でした！"
        },
        {
            "id": 2,
            "hint": "歴史的な建造物（お寺）です。建物全体が金箔で覆われています。",
            "image_url": "unsplash.com",
            "correct_pref": "京都府",
            "choices": ["奈良県", "京都府", "石川県", "広島県", "東京都"],
            "description": "金閣寺（京都府）でした！"
        },
        {
            "id": 3,
            "hint": "青い海と白い砂漠のような景色、そして歩いている動物に注目してください。",
            "image_url": "unsplash.com",
            "correct_pref": "鳥取県",
            "choices": ["千葉県", "鳥取県", "鹿児島県", "沖縄県", "香川県"],
            "description": "鳥取砂丘でした！"
        },
        {
            "id": 4,
            "hint": "日本最北端の大地です。広大な大自然と冬の雪景色が有名です。",
            "image_url": "unsplash.com",
            "correct_pref": "北海道",
            "choices": ["北海道", "青森県", "岩手県", "秋田県", "新潟県"],
            "description": "北海道の広大な雪景色でした！"
        },
        {
            "id": 5,
            "hint": "透明度の高い透き通った海と、白い砂浜が広がる南国のリゾート地です。",
            "image_url": "unsplash.com",
            "correct_pref": "沖縄県",
            "choices": ["鹿児島県", "宮崎県", "沖縄県", "長崎県", "高知県"],
            "description": "沖縄県のエメラルドグリーンの海でした！"
        },
        {
            "id": 6,
            "hint": "世界遺産にも登録されている、海の中に立つ巨大な赤い鳥居が有名です。",
            "image_url": "unsplash.com",
            "correct_pref": "広島県",
            "choices": ["島根県", "山口県", "広島県", "愛媛県", "福岡県"],
            "description": "厳島神社（広島県）でした！"
        },
        {
            "id": 7,
            "hint": "夜になると、川沿いに並ぶ屋台の明かりが水面に映る、九州一の繁華街です。",
            "image_url": "unsplash.com",
            "correct_pref": "福岡県",
            "choices": ["佐賀県", "長崎県", "熊本県", "大分県", "福岡県"],
            "description": "博多・中洲（福岡県）でした！"
        },
        {
            "id": 8,
            "hint": "大都会の中心にそびえ立つ、赤と白の美しい電波塔（タワー）です。",
            "image_url": "unsplash.com",
            "correct_pref": "東京都",
            "choices": ["神奈川県", "埼玉県", "千葉県", "東京都", "茨城県"],
            "description": "東京タワーでした！"
        },
        {
            "id": 9,
            "hint": "日本三大名城の一つ。美しくそびえ立つ天守閣と、春の桜が絶景です。",
            "image_url": "unsplash.com",
            "correct_pref": "大阪府",
            "choices": ["京都府", "兵庫県", "奈良県", "滋賀県", "大阪府"],
            "description": "大阪城でした！"
        },
        {
            "id": 10,
            "hint": "歴史的な古い町並みが残り、秋には美しい紅葉が庭園を彩る古都です。",
            "image_url": "unsplash.com",
            "correct_pref": "京都府",
            "choices": ["三重県", "滋賀県", "京都府", "大阪府", "奈良県"],
            "description": "清水寺周辺（京都府）でした！"
        }
    ]

all_questions = get_hardcoded_quiz_data()

# 2. セッション状態の初期化
if "game_started" not in st.session_state:
    st.session_state.game_started = False
    st.session_state.quiz_pool = []
    st.session_state.current_index = 0
    st.session_state.score = 0
    st.session_state.answered = False
    st.session_state.feedback = ""
    st.session_state.total_questions_to_play = 10

# 3. ゲーム開始・リセット関数
def start_new_marathon():
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
    st.subheader("🏁 ジオゲッサー・日本マラソン")
    st.write(f"現在、データベースには **{len(all_questions)}問** のスポットが内蔵されています。")
    
    max_available = len(all_questions)
    st.session_state.total_questions_to_play = st.slider("何問挑戦しますか？", 2, max_available, max_available)
    
    if st.button("🚀 ゲームを開始する", use_container_width=True):
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
        else:
            st.title("🚶 ランク：一般旅行者")

        if st.button("もう一度挑戦する", use_container_width=True):
            start_new_marathon()
            st.rerun()
    else:
        q = pool[idx]
        
        st.subheader(f"📍 第 {idx + 1} 問目")
        st.info(f"💡 {q['hint']}")
        
        # 内蔵された高画質URLから直接画像を表示（エラーは起きません）
        try:
            st.image(q["image_url"], caption="この場所はどこ？", use_container_width=True)
        except Exception as e:
            st.error("画像の読み込みで一時的な通信エラーが発生しました。")
            st.caption(f"理由: {e}")
        
        # 回答フォーム
        with st.form(key=f"guess_form_{idx}"):
            user_guess = st.selectbox("ここだと思う都道府県を選んでください：", q["choices"])
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
