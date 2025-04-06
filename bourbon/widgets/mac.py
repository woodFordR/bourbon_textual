from typing import List, Tuple
from uuid import uuid4

from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.reactive import reactive
from textual.widgets import Tree

from bourbon.models.types import MacOS

default_uuid = uuid4()
default_state = "stopped"


class Mac(Horizontal):

    # state_box: reactive[List[Tuple[UUID, str]]] = reactive(List[Tuple[default_uuid, str(default_state)]])
    mac_os: reactive[MacOS] = reactive(MacOS)

    def __init__(self, new_mac: MacOS) -> None:
        super().__init__()
        if MacOS:
            self.mac_os = MacOS.model_validate(new_mac)

    def compose(self) -> ComposeResult:
        tree: Tree[str] = Tree(f"{self.mac_os.name}")
        tree.root.expand()
        characters = tree.root.add("data", expand=True)
        characters.add_leaf(str(self.mac_os.mac_os))
        characters.add_leaf(str(self.mac_os.memory))
        characters.add_leaf(str(self.mac_os.status))
        characters.add_leaf(str(self.mac_os.public_ip))
        yield tree
