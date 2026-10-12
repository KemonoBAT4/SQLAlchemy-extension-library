# SQLAlchemy-extension-library
A library for SQLAlchemy that extends some of the functionality already implemented in SQLAlchemy, improving its behavior and making it easier to use. (Not related to the SQLAlchemy library)



Ecco una lista di costrutti utili per una libreria SQLAlchemy customizzata orientata a MariaDB/MySQL, senza implementazione. Tutti si prestano al pattern `FunctionElement` + `@compiles`.

## Aggregazioni

- **`group_concat`**: `GROUP_CONCAT` con opzioni `distinct`, `order_by` e `separator`. È la versione generalizzata di quello che abbiamo fatto.
- **`json_arrayagg`**: aggrega valori in un array JSON (`JSON_ARRAYAGG`), più robusto di `GROUP_CONCAT` se i valori contengono separatori.
- **`json_objectagg`**: aggrega coppie chiave/valore in un oggetto JSON.
- **`any_value`**: `ANY_VALUE(col)`, utile con `ONLY_FULL_GROUP_BY`.
- **`bit_and` / `bit_or` / `bit_xor`**: aggregati bitwise, utili per flag e permessi.

## JSON

- **`json_extract`** e **`json_unquote`**: con operatore `->` / `->>` come helper.
- **`json_contains`**: verifica se un documento JSON ne contiene un altro.
- **`json_table`**: espande un array JSON in righe (richiede un costrutto `FromClause`, più complesso).
- **`json_set` / `json_insert` / `json_remove`**: modifica parziale di colonne JSON negli `UPDATE`.

## Stringhe e testo

- **`concat_ws`**: concatenazione con separatore che ignora i `NULL`.
- **`find_in_set`**: ricerca in liste separate da virgole.
- **`regexp_replace` / `regexp_substr` / `regexp_instr`**: regex native in MariaDB 10.0.5+.
- **`match_against`**: full-text search (`MATCH(...) AGAINST(... IN BOOLEAN MODE)`) con modalità selezionabile.

## Window function

- **`row_number`, `rank`, `dense_rank`**: wrapper con `partition_by` e `order_by` semplificati.
- **`lag` / `lead`**: valori della riga precedente o successiva.
- **`first_value` / `last_value` / `nth_value`**
- **`ntile`, `percent_rank`, `cume_dist`**

## Data e ora

- **`date_format`** e **`str_to_date`**: formattazione e parsing.
- **`timestampdiff`** e **`timestampadd`**: differenze e somme con unità esplicita.
- **`date_add` / `date_sub`** con `INTERVAL`: richiede un costrutto per l'intervallo.
- **`from_unixtime`** e **`unix_timestamp`**
- **`last_day`**, **`week`**, **`yearweek`**

## Clausole e istruzioni speciali

- **`insert_on_duplicate_key_update`**: SQLAlchemy lo ha già per MySQL (`mysql.insert().on_duplicate_key_update()`), ma si può avvolgere con una API più comoda.
- **`insert_ignore`** e **`replace_into`**
- **`for_update_skip_locked`** / **`nowait`**: per code di lavoro (MariaDB 10.6+).
- **`straight_join`**, **`use_index`** / **`force_index`** / **`ignore_index`**: index hints.
- **`sql_calc_found_rows`** con `FOUND_ROWS()`: paginazione con totale (deprecato in MySQL 8, ma esiste in MariaDB).
- **`returning`** su `INSERT`/`DELETE` (MariaDB 10.5+): supportato da SQLAlchemy 2.0, ma va verificato per dialect.

## Utility e comparatori

- **`collate`**: forzare una collation in un confronto.
- **`binary`**: confronto case-sensitive (`BINARY col`).
- **`null_safe_equal`**: operatore `<=>`, comodo per confrontare con `NULL`.
- **`rlike`** / **`regexp`**: come operatori di colonna.
- **`greatest` / `least`**, **`if_`** (`IF(cond, a, b)`), **`ifnull`**
- **`uuid`**, **`uuid_short`**, **`sys_guid`** (MariaDB 10.7 ha anche il tipo `UUID`)
- **`last_insert_id`**

## Tipi custom

- **`UUID`** nativo MariaDB 10.7+ (con fallback a `CHAR(36)` / `BINARY(16)`).
- **`INET4` / `INET6`** (MariaDB 10.10+).
- **`Enum`** con migrazione sicura dei valori.
- **`TypeDecorator` per `JSON`** con serializzazione Pydantic automatica.
- **`Set`** (`SET('a','b')`) mappato su `set[str]`.

## Per SQLModel e hybrid property

- **Mixin per `label` aggregata**: pattern riutilizzabile come quello di `CustomOrderLine.label`.
- **Helper `correlated_subquery_property`**: factory che genera hybrid + expression da una descrizione dichiarativa.
- **`soft_delete` mixin** con filtro automatico a livello di query.
- **`timestamp` mixin** (`created_at` / `updated_at` con `ON UPDATE CURRENT_TIMESTAMP`).

Se vuoi, posso implementarne un sottoinsieme: partirei da `group_concat`, `concat_ws`, `json_arrayagg` e `if_`, che sono quelli con il miglior rapporto utilità/complessità.