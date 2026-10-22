# Contributing to Sidely

Thanks for helping with Sidely! This is a small fork; the rules are simpler than upstream's.

## Building

1. Clone with submodules:
   ```sh
   git clone --recurse-submodules https://github.com/ThatRey/Sidely.git
   ```
2. Copy the signing sample and fill in your team:
   ```sh
   cp CodeSigning.xcconfig.sample CodeSigning.xcconfig
   ```
3. Open `AltStore.xcodeproj` (scheme: **Sidely**) or run:
   ```sh
   make build fakesign ipa
   ```

You need macOS with Xcode 26+.

## Pull requests

- Keep changes focused; avoid broad refactors in signing/pairing/networking code.
- Describe what you tested (device model + iOS version if relevant).
- If a change is meant for SideStore upstream, submit it there yourself as a human. Sidely does not relay AI-generated PRs, issues, or comments to SideStore.

## Branding changes

- Icons: edit `scripts/branding/generate_icons.py`, run it, and include the regenerated assets plus the preview sheet.
- Source/URL defaults: use the `Sidely*` keys in `AltStore/Info.plist` where possible.
- Keep the AGPLv3 license and original copyright notices.

## Licensing

By contributing, you agree that your contributions are licensed under AGPLv3. See [LICENSE](LICENSE) and [NOTICE.md](NOTICE.md).
