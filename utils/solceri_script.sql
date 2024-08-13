CREATE DATABASE solceri;
USE solceri;

CREATE TABLE tbl_Grupos_de_trabajo (
    id_grupo INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(255),
    descripcion TEXT
);

CREATE TABLE tbl_Roles (
    id_rol INT PRIMARY KEY AUTO_INCREMENT,
    rol VARCHAR(255),
    descripcion TEXT
);

CREATE TABLE tbl_Estados (
    id_estado INT PRIMARY KEY AUTO_INCREMENT,
    estado VARCHAR(255),
    descripcion TEXT
);

CREATE TABLE tbl_Categorias (
    id_categoria INT PRIMARY KEY AUTO_INCREMENT,
    categoria VARCHAR(255),
    descripcion TEXT
);

CREATE TABLE tbl_Catalogo (
    id_catalogo INT PRIMARY KEY AUTO_INCREMENT,
    nombre_producto VARCHAR(255),
    descripcion TEXT,
    precio DECIMAL(10, 2)
);

CREATE TABLE tbl_Archivo (
    id_archivo INT PRIMARY KEY AUTO_INCREMENT,
    nombre_archivo VARCHAR(255),
    ruta_archivo VARCHAR(255),
    tamaño_archivo INT,
    fecha_carga DATETIME
);

CREATE TABLE tbl_Usuarios (
    id_usuario INT PRIMARY KEY AUTO_INCREMENT,
    cedula VARCHAR(255),
    correo VARCHAR(255),
    nombre VARCHAR(255),
    primer_apellido VARCHAR(255),
    segundo_apellido VARCHAR(255),
    id_rol INT,
    contraseña VARCHAR(255),
    estado BOOLEAN DEFAULT 0,
    ultima_actividad DATETIME,
    Fecha_Contratacion DATE,
    ruta_imagen VARCHAR(255),
    FOREIGN KEY (id_rol) REFERENCES tbl_Roles(id_rol)
);

CREATE TABLE tbl_Tiquetes (
    id_tiquete INT PRIMARY KEY AUTO_INCREMENT,
    cliente VARCHAR(255),
    resumen TEXT,
    descripcion TEXT,
    grupo_de_trabajo INT,
    trabajador_designado INT,
    prioridad INT,
    categoria INT,
    FOREIGN KEY (grupo_de_trabajo) REFERENCES tbl_Grupos_de_trabajo(id_grupo),
    FOREIGN KEY (trabajador_designado) REFERENCES tbl_Usuarios(id_usuario),
    FOREIGN KEY (categoria) REFERENCES tbl_Categorias(id_categoria)
);

CREATE TABLE tbl_Registros (
    id_registro INT PRIMARY KEY AUTO_INCREMENT,
    id_tiquete INT,
    id_usuario INT,
    fecha_hora DATETIME,
    comentario TEXT,
    FOREIGN KEY (id_tiquete) REFERENCES tbl_Tiquetes(id_tiquete),
    FOREIGN KEY (id_usuario) REFERENCES tbl_Usuarios(id_usuario)
);

CREATE TABLE tbl_Cotizaciones (
    id_cotizacion INT PRIMARY KEY AUTO_INCREMENT,
    id_tiquete INT,
    id_usuario INT,
    FOREIGN KEY (id_tiquete) REFERENCES tbl_Tiquetes(id_tiquete),
    FOREIGN KEY (id_usuario) REFERENCES tbl_Usuarios(id_usuario)
);

CREATE TABLE tbl_Solcitudes_vacaciones (
    id_solicitud INT PRIMARY KEY AUTO_INCREMENT,
    id_usuario INT,
    id_aprobador INT,
    estado VARCHAR(255),
    dia_inicio DATE,
    dia_final DATE,
    dia_aprobacion DATE,
    FOREIGN KEY (id_usuario) REFERENCES tbl_Usuarios(id_usuario),
    FOREIGN KEY (id_aprobador) REFERENCES tbl_Usuarios(id_usuario)
);

CREATE TABLE mtl_Usuarios_Grupos (
    id INT PRIMARY KEY AUTO_INCREMENT,
    id_usuario INT,
    id_grupo INT,
    FOREIGN KEY (id_usuario) REFERENCES tbl_Usuarios(id_usuario),
    FOREIGN KEY (id_grupo) REFERENCES tbl_Grupos_de_trabajo(id_grupo)
);

CREATE TABLE mtl_Tiquetes_archivos (
    id INT PRIMARY KEY AUTO_INCREMENT,
    id_tiquete INT,
    id_archivo INT,
    FOREIGN KEY (id_tiquete) REFERENCES tbl_Tiquetes(id_tiquete),
    FOREIGN KEY (id_archivo) REFERENCES tbl_Archivo(id_archivo)
);

CREATE TABLE mtl_Productos_cotizaciones (
    id INT PRIMARY KEY AUTO_INCREMENT,
    id_catalogo INT,
    id_cotizacion INT,
    producto VARCHAR(255),
    precio DECIMAL(10, 2),
    FOREIGN KEY (id_catalogo) REFERENCES tbl_Catalogo(id_catalogo),
    FOREIGN KEY (id_cotizacion) REFERENCES tbl_Cotizaciones(id_cotizacion)
);

# Cambio a tiquetes, tenia estados como foranea

ALTER TABLE tbl_Tiquetes
ADD COLUMN id_estado INT,
ADD FOREIGN KEY (id_estado) REFERENCES tbl_Estados(id_estado);

# Cambio para visibilidad de sesiones, heartbeats con celery

#ALTER TABLE tbl_Usuarios
#ADD COLUMN estado BOOLEAN DEFAULT 0,
#ADD COLUMN ultima_actividad DATETIME;
#ADD COLUMN Fecha_Contratacion DATE;

#
ALTER TABLE tbl_Tiquetes
ADD COLUMN fecha_creacion DATETIME,
ADD COLUMN ultima_asignacion DATETIME;


ALTER TABLE tbl_solcitudes_vacaciones
ADD COLUMN fecha_solicitud DATETIME;

#Se jodio la empanada
ALTER TABLE tbl_solcitudes_vacaciones RENAME tbl_solicitudes_vacaciones;

# Insertar roles

INSERT INTO roles (rol, descripcion) VALUES
('Administrador', 'Rol con privilegios administrativos'),
('Colaborador', 'Rol para usuarios colaboradores'),
('Cliente', 'Rol para usuarios clientes');


