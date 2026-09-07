import subprocess
import sys
import time
from datetime import datetime


def run_command(command):
    result = subprocess.run(
        command,
        shell=True,
        capture_output=True,
        text=True
    )
    return result.stdout.strip()


def check_system():
    cpu = int(run_command("nproc"))

    memory = int(run_command(
        "free -m | awk '/Mem:/ {print int($3/$2*100)}'"
    ))

    disk = int(run_command(
        "df / | awk 'NR==2 {print $5}'"
    ).replace("%", ""))

    load = float(run_command(
        "uptime | awk -F'load average:' '{print $2}' | cut -d, -f1"
    ).strip())

    if load >= cpu:
        cpu_status = "WARNING"
        cpu_score = 60
    else:
        cpu_status = "正常"
        cpu_score = 100

    if memory >= 90:
        memory_status = "CRITICAL"
        memory_score = 40
    elif memory >= 80:
        memory_status = "WARNING"
        memory_score = 70
    else:
        memory_status = "正常"
        memory_score = 100

    if disk >= 90:
        disk_status = "CRITICAL"
        disk_score = 40
    elif disk >= 80:
        disk_status = "WARNING"
        disk_score = 70
    else:
        disk_status = "正常"
        disk_score = 100

    score = int(
        (cpu_score + memory_score + disk_score) / 3
    )

    if score >= 90:
        system_status = "HEALTHY"
    elif score >= 70:
        system_status = "WARNING"
    else:
        system_status = "CRITICAL"

    return {
        "cpu": cpu,
        "memory": memory,
        "disk": disk,
        "load": load,
        "cpu_status": cpu_status,
        "memory_status": memory_status,
        "disk_status": disk_status,
        "score": score,
        "system_status": system_status
    }


def show_check():
    data = check_system()

    print("=" * 45)
    print("        Linux 系统健康检查")
    print("=" * 45)

    print(f"CPU核心数：{data['cpu']}")
    print(f"CPU状态：{data['cpu_status']}")

    print(f"内存使用率：{data['memory']}%")
    print(f"内存状态：{data['memory_status']}")

    print(f"磁盘使用率：{data['disk']}%")
    print(f"磁盘状态：{data['disk_status']}")

    print(f"系统负载：{data['load']}")

    print("-" * 45)
    print(f"综合评分：{data['score']}/100")
    print(f"系统状态：{data['system_status']}")
    print("=" * 45)


def write_report():
    data = check_system()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open("monitor.log", "a") as f:
        f.write("=" * 45 + "\n")
        f.write(f"时间：{now}\n")
        f.write(f"CPU核心数：{data['cpu']}\n")
        f.write(f"CPU状态：{data['cpu_status']}\n")
        f.write(f"内存使用率：{data['memory']}%\n")
        f.write(f"内存状态：{data['memory_status']}\n")
        f.write(f"磁盘使用率：{data['disk']}%\n")
        f.write(f"磁盘状态：{data['disk_status']}\n")
        f.write(f"系统负载：{data['load']}\n")
        f.write(f"综合评分：{data['score']}/100\n")
        f.write(f"系统状态：{data['system_status']}\n")


def show_logs():
    subprocess.run(
        ["tail", "-20", "monitor.log"]
    )


def show_help():
    print("""
Linux Monitor

使用方法：

python monitor.py check
    查看当前系统状态

python monitor.py report
    执行一次监控并写入日志

python monitor.py logs
    查看最近20条日志

python monitor.py start
    持续监控，每10秒记录一次

python monitor.py help
    查看帮助
""")


def start_monitor():
    print("监控程序启动...")
    print("每10秒检查一次")
    print("按 Ctrl+C 停止")

    try:
        while True:
            write_report()
            print(
                f"[{datetime.now().strftime('%H:%M:%S')}] "
                "监控完成"
            )
            time.sleep(10)

    except KeyboardInterrupt:
        print("\n监控程序已停止")


def main():
    if len(sys.argv) < 2:
        show_help()
        return

    command = sys.argv[1]

    if command == "check":
        show_check()

    elif command == "report":
        write_report()
        print("监控报告已写入 monitor.log")

    elif command == "logs":
        show_logs()

    elif command == "start":
        start_monitor()

    elif command == "help":
        show_help()

    else:
        print(f"未知命令：{command}")
        print("使用 python monitor.py help 查看帮助")


if __name__ == "__main__":
    main()
