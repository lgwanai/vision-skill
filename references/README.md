# References

> Source data and methodology docs from 3 GPT Image 2 community projects.
> The merged, searchable case library lives in `../cases/`.

## Sources

| Source | Project | Cases |
|--------|---------|-------|
| **youmind** | [YouMind-OpenLab/awesome-gpt-image-2](https://github.com/YouMind-OpenLab/awesome-gpt-image-2) | 135 |
| **freestylefly** | [freestylefly/awesome-gpt-image-2](https://github.com/freestylefly/awesome-gpt-image-2) | 503 |
| **evolink** | [EvoLinkAI/awesome-gpt-image-2-API-and-Prompts](https://github.com/EvoLinkAI/awesome-gpt-image-2-API-and-Prompts) | 706 |

**Total: 1322 cases** (merged into `../cases/index.json`)

## Directory Structure

```
references/
├── README.md              # This file
├── data/                  # Raw JSON data (used by scripts/merge_cases.py)
│   ├── youmind-all-prompts.json
│   ├── freestylefly-all-cases.json
│   └── evolink-all-cases.json
├── indexes/               # Original INDEX.md from each source
│   ├── youmind-INDEX.md
│   ├── freestylefly-INDEX.md
│   └── evolink-INDEX.md
├── methods/               # Prompt engineering methodology docs
│   ├── youmind-category-techniques.md
│   ├── youmind-prompt-engineering-techniques.md
│   ├── youmind-tools-and-integration.md
│   ├── freestylefly-prompt-length-analysis.md
│   ├── evolink-prompt-analysis.md
│   └── evolink-api-integration-guide.md
├── templates/             # Industrial prompt templates (from freestylefly)
│   ├── tpl-poster.md      # Poster & typography templates
│   ├── tpl-ui.md          # UI & interface templates
│   ├── tpl-photo.md       # Photography templates
│   ├── tpl-product.md     # Product & e-commerce templates
│   ├── tpl-infographic.md # Infographic & chart templates
│   ├── tpl-illustration.md# Illustration & art templates
│   ├── tpl-brand.md       # Brand & logo templates
│   ├── tpl-character.md   # Character design templates
│   ├── tpl-architecture.md# Architecture & space templates
│   ├── tpl-scene.md       # Scene & storytelling templates
│   ├── tpl-document.md    # Document & publishing templates
│   ├── tpl-history.md     # History & classical themes
│   ├── tpl-other.md       # Other use cases
│   └── README.md
└── style-library/         # Style reference library (from freestylefly)
    ├── agent-skill.md
    └── style-library-reference.md
```

## Rebuilding the Case Library

To regenerate `../cases/` from the JSON data:

```bash
python3 scripts/merge_cases.py
```
