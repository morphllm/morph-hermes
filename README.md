# morph-hermes

A [Hermes Agent](https://github.com/NousResearch/hermes-agent) model-provider
plugin for [Morph](https://www.morphllm.com). Morph serves open models such as Kimi,
GLM and DeepSeek on an OpenAI-compatible API.

## Install

```sh
hermes plugins install morphllm
```

## Setup

1. Create an API key at
   [morphllm.com/dashboard/api-keys](https://www.morphllm.com/dashboard/api-keys).

2. Save it, either in `~/.hermes/.env` or the process environment:

   ```sh
   MORPH_API_KEY=sk-...
   ```

   Optional: `MORPH_BASE_URL` points at another Morph endpoint. Default is
   `https://api.morphllm.com/v1`.

3. Select Morph in Hermes: `hermes model` → Morph (provider: `morph`).

The model picker lists the chat models your key can call, live from
`/v1/models`. Morph's Fast Apply, WarpGrep and compaction models are left out
because they are not chat models.

## Reasoning

When you set a reasoning effort in Hermes, it is sent as `reasoning_effort`.
Turning reasoning off sends `reasoning_effort: "none"`. With nothing set, each
model runs at its served default.

## What it does on your machine

- Makes HTTPS requests only to `api.morphllm.com` (or your `MORPH_BASE_URL`):
  `/v1/models` for the model list and the normal chat requests.
- Reads `MORPH_API_KEY` through Hermes's provider credentials. It stores
  nothing and reads no other files.
- No telemetry, no shell commands, no background processes, no self-updating
  code.
