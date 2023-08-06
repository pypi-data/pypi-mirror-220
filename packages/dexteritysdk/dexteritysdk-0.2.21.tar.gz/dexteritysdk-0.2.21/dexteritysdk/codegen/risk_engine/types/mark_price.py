# LOCK-BEGIN[imports]: DON'T MODIFY
from dexteritysdk.codegen.dex.types.fractional import Fractional
from dexteritysdk.codegen.risk_engine.types.fast_int import FastInt
from podite import (
    FixedLenArray,
    U64,
    U8,
    pod,
)
from solana.publickey import PublicKey

# LOCK-END


# LOCK-BEGIN[class(MarkPrice)]: DON'T MODIFY
@pod
class MarkPrice:
    product_key: PublicKey
    mark_price: FastInt
    prev_oracle_minus_book_ewma: FastInt
    oracle_minus_book_ewma: FastInt
    update_slot: U64
    is_qualifying_bid_price_some: U8
    _padding0: FixedLenArray[U8, 7]
    qualifying_bid_price: Fractional
    is_qualifying_ask_price_some: U8
    _padding1: FixedLenArray[U8, 7]
    qualifying_ask_price: Fractional
    # LOCK-END

    @classmethod
    def to_bytes(cls, obj, **kwargs):
        return cls.pack(obj, converter="bytes", **kwargs)

    @classmethod
    def from_bytes(cls, raw, **kwargs):
        return cls.unpack(raw, converter="bytes", **kwargs)
