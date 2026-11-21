# SenseBar Homebrew Tap

Install the signed Universal macOS app (Apple Silicon and Intel, macOS 14 or later):

```sh
brew install --cask Ngochiendev/tap/sensebar
```

If your Homebrew version asks you to trust this third-party cask, review [Casks/sensebar.rb](Casks/sensebar.rb), then run:

```sh
brew tap Ngochiendev/tap
brew trust --cask Ngochiendev/tap/sensebar
brew install --cask Ngochiendev/tap/sensebar
```

Open SenseBar from Applications and complete its permission setup. The same app supports English and Vietnamese.

## Updates

SenseBar can update itself from Settings. To check for a new cask version through Homebrew:

```sh
brew update
brew upgrade --cask --greedy Ngochiendev/tap/sensebar
```

`--greedy` includes apps that can update themselves. If Homebrew shows an older cask version than an in-app update, wait for this tap to be updated rather than forcing a downgrade.

## Uninstall

Quit SenseBar normally first so Presentation Mode can restore system changes, then run:

```sh
brew uninstall --cask sensebar
```

Use `brew uninstall --cask --zap sensebar` only if you also want to remove the listed local preferences and caches. macOS permission grants are managed separately in System Settings.

## Maintainers

The **Update SenseBar from appcast** workflow checks `https://updates.sensebar.site/appcast.xml` every hour (at minute 17 UTC; GitHub may delay scheduled jobs). It selects the highest build, downloads that version's GitHub Release DMG, and checks its SHA-256 against the release's `SHA256SUMS.txt`. A new version updates only the cask's version/checksum, runs Homebrew style and strict online audit, then commits to this tap automatically. No extra secret is required; the workflow uses this repository's GitHub token.

Run the workflow manually from Actions to check immediately. If the feed is ahead of the GitHub Release upload, verification fails without changing the cask; the next scheduled run retries. Downgrades and different bytes for the same version are rejected. No commit is created when already current. Future updates must keep stable `X.Y.Z` versions and the existing Universal ZIP/DMG names.

For a local check, run `python3 scripts/update_from_appcast.py` from any directory. This verifies the remote release and updates the cask locally; it does not commit or push. The cask uses the immutable versioned GitHub Release URL; do not replace archive bytes for an existing version.

This is the project's own tap, separate from the Homebrew-maintained `homebrew/cask` repository. See [SenseBar](https://github.com/Ngochiendev/SenseBar) for source code, security reporting, app licensing, and third-party artwork notices.
