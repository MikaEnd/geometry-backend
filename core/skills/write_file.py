    async def execute(self, user_id: str, message: str) -> str:
        def parse_response(raw_text: str) -> tuple[str, str] | None:
            raw_text = re.sub(r"^```(?:[a-z]+)?\n?", "", raw_text.strip(), flags=re.IGNORECASE)
            raw_text = re.sub(r"\n?```$", "", raw_text.strip())
            if "\n" not in raw_text:
                return None
            filename, content = raw_text.split("\n", 1)
            return filename.strip(), content.strip()

        system_prompt = (
            "Ты файловый помощник. Получи от пользователя имя файла и его содержимое. "
            "Ответь строго в формате:\n<имя файла>\n<содержимое файла>. "
            "Без markdown, без пояснений, без форматирования. Без кода, который сам записывает файл."
        )

        raw = ask_llm(system_prompt=system_prompt, user_message=message).get("text", "").strip()
        print(f"🔍 Ответ от LLM:\n{raw}")

        if "with open(" in raw and ".write(" in raw:
            retry_prompt = (
                "Ответь строго в формате:\n<имя файла>\n<содержимое файла>.\n"
                "Без пояснений, без markdown, без кода, без Python. Только имя файла и его содержимое."
            )
            raw = ask_llm(system_prompt=retry_prompt, user_message=message).get("text", "").strip()
            print(f"🔁 Перегенерация:\n{raw}")

        parsed = parse_response(raw)
        if not parsed:
            return f"⚠️ Не удалось извлечь имя и содержимое файла:\n{raw}"

        filename, content = parsed

        if not re.match(r"^[\w\-.а-яА-ЯёЁ]+(\.py|\.txt|\.sh|\.md)?$", filename, re.IGNORECASE):
            return f"🚫 Недопустимое имя файла: {filename}"

        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(content)
            return f"📄 Файл {filename} успешно создан."
        except Exception as e:
            return f"🚫 Ошибка при записи файла: {e}"
