# tests/conftest.py
import sys
import os

# Добавляем корень проекта (где находится папка app/) в sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))