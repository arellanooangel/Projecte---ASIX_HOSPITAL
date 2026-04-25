CREATE OR REPLACE FUNCTION planificar_visita(
    p_pacient_id INT,
    p_metge_id INT,
    p_data_hora TIMESTAMP
) RETURNS TEXT AS $$
DECLARE
    v_existeix_conflicte INTEGER;
BEGIN
    -- 1. Validem si el metge ja té una visita en aquella hora exacta
    SELECT COUNT(*) INTO v_existeix_conflicte
    FROM visites
    WHERE id_metge = p_metge_id AND data_visita = p_data_hora;

    IF v_existeix_conflicte > 0 THEN
        RETURN 'Error: El metge ja té una visita assignada a aquesta hora.';
    END IF;

    -- 2. Inserim la visita si tot és correcte
    INSERT INTO visites (id_pacient, id_metge, data_visita)
    VALUES (p_pacient_id, p_metge_id, p_data_hora);

    RETURN 'Visita planificada correctament per al dia ' || p_data_hora::date;
END;
$$ LANGUAGE plpgsql;