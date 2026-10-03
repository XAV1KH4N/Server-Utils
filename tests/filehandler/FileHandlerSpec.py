from unittest import TestCase, main

from Server.filehandler.FileHandler import FileHandler

class FileHandlerSpec(TestCase):

    def test_root_path(self):
        handler = FileHandler("test")
        self.assertEqual(handler.get_root_path(), "/home/xavi/Projects/Server-Utils/Server/filehandler")
        handler.remove_file()

    def test_full_path(self):
        handler = FileHandler("test")
        self.assertEqual(handler.full_file_path(), "/home/xavi/Projects/Server-Utils/Server/filehandler/test.txt")
        handler.remove_file()

    def test_file_exists(self):
        handler = FileHandler("test")
        self.assertTrue(handler.file_exists())
        handler.remove_file()
        self.assertFalse(handler.file_exists())

    def test_file_read_raw(self):
        handler = FileHandler("test")
        text = handler.read_raw()
        self.assertEqual(text, "")
        handler.remove_file()

    def test_file_read(self):
        handler = FileHandler("test")
        text = handler.read()
        self.assertEqual(text, list[str]())
        handler.remove_file()

    def test_file_write_single(self):
        handler = FileHandler("test")
        to_write = "hello"
        handler.write(to_write)
        text = handler.read_raw()
        self.assertEqual(text, "hello\n")
        handler.remove_file()

    def test_file_write_multi(self):
        handler = FileHandler("test")
        to_write = "hello\nTesting"
        handler.write(to_write)
        text = handler.read()
        self.assertEqual(text, ["hello", "Testing"])
        handler.remove_file()

    def test_file_append_single(self):
        handler = FileHandler("test")
        to_write = "hello"
        handler.write(to_write)
        text = handler.read()
        self.assertEqual(text, ["hello"])
        to_append = "testing"
        handler.append(to_append)
        text = handler.read()
        self.assertEqual(text, [to_write, to_append])
        handler.remove_file()

if __name__ == '__main__':
    main()