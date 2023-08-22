#!/bin/bash

which pytest > /dev/null || { echo "Pytest not found, can't run tests."; exit 1; }

# coverage report settings
cov_report=html
required_coverage=95

while getopts "r:c:h" opt; do
  case $opt in
    h)
        echo "Usage: test.sh [-r <required coverage>] [-c <coverage report type>]"
        exit 0
        ;;
    r)
      required_coverage=$OPTARG
      ;;
    c)
      cov_report=$OPTARG
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      ;;
  esac
done

# runs coverage with a html report
# fails if cov < required_coverage
pytest -n auto --cov=jpfreq --cov-report=$cov_report --cov-fail-under=$required_coverage tests/