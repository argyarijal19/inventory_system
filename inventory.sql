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

 Date: 01/09/2023 03:33:37
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
INSERT INTO `bahan` VALUES ('2307HT', 'Denim');
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
INSERT INTO `inventory` VALUES ('CL_001HM', 'string', 49, 'celana jeans hitam', 200000, NULL);
INSERT INTO `inventory` VALUES ('PM_001KS', 'string', 48, 'string Updated', 90000, 0);
INSERT INTO `inventory` VALUES ('PM_002JK', 'string', 48, 'Article 2', 50000, 113);
INSERT INTO `inventory` VALUES ('RM_001LM', '2307HT', 50, 'Rebel', 150000, NULL);
INSERT INTO `inventory` VALUES ('RM_002LM', '2307HT', 51, 'Rebel', 150000, 132);

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
  `status_pembuatan` enum('1','2','3','4') CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT '1',
  `status_inventory` enum('0','1') CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT '0',
  `qty_inventory` int NULL DEFAULT NULL,
  PRIMARY KEY (`id_pembuatan`) USING BTREE,
  INDEX `pembuatan_inv`(`id_inv`) USING BTREE,
  INDEX `id_produksi`(`id_produksi`) USING BTREE,
  CONSTRAINT `pembuatan_inv` FOREIGN KEY (`id_inv`) REFERENCES `inventory` (`id_inv`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 121 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of pembuatan
-- ----------------------------
INSERT INTO `pembuatan` VALUES (114, 'PRD_007', 'RM_001LM', '2023-08-31 23:17:36', NULL, 10, '1', NULL, NULL);
INSERT INTO `pembuatan` VALUES (115, 'PRD_008', 'RM_001LM', '2023-08-31 23:18:07', NULL, 10, '1', NULL, NULL);
INSERT INTO `pembuatan` VALUES (116, 'PRD_003', 'CL_001HM', '2023-08-31 23:18:51', NULL, 89, '1', NULL, NULL);
INSERT INTO `pembuatan` VALUES (117, 'PRD_004', 'PM_001KS', '2023-08-31 23:19:42', NULL, 10, '2', NULL, NULL);
INSERT INTO `pembuatan` VALUES (118, 'PRD_004', 'RM_002LM', '2023-08-31 23:19:42', NULL, 10, '2', NULL, NULL);
INSERT INTO `pembuatan` VALUES (119, 'PRD_005', 'RM_002LM', '2023-09-01 23:22:04', '2023-09-01 00:00:00', 137, '2', '0', NULL);
INSERT INTO `pembuatan` VALUES (120, 'PRD_005', 'PM_002JK', '2023-09-01 23:22:04', '2023-09-01 00:00:00', 89, '3', '1', 89);

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
) ENGINE = InnoDB AUTO_INCREMENT = 17 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of pos
-- ----------------------------
INSERT INTO `pos` VALUES (8, 'PM_001KS', 3, 270000, '2023-08-31 00:00:00');
INSERT INTO `pos` VALUES (9, 'PM_002JK', 9, 450000, '2023-08-31 00:00:00');
INSERT INTO `pos` VALUES (10, 'PM_002JK', 3, 150000, '2023-08-31 00:00:00');
INSERT INTO `pos` VALUES (11, 'PM_002JK', 5, 250000, '2023-08-31 00:00:00');
INSERT INTO `pos` VALUES (12, 'PM_001KS', 1, 90000, '2023-09-01 00:00:00');
INSERT INTO `pos` VALUES (13, 'RM_002LM', 1, 150000, '2023-09-01 00:00:00');
INSERT INTO `pos` VALUES (14, 'RM_002LM', 1, 150000, '2023-09-01 00:00:00');
INSERT INTO `pos` VALUES (15, 'RM_002LM', 1, 150000, '2023-09-02 00:00:00');
INSERT INTO `pos` VALUES (16, 'RM_002LM', 1, 150000, '2023-09-01 00:00:00');

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
) ENGINE = InnoDB AUTO_INCREMENT = 22 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of tabel_cuci
-- ----------------------------
INSERT INTO `tabel_cuci` VALUES (20, 'PRD_005', 2, NULL, NULL);
INSERT INTO `tabel_cuci` VALUES (21, 'PRD_004', 2, NULL, NULL);

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
) ENGINE = InnoDB AUTO_INCREMENT = 34 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of tabel_jait
-- ----------------------------
INSERT INTO `tabel_jait` VALUES (29, 'PRD_007', 1, NULL, NULL);
INSERT INTO `tabel_jait` VALUES (30, 'PRD_008', 1, NULL, NULL);
INSERT INTO `tabel_jait` VALUES (31, 'PRD_003', 17, NULL, NULL);
INSERT INTO `tabel_jait` VALUES (32, 'PRD_004', 17, NULL, NULL);
INSERT INTO `tabel_jait` VALUES (33, 'PRD_005', 17, NULL, NULL);

-- ----------------------------
-- Table structure for ukuran
-- ----------------------------
DROP TABLE IF EXISTS `ukuran`;
CREATE TABLE `ukuran`  (
  `id_ukuran` int NOT NULL AUTO_INCREMENT,
  `nama_ukuran` varchar(5) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id_ukuran`) USING BTREE,
  UNIQUE INDEX `nama_ukuran_unique`(`nama_ukuran`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 52 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of ukuran
-- ----------------------------
INSERT INTO `ukuran` VALUES (50, '28');
INSERT INTO `ukuran` VALUES (51, '30');
INSERT INTO `ukuran` VALUES (48, 'l');
INSERT INTO `ukuran` VALUES (49, 'm');

-- ----------------------------
-- Table structure for users
-- ----------------------------
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users`  (
  `id_user` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `nama_lengkap` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `username` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `password` varchar(350) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id_user`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of users
-- ----------------------------
INSERT INTO `users` VALUES ('db37ce8481f2b0299be1', 'string', 'argyarijal19', '$2b$12$ckwAf9R8yXR8ZInvOtSS8.1NaNfOLF8a9aa71pgJf.zFrSSadhm4q');

-- ----------------------------
-- Table structure for vendor
-- ----------------------------
DROP TABLE IF EXISTS `vendor`;
CREATE TABLE `vendor`  (
  `id_vendor` int NOT NULL AUTO_INCREMENT,
  `nama_vendor` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `jenis_vendor` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id_vendor`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 18 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of vendor
-- ----------------------------
INSERT INTO `vendor` VALUES (1, 'vendor jait', 'jaitan');
INSERT INTO `vendor` VALUES (2, 'vendor cuci', 'cucian');
INSERT INTO `vendor` VALUES (11, 'string', 'string');
INSERT INTO `vendor` VALUES (12, 'string', 'string');
INSERT INTO `vendor` VALUES (13, 'string', 'string');
INSERT INTO `vendor` VALUES (14, 'konveksi titit besar', 'Jahitan');
INSERT INTO `vendor` VALUES (15, 'cucian bandung', 'Cuci');
INSERT INTO `vendor` VALUES (16, 'Prisma', 'Cuci');
INSERT INTO `vendor` VALUES (17, 'Kebon Kopi', 'Jahitan');

SET FOREIGN_KEY_CHECKS = 1;
