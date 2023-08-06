# LOCK-BEGIN[imports]: DON'T MODIFY
from dexteritysdk.codegen.dex.types.account_tag import AccountTag
from dexteritysdk.codegen.dex.types.fractional import Fractional
from podite import pod

# LOCK-END


# LOCK-BEGIN[class(LockedCollateral)]: DON'T MODIFY
@pod
class LockedCollateral:
    tag: "AccountTag"
    ask_qty: "Fractional"
    bid_qty: "Fractional"
    # LOCK-END

    @classmethod
    def to_bytes(cls, obj, **kwargs):
        return cls.pack(obj, converter="bytes", **kwargs)

    @classmethod
    def from_bytes(cls, raw, **kwargs):
        return cls.unpack(raw, converter="bytes", **kwargs)
