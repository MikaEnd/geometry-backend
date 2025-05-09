# core/utils/helpers.py

import asyncio
import sys

async def countdown_with_control(seconds: int = 9):
    print("⏱️ Выполнение начнётся через 9 секунд...")
    print("↩️ Нажмите Enter — немедленно выполнить.")
    print("␛ Esc — отмена.")
    print("⏸️ Пробел — пауза / продолжить.")
    print("⌛", end=" ", flush=True)

    for i in range(seconds, 0, -1):
        await asyncio.sleep(1)
        print(i, end=" ", flush=True)

    print("\n✅ Подтверждено.")
