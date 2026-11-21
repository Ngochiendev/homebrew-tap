#!/usr/bin/env python3
"""Update the cask from the public feed after verifying the GitHub release DMG."""

import hashlib
import os
from pathlib import Path
import re
import tempfile
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent.parent
FEED = "https://updates.sensebar.site/appcast.xml"
RELEASES = "https://github.com/Ngochiendev/SenseBar/releases/download"
SPARKLE = "{http://www.andymatuschak.org/xml-namespaces/sparkle}"


def download(url):
    request = urllib.request.Request(url, headers={"Cache-Control": "no-cache", "User-Agent": "SenseBar-Homebrew-Updater"})
    return urllib.request.urlopen(request, timeout=120)


def latest_release(xml):
    items = ET.fromstring(xml).findall("channel/item")
    if not items:
        raise ValueError("Feed has no releases")
    builds = [int(item.findtext(SPARKLE + "version", "")) for item in items]
    if len(builds) != len(set(builds)) or any(build <= 0 for build in builds):
        raise ValueError("Feed has duplicate or invalid builds")
    item = items[builds.index(max(builds))]
    version = item.findtext(SPARKLE + "shortVersionString", "")
    if not re.fullmatch(r"\d+\.\d+\.\d+", version):
        raise ValueError("Expected stable X.Y.Z version")
    enclosure = item.find("enclosure")
    expected = f"https://updates.sensebar.site/releases/SenseBar-v{version}-macOS-Universal.zip"
    if enclosure is None or enclosure.get("url") != expected:
        raise ValueError("Unexpected feed enclosure URL")
    return version


def checksum_for(text, filename):
    entries = []
    for line in text.splitlines():
        match = re.fullmatch(r"([0-9a-fA-F]{64})\s+\*?(.+)", line)
        if match and match[2] == filename:
            entries.append(match[1].lower())
    if len(entries) != 1:
        raise ValueError("Release checksums must contain exactly one matching DMG")
    return entries[0]


def version_tuple(version):
    return tuple(int(part) for part in version.split("."))


def update(cask, version, digest):
    text = cask.read_text(encoding="utf-8")
    versions = re.findall(r'^  version "(\d+\.\d+\.\d+)"$', text, re.MULTILINE)
    checksums = re.findall(r'^  sha256 "([0-9a-f]{64})"$', text, re.MULTILINE)
    if len(versions) != 1 or len(checksums) != 1:
        raise ValueError("Unexpected cask format")
    if version_tuple(version) < version_tuple(versions[0]):
        raise ValueError("Refusing cask downgrade")
    if version == versions[0]:
        if digest != checksums[0]:
            raise ValueError("Same version has different archive bytes; refusing replacement")
        return False
    text = text.replace(f'  version "{versions[0]}"', f'  version "{version}"', 1)
    text = text.replace(f'  sha256 "{checksums[0]}"', f'  sha256 "{digest}"', 1)
    # Replace only after every remote check succeeds.
    with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=cask.parent, delete=False) as file:
        temporary = Path(file.name)
        file.write(text)
    try:
        temporary.chmod(cask.stat().st_mode & 0o777)
        temporary.replace(cask)
    finally:
        temporary.unlink(missing_ok=True)
    return True


def main():
    with download(FEED) as response:
        version = latest_release(response.read())
    filename = f"SenseBar-v{version}-macOS-Universal.dmg"
    release_url = f"{RELEASES}/v{version}"
    with download(release_url + "/SHA256SUMS.txt") as response:
        expected = checksum_for(response.read().decode("utf-8"), filename)
    digest = hashlib.sha256()
    with download(release_url + "/" + urllib.parse.quote(filename)) as response:
        for chunk in iter(lambda: response.read(1024 * 1024), b""):
            digest.update(chunk)
    if digest.hexdigest() != expected:
        raise ValueError("Downloaded DMG differs from release SHA256SUMS; cask unchanged")
    changed = update(ROOT / "Casks/sensebar.rb", version, expected)
    if output := os.environ.get("GITHUB_OUTPUT"):
        with open(output, "a", encoding="utf-8") as file:
            file.write(f"changed={str(changed).lower()}\nversion={version}\n")
    print(f"{'Updated' if changed else 'Already current'}: SenseBar {version} (verified SHA-256)")


if __name__ == "__main__":
    main()
