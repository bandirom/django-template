#!/bin/sh

FILE="$HOME/celerybeat.pid"

if [ -f "$FILE" ]; then
    echo "Clean PID file"
    rm "$FILE"
fi

celery -A application beat -l info
