from pathlib import Path
root = Path("/data/data/com.termux/files/home/storage/shared/Download")
for f in root.rglob("*"):
    if f.is_file() and not any(x in str(f) for x in ["proc", "mountinfo", "bugreport", ".py"]):
        print(f"Target: {f.name} ({f.stat().st_size} bytes)")
