# LOCK-BEGIN[imports]: DON'T MODIFY
from dexteritysdk.solmate.anchor import InstructionDiscriminant
from podite import (
    Enum,
    U64,
    pod,
)

# LOCK-END


# LOCK-BEGIN[instruction_tag]: DON'T MODIFY
@pod
class InstructionTag(Enum[U64]):
    RESIZE_VARIANCE_CACHE = InstructionDiscriminant()
    VALIDATE_ACCOUNT_HEALTH = InstructionDiscriminant()
    VALIDATE_ACCOUNT_LIQUIDATION = InstructionDiscriminant()
    CREATE_RISK_STATE_ACCOUNT = InstructionDiscriminant()
    INITIALIZE_COVARIANCE_MATRIX = InstructionDiscriminant()
    INITIALIZE_MARK_PRICES = InstructionDiscriminant()
    CLOSE_MARK_PRICES = InstructionDiscriminant()
    UPDATE_MARK_PRICES = InstructionDiscriminant()
    REMOVE_MARKET_PRODUCT_INDEX_FROM_VARIANCE_CACHE = InstructionDiscriminant()
    # LOCK-END
