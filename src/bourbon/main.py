import asyncio
import logging
import uuid

import uvloop
from textual import log, work
from textual.app import App, ComposeResult
from textual.containers import Center, Horizontal, Vertical
from textual.logging import TextualHandler
from textual.reactive import reactive
from textual.theme import Theme
from textual.widgets import Footer, Header, Input, TabbedContent, TabPane

from bourbon.models.types import MacOS
from bourbon.widgets.computer_deets import ComputerDeets
from bourbon.widgets.styled_progress_bar import StyledProgressBar

logging.basicConfig(
    level="DEBUG",
    handlers=[TextualHandler()],
)

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

trial_uuid = uuid.uuid4()
trial_uuid2 = uuid.uuid4()
trial_state = str("running")


STARTER_MAC = MacOS(
    id=trial_uuid2,
    name="Capybara",
    public_ip="127.5.5.5",
    status="running",
    memory=32,
    mac_os="Sequoia 15.3.2",
)


aquamarine_theme = Theme(
    name="aquamarine",
    primary="#88C0D0",
    secondary="#81A1C1",
    accent="#B48EAD",
    foreground="#D8DEE9",
    background="#2E3440",
    success="#A3BE8C",
    warning="#EBCB8B",
    error="#BF616A",
    surface="#3B4252",
    panel="#434C5E",
    dark=True,
    variables={
        "block-cursor-text-style": "none",
        "footer-key-foreground": "#88C0D0",
        "input-selection-background": "#81a1c1 35%",
    },
)


class BourbonApp(App):

    CSS_PATH = "bourbon.tcss"
    mac_os: reactive[MacOS] = reactive(MacOS)

    def __init__(self, new_mac: MacOS):
        super().__init__()
        self.mac_os = MacOS.model_validate(new_mac)

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True, icon="🥃🥃🥃")
        with TabbedContent(f"tabbed-content-{self.mac_os.id}"):
            with TabPane(f"tab-pane-{self.mac_os.name}"):
                with Horizontal(id=f"horizontal-{self.mac_os.name}"):
                    # yield StyledProgressBar(disable=True)
                    yield ComputerDeets(self.mac_os)
            with TabPane(f"tab-pane-progress-bar"):
                with Horizontal(id="horizontal-progress-bar"):
                    yield StyledProgressBar(disable=True)
        yield Footer()

    def on_computer_deets_deets_changed(
        self, event: ComputerDeets.DeetsChanged
    ) -> None:
        self.log("Input Submitted")
        self.notify("Loading ...")
        self.log(event)

    def on_mount(self) -> None:
        self.register_theme(aquamarine_theme)
        self.theme = "aquamarine"


if __name__ == "__main__":
    app: App = BourbonApp(STARTER_MAC)
    app.run()
