import sys
from typing import Sequence

import os
import numpy as np
import pandas as pd
import pytest
from IPython.display import HTML
from PIL import Image

sys.path.append(".")
sys.path.append("../.")
import ipyplot


BASE_NP_IMGS = list(np.asarray(
    np.random.randint(0, 255, (3, 128, 128, 3)), dtype=np.uint8))

BASE_INTERNET_URLS = [
    "https://raw.githubusercontent.com/karolzak/boxdetect/master/images/checkbox-example.jpg",  # NOQA E501
    "https://raw.githubusercontent.com/karolzak/boxdetect/master/images/checkboxes-details.jpg",  # NOQA E501
    "https://raw.githubusercontent.com/karolzak/boxdetect/master/images/example1.png",  # NOQA E501
]

BASE_LOCAL_URLS = [
    "docs/example1-tabs.jpg",
    "docs/example2-images.jpg",
    "docs/example3-classes.jpg",
]

LOCAL_URLS_AS_PIL = list([Image.open(url) for url in BASE_LOCAL_URLS])

LABELS = [
    None,
    ['a', 'b', 'a'],
    np.asarray(['a', 'b', 'a']),
    pd.Series(['a', 'b', 'a'])
]

TEST_DATA = [
    # (imgs, labels, custom_texts)
    (LOCAL_URLS_AS_PIL, LABELS[1], LABELS[0]),
    (BASE_NP_IMGS, LABELS[1], LABELS[0]),
    (pd.Series(BASE_NP_IMGS), LABELS[1], LABELS[0]),
    (np.asarray(BASE_NP_IMGS), LABELS[1], LABELS[0]),
    (np.asarray(BASE_INTERNET_URLS), LABELS[1], LABELS[0]),
    (np.asarray(BASE_LOCAL_URLS), LABELS[1], LABELS[0]),
    (np.asarray(BASE_NP_IMGS, dtype=np.float32) / 255, LABELS[1], LABELS[0]),
    (LOCAL_URLS_AS_PIL, LABELS[0], LABELS[0]),
    (LOCAL_URLS_AS_PIL, LABELS[1], LABELS[1]),
    (LOCAL_URLS_AS_PIL, LABELS[2], LABELS[2]),
    (LOCAL_URLS_AS_PIL, LABELS[3], LABELS[3]),
    # test case for abs to rel path convertion
    ([os.path.abspath(pth) for pth in BASE_LOCAL_URLS], LABELS[1], LABELS[0]),
]


@pytest.fixture(params=[True, False])
def test_true_false(request):
    return request.param


@pytest.mark.parametrize(
    "imgs, labels, custom_texts",
    TEST_DATA)
def test_plot_images(
        capsys, test_true_false, imgs, labels, custom_texts):
    ipyplot.plot_images(
        imgs,
        labels=labels,
        custom_texts=custom_texts,
        max_images=30,
        img_width=300,
        force_b64=test_true_false)
    captured = capsys.readouterr()
    if test_true_false and type(imgs[0]) is np.str_ and "http" in imgs[0]:
        assert("Ignoring 'force_b64' flag" in captured.out)

    assert(str(HTML).split("'")[1] in captured.out)


@pytest.mark.parametrize(
    "imgs, labels, custom_texts",
    TEST_DATA)
def test_plot_class_tabs(
        capsys, test_true_false, imgs, labels, custom_texts):
    ipyplot.plot_class_tabs(
        imgs,
        labels=labels if labels is not None else LABELS[1],
        custom_texts=custom_texts,
        img_width=300,
        force_b64=test_true_false)
    captured = capsys.readouterr()
    if test_true_false and type(imgs[0]) is np.str_ and "http" in imgs[0]:
        assert("Ignoring 'force_b64' flag" in captured.out)

    assert(str(HTML).split("'")[1] in captured.out)


GRID_IMAGES = [
    [BASE_LOCAL_URLS[0], BASE_LOCAL_URLS[1], BASE_LOCAL_URLS[2]],
    [BASE_LOCAL_URLS[2], BASE_LOCAL_URLS[0], BASE_LOCAL_URLS[1]],
]


def _capture_grid_html(monkeypatch, **kwargs):
    """Intercept the HTML string that plot_images would send to IPython."""
    from ipyplot import _plotting

    captured = {}

    def _fake_display(html_str):
        captured["html"] = html_str

    monkeypatch.setattr(_plotting, "_display_html", _fake_display)
    ipyplot.plot_images(
        GRID_IMAGES,
        nested_layout="grid",
        show_url=False,
        img_width=120,
        **kwargs,
    )
    return captured["html"]


def test_plot_images_grid_backcompat_labels(monkeypatch):
    """`labels=` on grid mode still works and renders as per-row titles."""
    html = _capture_grid_html(monkeypatch, labels=["row-one", "row-two"])
    assert '<div class="ipyplot-fixed-grid-row-label-' in html
    assert "row-one" in html and "row-two" in html
    # No column-label div should appear when only row labels were supplied.
    # (The CSS class is always declared, but the rendered `<div class="...">`
    # for a column header is only emitted when column_labels is set.)
    assert '<div class="ipyplot-fixed-grid-col-label-' not in html
    assert '<div class="ipyplot-fixed-grid-corner-' not in html


def test_plot_images_grid_row_and_column_labels(monkeypatch):
    """Explicit row_labels + column_labels render as axes with a corner cell."""
    html = _capture_grid_html(
        monkeypatch,
        row_labels=["bottoms", "tops"],
        column_labels=["farfetch", "ssense", "msscdn"],
    )
    assert '<div class="ipyplot-fixed-grid-row-label-' in html
    assert '<div class="ipyplot-fixed-grid-col-label-' in html
    assert '<div class="ipyplot-fixed-grid-corner-' in html  # corner cell
    for label in ("bottoms", "tops", "farfetch", "ssense", "msscdn"):
        assert label in html


def test_plot_images_grid_row_labels_kwarg_wins_over_labels(monkeypatch):
    """If both `labels` and `row_labels` are passed, `row_labels` is authoritative."""
    html = _capture_grid_html(
        monkeypatch,
        labels=["should-not-appear-1", "should-not-appear-2"],
        row_labels=["real-row-1", "real-row-2"],
    )
    assert "real-row-1" in html and "real-row-2" in html
    assert "should-not-appear-1" not in html
    assert "should-not-appear-2" not in html


@pytest.mark.parametrize(
    "imgs, labels, custom_texts",
    TEST_DATA)
def test_plot_class_representations(
        capsys, test_true_false, imgs, labels, custom_texts):
    ipyplot.plot_class_representations(
        imgs,
        labels=labels if labels is not None else LABELS[1],
        img_width=300,
        force_b64=test_true_false)
    captured = capsys.readouterr()
    if test_true_false and type(imgs[0]) is np.str_ and "http" in imgs[0]:
        assert("Ignoring 'force_b64' flag" in captured.out)

    assert(str(HTML).split("'")[1] in captured.out)
