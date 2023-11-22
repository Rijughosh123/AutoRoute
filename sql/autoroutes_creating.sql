-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Mar 29, 2022 at 07:31 PM
-- Server version: 10.4.22-MariaDB
-- PHP Version: 7.4.27

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `smartdelivery`
--

-- --------------------------------------------------------

--
-- Table structure for table `autoroutes_creating`
--

CREATE TABLE `autoroutes_creating` (
  `id` int(11) NOT NULL,
  `supplier_id` int(11) NOT NULL,
  `route_name` varchar(100) DEFAULT NULL,
  `delivery_date` date DEFAULT NULL,
  `delivery_time` varchar(20) DEFAULT NULL,
  `service_time` varchar(20) DEFAULT NULL,
  `loading_time` varchar(20) DEFAULT NULL,
  `route_id` varchar(100) NOT NULL,
  `list_id` int(11) NOT NULL,
  `pin_color` varchar(20) DEFAULT NULL,
  `start_address_id` varchar(255) NOT NULL DEFAULT '0',
  `end_address_id` varchar(255) NOT NULL DEFAULT '0',
  `route_created_status` enum('Creating','Reorder','Created') NOT NULL DEFAULT 'Creating',
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  `updated_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `autoroutes_creating`
--

INSERT INTO `autoroutes_creating` (`id`, `supplier_id`, `route_name`, `delivery_date`, `delivery_time`, `service_time`, `loading_time`, `route_id`, `list_id`, `pin_color`, `start_address_id`, `end_address_id`, `route_created_status`, `created_at`, `updated_at`) VALUES
(283, 32, '1', NULL, NULL, NULL, NULL, '1', 344, 'FFBF00', '0', '0', 'Creating', '2022-03-28 10:56:48', '2022-03-28 10:56:48'),
(284, 32, '2', NULL, NULL, NULL, NULL, '2', 344, 'FF7F50', '0', '0', 'Creating', '2022-03-28 10:56:49', '2022-03-28 10:56:49'),
(285, 32, '3', NULL, NULL, NULL, NULL, '3', 344, 'CCCCFF', '0', '0', 'Creating', '2022-03-28 10:56:49', '2022-03-28 10:56:49'),
(286, 32, '4', NULL, NULL, NULL, NULL, '4', 344, '40E0D0', '0', '0', 'Creating', '2022-03-28 10:56:49', '2022-03-28 10:56:49'),
(356, 32, '1', NULL, NULL, NULL, NULL, '1', 345, 'FFBF00', '0', '0', 'Creating', '2022-03-28 15:51:26', '2022-03-28 15:51:26'),
(357, 32, '2', NULL, NULL, NULL, NULL, '2', 345, 'FF7F50', '0', '0', 'Creating', '2022-03-28 15:51:26', '2022-03-28 15:51:26'),
(358, 32, '3', NULL, NULL, NULL, NULL, '3', 345, 'CCCCFF', '0', '0', 'Creating', '2022-03-28 15:51:26', '2022-03-28 15:51:26'),
(359, 32, '4', NULL, NULL, NULL, NULL, '4', 345, '40E0D0', '0', '0', 'Creating', '2022-03-28 15:51:26', '2022-03-28 15:51:26'),
(502, 32, '1', NULL, NULL, NULL, NULL, '1', 352, 'FFBF00', '0', '0', 'Creating', '2022-03-28 17:41:56', '2022-03-28 17:41:56'),
(503, 32, '2', NULL, NULL, NULL, NULL, '2', 352, 'FF7F50', '0', '0', 'Creating', '2022-03-28 17:41:56', '2022-03-28 17:41:56'),
(504, 32, '3', NULL, NULL, NULL, NULL, '3', 352, 'CCCCFF', '0', '0', 'Creating', '2022-03-28 17:41:56', '2022-03-28 17:41:56'),
(505, 32, '4', NULL, NULL, NULL, NULL, '4', 352, '40E0D0', '0', '0', 'Creating', '2022-03-28 17:41:56', '2022-03-28 17:41:56'),
(506, 32, '5', NULL, NULL, NULL, NULL, '5', 352, 'FF00FF', '0', '0', 'Creating', '2022-03-28 17:41:56', '2022-03-28 17:41:56'),
(507, 32, '6', NULL, NULL, NULL, NULL, '6', 352, '008080', '0', '0', 'Creating', '2022-03-28 17:41:56', '2022-03-28 17:41:56');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `autoroutes_creating`
--
ALTER TABLE `autoroutes_creating`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `autoroutes_creating`
--
ALTER TABLE `autoroutes_creating`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=508;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
