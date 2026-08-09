# uv environment (adds uv + tools to PATH)
. "$HOME/.local/bin/env"

# Aliases
alias dc="docker compose"
alias dcup="docker compose --profile dev up --build"
alias ls="eza --icons --color=never -F"
alias lg="lazygit"
alias ll="ls -l"

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

# Detect light vs dark background from $COLORFGBG (set by iTerm2's shell
# integration as "fg;bg"); background 7 or 15 means a light background.
if [[ "${COLORFGBG##*;}" == 7 || "${COLORFGBG##*;}" == 15 ]]; then
  PROMPT_PATH_COLOR=4    # blue
  PROMPT_BRANCH_COLOR=5  # purple
  PROMPT_VENV_COLOR=2    # dark green
else
  PROMPT_PATH_COLOR=12   # bright blue
  PROMPT_BRANCH_COLOR=13 # bright magenta
  PROMPT_VENV_COLOR=10   # bright green
fi

# Git branch, colored per detected theme
zstyle ':vcs_info:git:*' formats " %F{${PROMPT_BRANCH_COLOR}}(%b)%f"

# Active virtualenv, colored per detected theme
python_venv() {
  if [[ -n "$VIRTUAL_ENV" ]]; then
    echo " %F{${PROMPT_VENV_COLOR}}($(basename "$VIRTUAL_ENV"))%f"
  fi
}

# Prompt: ~/path (venv) (branch) %
PROMPT='%B%F{${PROMPT_PATH_COLOR}}%~%f%b$(python_venv)${vcs_info_msg_0_} %# '

# Large shared history
export HISTSIZE=100000
export SAVEHIST=100000

# Machine-local config: secrets, work aliases, machine-specific env, etc.
# Not tracked in dot-files. See .zshrc.local.example.
[[ -f "$HOME/.zshrc.local" ]] && source "$HOME/.zshrc.local"
