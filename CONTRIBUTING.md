# Contributing

Thank you for sharing a skill. Here is how to get one merged.

## Adding a skill

1. **Write it in the app.** In Samurai Scribe, Skills & Tools → New Skill. Give it a clear description: the assistant decides to use a skill from that line alone.
2. **Try it** on at least three real meetings of different lengths, from Skills & Tools (▶). Read what it produced. Fix the instructions until it is right every time.
3. **Copy its folder** from your vault's `Skills/` into `skills/` here, and open a pull request.

The pull request is checked automatically (`scripts/validate.py`): the folder name, the header, that every tool it names exists, and its size. You can run the same check first:

```bash
python3 scripts/validate.py
```

### What makes a good skill

- **Short, numbered steps** that name the tools to use. Small local models follow these far better than paragraphs.
- **Say what the output looks like**: the sections, the format of a line, roughly how long.
- **Say what to do when the material is not there**: "If there are none, say so in one line and stop."
- **"Use only what was said"**. A skill that invents a decision or a date is worse than none.
- **Portable**: nothing about your own vault. No folder names you made, no people's names, no client names, no email addresses. Use the tools to find things instead.
- **When it runs is not in the skill.** You may add `suggested_trigger` (see SPEC.md); the user decides.
- **Say what it runs on** with `accepts` (required here): `meeting`, `calendar_event`, `none`, or a list such as `meeting, none` when a meeting is optional. The app's editor sets it under **Runs on**, and running the skill offers exactly these. Name only what the instructions handle: a skill that reads a meeting's Summary does not accept `none`.

### `tested_with`

Say which models you checked it on: `local` for Samurai Scribe's built-in local model, `cloud` for a hosted one. Only claim `local` if it worked on the built-in model on short, medium and long meetings. That model is small, and people choosing a skill rely on this.

## Adding a connection

Only services that run their **own official remote MCP server** are listed, so that nothing here makes someone's computer download and run code.

```
connections/<id>/
├── connection.json
├── logo.png          the service's own logo: a square PNG, 128–1024 px, unaltered
└── logo-dark.png     optional
```

`connection.json` needs a one-line `description` of what the service is for beside meetings and a `category` (see SPEC.md). In the pull request, link the service's documentation for its MCP server. Use the logo as the service's brand guidelines allow; it is there only to name the service.

The app signs in with no account of its own at the service, so the service's sign-in must let apps register themselves (OAuth dynamic client registration). Check it before opening the pull request; the pull request runs the same check:

```
python3 scripts/check_connections.py <id>
```

Every connection should have at least one skill that uses it.

## Review

A maintainer reads every skill before it is merged, the way a user should before they run it: a skill is instructions an AI will follow with access to someone's meetings. Expect questions.

By opening a pull request you agree that your contribution is licensed under the repository's MIT license.
