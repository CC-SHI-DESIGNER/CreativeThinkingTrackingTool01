import pandas as pd
import json
import os

def run_xot_engine():
    # 讀取 CSV (請確保檔案名稱正確)
    # 我們合併兩張表的數據，這裡以 Sheet1 為主
    try:
        df = pd.read_csv('data/sheet1.csv', encoding='utf-8')
    except:
        df = pd.read_csv('data/sheet1.csv', encoding='gbk')
    
    nodes = [{"id": "Root", "label": "XoT 設計中心", "group": 0, "size": 30}]
    links = []

    # 遍歷 63 筆數據
    for i in range(len(df)):
        user_id = f"User_{i+1}"
        # 提取真實數據欄位
        name = str(df.iloc[i]['姓名'])
        feature = str(df.iloc[i]['產品的外型特徵'])
        items = str(df.iloc[i]['智能可穿戴產品'])
        
        # 1. 建立「人類原始創意節點」
        nodes.append({
            "id": user_id,
            "label": name,
            "group": 1,
            "feature": feature,
            "items": items,
            "sketch": f"../sketches/{user_id}.png" # 指向圖片路徑
        })
        links.append({"source": "Root", "target": user_id})

        # 2. XoT 思維分叉：模擬大模型基於該創意的推導
        # 分叉 A：技術可行性推導
        xot_a = f"{user_id}_XA"
        nodes.append({
            "id": xot_a,
            "label": "技術演化",
            "content": f"針對「{feature[:15]}...」的傳感器模組化設計方案。",
            "group": 2
        })
        links.append({"source": user_id, "target": xot_a})

        # 分叉 B：設計優化推導
        xot_b = f"{user_id}_XB"
        nodes.append({
            "id": xot_b,
            "label": "體驗優化",
            "content": f"利用 XoT 框架優化的「{items.split('、')[0]}」佩戴舒適度路徑。",
            "group": 2
        })
        links.append({"source": user_id, "target": xot_b})

    # 確保輸出目錄存在
    if not os.path.exists('web'): os.makedirs('web')
    with open('web/data.json', 'w', encoding='utf-8') as f:
        json.dump({"nodes": nodes, "links": links}, f, ensure_ascii=False, indent=4)
    print("✅ 成功：63 筆數據已轉化為 XoT 拓撲 JSON。")

if __name__ == "__main__":
    run_xot_engine()
