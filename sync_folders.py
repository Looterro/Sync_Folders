import os
import time
import shutil

#calulate the message digest of a file
def calculate_md5(file_path):
    pass

#main function to sync the source folder with the replica folder
def sync_folders(source_path, replica_path, log_path):
    
    #create the replica folder if it doesn't exist
    if not os.path.exists(replica_path):
        os.makedirs(replica_path)

    #initialize the log file with the current time of synchronization after a change
    with open(log_path, "a") as log_file:
        log_file.write("Sync started at: {}\n".format(time.ctime()))

        #for each file in the source folder
        #check if it exists in the replica folder
        for root, dirs, files in os.walk(source_path):

            for filename in files:

                #get the path of the file in the source folder and the replica
                source_file_path = os.path.join(root, filename)
                replica_file_path = os.path.join(replica_path, os.path.relpath(surce_file_path, source_path))
                
                #calculate the md5 of the file in the source folder and the replica if it exists
                source_md5 = calculate_md5(source_file_path)
                replica_md5 = calculate_md5(replica_file_path) if os.path.exists(replica_file_path) else None

                #if the file doesn't exist in the replica folder, copy it
                if source_md5 != replica_md5:
                    shutil.copy2(source_file_path, replica_file_path)
                    log_file.write("Copied: {}\n".format(replica_file_path))

            #write a message at the end of the synchronization
            log_file.write("Sync completed at: {}\n".format(time.ctime()))