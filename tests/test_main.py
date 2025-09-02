import builtins
import importlib
import runpy


def test_exit_application(monkeypatch, capsys):
    """
    Simulate a single input "4" to trigger application exit.
    """
    inputs = iter(["4"])
    monkeypatch.setattr(builtins, "input", lambda _: next(inputs))
    main = importlib.import_module("main")
    main.main()
    out = capsys.readouterr().out
    assert "Exiting the program. Goodbye!" in out


def test_menu_total_then_exit(monkeypatch, capsys):
    """
    Choose 1 (TOTAL) then 4 (Exit) to cover the TOTAL branch in main.
    """
    inputs = iter(["1", "4"])
    monkeypatch.setattr(builtins, "input", lambda _: next(inputs))
    main = importlib.import_module("main")
    main.main()
    out = capsys.readouterr().out
    assert "Account Management System" in out
    assert "Current balance:" in out
    assert "Exiting the program. Goodbye!" in out


def test_menu_invalid_choice_then_exit(monkeypatch, capsys):
    """
    Choose an invalid option then 4 (Exit) to cover the invalid branch.
    """
    inputs = iter(["9", "4"])
    monkeypatch.setattr(builtins, "input", lambda _: next(inputs))
    main = importlib.import_module("main")
    main.main()
    out = capsys.readouterr().out
    assert "Invalid choice, please select 1-4." in out
    assert "Exiting the program. Goodbye!" in out


def test_run_main_as_script(monkeypatch, capsys):
    """
    Execute main.py as a script to cover the __main__ guard.
    """
    inputs = iter(["4"])
    monkeypatch.setattr(builtins, "input", lambda _: next(inputs))
    runpy.run_path("main.py", run_name="__main__")
    out = capsys.readouterr().out
    assert "Exiting the program. Goodbye!" in out


def test_menu_credit_branch_dispatch(monkeypatch, capsys):
    """
    Choose 2 (CREDIT) then 4 (Exit): ensure main() dispatches CREDIT to operations.execute.
    """
    import main
    calls = []

    def fake_execute(arg):
        calls.append(arg)
        print(f"DISPATCH:{arg}")

    inputs = iter(["2", "4"])
    monkeypatch.setattr(builtins, "input", lambda _: next(inputs))
    monkeypatch.setattr(main.operations, "execute", fake_execute)

    main.main()
    out = capsys.readouterr().out
    assert "DISPATCH:CREDIT" in out
    assert calls == ["CREDIT"]
    assert "Exiting the program. Goodbye!" in out


def test_menu_debit_branch_dispatch(monkeypatch, capsys):
    """
    Choose 3 (DEBIT) then 4 (Exit): ensure main() dispatches DEBIT to operations.execute.
    """
    import main
    calls = []

    def fake_execute(arg):
        calls.append(arg)
        print(f"DISPATCH:{arg}")

    inputs = iter(["3", "4"])
    monkeypatch.setattr(builtins, "input", lambda _: next(inputs))
    monkeypatch.setattr(main.operations, "execute", fake_execute)

    main.main()
    out = capsys.readouterr().out
    assert "DISPATCH:DEBIT" in out
    assert calls == ["DEBIT"]
    assert "Exiting the program. Goodbye!" in out