# AutoShop API

专门用于接口自动化测试练习的 Mock 商城 API。

完整实现了一份 13 个接口的 RESTful 服务，统一返回格式、Bearer Token 鉴权、Mock 支付可控（SUCCESS / FAIL / PENDING），自带种子数据覆盖正常 / 库存不足 / 下架 / 不存在 四类商品场景。

---

## 一、技术栈

- Python 3.12 / FastAPI 0.115
- SQLAlchemy 2.0 + **MySQL 8.0**（驱动: PyMySQL）
- PyJWT + Passlib(bcrypt)
- Pydantic v2
- Swagger UI 自动生成于 `/docs`

---

## 二、目录结构

```
AutoShop API/
├── app/
│   ├── main.py              # FastAPI 入口
│   ├── config.py            # 配置(含 MySQL 连接参数)
│   ├── database.py          # SQLAlchemy engine / Session（含 reset_db）
│   ├── deps.py              # get_current_user 依赖
│   ├── security.py          # JWT + bcrypt
│   ├── response.py          # 标准响应信封
│   ├── exceptions.py        # BizException + 统一处理
│   ├── seed.py              # 种子数据
│   ├── models/              # ORM 模型（无 FOREIGN KEY，仅业务逻辑关联）
│   ├── schemas/             # Pydantic 模型
│   ├── routers/             # 5 个路由模块
│   └── services/            # 业务层
├── scripts/                 # 数据库脚本（建表/重置/删除外键）
├── tests/                   # pytest 自动化测试
├── deploy/                  # 部署文件
├── requirements.txt
└── README.md
```

### 数据库设计说明

**本项目不使用 MySQL FOREIGN KEY 外键约束。** 逻辑关联字段（user_id / product_id / order_id）由应用层业务代码保证数据完整性，各表均可独立 TRUNCATE / DELETE，互不干扰，适合接口自动化测试场景。

| 数据库脚本 | 说明 |
|---|---|
| `scripts/schema.sql` | 完整建表 SQL（无外键，带中文注释） |
| `scripts/reset_database.sql` | 测试前重置数据库（TRUNCATE + 种子数据） |
| `scripts/remove_foreign_keys.sql` | 删除现有数据库中的所有外键约束 |

---

## 三、MySQL 环境准备

### 3.1 本地已有 MySQL

创建数据库和用户（一条 SQL 搞定）：

```sql
CREATE DATABASE IF NOT EXISTS autoshop DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER IF NOT EXISTS 'autoshop'@'localhost' IDENTIFIED BY 'YourStrongPassword123';
CREATE USER IF NOT EXISTS 'autoshop'@'%' IDENTIFIED BY 'YourStrongPassword123';
GRANT ALL PRIVILEGES ON autoshop.* TO 'autoshop'@'localhost';
GRANT ALL PRIVILEGES ON autoshop.* TO 'autoshop'@'%';
FLUSH PRIVILEGES;
```

### 3.2 用 Docker 快速起 MySQL

```bash
# 方式 A:直接起 MySQL 容器(推荐开发用)
docker run -d \
  --name autoshop-mysql \
  -e MYSQL_ROOT_PASSWORD=rootpw \
  -e MYSQL_DATABASE=autoshop \
  -e MYSQL_USER=autoshop \
  -e MYSQL_PASSWORD=autoshoppw \
  -p 3306:3306 \
  -v autoshop_mysql_data:/var/lib/mysql \
  mysql:8.0 \
  --character-set-server=utf8mb4 \
  --collation-server=utf8mb4_unicode_ci
```

```bash
# 方式 B:用 docker-compose 一键起 MySQL + API
cd deploy
cp ../.env.example .env
# 编辑 .env 填好 MYSQL_PASSWORD 等
docker-compose up -d
```

---

## 四、本地启动

```bash
cd "AutoShop API"

# 1. 配置环境变量(开发用)
cp .env.example .env
# 编辑 .env 填入:
#   MYSQL_HOST=127.0.0.1
#   MYSQL_PORT=3306
#   MYSQL_USER=autoshop
#   MYSQL_PASSWORD=你的密码
#   MYSQL_DB=autoshop

# 2. 推荐用虚拟环境
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 3. 启动(首次启动自动建表并插入种子数据)
uvicorn app.main:app --reload --port 8000
# 或生产模式
gunicorn app.main:app -k uvicorn.workers.UvicornWorker -w 2 -b 127.0.0.1:8000
```

打开浏览器：

- Swagger UI：<http://localhost:8000/docs>
- ReDoc：<http://localhost:8000/redoc>
- 健康检查：<http://localhost:8000/healthz>

---

## 五、接口清单（13 个）

```
认证
POST    /api/v1/auth/register
POST    /api/v1/auth/login

商品
GET     /api/v1/products
GET     /api/v1/products/{productId}

购物车
GET     /api/v1/cart
POST    /api/v1/cart/items
PUT     /api/v1/cart/items/{cartItemId}
DELETE  /api/v1/cart/items/{cartItemId}

订单
POST    /api/v1/orders
GET     /api/v1/orders
GET     /api/v1/orders/{orderId}

个人中心
GET     /api/v1/users/me
PUT     /api/v1/users/me

测试用(仅 DEBUG=true 时可用)
POST    /api/v1/_test/reset
```

---

## 六、统一响应信封

```json
{
  "code": 200,
  "message": "成功",
  "data": { ... },
  "timestamp": 1787886000000,
  "requestId": "req_xxx"
}
```

- `message` 默认走中文(zh-CN),可通过请求头 `Accept-Language: en-US` 切英文
- 也支持查询参数 `?lang=zh-CN` / `?lang=en-US` 覆盖

### 业务码表

**编码规则:** 五位数 `XABCD` —— `X` 为大类(2 成功 / 4 客户端 / 5 服务端),`AB` 为模块,`CD` 为具体错误序号

| code    | 模块           | 中文含义                       | HTTP |
|---------|----------------|--------------------------------|------|
| 200     | -              | 成功                           | 200  |
| 40001   | 通用           | 参数格式错误                   | 422  |
| 40002   | 通用           | 必填参数缺失                   | 400  |
| 40003   | 通用           | 参数超出允许范围               | 400  |
| 40101   | 认证           | 未登录或登录已失效             | 401  |
| 40102   | 认证           | 登录凭证无效                   | 401  |
| 40103   | 认证           | 登录凭证已过期                 | 401  |
| 40104   | 认证           | 无权访问该资源                 | 403  |
| 40105   | 认证           | 账号已被禁用                   | 403  |
| 40201   | 账号密码格式   | 用户名格式不正确               | 422  |
| 40202   | 账号密码格式   | 用户名过短                     | 422  |
| 40203   | 账号密码格式   | 用户名过长                     | 422  |
| 40204   | 账号密码格式   | 密码格式不正确                 | 422  |
| 40205   | 账号密码格式   | 密码过短                       | 422  |
| 40206   | 账号密码格式   | 密码过长                       | 422  |
| 40207   | 账号密码格式   | 邮箱格式不正确                 | 422  |
| 40208   | 账号密码格式   | 邮箱过长                       | 422  |
| 40209   | 账号密码格式   | 手机号格式不正确               | 422  |
| 40210   | 账号密码格式   | 昵称过长                       | 422  |
| 40301   | 注册/登录业务  | 账号不存在(仅 DEBUG 暴露)     | 401  |
| 40302   | 注册/登录业务  | 密码错误(仅 DEBUG 暴露)       | 401  |
| 40303   | 注册/登录业务  | 用户名或密码错误(默认对外)    | 401  |
| 40401   | 用户资料       | 用户不存在                     | 404  |
| 40402   | 用户资料       | 资料无任何更新                 | 400  |
| 40501   | 商品           | 商品不存在                     | 404  |
| 40502   | 商品           | 商品已下架                     | 400  |
| 40503   | 商品           | 库存不足                       | 400  |
| 40504   | 商品           | 购买数量不合法                 | 400  |
| 40601   | 购物车         | 购物车项不存在                 | 404  |
| 40602   | 购物车         | 购物车为空                     | 400  |
| 40701   | 订单           | 订单不存在                     | 404  |
| 40702   | 订单           | 订单状态不允许此操作           | 400  |
| 40703   | 订单           | 支付失败                       | 400  |
| 40901   | 冲突           | 用户名已被占用                 | 409  |
| 40902   | 冲突           | 邮箱已被注册                   | 409  |
| 40903   | 冲突           | 手机号已被注册                 | 409  |
| 50001   | 系统           | 系统繁忙,请稍后再试           | 500  |
| 50002   | 系统           | 数据库异常                     | 500  |
| 50301   | 系统           | 服务暂不可用                   | 503  |

> **关于 40301 / 40302 / 40303:** 生产环境(prod)统一对外返回 `40303 用户名或密码错误` 防账号枚举;`AUTOSHOP_EXPOSE_AUTH_DETAIL=true`(默认 / 测试)时,会精确返回 `40301 账号不存在` 或 `40302 密码错误`,便于接口测试断言。

---

## 七、种子数据

### 商品（自动初始化）

| productId | name                  | price   | stock | status    |
|-----------|-----------------------|---------|-------|-----------|
| 1001      | iPhone 17             | 5999.00 | 100   | ON_SALE   |
| 1002      | MacBook Air           | 7999.00 | 50    | ON_SALE   |
| 1003      | AirPods               | 999.00  | 0     | ON_SALE   |
| 1004      | Test Offline Product  | 100.00  | 10    | OFF_SHELF |

### demo 用户（仅本地调试）

```
username: demo
password: Demo@123456
```

---

## 八、Mock 下单控制

```json
POST /api/v1/orders
{
  "cartItemIds": [80001],
  "receiver": { "name":"张三", "phone":"13800138000", "address":"..." },
  "remark": "...",
  "mockResult": "SUCCESS"   // SUCCESS | FAIL | PENDING
}
```

| mockResult | orderStatus        | paymentStatus  |
|------------|--------------------|----------------|
| SUCCESS    | PAID               | MOCK_SUCCESS   |
| FAIL       | PAY_FAILED         | MOCK_FAILED    |
| PENDING    | PENDING_PAYMENT    | MOCK_PENDING   |

---

## 九、核心链路示例

```bash
BASE=http://localhost:8000/api/v1

# 1. 注册
curl -s -X POST $BASE/auth/register -H 'Content-Type: application/json' \
  -d '{"username":"test001","password":"Test@123456","email":"t1@x.com","phone":"13800138000"}'

# 2. 登录
TOKEN=$(curl -s -X POST $BASE/auth/login -H 'Content-Type: application/json' \
  -d '{"username":"test001","password":"Test@123456"}' | jq -r '.data.accessToken')

# 3. 查询商品
curl -s $BASE/products

# 4. 加入购物车
curl -s -X POST $BASE/cart/items -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json' -d '{"productId":1001,"quantity":2}'

# 5. Mock 下单
curl -s -X POST $BASE/orders -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{"cartItemIds":[80001],"receiver":{"name":"张三","phone":"13800138000","address":"..."},"mockResult":"SUCCESS"}'

# 6. 个人中心
curl -s $BASE/users/me -H "Authorization: Bearer $TOKEN"

# 7. 重置数据(测试用)
curl -s -X POST $BASE/_test/reset
```

---

## 十、自动化测试

```bash
cd tests
pip install -r requirements-test.txt
pytest -v --html=report.html --self-contained-html
```

覆盖：

- 业务链路一条龙（注册→登录→加车→下单→订单→个人中心）
- 13 个接口的正向 + 反向用例
- 订单三种 Mock 结果的参数化
- JSON Schema 校验

---

## 十一、环境变量

| 变量名             | 默认值                          | 说明                          |
|--------------------|---------------------------------|-------------------------------|
| `AUTOSHOP_ENV`     | `dev`                           | dev / prod                    |
| `AUTOSHOP_DEBUG`   | `true`                          | 是否启用 `_test/reset`        |
| `AUTOSHOP_EXPOSE_AUTH_DETAIL` | `true`               | 是否在登录失败时返回具体原因(40301/40302);prod 建议 `false` 切到 40303 模糊提示 |
| `SECRET_KEY`       | 开发用默认值（**请改**）        | JWT 签名密钥                  |
| `MYSQL_HOST`       | `127.0.0.1`                     | MySQL 主机地址                |
| `MYSQL_PORT`       | `3306`                          | MySQL 端口                    |
| `MYSQL_USER`       | `autoshop`                      | MySQL 用户名                  |
| `MYSQL_PASSWORD`   | `autoshop`                      | MySQL 密码                    |
| `MYSQL_DB`         | `autoshop`                      | 数据库名                      |
| `MYSQL_CHARSET`    | `utf8mb4`                       | 字符集                        |
| `BCRYPT_ROUNDS`    | `4`                             | bcrypt 计算轮数（测试用 4）   |

---

## 十二、Linux 部署（完整步骤）

### 前置依赖

- 一台 Linux 服务器（Ubuntu 22.04 / Debian 12 / CentOS 8+）
- 已安装 MySQL 5.7+ 或 MariaDB 10.3+
- Python 3.12（建议用 `pyenv` 或系统包管理安装）
- `curl`、`git`

### 12.1 安装 MySQL（如果没有）

```bash
# Ubuntu / Debian
sudo apt update && sudo apt install -y mysql-server
sudo systemctl enable --now mysql

# CentOS / AlmaLinux
sudo dnf install -y mysql-server
sudo systemctl enable --now mysqld
```

### 12.2 创建数据库和用户

```bash
sudo mysql -e "
CREATE DATABASE IF NOT EXISTS autoshop DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER IF NOT EXISTS 'autoshop'@'localhost' IDENTIFIED BY 'YourStrongPassword123';
CREATE USER IF NOT EXISTS 'autoshop'@'%' IDENTIFIED BY 'YourStrongPassword123';
GRANT ALL PRIVILEGES ON autoshop.* TO 'autoshop'@'localhost';
GRANT ALL PRIVILEGES ON autoshop.* TO 'autoshop'@'%';
FLUSH PRIVILEGES;
"
```

### 12.3 一键部署脚本

```bash
# 把代码传到服务器后,进入项目目录执行
cd /path/to/AutoShop\ API

# 编辑 deploy/autoshop.env 填好数据库密码
vim deploy/autoshop.env
#   SECRET_KEY=改成随机 32 位字符串
#   MYSQL_PASSWORD=上面设置的数据库密码

# 以 root 执行部署
sudo bash deploy/deploy.sh
```

`deploy.sh` 会依次完成：

1. 检查 MySQL 连接，创建数据库/用户
2. 创建 `autoshop` 系统用户
3. 复制代码到 `/opt/autoshop-api`
4. 安装 Python 虚拟环境 + 依赖
5. 写入环境变量到 `/etc/autoshop/autoshop.env`
6. 注册 systemd 服务（`autoshop.service`）
7. 添加每日备份 crontab 任务（凌晨 2:00 `mysqldump`）
8. 配置 nginx 反向代理（如 nginx 已安装）
9. 健康检查

### 12.4 验证部署

```bash
# 查看服务状态
sudo systemctl status autoshop

# 健康检查
curl -fsS http://127.0.0.1:8000/healthz

# 查看日志
sudo journalctl -u autoshop -f
```

### 12.5 nginx 反向代理配置（生产推荐）

`deploy/nginx-autoshop.conf` 已准备好，部署脚本会自动启用。关键配置如下（按需修改 `server_name`）：

```nginx
server {
    listen 80;
    server_name api.your-domain.com;

    client_max_body_size 10M;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /docs {
        proxy_pass http://127.0.0.1:8000/docs;
    }
}
```

启用 HTTPS（用 certbot）：
```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d api.your-domain.com
```

### 12.6 数据库备份

备份脚本位于 `deploy/autoshop-backup.sh`，部署时会自动加入 crontab：

```cron
0 2 * * * MYSQL_HOST=127.0.0.1 MYSQL_PORT=3306 \
    MYSQL_USER=autoshop MYSQL_PASSWORD='YourPassword' \
    MYSQL_DB=autoshop bash /opt/autoshop-api/deploy/autoshop-backup.sh \
    >> /var/log/autoshop-backup.log 2>&1
```

- 备份路径：`/var/backups/autoshop/autoshop-YYYYMMDD_HHMMSS.sql.gz`
- 保留策略：自动删除 14 天前的备份

手动执行备份：
```bash
sudo -u autoshop \
  MYSQL_HOST=127.0.0.1 \
  MYSQL_USER=autoshop \
  MYSQL_PASSWORD='YourPassword' \
  MYSQL_DB=autoshop \
  bash /opt/autoshop-api/deploy/autoshop-backup.sh
```

恢复数据：
```bash
zcat /var/backups/autoshop/autoshop-20260901_020000.sql.gz | \
  mysql -h 127.0.0.1 -u autoshop -p autoshop
```

### 12.7 升级版本

```bash
cd /opt/autoshop-api
sudo bash deploy/deploy.sh   # 会覆盖代码并重启服务
```

### 12.8 卸载

```bash
sudo systemctl stop autoshop
sudo systemctl disable autoshop
sudo rm /etc/systemd/system/autoshop.service
sudo rm -rf /opt/autoshop-api
sudo rm /etc/autoshop/autoshop.env
sudo rm /var/backups/autoshop 2>/dev/null || true
```

---

## 十三、Docker 部署

```bash
cd deploy
docker-compose up -d
```

访问 `http://<your-server>:8000/docs`。

---

## 十四、提交到 Git

### 1. 首次提交

```bash
cd "AutoShop API"

# 1) 初始化仓库
git init
git branch -M main

# 2) 配置身份
git config user.name "你的名字"
git config user.email "your-email@example.com"

# 3) 查看哪些文件会被提交
git status

# 4) 加入并提交
git add .
git commit -m "feat: 初始化 AutoShop API

- 13 个接口(auth/products/cart/orders/users) + 标准响应信封
- JWT 鉴权 + bcrypt,MySQL 8.0 存储
- Mock 下单支持 SUCCESS / FAIL / PENDING 三态
- /api/v1/_test/reset 测试重置接口
- pytest + httpx 自动化测试(40+ 用例)
- Linux 部署全套(systemd/nginx/Docker/MySQL备份)"
```

### 2. 在 GitHub / GitLab / Gitee 上建空仓库

1. 打开 <https://github.com/new>
2. **Repository name**: `autoshop-api`
3. **Description**: `AutoShop API - 接口自动化测试练习`
4. Public 或 Private(练习项目建议 Private)
5. **不要勾选** "Add a README / .gitignore / license"
6. 点 Create repository，复制仓库地址

### 3. 关联远程仓库并推送

```bash
# SSH(推荐)
git remote add origin git@github.com:你的用户名/autoshop-api.git

# HTTPS(每次 push 要输 token)
git remote add origin https://github.com:你的用户名/autoshop-api.git

git push -u origin main
```

### 4. 日常提交三连

```bash
git status
git diff
git add <文件>          # 或 git add . 全部
git commit -m "feat(cart): 加数量上限校验"
git push
```

### 5. 常见问题

| 现象 | 原因 | 解决 |
|---|---|---|
| `Access denied` 连接 MySQL 失败 | 密码错误或用户无权限 | 检查 `MYSQL_PASSWORD` 和 `GRANT` 语句 |
| `Unknown database 'autoshop'` | 数据库未创建 | 执行建库 SQL（见 12.2 节） |
| `Table 'xxx' doesn't exist` | 表未创建 | 首次启动时 `init_db()` 会自动建表，确认服务已启动 |
| `git status` 出现 `.env` | `.gitignore` 没生效 | `git rm --cached <文件>` 取消追踪 |
| HTTPS push 提示 `Login failed` | 用错了账号密码 | 用 Personal Access Token 代替密码 |
