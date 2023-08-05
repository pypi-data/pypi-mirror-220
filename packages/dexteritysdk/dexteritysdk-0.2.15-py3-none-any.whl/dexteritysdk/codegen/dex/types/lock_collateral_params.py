# LOCK-BEGIN[imports]: DON'T MODIFY
from dexteritysdk.solmate.dtypes import Usize
from podite import pod, FixedLenArray


# LOCK-END


# LOCK-BEGIN[class(LockCollateralParams)]: DON'T MODIFY
@pod
class LockCollateralParams:
    num_products: Usize
    products: FixedLenArray["LockedCollateralProductIndex", 6]
    # LOCK-END

    @classmethod
    def to_bytes(cls, obj, **kwargs):
        return cls.pack(obj, converter="bytes", **kwargs)

    @classmethod
    def from_bytes(cls, raw, **kwargs):
        return cls.unpack(raw, converter="bytes", **kwargs)
