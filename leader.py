
import json
import os
import urllib.request
import urllib.error

SERVER = "http://127.0.0.1:5000"
TOKEN = os.environ.get("BOT_TOKEN", "")

def main():
    if not TOKEN:
        print("BOT_TOKEN ayarlanmamis!")
        return

    target_id = input("Paylasilacak test hedef ID'si: ").strip()

    if not target_id:
        print("Hedef ID bos olamaz.")
        return

    data = json.dumps({"target_id": target_id}).encode("utf-8")

    req = urllib.request.Request(
        SERVER + "/target",
        data=data,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {TOKEN}"
        },
        method="POST"
    )

    try:
        with urllib.request.urlopen(req) as response:
            print("Sunucu cevabi:", response.read().decode("utf-8"))
    except Exception as e:
        print("Gonderme hatasi:", e)

if __name__ == "__main__":
    main()
