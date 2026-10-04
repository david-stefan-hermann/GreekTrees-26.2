# Plan: Dattelpalme und Trauerweiden überarbeiten (Stand 2026-10-03, Mod 0.15.0)

Ziel: die Wuchsformen von Dattelpalme (ein Setzling und 2×2) und Trauerweide (ein Setzling und 2×2) in mehreren
Runden verbessern. Jede Runde zeigt Varianten nebeneinander, du wählst (Buchstabe, Mischung oder „keine“), erst
danach wird weitergebaut. In den Mod kommt nur, was du ausgesucht hast.

Grundlage: `TreeShapes.datePalm / largeDatePalm / palmCrown / palmTrunkPath` und `TreeShapes.willow`, dazu die
Render `concept/selftest_date_palm.png`, `selftest_large_date_palm.png`, `selftest_weeping_willow.png`,
`selftest_large_weeping_willow.png`.

## 1. Befund

### Dattelpalme (beide Größen)

1. **Die Krone ist ein Deckel, kein Wedelschopf.** `palmCrown` baut immer dasselbe: vier Wedel genau in den
   Himmelsrichtungen, dazwischen je fünf Füllblätter. Das ergibt eine geschlossene 9×9-Kappe, drei Blöcke hoch.
   Von der Seite liest sie sich wie eine Akazie oder ein Pilz. Lücken zwischen Wedeln gibt es nicht.
2. **Alle Kronen sind gleich.** Gewürfelt wird nur, welche der vier Wedelspitzen hängt, und das gilt für alle
   Stämme eines Baums gemeinsam. Länge, Bogen und Richtung der Wedel sind fest.
3. **Die Krone passt nicht zur Stammhöhe.** Ein Nebenstamm von 4–5 Blöcken trägt dieselbe 9 Blöcke breite Krone
   wie ein Stamm von 23. Bei der kleinen Palme verschmelzen die Kronen zu einem Klumpen (Wuchs 4 und 8), bei
   der großen sitzen kleine Puschel auf langen Stangen.
4. **Der Bogen knickt unter der Krone.** Seit 0.15.0 werden die geraden Stücke nach oben kürzer (oben 1–2
   Blöcke je Versatz). Bei 4–5 Versätzen entsteht oben eine 45°-Treppe, unten steht der Stamm kerzengerade
   (große Palme, Wuchs 4). Bei kurzen Stämmen (4–7 hoch, 2–3 Versätze) ist der ganze Stamm eine Treppe.
5. **Viele Stämme stehen wie Orgelpfeifen.** Bei vier und fünf Stämmen laufen die unteren 8–10 Blöcke parallel
   im Abstand von einem Block.
6. **Am Fuß passiert nichts.** Die Kretische Dattelpalme bildet in der Natur Horste mit Jungpflanzen am Fuß;
   bei uns steht der Stamm nackt im Gras.

Hinweis zum Render: `large_date_palm_6…11.json` stammen noch vom 2026-10-02 (der Selbsttest lässt die große
Palme nur sechsmal wachsen, die alten Dateien blieben liegen). Wuchs 7, 10 und 11 im Blatt zeigen also die
Form vor 0.15.0. Wird in Schritt 0 behoben.

### Trauerweide (beide Größen)

1. **Die Krone ist eine Halbkugel.** Ein geschlossener Ellipsoid plus Äste, die ringsum zu 85 % in Laub
   gehüllt werden. Von außen ist das ein glatter Helm; Äste sieht man nicht.
2. **Der Vorhang wirkt wie Gitterstäbe.** Einzelne Strähnen, eine je Spalte, nie eine neben der anderen, und
   80 % der Randsträhnen enden auf derselben Höhe (1–2 über dem Boden). Das Ergebnis ist ein Käfig mit
   gleichmäßigen Stäben und gerader Unterkante. (Die einzelnen Strähnen waren dein Wunsch in 0.15.0; das
   Problem ist die Gleichförmigkeit, deshalb bleibt „einzeln“ eine der Varianten.)
3. **Der Umriss ist ein Zylinder mit Kuppel.** Eine Trauerweide ist unten am breitesten, mit Stufen und
   Lücken zwischen den Laubkaskaden. Bei uns fällt alles am selben Radius senkrecht.
4. **Alle Weiden sehen gleich aus.** Der Größenwurf ändert Maße, nicht die Form. Auch die große Weide ist
   dieselbe Form mit 2×2-Stamm; im Blatt sind kleine (Wuchs 2, 6) und große kaum zu unterscheiden.
5. **Der Stamm trägt die Krone nicht.** 1×1, drei bis zehn Blöcke, darüber eine Kuppel von 10–14 Blöcken
   Breite. Die Knie am Versatz machen den dünnen Stamm zackig. Eine sichtbare Gabelung fehlt.

## 2. Was fest bleibt

Frühere Entscheidungen, die keine Variante anfasst (außer du willst es):

- Nur Vanilla-Blöcke; Holz immer `*_wood` (keine Jahresringe).
- Palme: `jungle_wood` + `jungle_leaves`, Stamm einen Block dick, nie zwei Stammblöcke nebeneinander,
  Versatz nur entlang einer Achse. Dattelrispen an den Seiten des obersten Stammblocks (brauchen Tropenholz
  dahinter), eine zweite Reihe einen Block tiefer.
- Weide: `pale_oak_wood` + `mangrove_leaves`, Stamm nie gerade, Versatz Fläche an Fläche, große Weide 2×2,
  Laub dauerhaft, Ranken außen.
- 2×2-Setzlinge geben die große Form.

Eine Folge für die Palme: Mit Vanilla-Laubzerfall (höchstens 6 Schritte vom Holz) ist die heutige Krone schon
am Limit (Radius 4). **Jede größere Krone braucht dauerhaftes Laub** wie bei der Weide; beim Fällen bleibt
es dann hängen und muss abgebaut werden. Die Runden zeigen deshalb beide Fälle getrennt: Varianten innerhalb
von Radius 4 und Varianten mit dauerhaftem Laub.

## 3. Ablauf der Runden

### Schritt 0: Werkzeug (erledigt 2026-10-03)

- `greektrees/tree/Drafts.java`: die Varianten als eigene Methoden neben dem jetzigen Code. In `TreeShapes`
  wurden dafür nur Hilfsfunktionen herausgelöst (`willowTrunk`, `willowVines`, Größe `g` als Parameter) und
  die Palmen-Helfer sichtbar gemacht; die Bäume im Spiel wachsen wie vorher (Selbsttest: alle Prüfungen
  bestanden). Nach der letzten Runde wandert der Sieger nach `TreeShapes`, `Drafts.java` wird gelöscht.
- `./drafts.sh p1 w1` = `./gradlew runServer -Pdrafts=p1,w1` + Render. Der Lauf würfelt nur Formen, schreibt
  `run/greektrees-drafts/draft_<runde>_<variante>_<n>.json` und beendet sich, bevor eine Welt lädt (wenige
  Sekunden). Je Variante drei Wüchse mit denselben drei Seeds, damit sich nur das Merkmal der Runde ändert.
- `concept/render_selftest.py drafts <runde>` schreibt `concept/drafts_<runde>.png`: eine Zeile je Variante
  (Buchstabe, Name, was anders ist), drei Wüchse in Iso- und Seitenansicht mit Steve als Maßstab, die
  jetzige Form als Zeile „0“. Die Texte der Zeilen stehen in `DRAFTS` in dieser Datei.
- Der Selbsttest leert seinen Ausgabeordner jetzt vor dem Lauf (die alten Palmen-Dateien sind weg).

### Regeln je Runde

- Eine Runde ändert **ein** Merkmal; alles andere bleibt auf dem zuletzt gewählten Stand.
- Vier bis fünf Varianten, die sich deutlich unterscheiden. Du antwortest mit Buchstabe, Mischung („A mit
  dem Rand von C“) oder „keine, weil …“; im letzten Fall gibt es dieselbe Runde noch einmal mit neuen Varianten.
- Palme und Weide laufen parallel: je Runde ein Blatt Palme, ein Blatt Weide.
- Die Blätter sind Render der echten Blockdaten. Vor der Schlussentscheidung kommen die Finalisten in den
  Dev-Client (Schritt 4), weil Laub im Spiel anders wirkt als im Render.

## Stand der Runden

| Runde | Blatt | Ergebnis |
| --- | --- | --- |
| P1 Krone | `concept/drafts_p1.png` | 2026-10-03: Stern (A) und Federball (B) gefallen; C, D, E gestrichen |
| W1 Umriss | `concept/drafts_w1.png` | 2026-10-03: die jetzige Halbkugel bleibt; es stört die Stammgeneration |
| P2 Stern und Federball | `concept/drafts_p2.png` | 2026-10-03: **AB**, Stern mit Schopf (Stern aus acht Wedeln, darüber vier steile) |
| P3 Stamm | `concept/drafts_p3.png` | 2026-10-03: **E**, gleichmäßig schräg, aber nur in **eine** Richtung: alle Versätze entlang derselben Achse, kein Winden |
| W3 Stamm | `concept/drafts_w3.png` | 2026-10-03: „alles schlecht“ (0, A–E); was genau stört, ist noch nicht gesagt |
| P4 ein bis drei Stämme | `concept/drafts_p4.png` | 2026-10-03: **B**, gestufte Kronen; dazu: Stämme nie nebeneinander, Füße immer diagonal aneinander („direktional“ als „diagonal“ gelesen) |
| W4 Stamm und Geäst | `concept/drafts_w4.png` | 2026-10-03: nicht gewählt. Das Problem ist „die Art und Weise, wie die Krümmung umgesetzt ist“; Geäst bleibt wie jetzt |
| P5 kleine Palme, Stand | `concept/drafts_p5.png` | wartet: Bestätigung; V (dritter Stamm an der Ecke daneben) oder L (gegenüber) oder beides gewürfelt |
| P6 große Palme | `concept/drafts_p6.png` | wartet: 0 jetzt, A volle Kronen, B gestufte Kronen, C gestuft und gestaffelt (Hauptstamm höher, andere stärker geneigt) |
| W5 Krümmung des Stamms | `concept/drafts_w5.png` | 2026-10-03: **D**, Bogen hinaus und zurück mit Knie; dazu soll es eine diagonale Variante geben („d ist gut“ als Weide D gelesen, P6 hat kein D) |
| W6 Bogen diagonal | `concept/drafts_w6.png` | 2026-10-03: klein **D**, „aber auch diagonal, beides möglich, aber nicht gleichzeitig“ → je Baum Achse oder diagonal (50/50), diagonal in Einzelschritten (G), nie beide Achsen in einer Schicht |
| W7 große Weide | `concept/drafts_w7.png` | 2026-10-03: groß **A**, ebenso auch diagonal; diagonal wie bei der kleinen in Einzelschritten (so noch auf keinem Blatt gezeigt, B sprang über Eck) |
| 0.17.0 nach Prism-Test von 0.16.2 | `PLAN-0.17.md`, `concept/willow_trunks.png` | 2026-10-03: Weidenstamm nach sechs von Hand umgebauten Stämmen (`concept/reference/`): Biegung (meist ein Versatz, bleibt draußen) oder C, nie Labyrinth, große Weide mit weichen Übergängen; große Weide mit mehr Strängen am Rand; Palmenkrone mit Zufall je Wedel; Datteln nur direkt unter dem Laub; Setzlings-Geister der 2×2-Palme behoben (nur in Prism prüfbar). Rückmeldung zum Blatt: kleine Weide ohne diagonale Biegung (Wurf 6 „genau das, was ich vermeiden möchte“), großes C nie als bloß verschobenes Stück (Wurf 3); kleine Palme: Füße im 2×2, zwei diagonal, drei als L; Palmen ein Versatz mehr |

**Eingebaut in 0.16.0 (2026-10-03):** Palme (Krone, Stamm, Füße, gestufte Kronen) und Weide (Bogen) stehen in
`TreeShapes`; Selbsttest „all checks passed“, neu darin `date palm shapes` (Stämme nie nebeneinander, einzelner
Stamm nur in eine Richtung, dauerhaftes Dschungellaub). Wüchse aus der Testwelt: `concept/selftest_date_palm.png`,
`selftest_large_date_palm.png`, `selftest_weeping_willow.png`, `selftest_large_weeping_willow.png`.

**0.16.1 (2026-10-03):** In 0.16.0 wuchs jede Palme als dieselbe Gerade (fester Versatz alle drei Blöcke); das
war nicht gewollt. Jetzt würfelt jeder Stamm Zahl und Lage der Versätze (oben gebogen, am Fuß gebogen oder
durchgehend schräg, dazu ±1 Block je Versatz), weiterhin nur in eine Richtung. Selbsttest bestanden.

Von mir gesetzt, weil P5 und P6 unbeantwortet blieben (bitte bestätigen oder ändern):
- kleine Palme: dritter Stamm je zur Hälfte V und Linie;
- große Palme: B (gestufte Kronen), wie bei der kleinen gewählt.

Offen: Test in Prism, Dev-Client-Screenshots; Vorhang der Weide (W2) nur, wenn gewünscht. `Drafts.java` ist
bis zur Abnahme ein leerer Rumpf, das Werkzeug (`drafts.sh`, Draft-Modus, Render) bleibt so lange stehen. Die Abschnitte unten sind der ursprüngliche Plan; wo die Tabelle oben abweicht, gilt die Tabelle.
`Drafts.java` enthält jeweils nur die laufenden Runden.

## 4. Runden Dattelpalme

### Runde P1: Krone (der größte Hebel) — Blatt `concept/drafts_p1.png`, wartet auf deine Wahl

Gezeigt an einem einzelnen Stamm von 10 Blöcken. Ein erster Versuch innerhalb des Zerfallslimits (Radius 4)
war von der jetzigen Krone kaum zu unterscheiden; da dauerhaftes Laub in Ordnung ist, nutzen alle neuen
Varianten es. „Fein“ heißt: die Blätter eines Wedels berühren sich an Schrägen nur über Kanten, wie bei
gebauten Palmen. Der Rock aus alten Wedeln war bei dieser Größe nicht zu sehen und ist gestrichen.

| | Name | Was sich ändert |
| --- | --- | --- |
| 0 | jetzt | 9×9-Kappe (zerfällt normal) |
| A | Stern | flacher Stern aus acht feinen Wedeln: lange entlang der Achsen (5), kürzere diagonal, nichts dazwischen |
| B | Federball | hohe, runde Krone aus 16 feinen Wedeln: oben steil aufwärts, in der Mitte waagrecht, unten hängend; zufällig gedreht. Kommt der Kretischen Dattelpalme am nächsten |
| C | Windschief | sieben bis neun feine Wedel in beliebige Richtungen; zur Neigung des Stamms hin hängen sie, auf der anderen Seite steigen sie |
| D | Groß, kräftig | zwei Kränze langer Wedel (5–7 Blöcke) mit hängenden Spitzen, lückenlos gebaut |
| E | Groß, fein | wie D mit feinen Wedeln |

### Runde P2: Kronengröße je Stamm

Mit der Krone aus P1, gezeigt an der kleinen Palme mit drei Stämmen und der großen mit vier.

- A: alle Kronen gleich (wie jetzt).
- B: Krone wächst mit der Stammhöhe; Nebenstämme von 4–5 Blöcken tragen einen kleinen Schopf (Radius 2).
- C: wie B, dazu größere Höhenabstände zwischen den Stämmen, damit keine Krone in der anderen steckt.
- D: wie C, die große Palme mit dauerhaften großen Kronen auf den zwei höchsten Stämmen.

### Runde P3: Stamm

- A: Bogen wie jetzt (oben am stärksten gekrümmt).
- B: derselbe Bogen, entschärft: oben mindestens zwei gerade Blöcke je Versatz, Zahl der Versätze nach
  Stammhöhe (kurze Stämme 0–1). Keine Treppe mehr.
- C: Bogen am Fuß: der Stamm verlässt den Boden schräg und richtet sich nach oben auf (so wachsen schiefe
  Palmen in der Natur).
- D: sanftes S: unten in eine Richtung, oben leicht zurück.
- E: Mischung je Baum gewürfelt (B, C oder D), damit ein Hain nicht einheitlich aussieht.

### Runde P4: Horst (vor allem die große Palme)

- A: wie jetzt.
- B: Fächer: Nebenstämme neigen sich schon ab dem Boden nach außen, keine parallelen Stangen.
- C: gestaffelt: ein hoher Hauptstamm, die anderen 50–75 % so hoch; höchstens vier Stämme.
- D: wie B oder C, dazu ein bis drei Jungpalmen am Fuß (ein Holzblock mit Mini-Schopf oder nur ein Büschel
  Laub am Boden).

## 5. Runden Trauerweide

### Runde W1: Umriss der Krone — Blatt `concept/drafts_w1.png`, wartet auf deine Wahl

Gezeigt an der Weide aus einem Setzling, mittlere Größe. Vorhang nach der jetzigen Regel, verallgemeinert auf
beliebige Umrisse: Strähnen hängen an den Spalten am äußeren Rand des Laubs, nicht mehr an einem festen Radius.

| | Name | Was sich ändert |
| --- | --- | --- |
| 0 | jetzt | Halbkugel |
| A | Kissen | statt einer Kuppel ein Laubkissen auf dem Leittrieb und drei bis fünf auf den Astenden, auf verschiedenen Höhen. Strähnen fallen vom Rand jedes Kissens: Stufen, dazwischen Himmel und sichtbare Äste |
| B | Fontäne | Äste steigen steil aus dem Stamm, laufen sichtbar über einen Bogen und kommen weit außen herunter; Laub nur außen am Bogen, über dem Stamm offen. Entspricht der Setzlingstextur W1, die du gewählt hast |
| C | Glocke | kleine Kuppel oben, darunter zwei Astkränze, der tiefere reicht weiter hinaus. Unten am breitesten. (Der Plan sah erst Strähnen vor, die nach unten nach außen wandern; das hinge gegen die Schwerkraft, deshalb entsteht die Glocke aus den Ästen.) |
| D | Schirm | höherer Stamm mit Gabelung, darauf ein flaches, breites Dach; der Vorhang macht den größten Teil der Höhe aus |

### Runde W2: Vorhang

Auf dem Umriss aus W1.

- A: einzelne Strähnen wie jetzt, aber stark gemischte Längen (ein Drittel bis fast zum Boden, der Rest
  40–80 %), ausgefranste Unterkante.
- B: Bündel: zwei bis drei Strähnen diagonal beieinander, dazwischen Lücken von 2–3 Blöcken. Wirkt wie
  Zweige statt Stäbe.
- C: zwei Schichten: außen lang, ein Ring weiter innen halb so lang. Gibt Tiefe, von innen bleibt der Raum.
- D: Schulter: jede Strähne beginnt zwei Blöcke breit und läuft einzeln aus; weicherer Übergang zur Krone.
- E: wie die beste aus A–D, ein Teil der Strähnen als Ranken oder Blasses Hängemoos statt Laub (prüfe
  vorher in der Jar, ob Hängemoos an Laub hält).

### Runde W3: Stamm und Äste

- A: wie jetzt.
- B: sichtbare Gabelung: der Stamm teilt sich unter der Krone in zwei bis drei dicke Äste, die man von
  außen sieht (Laub erst ab dem Bogen).
- C: kräftiger Fuß und längerer Stamm im Verhältnis zur Krone; Knie nur noch an einem Versatz.
- D: B + C.

### Runde W4: große Weide

Heute ist sie dieselbe Form mit 2×2-Stamm. Varianten auf Basis der Entscheidungen aus W1–W3:

- A: nur größer (wie jetzt).
- B: 2×2-Stamm teilt sich in drei bis vier 1×1-Äste mit je eigenem Kissen oder Bogen; mehrere Stockwerke.
- C: wie B, breiter als hoch, mit begehbarem Raum (mindestens drei Blöcke frei) unter der ganzen Krone.
- D: wie B, stark geneigt (über Wasser hängend): Krone einseitig, Vorhang auf der Neigungsseite bis zum Boden.

## 6. Abschluss

1. **Finalisten im Dev-Client.** Nach den Runden setzt der Draft-Modus die ein bis zwei besten Formen je Baum
   in einer Reihe in die Testwelt; Screenshots aus dem Dev-Client bei Tag, von außen und von unten/innen.
   Erst danach die endgültige Wahl.
2. **Einbau.** Sieger nach `TreeShapes`, `Drafts.java` und Draft-Modus löschen.
3. **Selbsttest anpassen.** `willowShapes` (Strähnen nebeneinander, Enden über dem Boden) und `palmClumps`
   prüfen heute die alte Form; die Prüfungen folgen den neuen Regeln. Neu: Palmenlaub zerfällt nicht (oder
   ist dauerhaft), Dattelrispen haben Holz hinter sich, keine losen Ranken.
4. **Doku.** Würfeltabellen 10, 11 und 13 in `VARIATIONEN.md` neu, Bilder in der README.
5. **Jar** `build/libs/greektrees-0.16.0+26.2.jar` für den Test in Prism.

## 7. Aufwand

Schritt 0 einmal, danach je Runde: Varianten schreiben, Draft-Lauf, zwei Blätter. Vier Runden je Baum, wenn
jede beim ersten Mal sitzt. P1 und W1 entscheiden am meisten; wenn dort schon alles passt, können P2–P4 und
W2–W4 zu je einer Runde zusammengelegt werden.

## 8. Offene Fragen an dich

1. Stimmt der Befund, oder stört dich etwas anderes (z. B. Materialien, Höhe, Früchte)? Dann kommt das als
   eigene Runde dazu.
2. Dauerhaftes Laub bei der Palme: grundsätzlich in Ordnung, oder sollen nur Varianten gezeigt werden, deren
   Laub nach dem Fällen von selbst verschwindet?
3. Einzelne Strähnen bei der Weide waren dein Wunsch. Sollen Bündel (W2 B, D) trotzdem gezeigt werden?
