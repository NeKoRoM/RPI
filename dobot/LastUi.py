import tkinter as tk
from tkinter import ttk
import json

class RobotControlUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Robot Control Panel")

        # Virtual Keyboard for Axes
        self.create_virtual_keyboard()

        # Position Management
        self.create_position_management()

        # Robot Commands
        self.create_robot_commands()

        # Logs Window
        self.create_logs_window()

    def create_virtual_keyboard(self):
        frame = tk.LabelFrame(self.root, text="Virtual Keyboard (Axes Control)", padx=10, pady=10)
        frame.pack(side="left", padx=10, pady=5, fill="y")

        self.axis_values = {axis: tk.DoubleVar() for axis in ['X', 'Y', 'Z']}

        for i, (axis, var) in enumerate(self.axis_values.items()):
            tk.Label(frame, text=f"{axis}:").grid(row=i, column=0, sticky="w")
            tk.Entry(frame, textvariable=var, width=10).grid(row=i, column=1)
            tk.Button(frame, text=f"Set {axis}", command=lambda a=axis: self.set_axis(a)).grid(row=i, column=2)
            tk.Button(frame, text="+", command=lambda a=axis: self.increment_axis(a)).grid(row=i, column=3)
            tk.Button(frame, text="-", command=lambda a=axis: self.decrement_axis(a)).grid(row=i, column=4)

        tk.Button(frame, text="Load Current Position", command=self.load_current_position_to_fields).grid(row=3, column=0, columnspan=2, pady=5)
        tk.Button(frame, text="Send Modified Position", command=self.send_modified_position).grid(row=3, column=2, columnspan=3, pady=5)

        joint_frame = tk.LabelFrame(self.root, text="Virtual Keyboard (Joint Control)", padx=10, pady=10)
        joint_frame.pack(side="left", padx=10, pady=5, fill="y")

        self.joint_values = {joint: tk.DoubleVar() for joint in ['Joint1', 'Joint2', 'Joint3']}

        for i, (joint, var) in enumerate(self.joint_values.items()):
            tk.Label(joint_frame, text=f"{joint}:").grid(row=i, column=0, sticky="w")
            tk.Entry(joint_frame, textvariable=var, width=10).grid(row=i, column=1)
            tk.Button(joint_frame, text=f"Set {joint}", command=lambda j=joint: self.set_joint(j)).grid(row=i, column=2)
            tk.Button(joint_frame, text="+", command=lambda j=joint: self.increment_joint(j)).grid(row=i, column=3)
            tk.Button(joint_frame, text="-", command=lambda j=joint: self.decrement_joint(j)).grid(row=i, column=4)

        # Field to show the current position
        self.current_position_var = tk.StringVar()
        tk.Label(self.root, textvariable=self.current_position_var, fg="blue").pack(pady=5)

    def create_position_management(self):
        frame = tk.LabelFrame(self.root, text="Position Management", padx=10, pady=10)
        frame.pack(padx=10, pady=5, fill="x")

        self.position_list = ttk.Combobox(frame, values=[])
        self.position_list.pack(side="left", padx=5)

        ttk.Button(frame, text="Save Position", command=self.save_position).pack(side="left", padx=5)
        ttk.Button(frame, text="Load Position", command=self.load_position).pack(side="left", padx=5)
        ttk.Button(frame, text="Delete Position", command=self.delete_position).pack(side="left", padx=5)

        ttk.Button(frame, text="Save to File", command=self.save_positions_to_file).pack(side="left", padx=5)
        ttk.Button(frame, text="Load from File", command=self.load_positions_from_file).pack(side="left", padx=5)

    def create_robot_commands(self):
        frame = tk.LabelFrame(self.root, text="Robot Commands", padx=10, pady=10)
        frame.pack(padx=10, pady=5, fill="x")

        ttk.Button(frame, text="Get Current Position", command=self.get_current_position).pack(side="left", padx=5)
        ttk.Button(frame, text="Reset Errors", command=self.reset_errors).pack(side="left", padx=5)

    def create_logs_window(self):
        frame = tk.LabelFrame(self.root, text="Logs", padx=10, pady=10)
        frame.pack(padx=10, pady=5, fill="both", expand=True)

        self.log_text = tk.Text(frame, height=10)
        self.log_text.pack(fill="both", expand=True, padx=5, pady=5)

    def set_axis(self, axis):
        value = self.axis_values[axis].get()
        self.log_message(f"Axis {axis} set to {value}")

    def increment_axis(self, axis):
        self.axis_values[axis].set(self.axis_values[axis].get() + 1)
        self.log_message(f"Axis {axis} incremented to {self.axis_values[axis].get()}")

    def decrement_axis(self, axis):
        self.axis_values[axis].set(self.axis_values[axis].get() - 1)
        self.log_message(f"Axis {axis} decremented to {self.axis_values[axis].get()}")

    def set_joint(self, joint):
        value = self.joint_values[joint].get()
        self.log_message(f"Joint {joint} set to {value}")

    def increment_joint(self, joint):
        self.joint_values[joint].set(self.joint_values[joint].get() + 1)
        self.log_message(f"Joint {joint} incremented to {self.joint_values[joint].get()}")

    def decrement_joint(self, joint):
        self.joint_values[joint].set(self.joint_values[joint].get() - 1)
        self.log_message(f"Joint {joint} decremented to {self.joint_values[joint].get()}")

    def load_current_position_to_fields(self):
        # Simulated current position (replace with actual robot data retrieval)
        current_position = {"X": 100.0, "Y": 200.0, "Z": 300.0, "Joint1": 45.0, "Joint2": 30.0, "Joint3": 60.0}
        for axis, value in current_position.items():
            if axis in self.axis_values:
                self.axis_values[axis].set(value)
            if axis in self.joint_values:
                self.joint_values[axis].set(value)
        self.current_position_var.set(f"Current: {current_position}")
        self.log_message("Current position loaded into fields.")

    def send_modified_position(self):
        modified_position = {axis: var.get() for axis, var in self.axis_values.items()}
        modified_position.update({joint: var.get() for joint, var in self.joint_values.items()})
        self.log_message(f"Sending modified position: {modified_position}")

    def save_position(self):
        pos_name = f"Position {len(self.position_list['values']) + 1}"
        values = list(self.position_list["values"])
        position_data = {axis: var.get() for axis, var in self.axis_values.items()}
        position_data.update({joint: var.get() for joint, var in self.joint_values.items()})
        values.append({"name": pos_name, "data": position_data})
        self.position_list["values"] = [pos["name"] for pos in values]
        self.log_message(f"Position '{pos_name}' saved.")

    def load_position(self):
        pos_name = self.position_list.get()
        values = list(self.position_list["values"])
        for pos in values:
            if pos["name"] == pos_name:
                for axis, value in pos["data"].items():
                    if axis in self.axis_values:
                        self.axis_values[axis].set(value)
                    if axis in self.joint_values:
                        self.joint_values[axis].set(value)
                self.current_position_var.set(f"Loaded: {pos['data']}")
                self.log_message(f"Loaded position: {pos_name}")
                return
        self.log_message("No position selected to load.")

    def delete_position(self):
        pos_name = self.position_list.get()
        values = list(self.position_list["values"])
        values = [pos for pos in values if pos["name"] != pos_name]
        self.position_list["values"] = [pos["name"] for pos in values]
        self.log_message(f"Position '{pos_name}' deleted.")

    def save_positions_to_file(self):
        values = list(self.position_list["values"])
        try:
            with open("positions.json", "w") as file:
                json.dump(values, file)
            self.log_message("Positions saved to file.")
        except Exception as e:
            self.log_message(f"Error saving positions to file: {e}")

    def load_positions_from_file(self):
        try:
            with open("positions.json", "r") as file:
                values = json.load(file)
                self.position_list["values"] = [pos["name"] for pos in values]
                self.log_message("Positions loaded from file.")
        except Exception as e:
            self.log_message(f"Error loading positions from file: {e}")

    def get_current_position(self):
        # Simulated current position retrieval
        current_position = {"X": 100.0, "Y": 200.0, "Z": 300.0, "Joint1": 45.0, "Joint2": 30.0, "Joint3": 60.0}
        self.current_position_var.set(f"Current: {current_position}")
        self.log_message(f"Current position: {current_position}")

    def reset_errors(self):
        self.log_message("Errors reset.")

    def log_message(self, message):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = RobotControlUI(root)
    root.mainloop()
