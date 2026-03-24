MEMORY_FILE = "memory.txt"

def save_name(name):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        f.write(name)

def load_name():
    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return f.read().strip()
    except:
        return ""