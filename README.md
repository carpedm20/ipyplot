# IPyPlot

IPyPlot renders notebook-friendly HTML galleries for image datasets.

## Installation

```bash
pip install git+https://github.com/carpedm20/ipyplot
```

## Representative Examples

`plot_images` accepts flat image sequences, `dict[str, sequence]` inputs for named tabs, and nested sequences that render as tabs by default or as fixed comparison grids with `nested_layout="grid"`. Image entries can be local paths, remote URLs, `PIL.Image` objects, `numpy.ndarray`s, or `(image, label)` tuples.

### Flat gallery with labels and per-image annotations

```python
import ipyplot

images = [
    "https://cdn-images.farfetch-contents.com/22/48/94/73/22489473_52451907_1000.jpg",
    "https://img.ssensemedia.com/images/f_jpg,c_limit,h_1024,w_1024/251331F069004_3/luu-dan-blue-side-zip-jeans.jpg",
    "https://cdn-images.farfetch-contents.com/16/48/68/50/16486850_32134463_1000.jpg",
]
labels = ["bags", "bottom", "dress"]
scores = ["source=farfetch", "source=ssense", "source=farfetch"]

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
    "bags": [
        "https://cdn-images.farfetch-contents.com/20/71/24/20/20712420_50859668_1000.jpg",
        "https://cdn-images.farfetch-contents.com/28/32/03/71/28320371_57706802_1000.jpg",
    ],
    "bottom": [
        "https://image.msscdn.net/images/prd_img/20210827/2094408/detail_2094408_3_500.jpg",
        "https://image.msscdn.net/images/prd_img/20230314/3147045/detail_3147045_17188565971180_500.jpg",
    ],
    "headwear": [
        "https://image.msscdn.net/images/prd_img/20230417/3238702/detail_3238702_16868957666567_500.jpg",
        "https://image.msscdn.net/images/prd_img/20240822/4358640/detail_4358640_17243106444853_500.jpg",
    ],
}

ipyplot.plot_images(images_by_group, img_width=150)
```

### Fixed comparison grid from nested lists

Grid mode renders the outer list as rows and each inner list as cells
within that row. Use `row_labels=` for per-row titles (left side) and
`column_labels=` for column headers across the top. Read the grid the
same way you'd read a spreadsheet: row = category/item, column = variant.

```python
# rows = product categories, columns = providers we want to compare.
comparison_rows = [
    [
        "https://cdn-images.farfetch-contents.com/24/24/49/50/24244950_54244583_1000.jpg",
        "https://image.msscdn.net/images/prd_img/20250228/4845168/detail_4845168_17422706902028_500.jpg",
    ],
    [
        "https://cdn-images.farfetch-contents.com/27/46/98/07/27469807_57275019_1000.jpg",
        "https://image.msscdn.net/images/goods_img/20210414/1898014/1898014_1_500.jpg",
    ],
    [
        "https://cdn-images.farfetch-contents.com/22/48/94/73/22489473_52451907_1000.jpg",
    ],
]

ipyplot.plot_images(
    comparison_rows,
    row_labels=["bottoms", "tops", "bags"],
    column_labels=["farfetch", "ssense"],
    nested_layout="grid",
    show_url=False,
    img_width=150,
)
```

> The older `labels=` kwarg still works as an alias for `row_labels` when
> `nested_layout="grid"` is set — keeping existing notebooks compatible.
> Prefer the explicit `row_labels` / `column_labels` kwargs in new code so
> the grid axes are obvious at the call site.

### Per-image display labels with tuples

```python
images = [
    ("https://cdn-images.farfetch-contents.com/22/48/94/73/22489473_52451907_1000.jpg", "Bags Example"),
    ("https://image.msscdn.net/images/prd_img/20250228/4845168/detail_4845168_17422706902028_500.jpg", "Bottom Example"),
    ("https://cdn-images.farfetch-contents.com/16/48/68/50/16486850_32134463_1000.jpg", "Dress Example"),
]

ipyplot.plot_images(images, img_width=150)
```

### Group a dataset into class tabs

```python
images = [
    "https://cdn-images.farfetch-contents.com/20/71/24/20/20712420_50859668_1000.jpg",
    "https://image.msscdn.net/images/prd_img/20210827/2094408/detail_2094408_3_500.jpg",
    "https://cdn-images.farfetch-contents.com/24/24/49/50/24244950_54244583_1000.jpg",
    "https://image.msscdn.net/images/prd_img/20230417/3238702/detail_3238702_16868957666567_500.jpg",
]
labels = ["bags", "bottom", "bags", "headwear"]

ipyplot.plot_class_tabs(
    images,
    labels,
    max_imgs_per_tab=8,
    tabs_order=["bags", "bottom", "headwear"],
    img_width=150,
)
```

### Show one representative image per class

```python
images = [
    "https://cdn-images.farfetch-contents.com/20/71/24/20/20712420_50859668_1000.jpg",
    "https://image.msscdn.net/images/prd_img/20240221/3887672/detail_3887672_17084957329879_500.jpg",
    "https://cdn-images.farfetch-contents.com/16/48/68/50/16486850_32134463_1000.jpg",
    "https://image.msscdn.net/images/prd_img/20191112/1221714/detail_1221714_17239720854482_500.jpg",
    "https://cdn-images.farfetch-contents.com/28/32/03/71/28320371_57706802_1000.jpg",
]
labels = ["bags", "outerwear", "dress", "rings", "unknown"]

ipyplot.plot_class_representations(
    images,
    labels,
    ignore_labels=["unknown"],
    labels_order=["bags", "outerwear", "dress", "rings"],
    img_width=150,
)
```

### Use base64 when the notebook cannot reach the local cache server (don't use this unless it's necessary)

```python
local_files = [
    "https://cdn-images.farfetch-contents.com/20/71/24/20/20712420_50859668_1000.jpg",
    "https://image.msscdn.net/images/prd_img/20250228/4845168/detail_4845168_17422706902028_500.jpg",
    "https://cdn-images.farfetch-contents.com/16/48/68/50/16486850_32134463_1000.jpg",
]

ipyplot.plot_images(local_files, img_width=150, force_b64=True)
```

### Configure the local image server for remote notebooks

```python
local_files = [
    "https://cdn-images.farfetch-contents.com/22/48/94/73/22489473_52451907_1000.jpg",
    "https://image.msscdn.net/images/prd_img/20230417/3238702/detail_3238702_16868957666567_500.jpg",
    "https://cdn-images.farfetch-contents.com/24/24/49/50/24244950_54244583_1000.jpg",
]

ipyplot.configure_server(
    host="0.0.0.0",
    public_host="my-notebook.example.com",
)

ipyplot.plot_images(local_files, img_width=150)
```
