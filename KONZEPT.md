# Greek Trees – Konzept (Stand 2026-10-01)

Ziel: griechisch aussehende Bäume in Minecraft, **nur aus Vanilla-Blöcken** (keine neuen Blöcke). Ausgangspunkt sind
die zwei Arten aus der griechischen Stadt auf dem Server (Screenshots in `screenshots/`, aufgenommen 2026-10-01 01:42).

Nicht im Repository (nur lokal): `screenshots/`, die ausgelesenen Bauten in `concept/built/` und die Blätter, die
den gebauten Riesenbaum zeigen (`concept/round4_giant_original.png`, `round4_giant.png`, `round5_design.png`,
`round6_design.png`). Die Skripte, die sie erzeugen, liegen in `concept/`.

## Entscheidungen (2026-10-01)

- **Gewählt:** 01 Zypresse, 02 Olivenbaum, 06 Feigenbaum, 09 Erdbeerbaum, 10 Kretische Dattelpalme.
  Die übrigen Entwürfe bleiben als Archiv in `concept/trees.py`.
- **Zypresse:** komplett nach den gebauten Bäumen, `acacia_log` + `azalea_leaves`. Die 32 Zypressen der Stadt wurden
  aus dem MC5-Backup ausgelesen (`concept/extract_trees.py` → `concept/built/trees.json`, Wegpunkt „0. Tempel“
  -9844/4905) und die Regeln daraus gemessen; Vergleich in `concept/cypress_compare.png`.
- **Erdbeerbaum:** Stämme ohne Füllblöcke (wie Akazienäste), damit keine Knubbel entstehen.
- **Ins Spiel:** später als neue Setzlinge. Wie die Varianten beim Wachsen entstehen: siehe `VARIATIONEN.md`.

## Inhalt dieses Ordners

| Pfad | Was |
| --- | --- |
| `screenshots/` | Die 10 Screenshots von heute (Zypressen, Olivenbaum) |
| `concept/sheet.png` | Übersicht aller 11 Karten |
| `concept/lineup.png` | Größenvergleich aller Arten, Seitenansicht, gleicher Maßstab, Spielerfigur als Referenz |
| `concept/cards/NN_<art>.png` | Eine Karte pro Art: Iso-Ansicht, 3 Varianten auf Augenhöhe, Form, Größe, Blöcke |
| `concept/species.py` | Die fünf gewählten Arten: würfeln (`roll`) und bauen (`build`) getrennt – Vorlage für die Java-Features |
| `concept/trees.py` | Gemeinsame Bauhilfen und Archiv der nicht gewählten Arten |
| `concept/variation/NN_<art>.png` | Wie die Varianten entstehen: Aufbau, 8 Wüchse mit Würfelwerten, Würfeltabelle |
| `concept/make_variation.py` | Erzeugt die Variationsgrafiken neu |
| `concept/world.py`, `concept/extract_trees.py` | Liest Bäume aus einem Weltordner (Anvil), ohne Zusatzpakete |
| `concept/cypress_compare.png` | Deine Zypressen (oben) neben Generator-Wüchsen (unten) |
| `concept/voxel.py` | Kleiner Iso-Renderer mit den echten 26.2-Texturen aus `minecraft-client.jar` |
| `concept/make_sheet.py` | Erzeugt Karten, Lineup und Übersicht neu: `cd concept && python make_sheet.py` |
| `concept/preview.py` | Schnellansicht einer Art mit beliebigen Seeds: `python preview.py plane 1 2 3 4` |

Die Bilder sind gerendert, nicht im Spiel aufgenommen: Vanilla-Texturen, Laubfarbe der Ebene (plains), ohne Shader.

## Vorhandene Arten

| # | Art | Blöcke | Hinweis |
| --- | --- | --- | --- |
| 01 | Zypresse (*Cupressus sempervirens*) | `acacia_log`, `azalea_leaves` | Stamm **Akazie statt Eiche**, Laub Azalee (Entscheidung 2026-10-01). Bauweise wie auf den Screenshots. |
| 02 | Olivenbaum (*Olea europaea*) | `oak_log`, `oak_wood`, `oak_leaves` | Nachbau aus den Screenshots: Gabelstamm mit Loch, liegende Wurzel, breite flache Krone. |

## Vorschläge für neue Arten

| # | Art | Silhouette | Blöcke | Wo |
| --- | --- | --- | --- | --- |
| 03 | Schirmpinie (*Pinus pinea*) | hoher kahler Stamm, flacher Nadelschirm | `spruce_log`, `spruce_wood`, `spruce_leaves` | Küste, Hügelkuppen |
| 04 | Aleppo-Kiefer (*Pinus halepensis*) | schräg, geknickt, Krone in Wolken zerlegt | `spruce_log`, `spruce_wood`, `acacia_leaves` | Küstenwald, Klippen |
| 05 | Morgenländische Platane (*Platanus orientalis*) | 2×2-Stamm, gefleckte Rinde, riesige Schattenkrone | `stripped_pale_oak_wood`, `stripped_birch_wood`, `pale_oak_wood`, `jungle_leaves` | Dorfplatz, Quellen |
| 06 | Feigenbaum (*Ficus carica*) | niedrig, breit, mehrere graue Stämme aus dem Boden | `acacia_wood`, `azalea_leaves` | Gärten, Hofecken |
| 07 | Mandelbaum in Blüte (*Prunus dulcis*) | kleine Vase, rosa Wolke, Blüten am Boden | `cherry_log`, `cherry_wood`, `cherry_leaves`, `pink_petals` | Obstgärten, Farbakzent |
| 08 | Oleander (*Nerium oleander*) | Strauchbaum, ~5 Blöcke | `jungle_log`, `azalea_leaves`, `flowering_azalea_leaves` | Wegränder, Flussbetten |
| 09 | Erdbeerbaum / Andrachne (*Arbutus andrachne*) | glatte orangerote verdrehte Stämme | `stripped_acacia_log`, `stripped_acacia_wood`, `mangrove_leaves` | Macchia, Felshänge |
| 10 | Kretische Dattelpalme (*Phoenix theophrasti*) | Horst aus 2–3 gebogenen Stämmen, hängende Wedel | `jungle_log`, `jungle_wood`, `jungle_leaves`, `cocoa` | Strand, Hafen |
| 11 | Johannisbrotbaum (*Ceratonia siliqua*) | dichte dunkle Kuppel fast bis zum Boden | `dark_oak_log`, `dark_oak_wood`, `dark_oak_leaves` | trockene Hänge, Gehöfte |

Empfehlung für eine erste Runde: **Schirmpinie, Platane, Mandelbaum, Oleander, Dattelpalme** – sie unterscheiden sich am
stärksten von Zypresse, Olive und den Vanilla-Bäumen. Feige, Erdbeerbaum und Aleppo-Kiefer als zweite Runde;
der Johannisbrotbaum ist der schwächste Kandidat (ähnliche Rolle wie die Olive, nur dunkler und runder).

Bewusst nicht gezeichnet:
- **Griechische Tanne** (*Abies cephalonica*, Olymp/Kefalonia): wäre fast eine Vanilla-Fichte.
- **Zitrone/Orange, Granatapfel**: ohne neue Blöcke gibt es keine passende Frucht; mit Laub allein nur „noch ein runder Baum“.
- Kermes-Eiche, Kastanie, Maulbeere, Tamariske: möglich, aber optisch zu nah an den vorhandenen Formen.

## Technische Regeln, die schon in den Generatoren stecken

- **Laubzerfall:** Jedes Blatt liegt höchstens 6 Schritte (über Blätter, flächenverbunden) von Holz entfernt, sonst
  zerfiele es. Die Generatoren setzen weiter entfernte Blätter gar nicht erst (`Tree.finish()`); das Java-Feature
  bekommt denselben Durchgang. Die Palme hat dafür einen versteckten Stamm-Block in der Krone.
- **Äste:** Seitliche Stämme werden zu `*_wood` (Rinde rundum), damit keine Jahresringe an Knicken sichtbar sind.
- **Datteln:** `cocoa` hält nur an Tropenbaumstämmen – die Palme hat genau so einen Stamm.
- Jede Art ist regelbasiert mit Zufallsbereichen; jeder Seed gibt eine andere Variante (siehe die drei Seitenansichten
  pro Karte).

## Mod (Stand 2026-10-02)

Fabric-Mod `greektrees` im Projektordner (`build.gradle`, `src/`), Jar `build/libs/greektrees-<version>.jar`.
0.1.1 (2026-10-02): alle Bäume aus Holz statt Stämmen, Olive mit mehr Variation (Wurzeln, Fuß, Größe, Kronen),
Palmenstämme einen Block dick mit diagonalem Versatz nach 2–3 Blöcken, Palmen höher (16–23).
0.1.2 (2026-10-02): Olive mit Azaleenlaub wie die gebauten, Crafting-Rezepte (siehe README.md) mit Freischaltung
im Rezeptbuch. Setzlings-Texturen vom Nutzer abgenommen.
0.1.3 (2026-10-02): Mod-Icon = Mosaik-Olivenbaum (Runde 2, Konzept H, mit weniger Boden und mehr Luft),
erzeugt von `tools/make_icons.py`; Runde 1 abgelehnt (`art/icon_concepts/round1/`).
0.2.0 (2026-10-02): die bisherige Palme ist jetzt der Große Dattelpalmensetzling (Rezept 4 Dattelpalmensetzlinge
2×2); der normale Dattelpalmensetzling wächst in ursprünglicher Höhe mit 1 Stamm, 2 diagonalen oder 3 im L.
Neu: Dattel (Item, essbar, an Tropenholz pflanzbar) und Dattelrispe (Block, reift wie Kakao, hängt an den Palmen);
Palmenlaub (Dschungellaub mit Tropenholz im Umkreis 5) lässt Datteln fallen. Damit gibt es doch einen neuen Block,
die Bäume selbst bleiben Vanilla.
0.3.0 (2026-10-02): Dattelrispe größer (füllt fast den ganzen Block) und ohne flackernde Flächen (vorher lagen
Modellboxen deckungsgleich übereinander; `tools/date_cluster.py` prüft das jetzt), Rispen unter jeder Palmenkrone
(4–6 je Stamm statt 2 am Hauptstamm) in gemischten Reifestufen, Laub-Drops verdreifacht (12 %). Neu: Olive
(Olivenzweig hängt unter der Olivenkrone, beim Essen bleibt ein Olivenkern, der sich wie ein Schneeball werfen
lässt) und Erdbeerbaumfrucht (Erdbeerbaumzweig); reife Früchte per Rechtsklick pflücken; eigener Creative-Tab
„Griechische Bäume“.
0.4.0 (2026-10-02): nur reife Früchte lassen sich pflücken, danach zurück auf Stufe 1 (halbreif, wie Süßbeeren);
unreif abgebaut immer 1 Frucht. Olivenkern 1,5 Herzen Schaden, Geschärfter Olivenkern (2 Kerne übereinander)
3,5 Herzen. Neue formlose Rezepte (siehe README.md). Neu: Feige (Feigenzweig unter der Feigenkrone; Feigenlaub
wird an den Feigenzweigen erkannt, weil Feige und Zypresse dasselbe Holz und Laub haben). Dattelmodell: vier
organischere Vorschläge in `art/date_concepts/sheet.png` (`tools/date_concepts.py`).
0.5.0 (2026-10-02): Dattelrispe = Mischung aus Vorschlag B und C (lange Fäden, dicht besetzt, gekippte Elemente;
`tools/date_cluster.py`, Vorschau `art/date_concepts/BC_final.png`). Reif hängt sie fast einen halben Block unter
ihren Block, deshalb sitzt eine tiefere Rispe nur noch an Seiten ohne Rispe darüber.
0.5.1 (2026-10-02): Pflanzen entfernt – ein Missverständnis, in 0.5.2 zurückgenommen.
0.5.2 (2026-10-02): Regeln vom Nutzer: Rechtsklick auf Laub pflanzt (jede Seite des Laubblocks, der Zweig hängt
darunter; Datteln an Tropenholz); Rechtsklick auf eine reife Frucht erntet sie, egal mit was in der Hand, und
pflanzt sie direkt nach (erste Stufe); Rechtsklick auf eine unreife Frucht macht nichts (Knochenmehl wirkt
weiter); Linksklick baut ab.
0.5.3 (2026-10-02): Im Prism-Test wurde jede Frucht in jeder Stufe geerntet – nicht von dieser Mod, sondern von
„Simple Harvesting“ (in der Instanz „26.2 Fabric new“): Sie hält jeden Block mit einer `age`-Eigenschaft für eine
Feldfrucht, kennt bei fremden Blöcken die letzte Stufe nicht (0) und bricht den Zweig in jeder Stufe ab, ohne
nachzupflanzen. Die Zweige heißen ihre Reife jetzt `stage`; Datteln bleiben Kakao-artig (Simple Harvesting erntet
nur reife und pflanzt nach). Im Selbsttest mit Simple Harvesting in `run/mods` nachgestellt (3 Fehler) und nach
der Änderung mit und ohne die Mod bestanden.
0.6.0 (2026-10-02): Feigenzweige und Feigen-Item mit den vier Grüntönen des Azaleenlaubs statt Neongrün (Vorher/
Nachher: `art/preview_fig_colour.png`; der Setzling folgt in 0.7.1). Große Dattelpalme mit 2–5
Stämmen, Nebenstämme auch diagonal versetzt (Regeln in `VARIATIONEN.md`, Wüchse in
`concept/selftest_large_date_palm.png`); der Selbsttest würfelt 500 Formen und prüft Stammzahlen und dass nie zwei
Stämme Seite an Seite stehen.
0.7.0 (2026-10-02): Maulbeerbaum (Material C: `pale_oak_wood` + `jungle_leaves`) und Trauerweide (Material A:
`dark_oak_wood` + `birch_leaves`) als Setzlinge, nach `concept/round3.py`. Neu: Maulbeere (Item, essbar, an Laub
pflanzbar) und Maulbeerzweig (weiß-grün → rot → schwarz); Dschungellaub mit Fahleichenholz im Umkreis 5 lässt
Maulbeeren fallen. Rezepte: Fahleichensetzling + Süßbeeren, Schwarzeichensetzling + Birkensetzling (von mir gewählt,
noch nicht abgenommen). Texturen in `art/preview_saplings.png` und `art/preview_fruit.png`, noch nicht abgenommen.
0.7.1 (2026-10-02): auch der Feigensetzling im Azaleen-Grün (auf Wunsch).
0.8.0 (2026-10-02): drei Maulbeersorten (Wunsch: „alle drei“): jeder Baum würfelt schwarz, weiß oder rot (je ein
Drittel). Alle beginnen weiß-grün; schwarz → rot → schwarz, weiß → creme → weiß mit rosa Hauch, rot → rosa →
tiefrot. Eigene Zweige und Items (`black_`/`white_`/`red_mulberry`, die 0.7-IDs `mulberry`/`mulberry_twig`
gibt es nicht mehr); das Laub lässt die Sorte fallen, deren Zweige in der Nähe hängen (Fahleichenholz und Zweig
im Umkreis 5). Vorschau `art/preview_mulberries.png`.
0.9.0 (2026-10-02): Maulbeerbaum ohne Wurzelanlauf. Trauerweide: Stamm versetzt sich Fläche an Fläche statt über
Kanten (Screenshots des Nutzers 2026-10-02_21.27.42 = vorher, 21.27.50 = so soll es sein), gewölbte Krone, ein
paar Ranken außen am Vorhang; große Trauerweide mit 2×2-Stamm aus vier Setzlingen im Quadrat (Vanilla-Mechanik
wie Schwarzeiche), 13–15 hoch, 17–19 breit. Wüchse in `concept/selftest_weeping_willow.png`,
`concept/selftest_large_weeping_willow.png`. Die Mod-Generatoren sind die Referenz; `concept/round3.py` hat den
Stand der Weide, nicht den des Maulbeerbaums.
0.10.0 (2026-10-02): Große Dattelpalme ohne eigenen Setzling: vier Dattelpalmensetzlinge im Quadrat (alte Items
`large_date_palm_sapling` verschwinden). Große Trauerweide meist mit Knick im 2×2-Stamm und 2–3 Blöcke höher
(16–17), damit sie immer über der normalen (bis 13) liegt. Selbsttest `squareGrowth` für beide.
Je Baum ein neuer Setzling (plus Topf-Variante), der Baum selbst besteht nur aus Vanilla-Blöcken. Java-Port der
Generatoren: `src/main/java/greektrees/tree/TreeShapes.java`. Setzlings-Texturen: `tools/make_textures.py`, Icon: `tools/make_icons.py`
(Vorschau in `art/`), JSON-Ressourcen: `tools/make_resources.py`. Selbsttest im Dev-Server:
`./gradlew runServer -PselfTest` → `run/greektrees-selftest/summary.txt`; die gewachsenen Bäume gerendert in
`concept/selftest_trees.png` (`concept/render_selftest.py`).

## Runde 3: Maulbeerbaum und Trauerweide (Konzept, 2026-10-02)

Generatoren in `concept/round3.py`, Bilder mit `cd concept && python make_round3.py`:
`concept/cards/12_mulberry.png`, `concept/cards/13_weeping_willow.png`, `concept/round3_materials.png` (je drei
Materialvarianten, Maulbeer-Skizze), `concept/round3_lineup.png` (neben den Mod-Bäumen aus dem letzten Selbsttest).

| # | Art | Silhouette | Blöcke (Vorschlag A) | Wo |
| --- | --- | --- | --- | --- |
| 12 | Maulbeerbaum (*Morus alba / nigra*) | kurzer dicker Stamm, gabelt tief, dichte runde Kuppel, 10 hoch, 7–11 breit; jeder dritte ein Kopfbaum (höherer Stamm, Knubbel-Faust, flacher Schirm) | `dark_oak_wood`, `jungle_leaves`, Maulbeerzweig | Dorfplatz, Seidenhöfe, Brunnen |
| 13 | Trauerweide (*Salix babylonica*) | schiefer kurzer Stamm, 5–7 Äste steigen und biegen sich zum Rand, Laubvorhang bis fast zum Boden, innen ein Raum; 9–11 hoch, 11–13 breit | `dark_oak_wood`, `birch_leaves` | Quellen, Bäche, Brunnen, Teiche |

- **Maulbeere als Frucht** wie Olive, Feige, Erdbeerbaumfrucht: Zweig unter der Krone, weiß-grün → rot → schwarz;
  Laub-Drops über Dschungellaub mit `dark_oak_wood` im Umkreis (Vanilla-Dschungelbäume haben Stämme, keine Hölzer,
  und Palmen erkennt man an `jungle_wood`).
- **Weide:** Die Strähnen enden dort, wo Vanilla-Laub zerfallen würde (6 Schritte vom Holz); deshalb reichen die
  gebogenen Astenden bis an den Rand. Ranken (`vine`) unter den Strähnen wären eine Option für noch längere Vorhänge.

## Runde 4: Widdereiche / Aries Oak (Konzept, 2026-10-02)

Name vom Nutzer gewählt: **Widdereiche** / **Aries Oak** (lateinisch für die Karte *Quercus arietina*), nach dem
Riesenbaum, den ein Mitspieler in der Stadt gebaut hat (Aries = Widder; das Goldene Vlies hing in einer heiligen Eiche).

Der Riesenbaum bei x -9955 z 4728 (MC5-Backup), ausgelesen mit `concept/extract_giant.py` → `concept/built/giant.json`,
gerendert in `concept/round4_giant_original.png`: 56 hoch, 31 breit; runder hohler Stamm (5 breit, 55 hoch, unten
verbreitert), Äste in zwei Etagen (29–32 und 43–46), unterer Laubkranz (31–38, Radius 4–14), hohle Laubkuppel
(Wand Radius 12,6 von 42–46, dann bis 55), Azaleen- und blühendes Azaleenlaub, Ranken vom Kranz bis zum Boden und
von der Kuppel bis auf den Kranz, Leuchtbeeren an Moosblöcken.

Generator `concept/round4.py` (Bild `concept/round4_giant.png`, `python make_round4.py`): 4×4-Stamm ohne Ecken
auf dem 4×4-Setzlingsquadrat, 50–56 hoch. Weil gewachsenes Laub (anders als gebautes) zerfällt, hat er mehr Holz
als das Original: 10 untere und 12–14 obere Äste, von denen Rippen unter der Kuppelschale bis nach oben laufen.
Organischer als der Bau (Wunsch des Nutzers): der Stamm schwingt in weichen Kurven (Mittellinie als gedrehter
Zufallsweg, dazwischen weich übergeblendet), Wurzeln laufen über den Boden aus, Äste sitzen ungleich hoch und
knicken, die Kuppel ist beulig und ihr Rand hängt ungleich tief, Ranken sind ungleich lang.
Die Kuppelform passte dem Nutzer nicht („schau dir Bilder von großen Minecraft-Bäumen an“). Dritte Form nach
Bildern großer gebauter Bäume (Bing-Bildersuche): ausgestellter Fuß mit 6–9 Kriechwurzeln, kegelig verjüngter,
leicht schwingender Stamm, der sich bei 40–48 % der Höhe in 3–5 dicke Äste (2×2) und einen Leittrieb teilt; die
Äste gabeln sich zweistufig, an jedem Ende und entlang der oberen Astteile sitzen Laubballen (Blumenkohl-Krone,
47–58 hoch, 36–54 breit), darunter Ranken (meist kurz, ein Drittel lang) und Leuchtbeeren an Moos.
Entschieden: eigener Setzling „Widdereichensetzling“ / „Aries Oak Sapling“, wächst nur als 4×4; Rezept formlos
Schwarzeichensetzling + blühende Azalee + Leuchtbeeren. Setzlings-Textur in `art/preview_saplings.png`.
Die Blumenkohl-Form passte auch nicht: „weniger große Wurzel, größere Haupt-Baumkuppel, eher wie im Original,
dann die abgehenden Kronen wie im 2. Versuch“. Vierte Form (jetzt in `concept/round4.py`): der geschwungene
Stamm des 2. Versuchs, Fuß nur leicht verbreitert mit 4–6 kurzen Wurzeln (2–3,5 Blöcke), große Hauptkuppel
(Radius 13,5–15, Original 12,6), darunter die Seitenkronen an den unteren Ästen wie im 2. Versuch;
52–57 hoch, 30–34 breit.
Die vierte Form passte nicht („der Stamm muss rund sein und organisch, unten breiter und nach oben schmaler
werdend, die seitlichen Kronen größer und weiter aus dem Baum herausragend“), weiter in Runde 5.

## Runde 5: Widdereiche, fünfte Form mit fünf Variationen (Konzept, 2026-10-02)

Generator `concept/round5.py` (`python make_round5.py`), Parameter in `DESIGN`, Variationen in `VARIANTS`;
`round4.py` bleibt als Geschichte der ersten vier Formen.

- `concept/round5_design.png`: Original und drei Wüchse des Entwurfs (ganz, aufgeschnitten, von der Seite).
- `concept/round5_variations.png`: Entwurf und fünf Variationen aus demselben Samen (ganz, aufgeschnitten).

Entwurf: runder Stamm, je Schicht eine Holzscheibe, die sich von unten nach oben verjüngt (am Boden etwa 11 breit,
Fuß samt kurzen Wurzeln 15–16, unter der Kuppel 4–5). Der Fuß weitet sich über die ersten 6–8 Blöcke mit 4–5
Wurzelanläufen aus, die in kurze Wurzeln (1,5–2,8 Blöcke) übergehen. Flache Rippen laufen gedreht die Rinde hoch,
dazu 3–5 Knollen; die Mittellinie schwingt weich. Seitenkronen: 5–7 runde Äste in gestaffelten Höhen (40–62 %),
dick am Stamm und dünn am Ende, steigen aus dem Stamm, biegen nach außen und heben sich an der Spitze; jede endet
in einer großen Krone aus 3–5 Laubballen (Radius 5–6,2) mit einem höheren Ballen obendrauf, die 10–35 % über den
Kuppelrand hinausragt, und trägt auf halber Strecke einen kleinen Ballen. Hauptkuppel wie Runde 4 (Radius 13,5–15,
hohle Schale mit Rippen). Ranken vom Kuppelrand und von den Kronenrändern, Leuchtbeeren an Moos. 52–57 hoch,
44–47 breit (ohne Ranken).

Variationen, je ein Merkmal betont:
1. **Stamm:** Fuß 14–15 breit, stärkere Verjüngung, kräftiger Schwung, tiefere gedrehte Rippen, 7–10 Knollen,
   wenig Ranken, damit der Stamm frei steht.
2. **Hauptkuppel:** Radius 17–18, Wand ab 72 % der Höhe, 4 Blöcke höhere Kappe, stärker beulig; die Seitenkronen
   schauen nur knapp darunter hervor. 56–61 hoch.
3. **Seitenkronen:** 8–9 Äste in zwei Etagen (34–64 %), Kronen Radius 6,4–7,4 weit draußen (135–165 % des
   Kuppelradius), Kuppel etwas kleiner (12,5–13,5). 52–57 breit.
4. **Geäst:** 7–8 dickere, stärker steigende Äste mit je zwei Gabeln, kleine lockere Kronen, kaum Ranken; die
   geschwungenen Äste sind von außen zu sehen. 37–42 breit.
5. **Ranken & Leuchtbeeren:** dichter Rankenvorhang (meist bis zum Boden), viermal so viel Moos, 30 % der
   Höhlenranken mit Leuchtbeeren.

Wahl des Nutzers (2026-10-03): „Entwurf 2“, gelesen als zweiter Wuchs des Entwurfs (der Nutzer unterscheidet
„Entwurf“ und „Variationen“), weiter in Runde 6.

## Runde 6: Widdereiche, Entwurf 2 ausgebaut (Konzept, 2026-10-03)

Wünsche nach Screenshots vom aktuellen Bau auf dem Server (Prism-Screenshots 2026-10-02_23.56.14 bis 23.57.08; das
MC5-Backup ist vom 2026-09-09 und zeigt den alten Stand): detailliertere Äste, Leuchtflechten, alle Kronen von
kleinen Ästen aufgespannt, damit man darin bauen kann, Laub zerfällt nicht von selbst.

Generator `concept/round6.py` (`python make_round6.py`): Stamm, Äste, Kuppel und Ranken aus Runde 5, dazu:

- Äste: je 2–4 Seitenäste mit Laubbüschel und 2–4 kurze Zweige; 3–5 Stummel am kahlen Stamm, manche mit Büschel.
- Seitenkronen hohl: Laubballen zwei Blöcke dick über einem Raum, der unten um den Ast herum offen ist (umgedrehte
  Schale); von der Astspitze läuft ein Zweig in die Mitte jedes Ballens und von dort drei Zweige bis ans Laub
  (Zweigschirm, zugleich Boden zum Bauen). Radius 5,6–6,8, halbe Höhe 4,4–5,0; 200–390 freie Blöcke Raum je
  Krone, bis 9–10 hoch. In 60 % der Kronen ein Moosblock mit Glühwürmchenbusch auf dem Ast.
- Hauptkuppel: Rippen ohne Laubhülle (innen sichtbar), jede gabelt sich einmal, wo die Kuppel sich schließt.
- Leuchtflechten in 35–50 Flecken auf Stamm und Ästen; Leuchtbeeren hängen auch von den Unterseiten der Äste
  (30 % mit Beeren), in den Kronenräumen nur kurz (1–4).
- Laub dauerhaft (im Mod `persistent=true`), nichts wird beschnitten; mit normalem Laub würden 150–370 Blätter
  zerfallen.
- 52–57 hoch, 45–49 breit, rund 10 000 Blöcke.

Bilder: `concept/round6_design.png` (Original, Wuchs 2, 1, 3), `concept/round6_details.png` (Gerüst ohne Laub,
Kuppel aufgeschnitten, Seitenkrone von außen / ohne Deckel / aufgeschnitten mit Spieler).

Eingebaut in 0.11.0 (2026-10-03, „baue es mal ein damit ich es mir besser ansehen kann“): `tree/AriesOak.java`
(Port von `round6.py`), `AriesOakSaplingBlock` (wächst nur als 4×4, eigener Prüfer in `advanceTree`, Knochenmehl nur
auf einem vollen Quadrat), `Shape.finishPersistent()` (Laub `persistent=true`), `Shape.softFoot(2)` (Wurzeln und
unterste Fußschicht weichen dem Boden). Selbsttest: 4/4 gewachsen, 54–57 hoch, 47–54 breit, alle Blätter dauerhaft,
nichts zerfallen, Ranken/Leuchtbeeren/Flechten/Glühwürmchenbüsche halten; 1×1, 2×2, 3×3 und 4×4 unter Decke bleiben
Setzlinge. Bild der Wüchse: `concept/selftest_aries_oak.png`.
0.12.0 (2026-10-03) nach dem ersten Blick des Nutzers („Guter Anfang“): Hauptkuppel natürlicher (Beulen: 11–16 Ballen
auf Kappe und Schulter, 3–5 tiefer am Rand; die Fläche wird vor dem Prüfen um bis zu ~1 Block verzogen, Rand
ausgefranst, einzelne Büschel obenauf) und ihre Schale zwei Blöcke dick aus Laub und Moos (Moos in Flecken, innen
die Hälfte, außen gut ein Zehntel; ein Viertel des Mooses innen lässt Leuchtbeeren hängen). Leuchtflechten entfernt.
Schwarzeichen-Treppen und -Stufen in den Absätzen von Stamm, Wurzeln und dicken Ästen (auf der Stufe eine Treppe
zum Holz hin, unter Überhängen umgedreht, Stufe zwischen zwei Seiten; die Treppen drehen sich nach dem Setzen in
die Ecken). Geschälte Schwarzeiche (Holzblock, also ohne Jahresringe) in langen Streifen, ~20 % des Holzes.
Laub: ~20 % Dschungellaub in Flecken, vom Rest ein Viertel blühend (insgesamt ~20 % statt 32 %). Seitenkronen
„zu kantig / zu gerade“: ebenfalls verzogen, unten rund statt flach abgeschnitten, ausgefranst, mit Büscheln.
Selbsttest bestanden: 56–62 hoch, 51–54 breit, ~360 Treppen und ~20 Stufen je Baum.
0.13.0 (2026-10-03): „nimm wieder die vorherige Kuppel als Basis, damit die Kuppel geschlossen ist und clean, dann
setz die neue Generierung außen drauf“: Grundform ist wieder die glatte Kuppel von 0.11 (Wand + Kappe, unverzogen),
jetzt zwei Blöcke dick aus Laub und Moos und geschlossen; die verzogene, beulige Form von 0.12 kommt nur außen
darauf (was davon außerhalb der Grundform liegt, wird mit Laub gefüllt, ausgefranst, mit Büscheln). Keine Treppen
mehr, nur Schwarzeichen-Stufen, etwa halb so viele (160–200 je Baum), drei Viertel an den Ästen. Lose Blöcke, die
das Verziehen und das Ausfransen abtrennen, fallen weg (nur die größte zusammenhängende Gruppe wird gesetzt);
geprüft an den Selbsttest-Bäumen: 0 Laub-/Moosblöcke ohne Verbindung zum Holz (vorher 81–159).
Selbsttest bestanden: 58–60 hoch, 52–58 breit, ~175 Stufen je Baum.
0.14.0 (2026-10-03): „Seitenkronen etwas größer und auch hier wieder eine cleane Kuppel als Basis und darauf die
Variation. Generell etwas weniger Chaos auf den Kuppeln, also einen Mittelweg finden“: Seitenkronen Radius 6,4–7,6
(vorher 5,6–6,8), halbe Höhe 4,8–5,6, Äste reichen 115–140 % des Kuppelradius; Grundform jeder Seitenkrone ist die
unverzogene Schale der Ballen (2 dick, unten offen), die verzogene Form mit 2–4 Beulen kommt nur außen darauf.
Mittelweg auf beiden Kuppeln: weniger und flachere Beulen (Hauptkuppel 8–12 statt 11–16, halb eingesunken),
Verzug 0,8 statt 1,0 (Seitenkronen 1,0 statt 1,4), ausgefranst 5–6 % statt 10–12 %, Büschel 2 % statt 4–5 %,
außen weniger Moos (8 % statt 12 %).
Trauerweiden (beide Größen): Blasseiche (`pale_oak_wood`) und Azaleenlaub statt Schwarzeiche und Birkenlaub.
Krumme Stämme neu: Bisher versetzte sich der Stamm in einer Schicht auf beiden Achsen zugleich (drei Blöcke im L)
und die große Weide knickte aus und wieder zurück, das ergab klotzige Treppen. Jetzt folgt der Stamm einer weichen
Kurve (verlässt den Fuß schräg, oben senkrecht), versetzt sich je Schicht höchstens einen Block auf einer Achse,
mit mindestens zwei geraden Schichten dazwischen; der dünne Stamm behält am Versatz ein Knie wie im gewünschten
Screenshot von 0.9.0. Selbsttest bestanden: Widdereiche 53–56 hoch, 51–58 breit, 0 lose Blöcke; Weide 10–12 hoch,
große Weide 15–18 hoch mit 2×2-Stamm.
Weiden-Rezept jetzt Blasseichensetzling + Azalee (Nutzer: „ja“). Je 5 Texturvorschläge für Widdereichen- und
Weidensetzling: `python tools/sapling_concepts.py` → `art/sapling_concepts/` (A–E, groß, als Kreuz auf Gras, auf
dem Boden neben bisheriger Textur und Vanilla-Setzling).
Gewählt („a und b“): Widdereiche A (kleine Widdereiche), Trauerweide B (Vorhang), eingebaut in
`tools/make_textures.py`. Danach je 3 Varianten der beiden (`python tools/sapling_concepts.py 2` →
`art/sapling_concepts/*_v2.png`): Widdereiche A1 Hochstamm, A2 mit Leuchtbeeren, A3 weit ausladend; Weide B1 lang
und dicht, B2 mit Bögen, B3 mit Knie.
Nutzer: „der Stamm der Trauerweide soll beim Setzling gekrümmt sein, 5 Variationen davon“ →
`python tools/sapling_concepts.py 3` → `art/sapling_concepts/weeping_willow_sapling_v3.png`: B mit K1 Bogen,
K2 S-Kurve, K3 schräg aus dem Fuß, K4 über dem Wasser, K5 zwei Triebe.
Nutzer: „sieht alles schlecht aus, der Stamm soll eine leichte C-Form haben und die Krone soll nach einer
Trauerweide aussehen“ → neu gezeichnet (`python tools/sapling_concepts.py 4` →
`art/sapling_concepts/weeping_willow_sapling_v4.png`, `fountain()`): gewölbte helle Kuppel, aus der die Ruten wie
eine Fontäne nach außen und dann senkrecht fallen, dunkel dazwischen, außen am längsten, in der Mitte frei für
den Stamm mit 1 Pixel C-Bogen; W1 dicht, W2 lang, W3 luftig.
Gewählt: W1 (dicht), eingebaut in `tools/make_textures.py`; die Widdereiche bleibt bei A.
Offen: Test in Prism.

## Offen

- Sollen die Bäume zusätzlich von selbst in bestimmten Biomen wachsen?
