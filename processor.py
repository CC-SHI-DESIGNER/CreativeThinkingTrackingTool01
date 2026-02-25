import pandas as pd
import json
import os

def run_xot_processor():
    # 1. 讀取數據 (處理可能存在的編碼問題)
    s1 = pd.read_csv('data/sheet1.csv', encoding='utf-8')
    s2 = pd.read_csv('data/sheet2.csv', encoding='utf-8')
    
    nodes = [{"id": "Root", "label": "智能穿戴設計中心", "group": 0, "level": 0}]
    links = []

    # 2. 整合 63 筆數據 (這裡以 s1 為主表)
    for i in range(len(s1)):
        try:
            name = str(s1.iloc[i]['姓名'])
            feature = str(s1.iloc[i]['產品的外型特徵'])
            items = str(s1.iloc[i]['智能可穿戴產品'])
            
            user_id = f"User_{i+1}"
            
            # 創建人類原始創意節點
            nodes.append({
                "id": user_id,
                "label": name,
                "group": 1,
                "level": 1,
                "details": feature,
                "items": items,
                "sketch": f"data/sketches/{user_id}.png" # 自動關聯圖片路徑
            })
            links.append({"source": "Root", "target": user_id})

            # 3. 執行 XoT 模擬分叉 (核心 SSCI 論點：AI 如何擴展人類創意)
            # 我們針對每個人的特徵，生成兩個 AI 演化節點
            xot_variants = ["功能增強路徑", "材料創新路徑"]
            for idx, variant in enumerate(xot_variants):
                xot_node_id = f"{user_id}_XoT_{idx}"
                nodes.append({
                    "id": xot_node_id,
                    "label": variant,
                    "group": 2,
                    "level": 2,
                    "parent_feat": feature
                })
                links.append({"source": user_id, "target": xot_node_id})
        except:
            continue

    # 4. 輸出 JSON 給前端
    with open('web/data.json', 'w', encoding='utf-8') as f:
        json.dump({"nodes": nodes, "links": links}, f, ensure_ascii=False, indent=4)
    print("✅ XoT 數據節點化完成！")

if __name__ == "__main__":
    if not os.path.exists('web'): os.makedirs('web')
    run_xot_processor()
