CREATE DATABASE IF NOT EXISTS `certificacion`
    DEFAULT CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;
USE `certificacion`;

CREATE TABLE IF NOT EXISTS `usuarios` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `nombre` VARCHAR(45) NOT NULL,
    `apellido` VARCHAR(45) NOT NULL,
    `email` VARCHAR(254) NOT NULL,
    `password` VARCHAR(255) NOT NULL,
    `created_at` DATETIME NOT NULL,
    `updated_at` DATETIME NOT NULL,
    PRIMARY KEY (`id`),
    UNIQUE INDEX `uq_usuarios_email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- cada viaje le pertenece a quien lo organiza
CREATE TABLE IF NOT EXISTS `viajes` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `destino` VARCHAR(120) NOT NULL,
    `fecha_inicio` DATE NOT NULL,
    `fecha_fin` DATE NOT NULL,
    `itinerario` VARCHAR(40) NOT NULL,
    `organizador_id` INT NOT NULL,
    `created_at` DATETIME NOT NULL,
    `updated_at` DATETIME NOT NULL,
    PRIMARY KEY (`id`),
    INDEX `fk_viajes_usuarios_idx` (`organizador_id`),
    CONSTRAINT `fk_viajes_usuarios`
        FOREIGN KEY (`organizador_id`)
        REFERENCES `usuarios` (`id`)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- quien se une a cada viaje, sin poder inscribirse dos veces
CREATE TABLE IF NOT EXISTS `viajeros` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `viaje_id` INT NOT NULL,
    `usuario_id` INT NOT NULL,
    `created_at` DATETIME NOT NULL,
    PRIMARY KEY (`id`),
    UNIQUE INDEX `uq_viajeros_viaje_usuario` (`viaje_id`, `usuario_id`),
    INDEX `fk_viajeros_usuarios_idx` (`usuario_id`),
    CONSTRAINT `fk_viajeros_viajes`
        FOREIGN KEY (`viaje_id`)
        REFERENCES `viajes` (`id`)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT `fk_viajeros_usuarios`
        FOREIGN KEY (`usuario_id`)
        REFERENCES `usuarios` (`id`)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
