-- MySQL dump 10.13  Distrib 8.0.45, for Win64 (x86_64)
--
-- Host: localhost    Database: asd_project
-- ------------------------------------------------------
-- Server version	8.0.45

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `apartments`
--

DROP TABLE IF EXISTS `apartments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `apartments` (
  `id` int NOT NULL AUTO_INCREMENT,
  `property_id` int NOT NULL,
  `unit_number` varchar(20) NOT NULL,
  `floor` int DEFAULT '0',
  `bedrooms` int NOT NULL,
  `bathrooms` int NOT NULL DEFAULT '1',
  `size_sqm` float DEFAULT NULL,
  `monthly_rent` decimal(10,2) NOT NULL,
  `apartment_type` varchar(50) DEFAULT NULL,
  `status` enum('available','occupied','maintenance') DEFAULT 'available',
  PRIMARY KEY (`id`),
  KEY `property_id` (`property_id`),
  CONSTRAINT `apartments_ibfk_1` FOREIGN KEY (`property_id`) REFERENCES `properties` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `apartments`
--

LOCK TABLES `apartments` WRITE;
/*!40000 ALTER TABLE `apartments` DISABLE KEYS */;
INSERT INTO `apartments` VALUES (1,1,'101',1,1,1,45,950.00,'Studio','occupied'),(2,1,'102',1,1,1,55,1100.00,'1-Bedroom','occupied'),(3,1,'201',2,2,1,70,1400.00,'2-Bedroom','occupied'),(4,1,'202',2,2,2,75,1500.00,'2-Bedroom','available'),(5,1,'301',3,3,2,95,2000.00,'3-Bedroom','available'),(6,1,'302',3,1,1,52,1050.00,'1-Bedroom','maintenance'),(7,2,'101',1,1,1,42,800.00,'Studio','available'),(8,2,'102',1,2,1,65,1200.00,'2-Bedroom','occupied'),(9,2,'201',2,2,2,78,1350.00,'2-Bedroom','available'),(10,3,'101',1,1,1,40,1800.00,'Studio','occupied'),(11,3,'102',1,2,1,62,2500.00,'2-Bedroom','available'),(12,3,'201',2,3,2,90,3200.00,'3-Bedroom','available'),(13,4,'101',1,1,1,44,750.00,'Studio','available'),(14,4,'102',1,2,1,68,1100.00,'2-Bedroom','available');
/*!40000 ALTER TABLE `apartments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `complaints`
--

DROP TABLE IF EXISTS `complaints`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `complaints` (
  `id` int NOT NULL AUTO_INCREMENT,
  `tenant_id` int DEFAULT NULL,
  `tenant_name` varchar(100) NOT NULL,
  `issue` text NOT NULL,
  `category` enum('Noise','Repair','Neighbour','Billing','Other') DEFAULT 'Other',
  `status` enum('Open','Investigating','Resolved','Closed') DEFAULT 'Open',
  `submission_date` datetime DEFAULT CURRENT_TIMESTAMP,
  `resolution_date` datetime DEFAULT NULL,
  `resolution_notes` text,
  PRIMARY KEY (`id`),
  KEY `tenant_id` (`tenant_id`),
  CONSTRAINT `complaints_ibfk_1` FOREIGN KEY (`tenant_id`) REFERENCES `tenants` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `complaints`
--

LOCK TABLES `complaints` WRITE;
/*!40000 ALTER TABLE `complaints` DISABLE KEYS */;
INSERT INTO `complaints` VALUES (1,1,'John Smith','Noise from upstairs flat after 11pm','Noise','Resolved','2026-01-15 10:00:00','2026-01-18 14:00:00','Spoken to upstairs tenant. Resolved.'),(2,2,'Sarah Jones','Hot water not working for 3 days','Repair','Investigating','2026-02-10 09:00:00',NULL,NULL),(3,3,'David Brown','Billing charge appears incorrect','Billing','Open','2026-03-05 11:00:00',NULL,NULL),(4,4,'Emma Wilson','Neighbour\'s dog barking constantly','Neighbour','Open','2026-03-20 14:00:00',NULL,NULL);
/*!40000 ALTER TABLE `complaints` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `invoices`
--

DROP TABLE IF EXISTS `invoices`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `invoices` (
  `id` int NOT NULL AUTO_INCREMENT,
  `tenant_id` int NOT NULL,
  `lease_id` int DEFAULT NULL,
  `amount` decimal(10,2) NOT NULL,
  `issue_date` date NOT NULL,
  `due_date` date NOT NULL,
  `month` int NOT NULL,
  `year` int NOT NULL,
  `status` enum('unpaid','paid','overdue','partial') DEFAULT 'unpaid',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `tenant_id` (`tenant_id`),
  KEY `lease_id` (`lease_id`),
  CONSTRAINT `invoices_ibfk_1` FOREIGN KEY (`tenant_id`) REFERENCES `tenants` (`id`),
  CONSTRAINT `invoices_ibfk_2` FOREIGN KEY (`lease_id`) REFERENCES `leases` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `invoices`
--

LOCK TABLES `invoices` WRITE;
/*!40000 ALTER TABLE `invoices` DISABLE KEYS */;
INSERT INTO `invoices` VALUES (1,1,1,1400.00,'2025-10-01','2025-10-28',10,2025,'paid','2026-04-03 01:54:36'),(2,1,1,1400.00,'2025-11-01','2025-11-28',11,2025,'paid','2026-04-03 01:54:36'),(3,1,1,1400.00,'2025-12-01','2025-12-28',12,2025,'paid','2026-04-03 01:54:36'),(4,1,1,1400.00,'2026-01-01','2026-01-28',1,2026,'paid','2026-04-03 01:54:36'),(5,1,1,1400.00,'2026-02-01','2026-02-28',2,2026,'paid','2026-04-03 01:54:36'),(6,1,1,1400.00,'2026-03-01','2026-03-28',3,2026,'overdue','2026-04-03 01:54:36'),(7,1,1,1400.00,'2026-04-01','2026-04-28',4,2026,'unpaid','2026-04-03 01:54:36'),(8,2,2,1100.00,'2025-10-01','2025-10-28',10,2025,'paid','2026-04-03 01:54:36'),(9,2,2,1100.00,'2025-11-01','2025-11-28',11,2025,'paid','2026-04-03 01:54:36'),(10,2,2,1100.00,'2025-12-01','2025-12-28',12,2025,'paid','2026-04-03 01:54:36'),(11,2,2,1100.00,'2026-01-01','2026-01-28',1,2026,'paid','2026-04-03 01:54:36'),(12,2,2,1100.00,'2026-02-01','2026-02-28',2,2026,'overdue','2026-04-03 01:54:36'),(13,2,2,1100.00,'2026-03-01','2026-03-28',3,2026,'unpaid','2026-04-03 01:54:36'),(14,3,3,950.00,'2025-10-01','2025-10-28',10,2025,'paid','2026-04-03 01:54:36'),(15,3,3,950.00,'2025-11-01','2025-11-28',11,2025,'paid','2026-04-03 01:54:36'),(16,3,3,950.00,'2025-12-01','2025-12-28',12,2025,'paid','2026-04-03 01:54:36'),(17,3,3,950.00,'2026-01-01','2026-01-28',1,2026,'unpaid','2026-04-03 01:54:36');
/*!40000 ALTER TABLE `invoices` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `leases`
--

DROP TABLE IF EXISTS `leases`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `leases` (
  `id` int NOT NULL AUTO_INCREMENT,
  `tenant_id` int NOT NULL,
  `apartment_id` int NOT NULL,
  `start_date` date NOT NULL,
  `end_date` date NOT NULL,
  `monthly_rent` decimal(10,2) NOT NULL,
  `deposit_amount` decimal(10,2) NOT NULL,
  `status` enum('active','expired','terminated') DEFAULT 'active',
  `notice_given_date` date DEFAULT NULL,
  `early_termination_fee` decimal(10,2) DEFAULT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `tenant_id` (`tenant_id`),
  KEY `apartment_id` (`apartment_id`),
  CONSTRAINT `leases_ibfk_1` FOREIGN KEY (`tenant_id`) REFERENCES `tenants` (`id`),
  CONSTRAINT `leases_ibfk_2` FOREIGN KEY (`apartment_id`) REFERENCES `apartments` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `leases`
--

LOCK TABLES `leases` WRITE;
/*!40000 ALTER TABLE `leases` DISABLE KEYS */;
INSERT INTO `leases` VALUES (1,1,3,'2025-04-01','2026-04-01',1400.00,2800.00,'active',NULL,NULL,'2026-04-03 01:54:36'),(2,2,2,'2025-06-01','2026-06-01',1100.00,2200.00,'active',NULL,NULL,'2026-04-03 01:54:36'),(3,3,1,'2025-10-01','2026-04-01',950.00,1900.00,'active',NULL,NULL,'2026-04-03 01:54:36'),(4,4,8,'2025-01-01','2027-01-01',1200.00,2400.00,'active',NULL,NULL,'2026-04-03 01:54:36'),(5,1,3,'2024-01-01','2025-01-01',1350.00,2700.00,'expired',NULL,NULL,'2026-04-03 01:54:36');
/*!40000 ALTER TABLE `leases` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `maintenance_requests`
--

DROP TABLE IF EXISTS `maintenance_requests`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `maintenance_requests` (
  `id` int NOT NULL AUTO_INCREMENT,
  `apartment_id` int NOT NULL,
  `tenant_id` int DEFAULT NULL,
  `description` text NOT NULL,
  `priority` enum('Low','Medium','High','Emergency') NOT NULL DEFAULT 'Medium',
  `status` enum('OPEN','IN_PROGRESS','RESOLVED','CLOSED') NOT NULL DEFAULT 'OPEN',
  `submission_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `scheduled_date` datetime DEFAULT NULL,
  `resolution_date` datetime DEFAULT NULL,
  `time_taken` float DEFAULT NULL,
  `cost` decimal(10,2) DEFAULT NULL,
  `assigned_staff` varchar(100) DEFAULT NULL,
  `notes` text,
  PRIMARY KEY (`id`),
  KEY `apartment_id` (`apartment_id`),
  KEY `tenant_id` (`tenant_id`),
  CONSTRAINT `maintenance_requests_ibfk_1` FOREIGN KEY (`apartment_id`) REFERENCES `apartments` (`id`),
  CONSTRAINT `maintenance_requests_ibfk_2` FOREIGN KEY (`tenant_id`) REFERENCES `tenants` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `maintenance_requests`
--

LOCK TABLES `maintenance_requests` WRITE;
/*!40000 ALTER TABLE `maintenance_requests` DISABLE KEYS */;
INSERT INTO `maintenance_requests` VALUES (1,3,1,'Leaking kitchen sink','High','RESOLVED','2025-11-10 09:00:00',NULL,'2025-11-11 14:00:00',2.5,180.00,'Mike Maint','Replaced washer'),(2,2,2,'Broken window latch','Medium','RESOLVED','2025-12-05 11:00:00',NULL,'2025-12-07 10:00:00',1.5,90.00,'Mike Maint','Replaced latch'),(3,1,3,'Boiler not heating','Emergency','IN_PROGRESS','2026-02-20 08:00:00','2026-02-22 09:00:00',NULL,NULL,NULL,'Mike Maint',NULL),(4,3,1,'Cracked bathroom tile','Low','OPEN','2026-03-01 15:00:00',NULL,NULL,NULL,NULL,NULL,NULL),(5,8,4,'Washing machine fault','Medium','OPEN','2026-03-10 10:00:00',NULL,NULL,NULL,NULL,NULL,NULL),(6,10,NULL,'Lobby light flickering','Low','IN_PROGRESS','2026-03-15 09:00:00','2026-03-20 10:00:00',NULL,NULL,NULL,'Mike Maint',NULL);
/*!40000 ALTER TABLE `maintenance_requests` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `payments`
--

DROP TABLE IF EXISTS `payments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `payments` (
  `id` int NOT NULL AUTO_INCREMENT,
  `invoice_id` int NOT NULL,
  `tenant_id` int NOT NULL,
  `amount` decimal(10,2) NOT NULL,
  `payment_date` datetime DEFAULT CURRENT_TIMESTAMP,
  `method` enum('Card','Bank Transfer','Cash') NOT NULL,
  `status` enum('completed','pending','failed') DEFAULT 'completed',
  `late_fee` decimal(10,2) DEFAULT '0.00',
  `receipt_number` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `receipt_number` (`receipt_number`),
  KEY `invoice_id` (`invoice_id`),
  KEY `tenant_id` (`tenant_id`),
  CONSTRAINT `payments_ibfk_1` FOREIGN KEY (`invoice_id`) REFERENCES `invoices` (`id`),
  CONSTRAINT `payments_ibfk_2` FOREIGN KEY (`tenant_id`) REFERENCES `tenants` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `payments`
--

LOCK TABLES `payments` WRITE;
/*!40000 ALTER TABLE `payments` DISABLE KEYS */;
INSERT INTO `payments` VALUES (1,1,1,1400.00,'2025-10-05 00:00:00','Card','completed',0.00,'RCP-00001'),(2,2,1,1400.00,'2025-11-04 00:00:00','Bank Transfer','completed',0.00,'RCP-00002'),(3,3,1,1400.00,'2025-12-03 00:00:00','Card','completed',0.00,'RCP-00003'),(4,4,1,1400.00,'2026-01-06 00:00:00','Card','completed',0.00,'RCP-00004'),(5,5,1,1400.00,'2026-02-03 00:00:00','Bank Transfer','completed',0.00,'RCP-00005'),(6,8,2,1100.00,'2025-10-07 00:00:00','Cash','completed',0.00,'RCP-00006'),(7,9,2,1100.00,'2025-11-05 00:00:00','Card','completed',0.00,'RCP-00007'),(8,10,2,1100.00,'2025-12-04 00:00:00','Card','completed',0.00,'RCP-00008'),(9,11,2,1100.00,'2026-01-07 00:00:00','Bank Transfer','completed',0.00,'RCP-00009'),(10,14,3,950.00,'2025-10-06 00:00:00','Card','completed',0.00,'RCP-00010'),(11,15,3,950.00,'2025-11-08 00:00:00','Cash','completed',0.00,'RCP-00011'),(12,16,3,950.00,'2025-12-06 00:00:00','Card','completed',0.00,'RCP-00012');
/*!40000 ALTER TABLE `payments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `properties`
--

DROP TABLE IF EXISTS `properties`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `properties` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `address` varchar(200) NOT NULL,
  `city` enum('Bristol','Cardiff','London','Manchester') NOT NULL,
  `postcode` varchar(10) NOT NULL,
  `total_units` int NOT NULL,
  `year_built` year DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `properties`
--

LOCK TABLES `properties` WRITE;
/*!40000 ALTER TABLE `properties` DISABLE KEYS */;
INSERT INTO `properties` VALUES (1,'Paragon Bristol','15 Queen Square','Bristol','BS1 4NT',12,2008),(2,'Paragon Cardiff','22 Cardiff Bay Road','Cardiff','CF10 5BT',8,2012),(3,'Paragon London','10 Canary Wharf Lane','London','E14 5AB',20,2015),(4,'Paragon Manchester','5 Spinningfields Ave','Manchester','M3 3AP',10,2018);
/*!40000 ALTER TABLE `properties` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tenants`
--

DROP TABLE IF EXISTS `tenants`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tenants` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `name` varchar(100) NOT NULL,
  `ni_number` varchar(20) NOT NULL,
  `phone` varchar(20) NOT NULL,
  `email` varchar(100) NOT NULL,
  `occupation` varchar(100) DEFAULT NULL,
  `reference1` varchar(200) DEFAULT NULL,
  `reference2` varchar(200) DEFAULT NULL,
  `apartment_type` varchar(50) DEFAULT NULL,
  `lease_period_months` int DEFAULT NULL,
  `registered_date` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ni_number` (`ni_number`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `tenants_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tenants`
--

LOCK TABLES `tenants` WRITE;
/*!40000 ALTER TABLE `tenants` DISABLE KEYS */;
INSERT INTO `tenants` VALUES (1,8,'John Smith','AB123456A','07700900008','john.s@email.com','Software Engineer','Dr. Peter Hall, UWE Bristol','Ms. Carol White','2-Bedroom',12,'2026-04-03 01:54:36'),(2,9,'Sarah Jones','CD789012B','07700900009','sarah.j@email.com','Nurse','Dr. Anna Green, NHS','Mr. Tom Black','1-Bedroom',12,'2026-04-03 01:54:36'),(3,10,'David Brown','EF345678C','07700900010','david.b@email.com','Teacher','Mrs. Jane Doe, Avon School','Mr. Paul Grey','Studio',6,'2026-04-03 01:54:36'),(4,NULL,'Emma Wilson','GH901234D','07700900011','emma.w@email.com','Accountant','Mr. Raj Patel, KPMG','Mrs. Sue Hill','2-Bedroom',24,'2026-04-03 01:54:36');
/*!40000 ALTER TABLE `tenants` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `password_hash` varchar(64) NOT NULL,
  `role` enum('Admin','Manager','FrontDesk','Finance','Maintenance','Tenant') NOT NULL,
  `full_name` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `location` varchar(50) DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT '1',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `last_login` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'admin1','e86f78a8a3caf0b60d8e74e5942aa6d86dc150cd3c03338aef25b7d2d7e3acc7','Admin','Alice Admin','alice@paragon.com','07700900001','Bristol',1,'2026-04-03 01:54:36','2026-04-03 01:56:44'),(2,'manager1','e8392925a98c9c22795d1fc5d0dfee5b9a6943f6b768ec5a2a0c077e5ed119cf','Manager','Mark Manager','mark@paragon.com','07700900002',NULL,1,'2026-04-03 01:54:36',NULL),(3,'frontdesk1','61cb195b78baa109f48faf12a917b0f2c09cebb9ed3b47f977c6d4b64b722f7a','FrontDesk','Fiona Desk','fiona@paragon.com','07700900003','Bristol',1,'2026-04-03 01:54:36',NULL),(4,'finance1','2d1e746e1e575b7c6a0b479d1ee3e410a4b5040da669a5c9fab62d80f65445bf','Finance','Frank Finance','frank@paragon.com','07700900004','Bristol',1,'2026-04-03 01:54:36',NULL),(5,'maint1','9345b8361cfdea0bbec79903743a139a4c27335cd4c6aae693138dfd7f60aac0','Maintenance','Mike Maint','mike@paragon.com','07700900005','Bristol',1,'2026-04-03 01:54:36',NULL),(6,'frontdesk2','61cb195b78baa109f48faf12a917b0f2c09cebb9ed3b47f977c6d4b64b722f7a','FrontDesk','Greg Desk','greg@paragon.com','07700900006','Cardiff',1,'2026-04-03 01:54:36','2026-04-03 01:56:22'),(7,'admin2','e86f78a8a3caf0b60d8e74e5942aa6d86dc150cd3c03338aef25b7d2d7e3acc7','Admin','Bob Admin','bob@paragon.com','07700900007','London',1,'2026-04-03 01:54:36',NULL),(8,'tenant1','556062553bf8fd1b3a295bbc956975943f33f3228b63446df12a75c0144d57db','Tenant','John Smith','john.s@email.com','07700900008',NULL,1,'2026-04-03 01:54:36',NULL),(9,'tenant2','556062553bf8fd1b3a295bbc956975943f33f3228b63446df12a75c0144d57db','Tenant','Sarah Jones','sarah.j@email.com','07700900009',NULL,1,'2026-04-03 01:54:36',NULL),(10,'tenant3','556062553bf8fd1b3a295bbc956975943f33f3228b63446df12a75c0144d57db','Tenant','David Brown','david.b@email.com','07700900010',NULL,1,'2026-04-03 01:54:36',NULL);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-04-03  2:05:27
