[![Build](https://github.com/karolzak/ipyplot/workflows/CI%20Build/badge.svg)](https://github.com/karolzak/ipyplot/actions?query=workflow%3A%22CI+Build%22)
[![PyPI - version](https://img.shields.io/pypi/v/ipyplot.svg "PyPI version")](https://pypi.org/project/ipyplot/)
[![Downloads](https://pepy.tech/badge/ipyplot)](https://pepy.tech/project/ipyplot)
[![Downloads/Month](https://pepy.tech/badge/ipyplot/month)](https://pepy.tech/project/ipyplot/month)
[![license](https://img.shields.io/github/license/mashape/apistatus.svg?maxAge=2592000)](https://github.com/karolzak/ipyplot/blob/master/LICENSE)

# IPyPlot

Fast, interactive image plotting for Python notebooks using IPython + HTML.

![](https://raw.githubusercontent.com/karolzak/ipyplot/master/docs/example1-tabs.gif)

## Installation

```bash
pip install ipyplot
```

## Quick Start

```python
import ipyplot
```

### Plot a flat list of images

```python
images = ["cat1.jpg", "cat2.jpg", "dog1.jpg", "dog2.jpg"]
ipyplot.plot_images(images, img_width=150)
```

![](https://raw.githubusercontent.com/karolzak/ipyplot/master/docs/example2-images.jpg)

### Plot with labels

```python
images = ["cat1.jpg", "cat2.jpg", "dog1.jpg"]
labels = ["cat", "cat", "dog"]
ipyplot.plot_images(images, labels=labels, img_width=150)
```

### Custom per-image labels with tuples

`(image, label)` tuples display the label and hide the URL:

```python
images = [
    ("cat1.jpg", "Whiskers"),
    ("cat2.jpg", "Mittens"),
    ("dog1.jpg", "Buddy"),
]
ipyplot.plot_images(images, img_width=150)
```

You can mix tuples and plain images — tuples show custom labels, plain images show URLs:

```python
images = [
    ("cat1.jpg", "Custom Label"),  # shows "Custom Label", no URL
    "dog1.jpg",                     # shows URL
]
ipyplot.plot_images(images, img_width=150)
```

### Dict of image lists (automatic tabs)

```python
images = {
    "Cats": ["cat1.jpg", "cat2.jpg", "cat3.jpg"],
    "Dogs": ["dog1.jpg", "dog2.jpg"],
    "Nature": ["nature1.jpg", "nature2.jpg"],
}
ipyplot.plot_images(images, img_width=150)
```

### List of lists as tabs

```python
images = [cats, dogs, nature]
ipyplot.plot_images(images, labels=["Cats", "Dogs", "Nature"], img_width=150)
```

### List of lists as a fixed grid

Each inner list is a row. Shorter rows get empty-cell placeholders:

```python
images = [
    ["row1_a.jpg", "row1_b.jpg", "row1_c.jpg"],
    ["row2_a.jpg", "row2_b.jpg"],
    ["row3_a.jpg", "row3_b.jpg", "row3_c.jpg", "row3_d.jpg"],
]
ipyplot.plot_images(
    images,
    labels=["Row 1", "Row 2", "Row 3"],
    nested_layout='grid',
    img_width=150,
)
```

### Tabs and grid with tuple labels

```python
# Dict with tuple labels
images = {
    "Cats": [("cat1.jpg", "Whiskers"), ("cat2.jpg", "Mittens")],
    "Dogs": [("dog1.jpg", "Buddy"), ("dog2.jpg", "Max")],
}
ipyplot.plot_images(images, img_width=150)

# Grid with tuple labels
images = [
    [("cat1.jpg", "Cat 1"), ("cat2.jpg", "Cat 2")],
    [("dog1.jpg", "Dog 1"), ("dog2.jpg", "Dog 2"), ("dog3.jpg", "Dog 3")],
]
ipyplot.plot_images(images, labels=["Cats", "Dogs"], nested_layout='grid', img_width=120)
```

### PIL images and numpy arrays

```python
from PIL import Image
import numpy as np

pil_images = [Image.open(p) for p in ["cat1.jpg", "cat2.jpg"]]
ipyplot.plot_images(pil_images, img_width=150)

np_images = [np.array(img) for img in pil_images]
ipyplot.plot_images(np_images, img_width=150)
```

### Interactive class tabs

```python
ipyplot.plot_class_tabs(images, labels, max_imgs_per_tab=10, img_width=150)
```

![](https://raw.githubusercontent.com/karolzak/ipyplot/master/docs/example1-tabs.gif)

### Class representations (first image per class)

```python
ipyplot.plot_class_representations(images, labels, img_width=150)
```

![](https://raw.githubusercontent.com/karolzak/ipyplot/master/docs/example3-classes.jpg)

## Supported image formats

| Format | Example |
|---|---|
| Local file paths | `["img/cat.jpg", "img/dog.jpg"]` |
| Remote URLs | `["https://example.com/cat.jpg"]` |
| `PIL.Image` objects | `[Image.open("cat.jpg")]` |
| `numpy.ndarray` | `[np.array(img)]` |
| `(image, label)` tuples | `[("cat.jpg", "Whiskers")]` |

Sequences can be `list`, `numpy.ndarray`, or `pandas.Series`.

## Nested structures in `plot_images`

| Input | Behavior |
|---|---|
| `dict` of image lists | Tabs with dict keys as tab names |
| List of lists (default) | Tabs — each inner list is a tab |
| List of lists + `nested_layout='grid'` | Fixed grid — each inner list is a row |

## Local file server & caching

On `import ipyplot` a lightweight HTTP server starts, serving files from `~/.ipyplot/`. Local paths are copied there and in-memory images (PIL/numpy) are cached by content hash, so HTML uses compact HTTP URLs instead of base64 payloads.

The server **binds** to `0.0.0.0` by default but generated HTML URLs point to `127.0.0.1`. Configure both independently:

```python
import ipyplot

# Check current URL used in HTML
ipyplot.get_server_url()          # "http://127.0.0.1:39876"

# Change the public hostname (used in HTML src attributes)
ipyplot.set_public_host("my-server.example.com")

# Change the bind address / port (restarts the server)
ipyplot.set_server_host("0.0.0.0")
ipyplot.set_server_port(41000)

# Or configure everything at once
ipyplot.configure_server(host="0.0.0.0", port=41000, public_host="my-server.example.com")
```

## Features

- Grid, tabs, and fixed-grid layouts
- Click-to-zoom on any image
- `custom_texts` for per-image annotations (e.g. confidence scores)
- `force_b64` flag for environments that can't reach the local server (e.g. Google Colab)
- `show_url=False` to hide URLs
- `max_images` / `img_width` to control display
- "show html" button to inspect generated markup
- Tab ordering & filtering via `tabs_order`
- Works on Jupyter, Google Colab, Azure Notebooks, Kaggle

## More examples

See [gear-images-examples.ipynb](https://github.com/karolzak/ipyplot/blob/master/notebooks/gear-images-examples.ipynb) for more complex scenarios.
