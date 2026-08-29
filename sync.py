import requests
import re
import json

# CONFIGURATION
CHANNEL_NAME = "lmopmopwnzbxjqp192jsmw9m01kanzna"
OUTPUT_FILE = "jan_shakti_live.json"

def scrape_telegram():
    url = f"https://t.me/s/{CHANNEL_NAME}"
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    html = response.text
    
    issues = []
    # Split by message blocks
    blocks = html.split('<div class="tgme_widget_message ')
    
    for block in blocks[1:]:
        if 'js-message_text' not in block: continue
        
        # Extract text content
        text_match = re.search(r'js-message_text[^>]*>(.*?)</div>', block, re.DOTALL)
        if not text_match: continue
        raw_text = re.sub(r'<[^>]*>', '', text_match.group(1)).strip()
        
        issue = {
            "rawText": raw_text,
            "id": "",
            "timestamp": 0
        }
        
        # Extract ID
        id_match = re.search(r'data-post="([^"]+)"', block)
        if id_match: issue["id"] = id_match.group(1)
        
        # Extract Timestamp
        time_match = re.search(r'datetime="([^"]+)"', block)
        if time_match: issue["timestamp"] = time_match.group(1)
        
        issues.append(issue)
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(issues, f, ensure_ascii=False, indent=4)
    print(f"Successfully synced {len(issues)} reports.")

if __name__ == "__main__":
    scrape_telegram()
