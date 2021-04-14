# magictypes

```zsh
mkdir data
cd data
curl https://mtgjson.com/api/v5/AllIdentifiers.json.zip | jar xv
curl https://mtgjson.com/api/v5/EnumValues.json.zip | jar xv
curl https://mtgjson.com/api/v5/SetList.json.zip | jar xv
pipenv install
pipenv shell
python3 src/magictypes.py
```
