import os

def resize_terminal(columns, rows):
    # Check if the operating system is supported
    if os.name == "posix":  # Linux and macOS
        os.system(f"printf '\\e[8;{rows};{columns}t'")
    elif os.name == "nt":  # Windows
        os.system(f"mode con: cols={columns} lines={rows}")
    else:
        print("Unsupported operating system")

# Example usage: Resize terminal to 100x30
resize_terminal(50, 30)
