"""
Local file server and caching utilities used by IPyPlot.
"""

import atexit
import hashlib
import io
import os
import shutil
import socket
import threading
from contextlib import closing
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Optional, Tuple, Union

import numpy as np
import PIL
from numpy import str_  # noqa: W0611
from PIL import Image

CACHE_ROOT = Path.home() / ".ipyplot"
FILES_DIR = CACHE_ROOT / "files"
GENERATED_DIR = CACHE_ROOT / "generated"

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 39876
MAX_PORT_SCAN = 25

_server: Optional[ThreadingHTTPServer] = None
_server_thread: Optional[threading.Thread] = None
_preferred_host: str = DEFAULT_HOST
_preferred_port: int = DEFAULT_PORT
_server_host: Optional[str] = None
_server_port: Optional[int] = None
_cache_lock = threading.Lock()


def _ensure_cache_dirs():
    FILES_DIR.mkdir(parents=True, exist_ok=True)
    GENERATED_DIR.mkdir(parents=True, exist_ok=True)


class _SilentRequestHandler(SimpleHTTPRequestHandler):
    """Request handler that keeps stdout clean inside notebooks."""

    def log_message(self, format, *args):  # noqa: A003
        return


def _start_http_server(host: str, port: int):
    handler = partial(_SilentRequestHandler, directory=str(CACHE_ROOT))
    server = ThreadingHTTPServer((host, port), handler)
    return server


def _pick_port(host: str, start_port: int) -> Tuple[str, int]:
    port = start_port
    for _ in range(MAX_PORT_SCAN):
        with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try:
                sock.bind((host, port))
                return host, port
            except OSError:
                next_port = port + 1
                print(f"[ipyplot] Port {port} busy, trying {next_port}")
                port = next_port
                continue
    raise RuntimeError(f"Unable to find available port starting from {start_port}")


def _run_server(host: str, port: int):
    global _server, _server_thread, _server_host, _server_port
    if _server and _server_thread and _server_thread.is_alive():
        return _server_host, _server_port

    _ensure_cache_dirs()
    host, port = _pick_port(host, port)
    server = _start_http_server(host, port)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    _server, _server_thread = server, thread
    _server_host, _server_port = host, port
    atexit.register(stop_server)
    return host, port


def ensure_server_running() -> Tuple[str, int]:
    """Start the local file server if it's not running and return its address."""
    return _run_server(_preferred_host, _preferred_port)


def configure_server(host: Optional[str] = None, port: Optional[int] = None) -> str:
    """Configure server binding. Restarts server when values change."""
    global _preferred_host, _preferred_port
    restart_needed = False
    if host and host != _preferred_host:
        _preferred_host = host
        restart_needed = True
    if port and port != _preferred_port:
        _preferred_port = int(port)
        restart_needed = True
    if restart_needed and _server:
        stop_server()
    ensure_server_running()
    return get_server_url()


def set_server_host(host: str) -> str:
    """Public helper to override the server host name."""
    return configure_server(host=host)


def set_server_port(port: int) -> str:
    """Public helper to override the starting port."""
    return configure_server(port=port)


def stop_server():
    """Shutdown the local HTTP server."""
    global _server, _server_thread
    if _server:
        _server.shutdown()
        _server.server_close()
        _server = None
    if _server_thread:
        _server_thread.join(timeout=1)
        _server_thread = None


def get_server_url() -> str:
    """Return base URL where cached files are served."""
    if not _server_host or not _server_port:
        ensure_server_running()
    return f"http://{_server_host}:{_server_port}"


def _sanitize_path_for_cache(path: Path) -> Path:
    parts = [p for p in path.expanduser().resolve().parts if p not in (path.anchor, os.sep, "")]  # noqa: E501
    if path.anchor and path.anchor not in (os.sep, ""):
        sanitized_anchor = path.anchor.replace(":", "").replace(os.sep, "")
        if sanitized_anchor:
            parts.insert(0, sanitized_anchor)
    return Path(*parts)


def cache_local_file(path: Union[str, os.PathLike]) -> str:
    """Copy local file into the cache directory and return served URL."""
    ensure_server_running()
    source_path = Path(path).expanduser()
    target_path = FILES_DIR / _sanitize_path_for_cache(source_path)
    target_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(str(source_path), str(target_path))
    return build_url_for_path(target_path)


def _coerce_to_pil(image: Union[np.ndarray, PIL.Image.Image, str, str_]) -> PIL.Image.Image:
    if isinstance(image, np.ndarray):
        if image.dtype in [np.float32, np.float64]:
            image = image * 255 if image.max() <= 1.0 else image
            image = PIL.Image.fromarray(image.astype(np.uint8))
        else:
            image = PIL.Image.fromarray(image)
    elif isinstance(image, PIL.Image.Image):
        image = image
    elif isinstance(image, (str, str_)):
        image = PIL.Image.open(image)
    else:
        raise TypeError(f"Unsupported image type: {type(image)}")
    return image


def cache_image_bytes(image: Union[np.ndarray, PIL.Image.Image, str, str_]) -> str:
    """Cache in-memory image into file cache and return served URL."""
    ensure_server_running()
    pil_image = _coerce_to_pil(image)
    with io.BytesIO() as output:
        pil_image.save(output, format="PNG")
        data = output.getvalue()
    digest = hashlib.sha256(data).hexdigest()
    target_path = GENERATED_DIR / f"{digest}.png"
    target_path.parent.mkdir(parents=True, exist_ok=True)
    with _cache_lock:
        if not target_path.exists():
            with open(target_path, "wb") as f:
                f.write(data)
    return build_url_for_path(target_path)


def build_url_for_path(path: Path) -> str:
    rel = path.relative_to(CACHE_ROOT)
    base_url = get_server_url()
    return f"{base_url}/{rel.as_posix()}"


def is_remote_url(url: str) -> bool:
    lowered = url.lower()
    return lowered.startswith(("http:", "https:", "ftp:", "www.", "data:", "file:"))
