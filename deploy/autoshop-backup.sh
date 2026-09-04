#!/usr/bin/env bash
# 每天凌晨 2 点备份 MySQL 数据库
# 用法: 放到 /etc/cron.d/autoshop-backup 或 crontab -e:
#   0 2 * * * autoshop bash /opt/autoshop-api/deploy/autoshop-backup.sh
set -euo pipefail

BACKUP_DIR=/var/backups/autoshop
mkdir -p "$BACKUP_DIR"

# 从环境变量或默认值读取
MYSQL_HOST="${MYSQL_HOST:-127.0.0.1}"
MYSQL_PORT="${MYSQL_PORT:-3306}"
MYSQL_USER="${MYSQL_USER:-autoshop}"
MYSQL_PASSWORD="${MYSQL_PASSWORD:-}"
MYSQL_DB="${MYSQL_DB:-autoshop}"

TS=$(date +%Y%m%d_%H%M%S)
DUMP_FILE="$BACKUP_DIR/autoshop-$TS.sql.gz"

if [ -z "$MYSQL_PASSWORD" ]; then
    echo "ERROR: MYSQL_PASSWORD not set"
    exit 1
fi

mysqldump -h "$MYSQL_HOST" \
          -P "$MYSQL_PORT" \
          -u "$MYSQL_USER" \
          -p"$MYSQL_PASSWORD" \
          --single-transaction \
          --routines \
          --triggers \
          --events \
          --default-character-set=utf8mb4 \
          "$MYSQL_DB" \
          | gzip > "$DUMP_FILE"

echo "[backup] saved to $DUMP_FILE ($(du -h "$DUMP_FILE" | cut -f1))"

# 保留 14 天
find "$BACKUP_DIR" -name 'autoshop-*.sql.gz' -mtime +14 -delete
echo "[backup] cleaned backups older than 14 days"
