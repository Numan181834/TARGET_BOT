
import json
import os
import urllib.request

SERVER = "http://127.0.0.1:5000"
TOKEN = os.environ.get("BOT_TOKEN", "")

def main():
    if not TOKEN:
        print("BOT_TOKEN ayarlanmamis!")
        return

    req = urllib.request.Request(
        SERVER + "/target",
        headers={"Authorization": f"Bearer {TOKEN}"},
        method="GET"
    )

    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode("utf-8"))

        target_id = data.get("target_id")

        if target_id:
            print("Liderin paylastigi hedef ID:", target_id)
        else:
            print("Henuz hedef paylasilmadi.")

    except Exception as e:
        print("Okuma hatasi:", e)

if __name__ == "__main__":
    main()
