"""

Steam API


steamBD search
    根据类型区分
    是否在库中 ??? 不做强制要求
    是否有parent app id

"""

import configparser
import json

import requests

API_KEY = "---"
STEAM_ID = "---"


def _load_app_secure_key():
    global API_KEY, STEAM_ID
    config = configparser.ConfigParser()
    config.read("personal.ini", encoding="utf8")

    if "steam" not in config.sections():
        raise SystemExit("no such config")

    steam_item = config["steam"]
    API_KEY = steam_item.get("api_key", "")
    STEAM_ID = steam_item.get("steam_id", "")


_load_app_secure_key()


def get_player_summary(steam_id=None):
    url = "https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/"
    if not steam_id:
        steam_id = STEAM_ID

    payload = {
        "key": API_KEY,
        "steamids": steam_id,
    }

    try:
        response = requests.get(url, params=payload)
        response.raise_for_status()
        data = response.json()
        players = data.get("response", {}).get("players", [])
        if not players:
            print("未找到该 Steam ID 的信息，请检查 ID 是否正确。")
            return
        my_info = players[0]

        print("=== Steam 个人信息 ===")
        print(f"昵称 (Persona Name): {my_info.get('personaname')}")
        print(f"Steam ID: {my_info.get('steamid')}")
        print(f"个人主页: {my_info.get('profileurl')}")
        print(f"头像 URL: {my_info.get('avatarfull')}")

        state_map = {
            0: "离线 (Offline)",
            1: "在线 (Online)",
            2: "忙碌 (Busy)",
            3: "离开 (Away)",
            4: "离开很久 (Snooze)",
            5: "准备交易 (Looking to trade)",
            6: "准备开玩 (Looking to play)",
        }
        persona_state = my_info.get("personastate", 0)
        print(f"当前状态: {state_map.get(persona_state, '未知')}")

        visibility = my_info.get("communityvisibilitystate")
        if visibility == 3:
            print("资料隐私: 公开 (Public)")
            if "gameextrainfo" in my_info:
                print(f"正在游玩: {my_info.get('gameextrainfo')}")
        else:
            print("资料隐私: 私密或仅好友可见 (Private / Friends Only)")

        print("\n=== 完整 JSON 数据 ===")
        print(json.dumps(my_info, indent=4, ensure_ascii=False))

    except requests.exceptions.RequestException as e:
        print(f"请求 API 时发生错误: {e}")


if __name__ == "__main__":
    get_player_summary()
