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
