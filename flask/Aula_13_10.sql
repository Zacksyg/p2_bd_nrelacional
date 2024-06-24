CREATE DATABASE aula_13_10;

USE aula_13_10;

CREATE TABLE funcionarios(
id INT AUTO_INCREMENT PRIMARY KEY,
primeiro_nome VARCHAR(50) NOT NULL,
sobrenome VARCHAR(50) NOT NULL,
data_admissao DATE NOT NULL,
status_funcionario BOOL NOT NULL,
);


