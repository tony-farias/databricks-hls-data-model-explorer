#!/usr/bin/env bash
set -euo pipefail

# Usage:
#   DATABRICKS_CONFIG_PROFILE=my-profile APP_NAME=hls-data-models ./deploy.sh
# Optional: WORKSPACE_PATH=/Workspace/Users/me@example.com/apps/hls-data-models

PROFILE="${DATABRICKS_CONFIG_PROFILE:-DEFAULT}"
APP_NAME="${APP_NAME:-hls-data-models}"

cd "$(dirname "$0")"

if [[ -z "${WORKSPACE_PATH:-}" ]]; then
  CURRENT_USER="$(databricks current-user me --profile "$PROFILE" --output json | python3 -c 'import json,sys; print(json.load(sys.stdin)["userName"])')"
  WORKSPACE_PATH="/Workspace/Users/${CURRENT_USER}/apps/${APP_NAME}"
fi

RUNTIME_FILES=(
  app.py
  app.yaml
  requirements.txt
  static/index.html
  static/data.js
  static/config.js
  static/genieflow-logo.png
  static/deploy-monday-morning-scintilla.zip
)

echo "Uploading app files to ${WORKSPACE_PATH}"
databricks workspace mkdirs "${WORKSPACE_PATH}/static" --profile "$PROFILE"
for file in "${RUNTIME_FILES[@]}"; do
  format="AUTO"
  [[ "$file" == *.zip ]] && format="RAW"
  databricks workspace import "${WORKSPACE_PATH}/${file}" \
    --file "$file" --format "$format" --overwrite --profile "$PROFILE"
done

if ! databricks apps get "$APP_NAME" --profile "$PROFILE" >/dev/null 2>&1; then
  echo "Creating Databricks App ${APP_NAME}"
  databricks apps create "$APP_NAME" \
    --description "Interactive HLS data-model explorer" --profile "$PROFILE"
fi

echo "Deploying ${APP_NAME}"
databricks apps deploy "$APP_NAME" --source-code-path "$WORKSPACE_PATH" \
  --profile "$PROFILE" --output json

databricks apps get "$APP_NAME" --profile "$PROFILE" --output json \
  | python3 -c 'import json,sys; d=json.load(sys.stdin); print("App URL:", d.get("url")); print("State:", d.get("app_status",{}).get("state"))'
