# Transcript Analytics v0 Specification

## High-Level Objective

- Create a CLI transcript analytics application

## Mid-Level Objective

- Build a python MVP typer CLI application.
- Accept a path to a text file.
- Count the frequency of each word in a file, filter out common words, and limit by count threshold.
- Use an openai chat completion with structured output analyze the transcript and word counts.
- Rich print the frequency of each word to the terminal and the transcript analysis.

## Implementation Notes
- No need to import any external libraries see pyproject.toml for dependencies.
- Comment every function.
- For typer commands add usage examples starting with `uv run main <func name dash sep and params>`
- When code block is given in low-level tasks, use it without making changes (Task 4).
- Carefully review each low-level task for exact code changes.

## Context

### Beginning context
- `src/spec_based_ai_coding/main.py`
- `pyproject.toml` (readonly)

### Ending context
- `src/spec_based_ai_coding/main.py`
- `pyproject.toml`
- `src/spec_based_ai_coding/llm.py` (new file)
- `src/spec_based_ai_coding/word_counter.py` (new file)
- `src/spec_based_ai_coding/data_types.py` (new file)
- `src/spec_based_ai_coding/constants.py` (new file)

## Low-Level Tasks
> Ordered from start to finish

1. Create common word blacklist.
```aider
CREATE src/spec_based_ai_coding/constants.py: 
    CREATE COMMON_WORDS_BLACKLIST = ['the', 'and', ...add 50 more common words]
```

2. Create our data types.
```aider
CREATE src/spec_based_ai_coding/data_types.py:

    CREATE pydantic types:

        WordCounts(BaseModel): {count_to_word_map: Dict[str, int]},

        TranscriptAnalysis(BaseModel): {
            quick_summary: str
            bullet_point_highlights: List[str]
            sentiment_analysis: str
            keywords: List[str]
        }
```

3. Create our word counter & filter out & limit by count threshold.
```aider
CREATE src/spec_based_ai_coding/word_counter.py:
    CREATE word_counter(script: str, min_count_threshold: int = 10) -> WordCounts:
        Remove punctuation from script and make all words lowercase,
        Use the COMMON_WORDS_BLACKLIST to filter out common words,
        Only include words that are greater than the min_count_threshold.
        Sort descending by count.
```

4. Create our LLM function using the code block below.
```python
# CREATE src/spec_based_ai_coding/llm.py: Use code block below no changes.

    from typing import List
    from pydantic import BaseModel
    from openai import OpenAI
    from .data_types import TranscriptAnalysis

    client = OpenAI()


    def analyze_transcript(transcript: str, word_count: dict) -> TranscriptAnalysis:
        completion = client.beta.chat.completions.parse(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant analyzing transcripts.",
                },
                {"role": "user", "content": f"{transcript}\n\nWord Count: {word_count}"},
            ],
            response_format=TranscriptAnalysis,
        )

        message = completion.choices[0].message
        if message.parsed:
            return message.parsed
        else:
            raise ValueError("Failed to parse the response")

```

5. Update our main function to use new count and analysis functions.

```aider
UPDATE src/spec_based_ai_coding/main.py:
    CREATE a new typer cli application:
        CREATE @app.command() def analyze_transcript(path_to_script_text_file, min_count_threshold: int = 10):
            Read file, count words, run analysis, rich print results,
            print words like '<word>: ###' where ### is count 3
```