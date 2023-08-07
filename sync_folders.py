import os
import time
import shutil
import sys
import hashlib

#calulate the message digest of a file
def calculate_md5(file_path):

    #create a md5 hash object
    hash_md5 = hashlib.md5()

    #read the file in binary mode
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            #update the hash object with the chunk
            hash_md5.update(chunk)

    #return the hex digest of the file
    return hash_md5.hexdigest()

#main function to sync the source folder with the replica folder
def sync_folders(source_path, replica_path, log_path):
    
    #create the replica folder if it doesn't exist
    if not os.path.exists(replica_path):
        os.makedirs(replica_path)

    #open the log file in append mode
    with open(log_path, "a") as log_file:

        #initialize the log file with the current time of synchronization after a change
        log_file.write("Sync started at: {}\n".format(time.ctime()))

        #copy new or updated files from the source folder to the replica folder
        for root, dirs, files in os.walk(source_path):

            for filename in files:

                #get the path of the file in the source folder and the replica
                source_file_path = os.path.join(root, filename)
                replica_file_path = os.path.join(replica_path, os.path.relpath(source_file_path, source_path))
                
                #calculate the md5 of the file in the source folder and the replica if it exists
                source_md5 = calculate_md5(source_file_path)
                replica_md5 = calculate_md5(replica_file_path) if os.path.exists(replica_file_path) else None

                #if the file doesn't exist in the replica folder, copy it
                if source_md5 != replica_md5:
                    shutil.copy2(source_file_path, replica_file_path)
                    log_file.write("Copied: {}\n".format(replica_file_path))

        #remove files not present in the source folder in the replica folder
        for root, dirs, files in os.walk(replica_path):

            for filename in files:
                
                #get the paths
                replica_file_path = os.path.join(root, filename)
                source_file_path = os.path.join(source_path, os.path.relpath(replica_file_path, replica_path))

                #if the file doesn't exist in the source folder, remove it and log it
                if not os.path.exists(source_file_path):
                    os.remove(replica_file_path)
                    log_file.write("Removed: {}\n".format(replica_file_path))


        #write a message at the end of the synchronization
        log_file.write("Sync completed at: {}\n".format(time.ctime()))

if __name__ == "__main__":

    #check if the number of arguments is correct
    #if not, print the usage information and exit
    if len(sys.argv) != 5:
        print("Usage: python3 sync_folders.py source_folder(folder path) replica_folder(folder path) sync_interval(number) log_file(file path)")
        sys.exit(1)

    #get the arguments in the following order:
    #source_folder, replica_folder, sync_interval, log_file
    source_path = sys.argv[1]
    replica_path = sys.argv[2]
    sync_interval = int(sys.argv[3])
    log_path = sys.argv[4]

    #sync the folders every sync_interval seconds
    while True:
        sync_folders(source_path, replica_path, log_path)
        time.sleep(sync_interval)