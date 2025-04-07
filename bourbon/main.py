import uuid

from textual import log
from textual.app import App, ComposeResult
from textual.containers import Horizontal, VerticalScroll
from textual.reactive import reactive
from textual.widgets import Footer, Header, Input, Markdown, Tree

from bourbon.models.types import MacOS
from bourbon.widgets.mac import Mac

trial_uuid = uuid.uuid4()
trial_state = str("running")

STARTER_MAC = MacOS(
    name="Capybara",
    public_ip="127.5.5.5",
    status="running",
    memory=32,
    mac_os="Sequoia 15.3.2",
)


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
            yield Mac(self.mac_os).data_bind(mac_os=BourbonApp.mac_os)
        yield Footer()

    async def on_input_submitted(self, event: Input.Submitted) -> None:
        log("Input Submitted")
        await self.update_mac_os(str(event.input.name), event.input.value)

    async def update_mac_os(self, name: str, value: str):
        if name and value:
            log("Input Updating")

            log("query of tree")
            tree = self.query_one(Tree)
            for x in tree.children:
                log(x)

            old_mac = self.mac_os.model_dump
            setattr(self.mac_os, name, value)
            log("Tree directory and old mac")
            log(tree.tree.__dir__())
            log("OLD_MAC")
            log(old_mac)
            log("NEW_MAC")
            log(self.mac_os)
            self.mutate_reactive(BourbonApp.mac_os)
        else:
            self.notify("Error")


if __name__ == "__main__":
    app = BourbonApp(STARTER_MAC)
    app.run()
