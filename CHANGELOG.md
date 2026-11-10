# Changelog

Tutte le modifiche rilevanti di Expanded Field Weapons. Le versioni seguono `MAGGIORE.MINORE.CORREZIONE`.

> Dopo un aggiornamento con contenuti nuovi è consigliata una **partita nuova**.

---

## v1.3.0 — "Si arrangia chi può" (2026-11-10)

### 🎯 Novità
- **Vocazioni Nazionali**: nuova categoria di decisioni con 5 percorsi a 3 livelli (Repubblica degli Scienziati, Officina della Nazione, Nazione in Armi, Signori del Mare, L'Arte dell'Arrangiarsi). Se ne sceglie una sola; ogni livello richiede edifici EFW e leggi a tema. Al terzo livello i bonus sono enormi (fino a +40% ricerca, +28% produzione, −60% penalità per risorse mancanti), con malus negli altri campi. Si può rinnegare la vocazione, a costo di una *Crisi d'Identità Nazionale* di 180 giorni.
- **Evento di benvenuto**: al primo giorno un ispettore con un tubo idraulico presenta la mod e offre un regalo a scelta (ricerca, costruzione, esercito, 2.000 Pipe-Gun Rifle oppure 25 PP).
- **Mezzi leggeri improvvisati**, disponibili dal primo giorno per tutte le nazioni e non usati dall'IA:
  - **Carro Veloce EFW** e Battaglione Carri Veloci: mini carro economico, corazza 12, buono contro la fanteria senza anticarro.
  - **Moto Mitragliera EFW** e Compagnia Motociclisti Mitraglieri: ricognizione economica che dà +5% attacco a tutta la fanteria della divisione.
  - **Autocannone Improvvisato EFW** e Batteria Autocannoni: artiglieria e anticarro su camion, veloce e senza corazza.
- **Mitra STEN**: arma di fanteria economica (0,25 IC, 1 acciaio) tra il Pipe-Gun e il fucile base, con più attacco e sfondamento e meno difesa. Disponibile dal primo giorno.
- **Aviotrasporto improvvisato** (l'IA non lo usa):
  - **Trasporto in Legno EFW**: versione rudimentale del trasporto vanilla, dal primo giorno per tutti. 16 IC invece di 38, niente alluminio, affidabilità 55%. Lancio di paracadutisti e rifornimento aereo.
  - **Trasporto vanilla** disponibile dal primo giorno per il giocatore, anche con le nazioni minori.
  - **Paracadutisti di Milizia**: battaglione paracadutabile non d'élite, fuori dal limite delle forze speciali.
  - La compagnia MG EFW ora è paracadutabile.
  - Minimo di trasporti per un lancio abbassato da 50 a **25** (`common/defines/zzz_efw_gameplay_defines.lua`, vale per tutti i paesi).
- **Traduzioni**: russo, tedesco, polacco e cinese semplificato (902 testi per lingua, tutta la mod).
- **Nuove icone** per i 4 edifici strategici: megafono, ingranaggio con martello, scudo con cassa, beuta.

### ⚖️ Bilanciamento
- **Campi di Grano**: per ogni stato −1% beni di consumo (prima −0,5%), +0,2% stabilità, +2% crescita della popolazione; nello stato +0,25 rifornimenti (prima +0,10) e +5% manpower.
- **Centro di Propaganda**: +0,5% stabilità e supporto alla guerra (prima +0,36% ciascuno).
- **Centro Logistico**: +0,40 rifornimenti locali (prima +0,30).

### ⚡ Prestazioni
- Rimossi tutti i controlli giornalieri (`on_daily`): prima circa 10 controlli al giorno per ogni paese, per tutta la partita.
- La sincronizzazione delle tecnologie gira **una volta a settimana** e si spegne da sola quando un paese ha sbloccato tutto (`efw_sync_complete_v2`).
- L'inizializzazione del giocatore (caccia in legno, navi improvvisate) è una catena di eventi nascosti eseguita una volta sola. Funziona anche per chi cambia nazione a partita in corso.

### 🐞 Correzioni
- Centro di Propaganda: la "difesa dalla deriva ideologica" non aveva effetto (modificatore non valido negli edifici). Sostituita.
- Centro Logistico: il "−12% attrito" non aveva effetto (modificatore non valido negli edifici). Sostituito.
- Le icone dei 4 edifici strategici erano scambiate (la Propaganda mostrava le rotaie).
- Lettore DDS degli script di sviluppo: corretta l'interpolazione dell'alpha DXT5.
- Rastrelliera Polivalente da Campo: tolto il tipo "bombardiere strategico", che l'airframe piccolo non accetta e quindi non aveva effetto.

### 🧹 Pulizia
- Aggiunto `.gitignore`. Rimossi `__pycache__`, `OLD_thumbnail.png`, le icone `OLD_divisions_large`, l'evento di test e un file segnaposto.
- Il README è stato riscritto con immagini, indice e tabelle.
- Nuova copertina in inglese con versione, funzionalità principali e lingue supportate.

### 🧩 Compatibilità
- La strip delle icone degli edifici passa da 40 a **44 frame** (`interface/countrystateview.gfx`). Le mod che modificano la stessa strip restano incompatibili.
- Nuovi file: `common/scripted_effects/efw_scripted_effects.txt`, `common/units/efw_light_vehicle_units.txt`, `common/units/equipment/efw_light_vehicles.txt`, `common/technologies/efw_hidden_vehicle_unlocks.txt`, `common/units/equipment/efw_air_transport.txt`, `common/units/efw_airborne_units.txt`, `common/defines/zzz_efw_gameplay_defines.lua`, le Vocazioni (`common/ideas`, `common/decisions`) e le cartelle di localizzazione `russian`, `german`, `polish`, `simp_chinese`.
- `common/defines/zzz_efw_gameplay_defines.lua` cambia un define globale (`MIN_PLANE_COUNT_PARADROP`): le mod che modificano lo stesso valore possono sovrascriverlo, o essere sovrascritte, a seconda dell'ordine di caricamento.
- Rimossi: `common/on_actions/efw_improvised_air_tank_on_actions.txt`, `common/on_actions/efw_improvised_naval_on_actions.txt`, `events/efw_test_events.txt`.

### 🛠️ Strumenti di sviluppo
- `utility/efw_translations/build_translations.py`: costruisce le traduzioni dai file TSV e controlla che codici colore, variabili e a capo siano intatti.
- `utility/efw_building_icons/make_building_icons.py`: disegna le icone degli edifici strategici.
- `utility/efw_vehicle_icons/make_gun_truck_icon.py`: genera l'icona dell'Autocannone.
- `utility/efw_vehicle_icons/make_transport_icons.py`: genera l'icona del Trasporto in Legno.
- `utility/make_readme_images.py`: converte le icone DDS nelle immagini del README.
- `utility/efw_thumbnail/make_thumbnail.py`: compone la copertina (titolo, versione, funzionalità, lingue) sopra l'illustrazione `thumbnail_new.jpg`.
- `pyproject.toml` e `uv.lock`: dipendenze degli script di sviluppo, si installano con `uv sync`.
- `utility/build_release.py`: crea una copia pulita della mod (solo file del gioco, circa 7 MB) da caricare sul Workshop.

---

## v1.2.0 (2026-10-25)

- Leggi nel pannello politico: 4 sezioni, 24 slot, 192 leggi.
- 21 designer generici e 8 consiglieri politici generici.
- Edifici delle risorse, Case Popolari, Campi di Grano e vista stato ingrandita.
- Opzione Invasioni Rapide.
- Ottimizzazione FPS integrata.
- Pipe-Gun Rifle, caccia in legno e moduli aerei e navali improvvisati.

---

## English summary — v1.3.0

- **New:** National Vocations (5 paths × 3 tiers, huge bonuses with drawbacks), welcome event with a starting gift, three improvised light vehicles available from day one (Tankette, MG Motorcycle, Gun Truck), the cheap STEN submachine gun, early airborne warfare (16 IC Wooden Transport, vanilla transport for the player from day one, non-elite Militia Paratroopers), translations into Russian, German, Polish and Simplified Chinese, new icons for the four strategic buildings.
- **Balance:** stronger Wheat Fields (−1% consumer goods per state, plus stability, population growth, supply and manpower); Propaganda Center and Logistics Center reworked.
- **Performance:** no more daily scripts; weekly technology sync that switches itself off; one-time hidden initialization events.
- **Fixes:** two building modifiers that had no effect, swapped strategic building icons, DDS alpha decoding in the dev tools.
- **Compatibility:** the building icon strip now has 44 frames. A new game is recommended.
