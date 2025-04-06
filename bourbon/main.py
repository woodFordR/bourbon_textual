import uuid

from textual.app import App, ComposeResult
from textual.containers import Horizontal, VerticalScroll
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

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True, icon="🥃")
        yield Footer()
        yield Input(placeholder="enter a word", id="word-enter")
        with VerticalScroll(id="response-container"):
            yield Markdown(id="response")
        with Horizontal(id="data-tree"):
            yield Mac(new_mac)

    async def on_input_changed(self, message: Input.Changed) -> None:
        if message.value:
            await self.query_one("#response", Markdown).update(
                f"{message.value} sucks."
            )
        else:
            await self.query_one("#response", Markdown).update(f"you suck.")


if __name__ == "__main__":
    app = BourbonApp()
    app.run()
