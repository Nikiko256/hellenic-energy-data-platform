from typer.testing import CliRunner

from hellenic_energy.__main__ import app

runner = CliRunner()


def test_doctor_command() -> None:
    result = runner.invoke(app, ["doctor"])
    
    assert result.exit_code == 0
    assert "environment is ready" in result.stdout