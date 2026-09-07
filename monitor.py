import subprocess
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


def write_log():
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cpu = run_command("nproc")
    memory = run_command("free -h | awk '/Mem:/ {print $3 \"/\" $2}'")
    disk = run_command("df / | awk 'NR==2 {print $5}'")
    load = run_command("uptime | awk -F'load average:' '{print $2}'")

    # 去掉磁盘使用率的 %
    disk_number = int(disk.replace("%", ""))

    # 判断系统状态
    if disk_number >= 90:
        status = "CRITICAL - 磁盘空间严重不足"
    elif disk_number >= 80:
        status = "WARNING - 磁盘空间不足"
    else:
        status = "正常"

    with open("monitor.log", "a") as f:
        f.write("=" * 40 + "\n")
        f.write(f"时间：{time_now}\n")
        f.write(f"CPU核心数：{cpu}\n")
        f.write(f"内存使用：{memory}\n")
        f.write(f"磁盘使用率：{disk}\n")
        f.write(f"系统负载：{load}\n")
        f.write(f"状态：{status}\n")
    # 如果异常，写入告警日志
    if disk_number >= 80:
        with open("alert.log", "a") as f:
            f.write(
                f"[{time_now}] {status}，当前使用率：{disk}\n"
            )

while True:
    write_log()
    time.sleep(10)
