# Prompt Engineering Methods

> Analysis of 706 curated GPT Image 2 prompts
---

## Key Patterns

1. **Natural Language Dominant**: Most prompts (421) use detailed natural language descriptions
2. **Raycast Parameterization**: 95 prompts use `{argument}` syntax for dynamic parameters
3. **E-commerce Focus**: Heavy emphasis on product photography, ad creatives, and UI mockups
4. **Multi-lingual**: Prompts in Chinese, Japanese, Korean, English, and more

## API-First Approach

This project uniquely combines prompt curation with API integration guides and a callable gen-skill (`npx evolink-gpt-image -y`).

## Curation Pipeline

- Daily batch curation from X/Twitter community
- Review and media validation before inclusion
- Multi-language sync via `script/sync_multilingual_readmes.py`
