-- =============================================================================
-- schema.sql
-- 功能：autoshop 数据库完整建表脚本（无外键版）。
--       所有表统一 ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci。
-- 注意：本脚本不含 FOREIGN KEY / REFERENCES / ON DELETE CASCADE。
--       逻辑关联（user_id / product_id / order_id）由业务代码保证。
-- =============================================================================

-- 创建数据库
CREATE DATABASE IF NOT EXISTS `autoshop`
  DEFAULT CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE `autoshop`;


-- =============================================================================
-- 用户表
-- =============================================================================
CREATE TABLE IF NOT EXISTS `users` (
  `id`            INT          NOT NULL  AUTO_INCREMENT  COMMENT '用户ID',
  `username`      VARCHAR(20)  NOT NULL                      COMMENT '登录用户名',
  `password_hash` VARCHAR(128) NOT NULL                      COMMENT '登录密码哈希值',
  `email`         VARCHAR(120) NOT NULL                      COMMENT '用户邮箱',
  `phone`         VARCHAR(20)  DEFAULT NULL                  COMMENT '手机号',
  `nickname`      VARCHAR(50)  DEFAULT NULL                  COMMENT '用户昵称',
  `created_at`    DATETIME     NOT NULL                      COMMENT '创建时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_username` (`username`),
  UNIQUE KEY `uq_email`    (`email`)
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_unicode_ci
  COMMENT='用户表';


-- =============================================================================
-- 商品表
-- =============================================================================
CREATE TABLE IF NOT EXISTS `products` (
  `id`          INT            NOT NULL  AUTO_INCREMENT  COMMENT '商品ID',
  `name`        VARCHAR(100)  NOT NULL                      COMMENT '商品名称',
  `description` VARCHAR(500)  DEFAULT 'AutoShop Test Product' COMMENT '商品描述',
  `category`    VARCHAR(50)   NOT NULL                      COMMENT '商品分类',
  `price`       DECIMAL(10,2) NOT NULL                      COMMENT '商品单价',
  `stock`       INT           NOT NULL  DEFAULT 0          COMMENT '当前库存数量',
  `status`      VARCHAR(20)   NOT NULL  DEFAULT 'ON_SALE'  COMMENT '商品状态（ON_SALE 在售 / OFF_SHELF 下架）',
  PRIMARY KEY (`id`),
  INDEX `ix_category` (`category`)
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_unicode_ci
  COMMENT='商品表';


-- =============================================================================
-- 购物车明细表
-- 注意：user_id / product_id 为逻辑关联字段，无 FOREIGN KEY 约束。
--       数据关联完整性由业务代码保证。
-- =============================================================================
CREATE TABLE IF NOT EXISTS `cart_items` (
  `id`          INT            NOT NULL  AUTO_INCREMENT  COMMENT '购物车项ID',
  `user_id`     INT            NOT NULL                      COMMENT '用户ID，逻辑关联 users.id',
  `product_id`  INT            NOT NULL                      COMMENT '商品ID，逻辑关联 products.id',
  `quantity`    INT            NOT NULL  DEFAULT 1          COMMENT '商品数量',
  `unit_price`  DECIMAL(10,2) NOT NULL                      COMMENT '加入购物车时商品单价快照',
  `created_at`  DATETIME       DEFAULT NULL                  COMMENT '加入购物车时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_user_product` (`user_id`, `product_id`),
  INDEX `ix_cart_user_id` (`user_id`),
  INDEX `ix_cart_product_id` (`product_id`)
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_unicode_ci
  COMMENT='购物车明细表';


-- =============================================================================
-- 订单主表
-- 注意：user_id 为逻辑关联字段，无 FOREIGN KEY 约束。
-- =============================================================================
CREATE TABLE IF NOT EXISTS `orders` (
  `id`             INT            NOT NULL  AUTO_INCREMENT  COMMENT '订单ID',
  `order_no`       VARCHAR(32)    NOT NULL                      COMMENT '订单编号',
  `user_id`        INT            NOT NULL                      COMMENT '用户ID，逻辑关联 users.id',
  `total_amount`   DECIMAL(10,2) NOT NULL                      COMMENT '订单总金额',
  `order_status`   VARCHAR(32)    NOT NULL                      COMMENT '订单状态（PAID 已支付 / PAY_FAILED 支付失败 / PENDING_PAYMENT 待支付）',
  `payment_status` VARCHAR(32)    NOT NULL                      COMMENT 'Mock支付状态（MOCK_SUCCESS / MOCK_FAILED / MOCK_PENDING）',
  `receiver`       JSON          NOT NULL                      COMMENT '收货人信息JSON',
  `remark`         VARCHAR(200)  DEFAULT NULL                  COMMENT '订单备注',
  `created_at`     DATETIME       NOT NULL                      COMMENT '下单时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_order_no` (`order_no`),
  INDEX `ix_orders_user_id` (`user_id`)
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_unicode_ci
  COMMENT='订单主表';


-- =============================================================================
-- 订单商品明细表
-- 注意：order_id / product_id 为逻辑关联字段，无 FOREIGN KEY 约束。
--       数据关联完整性由业务代码保证。
-- =============================================================================
CREATE TABLE IF NOT EXISTS `order_items` (
  `id`           INT            NOT NULL  AUTO_INCREMENT  COMMENT '订单项ID',
  `order_id`     INT            NOT NULL                      COMMENT '订单ID，逻辑关联 orders.id',
  `product_id`   INT            NOT NULL                      COMMENT '商品ID，逻辑关联 products.id',
  `product_name` VARCHAR(100)   NOT NULL                      COMMENT '下单时商品名称快照',
  `quantity`     INT            NOT NULL                      COMMENT '购买数量',
  `unit_price`   DECIMAL(10,2) NOT NULL                      COMMENT '下单时商品单价快照',
  `amount`       DECIMAL(10,2) NOT NULL                      COMMENT '商品小计',
  PRIMARY KEY (`id`),
  INDEX `ix_order_items_order_id` (`order_id`),
  INDEX `ix_order_items_product_id` (`product_id`)
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_unicode_ci
  COMMENT='订单商品明细表';
