/*
 Navicat Premium Data Transfer

 Source Server         : local Database
 Source Server Type    : MySQL
 Source Server Version : 100417 (10.4.17-MariaDB)
 Source Host           : localhost:3306
 Source Schema         : inventory1

 Target Server Type    : MySQL
 Target Server Version : 100417 (10.4.17-MariaDB)
 File Encoding         : 65001

 Date: 26/08/2023 21:09:44
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for bahan
-- ----------------------------
DROP TABLE IF EXISTS `bahan`;
CREATE TABLE `bahan`  (
  `id_bahan` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `nama_bahan` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id_bahan`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of bahan
-- ----------------------------
INSERT INTO `bahan` VALUES ('BHN_01', 'Katun');
INSERT INTO `bahan` VALUES ('string', 'stringg');

-- ----------------------------
-- Table structure for inventory
-- ----------------------------
DROP TABLE IF EXISTS `inventory`;
CREATE TABLE `inventory`  (
  `id_inv` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `id_bahan` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `id_ukuran` int NULL DEFAULT NULL,
  `nama_produk` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `harga_produk` int NULL DEFAULT NULL,
  `qty` int NULL DEFAULT NULL,
  `qty_washing` int NULL DEFAULT NULL,
  `qty_final` int NULL DEFAULT NULL,
  `status_trc` enum('0','1','2','3') CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT '0',
  `tanggal_mulai_jait` datetime NULL DEFAULT NULL,
  `tanggal_produk_jadi` datetime NULL DEFAULT NULL,
  PRIMARY KEY (`id_inv`) USING BTREE,
  INDEX `inv_bahan`(`id_bahan` ASC) USING BTREE,
  INDEX `in_ukuran`(`id_ukuran` ASC) USING BTREE,
  CONSTRAINT `in_ukuran` FOREIGN KEY (`id_ukuran`) REFERENCES `ukuran` (`id_ukuran`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `inv_bahan` FOREIGN KEY (`id_bahan`) REFERENCES `bahan` (`id_bahan`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of inventory
-- ----------------------------
INSERT INTO `inventory` VALUES ('KL_009JK', 'string', 11, 'artile 40', 100000, NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `inventory` VALUES ('PM_001LM', 'string', 11, 'article 1', 200000, 1, 1, 3, '3', '2023-08-26 01:48:40', NULL);
INSERT INTO `inventory` VALUES ('PM_002LM', 'string', 11, 'article 2', 20000, 1, 2, NULL, '3', '2023-08-26 01:50:37', NULL);
INSERT INTO `inventory` VALUES ('PM_003LM', 'string', 6, 'article 2', 20000, 1, NULL, NULL, '1', '2023-08-26 02:21:07', NULL);
INSERT INTO `inventory` VALUES ('PM_004LM', 'BHN_01', 6, 'Arcticle 2', 123123, 5, 5, 3, '3', '2023-08-26 05:07:54', NULL);
INSERT INTO `inventory` VALUES ('UP_090IK', 'string', 8, 'article 50', 50000, NULL, NULL, NULL, NULL, NULL, NULL);

-- ----------------------------
-- Table structure for pembuatan
-- ----------------------------
DROP TABLE IF EXISTS `pembuatan`;
CREATE TABLE `pembuatan`  (
  `id_pembuatan` int NOT NULL AUTO_INCREMENT,
  `id_inv` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `tanggal_pembuatan` datetime NULL DEFAULT NULL,
  `tanggal_selesai` datetime NULL DEFAULT NULL,
  `qty_pembuatan` int NULL DEFAULT NULL,
  `interval_pembuatan` int NULL DEFAULT NULL,
  PRIMARY KEY (`id_pembuatan`) USING BTREE,
  INDEX `pembuatan_inv`(`id_inv` ASC) USING BTREE,
  CONSTRAINT `pembuatan_inv` FOREIGN KEY (`id_inv`) REFERENCES `inventory` (`id_inv`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 69 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of pembuatan
-- ----------------------------
INSERT INTO `pembuatan` VALUES (27, 'PM_004LM', '2023-08-26 05:39:55', '2023-08-26 05:40:04', 3, 1);
INSERT INTO `pembuatan` VALUES (28, 'PM_004LM', '2023-08-26 05:42:13', '2023-08-26 05:42:24', 5, 2);
INSERT INTO `pembuatan` VALUES (67, 'KL_009JK', '2023-08-26 21:06:30', NULL, NULL, 1);
INSERT INTO `pembuatan` VALUES (68, 'UP_090IK', '2023-08-26 21:07:26', NULL, NULL, 1);

-- ----------------------------
-- Table structure for pos
-- ----------------------------
DROP TABLE IF EXISTS `pos`;
CREATE TABLE `pos`  (
  `id_pos` int NOT NULL AUTO_INCREMENT,
  `id_inv` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `total_qty` int NULL DEFAULT NULL,
  `total_income` int NULL DEFAULT NULL,
  `tanggal_barang_out` datetime NULL DEFAULT NULL,
  PRIMARY KEY (`id_pos`) USING BTREE,
  INDEX `pos_inv`(`id_inv` ASC) USING BTREE,
  CONSTRAINT `pos_inv` FOREIGN KEY (`id_inv`) REFERENCES `inventory` (`id_inv`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of pos
-- ----------------------------
INSERT INTO `pos` VALUES (1, 'PM_004LM', 10, 1231230, '2023-08-26 00:00:00');
INSERT INTO `pos` VALUES (2, 'PM_004LM', 1, 123123, '2023-08-26 00:00:00');
INSERT INTO `pos` VALUES (3, 'PM_004LM', 4, 492492, '2023-08-26 00:00:00');

-- ----------------------------
-- Table structure for ukuran
-- ----------------------------
DROP TABLE IF EXISTS `ukuran`;
CREATE TABLE `ukuran`  (
  `id_ukuran` int NOT NULL AUTO_INCREMENT,
  `nama_ukuran` varchar(5) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id_ukuran`) USING BTREE,
  UNIQUE INDEX `nama_ukuran_unique`(`nama_ukuran` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 48 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of ukuran
-- ----------------------------
INSERT INTO `ukuran` VALUES (11, 'kl');
INSERT INTO `ukuran` VALUES (6, 'm');
INSERT INTO `ukuran` VALUES (8, 'S');
INSERT INTO `ukuran` VALUES (9, 'xl');

SET FOREIGN_KEY_CHECKS = 1;
