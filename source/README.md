# Sidely source & news

`sidely.json` is the built-in source that Sidely fetches for project news.

- Edit the `news` array to add or change posts.
- Each post needs `identifier`, `title`, `caption`, `date`, and `tintColor`.
- `date` accepts `YYYY-MM-DD` or a full ISO 8601 timestamp.
- `url` is opened when the post is tapped; `imageURL` is optional.
- Add `"notify": true` to a post if it should also trigger a local notification.
- The `identifier` field at the top becomes the source group ID. Do not change it
  unless you also change `SidelyCommunitySourceURL`.

After editing, push to `main`. Sidely refreshes the source on launch, so users
receive the new post the next time they open the app.

## Anisette servers

`anisette-servers.json` is the catalog Sidely reads in remote-Anisette mode. It
currently lists the local Windows/WSL server:

- `http://192.168.2.107:6969` (LAN IP)
- `http://DESKTOP-O3DTEIE.local:6969` (mDNS fallback)

The `defaultSource` in `SideStore/AppConstants.swift` points at this file. If the
PC's IP or hostname changes, update this file and rebuild Sidely; the app also
uses `defaultServerURL` from `AppConstants.swift` as a fallback when the catalog
has not synced yet.

To use it, turn off **On-Device Anisette** under
**Settings → Advanced → User Customizations**, then select a local server under
**Settings → Advanced → Anisette Servers**.
