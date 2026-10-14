---
name: meeting-notes-to-notion
description: Puts a meeting's notes in Notion as a new page — the summary, decisions and action items, titled with the meeting and its date. Use it after a meeting your team keeps notes on in Notion.
metadata:
  accepts: "meeting"
  requires: "notion"
  tools: "notion__notion-create-pages"
  suggested_trigger: "after_meeting"
  category: "Follow-up"
  version: "0.1"
  spec: "1"
---
Put this meeting's notes in Notion as one new page.

1. Get the meeting with get_meeting: note its title and date.
2. Read its Summary with read_document.
   - If it has no Summary, reply "This meeting has no summary yet — process it first." and stop. Do not call any Notion tool.
3. Call notion__notion-create-pages once, with `pages` holding one page:
   - properties: `{"title": "<meeting title> — <date>"}`
   - content: the Summary, as Markdown, exactly as it is. Then a last line: `From Samurai Scribe.`
   Leave `parent` out: the page goes in the user's own private pages, where they can move it.
4. Reply in one line with the page's title and its link, if Notion gave one.

Rules:
- Copy the Summary; do not rewrite it, shorten it or add to it.
- One page, created once.
