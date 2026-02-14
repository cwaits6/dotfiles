# Obsidian Bases Reference

Obsidian Bases is a core plugin that enables powerful database-like functionality. For complete documentation, see https://help.obsidian.md/bases

## Overview

Bases allow you to create structured databases with:
- Rows (notes in your vault)
- Columns (properties from note frontmatter)
- Views (different ways to display and query data)
- Rich querying capabilities

## .base Files

`.base` files are YAML files that define the structure of a database.

### File Location
- Store in your vault alongside regular notes
- Naming: lowercase kebab-case with `.base` extension (e.g., `my-database.base`)
- Paths are relative to vault root

### Basic Structure
```yaml
id: <unique-identifier>
name: <database-name>
type: database
properties:
  <property-name>:
    type: <property-type>
    required: <boolean>
views:
  <view-name>:
    type: <view-type>
    <view-configuration>
```

## Property Types

Supported property types in Bases:
- `string` - Text values
- `number` - Numeric values
- `boolean` - True/false
- `date` - Dates
- `list` - List of values (matches frontmatter list format)
- `relation` - Links to other notes
- `tag` - Tags from note properties

## View Types

### Table View
Most common view type. Displays database rows as a table.

```yaml
views:
  table-view:
    type: table
    sourceType: folder
    source: <folder-path>
    properties:
      - <property-name>
      - <property-name>
```

### Gallery View
Display rows as cards/gallery.

```yaml
views:
  gallery-view:
    type: gallery
    sourceType: folder
    source: <folder-path>
```

### Kanban View
Display rows as cards on a kanban board (grouped by property values).

## Data Sources

Define which notes appear in your database:

```yaml
sourceType: folder
source: <folder-path>
```

Bases can pull from:
- Specific folders
- All notes with specific properties
- Custom filters

## Creating Bases via CLI

The Bases plugin exposes CLI commands. List available commands:
```bash
obsidian commands <vault-path> | grep -i base
```

Common patterns:
1. Define the `.base` file structure
2. Save as YAML in your vault
3. Trigger view updates via plugin commands if needed
4. Open in Obsidian to see the database views

## Linking Bases to Properties

For Bases to recognize notes:
1. Notes must have properties matching the Base's schema
2. Property names and types must align
3. Use folder source or property filters in the view definition

## Best Practices

- Define property types explicitly to match your note schema
- Use consistent naming across `.base` files and frontmatter
- Test in Obsidian UI first to understand the structure
- Keep `.base` files in a dedicated folder if managing many databases
