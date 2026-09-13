# EXPANDED FIELD WEAPONS (EFW) v1.2.0

**Compatibilità obiettivo:** Hearts of Iron IV `1.19.*`

---

## 🏗️ NUOVA ARCHITETTURA

La mod **NON** crea più modelli I/II/III delle armi pesanti. 

Esistono soltanto **tre linee produttive permanenti**:
1. **Mitragliatrici**
2. **Mortai**
3. **Armi anticarro**

La tecnologia **Support Weapons I** (`support_weapons`) sblocca contemporaneamente tutte e tre le linee produttive e quattro formazioni nel Division Designer:

* 🛡️ **Compagnia mitragliatrici** *(Supporto)*
* 🛡️ **Compagnia mortai** *(Supporto)*
* 🛡️ **Compagnia anticarro** *(Supporto)*
* 🎖️ **Battaglione d'élite armi pesanti** *(LINEA, non supporto)*

> **Nota sul Battaglione d'Élite:** Questa unità di linea impiega contemporaneamente Mitragliatrici, Mortai e Armi AT, oltre a una normale quota di `infantry_equipment`.

---

## 🧪 PROGRESSIONE TECNOLOGICA

**Support Weapons II, III e IV** **NON** sbloccano nuovi equipaggiamenti da produrre.
Migliorano direttamente le statistiche delle quattro formazioni EFW tramite tecnologie interne nascoste. I bonus applicati sono **cumulativi e moderati**.

* **Infantry Anti-Tank I/II:** Forniscono bonus extra mirati espressamente a *Hard Attack* e *Piercing* per la **Compagnia AT** e il **Battaglione d'élite**.

---

## 🎨 GRAFICA E ASSET

Copia i tre file `.dds` nel seguente percorso di destinazione:

```text
gfx/interface/equipment/efw/efw_machinegun.dds
gfx/interface/equipment/efw/efw_mortar.dds
gfx/interface/equipment/efw/efw_hmg.dds
```

> ⚠️ **ATTENZIONE:** Per questa build, `efw_hmg.dds` viene utilizzato **temporaneamente** come icona delle Armi Anticarro.
> Se crei un'icona specifica per l'AT chiamata `efw_antitank.dds`, modifica il file `interface/efw_equipment_icons.gfx` sostituendo `efw_hmg.dds` con `efw_antitank.dds`.

---

## 🏛️ NUOVI EDIFICI STATALI

| Edificio | Costo | Effetti e Caratteristiche |
| :--- | :---: | :--- |
| **Propaganda** | `1800` | • **+3%** Political Power Gain<br>• **+0.5%** Stability<br>• **+0.5%** War Support<br>• **-2%** Local Resistance Target |
| **Direzione Lavoro** | `2400` | • **+3%** Factory Output<br>• **+3%** Construction Speed<br>• **+5%** Local Resources<br>• *Consuma 1 shared building slot* |
| **Ricerca** | `4500`* | • **+2.5%** Research Speed<br>• *Consuma 1 shared building slot*<br>*( Costo: +1800 per ogni centro già controllato)* |
| **Logistica** | `3200` | • **+0.25** Local Supplies<br>• **+10%** Local Infrastructure Construction<br>• **+5%** Local Building Construction |

---

## 📈 PROGRESSIONE DECISIONI NAZIONALI

```
2 Propaganda ──► Investimenti Nazionali (75 PP)
                   │  +25% Speed Propaganda & Direzione Lavoro
                   │  +5% Construction Generale
                   └──► Sblocca: Emissione Bond
                         │
5 Propaganda + 2 Lavoro ─┴──► Coordinare Economia Nazionale (100 PP)
                                │  +10% Factory & Dockyard Output | +10% Construction
                                │  +5% War Support | -3% Stability
                                │
                                ├──► Finanziare Ricerca (50 PP) ──► +25% Speed Centro Ricerca
                                └──► Piano Infrastrutture (50 PP) ─► +25% Speed Centro Logistico
                                      │
5 Prop. + 3 Lavoro + 2 Ric. + 2 Log. ─┴──► Mobilitare la Nazione (150 PP)
```

### ⚡ Mobilitazione Nazionale *(Sostituisce Economia Coordinata)*
* **+15%** Factory Output
* **+12%** Dockyard Output
* **+15%** Construction Speed
* **+10%** Production Efficiency Growth
* **+5%** Conscription Factor
* **+5%** War Support
* **-5%** Stability

---

## 💰 OBBLIGAZIONI NAZIONALI (BOND)

È possibile attivarne **uno solo alla volta**. Applica un cooldown di **90 giorni** dopo la scadenza/rimborso.

* **Obbligazioni Nazionali:**
  * Costo: `0 PP`
  * Immediato: **+100 PP**
  * Dopo 365 giorni: **-150 PP**
* **Grande Prestito Nazionale:**
  * Costo: `0 PP`
  * Immediato: **+120 PP**
  * Dopo 730 giorni: **-200 PP**

---

## 🛠️ INSTALLAZIONE E COLLAUDO

### 📦 Installazione pulita
Durante lo sviluppo, **elimina completamente** la vecchia cartella `Expanded_Field_Weapons` prima di copiare questa versione, per evitare conflitti con i vecchi file residui (LMG/MMG/HMG I-II-III).

---

### 🧪 Test Rapido Equipaggiamenti

1. Avvia una **nuova partita** caricando esclusivamente la mod EFW.
2. Verifica la comparsa del popup **EFW v1.2**.
3. Se il paese possiede `Support Weapons I`, fai passare 1 giorno e controlla nella scheda **Produzione**: devono comparire *Mitragliatrici*, *Mortai* e *Armi anticarro*.
4. Nel **Division Designer**, verifica la presenza delle 3 compagnie di supporto e del *Battaglione d'élite armi pesanti* tra i battaglioni di linea.
5. Annota le statistiche di una divisione contenente queste unità.
6. Apri la console (`~`) ed esegui: `research support_weapons2`
7. Fai avanzare di 1 giorno: le statistiche della divisione devono **aumentare** senza che appaiano nuovi modelli nella scheda Produzione.
8. Ripeti la verifica per `support_weapons3` e `support_weapons4`.

#### 💻 Comandi Console Utili:
```bash
research support_weapons
research support_weapons2
research support_weapons3
research support_weapons4
research infantry_at
research infantry_at2
updateequipments
updatesubunits
```

---

### 🧪 Test Sistema Economico / Edifici

1. Avvia una **nuova partita**.
2. Apri il pannello **Decisions** e seleziona *"Mobilitazione e Investimenti Nazionali"*.
3. Seleziona uno stato *core* e avvia *"Costruire un Centro di Propaganda"*.
4. Controlla il consumo di **-10.000 manpower** e la presenza dell'edificio nella coda di costruzione.
5. Completati 2 centri di propaganda, verifica la comparsa della decisione *"Avviare gli Investimenti Nazionali"*.

> ⚠️ **NOTA v0.1:** Se cancelli manualmente una costruzione dalla coda o se l'edificio viene distrutto, il manpower dei lavoratori **NON** viene restituito automaticamente. La funzione di recupero verrà implementata nella versione v0.2.

---

## 🔍 DEBUG

Se riscontri anomalie, controlla il file `error.log` cercando le seguenti chiavi:
* `efw_propaganda`
* `efw_labor`
* `efw_research_center`
* `efw_logistics`
* `efw_national_mobilization`