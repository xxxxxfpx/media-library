"""merge the existing file-link and GuangYaPan migration heads"""

from collections.abc import Sequence

revision: str = "merge_filelink_guangyapan_heads"
down_revision: str | Sequence[str] | None = (
    "add_filelink_type",
    "add_guangyapan_config",
)
branch_labels = None
depends_on = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
