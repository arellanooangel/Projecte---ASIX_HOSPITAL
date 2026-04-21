# Resum de Permisos

| Taula / Vista     | rol_admin | rol_metge | rol_infermer | rol_vari | rol_consulta |
| ----------------- | --------- | --------- | ------------ | -------- | ------------ |
| especialitat      | ALL       | S         | S            | -        | S            |
| medicament        | ALL       | S         | S            | -        | S            |
| aparell           | ALL       | S         | S            | S        | S            |
| planta            | ALL       | S         | S            | S        | S            |
| pacient           | ALL       | SIUD      | S            | -        | S            |
| personal          | ALL       | S         | S            | -        | S            |
| usuaris           | ALL       | -         | -            | -        | -            |
| vari              | ALL       | -         | -            | S        | S            |
| metge             | ALL       | S         | S            | -        | S            |
| infermer          | ALL       | S         | S            | -        | S            |
| habitacio         | ALL       | S         | S            | S        | S            |
| quirofan          | ALL       | S         | S            | S        | S            |
| quirofan_aparell  | ALL       | S         | S            | S        | S            |
| inferm_planta     | ALL       | S         | S            | -        | S            |
| inferm_metge      | ALL       | S         | S            | -        | S            |
| visita            | ALL       | SIUD      | S            | -        | S            |
| ingres            | ALL       | SIUD      | SIU          | -        | S            |
| operacio          | ALL       | SIUD      | S            | -        | S            |
| visita_medicament | ALL       | SIUD      | S            | -        | S            |
| operacio_infermer | ALL       | SIUD      | S            | -        | S            |
| v_personal_masked | ALL       | -         | -            | S        | -            |
| v_ingres_masked   | ALL       | -         | -            | S        | -            |
## Llegenda

| Abreviació | Significat        |
| ---------- | ----------------- |
| ALL        | Tots els permisos |
| S          | SELECT            |
| I          | INSERT            |
| U          | UPDATE            |
| D          | DELETE            |
| -          | Sense accés       |

## Consideracions
Hem creat el rol de consulta per poder recollir dades en un futur com estadístiques. El metge ha de ser el rol amb més pes després de l'administrador, ja que serà qui insereixi més informació que la resta. Considerem que un infermer pot modificar i inserir ingresos, pero no borrar-los.
El datamasking està implementat a la creació de taules mitjançant les vistes, i els permisos otorgats a l'SQL que es troba en aquesta mateixa carpeta.
Les dades emmascarades han siguit: DNI, nom, cognom1, cognom2 i targeta_sanitaria. Aquestes dades es troven a les vistes v_personal_masked i v_ingres_masked.

