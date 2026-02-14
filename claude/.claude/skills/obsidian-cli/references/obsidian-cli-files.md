# File Operations Commands

Commands for creating, reading, moving, and deleting files. Obsidian CLI automatically updates all vault links when files are moved or renamed.

## create - Create a new file

```bash
obsidian create --name "filename" --path "folder/path" [--content "text"] [--template "name"] [--overwrite] [--silent] [--newtab]
```

**Parameters:**
- `--name` (required) - Filename without extension
- `--path` - Destination folder (relative to vault root)
- `--content` - Initial file content
- `--template` - Template to use for file content
- `--overwrite` - Overwrite if file already exists
- `--silent` - Don't show notification
- `--newtab` - Open in new tab

**Examples:**
```bash
# Create note in My-Notes folder
obsidian create --name "my-note" --path "My-Notes"

# Create with initial content
obsidian create --name "meeting-notes" --path "My-Notes" --content "## Attendees\n\n## Discussion\n\n## Action Items"

# Create from template
obsidian create --name "how-to-guide" --path "How-Tos" --template "how-to-template"
```

## read - Read file contents

```bash
obsidian read --file "path/to/file.md"
```

**Parameters:**
- `--file` or `--path` - File path relative to vault root

**Example:**
```bash
obsidian read --file "My-Notes/my-note.md"
```

## move - Move or rename file (auto-updates links)

```bash
obsidian move --file "old/path.md" --to "new/path.md"
```

**Parameters:**
- `--file` or `--path` - Current file path
- `--to` (required) - New file path (includes new filename)

**Use cases:**
- **Rename:** Same folder, different name: `obsidian move --file "Folder/old-name.md" --to "Folder/new-name.md"`
- **Move:** Different folder, same name: `obsidian move --file "Old-Folder/file.md" --to "New-Folder/file.md"`
- **Move + rename:** Different folder and name: `obsidian move --file "Old/old-name.md" --to "New/new-name.md"`

**Important:** All vault links are automatically updated to match the new path.

**Examples:**
```bash
# Rename file to kebab-case
obsidian move --file "My-Notes/My Meeting Notes.md" --to "My-Notes/my-meeting-notes.md"

# Move file to different folder
obsidian move --file "Captures/random-note.md" --to "My-Notes/organized-note.md"

# Batch rename with loop
for file in $(obsidian files --folder "Captures" --format "paths"); do
  normalized=$(echo "$file" | tr '[:upper:]' '[:lower:]' | tr ' ' '-')
  obsidian move --file "$file" --to "$normalized"
done
```

## append - Add content to end of file

```bash
obsidian append --file "path/to/file.md" --content "new content" [--inline] [--silent]
```

**Parameters:**
- `--file` or `--path` - Target file
- `--content` (required) - Content to append
- `--inline` - Don't add newline before content
- `--silent` - Don't show notification

**Example:**
```bash
obsidian append --file "My-Notes/meeting.md" --content "\n\n## Follow-up Items\n- [ ] Action 1"
```

## prepend - Add content to start of file

```bash
obsidian prepend --file "path/to/file.md" --content "new content" [--inline] [--silent]
```

**Same parameters as append**, but adds to beginning of file.

## delete - Delete file

```bash
obsidian delete --file "path/to/file.md" [--permanent]
```

**Parameters:**
- `--file` or `--path` - File to delete
- `--permanent` - Skip trash, permanently delete

**Example:**
```bash
# Move to trash
obsidian delete --file "Captures/old-note.md"

# Permanently delete
obsidian delete --file "Captures/old-note.md" --permanent
```

## open - Open file in Obsidian

```bash
obsidian open --file "path/to/file.md" [--newtab]
```

**Parameters:**
- `--file` or `--path` - File to open
- `--newtab` - Open in new tab instead of current pane

**Example:**
```bash
obsidian open --file "My-Notes/my-note.md" --newtab
```

## files - List files in a folder

```bash
obsidian files [--folder "folder/path"] [--ext ".md"] [--total]
```

**Parameters:**
- `--folder` - Folder to list (optional, defaults to vault root)
- `--ext` - Filter by extension (e.g., ".md", ".yaml")
- `--total` - Show file count

**Examples:**
```bash
# List all files in My-Notes
obsidian files --folder "My-Notes"

# List only YAML files in vault root
obsidian files --ext ".yaml"

# List and count files in folder
obsidian files --folder "Captures" --total
```

## Common Patterns

### Normalize filenames in a folder to kebab-case
```bash
obsidian files --folder "Captures" | while read file; do
  normalized=$(basename "$file" | tr '[:upper:]' '[:lower:]' | tr ' _' '-' | tr -s '-')
  obsidian move --file "Captures/$file" --to "Captures/$normalized"
done
```

### Batch move files from one folder to another with rename
```bash
obsidian files --folder "Source-Folder" | while read file; do
  filename=$(basename "$file")
  obsidian move --file "Source-Folder/$filename" --to "Dest-Folder/$filename"
done
```

### Create multiple notes from a list
```bash
for note_name in "note-1" "note-2" "note-3"; do
  obsidian create --name "$note_name" --path "My-Notes" --content "# $note_name"
done
```
