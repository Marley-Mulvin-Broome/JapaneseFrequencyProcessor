#!/bin/bash

which pytest > /dev/null || { echo "Pytest not found, can't run tests."; exit 1; }

# coverage report settings
cov_report=html
required_coverage=95
open_report=false

while getopts "r:c:ho" opt; do
  case $opt in
    h)
        echo "Usage: test.sh [-r <required coverage>] [-c <coverage report type>] [-o]"
        echo "-o opens the coverage report in a browser after running tests"
        exit 0
        ;;
    r)
      required_coverage=$OPTARG
      ;;
    c)
      cov_report=$OPTARG
      ;;
    o)
      open_report=true
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      ;;
  esac
done

# runs coverage with a html report
# fails if cov < required_coverage
pytest -n auto --cov=src/jpfreq --cov-branch --cov-report=$cov_report --cov-fail-under=$required_coverage tests/

ruff src/jpfreq/*.py


if [ "$open_report" = true ] ; then
  open htmlcov/index.html
fi