package greektrees;

import greektrees.client.GuideBookScreen;
import net.fabricmc.api.ClientModInitializer;
import net.fabricmc.fabric.api.client.event.lifecycle.v1.ClientTickEvents;
import net.fabricmc.fabric.api.client.rendering.v1.EntityRendererRegistry;
import net.minecraft.client.Minecraft;
import net.minecraft.client.Screenshot;
import net.minecraft.client.renderer.entity.ThrownItemRenderer;

/** Client side: a thrown olive pit is drawn as its item, like a snowball; the guide book opens its screen. */
public final class GreekTreesClient implements ClientModInitializer {
    private static int shot = -1, wait;

    @Override
    public void onInitializeClient() {
        EntityRendererRegistry.register(GreekTrees.OLIVE_PIT_ENTITY, ThrownItemRenderer::new);
        GuideBookItem.setOpener(() -> Minecraft.getInstance().gui.setScreen(new GuideBookScreen()));
        if (System.getProperty("greektrees.bookshots") != null) {
            ClientTickEvents.END_CLIENT_TICK.register(GreekTreesClient::bookShots);
        }
    }

    /**
     * Dev only ({@code ./gradlew runClient -PbookShots}): once the player stands in the world, opens every page of the
     * guide book in turn, saves screenshots/book_&lt;language&gt;_gui&lt;scale&gt;_&lt;nr&gt;.png ten ticks later each
     * and quits.
     */
    private static void bookShots(Minecraft minecraft) {
        if (shot < 0) {
            if (minecraft.player == null || minecraft.gui.screen() != null || minecraft.gui.overlay() != null) {
                wait = 0;
            } else if (++wait >= 40) { // two seconds in the world, so it is drawn behind the book
                wait = 0;
                shot = 0;
                minecraft.gui.setScreen(new GuideBookScreen(0));
            }
            return;
        }
        if (++wait < 10 || !(minecraft.gui.screen() instanceof GuideBookScreen book)) {
            return;
        }
        wait = 0;
        Screenshot.grab(minecraft.gameDirectory, String.format("book_%s_gui%d_%02d.png",
                minecraft.getLanguageManager().getSelected(), minecraft.getWindow().getGuiScale(), shot),
                minecraft.gameRenderer.mainRenderTarget(), 1, message -> { });
        if (++shot < book.pageCount()) {
            minecraft.gui.setScreen(new GuideBookScreen(shot));
        } else {
            minecraft.stop();
        }
    }
}
