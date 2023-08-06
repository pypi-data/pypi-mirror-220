from asyncio import get_running_loop
from pathlib import Path
from typing import (
    Literal,
    NamedTuple,
)

from textual import on
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Container, ScrollableContainer
from textual.events import MouseDown, Resize
from textual.reactive import reactive
from textual.screen import ModalScreen
from textual.widget import Widget
from textual.widgets import Footer, Markdown, OptionList, Static
from textual.widgets.option_list import Option
from watchfiles import awatch

from potoo.parse import parse_documents

Slide = tuple[str, ...]


class SlideCounter(NamedTuple):
    slide: int
    fragment: int


class PresentationFooter(Widget):
    progress = reactive(1)
    total = reactive(0)

    def update(self, *, total: int | None = None, progress: int | None = None) -> None:
        if total is not None:
            self.total = total
        if progress is not None:
            self.progress = progress

    def render(self) -> str:
        return f"{self.progress} / {self.total}"


class SlideNavigator(ModalScreen[int | None]):
    BINDINGS = [
        ("escape", "dismiss(None)"),
        ("q", "dismiss(None)"),
        # VIM movements inside optionlist
        ("j", "cursor_down"),
        ("k", "cursor_up"),
    ]

    def action_cursor_down(self):
        self.query_one(OptionList).action_cursor_down()

    def action_cursor_up(self):
        self.query_one(OptionList).action_cursor_up()

    def __init__(self, current_slide_index: int, slide_headings: list[str]) -> None:
        self.current_slide_index = current_slide_index
        self.slide_headings = slide_headings
        super().__init__()

    def compose(self) -> ComposeResult:
        yield Static("[b]Choose slide to jump to[/b] (esc/q to close)")
        option_list = OptionList(
            *[Option(first_line) for first_line in self.slide_headings]
        )
        option_list.highlighted = self.current_slide_index
        yield option_list

    @on(OptionList.OptionSelected)
    def slide_selected(self, event: OptionList.OptionSelected):
        self.dismiss(event.option_index)


class PauseScreen(ModalScreen[None]):
    BINDINGS = [("full_stop", "unpause", "Unpause")]

    @on(MouseDown)
    def action_unpause(self) -> None:
        self.app.pop_screen()

    def on_mount(self):
        # increase default alpha value to hide presentation content nearly completely
        self.styles.background = self.styles.background.with_alpha(0.95)

    def compose(self) -> ComposeResult:
        yield Static("Press `.` or click anywhere to continue")


class Potoo(App):
    CSS_PATH = "potoo.css"
    BINDINGS = [
        # slide navigation
        Binding("p,k,backspace", "change_slide('prev')", "Previous", show=False),
        Binding("left", "change_slide('prev')", "Previous", show=True),
        Binding("n,j,space", "change_slide('next')", "Next", show=False),
        Binding("right", "change_slide('next')", "Next", show=True),
        # scrolling shortcuts
        Binding("ctrl+d", "scroll('down')", "Scroll down", show=False),
        Binding("ctrl+u", "scroll('up')", "Scroll up", show=False),
        # additional bindings
        Binding("?", "display_help", "Help"),
        Binding("d", "toggle_dark", "Toggle Dark mode"),
        Binding("o", "slide_navigator", "Overview"),
        Binding("full_stop", "pause", "Toggle Pause"),
    ]

    slide_counter = reactive(SlideCounter(0, 0))
    show_help_footer = reactive(False)

    def __init__(
        self,
        document_path: Path,
        header_split_level: int,
        create_fragments: bool,
        static_footer_center: str | None = None,
        hot_reload: bool = False,
    ) -> None:
        self.document_path = document_path
        slides, presentation_meta = parse_documents(
            document_path, header_split_level, create_fragments
        )
        self.header_split_level = header_split_level
        self.create_fragments = create_fragments
        self.slides = slides
        self.presentation_meta = presentation_meta
        self.static_footer_center = static_footer_center or ""
        self.number_of_slides = len(self.slides)
        self.hot_reload = hot_reload
        super().__init__()

    async def reload_on_document_update(self):
        while True:
            async for _ in awatch(self.document_path):
                new_slides, presentation_meta = parse_documents(
                    self.document_path,
                    self.header_split_level,
                    self.create_fragments,
                )
                slide, _ = self.slide_counter
                current_slide_modified = self.slides[slide] != new_slides[slide]
                self.slides = new_slides
                self.watch_slide_counter(self.slide_counter)
                self.notify(
                    f"Current slide modified: {current_slide_modified}",
                    title="Slides reloaded",
                    severity="information",
                )

    def on_mount(self) -> None:
        if title := self.presentation_meta.get("title"):
            self.title = title
        if self.hot_reload:
            self.reload_on_change_task = get_running_loop().create_task(
                self.reload_on_document_update()
            )
            self.notify(
                f"Watching [i]{self.document_path}[/i] for changes",
                title="Task started",
                severity="information",
            )

    def action_scroll(self, direction: Literal["up", "down"]) -> None:
        if direction == "up":
            self.query(ScrollableContainer).only_one().scroll_up()
        elif direction == "down":
            self.query(ScrollableContainer).only_one().scroll_down()

    def action_pause(self) -> None:
        self.push_screen(PauseScreen())

    def action_slide_navigator(self) -> None:
        def handle_slide_change(new_slide_index: int | None) -> None:
            if new_slide_index is not None:
                self.slide_counter = SlideCounter(new_slide_index, 0)

        self.push_screen(
            SlideNavigator(
                self.slide_counter.slide,
                [slide[0].strip().splitlines()[0] for slide in self.slides],
            ),
            handle_slide_change,
        )

    def action_change_slide(
        self, action: Literal["next", "prev", "first", "last"] | int
    ) -> None:
        if isinstance(action, int):
            self.slide_counter = SlideCounter(action, 0)
            return
        slide, fragment = self.slide_counter
        if action == "first":
            self.slide_counter = SlideCounter(0, 0)
        elif action == "last":
            last_slide_index = self.number_of_slides - 1
            self.slide_counter = SlideCounter(
                last_slide_index, len(self.slides[last_slide_index]) - 1
            )
        elif action == "next":
            self.slide_counter = SlideCounter(slide, fragment + 1)
        elif action == "prev":
            self.slide_counter = SlideCounter(slide, fragment - 1)

    def action_display_help(self) -> None:
        self.show_help_footer = not self.show_help_footer

    def watch_show_help_footer(self, show: bool) -> None:
        self.query_one(Footer).display = show

    def validate_slide_counter(self, new_slide_counter: SlideCounter) -> SlideCounter:
        match new_slide_counter:
            # 'prev' on first slide
            case (0, -1):
                return SlideCounter(0, 0)
            # Switch to previous slide
            case (slide, -1):
                new_slide_index = slide - 1
                return SlideCounter(
                    new_slide_index, len(self.slides[new_slide_index]) - 1
                )
            case (slide, fragment) if fragment >= len(self.slides[slide]):
                if slide + 1 >= self.number_of_slides:
                    # Ensures that we do not go past the last slide
                    return SlideCounter(slide, fragment - 1)
                return SlideCounter(slide + 1, 0)
            case (slide, fragment) if slide >= self.number_of_slides:
                return SlideCounter(self.number_of_slides - 1, fragment)
            case _:
                return SlideCounter(*new_slide_counter)

    def watch_slide_counter(self, new_slide_counter: SlideCounter) -> None:
        slide, fragment = new_slide_counter
        self.query_one(PresentationFooter).update(
            progress=slide + 1, total=len(self.slides)
        )
        self.query_one(Markdown).update("\n".join(self.slides[slide][: fragment + 1]))

    @on(Resize)
    def dynamic_margin(self, event: Resize) -> None:
        size = event.size
        self.query_one("#slides").styles.margin = int(size.height / 10), int(
            size.width / 10
        )

    def compose(self) -> ComposeResult:
        yield Container(
            ScrollableContainer(Markdown(id="slides")),
            Container(
                Static(self.presentation_meta.get("title", "No title")),
                Static(self.static_footer_center, id="footer-center"),
                PresentationFooter(id="slide-counter"),
                id="footer",
            ),
        )
        yield Footer()
