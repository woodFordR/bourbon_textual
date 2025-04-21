import logging
import uuid

from textual import log, work
from textual.app import App, ComposeResult
from textual.containers import Horizontal, VerticalScroll
from textual.logging import TextualHandler
from textual.reactive import reactive
from textual.theme import Theme
from textual.widgets import Footer, Header, Input, Markdown

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


# arctic_theme = Theme(
#     name="aquamarine",
#     primary="#88C0D0",
#     secondary="#81A1C1",
#     accent="#B48EAD",
#     foreground="#D8DEE9",
#     background="#2E3440",
#     success="#A3BE8C",
#     warning="#EBCB8B",
#     error="#BF616A",
#     surface="#3B4252",
#     panel="#434C5E",
#     dark=True,
#     variables={
#         "block-cursor-text-style": "none",
#         "footer-key-foreground": "#88C0D0",
#         "input-selection-background": "#81a1c1 35%",
#     },
# )
#


class BourbonApp(App):

    CSS_PATH = "bourbon.tcss"
    mac_os: reactive[MacOS] = reactive(MacOS, recompose=True)

    def __init__(self, new_mac: MacOS):
        super().__init__()
        self.mac_os = MacOS.model_validate(new_mac)

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True, icon="🥃🥃🥃")
        yield Input(placeholder="enter name", name="name")
        yield Input(placeholder="enter IP", name="public_ip")
        yield Input(placeholder="enter status", name="status")
        yield Input(placeholder="enter memory", name="memory")
        yield Input(placeholder="enter operating system", name="mac_os")
        with VerticalScroll(id="response-container"):
            yield Markdown(id="response")
        with Horizontal(id="data-tree"):
            yield ComputerDeets(self.mac_os).data_bind(mac_os=BourbonApp.mac_os)
        yield Footer()

    async def on_input_submitted(self, event: Input.Submitted) -> None:
        log("Input Submitted")
        self.update_mac_os(str(event.input.name), event.input.value)

    @work(exclusive=True)
    async def update_mac_os(self, name: str, value: str):
        if name and value:
            setattr(self.mac_os, name, value)
            self.mutate_reactive(BourbonApp.mac_os)
        else:
            self.notify("Error")


if __name__ == "__main__":
    app = BourbonApp(STARTER_MAC)
    app.run()
