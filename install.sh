#!/usr/bin/env bash
# install.sh — installer for fractioncalc-cli
# Usage: bash install.sh

set -e

REPO="https://github.com/Nararinyan/fractioncalc-cli.git"
INSTALL_DIR="$HOME/.local/bin"
SCRIPT_NAME="fractioncalc"
TMP_DIR=$(mktemp -d)

# ── Colors ────────────────────────────────────────────────────
CYAN="\033[96m"
GREEN="\033[92m"
YELLOW="\033[93m"
RED="\033[91m"
DIM="\033[2m"
RESET="\033[0m"

info()    { echo -e "${CYAN}  →${RESET} $1"; }
success() { echo -e "${GREEN}  ✓${RESET} $1"; }
warn()    { echo -e "${YELLOW}  !${RESET} $1"; }
error()   { echo -e "${RED}  ✗${RESET} $1"; exit 1; }

echo -e "\n${CYAN}  fractioncalc-cli installer${RESET}\n"

# ── Check dependencies ────────────────────────────────────────
info "Mengecek dependencies..."
command -v python3 &>/dev/null || error "python3 tidak ditemukan. Install dulu: sudo pacman -S python"
command -v git    &>/dev/null || error "git tidak ditemukan. Install dulu: sudo pacman -S git"
success "Dependencies OK"

# ── Clone ─────────────────────────────────────────────────────
info "Mengunduh dari GitHub..."
git clone --depth=1 "$REPO" "$TMP_DIR/repo" &>/dev/null
success "Clone selesai"

# ── Install ───────────────────────────────────────────────────
info "Menginstall ke $INSTALL_DIR..."
mkdir -p "$INSTALL_DIR"
cp "$TMP_DIR/repo/fractioncalc.py" "$INSTALL_DIR/$SCRIPT_NAME"
chmod +x "$INSTALL_DIR/$SCRIPT_NAME"
success "File terpasang di $INSTALL_DIR/$SCRIPT_NAME"

# ── Cleanup ───────────────────────────────────────────────────
rm -rf "$TMP_DIR"

# ── PATH check ────────────────────────────────────────────────
if [[ ":$PATH:" != *":$INSTALL_DIR:"* ]]; then
    warn "$INSTALL_DIR belum ada di PATH kamu."
    echo ""

    # Detect shell config file
    if [[ -f "$HOME/.zshrc" ]]; then
        SHELL_RC="$HOME/.zshrc"
    elif [[ -f "$HOME/.bashrc" ]]; then
        SHELL_RC="$HOME/.bashrc"
    else
        SHELL_RC=""
    fi

    if [[ -n "$SHELL_RC" ]]; then
        echo -e "  Tambahkan baris ini ke ${DIM}$SHELL_RC${RESET}:"
        echo -e "  ${YELLOW}export PATH=\"\$HOME/.local/bin:\$PATH\"${RESET}"
        echo ""
        read -rp "  Tambahkan otomatis sekarang? [y/N] " confirm
        if [[ "$confirm" =~ ^[Yy]$ ]]; then
            echo '' >> "$SHELL_RC"
            echo '# fractioncalc-cli' >> "$SHELL_RC"
            echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$SHELL_RC"
            success "PATH ditambahkan ke $SHELL_RC"
            warn "Jalankan: source $SHELL_RC  (atau buka terminal baru)"
        fi
    else
        warn "Tambahkan manual ke shell config kamu:"
        echo -e "  ${YELLOW}export PATH=\"\$HOME/.local/bin:\$PATH\"${RESET}"
    fi
else
    success "PATH sudah OK"
fi

echo ""
echo -e "${GREEN}  Instalasi selesai!${RESET}"
echo -e "  Jalankan dengan: ${YELLOW}fractioncalc${RESET}\n"
