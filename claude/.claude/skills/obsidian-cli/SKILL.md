---
name: obsidian-cli
description: "Comprehensive Obsidian vault automation via CLI. Use for: (1) Migrating and reorganizing notes with intelligent property assignment, (2) Creating and managing Obsidian Bases (.base files) for database views, (3) Generating Templater templates with dynamic syntax, (4) Batch operations on notes. Prioritizes Obsidian CLI when available; provides native Obsidian workflows as fallback. Claude asks for explicit approval before any edits to your vault."
---

# Obsidian CLI Skill

## Overview

This skill enables batch automation of your Obsidian vault using the Obsidian CLI. It intelligently analyzes your notes, assigns properties based on content, and orchestrates migrations, base creation, template generation, and other vault operations.

**Core principle: Claude asks for explicit approval before modifying any of your notes.**

## Workflow

All operations follow this pattern:

1. **Analyze** - Claude reads notes/requirements
2. **Propose** - Claude shows you the changes (properties, structure, commands, etc.)
3. **Approve** - You review and approve before any files are modified
4. **Execute** - Obsidian CLI commands make the approved changes

## Obsidian CLI Command Categories

When you need to work with your vault, Claude will:
1. Determine which command category is needed (see below)
2. Read the corresponding reference file for detailed commands
3. Propose the specific CLI commands to run
4. Get your approval
5. Execute via Bash

### File Operations
Moving, renaming, creating, reading, deleting files. Obsidian CLI automatically updates all vault links.
- **See:** [obsidian-cli-files.md](references/obsidian-cli-files.md)
- **When to use:** Organizing notes, bulk migrations, file cleanup
- **Key command:** `obsidian move` (handles renaming and moving with auto-link updates)

### Property Operations
Setting, reading, removing properties/frontmatter on notes.
- **See:** [obsidian-cli-properties.md](references/obsidian-cli-properties.md)
- **When to use:** Assigning type, context, topic, tags, and other metadata
- **Key commands:** `obsidian property:set`, `obsidian property:read`, `obsidian property:remove`

### Base Operations
Creating and querying Obsidian Bases (.base files) for database-like functionality.
- **See:** [obsidian-cli-bases.md](references/obsidian-cli-bases.md)
- **When to use:** Setting up views to query notes by properties, creating dashboards
- **Key commands:** `obsidian bases`, `obsidian base:query`, `obsidian base:create`

### Template Operations
Creating, reading, and inserting Templater templates.
- **See:** [obsidian-cli-templates.md](references/obsidian-cli-templates.md)
- **When to use:** Automating note creation, inserting dynamic content
- **Key commands:** `obsidian templates`, `obsidian template:read`, `obsidian template:insert`

### Search Operations
Searching vault content and links.
- **See:** [obsidian-cli-search.md](references/obsidian-cli-search.md)
- **When to use:** Finding notes by content, analyzing link structure
- **Key commands:** `obsidian search`, `obsidian links`, `obsidian backlinks`

### Plugin Operations
Enabling, disabling, managing plugins.
- **See:** [obsidian-cli-plugins.md](references/obsidian-cli-plugins.md)
- **When to use:** Automating plugin setup, running plugin commands via CLI
- **Key commands:** `obsidian plugin:enable`, `obsidian plugin:disable`, `obsidian command`

## Common Workflows

### Migrate and Enrich Notes

Reorganize notes to a new folder while intelligently assigning properties:

1. Claude reads your notes from the source folder
2. Using the [property extraction guide](references/property-extraction-guide.md), Claude analyzes each note's content
3. Claude proposes properties (type, context, topic, tags, etc.) based on the content
4. You review and approve the proposed properties
5. Claude rewrites each note with the assigned YAML frontmatter (using `obsidian property:set`)
6. Claude moves enriched notes to the destination folder (using `obsidian move`)

**Approval step is mandatory** - Claude will show you the property assignments for each note before applying them.

### Create Obsidian Bases

Generate `.base` files to define database structures:

1. You describe what data you want to query (e.g., "all how-to notes organized by topic")
2. Claude references your [CONFIG_TEMPLATE.yaml](CONFIG_TEMPLATE.yaml) to understand your property schema
3. Claude proposes the `.base` file structure and view configuration
4. You approve the structure
5. Claude creates the `.base` file using Obsidian CLI
6. Open it in Obsidian to create database views

### Generate Templater Templates

Create new Templater templates for automating note creation:

1. You describe what the template should do
2. Claude proposes the template content with dynamic Templater syntax
3. You review and approve
4. Claude creates the template file in your Templates folder

## Reference Materials

### Configuration & Schema
- **[CONFIG_TEMPLATE.yaml](CONFIG_TEMPLATE.yaml)** - Template for your property schema (copy to config.yaml)
- **[property-schema.md](references/property-schema.md)** - Your universal and conditional properties
- **[property-extraction-guide.md](references/property-extraction-guide.md)** - How Claude analyzes content to assign properties

### Vault Understanding
- **[obsidian-bases.md](references/obsidian-bases.md)** - How to create and structure `.base` files
- **[templater-plugin.md](references/templater-plugin.md)** - Templater syntax and template patterns
- **[native-workflows.md](references/native-workflows.md)** - Fallback native Obsidian approaches

### Obsidian CLI Commands (by category)
- **[obsidian-cli-files.md](references/obsidian-cli-files.md)** - File operations (create, read, move, delete, etc.)
- **[obsidian-cli-properties.md](references/obsidian-cli-properties.md)** - Property management (set, get, remove)
- **[obsidian-cli-bases.md](references/obsidian-cli-bases.md)** - Base/database operations (query, create, list)
- **[obsidian-cli-templates.md](references/obsidian-cli-templates.md)** - Template operations (list, read, insert)
- **[obsidian-cli-search.md](references/obsidian-cli-search.md)** - Search, links, and query operations
- **[obsidian-cli-plugins.md](references/obsidian-cli-plugins.md)** - Plugin management and command execution

## Important Notes

- **Approval required:** Claude will always show you the commands and ask for approval before executing
- **Direct CLI calls:** Claude calls Obsidian CLI commands directly via Bash (no wrapper scripts)
- **Auto-link updates:** When moving/renaming files, Obsidian CLI automatically updates all vault links
- **File naming:** Normalized automatically to lowercase kebab-case where needed
- **Schema customization:** Always customize [CONFIG_TEMPLATE.yaml](CONFIG_TEMPLATE.yaml) to match your vault
- **CLI limitations:** If a task can't be done via CLI, detailed native Obsidian instructions will be provided
- **Nested operations:** For complex workflows (e.g., migrate + enrich + query), operations happen in sequence with approval at each step
