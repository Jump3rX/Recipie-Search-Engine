-- phpMyAdmin SQL Dump
-- version 4.9.0.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jan 07, 2020 at 02:35 PM
-- Server version: 10.4.6-MariaDB
-- PHP Version: 7.3.8

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `erecipies`
--

-- --------------------------------------------------------

--
-- Table structure for table `recipies`
--

CREATE TABLE `recipies` (
  `id` int(11) NOT NULL,
  `title` text NOT NULL,
  `ingredients` text NOT NULL,
  `steps` text NOT NULL,
  `author` varchar(200) NOT NULL,
  `time_created` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `recipies`
--

INSERT INTO `recipies` (`id`, `title`, `ingredients`, `steps`, `author`, `time_created`) VALUES
(2, 'Spinach Salad Dressing', '2 cloves garlic\r\n2 tbsp. red vinegar 1 tsp. sugar\r\n1 tsp. salt\r\n1/2 tsp. pepper\r\n1 tsp dry mustard\r\n6 tbsp. salad oil (Olive oil or Becel)', 'Mix all ingredients gently in a small jar. Cover with a lid and let stand in\r\nthe refrigerator at least overnight. ', 'paul@yahoo.com', '2020-01-01 11:34:50'),
(3, 'Cherry Pie', '2-3/4 cup frozen or thawed cherries (preferably sour)\r\n2/3 cup juice raspberry or pineapple, orange or other juice you like\r\n1/4 cup corn syrup\r\n2- 2/3 tablespoons corn starch\r\n1/8 tsp salt\r\n1 cup granulated sugar', 'Thaw and drain cherries. Place juice except about three tablespoons in a\r\nsauce pan with the corn syrup. Bring to boil. Dissolve corn starch in reserve juice and add alternately with mixed salt and sugar to boiling syrup, stirring constantly till mixture becomes thick and clear. Continue boiling for a minute or 2. Remove from heat, stir in cherries and cool. When cold, turn into a pastry lined pie pan and bake ten minutes at 450 degrees, reduce heat to 350 and continue to bake for 25 more minutes. This pie also tastes good with a meringue topping to which a few drops of almond extract have been added.', 'paul@yahoo.com', '2020-01-01 11:37:42');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `name` varchar(80) NOT NULL,
  `email` varchar(100) NOT NULL,
  `username` varchar(100) NOT NULL,
  `password` varchar(100) NOT NULL,
  `user_photo` longblob NOT NULL,
  `date_joined` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `name`, `email`, `username`, `password`, `user_photo`, `date_joined`) VALUES
(7, 'paul', 'paul@yahoo.com', 'paul22', '$5$rounds=535000$gYgafWMx9SrTSe/H$8UJbHPlxNDaQCAB8i00wyz9zvZ1zGe8N2wik4SYbmS8', '', '2020-01-01 12:54:23'),
(8, 'conrad', 'conrad@yahoo.com', 'con', '$5$rounds=535000$dysTpaZk.4/QsTXQ$hlFABONqv.QNs7OH8hqzde.v0295XDzOtww6EAFfep.', '', '2020-01-07 14:37:33');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `recipies`
--
ALTER TABLE `recipies`
  ADD PRIMARY KEY (`id`);
ALTER TABLE `recipies` ADD FULLTEXT KEY `title` (`title`,`ingredients`,`steps`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `recipies`
--
ALTER TABLE `recipies`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
