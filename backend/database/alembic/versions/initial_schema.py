"""initial_schema

Revision ID: initial_schema
Revises:
Create Date: 2026-08-18 00:00:00.000000

当前 ORM 模型对应的初始数据库架构。
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "initial_schema"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _enum_types():
    return (
        sa.Enum(
            "Source", "Movie", "Series", "Season", "Episode",
            "BoxSet", "Genre", "Person", "Studio", "Tag",
            name="media_type_enum",
        ),
        sa.Enum("Continuing", "Ended", "Cancelled", name="item_status_enum"),
        sa.Enum(
            "Image", "Video", "Subtitle", "EmbeddedImage", "Attachment", "Data", "Other",
            name="file_type_enum",
        ),
        sa.Enum("MediaSource", "Image", "Chapter", name="file_link_type_enum"),
        sa.Enum(
            "Primary", "Art", "Backdrop", "Banner", "Logo", "Thumb", "Disc", "Box",
            "BoxRear", "Profile", "Chapter", "Screenshot", "Menu",
            name="image_type_enum",
        ),
        sa.Enum("Chapter", "IntroStart", "IntroEnd", "CreditsStart", name="chapter_marker_type_enum"),
        sa.Enum(
            "Actor", "Director", "Writer", "Producer", "Composer", "Conductor",
            "Lyricist", "GuestStar",
            name="person_type_enum",
        ),
    )


def upgrade() -> None:
    media_type_enum, item_status_enum, file_type_enum, file_link_type_enum, image_type_enum, chapter_marker_type_enum, person_type_enum = _enum_types()

    op.create_table(
        "Files",
        sa.Column("Id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("Etag", sa.String(64), nullable=True),
        sa.Column("Size", sa.BigInteger(), nullable=True),
        sa.Column("Name", sa.Text(), nullable=True),
        sa.Column("SortName", sa.Text(), nullable=True),
        sa.Column("Path", sa.Text(), nullable=False),
        sa.Column("CloudId", sa.String(255), nullable=True),
        sa.Column("Type", file_type_enum, nullable=False),
        sa.Column("FFmpeg", sa.JSON(), nullable=True),
        sa.Column("CreatedAt", sa.DateTime(timezone=True), nullable=False),
        sa.Column("UpdatedAt", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("idx_files_etag", "Files", ["Etag"])
    op.create_index("idx_files_path", "Files", ["Path"], unique=True)
    op.create_index("idx_files_cloud_id", "Files", ["CloudId"], unique=True)

    op.create_table(
        "MediaItems",
        sa.Column("Id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("Type", media_type_enum, nullable=False),
        sa.Column("Name", sa.String(500), nullable=True),
        sa.Column("Overview", sa.Text(), nullable=True),
        sa.Column("Tagline", sa.Text(), nullable=True),
        sa.Column("EndDate", sa.DateTime(timezone=True), nullable=True),
        sa.Column("StartDate", sa.DateTime(timezone=True), nullable=True),
        sa.Column("OfficialRating", sa.String(255), nullable=True),
        sa.Column("CustomRating", sa.String(255), nullable=True),
        sa.Column("CommunityRating", sa.Float(), nullable=True),
        sa.Column("CriticRating", sa.Float(), nullable=True),
        sa.Column("Status", item_status_enum, nullable=True),
        sa.Column("DateCreated", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("DateModified", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("CreatedAt", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("UpdatedAt", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("IsDeleted", sa.Boolean(), server_default=sa.false(), nullable=False),
        sa.Column("PresentationUniqueKey", sa.Text(), nullable=True),
        sa.Column("LockedFields", sa.JSON(), nullable=True),
        sa.Column("SourceId", sa.String(255), nullable=True),
        sa.Column(
            "SourceItemId",
            sa.Integer(),
            sa.ForeignKey("MediaItems.Id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("RunTimeTicks", sa.BigInteger(), nullable=True),
        sa.Column("BirthPlace", sa.String(500), nullable=True),
        sa.Column("GenreName", sa.String(255), nullable=True),
        sa.Column("StudioName", sa.String(255), nullable=True),
        sa.Column("LabelName", sa.String(255), nullable=True),
        sa.CheckConstraint(
            "CommunityRating IS NULL OR (CommunityRating >= 0 AND CommunityRating <= 10)",
            name="ck_media_items_community_rating_range",
        ),
        sa.CheckConstraint(
            "CriticRating IS NULL OR (CriticRating >= 0 AND CriticRating <= 100)",
            name="ck_media_items_critic_rating_range",
        ),
        sa.CheckConstraint(
            "RunTimeTicks IS NULL OR RunTimeTicks >= 0",
            name="ck_media_items_runtime_ticks_non_negative",
        ),
        sa.CheckConstraint(
            "StartDate IS NULL OR EndDate IS NULL OR EndDate >= StartDate",
            name="ck_media_items_dates_order",
        ),
    )
    op.create_index("idx_media_items_type", "MediaItems", ["Type"])
    op.create_index("idx_media_items_name", "MediaItems", ["Name"])
    op.create_index("idx_media_items_start_date", "MediaItems", ["StartDate"])
    op.create_index("idx_media_items_community_rating", "MediaItems", ["CommunityRating"])
    op.create_index("idx_media_items_is_deleted", "MediaItems", ["IsDeleted"])
    op.create_index("idx_media_items_type_is_deleted", "MediaItems", ["Type", "IsDeleted"])
    op.create_index(
        "idx_media_items_type_is_deleted_created",
        "MediaItems",
        ["Type", "IsDeleted", "DateCreated"],
    )
    op.create_index(
        "idx_media_items_type_is_deleted_name",
        "MediaItems",
        ["Type", "IsDeleted", "Name"],
    )
    op.create_index(
        "idx_media_items_type_is_deleted_rating",
        "MediaItems",
        ["Type", "IsDeleted", "CommunityRating"],
    )
    op.create_index("idx_media_items_source_item", "MediaItems", ["SourceItemId"])
    op.create_index("idx_media_items_source_id", "MediaItems", ["SourceId"])
    op.create_index(
        "idx_media_items_source_item_type",
        "MediaItems",
        ["SourceItemId", "SourceId", "Type"],
    )
    op.create_index(
        "idx_media_items_active_date_created",
        "MediaItems",
        ["DateCreated", "Id"],
        sqlite_where=sa.text('"IsDeleted" = 0'),
        postgresql_where=sa.text('"IsDeleted" = false'),
    )
    op.create_index(
        "idx_media_items_active_name",
        "MediaItems",
        ["Name", "Id"],
        sqlite_where=sa.text('"IsDeleted" = 0'),
        postgresql_where=sa.text('"IsDeleted" = false'),
    )
    op.create_index(
        "uq_media_items_source_key",
        "MediaItems",
        ["SourceItemId", "SourceId", "Type"],
        unique=True,
        sqlite_where=sa.text(
            '"IsDeleted" = 0 AND "SourceItemId" IS NOT NULL AND "SourceId" IS NOT NULL'
        ),
        postgresql_where=sa.text(
            '"IsDeleted" = false AND "SourceItemId" IS NOT NULL AND "SourceId" IS NOT NULL'
        ),
    )

    op.create_table(
        "Users",
        sa.Column("Id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("Name", sa.String(255), nullable=False),
        sa.Column("PasswordHash", sa.String(255), nullable=False),
        sa.Column("Salt", sa.String(255), nullable=False),
        sa.Column("Email", sa.String(255), nullable=True),
        sa.Column("IsAdmin", sa.Boolean(), nullable=False),
        sa.Column("IsActive", sa.Boolean(), nullable=False),
        sa.Column("Setting", sa.JSON(), nullable=True),
        sa.Column("CreatedAt", sa.DateTime(timezone=True), nullable=False),
        sa.Column("UpdatedAt", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("idx_users_name", "Users", ["Name"])
    op.create_index("idx_users_email", "Users", ["Email"])

    op.create_table(
        "FileLinks",
        sa.Column("Id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column(
            "ItemId",
            sa.Integer(),
            sa.ForeignKey("MediaItems.Id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "FileId",
            sa.Integer(),
            sa.ForeignKey("Files.Id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("LinkType", file_link_type_enum, nullable=False),
        sa.Column("ImageType", image_type_enum, nullable=True),
        sa.Column("ImageIndex", sa.Integer(), nullable=False),
        sa.Column("ChapterIndex", sa.Integer(), nullable=True),
        sa.Column("ChapterName", sa.Text(), nullable=True),
        sa.Column("StartPositionTicks", sa.BigInteger(), nullable=True),
        sa.Column("MarkerType", chapter_marker_type_enum, nullable=True),
        sa.Column("CreatedAt", sa.DateTime(timezone=True), nullable=False),
        sa.Column("UpdatedAt", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("idx_file_links_file", "FileLinks", ["FileId"])
    op.create_index("idx_file_links_chapter", "FileLinks", ["ItemId", "ChapterIndex"])
    op.create_index("idx_file_links_item_file", "FileLinks", ["ItemId", "FileId"])
    op.create_index("idx_file_links_item_image_type", "FileLinks", ["ItemId", "ImageType"])

    op.create_table(
        "ItemLinks",
        sa.Column("Id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column(
            "ItemId",
            sa.Integer(),
            sa.ForeignKey("MediaItems.Id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "LinkedItemId",
            sa.Integer(),
            sa.ForeignKey("MediaItems.Id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("PeopleType", person_type_enum, nullable=True),
        sa.Column("PeopleRole", sa.Text(), nullable=True),
        sa.Column("Order", sa.Integer(), nullable=True),
        sa.Column("CreatedAt", sa.DateTime(timezone=True), nullable=False),
        sa.Column("UpdatedAt", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("ItemId", "LinkedItemId", name="uq_item_links_item_linked"),
    )
    op.create_index("idx_item_links_people_type", "ItemLinks", ["PeopleType"])
    op.create_index("idx_item_links_linked_item_item", "ItemLinks", ["LinkedItemId", "ItemId"])
    op.create_index("idx_item_links_linked_item_order", "ItemLinks", ["LinkedItemId", "Order"])
    op.create_index("idx_item_links_item_people_type", "ItemLinks", ["ItemId", "PeopleType"])

    op.create_table(
        "UserData",
        sa.Column(
            "UserId",
            sa.Integer(),
            sa.ForeignKey("Users.Id", ondelete="CASCADE"),
            primary_key=True,
        ),
        sa.Column(
            "ItemId",
            sa.Integer(),
            sa.ForeignKey("MediaItems.Id", ondelete="CASCADE"),
            primary_key=True,
        ),
        sa.Column("PlaybackPositionTicks", sa.Float(), nullable=False),
        sa.Column("PlayCount", sa.Integer(), nullable=False),
        sa.Column("IsPlayed", sa.Boolean(), nullable=False),
        sa.Column("Rating", sa.Float(), nullable=True),
        sa.Column("PlaybackRate", sa.Float(), nullable=False),
        sa.Column("LastPlayedAt", sa.DateTime(timezone=True), nullable=True),
        sa.Column("FavoritedAt", sa.DateTime(timezone=True), nullable=True),
        sa.Column("CreatedAt", sa.DateTime(timezone=True), nullable=False),
        sa.Column("UpdatedAt", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("idx_user_data_favorited_at", "UserData", ["FavoritedAt"])
    op.create_index("idx_user_data_item_user", "UserData", ["ItemId", "UserId"])
    op.create_index("idx_user_data_user_favorited", "UserData", ["UserId", "FavoritedAt"])
    op.create_index("idx_user_data_user_last_played", "UserData", ["UserId", "LastPlayedAt"])
    op.create_index("idx_user_data_user_rating", "UserData", ["UserId", "Rating"])

    op.create_table(
        "Aliases",
        sa.Column(
            "ItemId",
            sa.Integer(),
            sa.ForeignKey("MediaItems.Id", ondelete="CASCADE"),
            primary_key=True,
        ),
        sa.Column("Name", sa.Text(), primary_key=True),
        sa.Column("Source", sa.Text(), nullable=True),
        sa.Column("CreatedAt", sa.DateTime(timezone=True), nullable=False),
        sa.Column("UpdatedAt", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("idx_aliases_name", "Aliases", ["Name"])
    op.create_index("idx_aliases_source", "Aliases", ["Source", "ItemId"])


def downgrade() -> None:
    op.drop_table("Aliases")
    op.drop_table("UserData")
    op.drop_table("ItemLinks")
    op.drop_table("FileLinks")
    op.drop_table("Users")
    op.drop_table("MediaItems")
    op.drop_table("Files")

    bind = op.get_bind()
    for enum_type in reversed(_enum_types()):
        enum_type.drop(bind, checkfirst=True)
