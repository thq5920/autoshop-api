# AutoShop API

专门用于接口自动化测试练习的 Mock 商城 API。

完整实现了一份 13 个接口的 RESTful 服务，统一返回格式、Bearer Token 鉴权、Mock 支付可控（SUCCESS / FAIL / PENDING），自带种子数据覆盖正常 / 库存不足 / 下架 / 不存在 四类商品场景。

---

## 一、技术栈

- Python 3.12 / FastAPI 0.115
- SQLAlchemy 2.0 + SQLite（WAL 模式）
- PyJWT + Passlib(bcrypt)
- Pydantic v2
- Swagger UI 自动生成于 `/docs`

## 二、目录结构

```
AutoShop API/
├── app/
│   ├── main.py              # FastAPI 入口
│   ├── config.py            # 配置
│   ├── database.py          # SQLAlchemy engine / Session
│   ├── deps.py              # get_current_user 依赖
│   ├── security.py          # JWT + bcrypt
│   ├── response.py          # 标准响应信封
│   ├── exceptions.py        # BizException + 统一处理
│   ├── seed.py              # 种子数据
│   ├── models/              # ORM 模型
│   ├── schemas/             # Pydantic 模型
│   ├── routers/             # 5 个路由模块
│   └── services/            # 业务层
├── tests/                   # pytest 自动化测试
├── deploy/                  # 部署文件
├── requirements.txt
└── README.md
```

## 三、本地启动

```bash
cd "AutoShop API"

# 推荐用虚拟环境
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 启动
uvicorn app.main:app --reload --port 8000
# 或生产模式
gunicorn app.main:app -k uvicorn.workers.UvicornWorker -w 2 -b 127.0.0.1:8000
```

打开浏览器：

- Swagger UI：<http://localhost:8000/docs>
- ReDoc：<http://localhost:8000/redoc>
- 健康检查：<http://localhost:8000/healthz>

## 四、接口清单（13 个）

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

## 五、统一响应信封

```json
{
  "code": 200,
  "message": "success",
  "data": { ... },
  "timestamp": 1787886000000,
  "requestId": "req_xxx"
}
```

### 业务码表

| code    | 含义        | HTTP |
|---------|-------------|------|
| 200     | 成功        | 200  |
| 40001   | 参数错误    | 400  |
| 40002   | 参数缺失    | 400  |
| 40003   | 商品已下架  | 400  |
| 40101   | 未登录      | 401  |
| 40102   | Token 无效  | 401  |
| 40103   | Token 已过期| 401  |
| 40401   | 数据不存在  | 404  |
| 40901   | 数据已存在  | 409  |
| 50001   | 系统异常    | 500  |

## 六、种子数据

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

## 七、Mock 下单控制

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

## 八、核心链路示例

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

## 九、自动化测试

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

## 十、Linux 部署

详见 [`deploy/README.md`](deploy/README.md)。

```bash
# 一键部署
sudo bash deploy/deploy.sh
```

## 十一、环境变量

| 变量名             | 默认值                          | 说明                          |
|--------------------|---------------------------------|-------------------------------|
| `AUTOSHOP_ENV`     | `dev`                           | dev / prod                    |
| `AUTOSHOP_DEBUG`   | `true`                          | 是否启用 `_test/reset`        |
| `SECRET_KEY`       | 开发用默认值（**请改**）        | JWT 签名密钥                  |
| `AUTOSHOP_DB_PATH` | `<项目目录>/autoshop.db`        | SQLite 文件路径               |
| `BCRYPT_ROUNDS`    | `4`                             | bcrypt 计算轮数（测试用 4）   |
