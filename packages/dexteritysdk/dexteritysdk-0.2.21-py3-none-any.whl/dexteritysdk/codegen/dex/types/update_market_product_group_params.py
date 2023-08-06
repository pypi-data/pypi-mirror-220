# LOCK-BEGIN[imports]: DON'T MODIFY
from podite import (
    FixedLenArray,
    U16,
    U8,
    pod,
)

# LOCK-END


# LOCK-BEGIN[class(UpdateMarketProductGroupParams)]: DON'T MODIFY
@pod
class UpdateMarketProductGroupParams:
    find_fees_discriminant_len: U16
    find_fees_discriminant: FixedLenArray[U8, 8]
    create_fee_state_account_discriminant: FixedLenArray[U8, 8]
    # LOCK-END

    @classmethod
    def to_bytes(cls, obj, **kwargs):
        return cls.pack(obj, converter="bytes", **kwargs)

    @classmethod
    def from_bytes(cls, raw, **kwargs):
        return cls.unpack(raw, converter="bytes", **kwargs)
