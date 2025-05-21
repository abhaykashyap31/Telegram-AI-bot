import threading
import uvicorn
from main import main

def run_fastapi():
    uvicorn.run("main:main", host="0.0.0.0", port=8000, log_level="info")

if __name__ == "__main__":
    threading.Thread(target=run_fastapi, daemon=True).start()
    main()
