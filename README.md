# mydeepl-cli

## setup

```
python setup.py develop
```
## Useage

### Get API Key
https://www.deepl.com/pro-api?cta=header-pro-api

### Run dl-cli 

```
# authkeyの設定 -> ~/.mydeepl_auth.json
dl-cli init

# 標準入力で入力
dl-cli text <こんにちは>

# txtファイルで入力
dl-cli doc path/to/file.txt

# 英語 -> 日本語の場合 (デフォルトは 日本語 -> 英語) 
dl-cli text -l EN "Hello"

```
