package greektrees;

import java.io.IOException;
import java.io.UncheckedIOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Map;
import java.util.Set;

import com.google.gson.JsonArray;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;
import net.fabricmc.loader.api.FabricLoader;
import net.minecraft.core.component.DataComponents;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.resources.Identifier;
import net.minecraft.world.food.FoodProperties;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.ItemLike;

/**
 * The content of the guide book, as data: the spreads of the open book, each with a fixed layout drawn by the
 * client's {@code GuideBookScreen}. Texts are translation keys {@code greektrees.book.<key>} (written by
 * tools/make_book.py); every key a spread uses is listed by its {@link Spread#keys()}, which the self-test checks
 * against both language files.
 */
public final class GuideBook {
    /** Trees with a planting text of their own instead of {@code plant.default}. */
    private static final Set<String> OWN_PLANTING = Set.of("date_palm", "weeping_willow", "aries_oak");

    private GuideBook() {
    }

    public static String key(String name) {
        return GreekTrees.MOD_ID + ".book." + name;
    }

    public sealed interface Spread permits Cover, Contents, Tree, BigTrees, Fruits, Pits {
        List<String> keys();
    }

    /** The closed book: only the cover. */
    public record Cover() implements Spread {
        @Override
        public List<String> keys() {
            return List.of();
        }
    }

    /** A line of the contents: its icon, its title and the spread it opens. */
    public record Entry(ItemStack icon, String title, int spread) {
    }

    /** Left the clickable contents, right the basics. */
    public record Contents(List<Entry> entries) implements Spread {
        @Override
        public List<String> keys() {
            List<String> keys = new ArrayList<>(List.of(key("contents"), key("basics"), key("basics.text")));
            entries.forEach(e -> keys.add(e.title()));
            return keys;
        }
    }

    /**
     * One tree. Left its name, picture and description, right its recipe, how to plant it and its fruit; the Aries
     * oak shows its sixteen saplings in place of the fruit.
     */
    public record Tree(String name, Item sapling, List<ItemStack> fruits) implements Spread {
        public String title() {
            return key(name + ".name");
        }

        public String about() {
            return key(name + ".about");
        }

        public String lore() {
            return key(name + ".lore");
        }

        public String planting() {
            return key(OWN_PLANTING.contains(name) ? name + ".plant" : "plant.default");
        }

        public String fruit() {
            return key(fruits.isEmpty() ? "fruit.none" : name + ".fruit");
        }

        /** Grows only from a 4x4 square of saplings. */
        public boolean square() {
            return name.equals("aries_oak");
        }

        public Identifier picture() {
            return GuideBook.picture(name);
        }

        public Recipe recipe() {
            return GuideBook.recipe(name + "_sapling");
        }

        @Override
        public List<String> keys() {
            List<String> keys = new ArrayList<>(List.of(title(), about(), lore(), planting(),
                    key("heading.crafting"), key("heading.planting")));
            if (!square()) {
                keys.addAll(List.of(fruit(), key("heading.fruit")));
            }
            return keys;
        }
    }

    /** A tree four saplings in a square grow into. */
    public record BigTree(String name, Item sapling) {
        public String title() {
            return key(name + ".name");
        }

        public String about() {
            return key(name + ".about");
        }

        public Identifier picture() {
            return GuideBook.picture(name);
        }
    }

    /** The large date palm on the left, the big weeping willow on the right. */
    public record BigTrees(BigTree left, BigTree right) implements Spread {
        @Override
        public List<String> keys() {
            return List.of(key("big"), key("big.square"), left.title(), left.about(), right.title(), right.about());
        }
    }

    /** A fruit in the list: the item, its hunger points and the tree's name. */
    public record FruitRow(ItemStack fruit, int nutrition, String tree) {
    }

    /** Left how fruit ripens and is picked, with the olive's three stages; right every fruit. */
    public record Fruits(List<Identifier> stages, List<FruitRow> rows) implements Spread {
        @Override
        public List<String> keys() {
            List<String> keys = new ArrayList<>(List.of(key("fruit"), key("fruit.text"), key("fruit.row")));
            rows.forEach(r -> keys.add(r.tree()));
            return keys;
        }
    }

    /** Left the olive pits, right the sharpened pit's recipe. */
    public record Pits(Recipe recipe) implements Spread {
        @Override
        public List<String> keys() {
            return List.of(key("pits"), key("pits.text"), key("heading.crafting"));
        }
    }

    /** A crafting grid: nine stacks, row by row (empty where nothing goes), and what it makes. */
    public record Recipe(List<ItemStack> grid, ItemStack result) {
    }

    /** Built when the book opens: item stacks need the registries. */
    public static List<Spread> spreads() {
        List<Spread> spreads = new ArrayList<>();
        List<Entry> entries = new ArrayList<>();
        spreads.add(new Cover());
        spreads.add(new Contents(entries));
        Map<String, List<ItemLike>> fruit = Map.of("olive", List.of(GreekTrees.OLIVE), "fig", List.of(GreekTrees.FIG),
                "strawberry_tree", List.of(GreekTrees.ARBUTUS_BERRY), "date_palm", List.of(GreekTrees.DATE),
                "mulberry", List.of(GreekTrees.BLACK_MULBERRY, GreekTrees.WHITE_MULBERRY, GreekTrees.RED_MULBERRY));
        List<FruitRow> rows = new ArrayList<>();
        for (GreekTrees.Species s : GreekTrees.SPECIES) {
            List<ItemStack> fruits = fruit.getOrDefault(s.name(), List.of()).stream().map(ItemStack::new).toList();
            Tree tree = new Tree(s.name(), s.item(), fruits);
            entries.add(new Entry(new ItemStack(s.item()), tree.title(), spreads.size()));
            spreads.add(tree);
            for (ItemStack f : fruits) {
                FoodProperties food = f.get(DataComponents.FOOD);
                rows.add(new FruitRow(f, food == null ? 0 : food.nutrition(), tree.title()));
            }
        }
        Item palm = GreekTrees.SPECIES.get(4).item(), willow = GreekTrees.SPECIES.get(6).item();
        entries.add(new Entry(new ItemStack(palm), key("big"), spreads.size()));
        spreads.add(new BigTrees(new BigTree("large_date_palm", palm), new BigTree("large_weeping_willow", willow)));
        entries.add(new Entry(new ItemStack(GreekTrees.OLIVE), key("fruit"), spreads.size()));
        spreads.add(new Fruits(List.of(stage(0), stage(1), stage(2)), rows));
        entries.add(new Entry(new ItemStack(GreekTrees.OLIVE_PIT), key("pits"), spreads.size()));
        spreads.add(new Pits(recipe("sharpened_olive_pit")));
        return spreads;
    }

    private static Identifier picture(String name) {
        return GreekTrees.id("textures/gui/book/" + name + ".png");
    }

    private static Identifier stage(int stage) {
        return GreekTrees.id("textures/block/olive_twig_stage" + stage + ".png");
    }

    // ponytail: reads the mod's own recipe files; item ids only, no tags, datapack overrides are not shown
    /**
     * The recipe data/greektrees/recipe/&lt;name&gt;.json as a crafting grid: shapeless ingredients fill the fields in
     * order, a shaped pattern is centred. The client has no recipe manager since 1.21.2, hence the file.
     */
    public static Recipe recipe(String name) {
        JsonObject json;
        try {
            json = JsonParser.parseString(Files.readString(FabricLoader.getInstance().getModContainer(GreekTrees.MOD_ID)
                    .orElseThrow().findPath("data/greektrees/recipe/" + name + ".json").orElseThrow(),
                    StandardCharsets.UTF_8)).getAsJsonObject();
        } catch (IOException e) {
            throw new UncheckedIOException(e);
        }
        List<ItemStack> grid = new ArrayList<>(Collections.nCopies(9, ItemStack.EMPTY));
        if (json.has("pattern")) {
            JsonArray pattern = json.getAsJsonArray("pattern");
            JsonObject keys = json.getAsJsonObject("key");
            int h = pattern.size(), w = pattern.get(0).getAsString().length();
            for (int y = 0; y < h; y++) {
                String row = pattern.get(y).getAsString();
                for (int x = 0; x < w; x++) {
                    String symbol = String.valueOf(row.charAt(x));
                    if (keys.has(symbol)) {
                        grid.set((y + (3 - h) / 2) * 3 + x + (3 - w) / 2, stack(keys.get(symbol)));
                    }
                }
            }
        } else {
            JsonArray ingredients = json.getAsJsonArray("ingredients");
            for (int i = 0; i < ingredients.size(); i++) {
                grid.set(i, stack(ingredients.get(i)));
            }
        }
        return new Recipe(grid, stack(json.getAsJsonObject("result").get("id")));
    }

    private static ItemStack stack(JsonElement id) {
        return new ItemStack(BuiltInRegistries.ITEM.getValue(Identifier.parse(id.getAsString())));
    }
}
