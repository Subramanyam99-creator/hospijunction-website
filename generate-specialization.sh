#!/bin/bash
# generate-specialization.sh — Create a specialization+city landing page
# Usage: ./generate-specialization.sh <spec-slug> "<Specialization>" <city-slug> "<City Name>" "<State>"
# Example: ./generate-specialization.sh dermatologist "Dermatologist" tirupati "Tirupati" "Andhra Pradesh"
# Example: ./generate-specialization.sh orthopedic "Orthopedic" hyderabad "Hyderabad" "Telangana"

if [ $# -lt 5 ]; then
  echo "Usage: $0 <spec-slug> \"<Specialization>\" <city-slug> \"<City Name>\" \"<State>\""
  echo "Example: $0 dermatologist \"Dermatologist\" tirupati \"Tirupati\" \"Andhra Pradesh\""
  exit 1
fi

SPEC_SLUG="$1"
SPEC_NAME="$2"
CITY_SLUG="$3"
CITY_NAME="$4"
STATE="$5"
DIR="doctors/${SPEC_SLUG}/${CITY_SLUG}"

if [ -d "$DIR" ]; then
  echo "Directory $DIR already exists. Skipping."
  exit 1
fi

mkdir -p "$DIR"

sed \
  -e "s/Cardiologist/${SPEC_NAME}/g" \
  -e "s/cardiologist/${SPEC_SLUG}/g" \
  -e "s/Tirupati/${CITY_NAME}/g" \
  -e "s/tirupati/${CITY_SLUG}/g" \
  -e "s/Andhra Pradesh/${STATE}/g" \
  doctors/cardiologist/tirupati/index.html > "${DIR}/index.html"

echo "Created ${DIR}/index.html"
echo "  -> https://www.hospijunction.com/doctors/${SPEC_SLUG}/${CITY_SLUG}/"
echo ""
echo "Next steps:"
echo "  1. Add to sitemap.xml"
echo "  2. git add doctors/${SPEC_SLUG}/${CITY_SLUG}/ && git commit && git push"
