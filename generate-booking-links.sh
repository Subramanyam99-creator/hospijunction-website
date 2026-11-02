#!/bin/bash
# generate-booking-links.sh — Print booking page URLs for all hospitals
# Usage: ./generate-booking-links.sh
#
# These URLs are what hospitals put in their Google Business Profile
# under "Appointment URL" or "Booking link"

echo "============================================"
echo "  HospiJunction — Hospital Booking Links"
echo "  (Share these with hospital owners for GMB)"
echo "============================================"
echo ""
echo "Instructions for hospitals:"
echo "1. Go to business.google.com"
echo "2. Select your hospital"
echo "3. Click 'Edit profile' → 'Contact'"
echo "4. Under 'Appointment links', add your URL below"
echo "5. Save"
echo ""
echo "--------------------------------------------"
echo ""

# Examples — replace with actual hospital names
# The slug is the hospital name in lowercase, spaces/special chars replaced with hyphens

HOSPITALS=(
  "Apollo Hospital Tirupati"
  "SVIMS Hospital Tirupati"
)

for name in "${HOSPITALS[@]}"; do
  slug=$(echo "$name" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/-/g' | sed 's/--*/-/g' | sed 's/^-//;s/-$//')
  echo "Hospital: $name"
  echo "GMB Link: https://www.hospijunction.com/book/${slug}/"
  echo ""
done

echo "--------------------------------------------"
echo "To generate a link for any hospital:"
echo "  Take the hospital name, lowercase it,"
echo "  replace spaces with hyphens."
echo ""
echo "  Example: 'City Care Hospital' →"
echo "  https://www.hospijunction.com/book/city-care-hospital/"
