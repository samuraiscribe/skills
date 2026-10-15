# Drafts

Skills here are not published: they did not pass qualification on Samurai
Scribe's built-in local model (Qwen 3.5 4B), and nothing is shipped untested.
The app never lists them.

| Skill | What goes wrong on the local model |
|---|---|
| *(none waiting)* | follow-up-email passed in October 2026 once the app kept a draft that could not be sent as it stands from reaching the user (`draft_email` refuses placeholders, transcript labels, empty sections, the user's own address and addresses not invited). |

These were written for the connections added in October 2026 and have not run
against a live account yet. Each tool name comes from the service's own source
or documentation; the arguments marked in each still need a real `tools/list`.

| Skill | What is not yet known |
|---|---|
| [action-items-to-todoist](action-items-to-todoist/SKILL.md) | Nothing beyond qualification: tool names and fields are from Doist's own source. |
| [action-items-to-monday](action-items-to-monday/SKILL.md) | Whether the hosted server offers the same tools as monday's open-source one. |
| [action-items-to-clickup](action-items-to-clickup/SKILL.md) | The task tool's field names beyond `name` and the list id. |
| [meeting-notes-to-notion](meeting-notes-to-notion/SKILL.md) | Where a page with no `parent` lands. |
| [call-notes-to-attio](call-notes-to-attio/SKILL.md) | The search, note and task tools' argument names: Attio documents only the tool names. |

Calendly was tried and taken out: its server lets apps register, then refuses
any sign-in that returns to `http://127.0.0.1`, which is how every desktop
sign-in returns (`scripts/check_connections.py --register` shows it). It needs
an https return address — a page on `hub.samuraiscribe.com` that hands the
browser back to the app — before it can come back.

A Jira skill is waiting on one question: Atlassian's v2 address may offer two
general tools (`discover`, `execute`) rather than its own, unless asked for
`?tools=all`, and a skill can only list tools by name.

To move one to `skills/`, make it pass on short, medium and long meetings —
including one where it has nothing to report — and say what you tested in the
pull request.
