CREATE DATABASE store;
USE store;

-- Path: stock.sql
CREATE TABLE `product` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `description` varchar(255) NOT NULL,
  `price` int NOT NULL,
  `quantity` int NOT NULL,
  `category_id` int NOT NULL,
  PRIMARY KEY (`id`)
);

CREATE TABLE `category` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
);


INSERT INTO `category` (`id`, `name`) VALUES
(1, 'Electronics'),
(2, 'Clothes'),
(3, 'Books'),
(4, 'Food'),
(5, 'Toys');
