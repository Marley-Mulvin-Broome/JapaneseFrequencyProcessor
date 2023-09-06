#!/bin/bash

if which black > /dev/null; then
    echo "Running black..."
    black src/jpfreq/*.py src/jpfreq/exporters/*.py tests/*.py
fi

if which ruff > /dev/null; then
    echo "Running ruff..."
    ruff --fix src/jpfreq/*.py src/jpfreq/exporters/*.py tests/*.py
fi

