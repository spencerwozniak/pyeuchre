# pyeuchre

One of my first ever Python projects. I built this in **September 2020** while I was first learning Python and playing euchre every night my freshman year of college.

The codebase was recently refactored and upgraded with much better coding conventions (clearer structure, modules like `card`, `deck`, `game`, `players`, and `display`, and improved style).

**Run it:** `python main.py`

## Repo Structure
```bash
pyeuchre/
├── euchre/              # package (all game code)
│   ├── __init__.py
│   ├── constants.py
│   ├── card.py
│   ├── deck.py
│   ├── display.py
│   └── game.py
└── main.py              # entry point: runs the game
```