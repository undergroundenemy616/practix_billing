### Cloud Payments API Emulator

Service to emulate cloudpayments.ru API for local testing.

OpenAPI: [http://localhost/api/docs](http://localhost/api/docs)


**Setup**
1. Create .env file with sample:

`$ cp env.sample .env`

`$ vi .env`

**Run project without tests**

`$ docker-compose up --build -d`

**Single payment with cryptogram**
Endpoint: [http://localhost/payments/cards/charge](http://localhost/payments/cards/charge)

Sample POST request with JSON body:
```
{
    "Amount":10,
    "Currency":"RUB",
    "InvoiceId":"1234567",
    "IpAddress": "123.123.123.123",
    "Description":"Оплата товаров в example.com",
    "AccountId":"user_x",
    "Name":"CARDHOLDER NAME",
    "CardCryptogramPacket":"01492500008719030128SMfLeYdKp5dSQVIiO5l6ZCJiPdel4uDjdFTTz1UnXY+3QaZcNOW8lmXg0H670MclS4lI+qLkujKF4pR5Ri+T/E04Ufq3t5ntMUVLuZ998DLm+OVHV7FxIGR7snckpg47A73v7/y88Q5dxxvVZtDVi0qCcJAiZrgKLyLCqypnMfhjsgCEPF6d4OMzkgNQiynZvKysI2q+xc9cL0+CMmQTUPytnxX52k9qLNZ55cnE8kuLvqSK+TOG7Fz03moGcVvbb9XTg1oTDL4pl9rgkG3XvvTJOwol3JDxL1i6x+VpaRxpLJg0Zd9/9xRJOBMGmwAxo8/xyvGuAj85sxLJL6fA==",
    "Payer":
      { 
        "FirstName":"Тест",
        "LastName":"Тестов",
        "MiddleName":"Тестович",
        "Birth":"1955-02-24",
        "Address":"тестовый проезд дом тест",
        "Street":"Lenina",
        "City":"MO",
        "Country":"RU",
        "Phone":"123",
        "Postcode":"345"
    }
}
```

**Single payment with 3DSecure**

Endpoint: [http://localhost/payments/cards/post3ds](http://localhost/payments/cards/post3ds)

Sample POST request with JSON body:
```
{
    "TransactionId": 42,
    "PaRes": "eJxVUdtugkAQ/RXDe9mLgo0Z1nhpU9PQasWmPhLYAKksuEChfn13uVR9mGTO7MzZM2dg3qSn0Q+X\nRZIJxyAmNkZcBFmYiMgxDt7zw6MxZ+DFkvP1ngeV5AxcXhR+xEdJ6BhpEZnEYLBdfPAzg56JKSKT\nAhqgGpFB7IuSgR+cl5s3NqFTG2NAPYSUy82aETqeWPYUUAdB+ClnwSmrwtz/TbkoC0BtDYKsEqX8\nZfZkDGgAUMkTi8synyFU17V5N2nKCpBuAHRVs610VijCJgmZu17UXTxhFWP34l7evYPlegsHkO6A\n0C85o5hMsI3piNIZHc+IBaitg59qJYzgdrUOQK7/WNy+3FZAeSqV5cMqAwLe5JlQwpny8T8HdFW8\netFuBqUyahV+Hjf27vWCaSx22fe+KY6kXKZfJLK1x22TZkyUS8QiHaUGgDQN6s+H+tOq7O7kf8hd\nt30="
}
```

**Recurring payment with token**

Endpoint: [http://localhost/payments/tokens/charge](http://localhost/payments/tokens/charge)

Sample POST request with JSON body:
```
{
    "Amount": 59,
    "Currency": "RUB",
    "InvoiceId": "1234567",
    "Description": "Оплата товаров в example.com",
    "AccountId": "user_x",
    "Token": "success_1111a3e0-2428-48fb-a530-12815d90d0e8"
}
```
