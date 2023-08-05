import json
import sys
print('importing dexterity (it takes a while)...', end='', flush=True)
from dexteritysdk.dex.sdk_context import SDKContext, SDKTrader
from dexteritysdk.utils.aob import Side
print('success')
from solana.rpc.api import Client
from solana.keypair import Keypair
from solana.publickey import PublicKey

def load_keypair(fp):
    with open(fp, "r") as f:
        kp = json.load(f)
    return Keypair(kp).from_secret_key(kp)

def main():
    network = "http://localhost:8899/"
    client = Client(network)

    print('loading keypairs...', end='', flush=True)
    keypair = load_keypair('../deploy_key.json')
    mpg_keypair = load_keypair('../target/deploy/mpg-keypair.json')
    print('success')

    print('connecting...', end='', flush=True)
    ctx = SDKContext.connect(
	client=client,
	market_product_group_key=mpg_keypair.public_key,
	payer=keypair,
	raise_on_error=True
    )
    print('success')

    print('creating new trg...', end='', flush=True)
    trader = ctx.register_trader(keypair)
    print('success (trg pubkey: {})'.format(trader.account))

    print('depositing 100k USDC...', end='', flush=True)
    trader.deposit(ctx, 100000)
    print('success')

    print('withdrawing 1k USDC...', end='', flush=True)
    trader.withdraw(ctx, 1000)
    print('success')

    print('checking balance...', end='', flush=True)
    trg, _ = trader.get_trader_risk_group()
    trg.cash_balance
    print('success... (cash balance: {})'.format(trg.cash_balance))

    print('checking balance...', end='', flush=True)
    trg, _ = trader.get_trader_risk_group()
    trg.cash_balance
    print('success... (cash balance: {})'.format(trg.cash_balance))

    print('listing products and placing and cancelling orders...')
    for product in ctx.products:
        print(f"placing order on {product.name}...", end='', flush=True)
        size, price = 1, 100
        order_summary = trader.place_order(ctx, product, Side.ASK, size, price)
        print('success')
        print(f"cancelling order on {product.name}...", end='', flush=True)
        trader.cancel(ctx, product, order_summary.order_id)
        print('success')
    print('success')

    

main()
