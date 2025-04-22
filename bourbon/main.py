import asyncio
import logging
import sys
import uuid

import uvloop
from textual import log, work
from textual.app import App, ComposeResult
from textual.color import Gradient
from textual.containers import Horizontal, Vertical
from textual.logging import TextualHandler
from textual.reactive import reactive
from textual.theme import Theme
from textual.widgets import Footer, Header, Input, Markdown, ProgressBar

logging.basicConfig(
    level="DEBUG",
    handlers=[TextualHandler()],
)


from bourbon.models.types import MacOS
from bourbon.widgets.computer_deets import ComputerDeets

trial_uuid = uuid.uuid4()
trial_uuid2 = uuid.uuid4()
trial_state = str("running")

TREE_LABELS = [
    "name",
    "mac_os",
    "memory",
    "status",
    "public_ip",
]

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
    mac_os: reactive[MacOS] = reactive(MacOS, recompose=True)

    def __init__(self, new_mac: MacOS):
        super().__init__()
        self.mac_os = MacOS.model_validate(new_mac)

    def compose(self) -> ComposeResult:
        gradient = Gradient.from_colors(
            "#881177",
            "#aa3355",
            "#cc6666",
            "#ee9944",
            "#eedd00",
            "#99dd55",
            "#44dd88",
            "#22ccbb",
            "#00bbcc",
            "#0099cc",
            "#3366bb",
            "#663399",
        )
        yield Header(show_clock=True, icon="🥃🥃🥃")
        with Horizontal(id="data-inputs"):
            with Vertical():
                yield Input(placeholder="enter name", name="name")
                yield Input(placeholder="enter IP", name="public_ip")
                yield Input(placeholder="enter status", name="status")
                yield Input(placeholder="enter memory", name="memory")
                yield Input(placeholder="enter operating system", name="mac_os")
        with Horizontal(id="data-tree"):
            yield ComputerDeets(self.mac_os).data_bind(mac_os=BourbonApp.mac_os)
        with Horizontal(id="progress-bar"):
            yield ProgressBar(total=100, gradient=gradient)
        yield Footer()

    async def on_input_submitted(self, event: Input.Submitted) -> None:
        log("Input Submitted")
        self.update_mac_os(str(event.input.name), event.input.value)

    def key_space(self):
        self.query_one(ProgressBar).advance(5)

    @work(exclusive=True)
    async def update_mac_os(self, name: str, value: str):
        if name and value:
            setattr(self.mac_os, name, value)
            self.mutate_reactive(BourbonApp.mac_os)
        else:
            self.notify("Error")

    def on_mount(self) -> None:
        self._register(aquamarine_theme)
        self.theme = "aquamarine"


# -----
# -----
# -----
# -----
# -----
async def main():
    app = BourbonApp(STARTER_MAC)
    await app.run_async()


asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
runner = asyncio.Runner(loop_factory=uvloop.new_event_loop)
runner.run(main())
# -----
# -----
# -----
# if sys.version_info >= (3, 11):
#     with asyncio.Runner(loop_factory=uvloop.new_event_loop) as runner:
#         runner.run(app.run())
