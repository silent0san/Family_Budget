#!/bin/bash

yes | python family_budget/manage.py makemigrations
python family_budget/manage.py migrate
python family_budget/manage.py runserver 0.0.0.0:8000
