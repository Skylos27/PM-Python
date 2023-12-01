#!/bin/bash

# Répertoire source
SOURCE_DIR="./"

# Répertoire cible
TARGET_DIR="/PDF/"

# Crée le répertoire cible s'il n'existe pas
mkdir -p "$TARGET_DIR"

# Fichers HTML à convertir
wkhtmltopdf "$SOURCE_DIR/app.html" "$TARGET_DIR/app.pdf"
wkhtmltopdf "$SOURCE_DIR/index.html" "$TARGET_DIR/index.pdf"
wkhtmltopdf "$SOURCE_DIR/pm.html" "$TARGET_DIR/pm.pdf"

echo "Conversion en PDFs terminée."

