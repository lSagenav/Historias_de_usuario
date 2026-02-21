# Historia de Usuario – Semana 2

A continuación presento el desarrollo de la historia de usuario correspondiente a la semana 2. Incluye la creación de la base de datos, tablas, inserción de datos, consultas, vista, permisos y transacciones. El objetivo es demostrar el uso de SQL (DDL, DML, DQL, DCL y TCL) aplicado a un sistema académico sencillo.

---

## TASK 1 – Creación de la base de datos y tablas

```sql
CREATE DATABASE gestion_academica_universidad;
USE gestion_academica_universidad;
```

```sql
CREATE TABLE estudiantes (
 id_estudiante INT AUTO_INCREMENT PRIMARY KEY,
 nombre_completo VARCHAR(100) NOT NULL,
 correo_electronico VARCHAR(100) NOT NULL UNIQUE,
 genero ENUM('M','F','Otro') NOT NULL,
 identificacion VARCHAR(20) NOT NULL UNIQUE,
 carrera VARCHAR(100) NOT NULL,
 fecha_nacimiento DATE NOT NULL,
 fecha_ingreso DATE NOT NULL,
 CHECK (fecha_ingreso >= fecha_nacimiento)
);

CREATE TABLE docentes (
 id_docente INT AUTO_INCREMENT PRIMARY KEY,
 nombre_completo VARCHAR(100) NOT NULL,
 correo_institucional VARCHAR(100) NOT NULL UNIQUE,
 departamento_academico VARCHAR(100) NOT NULL,
 anios_experiencia INT NOT NULL CHECK (anios_experiencia >= 0)
);

CREATE TABLE cursos (
 id_curso INT AUTO_INCREMENT PRIMARY KEY,
 nombre VARCHAR(100) NOT NULL,
 codigo VARCHAR(20) NOT NULL UNIQUE,
 creditos INT NOT NULL CHECK (creditos > 0),
 semestre INT NOT NULL CHECK (semestre >= 1),
 id_docente INT,
 FOREIGN KEY (id_docente) REFERENCES docentes(id_docente) ON DELETE SET NULL
);

CREATE TABLE inscripciones (
 id_inscripcion INT AUTO_INCREMENT PRIMARY KEY,
 id_estudiante INT NOT NULL,
 id_curso INT NOT NULL,
 fecha_inscripcion DATE NOT NULL,
 calificacion_final DECIMAL(4,2) CHECK (calificacion_final BETWEEN 0 AND 5),
 FOREIGN KEY (id_estudiante) REFERENCES estudiantes(id_estudiante) ON DELETE CASCADE,
 FOREIGN KEY (id_curso) REFERENCES cursos(id_curso) ON DELETE CASCADE
);
```

---

## TASK 2 – Inserción de datos

```sql
INSERT INTO docentes VALUES
(NULL,'Carlos Ramirez','carlos@uni.edu','Ingenieria',10),
(NULL,'Ana Torres','ana@uni.edu','Matematicas',6),
(NULL,'Luis Gomez','luis@uni.edu','Humanidades',3);

INSERT INTO estudiantes VALUES
(NULL,'Maria Lopez','maria@gmail.com','F','1001','Ingenieria','2000-05-10','2022-01-15'),
(NULL,'Juan Perez','juan@gmail.com','M','1002','Matematicas','1999-08-20','2021-01-15'),
(NULL,'Sofia Martinez','sofia@gmail.com','F','1003','Derecho','2001-02-11','2023-01-15'),
(NULL,'Pedro Sanchez','pedro@gmail.com','M','1004','Ingenieria','2000-11-01','2022-01-15'),
(NULL,'Laura Diaz','laura@gmail.com','F','1005','Administracion','1998-03-25','2020-01-15');

INSERT INTO cursos VALUES
(NULL,'Base de Datos','BD101',3,2,1),
(NULL,'Calculo I','MAT101',4,1,2),
(NULL,'Etica Profesional','HUM201',2,3,3),
(NULL,'Programacion','PROG101',3,2,1);

INSERT INTO inscripciones VALUES
(NULL,1,1,'2024-02-01',4.5),
(NULL,1,2,'2024-02-01',3.8),
(NULL,2,1,'2024-02-01',4.0),
(NULL,2,3,'2024-02-01',3.5),
(NULL,3,2,'2024-02-01',4.2),
(NULL,4,4,'2024-02-01',3.9),
(NULL,5,1,'2024-02-01',4.7),
(NULL,5,3,'2024-02-01',4.1);
```

---

## TASK 3 – Consultas básicas

```sql
SELECT e.nombre_completo, c.nombre AS curso, i.calificacion_final
FROM estudiantes e
JOIN inscripciones i ON e.id_estudiante = i.id_estudiante
JOIN cursos c ON i.id_curso = c.id_curso;
```

```sql
SELECT c.nombre, d.nombre_completo
FROM cursos c
JOIN docentes d ON c.id_docente = d.id_docente
WHERE d.anios_experiencia > 5;
```

```sql
SELECT c.nombre, AVG(i.calificacion_final) AS promedio
FROM cursos c
JOIN inscripciones i ON c.id_curso = i.id_curso
GROUP BY c.nombre;
```

```sql
SELECT id_estudiante, COUNT(*)
FROM inscripciones
GROUP BY id_estudiante
HAVING COUNT(*) > 1;
```

```sql
ALTER TABLE estudiantes ADD estado_academico VARCHAR(50);
```

```sql
DELETE FROM docentes WHERE id_docente = 3;
SELECT * FROM cursos;
```

```sql
SELECT c.nombre, COUNT(*)
FROM inscripciones i
JOIN cursos c ON c.id_curso = i.id_curso
GROUP BY c.nombre
HAVING COUNT(*) > 2;
```

---

## TASK 4 – Subconsultas y funciones

```sql
SELECT id_estudiante, AVG(calificacion_final)
FROM inscripciones
GROUP BY id_estudiante
HAVING AVG(calificacion_final) > (SELECT AVG(calificacion_final) FROM inscripciones);
```

```sql
SELECT DISTINCT carrera
FROM estudiantes
WHERE id_estudiante IN (
 SELECT i.id_estudiante
 FROM inscripciones i
 JOIN cursos c ON c.id_curso = i.id_curso
 WHERE c.semestre >= 2
);
```

```sql
SELECT
 SUM(calificacion_final),
 MAX(calificacion_final),
 MIN(calificacion_final),
 COUNT(*),
 ROUND(AVG(calificacion_final),2)
FROM inscripciones;
```

---

## TASK 5 – Vista

```sql
CREATE VIEW vista_historial_academico AS
SELECT e.nombre_completo, c.nombre, d.nombre_completo, c.semestre, i.calificacion_final
FROM inscripciones i
JOIN estudiantes e ON i.id_estudiante = e.id_estudiante
JOIN cursos c ON i.id_curso = c.id_curso
JOIN docentes d ON c.id_docente = d.id_docente;
```

---

## TASK 6 – Permisos y transacciones

```sql
CREATE ROLE revisor_academico;
GRANT SELECT ON gestion_academica_universidad.vista_historial_academico TO revisor_academico;
REVOKE INSERT, UPDATE, DELETE ON gestion_academica_universidad.inscripciones FROM revisor_academico;
```

```sql
START TRANSACTION;
UPDATE inscripciones SET calificacion_final = 5.0 WHERE id_inscripcion = 1;
SAVEPOINT cambio1;
UPDATE inscripciones SET calificacion_final = 2.0 WHERE id_inscripcion = 1;
ROLLBACK TO cambio1;
COMMIT;
```



