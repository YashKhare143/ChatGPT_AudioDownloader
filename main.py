from tkinter import filedialog, messagebox, END
import subprocess
import os
import gui

save_dir = None  # Global variable for the save directory

def choose_directory(path_entry):
    global save_dir
    save_dir = filedialog.askdirectory()
    if save_dir:
        path_entry.delete(0, END)
        path_entry.insert(0, save_dir)
    else:
        path_entry.insert(0, "No directory selected.")
        # messagebox.showwarning("Directory Selection", )

def execute_command(command_entry, filename_entry, path_entry):
    global save_dir

    command = command_entry.get().strip()
    filename = filename_entry.get().strip()

    if not save_dir:
        path_entry.insert(0, "No directory selected.")
        
        messagebox.showerror("Input Error", "Please select a save directory.")
        return

    output_file = os.path.join(save_dir, filename)

    if not command:
        messagebox.showerror("Input Error", "Please enter a PowerShell command.")
        return

    if not filename:
        messagebox.showerror("Input Error", "Please enter an output file name.")
        return

    command += f' -outfile "{output_file}.aac"'

    try:
        # Run the PowerShell command
        result = subprocess.run(["powershell", "-Command", command], capture_output=True, text=True)

        # Save output to the file
        with open(output_file, "w", encoding="utf-8") as file:
            file.write(result.stdout)

        messagebox.showinfo("Success", f"Output saved to {output_file}")
    except Exception as e:
        messagebox.showerror("Execution Error", f"An error occurred: {e}")

# Run the GUI and pass the logic functions as arguments
if __name__ == "__main__":
    gui.create_window(choose_directory, execute_command)
