
import json
import os
import urllib.request

SERVER = "https://target-bot-dcni.onrender.com"
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

        leader_id = data.get("leader_id")
        target_id = data.get("target_id")

        if leader_id:
            print("Mevcut lider: Kisi", leader_id)
        else:
            print("Henuz lider secilmedi.")

        if target_id:
            print("Paylasilan test hedef ID:", target_id)
        else:
            print("Henuz hedef paylasilmadi.")

    except Exception as e:
        print("Okuma hatasi:", e)


if __name__ == "__main__":
    main()
