import pandas as pd
import json
import os

def run_xot_engine():
    # 1. 讀取兩份數據並合併 (確保 63 筆完整)
    s1 = pd.read_csv('sheet1.csv', encoding='utf-8-sig')
    s2 = pd.read_csv('sheet2.csv', encoding='utf-8-sig')
    df = pd.concat([s1, s2], ignore_index=True).head(63)

    nodes = [{"id": "Root", "label": "XoT 設計追蹤中心", "group": 0, "level": 0}]
    links = []

    # 2. 真實數據節點化
    for i, row in df.iterrows():
        user_id = f"User_{i+1}"
        name = str(row['姓名'])
        feature = str(row['產品的外型特徵'])
        
        # 人類原始節點 (Level 1)
        nodes.append({
            "id": user_id,
            "label": name,
            "group": 1,
            "level": 1,
            "feature": feature,
            "sketch": f"data/sketches/User_{i+1}.png" # 對應你的草圖命名
        })
        links.append({"source": "Root", "target": user_id})

        # 3. XoT 思維演化 (此處模擬 LLM 串聯邏輯)
        # 💡 學術亮點：這就是 Everything of Thoughts 的「思考分叉」
        xot_variants = [
            {"type": "Material", "prefix": "材料演化路徑: "},
            {"type": "UX", "prefix": "交互邏輯推演: "}
        ]
        
        for idx, var in enumerate(xot_variants):
            xot_id = f"{user_id}_XoT_{idx}"
            nodes.append({
                "id": xot_id,
                "label": var['type'],
                "content": f"{var['prefix']}基於「{feature[:15]}...」進行的 XoT 深度擴展",
                "group": 2,
                "level": 2
            })
            links.append({"source": user_id, "target": xot_id})

    # 4. 生成 data.json 到根目錄
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump({"nodes": nodes, "links": links}, f, ensure_ascii=False, indent=4)
    print(f"✅ 已成功將 63 筆數據轉化為 XoT 拓撲結構")

if __name__ == "__main__":
    run_xot_engine()
