#!/usr/bin/env bash
# AutoShop API 一键部署脚本(在目标 Linux 服务器上以 root 执行)
set -euo pipefail

APP_USER=autoshop
APP_DIR=/opt/autoshop-api
SERVICE_NAME=autoshop

echo "==> 1. 创建运行用户"
id -u $APP_USER >/dev/null 2>&1 || useradd -m -s /bin/bash $APP_USER

echo "==> 2. 复制代码到 $APP_DIR"
mkdir -p $APP_DIR
cp -a . $APP_DIR/
chown -R $APP_USER:$APP_USER $APP_DIR

echo "==> 3. 安装依赖"
sudo -iu $APP_USER bash -c "cd $APP_DIR && \
    [ -d .venv ] || python3 -m venv .venv && \
    source .venv/bin/activate && \
    pip install --upgrade pip && \
    pip install -r requirements.txt && \
    pip install 'gunicorn[uvicorn]==21.2.0'"

echo "==> 4. 写入环境变量"
mkdir -p /etc/autoshop
cp deploy/autoshop.env /etc/autoshop/autoshop.env
chmod 600 /etc/autoshop/autoshop.env
chown $APP_USER:$APP_USER /etc/autoshop/autoshop.env
if grep -q CHANGE_ME /etc/autoshop/autoshop.env; then
    echo "!! 请先编辑 /etc/autoshop/autoshop.env,把 SECRET_KEY 改成随机字符串后再启动服务"
fi

echo "==> 5. systemd"
cp deploy/autoshop.service /etc/systemd/system/$SERVICE_NAME.service
systemctl daemon-reload
systemctl enable $SERVICE_NAME || true
systemctl restart $SERVICE_NAME || true

echo "==> 6. nginx(若已安装)"
if command -v nginx >/dev/null 2>&1; then
    cp deploy/nginx-autoshop.conf /etc/nginx/sites-available/autoshop
    ln -sf /etc/nginx/sites-available/autoshop /etc/nginx/sites-enabled/autoshop
    nginx -t && systemctl reload nginx || true
else
    echo "    nginx 未安装,跳过"
fi

echo "==> 7. 健康检查"
sleep 2
curl -fsS http://127.0.0.1:8000/healthz || { echo "健康检查失败,请查看 journalctl -u $SERVICE_NAME"; exit 1; }
echo
echo "✔ Deploy OK"
echo
echo "下一步:"
echo "  - 编辑 /etc/autoshop/autoshop.env,设置 SECRET_KEY"
echo "  - 修改 /etc/nginx/sites-available/autoshop 里的 server_name"
echo "  - sudo certbot --nginx -d api.your-domain.com"
