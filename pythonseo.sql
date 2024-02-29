-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1:3306
-- Généré le : jeu. 29 fév. 2024 à 15:07
-- Version du serveur : 8.0.31
-- Version de PHP : 8.0.26

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `pythonseo`
--

-- --------------------------------------------------------

--
-- Structure de la table `analysis`
--

DROP TABLE IF EXISTS `analysis`;
CREATE TABLE IF NOT EXISTS `analysis` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `url` varchar(255) DEFAULT NULL,
  `title_tag` varchar(255) DEFAULT NULL,
  `internal_links` int DEFAULT NULL,
  `external_links` int DEFAULT NULL,
  `broken_internal_links` int DEFAULT NULL,
  `broken_external_links` int DEFAULT NULL,
  `h1_tag` varchar(255) DEFAULT NULL,
  `h2_tags` int DEFAULT NULL,
  `h3_tags` int DEFAULT NULL,
  `img_without_alt` int DEFAULT NULL,
  `header_tag` tinyint(1) DEFAULT NULL,
  `main_tag` tinyint(1) DEFAULT NULL,
  `footer_tag` tinyint(1) DEFAULT NULL,
  `nav_tags` int DEFAULT NULL,
  `div_nesting` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ;

-- --------------------------------------------------------

--
-- Structure de la table `user`
--

DROP TABLE IF EXISTS `user`;
CREATE TABLE IF NOT EXISTS `user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `password` varchar(254) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Structure de la table `users`
--

DROP TABLE IF EXISTS `users`;
CREATE TABLE IF NOT EXISTS `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4;

--
-- Déchargement des données de la table `users`
--

INSERT INTO `users` (`id`, `email`, `password`) VALUES
(1, 'admin', '123');

--
-- Contraintes pour les tables déchargées
--

--
-- Contraintes pour la table `analysis`
--
ALTER TABLE `analysis`
  ADD CONSTRAINT `analysis_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
