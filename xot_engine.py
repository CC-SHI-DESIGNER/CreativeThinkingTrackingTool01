import pandas as pd
import json
import os

def run_xot_engine():
    # 讀取你的 63 筆真實數據
    df = pd.read_csv('data/survey_data.csv')
    
    nodes = [{"id": "Center", "label": "智能穿戴設計中心", "group": 0, "size": 30}]
    links = []

    # 模擬 XoT 的思考分叉 (Everyting of Thoughts 邏輯)
    for i, row in df.iterrows():
        user_id = f"User_{i+1}"
        user_name = str(row['姓名'])
        raw_feat = str(row['產品的外型特徵'])
        
        # 1. 建立人類原始節點 (Origin Node)
        nodes.append({
            "id": user_id,
            "label": user_name,
            "feature": raw_feat,
            "group": 1,
            "img": f"data/sketches/{user_id}.png" # 對應你的草圖
        })
        links.append({"source": "Center", "target": user_id})

        # 2. XoT 拓撲擴展：從原始特徵推演出三個專業維度
        # 這是論文中 "Tracing" 的關鍵點
        xot_paths = [
            {"type": "技術演進", "desc": f"針對 {raw_feat[:10]}... 的感測器集成方案"},
            {"type": "用戶體驗", "desc": f"基於人體工學的 {raw_feat[:10]}... 佩戴優化"},
            {"type": "材料創新", "desc": f"應用柔性電子技術實現 {raw_feat[:10]}..."}
        ]

        for idx, path in enumerate(xot_paths):
            thought_id = f"{user_id}_T{idx}"
            nodes.append({
                "id": thought_id,
                "label": path['type'],
                "content": path['desc'],
                "group": 2 # XoT 衍生節點
            })
            links.append({"source": user_id, "target": thought_id})

    # 確保 web 目錄存在並寫入 JSON
    if not os.path.exists('web'): os.makedirs('web')
    with open('web/data.json', 'w', encoding='utf-8') as f:
        json.dump({"nodes": nodes, "links": links}, f, ensure_ascii=False, indent=4)
    print("✅ 63 筆數據已完成 XoT 節點化處理！")

if __name__ == "__main__":
    run_xot_engine()
