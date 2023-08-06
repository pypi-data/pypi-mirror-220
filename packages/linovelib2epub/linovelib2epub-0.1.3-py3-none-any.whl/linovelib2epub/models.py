from dataclasses import dataclass, field
from typing import Any, Dict, List, Union, Set


@dataclass
class LightNovelChapter:
    cid: Union[int, str]
    title: str = ''
    content: str = ''


@dataclass
class LightNovelVolume:
    vid: Union[int, str]
    title: str = ''
    chapters: list = field(default_factory=list)

    # The set "volume_img_folders" is used to extract images in specific volume when "divide_volume=True"
    volume_img_folders: set = field(default_factory=set)
    # volume_cover is used as the cover image in specific volume when "divide_volume=True"
    volume_cover: str = ''

    # example: https://img.linovelib.com/0/682/117077/50675.jpg
    # volume_img_folder = {"117077","117900"} or {"117097"}
    # volume_cover = "117077/50677.jpg"

    def add_chapter(self, cid: Union[int, str], title: str = '', content: str = ''):
        new_chapter = {
            'cid': cid,
            'title': title,
            'content': content
        }
        self.chapters.append(new_chapter)

    def get_chapter_by_cid(self, cid):
        for chapter in self.chapters:
            if chapter.cid == cid:
                return chapter
        return None

    def get_chapters_size(self):
        return len(self.get_chapters())

    def get_chapters(self):
        return self.chapters


@dataclass
class LightNovel:
    bid: Union[int, str] = None
    book_title: str = ''
    author: str = ''
    description: str = ''
    book_cover: str = ''
    book_cover_local: str = ''

    volumes: list[dict[str, Any]] = field(default_factory=list)

    # map<volume_name, List[img_url]>
    illustration_dict: dict[Union[int, str], list[str]] = field(default_factory=dict)

    def __post_init__(self):
        # data state flags
        self.basic_info_ready = False
        self.volumes_content_ready = False

    def get_volumes_size(self):
        return len(self.volumes)

    def get_chapters_size(self):
        count = 0
        for volume in self.volumes:
            if volume['chapters']:
                count += len(volume['chapters'])
        return count

    def get_illustration_set(self):
        image_set = set()
        for values in self.illustration_dict.values():
            for value in values:
                image_set.add(value)
        return image_set

    def add_volume(self, vid: Union[int, str], title: str = '', chapters: List = None, volume_img_folders: Set = None,
                   volume_cover: str = ''):
        new_volume = {
            'vid': vid,
            'title': title,
            'chapters': chapters if chapters else [],
            'volume_img_folders': volume_img_folders if volume_img_folders else set(),
            'volume_cover': volume_cover,
        }
        self.volumes.append(new_volume)

    def get_volume_by_vid(self, vid):
        for volume in self.volumes:
            if volume.vid == vid:
                return volume
        return None

    def set_illustration_dict(self, illustration_dict: Dict[Union[int, str], List[str]] = {}):
        self.illustration_dict = illustration_dict

    def mark_basic_info_ready(self):
        self.basic_info_ready = True

    def mark_volumes_content_ready(self):
        self.volumes_content_ready = True
