# Plugin Operations Commands

Commands for managing plugins and executing plugin commands via CLI.

## plugins - List installed plugins

```bash
obsidian plugins [--filter "name"] [--versions]
```

**Parameters:**
- `--filter` - Search for specific plugins
- `--versions` - Show version information

**Examples:**
```bash
# List all plugins
obsidian plugins

# Find Templater plugin
obsidian plugins --filter "templater"

# Show with versions
obsidian plugins --versions
```

## plugins:enabled - List enabled plugins

```bash
obsidian plugins:enabled [--filter "name"] [--versions]
```

**Parameters:**
- `--filter` - Search for specific plugins
- `--versions` - Show version information

**Example:**
```bash
obsidian plugins:enabled --filter "database"
```

## plugin - Get plugin info

```bash
obsidian plugin --id "plugin-id"
```

**Parameters:**
- `--id` (required) - Plugin ID (found in plugin directory or `.obsidian/plugins/`)

**Example:**
```bash
obsidian plugin --id "templater-obsidian"
```

## plugin:enable - Enable a plugin

```bash
obsidian plugin:enable --id "plugin-id" [--filter "filter"]
```

**Parameters:**
- `--id` (required) - Plugin ID
- `--filter` - Filter parameter (optional)

**Example:**
```bash
obsidian plugin:enable --id "obsidian-dataview"
```

## plugin:disable - Disable a plugin

```bash
obsidian plugin:disable --id "plugin-id" [--filter "filter"]
```

**Parameters:**
- `--id` (required) - Plugin ID
- `--filter` - Filter parameter (optional)

**Example:**
```bash
obsidian plugin:disable --id "old-plugin"
```

## plugin:reload - Reload a plugin

```bash
obsidian plugin:reload --id "plugin-id"
```

**Parameters:**
- `--id` (required) - Plugin ID

**Example:**
```bash
obsidian plugin:reload --id "templater-obsidian"
```

## command - Execute a command

```bash
obsidian command --id "command-id" [args]
```

**Parameters:**
- `--id` (required) - Command ID (from the `commands` list)

**Example:**
```bash
obsidian command --id "templater:create-note-from-template"
```

## commands - List available commands

```bash
obsidian commands [--filter "text"]
```

**Parameters:**
- `--filter` - Search for specific commands

**Examples:**
```bash
# List all commands
obsidian commands

# Find Templater commands
obsidian commands --filter "templater"

# Find commands containing "template"
obsidian commands --filter "template"
```

## Common Patterns

### Check if Templater is enabled
```bash
obsidian plugin --id "templater-obsidian"
```

### Enable Templater plugin
```bash
obsidian plugin:enable --id "templater-obsidian"
```

### Find and list all template-related commands
```bash
obsidian commands --filter "template"
```

### Execute Templater's create note command
```bash
obsidian command --id "templater:create-new-note-action"
```

### Reload plugin after configuration change
```bash
obsidian plugin:reload --id "templater-obsidian"
```

### Check plugin status before running plugin commands
```bash
obsidian plugins --filter "dataview" --versions
```

## Plugin IDs

Common plugin IDs for reference:
- `templater-obsidian` - Templater
- `obsidian-dataview` - Dataview
- `obsidian-git` - Obsidian Git
- `db-folder` - Database Folder
- `quickadd` - QuickAdd
- `omnisearch` - Omnisearch

Find the exact ID in:
1. `.obsidian/plugins/` directory (folder name)
2. Obsidian community plugins directory
3. Run `obsidian plugins` to list

## Tips

- **Find plugin ID:** Run `obsidian plugins --filter "name"` to find the exact ID
- **Before executing commands:** Check that plugin is enabled with `plugin:enable`
- **Reload after changes:** Use `plugin:reload` if plugin configuration changes
- **Command discovery:** Use `commands --filter "keyword"` to find available commands
- **Error messages:** Commands may fail if plugin isn't enabled or command ID is wrong

## When to Use Plugin Commands

Use plugin commands when:
- Creating notes from templates (Templater)
- Enabling/disabling plugins before operations
- Running plugin-specific CLI features
- Automating plugin-dependent workflows

See specific plugin documentation for CLI command availability and exact command IDs.
