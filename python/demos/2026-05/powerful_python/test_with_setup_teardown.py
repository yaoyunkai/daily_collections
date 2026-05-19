"""
test_with_setup_teardown.py


created at 2026-05-19
"""

import os
import tempfile
import unittest


class NoteManager:
    def __init__(self, filepath: str):
        self.filepath = filepath

    def add_note(self, note: str) -> None:
        with open(self.filepath, "a", encoding="utf-8") as f:
            f.write(note + "\n")

    def get_notes(self) -> list[str]:
        if not os.path.exists(self.filepath):
            return []
        with open(self.filepath, "r", encoding="utf-8") as f:
            return [line.strip() for line in f.readlines()]


class TestNoteManager(unittest.TestCase):
    def setUp(self):
        self.temp_file = tempfile.NamedTemporaryFile(delete=False)
        self.test_filepath = self.temp_file.name

        self.temp_file.close()

        self.manager = NoteManager(self.test_filepath)
        print(f"\n[setUp] 初始化 NoteManager，使用系统临时文件: {self.test_filepath}")

    def tearDown(self):
        if os.path.exists(self.test_filepath):
            os.remove(self.test_filepath)
            print(f"[tearDown] 删除了临时文件: {self.test_filepath}")

    def test_add_and_get_notes(self):
        print("--> 正在执行: test_add_and_get_notes")
        self.manager.add_note("第一条笔记")
        self.manager.add_note("第二条笔记")

        notes = self.manager.get_notes()
        self.assertEqual(notes, ["第一条笔记", "第二条笔记"])

    def test_empty_notes(self):
        print("--> 正在执行: test_empty_notes")
        notes = self.manager.get_notes()
        self.assertEqual(notes, [])


if __name__ == "__main__":
    unittest.main()
