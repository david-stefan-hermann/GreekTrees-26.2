# Plan 0.17.0: Weidenstamm, Stränge der großen Weide, Palmenkrone, Datteln, Setzlings-Artefakte

Stand 2026-10-03, Ausgangspunkt Mod 0.16.2 (Commit 861ef35, Arbeitsbaum sauber). Geschrieben für Opus 5.5.
Rückmeldung des Nutzers nach dem Prism-Test von 0.16.2:

1. Weidenstämme: „Die Übergänge sind nicht organisch genug." Er hat sechs Stämme in der Testwelt von Hand
   umgebaut (Screenshots `2026-10-03_19.11.27` bis `19.13.16` im Prism-Ordner
   `instances/26.2 Fabric new/minecraft/screenshots`). Die Weidenkrone ist gut und bleibt.
   Nachtrag des Nutzers zum ersten Planentwurf: „Der Baumstamm sieht aus wie ein Labyrinth: rechts, links,
   oben, unten, links, hoch, runter. Ich möchte, dass der Baum eine schöne subtile Biegung hat." Und: „Weiden
   sollen nicht IMMER eine C-Form haben, sondern eher eine Biegung und manchmal eine C-Form. Das soll aber
   alles variieren."
2. Große Weide (2×2): es sollen weitere einzelne Laubstränge dazukommen, und zwar nur am Rand.
3. Palmenkrone: gut, aber „zu mathematisch perfekt", mehr Zufall.
4. Bug: Beim Wachsen der 2×2-Palme bleiben Setzlinge stehen, die man nicht abbauen kann; Rechtsklick mit
   Knochenmehl lässt sie verschwinden.
5. Datteln sollen immer direkt unter den Blättern hängen, nie tiefer.

Reihenfolge: A und B (klein, sicher), dann C, D, E (E ist der größte Teil). Am Ende F.

## Regeln für die Umsetzung

- Bauen nur mit der Zeile aus `../CLAUDE.md` (bash, JDK 25, TEMP). Nie bauen oder Quellen ändern, während ein
  Selbsttest läuft. `./gradlew runServer -PselfTest -q > selftest.out 2>&1`, Ergebnis in
  `run/greektrees-selftest/`, Render mit `cd concept && python render_selftest.py <art>`.
- Formtests würfeln mit EINER `RandomSource` für alle Würfe (`RandomSource.create(0..n)` liefert ähnliche
  Anfänge).
- Kein Wuchs darf wie der andere aussehen. Vor dem Zeigen 6+ Wüchse je Art im Render auf Gleichförmigkeit
  prüfen. Jeden Würfel behalten, der nicht ausdrücklich gestrichen wird.
- Nur ändern, was verlangt ist: Weidenkrone, Vorhang der kleinen Weide, Palmenstamm, Stern-plus-Schopf-Form
  der Palmenkrone bleiben, wie sie sind.
- Nicht committen, nicht veröffentlichen. Version auf `0.17.0+26.2` (`gradle.properties`). Texte im Code Englisch.
- Am Ende Jar-Pfad nennen und die Render-Blätter zeigen; Testergebnisse so berichten, wie sie sind.

## A. Setzlings-Artefakte bei der 2×2-Palme (Bug)

**Ursache (im Bytecode von `TreeGrower.growTree` nachgesehen):** Im 2×2-Zweig setzt Vanilla die vier Setzlinge
mit Flag 260 (`UPDATE_NONE`) auf Luft, ruft `place` und kehrt zurück. Die Clients erfahren davon nichts. Bei
Vanilla fällt das nicht auf, weil der 2×2-Stamm alle vier Felder überschreibt. Der Einzelbaum-Zweig ruft
dagegen `sendBlockUpdated`, wenn das Feld frei bleibt. Unsere große Palme hat nur einen Stammblock auf der Ecke:
drei Felder sind auf dem Server Luft, der Client zeigt weiter Setzlinge (Geisterblöcke). Knochenmehl löst eine
Server-Antwort aus, die das Feld korrigiert. Die große Weide ist nicht betroffen (2×2-Stamm).

**Fix:** einmal in `GreekSaplingBlock`, durch das alle unsere Setzlinge laufen:

```java
@Override
public void advanceTree(ServerLevel level, BlockPos pos, BlockState state, RandomSource random) {
    super.advanceTree(level, pos, state, random);
    // Vanilla clears the four saplings of a 2x2 tree without telling the clients, because its 2x2 trunks cover
    // all four. Ours may not (the palm clump has one trunk on the corner), so the square is sent again.
    for (BlockPos p : BlockPos.betweenClosed(pos.offset(-1, 0, -1), pos.offset(1, 0, 1))) {
        BlockState now = level.getBlockState(p);
        if (!now.is(this)) {
            level.sendBlockUpdated(p.immutable(), state, now, Block.UPDATE_CLIENTS);
        }
    }
}
```

`AriesOakSaplingBlock` überschreibt `advanceTree` selbst und hat dieselbe Lücke nur theoretisch (der Stamm deckt
das 4×4). Dort nichts bauen; im Selbsttest einmal zählen, ob nach dem Wachsen ein Luftblock im 4×4 auf y 0
bleibt. Nur wenn ja, dieselbe Schleife über das 4×4 ergänzen.

**Prüfung:** Der Fehler liegt in der Client-Synchronisation, der Server-Selbsttest sieht ihn nicht. Im
Selbsttest (`squareGrowth`) nur festhalten: nach dem Wachsen der großen Palme steht im Quadrat kein Setzling
mehr. Die Abnahme macht der Nutzer in Prism (2×2-Palme mit Knochenmehl ziehen, es darf kein Setzling stehen
bleiben). Das im Bericht genau so sagen.

## B. Datteln nur direkt unter dem Laub

`TreeShapes.addDates`: die zweite Schleife (`dateCluster(t, top.below(), s, r)`) entfällt. Rispen hängen nur
noch an den Seiten des obersten Stammblocks; darüber liegt der Blattring der Krone (`palmCrown` setzt auf Höhe
`c` vier Blätter in den Himmelsrichtungen, die bleiben in C zwingend erhalten). Anzahl wie bisher: höchster
Stamm 3–4, jeder weitere 2–3.

- Selbsttest: die Prüfung „clusters right under another" ersetzen durch „Rispen ohne Palmenlaub direkt
  darüber = 0" (über alle gewachsenen und gewürfelten Palmen).
- Doku: `VARIATIONEN.md` Zeile „Datteln" (beide Palmentabellen), Javadoc von `addDates`.

## C. Palmenkrone: mehr Zufall

Heute ist `palmCrown` vierfach drehsymmetrisch: acht Wedel exakt auf 0°/45°/90°…, alle Achsenwedel gleich
lang, alle Diagonalwedel gleich, vier steile Wedel exakt auf 22,5° + k·90°, alle mit demselben Profil; gewürfelt
wird nur, ob die Spitze der Achsenwedel 1 oder 2 Blöcke hängt. Das Bild (Stern aus acht feinen Wedeln, darüber
ein Schopf steiler Wedel, Größen 0–2) hat der Nutzer ausgesucht und bleibt. Jeder Wedel bekommt eigene Würfel:

| Merkmal | heute | neu (je Wedel gewürfelt) |
|---|---|---|
| Richtung der 8 Sternwedel | exakt k·45° | k·45° ± 10° |
| Länge Achsenwedel | `5 - size` | `5 - size` + (−1, 0, 0, +1), mindestens 2 |
| Länge Diagonalwedel | fest | ± 1 Block entlang des Wedels |
| Bogen | steigt 1, kippt bei 0,6·Länge | steigt 1 oder 2; kippt bei 0,5–0,75·Länge |
| hängende Spitze | Achse 1–2, Diagonale fest 1 | Achse 0–3, Diagonale 0–2 |
| fehlender oder kurzer Wedel | nie | je Krone höchstens einer (Größe 0: höchstens zwei, nie benachbart), 25 % der Kronen; statt des Wedels ein Stummel von 2 Blöcken oder nichts |
| Schopf | 4 Wedel auf 22,5° + k·90°, ein Profil | 3–5 Wedel, Startwinkel frei, Abstand 360°/n ± 15°, Profil je Wedel aus den vorhandenen ± 1 Block Höhe/Länge |
| Kronenspitze | Blatt auf c+1 und c+2 | c+1 immer, c+2 zu 70 %, c+3 zu 15 % |

Fest bleiben: Kernblock auf `c`, die vier Blätter in den Himmelsrichtungen auf `c` (darunter hängen die
Datteln), Größenstufen 0–2, dauerhaftes Laub, alle Stamm- und Abstandsregeln (`sideBySide`, `crownsTouch`,
`tooClose`). Die Krone darf höchstens einen Block weiter reichen als heute.

`frond()` zeichnet schon beliebige Winkel als lückenlose Linie; es braucht nur andere Profile und Winkel.

**Prüfung:**
- Selbsttest neu: 200 Kronen je Größe würfeln (eine `RandomSource`), Blattmenge relativ zum Kernblock
  vergleichen: mindestens 150 verschiedene; keine Krone ist unter 90°-Drehung mit sich selbst deckungsgleich;
  jedes Blatt hängt (über Flächen, Kanten oder Ecken) mit dem Kern zusammen.
- Bestehende Palmenprüfungen (`palmClumps`, `smallPalms`, `squareGrowth`) müssen weiter bestehen.
- Render `selftest_date_palm.png` und `selftest_large_date_palm.png` (vorher die alten
  `run/greektrees-selftest/*date_palm*.json` löschen): Kronen nebeneinander ansehen. Sehen zwei gleich aus
  oder zerfällt das Sternbild, nachstellen.

## D. Große Weide: mehr einzelne Stränge

Vom Nutzer klargestellt: **nur am Rand** sollen weitere Stränge dazukommen. Das Mittelfeld unter der Krone
bleibt, wie es ist. Jeder Strang steht weiter für sich (Regel aus 0.15.0: nie ein Strang neben einem anderen,
auch nicht diagonal; `Shape.strands` bleibt).

Warum am Rand heute Stränge fehlen: `willowCrown` nennt eine Spalte „Rand", wenn sie höchstens 1,6 Blöcke
innerhalb des größten Abstands zur Mitte liegt (`d >= rim - 1.6`). Der Umriss der großen Krone ist aber kein
Kreis: die Astspitzen mit ihren Laubballen ragen heraus, dazwischen springt der Umriss zurück. Diese
zurückspringenden Kanten gelten als Mittelfeld (35 %, kurze Stränge), und von den echten Randspalten wird nur
70 % versucht.

Nur für `big` (die kleine Weide bleibt unverändert):

- Rand = jede Spalte am Umriss des Laubs von oben gesehen (mindestens eine der vier Nachbarspalten hat kein
  Laub), dazu wie bisher die Spalten im äußeren Ring.
- Alle Randspalten werden versucht (100 % statt 70 %); die Abstandsregel dünnt von selbst aus.
- Länge der Randstränge wie heute (80 % bis 1–2 über dem Boden, der Rest kürzer).
- Mittelfeld: Werte unverändert.

**Prüfung:** In `willowShapes` die mittlere Zahl der Randstränge je großer Weide ausgeben, einmal vor und einmal
nach der Änderung messen. Ziel: mindestens das 1,5-Fache; die Zahl der Mittelfeld-Stränge bleibt etwa gleich;
„strand ends side by side" bleibt 0. Render `selftest_large_weeping_willow.png` vorher/nachher nebeneinander
zeigen.

## E. Weidenstamm: organische Übergänge

### E.1 Messung der Umbauten des Nutzers

`concept/extract_willow_trunks.py` liest die sechs umgebauten Stämme aus der Prism-Welt „New World" und schreibt
`concept/reference/willow_trunk_{small_1..3,big_1..3}.json` (Format der Selbsttest-Dumps, Fuß bei 0, 0, 0).
Erneut ausführen, falls der Nutzer weitere Stämme umbaut (Fußpositionen in `TREES` ergänzen).

Kleine Weide, 1×1. A = Fußsäule, B = Nachbar von A, C = Nachbar von B. `A+B` heißt: beide Blöcke in der Schicht.

| Schicht | small_1 (th 5) | small_2 (th 9) | small_3 (th 9) |
|---|---|---|---|
| y0 | A + Wurzeln | A + Wurzeln | A + Wurzeln |
| y1 | A | A | A |
| y2 | A+B | A+B | A+B |
| y3 | B | B+C | B |
| y4 | A+B | C | B + Knorren |
| y5 | A | C | B + Knorren |
| y6 | (Krone) | B+C | B |
| y7 | | A+B | A+B |
| y8 | | A | A |
| y9 | | A | A |

- small_1: Bogen entlang einer Achse. small_2: Diagonalbogen (C liegt quer zu A→B), derselbe Weg zurück.
  small_3: Achsbogen mit einem Knorren, einem 2 Blöcke hohen Holzstück seitlich an der Mitte der Bauchsäule
  (quer zur Bogenrichtung).
- Zwei aufeinanderfolgende Säulen teilen genau eine Schicht (Fläche an Fläche). Das macht der heutige Code
  auch („Knie"). **Der Unterschied liegt darin, wo die Versätze sitzen:**
  - Heute Diagonalbogen: Versätze bei 2, 4, th−3, th−1, bei th 9 also 2/4/6/8: jede Säule 3 hoch, ein
    gleichmäßiges Zickzack. Beim Nutzer 2/3/6/7: die Zwischensäule B ist nur 2 hoch (beide Schichten geteilt),
    die Bauchsäule C ist lang. Die Versätze drängen sich am Fuß und unter der Krone, dazwischen steht der Stamm
    ruhig: ein Bogen statt einer Treppe.
  - Heute Achsbogen (Sinus über die ganze Stammhöhe): Rückkehr meist erst in der obersten Stammschicht th,
    das Knie ragt direkt unter der Krone neben dem Stamm hoch. Beim Nutzer kommt der Stamm eine oder zwei Schichten früher zurück (small_1 bei
    th−1, small_3 bei th−2); unter der Krone stehen 2–3 Blöcke der Fußsäule.

Große Weide, 2×2 (x nach rechts, z nach unten, `#` = Holz; y0 mit Wurzelansatz weggelassen):

```
big_1 (th 11): Achsbogen, 1 Block hinaus
y1-2   y3     y4-6   y7     y8-11
##     ##     ..     ##     ##
##     ##     ##     ##     ##
..     .#     ##     ##     ..

big_2 (th 10): hinaus über zwei Achsschritte, zurück in einem Diagonalschritt
y1    y2    y3    y4    y5    y6    y7    y8    y9-10
##.   .##   .##   ..#   ...   ...   .#.   ##.   ##.
##.   ###   .##   .##   .##   ###   ###   ###   ##.
...   ...   .#.   .##   .##   .##   .##   .#.   ...

big_3 (th 9): Diagonalschritt ohne Rückkehr, zwei Wurzeln 2 hoch (y1)
y1     y2     y3     y4     y5     y6-9
.##.   .##.   .##.   .#..   ....   ....
.###   .##.   ###.   ###.   ###.   ##..
.#..   ....   .#..   .#..   ##..   ##..
```

- Heute springt die ganze 2×2-Schicht auf einmal. Beim Nutzer wandern die vier Säulen des Stamms nicht in
  derselben Schicht: einzelne Blöcke gehen eine Schicht voraus oder bleiben eine Schicht länger stehen. Die
  Übergangsschichten haben 5–6 Blöcke.
- Achsschritt von Quadrat S nach S′ in Schicht L (S′ gilt ab L). Vorkommende Formen:
  (a) Vorläufer: einer der zwei neuen Blöcke steht schon in L−1 (big_1 y3, big_2 y3);
  (b) Nachzügler: einer der zwei alten Blöcke bleibt in L stehen (big_2 y2, y4);
  (c) beides, schräg gegenüber (big_2 y3/y4);
  (d) eine volle Übergangsschicht 2×3 (big_1 y7).
- Diagonalschritt (S und S′ teilen einen Block): über drei Schichten. big_2 y6–8: S + ein neuer Block, dann
  zweimal „beide Quadrate ohne eine äußerste Ecke" (6 Blöcke, erst fehlt die neue, dann die alte Ecke).
  big_3 y3–5: S + zwei neue Blöcke, dann ein Plus aus fünf Blöcken um den gemeinsamen Block, dann S′ + ein
  alter Block.
- Auslenkung nie mehr als ein Block je Achse, auch bei hohen Stämmen (heute bis zwei bei th ≥ 9).
- Fuß y0–1 und die obersten zwei Stammschichten sind ein glattes 2×2.
- big_3 kehrt nicht über den Fuß zurück und trägt Wurzeln, die zwei Blöcke hoch sind.

### E.2 Leitbild nach der Antwort des Nutzers

Die Messung zeigt, **wie** ein Versatz gebaut wird. **Wie viele** Versätze ein Stamm hat, regelt die Antwort
des Nutzers: Der Stamm darf kein Labyrinth sein. Er hat eine schöne, subtile Biegung, manchmal eine C-Form.

- **Übergang** = eine Stelle, an der der Stamm um einen Block weiterrückt: ein Achsschritt, oder ein
  Diagonalschritt aus zwei Achsschritten in direkt aufeinanderfolgenden Schichten (klein: wie small_2 y2/y3;
  groß: die Dreischicht-Formen). Ein Übergang liest sich als eine Bewegung.
- **Biegung** (der Normalfall, etwa zwei Drittel): ein einziger Übergang. Der Stamm rückt einmal zur Seite
  (Achse oder diagonal) und bleibt dort; die Krone sitzt über dem versetzten Stammende (wie big_3). Bei hohen
  Stämmen der kleinen Weide (th ≥ 8) in etwa 30 % der Fälle ein zweiter Übergang weiter oben **in dieselbe Richtung**, mit
  mindestens 3 ruhigen Schichten dazwischen (eine gleichmäßige Neigung).
- **C-Form** (etwa ein Drittel): zwei Übergänge, hinaus und denselben Weg zurück, dazwischen eine lange ruhige
  Bauchsäule (small_1, small_3, big_1; diagonal wie small_2 und big_2 nur selten und nur ab th 8).
- Nie mehr als zwei Übergänge je Stamm. Nie ein Richtungswechsel außer der einen Rückkehr der C-Form. Die
  heutige Form „Diagonalbogen mit vier gleichmäßig verteilten Schritten" entfällt: das ist das Labyrinth.
- Alles variiert: Form, Richtung (vier Achsen, vier Diagonalen), Höhe des Übergangs (am Fuß, in der Mitte, oben),
  Länge der Bauchsäule, weiche Form je Schritt, Knorren, Wurzeln. „Nie gerade" bleibt.

### E.3 Umsetzung in `TreeShapes`

`willowTrunk` gibt neben th zurück, wo das Stammende steht (Versatz dx, dz gegenüber dem Fuß). `willowCrown`
und `willowVines` setzen Leittrieb, Kuppel, Äste, Vorhang und Ranken über dieses Stammende statt über 0, 0
(heute `cx = cz = (size - 1) / 2` und Leittrieb-Blöcke bei `ox, oz`; beides um dx, dz verschieben). Stammhöhen
und Wurzelansatz bleiben.

**Klein (1×1).** Das Gerüst `at[y]` + Knie kann bleiben (zwei Säulen teilen genau eine Schicht):

- Biegung: `A,B` (Achse) oder `A,B,C` mit C quer zu A→B und B nur 2 Schichten hoch (diagonal). Übergang
  zwischen y2 und th−1 gewürfelt; bei th 4 ab y1. Zweiter Übergang in dieselbe Richtung nur wie in E.2.
- C-Form: `A,B,A`, selten (ab th 8) `A,B,C,B,A` kompakt wie small_2. Erster Versatz bei 2 (ab th 7 auch 3),
  Rückkehr auf A bei th−1 oder th−2, nie bei th. Die Bauchsäule ist die längste Säule außer A.
- Knorren: bei etwa einem Viertel der Stämme mit einer ruhigen Säule von mindestens 3 eigenen Schichten: 1–2
  Blöcke hoch, an einer freien Seite, in deren mittlerem Drittel.
- Selbstkontrolle der Regeln: small_1, small_2 und small_3 müssen mögliche Ergebnisse sein.

**Groß (2×2).**

- Biegung: ein weicher Achsschritt oder ein weicher Diagonalschritt (big_3 ist genau das), Lage gewürfelt.
- C-Form: hinaus und zurück, je ein weicher Schritt (big_1); selten diagonal (hinaus über zwei Achsschritte
  oder einen Diagonalschritt, zurück ebenso, wie big_2).
- Höchstens ein Block je Achse.
- Jeder Schritt wird weich gebaut, die Form je Schritt gewürfelt: Achsschritt (a)–(d), Diagonalschritt eine
  der beiden gemessenen Dreischicht-Formen. Ein harter Sprung des ganzen Quadrats kommt nicht mehr vor.
- Fuß y0–1 bleibt ein glattes 2×2, ebenso die oberste Stammschicht.
- Wurzeln: Ansatz wie bisher; bei 0–2 Wurzelblöcken ein zweiter Block darauf (y1).

### E.4 Prüfung

- `willowShapes` erweitern (300 kleine, 100 große Würfe, eine `RandomSource`):
  - gerade Stämme 0 (bleibt; die Prüfung liest heute die Fußsäule bis zur Kronenspitze und passt weiter);
  - jeder Stammblock hat einen Flächennachbarn aus Holz;
  - kein Labyrinth: höchstens zwei Übergänge je Stamm, höchstens ein Richtungswechsel (die Rückkehr der
    C-Form); Anteil Biegung 55–75 %, C-Form 25–45 % (ausgeben);
  - klein: jede Stammschicht ab y1 1–3 Blöcke;
  - groß: jede Stammschicht ab y1 4–6 Blöcke; zwei Schichten übereinander teilen mindestens 3 Blöcke (kein harter
    Sprung); kein Block mehr als einen Block neben dem Fußquadrat;
  - die Krone sitzt über dem Stammende: der Leittrieb steht auf der obersten Stammschicht;
  - Vielfalt: Zahl verschiedener Stämme ausgeben, mindestens 40 von 300 klein und 60 von 100 groß; keine Form
    über 15 %.
- Neu: 20 000 kleine Weiden würfeln; small_1, small_2 und small_3 müssen (bis auf Drehung und Spiegelung,
  Stammschichten 1 bis th) je mindestens einmal vorkommen.
- Blatt `concept/willow_trunks.png` (neuer Modus in `render_selftest.py`, die Stamm-allein-Darstellung aus
  `draft_sheet`, Zweig `TRUNK`, dafür herauslösen): oben die sechs Referenzen, darunter 9 gewürfelte kleine
  und 9 große Stämme; jeder Stamm allein, groß, Iso und zwei Seitenansichten. Die gewürfelten müssen neben den
  Referenzen wie von derselben Hand aussehen und untereinander verschieden sein. Selbst prüfen, bevor es der
  Nutzer sieht: Liest sich ein Stamm als Hin und Her, ist er falsch, auch wenn die Zählprüfung besteht. Dieses
  Blatt dem Nutzer zeigen.
- `squareGrowth` und die übrigen Weidenprüfungen bestehen weiter (wo sie den 2×2-Stamm an festen Feldern über
  dem Fuß erwarten, an das versetzte Stammende anpassen).

## F. Abschluss

1. Version `0.17.0+26.2`, Build, voller Selbsttest: alle Prüfungen bestanden, sonst die fehlgeschlagene nennen.
2. Render neu: `selftest_weeping_willow.png`, `selftest_large_weeping_willow.png`, `selftest_date_palm.png`,
   `selftest_large_date_palm.png`, `willow_trunks.png`.
3. Doku: `README.md` (Zeilen Date Palm und Weeping Willow), `VARIATIONEN.md` (Palmenkrone, Datteln,
   Weidenstamm, Stränge der großen Weide), Javadoc in `TreeShapes`; in `PLAN-PALME-WEIDE.md` die Rundentabelle
   um diese Runde ergänzen.
4. Dem Nutzer melden: Jar `greek-trees/build/libs/greektrees-0.17.0+26.2.jar`, die Blätter, die Zahlen
   (Randstränge vorher/nachher, Anteil Biegung/C-Form, Vielfalt), dazu offen: Setzlings-Bug nur in Prism
   prüfbar. Kein Commit ohne Auftrag.
