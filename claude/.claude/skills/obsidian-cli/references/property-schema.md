# Property Schema Reference

This document outlines how properties work in notes. See your `config.yaml` for the specific values your vault uses.

## Universal Properties

Every note requires three properties in its YAML frontmatter:

### type (required, string)
Classifies the note into a category. See `note_types` in your `config.yaml` for valid values.

### context (required, string)
Life domain the note belongs to. See `contexts` in your `config.yaml` for valid values.

### topic (required, list)
Always a list, even for a single value. Broad categories relevant to the note.

Examples: `[kubernetes]`, `[aws, terraform]`, `[security]`

## Optional Properties

### project (optional, string)
Specific initiative or project the note belongs to.

Examples: `project-a`, `my-initiative`, `quarterly-planning`

### tags (optional, list)
Freeform catch-all for miscellaneous metadata.

Examples: `[urgent]`, `[needs-review]`

## Conditional Properties

Check your `config.yaml` under `conditional_properties` for properties that apply only to specific note types.

Example: `resolved` (boolean) applies only when `type: troubleshooting`.

## Principle

Keep frontmatter lean. Put detailed information in the note body.
