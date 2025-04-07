import uuid

from textual import log
from textual.app import App, ComposeResult
from textual.containers import Horizontal, VerticalScroll
from textual.reactive import reactive
from textual.widgets import Footer, Header, Input, Markdown

from bourbon.models.types import MacOS
from bourbon.widgets.mac import Mac

trial_uuid = uuid.uuid4()
trial_state = str("running")

new_mac = MacOS(
    name="Capybara",
    public_ip="127.5.5.5",
    status="running",
    memory=32,
    mac_os="Sequoia 15.3.2",
)


class BourbonApp(App):

    CSS_PATH = "bourbon.tcss"
    mac_os: reactive[MacOS] = reactive(MacOS)

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
            yield Mac(new_mac).data_bind(mac_os=BourbonApp.mac_os)
        yield Footer()

    async def on_input_submitted(self, event: Input.Submitted) -> None:
        log("Input Submitted")
        if event.input.value:
            await self.update_mac_os(str(event.input.name) or "", event.input.value)
        else:
            await self.query_one("#response", Markdown).update(f"you empty.")

    async def update_mac_os(self, name: str, value: str):
        if name and value:
            log("Input Updating")
            setattr(self.mac_os, name, value)
            self.mutate_reactive(BourbonApp.mac_os)
        else:
            self.notify("Error")


if __name__ == "__main__":
    app = BourbonApp(new_mac)
    app.run()
