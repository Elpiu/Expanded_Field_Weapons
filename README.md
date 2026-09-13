# Expanded Field Weapons (EFW)

**Expanded Field Weapons** amplia Hearts of Iron IV con equipaggiamenti da campo, mezzi improvvisati e un sistema di mobilitazione economica nazionale.  
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

Il design utilizza un modulo speciale:

```text
efw_wooden_construction
```

che rappresenta una struttura costruita con materiali economici e facilmente reperibili.

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

# 7. Carro armato improvvisato

EFW include anche un mezzo terrestre improvvisato:

## EFW Tin Tank

Il Tin Tank è un carro leggero economico destinato a nazioni che non possono sostenere la produzione di mezzi corazzati più avanzati.

È basato sul sistema legacy dei light tanks e privilegia:

```text
basso costo industriale
velocità accettabile
armatura molto leggera
potenza di fuoco limitata
affidabilità ridotta
```

Il mezzo è pensato come soluzione d'emergenza, non come sostituto dei normali carri armati.

---

# 8. Edifici strategici

EFW introduce quattro nuovi edifici strategici.

Tutti gli edifici sono costruibili normalmente dalla schermata costruzioni e sono pensati per creare una progressione economica alternativa.

## Centro di Propaganda e Mobilitazione

Edificio politico-amministrativo dedicato alla propaganda e alla mobilitazione nazionale.

Effetti principali:

```text
Political Power Gain
Stability
War Support
riduzione locale della resistenza
```

Il Centro di Propaganda è la porta d'ingresso principale al sistema di investimenti nazionali.

## Direzione del Lavoro Nazionale

Organismo destinato al coordinamento della forza lavoro e della produzione.

Effetti principali:

```text
Factory Output
Construction Speed
risorse locali
```

È pensato per sostenere la crescita industriale del paese.

## Centro Nazionale di Ricerca

Complesso dedicato al coordinamento di università, laboratori e ricerca applicata.

Effetto principale:

```text
Research Speed
```

Il costo aumenta progressivamente con il numero di centri già controllati, in modo da evitare uno spam eccessivo.

## Centro Logistico e Difesa Civile

Centro regionale per logistica, trasporti, infrastrutture e difesa civile.

Effetti principali:

```text
Local Supplies
Infrastructure Construction
Local Construction
```

È particolarmente utile negli stati industriali, nelle aree strategiche e vicino ai fronti.

---

# 9. Investimenti Nazionali

Dopo aver iniziato a sviluppare la rete di propaganda, il giocatore può avviare:

## Avviare gli Investimenti Nazionali

La decisione rappresenta il primo vero passo verso una politica economica coordinata.

Fornisce bonus alla costruzione di:

```text
Centri di Propaganda
Direzioni del Lavoro
```

oltre a bonus generali alla costruzione e alla produzione industriale.

L'obiettivo è evitare che il giocatore debba aspettare anni prima di vedere un ritorno economico dagli edifici strategici.

---

# 10. Economia Nazionale Coordinata

Dopo aver sviluppato una rete sufficiente di propaganda e lavoro nazionale diventa disponibile:

## Coordinare l'Economia Nazionale

Questa fase rappresenta il passaggio da singoli progetti locali a una politica economica coordinata.

I bonus comprendono:

```text
Factory Output
Dockyard Output
Construction Speed
Production Efficiency Growth
War Support
```

con una piccola penalità alla stabilità per rappresentare la crescente pressione esercitata dallo Stato sulla società.

La decisione accelera inoltre la costruzione dei Centri di Ricerca e dei Centri Logistici.

---

# 11. Mobilitazione Nazionale

Il livello finale del sistema è:

## Mobilitare la Nazione

Richiede una rete sviluppata di:

```text
Centri di Propaganda
Direzioni del Lavoro
Centri di Ricerca
Centri Logistici
```

Una volta attivata, sostituisce la precedente Economia Nazionale Coordinata con un bonus nazionale più potente.

Gli effetti comprendono:

```text
Factory Output
Dockyard Output
Construction Speed
Production Efficiency Growth
Conscription Factor
War Support
```

con una penalità alla stabilità.

La Mobilitazione Nazionale rappresenta il punto in cui industria, propaganda, ricerca, logistica e forza lavoro vengono coordinate verso un unico sforzo nazionale.

---

# 12. Obbligazioni Nazionali

EFW introduce un semplice sistema di debito politico.

## Obbligazioni Nazionali

Il giocatore può ottenere:

```text
+100 Political Power immediatamente
```

ma dopo un anno deve restituire:

```text
-150 Political Power
```

## Grande Prestito Nazionale

Versione a lungo termine:

```text
+120 Political Power immediatamente
```

con rimborso dopo due anni:

```text
-200 Political Power
```

È possibile avere un solo prestito attivo alla volta.

Dopo il rimborso è previsto un breve periodo di cooldown prima di una nuova emissione.

Il sistema rappresenta un vero anticipo di capacità politica futura: permette di accelerare riforme e programmi economici nel presente in cambio di un costo maggiore nel futuro.

---

# 13. Campagna Nazionale di Industrializzazione

Una delle decisioni early-game più importanti è:

## Lanciare una Campagna di Industrializzazione

La decisione richiede:

```text
Political Power
manpower disponibile
treni disponibili
```

Una parte della popolazione viene temporaneamente spostata verso cantieri e programmi industriali.

Effetto previsto:

```text
+20% Construction Speed per circa 6 mesi
```

Durante il programma vengono utilizzati anche alcuni treni.

I treni vengono restituiti alla fine della campagna, mentre la forza lavoro rimane impegnata più a lungo e viene restituita successivamente.

Questa decisione permette a nazioni come l'Italia di accelerare l'industrializzazione iniziale senza ricevere un bonus completamente gratuito.

---

# 14. Esercito nei Lavori Pubblici

Il giocatore può utilizzare personale militare e unità del genio per sostenere lo sviluppo civile.

## Impiegare l'Esercito nei Lavori Pubblici

Il programma:

```text
consuma temporaneamente manpower
costa Political Power
```

e fornisce:

```text
+4 fabbriche civili permanenti
```

Le fabbriche vengono aggiunte come **offsite civilian factories**, evitando problemi con gli slot degli stati.

Il manpower impiegato viene restituito dopo il periodo previsto.

Questa decisione è pensata come forte investimento iniziale, ma ha un costo significativo sulla disponibilità di uomini.

---

# 15. Sovvenzioni Statali all'Industria

La decisione:

## Sovvenzioni Statali all'Industria

rappresenta un programma di finanziamento pubblico diretto all'industria e alla ricerca.

Per circa due anni fornisce bonus a:

```text
Research Speed
Factory Output
Dockyard Output
Political Power Gain
```

ma aumenta anche il peso dei beni di consumo.

Il giocatore ottiene quindi una crescita industriale e tecnologica maggiore in cambio di una parte delle fabbriche civili disponibili.

---

# 16. Programma Nazionale di Infrastrutture

Questa decisione concentra risorse e materiale ferroviario sull'espansione della rete logistica nazionale.

## Programma Nazionale di Infrastrutture

Durante il programma vengono temporaneamente impiegati alcuni treni.

I bonus comprendono:

```text
Infrastructure Construction Speed
Railway Construction Speed
Construction Speed generale
```

Alla conclusione del programma i treni utilizzati vengono restituiti.

---

# 17. Filosofia di bilanciamento

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

# 18. Filosofia tecnica

EFW cerca di utilizzare il più possibile i sistemi vanilla.

Per esempio:

```text
navi improvvisate
→ scafi vanilla + varianti custom

aerei improvvisati
→ airframe vanilla + moduli custom

carri improvvisati
→ archetipi vanilla compatibili

edifici
→ normale sistema di costruzione HOI4

bonus temporanei
→ timed ideas

scadenze
→ eventi ritardati
```

Questo riduce i problemi di compatibilità e rende più semplice il debug.

---

# 19. Contenuti pensati per il giocatore

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

# 20. Installazione

Per utilizzare la mod:

1. Copiare la cartella **Expanded Field Weapons** nella directory delle mod di Hearts of Iron IV.
2. Assicurarsi che il relativo `.mod` / descriptor punti alla cartella corretta.
3. Attivare EFW dal launcher.
4. Avviare preferibilmente una nuova partita dopo aggiornamenti importanti della mod.

Quando si installano pacchetti `MERGE`, copiare il contenuto direttamente nella root di EFW e scegliere **Sovrascrivi** quando richiesto.

---

# 21. Compatibilità

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

---

# 22. Debug

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

# 23. Struttura generale della mod

Le funzionalità di EFW sono distribuite principalmente nelle seguenti directory:

```text
common/
├── units/
├── technologies/
├── ideas/
├── decisions/
├── buildings/
├── on_actions/
└── equipment/modules/

events/

interface/

gfx/

localisation/
├── italian/
└── english/
```

Ogni nuovo contenuto utilizza, quando possibile, il prefisso:

```text
efw_
```

per ridurre conflitti con vanilla e altre mod.

---

# 24. Stato del progetto

Expanded Field Weapons è un progetto in sviluppo continuo.

Le principali aree già sviluppate comprendono:

```text
armi pesanti per fanteria
nuove support companies
battaglione armi pesanti
mezzi navali improvvisati
caccia in legno
carro leggero improvvisato
edifici strategici
mobilitazione economica nazionale
obbligazioni e prestiti
programmi economici early-game
```

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

---

**Expanded Field Weapons — rendere utile anche ciò che una nazione può produrre quando non può permettersi il meglio.**
