# LOCK-BEGIN[imports]: DON'T MODIFY
from dexteritysdk.codegen.dex.types.fractional import Fractional
from dexteritysdk.solmate.dtypes import Usize
from dexteritysdk.utils.aob.state.base import Side
from podite import pod, FixedLenArray


# LOCK-END


# LOCK-BEGIN[class(SignPrintTradeParams)]: DON'T MODIFY
@pod
class SignPrintTradeParams:
    num_products: Usize
    products: FixedLenArray["PrintTradeProductIndex", 6]
    price: Fractional
    side: Side
    operator_creator_fee_proportion: Fractional
    operator_counterparty_fee_proportion: Fractional
    use_locked_collateral: bool
    # LOCK-END

    @classmethod
    def to_bytes(cls, obj, **kwargs):
        return cls.pack(obj, converter="bytes", **kwargs)

    @classmethod
    def from_bytes(cls, raw, **kwargs):
        return cls.unpack(raw, converter="bytes", **kwargs)
