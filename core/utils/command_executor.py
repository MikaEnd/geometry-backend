import subprocess

def execute_command(command: str) -> str:
    try:
        result = subprocess.run(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            timeout=30
        )
        return result.stdout.strip()
    except Exception as e:
        return f"❌ Ошибка при выполнении команды: {str(e)}"
