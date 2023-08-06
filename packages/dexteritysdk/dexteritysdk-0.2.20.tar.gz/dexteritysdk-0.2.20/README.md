# Dexterity client SDK
**Dexterity** is a derivatives decentralized exchange running on Solana.
This package provides the basic blocks in order to integrate and trade on Dexterity.

You can learn more about Dexterity [here](https://docs.hxro.network/market-protocols/derivatives-protocol/dexterity).

## Prerequisites
* [Solana.py](https://pypi.org/project/solana/)

## Creating the client
First, an instance of a Solana client is required.
```python
from dexteritysdk.dex.sdk_context import SDKContext, SDKTrader
from solana.rpc.api import Client
from solana.keypair import Keypair
from solana.publickey import PublicKey

def main():
	# use "https://api.mainnet-beta.solana.com" for mainnet
	network = "https://api.devnet.solana.com"
	client = Client(network)
```

A Keypair for the payer has to also be provided.
```python
keypair = Keypair.from_secret_key(keypair_bytes)
```
The SDK also requires the **Market Product Group (MPG)** that we're going to trade on.

The public key of the default MPG is **`HiCy6vzuN3yLXD3z35D6nV7bzNLcyrvGLf3uSKuutSLo`** for mainnet or **`HyWxreWnng9ZBDPYpuYugAfpCMkRkJ1oz93oyoybDFLB`** for devnet.
```python
# mainnet MPG
mpg = PublicKey("HiCy6vzuN3yLXD3z35D6nV7bzNLcyrvGLf3uSKuutSLo")

# ** OR **
# devnet MPG
mpg = PublicKey("HyWxreWnng9ZBDPYpuYugAfpCMkRkJ1oz93oyoybDFLB")
```
Now, we're ready to get an instance of `SDKContext` for this MPG.
```python
ctx = SDKContext.connect(
	client=client,
	market_product_group_key=mpg,
	payer=keypair,
	raise_on_error=True
)
```

## Registering new trader / TRG
If you're a new trader, creation of a trading account is required.
```python
trader = ctx.register_trader(keypair)
trg_key = trader.account
```

The **Trader Risk Group (TRG)** is your trading account, that you can now use.

## Using an existing TRG
If you already have a trader set up, you need to provide the TRG public key for it.
The SDK allows you to list all your registered TRGs.
```python
# this will return a list of your all your TRG public keys
# for example: [HeykeQWRh6DC2Tz5X3WBuWdMHicyECDEFGMjomV6LBye, HeyZNJ9gQVAEqHeCFFQ781E53d66DATKXHeynwnCFBye]
trg_keys = ctx.list_trader_risk_groups()
```

After finding your TRG, you can initialise the `SDKTrader` instance.
```python
from dexteritysdk.codegen.dex.types import TraderRiskGroup
from dexteritysdk.program_ids import *
from dexteritysdk.utils.solana import explore

# ...
trader = SDKTrader.connect(ctx, trg_pubkey, keypair)
```

## Funding the TRG
To start trading, you need to deposit funds.
The tokens deposited have to be MPG vault mint tokens (e.g. USDC).
The wallet you provided will be debited.
```python
# this will deposit 733.1 USDC
trader.deposit(ctx, 733.1)
```

You can also withdraw in a similar fashion.
```python
# this will withdraw 0.1 USDC back to your wallet
trader.withdraw(ctx, 0.1)
```

You can check your balance at any time.
```python
trg, _ = trader.get_trader_risk_group()
trg.cash_balance
```

## Trading on Dexterity

### Listing trading products and order books
The `products` field of a `SDKContext` instance, is a list of the available trading products (`SDKProduct`).
Every `SDKProduct` has a `name` and a `get_orderbook(ctx)` function that will return its order book (`SDKOrderBook`).
The `SDKOrderBook` contains all `SDKOrders` on each side of the book.

Here's an example:
```python
for product in ctx.products:
	book = product.get_orderbook(ctx, refresh=True)
	print(f"Printing the order book of {product.name}")
	for order in book.bids:
		print(f"Bid of size {order.qty} at {order.price}")
	for order in book.asks:
		print(f"Ask of size {order.qty} at {order.price}")
```

### Placing an order

Placing an order is straightforward.
```python
from dexteritysdk.utils.aob import Side
# ...
order_summary = trader.place_order(ctx, product, Side.ASK, size, price)
```
The returned `SDKOrderSummary` contains the `order_id` of the new order, as well as the `remaining_qty` and `filled_qty` if your order has been filled. If the order is immediately fully filled, `order_id` will be `None`.

If there's any error, an exception will be raised.

### Cancelling orders
To cancel a previous order you can call `trader.cancel(ctx, product, order_id)`.
Following the previous example:
```python
trader.cancel(ctx, product, order_summary.order_id)
```

You can also cancel all your open orders for multiple products.
```python
# products is a list of SDKProduct
# if products list is empty or None, then all your open orders will be cancelled
products = [ctx.products[0], ctx.products[2]]
trader.cancel_all_orders(ctx, products)
```
If any cancel fails, an exception will be raised.

### Positions
Positions can also be listed, by iterating the `trader_positions` array:
```python
trg, _ = trader.get_trader_risk_group()
trg.trader_positions
```
