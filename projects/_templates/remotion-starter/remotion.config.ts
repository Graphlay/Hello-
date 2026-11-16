// See all configuration options: https://remotion.dev/docs/config
// Each option also is available as a CLI flag: https://remotion.dev/docs/cli

// Note: When using the Node.JS APIs, the config file doesn't apply. Instead, pass options directly to the APIs

import { Config } from "@remotion/cli/config";

Config.setRspack(true);
Config.setVideoImageFormat("jpeg");
Config.setOverwriteOutput(true);

// Cloud workspace: Remotion's own browser download host is blocked here, so use the
// pre-installed Chrome Headless Shell when it exists. On your own computer this is skipped
// and Remotion downloads its browser automatically.
import fs from "node:fs";
const preinstalledShell = "/opt/pw-browsers/chromium_headless_shell-1243/chrome-headless-shell-linux64/chrome-headless-shell";
if (fs.existsSync(preinstalledShell)) {
  Config.setBrowserExecutable(preinstalledShell);
}
