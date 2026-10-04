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
import net.minecraft.network.chat.Component;
import net.minecraft.resources.Identifier;
import net.minecraft.world.food.FoodProperties;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.ItemLike;

/**
 * The content of the guide book, as data: chapters of sections, which the client's {@code GuideBookScreen} wraps and
 * breaks into pages. Texts are translation keys {@code greektrees.book.<key>} (written by tools/make_book.py); every
 * key the book uses is listed by {@link #keys()}, which the self-test checks against both language files.
 */
public final class GuideBook {
    /** Trees with a planting text of their own instead of {@code plant.default}. */
    private static final Set<String> OWN_PLANTING = Set.of("date_palm", "weeping_willow", "aries_oak");

    private GuideBook() {
    }

    public static String key(String name) {
        return GreekTrees.MOD_ID + ".book." + name;
    }

    public sealed interface Section permits Heading, Text, Lore, Dedication, ItemLine, Recipe, Pictures, Saplings, Break {
        default List<String> keys() {
            return List.of();
        }
    }

    public record Heading(String key) implements Section {
        @Override
        public List<String> keys() {
            return List.of(key);
        }
    }

    public record Text(String key) implements Section {
        @Override
        public List<String> keys() {
            return List.of(key);
        }
    }

    /** A line of myth, set in italics. */
    public record Lore(String key) implements Section {
        @Override
        public List<String> keys() {
            return List.of(key);
        }
    }

    /** Whom a tree is dedicated to, set off in the title's blue. */
    public record Dedication(String key) implements Section {
        @Override
        public List<String> keys() {
            return List.of(key);
        }
    }

    /** Item icons with a text beside them. */
    public record ItemLine(List<ItemStack> icons, String key, Object... args) implements Section {
        @Override
        public List<String> keys() {
            return List.of(key);
        }
    }

    /** A crafting grid: nine stacks, row by row (empty where nothing goes), and what it makes. */
    public record Recipe(List<ItemStack> grid, ItemStack result) implements Section {
    }

    /** Square pictures side by side, each {@code size} wide, from textures {@code textureSize} wide. */
    public record Pictures(List<Identifier> textures, int size, int textureSize, boolean framed) implements Section {
    }

    /** A square of saplings, {@code side} to a side, the way they have to be planted; the texts stand beside it. */
    public record Saplings(Item sapling, int side, List<String> keys) implements Section {
    }

    /** What follows starts a new page. */
    public record Break() implements Section {
    }

    /** A chapter with its tab: the trees' tabs are on the left of the book, the others on the right. */
    public record Chapter(String title, ItemStack icon, boolean tree, List<Section> sections) {
    }

    /** Built when the book opens: item stacks need the registries. */
    public static List<Chapter> chapters() {
        List<Chapter> chapters = new ArrayList<>();
        chapters.add(new Chapter(key("basics"), new ItemStack(GreekTrees.GUIDE_BOOK), false,
                List.of(new Text(key("basics.text")))));
        Map<String, List<ItemLike>> fruit = Map.of("olive", List.of(GreekTrees.OLIVE), "fig", List.of(GreekTrees.FIG),
                "strawberry_tree", List.of(GreekTrees.ARBUTUS_BERRY), "date_palm", List.of(GreekTrees.DATE),
                "mulberry", List.of(GreekTrees.BLACK_MULBERRY, GreekTrees.WHITE_MULBERRY, GreekTrees.RED_MULBERRY));
        List<Section> rows = new ArrayList<>();
        for (GreekTrees.Species s : GreekTrees.SPECIES) {
            String name = s.name();
            List<ItemStack> fruits = fruit.getOrDefault(name, List.of()).stream().map(ItemStack::new).toList();
            List<Section> sections = new ArrayList<>(List.of(picture(name), new Text(key(name + ".about")),
                    new Lore(key(name + ".lore")), new Heading(key("heading.crafting")), recipe(name + "_sapling"),
                    new Heading(key("heading.planting"))));
            String planting = key(OWN_PLANTING.contains(name) ? name + ".plant" : "plant.default");
            if (name.equals("aries_oak")) { // grows only from a 4x4 square of saplings, and bears no fruit
                sections.add(3, new Dedication(key(name + ".dedication"))); // under the lore
                sections.add(new Saplings(s.item(), 4, List.of(planting)));
            } else {
                sections.add(new Text(planting));
                sections.add(new Heading(key("heading.fruit")));
                sections.add(fruits.isEmpty() ? new Text(key("fruit.none")) : new ItemLine(fruits, key(name + ".fruit")));
            }
            chapters.add(new Chapter(key(name + ".name"), new ItemStack(s.item()), true, sections));
            for (ItemStack f : fruits) {
                FoodProperties food = f.get(DataComponents.FOOD);
                rows.add(new ItemLine(List.of(f), key("fruit.row"), f.getHoverName(), food == null ? 0 : food.nutrition(),
                        Component.translatable(key(name + ".name"))));
            }
        }

        Item palm = GreekTrees.SPECIES.get(4).item(), willow = GreekTrees.SPECIES.get(6).item();
        List<Section> big = new ArrayList<>();
        for (Map.Entry<String, Item> tree : List.of(Map.entry("large_date_palm", palm), Map.entry("large_weeping_willow", willow))) {
            big.add(new Heading(key(tree.getKey() + ".name")));
            big.add(picture(tree.getKey()));
            big.add(new Saplings(tree.getValue(), 2, List.of(key(tree.getKey() + ".about"), key("big.square"))));
        }
        chapters.add(new Chapter(key("big"), new ItemStack(palm), false, big));

        List<Section> fruits = new ArrayList<>(List.of(new Text(key("fruit.text")),
                new Pictures(List.of(stage(0), stage(1), stage(2)), 32, 16, false), new Break()));
        fruits.addAll(rows);
        chapters.add(new Chapter(key("fruit"), new ItemStack(GreekTrees.OLIVE), false, fruits));

        chapters.add(new Chapter(key("pits"), new ItemStack(GreekTrees.OLIVE_PIT), false, List.of(
                new Text(key("pits.text")), new Heading(key("heading.crafting")), recipe("sharpened_olive_pit"))));
        return chapters;
    }

    /** Every translation key the book shows. */
    public static List<String> keys() {
        List<String> keys = new ArrayList<>();
        for (Chapter chapter : chapters()) {
            keys.add(chapter.title());
            chapter.sections().forEach(s -> keys.addAll(s.keys()));
        }
        return keys;
    }

    private static Pictures picture(String name) {
        return new Pictures(List.of(GreekTrees.id("textures/gui/book/" + name + ".png")), 96, 192, true);
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
