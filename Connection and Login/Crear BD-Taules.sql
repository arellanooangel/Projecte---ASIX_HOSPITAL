-- Crear extensió per al hash
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- Crear taula d'usuaris
CREATE TABLE IF NOT EXISTS usuaris (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role VARCHAR(20) NOT NULL
);

-- Inserir administrador per defecte
INSERT INTO usuaris (username, password, role)
VALUES (
    'ua-admin',
    encode(digest('admin123', 'sha256'), 'hex'),
    'admin'
)
    -- digest genera el hash SHA-256 de la contrasenya
    -- encode converteix aquest hash a text hexadecimal
ON CONFLICT (username) DO NOTHING;