#!/usr/bin/env bash
mkdir -p data

declare -a FileArray=(
  "https://mtgjson.com/api/v5/AllIdentifiers.json.zip"
  "https://mtgjson.com/api/v5/EnumValues.json.zip"
  "https://mtgjson.com/api/v5/SetList.json.zip"
  "https://mtgjson.com/api/v5/CardTypes.json.zip"
)

for file in ${FileArray[@]}; do
    curl $file | tar xv -C data
done