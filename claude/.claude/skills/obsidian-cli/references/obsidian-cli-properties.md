# Property Operations Commands

Commands for setting, reading, and removing properties (frontmatter) on notes.

## property:set - Set a property on a file

```bash
obsidian property:set --name "propertyName" --value "value" --file "path/to/file.md" [--type "string|number|boolean|date|list"]
```

**Parameters:**
- `--name` (required) - Property name
- `--value` (required) - Property value
- `--file` or `--path` (required) - Target file
- `--type` - Property type (optional; inferred if not specified)
  - `string` - Text value
  - `number` - Numeric value
  - `boolean` - true/false
  - `date` - Date value
  - `list` - Array of values

**Examples:**
```bash
# Set basic property
obsidian property:set --name "type" --value "how-to" --file "My-Notes/my-guide.md"

# Set with explicit type
obsidian property:set --name "resolved" --value "true" --type "boolean" --file "My-Notes/bug.md"

# Set list property
obsidian property:set --name "topic" --value "[kubernetes, aws]" --type "list" --file "My-Notes/note.md"

# Set date property
obsidian property:set --name "due-date" --value "2025-12-31" --type "date" --file "My-Notes/task.md"
```

## property:read - Read a specific property

```bash
obsidian property:read --name "propertyName" --file "path/to/file.md"
```

**Parameters:**
- `--name` (required) - Property name to read
- `--file` or `--path` (required) - Target file

**Example:**
```bash
obsidian property:read --name "context" --file "My-Notes/my-note.md"
```

## property:remove - Remove a property

```bash
obsidian property:remove --name "propertyName" --file "path/to/file.md"
```

**Parameters:**
- `--name` (required) - Property name to remove
- `--file` or `--path` (required) - Target file

**Example:**
```bash
obsidian property:remove --name "old-property" --file "My-Notes/note.md"
```

## properties - List all properties of a file

```bash
obsidian properties --file "path/to/file.md" [--format "json|md|table"] [--all] [--sort "name"]
```

**Parameters:**
- `--file` or `--path` (required) - Target file
- `--format` - Output format (json, md, table)
- `--all` - Include all properties, including empty ones
- `--sort` - Sort order (name, etc.)
- `--counts` - Show usage counts

**Example:**
```bash
obsidian properties --file "My-Notes/my-note.md" --format "json"
```

## Common Patterns

### Set multiple properties at once
```bash
obsidian property:set --name "type" --value "reference" --file "note.md"
obsidian property:set --name "context" --value "work" --file "note.md"
obsidian property:set --name "topic" --value "[kubernetes]" --type "list" --file "note.md"
obsidian property:set --name "project" --value "platform-upgrade" --file "note.md"
```

### Bulk set property on multiple files
```bash
obsidian files --folder "My-Notes" | while read file; do
  obsidian property:set --name "context" --value "work" --file "My-Notes/$file"
done
```

### Set conditional property (e.g., resolved for troubleshooting)
```bash
# For troubleshooting notes, add resolved property
obsidian property:set --name "resolved" --value "false" --type "boolean" --file "Troubleshooting/bug.md"
```

### Verify property was set
```bash
obsidian property:read --name "type" --file "My-Notes/my-note.md"
```

## Tips

- **Type inference:** If you don't specify `--type`, Obsidian CLI infers it from the value
  - `true`/`false` → boolean
  - Numbers → number
  - Dates in ISO format → date
  - Arrays in brackets → list

- **List values:** Use JSON array format: `[value1, value2]`

- **Special characters:** Quote values containing spaces: `--value "multi word value"`

- **Property names:** Use consistent naming (kebab-case recommended to match file naming)

- **Validate:** Always verify properties are set correctly by reading them back with `property:read`
