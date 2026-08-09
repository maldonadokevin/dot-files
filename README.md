# dot-files

Personal dot-files for macOS (work machine).

## Contents

| File / dir                 | Target                                              |
| -------------------------- | --------------------------------------------------- |
| `.zshrc`                   | `~/.zshrc`                                           |
| `.vimrc`                   | `~/.vimrc`                                           |
| `.gitconfig`               | `~/.gitconfig`                                       |
| `.gitignore_global`        | `~/.gitignore_global`                               |
| `.tmux.conf`               | `~/.tmux.conf`                                       |
| `vscode/settings.json`     | `~/Library/Application Support/Code/User/settings.json` |
| `claude/settings.json`     | `~/.claude/settings.json`                           |
| `claude/_settings.json`    | `~/.claude/_settings.json`                          |
| `claude/CLAUDE.md`         | `~/.claude/CLAUDE.md`                               |
| `iterm/…plist`             | iTerm2 preferences (see below)                      |

## Install

```sh
python3 install.py
```

The installer checks for required tools (Homebrew, uv, Rust, tmux), then
symlinks each dot-file after showing a diff and asking for confirmation.

## Secrets / machine-local config

Secrets and machine-specific settings live in **`~/.zshrc.local`**, which is
sourced by `.zshrc` but **never tracked**. Copy the template and fill it in:

```sh
cp .zshrc.local.example ~/.zshrc.local
```

Likewise, `~/.gitconfig.local` can hold per-machine git overrides.

## iTerm2

iTerm2 preferences are exported to `iterm/com.googlecode.iterm2.plist`.
macOS caches prefs, so don't symlink the plist directly. Instead point iTerm2
at this folder:

**iTerm2 → Settings → General → Settings**
- Check *"Load settings from a custom folder or URL"*
- Set it to this repo's `iterm/` directory
- Choose *"Save changes automatically"* (or save manually) to keep it updated

To refresh the tracked copy from the live prefs:

```sh
plutil -convert xml1 -o iterm/com.googlecode.iterm2.plist \
  ~/Library/Preferences/com.googlecode.iterm2.plist
```
