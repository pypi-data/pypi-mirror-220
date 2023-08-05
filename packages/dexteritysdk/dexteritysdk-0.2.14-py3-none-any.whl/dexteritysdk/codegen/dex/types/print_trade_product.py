# LOCK-BEGIN[imports]: DON'T MODIFY
from dexteritysdk.codegen.dex.types.fractional import Fractional
from podite import pod
from solana.publickey import PublicKey

# LOCK-END


# LOCK-BEGIN[class(PrintTradeProduct)]: DON'T MODIFY
@pod
class PrintTradeProduct:
    product_key: PublicKey
    size: Fractional
    # LOCK-END

    @classmethod
    def to_bytes(cls, obj, **kwargs):
        return cls.pack(obj, converter="bytes", **kwargs)

    @classmethod
    def from_bytes(cls, raw, **kwargs):
        return cls.unpack(raw, converter="bytes", **kwargs)
