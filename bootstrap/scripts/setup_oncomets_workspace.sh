#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  setup_oncomets_workspace.sh --project-path <path> [options]

Required:
  --project-path <path>         Path to OncoMETS project root in Werner machine.

Optional:
  --skills-repo-url <url>       Canonical repo URL. Default: https://github.com/ernestoelo/skills.git
  --skills-repo-path <path>     Local clone path. Default: ~/.config/opencode/skills
  --workspace-file <name>       Workspace file name. Default: OncoMETS-Isolated.code-workspace
  --link-full-library           Also expose full shared skills library in workspace settings.
  --force                       Overwrite existing instruction file and workspace file.
  -h, --help                    Show this help.

Example:
  ./setup_oncomets_workspace.sh \
    --project-path /mnt/disco_duro/onco \
    --link-full-library
EOF
}

PROJECT_PATH=""
SKILLS_REPO_URL="https://github.com/ernestoelo/skills.git"
SKILLS_REPO_PATH="${HOME}/.config/opencode/skills"
WORKSPACE_FILE_NAME="OncoMETS-Isolated.code-workspace"
LINK_FULL_LIBRARY=0
FORCE=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --project-path)
      PROJECT_PATH="${2:-}"
      shift 2
      ;;
    --skills-repo-url)
      SKILLS_REPO_URL="${2:-}"
      shift 2
      ;;
    --skills-repo-path)
      SKILLS_REPO_PATH="${2:-}"
      shift 2
      ;;
    --workspace-file)
      WORKSPACE_FILE_NAME="${2:-}"
      shift 2
      ;;
    --link-full-library)
      LINK_FULL_LIBRARY=1
      shift
      ;;
    --force)
      FORCE=1
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage
      exit 1
      ;;
  esac
done

if [[ -z "${PROJECT_PATH}" ]]; then
  echo "Error: --project-path is required." >&2
  usage
  exit 1
fi

if [[ ! -d "${PROJECT_PATH}" ]]; then
  echo "Error: project path does not exist: ${PROJECT_PATH}" >&2
  exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"
TEMPLATE_RELATIVE_PATH="bootstrap/templates/copilot-instructions.oncomets.md"
PILOT_SKILL_RELATIVE_PATH="oncomets-mil-loss-lab"
TEMPLATE_INSTRUCTIONS="${REPO_ROOT}/${TEMPLATE_RELATIVE_PATH}"
PILOT_SKILL_SOURCE="${REPO_ROOT}/${PILOT_SKILL_RELATIVE_PATH}"

if [[ ! -f "${TEMPLATE_INSTRUCTIONS}" ]]; then
  echo "Error: instruction template not found: ${TEMPLATE_INSTRUCTIONS}" >&2
  exit 1
fi

if [[ ! -d "${PILOT_SKILL_SOURCE}" ]]; then
  echo "Error: pilot skill folder not found: ${PILOT_SKILL_SOURCE}" >&2
  exit 1
fi

mkdir -p "$(dirname "${SKILLS_REPO_PATH}")"

if [[ -d "${SKILLS_REPO_PATH}/.git" ]]; then
  echo "[1/5] Updating skills repository at ${SKILLS_REPO_PATH}"
  git -C "${SKILLS_REPO_PATH}" fetch --all --prune
  git -C "${SKILLS_REPO_PATH}" pull --ff-only
else
  echo "[1/5] Cloning skills repository into ${SKILLS_REPO_PATH}"
  git clone "${SKILLS_REPO_URL}" "${SKILLS_REPO_PATH}"
fi

TEMPLATE_INSTRUCTIONS="${SKILLS_REPO_PATH}/${TEMPLATE_RELATIVE_PATH}"
PILOT_SKILL_SOURCE="${SKILLS_REPO_PATH}/${PILOT_SKILL_RELATIVE_PATH}"

if [[ ! -f "${TEMPLATE_INSTRUCTIONS}" ]]; then
  echo "Error: instruction template missing in canonical repo: ${TEMPLATE_INSTRUCTIONS}" >&2
  exit 1
fi

if [[ ! -d "${PILOT_SKILL_SOURCE}" ]]; then
  echo "Error: pilot skill missing in canonical repo: ${PILOT_SKILL_SOURCE}" >&2
  exit 1
fi

PROJECT_GITHUB_DIR="${PROJECT_PATH}/.github"
PROJECT_SKILLS_DIR="${PROJECT_GITHUB_DIR}/skills"
PROJECT_INSTRUCTIONS_FILE="${PROJECT_GITHUB_DIR}/copilot-instructions.md"
PROJECT_PILOT_SKILL_LINK="${PROJECT_SKILLS_DIR}/oncomets-mil-loss-lab"
WORKSPACE_FILE_PATH="${PROJECT_PATH}/${WORKSPACE_FILE_NAME}"

mkdir -p "${PROJECT_GITHUB_DIR}" "${PROJECT_SKILLS_DIR}"

echo "[2/5] Installing workspace instruction file"
if [[ -f "${PROJECT_INSTRUCTIONS_FILE}" && ${FORCE} -eq 0 ]]; then
  echo "  - Existing instruction preserved (use --force to overwrite): ${PROJECT_INSTRUCTIONS_FILE}"
else
  cp "${TEMPLATE_INSTRUCTIONS}" "${PROJECT_INSTRUCTIONS_FILE}"
  echo "  - Instruction installed: ${PROJECT_INSTRUCTIONS_FILE}"
fi

echo "[3/5] Linking pilot skill into project-local .github/skills"
if [[ -e "${PROJECT_PILOT_SKILL_LINK}" || -L "${PROJECT_PILOT_SKILL_LINK}" ]]; then
  if [[ ${FORCE} -eq 1 ]]; then
    rm -rf "${PROJECT_PILOT_SKILL_LINK}"
  else
    echo "  - Existing pilot skill link preserved (use --force to replace): ${PROJECT_PILOT_SKILL_LINK}"
  fi
fi

if [[ ! -e "${PROJECT_PILOT_SKILL_LINK}" ]]; then
  ln -s "${PILOT_SKILL_SOURCE}" "${PROJECT_PILOT_SKILL_LINK}"
  echo "  - Linked: ${PROJECT_PILOT_SKILL_LINK} -> ${PILOT_SKILL_SOURCE}"
fi

echo "[4/5] Generating isolated workspace file"
if [[ -f "${WORKSPACE_FILE_PATH}" && ${FORCE} -eq 0 ]]; then
  echo "  - Existing workspace file preserved (use --force to overwrite): ${WORKSPACE_FILE_PATH}"
else
  if [[ ${LINK_FULL_LIBRARY} -eq 1 ]]; then
    EXTRA_SKILL_LOCATION=",
      \"${SKILLS_REPO_PATH}\": true"
  else
    EXTRA_SKILL_LOCATION=""
  fi

  cat > "${WORKSPACE_FILE_PATH}" <<EOF
{
  "folders": [
    {
      "path": "."
    }
  ],
  "settings": {
    "chat.useAgentSkills": true,
    "chat.experimental.useSkillAdherencePrompt": true,
    "chat.agentSkillsLocations": {
      ".github/skills": true${EXTRA_SKILL_LOCATION}
    }
  }
}
EOF
  echo "  - Workspace file written: ${WORKSPACE_FILE_PATH}"
fi

echo "[5/5] Done"
echo ""
echo "Next steps:"
echo "1) Open the workspace over SSH in VS Code: ${WORKSPACE_FILE_PATH}"
echo "2) In Copilot Chat, test with: 'help me compare focal vs weighted BCE for CLAM imbalance'"
echo "3) Validate skill discovery by asking for 'oncomets mil loss' workflow"
