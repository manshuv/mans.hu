# manshuverma.com

This repository is the source for [manshuverma.com](https://manshuverma.com), a small static site made from plain HTML, CSS, and a little JavaScript. The goal is to keep the site simple enough to understand and edit by hand, while still letting individual pages host interactive HTML/CSS/JS experiments.

## What This Setup Uses

- **Domain registrar:** Squarespace
- **Hosting and edge delivery:** Cloudflare Workers
- **Source hosting:** GitHub
- **Design exploration:** Claude Design, using [nytimes.com](https://www.nytimes.com) as a visual reference
- **Initial implementation:** Claude Code
- **Final configuration and hardening:** Codex, especially its in-browser control for Cloudflare and GitHub settings

## Why This Shape Works

This is intentionally not a heavy app stack. There is no database, framework, CMS, or build pipeline required to understand the site. Each page can be a self-contained HTML document with its own CSS and JavaScript.

That makes the site useful for writing, demos, and interactive essays. A post can be mostly text, but it can also include small tools, cards, animations, calculators, visual maps, or other browser-native elements without needing a separate app.

## How To Replicate It

1. Register a domain.
   This site uses Squarespace as the registrar.

2. Move DNS control to Cloudflare.
   In Squarespace, set the domain nameservers to the Cloudflare nameservers for the zone.

3. Put the site source in GitHub.
   Keep the public site files in the repository. This repo uses simple top-level HTML files and a `posts/` directory.

4. Host with Cloudflare Workers.
   Connect the GitHub repository to Cloudflare Workers and deploy the static site from the repo.

5. Add custom domains in Cloudflare.
   Attach both the apex domain and `www` domain to the Worker:
   - `manshuverma.com`
   - `www.manshuverma.com`

6. Protect `main` in GitHub.
   Add a ruleset for the `main` branch that requires pull requests before merging, blocks force pushes, and prevents branch deletion.

## The Solo Maintainer Gotcha

If you are the only contributor, do not require one approving review unless someone else has write access.

GitHub does not let the PR author approve their own PR for the purpose of satisfying required review rules. That means this combination creates a catch-22:

- PRs are required to merge into `main`.
- One approval is required.
- You are the only person with write access.
- You cannot approve your own PR.

For a solo-maintainer setup, the better rule is:

- Require pull requests before merging.
- Set required approvals to `0`.
- Keep force-push and deletion protections enabled.

That still prevents direct pushes to `main`, but lets you merge your own PRs after the checks pass. If you later add collaborators, raise required approvals to `1` and decide who is trusted to approve changes.

## Tool Notes

Claude Design worked well for the visual direction once it had a concrete reference site. Giving it [nytimes.com](https://www.nytimes.com) as an example made the desired editorial feel much easier to communicate than describing the style from scratch.

Claude Code worked well for the initial build-out: creating the site structure, translating the design direction into HTML and CSS, and getting the first version running.

Codex was especially useful for the final setup because it could operate the browser directly. That mattered for Cloudflare DNS/custom-domain configuration and GitHub repository security settings, where the work is not just code edits but clicking through real dashboards, verifying state, and fixing configuration mistakes.

## Editing The Site

Most content lives in plain HTML files:

- `index.html` controls the home page.
- `about.html` controls the about page.
- `posts/` contains individual posts.

You can edit these files in any IDE or text editor. Posts can include their own CSS and JavaScript directly in the page when they need interactive elements.

## Email subscriptions and comments

The site supports Buttondown email subscriptions and Hyvor Talk comments without
adding a database or framework. Both are **off until configured**; visitors never
see a signup form pointing at a placeholder account. RSS works independently.

### Activate Buttondown

1. Create your newsletter at https://buttondown.com and complete email verification.
2. Set `buttondownUsername` in `community-config.js` to your public
   newsletter username (not your email address or API key).
3. Configure your sender identity and welcome message in Buttondown. Keep
   subscriber confirmation enabled. Publish the configuration through a PR.
4. Test with your own email: subscribe, complete confirmation, check the subscriber
   dashboard, send a test email, and verify unsubscribe works.
5. For automatic new-post emails, activate RSS-to-email in Buttondown and set its
   feed URL to `https://manshuverma.com/feed.xml`. Confirm current pricing before
   activating. **Check how existing feed items are handled before enabling sends**
   so your archive does not unexpectedly email new subscribers. Choose your cadence.

The standard HTML form submits directly to Buttondown so verification and CAPTCHA
flows work. Email addresses are never stored in the public repository. No API keys
are required by this integration. Automatic delivery requires the provider setup;
a working signup form alone does not enable it.

### Activate Hyvor Talk

1. Create an account at https://hyvor.com/talk and add `manshuverma.com` as a website.
2. Copy the numeric website ID from Console → Settings → Website into
   `hyvorWebsiteId` in `community-config.js`.
3. Enable guest commenting and pre-moderation in the Hyvor console, set up moderator
   notifications, and activate the appropriate plan when ready.
4. Publish through a PR. On a live post, load comments, submit a test comment,
   approve it from the console, and verify a reply notification.

Comment threads use each post's original filename stem as a permanent page ID.
Do not change an existing `data-page-id` when renaming a post. This keeps `.html`
and extensionless URLs attached to the same discussion. The third-party embed
loads only when a reader presses “Load comments.” If blocked, readers see retry
or content-blocker guidance. Turning either config value back to empty hides that
feature without deleting subscribers or comments at the provider.

### Publishing another article

Copy the community sections and the two deferred scripts from an existing post.
Use a unique, permanent `data-page-id` for the new article. Keep the newsletter
heading and input IDs unique within each page. New posts must have a filename
starting with `YYYY-MM-DD-`, a title, and a description meta tag.

After adding a post, run:

```sh
python3 generate-feed.py
```

Commit `feed.xml` with the new post. It contains dated summaries and links rather
than interactive HTML/scripts, so email readers return to the website for the full
experience. Existing GUIDs and publication dates must stay stable to avoid repeat
emails. The home page and each post advertise the feed to RSS readers.

### Verification limits

The initial integration can be checked locally with test public identifiers,
without submitting addresses or loading a real comments account. Live subscription,
email delivery, unsubscribe, and comment moderation require the owner's configured
accounts and must be verified after activation.
