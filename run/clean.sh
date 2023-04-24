#!/bin/bash
find src/hub -path "*/migrations/*.py" -not -name "__init__.py" -delete
find src/hub -path "*/migrations/*.pyc"  -delete
rm app/db.sqlite3
