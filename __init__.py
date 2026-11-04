# -*- coding: utf-8 -*-
"""SXS custom node package."""
from .sxs_node import SXS

NODE_CLASS_MAPPINGS = {"SXS": SXS}
NODE_DISPLAY_NAME_MAPPINGS = {"SXS": "SXS Scene Prompt"}
WEB_DIRECTORY = "./web/js"

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS", "WEB_DIRECTORY"]
