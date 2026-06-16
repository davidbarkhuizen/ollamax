# glossary

## ollama client

### chat method

    tools: Sequence[Mapping[str, Any] | Tool
    think: bool | Literal['low', 'medium', 'high']
    messages: Sequence[Mapping[str, Any] | Message]
    format: dict[str, Any] | Literal['', 'json']
    options: Mapping[str, Any] | Options

### role parameter

roles
- system [used to provide initial context]
- user [convey user invocation]
- assistant [last model response, used for continuity]
- tool [response to tool calls]

#### `think` parameter

The think parameter in the Ollama client chat method controls whether reasoning or "thinking" models perform a reasoning trace before generating a final response. 

##### Functionality

When enabled, the model's output is separated into a thinking section (the internal reasoning trace) and a content section (the final answer). 

##### Values

It accepts boolean values (true/false) for most models, or string values like "high", "medium", or "low" to control the depth of the trace (specifically for models like Qwen 3 or GPT-OSS). 

##### Accessing Output

The reasoning trace is returned in the message.thinking field, while the final answer is in message.content. 

##### Default Behavior

For some models like Qwen 3, thinking is enabled by default in the chat method, whereas for others like DeepSeek R1, it may be disabled by default in certain configurations.
