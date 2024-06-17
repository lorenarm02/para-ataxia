DROP DATABASE IF EXISTS bdataxia;
CREATE DATABASE bdataxia;
USE bdataxia;

-- Tabla para roles
CREATE TABLE roles (
    nombre VARCHAR(50) PRIMARY KEY
);

-- Tabla para usuarios
CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario VARCHAR(50),
    passwd VARCHAR(500),
    rol VARCHAR(50) NOT NULL,
    FOREIGN KEY (rol) REFERENCES roles(nombre)
);

-- Tabla para tipos de ataxia
CREATE TABLE tiposAtaxia (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) UNIQUE NOT NULL,
    descripcion TEXT
);

-- Tabla para publicaciones sobre ataxia
CREATE TABLE publicaciones (
    id INT AUTO_INCREMENT PRIMARY KEY,
	idUsuario INT,
    idTipoAtaxia INT,
    -- imagen_url VARCHAR(500) NOT NULL,
    descripcion TEXT,
    fecha_publicacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    likes INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (idUsuario) REFERENCES usuarios(id),
    FOREIGN KEY (idTipoAtaxia) REFERENCES tiposAtaxia(id)
);

-- Tabla para los likes de las publicaciones
CREATE TABLE likes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    idUsuario INT,
    idPublicacion INT,
    FOREIGN KEY (idUsuario) REFERENCES usuarios(id),
    FOREIGN KEY (idPublicacion) REFERENCES publicaciones(id),
    UNIQUE(idUsuario, idPublicacion)
);

-- Insertar roles
INSERT INTO roles (nombre) VALUES
('administrador'),
('usuario');

-- Insertar usuarios
INSERT INTO usuarios (usuario, passwd, rol) VALUES
('admin', 'Soyadmin1', 'administrador'),
('profe', 'Elprofe00', 'usuario'),
('lorenarm02', 'Lalore02', 'usuario');

-- Insertar tipos de ataxia
INSERT INTO tiposAtaxia (nombre, descripcion) VALUES
('Ataxia episódica', 'Es un tipo de ataxia hereditario. Tiene episodios breves que pueden durar segundos o minutos. No acorta la esperanza de vida,  y los síntomas pueden responder a ciertos medicamentos.'),
('Ataxia de Friedreich', 'Es un tipo de ataxia hereditario. Causa daño progresivo al sistema nervioso, lesiones en la médula espinal, cerebelo y los nervios periféricos.'),
('Ataxia telangiectasia', 'Es un tipo de ataxia hereditario. Es raro ya que afecta muchos sistemas del cuerpo y degeneración en el cerebro.'),
('Ataxia cerebelosa congénita', 'Es un tipo de ataxia hereditario. Tiene la consecuencia del daño al cerebelo en el nacimiento.'),
('Enfermedad de Wilson', 'Es un tipo de ataxia hereditario. Se provocada por una acumulación de cobre en el hígado, cerebro y otros órganos.'),
('Anormalidad congénita','Es un tipo de ataxia no hereditario. Porque el cerebelo se ha formado de forma inusual durante el embarazo.'),
('Metabólicas','Es un tipo de ataxia no hereditario. Es debido a la mala absorción de nutrientes de los alimentos.'),
('Por traumatismo','Es un tipo de ataxia no hereditario. Es producida por un golpe y/o lesión.'),
('Por infección','Es un tipo de ataxia no hereditario. Son provocados por el consumo de drogas o toxinas nocivas para la salud.'),
('Por tumores','Es un tipo de ataxia no hereditario. Es un tumor en el cerebro haya sido extirpado o no, puede causar daños.');

-- Insertar publicaciones sobre ataxia
INSERT INTO publicaciones (idUsuario, idTipoAtaxia, descripcion) VALUES
(2, 1, 'Soy usuaria de ataxia de Friedeich, maldita enfermedad.'),
(3, 2, 'Tengo un conocido con esta enfermedad y esta bien afectado.');

COMMIT;