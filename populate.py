import os
import random

TARGET_COUNT = 10000
DIRECTORY_NAME_BASE = "dir"
FILE_NAME_BASE = "file"
FILE_EXTENSION = ".txt"
BASE_PATH = "test_data"
SEED = 42  # A fixed seed for deterministic behavior


def create_file(path, num):
    file_name = f"{FILE_NAME_BASE}{num}{FILE_EXTENSION}"
    with open(os.path.join(path, file_name), "w") as file:
        file.write("test content")


def create_folder(path, num):
    folder_name = f"{DIRECTORY_NAME_BASE}{num}"
    full_path = os.path.join(path, folder_name)
    os.makedirs(full_path)
    return full_path


def populate_directory(base_path, remaining_count, current_num):
    created_count = 0
    while created_count < remaining_count:
        is_file = random.choices([True, False], weights=[0.55, 0.45])[0]

        if is_file:
            create_file(base_path, current_num)
            created_count += 1
            current_num += 1
        else:
            subfolder_path = create_folder(base_path, current_num)
            current_num += 1
            subfolder_items = min(remaining_count - created_count, random.randint(1, 100))
            sub_created, current_num = populate_directory(subfolder_path, subfolder_items, current_num)
            created_count += sub_created

    return (created_count, current_num)


if __name__ == "__main__":
    random.seed(SEED)
    os.makedirs(BASE_PATH, exist_ok=True)
    populate_directory(BASE_PATH, TARGET_COUNT, 1)
