#!/usr/bin/env python3
"""
generate_requirements.py

Scans a Django project directory, extracts third‑party imports,
and creates a requirements.txt file.

Usage:
    python generate_requirements.py [project_root]
"""

import os
import sys
import ast
import argparse
from pathlib import Path

# ----------------------------------------------------------------------
# Standard library module names (built‑in filter)
# ----------------------------------------------------------------------
try:
    # Python 3.10+ has this handy set
    STD_LIB_MODULES = sys.stdlib_module_names
except AttributeError:
    # Fallback for older Python versions (common modules)
    STD_LIB_MODULES = {
        "abc", "aifc", "argparse", "array", "ast", "asynchat", "asyncio",
        "asyncore", "atexit", "audioop", "base64", "bdb", "binascii", "binhex",
        "bisect", "builtins", "bz2", "calendar", "cgi", "cgitb", "chunk",
        "cmath", "cmd", "code", "codecs", "codeop", "collections", "colorsys",
        "compileall", "concurrent", "configparser", "contextlib", "contextvars",
        "copy", "copyreg", "cProfile", "crypt", "csv", "ctypes", "curses",
        "dataclasses", "datetime", "dbm", "decimal", "difflib", "dis",
        "distutils", "doctest", "email", "encodings", "ensurepip", "enum",
        "errno", "faulthandler", "fcntl", "filecmp", "fileinput", "fnmatch",
        "fractions", "ftplib", "functools", "gc", "getopt", "getpass",
        "gettext", "glob", "grp", "gzip", "hashlib", "heapq", "hmac", "html",
        "http", "idlelib", "imaplib", "imghdr", "imp", "importlib", "inspect",
        "io", "ipaddress", "itertools", "json", "keyword", "lib2to3", "linecache",
        "locale", "logging", "lzma", "mailbox", "mailcap", "marshal", "math",
        "mimetypes", "mmap", "modulefinder", "msilib", "msvcrt", "multiprocessing",
        "netrc", "nis", "nntplib", "numbers", "operator", "optparse", "os",
        "pathlib", "pdb", "pickle", "pickletools", "pipes", "pkgutil", "platform",
        "plistlib", "poplib", "posix", "pprint", "profile", "pstats", "pty",
        "pwd", "py_compile", "pyclbr", "pydoc", "queue", "quopri", "random",
        "re", "readline", "reprlib", "resource", "rlcompleter", "runpy", "sched",
        "secrets", "select", "selectors", "shelve", "shlex", "shutil", "signal",
        "site", "smtpd", "smtplib", "sndhdr", "socket", "socketserver", "spwd",
        "sqlite3", "ssl", "stat", "statistics", "string", "stringprep", "struct",
        "subprocess", "sunau", "symbol", "symtable", "sys", "sysconfig", "tabnanny",
        "tarfile", "telnetlib", "tempfile", "termios", "textwrap", "threading",
        "time", "timeit", "tkinter", "token", "tokenize", "trace", "traceback",
        "tracemalloc", "tty", "turtle", "turtledemo", "types", "typing", "unicodedata",
        "unittest", "urllib", "uu", "uuid", "venv", "warnings", "wave", "weakref",
        "webbrowser", "winreg", "winsound", "wsgiref", "xdrlib", "xml", "xmlrpc",
        "zipapp", "zipfile", "zipimport", "zlib"
    }

# ----------------------------------------------------------------------
# Directories to skip when scanning Python files
# ----------------------------------------------------------------------
EXCLUDED_DIRS = {
    ".git", "__pycache__", "venv", "env", ".venv", ".env",
    "dist", "build", "*.egg-info", ".tox", ".pytest_cache"
}

# ----------------------------------------------------------------------
# Core logic
# ----------------------------------------------------------------------
def collect_imports(root):
    """
    Walk through all Python files (excluding EXCLUDED_DIRS) and extract
    top‑level imported module names using ast.
    Returns a set of module names.
    """
    imports = set()
    for py_file in root.rglob("*.py"):
        # Skip files inside excluded directories
        if any(part in EXCLUDED_DIRS for part in py_file.relative_to(root).parts):
            continue
        try:
            with open(py_file, "r", encoding="utf-8") as f:
                tree = ast.parse(f.read(), filename=str(py_file))
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        # Top‑level module (first part before dot)
                        mod = alias.name.split('.')[0]
                        imports.add(mod)
                elif isinstance(node, ast.ImportFrom):
                    if node.module is not None:
                        mod = node.module.split('.')[0]
                        imports.add(mod)
        except (SyntaxError, UnicodeDecodeError):
            # Skip files that can't be parsed
            continue
    return imports


def is_local_module(root, mod_name):
    """
    Heuristic: treat a module as local if there is a directory or .py file
    with that name directly under the project root.
    """
    # Check for a directory
    if (root / mod_name).is_dir():
        return True
    # Check for a .py file (e.g., mymodule.py)
    if (root / f"{mod_name}.py").is_file():
        return True
    # Also check for common Django app structure: inside a subdirectory that is itself a package?
    # Simpler: we only check top-level to avoid listing local apps.
    return False


def filter_third_party(module_names, root):
    """Remove standard library and local project modules."""
    third_party = set()
    for mod in module_names:
        if mod in STD_LIB_MODULES or mod.startswith('_'):
            continue
        if is_local_module(root, mod):
            continue
        third_party.add(mod)
    return third_party


def generate_requirements(root, third_party):
    """Write requirements.txt with one package per line."""
    req_path = root / "requirements.txt"
    with open(req_path, "w", encoding="utf-8") as f:
        for pkg in sorted(third_party):
            f.write(f"{pkg}\n")
    print(f"✅ Created {req_path} with {len(third_party)} packages.")
    if not third_party:
        print("⚠️  No third‑party packages detected. Check your imports.")


def main():
    parser = argparse.ArgumentParser(
        description="Generate requirements.txt from a Django project by scanning imports."
    )
    parser.add_argument(
        "project_root", nargs="?", default=".",
        help="Root directory of the Django project (default: current directory)"
    )
    args = parser.parse_args()

    root = Path(args.project_root).resolve()
    if not root.is_dir():
        print(f"❌ Error: {root} is not a valid directory.", file=sys.stderr)
        sys.exit(1)

    # Optional: check for manage.py to confirm it's a Django project
    if not (root / "manage.py").exists():
        print(f"⚠️  Warning: {root} does not contain manage.py – may not be a Django project.")

    print(f"📁 Scanning project: {root}")
    module_names = collect_imports(root)
    print(f"   Found {len(module_names)} imported modules (including stdlib and local).")

    third_party = filter_third_party(module_names, root)
    if third_party:
        print(f"   Third‑party packages: {', '.join(sorted(third_party))}")

    generate_requirements(root, third_party)


if __name__ == "__main__":
    main()