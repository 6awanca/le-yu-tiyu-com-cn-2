from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

@dataclass
class KeywordNote:
    keyword: str
    source_url: str
    note: str = ""
    tags: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None

    def update_note(self, new_note: str) -> None:
        self.note = new_note
        self.updated_at = datetime.now()

    def add_tag(self, tag: str) -> None:
        if tag not in self.tags:
            self.tags.append(tag)
            self.updated_at = datetime.now()

    def remove_tag(self, tag: str) -> None:
        if tag in self.tags:
            self.tags.remove(tag)
            self.updated_at = datetime.now()

    def to_dict(self) -> dict:
        return {
            "keyword": self.keyword,
            "source_url": self.source_url,
            "note": self.note,
            "tags": self.tags,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


@dataclass
class NoteCollection:
    notes: List[KeywordNote] = field(default_factory=list)

    def add_note(self, note: KeywordNote) -> None:
        self.notes.append(note)

    def find_by_keyword(self, keyword: str) -> Optional[KeywordNote]:
        for note in self.notes:
            if note.keyword == keyword:
                return note
        return None

    def find_by_tag(self, tag: str) -> List[KeywordNote]:
        return [note for note in self.notes if tag in note.tags]


def format_note_simple(note: KeywordNote) -> str:
    lines = [
        f"关键词：{note.keyword}",
        f"来源：{note.source_url}",
        f"笔记：{note.note}" if note.note else "笔记：（无）",
        f"标签：{'、'.join(note.tags) if note.tags else '（无）'}",
        f"创建时间：{note.created_at.strftime('%Y-%m-%d %H:%M')}",
    ]
    if note.updated_at:
        lines.append(f"更新时间：{note.updated_at.strftime('%Y-%m-%d %H:%M')}")
    return "\n".join(lines)


def format_note_detailed(note: KeywordNote) -> str:
    separator = "-" * 40
    lines = [
        separator,
        f"【关键词笔记】",
        f"  关键词：{note.keyword}",
        f"  来源 URL：{note.source_url}",
        f"  笔记内容：{note.note if note.note else '（未填写）'}",
        f"  所属标签：{', '.join(note.tags) if note.tags else '（未分类）'}",
        f"  创建时间：{note.created_at.strftime('%Y-%m-%d %H:%M:%S')}",
    ]
    if note.updated_at:
        lines.append(f"  更新时间：{note.updated_at.strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(separator)
    return "\n".join(lines)


def format_collection_summary(collection: NoteCollection) -> str:
    count = len(collection.notes)
    tag_count = {}
    for note in collection.notes:
        for tag in note.tags:
            tag_count[tag] = tag_count.get(tag, 0) + 1
    lines = [
        f"笔记总数：{count}",
        "标签统计：",
    ]
    if tag_count:
        for tag, cnt in sorted(tag_count.items(), key=lambda x: -x[1]):
            lines.append(f"  - {tag}: {cnt} 条")
    else:
        lines.append("  （无标签）")
    return "\n".join(lines)


if __name__ == "__main__":
    note1 = KeywordNote(
        keyword="乐鱼体育",
        source_url="https://le-yu-tiyu.com.cn",
        note="这是一个体育相关的关键词笔记，用于记录平台信息与功能说明。",
        tags=["体育", "平台", "乐鱼"],
    )
    note2 = KeywordNote(
        keyword="乐鱼体育会员",
        source_url="https://le-yu-tiyu.com.cn/membership",
        note="会员权益包括专属赛事直播与数据分析。",
        tags=["会员", "体育", "直播"],
    )
    note3 = KeywordNote(
        keyword="乐鱼体育赛事",
        source_url="https://le-yu-tiyu.com.cn/events",
        note="涵盖足球、篮球、网球等热门赛事信息。",
        tags=["赛事", "足球", "篮球"],
    )

    collection = NoteCollection()
    collection.add_note(note1)
    collection.add_note(note2)
    collection.add_note(note3)

    print(format_note_simple(note1))
    print()
    print(format_note_detailed(note2))
    print()
    print(format_collection_summary(collection))