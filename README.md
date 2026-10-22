# Sidely

> A community fork of [SideStore](https://github.com/SideStore/SideStore) with a fresh identity, configurable sources, and small quality-of-life improvements.

Sidely is an iOS app store and sideloading client for non-jailbroken devices. It signs and installs apps with your own Apple ID, uses an on-device VPN loopback to install them without a computer, and refreshes them in the background before the 7-day free-developer certificate expires.

Sidely is **not affiliated with or endorsed by the SideStore project**. It is a fork of SideStore, which itself is a fork of [AltStore](https://github.com/rileytestut/AltStore).

## What's different in Sidely?

- **New identity** — Sidely app name, bundle IDs (`com.sidely.Sidely`), URL scheme (`sidely://`), accent color, and a fully regenerated icon pack with 12 color variants.
- **Editable icon pipeline** — `scripts/branding/generate_icons.py` renders every icon size and alternate icon from one geometry definition. Change the palette table, run the script, and the whole icon pack updates.
- **Configurable source defaults** — point Sidely at your own source list without touching Swift:
  `SidelyDefaultSourcesURL`, `SidelyCommunitySourceURL`, `SidelyFallbackIconURL`, `SidelyWebsiteURL`, `SidelyGitHubURL`, `SidelyIssuesURL`, and `SidelySupportEmail` in `AltStore/Info.plist`.
- **Quality-of-life additions** — copy an app's bundle identifier or version straight from its context menu in *My Apps*.
- **Fork-friendly CI** — a single GitHub Actions workflow builds an unsigned/fakesigned `Sidely.ipa` on every push to `main`/`sidely` and on demand. Free for public repositories.

Everything else — signing, pairing, refresh, backups, widgets — is inherited from SideStore.

## Requirements

- iOS 15+
- Xcode 26+ and macOS to build the app
- Rustup (`brew install rustup`) for the bundled dependency build

## Building

```sh
git clone --recurse-submodules https://github.com/ThatRey/Sidely.git
cd Sidely
cp CodeSigning.xcconfig.sample CodeSigning.xcconfig   # set DEVELOPMENT_TEAM / signing
open AltStore.xcodeproj
```

Command-line build:

```sh
make build fakesign ipa     # produces Sidely.ipa
```

The GitHub Actions workflow in `.github/workflows/build.yml` does the same on a macOS runner.

### Building without a Mac

Push the repository to GitHub and run **Actions → Build Sidely IPA → Run workflow**, then download the `Sidely-unsigned-ipa` artifact. The IPA is fakesigned and must be installed/resigned through Sidely (or another signing tool) with your Apple ID.

## Rebranding / icons

The icon artwork uses a simple download-into-tray mark on a diagonal gradient. To restyle it:

1. Edit `PALETTES` (or the glyph geometry) in `scripts/branding/generate_icons.py`.
2. Run `python3 scripts/branding/generate_icons.py`.
3. Open `branding/SidelyIcon-preview.png` to review all variants.
4. Build — the script writes every `AppIcon.appiconset` size, all alternate icon sets, the in-app logo, and the widget badge.

Alternate icons are exposed in **Settings → Change App Icon**.

## News feed

The built-in news feed lives in [`source/sidely.json`](source/sidely.json) and is fetched from GitHub. To post an update:

1. Edit the `news` array in `source/sidely.json`.
2. Push to `main` (the file is served from `raw.githubusercontent.com`, so no build is required).
3. Sidely picks it up on the next source refresh.

Each post needs `identifier`, `title`, `caption`, `date`, and `tintColor`. See [`source/README.md`](source/README.md) for the full schema.

## Project layout

| Path | Purpose |
| --- | --- |
| `AltStore/` | Main app target: UI, browsing, My Apps, settings |
| `SideStore/` | SideStore/Sidely-specific logic (boot, refresh, device APIs) |
| `SideBackup/` | Backup helper app |
| `AltWidget/` | Widget extension |
| `Shared/` | Shared utilities |
| `Dependencies/` | Git submodules: `minimuxer`, `SideSign` |
| `scripts/branding/` | Icon generator |
| `branding/` | Generated icon masters and preview sheet |

## Upstream relationship and contributing

Sidely tracks SideStore's `develop` branch. Fixes that belong upstream should be proposed to [SideStore](https://github.com/SideStore/SideStore) by a human, following the rules in SideStore's `AGENTS.md` at the time (SideStore does not accept AI-generated pull requests, issues, or comments). Do not send AI-authored PRs to SideStore.

For this fork, see [CONTRIBUTING.md](CONTRIBUTING.md).

## Credits

Sidely is built on the work of the SideStore and AltStore communities:

- [SideStore](https://github.com/SideStore/SideStore) — the upstream project this fork is based on
- [AltStore](https://github.com/rileytestut/AltStore) — SideStore's upstream
- [minimuxer](https://github.com/jkcoxson/minimuxer), [em_proxy](https://github.com/jkcoxson/em_proxy), [SideSign](https://github.com/SideStore/SideSign), and [Roxas](https://github.com/rileytestut/roxas)

See [NOTICE.md](NOTICE.md) for licensing details.

## License

AGPLv3. See [LICENSE](LICENSE). Sidely is a modified version of SideStore; the original copyright notices are retained.
