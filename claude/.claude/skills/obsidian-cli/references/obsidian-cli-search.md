# Search & Link Operations Commands

Commands for searching vault content and analyzing vault links.

## search - Search vault

```bash
obsidian search --query "search term" [--path "folder"] [--limit 50] [--format "json|md|paths"] [--case] [--matches] [--total]
```

**Parameters:**
- `--query` (required) - Search query
- `--path` - Limit search to specific folder
- `--limit` - Maximum results to return
- `--format` - Output format
  - `json` - JSON format
  - `md` - Markdown format
  - `paths` - File paths only (default)
- `--case` - Case-sensitive search
- `--matches` - Show match count
- `--total` - Show total results

**Examples:**
```bash
# Basic search
obsidian search --query "kubernetes"

# Search in specific folder
obsidian search --query "setup" --path "My-Notes/DevOps" --limit 20

# Search as markdown table
obsidian search --query "important" --format "md"

# Case-sensitive search
obsidian search --query "MyProject" --case

# Show match counts
obsidian search --query "todo" --matches --total
```

## search:open - Open search view

```bash
obsidian search:open --query "search term"
```

**Parameters:**
- `--query` (required) - Initial search query

**Example:**
```bash
obsidian search:open --query "kubernetes setup"
```

## backlinks - List incoming links to a file

```bash
obsidian backlinks --file "path/to/file.md" [--counts] [--total]
```

**Parameters:**
- `--file` or `--path` (required) - Target file
- `--counts` - Show link counts
- `--total` - Show total count

**Example:**
```bash
obsidian backlinks --file "Reference/kubernetes.md" --total
```

## links - List outgoing links from a file

```bash
obsidian links --file "path/to/file.md" [--total]
```

**Parameters:**
- `--file` or `--path` (required) - Source file
- `--total` - Show total count

**Example:**
```bash
obsidian links --file "My-Notes/project-overview.md" --total
```

## unresolved - List broken/unresolved links

```bash
obsidian unresolved [--verbose] [--total] [--counts]
```

**Parameters:**
- `--verbose` - Detailed output
- `--total` - Show count
- `--counts` - Show counts by type

**Example:**
```bash
# Find all broken links
obsidian unresolved --total

# See detailed info
obsidian unresolved --verbose
```

## orphans - List files with no incoming links

```bash
obsidian orphans [--all] [--total]
```

**Parameters:**
- `--all` - Include all files, not just recent
- `--total` - Show count

**Example:**
```bash
obsidian orphans --total
```

## deadends - List files with no outgoing links

```bash
obsidian deadends [--all] [--total]
```

**Parameters:**
- `--all` - Include all files, not just recent
- `--total` - Show count

**Example:**
```bash
obsidian deadends --total
```

## Common Patterns

### Find all notes about a topic
```bash
obsidian search --query "kubernetes" --format "md"
```

### Analyze link structure of a note
```bash
echo "=== Incoming Links ==="
obsidian backlinks --file "My-Notes/architecture.md" --total

echo "=== Outgoing Links ==="
obsidian links --file "My-Notes/architecture.md" --total
```

### Identify orphaned notes (no one links to them)
```bash
obsidian orphans --total
```

### Find broken links in vault
```bash
obsidian unresolved --verbose
```

### Search for unfinished work
```bash
obsidian search --query "TODO|FIXME|XXX" --format "md"
```

### Find all notes in a folder matching a pattern
```bash
obsidian search --query "error" --path "Troubleshooting" --format "paths"
```

### Export search results to file
```bash
obsidian search --query "important" --format "md" > search-results.md
```
