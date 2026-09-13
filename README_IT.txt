EXPANDED FIELD WEAPONS v1.2.0
================================
Compatibilita obiettivo: Hearts of Iron IV 1.19.*

NUOVA ARCHITETTURA
------------------
La mod NON crea piu modelli I/II/III delle nostre armi.
Esistono soltanto tre linee produttive permanenti:

  1) Mitragliatrici
  2) Mortai
  3) Armi anticarro

Support Weapons I (support_weapons) sblocca tutte e tre le linee e quattro formazioni:

  - Compagnia mitragliatrici (supporto)
  - Compagnia mortai (supporto)
  - Compagnia anticarro (supporto)
  - Battaglione d'elite armi pesanti (LINEA, non supporto)

Il battaglione d'elite usa contemporaneamente Mitragliatrici, Mortai e Armi AT, oltre a una quota di normale infantry_equipment.

PROGRESSIONE TECNOLOGICA
------------------------
Support Weapons II, III e IV NON sbloccano nuovi equipaggiamenti.
Migliorano direttamente le statistiche delle quattro formazioni EFW tramite tecnologie interne nascoste.
I bonus sono cumulativi e volutamente moderati.

Infantry Anti-Tank I/II forniscono inoltre bonus extra mirati a hard attack e piercing della Compagnia AT e del Battaglione d'elite.

GRAFICA
-------
Copia i tuoi tre DDS qui:

  gfx/interface/equipment/efw/efw_machinegun.dds
  gfx/interface/equipment/efw/efw_mortar.dds
  gfx/interface/equipment/efw/efw_hmg.dds

ATTENZIONE: per questa build efw_hmg.dds e usato TEMPORANEAMENTE come icona delle Armi anticarro, perche era il terzo filename fornito.
Se crei una vera icona AT chiamata efw_antitank.dds, modifica interface/efw_equipment_icons.gfx sostituendo efw_hmg.dds con efw_antitank.dds.

INSTALLAZIONE
-------------
Durante lo sviluppo e consigliato eliminare completamente la vecchia cartella Expanded_Field_Weapons prima di copiare questa versione, per evitare che rimangano i vecchi file con LMG/MMG/HMG I-II-III.

TEST RAPIDO
-----------
1) Nuova partita con solo EFW.
2) Deve apparire il popup EFW v1.2.
3) Se il paese possiede Support Weapons I, dopo un giorno dovresti trovare in Produzione Mitragliatrici, Mortai e Armi anticarro.
4) Nel designer dovresti vedere le 3 compagnie supporto e il Battaglione d'elite armi pesanti tra i battaglioni di linea.
5) Segna le statistiche di una divisione con una di queste unita.
6) Console: research support_weapons2
7) Fai passare un giorno: le statistiche della nuova unita devono aumentare senza comparsa di un nuovo modello in Produzione.
8) Ripeti con support_weapons3 e support_weapons4.

Comandi utili:
  research support_weapons
  research support_weapons2
  research support_weapons3
  research support_weapons4
  research infantry_at
  research infantry_at2
  updateequipments
  updatesubunits
