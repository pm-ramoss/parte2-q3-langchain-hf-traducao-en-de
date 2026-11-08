"""Testes com a cadeia substituída por um stub (sem baixar o modelo)."""
from fastapi.testclient import TestClient

from app import main


class FakeChain:
    def invoke(self, inputs):
        return f"[DE] {inputs['text']}"


def test_translate_ok(monkeypatch):
    monkeypatch.setattr(main, "build_chain", lambda: FakeChain())
    with TestClient(main.app) as client:
        r = client.post("/translate", json={"text": "Hello"})
    assert r.status_code == 200
    assert r.json()["translated_text"] == "[DE] Hello"


def test_empty_text_rejected(monkeypatch):
    monkeypatch.setattr(main, "build_chain", lambda: FakeChain())
    with TestClient(main.app) as client:
        r = client.post("/translate", json={"text": ""})
    assert r.status_code == 422
