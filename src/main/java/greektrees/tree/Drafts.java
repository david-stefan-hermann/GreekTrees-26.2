package greektrees.tree;

import java.util.Map;
import java.util.function.BiFunction;

import net.minecraft.util.RandomSource;

/**
 * Draft rounds of a rework (PLAN-PALME-WEIDE.md): a round shows a few variants of one feature of a tree side by
 * side, the picked one moves into {@link TreeShapes}. Written out by {@code ./drafts.sh <round> <round>}, drawn by
 * {@code concept/render_selftest.py drafts <round>} (the rows' texts are in its DRAFTS table). No round is open:
 * the picks of the palm and willow rounds are built into TreeShapes. This class and the draft mode go once the
 * rework is accepted in the game.
 */
public final class Drafts {
    private Drafts() {
    }

    /** The variants of a round by their name; each rolls one tree, given the number of the growth (0, 1, 2). */
    public static Map<String, BiFunction<RandomSource, Integer, Shape>> round(String key) {
        throw new IllegalArgumentException("no draft round " + key);
    }
}
