# AutoShop API 部署指南

## 文件清单

```
deploy/
├── deploy.sh           # 一键部署脚本
├── autoshop.service    # systemd unit
├── autoshop.env        # 环境变量
├── nginx-autoshop.conf # Nginx 反向代理
├── logrotate-autoshop  # 日志切割
├── autoshop.db.backup  # SQLite 备份 cron
├── Dockerfile          # Docker 镜像
├── docker-compose.yml  # 单机编排
└── README.md           # 本文件
```

## 一键部署（systemd + nginx）

```bash
# 1) 上传代码到 /opt/autoshop-api
sudo mkdir -p /opt/autoshop-api
sudo rsync -av --exclude='.venv' --exclude='*.db*' --exclude='__pycache__' \
    ./ /opt/autoshop-api/

# 2) 创建运行用户
sudo useradd -m -s /bin/bash autoshop || true

# 3) 安装依赖
sudo -iu autoshop bash -c "cd /opt/autoshop-api && \
    python3 -m venv .venv && \
    source .venv/bin/activate && \
    pip install -r requirements.txt"

# 4) 写入环境变量
sudo cp deploy/autoshop.env /etc/autoshop/autoshop.env
sudo chmod 600 /etc/autoshop/autoshop.env
sudo chown autoshop:autoshop /etc/autoshop/autoshop.env
# 编辑 /etc/autoshop/autoshop.env,把 SECRET_KEY 改成随机字符串

# 5) systemd
sudo cp deploy/autoshop.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now autoshop
sudo systemctl status autoshop

# 6) nginx
sudo cp deploy/nginx-autoshop.conf /etc/nginx/sites-available/autoshop
sudo ln -sf /etc/nginx/sites-available/autoshop /etc/nginx/sites-enabled/autoshop
# 修改 server_name 为你的域名
sudo nginx -t && sudo systemctl reload nginx

# 7) HTTPS
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d api.your-domain.com

# 8) 日志切割 + 备份 cron
sudo cp deploy/logrotate-autoshop /etc/logrotate.d/autoshop
sudo cp deploy/autoshop.db.backup /etc/cron.d/autoshop-db-backup
```

## 验证

```bash
curl -s http://127.0.0.1:8000/healthz | jq .
curl -s https://api.your-domain.com/healthz | jq .
```

## Docker 部署（可选）

```bash
docker compose -f deploy/docker-compose.yml up -d
docker compose logs -f autoshop
```
