"""Sparse Curveball kernel wrapper. No real-data evaluation entry point.

The library is compiled for the calling Python interpreter's architecture,
including x86_64 Python on Apple Silicon. Build products live in work/.
"""
import ctypes as ct
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path(__file__).with_name("curveball_kernel.cpp")


def build_library():
    digest = hashlib.sha256(SOURCE.read_bytes()).hexdigest()[:16]
    arch = platform.machine()
    directory = ROOT / "work/curveball_build"
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / f"curveball_{arch}_{digest}.dylib"
    if not path.exists():
        command = ["clang++", "-std=c++17", "-O3", "-shared", "-fPIC"]
        if platform.system() == "Darwin":
            sdk = subprocess.check_output(["xcrun", "--show-sdk-path"], text=True).strip()
            command += ["-arch", arch, "-isysroot", sdk]
            headers = Path(sdk) / "usr/include/c++/v1"
            if headers.is_dir():
                command += ["-isystem", str(headers)]
        temporary = path.with_name(path.name + f".{os.getpid()}.tmp")
        try:
            subprocess.run([*command, str(SOURCE), "-o", str(temporary)], check=True)
            temporary.replace(path)
            path.with_suffix('.build.json').write_text(json.dumps({
                'command': [*command, str(SOURCE), '-o', str(path)],
                'compiler': subprocess.check_output(['clang++', '--version'], text=True),
                'architecture': arch,
                'source_sha256': hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
                'library_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
            }, indent=2) + '\n')
        finally:
            temporary.unlink(missing_ok=True)
    return path


def library():
    lib = ct.CDLL(str(build_library()))
    ptr64 = ct.POINTER(ct.c_uint64); ptr32 = ct.POINTER(ct.c_uint32)
    lib.cb_create.argtypes = [ct.c_uint64, ct.c_uint32, ptr64, ptr32, ct.c_uint64]
    lib.cb_create.restype = ct.c_void_p
    lib.cb_error.restype = ct.c_char_p
    lib.cb_destroy.argtypes = [ct.c_void_p]
    lib.cb_step.argtypes = [ct.c_void_p, ct.c_uint64]
    lib.cb_step.restype = ct.c_int
    lib.cb_export.argtypes = [ct.c_void_p, ptr32]
    lib.cb_reference.argtypes = [ct.c_void_p, ptr32]
    lib.cb_margins.argtypes = [ct.c_void_p, ptr64]
    for name in ("cb_distance", "cb_attempts", "cb_tradable"):
        function = getattr(lib, name)
        function.argtypes = [ct.c_void_p]; function.restype = ct.c_uint64
    lib.cb_counts.argtypes = [ct.c_void_p, ct.c_uint64, ptr32, ptr64]
    lib.cb_counts.restype = ct.c_int
    return lib


def pointer(array, ctype):
    return array.ctypes.data_as(ct.POINTER(ctype))


class Curveball:
    def __init__(self, rows, n_columns, seed):
        if not 0 <= n_columns < 2**32 or not 0 <= seed < 2**64:
            raise ValueError("column count or seed out of range")
        canonical = []
        for row in rows:
            values = sorted(row)
            if any(int(x) != x or not 0 <= x < n_columns for x in values):
                raise ValueError("invalid label")
            if len(set(values)) != len(values):
                raise ValueError("duplicate label within binary row")
            canonical.append(values)
        self.offsets = np.r_[np.uint64(0), np.cumsum([len(r) for r in canonical], dtype=np.uint64)]
        self.offsets = np.ascontiguousarray(self.offsets, dtype=np.uint64)
        self.labels = np.asarray([x for row in canonical for x in row], dtype=np.uint32)
        self.n_columns = n_columns
        self.lib = library()
        self.handle = self.lib.cb_create(len(canonical), n_columns,
                       pointer(self.offsets, ct.c_uint64), pointer(self.labels, ct.c_uint32), seed)
        if not self.handle:
            raise RuntimeError(self.lib.cb_error().decode())

    def close(self):
        if getattr(self, "handle", None):
            self.lib.cb_destroy(self.handle); self.handle = None

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def __del__(self):
        self.close()

    def _check_open(self):
        if self.handle is None:
            raise RuntimeError("chain has been closed")

    def step(self, attempts):
        self._check_open()
        if not 0 <= attempts < 2**64 or int(attempts) != attempts:
            raise ValueError("invalid attempt count")
        if self.lib.cb_step(self.handle, attempts):
            raise RuntimeError(self.lib.cb_error().decode())

    def rows(self):
        self._check_open()
        result = np.empty_like(self.labels)
        self.lib.cb_export(self.handle, pointer(result, ct.c_uint32))
        return [result[a:b].tolist() for a,b in zip(self.offsets[:-1],self.offsets[1:])]

    def margins(self):
        self._check_open()
        result = np.zeros(self.n_columns, dtype=np.uint64)
        self.lib.cb_margins(self.handle, pointer(result, ct.c_uint64))
        return result

    def set_reference(self, rows):
        """Distance reference only; does not alter states, margins or RNG."""
        self._check_open()
        if len(rows) != len(self.offsets)-1 or any(
                len(r) != b-a for r,a,b in zip(rows,self.offsets[:-1],self.offsets[1:])):
            raise ValueError('reference row degrees differ')
        if any(len(set(r)) != len(r) or any(int(x)!=x or not 0<=x<self.n_columns for x in r)
               for r in rows):
            raise ValueError('invalid reference labels')
        flat = np.asarray([x for r in rows for x in sorted(r)], dtype=np.uint32)
        self.lib.cb_reference(self.handle, pointer(flat, ct.c_uint32))

    def counts(self, pairs):
        self._check_open()
        pairs = np.asarray(pairs)
        if pairs.size == 0:
            return np.zeros(0, dtype=np.uint64)
        if pairs.ndim != 2 or pairs.shape[1] != 2 or \
                np.any(pairs < 0) or np.any(pairs >= self.n_columns) or \
                np.any(pairs != np.floor(pairs)):
            raise ValueError("invalid pair array")
        pairs = np.ascontiguousarray(pairs, dtype=np.uint32)
        result = np.zeros(len(pairs), dtype=np.uint64)
        if self.lib.cb_counts(self.handle, len(pairs), pointer(pairs, ct.c_uint32),
                              pointer(result, ct.c_uint64)):
            raise RuntimeError(self.lib.cb_error().decode())
        return result

    def diagnostics(self):
        self._check_open()
        return {"attempts": self.lib.cb_attempts(self.handle),
                "tradable_attempts": self.lib.cb_tradable(self.handle),
                "changed_binary_entries": self.lib.cb_distance(self.handle)}
