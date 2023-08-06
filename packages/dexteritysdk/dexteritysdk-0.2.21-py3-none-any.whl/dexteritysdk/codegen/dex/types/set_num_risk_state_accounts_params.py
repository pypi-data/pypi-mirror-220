# LOCK-BEGIN[imports]: DON'T MODIFY
from dexteritysdk.solmate.dtypes import Usize
from podite import pod

# LOCK-END


# LOCK-BEGIN[class(SetNumRiskStateAccountsParams)]: DON'T MODIFY
@pod
class SetNumRiskStateAccountsParams:
    num_risk_state_accounts: Usize
    # LOCK-END

    @classmethod
    def to_bytes(cls, obj, **kwargs):
        return cls.pack(obj, converter="bytes", **kwargs)

    @classmethod
    def from_bytes(cls, raw, **kwargs):
        return cls.unpack(raw, converter="bytes", **kwargs)
