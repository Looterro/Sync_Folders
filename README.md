# Synchronize Folders Project

A program that synchronizes two folders. The program maintains a full, identical copy of source folder at replica folder.

### Setup

In project directory run:

`python3 sync_folders.py source_folder(folder path) replica_folder(folder path) sync_interval(number) log_file(file path)`

For tests check for pytest package and run:

`pytest test_sync_folders.py`

### Functionality

• The speed of synchronizing the shadow folder can be manually adjusted

• Once run, the program adds new files in source folder to the shadow one and removes them if deleted

• Updated files will be compared and changed

• All changes are logged with the time of synchronizations

### Technologies used:

• Python3 with the built-in shutil library to perform the synchronization and hashlib library to calculate MD5 hashes

• Pytest for tests
