# LOCK-BEGIN[imports]: DON'T MODIFY
from dexteritysdk.codegen.dex.types.fractional import Fractional
from dexteritysdk.codegen.dex.types.print_trade_products import PrintTradeProducts
from dexteritysdk.solmate.dtypes import Usize
from dexteritysdk.utils.aob.state.base import Side
from podite import (
    U8,
    pod,
)
from solana.publickey import PublicKey

# LOCK-END


# LOCK-BEGIN[class(PrintTrade)]: DON'T MODIFY
@pod
class PrintTrade:
    is_initialized: bool
    creator: PublicKey
    counterparty: PublicKey
    market_product_group: PublicKey
    num_products: Usize
    products: "PrintTradeProducts"
    price: Fractional
    side: Side
    operator: PublicKey
    operator_creator_fee_proportion: Fractional
    operator_counterparty_fee_proportion: Fractional
    is_operator_signer: bool
    is_collateral_locked: bool
    bump: U8
    # LOCK-END

    @classmethod
    def to_bytes(cls, obj, **kwargs):
        return cls.pack(obj, converter="bytes", **kwargs)

    @classmethod
    def from_bytes(cls, raw, **kwargs):
        return cls.unpack(raw, converter="bytes", **kwargs)
