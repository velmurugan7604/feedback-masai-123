import os
import shutil

base_dir = r"c:\Users\ELCOT\feedback app"
files_to_remove = ["app.py", "requirements.txt", ".env", ".env.example", "feedback.db"]
dirs_to_remove = ["static", "templates"]

for f in files_to_remove:
    path = os.path.join(base_dir, f)
    if os.path.exists(path):
        os.remove(path)

for d in dirs_to_remove:
    path = os.path.join(base_dir, d)
    if os.path.exists(path):
        shutil.rmtree(path)

print("Cleanup complete.")
