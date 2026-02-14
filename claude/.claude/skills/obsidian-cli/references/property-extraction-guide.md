# Property Extraction Guide

This guide helps Claude intelligently analyze note content and populate properties based on the note's structure and context. Use this **before** running the migration script.

## Property Detection Logic

### type (required)

Infer from note structure and content:

- **meeting** - Contains "meeting", "discussion", "standup", attendees list, action items, or date-based structure
- **how-to** - Numbered steps, "How to", "Instructions", procedure-oriented content
- **reference** - Definitions, "What is", "Overview", concepts, learning material, documentation
- **troubleshooting** - "Problem:", "Solution:", errors, debugging, root cause analysis
- **snippet** - Code blocks, commands, configs, short reusable content
- **skill** - AI-generated skills, explicitly marked
- **inbox** - Unstructured, rough captures, "TODO", incomplete thoughts
- **note** - Default if no clear pattern (general knowledge, mixed content)

### context (required)

Infer from content clues using your config's contexts:

- Look for domain indicators, work terminology, personal references
- Check surrounding folder/project context
- Ask if ambiguous

### topic (required list)

Extract keywords and categories:

1. **Explicit mentions** - Technologies, domains mentioned in content
2. **File name clues** - "kubernetes-setup" → `[kubernetes]`
3. **Folder structure** - "My-Notes/DevOps/" → `[devops]`
4. **Content analysis** - Scan for domain keywords
5. **Always a list** - Even single topics: `[kubernetes]` not `kubernetes`

### project (optional)

Infer if referencing a specific initiative:

- Explicit project names
- Client/customer names
- Time-bounded work: "Q2 Planning"
- Leave blank if general or unclear

### tags (optional list)

Extract metadata not covered by other properties:

- Priority: `[urgent]`, `[low-priority]`
- Status: `[in-progress]`, `[blocked]`, `[follow-up]`
- Source: `[from-meeting]`, `[needs-review]`

### resolved (conditional, troubleshooting only)

For `type: troubleshooting` only:

- `false` - Problem unsolved or status unclear
- `true` - Solution worked, issue closed
- Default: `false`

## Analysis Approach

1. **Read the full content** - Understand purpose and structure
2. **Apply detection logic** - Infer each property using patterns above
3. **Validate** - Check config for valid values
4. **Confirm with user** - Ask if uncertain about type, context, or topic
5. **Handle unknowns** - Ask rather than guess

## When to Ask

- Note doesn't fit a type clearly
- Context is ambiguous (work vs. personal, or custom domain)
- Topic is unclear or very broad
- Multiple projects mentioned
- Uncertain about troubleshooting resolution status
