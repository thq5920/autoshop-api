-- =============================================================================
-- reset_database.sql
-- 功能：自动化测试前重置数据库。清空所有表数据，AUTO_INCREMENT 重置为初始值。
-- 说明：本脚本不依赖 SET FOREIGN_KEY_CHECKS=0，因为数据库已彻底删除外键约束。
--       各表可按任意顺序单独 TRUNCATE，互不影响。
-- 注意：执行前请确认已连接 autoshop 数据库（USE autoshop;）。
-- =============================================================================

USE `autoshop`;

-- 1. 清空所有表（顺序无所谓，无外键约束）
TRUNCATE TABLE `order_items`;
TRUNCATE TABLE `orders`;
TRUNCATE TABLE `cart_items`;
TRUNCATE TABLE `products`;
TRUNCATE TABLE `users`;

-- 2. 恢复商品种子数据
INSERT INTO `products` (`id`, `name`, `description`, `category`, `price`, `stock`, `status`) VALUES
  (1001, 'iPhone 17',            'AutoShop Test Product', 'phone',    5999.00, 100, 'ON_SALE'),
  (1002, 'MacBook Air',          'AutoShop Test Product', 'computer', 7999.00,  50, 'ON_SALE'),
  (1003, 'AirPods',              'AutoShop Test Product', 'audio',     999.00,   0, 'ON_SALE'),
  (1004, 'Test Offline Product', 'AutoShop Test Product', 'test',      100.00,  10, 'OFF_SHELF');

-- 3. 恢复 demo 测试用户
--    password_hash 为 bcrypt('Demo@123456', rounds=4) 的哈希值
--    实际值由 Python: from app.security import hash_password; hash_password('Demo@123456') 生成
--    此处为占位符，运行时通过 app/seed.py 或 /_test/reset 接口重新生成
INSERT INTO `users` (`username`, `password_hash`, `email`, `phone`, `nickname`, `created_at`) VALUES
  ('demo', '$2b$04$placeholder_hash_replace_by_seed_or_api', 'demo@example.com', '13800138000', '演示用户', NOW());

-- 4. 验证
SELECT 'reset complete' AS status;
SELECT COUNT(*) AS product_count FROM products;
SELECT COUNT(*) AS user_count   FROM users;
