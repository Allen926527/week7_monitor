#!/bin/bash

PROJECT_DIR="$HOME/linux_practice/week7_monitor"
PYTHON="$PROJECT_DIR/.venv/bin/python"
SCRIPT="$PROJECT_DIR/monitor.py"

cd "$PROJECT_DIR" || exit 1

case "$1" in
    start)
        "$PYTHON" "$SCRIPT" start
        ;;

    stop)
        "$PYTHON" "$SCRIPT" stop
        ;;

    status)
        "$PYTHON" "$SCRIPT" status
        ;;

    check)
        "$PYTHON" "$SCRIPT" check
        ;;

    report)
        "$PYTHON" "$SCRIPT" report
        ;;

    logs)
        "$PYTHON" "$SCRIPT" logs
        ;;

    *)
        echo "Linux Monitor"
        echo ""
        echo "用法："
        echo "./monitor.sh start"
        echo "./monitor.sh stop"
        echo "./monitor.sh status"
        echo "./monitor.sh check"
        echo "./monitor.sh report"
        echo "./monitor.sh logs"
        ;;
esac
