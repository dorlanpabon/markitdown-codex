import json
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "markitdown"


def test_marketplace_and_bundles_are_portable(tmp_path):
    marketplace = json.loads((ROOT / ".agents/plugins/marketplace.json").read_text())
    entry = marketplace["plugins"][0]
    assert (ROOT / entry["source"]["path"]).resolve() == PLUGIN
    manifest = json.loads((PLUGIN / ".codex-plugin/plugin.json").read_text())
    assert entry["name"] == manifest["name"]
    subprocess.run([sys.executable, "scripts/build_release.py"], cwd=ROOT, check=True)
    bundle = ROOT / "dist" / f"markitdown-skills-{manifest['version']}.zip"
    with zipfile.ZipFile(bundle) as archive:
        assert "markitdown/SKILL.md" in archive.namelist()
        assert "markitdown/scripts/convert.py.lock" in archive.namelist()
        assert not any("__pycache__" in name for name in archive.namelist())
        archive.extractall(tmp_path / "installed")
    with zipfile.ZipFile(ROOT / "dist/markitdown-review-fixtures.zip") as archive:
        archive.extractall(tmp_path / "fixtures")
    script = tmp_path / "installed/markitdown/scripts/convert.py"
    for filename, expected in [
        ("sample.pdf", "Quarterly report 2026"),
        ("sample.docx", "Project document"),
        ("sample.pptx", "Project slides"),
        ("sample.xlsx", "Coffee"),
        ("unicode.txt", "Bogotá"),
    ]:
        output = tmp_path / (filename + ".md")
        result = subprocess.run(
            [
                "uv",
                "run",
                "--locked",
                "--script",
                str(script),
                str(tmp_path / "fixtures" / filename),
                "--output",
                str(output),
            ],
            cwd=tmp_path,
            capture_output=True,
            timeout=120,
        )
        assert result.returncode == 0, result.stderr
        assert expected in output.read_text(encoding="utf-8")
