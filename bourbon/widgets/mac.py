import asyncio
import re
from typing import List, Tuple
from uuid import uuid4

from deepdiff import DeepDiff
from textual import log, work
from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.reactive import reactive
from textual.widgets import Tree
from textual.widgets.tree import TreeNode

from bourbon.models.types import MacOS

default_uuid = uuid4()
default_state = "stopped"


class Mac(Horizontal):

    # state_box: reactive[List[Tuple[UUID, str]]] = reactive(List[Tuple[default_uuid, str(default_state)]])
    mac_os: reactive[MacOS] = reactive(MacOS, recompose=True)

    def __init__(self, new_mac: MacOS) -> None:
        super().__init__()
        if MacOS:
            self.mac_os = MacOS.model_validate(new_mac)

    def compose(self) -> ComposeResult:
        tree: Tree[str] = Tree(f"{self.mac_os.name}")
        tree.root.expand()
        characters = tree.root.add("data", expand=True)
        characters.add_leaf(label=str("selfie: " + self.mac_os.mac_os), data="mac_os")
        characters.add_leaf(
            label=f"memory: {str(self.mac_os.memory)}GBs", data="memory"
        )
        characters.add_leaf(label=str("status: " + self.mac_os.status), data="status")
        characters.add_leaf(
            label=str("public ip: " + self.mac_os.public_ip), data="public_ip"
        )
        yield tree

    async def update_tree_leaf(self, field: str | None):
        if not field:
            return None
        log("update_tree_leaf")
        log(field)
        tree_leaf = self.query()
        # if tree_leaf.styles.background == "black 10%":
        #     tree_leaf.set_styles.background = "green 10%"
        # if tree_leaf.styles.background == "green 10%":
        #     tree_leaf.set_styles.background = "black 10%"
        # else:
        #     tree_leaf.set_styles.background = "black 10%"
        self.toggle_class("in-progress")
        await asyncio.sleep(3)
        tree_leaf.toggle_class("in-progress")
        # tree_leaf.label.styles.animate("backgroundcolor", value="green", duration=2.0)
        self.log("COMPLETE!!!")

    @work
    async def watch_mac_os(self, old_mac, new_mac):
        diffs = DeepDiff(old_mac, new_mac)

        await self.update_tree_leaf("name")

        if "values_changed" in diffs.keys():
            attrs = diffs["values_changed"]
            for k in attrs.keys():
                field_re = re.search("root.(.*)", k)
                field = field_re.group(1)
                if field:
                    await self.update_tree_leaf(field)
            return None

    # def on_mount(self) -> None:
    #     self.set_interval(1, self.watch_mac_os)
