-- =============================================================================
-- mock_data.sql
-- 功能：AutoShop 完整拟真测试数据（每表100条）
-- 
-- 使用方法：
--   mysql -u 用户名 -p autoshop < scripts/mock_data.sql
--
-- 可重复执行：每次执行前会先清空所有表数据，再重新插入
-- =============================================================================

SET FOREIGN_KEY_CHECKS = 0;

-- 清空现有数据（按依赖关系逆序）
TRUNCATE TABLE order_items;
TRUNCATE TABLE orders;
TRUNCATE TABLE cart_items;
TRUNCATE TABLE products;
TRUNCATE TABLE users;

SET FOREIGN_KEY_CHECKS = 1;

-- =============================================================================
-- 一、users 用户表（100条）
-- 密码统一为：Test@123456
-- =============================================================================

INSERT INTO users (id, username, password_hash, email, phone, nickname, created_at) VALUES
(1, 'alex.chen', '$2b$04$.wQOhyzH8ABEiXAmSFWG0.ngeILz59rXqZVilzToLr2MpVmD/zmBG', 'alex.chen@example.com', '+8613812345678', 'Alex', '2025-09-15 10:23:45'),
(2, 'michael_wang', '$2b$04$.wQOhyzH8ABEiXAmSFWG0.ngeILz59rXqZVilzToLr2MpVmD/zmBG', 'michael.wang@example.com', '+8618612345679', 'Michael', '2025-09-22 14:35:12'),
(3, 'emily.zhang', '$2b$04$.wQOhyzH8ABEiXAmSFWG0.ngeILz59rXqZVilzToLr2MpVmD/zmBG', 'emily.zhang@example.net', '+8613912345680', 'Emily', '2025-10-03 09:15:33'),
(4, 'kevinliu88', '$2b$04$.wQOhyzH8ABEiXAmSFWG0.ngeILz59rXqZVilzToLr2MpVmD/zmBG', 'kevin.liu@example.org', '+6591234567', 'Kevin', '2025-10-18 16:45:21'),
(5, 'sophia_lin', '$2b$04$.wQOhyzH8ABEiXAmSFWG0.ngeILz59rXqZVilzToLr2MpVmD/zmBG', 'sophia.lin@example.com', '+8615512345682', 'Sophia', '2025-11-02 11:20:15'),
(6, 'jasonwu', '$2b$04$.wQOhyzH8ABEiXAmSFWG0.ngeILz59rXqZVilzToLr2MpVmD/zmBG', 'jason.wu@example.net', '+8618612345683', 'Jason', '2025-11-15 08:30:44'),
(7, 'olivia_zhou', '$2b$04$.wQOhyzH8ABEiXAmSFWG0.ngeILz59rXqZVilzToLr2MpVmD/zmBG', 'olivia.zhou@example.com', '+8613912345684', 'Olivia', '2025-11-28 19:55:02'),
(8, 'danielhuang', '$2b$04$.wQOhyzH8ABEiXAmSFWG0.ngeILz59rXqZVilzToLr2MpVmD/zmBG', 'daniel.huang@example.org', '+6592345678', 'Daniel', '2025-12-05 13:40:18'),
(9, 'mia.li', '$2b$04$.wQOhyzH8ABEiXAmSFWG0.ngeILz59rXqZVilzToLr2MpVmD/zmBG', 'mia.li@example.com', '+8613812345686', 'Mia', '2025-12-12 20:15:30'),
(10, 'leotanaka', '$2b$04$.wQOhyzH8ABEiXAmSFWG0.ngeILz59rXqZVilzToLr2MpVmD/zmBG', 'leo.tanaka@example.jp', '+819012345678', 'Leo', '2025-12-20 07:25:11'),
(11, 'gracekim', '$2b$04$.wQOhyzH8ABEiXAmSFWG0.ngeILz59rXqZVilzToLr2MpVmD/zmBG', 'grace.kim@example.kr', '+8210123456789', 'Grace', '2026-01-03 15:50:22'),
(12, 'ethanyeoh', '$2b$04$.wQOhyzH8ABEiXAmSFWG0.ngeILz59rXqZVilzToLr2MpVmD/zmBG', 'ethan.yeo@example.sg', '+6598765432', 'Ethan', '2026-01-10 12:35:48'),
(13, 'wendy.lee', '$2b$04$.wQOhyzH8ABEiXAmSFWG0.ngeILz59rXqZVilzToLr2MpVmD/zmBG', 'wendy.lee@example.com', '+8613912345690', 'Wendy', '2026-01-18 21:10:05'),
(14, 'richardzhou', '$2b$04$.wQOhyzH8ABEiXAmSFWG0.ngeILz59rXqZVilzToLr2MpVmD/zmBG', 'richard.zhou@example.net', '+8618612345691', 'Richard', '2026-01-25 10:45:33'),
(15, 'amanda.chen', '$2b$04$.wQOhyzH8ABEiXAmSFWG0.ngeILz59rXqZVilzToLr2MpVmD/zmBG', 'amanda.chen@example.com', '+254712345678', 'Amanda', '2026-02-01 18:20:15'),
(16, 'brianwang', '$2b$04$.wQOhyzH8ABEiXAmSFWG0.ngeILz59rXqZVilzToLr2MpVmD/zmBG', 'brian.wang@example.org', '+8615512345693', 'Brian', '2026-02-08 14:55:42'),
(17, 'charlotte.liu', '$2b$04$.wQOhyzH8ABEiXAmSFWG0.ngeILz59rXqZVilzToLr2MpVmD/zmBG', 'charlotte.liu@example.com', '+8613912345694', 'Charlotte', '2026-02-15 09:30:20'),
(18, 'davidwu', '$2b$04$.wQOhyzH8ABEiXAmSFWG0.ngeILz59rXqZVilzToLr2MpVmD/zmBG', 'david.wu@example.net', '+6593456789', 'David', '2026-02-22 16:40:55'),
(19, 'emilybrown', '$2b$04$.wQOhyzH8ABEiXAmSFWG0.ngeILz59rXqZVilzToLr2MpVmD/zmBG', 'emily.brown@example.com', '+8613812345696', NULL, '2026-03-01 22:15:08'),
(20, 'felixzhang', '$2b$04$.wQOhyzH8ABEiXAmSFWG0.ngeILz59rXqZVilzToLr2MpVmD/zmBG', 'felix.zhang@example.org', '+8618612345697', 'Felix', '2026-03-08 11:25:37'),
(21, 'gabriellaliu', '$2b$04$.wQOhyzH8ABEiXAmSFWG0.ngeILz59rXqZVilzToLr2MpVmD/zmBG', 'gabriella.liu@example.com', '+8615512345698', 'Gabriella', '2026-03-15 08:50:19'),
(22, 'henry.wu', '$2b$04$.wQOhyzH8ABEiXAmSFWG0.ngeILz59rXqZVilzToLr2MpVmD/zmBG', 'henry.wu@example.net', '+8613912345699', 'Henry', '2026-03-22 13:35:44'),
(23, 'irene.zhou', '$2b$04$.wQOhyzH8ABEiXAmSFWG0.ngeILz59rXqZVilzToLr2MpVmD/zmBG', 'irene.zhou@example.com', NULL, 'Irene', '2026-03-29 19:10:02'),
(24, 'jacobhuang', '$2b$04$.wQOhyzH8ABEiXAmSFWG0.ngeILz59rXqZVilzToLr2MpVmD/zmBG', 'jacob.huang@example.org', '+6594567890', 'Jacob', '2026-04-05 15:45:28'),
(25, 'karen.lin', '$2b$04$.wQOhyzH8ABEiXAmSFWG0.ngeILz59rXqZVilzToLr2MpVmD/zmBG', 'karen.lin@example.com', '+8613812345702', 'Karen', '2026-04-12 10:20:51'),
(26, 'lawrence.chen', '$2b$04$.wQOhyzH8ABEiXAmSFWG0.ngeILz59rXqZVilzToLr2MpVmD/zmBG', 'lawrence.chen@example.net', '+8618612345703', 'Lawrence', '2026-04-19 17:30:16'),
(27, 'monica.wang', '$2b$04$.wQOhyzH8ABEiXAmSFWG0.ngeILz59rXqZVilzToLr2MpVmD/zmBG', 'monica.wang@example.com', '+8613912345704', 'Monica', '2026-04-26 21:55:33'),
(28, 'nicholas.liu', '$2b$04$.wQOhyzH8ABEiXAmSFWG0.ngeILz59rXqZVilzToLr2MpVmD/zmBG', 'nicholas.liu@example.org', '+6595678901', 'Nicholas', '2026-05-03 06:15:47'),
(29, 'oliverzhou', '$2b$04$.wQOhyzH8ABEiXAmSFWG0.ngeILz59rXqZVilzToLr2MpVmD/zmBG', 'oliver.zhou@example.com', '+8615512345706', 'Oliver', '2026-05-10 12:40:22'),
(30, 'pamela.huang', '$2b$04$.wQOhyzH8ABEiXAmSFWG0.ngeILz59rXqZVilzToLr2MpVmD/zmBG', 'pamela.huang@example.net', '+8613812345707', NULL, '2026-05-17 09:25:10'),
(31, 'quinn.chen', '$2b$04$.wQOhyzH8ABEiXAmSFWG0.ngeILz59rXqZVilzToLr2MpVmD/zmBG', 'quinn.chen@example.com', '+8618612345708', 'Quinn', '2026-05-24 14:50:38'),
(32, 'rachel.wang', '$2b$04$.wQOhyzH8ABEiXAmSFWG0.ngeILz59rXqZVilzToLr2MpVmD/zmBG', 'rachel.wang@example.org', '+8613912345709', 'Rachel', '2026-05-31 18:35:15'),
(33, 'stephen.liu', '$2b$04$.wQOhyzH8ABEiXAmSFWG0.ngeILz59rXqZVilzToLr2MpVmD/zmBG', 'stephen.liu@example.com', '+6596789012', 'Stephen', '2026-06-07 11:20:44'),
(34, 'tinazhou', '$2b$04$.wQOhyzH8ABEiXAmSFWG0.ngeILz59rXqZVilzToLr2MpVmD/zmBG', 'tina.zhou@example.com', '+8615512345711', 'Tina', '2026-06-14 20:45:29'),
(35, 'ulrich.huang', '$2b$04$.wQOhyzH8ABEiXAmSFWG0.ngeILz59rXqZVilzToLr2MpVmD/zmBG', 'ulrich.huang@example.com', '+8613812345712', 'Ulrich', '2026-06-21 15:10:53'),
(36, 'vivian.chen', '$2b$04$.wQOhyzH8ABEiXAmSFWG0.ngeILz59rXqZVilzToLr2MpVmD/zmBG', 'vivian.chen@example.org', '+8618612345713', 'Vivian', '2026-06-28 08:30:17'),
(37, 'walter.wang', '$2b$04$.wQOhyzH8ABEiXAmSFWG0.ngeILz59rXqZVilzToLr2MpVmD/zmBG', 'walter.wang@example.com', '+8613912345714', NULL, '2026-07-05 13:55:41'),
(38, 'xiaomei.liu', '$2b$04$.wQOhyzH8ABEiXAmSFWG0.ngeILz59rXqZVilzToLr2MpVmD/zmBG', 'xiaomei.liu@example.net', '+6597890123', 'Xiaomei', '2026-07-12 19:40:08'),
(39, 'yifan.zhou', '$2b$04$.wQOhyzH8ABEiXAmSFWG0.ngeILz59rXqZVilzToLr2MpVmD/zmBG', 'yifan.zhou@example.com', '+8615512345716', 'Yifan', '2026-07-19 22:25:35'),
(40, 'zoe.huang', '$2b$04$.wQOhyzH8ABEiXAmSFWG0.ngeILz59rXqZVilzToLr2MpVmD/zmBG', 'zoe.huang@example.org', '+8613812345717', 'Zoe', '2026-07-26 10:15:22'),
(41, 'andrew.chen', '$2b$04$.wQOhyzH8ABEiXAmSFWG0.ngeILz59rXqZVilzToLr2MpVmD/zmBG', 'andrew.chen@example.com', '+8618612345718', 'Andrew', '2026-08-02 16:50:49'),
(42, 'bella.wang', '$2b$04$.wQOhyzH8ABEiXAmSFWG0.ngeILz59rXqZVilzToLr2MpVmD/zmBG', 'bella.wang@example.net', '+8613912345719', 'Bella', '2026-08-09 12:35:14'),
(43, 'carlos.liu', '$2b$04$.wQOhyzH8ABEiXAmSFWG0.ngeILz59rXqZVilzToLr2MpVmD/zmBG', 'carlos.liu@example.org', '+6598901234', 'Carlos', '2026-08-16 07:20:38'),
(44, 'diana.zhou', '$2b$04$.wQOhyzH8ABEiXAmSFWG0.ngeILz59rXqZVilzToLr2MpVmD/zmBG', 'diana.zhou@example.com', '+8615512345721', 'Diana', '2026-08-23 14:45:25'),
(45, 'eugene.huang', '$2b$04$.wQOhyzH8ABEiXAmSFWG0.ngeILz59rXqZVilzToLr2MpVmD/zmBG', 'eugene.huang@example.net', '+8613812345722', 'Eugene', '2026-08-30 20:30:11'),
(46, 'fiona.chen', '$2b$04$.wQOhyzH8ABEiXAmSFWG0.ngeILz59rXqZVilzToLr2MpVmD/zmBG', 'fiona.chen@example.com', '+8618612345723', NULL, '2026-09-01 09:15:47'),
(47, 'george.wang', '$2b$04$.wQOhyzH8ABEiXAmSFWG0.ngeILz59rXqZVilzToLr2MpVmD/zmBG', 'george.wang@example.org', '+8613912345724', 'George', '2026-09-02 11:40:33'),
(48, 'hannah.liu', '$2b$04$.wQOhyzH8ABEiXAmSFWG0.ngeILz59rXqZVilzToLr2MpVmD/zmBG', 'hannah.liu@example.com', '+6599012345', 'Hannah', '2026-09-03 15:25:19'),
(49, 'ian.zhou', '$2b$04$.wQOhyzH8ABEiXAmSFWG0.ngeILz59rXqZVilzToLr2MpVmD/zmBG', 'ian.zhou@example.net', '+8615512345726', 'Ian', '2026-09-04 18:50:55'),
(50, 'julia.huang', '$2b$04$.wQOhyzH8ABEiXAmSFWG0.ngeILz59rXqZVilzToLr2MpVmD/zmBG', 'julia.huang@example.com', '+8613812345727', 'Julia', '2026-09-05 21:35:42'),
(51, 'kevin.miller', '$2b$04$.wQOhyzH8ABEiXAmSFWG0.ngeILz59rXqZVilzToLr2MpVmD/zmBG', 'kevin.miller@example.com', '+8618612345728', 'Kevin', '2026-09-06 08:20:15'),
(52, 'lisa.wang', '$2b$04$.wQOhyzH8ABEiXAmSFWG0.ngeILz59rXqZVilzToLr2MpVmD/zmBG', 'lisa.wang@example.net', '+8613912345729', 'Lisa', '2026-09-07 10:45:38'),
(53, 'mark.liu', '$2b$04$.wQOhyzH8ABEiXAmSFWG0.ngeILz59rXqZVilzToLr2MpVmD/zmBG', 'mark.liu@example.org', NULL, 'Mark', '2026-09-08 06:30:22'),
(54, 'nancy.zhou', '$2b$04$.wQOhyzH8ABEiXAmSFWG0.ngeILz59rXqZVilzToLr2MpVmD/zmBG', 'nancy.zhou@example.com', '+8615512345731', 'Nancy', '2025-10-10 13:15:48'),
(55, 'oscar.chen', '$2b$04$.wQOhyzH8ABEiXAmSFWG0.ngeILz59rXqZVilzToLr2MpVmD/zmBG', 'oscar.chen@example.net', '+8613812345732', 'Oscar', '2025-11-20 17:40:35'),
(56, 'patricia.wang', '$2b$04$.wQOhyzH8ABEiXAmSFWG0.ngeILz59rXqZVilzToLr2MpVmD/zmBG', 'patricia.wang@example.com', '+8618612345733', 'Patricia', '2025-12-25 20:55:11'),
(57, 'queenie.liu', '$2b$04$.wQOhyzH8ABEiXAmSFWG0.ngeILz59rXqZVilzToLr2MpVmD/zmBG', 'queenie.liu@example.org', '+6590123456', 'Queenie', '2026-01-05 14:20:27'),
(58, 'robert.zhou', '$2b$04$.wQOhyzH8ABEiXAmSFWG0.ngeILz59rXqZVilzToLr2MpVmD/zmBG', 'robert.zhou@example.com', '+8615512345735', 'Robert', '2026-01-20 19:35:43'),
(59, 'sabrina.huang', '$2b$04$.wQOhyzH8ABEiXAmSFWG0.ngeILz59rXqZVilzToLr2MpVmD/zmBG', 'sabrina.huang@example.net', '+8613812345736', 'Sabrina', '2026-02-14 22:50:09'),
(60, 'tony.chen', '$2b$04$.wQOhyzH8ABEiXAmSFWG0.ngeILz59rXqZVilzToLr2MpVmD/zmBG', 'tony.chen@example.com', '+8618612345737', 'Tony', '2026-02-28 11:25:34'),
(61, 'ursula.wang', '$2b$04$.wQOhyzH8ABEiXAmSFWG0.ngeILz59rXqZVilzToLr2MpVmD/zmBG', 'ursula.wang@example.org', '+8613912345738', NULL, '2026-03-15 16:40:51'),
(62, 'victor.liu', '$2b$04$.wQOhyzH8ABEiXAmSFWG0.ngeILz59rXqZVilzToLr2MpVmD/zmBG', 'victor.liu@example.com', '+6591234567', 'Victor', '2026-03-30 09:15:18'),
(63, 'wendy.zhou', '$2b$04$.wQOhyzH8ABEiXAmSFWG0.ngeILz59rXqZVilzToLr2MpVmD/zmBG', 'wendy.zhou@example.net', '+8615512345740', 'Wendy', '2026-04-12 12:30:45'),
(64, 'xavier.huang', '$2b$04$.wQOhyzH8ABEiXAmSFWG0.ngeILz59rXqZVilzToLr2MpVmD/zmBG', 'xavier.huang@example.com', '+8613812345741', 'Xavier', '2026-04-25 18:55:22'),
(65, 'yvonne.chen', '$2b$04$.wQOhyzH8ABEiXAmSFWG0.ngeILz59rXqZVilzToLr2MpVmD/zmBG', 'yvonne.chen@example.org', '+8618612345742', 'Yvonne', '2026-05-08 21:20:39'),
(66, 'zachary.wang', '$2b$04$.wQOhyzH8ABEiXAmSFWG0.ngeILz59rXqZVilzToLr2MpVmD/zmBG', 'zachary.wang@example.com', '+8613912345743', 'Zachary', '2026-05-22 14:45:16'),
(67, 'alice.liu', '$2b$04$.wQOhyzH8ABEiXAmSFWG0.ngeILz59rXqZVilzToLr2MpVmD/zmBG', 'alice.liu@example.net', '+6592345678', 'Alice', '2026-06-05 10:30:53'),
(68, 'brad.zhou', '$2b$04$.wQOhyzH8ABEiXAmSFWG0.ngeILz59rXqZVilzToLr2MpVmD/zmBG', 'brad.zhou@example.com', '+8615512345745', 'Brad', '2026-06-18 07:15:27'),
(69, 'cathy.huang', '$2b$04$.wQOhyzH8ABEiXAmSFWG0.ngeILz59rXqZVilzToLr2MpVmD/zmBG', 'cathy.huang@example.org', '+8613812345746', 'Cathy', '2026-07-01 13:40:44'),
(70, 'derek.chen', '$2b$04$.wQOhyzH8ABEiXAmSFWG0.ngeILz59rXqZVilzToLr2MpVmD/zmBG', 'derek.chen@example.com', '+8618612345747', NULL, '2026-07-15 19:25:11'),
(71, 'emma.wang', '$2b$04$.wQOhyzH8ABEiXAmSFWG0.ngeILz59rXqZVilzToLr2MpVmD/zmBG', 'emma.wang@example.net', '+8613912345748', 'Emma', '2026-07-28 22:50:38'),
(72, 'frank.liu', '$2b$04$.wQOhyzH8ABEiXAmSFWG0.ngeILz59rXqZVilzToLr2MpVmD/zmBG', 'frank.liu@example.com', '+6593456789', 'Frank', '2026-08-10 15:35:25'),
(73, 'grace.zhou', '$2b$04$.wQOhyzH8ABEiXAmSFWG0.ngeILz59rXqZVilzToLr2MpVmD/zmBG', 'grace.zhou@example.org', '+8615512345750', 'Grace', '2026-08-22 11:20:42'),
(74, 'henry.chen', '$2b$04$.wQOhyzH8ABEiXAmSFWG0.ngeILz59rXqZVilzToLr2MpVmD/zmBG', 'henry.chen@example.com', '+8613812345751', 'Henry', '2026-09-03 08:45:19'),
(75, 'ivy.wang', '$2b$04$.wQOhyzH8ABEiXAmSFWG0.ngeILz59rXqZVilzToLr2MpVmD/zmBG', 'ivy.wang@example.net', '+8618612345752', 'Ivy', '2026-09-05 16:30:56'),
(76, 'jack.liu', '$2b$04$.wQOhyzH8ABEiXAmSFWG0.ngeILz59rXqZVilzToLr2MpVmD/zmBG', 'jack.liu@example.com', '+8613912345753', 'Jack', '2025-09-08 20:15:33'),
(77, 'kelly.zhou', '$2b$04$.wQOhyzH8ABEiXAmSFWG0.ngeILz59rXqZVilzToLr2MpVmD/zmBG', 'kelly.zhou@example.org', '+6594567890', 'Kelly', '2025-10-15 12:40:48'),
(78, 'lucas.huang', '$2b$04$.wQOhyzH8ABEiXAmSFWG0.ngeILz59rXqZVilzToLr2MpVmD/zmBG', 'lucas.huang@example.net', '+8615512345755', 'Lucas', '2025-11-22 17:25:14'),
(79, 'mabel.chen', '$2b$04$.wQOhyzH8ABEiXAmSFWG0.ngeILz59rXqZVilzToLr2MpVmD/zmBG', 'mabel.chen@example.com', '+8613812345756', 'Mabel', '2025-12-18 23:50:29'),
(80, 'neil.wang', '$2b$04$.wQOhyzH8ABEiXAmSFWG0.ngeILz59rXqZVilzToLr2MpVmD/zmBG', 'neil.wang@example.org', '+8618612345757', 'Neil', '2026-01-25 10:35:45'),
(81, 'ophelia.liu', '$2b$04$.wQOhyzH8ABEiXAmSFWG0.ngeILz59rXqZVilzToLr2MpVmD/zmBG', 'ophelia.liu@example.com', '+8613912345758', 'Ophelia', '2026-02-11 14:20:12'),
(82, 'peter.zhou', '$2b$04$.wQOhyzH8ABEiXAmSFWG0.ngeILz59rXqZVilzToLr2MpVmD/zmBG', 'peter.zhou@example.net', '+6595678901', 'Peter', '2026-02-28 19:45:37'),
(83, 'queen.huang', '$2b$04$.wQOhyzH8ABEiXAmSFWG0.ngeILz59rXqZVilzToLr2MpVmD/zmBG', 'queen.huang@example.com', '+8615512345760', NULL, '2026-03-20 21:30:54'),
(84, 'randy.chen', '$2b$04$.wQOhyzH8ABEiXAmSFWG0.ngeILz59rXqZVilzToLr2MpVmD/zmBG', 'randy.chen@example.org', '+8613812345761', 'Randy', '2026-04-05 11:15:21'),
(85, 'sally.wang', '$2b$04$.wQOhyzH8ABEiXAmSFWG0.ngeILz59rXqZVilzToLr2MpVmD/zmBG', 'sally.wang@example.com', '+8618612345762', 'Sally', '2026-04-18 16:40:38'),
(86, 'tommy.liu', '$2b$04$.wQOhyzH8ABEiXAmSFWG0.ngeILz59rXqZVilzToLr2MpVmD/zmBG', 'tommy.liu@example.net', '+8613912345763', 'Tommy', '2026-05-02 08:25:15'),
(87, 'una.zhou', '$2b$04$.wQOhyzH8ABEiXAmSFWG0.ngeILz59rXqZVilzToLr2MpVmD/zmBG', 'una.zhou@example.com', '+6596789012', 'Una', '2026-05-16 13:50:42'),
(88, 'vince.huang', '$2b$04$.wQOhyzH8ABEiXAmSFWG0.ngeILz59rXqZVilzToLr2MpVmD/zmBG', 'vince.huang@example.org', '+8615512345765', 'Vince', '2026-05-30 18:35:09'),
(89, 'wanda.chen', '$2b$04$.wQOhyzH8ABEiXAmSFWG0.ngeILz59rXqZVilzToLr2MpVmD/zmBG', 'wanda.chen@example.com', '+8613812345766', 'Wanda', '2026-06-13 22:20:26'),
(90, 'xander.wang', '$2b$04$.wQOhyzH8ABEiXAmSFWG0.ngeILz59rXqZVilzToLr2MpVmD/zmBG', 'xander.wang@example.net', '+8618612345767', 'Xander', '2026-06-27 15:45:53'),
(91, 'yolanda.liu', '$2b$04$.wQOhyzH8ABEiXAmSFWG0.ngeILz59rXqZVilzToLr2MpVmD/zmBG', 'yolanda.liu@example.org', '+8613912345768', 'Yolanda', '2026-07-11 10:30:40'),
(92, 'zelda.zhou', '$2b$04$.wQOhyzH8ABEiXAmSFWG0.ngeILz59rXqZVilzToLr2MpVmD/zmBG', 'zelda.zhou@example.com', '+6597890123', 'Zelda', '2026-07-25 12:15:17'),
(93, 'aaron.huang', '$2b$04$.wQOhyzH8ABEiXAmSFWG0.ngeILz59rXqZVilzToLr2MpVmD/zmBG', 'aaron.huang@example.net', '+8615512345770', 'Aaron', '2026-08-08 19:50:34'),
(94, 'beatrice.chen', '$2b$04$.wQOhyzH8ABEiXAmSFWG0.ngeILz59rXqZVilzToLr2MpVmD/zmBG', 'beatrice.chen@example.com', '+8613812345771', 'Beatrice', '2026-08-21 21:35:51'),
(95, 'chris.wang', '$2b$04$.wQOhyzH8ABEiXAmSFWG0.ngeILz59rXqZVilzToLr2MpVmD/zmBG', 'chris.wang@example.org', '+8618612345772', NULL, '2026-09-03 14:20:28'),
(96, 'doris.liu', '$2b$04$.wQOhyzH8ABEiXAmSFWG0.ngeILz59rXqZVilzToLr2MpVmD/zmBG', 'doris.liu@example.com', '+8613912345773', 'Doris', '2026-09-04 17:45:15'),
(97, 'evan.zhou', '$2b$04$.wQOhyzH8ABEiXAmSFWG0.ngeILz59rXqZVilzToLr2MpVmD/zmBG', 'evan.zhou@example.net', '+6598901234', 'Evan', '2026-09-05 20:30:42'),
(98, 'faith.huang', '$2b$04$.wQOhyzH8ABEiXAmSFWG0.ngeILz59rXqZVilzToLr2MpVmD/zmBG', 'faith.huang@example.com', '+8615512345775', 'Faith', '2026-09-06 23:15:09'),
(99, 'gary.chen', '$2b$04$.wQOhyzH8ABEiXAmSFWG0.ngeILz59rXqZVilzToLr2MpVmD/zmBG', 'gary.chen@example.org', '+8613812345776', 'Gary', '2026-09-07 11:40:36'),
(100, 'heidi.wang', '$2b$04$.wQOhyzH8ABEiXAmSFWG0.ngeILz59rXqZVilzToLr2MpVmD/zmBG', 'heidi.wang@example.com', '+8618612345777', 'Heidi', '2026-09-08 08:25:23');

-- =============================================================================
-- 二、products 商品表（100条）
-- =============================================================================

INSERT INTO products (id, name, description, category, price, stock, status) VALUES
(1001, 'iPhone 17', 'Apple latest flagship smartphone with A19 chip', 'phone', 5999.00, 120, 'ON_SALE'),
(1002, 'iPhone 17 Pro', 'Apple Pro flagship with titanium design', 'phone', 7999.00, 86, 'ON_SALE'),
(1003, 'iPhone 17 Pro Max', 'Apple largest flagship with best camera', 'phone', 9999.00, 50, 'ON_SALE'),
(1004, 'Samsung Galaxy S26', 'Samsung flagship with AI features', 'phone', 5499.00, 95, 'ON_SALE'),
(1005, 'Samsung Galaxy S26 Ultra', 'Samsung premium flagship with S Pen', 'phone', 8999.00, 45, 'ON_SALE'),
(1006, 'Google Pixel 11', 'Google pure Android experience', 'phone', 4299.00, 68, 'ON_SALE'),
(1007, 'Google Pixel 11 Pro', 'Google Pro with advanced AI camera', 'phone', 6499.00, 32, 'ON_SALE'),
(1008, 'Xiaomi 15 Ultra', 'Xiaomi flagship with Leica camera', 'phone', 5999.00, 0, 'ON_SALE'),
(1009, 'OnePlus 13', 'OnePlus performance flagship', 'phone', 3999.00, 150, 'ON_SALE'),
(1010, 'OPPO Find X8', 'OPPO flagship with MariSilicon chip', 'phone', 4499.00, 55, 'ON_SALE'),
(1011, 'MacBook Air 13 M4', 'Apple ultra-thin laptop with M4 chip', 'computer', 7999.00, 80, 'ON_SALE'),
(1012, 'MacBook Air 15 M4', 'Apple larger ultra-thin laptop', 'computer', 9999.00, 60, 'ON_SALE'),
(1013, 'MacBook Pro 14 M4', 'Apple professional laptop', 'computer', 12999.00, 40, 'ON_SALE'),
(1014, 'MacBook Pro 16 M4 Pro', 'Apple largest Pro laptop', 'computer', 15999.00, 25, 'ON_SALE'),
(1015, 'Dell XPS 14', 'Dell premium ultrabook', 'computer', 11999.00, 35, 'ON_SALE'),
(1016, 'Dell XPS 16', 'Dell flagship ultrabook', 'computer', 14999.00, 20, 'ON_SALE'),
(1017, 'Lenovo ThinkPad X1 Carbon', 'Lenovo business flagship', 'computer', 12999.00, 28, 'ON_SALE'),
(1018, 'Lenovo ThinkPad T14s', 'Lenovo business laptop', 'computer', 8999.00, 42, 'ON_SALE'),
(1019, 'HP EliteBook 1040', 'HP business premium laptop', 'computer', 10999.00, 18, 'ON_SALE'),
(1020, 'ASUS ROG Zephyrus G14', 'ASUS gaming ultrabook', 'computer', 9999.00, 0, 'ON_SALE'),
(1021, 'iPad Air 11 M3', 'Apple mid-range tablet', 'tablet', 4799.00, 100, 'ON_SALE'),
(1022, 'iPad Pro 11 M4', 'Apple Pro tablet', 'tablet', 7999.00, 65, 'ON_SALE'),
(1023, 'iPad Pro 13 M4', 'Apple largest Pro tablet', 'tablet', 9999.00, 40, 'ON_SALE'),
(1024, 'iPad Mini 7', 'Apple compact tablet', 'tablet', 3999.00, 85, 'ON_SALE'),
(1025, 'Samsung Galaxy Tab S10', 'Samsung flagship tablet', 'tablet', 5499.00, 50, 'ON_SALE'),
(1026, 'Samsung Galaxy Tab S10 Ultra', 'Samsung largest tablet', 'tablet', 7999.00, 30, 'ON_SALE'),
(1027, 'Xiaomi Pad 7 Pro', 'Xiaomi flagship tablet', 'tablet', 2999.00, 75, 'ON_SALE'),
(1028, 'Microsoft Surface Pro 10', 'Microsoft 2-in-1 flagship', 'tablet', 8999.00, 22, 'ON_SALE'),
(1029, 'Microsoft Surface Go 4', 'Microsoft affordable 2-in-1', 'tablet', 3999.00, 55, 'ON_SALE'),
(1030, 'Lenovo Tab P12 Pro', 'Lenovo flagship tablet', 'tablet', 4499.00, 0, 'ON_SALE'),
(1031, 'AirPods Pro 3', 'Apple premium wireless earbuds', 'audio', 1899.00, 200, 'ON_SALE'),
(1032, 'AirPods 4', 'Apple wireless earbuds', 'audio', 999.00, 180, 'ON_SALE'),
(1033, 'AirPods Max 2', 'Apple premium over-ear headphones', 'audio', 3999.00, 60, 'ON_SALE'),
(1034, 'Sony WH-1000XM6', 'Sony flagship noise-canceling headphones', 'audio', 2799.00, 90, 'ON_SALE'),
(1035, 'Sony WF-1000XM6', 'Sony flagship wireless earbuds', 'audio', 1999.00, 70, 'ON_SALE'),
(1036, 'Bose QuietComfort Ultra', 'Bose premium headphones', 'audio', 3299.00, 45, 'ON_SALE'),
(1037, 'Bose QC Earbuds II', 'Bose wireless earbuds', 'audio', 1799.00, 65, 'ON_SALE'),
(1038, 'Sennheiser Momentum 4', 'Sennheiser premium headphones', 'audio', 2499.00, 35, 'ON_SALE'),
(1039, 'Samsung Galaxy Buds3 Pro', 'Samsung premium earbuds', 'audio', 1299.00, 120, 'ON_SALE'),
(1040, 'Xiaomi Buds 5 Pro', 'Xiaomi premium earbuds', 'audio', 799.00, 95, 'ON_SALE'),
(1041, 'Apple Watch Series 12', 'Apple latest smartwatch', 'wearable', 2999.00, 150, 'ON_SALE'),
(1042, 'Apple Watch Ultra 3', 'Apple premium sports watch', 'wearable', 4999.00, 50, 'ON_SALE'),
(1043, 'Apple Watch SE 3', 'Apple affordable smartwatch', 'wearable', 1999.00, 110, 'ON_SALE'),
(1044, 'Samsung Galaxy Watch 8', 'Samsung flagship smartwatch', 'wearable', 2299.00, 80, 'ON_SALE'),
(1045, 'Samsung Galaxy Watch 8 Classic', 'Samsung premium smartwatch', 'wearable', 2999.00, 40, 'ON_SALE'),
(1046, 'Google Pixel Watch 3', 'Google smartwatch', 'wearable', 2199.00, 55, 'ON_SALE'),
(1047, 'Garmin Forerunner 965', 'Garmin running watch', 'wearable', 3999.00, 25, 'ON_SALE'),
(1048, 'Garmin Fenix 8', 'Garmin outdoor watch', 'wearable', 5999.00, 15, 'ON_SALE'),
(1049, 'Huawei Watch GT 5', 'Huawei sports watch', 'wearable', 1499.00, 90, 'ON_SALE'),
(1050, 'Xiaomi Watch S4', 'Xiaomi smartwatch', 'wearable', 799.00, 0, 'ON_SALE'),
(1051, 'Sony Alpha A7 V', 'Sony full-frame mirrorless camera', 'camera', 18999.00, 12, 'ON_SALE'),
(1052, 'Sony Alpha A7C II', 'Sony compact full-frame camera', 'camera', 13999.00, 18, 'ON_SALE'),
(1053, 'Canon EOS R6 III', 'Canon full-frame mirrorless', 'camera', 16999.00, 15, 'ON_SALE'),
(1054, 'Canon EOS R8', 'Canon entry full-frame camera', 'camera', 8999.00, 25, 'ON_SALE'),
(1055, 'Nikon Z8', 'Nikon flagship mirrorless', 'camera', 21999.00, 10, 'ON_SALE'),
(1056, 'Nikon Z6 III', 'Nikon mid-range mirrorless', 'camera', 14999.00, 14, 'ON_SALE'),
(1057, 'Fujifilm X-T5', 'Fujifilm APS-C flagship', 'camera', 11999.00, 22, 'ON_SALE'),
(1058, 'GoPro Hero 13 Black', 'GoPro action camera', 'camera', 3299.00, 45, 'ON_SALE'),
(1059, 'DJI Osmo Pocket 3', 'DJI handheld camera', 'camera', 2499.00, 38, 'ON_SALE'),
(1060, 'Insta360 X4', 'Insta360 panoramic camera', 'camera', 2999.00, 0, 'ON_SALE'),
(1061, 'Nintendo Switch 2', 'Nintendo next-gen console', 'gaming', 2499.00, 0, 'ON_SALE'),
(1062, 'PlayStation 5 Pro', 'Sony next-gen console', 'gaming', 3999.00, 8, 'ON_SALE'),
(1063, 'Xbox Series X2', 'Microsoft next-gen console', 'gaming', 3499.00, 12, 'ON_SALE'),
(1064, 'Steam Deck OLED', 'Valve gaming handheld', 'gaming', 3899.00, 20, 'ON_SALE'),
(1065, 'PlayStation DualSense 2', 'PS5 controller', 'gaming', 499.00, 150, 'ON_SALE'),
(1066, 'Xbox Elite Controller 2', 'Xbox premium controller', 'gaming', 999.00, 55, 'ON_SALE'),
(1067, 'Nintendo Switch Pro Controller', 'Switch premium controller', 'gaming', 459.00, 80, 'ON_SALE'),
(1068, 'Logitech G Pro X Superlight 3', 'Logitech gaming mouse', 'gaming', 999.00, 75, 'ON_SALE'),
(1069, 'Razer DeathAdder V4', 'Razer gaming mouse', 'gaming', 399.00, 95, 'ON_SALE'),
(1070, 'Corsair K100 Air', 'Corsair wireless keyboard', 'gaming', 1299.00, 0, 'ON_SALE'),
(1071, 'Logitech MX Master 4', 'Logitech productivity mouse', 'accessory', 799.00, 120, 'ON_SALE'),
(1072, 'Logitech MX Keys S', 'Logitech wireless keyboard', 'accessory', 599.00, 100, 'ON_SALE'),
(1073, 'Apple Magic Keyboard', 'Apple wireless keyboard', 'accessory', 999.00, 65, 'ON_SALE'),
(1074, 'Apple Magic Mouse 3', 'Apple wireless mouse', 'accessory', 799.00, 70, 'OFF_SHELF'),
(1075, 'Anker 735 Charger', 'Anker 65W GaN charger', 'accessory', 199.00, 200, 'ON_SALE'),
(1076, 'Anker PowerCore 26800', 'Anker portable battery', 'accessory', 299.00, 150, 'ON_SALE'),
(1077, 'Samsung T9 Portable SSD 2TB', 'Samsung portable SSD', 'accessory', 1299.00, 45, 'OFF_SHELF'),
(1078, 'WD My Passport 2TB', 'WD portable HDD', 'accessory', 499.00, 80, 'OFF_SHELF'),
(1079, 'SanDisk Extreme Pro 1TB', 'SanDisk portable SSD', 'accessory', 799.00, 60, 'ON_SALE'),
(1080, 'Logitech C920s Pro HD', 'Logitech webcam', 'accessory', 399.00, 0, 'ON_SALE'),
(1081, 'Apple HomePod mini', 'Apple smart speaker', 'home', 699.00, 90, 'ON_SALE'),
(1082, 'Apple HomePod 2', 'Apple premium smart speaker', 'home', 2299.00, 35, 'ON_SALE'),
(1083, 'Sonos One SL', 'Sonos smart speaker', 'home', 1799.00, 40, 'OFF_SHELF'),
(1084, 'Sonos Arc', 'Sonos soundbar', 'home', 6999.00, 15, 'ON_SALE'),
(1085, 'Amazon Echo Show 10', 'Amazon smart display', 'home', 2499.00, 30, 'OFF_SHELF'),
(1086, 'Google Nest Hub 3', 'Google smart display', 'home', 999.00, 55, 'ON_SALE'),
(1087, 'Philips Hue Starter Kit', 'Philips smart lighting', 'home', 799.00, 45, 'ON_SALE'),
(1088, 'Xiaomi Smart Screen 86', 'Xiaomi smart TV 86 inch', 'home', 8999.00, 10, 'OFF_SHELF'),
(1089, 'Ring Video Doorbell Pro 2', 'Ring smart doorbell', 'home', 1599.00, 35, 'ON_SALE'),
(1090, 'Dyson V20 Vacuum', 'Dyson cordless vacuum', 'home', 4999.00, 0, 'ON_SALE'),
(1091, 'Canon TS3530 Printer', 'Canon wireless printer', 'office', 599.00, 60, 'ON_SALE'),
(1092, 'HP LaserJet Pro MFP', 'HP laser printer', 'office', 1999.00, 30, 'OFF_SHELF'),
(1093, 'Epson L3250 Printer', 'Epson ink tank printer', 'office', 1299.00, 45, 'OFF_SHELF'),
(1094, 'Logitech Rally Camera', 'Logitech conference camera', 'office', 5999.00, 20, 'ON_SALE'),
(1095, 'Jabra PanaCast 50', 'Jabra conference camera', 'office', 8999.00, 12, 'OFF_SHELF'),
(1096, 'Dell U2723QE Monitor', 'Dell 4K USB-C monitor', 'office', 3999.00, 35, 'OFF_SHELF'),
(1097, 'LG 27UK850 Monitor', 'LG 4K monitor', 'office', 3499.00, 28, 'OFF_SHELF'),
(1098, 'BenQ ScreenBar Plus', 'BenQ monitor light', 'office', 799.00, 70, 'OFF_SHELF'),
(1099, 'Autonomous ErgoChair 2', 'Autonomous ergonomic chair', 'office', 2999.00, 25, 'OFF_SHELF'),
(1100, 'Xiaomi Smart Desk', 'Xiaomi electric standing desk', 'office', 1999.00, 0, 'OFF_SHELF');

-- =============================================================================
-- 三、cart_items 购物车表（100条）
-- =============================================================================

INSERT INTO cart_items (id, user_id, product_id, quantity, unit_price, created_at) VALUES
(1, 1, 1001, 1, 5999.00, '2026-09-08 10:30:00'),
(2, 1, 1031, 2, 1899.00, '2026-09-08 10:31:00'),
(3, 2, 1011, 1, 7999.00, '2026-09-07 15:20:00'),
(4, 2, 1071, 1, 799.00, '2026-09-07 15:22:00'),
(5, 3, 1041, 1, 2999.00, '2026-09-06 09:45:00'),
(6, 4, 1004, 1, 5499.00, '2026-09-05 18:10:00'),
(7, 5, 1012, 1, 9999.00, '2026-09-04 14:30:00'),
(8, 6, 1021, 1, 4799.00, '2026-09-03 20:15:00'),
(9, 7, 1032, 1, 999.00, '2026-09-02 11:50:00'),
(10, 8, 1051, 1, 18999.00, '2026-09-01 16:40:00'),
(11, 9, 1061, 1, 2499.00, '2026-08-30 08:25:00'),
(12, 10, 1072, 1, 599.00, '2026-08-28 13:35:00'),
(13, 11, 1081, 1, 699.00, '2026-08-26 19:20:00'),
(14, 12, 1091, 1, 599.00, '2026-08-24 22:45:00'),
(15, 13, 1006, 1, 4299.00, '2026-08-22 07:10:00'),
(16, 14, 1022, 1, 7999.00, '2026-08-20 12:55:00'),
(17, 15, 1033, 1, 3999.00, '2026-08-18 17:30:00'),
(18, 16, 1042, 1, 4999.00, '2026-08-16 21:15:00'),
(19, 17, 1052, 1, 13999.00, '2026-08-14 10:40:00'),
(20, 18, 1062, 1, 3999.00, '2026-08-12 15:25:00'),
(21, 19, 1073, 1, 999.00, '2026-08-10 09:50:00'),
(22, 20, 1084, 1, 6999.00, '2026-08-08 14:35:00'),
(23, 21, 1094, 1, 5999.00, '2026-08-06 18:20:00'),
(24, 22, 1002, 1, 7999.00, '2026-08-04 11:45:00'),
(25, 23, 1013, 1, 12999.00, '2026-08-02 20:30:00'),
(26, 24, 1023, 1, 9999.00, '2026-07-31 08:15:00'),
(27, 25, 1034, 1, 2799.00, '2026-07-29 13:50:00'),
(28, 26, 1043, 1, 1999.00, '2026-07-27 17:25:00'),
(29, 27, 1053, 1, 16999.00, '2026-07-25 22:40:00'),
(30, 28, 1063, 1, 3499.00, '2026-07-23 10:55:00'),
(31, 29, 1074, 1, 799.00, '2026-07-21 15:20:00'),
(32, 30, 1085, 1, 2499.00, '2026-07-19 19:35:00'),
(33, 31, 1096, 1, 3999.00, '2026-07-17 08:40:00'),
(34, 32, 1005, 1, 8999.00, '2026-07-15 12:05:00'),
(35, 33, 1014, 1, 15999.00, '2026-07-13 16:30:00'),
(36, 34, 1024, 1, 3999.00, '2026-07-11 21:45:00'),
(37, 35, 1035, 1, 1999.00, '2026-07-09 09:20:00'),
(38, 36, 1044, 1, 2299.00, '2026-07-07 13:55:00'),
(39, 37, 1054, 1, 8999.00, '2026-07-05 18:10:00'),
(40, 38, 1064, 1, 3899.00, '2026-07-03 22:25:00'),
(41, 39, 1075, 1, 199.00, '2026-07-01 11:40:00'),
(42, 40, 1086, 1, 999.00, '2026-06-29 15:05:00'),
(43, 41, 1097, 1, 3499.00, '2026-06-27 20:30:00'),
(44, 42, 1006, 1, 4299.00, '2026-06-25 08:15:00'),
(45, 43, 1015, 1, 11999.00, '2026-06-23 12:40:00'),
(46, 44, 1025, 1, 5499.00, '2026-06-21 17:05:00'),
(47, 45, 1036, 1, 3299.00, '2026-06-19 21:20:00'),
(48, 46, 1045, 1, 2999.00, '2026-06-17 10:35:00'),
(49, 47, 1055, 1, 21999.00, '2026-06-15 14:50:00'),
(50, 48, 1065, 2, 499.00, '2026-06-13 19:15:00'),
(51, 49, 1076, 1, 299.00, '2026-06-11 23:40:00'),
(52, 50, 1087, 1, 799.00, '2026-06-09 12:05:00'),
(53, 51, 1098, 1, 799.00, '2026-06-07 16:20:00'),
(54, 52, 1007, 1, 6499.00, '2026-06-05 20:45:00'),
(55, 53, 1016, 1, 14999.00, '2026-06-03 09:30:00'),
(56, 54, 1026, 1, 7999.00, '2026-06-01 13:55:00'),
(57, 55, 1037, 1, 1799.00, '2026-05-30 18:10:00'),
(58, 56, 1046, 1, 2199.00, '2026-05-28 22:35:00'),
(59, 57, 1056, 1, 14999.00, '2026-05-26 11:00:00'),
(60, 58, 1066, 1, 999.00, '2026-05-24 15:25:00'),
(61, 59, 1077, 1, 1299.00, '2026-05-22 19:50:00'),
(62, 60, 1088, 1, 8999.00, '2026-05-20 08:15:00'),
(63, 61, 1099, 1, 2999.00, '2026-05-18 12:40:00'),
(64, 62, 1008, 1, 5999.00, '2026-05-16 17:05:00'),
(65, 63, 1017, 1, 12999.00, '2026-05-14 21:30:00'),
(66, 64, 1027, 1, 2999.00, '2026-05-12 10:45:00'),
(67, 65, 1038, 1, 2499.00, '2026-05-10 15:10:00'),
(68, 66, 1047, 1, 3999.00, '2026-05-08 19:35:00'),
(69, 67, 1057, 1, 11999.00, '2026-05-06 23:50:00'),
(70, 68, 1067, 1, 459.00, '2026-05-04 12:15:00'),
(71, 69, 1078, 1, 499.00, '2026-05-02 16:40:00'),
(72, 70, 1089, 1, 1599.00, '2026-04-30 21:05:00'),
(73, 71, 1009, 1, 3999.00, '2026-04-28 09:30:00'),
(74, 72, 1018, 1, 8999.00, '2026-04-26 13:55:00'),
(75, 73, 1028, 1, 8999.00, '2026-04-24 18:20:00'),
(76, 74, 1039, 1, 1299.00, '2026-04-22 22:45:00'),
(77, 75, 1048, 1, 5999.00, '2026-04-20 11:10:00'),
(78, 76, 1058, 1, 3299.00, '2026-04-18 15:35:00'),
(79, 77, 1068, 1, 999.00, '2026-04-16 20:00:00'),
(80, 78, 1079, 1, 799.00, '2026-04-14 08:25:00'),
(81, 79, 1090, 1, 4999.00, '2026-04-12 12:50:00'),
(82, 80, 1010, 1, 4499.00, '2026-04-10 17:15:00'),
(83, 81, 1019, 1, 10999.00, '2026-04-08 21:40:00'),
(84, 82, 1029, 1, 3999.00, '2026-04-06 10:05:00'),
(85, 83, 1030, 1, 4499.00, '2026-04-04 14:30:00'),
(86, 84, 1040, 1, 799.00, '2026-04-02 18:55:00'),
(87, 85, 1050, 1, 799.00, '2026-03-31 23:20:00'),
(88, 86, 1060, 1, 2999.00, '2026-03-29 11:45:00'),
(89, 87, 1070, 1, 1299.00, '2026-03-27 16:10:00'),
(90, 88, 1080, 1, 399.00, '2026-03-25 20:35:00'),
(91, 89, 1091, 1, 599.00, '2026-03-23 09:00:00'),
(92, 90, 1001, 1, 5999.00, '2026-03-21 13:25:00'),
(93, 91, 1011, 1, 7999.00, '2026-03-19 17:50:00'),
(94, 92, 1021, 1, 4799.00, '2026-03-17 22:15:00'),
(95, 93, 1031, 1, 1899.00, '2026-03-15 10:40:00'),
(96, 94, 1041, 1, 2999.00, '2026-03-13 15:05:00'),
(97, 95, 1051, 1, 18999.00, '2026-03-11 19:30:00'),
(98, 96, 1009, 1, 3999.00, '2026-03-09 23:55:00'),
(99, 97, 1071, 1, 799.00, '2026-03-07 12:20:00'),
(100, 98, 1081, 1, 699.00, '2026-03-05 16:45:00');

-- =============================================================================
-- 四、orders 订单表（100条）
-- =============================================================================

INSERT INTO orders (id, order_no, user_id, total_amount, order_status, payment_status, receiver, remark, created_at) VALUES
(1, 'AS202609081005231847', 1, 5999.00, 'PAID', 'MOCK_SUCCESS', '{"name":"Alex Chen","phone":"+8613812345678","province":"Guangdong","city":"Shenzhen","district":"Nanshan","address":"88 Keyuan Road"}', NULL, '2026-09-08 10:05:23'),
(2, 'AS202609071423558921', 2, 5999.00, 'PAID', 'MOCK_SUCCESS', '{"name":"Michael Wang","phone":"+8618612345679","province":"Shanghai","city":"Shanghai","district":"Pudong","address":"100 Century Avenue"}', 'Please deliver after 6 PM', '2026-09-07 14:23:55'),
(3, 'AS202609061837412536', 3, 2999.00, 'PAID', 'MOCK_SUCCESS', '{"name":"Emily Zhang","phone":"+8613912345680","province":"Beijing","city":"Beijing","district":"Chaoyang","address":"15 Jianguo Road"}', NULL, '2026-09-06 18:37:41'),
(4, 'AS202609051956723412', 4, 5499.00, 'PAID', 'MOCK_SUCCESS', '{"name":"Kevin Liu","phone":"+6591234567","province":"Singapore","city":"Singapore","district":"Marina Bay","address":"1 Marina Boulevard"}', 'Leave at reception', '2026-09-05 19:56:23'),
(5, 'AS202609042315894731', 5, 9999.00, 'PAID', 'MOCK_SUCCESS', '{"name":"Sophia Lin","phone":"+8615512345698","province":"Guangdong","city":"Guangzhou","district":"Tianhe","address":"233 Tianhe Road"}', NULL, '2026-09-04 23:15:89'),
(6, 'AS202609032126547892', 6, 4799.00, 'PAID', 'MOCK_SUCCESS', '{"name":"Jason Wu","phone":"+8618612345683","province":"Zhejiang","city":"Hangzhou","district":"Xihu","address":"88 West Lake Road"}', 'Gift order', '2026-09-03 21:26:54'),
(7, 'AS202609021847362197', 7, 999.00, 'PENDING_PAYMENT', 'MOCK_PENDING', '{"name":"Olivia Zhou","phone":"+8613912345684","province":"Jiangsu","city":"Suzhou","district":"Gusu","address":"66 Guanqian Street"}', NULL, '2026-09-02 18:47:36'),
(8, 'AS202609011923478521', 8, 18999.00, 'PAID', 'MOCK_SUCCESS', '{"name":"Daniel Huang","phone":"+6592345678","province":"Singapore","city":"Singapore","district":"Orchard","address":"391 Orchard Road"}', 'Call before delivery', '2026-09-01 19:23:47'),
(9, 'AS202608311456782391', 9, 2499.00, 'PAID', 'MOCK_SUCCESS', '{"name":"Mia Li","phone":"+8613812345686","province":"Sichuan","city":"Chengdu","district":"Wuhou","address":"88 Wuhou Avenue"}', NULL, '2026-08-31 14:56:23'),
(10, 'AS202608301823451672', 10, 599.00, 'PAY_FAILED', 'MOCK_FAILED', '{"name":"Leo Tanaka","phone":"+819012345678","province":"Japan","city":"Tokyo","district":"Shibuya","address":"1-2-3 Shibuya"}', NULL, '2026-08-30 18:23:45'),
(11, 'AS202608291534896231', 11, 3999.00, 'PAID', 'MOCK_SUCCESS', '{"name":"Grace Kim","phone":"+8210123456789","province":"Korea","city":"Seoul","district":"Gangnam","address":"521 Teheran Road"}', 'Do not bend package', '2026-08-29 15:34:23'),
(12, 'AS202608281745623481', 12, 599.00, 'PENDING_PAYMENT', 'MOCK_PENDING', '{"name":"Ethan Yeo","phone":"+6598765432","province":"Singapore","city":"Singapore","district":"Bugis","address":"200 Victoria Street"}', NULL, '2026-08-28 17:45:23'),
(13, 'AS202608271856934721', 13, 3999.00, 'PAID', 'MOCK_SUCCESS', '{"name":"Wendy Lee","phone":"+8613912345690","province":"Guangdong","city":"Shenzhen","district":"Futian","address":"188 Fuhua Road"}', NULL, '2026-08-27 18:56:23'),
(14, 'AS202608261923874152', 14, 7999.00, 'PAID', 'MOCK_SUCCESS', '{"name":"Richard Zhou","phone":"+8618612345691","province":"Zhejiang","city":"Hangzhou","district":"Binjiang","address":"77 Binsheng Road"}', 'Leave at front door', '2026-08-26 19:23:23'),
(15, 'AS202608251852319472', 15, 8999.00, 'PAID', 'MOCK_SUCCESS', '{"name":"Amanda Chen","phone":"+254712345678","province":"Kenya","city":"Nairobi","district":"Westlands","address":"100 Waiyaki Way"}', NULL, '2026-08-25 18:52:23'),
(16, 'AS202608241734628912', 16, 7999.00, 'PAY_FAILED', 'MOCK_FAILED', '{"name":"Brian Wang","phone":"+8615512345693","province":"Fujian","city":"Xiamen","district":"Siming","address":"68 Hubin Road"}', NULL, '2026-08-24 17:34:23'),
(17, 'AS202608231645379281', 17, 3999.00, 'PAID', 'MOCK_SUCCESS', '{"name":"Charlotte Liu","phone":"+8613912345694","province":"Hubei","city":"Wuhan","district":"Wuchang","address":"368 Wuluo Road"}', NULL, '2026-08-23 16:45:23'),
(18, 'AS202608221856921741', 18, 13999.00, 'PAID', 'MOCK_SUCCESS', '{"name":"David Wu","phone":"+6593456789","province":"Singapore","city":"Singapore","district":"Clarke Quay","address":"3 River Valley Road"}', 'Fragile, handle with care', '2026-08-22 18:56:23'),
(19, 'AS202608211723465812', 19, 999.00, 'PENDING_PAYMENT', 'MOCK_PENDING', '{"name":"Emily Brown","phone":"+8613812345696","province":"Guangdong","city":"Dongguan","district":"Nancheng","address":"99 Hongfu Road"}', NULL, '2026-08-21 17:23:23'),
(20, 'AS202608201934872351', 20, 6999.00, 'PAID', 'MOCK_SUCCESS', '{"name":"Felix Zhang","phone":"+8618612345697","province":"Jiangsu","city":"Nanjing","district":"Xuanwu","address":"188 Zhongshan Road"}', NULL, '2026-08-20 19:34:23'),
(21, 'AS202608191823564192', 21, 5999.00, 'PAID', 'MOCK_SUCCESS', '{"name":"Gabriella Liu","phone":"+8615512345698","province":"Guangdong","city":"Shenzhen","district":"Nanshan","address":"100 Software Park"}', 'Morning delivery preferred', '2026-08-19 18:23:23'),
(22, 'AS202608181745923472', 22, 9999.00, 'PAY_FAILED', 'MOCK_FAILED', '{"name":"Henry Wu","phone":"+8613912345699","province":"Shandong","city":"Qingdao","district":"Shinan","address":"88 Wusi Road"}', NULL, '2026-08-18 17:45:23'),
(23, 'AS202608171856347821', 23, 1799.00, 'PAID', 'MOCK_SUCCESS', '{"name":"Irene Zhou","phone":null,"province":"Zhejiang","city":"Ningbo","district":"Yinzhou","address":"168 Yinxian Road"}', NULL, '2026-08-17 18:56:23'),
(24, 'AS202608161923678541', 24, 799.00, 'PAID', 'MOCK_SUCCESS', '{"name":"Jacob Huang","phone":"+6594567890","province":"Singapore","city":"Singapore","district":"Sentosa","address":"50 Resorts World"}', 'Hotel delivery', '2026-08-16 19:23:23'),
(25, 'AS202608151834296172', 25, 199.00, 'PENDING_PAYMENT', 'MOCK_PENDING', '{"name":"Karen Lin","phone":"+8613812345702","province":"Guangxi","city":"Nanning","district":"Qingxiu","address":"66 Minzu Road"}', NULL, '2026-08-15 18:34:23'),
(26, 'AS202608141756823492', 26, 2999.00, 'PAID', 'MOCK_SUCCESS', '{"name":"Lawrence Chen","phone":"+8618612345703","province":"Henan","city":"Zhengzhou","district":"Jinshui","address":"188 Zhengdong Road"}', NULL, '2026-08-14 17:56:23'),
(27, 'AS202608131847934721', 27, 999.00, 'PAID', 'MOCK_SUCCESS', '{"name":"Monica Wang","phone":"+8613912345704","province":"Shaanxi","city":"Xian","district":"Beilin","address":"99 South Street"}', 'Evening delivery', '2026-08-13 18:47:23'),
(28, 'AS202608121923451672', 28, 499.00, 'PAY_FAILED', 'MOCK_FAILED', '{"name":"Nicholas Liu","phone":"+6595678901","province":"Singapore","city":"Singapore","district":"Changi","address":"78 Changi Airport"}', NULL, '2026-08-12 19:23:23'),
(29, 'AS202608111834782392', 29, 999.00, 'PAID', 'MOCK_SUCCESS', '{"name":"Oliver Zhou","phone":"+8615512345706","province":"Yunnan","city":"Kunming","district":"Chenggong","address":"168 Chuncheng Road"}', NULL, '2026-08-11 18:34:23'),
(30, 'AS202608101956234892', 30, 2499.00, 'PAID', 'MOCK_SUCCESS', '{"name":"Pamela Huang","phone":"+8613812345707","province":"Hainan","city":"Sanya","district":"Jiyang","address":"199 Yalong Bay"}', NULL, '2026-08-10 19:56:23'),
(31, 'AS202608091845671921', 31, 1999.00, 'PENDING_PAYMENT', 'MOCK_PENDING', '{"name":"Quinn Chen","phone":"+8618612345708","province":"Anhui","city":"Hefei","district":"Shushan","address":"288 Shushan Road"}', NULL, '2026-08-09 18:45:23'),
(32, 'AS202608081756389241', 32, 7999.00, 'PAID', 'MOCK_SUCCESS', '{"name":"Rachel Wang","phone":"+8613912345709","province":"Jilin","city":"Changchun","district":"Chaoyang","address":"99 Renmin Street"}', NULL, '2026-08-08 17:56:23'),
(33, 'AS202608071923847561', 33, 1299.00, 'PAID', 'MOCK_SUCCESS', '{"name":"Stephen Liu","phone":"+6596789012","province":"Singapore","city":"Singapore","district":"Jurong","address":"200 Jurong East"}', 'Business address', '2026-08-07 19:23:23'),
(34, 'AS202608061834962172', 34, 5499.00, 'PAID', 'MOCK_SUCCESS', '{"name":"Tina Zhou","phone":"+8615512345711","province":"Guangdong","city":"Shenzhen","district":"Baoan","address":"66 Qianhai Road"}', NULL, '2026-08-06 18:34:23'),
(35, 'AS202608051756478291', 35, 3999.00, 'PAY_FAILED', 'MOCK_FAILED', '{"name":"Ulrich Huang","phone":"+8613812345712","province":"Liaoning","city":"Dalian","district":"Zhongshan","address":"188 Victory Road"}', NULL, '2026-08-05 17:56:23'),
(36, 'AS202608041923561841', 36, 8999.00, 'PAID', 'MOCK_SUCCESS', '{"name":"Vivian Chen","phone":"+8618612345713","province":"Jiangxi","city":"Nanchang","district":"Honggutan","address":"168 Honggu Road"}', NULL, '2026-08-04 19:23:23'),
(37, 'AS202608031845723492', 37, 699.00, 'PENDING_PAYMENT', 'MOCK_PENDING', '{"name":"Walter Wang","phone":null,"province":"Shanxi","city":"Taiyuan","district":"Yingze","address":"188 Jinyuan Road"}', NULL, '2026-08-03 18:45:23'),
(38, 'AS202608021756894231', 38, 2299.00, 'PAID', 'MOCK_SUCCESS', '{"name":"Xiaomei Liu","phone":"+6597890123","province":"Singapore","city":"Singapore","district":"Bishan","address":"88 Bishan Street"}', NULL, '2026-08-02 17:56:23'),
(39, 'AS202608011923478522', 39, 799.00, 'PAID', 'MOCK_SUCCESS', '{"name":"Yifan Zhou","phone":"+8615512345716","province":"Gansu","city":"Lanzhou","district":"Chengguan","address":"99 Donggang Road"}', NULL, '2026-08-01 19:23:23'),
(40, 'AS202607311834672912', 40, 11999.00, 'PAID', 'MOCK_SUCCESS', '{"name":"Zoe Huang","phone":"+8613812345717","province":"Hebei","city":"Shijiazhuang","district":"Yuhua","address":"168 Yuhua Road"}', NULL, '2026-07-31 18:34:23'),
(41, 'AS202607301756489231', 41, 6999.00, 'PAY_FAILED', 'MOCK_FAILED', '{"name":"Andrew Chen","phone":"+8618612345718","province":"Heilongjiang","city":"Harbin","district":"Daoli","address":"88 Zhongyang Street"}', NULL, '2026-07-30 17:56:23'),
(42, 'AS202607291923845671', 42, 499.00, 'PAID', 'MOCK_SUCCESS', '{"name":"Bella Wang","phone":"+8613912345719","province":"Inner Mongolia","city":"Hohhot","district":"Saihan","address":"168 Xilin Road"}', NULL, '2026-07-29 19:23:23'),
(43, 'AS202607281834296172', 43, 1799.00, 'PENDING_PAYMENT', 'MOCK_PENDING', '{"name":"Carlos Liu","phone":"+6598901234","province":"Singapore","city":"Singapore","district":"Tampines","address":"5 Tampines Walk"}', NULL, '2026-07-28 18:34:23'),
(44, 'AS202607271756723481', 44, 7999.00, 'PAID', 'MOCK_SUCCESS', '{"name":"Diana Zhou","phone":"+8615512345721","province":"Tianjin","city":"Tianjin","district":"Heping","address":"66 Nanjing Road"}', NULL, '2026-07-27 17:56:23'),
(45, 'AS202607261923894561', 45, 1299.00, 'PAID', 'MOCK_SUCCESS', '{"name":"Eugene Huang","phone":"+8613812345722","province":"Ningxia","city":"Yinchuan","district":"Jinfeng","address":"188 Yinchuan Road"}', NULL, '2026-07-26 19:23:23'),
(46, 'AS202607251845672312', 46, 3999.00, 'PENDING_PAYMENT', 'MOCK_PENDING', '{"name":"Fiona Chen","phone":null,"province":"Qinghai","city":"Xining","district":"Chengxi","address":"99 Xinning Road"}', NULL, '2026-07-25 18:45:23'),
(47, 'AS202607241756389471', 47, 799.00, 'PAID', 'MOCK_SUCCESS', '{"name":"George Wang","phone":"+8613912345724","province":"Xinjiang","city":"Urumqi","district":"Tianshan","address":"168 Yanan Road"}', NULL, '2026-07-24 17:56:23'),
(48, 'AS202607231923451672', 48, 999.00, 'PAID', 'MOCK_SUCCESS', '{"name":"Hannah Liu","phone":"+6599012345","province":"Singapore","city":"Singapore","district":"Woodlands","address":"1 Woodlands Square"}', NULL, '2026-07-23 19:23:23'),
(49, 'AS202607221834782392', 49, 2999.00, 'PAY_FAILED', 'MOCK_FAILED', '{"name":"Ian Zhou","phone":"+8615512345726","province":"Tibet","city":"Lhasa","district":"Chengguan","address":"88 Beijing Road"}', NULL, '2026-07-22 18:34:23'),
(50, 'AS202607211756234892', 50, 599.00, 'PAID', 'MOCK_SUCCESS', '{"name":"Julia Huang","phone":"+8613812345727","province":"Guizhou","city":"Guiyang","district":"Guanshan","address":"168 Zhonghua Road"}', NULL, '2026-07-21 17:56:23'),
(51, 'AS202607201923678541', 51, 3999.00, 'PAID', 'MOCK_SUCCESS', '{"name":"Kevin Miller","phone":"+8618612345728","province":"Guangdong","city":"Shenzhen","district":"Longgang","address":"66 Longcheng Road"}', NULL, '2026-07-20 19:23:23'),
(52, 'AS202607191845923471', 52, 5999.00, 'PENDING_PAYMENT', 'MOCK_PENDING', '{"name":"Lisa Wang","phone":"+8613912345729","province":"Chongqing","city":"Chongqing","district":"Yuzhong","address":"188 Minzu Road"}', NULL, '2026-07-19 18:45:23'),
(53, 'AS202607181756347812', 53, 999.00, 'PAID', 'MOCK_SUCCESS', '{"name":"Mark Liu","phone":null,"province":"Sichuan","city":"Mianyang","district":"Fucheng","address":"99 Changqing Road"}', NULL, '2026-07-18 17:56:23'),
(54, 'AS202607171923894231', 54, 4999.00, 'PAID', 'MOCK_SUCCESS', '{"name":"Nancy Zhou","phone":"+8615512345731","province":"Hunan","city":"Changsha","district":"Yuelu","address":"168 Yuelu Road"}', NULL, '2026-07-17 19:23:23'),
(55, 'AS202607161845672391', 55, 1799.00, 'PAY_FAILED', 'MOCK_FAILED', '{"name":"Oscar Chen","phone":"+8613812345732","province":"Shandong","city":"Jinan","district":"Lixia","address":"88 Lixia Road"}', NULL, '2026-07-16 18:45:23'),
(56, 'AS202607151756489231', 56, 799.00, 'PAID', 'MOCK_SUCCESS', '{"name":"Patricia Wang","phone":"+8618612345733","province":"Jiangsu","city":"Suzhou","district":"Industrial Park","address":"168 Xinghu Road"}', NULL, '2026-07-15 17:56:23'),
(57, 'AS202607141923562172', 57, 5999.00, 'PAID', 'MOCK_SUCCESS', '{"name":"Queenie Liu","phone":"+6590123456","province":"Singapore","city":"Singapore","district":"Pasir Ris","address":"3 Pasir Ris Drive"}', NULL, '2026-07-14 19:23:23'),
(58, 'AS202607131845394721', 58, 11999.00, 'PENDING_PAYMENT', 'MOCK_PENDING', '{"name":"Robert Zhou","phone":"+8615512345735","province":"Guangdong","city":"Foshan","district":"Chancheng","address":"88 Zumiao Road"}', NULL, '2026-07-13 18:45:23'),
(59, 'AS202607121756278941', 59, 999.00, 'PAID', 'MOCK_SUCCESS', '{"name":"Sabrina Huang","phone":"+8613812345736","province":"Hainan","city":"Haikou","district":"Longhua","address":"66 Haixiu Road"}', NULL, '2026-07-12 17:56:23'),
(60, 'AS202607111923845671', 60, 8999.00, 'PAID', 'MOCK_SUCCESS', '{"name":"Tony Chen","phone":"+8618612345737","province":"Zhejiang","city":"Wenzhou","district":"Lucheng","address":"188 Xueyuan Road"}', NULL, '2026-07-11 19:23:23'),
(61, 'AS202607101845723492', 61, 499.00, 'PAY_FAILED', 'MOCK_FAILED', '{"name":"Ursula Wang","phone":null,"province":"Sichuan","city":"Leshan","district":"Shizhong","address":"99 Baihua Road"}', NULL, '2026-07-10 18:45:23'),
(62, 'AS202607091756834291', 62, 999.00, 'PAID', 'MOCK_SUCCESS', '{"name":"Victor Liu","phone":"+6591234567","province":"Singapore","city":"Singapore","district":"Serangoon","address":"200 Serangoon Road"}', NULL, '2026-07-09 17:56:23'),
(63, 'AS202607081923476512', 63, 2499.00, 'PAID', 'MOCK_SUCCESS', '{"name":"Wendy Zhou","phone":"+8615512345740","province":"Shaanxi","city":"Xianyang","district":"Weiyang","address":"168 Fengcheng Road"}', NULL, '2026-07-08 19:23:23'),
(64, 'AS202607071845291341', 64, 199.00, 'PENDING_PAYMENT', 'MOCK_PENDING', '{"name":"Xavier Huang","phone":"+8613812345741","province":"Yunnan","city":"Dali","district":"Dali","address":"88 Cangshan Road"}', NULL, '2026-07-07 18:45:23'),
(65, 'AS202607061756423981', 65, 2999.00, 'PAID', 'MOCK_SUCCESS', '{"name":"Yvonne Chen","phone":"+8618612345742","province":"Guangxi","city":"Guilin","district":"Qixing","address":"66 Jinzhong Road"}', NULL, '2026-07-06 17:56:23'),
(66, 'AS202607051923789141', 66, 8999.00, 'PAID', 'MOCK_SUCCESS', '{"name":"Zachary Wang","phone":"+8613912345743","province":"Jiangsu","city":"Wuxi","district":"Liangxi","address":"188 Renmin Road"}', NULL, '2026-07-05 19:23:23'),
(67, 'AS202607041845634291', 67, 799.00, 'PAY_FAILED', 'MOCK_FAILED', '{"name":"Alice Liu","phone":"+6592345678","province":"Singapore","city":"Singapore","district":"Ang Mo Kio","address":"50 Ang Mo Kio"}', NULL, '2026-07-04 18:45:23'),
(68, 'AS202607031756892471', 68, 299.00, 'PAID', 'MOCK_SUCCESS', '{"name":"Brad Zhou","phone":"+8615512345745","province":"Jilin","city":"Jilin City","district":"Changyi","address":"99 Jilin Street"}', NULL, '2026-07-03 17:56:23'),
(69, 'AS202607021923145671', 69, 799.00, 'PAID', 'MOCK_SUCCESS', '{"name":"Cathy Huang","phone":"+8613812345746","province":"Heilongjiang","city":"Mudanjiang","district":"Aimin","address":"88 Wenhua Road"}', NULL, '2026-07-02 19:23:23'),
(70, 'AS202607011845376921', 70, 1599.00, 'PENDING_PAYMENT', 'MOCK_PENDING', '{"name":"Derek Chen","phone":null,"province":"Liaoning","city":"Anshan","district":"Tiedong","address":"66 Tiexi Road"}', NULL, '2026-07-01 18:45:23'),
(71, 'AS202606301756498271', 71, 499.00, 'PAID', 'MOCK_SUCCESS', '{"name":"Emma Wang","phone":"+8613912345748","province":"Shandong","city":"Yantai","district":"Laishan","address":"188 Qingnian Road"}', NULL, '2026-06-30 17:56:23'),
(72, 'AS202606291923672181', 72, 999.00, 'PAID', 'MOCK_SUCCESS', '{"name":"Frank Liu","phone":"+6593456789","province":"Singapore","city":"Singapore","district":"Toa Payoh","address":"1 Toa Payoh"}', NULL, '2026-06-29 19:23:23'),
(73, 'AS202606281845123491', 73, 799.00, 'PAY_FAILED', 'MOCK_FAILED', '{"name":"Grace Zhou","phone":"+8615512345750","province":"Fujian","city":"Quanzhou","district":"Licheng","address":"168 West Lake Road"}', NULL, '2026-06-28 18:45:23'),
(74, 'AS202606271756934281', 74, 3999.00, 'PAID', 'MOCK_SUCCESS', '{"name":"Henry Chen","phone":"+8613812345751","province":"Anhui","city":"Wuhu","district":"Jiujiang","address":"99 Beijing Road"}', NULL, '2026-06-27 17:56:23'),
(75, 'AS202606261923487161', 75, 999.00, 'PAID', 'MOCK_SUCCESS', '{"name":"Ivy Wang","phone":"+8618612345752","province":"Henan","city":"Luoyang","district":"Laocheng","address":"88 Zhongzhou Road"}', NULL, '2026-06-26 19:23:23'),
(76, 'AS202606251845691341', 76, 459.00, 'PENDING_PAYMENT', 'MOCK_PENDING', '{"name":"Jack Liu","phone":"+8613912345753","province":"Hubei","city":"Xiangyang","district":"Xiangcheng","address":"166 Changhong Road"}', NULL, '2026-06-25 18:45:23'),
(77, 'AS202606241756329841', 77, 499.00, 'PAID', 'MOCK_SUCCESS', '{"name":"Kelly Zhou","phone":"+6594567890","province":"Singapore","city":"Singapore","district":"Hougang","address":"300 Hougang"}', NULL, '2026-06-24 17:56:23'),
(78, 'AS202606231923854971', 78, 799.00, 'PAID', 'MOCK_SUCCESS', '{"name":"Lucas Huang","phone":"+8615512345755","province":"Sichuan","city":"Deyang","district":"Jingyang","address":"188 Taoyuan Road"}', NULL, '2026-06-23 19:23:23'),
(79, 'AS202606221845279131', 79, 1999.00, 'PAY_FAILED', 'MOCK_FAILED', '{"name":"Mabel Chen","phone":"+8613812345756","province":"Guangdong","city":"Zhongshan","district":"Dongqu","address":"66 Boai Road"}', NULL, '2026-06-22 18:45:23'),
(80, 'AS202606211756498211', 80, 4499.00, 'PAID', 'MOCK_SUCCESS', '{"name":"Neil Wang","phone":"+8618612345757","province":"Zhejiang","city":"Jinhua","district":"Wucheng","address":"88 Yalu Road"}', NULL, '2026-06-21 17:56:23'),
(81, 'AS202606201923672931', 81, 2999.00, 'PAID', 'MOCK_SUCCESS', '{"name":"Ophelia Liu","phone":"+8613912345758","province":"Jiangsu","city":"Yangzhou","district":"Guazhou","address":"168 Yangtze Road"}', NULL, '2026-06-20 19:23:23'),
(82, 'AS202606191845134291', 82, 8999.00, 'PENDING_PAYMENT', 'MOCK_PENDING', '{"name":"Peter Zhou","phone":"+6595678901","province":"Singapore","city":"Singapore","district":"Clementi","address":"315 Clementi"}', NULL, '2026-06-19 18:45:23'),
(83, 'AS202606181756923471', 83, 1299.00, 'PAID', 'MOCK_SUCCESS', '{"name":"Queen Huang","phone":"+8615512345760","province":"Shandong","city":"Weifang","district":"Weicheng","address":"99 Shengli Road"}', NULL, '2026-06-18 17:56:23'),
(84, 'AS202606171923487621', 84, 3999.00, 'PAID', 'MOCK_SUCCESS', '{"name":"Randy Chen","phone":"+8613812345761","province":"Jiangxi","city":"Jiujiang","district":"Xunyang","address":"88 Xunyang Road"}', NULL, '2026-06-17 19:23:23'),
(85, 'AS202606161845692141', 85, 799.00, 'PAY_FAILED', 'MOCK_FAILED', '{"name":"Sally Wang","phone":"+8618612345762","province":"Hainan","city":"Qionghai","district":"Qionghai","address":"66 Dongzhour Road"}', NULL, '2026-06-16 18:45:23'),
(86, 'AS202606151756413921', 86, 5999.00, 'PAID', 'MOCK_SUCCESS', '{"name":"Tommy Liu","phone":"+8613912345763","province":"Sichuan","city":"Yibin","district":"Cuiping","address":"188 Changning Road"}', NULL, '2026-06-15 17:56:23'),
(87, 'AS202606141923857291', 87, 2499.00, 'PAID', 'MOCK_SUCCESS', '{"name":"Una Zhou","phone":"+6596789012","province":"Singapore","city":"Singapore","district":"Bedok","address":"200 Bedok"}', NULL, '2026-06-14 19:23:23'),
(88, 'AS202606131845329141', 88, 1799.00, 'PENDING_PAYMENT', 'MOCK_PENDING', '{"name":"Vince Huang","phone":"+8615512345765","province":"Guangdong","city":"Jiangmen","district":"Pengjiang","address":"99 Donghai Road"}', NULL, '2026-06-13 18:45:23'),
(89, 'AS202606121756984231', 89, 999.00, 'PAID', 'MOCK_SUCCESS', '{"name":"Wanda Chen","phone":"+8613812345766","province":"Guangxi","city":"Beihai","district":"Haicheng","address":"88 Chating Road"}', NULL, '2026-06-12 17:56:23'),
(90, 'AS202606111923471821', 90, 2999.00, 'PAID', 'MOCK_SUCCESS', '{"name":"Xander Wang","phone":"+8618612345767","province":"Zhejiang","city":"Shaoxing","district":"Yuecheng","address":"168 Shen Road"}', NULL, '2026-06-11 19:23:23'),
(91, 'AS202606101845628931', 91, 1999.00, 'PAY_FAILED', 'MOCK_FAILED', '{"name":"Yolanda Liu","phone":"+8613912345768","province":"Shandong","city":"Linyi","district":"Lanshan","address":"99 Moscow Road"}', NULL, '2026-06-10 18:45:23'),
(92, 'AS202606091756391241', 92, 1299.00, 'PAID', 'MOCK_SUCCESS', '{"name":"Zelda Zhou","phone":"+6597890123","province":"Singapore","city":"Singapore","district":"Bukit Merah","address":"1 Lengkok Bahru"}', NULL, '2026-06-09 17:56:23'),
(93, 'AS202606081923845671', 93, 599.00, 'PAID', 'MOCK_SUCCESS', '{"name":"Aaron Huang","phone":"+8615512345770","province":"Heilongjiang","city":"Qiqihar","district":"Longsha","address":"188 Longsha Road"}', NULL, '2026-06-08 19:23:23'),
(94, 'AS202606071845192371', 94, 799.00, 'PENDING_PAYMENT', 'MOCK_PENDING', '{"name":"Beatrice Chen","phone":"+8613812345771","province":"Jilin","city":"Siping","district":"Tiedong","address":"66 Beihua Road"}', NULL, '2026-06-07 18:45:23'),
(95, 'AS202606061756482931', 95, 499.00, 'PAID', 'MOCK_SUCCESS', '{"name":"Chris Wang","phone":"+8618612345772","province":"Liaoning","city":"Fushun","district":"Shuncheng","address":"88 Xianlu Road"}', NULL, '2026-06-06 17:56:23'),
(96, 'AS202606051923674521', 96, 999.00, 'PAID', 'MOCK_SUCCESS', '{"name":"Doris Liu","phone":"+8613912345773","province":"Shaanxi","city":"Baoji","district":"Weibin","address":"168 Jinling Road"}', NULL, '2026-06-05 19:23:23'),
(97, 'AS202606041845397121', 97, 699.00, 'PAY_FAILED', 'MOCK_FAILED', '{"name":"Evan Zhou","phone":"+6598901234","province":"Singapore","city":"Singapore","district":"Geylang","address":"99 Geylang"}', NULL, '2026-06-04 18:45:23'),
(98, 'AS202606031756912841', 98, 2999.00, 'PAID', 'MOCK_SUCCESS', '{"name":"Faith Huang","phone":"+8615512345775","province":"Gansu","city":"Tianshui","district":"Maiji","address":"188 Tianshui Road"}', NULL, '2026-06-03 17:56:23'),
(99, 'AS202606021923586471', 99, 2999.00, 'PENDING_PAYMENT', 'MOCK_PENDING', '{"name":"Gary Chen","phone":"+8613812345776","province":"Ningxia","city":"Shizuishan","district":"Dawukou","address":"66 Huayuan Road"}', NULL, '2026-06-02 19:23:23'),
(100, 'AS202606011845273911', 100, 1299.00, 'PAID', 'MOCK_SUCCESS', '{"name":"Heidi Wang","phone":"+8618612345777","province":"Qinghai","city":"Xining","district":"Chengxi","address":"88 Huanghe Road"}', NULL, '2026-06-01 18:45:23');

-- =============================================================================
-- 五、order_items 订单明细表（100条）
-- 每个订单对应1条订单明细，金额与orders.total_amount一致
-- =============================================================================

INSERT INTO order_items (id, order_id, product_id, product_name, quantity, unit_price, amount) VALUES
(1, 1, 1001, 'iPhone 17', 1, 5999.00, 5999.00),
(2, 2, 1001, 'iPhone 17', 1, 5999.00, 5999.00),
(3, 3, 1041, 'Apple Watch Series 12', 1, 2999.00, 2999.00),
(4, 4, 1004, 'Samsung Galaxy S26', 1, 5499.00, 5499.00),
(5, 5, 1012, 'MacBook Air 15 M4', 1, 9999.00, 9999.00),
(6, 6, 1021, 'iPad Air 11 M3', 1, 4799.00, 4799.00),
(7, 7, 1032, 'AirPods 4', 1, 999.00, 999.00),
(8, 8, 1051, 'Sony Alpha A7 V', 1, 18999.00, 18999.00),
(9, 9, 1061, 'Nintendo Switch 2', 1, 2499.00, 2499.00),
(10, 10, 1072, 'Logitech MX Keys S', 1, 599.00, 599.00),
(11, 11, 1006, 'Google Pixel 11', 1, 4299.00, 4299.00),
(12, 12, 1091, 'Canon TS3530 Printer', 1, 599.00, 599.00),
(13, 13, 1041, 'Apple Watch Series 12', 1, 2999.00, 2999.00),
(14, 14, 1011, 'MacBook Air 13 M4', 1, 7999.00, 7999.00),
(15, 15, 1005, 'Samsung Galaxy S26 Ultra', 1, 8999.00, 8999.00),
(16, 16, 1011, 'MacBook Air 13 M4', 1, 7999.00, 7999.00),
(17, 17, 1033, 'AirPods Max 2', 1, 3999.00, 3999.00),
(18, 18, 1052, 'Sony Alpha A7C II', 1, 13999.00, 13999.00),
(19, 19, 1032, 'AirPods 4', 1, 999.00, 999.00),
(20, 20, 1084, 'Sonos Arc', 1, 6999.00, 6999.00),
(21, 21, 1022, 'iPad Pro 11 M4', 1, 7999.00, 7999.00),
(22, 22, 1012, 'MacBook Air 15 M4', 1, 9999.00, 9999.00),
(23, 23, 1037, 'Bose QC Earbuds II', 1, 1799.00, 1799.00),
(24, 24, 1071, 'Logitech MX Master 4', 1, 799.00, 799.00),
(25, 25, 1075, 'Anker 735 Charger', 1, 199.00, 199.00),
(26, 26, 1041, 'Apple Watch Series 12', 1, 2999.00, 2999.00),
(27, 27, 1032, 'AirPods 4', 1, 999.00, 999.00),
(28, 28, 1065, 'PlayStation DualSense 2', 1, 499.00, 499.00),
(29, 29, 1032, 'AirPods 4', 1, 999.00, 999.00),
(30, 30, 1085, 'Amazon Echo Show 10', 1, 2499.00, 2499.00),
(31, 31, 1043, 'Apple Watch SE 3', 1, 1999.00, 1999.00),
(32, 32, 1002, 'iPhone 17 Pro', 1, 7999.00, 7999.00),
(33, 33, 1079, 'SanDisk Extreme Pro 1TB', 1, 1299.00, 1299.00),
(34, 34, 1025, 'Samsung Galaxy Tab S10', 1, 5499.00, 5499.00),
(35, 35, 1033, 'AirPods Max 2', 1, 3999.00, 3999.00),
(36, 36, 1002, 'iPhone 17 Pro', 1, 7999.00, 7999.00),
(37, 37, 1081, 'Apple HomePod mini', 1, 699.00, 699.00),
(38, 38, 1044, 'Samsung Galaxy Watch 8', 1, 2299.00, 2299.00),
(39, 39, 1071, 'Logitech MX Master 4', 1, 799.00, 799.00),
(40, 40, 1015, 'Dell XPS 14', 1, 11999.00, 11999.00),
(41, 41, 1084, 'Sonos Arc', 1, 6999.00, 6999.00),
(42, 42, 1072, 'Logitech MX Keys S', 1, 599.00, 599.00),
(43, 43, 1037, 'Bose QC Earbuds II', 1, 1799.00, 1799.00),
(44, 44, 1012, 'MacBook Air 15 M4', 1, 9999.00, 9999.00),
(45, 45, 1079, 'SanDisk Extreme Pro 1TB', 1, 1299.00, 1299.00),
(46, 46, 1033, 'AirPods Max 2', 1, 3999.00, 3999.00),
(47, 47, 1073, 'Apple Magic Keyboard', 1, 999.00, 999.00),
(48, 48, 1032, 'AirPods 4', 1, 999.00, 999.00),
(49, 49, 1027, 'Xiaomi Pad 7 Pro', 1, 2999.00, 2999.00),
(50, 50, 1091, 'Canon TS3530 Printer', 1, 599.00, 599.00),
(51, 51, 1041, 'Apple Watch Series 12', 1, 2999.00, 2999.00),
(52, 52, 1022, 'iPad Pro 11 M4', 1, 7999.00, 7999.00),
(53, 53, 1032, 'AirPods 4', 1, 999.00, 999.00),
(54, 54, 1042, 'Apple Watch Ultra 3', 1, 4999.00, 4999.00),
(55, 55, 1037, 'Bose QC Earbuds II', 1, 1799.00, 1799.00),
(56, 56, 1073, 'Apple Magic Keyboard', 1, 999.00, 999.00),
(57, 57, 1022, 'iPad Pro 11 M4', 1, 7999.00, 7999.00),
(58, 58, 1057, 'Fujifilm X-T5', 1, 11999.00, 11999.00),
(59, 59, 1032, 'AirPods 4', 1, 999.00, 999.00),
(60, 60, 1007, 'Google Pixel 11 Pro', 1, 6499.00, 6499.00),
(61, 61, 1065, 'PlayStation DualSense 2', 1, 499.00, 499.00),
(62, 62, 1032, 'AirPods 4', 1, 999.00, 999.00),
(63, 63, 1085, 'Amazon Echo Show 10', 1, 2499.00, 2499.00),
(64, 64, 1075, 'Anker 735 Charger', 1, 199.00, 199.00),
(65, 65, 1027, 'Xiaomi Pad 7 Pro', 1, 2999.00, 2999.00),
(66, 66, 1005, 'Samsung Galaxy S26 Ultra', 1, 8999.00, 8999.00),
(67, 67, 1073, 'Apple Magic Keyboard', 1, 999.00, 999.00),
(68, 68, 1076, 'Anker PowerCore 26800', 1, 299.00, 299.00),
(69, 69, 1071, 'Logitech MX Master 4', 1, 799.00, 799.00),
(70, 70, 1089, 'Ring Video Doorbell Pro 2', 1, 1599.00, 1599.00),
(71, 71, 1065, 'PlayStation DualSense 2', 1, 499.00, 499.00),
(72, 72, 1032, 'AirPods 4', 1, 999.00, 999.00),
(73, 73, 1071, 'Logitech MX Master 4', 1, 799.00, 799.00),
(74, 74, 1041, 'Apple Watch Series 12', 1, 2999.00, 2999.00),
(75, 75, 1032, 'AirPods 4', 1, 999.00, 999.00),
(76, 76, 1067, 'Nintendo Switch Pro Controller', 1, 459.00, 459.00),
(77, 77, 1078, 'WD My Passport 2TB', 1, 499.00, 499.00),
(78, 78, 1071, 'Logitech MX Master 4', 1, 799.00, 799.00),
(79, 79, 1090, 'Dyson V20 Vacuum', 1, 4999.00, 4999.00),
(80, 80, 1010, 'OPPO Find X8', 1, 4499.00, 4499.00),
(81, 81, 1028, 'Microsoft Surface Pro 10', 1, 8999.00, 8999.00),
(82, 82, 1029, 'Microsoft Surface Go 4', 1, 3999.00, 3999.00),
(83, 83, 1039, 'Samsung Galaxy Buds3 Pro', 1, 1299.00, 1299.00),
(84, 84, 1047, 'Garmin Forerunner 965', 1, 3999.00, 3999.00),
(85, 85, 1071, 'Logitech MX Master 4', 1, 799.00, 799.00),
(86, 86, 1022, 'iPad Pro 11 M4', 1, 7999.00, 7999.00),
(87, 87, 1063, 'Xbox Series X2', 1, 3499.00, 3499.00),
(88, 88, 1037, 'Bose QC Earbuds II', 1, 1799.00, 1799.00),
(89, 89, 1032, 'AirPods 4', 1, 999.00, 999.00),
(90, 90, 1088, 'Xiaomi Smart Screen 86', 1, 8999.00, 8999.00),
(91, 91, 1009, 'OnePlus 13', 1, 3999.00, 3999.00),
(92, 92, 1079, 'SanDisk Extreme Pro 1TB', 1, 1299.00, 1299.00),
(93, 93, 1091, 'Canon TS3530 Printer', 1, 599.00, 599.00),
(94, 94, 1071, 'Logitech MX Master 4', 1, 799.00, 799.00),
(95, 95, 1073, 'Apple Magic Keyboard', 1, 999.00, 999.00),
(96, 96, 1032, 'AirPods 4', 1, 999.00, 999.00),
(97, 97, 1081, 'Apple HomePod mini', 1, 699.00, 699.00),
(98, 98, 1009, 'OnePlus 13', 1, 3999.00, 3999.00),
(99, 99, 1041, 'Apple Watch Series 12', 1, 2999.00, 2999.00),
(100, 100, 1039, 'Samsung Galaxy Buds3 Pro', 1, 1299.00, 1299.00);

-- =============================================================================
-- 六、数据校验
-- =============================================================================

-- 1. 检查每表数据量
SELECT 'users' AS table_name, COUNT(*) AS count FROM users
UNION ALL SELECT 'products', COUNT(*) FROM products
UNION ALL SELECT 'cart_items', COUNT(*) FROM cart_items
UNION ALL SELECT 'orders', COUNT(*) FROM orders
UNION ALL SELECT 'order_items', COUNT(*) FROM order_items;

-- 2. 检查购物车用户关联
SELECT COUNT(*) AS invalid_cart_user_count
FROM cart_items c
LEFT JOIN users u ON c.user_id = u.id
WHERE u.id IS NULL;

-- 3. 检查购物车商品关联
SELECT COUNT(*) AS invalid_cart_product_count
FROM cart_items c
LEFT JOIN products p ON c.product_id = p.id
WHERE p.id IS NULL;

-- 4. 检查订单用户关联
SELECT COUNT(*) AS invalid_order_user_count
FROM orders o
LEFT JOIN users u ON o.user_id = u.id
WHERE u.id IS NULL;

-- 5. 检查订单明细订单关联
SELECT COUNT(*) AS invalid_orderitem_order_count
FROM order_items oi
LEFT JOIN orders o ON oi.order_id = o.id
WHERE o.id IS NULL;

-- 6. 检查订单明细商品关联
SELECT COUNT(*) AS invalid_orderitem_product_count
FROM order_items oi
LEFT JOIN products p ON oi.product_id = p.id
WHERE p.id IS NULL;

-- 7. 检查订单明细金额计算
SELECT COUNT(*) AS invalid_amount_count
FROM order_items
WHERE amount <> quantity * unit_price;

-- 8. 检查订单总金额与明细合计一致性
SELECT COUNT(*) AS invalid_order_total_count
FROM orders o
LEFT JOIN (
    SELECT order_id, SUM(amount) AS item_total
    FROM order_items
    GROUP BY order_id
) oi ON oi.order_id = o.id
WHERE o.total_amount <> oi.item_total;

-- 9. 检查订单状态与支付状态一致性
SELECT COUNT(*) AS invalid_status_count
FROM orders
WHERE (order_status = 'PAID' AND payment_status != 'MOCK_SUCCESS')
   OR (order_status = 'PAY_FAILED' AND payment_status != 'MOCK_FAILED')
   OR (order_status = 'PENDING_PAYMENT' AND payment_status != 'MOCK_PENDING');

-- 10. 检查订单号唯一性
SELECT COUNT(*) - COUNT(DISTINCT order_no) AS duplicate_order_no_count
FROM orders;

-- 11. 检查用户名唯一性
SELECT COUNT(*) - COUNT(DISTINCT username) AS duplicate_username_count
FROM users;

-- 12. 检查邮箱唯一性
SELECT COUNT(*) - COUNT(DISTINCT email) AS duplicate_email_count
FROM users;
