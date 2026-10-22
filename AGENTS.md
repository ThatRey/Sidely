# Agent Guidelines for Sidely

Sidely is a **fork** of [SideStore](https://github.com/SideStore/SideStore). It sideloads and refreshes iOS apps on-device with a personal Apple ID using a local VPN loopback (`em_proxy` + `minimuxer`) instead of a computer. The internals use Swift Concurrency.

## Scope of this fork

- The app is branded **Sidely**. Bundle IDs live under `com.sidely`, the URL scheme is `sidely://`, and the Swift module name intentionally remains `SideStore` so storyboards and `@testable import SideStore` keep working.
- Upstream service endpoints (`sidestore.io`, `ani.sidestore.io`, `servers.sidestore.io`) are still used for anisette and the default source list because Sidely does not host its own infrastructure. They are centralized in `SideStore/SidelyConfig.swift` and can be overridden from `AltStore/Info.plist`.
- Do not change signing, pairing, installation, or networking behavior unless the task explicitly requires it. These paths have device-specific edge cases across iOS versions.

## Project structure

- `AltStore/` — main iOS app target: UI, browse, My Apps, settings, permissions.
- `SideStore/` — Sidely/SideStore-specific logic: boot, maintenance, device APIs, theme, config.
- `SideBackup/` — backup helper target.
- `AltWidget/` — widget extension.
- `Shared/` — shared utilities and extensions.
- `Dependencies/` — git submodules (`minimuxer`, `SideSign`), managed as local Swift packages.
- `scripts/branding/generate_icons.py` — regenerates the entire icon pack.
- `.github/workflows/build.yml` — CI build of an unsigned/fakesigned `Sidely.ipa`.

## Building

Requires macOS + Xcode 26+.

```sh
git clone --recurse-submodules <repo>
cp CodeSigning.xcconfig.sample CodeSigning.xcconfig
open AltStore.xcodeproj
```

CLI:

```sh
make build fakesign ipa   # Sidely.ipa
```

The Xcode scheme is named `Sidely`; the target and Swift module are still named `SideStore`.

## Branding

- App name / bundle IDs: `Build.xcconfig`.
- User-facing URLs and source defaults: `SideStore/SidelyConfig.swift` + Info.plist keys prefixed `Sidely`.
- Colors: `AltStore/Core/Resources/Colors.xcassets/Primary.colorset`, `GradientTop/Bottom`.
- Icons: edit `scripts/branding/generate_icons.py`, run it, review `branding/SidelyIcon-preview.png`.
- Alternate icons are listed in `AltStore/Resources/AltIcons.plist` and exposed through the existing icon picker.

## Formatting

- Swift: 4 spaces, UTF-8, LF.
- Modern Swift Concurrency (`async`/`await`, `Task`, actors) over GCD.
- Makefiles: tabs only.
- Match surrounding style; don't reformat unrelated lines.

## Safety rules

- Never commit pairing files, certificates, private keys, anisette data, Apple IDs, passwords, device UDIDs, or GitHub tokens.
- Do not add secrets to `Build.xcconfig` or `CodeSigning.xcconfig`; those files are ignored or local-only.
- Keep AGPLv3 headers and copyright notices intact.

## Upstream contributions

Sidely is not SideStore. If a change is intended for SideStore itself, a **human** must submit it following SideStore's own `AGENTS.md`: SideStore does not accept AI-generated pull requests, issues, discussions, commit messages, or review replies. Do not use GitHub automation to post to the SideStore repository.
