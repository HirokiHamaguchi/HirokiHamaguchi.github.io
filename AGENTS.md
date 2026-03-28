# AGENTS

## Subprogram update rule

- `subprogram` 配下の実装を変更した後は、必ず以下を実行して生成物を更新すること。

```bash
uv run ./subprogram/build-all.py
```

- これは `subprogram` のビルド成果物（`_program/dist` など）を反映するために必要。
