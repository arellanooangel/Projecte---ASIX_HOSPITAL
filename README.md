# Projecte---ASIX_HOSPITAL
Aquest es el projecte intermodular dels autors Angel Arellano i Unai Llamas, alumnes de 1r ASIX.
## MODEL RELACIONAL
**ESPECIALITAT** (<u>id_especialitat</u>, descripcio)

**MEDICAMENT** (<u>id_medicament</u>, nom)

**APARELL** (<u>id_aparell</u>, descripcio)

**PLANTA** (<u>id_planta</u>, descripcio)

**PACIENT** (<u>targeta_sanitaria</u>, nom, cognom1, cognom2, data_naixement)

**PERSONAL** (<u>id_personal</u>, dni, nom, cognom1, cognom2, email, user, password)

**VARI** (<u>id_personal</u>, feina)

ON (id_personal) REFERENCIA PERSONAL (id_personal)

**METGE** (<u>id_personal</u>, estudis, experiencia, id_especialitat)

ON (id_personal) REFERENCIA PERSONAL (id_personal)

ON (id_especialitat) REFERENCIA ESPECIALITAT (id_especialitat)

**INFERMER** (<u>id_personal</u>, curs, experiencia)

ON (id_personal) REFERENCIA PERSONAL (id_personal)

**INFERM_PLANTA** (<u>id_personal</u>, id_planta)

ON (id_personal) REFERENCIA PERSONAL (id_personal)

ON (id_planta) REFERENCIA PLANTA (id_planta)

**INFERM_METGE** (<u>id_personal</u>, id_metge)

ON (id_personal) REFERENCIA PERSONAL (id_personal)

ON (id_metge) REFERENCIA METGE (id_personal)

**HABITACIO** (<u>id_habitacio</u>, descripcio, id_planta)

ON (id_planta) REFERENCIA PLANTA (id_planta)

**VISITA** (<u>id_visita</u>, data_hora, diagnostic, id_metge, targeta_sanitaria)

ON (id_metge) REFERENCIA METGE (id_metge)

ON (tarjeta_sanitaria) REFERENCIA PACIENT (tarjeta_sanitaria)

**INGRES** (<u>id_ingres</u>, data_ingres, data_alta, targeta_sanitaria, id_habitacio)

ON (tarjeta_sanitaria) REFERENCIA PACIENT (tarjeta_sanitaria)

ON (id_habitacio) REFERENCIA HABITACIO (id_habitacio)

**OPERACIO** (<u>id_operacio</u>, descripcio, data_hora, targeta_sanitaria, id_metge, id_infermer, id_planta, id_quirofan)

ON (tarjeta_sanitaria) REFERENCIA PACIENT (tarjeta_sanitaria)

ON (id_metge) REFERENCIA METGE (id_personal)

ON (id_infermer) REFERENCIA INFERMER (id_personal)

ON (id_planta) REFERENCIA PLANTA (id_planta)

ON (id_quirofan) REFERENCIA QUIROFAN (id_quirofan)


**QUIROFAN_APARELL** (<u>id_planta, id_quirofan, id_aparell</u>, quantitat)

ON (id_planta) REFERENCIA PLANTA (id_planta)

ON (id_quirofan) REFERENCIA QUIROFAN (id_quirofan)

ON (id_aparell) REFERENCIA APARELL (id_aparell)

**VISITA_MEDICAMENT** (<u>id_visita, id_medicament</u>)

ON (id_visita) REFERENCIA VISITA (id_visita)

ON (id_medicament) REFERENCIA MEDICAMENT (id_medicament)

**OPERACIO_INFERMER** (<u>id_operacio, id_infermer</u>)

ON (id_operacio) REFERENCIA OPERACIO (id_operacio)

ON (id_infermer) REFERENCIA INFERMER (id_personal)
