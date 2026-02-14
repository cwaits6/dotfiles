# Templater Plugin Reference

Templater is a powerful templating engine for Obsidian that can generate dynamic content. For complete documentation, see https://docs.zervell.com/templater

## Overview

Templater enables:
- Dynamic template variables (date, filename, user input, etc.)
- JavaScript code execution within templates
- File creation from templates with variable substitution
- Macro automation

## Template Syntax

Templates use `<% %>` syntax for dynamic content.

### Built-in Variables

```
<% tp.file.title %>           - Note title (without extension)
<% tp.file.folder %>          - Folder path of the note
<% tp.file.creation_date() %> - File creation date
<% tp.date.now() %>           - Current date/time
<% tp.system.clipboard_manager.getValue() %> - Clipboard contents
```

### Conditionals

```
<% if (tp.file.title === "template") { %>
  This is template-only content
<% } %>
```

### JavaScript Execution

```
<%
  let title = tp.file.title;
  let words = title.split('-').length;
  tR += `Word count: ${words}`;
%>
```

### User Prompts

```
<% await tp.system.prompt("What is the context?") %>
```

## Creating Templates

### Template File Location
- Store in a `Templates` folder (or custom path configured in Templater settings)
- File format: `.md` files with template syntax
- Naming: Clear, descriptive names (e.g., `meeting-template.md`, `how-to-template.md`)

### Template Structure Example

```markdown
---
type: <% tp.system.prompt("Note type") %>
context: <% tp.system.prompt("Context") %>
topic: []
project:
tags: []
---

# <% tp.file.title %>

Created: <% tp.date.now("YYYY-MM-DD HH:mm") %>

## Content

```

## Using Templates with CLI

### Creating a Note from Template
```bash
obsidian open <vault-path>/<path-to-note>
```

Then trigger template insertion via Templater commands, or:
1. Create the template file
2. Create a new note that references the template
3. Use Templater's "Insert template" command via CLI (if exposed by plugin)

### Template Automation via CLI

If Templater exposes CLI commands:
```bash
obsidian plugins call <vault-path> templater insert-template [args]
```

Check available Templater commands:
```bash
obsidian commands <vault-path> | grep -i templater
```

## Common Patterns

### Auto-Generate Frontmatter
```
---
type: how-to
context: work
topic: []
created: <% tp.date.now("YYYY-MM-DD") %>
---
```

### Dynamic Title Transformation
```markdown
# <% tp.file.title.replace(/-/g, ' ').toUpperCase() %>
```

### Conditional Sections
```
<% if (type === "troubleshooting") { %>
## Resolution Status
[ ] Resolved
<% } %>
```

### Template with Macro
For repeated operations, define macros in Templater settings that can be invoked via CLI.

## Best Practices

- Keep templates simple and focused on structure, not content
- Use prompts sparingly to avoid interactive delays
- Name templates descriptively for easy reference
- Document custom functions/macros in template comments
- Test templates manually first before automating via CLI
