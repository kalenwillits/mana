#!/bin/bash
find app/ -path "*/migrations/*.py" -not -name "__init__.py" -delete
find app/ -path "*/migrations/*.pyc"  -delete
