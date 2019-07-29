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
        result = client.get_private_order_data('bito_twd', 12345678)
        print(f"[I] Invoked get_private_order_data('bito_twd', 12345678) API Result: \n    {result}\n")
        result = client.get_private_order_history()
        print(f"[I] Invoked get_private_order_history() API Result: \n    {result}\n")
        result = client.get_private_order_list('bito_twd', 1, False)
        print(f"[I] Invoked get_private_order_list('bito_twd', 1, False) API Result: \n    {result}\n")

        # Private (Write)
        # result = client.set_private_cancel_order('bito_twd', 12345678)
        # print(f"[I] Invoked set_private_cancel_order('bito_twd', 12345678) API Result: \n    {result}\n")
        # result = client.set_private_create_order('bito_twd', 'SELL', 600, 123456)
        # print(f"[I] Invoked set_private_create_order('bito_twd', 'SELL', 600, 123456) API Result: \n    {result}\n")
    except Exception as error:
        print(f"[X] {str(error)}")

        # Networking errors occurred here
        response = getattr(error, 'read', None)
        if callable(response):
            print(f"[X] {response().decode('utf-8')}")