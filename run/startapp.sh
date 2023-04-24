#!/bin/bash

set -xe
python src/hub/manage.py startapp src/$1
