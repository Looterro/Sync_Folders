import unittest
import shutil
import os
import tempfile
import time

from sync_folders import sync_folders 


class TestFolderSynchronization(unittest.TestCase):

    def setUp(self):

        #create temporary directories and files for testing
        self.source_dir = tempfile.mkdtemp()
        self.replica_dir = tempfile.mkdtemp()
        self.log_file = tempfile.mktemp()

    def tearDown(self):

        #remove the directories and files created during the test
        shutil.rmtree(self.source_dir)
        shutil.rmtree(self.replica_dir)
        os.remove(self.log_file)

    def test_synchronization(self):

        #create sample files in the source folder
        file1_path = os.path.join(self.source_dir, "file1.txt")
        with open(file1_path, "w") as f:
            f.write("Hello World!")

        #run synchronization
        sync_folders(self.source_dir, self.replica_dir, self.log_file)

        #check if the file was copied to the replica folder
        replica_file1_path = os.path.join(self.replica_dir, "file1.txt")
        self.assertTrue(os.path.exists(replica_file1_path))

        #modify the source file
        with open(file1_path, "w") as f:
            f.write("Modified Hello World!")

        #run synchronization again
        sync_folders(self.source_dir, self.replica_dir, self.log_file)

        #check if the modified file was copied to the replica folder
        with open(replica_file1_path, "r") as f:
            content = f.read()
            self.assertEqual(content, "Modified Hello World!")

        #remove the source file
        os.remove(file1_path)

        #run synchronization again
        sync_folders(self.source_dir, self.replica_dir, self.log_file)

        #check if the file was removed from the replica folder
        self.assertFalse(os.path.exists(replica_file1_path))

#run the script
if __name__ == "__main__":
    unittest.main()