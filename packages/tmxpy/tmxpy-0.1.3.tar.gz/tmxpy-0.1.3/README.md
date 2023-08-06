# TMXpy

A Python library for reading and writing TMX files.

This library is fairly computer intensive, especially when rendering large maps. It is recommended to use a computer with decent specs when using this library.

## Features

- Rendering of TMX files to images (CSV encoding only)

## Installation

```bash
pip install tmxpy
```

## Usage

```python
from tmxpy import TMXpy
from pathlib import Path

tmx = TMXpy(sheets=[Path("path/to/tilesheet/directory")], path=Path("path/to/tmx/file"))
tmx.generateGIDDict()
tmx.renderAllLayers().save("path/to/output/image.png")
```

## Development/Testing

- Install dependencies with `pip install -r requirements.txt`
- Tests can be added to tests/name_of_test.py and run with `py -m tests.name_of_test`
- It can be built with `py -m build`