import os
import glob
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

modes_to_delete = []

def get_mode_option():
    """
    Displays a deletion options menu and prompts the user to choose an option.

    Returns:
        str: The chosen mode option.
    """
    print("Select an option(1-6):")
    print("WARNING!! THIS WILL PERMANENTLY DELETE THE FILES")
    print("1. Delete files of all modes except Osu!Standard.")
    print("2. Delete only Standard mode files.")
    print("3. Delete only Taiko mode files.")
    print("4. Delete only Catch mode files.")
    print("5. Delete only Mania mode files.")
    print("6. Exit - Exit the program.")

    while True:
        option = input("Enter your choice (1-6): ")

        if option in ["1", "2", "3", "4", "5", "6"]:
            return option
        print("Invalid option. Please try again.")

def delete_file(file_path):
    """
    Deletes the file if it contains any of the modes specified in `modes_to_delete`.

    Args:
        file_path (str): The path of the file to be checked and deleted.

    Returns:
        int: 1 if the file was deleted, 0 otherwise.
    """
    global modes_to_delete
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            content = file.read()
            if any(mode in content for mode in modes_to_delete):
                # Close the file before deletion
                file.close()
                os.remove(file_path)
                
                # Check if the folder is empty
                folder_path = os.path.dirname(file_path)
                if not any(file.endswith('.osu') for file in os.listdir(folder_path)):
                    os.rmdir(folder_path)
                
                return 1
    except UnicodeDecodeError:
        pass
    return 0

def process_files(file_chunk, thread_progress):
    """
    Processes a chunk of files, calling `delete_file` on each file in the chunk.

    Args:
        file_chunk (list): A list of file paths to be processed.
        thread_progress (tqdm): Progress bar associated with the current thread.

    Returns:
        int: The number of files deleted in the chunk.
    """
    deleted_count = 0
    for file_path in file_chunk:
        deleted_count += delete_file(file_path)
        thread_progress.update(1)
    return deleted_count

def calculate_elapsed_time(start_time):
    """
    Calculates the elapsed time since `start_time` in minutes and seconds format.

    Args:
        start_time (float): The starting time in seconds.

    Returns:
        str: The elapsed time in minutes and seconds format.
    """
    elapsed_time = time.time() - start_time
    minutes = int(elapsed_time // 60)
    seconds = int(elapsed_time % 60)
    return f"{minutes} m, {seconds} s"


def choose_file_type():
        """
    Displays a deletion options menu and prompts the user to choose an option.

    Returns:
        str: The chosen type option.
    """
    while True:
        print("Please select a file type:")
        print("1. Beatmaps (If you pick this option you will be asked which beatmap modes you want to delete)")
        print("2. Video files (mp4, avi, flv) (WARNING!! THIS WILL IMMEDIATLY DELETE THE FILES PERMANENTLY)")
        print("3. Exit - Exit the program.")
        choice = input("Enter your choice (1-3): ")
        
        if choice == '1':
            return "*.osu"
        elif choice == '2':
            return "*.mp4|*.avi|*.flv"
        elif choice == "3":
            print("Exiting...")
            quit()

        print("Invalid choice. Please try again.")


def main():
    """
    The main function of the script. It controls the flow of execution and user interaction.

    This function prompts the user for the path to the "osu!\\Songs" folder, presents the deletion options menu,
    performs file reading and processing, and displays relevant information about the execution.

    This function utilizes multithreading to improve performance during file processing.

    Note: The global variable `modes_to_delete` is used to store the selected modes for deletion.

    Returns:
        None
    """ 
    global modes_to_delete
    # Prompt user for folder path
    folder_path = input("Enter the full path to the 'osu!\\Songs' folder:")
    


    while True:
        file_type = choose_file_type()

        if file_type == "*.osu":
            option = get_mode_option()
            if option == "1":
                modes_to_delete = ["Mode: 2", "Mode: 3", "Mode: 4"]
            elif option == "2":
                modes_to_delete = ["Mode: 1"]
            elif option == "3":
                modes_to_delete = ["Mode: 2"]
            elif option == "4":
                modes_to_delete = ["Mode: 3"]
            elif option == "5":
                modes_to_delete = ["Mode: 4"]
            elif option == "6":
                print("Exiting...")
                quit()
            
        # File reading
        print("File reading in progress...")
        start_time_reading = time.time()
        file_pattern = os.path.join(folder_path, '**', file_type)
        files = glob.glob(file_pattern, recursive=True)
        num_threads = max(os.cpu_count() - 4, 1)  # Ensure at least 1 thread is used

        end_time_reading = time.time()

        start_time_processing = time.time()

        print("File processing in progress...(this might take a while)")
        # File processing
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            thread_progresses = [tqdm(total=0, ncols=80, unit='file', desc=f'Thread {i + 1}') for i in range(num_threads)]

            chunk_size = len(files) // num_threads
            file_chunks = [files[i:i + chunk_size] for i in range(0, len(files) - chunk_size + 1, chunk_size)]
            if len(files) % num_threads != 0:
                file_chunks[-1].extend(files[-(len(files) % num_threads):])

            futures = []
            for i, file_chunk in enumerate(file_chunks, start=1):
                thread_progress = thread_progresses[i - 1]
                thread_progress.total = len(file_chunk)
                future = executor.submit(process_files, file_chunk, thread_progress)
                futures.append(future)

            # Wait for all futures to complete
            total_deleted = 0
            for future in as_completed(futures):
                total_deleted += future.result()

            for thread_progress in thread_progresses:
                thread_progress.close()

        end_time_processing = time.time()

        print(modes_to_delete)

        print("File reading elapsed time:", calculate_elapsed_time(start_time_reading))
        print("File processing elapsed time:", calculate_elapsed_time(start_time_processing))

        print(f"Total files read: {len(files)}")
        print(f"Total files deleted: {total_deleted}")

if __name__ == '__main__':
    main()
