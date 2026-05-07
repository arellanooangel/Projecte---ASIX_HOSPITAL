# 4.1. Especificació de la Infraestructura de Maquinari i Justificació

Per complir amb el requisit de l'alta disponibilitat de l'Hospital i assegurar el rendiment, s'ha dissenyat una arquitectura redundant basada en dos nodes (Actiu-Passiu) amb una segmentació avançada de l'emmagatzematge mitjançant LVM2.

## 1. Servidors de Base de Dades (Nodes Redundants)

S'han desplegat dues màquines virtuals amb especificacions idèntiques. El Node 1 actua com a servidor principal al Datacenter local, mentre que el Node 2 es troba en un entorn que mimetitza una infraestructura Cloud.

* **Sistema Operatiu:** Ubuntu Server 24.04.2 LTS (Noble Numbat).
* **Processador (CPU):** 4 nuclis (vCPUs) amb acceleració per paravirtualització KVM.
* **Memòria RAM:** 8.192 MB (8 GB), dimensionada per suportar el *buffer cache* necessari per a consultes massives.
* **Xarxa:** Adaptador Intel PRO/1000 MT en mode "Xarxa NAT" (vLAN «HOSPITAL»), configurat per a connexions segures via SSL.

## 2. Arquitectura d'Emmagatzematge Multi-Disc (LVM2)

La solució utilitza una arquitectura de*6 discos independents gestionats per LVM2. Aquesta segmentació és una pràctica de producció crítica per evitar colls d'ampolla d'I/O (Entrada/Sortida).

| Unitat | Volume Group (VG) | Logical Volume (LV) i Punt de muntatge | Mida | Finalitat Tècnica |
| :--- | :--- | :--- | :--- | :--- |
| **sda** | `vg_sistema` | `/`, `/var`, `/tmp`, `/home`, `swap` | 30 GB | OS i aïllament de directoris crítics del sistema. |
| **sdb** | `vg_pgbinaris` | `/opt/postgresql` | 10 GB | Binaris i llibreries de PostgreSQL 18.3. |
| **sdc** | `vg_pgdata` | `/var/lib/postgresql/data` | 40 GB | Directori principal de dades (PGDATA). |
| **sdd** | `vg_pgfast` | `/var/lib/postgresql/fastdata` | 40 GB | Tablespaces d'alt rendiment per a taules crítiques. |
| **sde** | `vg_pglogs` | `/var/log/postgresql` | 15 GB | Logs de sistema i Write-Ahead Logs (WAL). |
| **sdf** | `vg_pgbackup` | `/var/backups/postgresql` | 50 GB | Magatzem per a les 5 còpies de seguretat diàries. |

## 3. Justificació Professional de la Solució

L'elecció d'aquesta infraestructura es fonamenta en els següents pilars de l'administració de sistemes:

1.  **Optimització del Throughput d'E/S:** En separar físicament els WAL (`sde`) de les dades (`sdc`), les escriptures seqüencials de transaccions no competeixen amb les lectures aleatòries del personal mèdic, garantint el rendiment exigit.
2.  **Alta Disponibilitat i Disaster Recovery:** La configuració actiu-passiu garanteix que el Node 2 pugui assumir el servei 24x7 si el Datacenter local pateix un desastre físic.
3.  **Fiabilitat amb LVM2:** L'ús de volums lògics permet la creació de snapshots consistents per a backups i la capacitat d'ampliar qualsevol disc "en calent" (sense aturar el servei) si l'hospital creix.
4.  **Aïllament de Fallades:** Si el disc de backups o de logs s'omple, el volum arrel (`/`) romandrà operatiu, evitant que el sistema operatiu col·lapsi i permetent la intervenció de l'administrador.
