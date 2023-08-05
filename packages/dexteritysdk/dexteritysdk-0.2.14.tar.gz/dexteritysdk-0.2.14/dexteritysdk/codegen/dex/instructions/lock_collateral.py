# LOCK-BEGIN[imports]: DON'T MODIFY
from .instruction_tag import InstructionTag
from dataclasses import dataclass
from dexteritysdk.codegen.dex.types import LockCollateralParams
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


# LOCK-BEGIN[ix_cls(lock_collateral)]: DON'T MODIFY
@dataclass
class LockCollateralIx:
    program_id: PublicKey

    # account metas
    user: AccountMeta
    trader_risk_group: AccountMeta
    market_product_group: AccountMeta
    fee_model_program: AccountMeta
    fee_model_configuration_acct: AccountMeta
    fee_output_register: AccountMeta
    risk_engine_program: AccountMeta
    risk_model_configuration_acct: AccountMeta
    risk_output_register: AccountMeta
    risk_and_fee_signer: AccountMeta
    fee_state_acct: AccountMeta
    risk_state_acct: AccountMeta
    remaining_accounts: Optional[List[AccountMeta]]

    # data fields
    params: LockCollateralParams

    def to_instruction(self):
        keys = []
        keys.append(self.user)
        keys.append(self.trader_risk_group)
        keys.append(self.market_product_group)
        keys.append(self.fee_model_program)
        keys.append(self.fee_model_configuration_acct)
        keys.append(self.fee_output_register)
        keys.append(self.risk_engine_program)
        keys.append(self.risk_model_configuration_acct)
        keys.append(self.risk_output_register)
        keys.append(self.risk_and_fee_signer)
        keys.append(self.fee_state_acct)
        keys.append(self.risk_state_acct)
        if self.remaining_accounts is not None:
            keys.extend(self.remaining_accounts)

        buffer = BytesIO()
        buffer.write(InstructionTag.to_bytes(InstructionTag.LOCK_COLLATERAL))
        buffer.write(BYTES_CATALOG.pack(LockCollateralParams, self.params))

        return TransactionInstruction(
            keys=keys,
            program_id=self.program_id,
            data=buffer.getvalue(),
        )

# LOCK-END


# LOCK-BEGIN[ix_fn(lock_collateral)]: DON'T MODIFY
def lock_collateral(
    user: Union[str, PublicKey, AccountMeta],
    trader_risk_group: Union[str, PublicKey, AccountMeta],
    market_product_group: Union[str, PublicKey, AccountMeta],
    fee_model_program: Union[str, PublicKey, AccountMeta],
    fee_model_configuration_acct: Union[str, PublicKey, AccountMeta],
    fee_output_register: Union[str, PublicKey, AccountMeta],
    risk_engine_program: Union[str, PublicKey, AccountMeta],
    risk_model_configuration_acct: Union[str, PublicKey, AccountMeta],
    risk_output_register: Union[str, PublicKey, AccountMeta],
    risk_and_fee_signer: Union[str, PublicKey, AccountMeta],
    fee_state_acct: Union[str, PublicKey, AccountMeta],
    risk_state_acct: Union[str, PublicKey, AccountMeta],
    params: LockCollateralParams,
    remaining_accounts: Optional[List[AccountMeta]] = None,
    program_id: Optional[PublicKey] = None,
):
    if program_id is None:
        program_id = PublicKey("FUfpR31LmcP1VSbz5zDaM7nxnH55iBHkpwusgrnhaFjL")

    if isinstance(user, (str, PublicKey)):
        user = to_account_meta(
            user,
            is_signer=True,
            is_writable=True,
        )
    if isinstance(trader_risk_group, (str, PublicKey)):
        trader_risk_group = to_account_meta(
            trader_risk_group,
            is_signer=False,
            is_writable=True,
        )
    if isinstance(market_product_group, (str, PublicKey)):
        market_product_group = to_account_meta(
            market_product_group,
            is_signer=False,
            is_writable=True,
        )
    if isinstance(fee_model_program, (str, PublicKey)):
        fee_model_program = to_account_meta(
            fee_model_program,
            is_signer=False,
            is_writable=False,
        )
    if isinstance(fee_model_configuration_acct, (str, PublicKey)):
        fee_model_configuration_acct = to_account_meta(
            fee_model_configuration_acct,
            is_signer=False,
            is_writable=False,
        )
    if isinstance(fee_output_register, (str, PublicKey)):
        fee_output_register = to_account_meta(
            fee_output_register,
            is_signer=False,
            is_writable=True,
        )
    if isinstance(risk_engine_program, (str, PublicKey)):
        risk_engine_program = to_account_meta(
            risk_engine_program,
            is_signer=False,
            is_writable=False,
        )
    if isinstance(risk_model_configuration_acct, (str, PublicKey)):
        risk_model_configuration_acct = to_account_meta(
            risk_model_configuration_acct,
            is_signer=False,
            is_writable=False,
        )
    if isinstance(risk_output_register, (str, PublicKey)):
        risk_output_register = to_account_meta(
            risk_output_register,
            is_signer=False,
            is_writable=True,
        )
    if isinstance(risk_and_fee_signer, (str, PublicKey)):
        risk_and_fee_signer = to_account_meta(
            risk_and_fee_signer,
            is_signer=False,
            is_writable=False,
        )
    if isinstance(fee_state_acct, (str, PublicKey)):
        fee_state_acct = to_account_meta(
            fee_state_acct,
            is_signer=False,
            is_writable=True,
        )
    if isinstance(risk_state_acct, (str, PublicKey)):
        risk_state_acct = to_account_meta(
            risk_state_acct,
            is_signer=False,
            is_writable=True,
        )

    return LockCollateralIx(
        program_id=program_id,
        user=user,
        trader_risk_group=trader_risk_group,
        market_product_group=market_product_group,
        fee_model_program=fee_model_program,
        fee_model_configuration_acct=fee_model_configuration_acct,
        fee_output_register=fee_output_register,
        risk_engine_program=risk_engine_program,
        risk_model_configuration_acct=risk_model_configuration_acct,
        risk_output_register=risk_output_register,
        risk_and_fee_signer=risk_and_fee_signer,
        fee_state_acct=fee_state_acct,
        risk_state_acct=risk_state_acct,
        remaining_accounts=remaining_accounts,
        params=params,
    ).to_instruction()

# LOCK-END
