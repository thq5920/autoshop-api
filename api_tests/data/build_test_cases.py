"""
api_tests/data/build_test_cases.py
=================================
无三方依赖（stdlib zipfile + xml）生成 test_cases.xlsx
五个 Sheet：auth / users / products / cart / orders

直接运行：
    python api_tests/data/build_test_cases.py
"""
from __future__ import annotations

import sys
import zipfile
from pathlib import Path
from xml.sax.saxutils import escape


THIS_DIR = Path(__file__).resolve().parent
OUTPUT_PATH = THIS_DIR / "test_cases.xlsx"


# 表头（统一五列：ID / 用例标题 / 步骤 / 期望 / 优先级）
COMMON_HEADERS = ["ID", "Title", "Steps", "Expected", "Priority"]


SHEETS: dict[str, list[list[str]]] = {
    "auth": [
        ["AT001", "Register & Login happy path",
         "POST /auth/register with valid payload | POST /auth/login",
         "code=200, returns accessToken (JWT 3 parts)",
         "P0"],
        ["AT002", "Register duplicate username",
         "POST /auth/register with same username twice",
         "second returns 409 / code=40901",
         "P0"],
        ["AT003", "Login wrong password",
         "POST /auth/login with wrong password",
         "401 / code=40302 (DEBUG mode)",
         "P0"],
        ["AT004", "Login non-existing user",
         "POST /auth/login with random username",
         "401 / code=40301 (DEBUG mode)",
         "P0"],
        ["AT005", "Register weak password",
         "POST /auth/register with password='short'",
         "422 / code=40205",
         "P1"],
        ["AT006", "Register invalid email",
         "POST /auth/register with email='not-an-email'",
         "422 / code=40207",
         "P1"],
    ],
    "users": [
        ["US001", "Get current user",
         "GET /users/me with Bearer token",
         "code=200, returns userId/username/email",
         "P0"],
        ["US002", "Update user profile",
         "PUT /users/me with nickname='X'",
         "code=200, nickname updated",
         "P1"],
        ["US003", "Get me without auth",
         "GET /users/me without token",
         "401 / code=40101",
         "P0"],
    ],
    "products": [
        ["PR001", "List products",
         "GET /products",
         "code=200, list with pagination",
         "P0"],
        ["PR002", "Filter by keyword",
         "GET /products?keyword=iphone",
         "code=200, name contains 'iphone'",
         "P1"],
        ["PR003", "Filter by price range",
         "GET /products?minPrice=1000&maxPrice=7000",
         "code=200, all in range",
         "P1"],
        ["PR004", "Get product by id",
         "GET /products/1001",
         "code=200, returns product detail",
         "P0"],
        ["PR005", "Get non-existing product",
         "GET /products/99999",
         "404 / code=40501",
         "P0"],
        ["PR006", "Get off-shelf product",
         "GET /products/1004",
         "code=200, status=OFF_SHELF",
         "P1"],
        ["PR007", "Get out-of-stock product",
         "GET /products/1003",
         "code=200, stock=0, status=ON_SALE",
         "P1"],
    ],
    "cart": [
        ["CR001", "Add to cart",
         "POST /cart/items {productId:1001, quantity:2}",
         "code=200, cartItemId+totalAmount=11998.00",
         "P0"],
        ["CR002", "Add out-of-stock",
         "POST /cart/items {productId:1003, quantity:1}",
         "400 / code=40503",
         "P0"],
        ["CR003", "Add off-shelf product (allowed)",
         "POST /cart/items {productId:1004, quantity:1}",
         "code=200 (off-shelf allowed in cart, blocked at order)",
         "P0"],
        ["CR004", "Add non-existing product",
         "POST /cart/items {productId:99999, quantity:1}",
         "404 / code=40501",
         "P0"],
        ["CR005", "Update cart item quantity",
         "PUT /cart/items/{id} {quantity:3}",
         "code=200, quantity/totalAmount updated",
         "P0"],
        ["CR006", "Delete cart item",
         "DELETE /cart/items/{id}",
         "code=200, item removed",
         "P1"],
        ["CR007", "List cart",
         "GET /cart",
         "code=200, items with totalQuantity/totalAmount",
         "P0"],
        ["CR008", "Invalid quantity=0",
         "POST /cart/items {quantity:0}",
         "422 / code=40001",
         "P1"],
        ["CR009", "Cart without auth",
         "GET /cart",
         "401 / code=40101",
         "P0"],
    ],
    "orders": [
        ["OR001", "Create order (mock SUCCESS)",
         "POST /orders {cartItemIds:[id], mockResult:'SUCCESS'}",
         "code=200, orderStatus=PAID/MOCK_SUCCESS",
         "P0"],
        ["OR002", "Create order (mock FAIL)",
         "POST /orders {mockResult:'FAIL'}",
         "code=200, orderStatus=PAY_FAILED/MOCK_FAILED",
         "P0"],
        ["OR003", "Create order (mock PENDING)",
         "POST /orders {mockResult:'PENDING'}",
         "code=200, orderStatus=PENDING_PAYMENT/MOCK_PENDING",
         "P0"],
        ["OR004", "Create order with empty cart",
         "POST /orders {cartItemIds:[]}",
         "400 / code=40602",
         "P0"],
        ["OR005", "Create order invalid cart_item",
         "POST /orders {cartItemIds:[99999]}",
         "404 / code=40601",
         "P0"],
        ["OR006", "Create order off-shelf product",
         "POST /orders {productId:1004 in cart}",
         "400 / code=40502",
         "P0"],
        ["OR007", "Order detail",
         "GET /orders/{id}",
         "code=200, items[] length matches",
         "P0"],
        ["OR008", "Order detail not found",
         "GET /orders/99999",
         "404 / code=40701",
         "P0"],
        ["OR009", "List my orders",
         "GET /orders",
         "code=200, paginated list",
         "P1"],
        ["OR010", "Filter orders by status",
         "GET /orders?status=PAY_FAILED",
         "code=200, all orders have status=PAY_FAILED",
         "P1"],
    ],
}


def _sheet_xml(rows: list[list[str]]) -> str:
    body = []
    for r_idx, row in enumerate(rows, start=1):
        cells = []
        for c_idx, val in enumerate(row, start=1):
            ref = f"{chr(64 + c_idx)}{r_idx}"
            cells.append(
                f'<c r="{ref}" t="inlineStr"><is><t xml:space="preserve">'
                f"{escape(val)}"
                f"</t></is></c>"
            )
        body.append(f'<row r="{r_idx}">' + "".join(cells) + "</row>")
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
        '<sheetData>' + "".join(body) + '</sheetData></worksheet>'
    )


def build(sheets: dict[str, list[list[str]]], output: Path) -> None:
    sheet_names = list(sheets.keys())
    sheet_xml = {name: _sheet_xml([COMMON_HEADERS] + rows)
                 for name, rows in sheets.items()}

    # workbook.xml
    sheets_block = "".join(
        f'<sheet name="{name}" sheetId="{i+1}" r:id="rId{i+1}"/>'
        for i, name in enumerate(sheet_names)
    )
    workbook_xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
        f"<sheets>{sheets_block}</sheets></workbook>"
    )
    workbook_rels = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        + "".join(
            f'<Relationship Id="rId{i+1}" '
            f'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" '
            f'Target="worksheets/sheet{i+1}.xml"/>'
            for i in range(len(sheet_names))
        )
        + "</Relationships>"
    )
    content_types = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
        '<Default Extension="xml" ContentType="application/xml"/>'
        '<Override PartName="/xl/workbook.xml" '
        'ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>'
        + "".join(
            f'<Override PartName="/xl/worksheets/sheet{i+1}.xml" '
            f'ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
            for i in range(len(sheet_names))
        )
        + "</Types>"
    )
    root_rels = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" '
        'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" '
        'Target="xl/workbook.xml"/>'
        "</Relationships>"
    )

    with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", content_types)
        z.writestr("_rels/.rels", root_rels)
        z.writestr("xl/workbook.xml", workbook_xml)
        z.writestr("xl/_rels/workbook.xml.rels", workbook_rels)
        for i, name in enumerate(sheet_names, start=1):
            z.writestr(f"xl/worksheets/sheet{i}.xml", sheet_xml[name])


if __name__ == "__main__":
    build(SHEETS, OUTPUT_PATH)
    print(f"written: {OUTPUT_PATH} ({len(SHEETS)} sheets)")
