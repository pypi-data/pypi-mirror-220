class WalletAddress:
    def __init__(self,address, address_type, label=None) -> None:
        self.address = address
        self.address_type = address_type
        self.label = label

class Transaction:
    def __init__(self, id, reference, amount, 
                btc_amount, fees, btc_fees, sat_fees, 
                sat_amount, spot_price, action,
                transaction_type, status,description,
                companyId, createdAt, updatedAt, 
                address, channel, chain,
                customerId) -> None:
        self.id = id
        self.reference = reference
        self.amount = amount
        self.btc_amount = btc_amount
        self.btc_fees = btc_fees
        self.fees = fees
        self.sat_fees = sat_fees
        self.sat_amount = sat_amount
        self.spot_price = spot_price
        self.transaction_type = transaction_type
        self.status = status
        self.action = action
        self.description = description
        self.company_id = companyId
        self.created_at = createdAt
        self.updated_at = updatedAt
        self.address = address
        self.channel = channel
        self.chain = chain
        self.customer_id = customerId


class Quote: 
    def __init__(self, id, expiration, expirationInSec, amount, volume, price, v, description) -> None:
        self.id = id
        self.expiration = expiration
        self.expiration_in_sec = expirationInSec
        self.amount = amount 
        self.volume = volume
        self.price = price
        self.v = v
        self.description = description