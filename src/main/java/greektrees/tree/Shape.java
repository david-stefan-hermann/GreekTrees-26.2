package greektrees.tree;

import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.function.Consumer;
import java.util.function.Function;
import java.util.function.Supplier;
import java.util.function.ToIntFunction;

import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.util.Mth;
import net.minecraft.util.RandomSource;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.RotatedPillarBlock;
import net.minecraft.world.level.block.state.BlockState;

/**
 * Block layout of one tree relative to the sapling (y = 0 is the sapling's block, trunk base at x = z = 0).
 * Java port of the concept generator helpers in concept/trees.py; the species live in {@link TreeShapes}.
 */
public final class Shape {
    public enum Kind { LOG, LEAF, OTHER }

    public record Cell(BlockState state, Kind kind) {
    }

    final RandomSource rng;
    private final Map<BlockPos, Cell> cells = new LinkedHashMap<>();
    private final Map<BlockPos, Integer> leafDistance = new HashMap<>();
    private boolean persistent;
    private int softFoot;
    int trunkTop;
    int[] strandCounts = new int[3];

    Shape(RandomSource rng) {
        this.rng = rng;
    }

    public Map<BlockPos, Cell> cells() {
        return cells;
    }

    /** Vanilla leaf distance (1..6) of every leaf, valid after {@link #finish()}. */
    public int leafDistance(BlockPos rel) {
        return leafDistance.getOrDefault(rel, 7);
    }

    /** Whether the leaves go in persistent, like leaves a player places (see {@link #finishPersistent()}). */
    public boolean persistentLeaves() {
        return persistent;
    }

    /** Logs below this height (roots, the flare of a foot) may be left out where the ground is in the way. */
    public int softFoot() {
        return softFoot;
    }

    /** Lets the logs of the lowest layers give way to the ground (see {@link #softFoot()}). */
    Shape softFoot(int layers) {
        softFoot = layers;
        return this;
    }

    /** A willow's trunk height (the crown's leader starts above it), for the self-test; 0 on other trees. */
    public int trunkTop() {
        return trunkTop;
    }

    /**
     * A willow's strands, for the self-test: hung at the rim of its crown, further in, and (counted apart, wherever
     * they come from) more than three blocks in from the rim.
     */
    public int[] strandCounts() {
        return strandCounts;
    }

    static int ip(double c) {
        return Mth.floor(c + 0.5);
    }

    static BlockPos ip(double x, double y, double z) {
        return new BlockPos(ip(x), ip(y), ip(z));
    }

    // -- placement --------------------------------------------------------------------------------------------

    void log(double x, double y, double z, Block block, Direction.Axis axis) {
        BlockPos p = ip(x, y, z);
        Cell old = cells.get(p);
        if (old == null || old.kind() != Kind.LOG) {
            cells.put(p, new Cell(block.defaultBlockState().setValue(RotatedPillarBlock.AXIS, axis), Kind.LOG));
        } else if (axis == Direction.Axis.Y && old.state().getValue(RotatedPillarBlock.AXIS) != Direction.Axis.Y) {
            cells.put(p, new Cell(old.state().setValue(RotatedPillarBlock.AXIS, Direction.Axis.Y), Kind.LOG));
        }
    }

    void log(double x, double y, double z, Block block) {
        log(x, y, z, block, Direction.Axis.Y);
    }

    /** Swaps the block of a log cell for another log or wood block, keeping its axis (bark variants). */
    void replaceLog(BlockPos p, Block block) {
        Cell c = cells.get(p);
        if (c != null && c.kind() == Kind.LOG) {
            cells.put(p, new Cell(block.defaultBlockState().setValue(RotatedPillarBlock.AXIS,
                    c.state().getValue(RotatedPillarBlock.AXIS)), Kind.LOG));
        }
    }

    void leaf(double x, double y, double z, Block block) {
        cells.putIfAbsent(ip(x, y, z), new Cell(block.defaultBlockState(), Kind.LEAF));
    }

    void put(double x, double y, double z, BlockState state) {
        cells.put(ip(x, y, z), new Cell(state, Kind.OTHER));
    }

    /** Like {@link #put}, but leaves a cell alone that already holds a log, a leaf or anything else. */
    void putIfFree(double x, double y, double z, BlockState state) {
        cells.putIfAbsent(ip(x, y, z), new Cell(state, Kind.OTHER));
    }

    /**
     * Fruit hanging under the crown: count free cells right below the lowest leaf of a column (the ones seen from
     * below), each with its own state from fruit. Call after {@link #finish()}, so pruned leaves don't count.
     */
    Shape hangUnder(int count, Supplier<BlockState> fruit) {
        Map<Long, Integer> lowest = new HashMap<>();
        cells.forEach((p, c) -> {
            if (c.kind() == Kind.LEAF) {
                lowest.merge(column(p), p.getY(), Math::min);
            }
        });
        List<BlockPos> spots = new ArrayList<>();
        cells.forEach((p, c) -> {
            if (c.kind() == Kind.LEAF && p.getY() == lowest.get(column(p)) && !cells.containsKey(p.below())) {
                spots.add(p.below());
            }
        });
        for (int i = 0; i < count && i < spots.size(); i++) {
            int j = i + rng.nextInt(spots.size() - i);
            BlockPos p = spots.get(j);
            spots.set(j, spots.get(i));
            cells.put(p, new Cell(fruit.get(), Kind.OTHER));
        }
        return this;
    }

    /**
     * Strands of leaves hanging from under the given leaves, tried in the given order: each runs down from the block
     * under its leaf to the y bottom gives it (included) and stops at anything in the way. A strand only hangs where
     * no other strand hangs right or diagonally beside it, so each one stands apart. Returns the strands' columns.
     */
    Set<Long> strands(List<BlockPos> from, ToIntFunction<BlockPos> bottom, Function<BlockPos, Block> leaves) {
        Set<Long> hung = new HashSet<>();
        for (BlockPos top : from) {
            int end = bottom.applyAsInt(top);
            if (end >= top.getY() || cells.containsKey(top.below()) || besideStrand(hung, top)) {
                continue;
            }
            hung.add(column(top));
            for (BlockPos p = top.below(); p.getY() >= end && !cells.containsKey(p); p = p.below()) {
                leaf(p.getX(), p.getY(), p.getZ(), leaves.apply(p));
            }
        }
        return hung;
    }

    /** Whether one of the columns sits on p's column or right or diagonally beside it. */
    static boolean besideStrand(Set<Long> columns, BlockPos p) {
        for (int dx = -1; dx <= 1; dx++) {
            for (int dz = -1; dz <= 1; dz++) {
                if (columns.contains(BlockPos.asLong(p.getX() + dx, 0, p.getZ() + dz))) {
                    return true;
                }
            }
        }
        return false;
    }

    static long column(BlockPos p) {
        return BlockPos.asLong(p.getX(), 0, p.getZ());
    }

    /** Face-connected log line from a to b; the axis follows the dominant direction unless given. */
    void branch(double[] a, double[] b, Block block, Direction.Axis axis) {
        Direction.Axis ax = axis != null ? axis : dominant(a, b);
        line(a, b, p -> log(p.getX(), p.getY(), p.getZ(), block, ax));
    }

    void leafLine(double[] a, double[] b, Block block) {
        line(a, b, p -> leaf(p.getX(), p.getY(), p.getZ(), block));
    }

    void path(double[][] points, Block block, Direction.Axis axis) {
        for (int i = 0; i + 1 < points.length; i++) {
            branch(points[i], points[i + 1], block, axis);
        }
    }

    /**
     * Log line that steps diagonally like a vanilla acacia, without filler blocks, so bends stay one block thick.
     * Leaf decay only cares how far leaves are from any log, not whether the logs touch.
     */
    void stem(double[][] points, Block block) {
        for (int s = 0; s + 1 < points.length; s++) {
            double[] a = points[s];
            double[] b = points[s + 1];
            double dx = b[0] - a[0], dy = b[1] - a[1], dz = b[2] - a[2];
            int n = Math.max(1, (int) Math.ceil(Math.max(Math.abs(dx), Math.max(Math.abs(dy), Math.abs(dz)))));
            for (int i = 0; i <= n; i++) {
                double t = (double) i / n;
                log(a[0] + dx * t, a[1] + dy * t, a[2] + dz * t, block);
            }
        }
    }

    /** Ellipsoid of leaves; the rim is ragged (erode) and everything below floor is cut off. */
    void blob(double cx, double cy, double cz, double rx, double ry, double rz, Block block, double erode,
              Integer floor) {
        blob(cx, cy, cz, rx, ry, rz, block, erode, floor, 0, 0);
    }

    /**
     * Like {@link #blob(double, double, double, double, double, double, Block, double, Integer)}, but below
     * hollowTop a column of radius hollowR round the trunk axis (x = z = 0) stays free.
     */
    void blob(double cx, double cy, double cz, double rx, double ry, double rz, Block block, double erode,
              Integer floor, double hollowR, int hollowTop) {
        for (int x = Mth.floor(cx - rx); x <= Mth.ceil(cx + rx); x++) {
            for (int y = Mth.floor(cy - ry); y <= Mth.ceil(cy + ry); y++) {
                if (floor != null && y < floor) {
                    continue;
                }
                for (int z = Mth.floor(cz - rz); z <= Mth.ceil(cz + rz); z++) {
                    double d = sq((x - cx) / rx) + sq((y - cy) / ry) + sq((z - cz) / rz);
                    if (d > 1 || (y < hollowTop && x * x + z * z < hollowR * hollowR)) {
                        continue;
                    }
                    if (d > 0.5 && rng.nextDouble() < erode * (d - 0.35) * 2) {
                        continue;
                    }
                    leaf(x, y, z, block);
                }
            }
        }
    }

    // -- finishing pass ---------------------------------------------------------------------------------------

    /**
     * Works out the vanilla leaf distance of every leaf; leaves that would decay (distance 7) are never placed.
     * (The trees are built from wood blocks, bark on every face, so no log ends show anywhere.)
     */
    Shape finish() {
        return distances(true);
    }

    /**
     * Like {@link #finish()}, but every leaf stays, however far it is from wood: the leaves are placed persistent
     * (like leaves a player sets) and never decay.
     */
    Shape finishPersistent() {
        persistent = true;
        return distances(false);
    }

    private Shape distances(boolean prune) {
        ArrayDeque<BlockPos> queue = new ArrayDeque<>();
        Map<BlockPos, Integer> dist = new HashMap<>();
        cells.forEach((p, c) -> {
            if (c.kind() == Kind.LOG) {
                dist.put(p, 0);
                queue.add(p);
            }
        });
        while (!queue.isEmpty()) {
            BlockPos p = queue.poll();
            int d = dist.get(p);
            if (d >= 6) {
                continue;
            }
            for (Direction dir : Direction.values()) {
                BlockPos n = p.relative(dir);
                Cell c = cells.get(n);
                if (c != null && c.kind() == Kind.LEAF && !dist.containsKey(n)) {
                    dist.put(n, d + 1);
                    queue.add(n);
                }
            }
        }
        if (prune) {
            cells.entrySet().removeIf(e -> e.getValue().kind() == Kind.LEAF && !dist.containsKey(e.getKey()));
        }
        cells.forEach((p, c) -> {
            if (c.kind() == Kind.LEAF) {
                leafDistance.put(p, dist.getOrDefault(p, 7));
            }
        });
        return this;
    }

    // -- helpers ----------------------------------------------------------------------------------------------

    private static void line(double[] a, double[] b, Consumer<BlockPos> put) {
        double dx = b[0] - a[0], dy = b[1] - a[1], dz = b[2] - a[2];
        int steps = Math.max(1, (int) Math.ceil(Math.max(Math.abs(dx), Math.max(Math.abs(dy), Math.abs(dz))) * 3));
        BlockPos prev = null;
        for (int i = 0; i <= steps; i++) {
            double t = (double) i / steps;
            BlockPos p = ip(a[0] + dx * t, a[1] + dy * t, a[2] + dz * t);
            if (prev != null && !p.equals(prev)) {
                // Fill diagonal moves (y first, then x, then z) so the chain stays face connected.
                int[] cur = {prev.getX(), prev.getY(), prev.getZ()};
                int[] to = {p.getX(), p.getY(), p.getZ()};
                for (int k : new int[]{1, 0, 2}) {
                    if (cur[k] != to[k]) {
                        cur[k] = to[k];
                        BlockPos c = new BlockPos(cur[0], cur[1], cur[2]);
                        if (!c.equals(p)) {
                            put.accept(c);
                        }
                    }
                }
            }
            put.accept(p);
            prev = p;
        }
    }

    private static Direction.Axis dominant(double[] a, double[] b) {
        double dx = Math.abs(b[0] - a[0]), dy = Math.abs(b[1] - a[1]), dz = Math.abs(b[2] - a[2]);
        if (dx >= dy && dx >= dz) {
            return Direction.Axis.X;
        }
        return dy >= dz ? Direction.Axis.Y : Direction.Axis.Z;
    }

    private static double sq(double v) {
        return v * v;
    }
}
