/*
 Navicat Premium Data Transfer

 Source Server Type    : MySQL
 Source Schema         : flood

 Target Server Type    : MySQL
 Target Server Version : 50728
 File Encoding         : 65001

 Date: 25/06/2020 22:19:14
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for waterLevel
-- ----------------------------
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
