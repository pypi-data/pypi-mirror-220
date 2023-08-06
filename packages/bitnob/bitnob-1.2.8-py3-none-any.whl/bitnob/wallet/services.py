from bitnob.base import Bitnob, pagination_filter
from bitnob.wallet.model import Quote, Transaction

class Wallet(Bitnob): 
    def __generate_transaction_object(self, data):
        
        return Transaction(            
            reference = data.get("reference"),
            description = data.get("description"),
            amount = data.get("amount"),
            btc_amount = data.get("btcAmount"),
            sat_amount = data.get("satAmount"),
            fees = data.get("fees"),
            btc_fees = data.get("btcFees"),
            sat_fees = data.get("satFees"),
            action = data.get("action"),
            transaction_type = data.get("type"),
            status = data.get("status"),
            id = data.get("id"),
            companyId = data.get("companyId"),
            spot_price = data.get("spotPrice"),
            createdAt = data.get("createdAt"), 
            updatedAt = data.get("updatedAt"),
            address = data.get("address"),
            channel = data.get("channel"),
            chain = data.get("chain"),
            customerId = data.get("customerId")
        )

    def __generate_quote(self, data):
        return Quote(
            id = data.get("id"),
            expiration=data.get("expiration"),
            expirationInSec=data.get("expirationInSec"),
            amount= data.get("amount"),
            volume=data.get("volume"),
            price = data.get("price"),
            description = data.get("description"),
            v = data.get("__v"),
        )
    
    def wallet_detail(self):
        """
        Retrive company wallet details

        - GET Request
        """
        return self.send_request("GET", "wallets")

    def get_transaction(self, transaction_id):
        """
        Getting a transaction based on transaction_id 

        - GET Request
        """
        return self.send_request("GET", f"/transactions/{transaction_id}")
    
    def list_transactions(self, **kwargs):
        """
        Listing all transactions

        order = (optional) Result order. Accepted values: `DESC` (default), ASC
        page = (optional) Result page.
        take = (optional) Number of results per request. Accepted values: 0 - 100. Default 10
        
        - GET Request
        """
        url_params = None
        if kwargs != {}:
            url_params = pagination_filter(**kwargs)
        return self.send_request("GET", f"transactions/?{url_params}")

    def initialize_swap_usd_for_btc(self, amount):
        """
        Initialize swap USD to BTC
        amount = 30

        - POST Request
        """
        body = {
            "amount" : amount
        }

        response = self.send_request("POST", "wallets/initialize-swap-for-bitcoin", json=body)
        quote = response["data"]["quote"]
        return self.__generate_quote(data=quote)
        
    def swap_usd_to_btc(self, quote_id:str):
        """
        Finalize swap USD to BTC
        quote_id = 642af37e0ae567b6fe9a189c

        - POST Request
        """
        body = {
            "quoteId" : quote_id
        }

        response = self.send_request("POST", "wallets/finalize-swap-for-bitcoin", json=body)
        transaction = response["data"]
        return self.__generate_transaction_object(data=transaction)

    def initialize_swap_btc_for_usd(self, amount):
        """
        Initialize swap USD to BTC
        amount = 0.00001

        - POST Request
        """
        body = {
            "amount" : amount
        }

        response = self.send_request("POST", "wallets/initialize-swap-for-usd", json=body)
        quote = response["data"]["quote"]
        return self.__generate_quote(data=quote)
    
    def swap_btc_to_usd(self, quote_id:str):
        """
        Finalize swap BTC to USD
        quote_id = 642af37e0ae567b6fe9a189c

        - POST Request
        """
        body = {
            "quoteId" : quote_id
        }

        response = self.send_request("POST", "wallets/finalize-swap-for-usd", json=body)
        transaction = response["data"]
        return self.__generate_transaction_object(data=transaction)