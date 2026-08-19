import os
import io
import zipfile
from pathlib import Path

from flask import Flask, send_file, send_from_directory

app = Flask(__name__, static_folder="static")


@app.route("/")
def index():
    return send_from_directory("static", "index.html")


@app.route("/deploy-monday-morning-scintilla.zip")
def monday_morning_skill():
    """Serve the skill even when the Apps snapshot expands the source ZIP."""
    archive = Path("static/deploy-monday-morning-scintilla.zip")
    if archive.is_file():
        return send_file(archive, as_attachment=True, download_name=archive.name)

    skill_dir = Path("static/deploy-monday-morning-scintilla")
    if not skill_dir.is_dir():
        return ("Monday Morning skill package is unavailable", 404)

    output = io.BytesIO()
    with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as bundle:
        for source in sorted(p for p in skill_dir.rglob("*") if p.is_file()):
            bundle.write(source, Path(skill_dir.name) / source.relative_to(skill_dir))
    output.seek(0)
    return send_file(
        output,
        mimetype="application/zip",
        as_attachment=True,
        download_name="deploy-monday-morning-scintilla.zip",
    )


@app.route("/<path:path>")
def assets(path):
    return send_from_directory("static", path)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("DATABRICKS_APP_PORT", 8000)))
