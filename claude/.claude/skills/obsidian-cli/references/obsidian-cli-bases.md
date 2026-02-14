# Base/Database Operations Commands

Commands for working with Obsidian Bases (.base files) and database views.

## bases - List all .base files

```bash
obsidian bases
```

**Output:** Lists all `.base` files in your vault.

## base:query - Query a base

```bash
obsidian base:query --path "path/to/file.base" [--format "json|csv|tsv|md|paths"]
```

**Parameters:**
- `--path` (required) - Path to `.base` file relative to vault root
- `--format` - Output format
  - `json` - JSON format
  - `csv` - Comma-separated values
  - `tsv` - Tab-separated values
  - `md` - Markdown table
  - `paths` - File paths only (default)

**Examples:**
```bash
# Query base as markdown table
obsidian base:query --path "Bases/my-database.base" --format "md"

# Get results as JSON
obsidian base:query --path "Bases/work-notes.base" --format "json"

# Get just file paths
obsidian base:query --path "Bases/references.base"
```

## base:create - Create item in base

```bash
obsidian base:create --path "path/to/file.base" [--silent] [--newtab]
```

**Parameters:**
- `--path` (required) - Path to `.base` file
- `--silent` - Don't show notification
- `--newtab` - Open in new tab

**Example:**
```bash
obsidian base:create --path "Bases/work-database.base" --newtab
```

## Creating .base Files

To create a `.base` file, create a YAML file with the following structure:

```yaml
id: unique-id-here
name: Database Name
type: database
properties:
  type:
    type: string
  context:
    type: string
  topic:
    type: list
  project:
    type: string
views:
  table-view:
    type: table
    sourceType: folder
    source: My-Notes
    properties:
      - type
      - context
      - topic
      - project
```

Then create the file via CLI:
```bash
obsidian create --name "my-database" --path "Bases" --content "$(cat base-config.yaml)"
```

## Common Patterns

### Create a base to view all work notes by topic
```yaml
id: work-by-topic
name: Work Notes by Topic
type: database
properties:
  type:
    type: string
  context:
    type: string
  topic:
    type: list
  project:
    type: string
views:
  by-topic:
    type: table
    sourceType: folder
    source: My-Notes
    properties:
      - type
      - context
      - topic
      - project
```

### Query base and display results
```bash
obsidian base:query --path "Bases/work-by-topic.base" --format "md"
```

## See Also

- [obsidian-bases.md](obsidian-bases.md) for detailed `.base` file structure and configuration
- [property-schema.md](property-schema.md) for your property definitions
