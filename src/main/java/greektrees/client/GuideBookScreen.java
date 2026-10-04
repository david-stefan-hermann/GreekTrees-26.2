package greektrees.client;

import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

import greektrees.GreekTrees;
import greektrees.GuideBook;
import net.fabricmc.loader.api.FabricLoader;
import net.minecraft.client.gui.GuiGraphicsExtractor;
import net.minecraft.client.gui.components.Button;
import net.minecraft.client.gui.components.Tooltip;
import net.minecraft.client.gui.screens.Screen;
import net.minecraft.client.input.KeyEvent;
import net.minecraft.client.renderer.RenderPipelines;
import net.minecraft.client.resources.sounds.SimpleSoundInstance;
import net.minecraft.network.chat.Component;
import net.minecraft.network.chat.MutableComponent;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.util.FormattedCharSequence;
import net.minecraft.world.item.ItemStack;
import org.lwjgl.glfw.GLFW;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * The guide book: a blue panel with one marble-white page, the trees' tabs on the left and the other chapters' on the
 * right, arrows and the page number below. Everything is drawn with rectangles, no textures but the pictures. The
 * screen wraps the chapters' sections and breaks them into pages itself: a section that does not fit on the page
 * starts the next one, so no text can run off the page. Turned with the tabs, the arrows, the arrow and page keys or
 * the mouse wheel.
 */
public class GuideBookScreen extends Screen {
    private static final Logger LOGGER = LoggerFactory.getLogger(GreekTrees.MOD_ID);
    private static final int PANEL_W = 232, PANEL_H = 230;
    private static final int TAB_W = 26, TAB_H = 24, TAB_GAP = 3;
    private static final int PAGE_MARGIN = 8, TEXT_MARGIN = 6, HEADER_H = 20, FOOTER_H = 24;
    private static final int TEXT_W = PANEL_W - 2 * PAGE_MARGIN - 2 * TEXT_MARGIN;
    private static final int CONTENT_H = PANEL_H - 2 * PAGE_MARGIN - HEADER_H - FOOTER_H;
    private static final int SLOT_SIZE = 18;
    private static final int RECIPE_W = 3 * SLOT_SIZE + 6 + 13 + 6 + SLOT_SIZE; // grid, arrow, result

    private static final int PANEL = 0xFF3F74B8, BORDER = 0xFF000000, LIGHT = 0xFF9CC3EC, SHADOW = 0xFF234A80;
    private static final int TAB = 0xFF2F5C99, TAB_HOVER = 0xFF5A92D6;
    private static final int PAGE = 0xFFF4F1EA, PAGE_EDGE = 0xFFB9C4D2;
    private static final int TITLE = 0xFF1A3C78, HEADING = 0xFF2C60AA, BODY = 0xFF1E2430, LORE = 0xFF5A6478;
    private static final int SLOT = 0xFFE2E0D8, SLOT_EDGE = 0xFF9AA3B0, ARROW = 0xFF5F7FA8;
    private static final int BUTTON = 0xFF2C60AA, BUTTON_HOVER = 0xFF4A86D8, BUTTON_OFF = 0xFF6B7F9A,
            BUTTON_EDGE = 0xFF14305C, BUTTON_LIGHT = 0xFF8FBBEF, BUTTON_TEXT = 0xFFFFFFFF, BUTTON_TEXT_OFF = 0xFFC6D0DE;

    private static final Set<String> LOGGED = new HashSet<>();
    /** The page open when the book was last closed; this session only. */
    private static int lastPage;

    private final List<GuideBook.Chapter> chapters = GuideBook.chapters();
    /** Laid out in {@link #init}: every page with its chapter and its sections, each with its wrapped lines. */
    private final List<Page> pages = new ArrayList<>();
    private int page;
    private int left, top;
    private BookButton previous, next;
    private ItemStack hovered = ItemStack.EMPTY;
    private int mouseX, mouseY;

    private record Placed(GuideBook.Section section, List<FormattedCharSequence> lines, int height) {
    }

    private record Page(int chapter, List<Placed> sections) {
    }

    public GuideBookScreen() {
        this(lastPage);
    }

    public GuideBookScreen(int page) {
        super(Component.translatable("item.greektrees.guide_book"));
        this.page = Math.max(0, page);
    }

    /** Known once the screen is open: the pages depend on the font and the language. */
    public int pageCount() {
        return pages.size();
    }

    @Override
    protected void init() {
        left = (width - PANEL_W) / 2;
        top = Math.max(2, (height - PANEL_H) / 2);
        layOut();
        page = Math.min(page, pages.size() - 1);
        int trees = 0, others = 0;
        for (int i = 0; i < chapters.size(); i++) {
            boolean right = !chapters.get(i).tree();
            int row = right ? others++ : trees++;
            addRenderableWidget(new TabButton(right ? left + PANEL_W - 3 : left - TAB_W + 3,
                    top + 8 + row * (TAB_H + TAB_GAP), i, right));
        }
        int buttonY = top + PANEL_H - FOOTER_H + 2;
        previous = addRenderableWidget(new BookButton(left + PAGE_MARGIN, buttonY, 22, 18, Component.literal("<"),
                button -> turnTo(page - 1)));
        next = addRenderableWidget(new BookButton(left + PANEL_W - PAGE_MARGIN - 22, buttonY, 22, 18,
                Component.literal(">"), button -> turnTo(page + 1)));
        updateButtons();
    }

    /**
     * Breaks every chapter into pages: sections go onto a page until the next one would not fit. A heading never ends
     * a page: it moves over together with what follows it.
     */
    private void layOut() {
        pages.clear();
        StringBuilder count = new StringBuilder();
        for (int c = 0; c < chapters.size(); c++) {
            int first = pages.size();
            List<Placed> current = new ArrayList<>();
            int used = 0;
            List<GuideBook.Section> sections = chapters.get(c).sections();
            for (int i = 0; i < sections.size(); i++) {
                Placed placed = place(sections.get(i));
                int needed = placed.height();
                for (int j = i; j + 1 < sections.size() && sections.get(j) instanceof GuideBook.Heading; j++) {
                    needed += place(sections.get(j + 1)).height();
                }
                boolean turn = sections.get(i) instanceof GuideBook.Break || used + needed > CONTENT_H;
                if (turn && !current.isEmpty()) {
                    pages.add(new Page(c, current));
                    current = new ArrayList<>();
                    used = 0;
                }
                if (placed.height() > CONTENT_H) {
                    LOGGER.warn("BOOK OVERFLOW {} section {}: {} of {} pixels", chapters.get(c).title(), i,
                            placed.height(), CONTENT_H);
                }
                current.add(placed);
                used += placed.height();
            }
            pages.add(new Page(c, current));
            count.append(' ').append(chapters.get(c).title().substring(GuideBook.key("").length())).append('=')
                    .append(pages.size() - first);
        }
        String language = minecraft.getLanguageManager().getSelected();
        if (FabricLoader.getInstance().isDevelopmentEnvironment() && LOGGED.add(language)) {
            LOGGER.info("BOOK PAGES {}: {} pages,{}", language, pages.size(), count);
        }
    }

    private Placed place(GuideBook.Section section) {
        return switch (section) {
            case GuideBook.Heading heading -> text(section, Component.translatable(heading.key()), TEXT_W, 10, 5);
            case GuideBook.Text text -> text(section, Component.translatable(text.key()), TEXT_W, 9, 5);
            case GuideBook.Lore lore -> text(section, Component.translatable(lore.key())
                    .withStyle(s -> s.withItalic(true)), TEXT_W, 9, 5);
            case GuideBook.Dedication dedication -> text(section, Component.translatable(dedication.key()), TEXT_W, 9, 5);
            case GuideBook.ItemLine line -> {
                List<FormattedCharSequence> lines = font.split(Component.translatable(line.key(), line.args()),
                        TEXT_W - line.icons().size() * SLOT_SIZE - 2);
                yield new Placed(section, lines, Math.max(17, lines.size() * 9 + 1) + 4);
            }
            case GuideBook.Saplings saplings -> {
                MutableComponent text = Component.empty();
                for (String key : saplings.keys()) {
                    text.append(text.getSiblings().isEmpty() ? "" : " ").append(Component.translatable(key));
                }
                int grid = saplings.side() * SLOT_SIZE;
                List<FormattedCharSequence> lines = font.split(text, TEXT_W - grid - 6);
                yield new Placed(section, lines, Math.max(grid, lines.size() * 9) + 4);
            }
            case GuideBook.Recipe recipe -> new Placed(section, List.of(), 3 * SLOT_SIZE + 4);
            case GuideBook.Pictures pictures -> new Placed(section, List.of(), pictures.size() + 4);
            case GuideBook.Break turn -> new Placed(section, List.of(), 0);
        };
    }

    private Placed text(GuideBook.Section section, Component text, int width, int lineHeight, int gap) {
        List<FormattedCharSequence> lines = font.split(text, width);
        return new Placed(section, lines, lines.size() * lineHeight + gap);
    }

    private int firstPageOf(int chapter) {
        for (int i = 0; i < pages.size(); i++) {
            if (pages.get(i).chapter() == chapter) {
                return i;
            }
        }
        return 0;
    }

    private void turnTo(int target) {
        int clamped = Math.clamp(target, 0, pages.size() - 1);
        if (clamped != page) {
            minecraft.getSoundManager().play(SimpleSoundInstance.forUI(SoundEvents.BOOK_PAGE_TURN, 1.0f));
        }
        page = clamped;
        lastPage = page;
        updateButtons();
    }

    private void updateButtons() {
        previous.active = page > 0;
        next.active = page < pages.size() - 1;
    }

    @Override
    public boolean keyPressed(KeyEvent event) {
        switch (event.key()) {
            case GLFW.GLFW_KEY_LEFT, GLFW.GLFW_KEY_PAGE_UP -> turnTo(page - 1);
            case GLFW.GLFW_KEY_RIGHT, GLFW.GLFW_KEY_PAGE_DOWN -> turnTo(page + 1);
            default -> {
                return super.keyPressed(event);
            }
        }
        return true;
    }

    @Override
    public boolean mouseScrolled(double x, double y, double scrollX, double scrollY) {
        if (scrollY != 0) {
            turnTo(page + (scrollY > 0 ? -1 : 1));
        }
        return true;
    }

    @Override
    public boolean isPauseScreen() {
        return false;
    }

    @Override
    public void extractBackground(GuiGraphicsExtractor graphics, int mouseX, int mouseY, float partialTick) {
        super.extractBackground(graphics, mouseX, mouseY, partialTick);
        panel(graphics, left, top, PANEL_W, PANEL_H);
        int x0 = left + PAGE_MARGIN, y0 = top + PAGE_MARGIN;
        int x1 = left + PANEL_W - PAGE_MARGIN, y1 = top + PANEL_H - FOOTER_H;
        graphics.fill(x0 - 1, y0 - 1, x1 + 1, y1 + 1, PAGE_EDGE);
        graphics.fill(x0, y0, x1, y1, PAGE);
    }

    @Override
    public void extractRenderState(GuiGraphicsExtractor graphics, int mouseX, int mouseY, float partialTick) {
        this.mouseX = mouseX;
        this.mouseY = mouseY;
        hovered = ItemStack.EMPTY;
        Page current = pages.get(page);
        GuideBook.Chapter chapter = chapters.get(current.chapter());
        int x = left + PAGE_MARGIN + TEXT_MARGIN;
        int y = top + PAGE_MARGIN + 3;
        graphics.item(chapter.icon(), x, y);
        graphics.text(font, Component.translatable(chapter.title()), x + 20, y + 4, TITLE, false);
        graphics.fill(x, y + HEADER_H - 4, x + TEXT_W, y + HEADER_H - 3, PAGE_EDGE);

        int cursorY = top + PAGE_MARGIN + HEADER_H + 2;
        for (Placed placed : current.sections()) {
            List<FormattedCharSequence> lines = placed.lines();
            switch (placed.section()) {
                case GuideBook.Heading heading -> lines(graphics, lines, x, cursorY + 3, 10, HEADING);
                case GuideBook.Text text -> lines(graphics, lines, x, cursorY, 9, BODY);
                case GuideBook.Lore lore -> lines(graphics, lines, x, cursorY, 9, LORE);
                case GuideBook.Dedication dedication -> lines(graphics, lines, x, cursorY, 9, TITLE);
                case GuideBook.ItemLine line -> {
                    for (int i = 0; i < line.icons().size(); i++) {
                        item(graphics, line.icons().get(i), x + i * SLOT_SIZE, cursorY);
                    }
                    lines(graphics, lines, x + line.icons().size() * SLOT_SIZE + 2, cursorY + (lines.size() == 1 ? 4 : 0),
                            9, BODY);
                }
                case GuideBook.Saplings saplings -> {
                    int side = saplings.side();
                    for (int i = 0; i < side * side; i++) {
                        slot(graphics, new ItemStack(saplings.sapling()), x + i % side * SLOT_SIZE,
                                cursorY + i / side * SLOT_SIZE);
                    }
                    lines(graphics, lines, x + side * SLOT_SIZE + 6,
                            cursorY + Math.max(0, (side * SLOT_SIZE - lines.size() * 9) / 2), 9, BODY);
                }
                case GuideBook.Recipe recipe -> recipe(graphics, recipe, x + (TEXT_W - RECIPE_W) / 2, cursorY);
                case GuideBook.Pictures pictures -> {
                    int size = pictures.size(), texture = pictures.textureSize();
                    int px = x + (TEXT_W - pictures.textures().size() * (size + 8) + 8) / 2;
                    for (int i = 0; i < pictures.textures().size(); i++, px += size + 8) {
                        if (pictures.framed()) {
                            graphics.fill(px, cursorY, px + size, cursorY + size, PAGE_EDGE);
                            graphics.fill(px + 1, cursorY + 1, px + size - 1, cursorY + size - 1, PAGE);
                        }
                        graphics.blit(RenderPipelines.GUI_TEXTURED, pictures.textures().get(i), px, cursorY, 0, 0, size,
                                size, texture, texture, texture, texture);
                    }
                }
                case GuideBook.Break turn -> {
                }
            }
            cursorY += placed.height();
        }
        graphics.centeredText(font, Component.literal((page + 1) + " / " + pages.size()), left + PANEL_W / 2,
                top + PANEL_H - FOOTER_H + 7, BUTTON_TEXT);
        super.extractRenderState(graphics, mouseX, mouseY, partialTick);
        if (!hovered.isEmpty()) {
            graphics.setTooltipForNextFrame(font, hovered, mouseX, mouseY);
        }
    }

    // ---------------------------------------------------------------- pieces

    private void lines(GuiGraphicsExtractor graphics, List<FormattedCharSequence> lines, int x, int y, int lineHeight,
                       int colour) {
        for (FormattedCharSequence line : lines) {
            graphics.text(font, line, x, y, colour, false);
            y += lineHeight;
        }
    }

    /** A crafting grid, always three by three, an arrow and the result. */
    private void recipe(GuiGraphicsExtractor graphics, GuideBook.Recipe recipe, int x, int y) {
        for (int i = 0; i < 9; i++) {
            slot(graphics, recipe.grid().get(i), x + i % 3 * SLOT_SIZE, y + i / 3 * SLOT_SIZE);
        }
        int arrow = x + 3 * SLOT_SIZE + 6, mid = y + 3 * SLOT_SIZE / 2;
        graphics.fill(arrow, mid - 1, arrow + 9, mid + 1, ARROW);
        for (int i = 0; i < 4; i++) {
            graphics.fill(arrow + 9 + i, mid - 4 + i, arrow + 10 + i, mid + 4 - i, ARROW);
        }
        slot(graphics, recipe.result(), arrow + 13 + 6, mid - SLOT_SIZE / 2);
    }

    /** The one slot of the book, for recipes and sapling squares alike, so every grid looks the same. */
    private void slot(GuiGraphicsExtractor graphics, ItemStack stack, int x, int y) {
        graphics.fill(x, y, x + SLOT_SIZE, y + SLOT_SIZE, SLOT_EDGE);
        graphics.fill(x + 1, y + 1, x + SLOT_SIZE - 1, y + SLOT_SIZE - 1, SLOT);
        item(graphics, stack, x + 1, y + 1);
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

    /** Vanilla container panel: transparent corner pixels, 1 px black border, 2 px highlight, 2 px shadow. */
    private static void panel(GuiGraphicsExtractor graphics, int x0, int y0, int w, int h) {
        int x1 = x0 + w, y1 = y0 + h;
        graphics.fill(x0 + 1, y0 + 1, x1 - 1, y1 - 1, PANEL);
        graphics.fill(x0 + 2, y0, x1 - 2, y0 + 1, BORDER);
        graphics.fill(x0 + 2, y1 - 1, x1 - 2, y1, BORDER);
        graphics.fill(x0, y0 + 2, x0 + 1, y1 - 2, BORDER);
        graphics.fill(x1 - 1, y0 + 2, x1, y1 - 2, BORDER);
        graphics.fill(x0 + 1, y0 + 1, x0 + 2, y0 + 2, BORDER);
        graphics.fill(x1 - 2, y0 + 1, x1 - 1, y0 + 2, BORDER);
        graphics.fill(x0 + 1, y1 - 2, x0 + 2, y1 - 1, BORDER);
        graphics.fill(x1 - 2, y1 - 2, x1 - 1, y1 - 1, BORDER);
        graphics.fill(x0 + 2, y0 + 1, x1 - 3, y0 + 2, LIGHT);
        graphics.fill(x0 + 1, y0 + 2, x1 - 3, y0 + 3, LIGHT);
        graphics.fill(x0 + 1, y0 + 3, x0 + 3, y1 - 3, LIGHT);
        graphics.fill(x0 + 3, y0 + 3, x0 + 4, y0 + 4, LIGHT);
        graphics.fill(x0 + 3, y1 - 2, x1 - 2, y1 - 1, SHADOW);
        graphics.fill(x0 + 3, y1 - 3, x1 - 1, y1 - 2, SHADOW);
        graphics.fill(x1 - 3, y0 + 3, x1 - 1, y1 - 3, SHADOW);
        graphics.fill(x1 - 4, y1 - 4, x1 - 3, y1 - 3, SHADOW);
    }

    /** Vanilla button behaviour (click, focus, narration, tooltip) in the book's blue. */
    private class BookButton extends Button {
        BookButton(int x, int y, int w, int h, Component label, OnPress onPress) {
            super(x, y, w, h, label, onPress, DEFAULT_NARRATION);
        }

        @Override
        protected void extractContents(GuiGraphicsExtractor graphics, int mouseX, int mouseY, float partialTick) {
            int x0 = getX(), y0 = getY(), x1 = x0 + getWidth(), y1 = y0 + getHeight();
            graphics.fill(x0, y0, x1, y1, BUTTON_EDGE);
            graphics.fill(x0 + 1, y0 + 1, x1 - 1, y1 - 1, !active ? BUTTON_OFF : isHoveredOrFocused() ? BUTTON_HOVER : BUTTON);
            if (active) {
                graphics.fill(x0 + 1, y0 + 1, x1 - 1, y0 + 2, BUTTON_LIGHT);
            }
            graphics.fill(x0 + 1, y1 - 2, x1 - 1, y1 - 1, SHADOW);
            graphics.centeredText(font, getMessage(), (x0 + x1) / 2, y0 + (getHeight() - 8) / 2,
                    active ? BUTTON_TEXT : BUTTON_TEXT_OFF);
        }
    }

    /**
     * A chapter tab: the chapter's icon on a blue tab, the panel's colour and open towards it for the open chapter;
     * the title as tooltip.
     */
    private class TabButton extends BookButton {
        private final int chapter;
        private final boolean right;

        TabButton(int x, int y, int chapter, boolean right) {
            super(x, y, TAB_W, TAB_H, Component.translatable(chapters.get(chapter).title()),
                    button -> turnTo(firstPageOf(chapter)));
            this.chapter = chapter;
            this.right = right;
            setTooltip(Tooltip.create(getMessage()));
        }

        @Override
        protected void extractContents(GuiGraphicsExtractor graphics, int mouseX, int mouseY, float partialTick) {
            boolean open = pages.get(page).chapter() == chapter;
            int x0 = getX(), y0 = getY(), x1 = x0 + getWidth(), y1 = y0 + getHeight();
            graphics.fill(x0, y0, x1, y1, BORDER);
            graphics.fill(x0 + (open && right ? 0 : 1), y0 + 1, x1 - (open && !right ? 0 : 1), y1 - 1,
                    open ? PANEL : isHoveredOrFocused() ? TAB_HOVER : TAB);
            graphics.fill(x0 + 1, y0 + 1, x1 - 1, y0 + 2, LIGHT);
            graphics.item(chapters.get(chapter).icon(), x0 + 5, y0 + 4);
        }
    }
}
