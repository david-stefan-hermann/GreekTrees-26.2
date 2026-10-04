# Greek Trees

Nine Mediterranean trees for Minecraft 26.2 (Fabric), each grown from its own new sapling, six of them with
fruit. The trees themselves are built from vanilla blocks only (wood blocks with bark on every face, so no log ends
show), and every growth rolls a new shape.

| Sapling | Tree | Blocks |
| --- | --- | --- |
| Cypress Sapling | tall narrow column with a single-block spire | acacia wood, azalea leaves |
| Olive Sapling | short forked trunk, roots on the ground, crowns at different heights, olives | oak wood, azalea leaves |
| Fig Sapling | low and wide, several stems from the ground, figs | acacia wood, azalea leaves |
| Strawberry Tree Sapling | thin orange-red stems, open dark crown, arbutus berries | stripped acacia wood, mangrove leaves |
| Date Palm Sapling | one to three slim trunks within a 2x2 square (two on a diagonal, three in an L), each leaning to its own side only, bent near the crown, bent at the foot or slanted, no two alike; on every trunk a star of fine fronds under a tuft of steep ones, smaller on the lower trunks, every frond with its own direction, length and arch; 15-18 tall, dates right under the leaves; four saplings in a square grow a large date palm: two to five tall trunks slanting apart, 19-27 tall | jungle wood, jungle leaves |
| Mulberry Sapling | short thick trunk forking low under a dense round dome; three in ten pollarded (knobbly fist, flat umbrella), mulberries | pale oak wood, jungle leaves |
| Weeping Willow Sapling | a trunk with a soft bend (along an axis or over a corner; now and then out and back like a C), limbs arching out and down under a rounded crown over the trunk's top, a curtain of single leaf strands with a room inside, a few vines, 11-21 tall; four saplings in a square grow a big one with a 2x2 trunk bending the same way, its steps spread over a few layers, and more strands along the rim, 15-25 tall | pale oak wood, mangrove leaves, vines |
| Aries Oak Sapling | a giant, 53-60 tall and about 50-58 wide, that only grows from sixteen saplings in a 4x4 square: a round trunk, wide and flared at the foot and narrowing upwards, with ridges, burls and stubs, slabs evening out the steps of its limbs and, fewer, of the trunk, and streaks of stripped bark; five to seven limbs with side branches, each carrying a big hollow side crown spanned by twigs (room to build inside) that reaches out past a hollow main dome; dome and side crowns are clean shells of leaves (and moss, on the dome) two blocks thick, lumpy on the outside; vines, glow berries and firefly bushes; its leaves never decay | dark oak wood, stripped dark oak wood, dark oak slabs, azalea, flowering azalea and jungle leaves, moss, vines, glow berries, firefly bushes |

Saplings grow like vanilla ones (random ticks with light level 9 or more, or bone meal); like a vanilla dark
oak, four date palm or four weeping willow saplings in a square grow into one big tree. Aries oak saplings only grow
as a 4x4 square (any of the sixteen starts it); a single one or a smaller group stays a sapling and takes no bone
meal. Saplings can be potted and
composted. Date palm saplings can also be planted on sand. Everything the mod adds is listed in its own
creative tab, "Greek Trees"; the saplings, fruit and pits also appear in the vanilla tabs.

A tree only grows when all of its logs fit (the Aries oak's roots and the lowest layer of its foot give way to the
ground); leaves are placed with their correct vanilla distance, so nothing decays. The leaves of the Aries oak, the
weeping willows and the date palms are placed persistent, like leaves a player sets: hollow crowns, long strands
and fine fronds keep every leaf however far it is from wood, and stay when the tree is felled.

## Fruit

| Fruit | Hangs on | Food | Extra |
| --- | --- | --- | --- |
| Olive | twigs under the olive crown | 2 hunger, good saturation | eating it leaves an Olive Pit |
| Fig | twigs under the fig crown | 3 hunger, good saturation | |
| Arbutus Berry | twigs under the strawberry tree crown | 3 hunger | |
| Date | clusters on the trunk under every palm crown | 3 hunger | |
| Black, White and Red Mulberry | twigs under the mulberry crown, one kind per tree | 2 hunger | |

A grown tree carries its fruit at mixed stages (olives green, yellowish, black; figs green, blushing, purple;
arbutus berries with white flowers, yellow and orange, red; dates green, yellow, brown; mulberries all white-green
at first, then black ones red and black, white ones cream and white, red ones pink and deep red). Fruit ripens on random
ticks like cocoa, or with bone meal.

- Right click on ripe fruit, whatever is in your hand: harvests 2-3 fruit; the twig or cluster stays and starts over
  at its first stage, as if planted anew.
- Right click on unripe fruit: nothing happens (bone meal still makes it grow).
- Left click: breaks it; ripe gives 2-3 fruit, unripe a single one.
- Planting: right click with an olive, fig, arbutus berry or any mulberry on any face of a leaf block hangs a new twig under it;
  a date goes on the side of jungle wood or jungle logs. Where nothing can be planted, the fruit is eaten.

Right-click harvest mods: the twigs keep their ripeness in a property called `stage`, not `age`, because such mods
(Simple Harvesting, for one) treat any block with an `age` property as a crop and pick it at every stage. Date
clusters are cocoa to them: they harvest only ripe ones and replant them, which matches the rules above.

Breaking the leaves of a grown tree now and then drops its fruit (12 %, more with Fortune; not with shears or Silk
Touch). The leaves are vanilla blocks, so the mod tells them apart by what is within five blocks: jungle leaves
near jungle wood (palms), azalea leaves near oak wood (olives), mangrove leaves near stripped acacia wood
(strawberry trees), jungle leaves near pale oak wood (mulberries, of the kind whose twigs hang nearby), azalea leaves near a fig twig (figs; the fig
shares wood and leaves with the cypress). Vanilla jungle, azalea, mangrove and pale oak trees are made of logs and
drop nothing extra, cypress leaves drop no figs and palm leaves no mulberries. Leaves
that decay after all of the tree's wood is gone drop no fruit.

## Olive pits

The Olive Pit left over from an olive is thrown like a snowball, by hand or from a dispenser, and hurts for 1.5
hearts. Two pits on top of each other in the crafting grid make a Sharpened Olive Pit, which hurts for 3.5 hearts.
Both break on impact.

## Crafting

Shapeless; picking up any of the ingredients unlocks the recipe in the recipe book:

| Sapling | Ingredients |
| --- | --- |
| Cypress | spruce sapling, acacia sapling |
| Olive | oak sapling, azalea leaves, apple |
| Fig | 2 acacia saplings, sweet berries |
| Strawberry Tree | acacia sapling, sweet berries |
| Date Palm | jungle sapling, cocoa beans |
| Mulberry | pale oak sapling, sweet berries |
| Weeping Willow | pale oak sapling, azalea |
| Aries Oak | dark oak sapling, flowering azalea, glow berries |
| Sharpened Olive Pit | 2 olive pits on top of each other (shaped) |

The shapes come from the concept work in `concept/` (the cypress rules were measured on hand-built cypresses); the
dice ranges of every tree are listed in `VARIATIONEN.md` (German).

## Building

Requires Java 25. `./gradlew build` writes `build/libs/greektrees-<version>.jar`. Install it together with
Fabric API on the server and on every client.

`./gradlew runServer -PselfTest` grows every sapling a dozen times on a fresh dev-server world, lets vanilla
recompute and decay the leaves, checks blocked growth, sand planting, recipes, the fruit (drops, picking, leaf
drops), the olive pits (flight, damage) and the creative tab, writes `run/greektrees-selftest/` and stops. Mods
dropped into `run/mods` (a harvest mod, say) are loaded too and listed in the summary, so the right-click checks
can be run against them.

`python tools/date_cluster.py` builds the date cluster model (tilted stalk, strands and dates) and checks that no
two dates overlap and no two faces share a plane (such faces flicker in the game); `tools/make_resources.py`
refuses to write the model otherwise. `python tools/date_concepts.py` renders the concepts the model was chosen from.

## License

MIT, see `LICENSE`. Author: BaconCakeFactory.
