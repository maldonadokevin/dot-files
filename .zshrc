# Make Homebrew-installed tools available
eval "$(/opt/homebrew/bin/brew shellenv)"

# Enable zsh completion system (picks up Homebrew completions via FPATH)
autoload -Uz compinit && compinit

# uv environment (includes uv tools in PATH, only if installed)
[[ -f "$HOME/.local/bin/env" ]] && . "$HOME/.local/bin/env"

# Rust (only if installed)
[[ -f "$HOME/.cargo/env" ]] && . "$HOME/.cargo/env"

# Don't let virtualenv modify the prompt (we handle it below)
export VIRTUAL_ENV_DISABLE_PROMPT=1

setopt PROMPT_SUBST

# Load version control info
autoload -Uz vcs_info
precmd() { vcs_info }

# Git branch in purple
zstyle ':vcs_info:git:*' formats ' %F{13}(%b)%f'

# Active virtualenv in green
python_venv() {
  if [[ -n "$VIRTUAL_ENV" ]]; then
    echo " %F{2}($(basename "$VIRTUAL_ENV"))%f"
  fi
}

# Prompt: user:~/path (venv) (branch) %
PROMPT='%F{0}%n%f:%B%F{4}%~%f%b$(python_venv)${vcs_info_msg_0_} %# '

# Machine-local config: secrets, work aliases, etc. Not tracked in dot-files.
[[ -f "$HOME/.zshrc.local" ]] && source "$HOME/.zshrc.local"
