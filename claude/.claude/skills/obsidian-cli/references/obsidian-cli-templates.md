# Template Operations Commands

Commands for working with Templater templates.

## templates - List all templates

```bash
obsidian templates [--total]
```

**Parameters:**
- `--total` - Show count of templates

**Example:**
```bash
obsidian templates --total
```

## template:read - Read a template

```bash
obsidian template:read --name "template-name" [--resolve] [--title "custom title"]
```

**Parameters:**
- `--name` (required) - Template name (without extension)
- `--resolve` - Resolve template variables (useful for preview)
- `--title` - Custom title for the template

**Example:**
```bash
# Read template
obsidian template:read --name "how-to-template"

# Read and resolve variables to see what it will look like
obsidian template:read --name "how-to-template" --resolve
```

## template:insert - Insert template into current note

```bash
obsidian template:insert --name "template-name"
```

**Parameters:**
- `--name` (required) - Template name (without extension)

**Example:**
```bash
obsidian template:insert --name "meeting-template"
```

## Creating Template Files

Templates are Markdown files stored in your Templates folder (configured in Templater plugin settings). They use Templater syntax with `<% %>` delimiters.

### Basic Template Structure

Create a file named `how-to-template.md` in your Templates folder:

```markdown
---
type: how-to
context:
topic: []
project:
tags: []
---

# <% tp.file.title %>

**Created:** <% tp.date.now("YYYY-MM-DD") %>

## Overview

[Brief description of what this how-to covers]

## Prerequisites

- [ ] Prerequisite 1
- [ ] Prerequisite 2

## Steps

1. **Step 1**
   - Detailed instructions

2. **Step 2**
   - Detailed instructions

## Tips & Tricks

- Tip 1
- Tip 2

## References

- [Link 1]()
- [Link 2]()
```

### Common Template Variables

See [templater-plugin.md](templater-plugin.md) for comprehensive Templater syntax. Common variables:

- `<% tp.file.title %>` - Note title
- `<% tp.date.now("YYYY-MM-DD") %>` - Current date
- `<% tp.file.creation_date() %>` - File creation date
- `<% tp.file.folder %>` - Folder path

## Common Patterns

### Meeting Template
```markdown
---
type: meeting
context: work
topic: []
project:
tags: []
---

# Meeting - <% tp.date.now("YYYY-MM-DD") %>

**Attendees:**
-

**Date:** <% tp.date.now("YYYY-MM-DD HH:mm") %>

## Agenda

-

## Discussion

-

## Action Items

- [ ] Action 1 @assigned-to
- [ ] Action 2 @assigned-to

## Decisions Made

-

## Follow-up Notes

-
```

### Reference/Learning Template
```markdown
---
type: reference
context:
topic: []
project:
tags: []
---

# <% tp.file.title %>

**Last Updated:** <% tp.date.now("YYYY-MM-DD") %>

## Definition

[What is this? What does it do?]

## Key Concepts

### Concept 1
-

### Concept 2
-

## Use Cases

-

## Related Topics

- [[]]
- [[]]

## Resources

- [Link](url)
- [Link](url)
```

### Troubleshooting Template
```markdown
---
type: troubleshooting
context:
topic: []
project:
tags: []
resolved: false
---

# <% tp.file.title %>

**Date:** <% tp.date.now("YYYY-MM-DD") %>

## Problem Statement

[What's the issue?]

## Error Messages / Symptoms

```
[Error output or symptoms]
```

## Environment

- [Relevant tools/versions]

## Root Cause Analysis

[What caused this?]

## Solution

[What fixed it?]

## Prevention

[How to prevent in the future?]

## Related Issues

- [[]]
```

## Workflow: Create & Use Template

1. **Create template file:**
   ```bash
   obsidian create --name "custom-template" --path "Templates"
   ```

2. **Add template content:**
   ```bash
   obsidian append --file "Templates/custom-template.md" --content "[your template content]"
   ```

3. **List templates to verify:**
   ```bash
   obsidian templates
   ```

4. **Use the template:**
   When creating a new note:
   ```bash
   obsidian create --name "new-note" --path "My-Notes" --template "custom-template"
   ```

## See Also

- [templater-plugin.md](templater-plugin.md) for complete Templater syntax reference
