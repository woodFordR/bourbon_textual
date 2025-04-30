from textual.widgets import Tree


class StyledTree(Tree):

    ICON_NODE = "⫸ "
    ICON_NODE_EXPANDED = "🢆 "

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
            id=id,
            classes=None,
            disabled=False,
        )
