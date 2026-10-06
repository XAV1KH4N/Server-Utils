from unittest import TestCase, main

from Server.filehandler.FileHandler import FileHandler
from movielist.server.MovieCacheManager import MovieCacheManager
from movielist.common.Movie import Movie, MovieEntry, MovieEntryData

class FileHandlerSpec(TestCase):

    def test_entries_empty(self):
        manager = MovieCacheManager(override_name="test")
        self.assertEqual(manager.get_entries_count(), 0)

    def test_add_entry(self):
        movie = Movie("test")
        entry = MovieEntry(MovieEntryData(movie, "abc"))
        manager = MovieCacheManager(override_name="test")
        manager.add_entry(entry)
        self.assertEqual(manager.get_entries_count(), 1)
        test_file_handler = FileHandler("test")
        test_file_handler.remove_file()

    def test_add_entry_and_check(self):
        movie = Movie("test")
        entry = MovieEntry(MovieEntryData(movie, "abc"))
        manager = MovieCacheManager(override_name="test")
        manager.add_entry(entry)
        self.assertEqual(manager.get_entries(), [entry])
        test_file_handler = FileHandler("test")
        test_file_handler.remove_file()

    def test_add_entry_and_check_moveis(self):
        movie = Movie("test")
        entry = MovieEntry(MovieEntryData(movie, "abc"))
        manager = MovieCacheManager(override_name="test")
        manager.add_entry(entry)
        self.assertEqual(manager.get_movies(), [movie])
        test_file_handler = FileHandler("test")
        test_file_handler.remove_file()


    def test_init_filehandler(self):
        test_file_handler = FileHandler("test")
        test_file_handler.remove_file()

        self.assertFalse(test_file_handler.file_exists())
        manager = MovieCacheManager(override_name="test")
        self.assertTrue(test_file_handler.file_exists())
        test_file_handler.remove_file()

    def test_add_to_file(self):
        test_file_handler = FileHandler("test")
        test_file_handler.remove_file()

        manager = MovieCacheManager(override_name="test")
        movie = Movie("test")
        entry = MovieEntry(MovieEntryData(movie, "abc"))

        manager.add_entry(entry)

        text = test_file_handler.read_raw()
        self.assertTrue(text, '''[{"movie": "{\"movie_name\": \"test\"}", "username": "abc"}]''')

        test_file_handler.remove_file()

    def test_init_cache_from(self):
        manager = MovieCacheManager(override_name="test")
        movie = Movie("test")
        entry = MovieEntry(MovieEntryData(movie, "abc"))

        manager.add_entry(entry)

        manager_2 = MovieCacheManager(override_name="test")
        entries = manager_2.get_entries()
        self.assertEqual(entries, [entry])

        test_file_handler = FileHandler("test")
        test_file_handler.remove_file()        

    def test_init_cache_from_multi(self):
        manager = MovieCacheManager(override_name="test")
        entry_1 = MovieEntry(MovieEntryData(Movie("Film A"), "Xavi"))
        entry_2 = MovieEntry(MovieEntryData(Movie("Film B"), "Xavi"))
        entry_3 = MovieEntry(MovieEntryData(Movie("Film C"), "Mims"))

        manager.add_entry(entry_1)
        manager.add_entry(entry_2)
        manager.add_entry(entry_3)

        manager_2 = MovieCacheManager(override_name="test")
        entries = manager_2.get_entries()
        self.assertEqual(entries, [entry_1, entry_2, entry_3])

        test_file_handler = FileHandler("test")
        test_file_handler.remove_file()        

    def test_delete_failed(self):
        manager = MovieCacheManager(override_name="test")
        entry_1 = MovieEntry(MovieEntryData(Movie("Film A"), "Xavi"))
        entry_2 = MovieEntry(MovieEntryData(Movie("Film B"), "Xavi"))

        manager.add_entry(entry_2)

        entries = manager.get_entries()
        self.assertEqual(entries, [entry_2])

        is_deleted = manager.remove_entry(entry_1)
        self.assertFalse(is_deleted)

        test_file_handler = FileHandler("test")
        test_file_handler.remove_file()     

    def test_delete_pass(self):
        manager = MovieCacheManager(override_name="test")
        entry_1 = MovieEntry(MovieEntryData(Movie("Film A"), "Xavi"))
        entry_2 = MovieEntry(MovieEntryData(Movie("Film B"), "Xavi"))

        manager.add_entry(entry_1)
        manager.add_entry(entry_2)

        entries = manager.get_entries()
        self.assertEqual(entries, [entry_1, entry_2])

        is_deleted = manager.remove_entry(entry_2)
        self.assertTrue(is_deleted)

        entries = manager.get_entries()
        self.assertEqual(entries, [entry_1])

        test_file_handler = FileHandler("test")
        test_file_handler.remove_file()    


if __name__ == '__main__':
    main()