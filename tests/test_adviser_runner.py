from __future__ import annotations

import importlib.util
import io
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "skills" / "adviser" / "scripts"
sys.path.insert(0, str(SCRIPTS))
MODULE_PATH = SCRIPTS / "run_adviser.py"
SPEC = importlib.util.spec_from_file_location("run_adviser", MODULE_PATH)
assert SPEC and SPEC.loader
run_adviser = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = run_adviser
SPEC.loader.exec_module(run_adviser)


def jsonl(*events: dict[str, object]) -> str:
    return "\n".join(json.dumps(event) for event in events) + "\n"


def test_extracts_only_the_final_completed_agent_message() -> None:
    output = jsonl(
        {"type": "thread.started", "thread_id": "test"},
        {"type": "item.completed", "item": {"type": "agent_message", "text": "review"}},
        {"type": "turn.completed", "usage": {}},
    )

    assert run_adviser.extract_review(output) == "review"


@pytest.mark.parametrize(
    "output",
    [
        jsonl({"type": "turn.failed"}),
        jsonl({"type": "error"}),
        jsonl({"type": "turn.completed", "usage": {}}),
        jsonl({"type": "item.completed", "item": {"type": "agent_message", "text": "review"}}),
        "not-json\n",
    ],
)
def test_rejects_failed_or_incomplete_output(output: str) -> None:
    with pytest.raises(run_adviser.RouteError):
        run_adviser.extract_review(output)


def test_main_requests_the_exact_route_with_argv_and_stdin(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    captured: dict[str, object] = {}

    def fake_execute(
        command: list[str], prompt: str, child_env: dict[str, str], timeout: float
    ) -> subprocess.CompletedProcess[str]:
        captured["command"] = command
        captured["input"] = prompt
        captured["env"] = child_env
        captured["timeout"] = timeout
        output = jsonl(
            {"type": "item.completed", "item": {"type": "agent_message", "text": "review"}},
            {"type": "turn.completed", "usage": {}},
        )
        return subprocess.CompletedProcess(command, 0, output, "")

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "run_adviser.py",
            "--model",
            "gpt-5.6-sol",
            "--effort",
            "medium",
            "--codex-bin",
            "/safe/codex",
        ],
    )
    monkeypatch.setattr(sys, "stdin", io.StringIO("packet with $(shell) and `quotes`"))
    monkeypatch.setattr(run_adviser, "execute_codex", fake_execute)
    monkeypatch.delenv("CODEX_ADVISER_CHILD", raising=False)
    monkeypatch.setenv("CODEX_THREAD_ID", "parent-thread")

    assert run_adviser.main() == 0

    command = captured["command"]
    assert isinstance(command, list)
    assert command[0] == "/safe/codex"
    assert command[command.index("--model") + 1] == "gpt-5.6-sol"
    config_values = [command[index + 1] for index, value in enumerate(command) if value == "-c"]
    assert config_values == ['model_reasoning_effort="high"', 'approval_policy="never"']
    assert "--ask-for-approval" not in command
    assert "$(shell)" not in command
    assert "$(shell)" in str(captured["input"])
    child_env = captured["env"]
    assert isinstance(child_env, dict)
    assert "CODEX_THREAD_ID" not in child_env
    assert child_env["CODEX_ADVISER_CHILD"] == "1"
    assert capsys.readouterr().out.strip() == "review"


def test_main_reports_timeout(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    def timeout(*args: object, **kwargs: object) -> subprocess.CompletedProcess[str]:
        raise subprocess.TimeoutExpired("codex", 0.01)

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "run_adviser.py",
            "--model",
            "gpt-5.6-sol",
            "--effort",
            "medium",
            "--timeout-seconds",
            "0.01",
        ],
    )
    monkeypatch.setattr(sys, "stdin", io.StringIO("packet"))
    monkeypatch.setattr(run_adviser, "execute_codex", timeout)
    monkeypatch.delenv("CODEX_ADVISER_CHILD", raising=False)

    assert run_adviser.main() == 124
    assert "timed out" in capsys.readouterr().err


def test_main_preserves_nonzero_cli_failure(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    def fail(command: list[str], *args: object) -> subprocess.CompletedProcess[str]:
        return subprocess.CompletedProcess(command, 7, "", "model unavailable")

    monkeypatch.setattr(
        sys,
        "argv",
        ["run_adviser.py", "--model", "gpt-5.6-terra", "--effort", "high"],
    )
    monkeypatch.setattr(sys, "stdin", io.StringIO("packet"))
    monkeypatch.setattr(run_adviser, "execute_codex", fail)
    monkeypatch.delenv("CODEX_ADVISER_CHILD", raising=False)

    assert run_adviser.main() == 7
    assert "model unavailable" in capsys.readouterr().err


def test_main_refuses_recursive_execution(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr(sys, "argv", ["run_adviser.py"])
    monkeypatch.setattr(sys, "stdin", io.StringIO("packet"))
    monkeypatch.setenv("CODEX_ADVISER_CHILD", "1")

    assert run_adviser.main() == 2
    assert "nested Adviser" in capsys.readouterr().err


def test_recursion_guard_holds_across_a_real_process_boundary() -> None:
    environment = os.environ.copy()
    environment["CODEX_ADVISER_CHILD"] = "1"

    result = subprocess.run(
        [
            sys.executable,
            str(MODULE_PATH),
            "--model",
            "gpt-5.6-sol",
            "--effort",
            "medium",
            "--codex-bin",
            "/must-not-run",
        ],
        input="packet",
        text=True,
        capture_output=True,
        env=environment,
        check=False,
    )

    assert result.returncode == 2
    assert "nested Adviser execution is prohibited" in result.stderr


def test_timeout_kills_the_isolated_process_group(monkeypatch: pytest.MonkeyPatch) -> None:
    calls: list[tuple[object, ...]] = []

    class FakeProcess:
        pid = 1234
        returncode = 124

        def communicate(
            self, input: str | None = None, timeout: float | None = None
        ) -> tuple[str, str]:
            calls.append(("communicate", input, timeout))
            if timeout is not None:
                raise subprocess.TimeoutExpired("codex", timeout)
            return "", ""

        def kill(self) -> None:
            calls.append(("kill",))

    def fake_popen(*args: object, **kwargs: object) -> FakeProcess:
        calls.append(("popen", args, kwargs))
        return FakeProcess()

    monkeypatch.setattr(run_adviser.subprocess, "Popen", fake_popen)
    monkeypatch.setattr(run_adviser.os, "name", "posix")
    monkeypatch.setattr(
        run_adviser.os, "killpg", lambda pid, sig: calls.append(("killpg", pid, sig))
    )

    with pytest.raises(subprocess.TimeoutExpired):
        run_adviser.execute_codex(["codex"], "packet", {}, 0.01)

    assert ("killpg", 1234, run_adviser.signal.SIGKILL) in calls
    assert ("kill",) not in calls
    assert calls[-1] == ("communicate", None, None)
