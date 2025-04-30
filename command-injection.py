import subprocess

def execute_command(user_input):
    """Executes the user-provided command directly on the system."""
    subprocess.run(user_input, shell=True, check=False)

if __name__ == "__main__":
    command = input("Enter a command to execute: ")
    print(f"Executing: {command}")
    execute_command(command)
    print("Command execution finished.")
