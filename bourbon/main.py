import uuid

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

    mac_os: reactive[MacOS] = reactive(MacOS)

    def __init__(self, new_mac: MacOS):
        self.mac_os = MacOS.model_validate(new_mac)

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True, icon="🥃")
        yield Input(placeholder="enter name", name="name")
        yield Input(placeholder="enter IP", name="public_ip")
        yield Input(placeholder="enter status", name="status")
        yield Input(placeholder="enter memory", name="memory")
        yield Input(placeholder="enter operating system", name="mac_os")
        with VerticalScroll(id="response-container"):
            yield Markdown(id="response")
        with Horizontal(id="data-tree"):
            yield Mac(new_mac).data_bind(BourbonApp.mac_os)
        yield Footer()

    async def on_input_submitted(self, event: Input.Submitted, input: Input) -> None:
        if input.Submitted.value:
            await self.update_mac_os(str(input.name) or "", input.Submitted.value)
        else:
            await self.query_one("#response", Markdown).update(f"you suck.")

    async def update_mac_os(self, name: str, value: str):
        setattr(self.mac_os, name, value)


if __name__ == "__main__":
    app = BourbonApp(new_mac)
    app.run()
