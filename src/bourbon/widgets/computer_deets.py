from uuid import uuid4

from textual import work
from textual.app import ComposeResult
from textual.color import Color, Gradient
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import ProgressBar, Tree

from bourbon.models.types import MacOS

default_uuid = uuid4()
default_state = "stopped"


class TopTree(Tree):

    ICON_NODE = "⫸ "
    ICON_NODE_EXPANDED = "⨈ "

    TREE_GUIDES: dict[str, tuple[str, str, str, str]] = {
        "default": (
            "    ",
            "  ─⫸",
            " ──⫸",
            "───⫸",
        ),
        "bold": (
            "    ",
            "  ━⫸",
            " ━━⫸",
            "━━━⫸",
        ),
        "double": (
            "    ",
            "  ═⫸",
            " ══⫸",
            "═══⫸",
        ),
    }

    def __init__(
        self,
        label,
        data=None,
        *,
        id,
    ) -> None:
        super().__init__(
            label=label,
            data=data,
            name=None,
            id=None,
            classes=None,
            disabled=False,
        )


class ComputerDeets(Widget):

    mac_os: reactive[MacOS] = reactive(MacOS, recompose=True)
    show_guides = reactive(True)
    show_root = reactive(True)

    def __init__(self, new_mac: MacOS) -> None:
        super().__init__()
        if MacOS:
            self.mac_os = MacOS.model_validate(new_mac)
            self.id = "computer_widget"
            self.TREE_LABELS = [
                f"a bourbon oaky mist",
                f"name: {self.mac_os.name}",
                f"selfie: {self.mac_os.mac_os}",
                f"memory: {self.mac_os.memory}GBs",
                f"status: {self.mac_os.status}",
                f"public ip: {self.mac_os.public_ip}",
            ]

    def compose(self) -> ComposeResult:
        tree = TopTree(
            id=f"tree_id_{str(self.mac_os.id)[0:4]}",
            label=self.TREE_LABELS[0],
        )
        tree.root.expand()
        tree.set_class(True, "box")
        characters = tree.root.add(label=self.TREE_LABELS[1], before=1, expand=True)
        characters.add(self.TREE_LABELS[2], before=2)
        characters.add(self.TREE_LABELS[3], before=3)
        characters.add(self.TREE_LABELS[4], before=4)
        characters.add(self.TREE_LABELS[5], before=5)
        yield tree

    @work(exclusive=True)
    async def watch_mac_os(self):
        # cubic-bezier(.4,.24,.09,1.57)
        for tree in self.query(TopTree):
            if tree:
                tree.styles.animate("opacity", value=0.5, duration=0.5)
                tree.styles.animate("opacity", 1.0, duration=0.5, delay=2.0)
                tree.styles.animate(
                    "background",
                    value="mediumvioletred",
                    final_value="lightslategray",
                    duration=2.0,
                )
