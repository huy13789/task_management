import requests
import time

URL = "http://localhost:8080/user/test-rate-limit"

def call_api(i):
    try:
        headers = {"x-user-id": "user_vip_1"}
        response = requests.get(URL, headers=headers)
        
        if response.status_code == 200:
            print(f"✅ Lần {i}: Thành công")
        elif response.status_code == 429:
            print(f"⛔ Lần {i}: BỊ CHẶN (429 Too Many Requests)")
        else:
            print(f"⚠️ Lần {i}: Lỗi {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"❌ Lỗi kết nối: {e}")

for i in range(1, 6):
    call_api(i)