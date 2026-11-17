
import json
import os
import urllib.request

SERVER = "https://target-bot-dcni.onrender.com"
TOKEN = os.environ.get("BOT_TOKEN", "")


def send_request(path, data):
    body = json.dumps(data).encode("utf-8")

    req = urllib.request.Request(
        SERVER + path,
        data=body,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {TOKEN}"
        },
        method="POST"
    )

    with urllib.request.urlopen(req) as response:
        return response.read().decode("utf-8")


def main():
    if not TOKEN:
        print("BOT_TOKEN ayarlanmamis!")
        return

    try:
        user_id = int(input("Kullanici numaran (1-8): "))

        if not 1 <= user_id <= 8:
            print("Numara 1 ile 8 arasinda olmali.")
            return

        result = send_request("/leader", {"user_id": user_id})
        print("Liderlik cevabi:", result)

        target_id = input("Paylasilacak test hedef ID'si: ").strip()

        if not target_id:
            print("Hedef ID bos olamaz.")
            return

        result = send_request(
            "/target",
            {"user_id": user_id, "target_id": target_id}
        )

        print("Sunucu cevabi:", result)

    except Exception as e:
        print("Hata:", e)


if __name__ == "__main__":
    main()
