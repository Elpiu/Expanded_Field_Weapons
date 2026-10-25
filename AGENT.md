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
        special_type_slot_1 = efw_wooden_boost_airframe
    }
}
```

Il modulo è sbloccato dalla tech nascosta `efw_wooden_construction_unlock`, assegnata in `common/on_actions/efw_improvised_air_tank_on_actions.txt`.

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
Attenzione: `light_tank_equipment` in 1.19 **non esiste proprio** (i carri sono chassis), quindi lì nessun ordine di caricamento aiutava. Il Tin Tank che lo usava è stato rimosso.

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

### Bilanciamento (v0.6)
I `country_modifiers` degli edifici si sommano **per ogni edificio** (uno per stato): senza limiti una nazione con 40 stati otteneva +120% PP / produzione.
- Propaganda, Lavoro e Ricerca usano `per_controlled_building_extra_cost` (1500 / 2000 / 1000).
- Ogni edificio con bonus nazionali ha un malus a tema: Propaganda -0.5% ricerca, Lavoro -3% crescita popolazione e -0.4% stabilità, Ricerca +0.5% consumer goods.
- Il Centro Logistico ha solo effetti locali: niente costo crescente né malus.

## Edifici risorse e civili (da "Resource Plants" 3513657215)

File: `common/buildings/zzz_efw_resource_buildings.txt`.

- Ogni coppia piccolo/grande della mod originale è fusa in un solo edificio con valori medi (costo 5500 + 3500/livello, 30 risorse; tungsteno/cromo 18). Il carbone resta com'era.
- Gli edifici risorse **non** usano slot (come l'originale). Compaiono nella riga alta della vista stato: `interface/countrystateview.gui` (copia vanilla 1.19) la porta a 3 righe x 5 e allunga la finestra di 168 px, con sfondo `gfx/interface/stateview/efw_stateview_bg.dds` (sprite `GFX_efw_stateview_bg` in `interface/efw_stateview.gfx`). Edifici senza slot attuali: 4 vanilla + 9 EFW = 13 su 15 posti. Aggiungendone altri senza slot va aggiunta un'altra riga.
- `efw_public_housing` (+10% manpower locale, +10% popolazione reclutabile) e `efw_wheat_fields` (-0.5% consumer goods per stato, stackabile, +3 slot di costruzione) usano uno slot e hanno `state_max = 1`.
- Icone: `gfx/interface/buildings/building_icon_strip.dds` = 31 frame vanilla + 9 EFW (32-40). Il numero frame è in `interface/countrystateview.gfx` (copia vanilla 1.19 con solo `noOfFrames = 40`). **Dopo ogni patch HOI4 che aggiunge edifici vanilla** la strip e quel file vanno rigenerati partendo dai nuovi vanilla.

---

## Define resi attivabili (Invasioni Rapide)

I define (`common/defines/*.lua`) sono statici: valgono per tutti i paesi e non si possono cambiare in partita. Per rendere un define attivabile serve un modificatore nazionale equivalente in un'idea, aggiunta/tolta da due decisioni che si alternano (`has_idea` nel `visible`).

Esempio: `efw_rapid_invasions_idea` (`common/ideas/efw_military_options_ideas.txt`) con le decisioni in `common/decisions/efw_military_options_decisions.txt`, categoria `efw_military_options_category`. Per i limiti si somma la differenza dal valore vanilla (es. piani invasione 1 -> 1000 = `naval_invasion_plan_cap = 999`). Controllare in `documentation/modifiers_documentation.md` del gioco che il modificatore esista: non tutti i define ne hanno uno.

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

Esempi progettati nella prima versione (le decisioni attuali, con costi ed effetti, sono nel README, sezione 8):

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

Sistema volutamente semplice, una sola decisione ripetibile (`efw_issue_national_bonds`):

```text
+120 PP ora
-180 PP dopo 365 giorni (evento efw_national_mobilization.34)
90 giorni di cooldown dopo il rimborso
```

Il vecchio "Grande Prestito Nazionale" (+120 / -200 dopo 730 giorni) non esiste più: le sue chiavi di localisation sono rimaste in `efw_l_*.yml` ma non sono usate.

Usare:
- flag `efw_national_bond_active`;
- evento ritardato;
- flag a tempo `efw_national_bond_cooldown` dopo il rimborso.

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

# Leggi nel pannello politico (idea_categories)

Le sezioni del pannello politico sono `idea_categories` in `common/idea_tags/`. Ogni `slot = X` è un gruppo di leggi `X = { law = yes use_list_view = yes ... }` in `common/ideas/`.

File EFW: `common/idea_tags/efw_policy_categories.txt`, `common/ideas/efw_policy_laws.txt`. **Sono generati** da `utility/efw_laws/gen_laws.py` partendo da `utility/efw_laws/laws_data.py`: modificare la tabella e rilanciare, non i file generati.

Regole verificate in gioco (1.19.3):
- il pannello mostra **al massimo 6 slot per riga**: il 7° esce dal pannello e non si vede;
- l'icona della sezione è il frame N di `GFX_idea_categories`, dove N è la posizione (da 1) della categoria tra tutte quelle definite. Vanilla ne definisce 14, quindi le 4 EFW sono i frame 15-18. EFW sovrascrive lo sprite in `interface/zzz_efw_idea_categories.gfx` (20 frame da 48x33). Se un'altra mod aggiunge categorie, le posizioni si spostano;
- l'icona dello slot vuoto è `GFX_idea_slot_<slot>`, quella della legge `GFX_idea_<picture>`;
- localisation: chiave della categoria e `_desc`, chiave dello slot, chiave della legge e `_desc`;
- ogni slot ha 8 leggi: 5 da 50 PP e 3 da 100 PP (un po' più forti), ognuna con almeno un bonus e un malus. Nessuna legge ha `default = yes`: gli slot partono vuoti e tutte le leggi hanno `ai_will_do = { factor = 0 }`, quindi l'IA non le usa. (Una versione precedente aveva una legge neutra di default per slot: rimossa su richiesta.)
- `cancel_if_invalid = no`, come le leggi economiche vanilla: un requisito (`available`) blocca solo l'adozione.

Le leggi (4 sezioni da 6 slot: Economia e Finanza, Società e Ordine Interno, Esercito e Stato Maggiore, Marina, Aviazione e Servizi) sostituiscono le vecchie categorie di decisioni Tesoro / Fronte Interno / Stato Maggiore: per scelte permanenti e alternative tra loro una legge in uno slot è più chiara di più decisioni a tempo.

---

# Grafica di unità e moduli

## Modello 3D delle unità
- `sprite = X` in un sub_unit sceglie il modello 3D `X_entity` (con varianti di cultura). Un nome custom senza entity fa sparire l'unità sulla mappa e in battaglia: usare sprite vanilla (`infantry`, `artillery`, `anti_tank`, ...).
- Il modello della divisione è quello del battaglione con `priority` più alta. Le compagnie di supporto devono avere `priority = 0` come quelle vanilla.

## Icone delle unità
Le icone si cercano per **nome del sub_unit**, non per `sprite`:
```text
GFX_unit_<sub_unit>_icon_medium   designer divisioni, 152x42, noOfFrames = 2 (76x42: disegno | simbolo NATO)
GFX_unit_<sub_unit>_icon_small    finestra di battaglia e tooltip ("Couldnt find texticon" se manca)
```
Un'immagine unica centrata su tutta la texture viene tagliata a metà dai 2 frame.

## Icone dei moduli del designer
```text
aerei   GFX_EMI_<modulo>
navi    GFX_SMI_<gfx> se il modulo ha gfx = ..., altrimenti GFX_SMI_<modulo>
```
Le icone EFW sono in `interface/efw_module_icons.gfx`, generate da `utility/efw_module_icons/make_module_icons.py`. Icone aerei 56x42, navi 76x42, DDS non compressi A8R8G8B8 come i vanilla.

---

# Define

- I define grafici stanno in `NDefines_Graphics` (`common/defines/00_graphics.lua`), non in `NDefines`. `NDefines.NGraphics.X = ...` è un errore Lua che blocca il resto del file.
- Una chiave nella tabella sbagliata (es. `NDefines.NAir.BOMBERS_DIVISION_FACTOR` invece di `NDefines_Graphics.NAirGfx`) non dà errore e non ha effetto. Verificare sempre la tabella in `00_defines.lua` / `00_graphics.lua`.
- File EFW: `common/defines/zzz_efw_fps_defines.lua` (ottimizzazione FPS). `zzz_` per caricarlo dopo i file vanilla.
- `gfx/posteffect_volumes.txt` vuoto dà errore ("should atleast have one for base values"): non sovrascriverlo con un file vuoto.
- In `common/weather.txt` le soglie `weather_ground_snow_*` sono gameplay (malus a attacco, velocità e rifornimenti): togliere solo le `weather_effect` (particelle).

---

# Errori da NON ripetere

Trigger ed effetti che non esistono (o non più) in 1.19:
```text
num_equipment@train_equipment > 4     ->  has_equipment = { train_equipment > 4 }
enable_equipments in un effetto        ->  solo dentro una tecnologia (vedi efw_pipe_gun_unlock + set_technology)
allow_mission_type = { naval_strike }  ->  naval_bomber
archetype = light_tank_equipment       ->  i carri sono chassis (light_tank_chassis): usare create_equipment_variant
equipment_bonus = { fighter_equipment } ->  airframe 1.19: small_plane_airframe, cv_small_plane_airframe,
                                            small_plane_cas_airframe, medium_plane_airframe,
                                            medium_plane_fighter_airframe, large_plane_airframe, ...
```

Nei tratti dei designer (`common/country_leader/`) una statistica ripetuta nello stesso blocco viene sommata ("Duplicated equipment stat type ... combining values" nel game.log): scriverla una volta sola. I designer generici EFW sono in `common/ideas/efw_generic_designers.txt` e `common/country_leader/efw_designer_traits.txt`.

Designer di materiale e concessioni industriali: i `materiel_manufacturer` hanno `designer = yes` e i tratti usano `equipment_bonus` (tipi validi: `infantry_equipment`, `support_equipment`, `artillery_equipment`, `anti_tank_equipment`, `anti_air_equipment`, `motorized_equipment`, `armored_car_equipment`, `rocket_artillery_equipment`). Gli `industrial_concern` non hanno `designer = yes` e i loro tratti contengono direttamente modificatori nazionali (`country_resource_steel`, `factory_energy_consumption`, ...). Non usare le armi EFW dentro `equipment_bonus`: non sono nell'enum `script_enum_equipment_bonus_type`.

Consiglieri politici generici: dalla 1.11 i consiglieri sono personaggi, non idee. Per darli a tutti i paesi si usa `every_possible_country` + `generate_character` in `history/general/` (come `generic_advisors.txt` vanilla): una copia per paese, a inizio partita. EFW: `history/general/efw_generic_advisors.txt`, tratti in `common/country_leader/efw_advisor_traits.txt`; i 4 consiglieri di governo hanno `available = { has_government = <ideologia> }` (`democratic`, `communism`, `fascism`, `neutrality`). Ritratti: `GFX_idea_generic_political_advisor_*` vanilla.

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
