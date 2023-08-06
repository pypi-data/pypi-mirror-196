"""Defines misc. utilities used by this example module."""

from typing import Any


def _gen_prep_msg(module_name: str) -> Any:
    def _prep_msg() -> None:
        print(f"🔧 {module_name} module prepared!")

    return _prep_msg


def _gen_cleanup_msg(module_name: str) -> Any:
    def _cleanup_msg() -> None:
        print(f"🔧 {module_name} module cleaned up!")

    return _cleanup_msg
