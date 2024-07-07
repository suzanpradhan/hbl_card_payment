# HBL Card Payment

Implementation of HBL PACO Core APIs for Card Payment with jose request.

APIs included:  
 ✅ Payment  
 ❌ Inquiry  
 ❌ Void request  
 ❌ Settlement  
 ❌ Refund

## Requirements

To get started, hit the 'clear' button at the top of the editor!

- Python 3.x
- Dependencies: PyJWT, requests, python-jose

## Installation

You can install the package via pip:

```bash
pip install hbl-card-payment
```

## Usage

Importing the Module

```python
from hbl_card_payment.card_payment import HBLCardPayment
```

### Initialization

Create an instance of HBLCardPayment with the required parameters:

```python
payment = HBLCardPayment(
    merchant_id='your_merchant_id',
    api_key='your_api_key',
    encryption_key='your_encryption_key',
    callback_url='your_callback_url',
    merchant_signing_private_key='merchant_signing_private_key',
    paco_encryption_public_key='paco_encryption_public_key',
    merchant_decryption_private_key='merchant_decryption_private_key',
    paco_signing_public_key='paco_signing_public_key'
)
```

### Making a Payment Request

Use the request method to make a payment request:

```python
response = payment.request(
    order_no='123456789',
    product_desc='Product Description',
    amount=100.0
)

print(response)
```

### Setting Additional Payload Values

If you need to set additional values in the request payload, use the set_value method:

```python
payment.set_value('purchaseItems',
  [
      [
          "purchaseItemType" => "ticket",
          "referenceNo" => "2322460376026",
          "purchaseItemDescription" => "Bundled insurance",
          "purchaseItemPrice" => [
              "amountText" => "000000002000",
              "currencyCode" => "NPR",
              "decimalPlaces" => 2,
              "amount" => 1
          ],
          "subMerchantID" => "string",
          "passengerSeqNo" => 1
      ]
  ]
)

payment.set_value('customFieldList',
  [
      "fieldName" => "TestField",
      "fieldValue" => "This is test"
  ]
)
```
