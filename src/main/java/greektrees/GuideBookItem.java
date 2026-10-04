package greektrees;

import com.mojang.serialization.Codec;
import net.fabricmc.fabric.api.attachment.v1.AttachmentRegistry;
import net.fabricmc.fabric.api.attachment.v1.AttachmentType;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.Level;

/**
 * The guide book: every tree, its recipe, how to plant it and its fruit, in its own screen (the content is
 * {@link GuideBook}). The client sets the screen opener; on a dedicated server the item does nothing. Every player
 * gets one book once, the first time they join after the mod is installed.
 */
public class GuideBookItem extends Item {
    /** Set once the player has had the book; kept through death (vanilla entity tags are not). */
    public static final AttachmentType<Boolean> GOT_BOOK = AttachmentRegistry.create(GreekTrees.id("got_guide_book"),
            b -> b.persistent(Codec.BOOL).copyOnDeath());

    private static Runnable opener = () -> {
    };

    public GuideBookItem(Properties properties) {
        super(properties);
    }

    /** Set by the client entry point: opens the book screen. */
    public static void setOpener(Runnable clientOpener) {
        opener = clientOpener;
    }

    @Override
    public InteractionResult use(Level level, Player player, InteractionHand hand) {
        if (level.isClientSide()) {
            opener.run();
        }
        return InteractionResult.SUCCESS;
    }

    /** The welcome gift: the book, once per player. */
    public static void giveBookOnce(ServerPlayer player) {
        if (player.hasAttached(GOT_BOOK)) {
            return;
        }
        ItemStack book = new ItemStack(GreekTrees.GUIDE_BOOK);
        if (!player.getInventory().add(book)) {
            player.drop(book, false);
        }
        player.setAttached(GOT_BOOK, true);
    }
}
