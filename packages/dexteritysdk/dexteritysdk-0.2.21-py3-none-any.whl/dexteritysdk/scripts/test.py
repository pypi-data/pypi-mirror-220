import json
from random import random
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
    trader.subscribe(ctx, 'ws://localhost:8900')
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

    tick = 0.1
    size, price = tick, 100

    print('checking open orders...', end='', flush=True)
    open_orders = list(trader.open_orders(ctx))
    if len(open_orders) != 0:
        print("printing open orders")
        for o in open_orders:
            print(o)
        raise RuntimeError(f"expected zero open orders but saw but saw {len(open_orders)} open orders")
    print('success')

    for product in ctx.products:
        client_order_id = int(random() * 1e6)
        print(f"placing order with client_order_id={client_order_id} on {product.name}...", end='', flush=True)
        trader.place_order(ctx, product, Side.ASK, size, price, client_order_id=client_order_id)
        print('success')

        print('checking open orders...', end='', flush=True)
        open_orders = list(trader.open_orders(ctx))
        if len(open_orders) != 1:
            print("printing open orders")
            for o in open_orders:
                print(o)
            raise RuntimeError(f"expected 1 open order but saw {len(open_orders)} open orders")
        if open_orders[0].client_order_id != client_order_id:
            print("printing open orders")
            for o in open_orders:
                print(o)
            raise RuntimeError(f"expected 1 open order but saw {len(open_orders)} open orders")
        print('success')

        print(f"cancelling order with client_order_id={client_order_id} on {product.name}...", end='', flush=True)
        trader.cancel(ctx, product, 0, client_order_id=client_order_id)
        print('success')

        print('waiting a few seconds for the crank...', end='', flush=True)
        time.sleep(3)
        print('done waiting')
        print('checking open orders...', end='', flush=True)
        open_orders = list(trader.open_orders(ctx))
        if len(open_orders) != 0:
            print("printing open orders")
            for o in open_orders:
                print(o)
            raise RuntimeError(f"expected zero open orders but saw but saw {len(open_orders)} open orders")
        print('success')

    print('success')

    print('waiting a few seconds for the crank...', end='', flush=True)
    time.sleep(3)
    print('done waiting')
    print('checking open orders...', end='', flush=True)
    open_orders = list(trader.open_orders(ctx))
    if len(open_orders) != 0:
        print("printing open orders")
        for o in open_orders:
            print(o)
        raise RuntimeError(f"expected zero open orders but saw but saw {len(open_orders)} open orders")
    print('success')

    for product in ctx.products:
        print(f"placing order on {product.name}...", end='', flush=True)
        order_summary = trader.place_order(ctx, product, Side.ASK, size, price)
        print('success')

    batch_size = 1
    print(f"calling cancel_all_orders (batch size = {batch_size})...", end='', flush=True)
    trader.cancel_all_orders(ctx, no_err=True, batch_size=batch_size)
    print('success')

    batch_size = 2
    for product in ctx.products:
        for i in range(batch_size):
            print(f"placing order on {product.name}...", end='', flush=True)
            order_summary = trader.place_order(ctx, product, Side.ASK, size + i*tick, price)
            print('success')

    print(f"calling cancel_all_orders (batch size = {batch_size})...", end='', flush=True)
    trader.cancel_all_orders(ctx, no_err=True, batch_size=batch_size)
    print('success')

    batch_size = 4
    for product in ctx.products:
        for i in range(batch_size):
            print(f"placing order on {product.name}...", end='', flush=True)
            order_summary = trader.place_order(ctx, product, Side.ASK, size + i*tick, price)
            print('success')

    print(f"calling cancel_all_orders (batch size = {batch_size})...", end='', flush=True)
    trader.cancel_all_orders(ctx, no_err=True, batch_size=batch_size)
    print('success')

    batch_size = 8
    for product in ctx.products:
        for i in range(batch_size):
            print(f"placing order on {product.name}...", end='', flush=True)
            order_summary = trader.place_order(ctx, product, Side.ASK, size + i*tick, price)
            print('success')

    print(f"calling cancel_all_orders (batch size = {batch_size})...", end='', flush=True)
    trader.cancel_all_orders(ctx, no_err=True, batch_size=batch_size)
    print('success')

    batch_size = 16
    for product in ctx.products:
        for i in range(batch_size):
            print(f"placing order on {product.name}...", end='', flush=True)
            order_summary = trader.place_order(ctx, product, Side.ASK, size + i*tick, price)
            print('success')

    print(f"calling cancel_all_orders (batch size = {batch_size})...", end='', flush=True)
    trader.cancel_all_orders(ctx, no_err=True, batch_size=batch_size)
    print('success')

    for product in ctx.products:
        print(f"placing order on {product.name}...", end='', flush=True)
        order_summary = trader.place_order(ctx, product, Side.ASK, size, price)
        print('success')

        print(f"replacing order on {product.name}...", end='', flush=True)
        order_summary = trader.replace(
            ctx,
            product,
            order_summary.order_id,
            Side.ASK,
            size,
            price,
        )
        print('success')

        print(f"cancelling order on {product.name}...", end='', flush=True)
        trader.cancel(ctx, product, order_summary.order_id)
        print('success')
    print('success')

    print('waiting a few seconds for the crank...', end='', flush=True)
    time.sleep(3)
    print('done waiting')
    print('checking open orders...', end='', flush=True)
    open_orders = list(trader.open_orders(ctx))
    if len(open_orders) != 0:
        print("printing open orders")
        for o in open_orders:
            print(o)
        raise RuntimeError(f"expected zero open orders but saw but saw {len(open_orders)} open orders")
    print('success')

main()
