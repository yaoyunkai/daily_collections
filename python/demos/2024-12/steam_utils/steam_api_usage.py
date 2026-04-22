"""

Steam API


steamBD search
    根据类型区分
    是否在库中 ??? 不做强制要求
    是否有parent app id

"""

import configparser
import json
from datetime import datetime

import openpyxl
import requests

API_KEY = "---"
STEAM_ID = "---"
LANGUAGE_PARAM = "schinese"


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


def get_owned_games():
    url = "https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/"

    payload = {
        "key": API_KEY,
        "steamid": STEAM_ID,
        "include_appinfo": True,
        "include_played_free_games": True,
        "include_free_sub": True,
        "language": "schinese",
    }

    try:
        response = requests.get(url, params=payload)
        response.raise_for_status()
        data = response.json()
        # pprint.pprint(data)
        save_to_excel(data["response"]["games"])

    except Exception as e:
        print(f"请求 API 时发生错误: {e}")


def save_to_excel(games_list, filename="游戏时长.xlsx"):
    """
    步骤 2: 将游戏数据清洗并写入 Excel 文件
    """
    if not games_list:
        print("没有数据可写入 Excel。")
        return

    print(f"正在生成 Excel 文件: {filename} ...")

    # 创建一个新的 Excel 工作簿和活动的工作表
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "我的 Steam 游戏库"

    # 写入表头 (Header)
    headers = ["App ID", "游戏名称", "总游玩时间 (小时)", "最后运行时间"]
    sheet.append(headers)

    # 遍历游戏列表，处理数据并写入行
    for game in games_list:
        app_id = game.get("appid", "")
        name = game.get("name", "未知游戏")

        # 将分钟转换为小时，保留两位小数
        playtime_minutes = game.get("playtime_forever", 0)
        playtime_hours = round(playtime_minutes / 60, 2)

        # 处理时间戳
        last_played_timestamp = game.get("rtime_last_played", 0)
        if last_played_timestamp > 0:
            # 将 Unix 时间戳转换为本地时间字符串
            last_played_date = datetime.fromtimestamp(last_played_timestamp).strftime("%Y-%m-%d %H:%M:%S")
        else:
            last_played_date = "从未运行"

        # 将这一行数据追加到 Excel 表格中
        row_data = [app_id, name, playtime_hours, last_played_date]
        sheet.append(row_data)

    # 调整列宽以提高可读性 (可选优化)
    sheet.column_dimensions["A"].width = 12  # App ID 列
    sheet.column_dimensions["B"].width = 40  # 游戏名称列
    sheet.column_dimensions["C"].width = 20  # 游玩时间列
    sheet.column_dimensions["D"].width = 25  # 最后运行时间列

    # 保存文件
    try:
        workbook.save(filename)
        print(f"✅ 导出成功！文件已保存至当前目录: {filename}")
    except PermissionError:
        print(f"❌ 保存失败：文件 '{filename}' 可能正在被其他程序（如 Excel）占用，请关闭后重试。")


def get_specific_app_info(app_id):
    """
    请求 Steam API 并提取指定的 App 信息
    """
    url = "https://store.steampowered.com/api/appdetails"

    params = {"appids": app_id, "l": LANGUAGE_PARAM}

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        json_data = response.json()

        # 检查数据是否有效
        if str(app_id) not in json_data or not json_data[str(app_id)]["success"]:
            return {"error": f"无法获取 App ID {app_id} 的信息"}

        raw_data = json_data[str(app_id)]["data"]

        # ------------------------------------------------
        # 数据解析与提取逻辑
        # ------------------------------------------------

        # 1. 解析 Steam 云和成就系统 (遍历 categories)
        supports_cloud = False
        has_achievements = False
        categories = raw_data.get("categories", [])
        for category in categories:
            if category.get("id") == 23:  # 23 代表 Steam Cloud
                supports_cloud = True
            elif category.get("id") == 22:  # 22 代表 Steam Achievements
                has_achievements = True

        # 2. 解析官方类型 (Genres) 以替代玩家标签 (Tags)
        genres_list = [genre.get("description") for genre in raw_data.get("genres", [])]

        # 3. 解析支持的操作系统
        platforms = raw_data.get("platforms", {})
        supported_os = [os_name for os_name, is_supported in platforms.items() if is_supported]

        # 4. 构建目标数据字典
        extracted_info = {
            "app_id": app_id,
            "name": raw_data.get("name", "未知"),
            "app_type": raw_data.get("type", "未知"),
            "developers": raw_data.get("developers", []),
            "publishers": raw_data.get("publishers", []),
            "supported_os": supported_os,
            "release_date": raw_data.get("release_date", {}).get("date", "未知"),
            "last_update_time": "API不支持获取此数据",  # API 限制说明
            "short_description": raw_data.get("short_description", ""),
            "genres_as_tags": genres_list,
            "supported_languages": raw_data.get("supported_languages", ""),
            "features": {"supports_steam_cloud": supports_cloud, "has_achievements": has_achievements},
        }

        return extracted_info

    except requests.exceptions.RequestException as e:
        return {"error": f"网络请求失败: {e}"}


if __name__ == "__main__":
    get_owned_games()
