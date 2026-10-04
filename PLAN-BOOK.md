# Plan 0.18.0: das Baumbuch (Guide Book)

Stand 2026-10-04, Ausgangspunkt Mod 0.17.0 (gebaut, Selbsttest bestanden, NICHT committet, wartet auf den
Prism-Test). Geschrieben für Opus 5.5. Auf dem Arbeitsbaum weiterbauen, nichts committen, nichts zurücksetzen.

Wunsch des Nutzers: ein Buch im Spiel, das jeden Baum erklärt: wie man den Setzling craftet (mit Bild), wie man
ihn setzt, welche Früchte er trägt, dazu je ein Bild eines gewachsenen Baums. Das Cover im Stil des Mod-Logos
(Mosaik, `src/main/resources/assets/greektrees/icon.png`).

## Entscheidungen des Nutzers (fest, nicht neu aufrollen)

| Frage | Antwort |
| --- | --- |
| Baumbilder | **A: Iso-Render auf Pergament** mit Grasplatte und dünnem Rahmen, genau wie in `art/book_concepts/preview_tree_pictures.png`, Spalte A. Kein Mosaik für die Baumbilder. |
| Erhalt | Rezept (Buch + beliebiger Mod-Setzling, formlos) **und** einmaliges Startgeschenk je Spieler. |
| Cover | Mosaik im Logo-Stil für die **Item-Textur** und die **Titelseite** im Buch. Inhaltsseiten schlichtes Pergament. |
| Kapitel | 8 Baumseiten, dazu Inhaltsverzeichnis (anklickbar), „Große Bäume" (große Dattelpalme, große Trauerweide mit eigenen Bildern), „Früchte" allgemein, „Olivenkerne". |
| Ton | Kurze Spielinfos plus ein Satz Flair (echte Pflanze / griechische Mythologie). |

## Regeln für die Umsetzung

- Bauen nur mit der Zeile aus `../CLAUDE.md` (bash, JDK 25, TEMP). Nie bauen oder Quellen ändern, während ein
  Selbsttest oder der Dev-Client läuft.
- Keine neue Abhängigkeit (kein Patchouli o. ä.): eigenes Item, eigener Screen. Fabric API ist schon da.
- **Vorlage, zuerst lesen:** `../goblin-labour` hat genau das schon einmal gelöst:
  `src/main/java/goblinlabour/item/GoblinHandbookItem.java` (Item mit Client-Opener),
  `item/Handbook.java` (Inhalt als Records im gemeinsamen Code),
  `client/HandbookScreen.java` (Screen, Tooltips, Seitenwechsel). Muster übernehmen, nicht den Goblin-Look.
  goblin-labour ist auf 26.3, greek-trees auf **26.2**: jede API vor dem Benutzen mit `javap` am 26.2-Jar prüfen.
- Am 26.2-Jar bereits geprüft (2026-10-04): `Screen.extractBackground/extractRenderState(GuiGraphicsExtractor,
  int, int, float)`, `Screen.keyPressed(KeyEvent)`, `Minecraft.setScreen(Screen)`,
  `GuiGraphicsExtractor.fill/text/centeredText/item/setTooltipForNextFrame`,
  `GuiGraphicsExtractor.blit(RenderPipeline, Identifier, int x, int y, float u, float v, int w, int h,
  int regionW, int regionH, int texW, int texH)` mit `RenderPipelines.GUI_TEXTURED` (zeichnet eine Textur
  skaliert), `net.minecraft.client.gui.screens.inventory.PageButton(int x, int y, boolean forward, OnPress,
  boolean playTurnSound)` (die Blätterpfeile des Vanilla-Buchs), `Screenshot.grab(File, String, RenderTarget,
  int, Consumer<Component>)`, `Inventory.add(ItemStack)`, `Item.use(Level, Player, InteractionHand)`,
  Fabric `AttachmentRegistry.create(Identifier, Consumer<Builder>)` mit `persistent(Codec)` und `copyOnDeath()`.
- Sprachdateien, Rezepte, Item-Modelle werden **erzeugt** (`tools/make_resources.py` schreibt `en_us.json` und
  `de_de.json` komplett, `tools/make_fruits.py` hängt seine Einträge an). Buchtexte nie von Hand in die
  JSON-Dateien schreiben, sondern über denselben Weg (siehe B). Erst nachsehen, wie `make_fruits.py` an
  `make_resources.py` hängt, und es genauso machen.
- Texte: `en_us` und `de_de`, immer beide. Autor ist BaconCakeFactory. Der Spielername hinter der Widdereiche
  kommt nirgends vor.
- Zwei Freigaben durch den Nutzer, jeweils anhalten und Bilder zeigen (`SendUserFile`):
  1. nach B: Vorschaubögen (Cover-Varianten, Item-Textur, alle Baumbilder), **bevor** Screenshots entstehen;
  2. nach E: Dev-Client-Screenshots aller Doppelseiten in beiden Sprachen.
- Nichts als fertig melden ohne Selbsttest-Zeile oder Screenshot. Am Ende den Jar-Pfad nennen
  (`greek-trees/build/libs/greektrees-0.18.0+26.2.jar`), nicht committen, nicht veröffentlichen.

## Aufbau des Buchs

Aufgeschlagenes Buch als Doppelseite, in GUI-Pixeln **312 × 196** (zwei Seiten je 156 × 196, Rand 12, Textbreite
132). Das passt in die kleinste GUI-Fläche (320 × 240). Die Zahlen sind Startwerte: wenn Texte nicht passen,
zuerst Text kürzen, dann Maße ändern.

| Nr. | Doppelseite | Links | Rechts |
| --- | --- | --- | --- |
| 0 | Cover | geschlossenes Buch: nur das Mosaik-Cover (156 × 196), mittig | – |
| 1 | Inhalt | anklickbare Liste: 8 Bäume (Setzling-Icon + Name), Große Bäume, Früchte, Olivenkerne | „Grundlagen" (Text unten) |
| 2–9 | je ein Baum: Zypresse, Olive, Feige, Erdbeerbaum, Dattelpalme, Maulbeere, Trauerweide, Widdereiche (Reihenfolge von `GreekTrees.SPECIES`) | Name, Baumbild 112 × 112, Beschreibung mit Flair-Satz | „Herstellung": 3×3-Raster mit Zutaten, Pfeil, Ergebnis; „Pflanzen": Text; „Früchte": Frucht-Icon(s) + Text |
| 10 | Große Bäume | Bild große Dattelpalme, 2×2-Setzlingsraster, ein Satz | Bild große Trauerweide, 2×2-Raster, ein Satz |
| 11 | Früchte | Reifen, Ernten, Pflanzen (Text) + drei Reifestufen der Olive als Bild (die drei Texturen `textures/block/olive_twig_stage0..2.png` nebeneinander, 2× groß) | Liste der 7 Früchte: Icon, Name, Hunger, Baum |
| 12 | Olivenkerne | Text (Wurf, Schaden, Werfer) | Rezept geschärfter Kern (geformt: zwei Kerne übereinander) |

Höhenbudget rechte Baumseite (172 nutzbar): Überschrift 12 + Raster 58 + Überschrift 12 + Pflanztext bis 4 Zeilen
(36) + Überschrift 12 + Fruchtzeilen bis 3 (27) = 157. Linke Seite: Name 12 + Bild 116 + Beschreibung bis 5 Zeilen
(45) = 173. Bäume ohne Frucht (Zypresse, Trauerweide, Widdereiche): Zeile „Trägt keine Früchte"; bei der
Widdereiche steht dort stattdessen ein 4×4-Raster aus Setzling-Icons in halber Größe (Pose-Skalierung 0,5).

Bedienung: `PageButton` unten links/rechts auf den Seiten (bringt den Blätterton mit), Pfeiltasten und Bild
auf/ab, Mausrad; Klick aufs Cover oder „weiter" schlägt auf; Klick auf einen Inhaltseintrag springt zur Seite.
Item-Icons zeigen beim Überfahren den Vanilla-Tooltip (`setTooltipForNextFrame`, wie `HandbookScreen`).
`isPauseScreen()` = false. Die zuletzt offene Doppelseite merkt sich ein `static int` im Screen (nur für die
Sitzung); erstes Öffnen zeigt das Cover.

## A. Item, Rezept, Startgeschenk (gemeinsamer Code)

1. `GuideBookItem extends Item` nach dem Muster `GoblinHandbookItem`: statischer `Runnable`/`Consumer`-Opener, den
   `GreekTreesClient` setzt; `use` ruft ihn auf dem Client und gibt `InteractionResult.SUCCESS` zurück. Kein
   Client-Import im gemeinsamen Code (dedizierter Server!). Registrieren als `greektrees:guide_book`,
   `stacksTo(1)`. Namen: „Greek Trees Guide" / „Baumkunde: Griechische Bäume". Im Mod-Tab an erster Stelle.
2. Rezept `data/greektrees/recipe/guide_book.json`: formlos, `minecraft:book` + `#greektrees:saplings`.
   Neuer Item-Tag `data/greektrees/tags/item/saplings.json` mit den 8 Setzlingen (aus derselben Liste erzeugen,
   die `make_resources.py` für `minecraft:saplings` benutzt). Rezeptbuch-Freischaltung mit
   `tools/recipes.py: recipe_unlock` (Buch oder ein Mod-Setzling im Inventar).
3. Startgeschenk: `AttachmentType<Boolean> GOT_BOOK = AttachmentRegistry.create(id("got_guide_book"),
   b -> b.persistent(Codec.BOOL).copyOnDeath())`. Eine Methode `giveBookOnce(ServerPlayer)`: wenn das Attachment
   fehlt, Buch ins Inventar (`getInventory().add`, sonst `drop`), Attachment setzen. Aufruf aus
   `ServerPlayConnectionEvents.JOIN`. Vanilla-Entity-Tags gehen dafür nicht: `ServerPlayer.restoreFrom` kopiert
   sie nicht (am Jar geprüft), nach dem ersten Tod gäbe es ein zweites Buch. Auch Spieler bestehender Welten
   bekommen das Buch so einmal nach dem Update; das ist gewollt.

## B. Generator `tools/make_book.py` und Vorschau (Freigabe 1)

`tools/book_preview.py` (Vorschau dieser Sitzung) geht darin auf: `fit()`, `parchment()` und die Mosaikroutine
übernehmen, danach `book_preview.py` löschen. Mosaiksteine wie im Logo: `tools/make_icons.py`
(`icon_mosaic`, `mosaic_tiles`: Farben, Fugen, Zittern, Randringe dunkelblau / blau-weiß im Wechsel).

1. **Baumbilder** → `assets/greektrees/textures/gui/book/<name>.png` für die 8 Bäume plus `large_date_palm`,
   `large_weeping_willow`. Quelle: `run/greektrees-selftest/<name>_<n>.json` (Stand 0.17.0 liegt vor; wenn der
   Baumcode seither geändert wurde, erst `./gradlew runServer -PselfTest`). Render wie Spalte A der Vorschau
   (`voxel.render` mit Grasplatte, auf Pergament, 2 px Rahmen), Ausgabe **224 × 224** (2× GUI-Auflösung,
   gezeichnet auf 112 × 112). Welcher Wuchs je Art: ein Dict `PICK = {'olive': 0, ...}` im Skript.
   Die Widdereiche (55–61 hoch) wird nur kleiner skaliert, sonst gleich.
2. **Cover** → `textures/gui/book/cover.png` (312 × 392, gezeichnet auf 156 × 196): Mosaik mit den Randringen des
   Logos, cremefarbenes Feld, Ockerboden, Baum, Schriftzug. Drei Varianten für den Vorschaubogen:
   K1 Olivensetzling groß wie im Logo + Schriftzug „GREEK TREES" aus Steinen (zwei Zeilen, 5×7-Steinschrift);
   K2 gewachsener Olivenbaum (der Mosaikbaum aus `icon_mosaic()` ohne `sapling_name`, größer) + Schriftzug;
   K3 wie K1 ohne Schriftzug, der Titel wird im Spiel mit der Spielschrift auf ein Ockerband gesetzt
   (übersetzbar).
3. **Item-Textur** → `textures/item/guide_book.png`, 16 × 16: Buchform (Seitenschnitt unten/rechts hell), der
   Deckel als Mini-Mosaik: dunkelblauer Rand, cremefarbenes Feld, kleiner grüner Baum mit braunem Stamm. Drei
   Varianten (Baumgröße / Randbreite / mit Ockerboden) auf dem Bogen, je in 16 px, 64 px und 8× vergrößert,
   daneben zum Vergleich das Vanilla-Buch.
4. **Doppelseite** → `textures/gui/book/spread.png`, 312 × 196 in GUI-Auflösung (1×, Pixel-Art wie Vanilla):
   zwei Pergamentseiten (Farbe wie in der Vorschau, `PAGE`), dunkler Falz in der Mitte, 1 px dunkler Rand,
   unten/außen zwei Pixel „Seitenstapel". Schlicht, kein Mosaik.
5. Item-Modell/`items/guide_book.json`, Rezept, Tag, Freischaltung und alle Sprachschlüssel (Tabelle unten)
   schreibt dasselbe Skript über den vorhandenen `write`-/Lang-Weg.
6. Vorschaubögen nach `art/book_concepts/`: `preview_cover.png` (K1–K3 + Item-Varianten) und
   `preview_tree_pictures_all.png` (je Art die ersten vier Wüchse nebeneinander als fertiges Buchbild, der
   vorgeschlagene markiert). **Anhalten, beide Bögen zeigen, Auswahl abwarten.** Erst danach C–E.
   Nur ändern, was der Nutzer zu einer Variante sagt; die gewählte Variante sonst unangetastet lassen.

## C. Inhalt `GuideBook` (gemeinsamer Code) und Rezeptdaten

- `GuideBook.java` im gemeinsamen Paket, nach dem Muster `Handbook.java`: die Liste der Doppelseiten als Records
  (z. B. `Cover`, `Contents`, `Tree(Species, fruits, plantingGrid)`, `BigTrees`, `Fruit`, `Pits`). Keine
  allgemeine Layout-Engine, keine Seitenumbrüche: jede Doppelseite hat ein festes Layout.
- **Rezepte nicht doppelt pflegen:** die Zutaten liest `GuideBook.recipe(name)` aus der eigenen Rezeptdatei im
  Mod-Jar (`FabricLoader.getInstance().getModContainer(MOD_ID).get().findPath("data/greektrees/recipe/<name>.json")`,
  Gson ist im Spiel): `crafting_shapeless` → Zutaten der Reihe nach in die Felder 0..n, `crafting_shaped` →
  `pattern` + `key`. Ergebnis: neun `ItemStack` + Ergebnis-Stack. Der Client hat seit 1.21.2 keinen
  Rezept-Manager mehr, deshalb dieser Weg. Dazu ein Kommentar
  `// ponytail: reads the mod's own recipe files; item ids only, no tags, datapack overrides are not shown`.
- Texte nur als Übersetzungsschlüssel `greektrees.book.<seite>.<teil>`.

## D. Screen `client/GuideBookScreen`

- `extractBackground`: Vanilla-Abdunklung, dann `spread.png` (oder auf Seite 0 `cover.png`) mit `blit`.
- `extractRenderState`: je Seitentyp eine kleine Zeichenmethode. Text mit `font.split(component, 132)`,
  Zeilenhöhe 9, Tintenfarbe dunkelbraun, ohne Schatten; Überschriften in Mosaikblau (`0xFF2C60AA`), Flair-Satz
  kursiv. Baumbild: `blit(GUI_TEXTURED, id, x, y, 0, 0, 112, 112, 224, 224, 224, 224)`.
- Rezeptraster: neun Felder 18 × 18 mit `fill` (Feld etwas dunkler als das Pergament, 1 px Rand), Items mit
  `graphics.item`, Pfeil wie `HandbookScreen.drawArrow`, Ergebnis rechts. Kein Vanilla-Containerbild.
- Jede Zeichenmethode gibt die benutzte Höhe zurück; ist sie größer als die Seite, einmal
  `LOGGER.warn("BOOK OVERFLOW spread {} {}", nr, sprache)`. Das ist die Prüfung, an der zu lange Texte auffallen.
- GUI-Größen 2, 3 und 4 ansehen: sehen die 224er-Baumbilder bei 3 unsauber aus, im Generator 336 × 336 probieren
  und die bessere Auflösung nehmen.

## E. Prüfen

1. **Selbsttest** (`DevSelfTest`, Server, neue Zeilen in `summary.txt`, Fehler zählen wie die anderen Checks):
   - `guide book recipe`: Buch + jeder der 8 Setzlinge ergibt `guide_book` (vorhandene Craft-Hilfe benutzen).
   - `guide book gift`: `giveBookOnce` zweimal mit einem `FakePlayer` → genau ein Buch.
   - `guide book content`: für jede Baumseite liefert `GuideBook.recipe` als Ergebnis den Setzling der Art und
     keine Zutat ist Luft; jeder vom Buch benutzte Sprachschlüssel steht in `en_us.json` **und** `de_de.json`
     (beide Dateien per Gson aus dem Mod-Container lesen).
   - `creative tab`: der vorhandene Check kennt das Buch.
2. **Screenshots** (Freigabe 2): greek-trees hat noch keinen Client-Harness. Kleinster Weg, ohne Welt und ohne
   Server: in `GreekTreesClient` mit `-Dgreektrees.bookshots=1` ein `ClientTickEvents.END_CLIENT_TICK`-Hook, der
   wartet, bis der Titelbildschirm steht (`minecraft.screen instanceof TitleScreen`, kein Overlay), dann der
   Reihe nach jede Doppelseite öffnet, nach 10 Ticks `Screenshot.grab(gameDirectory, "book_<lang>_<nr>.png",
   mainRenderTarget, 1, ...)` aufruft und am Ende `minecraft.stop()`. In `build.gradle` ein Block
   `if (project.hasProperty('bookShots'))` wie die vorhandenen (`vmArg`, `programArgs "--width", "1280",
   "--height", "720"` → GUI-Größe 3). Sprache über `lang:de_de` bzw. `lang:en_us` in `run/options.txt`, zwei
   Läufe. Falls Item-Icons ohne Welt nicht zeichnen: Weg von goblin-labour nehmen (`build.gradle` Zeilen 22–46,
   `DevClientHooks`: Client tritt dem Dev-Server bei). Jeden Screenshot selbst ansehen (Überlauf, abgeschnittene
   Wörter, Icons, Rahmen), dann alle 26 dem Nutzer zeigen und anhalten.
3. `./gradlew build`, Log auf `BOOK OVERFLOW` und Fehler prüfen.

## F. Abschluss

- `gradle.properties`: `mod_version=0.18.0+26.2`.
- `README.md`: Abschnitt „Guide book" (Rezept, Startgeschenk, was drinsteht) und das Buch in der Crafting-Tabelle.
- Ergebnisbericht: Selbsttest-Zeilen, Screenshots, Jar-Pfad für den Prism-Test. Kein Commit, kein Release.

## Texte (Entwurf, en / de)

Kürzen erlaubt, wenn `BOOK OVERFLOW` meldet; Fakten nicht ändern (Quelle: `README.md`, `summary.txt`).
Schlüssel: `greektrees.book.<baum>.about|plant|fruit`. `about` endet mit dem Flair-Satz (kursiv, eigener
Schlüssel `.lore`).

Gemeinsame Bausteine: `plant.default` = „Plant on dirt or grass. Grows with light or bone meal." /
„Auf Erde oder Gras. Wächst mit Licht oder Knochenmehl."; `fruit.none` = „Bears no fruit." / „Trägt keine
Früchte."; Überschriften „Crafting / Herstellung", „Planting / Pflanzen", „Fruit / Früchte".

| Baum | about (en / de) | lore (en / de) | plant | fruit (en / de) |
| --- | --- | --- | --- | --- |
| cypress | Tall, narrow column, 21–23 high. Acacia wood, azalea leaves. / Hohe, schmale Säule, 21–23 hoch. Akazienholz, Azaleenlaub. | Named after Kyparissos, whom Apollo turned into the tree of mourning. / Benannt nach Kyparissos, den Apollon in den Baum der Trauer verwandelte. | default | none |
| olive | Short forked trunk with roots, crowns at different heights, 8–12 high. Oak wood, azalea leaves. / Kurzer, gegabelter Stamm mit Wurzeln, Kronen auf mehreren Höhen, 8–12 hoch. Eichenholz, Azaleenlaub. | Athena's gift to Athens. / Athenes Geschenk an Athen. | default | Olives under the leaves. 2 hunger; eating one leaves a pit. / Oliven unter dem Laub. 2 Hunger; übrig bleibt ein Kern. |
| fig | Low and wide, several stems, 7 high. Acacia wood, azalea leaves. / Niedrig und breit, mehrere Stämme, 7 hoch. Akazienholz, Azaleenlaub. | Figs fed the first athletes of Olympia. / Feigen nährten die ersten Athleten von Olympia. | default | Figs under the leaves. 3 hunger. / Feigen unter dem Laub. 3 Hunger. |
| strawberry_tree | Thin orange-red stems, open dark crown, 10–11 high. Stripped acacia wood, mangrove leaves. / Dünne, orangerote Stämme, lichte dunkle Krone, 10–11 hoch. Entrindetes Akazienholz, Mangrovenlaub. | Its berries take a year to ripen, so flowers and fruit hang side by side. / Die Früchte reifen ein Jahr, darum hängen Blüten und Früchte nebeneinander. | default | Arbutus berries under the leaves. 3 hunger. / Erdbeerbaumfrüchte unter dem Laub. 3 Hunger. |
| date_palm | One to three slim, leaning trunks, 15–18 high. Jungle wood, jungle leaves. / Ein bis drei schlanke, geneigte Stämme, 15–18 hoch. Tropenholz, Tropenlaub. | The Cretan date palm, named after Theophrastus, grows wild on the beach of Vai. / Die Kretische Dattelpalme, benannt nach Theophrast, wächst wild am Strand von Vai. | On dirt, grass or sand. Four in a square grow a large palm. / Auf Erde, Gras oder Sand. Vier im Quadrat ergeben eine große Palme. | Dates on the trunk, right under the crown. 3 hunger. / Datteln am Stamm, direkt unter der Krone. 3 Hunger. |
| mulberry | Short thick trunk under a dense round dome, 10–11 high. Pale oak wood, jungle leaves. / Kurzer, dicker Stamm unter dichter, runder Krone, 10–11 hoch. Blasseichenholz, Tropenlaub. | Once white, the berries turned dark with the blood of Pyramus. / Einst weiß, färbte das Blut des Pyramus die Beeren dunkel. | default | Black, white or red mulberries, one kind per tree. 2 hunger. / Schwarze, weiße oder rote Maulbeeren, je Baum eine Sorte. 2 Hunger. |
| weeping_willow | Softly bent trunk, a curtain of leaf strands with room inside, 11–21 high. Pale oak wood, mangrove leaves, vines. / Sanft gebogener Stamm, ein Vorhang aus Laubsträngen mit Raum darunter, 11–21 hoch. Blasseichenholz, Mangrovenlaub, Ranken. | Orpheus carried a willow branch into the underworld. / Orpheus trug einen Weidenzweig in die Unterwelt. | default + Four in a square grow a big willow. / Vier im Quadrat ergeben eine große Weide. | none |
| aries_oak | A giant, 53–60 high and as wide, with hollow crowns to build in. Its leaves never decay. / Ein Riese, 53–60 hoch und ebenso breit, mit hohlen Kronen zum Bauen. Sein Laub verfällt nie. | Like the oak of Dodona, in whose leaves Zeus was heard. / Wie die Eiche von Dodona, in deren Laub man Zeus hörte. | Only grows from 16 saplings in a 4×4 square. Fewer never grow and take no bone meal. / Wächst nur aus 16 Setzlingen im 4×4-Quadrat. Weniger wachsen nie und nehmen kein Knochenmehl. | 4×4-Raster statt Fruchtzeile |

Weitere Seiten:

- `contents.basics` (Inhalt, rechts): „Every tree grows from its own sapling and is built from vanilla blocks; no
  two grow alike. Saplings can be potted and composted. A tree only grows where all of its wood fits." /
  „Jeder Baum wächst aus seinem eigenen Setzling und besteht aus Vanilla-Blöcken; keine zwei wachsen gleich.
  Setzlinge lassen sich eintopfen und kompostieren. Ein Baum wächst nur, wo sein ganzes Holz Platz hat."
- `big.date_palm`: „Two to five tall trunks slanting apart, 19–27 high." / „Zwei bis fünf hohe Stämme, die
  auseinanderstreben, 19–27 hoch." `big.weeping_willow`: „A 2×2 trunk and more strands along the rim, 15–25
  high." / „Stamm 2×2 und mehr Stränge am Rand, 15–25 hoch." Beide mit „Four saplings in a square." /
  „Vier Setzlinge im Quadrat."
- `fruit.text`: „Fruit ripens in three stages, like cocoa; bone meal helps. Right click ripe fruit: 2–3 fruit, the
  twig stays and starts over. Breaking unripe fruit gives one. Plant fruit on a leaf block to hang a new twig;
  dates go on the side of jungle wood. Breaking a tree's leaves sometimes drops fruit." / „Früchte reifen in
  drei Stufen wie Kakao; Knochenmehl hilft. Rechtsklick auf reife Früchte: 2–3 Früchte, der Zweig bleibt und
  beginnt von vorn. Unreif abgebaut gibt es eine. Frucht auf einen Laubblock setzen: ein neuer Zweig; Datteln
  an die Seite von Tropenholz. Laub eines Baums lässt manchmal Früchte fallen."
- `pits.text`: „Eating an olive leaves a pit. Throw it like a snowball, by hand or from a dispenser: 1.5 hearts.
  Two pits on top of each other make a sharpened pit: 3.5 hearts. Both break on impact." / „Vom Essen einer
  Olive bleibt ein Kern. Er fliegt wie ein Schneeball, aus der Hand oder dem Werfer: 1,5 Herzen. Zwei Kerne
  übereinander ergeben einen geschärften Kern: 3,5 Herzen. Beide zerbrechen beim Aufprall."

## Nicht Teil dieses Plans

Suche, Lesezeichen, Fortschritt/Advancements, drehbare 3D-Bäume, Mosaikrahmen auf Inhaltsseiten, weitere
Sprachen, Buch im Vanilla-Kreativtab. Erst bauen, wenn der Nutzer es verlangt.
