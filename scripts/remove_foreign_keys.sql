-- =============================================================================
-- remove_foreign_keys.sql
-- 功能：从 autoshop 数据库中删除所有外键约束。
--       约束名通过 information_schema.KEY_COLUMN_USAGE 实时查询生成，
--       不依赖固定命名规则，适用于任何 FK 约束名。
-- 使用：mysql -u autoshop -p autoshop < scripts/remove_foreign_keys.sql
-- =============================================================================

-- 0. 确保在 autoshop 库
USE `autoshop`;

-- 1. 查询当前所有外键约束（供人工确认）
SELECT
    TABLE_NAME          AS `表名`,
    CONSTRAINT_NAME     AS `约束名`,
    COLUMN_NAME         AS `字段`,
    REFERENCED_TABLE_NAME  AS `引用表`,
    REFERENCED_COLUMN_NAME AS `引用字段`
FROM information_schema.KEY_COLUMN_USAGE
WHERE TABLE_SCHEMA = 'autoshop'
  AND REFERENCED_TABLE_NAME IS NOT NULL;

-- 2. 动态生成并执行 DROP FOREIGN KEY（遍历所有外键约束）
--    生成语句示例：ALTER TABLE cart_items DROP FOREIGN KEY fk_cart_user;
SET @sql = NULL;

SELECT GROUP_CONCAT(
    CONCAT('ALTER TABLE `', TABLE_NAME, '` DROP FOREIGN KEY `', CONSTRAINT_NAME, '`')
    SEPARATOR ';\n'
) INTO @sql
FROM information_schema.KEY_COLUMN_USAGE
WHERE TABLE_SCHEMA = 'autoshop'
  AND REFERENCED_TABLE_NAME IS NOT NULL;

-- 仅当有外键时才执行
IF @sql IS NOT NULL THEN
    SET @sql = CONCAT(@sql, ';');
    PREPARE stmt FROM @sql;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;
    SELECT 'All foreign keys dropped.' AS result;
ELSE
    SELECT 'No foreign keys found in autoshop database.' AS result;
END IF;

-- 3. 验证：确认数据库中不再有任何外键约束
SELECT COUNT(*) AS remaining_foreign_keys
FROM information_schema.KEY_COLUMN_USAGE
WHERE TABLE_SCHEMA = 'autoshop'
  AND REFERENCED_TABLE_NAME IS NOT NULL;
