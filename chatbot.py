#!/usr/bin/env python3
"""Simple local chatbot with persistent conversation memory."""

from __future__ import annotations

import pickle
import re
import pathlib
import sys
import zlib
from typing import Any

STORAGE_DIR = pathlib.Path("chat_memory")
STORAGE_FILE = STORAGE_DIR / "conversation.bin"

class ChatMemory:
    def __init__(self, storage_file: pathlib.Path = STORAGE_FILE):
        self.storage_file = storage_file
        self.storage_file.parent.mkdir(parents=True, exist_ok=True)
        self.conversation = self._load() or []

    def add_message(self, role: str, text: str) -> None:
        self.conversation.append({"role": role, "text": text})
        self._save()

    def _load(self) -> list[dict[str, str]] | None:
        if not self.storage_file.exists():
            return None

        try:
            compressed = self.storage_file.read_bytes()
            return pickle.loads(zlib.decompress(compressed))
        except Exception:
            return []

    def _save(self) -> None:
        data = pickle.dumps(self.conversation)
        self.storage_file.write_bytes(zlib.compress(data))

    def get_recent(self, limit: int = 5) -> list[dict[str, str]]:
        return self.conversation[-limit:]

    def find_user_facts(self) -> dict[str, str]:
        facts: dict[str, str] = {}
        for message in self.conversation:
            if message["role"] != "user":
                continue
            match = re.search(r"i am (?:called|named)?\s*(.+?)($|\.|!|\?)", message["text"], re.I)
            if match:
                facts["name"] = match.group(1).strip()
        return facts


class ChatBot:
    def __init__(self) -> None:
        self.memory = ChatMemory()

    def run(self) -> None:
        self._print_welcome()
        while True:
            try:
                prompt = input("You: ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\nGoodbye!")
                break

            if not prompt:
                continue

            response = self.generate_response(prompt)
            self.memory.add_message("user", prompt)
            self.memory.add_message("assistant", response)
            print(f"Bot: {response}")

            if self._is_exit_command(prompt):
                break

    def generate_response(self, text: str) -> str:
        text_lower = text.lower()

        if self._is_exit_command(text):
            return "Goodbye! I’ll remember our chat."

        if self._is_thanks(text_lower):
            return "You’re welcome! Anything else you’d like to talk about?"

        if self._is_greeting(text_lower):
            return self._greeting_response()

        if "remember" in text_lower and "that" in text_lower:
            return self._remember_fact(text)

        facts = self.memory.find_user_facts()
        if "name" in facts and re.search(r"what is my name|who am i", text_lower):
            return f"You told me your name is {facts['name']}."

        if "name" in facts and re.search(r"my name|call me", text_lower):
            return f"I remember your name is {facts['name']}."

        if "name" in text_lower and ("my name" in text_lower or "call me" in text_lower):
            return "Nice to meet you. I’ll remember your name for the next conversation."

        return self._fallback_response()

    def _greeting_response(self) -> str:
        facts = self.memory.find_user_facts()
        if "name" in facts:
            return f"Hello again, {facts['name']}! What would you like to discuss today?"
        return "Hello! I’m your local chatbot. What would you like to talk about?"

    def _remember_fact(self, text: str) -> str:
        match = re.search(r"remember that (.+)", text, re.I)
        if match:
            fact = match.group(1).strip()
            self.memory.add_message("assistant", f"I will remember that: {fact}")
            return f"Okay, I’ll remember that: {fact}"
        return "Sure, what would you like me to remember?"

    def _is_greeting(self, text_lower: str) -> bool:
        return any(word in text_lower for word in ["hello", "hi", "hey", "good morning", "good afternoon", "good evening"])

    def _is_thanks(self, text_lower: str) -> bool:
        return any(word in text_lower for word in ["thanks", "thank you", "thx"])

    def _is_exit_command(self, text: str) -> bool:
        return bool(re.fullmatch(r"(quit|exit|bye|goodbye|stop|end)(\W*)", text.strip().lower()))

    def _fallback_response(self) -> str:
        return (
            "I’m a simple local chatbot. Tell me more, or ask me to remember something. "
            "You can say ‘quit’ to end the conversation."
        )

    def _print_welcome(self) -> None:
        print("Simple Chatbot")
        print("Type a message and press Enter. Type 'quit' to exit.")
        recent = self.memory.get_recent()
        if recent:
            print(f"Loaded {len(recent)} recent messages from memory.")


def main() -> None:
    bot = ChatBot()
    bot.run()


if __name__ == "__main__":
    main()
