# LOCK-BEGIN[imports]: DON'T MODIFY
from .instruction_tag import InstructionTag
from dataclasses import dataclass
from dexteritysdk.solmate.utils import to_account_meta
from io import BytesIO
from podite import BYTES_CATALOG
from solana.publickey import PublicKey
from solana.transaction import (
    AccountMeta,
    TransactionInstruction,
)
from typing import (
    List,
    Optional,
    Union,
)

# LOCK-END


# LOCK-BEGIN[ix_cls(disable_killswitch)]: DON'T MODIFY
@dataclass
class DisableKillswitchIx:
    program_id: PublicKey

    # account metas
    authority: AccountMeta
    market_product_group: AccountMeta
    remaining_accounts: Optional[List[AccountMeta]]

    def to_instruction(self):
        keys = []
        keys.append(self.authority)
        keys.append(self.market_product_group)
        if self.remaining_accounts is not None:
            keys.extend(self.remaining_accounts)

        buffer = BytesIO()
        buffer.write(InstructionTag.to_bytes(InstructionTag.DISABLE_KILLSWITCH))

        return TransactionInstruction(
            keys=keys,
            program_id=self.program_id,
            data=buffer.getvalue(),
        )

# LOCK-END


# LOCK-BEGIN[ix_fn(disable_killswitch)]: DON'T MODIFY
def disable_killswitch(
    authority: Union[str, PublicKey, AccountMeta],
    market_product_group: Union[str, PublicKey, AccountMeta],
    remaining_accounts: Optional[List[AccountMeta]] = None,
    program_id: Optional[PublicKey] = None,
):
    if program_id is None:
        program_id = PublicKey("FUfpR31LmcP1VSbz5zDaM7nxnH55iBHkpwusgrnhaFjL")

    if isinstance(authority, (str, PublicKey)):
        authority = to_account_meta(
            authority,
            is_signer=True,
            is_writable=False,
        )
    if isinstance(market_product_group, (str, PublicKey)):
        market_product_group = to_account_meta(
            market_product_group,
            is_signer=False,
            is_writable=True,
        )

    return DisableKillswitchIx(
        program_id=program_id,
        authority=authority,
        market_product_group=market_product_group,
        remaining_accounts=remaining_accounts,
    ).to_instruction()

# LOCK-END
