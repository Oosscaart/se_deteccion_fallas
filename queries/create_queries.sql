----------------------------------------- CREACION DE TABLAS ------------------------------------------
-- Creacion tabla fallas
CREATE TABLE fallas_computadora (
    id INT AUTO_INCREMENT,
    nombre VARCHAR(255) NOT NULL,
    descripcion TEXT NOT NULL,
    imagen LONGBLOB NOT NULL,
    PRIMARY KEY (id, nombre)
);

-- Creacion tabla caracteristicas
CREATE TABLE caracteristicas (
    id INT AUTO_INCREMENT,
    nombre VARCHAR(255) NOT NULL,
    imagen LONGBLOB NOT NULL,
    PRIMARY KEY (id, nombre)
);

--Creacion tabla caracteristicas fallas
CREATE TABLE caracteristicas_fallas_computadora (
    id_fallas_computadora INT,
    id_caracteristicas INT,
    peso DECIMAL(5, 2),
    PRIMARY KEY (id_fallas_computadora, id_caracteristicas),
    FOREIGN KEY (id_fallas_computadora) REFERENCES fallas_computadora(id),
    FOREIGN KEY (id_caracteristicas) REFERENCES caracteristicas(id)
);

---------------------------------------------------------------------------------------------------------

