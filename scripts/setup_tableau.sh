#!/usr/bin/env bash
# Prepare Anshivya Tableau workbook for publishing (Linux-safe prep step)
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

echo "=== Anshivya Tableau setup ==="
echo "Project root: $ROOT"
echo

# Ensure data copy exists
mkdir -p data
if [[ ! -f data/train.csv ]]; then
  cp "Machine learning Models/Neural_Networks/train.csv" data/train.csv
  echo "✓ Copied train.csv → data/train.csv"
else
  echo "✓ data/train.csv already exists"
fi

# Regenerate workbook with current absolute paths
TRAIN="$ROOT/data/train.csv"
TRAIN_DIR="$ROOT/data"
sed -e 's|BankChurnVisualisation|AnshivyaChurnVisualisation|g' \
    -e "s|/Users/talieh/Studies/Monash_Bootcamp/Assignments/Project_4/Bank_Churn_Project/train.csv|${TRAIN}|g" \
    -e "s|/Users/talieh/Studies/Monash_Bootcamp/Assignments/Project_4/Bank_Churn_Project|${TRAIN_DIR}|g" \
    "Bank Churn Visualisation.twb" > "Anshivya Churn Visualisation.twb"

echo "✓ Created Anshivya Churn Visualisation.twb"
echo
echo "Tableau Public is NOT available on Linux."
echo "Next: publish on Windows/Mac — see scripts/publish_tableau.md"
echo
echo "After publishing, verify:"
echo "  https://public.tableau.com/views/AnshivyaChurnVisualisation/Dashboard1"
echo
echo "Then run Flask and open:"
echo "  http://localhost:9092/visualization"
