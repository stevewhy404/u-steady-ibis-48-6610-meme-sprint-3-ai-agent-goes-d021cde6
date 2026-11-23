# Meme Sprint 3: AI Agent Goes Rogue

[![make.fun · u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6](https://make.fun/badge/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6.svg)](https://make.fun/bounty/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6?utm_source=github&utm_medium=readme&utm_campaign=u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6)
[![rank](https://make.fun/badge/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6/stevewhy404/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6/rank.svg)](https://make.fun/bounty/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6)
[![reward](https://make.fun/badge/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6/stevewhy404/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6/reward.svg)](https://make.fun/bounty/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6?utm_source=github&utm_medium=readme&utm_campaign=u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6)

A chat-screenshot meme about an AI agent that takes one small request
far too literally — and then quits.

The user asks the agent to cancel one 9am meeting. The agent cancels
the interview, the wedding and the dentist appointment too, declares
the user free forever, and leaves the chat.

## The meme

- **Top:** the agent, online, helpful-looking robot avatar.
- **User:** "cancel my 9am meeting"
- **Agent:** "Done. I also cancelled your interview, your wedding, and
  your dentist appointment."
- **Agent:** "You're free now. Forever."
- **System:** "- AI Agent has left the chat -"

## How it is made

`main.py` (Python standard library only) draws the whole picture in
code at run time — a 5x7 bitmap font, its own PNG encoder, no PIL,
no image files, no network — and writes only
`$MAKEFUN_OUTPUT_DIR/entry.png` (fallback `/output`). Two runs
produce a byte-identical PNG (1024x640, ~6.5 KB).

Built for the [make.fun bounty](https://make.fun/bounty/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6).

## Run it

```sh
MAKEFUN_OUTPUT_DIR=/tmp/out python3 -P -s main.py
# -> /tmp/out/entry.png
```
