#!/bin/bash

# Generate documentation
# Requires: pdoc3

if which pdoc >/dev/null; then
    pdoc --html --force --output-dir docs src/jpfreq
    mv -f docs/jpfreq/* docs/
else
    echo "pdoc not found. Install with 'pip install pdoc3'"
fi