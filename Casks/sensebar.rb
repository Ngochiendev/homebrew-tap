cask "sensebar" do
  version "1.4.0"
  sha256 "ffa2299300d6458526c8a6fcdd31c5cde9f5a1ac7ad4c371d66dd45900990e89"

  url "https://github.com/Ngochiendev/SenseBar/releases/download/v#{version}/SenseBar-v#{version}-macOS-Universal.dmg"
  name "SenseBar"
  desc "Dynamic Island, presentation mode, and per-app audio controls"
  homepage "https://sensebar.site/"

  livecheck do
    url :url
    strategy :github_latest
  end

  auto_updates true
  depends_on macos: ">= :sonoma"

  app "SenseBar.app"

  zap trash: [
    "~/Library/Caches/com.sensebar.SenseBar",
    "~/Library/Preferences/com.sensebar.SenseBar.plist",
    "~/Library/Saved Application State/com.sensebar.SenseBar.savedState",
  ]
end
