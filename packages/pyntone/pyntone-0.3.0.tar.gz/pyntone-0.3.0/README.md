# pyntone
![](https://img.shields.io/badge/Python-%3E%3D3.9-blue)  
API client for Kintone REST API.

## Installation
```bash
$ pip install pyntone
```

## Example
### Get Record
```python
from pyntone import ApiTokenAuth, KintoneRestAPIClient

auth = ApiTokenAuth(api_token='[YOUR API TOKEN]')
client = KintoneRestAPIClient(
    base_url='https://[YOUR SUBDOMAIN].cybozu.com',
    auth=auth
)
res = client.record.get_record(1, 1)
print(res)
```