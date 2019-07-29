# bitopro-api-python3

## Warning

This is an UNOFFICIAL wrapper for BitoPro exchange [HTTP API v2](https://developer.bitopro.com/docs) written in Python 3.6

USE THIS WRAPPER AT YOUR OWN RISK, I WILL NOT CORRESPOND TO ANY LOSES

## Features

- Implementation of all [public](https://developer.bitopro.com/docs#tag/public) and [private](https://developer.bitopro.com/docs#tag/authenticated) endpoints
- Simple handling of [authentication](https://developer.bitopro.com/docs#section/Authentication/signature) with API key and secret
- All HTTP raw requests and responses can be found [here](https://gist.github.com/kulisu/334854643c6351aa4b1a0a702d0bacd5)

## Donate

If you feel this wrapper saved your lifes, buy me a coffee ?

- BITO: 0x70ef948a346f96ce2929d00e389607b11e99f219
- BTC: 12axXPJG5KGsHGUdsiSmSFyh92vPcfsuFb
- ETH: 0xdbcb141a5e5867388db4e6aef21d4743cc95c84f
- LTC: LKVbc2KeDLwuPChiFYqKF8YFY2FLdCfrrr
- USDT: 14N4b217RyXoN47vvzRjmMAtdiVLXzMVNF

## Example

1. [Register an account](https://www.bitopro.com/landing_pages/reward?referrer=7907917522) with BitoPro exchange _(referral link)_
2. [Generate API key and secret](https://www.bitopro.com/api), assign relevant permissions to it
3. Clone this repository, and run `examples/all_api_endpoints.py`
4. Write your own trading policies and get profits ! 

```bash
cd ~/ && git clone https://github.com/kulisu/bitopro-api-python3
cd ~/bitopro-api-python3 && cp examples/all_api_endpoints.py .

# update mail address, API key and secret
# vim all_api_endpoints.py

python3 all_api_endpoints.py
```

```python
#!/usr/bin/env python3

from bitopro.client import Client

if __name__ == '__main__':
    client = Client('PUT_MY_EMAIL_ADDRESS_HERE', 'PUY_MY_API_KEY_HERE', 'PUY_MY_API_SECRET_HERE')

    try:
        # Public (Read)
        result = client.get_public_all_tickers()
        print(f"[I] Invoked get_public_all_tickers() API Result: \n    {result}\n")

        result = client.get_public_available_currencies()
        print(f"[I] Invoked get_public_available_currencies() API Result: \n    {result}\n")

        result = client.get_public_available_pairs()
        print(f"[I] Invoked get_public_available_pairs() API Result: \n    {result}\n")
        
        result = client.get_public_order_book('bito_twd', 10)
        print(f"[I] Invoked get_public_order_book('bito_twd', 10) API Result: \n    {result}\n")

        result = client.get_public_recent_trades('bito_twd')
        print(f"[I] Invoked get_public_recent_trades('bito_twd') API Result: \n    {result}\n")

        # Private (Read)
        result = client.get_private_account_balance()
        print(f"[I] Invoked get_private_account_balance() API Result: \n    {result}\n")

        result = client.get_private_order_data('bito_twd', 1122334455)
        print(f"[I] Invoked get_private_order_data('bito_twd', 1122334455) API Result: \n    {result}\n")

        result = client.get_private_order_history()
        print(f"[I] Invoked get_private_order_history() API Result: \n    {result}\n")

        result = client.get_private_order_list('bito_twd', 1, False)
        print(f"[I] Invoked get_private_order_list('bito_twd', 1, False) API Result: \n    {result}\n")
    except Exception as error:
        print(f"[X] {str(error)}")

        # Networking errors occurred here
        response = getattr(error, 'read', None)
        if callable(response):
            print(f"[X] {response().decode('utf-8')}")
```