from rich.progress import BarColumn, Progress
from rich.style import Style
from textual.color import Gradient
from textual.timer import Timer
from textual.widgets import Static


class StyledProgressBar(Static):
    timer: Timer

    def __init__(self):
        super().__init__()
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
        style = Style(color="green")
        style_1 = Style(color="blue")
        self._bar = Progress(BarColumn(style=style, pulse_style=style_1))
        self._bar.add_task("", total=None)

    def on_mount(self) -> None:
        self.update_render = self.set_interval(1 / 60, self.add_progress)

    def add_progress(self) -> None:
        self.update(self._bar)
