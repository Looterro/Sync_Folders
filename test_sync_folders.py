import os
import shutil
import tempfile
import time

from sync_folders import sync_folders

def test_synchronization():

    #create temporary folders and files
    source_dir = tempfile.mkdtemp()
    replica_dir = tempfile.mkdtemp()
    log_file = tempfile.mktemp()

    try:

        #create some sample files in the source folder
        file1_path = os.path.join(source_dir, "file1.txt")
        with open(file1_path, "w") as f:
            f.write("Hello, World!")

        #run synchronization
        sync_folders(source_dir, replica_dir, log_file)

        #check if the file was copied to the replica folder
        replica_file1_path = os.path.join(replica_dir, "file1.txt")
        assert os.path.exists(replica_file1_path)

        #modify the source file
        with open(file1_path, "w") as f:
            f.write("Modified content")

        #run synchronization again
        sync_folders(source_dir, replica_dir, log_file)

        #check if the modified file was copied to the replica folder
        with open(replica_file1_path, "r") as f:
            content = f.read()
            assert content == "Modified content"

        #remove the source file
        os.remove(file1_path)

        #run synchronization again
        sync_folders(source_dir, replica_dir, log_file)

        #check if the file was removed from the replica folder
        assert not os.path.exists(replica_file1_path)

    finally:
        shutil.rmtree(source_dir)
        shutil.rmtree(replica_dir)
        os.remove(log_file)
