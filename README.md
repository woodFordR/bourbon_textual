## The Bourbon 🥃 Textual App
---
---
## Woodford <woody@woodford.life>
---
---
### Application Development
 - creation of a python textual application
 - sqlmodel with typing for read, update models
 - simple input and tree widgets with horizontal containers
---

---
### How to run
 - `uv python --managed-python install 3.13.3`
 - `uv python pin 3.13.3`
 - `uv venv -p 3.13`
 - `source .venv/bin/activate`
 - `uv pip install -U pip`
 - `uv pip install -r pyproject.toml --all-extras`
 - `uv pip install -r pyproject.toml --group=dev`
---

---
### `pyproject.toml` needs
- [build-system]
- requires = ["setuptools", "wheel", "pip"]
- build-backend = "setuptools.build_meta"
---

---
### Running Application
 - `uv run -- textual run --dev src/bourbon/main.py`
---

