import subprocess
import logging

class CommandExecutorService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def execute(self, command: str) -> dict:
        try:
            result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True)
            self.logger.info(f"[EXECUTE] ✅ {command}")
            return {"status": "success", "command": command, "output": result.strip()}
        except subprocess.CalledProcessError as e:
            self.logger.warning(f"[EXECUTE] ❌ {command}: {e.output.strip()}")
            return {"status": "error", "command": command, "output": e.output.strip()}
