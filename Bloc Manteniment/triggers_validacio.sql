-- ==========================================================
-- TRIGGERS DE VALIDACIÓ (INTEGRITAT DE DADES)
-- ==========================================================
SET search_path TO hospital;

-- Funció de validació per al Trigger
CREATE OR REPLACE FUNCTION fn_validar_infermeria()
RETURNS TRIGGER AS $$
BEGIN
    -- Si s'insereix a inferm_planta, comprovem que no estigui ja a inferm_metge
    IF (TG_TABLE_NAME = 'inferm_planta') THEN
        IF EXISTS (SELECT 1 FROM inferm_metge WHERE id_personal = NEW.id_personal) THEN
            RAISE EXCEPTION 'L infermer amb ID % ja depèn d un metge i no pot ser de planta.', NEW.id_personal;
        END IF;
    END IF;

    -- Si s'insereix a inferm_metge, comprovem que no estigui ja a inferm_planta
    IF (TG_TABLE_NAME = 'inferm_metge') THEN
        IF EXISTS (SELECT 1 FROM inferm_planta WHERE id_personal = NEW.id_personal) THEN
            RAISE EXCEPTION 'L infermer amb ID % ja és de planta i no pot dependre d un metge.', NEW.id_personal;
        END IF;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Definició dels triggers
DROP TRIGGER IF EXISTS tg_check_exclusivitat_planta ON inferm_planta;
CREATE TRIGGER tg_check_exclusivitat_planta
BEFORE INSERT OR UPDATE ON inferm_planta
FOR EACH ROW EXECUTE FUNCTION fn_validar_infermeria();

DROP TRIGGER IF EXISTS tg_check_exclusivitat_metge ON inferm_metge;
CREATE TRIGGER tg_check_exclusivitat_metge
BEFORE INSERT OR UPDATE ON inferm_metge
FOR EACH ROW EXECUTE FUNCTION fn_validar_infermeria();