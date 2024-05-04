#!/bin/sh
set -x

echo "Starting entrypoint script..."

apt-get update && apt-get install -y cron curl

echo "Installed cron and curl."
echo "Logs:" > /code/cron_output.log

echo "30 15 * * * curl https://edu-news-43e47.duckdns.org/refresh_news/ >> /code/cron_output.log 2>&1
# This extra line makes it a valid cron" > /code/scheduler.txt

echo "Scheduler file created."

crontab /code/scheduler.txt
echo "Crontab updated."

if ! cron -f; then
    echo "Failed to start cron. Exiting."
    exit 1
fi
