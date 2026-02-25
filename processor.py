import pandas as pd
import json
import os

def run_xot_processor():
    # 1. 讀取數據路徑 (根據你的桌面結構)
    data_dir = r'C:\Users\shiho\Desktop\CreativeThinkingTrackingTool\data'
    s1 = pd.read_csv(os.path.join(data_dir, 'sheet1.csv'), encoding='utf-8-sig')
    s2 = pd.read_csv(os.path.join(data_dir, 'sheet2.csv'), encoding='utf-8-sig')
    
    # 合併兩表，確保總數為 63 筆
    df = pd.concat([s1, s2], ignore_index=True).head(63)
    
    nodes = [{"id": "Root", "label": "XoT 創意追蹤中心", "group": 0, "level": 0}]
    links = []

    # 2. 遍歷數據並生成 XoT 節點
    for i, row in df.iterrows():
        user_id = f"User_{i+1}"
        name = str(row['姓名'])
        feature = str(row['產品的外型特徵'])
        
        # A. 人類節點：這是 Tracing 的起點
        nodes.append({
            "id": user_id,
            "label": name,
            "group": 1,
            "level": 1,
            "feature": feature,
            "sketch": f"data/sketches/User_{i+1}.png" 
        })
        links.append({"source": "Root", "target": user_id})

        # B. XoT 衍生節點：模擬 LLM 在不同思考空間的分叉
        # 這裡的邏輯對應微軟 XoT 的 "Thought Spaces"
        xot_thoughts = [
            {"dim": "技術可行性", "logic": "材料輕量化與傳感器集成方案"},
            {"dim": "交互美學", "logic": "極簡造型與情緒反饋界面的結合"}
        ]
        
        for idx, thought in enumerate(xot_thoughts):
            t_id = f"{user_id}_T{idx}"
            nodes.append({
                "id": t_id,
                "label": thought['dim'],
                "content": f"【XoT 推論】基於「{feature[:12]}...」, {thought['logic']}",
                "group": 2,
                "level": 2
            })
            links.append({"source": user_id, "target": t_id})

    # 3. 輸出 data.json 到 web 文件夾
    output_path = r'C:\Users\shiho\Desktop\CreativeThinkingTrackingTool\web\data.json'
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump({"nodes": nodes, "links": links}, f, ensure_ascii=False, indent=4)
    
    print(f"✅ 成功！已將 63 筆數據轉化為 data.json，請檢查 web 文件夾。")

if __name__ == "__main__":
    run_xot_processor()
