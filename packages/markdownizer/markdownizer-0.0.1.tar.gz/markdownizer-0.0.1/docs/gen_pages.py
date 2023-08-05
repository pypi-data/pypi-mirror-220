"""Generate the code reference pages and navigation."""


from __future__ import annotations

import logging
import sys

import markdownizer
import mkdocs
from markdownizer import classhelpers

logger = logging.getLogger(__name__)

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

docs = markdownizer.Docs(module=markdownizer)
nav = docs.create_nav(section="markdownizer")
# na2 = docs.create_nav(section="test")

nav[("overview",)] = "index.md"
# na2[("overview",)] = "index.md"

for klass in docs.iter_classes_for_module("markdownizer"):
    nav.add_class_page(klass=klass, path=f"{klass.__name__}.md")

# nav.pretty_print()
print(str(docs))

# nav.write()
docs.write()
