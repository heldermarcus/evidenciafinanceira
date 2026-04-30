#!/usr/bin/env bash
# Script de build para o Render
# Executado automaticamente antes de iniciar o servidor

set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input

python manage.py migrate
