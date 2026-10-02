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


if __name__ == '__main__':
    main()