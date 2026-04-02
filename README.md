# IPyPlot

IPyPlot renders notebook-friendly HTML galleries for image datasets.

## Installation

```bash
pip install ipyplot
```

## Representative Examples

`plot_images` accepts flat image sequences, `dict[str, sequence]` inputs for named tabs, and nested sequences that render as tabs by default or as fixed comparison grids with `nested_layout="grid"`. Image entries can be local paths, remote URLs, `PIL.Image` objects, `numpy.ndarray`s, or `(image, label)` tuples.

### Flat gallery with labels and per-image annotations

```python
import ipyplot

images = ["cat-1.jpg", "dog-1.jpg", "cat-2.jpg"]
labels = ["cat", "dog", "cat"]
scores = ["p=0.99", "p=0.94", "p=0.87"]

ipyplot.plot_images(
    images,
    labels=labels,
    custom_texts=scores,
    img_width=150,
    max_images=20,
)
```

### Named tabs from a dictionary

```python
images_by_group = {
    "cats": ["cat-1.jpg", "cat-2.jpg"],
    "dogs": ["dog-1.jpg", "dog-2.jpg"],
    "nature": ["tree-1.jpg", "lake-1.jpg"],
}

ipyplot.plot_images(images_by_group, img_width=150)
```

### Fixed comparison grid from nested lists

```python
comparison_rows = [
    ["baseline/cat.jpg", "baseline/dog.jpg"],
    ["model-a/cat.jpg", "model-a/dog.jpg"],
    ["model-b/cat.jpg"],
]

ipyplot.plot_images(
    comparison_rows,
    labels=["baseline", "model-a", "model-b"],
    nested_layout="grid",
    show_url=False,
    img_width=150,
)
```

### Per-image display labels with tuples

```python
images = [
    ("cat-1.jpg", "Whiskers"),
    ("cat-2.jpg", "Mittens"),
    ("dog-1.jpg", "Buddy"),
]

ipyplot.plot_images(images, img_width=150)
```

### Group a dataset into class tabs

```python
images = ["cat-1.jpg", "dog-1.jpg", "cat-2.jpg", "fox-1.jpg"]
labels = ["cat", "dog", "cat", "fox"]

ipyplot.plot_class_tabs(
    images,
    labels,
    max_imgs_per_tab=8,
    tabs_order=["cat", "dog", "fox"],
    img_width=150,
)
```

### Show one representative image per class

```python
images = ["cat-1.jpg", "dog-1.jpg", "cat-2.jpg", "fox-1.jpg", "unknown-1.jpg"]
labels = ["cat", "dog", "cat", "fox", "unknown"]

ipyplot.plot_class_representations(
    images,
    labels,
    ignore_labels=["unknown"],
    labels_order=["cat", "dog", "fox"],
    img_width=150,
)
```

### Use base64 when the notebook cannot reach the local cache server (don't use this unless it's necessary)

```python
local_files = ["cat-1.jpg", "dog-1.jpg", "cat-2.jpg"]

ipyplot.plot_images(local_files, img_width=150, force_b64=True)
```

### Configure the local image server for remote notebooks

```python
local_files = ["cat-1.jpg", "dog-1.jpg", "cat-2.jpg"]

ipyplot.configure_server(
    host="0.0.0.0",
    public_host="my-notebook.example.com",
)

ipyplot.plot_images(local_files, img_width=150)
```
