package greektrees;

import com.mojang.serialization.Codec;
import com.mojang.serialization.MapCodec;
import com.mojang.serialization.codecs.RecordCodecBuilder;

import net.minecraft.core.BlockPos;
import net.minecraft.tags.BlockTags;
import net.minecraft.world.level.BlockGetter;
import net.minecraft.world.level.block.SaplingBlock;
import net.minecraft.world.level.block.grower.TreeGrower;
import net.minecraft.world.level.block.state.BlockState;

/** A vanilla sapling with its own tree; the date palm may also be planted on sand. */
public class GreekSaplingBlock extends SaplingBlock {
    public static final MapCodec<GreekSaplingBlock> CODEC = RecordCodecBuilder.mapCodec(i -> i.group(
            TreeGrower.CODEC.fieldOf("tree").forGetter(b -> b.treeGrower),
            Codec.BOOL.fieldOf("grows_on_sand").forGetter(b -> b.growsOnSand),
            propertiesCodec()).apply(i, GreekSaplingBlock::new));

    private final boolean growsOnSand;

    public GreekSaplingBlock(TreeGrower treeGrower, boolean growsOnSand, Properties properties) {
        super(treeGrower, properties);
        this.growsOnSand = growsOnSand;
    }

    @Override
    public MapCodec<? extends GreekSaplingBlock> codec() {
        return CODEC;
    }

    @Override
    protected boolean mayPlaceOn(BlockState state, BlockGetter level, BlockPos pos) {
        return super.mayPlaceOn(state, level, pos) || (growsOnSand && state.is(BlockTags.SAND));
    }
}
