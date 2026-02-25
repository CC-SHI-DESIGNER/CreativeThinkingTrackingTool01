import pandas as pd
import json
import os

# 模擬 XoT 的思維演化邏輯 (與微軟 XoT 論文思路一致)
def xot_expand_thoughts(feature_text):
    """
    Everything of Thoughts (XoT) 核心邏輯：
    從一個人類創意點出發，在不同的思考空間（Thought Spaces）進行分叉推演。
    """
    # 在 SSCI 論文中，你可以定義這三個思維維度作為你的 XoT 框架
    thought_spaces = [
        {"type": "Material_Innovation", "logic": "基於材料科學的演化"},
        {"type": "Interaction_Logic", "logic": "基於用戶交互行為的演化"},
        {"type": "Technological_Feasibility", "logic": "基於現有技術路徑的演化"}
    ]
    
    # 這裡未來可以對接 llm_bridge.py 調用真實 LLM
    derived_thoughts = []
    for space in thought_spaces:
        derived_thoughts.append({
            "label": space["type"],
            "content": f"{space['logic']}: 針對 '{feature_text[:10]}...' 的深度推導節點"
        })
    return derived_thoughts

def process_63_data():
    # 讀取數據 (加入 encoding 處理亂碼)
    df = pd.read_csv('data/sheet1.csv', encoding='utf-8-sig')
    
    nodes = [{"id": "Center", "label": "Early-Stage Design Project", "group": 0}]
    links = []

    # 遍歷 63 筆數據
    for i, row in df.iterrows():
        user_id = f"User_{i+1}"
        raw_feature = str(row['產品的外型特徵'])
        
        # 1. 數據節點化：創建「初始人類節點」
        nodes.append({
            "id": user_id,
            "label": str(row['姓名']),
            "feature": raw_feature,
            "group": 1,
            "sketch": f"sketches/User_{i+1}.png"
        })
        links.append({"source": "Center", "target": user_id})

        # 2. 思維演化：執行 XoT 分叉
        # 這是 Tracing 過程的關鍵證據
        xot_nodes = xot_expand_thoughts(raw_feature)
        for idx, thought in enumerate(xot_nodes):
            thought_id = f"{user_id}_T{idx}"
            nodes.append({
                "id": thought_id,
                "label": thought['label'],
                "content": thought['content'],
                "group": 2 # AI 衍生節點
            })
            links.append({"source": user_id, "target": thought_id})

    # 輸出給 D3.js 使用的 JSON
    if not os.path.exists('web'): os.makedirs('web')
    with open('web/data.json', 'w', encoding='utf-8') as f:
        json.dump({"nodes": nodes, "links": links}, f, ensure_ascii=False, indent=4)
    print(f"✅ 成功處理 63 筆數據，已生成 XoT 節點數據庫。")

if __name__ == "__main__":
    process_63_data()
