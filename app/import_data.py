from os import environ
from swiftclient import Connection
from swiftclient.multithreading import MultiThreadingManager
from queue import Queue
from swiftclient.exceptions import ClientException
from concurrent.futures import as_completed
import os
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

OBJECT_STORAGE_URL = os.environ["OBJECT_STORAGE_URL"]
PATH = os.environ["DATA_SOURCE_PATH"]

def get_from_queue(q, timeout=864000):
    while True:
        try:
            item = q.get(timeout=timeout)
            return item
        except QueueEmpty:
            # Do nothing here, we only have a timeout to allow interruption
            pass
        
def download_file(conn, obj, path):
    resp_headers, obj_contents = conn.get_object('BUDGET', obj)
    if obj.split("/")[0] in list_dir:
        os.chdir(PATH+obj.split("/")[0])
        with open(obj.split("/")[2], 'wb') as local:
            local.write(obj_contents)
    else:
        os.mkdir(PATH+obj.split("/")[0])
        list_dir.append(obj.split("/")[0])
        os.chdir(PATH+obj.split("/")[0])
        with open(obj.split("/")[2], 'wb') as local:
            local.write(obj_contents)
            
def download_file_in_same_folder(conn, obj, path):
    os.chdir(PATH)
    resp_headers, obj_contents = conn.get_object('BUDGET', obj)
    with open(obj.split("/")[1]+"."+obj.split(".")[1]+"."+obj.split(".")[2], 'wb') as local:
        local.write(obj_contents)
   
def fn(conn):
    pass
    #return print(conn.get_object('BUDGET', selected[0]))

def interruptable_as_completed(fs, timeout=86400):
    while True:
        try:
            for f in as_completed(fs, timeout=timeout):
                fs.remove(f)
                yield f
            return
        except TimeoutError:
            # Do nothing here, we only have a timeout to allow interruption
            pass
        
def create_connection():
    return Connection(os_options={
    "object_storage_url" : OBJECT_STORAGE_URL},
    preauthtoken = "fd1e4e59405d424db77e677913bb0a57",
                           insecure=True)


def download_queue():
    thread_manager = MultiThreadingManager(
                create_connection,
                segment_threads=20,
                object_dd_threads=20,
                object_uu_threads=20,
                container_threads=20
            )
    conn=create_connection()
    o_downs = [thread_manager.object_dd_pool.submit(
                        #fn
                        download_file_in_same_folder, obj, path
                    ) for obj in selected]

    for o_down in interruptable_as_completed(o_downs):
        yield o_down.result()

def main():
    while True:
        next(download_queue())

if  __name__ == "__main__":
    conn = create_connection()
    resp_headers, containers = conn.get_account()
    info, objects = conn.get_container('BUDGET', full_listing=True)
    selected = [i["name"] for i in objects]
    main()