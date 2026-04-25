-- ==========================================================
-- CONSULTES D'AGENDA I PLANIFICACIÓ
-- ==========================================================
SET search_path TO hospital;

-- 1. Funció per consultar l'agenda de Quiròfan per dia
CREATE OR REPLACE FUNCTION get_agenda_quirofan(
    p_data DATE, 
    p_quirofan INT, 
    p_planta INT
)
RETURNS TABLE(
    hora_operacio TIME, 
    nom_pacient TEXT, 
    nom_metge TEXT, 
    personal_infermeria TEXT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        o.data_hora::time,
        (pa.nom || ' ' || pa.cognom1 || ' ' || COALESCE(pa.cognom2, '')),
        (per_m.nom || ' ' || per_m.cognom1),
        string_agg(per_i.nom || ' ' || per_i.cognom1, ', ')
    FROM operacio o
    JOIN pacient pa ON o.targeta_sanitaria = pa.targeta_sanitaria
    JOIN metge m ON o.id_metge = m.id_personal
    JOIN personal per_m ON m.id_personal = per_m.id_personal
    LEFT JOIN operacio_infermer oi ON o.id_operacio = oi.id_operacio
    LEFT JOIN personal per_i ON oi.id_infermer = per_i.id_personal
    WHERE o.data_hora::date = p_data 
      AND o.id_quirofan = p_quirofan 
      AND o.id_planta = p_planta
    GROUP BY o.id_operacio, o.data_hora, pa.nom, pa.cognom1, pa.cognom2, per_m.nom, per_m.cognom1
    ORDER BY o.data_hora ASC;
END;
$$ LANGUAGE plpgsql;

-- 2. Vista per a les visites planificades (Requeriment: Pacient, Hora, Metge)
CREATE OR REPLACE VIEW v_planificacio_diaria AS
SELECT 
    v.data_hora::date AS dia,
    v.data_hora::time AS hora_entrada,
    (p_m.nom || ' ' || p_m.cognom1) AS metge,
    (p_p.nom || ' ' || p_p.cognom1) AS pacient
FROM visita v
JOIN personal p_m ON v.id_metge = p_m.id_personal
JOIN pacient p_p ON v.targeta_sanitaria = p_p.targeta_sanitaria;