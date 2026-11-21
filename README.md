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

After publishing an app release, update `version` and the DMG `sha256` in `Casks/sensebar.rb`. Verify the checksum against the release's `SHA256SUMS.txt`, then run Homebrew style and audit checks before pushing. The cask uses the immutable versioned GitHub Release URL; do not replace the archive bytes for an existing version.

This is the project's own tap, separate from the Homebrew-maintained `homebrew/cask` repository. See [SenseBar](https://github.com/Ngochiendev/SenseBar) for source code, security reporting, app licensing, and third-party artwork notices.
