# Wie die Varianten beim Wachsen entstehen (Stand 2026-10-03)

Maßgeblich ist seit der Mod der Java-Code `src/main/java/greektrees/tree/TreeShapes.java`. Die Konzeptgrafiken in
`concept/variation/` (aus `concept/species.py`) zeigen für Olive und Palme noch den Stand vor dem 2026-10-02; aktuelle
Wüchse aus dem Dev-Server: `concept/selftest_<art>.png` (`./gradlew runServer -PselfTest`, dann
`cd concept && python render_selftest.py olive date_palm`).

## 1. Was Vanilla beim Wachsen macht

Geprüft in der 26.2-Jar (`SaplingBlock`, `TreeGrower`):

- Ein Setzling hat zwei Stufen. Bei jedem Random Tick mit Licht ≥ 9 gibt es eine Chance von 1/7, eine Stufe
  weiterzukommen; nach der zweiten wächst der Baum. Knochenmehl schafft denselben Schritt mit 45 % pro Anwendung.
- Beim Wachsen wählt `TreeGrower` das Baum-Feature:
  - vier Setzlinge im 2×2 → Mega-Variante (Fichte, Tropenbaum, Schwarzeiche, Blasse Eiche),
  - sonst der Hauptbaum, mit einer Zweitchance auf eine seltene Form (Eiche: 10 % Riesen-Eiche),
  - Blumen in der Nähe → Variante mit Bienennest.
- Das Feature bekommt den Zufallsgenerator der Welt. Deshalb wird jeder Baum anders, auch am selben Fleck nach
  Abholzen und Neupflanzen. Passt der Baum nicht (kein Platz), bleibt der Setzling stehen und versucht es später wieder.

## 2. Unsere Bäume: würfeln, bauen, aufräumen

Jedes Wachsen läuft in drei Schritten (Code: `TreeShapes`, dann `Shape.finish`):

1. **Würfeln.** Alle Zufallsentscheidungen fallen auf einmal, jede in einem festen Bereich (Tabellen unten). Heraus
   kommt ein kleiner Steckbrief, z. B. Zypresse: Stamm 3, Körper 6, Oben 1, Kreuz 4, Spitze 4, vier Beulen.
2. **Bauen.** Der Steckbrief wird nach festen Regeln zu Blöcken. Bei Olive, Feige, Erdbeerbaum und Palme bleibt
   danach nur noch ein Zufall übrig: der ausgefranste Rand der Laubwolken (jeder Randblock bleibt oder fällt einzeln).
   Die Zypresse hat keinen solchen Rand, sie bleibt glatt wie auf den Screenshots.
3. **Aufräumen.** Blätter, die mehr als 6 Schritte vom Holz entfernt wären, werden gar nicht gesetzt (sie würden
   sonst zerfallen).

Alle Bäume bestehen aus Holzblöcken (`*_wood`, Rinde auf allen Seiten), nie aus Stämmen: so gibt es nirgends offene
Jahresringe.

Fest sind also die Blocksorten, der Grundaufbau und die Regeln; gewürfelt werden nur Maße, Anzahlen und Richtungen.
Dadurch bleibt jede Art auf einen Blick erkennbar, zwei gleiche Bäume kommen aber praktisch nicht vor.

- **Drehung:** Olive, Feige und Palme drehen stufenlos (0–360°), nicht nur in vier Himmelsrichtungen. Der
  Erdbeerbaum wählt Himmelsrichtungen, damit seine Stämme dünn bleiben.
- **Zypresse:** Die Abschnitte sind fest gestapelt; gewürfelt werden ihre Längen, die Ecken der Übergangsschichten,
  die Seiten der Kappe und jeder Leistenblock einzeln.
- Die Seeds 1–8 in den Grafiken sind nur zum Wiederfinden; im Spiel würfelt der Weltzufall.

## 3. Würfel je Art

### 01 Zypresse – `acacia_wood`, `azalea_leaves`
Gemessen an den 32 Zypressen der Stadt (MC5-Backup, siehe `concept/cypress_compare.png`). Von unten nach oben:
Stamm, Fuß, Körper, Übergang, Kreuz, Kappe, Spitze. Zuerst wird die Höhe gewürfelt, dann die Abschnitte; der
Körper nimmt den Rest auf.

| Würfel | Bereich | Wirkung |
| --- | --- | --- |
| Höhe | 20–23 | wie bei deinen Bäumen: 22 zu 65 %, 23 zu 25 % |
| Stamm | 4 | immer 4; 8 % ein einzelnes Blatt am Stamm darunter |
| Fuß | Kreuz + Kreuz mit Ecken | 85 %; sonst zweimal Kreuz (10 %) oder eine Kreuzschicht (5 %) |
| Körper | 5–8, meist 6–7 | volles 3×3 |
| Leisten | je Seite und Schicht | Block zwei vor der Seitenmitte: 86 % in der Körpermitte, 70 % unten, 55 % oben |
| Übergang | 0–2, meist 1 | Kreuz mit 1–3 Ecken |
| Kreuz | 2–4, meist 3 | 3×3 ohne Ecken; der Stamm endet in der obersten Kreuzschicht |
| Kappe | 0–2, meist 1 | Mitte plus 1–3 Seiten |
| Spitze | 4–5 | einzelne Säule; Kappe + Spitze höchstens 6, sonst zerfiele die Spitze |

### 02 Olivenbaum – `oak_wood`, `azalea_leaves`
Ein Größenwurf skaliert den ganzen Baum; jeder Stamm hat seine eigene Höhe und Krone, dadurch sitzen die Kronen auf
verschiedenen Höhen, oft mit Lücken dazwischen.

| Würfel | Bereich | Wirkung |
| --- | --- | --- |
| Größe | 0,85–1,3 | skaliert Stammhöhen und Neigung |
| Fuß | 0–2 Seiten | verdickter Fuß an zufälligen Seiten |
| Wurzeln | 1–3 | liegen am Boden, in jede Richtung, 1,5–3,2 lang |
| Stämme | 2 (60 %) oder 3 (40 %) | gleichmäßig verteilt, je ±25° |
| Drehung | 0–360° | Ausrichtung des ganzen Baums |
| Stammhöhe | 4–6,5 × Größe, mindestens 3 | je Stamm einzeln |
| Neigung | 1,3–2,6 × Größe | wie weit die Stammspitze nach außen geht |
| Knie | 1,6–2,8 hoch, bei 35–70 % der Neigung | erster Knick des Stamms |
| Ast | ±45°, 1,4–2,6 lang | in die Krone |
| Krone | r 2,5–3,9 · h 1,3–2,3 · 1–2 über dem Ast | je Stamm eine eigene |
| Zusatzwolken | 1–3 | r 1,6–2,6, etwas höher oder tiefer als ihre Krone |
| Oliven | 4–8 Olivenzweige | unter dem untersten Laub einer Spalte (von unten sichtbar), Reifestufe je Zweig: grün 30 %, halbreif 40 %, reif 30 % |

### 06 Feigenbaum – `acacia_wood`, `azalea_leaves`
| Würfel | Bereich | Wirkung |
| --- | --- | --- |
| Stämme | 4–5 | gleichmäßig verteilt, je ±20° |
| Drehung | 0–360° | |
| Knie | weit 2–3, hoch 1–2 | erster flacher Knick aus dem Boden |
| Spitze | weit 3,2–4,2, hoch 3–4 | Ende des Stamms |
| Krone | r 2,5–3,0 | Wolke je Stammspitze, dazu eine feste Kappe in der Mitte |
| Feigen | 4–8 Feigenzweige | wie bei der Olive unter dem untersten Laub, Reifestufen 30/40/30 % |

### 09 Erdbeerbaum – `stripped_acacia_wood`, `mangrove_leaves`
Stämme wie Vanilla-Akazienäste: jeder Schritt ein Block hoch und höchstens einer zur Seite, ohne Füllblöcke. So gibt
es keine Knubbel an Knicken und Gabelung.

| Würfel | Bereich | Wirkung |
| --- | --- | --- |
| Stamm | 2–3 | gemeinsamer gerader Fuß |
| Stämme | 2 oder 3 | 2: genau gegenüber; 3: drei der vier Himmelsrichtungen |
| Stammhöhe | 6–8 | je Stamm |
| Weite | 2–4 | Blöcke nach außen; die ersten zwei Schritte gehen immer nach außen |
| Drall | links/rechts/keiner | ein Schritt seitlich an zufälliger Höhe |
| Seitenast | 1–2 lang | 2–3 unter der Spitze, nach links oder rechts |
| Krone | r 2,0–2,6, Ast r 1,6–2,0 | je eine Wolke auf Stamm und Seitenast |
| Früchte | 4–8 Erdbeerbaumzweige | wie bei der Olive unter dem untersten Laub, Reifestufen 30/40/30 % |

### 10 Kretische Dattelpalme – `jungle_wood`, `jungle_leaves`, Dattelrispen
Seit 0.16.0 (Runden P1–P5, `PLAN-PALME-WEIDE.md`): 15–17 hoch mit Krone. Jeder Stamm ist einen Block dick und
neigt sich nur in eine Richtung, ohne sich zu winden. Ein Versatz heißt: eine Schicht steht einen Block weiter
(Kante an Kante, ohne Füllblock). Das Laub ist dauerhaft.

Seit 0.16.1 wächst kein Stamm mehr als Gerade (in 0.16.0 stand der Versatz fest alle drei Blöcke):

| Würfel | Bereich | Wirkung |
| --- | --- | --- |
| Versätze | Höhe/4 bis Höhe/3, plus 1 (seit 0.17.0, deutlichere Kurve), mindestens 1, höchstens (Höhe − 2)/2 | ein kurzer Stamm (4–5) hat einen, der höchste einer Dattelpalme drei bis vier, die der großen Palme bis sechs |
| Biegung | je ⅓ | oben gebogen (Versätze drängen sich unter der Krone), am Fuß gebogen (darüber gerade), durchgehend schräg |
| Streuung | jeder Versatz ±1 Block | auch zwei „durchgehend schräge“ Stämme sind nicht gleich |
| Abstand | mindestens zwei Blöcke übereinander am Fuß, zwischen zwei Versätzen und unter der Krone | keine Treppe; die Dattelrispen haben oben Holz hinter sich |

| Würfel | Bereich | Wirkung |
| --- | --- | --- |
| Stämme | 1, 2 oder 3 (je ⅓) | seit 0.17.0 alle Füße in einem 2×2: zwei auf einer Diagonale (berühren sich über die Ecke), drei als L auf drei der vier Felder (die Arme Fläche an Fläche am Eckstamm) |
| Ausrichtung | 4 Drehungen × gespiegelt | das Fußmuster in jede Richtung |
| Höhen | 9–11 / 6–7 / 4–5 | bei drei Stämmen steht der höchste auf einem gewürfelten Feld des L |
| Neigung | zwei Stämme: der höchste in eine der vier Richtungen, der andere von ihm weg entlang x oder z; drei Stämme: jeder Arm in seine Richtung, der Eckstamm von beiden weg | nebeneinander dürfen Stammblöcke nur in den untersten drei Schichten stehen; ein Wurf, der das bricht, wird neu gewürfelt |
| Krone | Stern aus acht feinen Wedeln (gerade etwa 5 lang mit hängender Spitze, diagonal kürzer), darüber ein Schopf aus steilen | auf dem zweit- und dritthöchsten Stamm kleiner: gerade Wedel etwa 4 und 3 lang, Schopf kürzer |
| Kronenzufall | seit 0.17.0 je Wedel gewürfelt | Richtung k·45° ± 10°; gerade Wedel 5 − Größe + (−1, 0, 0, +1), mindestens 2; diagonale ± 1 Block; Bogen steigt 1 oder 2 und kippt bei 50–75 % der Länge; hängende Spitze gerade 0–3, diagonal 0–2 |
| Lücken | 25 % der Kronen | ein Sternwedel fehlt oder ist ein Stummel aus 2 Blöcken (je 50 %); die volle Krone hat dann zur Hälfte eine zweite Lücke, nie neben der ersten |
| Schopf | 3–5 steile Wedel | Startwinkel frei, Abstand 360°/n ± 15°, jeder ± 1 Block länger/kürzer und höher/tiefer an der Spitze |
| Kronenspitze | über dem Kern | 1 Blatt immer, 2. zu 70 %, 3. zu 15 %; die vier Blätter neben dem Kern bleiben fest (die Datteln hängen darunter) |
| Datteln | höchster Stamm: 3–4 Seiten am obersten Stammblock, jeder weitere Stamm 2–3 | seit 0.17.0 nur direkt unter dem Laub (unter den vier Blättern neben dem Kronenkern), nie tiefer; Reifestufe je Rispe 30/40/30 % |

### 11 Große Dattelpalme – `jungle_wood`, `jungle_leaves`, Dattelrispen
Wächst seit 0.10.0 aus vier Dattelpalmensetzlingen im Quadrat (wie die Schwarzeiche), der Hauptstamm auf der
Ecke 0, 0 des Quadrats; der eigene Setzling ist weg. Seit 0.6.0 mit bis zu 5 Stämmen, auch diagonal versetzt.

| Würfel | Bereich | Wirkung |
| --- | --- | --- |
| Stämme | 2/3/4/5 (Gewichte 3/4/3/2) | gleichmäßig rundum verteilt, der Hauptstamm zeigt in die Lücke zwischen den Nebenstämmen |
| Fuß der Nebenstämme | nächstes freies Feld zum Ziel (Richtung ±25°, Abstand 1,3–2,9) | eine Ecke direkt am Hauptstamm oder irgendein Feld im Ring 2 Blöcke weiter, also gerade oder diagonal versetzt; nie direkt neben einem anderen Fuß |
| Neigung | jeder Stamm in eine Richtung, gebogen oder schräg gewürfelt (wie bei der Dattelpalme): Nebenstämme zu der Seite, auf der ihr Fuß liegt, der Hauptstamm in die Lücke | seit 0.16.0; liegt der Fuß genau diagonal, entscheidet ein Münzwurf zwischen x und z |
| Höhen | Haupt 12–14, bei 2–3 Stämmen +1, ab 4 Stämmen +2; zweiter 2–4 niedriger, weitere 3–6 niedriger | |
| Abstand | Kronen mindestens 2 Blöcke Höhenunterschied | sonst wird der Stamm um 1 erhöht, bis es passt |
| Regeln | keine zwei Stämme teilen einen Block oder stehen auf gleicher Höhe Seite an Seite; Kronen nicht direkt nebeneinander | ein Wurf, der das bricht, wird neu gewürfelt (nach 25 Fehlversuchen mit einem Stamm weniger) |
| Krone | wie bei der Dattelpalme; der höchste Stamm trägt die ganze, die nächsten beiden die mittlere, weitere die kleine | Laub dauerhaft |
| Datteln | wie bei der Dattelpalme | Dattelrispen unter jeder Krone |

### 12 Maulbeerbaum – `pale_oak_wood`, `jungle_leaves`, Maulbeerzweige
Konzept-Karte 12 (`concept/round3.py`), Material C. Rezept: Fahleichensetzling + Süßbeeren.

| Würfel | Bereich | Wirkung |
| --- | --- | --- |
| Sorte | schwarz / weiß / rot, je ein Drittel | alle Zweige eines Baums tragen dieselbe Sorte |
| Wuchsform | 70 % frei, 30 % Kopfbaum | |
| Stamm | frei 2–3, Kopfbaum 3–4 | gerade, 1×1 |
| Frei: Äste | 3–5, gleichmäßig rundum ±20°, 2–3 weit | über einen Mittelpunkt (55 %, 1–2 höher) zur Spitze 3–4 über dem Stamm |
| Frei: Kuppel | Radius 4,3–5,2, Höhe 3 | über Stamm + 4, unten offen um den Stamm; dazu je Ast eine Wolke (2,4 × 1,8) |
| Kopfbaum: Faust | jede Seite am Stammende zu 60 % ein Knubbel | |
| Kopfbaum: Äste | 3–4, 1,8–2,4 weit, 2 hoch, je ein Knubbel obendrauf | |
| Kopfbaum: Schirm | Radius 3,8–4,4, Höhe 2,1 | flach, erst über den Knubbeln, die man darunter sieht |
| Maulbeeren | 5–9 Zweige unter der Krone | Reifestufe je Zweig 30/40/30 % |

### 13 Trauerweide – `pale_oak_wood`, `mangrove_leaves`
Konzept-Karte 13 (`concept/round3.py`), bis 0.13 Material A (`dark_oak_wood`, `birch_leaves`), seit 0.14 Blasseiche
und Azaleenlaub. Rezept: Blasseichensetzling + Azalee (bis 0.13 Schwarzeichen- + Birkensetzling).

Zwei Größen: ein Setzling gibt die normale Weide, vier Setzlinge im Quadrat (wie bei der Schwarzeiche) die große
mit 2×2-Stamm. Werte: normal / groß.

| Würfel | Bereich | Wirkung |
| --- | --- | --- |
| Stamm | 3–5 / 6–8 hoch, plus bis zu 5 / 4 je nach Größenwurf, mindestens 4 | seit 0.17.0 nach sechs von Hand umgebauten Stämmen (`concept/reference/`, `PLAN-0.17.md`): eine subtile Biegung, manchmal ein C, nie ein Labyrinth; Fuß und oberste Stammschicht glatt; die Krone sitzt über dem Stammende |
| Form | Biegung etwa ⅔, C etwa ⅓ | Biegung: der Stamm rückt einmal um einen Block weiter und bleibt dort (kleine Weide nur entlang einer Achse, ein einzelner Diagonalschritt sähe aus wie ein Zickzack; große Weide Achse oder diagonal, je 50 %); bei der kleinen Weide ab 8 Höhe zu 30 % ein zweites Mal in dieselbe Richtung, mindestens drei ruhige Schichten höher. C: hinaus und denselben Weg zurück, dazwischen ein ruhiger Bauch; diagonal nur selten (30 % der C) |
| Kleine Weide | Säulen mit Knie | ein Versatz = die alte Säule läuft eine Schicht neben der neuen weiter (Fläche an Fläche); diagonal = zwei Versätze in direkt aufeinanderfolgenden Schichten. Biegung zwischen der 3. Schicht und der unter der obersten (bei 4 Höhe ab der 2.); C hinaus in der 3. (ab 7 Höhe auch 4.) Schicht, zurück eine oder zwei Schichten unter der obersten, Bauch mindestens 2 Schichten |
| Knorren | 25 % der kleinen Stämme mit einer ruhigen Säule von mindestens 3 Schichten | 1–2 Blöcke an einer freien Seite der längsten ruhigen Säule, in deren mittlerem Drittel |
| Große Weide | 2×2, weiche Übergänge | höchstens einen Block neben dem Fußquadrat. Achsschritt gewürfelt aus: Vorläufer (ein neuer Block eine Schicht früher), Nachzügler (ein alter Block eine Schicht länger), beides schräg gegenüber, volle 2×3-Übergangsschicht. Diagonalschritt über drei Schichten in einer der zwei gemessenen Formen; beim C auch als zwei Achsschritte zwei Schichten auseinander. Übergangsschichten 5–6 Blöcke, zwei Schichten übereinander teilen immer mindestens 3; C-Bauch mindestens 2 ruhige Schichten. Beim C entlang einer Achse bewegt mindestens einer der beiden Übergänge Blöcke in beiden Spuren (beides oder volle Schicht), sonst sähe eine Seite aus wie ein bloß verschobenes Stammstück |
| Wurzelanlauf | 2–3 / 4–6 Felder neben dem Fuß (ohne Ecken) | große Weide: auf 0–2 davon ein zweiter Block |
| Mitte | Stamm + 3–4 / 5–6 | gerader Leittrieb über dem Stammende bis zur Kronenmitte |
| Krone | Radius 3,0–3,6 / 4,2–4,8, Höhe 2,4 / 3,0 | gewölbt, über der Mitte am höchsten |
| Äste | 5–7 / 7–9, rundum ±14°, Reichweite 4,3–5,2 / 6,3–7,3 ±0,5 | steigen, laufen über einen Bogen und kommen am Rand 2–3 / 3–4 unter der Mitte an; oben ringsum in Laub gehüllt (je Seite 85 %), am Ende eine kleine Wolke |
| Vorhang am Rand | äußerer Ring (1,6 Blöcke), je Spalte 65 % | Strähne 4–9 / 5–11 lang vom untersten Blatt nach unten. Große Weide seit 0.17.0: dazu jede Spalte am Umriss des Laubs von oben (eine Nachbarspalte ohne Laub) in den äußeren 3 Blöcken, und jede Randspalte wird versucht; der Abstand zwischen den Strängen dünnt sie aus (im Mittel 21,5 statt 10,7 Randstränge je Baum) |
| Vorhang innen | ab 2,5 / 3,5 vom Stamm, je Spalte 23 % | Strähne 1–3 / 1–4 |
| Raum | innerhalb 2,5 / 3,5 vom Stamm | keine Strähnen |
| Länge | | `finish()` kappt jede Strähne, wo Vanilla-Laub zerfiele (6 Schritte vom Holz) |
| Ranken | 3–6 / 6–10, je 3–6 / 3–8 lang | außen an Laub des Randes, hängen darunter weiter (jede hält sich an der darüber) |

### 14 Widdereiche (Aries Oak) – `dark_oak_wood` + `stripped_dark_oak_wood`, Azaleen- und Dschungellaub
Nach dem Riesenbaum der Stadt, Konzept Runde 6 (`concept/round6.py`, KONZEPT.md). Wächst nur aus 16 Setzlingen
im 4×4-Quadrat; der Stamm steht mittig darauf. Rezept: Schwarzeichensetzling + blühende Azalee + Leuchtbeeren.
Laub dauerhaft (`persistent=true`), nichts wird beschnitten.

| Würfel | Bereich | Wirkung |
| --- | --- | --- |
| Höhe | Stamm 50–56, Kuppel schließt 1 darüber | |
| Stamm | Radius am Boden 5,2–5,8, nach dem Anlauf 3,3–3,7, oben 2,1–2,4 | je Schicht eine runde Holzscheibe; Anlauf über 6–8 Blöcke mit 4–5 Wurzelanläufen (28 %), Rippen 9 % tief, 0,035 rad je Block gedreht |
| Schwung | Mittellinie über 4 Punkte, je 1,6–2,6 versetzt, Richtung dreht 70–150° | weich übergeblendet |
| Wurzeln | je Anlauf eine, 1,5–2,8 über den Fuß hinaus | unterste zwei Schichten weichen dem Boden |
| Knollen, Stummel | 3–5 Knollen, 3–5 Stummel (2–4 lang, halb mit Laubbüschel) | an kahlen Stamm |
| Äste | 5–7 auf 40–62 % der Höhe, gestaffelt, rundum ±11° | runde Röhre, Radius 1,5–1,9 → 0,4; steigt 4–7, Spitze 115–140 % des Kuppelradius vom Stamm |
| Seitenäste, Zweige | je Ast 2–4 Seitenäste (3–5,5 lang, Laubbüschel 2–2,8) und 2–4 kahle Zweige | |
| Seitenkronen | Radius 6,4–7,6, halbe Höhe 4,8–5,6, ein Ballen obenauf, 4–6 am Rand | Grundform glatt: Laub 2 dick, innen Raum, unten rund und offen; je Ballen ein Zweig von der Astspitze, von dort 3 Zweige ans Laub; 60 % Moos + Glühwürmchenbusch |
| Seitenkronen außen | dieselben Ballen um bis zu ~1 Block verzogen, dazu 2–4 Beulen (2,2–3,2) oben | nur ihre Schale, soweit sie außerhalb der Grundform liegt (der Raum bleibt unten offen); außen 6 % ausgefranst, 2 % Büschel |
| Hauptkuppel | Radius 13,5–15, Wand ab 80 % der Höhe, Beulen 4–8 % | Grundform glatt und geschlossen, Schale 2 dick aus Laub und Moos; 12–14 Rippen 3 unter der Außenhaut, jede gabelt sich einmal |
| Kuppel außen | dieselbe Kuppel um bis zu ~0,8 Blöcke verzogen, dazu 8–12 Ballen (3–5, zur Hälfte eingesunken) auf Kappe und Schulter, 2–4 (3–4) am Rand | was außerhalb der Grundform liegt, wird Laub (8 % Moos), außen 5 % ausgefranst, 2 % Büschel; nur die größte zusammenhängende Gruppe bleibt |
| Moos | Kuppel in Flecken: außen 8 %, innen 50 %; Kronendecken 3 % | Leuchtbeeren: ein Viertel des Kuppelmooses 3–24 lang (12 % Beeren), Kronen 1–4 (9 %) |
| Leuchtbeeren an Ästen | 3 % der Astblöcke mit Luft darunter | 3–14 lang, 30 % mit Beeren |
| Ranken | 25 % der Randblätter außen (ab 60 % des Kuppelradius) | 35 % bis zum Boden, sonst 2–10 |
| Stufen | 160–200, drei Viertel an Ästen und Seitenästen, der Rest an Stamm und Wurzeln | freie Zelle auf (untere Stufe) oder unter (obere Stufe) dickem Holz mit Holz daneben |
| Geschältes Holz | Streifen (Wellenfeld, senkrecht 4× gestreckt), ~20 % | `stripped_dark_oak_wood` |
| Laub | Dschungellaub in Flecken ~20 %, sonst Azalee, davon 25 % blühend | |

## 4. Für später: Setzlinge

- Eigene Setzlinge sind neue Blöcke (Setzling, Item, Topf-Variante, Texturen). Die Bäume selbst blieben Vanilla.
  Ohne neue Blöcke ginge es nur über Vanilla-Setzlinge mit Bedingung (z. B. Akaziensetzling auf Sand → Zypresse).
- Die Würfel bleiben wie oben. Zusätzlich möglich, alles wie bei Vanilla:
  - 2×2-Setzlinge für eine große Variante,
  - eine Zweitchance für eine seltene Form,
  - bei zu wenig Platz kleinere Würfe probieren, statt gar nicht zu wachsen.
