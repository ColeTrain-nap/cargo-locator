import requests
from bs4 import BeautifulSoup
import json
import time

# 後で増やせるようにリスト形式にしておきます
TARGET_TRAINS = ["2059"]

def scrap_loco_info(train_no):
    # 貨物ちゃんねるの運用情報ページ（例）
    url = f"https://kamo.apreed.com/unyo.html" 
    
    try:
        # 相手サーバーへのマナー：1秒待機
        time.sleep(1)
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        response.encoding = response.apparent_encoding
        soup = BeautifulSoup(response.text, 'html.parser')

        # ページ内から列車番号を探す（ここはサイトの構造に合わせて微調整が必要）
        # 仮のロジック：テキストの中から列車番号の次に来る機番（EF210-xxx等）を探す
        content = soup.get_text()
        if train_no in content:
            import re
            # EF210-123 や EF66-100 などのパターンを抽出
            match = re.search(r'EF[0-9]{2,3}-[0-9]+', content)
            if match:
                return match.group()
        return "不明"
    except Exception as e:
        return f"Error: {e}"

# メイン処理
results = {}
for train in TARGET_TRAINS:
    loco = scrap_loco_info(train)
    results[train] = loco

# GitHubに保存するためのJSONファイル作成
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=4)

print("データ更新完了:", results)