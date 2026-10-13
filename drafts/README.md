# Drafts

Skills here are not published: they did not pass qualification on Samurai
Scribe's built-in local model (Qwen 3.5 4B), and nothing is shipped untested.
The app never lists them.

| Skill | What goes wrong on the local model |
|---|---|
| [follow-up-email](follow-up-email/SKILL.md) | On a meeting where nothing was decided or assigned, it invents decisions and tasks (and a `[date]` placeholder) rather than leaving those sections out; it sometimes signs the email. Fine on meetings with clear decisions. |

To move one to `skills/`, make it pass on short, medium and long meetings —
including one where it has nothing to report — and say what you tested in the
pull request.
