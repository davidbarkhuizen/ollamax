david barkhuizen, 2026

# yoke

llm harness

## target model

`qwen3.6:35b-a3b`

```
    FROM qwen3.6:35b-a3b

    PARAMETER num_ctx 32768
    PARAMETER temperature 0.6
    PARAMETER top_p 0.95
    PARAMETER top_k 20
    PARAMETER min_p 0.0
    PARAMETER presence_penalty 0.0
    PARAMETER repeat_penalty 1.0
```

## notes

- functional requirements
- objectives
- input/output expectations
- constraints
- domain context

## TODO

- list-tasks command
