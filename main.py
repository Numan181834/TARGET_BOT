
import json
from pathlib import Path

TARGET_FILE = Path("leader_target.json")


def publish_target(target_id):
    if not target_id:
        print("Hedef seçilmedi.")
        return

    data = {
        "leader_target_id": str(target_id)
    }

    TARGET_FILE.write_text(
        json.dumps(data, indent=4),
        encoding="utf-8"
    )

    print(f"Lider hedefi paylaşıldı: {target_id}")


def main():
    print("TargetBot - Lider Hedef Sistemi")
    target_id = input("Test hedef ID'sini gir: ")
    publish_target(target_id)


if __name__ == "__main__":
    main()
