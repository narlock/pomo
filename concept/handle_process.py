import multiprocessing
import time
import signal
import sys

child_processes = []  # List to track all child processes

def background_task():
    """A long-running task that runs in a separate process."""
    while True:
        print("Running in background...")
        time.sleep(2)

def background_task_other():
    """A long-running task that runs in a separate process."""
    while True:
        print("My other background process...")
        time.sleep(2)

def signal_handler(sig, frame):
    """Handles the SIGINT (CTRL + C) signal to ensure all child processes are terminated."""
    if multiprocessing.current_process().name == "MainProcess":  # Ensure only the main process handles SIGINT
        print("\nCTRL + C detected! Stopping all background processes...")

        # Terminate all child processes
        for process in child_processes:
            if process.is_alive():
                print(f"terminating process")
                process.terminate()
                process.join()

        print("All background processes stopped. Exiting program.")
        sys.exit(0)

def main():
    # Register the signal handler for CTRL + C (only for the main process)
    signal.signal(signal.SIGINT, signal_handler)

    while True:
        x = 0

        # Create a new background process
        process = multiprocessing.Process(target=background_task)
        process.daemon = True  # Ensure the process is killed when the main process exits
        process.start()

        # Track the child process
        child_processes.append(process)

        # Create a new background process
        other_process = multiprocessing.Process(target=background_task_other)
        other_process.daemon = True  # Ensure the process is killed when the main process exits
        other_process.start()

        # Track the child process
        child_processes.append(other_process)

        print(x)

        # Wait for user input to terminate the process
        input("Press Enter to stop the background task...\n")
        x = x + 1

        # Terminate the latest process only
        if process.is_alive():
            process.terminate()
            process.join()

        if other_process.is_alive():
            other_process.terminate()
            other_process.join()

        # Remove the process from the tracking list
        child_processes.remove(process)
        child_processes.remove(other_process)

        print("Background task stopped.")

if __name__ == "__main__":
    main()
