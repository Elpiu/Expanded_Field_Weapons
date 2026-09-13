# AGENT.md — Expanded Field Weapons / HOI4 Modding Handoff

## Scopo

Questo file serve come passaggio di consegne per continuare a sviluppare **Expanded Field Weapons (EFW)** per Hearts of Iron IV, mantenendo lo stesso approccio usato finora: modifiche semplici, testabili, facili da mergiare e compatibili con una build moderna di HOI4 1.19.x.

L'obiettivo principale non è costruire sistemi troppo eleganti o astratti, ma ottenere contenuti che **funzionano davvero in gioco**, siano facili da diagnosticare tramite `error.log` e possano essere iterati rapidamente.

---

## Principi di lavoro

1. **Preferire sempre la soluzione più semplice che funziona.**  
   Se una feature richiede troppi scope, hidden tech, on_action, scripted effect e flag, provare prima una versione più diretta.

2. **Il test in gioco vale più della teoria.**  
   La documentazione è utile, ma per HOI4 molte sintassi cambiano tra versioni o hanno scope poco intuitivi.  
   Se `error.log` contraddice una supposizione, fidarsi di `error.log`.

3. **Fare modifiche isolate.**  
   Una nuova feature dovrebbe toccare pochi file e possibilmente un solo sottosistema alla volta.

4. **Preparare sempre pacchetti `MERGE`.**  
   Struttura desiderata:
   ```text
   common/
   events/
   localisation/
   gfx/              # solo se necessario
   README_MERGE_IT.txt
   ```
   Il contenuto deve poter essere copiato direttamente nella root della mod.

5. **Non distruggere contenuti vanilla se non necessario.**  
   Quando possibile, usare archetipi, hull, airframe e componenti vanilla e creare varianti custom sopra di essi.

6. **Ridurre al minimo i sistemi nascosti.**  
   Il giocatore deve capire da UI e tooltip cosa serve per sbloccare una decisione o ottenere un bonus.

---

## Workflow consigliato

### 1. Progettazione
Prima di scrivere codice:
- definire effetto;
- costo;
- durata;
- requisiti;
- se è player-only;
- file coinvolti;
- come testarlo in meno di 5 minuti.

### 2. Implementazione
Creare pochi file, nomi univoci con prefisso `efw_`.

Esempi:
```text
efw_propaganda_center
efw_national_investments_idea
efw_issue_national_bonds
efw_national_mobilization.1
```

### 3. Sanity check
Prima di testare:
- parentesi `{}` bilanciate;
- nessun ID duplicato;
- localisation presente;
- namespace eventi corretto;
- file vecchi neutralizzati o rimossi se incompatibili.

### 4. Test minimo
Usare **nuova partita** quando si modificano:
- tecnologie;
- archetipi;
- edifici;
- decisioni con flag;
- equipment variants;
- on_actions.

Poi testare una cosa per volta.

### 5. Debug
Cercare in `error.log`:
```text
efw_
Unexpected token
Malformed token
Unknown modifier
Invalid scope
Invalid effect
```

Non correggere dieci problemi insieme: isolare il primo errore EFW e risolverlo.

---

# Best practices apprese durante EFW

## Equipment e varianti navali

La soluzione più affidabile per navi improvvisate è stata:

- usare **hull vanilla**;
- usare moduli custom solo dove serve;
- creare il design tramite `create_equipment_variant`.

Esempio validato:
```txt
create_equipment_variant = {
    name = "EFW TEST BOAT"
    type = ship_hull_light_1
    allow_without_tech = yes

    modules = {
        fixed_ship_battery_slot = ship_light_battery_1
        fixed_ship_engine_slot = light_ship_engine_1
        fixed_ship_anti_air_slot = empty
        fixed_ship_fire_control_system_slot = empty
        fixed_ship_radar_slot = empty
        fixed_ship_torpedo_slot = empty
        mid_1_custom_slot = empty
        rear_1_custom_slot = empty
    }
}
```

### Lezione
Un custom hull può fallire per archetype/load order/UI integration anche se apparentemente corretto.  
Quando non è necessario, evitare un nuovo hull e riusare quello vanilla.

---

## Aircraft Designer

Per aerei custom:
- usare airframe vanilla, ad esempio `small_plane_airframe_0`;
- creare la variante con `create_equipment_variant`;
- se si aggiunge un modulo custom, quel modulo deve essere correttamente definito e, se richiesto, abilitato.

Esempio:
```txt
create_equipment_variant = {
    name = "EFW Wooden Fighter"
    type = small_plane_airframe_0
    parent_version = 0
    obsolete = no
    allow_without_tech = yes

    modules = {
        fixed_main_weapon_slot = light_mg_2x
        engine_type_slot = engine_1_1x
        special_type_slot_1 = efw_wooden_construction
    }
}
```

### Lezione
Se una variante smette di apparire dopo aver aggiunto un modulo:
1. controllare che il modulo esista;
2. controllare categoria/slot;
3. controllare se necessita di unlock;
4. cambiare eventuali vecchi flag di creazione quando si testa su save già usati.

---

## Load order

Problema già incontrato:
```text
Malformed token: fighter_equipment
Malformed token: light_tank_equipment
```

Può succedere se un file custom viene caricato prima che l'archetipo vanilla sia disponibile.

### Best practice
Quando serve caricare un file dopo vanilla:
```text
zzz_efw_...
```

Non è una soluzione universale, ma è utile per problemi di ordine di caricamento.

---

## Moduli equipment

Non mettere modifier fuori scope nei moduli equipment.

Errore già visto:
```text
manpower = ...
```

dentro un equipment module.

### Best practice
Le statistiche di equipment devono essere statistiche supportate dal relativo scope.  
Costi politici, manpower, stabilità ecc. vanno gestiti tramite:
- decisioni;
- idee;
- eventi;
- scripted effects;
non dentro i moduli di equipaggiamento.

---

# Strategic Buildings — architettura finale consigliata

Dopo vari tentativi, la versione più robusta è:

- **tutti gli edifici costruibili normalmente**;
- tutte le decisioni visibili fin dall'inizio;
- requisiti nelle decisioni;
- niente hidden tech per gli edifici;
- niente decisioni mirate agli stati;
- niente `add_building_construction` se non strettamente necessario.

Edifici principali:
```text
efw_propaganda_center
efw_labor_directorate
efw_research_center
efw_logistics_center
```

### Perché
Le decisioni state-targeted e gli unlock nascosti hanno introdotto troppi punti di rottura:
- category mancante;
- scope `FROM`;
- hidden tech;
- decisioni che non apparivano;
- edifici bloccati.

La soluzione semplice è molto più robusta e facile da bilanciare.

---

## Conteggio edifici nelle decisioni

Per custom buildings, usare direttamente il trigger quantitativo quando funziona nella build:

```txt
available = {
    efw_propaganda_center > 0
}
```

oppure:
```txt
efw_propaganda_center > 2
efw_labor_directorate > 0
```

Questo approccio è preferibile a `has_built` quando si vuole verificare **quanti edifici il paese possiede attualmente**.

---

# Early game economy

La filosofia migliore emersa è:

> non chiedere al giocatore di investire per due anni prima di ricevere qualcosa.

Le decisioni early-game devono dare un beneficio subito, ma avere un costo reale.

Esempi progettati:

### Campagna Nazionale di Industrializzazione
- 25 PP;
- -200k manpower;
- -10 treni;
- +20% construction per 180 giorni;
- treni restituiti dopo 180 giorni;
- manpower restituito dopo 2 anni.

### Esercito nei Lavori Pubblici
- 40 PP;
- -100k manpower per 1 anno;
- +4 civili permanenti;
- manpower restituito dopo 365 giorni.

Per dare fabbriche civili senza scegliere uno stato:
```txt
add_offsite_building = {
    type = industrial_complex
    level = 4
}
```

### Sovvenzioni Statali
Idea temporanea:
- +10% Consumer Goods Factor;
- +6% research;
- +3% factory output;
- +3% dockyard output;
- +10% Political Power Gain;
- durata 2 anni.

### Infrastrutture
- 25 PP;
- usa 5 treni;
- +20% infrastructure construction;
- +20% railway construction;
- +5% construction;
- durata 1 anno.

---

# Bond / debito politico

Sistema volutamente semplice:

### Bond breve
```text
+100 PP ora
-150 PP dopo 365 giorni
```

### Prestito lungo
```text
+120 PP ora
-200 PP dopo 730 giorni
```

Usare:
- flag `efw_national_bond_active`;
- evento ritardato;
- breve cooldown dopo il rimborso.

Evita un sistema di debito con troppe variabili finché non serve davvero.

---

# Timed effects

Per bonus temporanei:
```txt
add_timed_idea = {
    idea = efw_example_idea
    days = 180
}
```

Per restituire risorse in futuro:
```txt
country_event = {
    id = efw_national_mobilization.10
    days = 180
}
```

Gli eventi nascosti sono ottimi per:
- restituire manpower;
- restituire treni;
- applicare scadenze;
- chiudere programmi temporanei.

---

# Player-only

Quando il contenuto deve essere solo per il giocatore:
```txt
visible = {
    is_ai = no
}
```

e:
```txt
ai_will_do = {
    factor = 0
}
```

Per sistemi semplici, è preferibile questo rispetto a complessi unlock via `on_daily`.

---

# Localisation

Usare sempre file dedicati:

```text
localisation/italian/
    efw_..._l_italian.yml
```

Header:
```yml
l_italian:
```

Preferire UTF-8 BOM per evitare problemi con caratteri italiani.

I tooltip devono spiegare:
- costo PP;
- durata;
- manpower;
- equipment consumato;
- cosa viene restituito;
- requisiti.

---

# Naming convention

Usare sempre prefisso:
```text
efw_
```

Per versioni sperimentali di flag:
```text
efw_wooden_plane_v03_created
```

Quando un vecchio save contiene un flag che impedisce la rigenerazione, cambiare il nome del flag per il nuovo test.

---

# Riferimenti utili / skill usate

## HOI4 modding skill / reference
Repository pubblico:
```text
https://github.com/kkkunny/hoi4-mod-skills
```

Percorsi particolarmente utili:
```text
skills/hoi4-mod/references/Building modding.md
skills/hoi4-mod/references/Effect.md
```

## HOI4 documentation
```text
https://hoi4doc.dev/
```

Utile per verificare:
- effects;
- triggers;
- modifiers;
- scope;
- `add_building_construction`;
- `add_manpower`;
- `add_offsite_building`.

## CWTools HOI4 config
```text
https://github.com/cwtools/cwtools-hoi4-config
```

Molto utile per controllare:
- nomi dei modifier;
- scope validi;
- token supportati.

---

# Errori da NON ripetere

Non usare alla cieca modifier come:
```text
war_support
armor_value_factor
hard_attack_factor
air_equipment_production_cost_factor
naval_equipment_production_cost_factor
tank_equipment_production_cost_factor
```

senza verificare scope e validità nella versione attuale.

Per esempio, nei modifier country:
```text
war_support_factor
```
è preferibile al token non valido:
```text
war_support
```

Non dare per scontato che un vecchio mod del 2020-2023 sia compatibile con HOI4 1.19.

---

# Regola finale

Quando esistono due soluzioni:

```text
A) elegante ma complessa
B) semplice, leggibile e testabile
```

per EFW scegliere quasi sempre **B**.

Prima far funzionare il contenuto.  
Poi, se serve, renderlo più sofisticato.
