def confirm_or_cancel(command: str) -> bool:
    print(f"\n🧾 Команда для выполнения: {command}")
    print("⏱️ Выполнение начнётся через 9 секунд...")
    print("↩️ Нажмите Enter — немедленно выполнить.")
    print("␛ Esc — отмена.")
    print("⏸️ Пробел — пауза / продолжить.")

    import sys, termios, tty, time, os, fcntl

    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    old_flags = fcntl.fcntl(fd, fcntl.F_GETFL)

    tty.setcbreak(fd)
    fcntl.fcntl(fd, fcntl.F_SETFL, old_flags | os.O_NONBLOCK)

    countdown = 9
    paused = False
    try:
        while countdown > 0:
            if not paused:
                print(f"\r⌛ {countdown} ", end='', flush=True)
                time.sleep(1)
                countdown -= 1

            try:
                key = os.read(fd, 1).decode()
                if key == "\x1b":
                    print("\n🚫 Отменено пользователем.")
                    return False
                elif key == "\n":
                    print("\n✅ Подтверждено.")
                    return True
                elif key == " ":
                    paused = not paused
                    print("\n⏸️ Пауза" if paused else "\n▶️ Продолжение")
            except BlockingIOError:
                continue

        print("\n⌛ Время истекло — выполняем.")
        return True
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        fcntl.fcntl(fd, fcntl.F_SETFL, old_flags)
