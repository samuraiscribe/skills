# Samurai Scribe skills

Skills for [Samurai Scribe](https://samuraiscribe.com), the private, local meeting notetaker: plain-English instructions its assistant follows to do something useful with your meetings — prepare you for the next one, keep a decision log, track your action items, review your week.

A skill is just a folder with a `SKILL.md` in the open [Agent Skills](https://agentskills.io) format, so you can read every word of what it will do before you use it. Skills run on your own computer, on the model you chose; nothing here sends your meetings anywhere.

## The skills

| Skill | What it does | Suggested to run |
|---|---|---|
| [meeting-prep-brief](skills/meeting-prep-brief/SKILL.md) | A one-page brief before a meeting, from earlier meetings with the same people or on the same topic | 15 min before calendar meetings |
| [weekly-review](skills/weekly-review/SKILL.md) | The past seven days of meetings in one note: decisions, open items, loose ends | Mondays at 09:00 |
| [my-action-items](skills/my-action-items/SKILL.md) | Everything you committed to in the last two weeks, in one list | Weekday mornings |
| [one-on-one-tracker](skills/one-on-one-tracker/SKILL.md) | Adds each 1:1 to a running note per person | After 1:1s |
| [decision-log](skills/decision-log/SKILL.md) | Adds each meeting's decisions to one running log | After meetings |
| [sales-call-notes](skills/sales-call-notes/SKILL.md) | Pain, decision maker, budget, timeline, objections, next step | After sales calls |
| [lecture-study-guide](skills/lecture-study-guide/SKILL.md) | Concepts, definitions, examples and practice questions from a lecture | By hand |

## Install one

Copy the skill's folder into your vault's **Skills** folder (the one beside `Meetings/`). It appears in **Skills & Tools** at once.

A skill never runs by itself because you installed it. Run it from Skills & Tools or the assistant, or give it an **automation** — after meetings, before calendar meetings, or on a schedule — in Skills & Tools → Automations. The "Suggested to run" column is only a suggestion for that.

One-click install from inside the app is on its way.

## Connections

`connections/` will list services a skill can act in — Jira, Linear, Notion and others — as small address files. A connection is not code: each service runs its own server, and Samurai Scribe signs in to it with your permission. See [SPEC.md](SPEC.md#connections-the-repositorys-connections-folder).

## Make your own

Write it in Samurai Scribe (Skills & Tools → New Skill), try it on a few meetings, then open a pull request here. [CONTRIBUTING.md](CONTRIBUTING.md) says how; [SPEC.md](SPEC.md) is the format.

## License

MIT. See [LICENSE](LICENSE).

## Drafts

[`drafts/`](drafts/) holds skills that are not published yet because they do not
pass on the app's built-in local model. They are not in the app's list. Improving
one until it passes is a welcome first contribution: see [CONTRIBUTING.md](CONTRIBUTING.md).
