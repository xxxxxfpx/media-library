"""
数据库测试数据填充脚本
========================

功能：创建媒体源、电影、剧集、季度、剧集、音乐、图书等测试数据。
通过 ItemLinks 将内容项关联到对应媒体源，并建立 Series→Season→Episode 层级关系。

作者：白鸟青城
版本：4.0.0 (移除 Path 字段)
"""

import asyncio
import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from config import get_config
from database.models import (
    MediaItem, ItemLinks, File, FileLink, FileType, ImageType,
    ItemLinkType, PersonType, MediaType, Base
)

config = get_config()


def get_engine():
    if config.database.type == "sqlite":
        url = f"sqlite+aiosqlite:///{config.database.sqlite_path}"
    else:
        url = f"postgresql+asyncpg://{config.database.username}:{config.database.password}@{config.database.host}:{config.database.port}/{config.database.database}"
    return create_async_engine(url, echo=False)


async def create_seed_data():
    engine = get_engine()

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("数据库表已创建/已存在")

    async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session_maker() as db:
        print("开始创建测试数据...")

        sources_data = [
            {"name": "电影源", "overview": "收藏的电影作品", "key": "movies", "id": "source-movie-001", "link": "/sources/movies"},
            {"name": "剧集源", "overview": "收录的电视剧集", "key": "tvshows", "id": "source-tv-001", "link": "/sources/tv"},
            {"name": "音乐源", "overview": "珍藏的音乐专辑和单曲", "key": "music", "id": "source-music-001", "link": "/sources/music"},
            {"name": "图书源", "overview": "电子书和文档资料", "key": "books", "id": "source-book-001", "link": "/sources/books"},
        ]
        source_map = {}
        for src in sources_data:
            source = MediaItem(
                Type=MediaType.Source,
                Name=src["name"],
                Overview=src["overview"],
            )
            db.add(source)
            await db.flush()
            source_map[src["key"]] = {"item": source, "source_id": src["id"], "source_link": src["link"]}
            print(f"创建媒体源: ID={source.Id}, Name={source.Name}")

        movies_data = [
            {"name": "星际穿越", "overview": "一组宇航员穿越虫洞，寻找人类新家园的科幻史诗。", "year": 2014},
            {"name": "盗梦空间", "overview": "窃取他人梦境中的秘密，植入思想的惊险之旅。", "year": 2010},
            {"name": "黑客帝国", "overview": "一名黑客发现现实世界其实是人工智能的模拟。", "year": 1999},
            {"name": "肖申克的救赎", "overview": "银行家安迪因冤案入狱，用智慧和毅力在肖申克监狱中寻找自由。", "year": 1994},
            {"name": "阿甘正传", "overview": "智商只有75的阿甘，凭借纯真和执着创造了不可思议的人生。", "year": 1994},
        ]
        movies = []
        for data in movies_data:
            movie = MediaItem(
                Type=MediaType.Movie,
                Name=data["name"],
                Overview=data["overview"],
                ProductionYear=data["year"],
                RunTimeTicks=72000000000,
            )
            db.add(movie)
            movies.append(movie)
        await db.flush()
        print(f"创建 {len(movies)} 部电影")

        src_movie = source_map["movies"]
        for movie in movies:
            link = ItemLinks(
                ItemId=movie.Id,
                LinkedItemId=src_movie["item"].Id,
                Type=ItemLinkType.Source,
                SourceId=src_movie["source_id"],
                SourceLink=src_movie["source_link"],
            )
            db.add(link)
        await db.flush()
        print(f"创建电影→电影源关联: {len(movies)} 条")

        series_data = [
            {"name": "绝命毒师", "overview": "高中化学老师沃特·怀特身患绝症后，与昔日学生联手制造冰毒的故事。", "year": 2008},
            {"name": "权力的游戏", "overview": "维斯特洛大陆上七大王国争夺铁王座的史诗奇幻故事。", "year": 2011},
            {"name": "行尸走肉", "overview": "丧尸末世中，一群幸存者为了活下去而战斗的故事。", "year": 2010},
        ]
        series_items = []
        for data in series_data:
            series = MediaItem(
                Type=MediaType.Series,
                Name=data["name"],
                Overview=data["overview"],
                ProductionYear=data["year"],
            )
            db.add(series)
            series_items.append(series)
        await db.flush()
        print(f"创建 {len(series_items)} 个系列")

        seasons_data = []
        for series in series_items:
            for i in range(1, 3):
                season = MediaItem(
                    Type=MediaType.Season,
                    Name=f"{series.Name} 第{i}季",
                )
                db.add(season)
                seasons_data.append({"season": season, "series": series, "season_num": i})
        await db.flush()
        print(f"创建 {len(seasons_data)} 个季度")

        episodes = []
        for season_info in seasons_data:
            for ep_num in range(1, 11):
                episode = MediaItem(
                    Type=MediaType.Episode,
                    Name=f"{season_info['season'].Name} 第{ep_num}集",
                    RunTimeTicks=27000000000,
                )
                db.add(episode)
                episodes.append(episode)
        await db.flush()
        print(f"创建 {len(episodes)} 个剧集")

        for season_info in seasons_data:
            series_link = ItemLinks(
                ItemId=season_info["series"].Id,
                LinkedItemId=season_info["season"].Id,
                Type=ItemLinkType.SeriesSeason,
            )
            db.add(series_link)
        print(f"创建 Series→Season 层级关联: {len(seasons_data)} 条")

        ep_by_season = {}
        for season_info in seasons_data:
            ep_by_season[season_info["season"].Id] = []
        for ep in episodes:
            for season_info in seasons_data:
                if season_info["series"].Name in ep.Name and f"Season {season_info['season_num']}" in ep.Name:
                    ep_by_season[season_info["season"].Id].append(ep)
                    break

        for season_id, ep_list in ep_by_season.items():
            for ep in ep_list:
                season_ep_link = ItemLinks(
                    ItemId=season_id,
                    LinkedItemId=ep.Id,
                    Type=ItemLinkType.SeasonEpisode,
                )
                db.add(season_ep_link)
        print(f"创建 Season→Episode 层级关联: {len(episodes)} 条")

        src_tv = source_map["tvshows"]
        all_tv_items = series_items + [s["season"] for s in seasons_data] + episodes
        for item in all_tv_items:
            link = ItemLinks(
                ItemId=item.Id,
                LinkedItemId=src_tv["item"].Id,
                Type=ItemLinkType.Source,
                SourceId=src_tv["source_id"],
                SourceLink=src_tv["source_link"],
            )
            db.add(link)
        await db.flush()
        print(f"创建系列→剧集源关联: {len(all_tv_items)} 条")

        audio_data = [
            {"name": "Bohemian Rhapsody", "overview": "Queen 经典摇滚名曲", "year": 1975},
            {"name": "Hotel California", "overview": "Eagles 标志性歌曲", "year": 1976},
            {"name": "天空之城", "overview": "久石让经典电影原声", "year": 1986},
        ]
        audios = []
        for data in audio_data:
            audio = MediaItem(
                Type=MediaType.Audio,
                Name=data["name"],
                Overview=data["overview"],
                ProductionYear=data["year"],
            )
            db.add(audio)
            audios.append(audio)
        await db.flush()
        print(f"创建 {len(audios)} 个音乐")

        src_music = source_map["music"]
        for audio in audios:
            link = ItemLinks(
                ItemId=audio.Id,
                LinkedItemId=src_music["item"].Id,
                Type=ItemLinkType.Source,
                SourceId=src_music["source_id"],
                SourceLink=src_music["source_link"],
            )
            db.add(link)
        await db.flush()
        print(f"创建音乐→音乐源关联: {len(audios)} 条")

        book_data = [
            {"name": "三体", "overview": "刘慈欣创作的科幻巨著", "year": 2008},
            {"name": "百年孤独", "overview": "加西亚·马尔克斯的魔幻现实主义经典", "year": 1967},
        ]
        books = []
        for data in book_data:
            book = MediaItem(
                Type=MediaType.Book,
                Name=data["name"],
                Overview=data["overview"],
                ProductionYear=data["year"],
            )
            db.add(book)
            books.append(book)
        await db.flush()
        print(f"创建 {len(books)} 本图书")

        src_book = source_map["books"]
        for book in books:
            link = ItemLinks(
                ItemId=book.Id,
                LinkedItemId=src_book["item"].Id,
                Type=ItemLinkType.Source,
                SourceId=src_book["source_id"],
                SourceLink=src_book["source_link"],
            )
            db.add(link)
        await db.flush()
        print(f"创建图书→图书源关联: {len(books)} 条")

        genres_data = ["科幻", "动作", "惊悚", "冒险", "剧情", "悬疑", "奇幻"]
        genres = []
        for name in genres_data:
            genre = MediaItem(Type=MediaType.Genre, Name=name)
            db.add(genre)
            genres.append(genre)
        await db.flush()
        print(f"创建 {len(genres)} 个标签")

        studios_data = ["华纳兄弟", "环球影业", "派拉蒙", "索尼影业", "迪士尼"]
        studios = []
        for name in studios_data:
            studio = MediaItem(Type=MediaType.Studio, Name=name)
            db.add(studio)
            studios.append(studio)
        await db.flush()
        print(f"创建 {len(studios)} 个工作室")

        persons_data = [
            {"name": "克里斯托弗·诺兰", "type": PersonType.Director},
            {"name": "马修·麦康纳", "type": PersonType.Actor},
            {"name": "安妮·海瑟薇", "type": PersonType.Actor},
            {"name": "莱昂纳多·迪卡普里奥", "type": PersonType.Actor},
            {"name": "约瑟夫·高登-莱维特", "type": PersonType.Actor},
            {"name": "艾伦·佩吉", "type": PersonType.Actor},
            {"name": "基努·里维斯", "type": PersonType.Actor},
            {"name": "劳伦斯·菲什伯恩", "type": PersonType.Actor},
        ]
        persons = []
        for data in persons_data:
            person = MediaItem(Type=MediaType.Person, Name=data["name"])
            db.add(person)
            persons.append({"person": person, "type": data["type"]})
        await db.flush()
        print(f"创建 {len(persons)} 个人物")

        all_content = movies + series_items
        item_links_count = 0
        for idx, item in enumerate(all_content):
            for genre in genres[idx:idx+2]:
                link = ItemLinks(
                    ItemId=item.Id,
                    LinkedItemId=genre.Id,
                    Type=ItemLinkType.Genre,
                )
                db.add(link)
                item_links_count += 1

            studio = studios[idx % len(studios)]
            link = ItemLinks(
                ItemId=item.Id,
                LinkedItemId=studio.Id,
                Type=ItemLinkType.Studio,
            )
            db.add(link)
            item_links_count += 1

            director = next(p for p in persons if p["type"] == PersonType.Director)
            link = ItemLinks(
                ItemId=item.Id,
                LinkedItemId=director["person"].Id,
                Type=ItemLinkType.Person,
                PeopleType=PersonType.Director,
                PeopleRole="导演",
            )
            db.add(link)
            item_links_count += 1

            actor_idx = 0
            for person_info in persons:
                if person_info["type"] == PersonType.Actor and actor_idx < 3:
                    link = ItemLinks(
                        ItemId=item.Id,
                        LinkedItemId=person_info["person"].Id,
                        Type=ItemLinkType.Person,
                        PeopleType=PersonType.Actor,
                        PeopleRole=f"演员{actor_idx+1}",
                    )
                    db.add(link)
                    item_links_count += 1
                    actor_idx += 1

        await db.flush()
        print(f"创建 {item_links_count} 个标签/工作室/人物关联")

        files = []
        ep_file_paths = [
            f"/media/tvshows/{ep.Name}.mkv" for ep in episodes
        ]
        for idx, (episode, file_path) in enumerate(zip(episodes, ep_file_paths)):
            file = File(
                Path=file_path,
                Name=episode.Name + ".mkv",
                Type=FileType.Video,
                Size=1500000000 + idx * 100000000,
                Etag=f"etag-{episode.Id}",
                FFmpeg={
                    "duration": 2700,
                    "format": "mkv",
                    "video_codec": "h264",
                    "audio_codec": "aac",
                }
            )
            db.add(file)
            files.append(file)
        await db.flush()
        print(f"创建 {len(files)} 个视频文件")

        for episode, file in zip(episodes, files):
            file_link = FileLink(ItemId=episode.Id, FileId=file.Id)
            db.add(file_link)
        await db.flush()
        print(f"创建 {len(files)} 个文件关联")

        images = []
        for item in all_content:
            for img_type in [ImageType.Primary, ImageType.Thumb]:
                idx = all_content.index(item)
                image = File(
                    Path=f"/images/{item.Name}_{img_type.value}.jpg",
                    Name=f"{item.Name}_{img_type.value}",
                    Type=FileType.Image,
                    Size=500000 + idx * 10000,
                )
                db.add(image)
                images.append({"file": image, "item": item, "img_type": img_type})
        await db.flush()
        print(f"创建 {len(images)} 个图片文件")

        for img_info in images:
            file_link = FileLink(
                ItemId=img_info["item"].Id,
                FileId=img_info["file"].Id,
                ImageType=img_info["img_type"],
            )
            db.add(file_link)
        await db.flush()
        print(f"创建 {len(images)} 个图片关联")

        await db.commit()
        print("✅ 测试数据创建完成！")


if __name__ == "__main__":
    asyncio.run(create_seed_data())