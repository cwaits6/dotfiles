# Obsidian CLI Reference

The Obsidian CLI enables command-line automation for Obsidian vaults. This is a quick reference for common commands. For complete documentation, see https://help.obsidian.md/cli

## Installation

```bash
npm install -g @obsidianmd/obsidian-cli
```

Verify installation:
```bash
obsidian --version
```

## Core Commands

### Open Vault
```bash
obsidian open <vault-path>
```

Opens the vault in the desktop app.

### Open File
```bash
obsidian open <vault-path>/<path-to-file>
```

Opens a specific file in the vault. The file path is relative to the vault root.

### Create File
Via CLI: Use the `obsidian` command to create and modify files. Files are created as standard markdown files with YAML frontmatter.

### Run Plugin Commands
```bash
obsidian plugins call <vault-path> <plugin-id> <command-name> [args]
```

Executes a command provided by a plugin (core or community). Plugin IDs can be found in the `.obsidian/plugins` directory or plugin marketplace.

### Execute Obsidian Native Features
The CLI can trigger many Obsidian native features through the command system. Check the vault's commands available:

```bash
obsidian commands <vault-path>
```

Lists all available commands in the vault (includes core commands and plugin commands).

## Working with Files

### File Paths
- Paths are relative to the vault root
- Use forward slashes `/` even on Windows
- Extensions matter: `.md` for markdown, `.yaml`/`.yml` for YAML files

### File Operations
When modifying files via the CLI:
- YAML frontmatter must be valid YAML
- Separate frontmatter from body with `---` on its own line
- Standard markdown syntax for the body

## Plugin Integration

The CLI can invoke any plugin that exposes commands. Common use cases:
- **Templater** - Create notes from templates, run template code
- **Bases** (core plugin) - Manage base files and views
- **Dataview** - Query vault data
- Community plugins with CLI support - Check plugin documentation

Always verify a plugin supports CLI before attempting to use it via `obsidian plugins call`.

## Environment Variables

Set the Obsidian vault path as an environment variable for convenience:
```bash
export OBSIDIAN_VAULT=/path/to/vault
obsidian open $OBSIDIAN_VAULT
```

## Common Patterns

### Batch Operations
For bulk file creation or modification:
1. Generate the file content (YAML frontmatter + markdown body)
2. Write to disk using standard file operations
3. Optionally trigger plugin commands afterward if needed

### Plugin-Specific Operations
When a specific plugin command is needed:
1. List available commands: `obsidian commands <vault-path>`
2. Check plugin documentation for command format
3. Call the command with appropriate arguments

## Limitations & Fallbacks

The CLI is in early access beta. Not all operations may be available:
- Some plugins may not expose CLI commands yet
- Direct file system manipulation may be the fallback for unsupported operations
- Obsidian desktop app features not yet mirrored in CLI require native Obsidian usage

See `native-workflows.md` for alternatives when CLI cannot accomplish a task.
