import argparse
import datetime
import os
import subprocess


def dump_postgres_db(
    host: str,
    port: int,
    dbname: str,
    user: str,
    password: str,
    output_dir: str,
    include_data: bool = False,
):
    # 1. 根据是否包含数据，生成不同的文件名前缀和时间戳
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    mode_str = "full" if include_data else "schema_only"
    output_filename = f"{dbname}_{mode_str}_{timestamp}.sql"
    output_filepath = os.path.join(output_dir, output_filename)

    # 2. 设置环境变量传递密码，避免交互式输入
    env = os.environ.copy()
    env["PGPASSWORD"] = password

    # 3. 构建 pg_dump 基础命令
    # -F p: 输出为纯文本的 SQL 脚本
    command = ["pg_dump", "-h", host, "-p", str(port), "-U", user, "-d", dbname, "-F", "p", "-f", output_filepath]

    # 🌟 核心逻辑：如果不包含数据，追加 --schema-only 参数
    if not include_data:
        command.append("--schema-only")
    else:
        # 如果包含数据，使用 --inserts 生成 INSERT 语句而不是 COPY，兼容性更好
        command.append("--inserts")

    print(f"🚀 开始导出数据库 '{dbname}'...")
    print(f"📦 导出模式: {'表结构 + 数据' if include_data else '仅表结构 (默认)'}")
    print(f"📂 目标文件: {output_filepath}")

    try:
        # 4. 执行命令
        subprocess.run(command, env=env, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print("✅ 导出成功！")

    except subprocess.CalledProcessError as e:
        print("❌ 导出失败！")
        print(f"错误信息:\n{e.stderr}")
    except FileNotFoundError:
        print("❌ 找不到 'pg_dump' 命令。请确保已安装 PostgreSQL 客户端并配置了环境变量。")
    finally:
        # 清理环境变量中的密码，保证安全性
        if "PGPASSWORD" in env:
            del env["PGPASSWORD"]


# ==========================================
# 使用示例 (支持直接运行或命令行传参)
# ==========================================
if __name__ == "__main__":
    DB_HOST = "127.0.0.1"
    DB_PORT = 5432
    DB_NAME = "demo1"
    DB_USER = "postgres"
    DB_PASS = "postgres"
    OUTPUT_DIR = "."

    parser = argparse.ArgumentParser(description="PostgreSQL 数据库导出脚本")
    parser.add_argument("--with-data", action="store_true", help="导出表结构的同时包含数据")

    args = parser.parse_args()

    # 执行导出函数
    dump_postgres_db(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        output_dir=OUTPUT_DIR,
        include_data=args.with_data,  # 默认为 False，如果传入了 --with-data，这里就是 True
    )
