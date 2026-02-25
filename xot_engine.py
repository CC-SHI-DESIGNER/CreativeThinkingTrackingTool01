import pandas as pd
import json
import os

# 模擬 XoT 的思維分叉函數 (真實應用時可對接 OpenAI/Gemini API)
def xot_thought_expansion(raw_feature):
    # XoT 的核心在於從一個想法出發，生成多個維度的思考節點
    # 這裡我們定義三個 XoT 維度：技術可行性、用戶體驗、未來演化
    thoughts = [
        {"type": "Technical", "content": f"基於{raw_feature}的材料科學優化"},
        {"type": "UX", "content": f"針對{raw_feature}的交互行為建模"},
        {"type": "Evolution", "content": f"下一代{raw_feature}的模組化演進"}
    ]
    return thoughts

def generate_real_nodes():
    # 1. 讀取真實數據
    df = pd.read_csv('data/sheet1.csv')
    
    nodes = [{"id": "Root", "label": "Smart Wearable XoT Center", "group": 0}]
    links = []

    # 2. 處理 63 筆數據
    for i, row in df.iterrows():
        user_id = f"User_{i+1}"
        user_name = str(row['姓名'])
        raw_feature = str(row['產品的外型特徵'])
        
        # A. 創建「人類原始創意節點」
        nodes.append({
            "id": user_id,
            "label": user_name,
            "feature": raw_feature,
            "group": 1,
            "sketch": f"data/sketches/{user_id}.png"
        })
        links.append({"source": "Root", "target": user_id})

        # B. 結合 XoT：生成衍生思考節點
        # 這是實行 Tracing Creative Thinking 的核心步驟
        xot_results = xot_thought_expansion(raw_feature)
        
        for idx, thought in enumerate(xot_results):
            thought_id = f"{user_id}_T{idx}"
            nodes.append({
                "id": thought_id,
                "label": thought['type'],
                "content": thought['content'],
                "group": 2 # 代表 XoT 衍生節點
            })
            # 將衍生節點與原始人類創意連結
            links.append({"source": user_id, "target": thought_id})

    # 3. 儲存為前端可讀格式
    if not os.path.exists('web'): os.makedirs('web')
    with open('web/data.json', 'w', encoding='utf-8') as f:
        json.dump({"nodes": nodes, "links": links}, f, ensure_ascii=False, indent=4)
    print("✅ XoT 節點鏈接完成！")

if __name__ == "__main__":
    generate_real_nodes()
