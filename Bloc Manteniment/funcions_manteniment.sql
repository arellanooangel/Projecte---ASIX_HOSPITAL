-- ==========================================================
-- PROCEDIMENTS I FUNCIONS D'ALTA (MANTENIMENT)
-- ==========================================================
SET search_path TO hospital;

-- 1. Procediment per a l'Alta de Personal completa
CREATE OR REPLACE PROCEDURE sp_alta_personal(
    p_dni VARCHAR, 
    p_nom VARCHAR, 
    p_cog1 VARCHAR, 
    p_cog2 VARCHAR, 
    p_email VARCHAR,
    p_user VARCHAR, 
    p_pass TEXT, 
    p_rol VARCHAR, -- 'METGE', 'INFERMER', 'ADMIN', 'VARI'
    p_extra TEXT   -- Especialitat per a metges o curs per a infermers
) AS $$
DECLARE
    v_id_pers INTEGER;
    v_id_esp INTEGER;
BEGIN
    -- Inserir a la taula base personal
    INSERT INTO personal (dni, nom, cognom1, cognom2, email)
    VALUES (p_dni, p_nom, p_cog1, p_cog2, p_email)
    RETURNING id_personal INTO v_id_pers;

    -- Inserir a la taula usuaris amb hash SHA-256
    INSERT INTO usuaris (username, password, id_personal)
    VALUES (p_user, encode(digest(p_pass, 'sha256'), 'hex'), v_id_pers);

    -- Lògica d'assignació de rols
    CASE UPPER(p_rol)
        WHEN 'METGE' THEN
            -- Busquem o creem l'especialitat
            SELECT id_especialitat INTO v_id_esp FROM especialitat WHERE descripcio = p_extra;
            IF NOT FOUND THEN
                INSERT INTO especialitat (descripcio) VALUES (p_extra) RETURNING id_especialitat INTO v_id_esp;
            END IF;
            INSERT INTO metge (id_personal, estudis, experiencia, id_especialitat)
            VALUES (v_id_pers, 'Grau en Medicina', 'Sènior', v_id_esp);
            
        WHEN 'INFERMER' THEN
            INSERT INTO infermer (id_personal, curs, experiencia)
            VALUES (v_id_pers, p_extra, 'Estàndard');
            
        ELSE -- Cas Vari o Administratiu
            INSERT INTO vari (id_personal, feina)
            VALUES (v_id_pers, COALESCE(p_extra, p_rol));
    END CASE;
    
    RAISE NOTICE 'Personal % creat correctament amb ID %', p_nom, v_id_pers;
END;
$$ LANGUAGE plpgsql;

-- 2. Funció per a l'Alta de Pacients
CREATE OR REPLACE FUNCTION donar_alta_pacient(
    p_ts VARCHAR,
    p_nom VARCHAR,
    p_cog1 VARCHAR,
    p_cog2 VARCHAR,
    p_naixement DATE
) RETURNS TEXT AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM pacient WHERE targeta_sanitaria = p_ts) THEN
        RETURN 'Error: El pacient ja existeix.';
    END IF;

    INSERT INTO pacient (targeta_sanitaria, nom, cognom1, cognom2, data_naixement)
    VALUES (p_ts, p_nom, p_cog1, p_cog2, p_naixement);

    RETURN 'Pacient ' || p_nom || ' registrat correctament.';
END;
$$ LANGUAGE plpgsql;