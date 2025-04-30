from uuid import uuid4

from textual import on, work
from textual.app import ComposeResult
from textual.containers import Center, Horizontal, Vertical
from textual.message import Message
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Input

from bourbon.models.types import MacOS
from bourbon.widgets.styled_tree import StyledTree

default_uuid = uuid4()
default_state = "stopped"

OLD_TREE_LABELS = [
    "name",
    "mac_os",
    "memory",
    "status",
    "public_ip",
]


class ComputerDeets(Widget):

    class DeetsChanged(Message):
        def __init__(self, name: str, value: str | int):
            super().__init__()
            self.name = name
            self.value = value

    mac_os: reactive[MacOS] = reactive(MacOS, recompose=True)
    show_guides = reactive(True)
    show_root = reactive(True)

    def __init__(self, new_mac: MacOS) -> None:
        super().__init__()
        if MacOS:
            self.mac_os = new_mac.model_copy()
            self.id = f"computer-deets-{new_mac.id}"
            self.TREE_LABELS = [
                f"title: a bourbon oaky mist",
                f"name: ",
                f"selfie: ",
                f"memory: ",
                f"status: ",
                f"public ip: ",
            ]
            self.log(
                "Tree data: ",
                mac_os=self.mac_os,
                id=self.id,
                tree_labels=self.TREE_LABELS,
            )

    def compose(self) -> ComposeResult:
        tree = StyledTree(
            id=f"tree-id-{str(self.mac_os.id)[0:4]}",
            label=self.TREE_LABELS[0],
        )
        tree.root.expand()
        tree.set_class(True, "box")
        characters = tree.root.add(
            label=f"{self.TREE_LABELS[1]}{self.mac_os.name}", before=1, expand=True
        )
        characters.add(f"{self.TREE_LABELS[2]}{self.mac_os.public_ip}", before=2)
        characters.add(f"{self.TREE_LABELS[3]}{self.mac_os.status}", before=3)
        characters.add(f"{self.TREE_LABELS[4]}{self.mac_os.memory}MiBs", before=4)
        characters.add(f"{self.TREE_LABELS[5]}{self.mac_os.mac_os}", before=5)
        self.log("Constructing Tree: ...", tree=tree)

        with Vertical():
            yield Input(placeholder="enter name", name="name")
            yield Input(placeholder="enter IP", name="public_ip")
            yield Input(placeholder="enter status", name="status")
            yield Input(placeholder="enter memory", name="memory")
            yield Input(placeholder="enter operating system", name="mac_os")
        with Vertical():
            yield tree

    @on(Input.Submitted)
    def handle_input_submit(self, event: Input.Submitted):
        if event.input and event.input.name:
            self.post_message(self.DeetsChanged(event.input.name, event.input.value))
            self.update_mac_os(str(event.input.name), event.input.value)

    @work(exclusive=True)
    async def watch_mac_os(self):
        # cubic-bezier(.4,.24,.09,1.57)
        for tree in self.query(StyledTree):
            if tree:
                tree.styles.animate("opacity", value=0.5, duration=0.5)
                tree.styles.animate("opacity", 1.0, duration=0.5, delay=2.0)
                tree.styles.animate(
                    "background",
                    value="mediumvioletred",
                    final_value="lightslategray",
                    duration=2.0,
                )
            self.refresh()

    @work(exclusive=True)
    async def update_mac_os(self, name: str, value: str):
        if name and value:
            self.log(self.mac_os)
            setattr(self.mac_os, name, value)
            self.log(self.mac_os)
            self.mutate_reactive(ComputerDeets.mac_os)
        else:
            self.notify("Error")
