from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

# 示例配置：关键词与关联站点
DEMO_KEYWORD = "爱游戏"
DEMO_URL = "https://homesite-i-game.com.cn"


@dataclass
class KeywordNote:
    """单个关键词笔记的数据容器"""
    keyword: str
    url: Optional[str] = None
    note: str = ""
    tags: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)

    def formatted_entry(self) -> str:
        """返回格式化的单条笔记字符串"""
        parts = [
            f"关键词: {self.keyword}",
            f"时间: {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}",
        ]
        if self.url:
            parts.append(f"关联URL: {self.url}")
        if self.note:
            parts.append(f"备注: {self.note}")
        if self.tags:
            tags_str = ", ".join(self.tags)
            parts.append(f"标签: {tags_str}")
        return " | ".join(parts)

    def short_summary(self) -> str:
        """返回简短的单行摘要"""
        tag_hint = f" [{', '.join(self.tags)}]" if self.tags else ""
        return f"{self.keyword}{tag_hint}: {self.note[:40] if self.note else '无备注'}"


@dataclass
class KeywordNoteBook:
    """关键词笔记本，管理多条 KeywordNote 并支持格式化输出"""
    notes: List[KeywordNote] = field(default_factory=list)

    def add_note(self, note: KeywordNote) -> None:
        self.notes.append(note)

    def load_example_data(self) -> None:
        """加载示例笔记数据，包含演示用途的 URL 与关键词"""
        self.notes = [
            KeywordNote(
                keyword=DEMO_KEYWORD,
                url=DEMO_URL,
                note="一个提供游戏相关内容的站点",
                tags=["游戏", "示例"],
            ),
            KeywordNote(
                keyword=DEMO_KEYWORD,
                url=DEMO_URL,
                note="用户活跃度较高",
                tags=["游戏", "分析"],
            ),
            KeywordNote(
                keyword="Python笔记",
                note="使用dataclass组织数据",
                tags=["编程", "学习"],
            ),
        ]

    def format_all(self, use_style: str = "long") -> str:
        """根据指定格式返回所有笔记的文本"""
        if use_style == "long":
            lines = [note.formatted_entry() for note in self.notes]
        elif use_style == "short":
            lines = [note.short_summary() for note in self.notes]
        else:
            lines = [f"[{i+1}] {note.short_summary()}" for i, note in enumerate(self.notes)]
        return "\n".join(lines)

    def filter_by_keyword(self, keyword: str) -> "KeywordNoteBook":
        """按关键词筛选笔记，返回新的笔记本"""
        matched = [note for note in self.notes if note.keyword == keyword]
        return KeywordNoteBook(notes=matched)

    def filter_by_tag(self, tag: str) -> "KeywordNoteBook":
        """按标签筛选笔记，返回新的笔记本"""
        matched = [note for note in self.notes if tag in note.tags]
        return KeywordNoteBook(notes=matched)

    def stats(self) -> str:
        """返回笔记本的统计信息"""
        total = len(self.notes)
        if total == 0:
            return "笔记本为空"
        keywords = {note.keyword for note in self.notes}
        tags = {tag for note in self.notes for tag in note.tags}
        return f"共 {total} 条笔记，涉及 {len(keywords)} 个关键词，{len(tags)} 个标签"


def demo_run() -> None:
    """演示笔记本的创建与格式化输出"""
    book = KeywordNoteBook()
    book.load_example_data()

    print("【完整格式输出】")
    print(book.format_all(use_style="long"))
    print()

    print("【简短格式输出】")
    print(book.format_all(use_style="short"))
    print()

    print("【统计信息】")
    print(book.stats())
    print()

    # 筛选演示
    filtered = book.filter_by_keyword(DEMO_KEYWORD)
    print(f"筛选关键词「{DEMO_KEYWORD}」后的笔记：")
    print(filtered.format_all(use_style="short"))


if __name__ == "__main__":
    demo_run()