#!/usr/bin/env bash
mkdir -p data
curl https://mtgjson.com/api/v5/AllIdentifiers.json.zip | tar xv -C data
curl https://mtgjson.com/api/v5/EnumValues.json.zip | tar xv -C data
curl https://mtgjson.com/api/v5/SetList.json.zip | tar xv -C data