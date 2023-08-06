from bitnob.base import Bitnob
from abc import ABC, abstractmethod
from bitnob.stablecoin.model import Receipt
from bitnob.wallet.model import WalletAddress, Transaction

class StableCoin(ABC):

    @abstractmethod
    def send(self):
        pass

    @abstractmethod
    def generate_address(self):
        pass

    def __generate_address_object(self, data):
        return WalletAddress(
            address = data.get("address"),
            address_type=data.get("addressType"),
            label=data.get("label")
        )
    
    def ____generate_transaction_object(self, data):
        
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
    



class USDC(StableCoin, Bitnob): 
    
    def send(self, body:dict):
        """
        Sending USDC

        body = {
            amount: 3000,
            address: "tb1q9h0yjdupyfpxfjg24rpx755xrplvzd9hz2nj7v",
            chain: "BSC"
            description: "lorem ipsum",
        } 

        - POST Request
        """
        required_data = ["amount", "address", "chain"]
        self.check_required_data(required_data, body)

        response = self.send_request("POST", "wallets/send-usdc", json=body)
        return self.(data=response["data"])


    def generate_address(self, body:dict):
        """
        Generate Address for Customer

        body = {
            "label": "purchase xbox",
            "customerEmail": "customer@gmail.com",
            "chain": "BSC"
        }

        - POST Request
        """
        required_data = ["customerEmail", "chain"]
        self.check_required_data(required_data, body)

        response =  self.send_request("POST", "addresses/generate/usdc", json=body)
        return self.__generate_address_object(data=response["data"])

class USDT(StableCoin, Bitnob): 
    
    def send(self, body:dict):
        """
        Sending USDC

        body = {
            amount: 3000,
            address: "tb1q9h0yjdupyfpxfjg24rpx755xrplvzd9hz2nj7v",
            chain: "BSC",
            description: "lorem ipsum",
        } 

        - POST Request
        """
        required_data = ["amount", "address", "chain"]
        self.check_required_data(required_data, body)

        response = self.send_request("POST", "wallets/send-usdt", json=body)
        return self.__generate_transaction_object(data=response["data"])

    def generate_address(self, body:dict):
        """
        Generate Address for Customer

        body = {
            "label": "purchase xbox",
            "customerEmail": "customer@gmail.com"
            "chain": "BSC"
        }

        - POST Request
        """
        required_data = ["customerEmail", "chain"]
        self.check_required_data(required_data, body)

        response =  self.send_request("POST", "addresses/generate/usdt", json=body)
        return self.__generate_address_object(data=response["data"])