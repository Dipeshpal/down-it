from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import subprocess
import threading
import os

app = FastAPI()


class SubprocessOutputCaptureThread(threading.Thread):
    def __init__(self, process):
        super().__init__()
        self.process = process
        self.output = []

    def run(self):
        for line in iter(self.process.stdout.readline, b''):
            line = line.decode().rstrip()
            self.output.append(line)
            print(line)

        self.process.stdout.close()


def capture_subprocess_output(command, timeout=30):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    capture_thread = SubprocessOutputCaptureThread(process)
    capture_thread.start()

    try:
        capture_thread.join(timeout=timeout)
    except KeyboardInterrupt:
        process.kill()

    return "\n".join(capture_thread.output)


@app.get("/check_log")
async def check_log(request: Request):
    log_output = capture_subprocess_output(["tail", "-n", "100", "logfile.txt"])
    html_content = f"<html><body><pre>{log_output}</pre></body></html>"
    return HTMLResponse(content=html_content, status_code=200)


@app.get("/")
async def start_process():
    command = "python hammer_app.py"
    subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return {"status": "success", "message": "Started process."}


if __name__ == "__main__":
    # Run the templates
    os.system("uvicorn main2:templates --reload")
