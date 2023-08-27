/*
 Navicat Premium Data Transfer

 Source Server         : inventory
 Source Server Type    : MySQL
 Source Server Version : 100428
 Source Host           : localhost:3306
 Source Schema         : inventory

 Target Server Type    : MySQL
 Target Server Version : 100428
 File Encoding         : 65001

 Date: 28/08/2023 03:33:13
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
INSERT INTO `bahan` VALUES ('string', 'string');

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
  `qty_final` int NULL DEFAULT NULL,
  PRIMARY KEY (`id_inv`) USING BTREE,
  INDEX `inv_bahan`(`id_bahan`) USING BTREE,
  INDEX `in_ukuran`(`id_ukuran`) USING BTREE,
  CONSTRAINT `in_ukuran` FOREIGN KEY (`id_ukuran`) REFERENCES `ukuran` (`id_ukuran`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `inv_bahan` FOREIGN KEY (`id_bahan`) REFERENCES `bahan` (`id_bahan`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of inventory
-- ----------------------------
INSERT INTO `inventory` VALUES ('PM_001LM', 'string', 48, 'Article 1', 50000, NULL);
INSERT INTO `inventory` VALUES ('PM_002JK', 'string', 48, 'Article 2', 50000, NULL);

-- ----------------------------
-- Table structure for pembuatan
-- ----------------------------
DROP TABLE IF EXISTS `pembuatan`;
CREATE TABLE `pembuatan`  (
  `id_pembuatan` int NOT NULL AUTO_INCREMENT,
  `id_produksi` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `id_inv` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `tanggal_pembuatan` datetime NULL DEFAULT NULL,
  `tanggal_selesai` datetime NULL DEFAULT NULL,
  `qty_pembuatan` int NULL DEFAULT NULL,
  `status_pembuatan` enum('0','1','2','3') CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT '1',
  `status_inventory` enum('0','1') CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT '0',
  `qty_inventory` int NULL DEFAULT NULL,
  PRIMARY KEY (`id_pembuatan`) USING BTREE,
  INDEX `pembuatan_inv`(`id_inv`) USING BTREE,
  INDEX `id_produksi`(`id_produksi`) USING BTREE,
  CONSTRAINT `pembuatan_inv` FOREIGN KEY (`id_inv`) REFERENCES `inventory` (`id_inv`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 77 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of pembuatan
-- ----------------------------
INSERT INTO `pembuatan` VALUES (73, 'PROD_001', 'PM_001LM', '2023-08-27 00:00:00', NULL, 220, '0', '0', NULL);
INSERT INTO `pembuatan` VALUES (74, 'PROD_001', 'PM_002JK', '2023-08-27 00:00:00', NULL, 20, '0', '0', NULL);
INSERT INTO `pembuatan` VALUES (76, 'PROD_003', 'PM_001LM', '2023-08-28 00:00:00', NULL, 110, '1', '0', NULL);

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
  INDEX `pos_inv`(`id_inv`) USING BTREE,
  CONSTRAINT `pos_inv` FOREIGN KEY (`id_inv`) REFERENCES `inventory` (`id_inv`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 5 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of pos
-- ----------------------------

-- ----------------------------
-- Table structure for tabel_cuci
-- ----------------------------
DROP TABLE IF EXISTS `tabel_cuci`;
CREATE TABLE `tabel_cuci`  (
  `id_cucian` int NOT NULL AUTO_INCREMENT,
  `id_produksi` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `id_vendor` int NULL DEFAULT NULL,
  `tanggal_cuci` datetime NULL DEFAULT NULL,
  `tanggal_selesai` datetime NULL DEFAULT NULL,
  PRIMARY KEY (`id_cucian`) USING BTREE,
  INDEX `produksi_cuci`(`id_produksi`) USING BTREE,
  INDEX `vendor_cuci`(`id_vendor`) USING BTREE,
  CONSTRAINT `produksi_cuci` FOREIGN KEY (`id_produksi`) REFERENCES `pembuatan` (`id_produksi`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `vendor_cuci` FOREIGN KEY (`id_vendor`) REFERENCES `vendor` (`id_vendor`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of tabel_cuci
-- ----------------------------
INSERT INTO `tabel_cuci` VALUES (1, 'PROD_001', 2, '2023-08-28 01:18:44', NULL);

-- ----------------------------
-- Table structure for tabel_jait
-- ----------------------------
DROP TABLE IF EXISTS `tabel_jait`;
CREATE TABLE `tabel_jait`  (
  `id_jait` int NOT NULL AUTO_INCREMENT,
  `id_produksi` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `id_vendor` int NULL DEFAULT NULL,
  `tanggal_jait` datetime NULL DEFAULT NULL,
  `tanggal_selesai` datetime NULL DEFAULT NULL,
  PRIMARY KEY (`id_jait`) USING BTREE,
  INDEX `produksi_jait`(`id_produksi`) USING BTREE,
  INDEX `vendor_jait`(`id_vendor`) USING BTREE,
  CONSTRAINT `produksi_jait` FOREIGN KEY (`id_produksi`) REFERENCES `pembuatan` (`id_produksi`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `vendor_jait` FOREIGN KEY (`id_vendor`) REFERENCES `vendor` (`id_vendor`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 6 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of tabel_jait
-- ----------------------------
INSERT INTO `tabel_jait` VALUES (1, 'PROD_001', 1, '2023-08-28 01:17:42', NULL);
INSERT INTO `tabel_jait` VALUES (4, 'PROD_003', 1, '2023-08-28 00:00:00', NULL);
INSERT INTO `tabel_jait` VALUES (5, 'PROD_003', 1, '2023-08-28 00:00:00', NULL);

-- ----------------------------
-- Table structure for ukuran
-- ----------------------------
DROP TABLE IF EXISTS `ukuran`;
CREATE TABLE `ukuran`  (
  `id_ukuran` int NOT NULL AUTO_INCREMENT,
  `nama_ukuran` varchar(5) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id_ukuran`) USING BTREE,
  UNIQUE INDEX `nama_ukuran_unique`(`nama_ukuran`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 49 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of ukuran
-- ----------------------------
INSERT INTO `ukuran` VALUES (48, 'l');

-- ----------------------------
-- Table structure for vendor
-- ----------------------------
DROP TABLE IF EXISTS `vendor`;
CREATE TABLE `vendor`  (
  `id_vendor` int NOT NULL AUTO_INCREMENT,
  `nama_vendor` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `jenis_vendor` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id_vendor`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of vendor
-- ----------------------------
INSERT INTO `vendor` VALUES (1, 'vendor jait', 'jaitan');
INSERT INTO `vendor` VALUES (2, 'vendor cuci', 'cucian');

SET FOREIGN_KEY_CHECKS = 1;
