"""merge the existing file-link and GuangYaPan migration heads"""

from typing import Sequence, Union

from alembic import op


revision: str = "merge_filelink_guangyapan_heads"
down_revision: Union[str, Sequence[str], None] = (
    "add_filelink_type",
    "add_guangyapan_config",
)
branch_labels = None
depends_on = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
