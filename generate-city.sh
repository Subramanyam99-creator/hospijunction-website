#!/bin/bash
# generate-city.sh — Create a new city landing page from the Tirupati template
# Usage: ./generate-city.sh <slug> "<City Name>" "<State>"
# Example: ./generate-city.sh hyderabad "Hyderabad" "Telangana"

if [ $# -lt 3 ]; then
  echo "Usage: $0 <slug> \"<City Name>\" \"<State>\""
  echo "Example: $0 hyderabad \"Hyderabad\" \"Telangana\""
  exit 1
fi

SLUG="$1"
CITY="$2"
STATE="$3"
DIR="hospitals/${SLUG}"

if [ -d "$DIR" ]; then
  echo "⚠  Directory $DIR already exists. Skipping."
  exit 1
fi

mkdir -p "$DIR"

sed \
  -e "s/Tirupati/${CITY}/g" \
  -e "s/tirupati/${SLUG}/g" \
  -e "s/Andhra Pradesh/${STATE}/g" \
  hospitals/tirupati/index.html > "${DIR}/index.html"

echo "✓  Created ${DIR}/index.html"
echo "   → https://www.hospijunction.com/hospitals/${SLUG}/"
echo ""
echo "Next steps:"
echo "  1. Add to sitemap.xml"
echo "  2. git add hospitals/${SLUG}/ && git commit && git push"
