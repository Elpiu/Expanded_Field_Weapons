Generatore delle leggi EFW (pannello politico)

1. Modifica laws_data.py (nomi, costi, modificatori, icone, testi IT/EN).
2. Lancia dalla cartella della mod:

   python utility/efw_laws/gen_laws.py . "D:/Program Files (x86)/Steam/steamapps/workshop/content/394360/3097661966" "D:/Program Files (x86)/Steam/steamapps/common/Hearts of Iron IV"

Rigenera: common/idea_tags/efw_policy_categories.txt, common/ideas/efw_policy_laws.txt,
interface/efw_policy_laws.gfx, interface/zzz_efw_idea_categories.gfx,
gfx/interface/efw_idea_categories.dds, le icone in gfx/interface/ideas/efw_laws/ e
localisation/*/efw_laws_l_*.yml. Non modificare a mano quei file: verrebbero sovrascritti.
Il secondo percorso serve per le icone di Better Laws and Policies (deve essere iscritta).
Lo script si ferma se un modificatore non esiste, se uno slot non ha 5 leggi da 50 PP
seguite da 3 da 100 PP, se una legge non ha almeno 2 modificatori o se una sezione supera i 6 slot.
