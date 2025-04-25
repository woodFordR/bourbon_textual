from textual.app import ComposeResult
from textual.color import Gradient
from textual.timer import Timer
from textual.widget import Widget
from textual.widgets import ProgressBar


class StyledProgressBar(Widget):

    timer: Timer

    def __init__(self, gradient: Gradient | None = None):
        super().__init__()
        if not gradient:
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
        self.gradient = gradient

    def compose(self) -> ComposeResult:
        yield ProgressBar(gradient=self.gradient)

    def on_mount(self) -> None:
        self.timer = self.set_interval(10, self.add_progress, pause=False)

    def add_progress(self) -> None:
        self.query_one(ProgressBar).advance(1)

    def start_timer(self) -> None:
        self.query_one(ProgressBar).update(total=100)
        self.timer.resume()
