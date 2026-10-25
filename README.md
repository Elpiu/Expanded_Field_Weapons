# Expanded Field Weapons (EFW)

**Expanded Field Weapons** amplia Hearts of Iron IV con equipaggiamenti da campo, mezzi improvvisati, un sistema di mobilitazione economica nazionale e 192 nuove leggi nel pannello politico.  
La mod nasce per dare maggiore importanza a mitragliatrici, mortai, armi anticarro, mezzi navali e aerei improvvisati, oltre alla preparazione industriale del paese.  
L'obiettivo è aggiungere nuove scelte strategiche senza sostituire i sistemi vanilla, mantenendo tutto leggibile, modulare e facile da bilanciare.  
Molti contenuti sono pensati soprattutto per il giocatore e sfruttano equipaggiamenti, designer e meccaniche già presenti in HOI4.  
La mod è sviluppata e testata principalmente su **Hearts of Iron IV 1.19.x**.

Link Steam Workshop

https://steamcommunity.com/sharedfiles/filedetails/?id=3801242021

---

# Contenuti della mod

## 1. Nuovi equipaggiamenti da campo

EFW separa parte dell'equipaggiamento pesante della fanteria dalle normali Infantry Equipment, introducendo tre nuove categorie produttive dedicate.

### Mitragliatrici

Le **Mitragliatrici** rappresentano mitragliatrici leggere, medie e pesanti destinate alle unità di supporto e ai reparti di armi pesanti.

Sono prodotte come equipaggiamento separato e vengono utilizzate da:

- Compagnia Supporto Mitragliatrici
- Battaglione Armi Pesanti

### Mortai

I **Mortai** rappresentano mortai leggeri e medi utilizzati come supporto diretto alla fanteria.

Sono prodotti separatamente e vengono utilizzati da:

- Compagnia Supporto Mortai
- Battaglione Armi Pesanti

### Armi anticarro di fanteria

Le **Armi anticarro** rappresentano fucili anticarro, lanciatori, cariche e altri sistemi portatili destinati alla fanteria.

Sono prodotti separatamente e vengono utilizzati da:

- Compagnia Supporto Anticarro di Fanteria
- Battaglione Armi Pesanti

Questi equipaggiamenti sono pensati per rendere più interessante la produzione terrestre e per distinguere meglio la fanteria standard dai reparti specializzati.

---

# 2. Nuove compagnie di supporto

La mod aggiunge tre compagnie di supporto dedicate.

## Compagnia Supporto Mitragliatrici

Una compagnia specializzata nel fuoco automatico e nella soppressione.

Utilizza principalmente:

```text
Mitragliatrici
```

Il suo scopo è aumentare la capacità della fanteria di mantenere un volume di fuoco elevato senza richiedere un intero battaglione di linea.

## Compagnia Supporto Mortai

Una compagnia specializzata nel supporto indiretto a corto raggio.

Utilizza:

```text
Mortai
```

È pensata per aumentare soprattutto la capacità offensiva contro bersagli morbidi e fortificazioni leggere.

## Compagnia Supporto Anticarro di Fanteria

Una compagnia dedicata alla difesa contro mezzi corazzati leggeri e medi.

Utilizza:

```text
Armi anticarro
```

Permette di dare capacità anticarro alla fanteria senza dipendere esclusivamente dai normali battaglioni AT vanilla.

---

# 3. Battaglione Armi Pesanti

EFW introduce anche un battaglione di linea dedicato:

## Battaglione Armi Pesanti

Questo reparto combina:

```text
Mitragliatrici
Mortai
Armi anticarro
```

in un'unica formazione.

È pensato come reparto costoso ma versatile, utile per divisioni d'élite, fanteria pesante o unità destinate a sostenere combattimenti prolungati.

Il battaglione non sostituisce artiglieria, anticarro o support companies vanilla, ma rappresenta una concentrazione di armi pesanti direttamente all'interno della fanteria.

---

# 4. Integrazione con Support Weapons

Le tecnologie vanilla della famiglia **Support Weapons** sono integrate con i nuovi equipaggiamenti EFW.

## Support Weapons I

Sblocca l'accesso iniziale ai nuovi equipaggiamenti:

```text
Mitragliatrici
Mortai
Armi anticarro
```

e permette l'utilizzo delle relative unità EFW.

## Support Weapons II / III / IV

Le tecnologie successive forniscono bonus cumulativi ai nuovi reparti e alle armi pesanti.

In questo modo il sistema EFW cresce insieme alla normale progressione tecnologica della fanteria invece di creare un albero tecnologico completamente separato.

---

# 5. Navi improvvisate

EFW aggiunge una linea di mezzi navali improvvisati progettati per nazioni con capacità industriale limitata o per situazioni di emergenza.

La soluzione utilizza scafi vanilla compatibili con il Naval Designer, insieme a moduli e varianti EFW.

Questo permette ai mezzi improvvisati di funzionare come normali navi HOI4:

```text
design personalizzabile
nomi delle navi
missioni navali
flotte
esperienza navale
supremazia navale
produzione nei cantieri
```

La mod evita, quando possibile, di creare nuovi hull completamente separati e preferisce creare varianti sopra scafi vanilla già supportati dal gioco.

Sono presenti configurazioni improvvisate basate su:

```text
ship_hull_light_1
ship_hull_submarine_1
```

con moduli dedicati EFW.

Questa architettura è stata scelta per mantenere la piena compatibilità con il designer navale e con le normali meccaniche di flotta.

---

# 6. Aereo da caccia in legno

EFW aggiunge un aereo improvvisato:

## EFW Wooden Fighter

Il caccia in legno è costruito utilizzando un airframe vanilla:

```text
small_plane_airframe_0
```

e viene creato come variante compatibile con l'Air Designer.

Il design di partenza monta il modulo speciale:

```text
efw_wooden_boost_airframe     Telaio in Legno e Compressore Overboost
```

che rappresenta una struttura costruita con materiali economici e facilmente reperibili.
Nel designer sono disponibili anche altri moduli improvvisati per lo slot speciale piccolo:

```text
efw_improvised_drop_tank      Serbatoio Ausiliario in Carta Pressata
efw_multirole_combat_rack     Rastrelliera d'Armamento Polivalente da Campo
efw_cast_iron_stove_armor     Blindatura Improvvisata "Stufa da Campo"
efw_bazooka_charlie_tubes     Tubi Lanciarazzi "Bazooka Charlie"
```

La filosofia del mezzo è semplice:

```text
costo inferiore
peso ridotto
buona agilità
autonomia migliorata
affidabilità inferiore
protezione ridotta
```

Il Wooden Fighter utilizza componenti vanilla per motore e armamento, mantenendo la piena compatibilità con il sistema aeronautico del gioco.

---

# 7. Edifici strategici

EFW introduce quattro nuovi edifici strategici, sette edifici delle risorse e due edifici civili.

Tutti gli edifici sono costruibili normalmente dalla schermata costruzioni e sono pensati per creare una progressione economica alternativa.

Gli edifici strategici sono massimo 1 per stato. I bonus nazionali si sommano per ogni edificio costruito, quindi:

- Propaganda, Lavoro e Ricerca hanno un **costo crescente**: ogni edificio già posseduto aumenta il costo del successivo;
- ogni edificio con bonus nazionali ha anche un **malus a tema**.

I primi edifici restano economici; costruirne uno in ogni stato di una grande nazione diventa molto costoso.

Valori indicati per singolo edificio.

## Centro di Propaganda e Mobilitazione

Edificio politico-amministrativo dedicato alla propaganda e alla mobilitazione nazionale.

Costo: 1000 + 1500 per ogni Centro di Propaganda già posseduto. Non usa slot.

```text
+3.6% Political Power Gain
+0.36% Stability
+0.36% War Support
+3.6% difesa dalla deriva ideologica
+1.2% popolazione reclutabile
-0.5% Research Speed            (malus: censura)
-2.4% resistenza locale
```

Il Centro di Propaganda è la porta d'ingresso principale al sistema di investimenti nazionali.

## Direzione del Lavoro Nazionale

Organismo destinato al coordinamento della forza lavoro e della produzione.

Costo: 1600 + 2000 per ogni Direzione già posseduta. Usa uno slot di costruzione.

```text
+4.8% Factory Output
+3.6% Construction Speed
+3.6% crescita dell'efficienza produttiva
-3%   crescita mensile della popolazione   (malus: condizioni di lavoro dure)
-0.4% Stability                            (malus)
+6%   risorse locali dello stato
```

Il calo di stabilità è pensato per essere compensato dai Centri di Propaganda.

È pensato per sostenere la crescita industriale del paese.

## Centro Nazionale di Ricerca

Complesso dedicato al coordinamento di università, laboratori e ricerca applicata.

Costo: 3000 + 1000 per ogni Centro di Ricerca già posseduto. Usa uno slot di costruzione.

```text
+3%   Research Speed
+1.2% efficienza iniziale delle nuove linee di produzione
+0.5% Consumer Goods                (malus: laboratori e personale specializzato)
```

## Centro Logistico e Difesa Civile

Centro regionale per logistica, trasporti, infrastrutture e difesa civile.

Costo: 2200. Non usa slot. Tutti gli effetti sono locali allo stato, per questo non ha costo crescente né malus.

```text
+0.30 rifornimenti locali
-12%  attrito per il controllore dello stato
+12%  velocità costruzione infrastrutture
+12%  velocità costruzione ferrovie
+12%  velocità costruzione snodi di rifornimento
+6%   velocità costruzione edifici nello stato
```

È particolarmente utile negli stati industriali, nelle aree strategiche e vicino ai fronti.

## Edifici delle risorse

Basati sulla mod **Resource Plants** (Steam Workshop 3513657215).  
Ogni coppia di edifici piccolo/grande dell'originale (miniera + impianto) è stata fusa in **un solo edificio per risorsa**, con valori medi tra i due.

Non usano slot di costruzione e hanno un massimo di 5 livelli per stato (carbone: 10).

```text
Acciaieria Integrata     +30 acciaio      per livello
Complesso Petrolifero    +30 petrolio     per livello
Piantagione di Gomma     +30 gomma        per livello
Impianto di Alluminio    +30 alluminio    per livello
Miniera di Tungsteno     +18 tungsteno    per livello
Miniera di Cromo         +18 cromo        per livello
Miniera di Carbone       +25 carbone      per livello
```

Costo: 5500 + 3500 per livello aggiuntivo (carbone: 1000 + 2000).  
Tungsteno e cromo rendono meno perché nell'originale il "grande" (raffineria di terre rare) divideva la produzione tra i due metalli.

Le tecnologie della mod originale non sono incluse: la produzione non cresce con la ricerca.

## Case Popolari

Quartieri di edilizia popolare che attirano lavoratori e famiglie nello stato.

```text
+10% manpower locale
+10% popolazione reclutabile
```

Usa uno slot di costruzione, massimo 1 per stato.

## Campi di Grano

Aziende agricole statali che riducono la domanda di beni di consumo.

```text
-0.5% Consumer Goods per ogni stato con Campi di Grano
+3 slot di costruzione nello stato (usa 1 slot: +2 netti)
+0.1 rifornimenti locali
```

Massimo 1 per stato. Il bonus ai Consumer Goods si somma tra gli stati (10 stati = -5%).

## Interfaccia della vista stato

La riga degli edifici senza slot nella vista stato vanilla ha solo 5 posti.  
EFW la porta a **3 righe da 5** e allunga la finestra verso l'alto, così tutti gli edifici (vanilla + EFW) restano visibili.  
Le nuove icone degli edifici sono aggiunte in coda alla strip vanilla delle icone.

---

# 8. Decisioni: Mobilitazione e Investimenti Nazionali

Tutte le decisioni economiche stanno in un'unica categoria, **Mobilitazione e Investimenti Nazionali**, visibile solo al giocatore.  
Quasi tutte seguono la stessa logica: un beneficio subito, pagato con Political Power, manpower e mezzi (treni e camion) che in molti casi vengono restituiti a fine programma.

| Decisione | Costo | Effetto |
|---|---|---|
| **Piano Industriale – Fase I** | 35 PP, 50k manpower, 5 treni, 200 camion | +8 civili e +2 militari offsite, +15% velocità di costruzione per 180 giorni. Al termine sblocca la Fase II |
| **Piano Industriale – Fase II** | 35 PP, 50k manpower, 5 treni, 200 camion | +7 civili e +4 militari offsite, +15% costruzione per 180 giorni. Alla fine restituisce 10 treni, 400 camion e 50k manpower |
| **Grandi Opere e Piani Regolatori** | 50 PP, 60k manpower, 15 treni, 500 camion | +1 infrastruttura negli stati core sotto il livello 5, +2 slot edificio negli stati core, +30% costruzione per 540 giorni. Risorse restituite alla fine |
| **Programma Navale Straordinario** | 40 PP, 50k manpower, 200 camion | +6 cantieri navali offsite permanenti. Manpower e camion restituiti dopo 1 anno |
| **Autarchia del Carburante** | 45 PP, 30k manpower | Per 365 giorni: +30% velocità raffinerie sintetiche, +10% carburante, +2% beni di consumo. 30% di probabilità di -2% stabilità. Ripetibile |
| **Obbligazioni Nazionali** | 0 PP | +120 PP subito, -180 PP dopo 365 giorni, poi 90 giorni di cooldown. Ripetibile |
| **Patto Sociale e Produzione Diffusa** | 40 PP, 5 treni, 300 camion | Per 3 anni: +500 manpower a settimana, +25% crescita demografica, +6% ricerca, +8% efficienza massima, +10% produzione militare, +4% beni di consumo |
| **Coordinare l'Economia Nazionale** | 75 PP | Richiede 2 Centri di Propaganda e 1 Direzione del Lavoro. Idea permanente: +10% produzione militare e navale, +10% costruzione, +5% crescita efficienza, +5% supporto alla guerra, -2% stabilità |
| **Mobilitare la Nazione** | 100 PP | Richiede 4 Propaganda, 2 Lavoro, 1 Ricerca, 1 Logistica. Sostituisce l'Economia Coordinata: +18% produzione militare, +15% navale, +20% costruzione, +12% crescita efficienza, +7,5% coscrizione, +7,5% supporto alla guerra, -5% stabilità |

Le due decisioni di coordinamento accelerano anche la costruzione di Centri di Ricerca e Centri Logistici (+35%).

---

# 9. Leggi nel pannello politico

Ispirate alla mod **Better Laws and Policies** (Workshop 3097661966), di cui riusano le icone.  
EFW aggiunge **4 nuove sezioni** nel pannello politico, sotto quelle vanilla (Leggi e Governo, Ricerca e Produzione, Stato Maggiore).

Ogni sezione ha **6 slot**, il massimo che il pannello mostra su una riga. Ogni slot contiene **8 leggi**: in tutto 24 slot e 192 leggi.

| Sezione | Slot |
|---|---|
| **Economia e Finanza** | Politica Fiscale · Commercio e Dogane · Industria e Cantieri · Capitali Stranieri · Sussidi e Investimenti · Risorse e Materie Prime |
| **Società e Ordine Interno** | Lavoro e Stato Sociale · Stampa e Propaganda · Ordine Pubblico · Istruzione e Ricerca · Popolazione e Sanità · Difesa Civile |
| **Esercito e Stato Maggiore** | Comando e Ufficiali · Addestramento e Reclutamento · Logistica e Rifornimenti · Armi da Campo e Fanteria · Sanità e Condotta · Dottrina Operativa |
| **Marina, Aviazione e Servizi** | Flotta · Convogli e Sottomarini · Aviazione da Caccia · Aviazione d'Appoggio · Servizi Segreti · Operazioni all'Estero |

Regole comuni a tutti gli slot:

```text
5 leggi da  50 PP   bonus moderati con un malus
3 leggi da 100 PP   un po' più forti, con malus più pesanti
```

Ogni legge mescola almeno un bonus e un malus: nessuna è gratis, ma combinando bene gli slot (per esempio Industria Pesante + Mobilitazione del Lavoro + Finanza di Guerra) si ottiene un vantaggio importante.

Gli slot partono **vuoti**: non c'è una legge di default, la prima scelta la fa il giocatore. Alcune leggi richiedono la guerra in corso o un supporto alla guerra minimo.  
L'IA non adotta queste leggi (`ai_will_do = 0`), quindi le nuove sezioni non cambiano il comportamento dei paesi IA.

Le leggi sono generate da uno script (vedi **Strumenti di sviluppo**): per ribilanciarle si modifica una sola tabella invece dei file generati.

## Designer generici

Nella sezione vanilla **Ricerca e Produzione** EFW aggiunge 21 designer disponibili a tutti i paesi. I 9 per carri, navi e aerei sono in tre livelli di costo:

| Tipo | 500 PP | 1000 PP | 2000 PP |
|---|---|---|---|
| Carri (ricerca corazzati +20/30/40%) | Compagnia Hornet | Consorzio Fury | Raven Corporation |
| Navi (ricerca navale +15/20/30%) | Compagnia Siren | Consorzio Leviathan | Poseidon Corporation |
| Aerei (ricerca aerea +10/20/30%) | Compagnia Insomnia | Consorzio Wardon | Shadow Corporation |

Ogni designer ha un tratto (Progettista Base / Avanzato / Moderno) con bonus alle statistiche di tutti i carri, le navi o gli aerei.

EFW aggiunge anche 6 **designer di materiale** e 6 **concessioni industriali**, specializzati invece che a livelli. Ogni tratto ha un bonus e un piccolo malus:

| Designer di materiale | Costo | Ricerca | Tratto |
|---|---|---|---|
| Armeria Nazionale | 500 | fanteria +15% | equip. fanteria: attacco e affidabilità +5%, costo +5% |
| Fonderie d'Artiglieria | 500 | artiglieria +15% | artiglieria +10% attacco (costo +5%), lanciarazzi +5% |
| Officine della Motorizzazione | 500 | motorizzati +15% | camion: affidabilità +10%, velocità +5%; autoblindo: affidabilità +10% (costo +5%) |
| Consorzio Armi Pesanti | 1000 | supporto +15%, fanteria +5% | supporto: affidabilità +10%; anticarro: attacco +10%; contraerea: attacco aereo +5% (costo +5%) |
| Arsenale Economico | 1000 | fanteria +10%, artiglieria +5% | fanteria, supporto e artiglieria costano meno, ma sono meno affidabili |
| Gruppo Armamenti Integrati | 2000 | fanteria, artiglieria e supporto +15%, motorizzati +10% | +5% a fanteria, artiglieria, anticarro e camion |

| Concessione industriale | Costo | Ricerca | Tratto |
|---|---|---|---|
| Acciaierie Riunite | 500 | industria +10% | +8 acciaio, +1% beni di consumo |
| Compagnia Elettrica Nazionale | 500 | elettronica +10% | -10% consumo energetico delle fabbriche, -2% velocità di costruzione |
| Raffinerie Sintetiche | 500 | risorse sintetiche +15% | raffinerie sintetiche +15%, carburante +5%, +1% beni di consumo |
| Imprese di Costruzioni | 1000 | costruzioni +15% | costruzione +5%, infrastrutture +10%, +1% beni di consumo |
| Consorzio Minerario | 1000 | estrazione +15% | +4 tungsteno, +4 cromo, risorse locali +5%, -1% stabilità |
| Conglomerato Industriale | 2000 | industria +15%, elettronica +10% | produzione militare +3%, crescita efficienza +5%, -5% PP |

Sono adattati dalla mod **Designers Extend** (Workshop 2742251002), scritta per la 1.11, con tre correzioni:

```text
tipi aerei pre-1.12 (fighter_equipment, CAS_equipment, ...)  ->  airframe 1.19 (small_plane_airframe, ...)
reliability scritto due volte nei tratti dei carri            ->  una sola volta
nomi senza prefisso                                           ->  prefisso efw_
```

Nella mod originale i bonus degli aerei non funzionavano più: i vecchi tipi non esistono in 1.19.  
**Disattivare Designers Extend** quando si usa EFW, altrimenti i designer compaiono due volte.

## Consiglieri politici generici

EFW aggiunge 8 consiglieri politici a ogni paese (nome casuale, ritratto generico vanilla, 150 PP come i consiglieri vanilla). Ognuno ha bonus e un malus.

Quattro sono **consiglieri di governo**, uno per ideologia, e si possono assumere solo quando quel partito è al potere:

| Consigliere | Partito al governo | Effetto |
|---|---|---|
| Statista Parlamentare | Democratici | +6% stabilità, +6% PP, +15% opinione commerciale, -3% supporto alla guerra |
| Commissario del Piano | Comunisti | +5% efficienza massima, +4% produzione militare, -3% stabilità |
| Gerarca del Partito | Fascisti | +7% supporto alla guerra, +3% coscrizione, -3% ricerca |
| Uomo d'Ordine | Non allineati | +8% stabilità, +20% difesa dall'influenza ideologica, -3% supporto alla guerra |

Gli altri quattro sono **consiglieri tecnici**, disponibili per tutti:

| Consigliere | Effetto |
|---|---|
| Ministro degli Armamenti | +10% costruzione fabbriche militari, +3% produzione militare, -5% costruzione fabbriche civili |
| Capo della Propaganda | +5% supporto alla guerra, +5% PP, -2% ricerca |
| Diplomatico di Carriera | +15% guadagno di opinione, +15% opinione commerciale, giustificazione dei wargoal +10% più lenta |
| Economista di Guerra | -4% beni di consumo, -3% stabilità |

Sono creati a inizio partita da `history/general/efw_generic_advisors.txt` (stesso meccanismo dei consiglieri generici vanilla): serve una **partita nuova**. Si sommano ai consiglieri vanilla e anche l'IA può assumerli.

---

# 10. Opzioni Militari: Invasioni Rapide

Basata sulla mod **Invasions** (Steam Workshop 3709777606).

Nella categoria di decisioni **Opzioni Militari EFW** il giocatore può attivare e disattivare in qualsiasi momento le **Invasioni Rapide**. Le decisioni sono gratuite e ripetibili.

Quando sono attive viene aggiunta l'idea nazionale **Invasioni Rapide**:

```text
-60 giorni   preparazione invasioni navali      (base 60: nessuna attesa)
+999         invasioni navali pianificabili     (base 1)
+996         divisioni per invasione navale     (base 4)
-7 giorni    preparazione invasioni aviotrasportate (base 7)
```

La mod originale usa i define, che sono fissi e si applicano a tutti i paesi. EFW li riproduce con modificatori nazionali, così l'opzione si può spegnere e vale **solo per il giocatore** che la attiva.

Due define dell'originale non hanno un modificatore equivalente e non sono inclusi:

```text
PARADROP_HOURS                    durata della penalità dei paracadutisti dopo il lancio
INVASION_REPORT_EXPERATION_DAYS   durata dei report di invasione (solo notifiche)
```

---

# 11. Grafica e prestazioni

## Unità sulla mappa e in battaglia

Le compagnie e i battaglioni EFW usano **modelli 3D vanilla** (`infantry`, `artillery`, `anti_tank`): un `sprite` personalizzato senza modello mostrerebbe un'unità mancante sulla mappa e in battaglia.  
Le compagnie di supporto hanno `priority = 0`, come quelle vanilla, così non decidono mai il modello della divisione.

Ogni unità EFW ha:

```text
GFX_unit_<unità>_icon_medium   icona del designer divisioni (152x42, 2 frame: disegno + simbolo NATO)
GFX_unit_<unità>_icon_small    icona piccola della finestra di battaglia e dei tooltip
```

## Icone dei moduli

Tutti i moduli EFW di aerei e navi hanno un'icona nel designer.  
Quelle nuove sono ricavate dalle icone vanilla e ricolorate con materiali "improvvisati" (legno, cartone, ruggine, ghisa, rame), più qualche segno di usura. Le vele sono disegnate da zero:

```text
aerei   telaio in legno · serbatoi in carta pressata · gondola polivalente · blindatura "stufa" · tubi "Bazooka Charlie"
navi    serbatoio ausiliario improvvisato · scafo carenato · vela piccola · vela grande
```

## Ottimizzazione FPS

Adattata dalla mod **FPS BOOSTER** (Workshop 3765424442) e corretta per 1.19 (`common/defines/zzz_efw_fps_defines.lua`):

```text
log e storico      combat log, convogli, guarnigioni e incidenti navali conservati meno a lungo
IA                 template, equipaggiamento, dottrine e diplomazia ricalcolati meno spesso
grafica            niente ombre, alberi, rifrazioni dell'acqua, edifici 3D civili e nebbia visiva;
                   modelli 3D sostituiti dai segnalini prima; meno aerei disegnati
meteo              niente particelle 3D di pioggia, neve, temporali e sabbia (common/weather.txt)
```

La neve al suolo **non** è stata toccata: dà malus di gameplay (attacco, velocità, rifornimenti) e resta come in vanilla.  
Le texture del terreno e il `posteffect_volumes.txt` dell'originale non sono inclusi: le prime non vengono mai caricate, il secondo dà errore.

Per disattivare l'ottimizzazione basta cancellare `zzz_efw_fps_defines.lua` e `common/weather.txt`.

---

# 12. Filosofia di bilanciamento

EFW cerca di evitare bonus completamente gratuiti.

Gran parte dei sistemi segue questa logica:

```text
vantaggio immediato
        ↓
costo politico / industriale / logistico
        ↓
possibile penalità o rimborso futuro
```

Gli edifici strategici sono relativamente economici, ma richiedono comunque tempo di costruzione.

Le decisioni early-game aiutano a ridurre il periodo iniziale di attesa e permettono al giocatore di scegliere come accelerare lo sviluppo:

```text
Political Power
manpower
treni
consumer goods
debito futuro
```

diventano quindi risorse da scambiare tra loro.

---

# 13. Filosofia tecnica

EFW cerca di utilizzare il più possibile i sistemi vanilla.

Per esempio:

```text
navi improvvisate
→ scafi vanilla + varianti custom

aerei improvvisati
→ airframe vanilla + moduli custom

leggi
→ idea_categories + leggi vanilla (law = yes)

edifici
→ normale sistema di costruzione HOI4

bonus temporanei
→ timed ideas

scadenze
→ eventi ritardati
```

Questo riduce i problemi di compatibilità e rende più semplice il debug.

---

# 14. Contenuti pensati per il giocatore

Diverse parti di EFW sono progettate soprattutto per il giocatore umano.

Quando necessario vengono utilizzati controlli come:

```txt
is_ai = no
```

e:

```txt
ai_will_do = {
    factor = 0
}
```

in modo da evitare che l'AI utilizzi decisioni economiche o contenuti sperimentali non ancora bilanciati per il comportamento automatico.

---

# 15. Installazione

Per utilizzare la mod:

1. Copiare la cartella **Expanded Field Weapons** nella directory delle mod di Hearts of Iron IV.
2. Assicurarsi che il relativo `.mod` / descriptor punti alla cartella corretta.
3. Attivare EFW dal launcher.
4. Avviare preferibilmente una nuova partita dopo aggiornamenti importanti della mod.

Quando si installano pacchetti `MERGE`, copiare il contenuto direttamente nella root di EFW e scegliere **Sovrascrivi** quando richiesto.

---

# 16. Compatibilità

EFW è sviluppata principalmente per:

```text
Hearts of Iron IV 1.19.x
```

La compatibilità con altre mod dipende soprattutto da eventuali modifiche agli stessi file vanilla o agli stessi sistemi.

In generale EFW cerca di ridurre i conflitti utilizzando:

```text
ID con prefisso efw_
file separati
varianti invece di replacement vanilla
custom buildings separati
custom decisions separate
```

Fanno eccezione alcuni file di interfaccia che sostituiscono quelli vanilla per mostrare i nuovi edifici:

```text
interface/countrystateview.gui                     vista stato più alta (3 righe di edifici senza slot)
interface/countrystateview.gfx                     strip icone edifici a 40 frame
gfx/interface/buildings/building_icon_strip.dds    31 icone vanilla + 9 EFW
interface/zzz_efw_idea_categories.gfx              strip icone delle sezioni del pannello politico (20 frame)
common/weather.txt                                 meteo vanilla 1.19 senza particelle 3D
common/defines/zzz_efw_fps_defines.lua             define dell'ottimizzazione FPS
```

Le icone delle sezioni del pannello politico dipendono dall'ordine delle categorie di idee: le 14 vanilla occupano i frame 1-14, le 4 di EFW i frame 15-18.
Altre mod che aggiungono categorie di idee (per esempio Better Laws and Policies) spostano queste posizioni e sono **incompatibili** con questa parte di EFW.

Altre mod che modificano la vista stato o la strip delle icone degli edifici (per esempio Resource Plants) sono **incompatibili** con questa parte di EFW.  
Dopo una patch di HOI4 che cambia questi file vanilla, vanno rigenerati partendo dalla nuova versione.

---

# 17. Debug

In caso di problemi controllare:

```text
Documents/Paradox Interactive/Hearts of Iron IV/logs/error.log
```

Le stringhe più utili da cercare sono:

```text
efw_
Unexpected token
Malformed token
Unknown modifier
Invalid scope
Invalid effect
```

Dopo modifiche a:

```text
equipment
technologies
buildings
decisions
variants
on_actions
```

è consigliato testare con una **nuova partita**.

---

# 18. Struttura generale della mod

Le funzionalità di EFW sono distribuite principalmente nelle seguenti directory:

```text
common/
├── units/
├── technologies/
├── ideas/
├── idea_tags/
├── decisions/
├── buildings/
├── defines/
├── on_actions/
└── equipment/modules/

events/

history/general/  consiglieri politici generici

interface/

gfx/

localisation/
├── italian/
└── english/

utility/          script di sviluppo (non caricati dal gioco)
```

Ogni nuovo contenuto utilizza, quando possibile, il prefisso:

```text
efw_
```

per ridurre conflitti con vanilla e altre mod.

---

# 19. Strumenti di sviluppo

La cartella `utility/` contiene script Python (non caricati dal gioco):

```text
utility/efw_laws/gen_laws.py                   genera le leggi del pannello politico da laws_data.py
utility/efw_module_icons/make_module_icons.py  genera le icone dei moduli di aerei e navi
utility/generic_sprite_cropper_v3.py           ritaglio sprite generico
```

`gen_laws.py` rigenera idea_tags, leggi, icone, localizzazione e la strip delle icone di sezione. Si ferma con un errore se:

```text
un modificatore non esiste nella documentazione 1.19
una sezione ha più di 6 slot
uno slot non ha esattamente 5 leggi da 50 PP seguite da 3 da 100 PP
una legge non ha almeno 2 modificatori (un bonus e un malus)
```

I file generati non vanno modificati a mano: verrebbero sovrascritti. Istruzioni in `utility/efw_laws/README_IT.txt`.

---

# 20. Stato del progetto

Expanded Field Weapons è un progetto in sviluppo continuo.

Le principali aree già sviluppate comprendono:

```text
armi pesanti per fanteria
nuove support companies
battaglione armi pesanti
mezzi navali improvvisati
caccia in legno
edifici strategici
edifici delle risorse e civili
opzione Invasioni Rapide
mobilitazione economica nazionale
obbligazioni e prestiti
programmi economici early-game
leggi nel pannello politico (4 sezioni, 192 leggi)
icone di unità e moduli
ottimizzazione FPS
```

Il carro leggero improvvisato (Tin Tank) è stato rimosso: usava l'archetipo `light_tank_equipment`, che in 1.19 non esiste più. Potrà tornare come variante di `light_tank_chassis_0` creata con `create_equipment_variant`.

Bilanciamento, costi, statistiche e requisiti possono essere modificati durante i test.

---

# Credits / Development Notes

Expanded Field Weapons è stata sviluppata attraverso test iterativi direttamente in Hearts of Iron IV, con particolare attenzione a compatibilità, semplicità e facilità di merge.

Per lo sviluppo e il controllo della sintassi sono stati utilizzati come riferimento:

```text
HOI4 Modding documentation
hoi4doc.dev
CWTools HOI4 configuration
HOI4 modding references / community documentation
```

Gli edifici delle risorse si basano sulla mod **Resource Plants** (Steam Workshop 3513657215), rielaborata con un solo edificio per risorsa.

L'opzione Invasioni Rapide si basa sulla mod **Invasions** (Steam Workshop 3709777606), convertita da define a modificatori attivabili.

Le leggi del pannello politico sono ispirate alla mod **Better Laws and Policies** (Steam Workshop 3097661966), di cui riusano le icone delle leggi, degli slot e delle sezioni.

I designer generici si basano sulla mod **Designers Extend** (Steam Workshop 2742251002), aggiornata agli airframe di 1.19.

L'ottimizzazione FPS si basa sulla mod **FPS BOOSTER** (Steam Workshop 3765424442), corretta per le tabelle dei define di 1.19.

---

**Expanded Field Weapons — rendere utile anche ciò che una nazione può produrre quando non può permettersi il meglio.**
