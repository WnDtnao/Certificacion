-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema certificacion
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema certificacion
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `certificacion` DEFAULT CHARACTER SET utf8 ;
USE `certificacion` ;

-- -----------------------------------------------------
-- Table `certificacion`.`usuarios`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `certificacion`.`usuarios` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(45) NOT NULL,
  `apellido` VARCHAR(45) NOT NULL,
  `email` VARCHAR(254) NOT NULL,
  `password` VARCHAR(255) NOT NULL,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `uq_usuarios_email` (`email` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `certificacion`.`peliculas`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `certificacion`.`peliculas` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nombre_pelicula` VARCHAR(45) NULL,
  `director` VARCHAR(45) NULL,
  `fecha_estreno` VARCHAR(45) NULL,
  `sinopsis` TEXT NULL,
  `usuario_id` INT NOT NULL,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_peliculas_usuarios_idx` (`usuario_id` ASC) VISIBLE,
  CONSTRAINT `fk_peliculas_usuarios`
    FOREIGN KEY (`usuario_id`)
    REFERENCES `certificacion`.`usuarios` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `certificacion`.`comentarios`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `certificacion`.`comentarios` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `comentario` TEXT NOT NULL,
  `usuario_id` INT NOT NULL,
  `pelicula_id` INT NOT NULL,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_comentarios_usuarios_idx` (`usuario_id` ASC) VISIBLE,
  INDEX `fk_comentarios_peliculas1_idx` (`pelicula_id` ASC) VISIBLE,
  CONSTRAINT `fk_comentarios_usuarios`
    FOREIGN KEY (`usuario_id`)
    REFERENCES `certificacion`.`usuarios` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_comentarios_peliculas1`
    FOREIGN KEY (`pelicula_id`)
    REFERENCES `certificacion`.`peliculas` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Nuevas tablas para organizar viajes e inscribir viajeros.
-- Las tablas antiguas de películas y comentarios se conservan sin cambios.
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `certificacion`.`viajes` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `destino` VARCHAR(120) NOT NULL,
  `fecha_inicio` DATE NOT NULL,
  `fecha_fin` DATE NOT NULL,
  `itinerario` VARCHAR(40) NOT NULL,
  `organizador_id` INT NOT NULL,
  `created_at` DATETIME NOT NULL,
  `updated_at` DATETIME NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_viajes_usuarios_idx` (`organizador_id` ASC),
  CONSTRAINT `fk_viajes_usuarios`
    FOREIGN KEY (`organizador_id`)
    REFERENCES `certificacion`.`usuarios` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS `certificacion`.`viajeros` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `viaje_id` INT NOT NULL,
  `usuario_id` INT NOT NULL,
  `created_at` DATETIME NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `uq_viajeros_viaje_usuario` (`viaje_id` ASC, `usuario_id` ASC),
  INDEX `fk_viajeros_usuarios_idx` (`usuario_id` ASC),
  CONSTRAINT `fk_viajeros_viajes`
    FOREIGN KEY (`viaje_id`)
    REFERENCES `certificacion`.`viajes` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_viajeros_usuarios`
    FOREIGN KEY (`usuario_id`)
    REFERENCES `certificacion`.`usuarios` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;