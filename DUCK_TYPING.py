class TextFile:
    def __init__(self, filename):
        self.filename = filename

    # The "Quack" method
    def write(self, data):
        print(f"[Disk Operation] Opening '{self.filename}'...")
        print(f"[Disk Operation] Writing '{data}' to text file.")
        print("[Disk Operation] Save Complete.\n")


class CloudStorage:
    def __init__(self, provider):
        self.provider = provider

    # The "Quack" method
    def write(self, data):
        print(f"[Network] Connecting to {self.provider} API...")
        print(f"[Network] Uploading packet: '{data}'")
        print("[Network] 200 OK: Upload Complete.\n")


class Database:
    def __init__(self, db_name):
        self.db_name = db_name
        self.connected = False

    def connect(self):
        self.connected = True

    # The "Quack" method
    def write(self, data):
        if not self.connected:
            self.connect()
        print(f"[SQL] INSERT INTO {self.db_name} VALUES ('{data}')")
        print("[SQL] Commit successful.\n")


class ReadOnlyPDF:
    """
    This class represents an object that CANNOT write data.
    It does NOT have the 'write' method.
    It is the 'Non-Duck'.
    """

    def __init__(self, filename):
        self.filename = filename

    def read(self):
        return "Reading PDF content..."


# ==========================================
# The Duck Typing Function
# ==========================================
def archive_data(storage_device, data_to_save):
    """
    This function demonstrates Duck Typing.

    It accepts 'storage_device'. It does not care if it is a
    TextFile, CloudStorage, or Database.

    It only cares: "Can you .write()?"
    """
    print(f"--- Attempting to save to {type(storage_device).__name__} ---")

    # EAFP Principle: "Easier to Ask for Forgiveness than Permission"
    # Try to do it, and catch the error if the object can't handle it.
    try:
        storage_device.write(data_to_save)
    except AttributeError as e:
        print(f"!!! ERROR: This object cannot write data.")
        print(f"!!! Details: {e}\n")


# ==========================================
# Main Execution
# ==========================================
if __name__ == "__main__":
    # 1. Instantiate completely different objects
    my_file = TextFile("notes.txt")
    my_cloud = CloudStorage("AWS S3")
    my_db = Database("User_Table")

    # 2. Instantiate an object that doesn't fit
    my_pdf = ReadOnlyPDF("manual.pdf")

    # 3. Create a list of objects
    # In a static language, a list usually holds only one type of object.
    # In Python, this list is a mix of totally unrelated things.
    storage_devices = [my_file, my_cloud, my_db, my_pdf]

    # 4. Iterate and Process
    content = "Important Project Data"

    for device in storage_devices:
        archive_data(device, content)