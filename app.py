import requests as rq
import json
import tkinter as tk
from tkinter import ttk
from datetime import datetime


def capitalize_first(input_str):
    """
        Capitalizes the first letter of a string while keeping rest lowercase.

                Parameters:
                        input_str (str): The string to format & capitalize.

                Returns:
                    str: input_str.lower().capitalize()
    """
    return input_str.lower().capitalize()


def get_data():
    """
        Reads and returns the ATHEX Status JSON file.

                Parameters:


                Returns:
                    list: name, list: status, int: response_code
        """
    url = 'https://status.athexgroup.gr/components.json'
    response = rq.get(url)

    name, status = [], []
    if response.status_code == 200:
        json_data = response.content.decode('utf-8')
        data = json.loads(json_data)

        # Extracting components
        components = data.get('components', [])
        for component in components:
            name.append(component['name'])
            status.append(capitalize_first(component['status']))

    return name, status, response.status_code


class App:
    """
        A class to represent the App.

        ...

        Attributes
        ----------

        Methods
        -------
        __init__():
            Initializes the App.
        update_table():
            Updates the data by making a new GET request.
        """

    def __init__(self):
        """
                Initializes the GUI and runs initial population of the data.

        """

        # Create the main window
        root = tk.Tk()
        root.title("ATHEX Live Status")

        # Variable to store text to display
        display_text = tk.StringVar()
        last_updated_text = tk.StringVar()

        sub_label = tk.Label(root, text="ATHEX Live Status - version 0.1.a. - F. Raissis", font=("Calibri", 9))
        sub_label.grid(row=1, column=0, columnspan=6, pady=1)

        # Label to display last updated time
        last_updated_label = tk.Label(root, textvariable=last_updated_text)
        last_updated_label.grid(row=4, column=0, columnspan=2, padx=2, pady=2)

        # Create a treeview widget for the table
        tree = ttk.Treeview(root, columns=("Column A", "Column B"), show="headings", height=6)
        tree.heading("Column A", text="Feed")
        tree.heading("Column B", text="Status")

        self.root = root
        self.tree = tree
        self.time = last_updated_text

        # Initial table setup
        self.update_table()

        # Place the treeview widget in the window
        tree.grid(row=3, column=0, columnspan=2, padx=10)

        # Run the Tkinter event loop
        root.mainloop()

    def update_table(self):
        """
            Updates the Data that is loaded onto the GUI via `mainloop()`.

                """

        tree = self.tree
        root = self.root
        # Clear existing data
        for item in tree.get_children():
            tree.delete(item)

        name, status, resp = get_data()
        # Update last updated time
        last_updated_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.time.set(f"Response: {resp} ---- Last Updated: {last_updated_time}")
        # Insert new data
        for a, b in zip(name, status):
            tree.insert("", "end", values=(a, b))

        # Apply adjustments to the treeview items
        for i in range(len(status)):
            if status[i] == "Operational":
                tree.item(tree.get_children()[i], values=(name[i], status[i]), tags=('green_background',))
            elif status[i] == "Maintenance":
                tree.item(tree.get_children()[i], values=(name[i], status[i]), tags=('orange_background',))
            else:
                tree.item(tree.get_children()[i], values=(name[i], status[i]), tags=('red_background',))

        # Configure the tags for styling for 'Column B'
        tree.tag_configure('green_background', background='lightgreen', foreground='black')
        tree.tag_configure('orange_background', background='lightcoral', foreground='darkorange')
        tree.tag_configure('red_background', background='lightcoral', foreground='red')

        # Schedule the next update
        root.after(int(1.5 * 1000), self.update_table)


if __name__ == '__main__':
    App()
