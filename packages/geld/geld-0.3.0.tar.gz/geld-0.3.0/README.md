# Geld

A library to easily handle currency conversions.


## Official documentation
- We do not have an official documentation yet, we are working on this.

## Data origin
Currently the API used to get the values is https://theforexapi.com/api. (If the forex API the default client will not work)
We are working to make the lib extensable so you can pick info from different sources in the future.


## How to install

```
pip install geld
```

## How to use the Sync Client

Code:
```python
from geld.clients import sync_client as client
result = client.convert_currency("USD", "BRL", 25, "2021-12-05")
print(result)
```

Result:
```
141.0127535205030424592109739
```