import requests
import re
import json
import html

CHANNEL_NAME = "lmopmopwnzbxjqp192jsmw9m01kanzna"
OUTPUT_FILE = "jan_shakti_live.json"

def scrape_telegram():
    url = f"https://t.me/s/{CHANNEL_NAME}"
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    
    issues = []
    blocks = response.text.split('<div class="tgme_widget_message ')
    
    for block in blocks[1:]:
        if 'js-message_text' not in block: continue
        
        # 1. Capture text while PRESERVING line breaks
        text_match = re.search(r'js-message_text[^>]*>(.*?)</div>', block, re.DOTALL)
        if not text_match: continue
        
        raw_html = text_match.group(1)
        # Convert <br/> tags to actual newlines before stripping other HTML
        formatted_text = raw_html.replace('<br/>', '\n').replace('<br>', '\n')
        clean_text = re.sub(r'<[^>]*>', '', formatted_text)
        # Unescape entities (e.g. &amp; to &)
        final_text = html.unescape(clean_text).strip()
        
        issue = {
            "rawText": final_text,
            "id": "",
            "timestamp": ""
        }
        
        # 2. Extract ID
        id_match = re.search(r'data-post="([^"]+)"', block)
        if id_match: issue["id"] = id_match.group(1)
        
        # 3. Extract Timestamp
        time_match = re.search(r'datetime="([^"]+)"', block)
        if time_match: issue["timestamp"] = time_match.group(1)
        
        issues.append(issue)
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(issues, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    scrape_telegram()
