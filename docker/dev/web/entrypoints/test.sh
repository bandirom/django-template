#!/bin/sh

coverage erase
coverage run manage.py test || exit
coverage report --fail-under="$COVERAGE_THRESHOLD" || exit
coverage xml
