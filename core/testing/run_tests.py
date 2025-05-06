import os
import subprocess

TESTS = [
    {
        "id": "DOCX-001",
        "description": "Создание Word-файла с текстом",
        "command": 'создай документ Word про Луну с текстом',
        "expected_file": "moon.docx"
    },
    {
        "id": "DEV-002",
        "description": "Создание директории и файла",
        "command": 'создай папку hello123 и положи туда файл info.txt',
        "expected_file": "hello123/info.txt"
    }
]

def run_test(test):
    print(f"🧪 Тест {test['id']}: {test['description']}")
    process = subprocess.Popen(
        ["python3", "bot.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    try:
        stdout, stderr = process.communicate(input=test['command'] + "\n", timeout=15)
    except subprocess.TimeoutExpired:
        process.kill()
        print("❌ Timeout")
        return False

    path = os.path.join(os.getcwd(), test["expected_file"])
    if os.path.exists(path):
        print(f"✅ Успешно: найден {test['expected_file']}")
        return True
    else:
        print(f"❌ Не найден: {test['expected_file']}")
        return False

def main():
    passed = 0
    for test in TESTS:
        if run_test(test):
            passed += 1
    print(f"\n🏁 Всего пройдено: {passed}/{len(TESTS)}")

if __name__ == "__main__":
    main()
