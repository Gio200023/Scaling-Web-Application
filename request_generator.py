import requests
import threading
import time

BASE_URL = "http://localhost:80"

def get_objects():
    """GET request to fetch a list of all objects."""
    response = requests.get(f"{BASE_URL}/")
    if response.ok:
        print("GET /:", response.json())
    else:
        print("Failed to fetch objects:", response.status_code)

def create_or_update_object(obj_id, content):
    """PUT request to create or update an object using form-encoded data."""
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = {'content': content}
    response = requests.put(f"{BASE_URL}/objs/{obj_id}", data=data, headers=headers)
    if response.ok:
        print(f"PUT /objs/{obj_id}:", response.json())
    else:
        print(f"Failed to create/update object {obj_id}:", response.status_code, response.text)

def get_object(obj_id):
    """GET request to fetch a specific object."""
    response = requests.get(f"{BASE_URL}/objs/{obj_id}")
    if response.ok:
        print(f"GET /objs/{obj_id}:", response.text)
    else:
        print(f"Failed to fetch object {obj_id}:", response.status_code)

def compress_object(obj_id):
    """GET request to fetch the compressed content of a specific object."""
    response = requests.get(f"{BASE_URL}/objs/{obj_id}/compress")
    if response.ok:
        print(f"GET /objs/{obj_id}/compress:", response.text)
    else:
        print(f"Failed to compress object {obj_id}:", response.status_code)

def delete_object(obj_id):
    """DELETE request to remove a specific object."""
    response = requests.delete(f"{BASE_URL}/objs/{obj_id}")
    if response.ok:
        print(f"DELETE /objs/{obj_id}: Object deleted successfully")
    else:
        print(f"Failed to delete object {obj_id}:", response.status_code)

def delete_all_objects():
    """DELETE request to remove all objects."""
    response = requests.delete(f"{BASE_URL}/")
    if response.ok:
        print("DELETE /: All objects deleted successfully")
    else:
        print("Failed to delete all objects:", response.status_code)
        
def perform_api_calls(obj_id, content):
    create_or_update_object(obj_id, content)
    get_object(obj_id)
    compress_object(obj_id)
    delete_object(obj_id)
        
def load_generator(thread_count, obj_id, content):
    """Starts multiple threads to generate load."""
    threads = []
    for _ in range(thread_count):
        thread = threading.Thread(target=create_or_update_object, args=(obj_id, content))
        thread.start()
        threads.append(thread)
    
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    while True:
        load_generator(20, "test", "Sample content for test1")
        # create_or_update_object("test1", "Sample content for test1")
        # get_object("test1")
        # compress_object("test1")
        # delete_object("test1")
        # delete_all_objects()
