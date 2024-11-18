import os
import sys
import threading
import subprocess
import tkinter as tk
from tkinter import ttk


process_is_running = False
process_thread = None
process = None


def run_process(line_callback: callable = None):
    global process_thread
    def run_process():
        global process_is_running
        global process
        process_is_running = True

        try:
            curr_env = os.environ.copy()

            command = ["python", "ui_main.py"]

            process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True, env=curr_env)

            while process_is_running:
                output = process.stdout.readline()
                if not output and process.poll() is not None:
                    break

                decoded_output = output.decode("utf-8", "replace")
                if line_callback is not None:
                    line_callback(decoded_output)
                print(f">> {decoded_output.rstrip()}")

            process.stdout.close()
            process.stderr.close()
            print("Process finished with code: " + str(process.returncode))
        
        except KeyboardInterrupt:
            pass

        except Exception as e:
            print("Error: " + str(e))

        finally:
            process_is_running = False

    process_thread = threading.Thread(target=run_process)
    process_thread.start()


def stop_process():
    global process_is_running
    global process
    global process_thread

    if not process_is_running or process is None: 
        print("Process is not running")
        return
    
    process_is_running = False

    def terminate_process():
        global process
        try:
            if process and process.poll() is None:
                process.terminate()
            process_thread.join()
            print("Process terminated")

        except Exception as e:
            print("Error: " + str(e))

    threading.Thread(target=terminate_process).start()


class RunGUI: #run GUI
    def __init__(self, debug: bool = False):
        self.debug = debug
        root = tk.Tk()
        root.title("Talk-AI")
        root.geometry("500x500")
        root.resizable(False, False)
        root.iconbitmap("icon.ico")

        frame = ttk.Frame(root)
        frame.pack(fill=tk.BOTH, expand=False)

        run_button = ttk.Button(frame, text="Run", command=lambda: run_process(lambda line: (console.insert(tk.END, line), console.yview_moveto(1))))
        run_button.grid(row=0, column=0, padx=5, pady=5)
            
        stop_button = ttk.Button(frame, text="Stop", command=stop_process)
        stop_button.grid(row=0, column=1, padx=5, pady=5)

        console = tk.Text(frame, height=25, width=60)
        console.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

        self.root = root

    def log_debug(self, message: str):
        if self.debug:
            print("DEBUG: " + message)

    def run(self):
        self.log_debug("Run")
        self.root.mainloop()


if __name__ == "__main__":
    try:
        RunGUI(debug=True).run()
    
    except KeyboardInterrupt:
        print("Program terminated by user.")
        stop_process()
        sys.exit()