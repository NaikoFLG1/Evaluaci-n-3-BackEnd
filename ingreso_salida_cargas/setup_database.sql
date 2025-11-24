CREATE DATABASE forest_log CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'usuario'@'localhost' IDENTIFIED BY 'clave';
GRANT ALL PRIVILEGES ON forest_log.* TO 'usuario'@'localhost';
FLUSH PRIVILEGES;
