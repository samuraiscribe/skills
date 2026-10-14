# Samurai Scribe skills

This repo holds the skills and connections you can add from the Skills page in [Samurai Scribe](https://samuraiscribe.com).

- A **skill** is a set of instructions the app's assistant follows to do something with your meetings, like writing a prep brief before a call or keeping a log of decisions. Each one is a folder with a `SKILL.md` file in the [Agent Skills](https://agentskills.io) format. It's plain text, so you can read exactly what a skill will do before you install it.
- A **connection** lets a skill work in another service, like creating issues in Linear. A connection is only an address, not code. The service runs its own MCP server, and the app signs in to it once you approve.

Skills run on your computer with whatever model you've picked in the app. Nothing leaves your machine unless a skill uses a connection.

## Skills

| Skill | What it does | Suggested schedule |
|---|---|---|
| [meeting-prep-brief](skills/meeting-prep-brief/SKILL.md) | A one-page brief before a meeting, based on earlier meetings with the same people or on the same topic | 15 min before calendar meetings |
| [weekly-review](skills/weekly-review/SKILL.md) | One note covering the past week of meetings: decisions, open items, loose ends | Mondays at 09:00 |
| [my-action-items](skills/my-action-items/SKILL.md) | Everything you committed to in the last two weeks, in one list | Weekday mornings |
| [one-on-one-tracker](skills/one-on-one-tracker/SKILL.md) | Adds each 1:1 to a running note for that person | After 1:1s |
| [decision-log](skills/decision-log/SKILL.md) | Adds each meeting's decisions to a running log | After meetings |
| [sales-call-notes](skills/sales-call-notes/SKILL.md) | Pain points, decision maker, budget, timeline, objections and next step | After sales calls |
| [lecture-study-guide](skills/lecture-study-guide/SKILL.md) | Concepts, definitions, examples and practice questions from a lecture | Manually |
| [action-items-to-linear](skills/action-items-to-linear/SKILL.md) | Creates a Linear issue for each action item in a meeting (needs the Linear connection) | After meetings |

## Connections

| Connection | What it's for |
|---|---|
| [Linear](connections/linear/connection.json) | Turn a meeting's action items into Linear issues |
| [Jira & Confluence](connections/atlassian/connection.json) | File action items as Jira issues and keep meeting notes in Confluence |
| [Notion](connections/notion/connection.json) | Keep meeting notes, decisions and summaries in your Notion workspace |
| [Todoist](connections/todoist/connection.json) | Send a meeting's action items to your Todoist inbox or a project |
| [monday.com](connections/monday/connection.json) | Add a meeting's action items to a monday.com board |
| [ClickUp](connections/clickup/connection.json) | Turn a meeting's action items into ClickUp tasks |
| [Attio](connections/attio/connection.json) | Log call notes and follow-up tasks on the right Attio records |

The Linear skill is published. Skills for most of the other services are still in [`drafts/`](drafts/).

## Installing

Open the Skills page in Samurai Scribe. Skills from this repo are listed below your own. Click one to read it, then press Install. The app checks the files against what's published here, and lets you know when an installed skill has an update. You can also copy a skill's folder into the Skills folder in your vault (next to `Meetings/`).

Connections are on the Connections tab of the same page. When you open a skill that needs one, it says so and offers a button to connect.

Installing a skill doesn't make it run. You can run it yourself from the Skills page or the assistant, or set up an automation under Skills → Automations to run it after meetings, before calendar events or on a schedule. The suggested schedule in the table is only a starting point.

## Writing your own

Create the skill in the app (Skills → New Skill) and try it on a few meetings. When it works well, open a pull request. [CONTRIBUTING.md](CONTRIBUTING.md) explains the process for skills and connections, and [SPEC.md](SPEC.md) describes the format.

## Drafts

[`drafts/`](drafts/) has skills that aren't published yet because they don't work reliably on the app's built-in local model, so the app doesn't list them. Getting one of them to pass is a good first contribution.

## License

MIT. See [LICENSE](LICENSE).
