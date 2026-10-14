# Samurai Scribe skills: the format

Spec version **1**. This is the contract a skill is written against: the file layout, the keys Samurai Scribe reads, and the tools a skill may tell the assistant to use. It is published as `SPEC.md` in the public skills repository (`samuraiscribe/skills`), and Samurai Scribe's own tests fail if the app's tools and the table below ever disagree.

## A skill is a folder

```
<skill-name>/
├── SKILL.md         required
├── examples/        optional: anything the instructions point to
└── references/
```

`SKILL.md` is the cross-tool [Agent Skills](https://agentskills.io) format: a YAML header between `---` lines, then the instructions in plain English (Markdown).

```markdown
---
name: meeting-prep-brief
description: Before a calendar meeting, writes a one-page brief from past meetings with the same people or on the same topic. Use it to get ready for a meeting.
metadata:
  accepts: "calendar_event, meeting"
  suggested_trigger: "before_meeting 15"
  category: "Preparation"
  tested_with: "local, cloud"
  version: "1.0"
  spec: "1"
---
Write a short brief for the meeting that is about to start.

1. Find earlier meetings about the same thing with search_meetings…
```

### Header

| Key | Required | Meaning |
|---|---|---|
| `name` | yes | Equal to the folder's name: lowercase letters, digits and single hyphens, at most 64 characters. |
| `description` | yes | What it does **and when to use it**, in one or two sentences. The assistant decides to use a skill from this line alone. |
| `metadata` | no | Samurai Scribe's settings, below. One level of `key: "value"` lines; values are quoted strings. |

Other top-level keys (`license`, …) and other `metadata` keys are allowed and kept exactly as written.

### `metadata` keys

| Key | Meaning |
|---|---|
| `accepts` | What the skill is run on, comma-separated, in the order the app offers them when someone runs it: `meeting` (a meeting in the vault, transcribed or not), `calendar_event` (a calendar meeting, usually one coming up; the run is told its title, time, attendees and invitation), `none` (nothing). `none` beside another word makes it optional: `"meeting, none"` runs on a meeting or on nothing. **Declare it**: without it the app guesses — a meeting if the skill has a `document` or suggests `after_meeting`, otherwise nothing. Words reserved for later: `notebook`, `note`, `folder`. The app skips a word it does not know, so a skill written for a newer version still runs; the repository's checks refuse one, so a typo fails its pull request. |
| `suggested_trigger` | When the author suggests running it. **Only a hint**: it prefills an automation the user may create. Installing a skill never makes it run by itself. Values: `after_meeting`; `before_meeting` or `before_meeting <minutes>`; `schedule <when>`, where `<when>` is `hourly`, `daily HH:MM`, `weekdays HH:MM` or a weekday and a time (`monday 09:00`), in the user's local time. |
| `requires` | Connections the skill needs, comma-separated **preset ids** from the repository's `connections/` folder (`linear`, `jira`), never a name a user gave their own connection. Until each is connected, the app shows the skill greyed out with a Connect button. |
| `tools` | The tools of those connections it uses, comma-separated as `<connection>__<tool>` (`linear__list_teams, linear__save_issue`). A run of the skill is offered only these of a connection it lists any of, not the service's other tools, and the app shows them before you install. Every connection tool the instructions name must be listed here. |
| `document` | When the skill runs as a step of a meeting's processing, the name of the document its reply is saved as (`Summary`, `Follow-up email`). |
| `category` | A short label for browsing: `Preparation`, `Follow-up`, `Review`, `Sales`, `Learning`… |
| `tested_with` | `local`, `cloud`, or `local, cloud`: which kinds of model it was checked on. A skill marked `local` was qualified on the app's built-in local model. |
| `version` | The author's own version of the skill. |
| `spec` | The version of this format it was written for: `"1"`. |

**What a run is given follows from when it runs.** An automation after a meeting hands the skill that meeting, one before a calendar meeting hands it that event, and one on a schedule hands it nothing — so `accepts` should name what each automation a skill suits will give it. The app warns, but does not refuse, an automation that hands a skill something it does not say it accepts.

A meeting may not be transcribed yet: it can still have notes, documents, a calendar event, or a recording under way. A run on a meeting is told what the meeting holds, and a skill that cannot work without a transcript should check and say so ("If the meeting has no transcript yet, say so in one line and stop.").

**When a skill runs is never in the skill.** It runs when the user runs it, when its description fits what they ask the assistant, or when one of the user's own **automations** says so: after meetings, before calendar meetings, or on a schedule. An automation belongs to the user because "only meetings titled *Acme*" means something in one calendar and nothing in another.

Skills written before automations existed carried `trigger`, `schedule`, `minutes_before` and `title_contains` in `metadata`. The app turns those into automations once, keeps them in the file, and does not act on them again. Do not use them in new skills.

## Instructions

Write the steps the assistant should follow, naming the tools it should use. Small local models follow short numbered steps far better than prose. Say what the output must look like, and what to do when the material is not there ("If there are none, say so in one line and stop.").

What a skill writes outside the meeting it runs on, it **proposes**: notes, edits and new notebooks wait for the user's review when nobody was watching the run. Inside a meeting's processing, `write_document` and the reply itself are written directly.

## Tools

A skill may name these tools. Where it runs decides which are offered:

- **Chat**: the in-app assistant, whether the user ran the skill or an automation did.
- **AI apps**: Claude Desktop, Claude Code, Codex, Cursor and other MCP clients connected to Samurai Scribe.
- **Processing step**: the skill as a step of a meeting's processing profile.

| Tool | Chat | AI apps | Processing step | What it does |
|---|:-:|:-:|:-:|---|
| `search_meetings` | ✓ | ✓ | ✓ | Search transcripts, titles and documents; returns lines with meeting ids and times. |
| `list_meetings` | ✓ | ✓ |  | Meetings by date or title, newest first. |
| `upcoming_meetings` | ✓ | ✓ |  | Calendar meetings ahead, with attendees, linked to their meeting if one exists. |
| `get_meeting` | ✓ | ✓ |  | One meeting: title, date, speakers, its documents and folder. |
| `read_transcript` | ✓ | ✓ | ✓ | A meeting's transcript, a window at a time (`from_seconds`). |
| `digest_transcript` | ✓ |  | ✓ | Reads a whole meeting for one instruction and returns the notes; the way to read a long meeting on a small model. |
| `read_document` | ✓ | ✓ | ✓ | A meeting's document: `Summary`, `Notes`, or one the user attached. |
| `search_notes` | ✓ | ✓ |  | Search the user's notes outside meetings. |
| `list_folder` | ✓ | ✓ |  | What a folder holds. |
| `read_note` | ✓ | ✓ |  | A note's text. |
| `create_note` | ✓ | ✓ |  | Propose a new note. |
| `edit_note` | ✓ | ✓ |  | Propose changes to a note. |
| `move_note` | ✓ | ✓ |  | Propose moving a note. |
| `delete_note` | ✓ | ✓ |  | Propose moving a note to the trash. |
| `list_notebooks` | ✓ | ✓ |  | The user's notebooks and the meetings in each. |
| `create_notebook` | ✓ | ✓ |  | Propose a notebook. |
| `add_to_notebook` | ✓ | ✓ |  | Propose adding meetings to a notebook. |
| `list_skills` | ✓ | ✓ |  | The user's skills. |
| `use_skill` | ✓ | ✓ |  | Another skill's instructions. |
| `create_skill` | ✓ | ✓ |  | Propose a new skill. |
| `check_change` | ✓ | ✓ |  | Whether a proposed change was kept. |
| `read_memory` | ✓ | ✓ |  | What the user asked the assistant to remember about them. |
| `remember` | ✓ |  |  | Propose a line for that memory. |
| `edit_memory` | ✓ |  |  | Propose changes to that memory. |
| `write_document` |  |  | ✓ | Write a document into the meeting being processed. |
| `set_title` |  |  | ✓ | Name the meeting being processed. |

A skill meant for both the app and AI apps should read meetings with `read_transcript`, not `digest_transcript`. A connection's tools (once connected) are named `<connection>__<tool>`; a skill that uses them lists the connection in `requires` and the tools in `tools`, and its runs are offered only those.

Tool names do not change. If one is ever renamed, its old name keeps working.

## Connections (the repository's `connections/` folder)

A connection is an address, not code: the service runs its own MCP server, and the app connects to it.

```
connections/<id>/
├── connection.json
├── logo.png          a square PNG, 128–1024 px, as the brand ships it
└── logo-dark.png     optional, for dark mode
```

```json
{
  "id": "example-tracker",
  "name": "Example Tracker",
  "url": "https://mcp.example-tracker.com/mcp",
  "auth": "oauth",
  "suggested": { "create_issue": "ask" }
}
```

| Key | Meaning |
|---|---|
| `id` | Equal to the folder's name. What skills put in `requires`. |
| `name` | As the service writes its own name. |
| `url` | The service's own remote MCP server. |
| `auth` | `oauth` (the user signs in on the service's page) or `api_key` (the user pastes a key). |
| `client_id` | Only for a service that does not let apps register themselves: Samurai Scribe's public OAuth client id there. |
| `suggested` | Starting permissions for named tools: `allow` or `ask`. Any tool not named starts at Allow if the server marks it read-only, else Ask. A preset can never start a tool at "allow in automatic runs". |

Only services with an official remote MCP server are listed. Logos are used to name the service, following its brand guidelines.
