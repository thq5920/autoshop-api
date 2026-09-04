#!/usr/bin/env bash
# AutoShop API 一键部署脚本(在目标 Linux 服务器上以 root 执行)
#
# 依赖: MySQL 5.7+ / MariaDB 10.3+, Python 3.12, curl
# 用法: sudo bash deploy/deploy.sh
set -euo pipefail

APP_USER=autoshop
APP_DIR=/opt/autoshop-api
SERVICE_NAME=autoshop

echo "==> 1. 检查 MySQL"
if command -v mysql >/dev/null 2>&1; then
    echo "    MySQL 已安装: $(mysql --version)"
else
    echo "    警告: 未检测到 mysql 命令,请确保 MySQL 已安装并在 PATH 中"
fi

echo "==> 2. 创建 MySQL 数据库和用户(如果不存在)"
DB_NAME="${MYSQL_DB:-autoshop}"
DB_USER="${MYSQL_USER:-autoshop}"
DB_PASS="${MYSQL_PASSWORD:-}"

# 用 root 执行建库建用户,密码通过 MYSQL_ROOT_PASSWORD 环境变量传入
if [ -n "$DB_PASS" ] && command -v mysql >/dev/null 2>&1; then
    mysql -e "CREATE DATABASE IF NOT EXISTS ${DB_NAME} DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;" \
          -u root -p"${MYSQL_ROOT_PASSWORD:-}" 2>/dev/null || \
        echo "    (无法以 root 创建数据库,请手动执行以下 SQL):"
    echo "    CREATE DATABASE IF NOT EXISTS ${DB_NAME} DEFAULT CHARACTER SET utf8mb4;"
    echo "    CREATE USER IF NOT EXISTS '${DB_USER}'@'localhost' IDENTIFIED BY '${DB_PASS}';"
    echo "    CREATE USER IF NOT EXISTS '${DB_USER}'@'%' IDENTIFIED BY '${DB_PASS}';"
    echo "    GRANT ALL PRIVILEGES ON ${DB_NAME}.* TO '${DB_USER}'@'localhost';"
    echo "    GRANT ALL PRIVILEGES ON ${DB_NAME}.* TO '${DB_USER}'@'%';"
    echo "    FLUSH PRIVILEGES;"
fi

echo "==> 3. 创建运行用户"
id -u $APP_USER >/dev/null 2>&1 || useradd -m -s /bin/bash $APP_USER

echo "==> 4. 复制代码到 $APP_DIR"
mkdir -p $APP_DIR
cp -a . $APP_DIR/
chown -R $APP_USER:$APP_USER $APP_DIR

echo "==> 5. 安装依赖"
sudo -iu $APP_USER bash -c "cd $APP_DIR && \
    [ -d .venv ] || python3 -m venv .venv && \
    source .venv/bin/activate && \
    pip install --upgrade pip && \
    pip install -r requirements.txt && \
    pip install 'gunicorn[uvicorn]==21.2.0'"

echo "==> 6. 写入环境变量"
mkdir -p /etc/autoshop
cp deploy/autoshop.env /etc/autoshop/autoshop.env
chmod 600 /etc/autoshop/autoshop.env
chown $APP_USER:$APP_USER /etc/autoshop/autoshop.env
if grep -q CHANGE_ME /etc/autoshop/autoshop.env; then
    echo "!! 请先编辑 /etc/autoshop/autoshop.env,配置 SECRET_KEY 和 MYSQL_PASSWORD"
fi

echo "==> 7. systemd"
cp deploy/autoshop.service /etc/systemd/system/$SERVICE_NAME.service
systemctl daemon-reload
systemctl enable $SERVICE_NAME || true
systemctl restart $SERVICE_NAME || true

echo "==> 8. 备份定时任务(crontab)"
BACKUP_SCRIPT="$APP_DIR/deploy/autoshop-backup.sh"
if [ -f "$BACKUP_SCRIPT" ]; then
    chmod +x "$BACKUP_SCRIPT"
    (crontab -u $APP_USER -l 2>/dev/null | grep -v autoshop-backup.sh; \
     echo "0 2 * * * MYSQL_HOST=${MYSQL_HOST:-127.0.0.1} MYSQL_PORT=${MYSQL_PORT:-3306} MYSQL_USER=${MYSQL_USER:-autoshop} MYSQL_PASSWORD='${MYSQL_PASSWORD:-}' MYSQL_DB=${MYSQL_DB:-autoshop} bash $BACKUP_SCRIPT >> /var/log/autoshop-backup.log 2>&1") \
     | crontab -u $APP_USER - 2>/dev/null || \
    echo "    (无法自动写入 crontab,请手动添加备份任务)"
    echo "    0 2 * * * ... autoshop-backup.sh"
fi

echo "==> 9. nginx(若已安装)"
if command -v nginx >/dev/null 2>&1; then
    cp deploy/nginx-autoshop.conf /etc/nginx/sites-available/autoshop
    ln -sf /etc/nginx/sites-available/autoshop /etc/nginx/sites-enabled/autoshop
    nginx -t && systemctl reload nginx || true
else
    echo "    nginx 未安装,跳过"
fi

echo "==> 10. 健康检查"
sleep 3
curl -fsS http://127.0.0.1:8000/healthz || { echo "健康检查失败,请查看 journalctl -u $SERVICE_NAME"; exit 1; }
echo
echo "✔ Deploy OK"
echo
echo "下一步:"
echo "  - 编辑 /etc/autoshop/autoshop.env,设置 SECRET_KEY 和 MYSQL_PASSWORD"
echo "  - 修改 /etc/nginx/sites-available/autoshop 里的 server_name"
echo "  - sudo certbot --nginx -d api.your-domain.com"
