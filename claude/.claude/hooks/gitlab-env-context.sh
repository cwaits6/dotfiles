#!/bin/bash
if [ -n "$GITLAB_TOKEN" ] && [ -n "$GITLAB_URL" ]; then
  echo '{"hookSpecificOutput":{"hookEventName":"SessionStart","additionalContext":"GITLAB_TOKEN and GITLAB_URL are set in the environment. Use them by name in shell commands. Do not echo, print, or display their values."}}'
fi
