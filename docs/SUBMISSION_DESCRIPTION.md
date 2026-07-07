# ASI — Agent Solutions Inc.

**An AI consulting team for business owners who can't code.** It interviews you about your company, shows where an agent pays off first, and hands you a build plan any coding agent can execute — built for Vietnam's SMEs, where the owner runs everything and consultants cost too much.

## The problem

- SME owners decide where AI goes. Most aren't technical.
- Hype tells them "agents will change everything" — never *where*.
- They can't describe what to build, so vibe coding fails.
- Real discovery work costs consulting money they don't have.

## 💡 What it does

- **Interviews like a consultant.** Plain-language discovery fills a structured checklist.
- **Answers side questions mid-interview** via a docs-grounded RAG agent. Reads uploaded files too.
- **Writes a value report:** value-vs-complexity table, process charts, one recommended starting point.
- **Drafts an 8-section build plan** — paste it into Antigravity, Claude Code, or Cursor and get a working agent.

## 🔧 Under the hood

- 5 ADK `LlmAgent`s + 5 code nodes on a 20-edge graph `Workflow`.
- RAG agent uses Google's official Developer Knowledge MCP server.
- Self-repairing quality gate: 10 deterministic checks, targeted feedback, max 2 retries.
- LLM decides, code routes — Pydantic schemas make unroutable events impossible.
- Prompt-injection hardening: tagged input, hardened prompts, adversarial eval dataset.
- Scaffolded, run, evaluated, and deployed with agents-cli.

## 🏆 Why it stands out

- The output isn't a slide deck — a coding agent executes it verbatim.
- Deterministic code validates every LLM output before it ships.
- Tested with simulated clients (Claude role-playing non-technical owners); logs fed back to fix real bugs.

**Key concepts demonstrated:** Multi-agent (ADK) · MCP server · Security · Agent skills (agents-cli) · Deployability · Antigravity (in video)

🔗 Repo: https://github.com/mystvearn/agent-solutions-inc
▶️ Video: <YOUTUBE_URL>
