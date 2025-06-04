import threading
import uvicorn
from main import main, app_fastapi

def run_fastapi():
    uvicorn.run(app_fastapi, host="0.0.0.0", port=8000, log_level="info")

if __name__ == "__main__":
    threading.Thread(target=run_fastapi, daemon=True).start()
    main()
