# Flood-Spider
对www.cjh.com.cn中国各个水文站点实时数据的爬虫与数据简单可视化

### 配置说明

本项目分爬虫与数据处理两部分，爬虫会将爬取的数据存入数据库，数据处理部分将查询数据绘图。

爬虫部分依赖pymysql库，对接mysql数据库，数据库默认ip为localhost本地数据库，默认用户名root，默认密码空，默认库名flood。

数据库环境可使用以下sql语句创建（[或者使用sql脚本](flood.sql)）：
```sql
SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

DROP TABLE IF EXISTS `waterLevel`;
CREATE TABLE `waterLevel`  (
  `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  `site` varchar(31) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `waterSource` varchar(31) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `datetime` datetime(0) NULL,
  `waterlevel` decimal(11, 2) NULL DEFAULT NULL COMMENT '单位：米',
  `flow` int(11) NULL DEFAULT NULL COMMENT '单位：立方米每秒',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1223 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;
```

爬虫爬取的api每小时更新，建议放在自己的服务器上设置定时运行。

>如果使用了自定义的数据库ip，用户等，记得也在数据分析代码中修改相关连接串。
