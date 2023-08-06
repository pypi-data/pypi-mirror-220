# MayfPayApi BETA

## MayfPayApi is a Python library for interacting with the MayfPay payment system API. It provides methods for retrieving kassa balances, creating and checking invoices.

## Installation

You can install MayfPayApi using pip:

```python
pip install mayfpayapi
```


## Usage

# Creating an instance of the MayfPayApi class
```python
api = MayfPayApi(api_token="your_api_token", kassa_id=your_kassa_id, public_key="your_public_key", secret_key="your_secret_key")
```

# Calling the get_kassa_balance method
```python
kassa_balance = api.get_kassa_balance()
print(kassa_balance)
```

# Calling the create_invoice method
```python
amount = 100.0
order_id = "your_order_id"
expire_invoice = 3600
payment_method = "your_payment_method"
comment = "your_comment"
data = {"key": "value"}
invoice = api.create_invoice(amount, order_id, expire_invoice, payment_method, comment, data)
print(invoice)
```

# Calling the check_invoice method
```python
order_id = "your_order_id"
invoice_status = api.check_invoice(order_id)
print(invoice_status)
```


## Contributing

Contributions are welcome! Please feel free to submit a pull request.

## License
### MayfPayApi is released under the MIT License. See LICENSE for more information.
