#!/bin/bash

ES_URL="http://localhost:9200/vehicle_telemetry/_doc"

plate_numbers=("ABC-1234" "XYZ-9876" "LMN-4567" "PQR-5432" "JKL-7890" "DEF-1111" "GHI-2222" "MNO-3333" "STU-4444" "VWY-5555")

# 50.000 Creating Data
for i in {1..50000}
do
  plate_number="${plate_numbers[$RANDOM % ${#plate_numbers[@]}]}"  # Rastgele plaka numarası
  latitude=$(awk -v min=-90 -v max=90 'BEGIN{srand(); print min+rand()*(max-min)}')
  longitude=$(awk -v min=-180 -v max=180 'BEGIN{srand(); print min+rand()*(max-min)}')

  if [[ "$OSTYPE" == "darwin"* ]]; then
    timestamp=$(date -v-"$((RANDOM % 365))d" -u +"%Y-%m-%dT%H:%M:%SZ")
  else
    timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ" -d "$((RANDOM % 365)) days ago")
  fi

  curl -s -X POST "$ES_URL" -H "Content-Type: application/json" -d '{
    "plate_number": "'"$plate_number"'",
    "latitude": '"$latitude"',
    "longitude": '"$longitude"',
    "timestamp": "'"$timestamp"'"
  }' > /dev/null

  if (( i % 1000 == 0 )); then
    echo "$i records inserted..."
  fi
done

echo "Data generation completed!"