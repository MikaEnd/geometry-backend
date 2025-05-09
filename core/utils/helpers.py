# core/utils/helpers.py

import asyncio
import sys
import termios
import tty
import select

async def countdown_with_control(seconds: int = 9):
    print("⏱️ Выполнение начнётся через 9 секунд...")
    print("↩️ Нажмите Enter — немедленно выполнить.")
    print("␛ Esc — отмена.")
    print("⏸️ Пробел — пауза / продолжить.")
    print("⌛", end=" ", flush=True)

    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    paused = False

    try:
        tty.setcbreak(fd)
        for i in range(seconds, 0, -1):
            if sys.stdin in select.select([sys.stdin], [], [], 1)[0]:
                char = sys.stdin.read(1)
                if char == "\n":
                    print("\n✅ Выполнение подтверждено клавишей Enter.")
                    return
                elif char == "\x1b":  # ESC
                    print("\n❌ Выполнение отменено.")
                    raise KeyboardInterrupt()
                elif char == " ":
                    paused = not paused
                    print("\n⏸️ Пауза." if paused else "\n▶️ Продолжение.")

            if not paused:
                print(i, end=" ", flush=True)

        print("\n✅ Подтверждено.")
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
