package greektrees.client;

import java.util.HashSet;
import java.util.List;
import java.util.Set;

import greektrees.GreekTrees;
import greektrees.GuideBook;
import net.minecraft.client.gui.GuiGraphicsExtractor;
import net.minecraft.client.gui.screens.Screen;
import net.minecraft.client.gui.screens.inventory.PageButton;
import net.minecraft.client.input.KeyEvent;
import net.minecraft.client.input.MouseButtonEvent;
import net.minecraft.client.renderer.RenderPipelines;
import net.minecraft.client.resources.sounds.SimpleSoundInstance;
import net.minecraft.network.chat.Component;
import net.minecraft.network.chat.MutableComponent;
import net.minecraft.resources.Identifier;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.util.FormattedCharSequence;
import net.minecraft.world.item.ItemStack;
import org.lwjgl.glfw.GLFW;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * The guide book, open as a spread of two parchment pages (the cover alone on the first spread). Every kind of spread
 * has a fixed layout; a page whose content runs past its foot logs {@code BOOK OVERFLOW} once, which is how a text
 * that grew too long shows up. Turned with the arrows below the book, the arrow and page keys or the mouse wheel; a
 * click on the cover opens it, a click on a contents line turns to that page.
 */
public class GuideBookScreen extends Screen {
    private static final Logger LOGGER = LoggerFactory.getLogger(GreekTrees.MOD_ID);
    private static final int W = 312, H = 196, PAGE_W = 156, MARGIN = 12, TEXT_W = 132, PAGE_H = 172;
    private static final int PICTURE = 96, PICTURE_TEXTURE = 192;
    private static final int ROW = 14; // a line of the contents
    private static final int INK = 0xFF3B2A1A, HEADING = 0xFF2C60AA, SLOT = 0xFFDCCAA0, SLOT_EDGE = 0xFFA08A62,
            ARROW = 0xFF8A6A40;
    private static final Identifier SPREAD = GreekTrees.id("textures/gui/book/spread.png");
    private static final Identifier COVER = GreekTrees.id("textures/gui/book/cover.png");
    private static final Set<String> OVERFLOWS_LOGGED = new HashSet<>();
    /** The spread open when the book was last closed; this session only, the first opening shows the cover. */
    private static int lastSpread;

    private final List<GuideBook.Spread> spreads = GuideBook.spreads();
    private int spread;
    private int left, top;
    private PageButton back, forward;
    private ItemStack hovered = ItemStack.EMPTY;
    private int mouseX, mouseY;

    public GuideBookScreen() {
        this(lastSpread);
    }

    public GuideBookScreen(int spread) {
        super(Component.translatable("item.greektrees.guide_book"));
        this.spread = Math.clamp(spread, 0, spreads.size() - 1);
    }

    public int spreadCount() {
        return spreads.size();
    }

    @Override
    protected void init() {
        left = (width - W) / 2;
        top = Math.max(2, (height - H - 15) / 2); // the arrows sit below the book
        back = addRenderableWidget(new PageButton(left, top + H + 2, false, b -> turnTo(spread - 1, false), true));
        forward = addRenderableWidget(new PageButton(left + W - 23, top + H + 2, true, b -> turnTo(spread + 1, false), true));
        updateButtons();
    }

    private void turnTo(int target, boolean sound) {
        int clamped = Math.clamp(target, 0, spreads.size() - 1);
        if (clamped != spread && sound) {
            minecraft.getSoundManager().play(SimpleSoundInstance.forUI(SoundEvents.BOOK_PAGE_TURN, 1.0f));
        }
        spread = clamped;
        lastSpread = spread;
        updateButtons();
    }

    private void updateButtons() {
        back.visible = spread > 0;
        forward.visible = spread < spreads.size() - 1;
        forward.setX(spread == 0 ? left + (W + PAGE_W) / 2 - 23 : left + W - 23); // under the cover's corner
    }

    @Override
    public boolean keyPressed(KeyEvent event) {
        switch (event.key()) {
            case GLFW.GLFW_KEY_LEFT, GLFW.GLFW_KEY_PAGE_UP -> turnTo(spread - 1, true);
            case GLFW.GLFW_KEY_RIGHT, GLFW.GLFW_KEY_PAGE_DOWN -> turnTo(spread + 1, true);
            default -> {
                return super.keyPressed(event);
            }
        }
        return true;
    }

    @Override
    public boolean mouseScrolled(double x, double y, double scrollX, double scrollY) {
        if (scrollY != 0) {
            turnTo(spread + (scrollY > 0 ? -1 : 1), true);
        }
        return true;
    }

    @Override
    public boolean mouseClicked(MouseButtonEvent event, boolean doubleClick) {
        if (super.mouseClicked(event, doubleClick)) {
            return true;
        }
        if (event.button() != GLFW.GLFW_MOUSE_BUTTON_LEFT) {
            return false;
        }
        int x = (int) event.x(), y = (int) event.y();
        switch (spreads.get(spread)) {
            case GuideBook.Cover cover -> {
                int x0 = left + (W - PAGE_W) / 2;
                if (x >= x0 && x < x0 + PAGE_W && y >= top && y < top + H) {
                    turnTo(1, true);
                    return true;
                }
            }
            case GuideBook.Contents contents -> {
                int entry = entryAt(contents, x, y);
                if (entry >= 0) {
                    turnTo(contents.entries().get(entry).spread(), true);
                    return true;
                }
            }
            default -> {
            }
        }
        return false;
    }

    private int entryAt(GuideBook.Contents contents, int x, int y) {
        int x0 = left + MARGIN, y0 = top + MARGIN + ROW;
        if (x < x0 || x >= x0 + TEXT_W || y < y0) {
            return -1;
        }
        int i = (y - y0) / ROW;
        return i < contents.entries().size() ? i : -1;
    }

    @Override
    public boolean isPauseScreen() {
        return false;
    }

    @Override
    public void extractBackground(GuiGraphicsExtractor graphics, int mouseX, int mouseY, float partialTick) {
        super.extractBackground(graphics, mouseX, mouseY, partialTick);
        if (spreads.get(spread) instanceof GuideBook.Cover) {
            graphics.blit(RenderPipelines.GUI_TEXTURED, COVER, left + (W - PAGE_W) / 2, top, 0, 0, PAGE_W, H,
                    2 * PAGE_W, 2 * H, 2 * PAGE_W, 2 * H);
        } else {
            graphics.blit(RenderPipelines.GUI_TEXTURED, SPREAD, left, top, 0, 0, W, H, W, H);
        }
    }

    @Override
    public void extractRenderState(GuiGraphicsExtractor graphics, int mouseX, int mouseY, float partialTick) {
        this.mouseX = mouseX;
        this.mouseY = mouseY;
        hovered = ItemStack.EMPTY;
        int lx = left + MARGIN, rx = left + PAGE_W + MARGIN, y = top + MARGIN;
        switch (spreads.get(spread)) {
            case GuideBook.Cover cover -> {
            }
            case GuideBook.Contents contents -> {
                fits("left", contents(graphics, contents, lx, y));
                fits("right", heading(graphics, GuideBook.key("basics"), rx, y)
                        + text(graphics, Component.translatable(GuideBook.key("basics.text")), rx, y + 12, TEXT_W));
            }
            case GuideBook.Tree tree -> {
                fits("left", treeLeft(graphics, tree, lx, y));
                fits("right", treeRight(graphics, tree, rx, y));
            }
            case GuideBook.BigTrees big -> {
                fits("left", bigTree(graphics, big.left(), lx, y));
                fits("right", bigTree(graphics, big.right(), rx, y));
            }
            case GuideBook.Fruits fruits -> {
                fits("left", fruitsLeft(graphics, fruits, lx, y));
                fits("right", fruitsRight(graphics, fruits, rx, y));
            }
            case GuideBook.Pits pits -> {
                fits("left", heading(graphics, GuideBook.key("pits"), lx, y)
                        + text(graphics, Component.translatable(GuideBook.key("pits.text")), lx, y + 12, TEXT_W));
                int used = heading(graphics, GuideBook.key("heading.crafting"), rx, y);
                fits("right", used + recipe(graphics, pits.recipe(), rx, y + used));
            }
        }
        super.extractRenderState(graphics, mouseX, mouseY, partialTick);
        if (!hovered.isEmpty()) {
            graphics.setTooltipForNextFrame(font, hovered, mouseX, mouseY);
        }
    }

    /** Logs a page that runs past its foot, once per spread, page and language. */
    private void fits(String page, int used) {
        String language = minecraft.getLanguageManager().getSelected();
        if (used > PAGE_H && OVERFLOWS_LOGGED.add(spread + page + language)) {
            LOGGER.warn("BOOK OVERFLOW spread {} {} {}: {} of {} pixels", spread, page, language, used, PAGE_H);
        }
    }

    // ---------------------------------------------------------------- the spreads; each returns the height it used

    private int contents(GuiGraphicsExtractor graphics, GuideBook.Contents contents, int x, int y) {
        heading(graphics, GuideBook.key("contents"), x, y);
        int over = entryAt(contents, mouseX, mouseY);
        for (int i = 0; i < contents.entries().size(); i++) {
            GuideBook.Entry entry = contents.entries().get(i);
            int ry = y + ROW + i * ROW;
            item(graphics, entry.icon(), x, ry - 1);
            graphics.text(font, Component.translatable(entry.title()), x + 20, ry + 3, i == over ? HEADING : INK, false);
        }
        return ROW + contents.entries().size() * ROW;
    }

    /** Name, picture, description. */
    private int treeLeft(GuiGraphicsExtractor graphics, GuideBook.Tree tree, int x, int y) {
        int used = title(graphics, tree.title(), x, y);
        used += picture(graphics, tree.picture(), x, y + used);
        return used + text(graphics, Component.translatable(tree.about()), x, y + used, TEXT_W);
    }

    /** Recipe, planting, fruit (the Aries oak: its sixteen saplings), the line of lore at the foot. */
    private int treeRight(GuiGraphicsExtractor graphics, GuideBook.Tree tree, int x, int y) {
        int used = heading(graphics, GuideBook.key("heading.crafting"), x, y);
        used += recipe(graphics, tree.recipe(), x, y + used) + 4;
        used += heading(graphics, GuideBook.key("heading.planting"), x, y + used);
        used += text(graphics, Component.translatable(tree.planting()), x, y + used, TEXT_W) + 3;
        if (tree.square()) {
            int gx = x + (TEXT_W - 36) / 2;
            for (int i = 0; i < 16; i++) {
                smallItem(graphics, new ItemStack(tree.sapling()), gx + i % 4 * 9, y + used + i / 4 * 9);
            }
            used += 36 + 3;
        } else {
            used += heading(graphics, GuideBook.key("heading.fruit"), x, y + used);
            int icons = tree.fruits().size() * 18;
            for (int i = 0; i < tree.fruits().size(); i++) {
                item(graphics, tree.fruits().get(i), x + i * 18, y + used);
            }
            int textX = x + icons + (icons > 0 ? 2 : 0);
            int lines = text(graphics, Component.translatable(tree.fruit()), textX, y + used + (icons > 0 ? 1 : 0),
                    TEXT_W - (textX - x));
            used += Math.max(icons > 0 ? 18 : 0, lines) + 3;
        }
        List<FormattedCharSequence> lore = font.split(Component.translatable(tree.lore())
                .withStyle(s -> s.withItalic(true)), TEXT_W);
        int loreY = y + PAGE_H - lore.size() * 9;
        lines(graphics, lore, x, loreY);
        return used + 2 + lore.size() * 9;
    }

    /** Name, picture, the 2x2 saplings with the text beside them. */
    private int bigTree(GuiGraphicsExtractor graphics, GuideBook.BigTree tree, int x, int y) {
        int used = title(graphics, tree.title(), x, y);
        used += picture(graphics, tree.picture(), x, y + used);
        for (int i = 0; i < 4; i++) {
            item(graphics, new ItemStack(tree.sapling()), x + i % 2 * 17, y + used + i / 2 * 17);
        }
        MutableComponent text = Component.translatable(tree.about()).append(" ")
                .append(Component.translatable(GuideBook.key("big.square")));
        return used + Math.max(34, text(graphics, text, x + 38, y + used, TEXT_W - 38));
    }

    /** How fruit ripens and is picked, the olive's three stages. */
    private int fruitsLeft(GuiGraphicsExtractor graphics, GuideBook.Fruits fruits, int x, int y) {
        int used = heading(graphics, GuideBook.key("fruit"), x, y);
        used += text(graphics, Component.translatable(GuideBook.key("fruit.text")), x, y + used, TEXT_W) + 4;
        int sx = x + (TEXT_W - 3 * 32 - 2 * 8) / 2;
        for (int i = 0; i < fruits.stages().size(); i++) {
            graphics.blit(RenderPipelines.GUI_TEXTURED, fruits.stages().get(i), sx + i * 40, y + used, 0, 0, 32, 32,
                    16, 16, 16, 16);
        }
        return used + 32;
    }

    /** Every fruit: icon, name, hunger and tree. */
    private int fruitsRight(GuiGraphicsExtractor graphics, GuideBook.Fruits fruits, int x, int y) {
        int ry = y;
        for (GuideBook.FruitRow row : fruits.rows()) {
            item(graphics, row.fruit(), x, ry + 1);
            graphics.text(font, row.fruit().getHoverName(), x + 20, ry, INK, false);
            graphics.text(font, Component.translatable(GuideBook.key("fruit.row"), row.nutrition(),
                    Component.translatable(row.tree())), x + 20, ry + 9, INK, false);
            ry += 21;
        }
        return ry - y - 3;
    }

    // ---------------------------------------------------------------- pieces

    private int heading(GuiGraphicsExtractor graphics, String key, int x, int y) {
        graphics.text(font, Component.translatable(key), x, y, HEADING, false);
        return 12;
    }

    /** A name over the page's middle. */
    private int title(GuiGraphicsExtractor graphics, String key, int x, int y) {
        Component title = Component.translatable(key);
        graphics.text(font, title, x + (TEXT_W - font.width(title)) / 2, y, HEADING, false);
        return 12;
    }

    private int picture(GuiGraphicsExtractor graphics, Identifier picture, int x, int y) {
        graphics.blit(RenderPipelines.GUI_TEXTURED, picture, x + (TEXT_W - PICTURE) / 2, y, 0, 0, PICTURE, PICTURE,
                PICTURE_TEXTURE, PICTURE_TEXTURE, PICTURE_TEXTURE, PICTURE_TEXTURE);
        return PICTURE + 4;
    }

    /** Wrapped to {@code width}, in ink; returns the height of its lines. */
    private int text(GuiGraphicsExtractor graphics, Component text, int x, int y, int width) {
        List<FormattedCharSequence> lines = font.split(text, width);
        lines(graphics, lines, x, y);
        return lines.size() * 9;
    }

    private void lines(GuiGraphicsExtractor graphics, List<FormattedCharSequence> lines, int x, int y) {
        for (FormattedCharSequence line : lines) {
            graphics.text(font, line, x, y, INK, false);
            y += 9;
        }
    }

    /**
     * A crafting grid three slots wide and as many rows high as the recipe fills, an arrow and the result.
     */
    private int recipe(GuiGraphicsExtractor graphics, GuideBook.Recipe recipe, int x, int y) {
        int rows = 1;
        for (int i = 0; i < 9; i++) {
            if (!recipe.grid().get(i).isEmpty()) {
                rows = i / 3 + 1;
            }
        }
        int x0 = x + (TEXT_W - 94) / 2;
        for (int i = 0; i < rows * 3; i++) {
            int sx = x0 + i % 3 * 18, sy = y + i / 3 * 18;
            slot(graphics, sx, sy);
            item(graphics, recipe.grid().get(i), sx + 1, sy + 1);
        }
        int mid = y + rows * 9;
        graphics.fill(x0 + 58, mid - 1, x0 + 67, mid + 1, ARROW);
        for (int i = 0; i < 4; i++) {
            graphics.fill(x0 + 67 + i, mid - 4 + i, x0 + 68 + i, mid + 4 - i, ARROW);
        }
        slot(graphics, x0 + 76, mid - 9);
        item(graphics, recipe.result(), x0 + 77, mid - 8);
        return rows * 18;
    }

    private static void slot(GuiGraphicsExtractor graphics, int x, int y) {
        graphics.fill(x, y, x + 18, y + 18, SLOT_EDGE);
        graphics.fill(x + 1, y + 1, x + 17, y + 17, SLOT);
    }

    private void item(GuiGraphicsExtractor graphics, ItemStack stack, int x, int y) {
        if (stack.isEmpty()) {
            return;
        }
        graphics.item(stack, x, y);
        if (mouseX >= x && mouseX < x + 16 && mouseY >= y && mouseY < y + 16) {
            hovered = stack;
        }
    }

    /** At half size, eight pixels square. */
    private void smallItem(GuiGraphicsExtractor graphics, ItemStack stack, int x, int y) {
        graphics.pose().pushMatrix();
        graphics.pose().translate(x, y);
        graphics.pose().scale(0.5f, 0.5f);
        graphics.item(stack, 0, 0);
        graphics.pose().popMatrix();
        if (mouseX >= x && mouseX < x + 8 && mouseY >= y && mouseY < y + 8) {
            hovered = stack;
        }
    }
}
