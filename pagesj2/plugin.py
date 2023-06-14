################################################################################
# @file        : plugin.py
# @brief       : Pages-J2 Plugin for MkDocs
# @author      : Jacques Supcik <jacques.supcik@hefr.ch>
# @date        : 14. June 2023
# ------------------------------------------------------------------------------
# @copyright   : Copyright (c) 2022 HEIA-FR / ISC
#                Haute école d'ingénierie et d'architecture de Fribourg
#                Informatique et Systèmes de Communication
# @attention   : SPDX-License-Identifier: MIT OR Apache-2.0
# ------------------------------------------------------------------------------
# @details
# Pages-J2 Plugin Plugin for MkDocs
################################################################################

import collections.abc
import logging
import os
from datetime import date
from typing import Type

import jinja2
from mkdocs.config.base import Config as BaseConfig
from mkdocs.config.config_options import Type as PluginType
from mkdocs.exceptions import PluginError
from mkdocs.plugins import BasePlugin

logger = logging.getLogger("mkdocs.plugins." + __name__)
logTag = "[pages-j2] -"


class PagesJ2Config(BaseConfig):
    pass


class PagesJ2Plugin(BasePlugin[PagesJ2Config]):
    def on_pre_build(self, config):
        """
        Build the `.pages` files from `pages.j2`
        """
        logger.info(f"{logTag} Building .pages files")
        for root, _, files in os.walk(config["docs_dir"], topdown=False):
            env = jinja2.Environment(
                loader=jinja2.FileSystemLoader(root),
            )
            for name in files:
                if name != "pages.j2":
                    continue

                template = env.get_template(name)
                content = template.render(config=config, env=os.environ)
                dst = os.path.join(root, ".pages")
                # Do not write the file if the content is the same.
                # Otherwise, the "watcher" will continuously reload the page.
                if os.path.exists(dst):
                    with open(dst) as f:
                        orig = f.read()
                    if content == orig:
                        continue
                with open(dst, "w") as f:
                    logger.info(f"{logTag} Writing {dst}")
                    f.write(content)
