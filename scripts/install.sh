#!/bin/sh
# Install and update script: puts oc-spoolman.conf in the config folder (an existing one
# is kept) and includes it from moonraker.conf. Safe to run more than once.
set -e

CONFIG_DIR="${OC_CONFIG_DIR:?OC_CONFIG_DIR is not set}"
MOONRAKER_CONF="$CONFIG_DIR/moonraker.conf"
SPOOLMAN_CONF="$CONFIG_DIR/oc-spoolman.conf"
INCLUDE="[include oc-spoolman.conf]"

# On a printer tunneled to an SBC, Klipper and Moonraker run on the SBC and oc-plugin
# links nothing here, so the plugin would do nothing. It belongs on the SBC.
if [ "$OC_TUNNELED" = 1 ]; then
    echo "This printer is tunneled: Klipper and Moonraker run on the SBC." >&2
    echo "Install the plugin on the SBC instead (oc-plugin install ... there)." >&2
    exit 1
fi

if [ ! -f "$MOONRAKER_CONF" ]; then
    echo "There's no moonraker.conf in $CONFIG_DIR" >&2
    exit 1
fi

# A [spoolman] section in moonraker.conf itself would be defined twice.
if grep -q '^\[spoolman\]' "$MOONRAKER_CONF"; then
    echo "moonraker.conf has its own [spoolman] section already: using that, nothing added."
    exit 0
fi

# OpenCreator's default moonraker.conf has a commented-out [spoolman] example.
if grep -q '^#[[:space:]]*\[spoolman\]' "$MOONRAKER_CONF"; then
    echo "moonraker.conf has OpenCreator's default [spoolman] section, commented out. Leave it commented out:"
    echo "Spoolman's address goes in oc-spoolman.conf, and uncommenting both defines [spoolman] twice,"
    echo "which might prevent the machine from starting correctly."
fi

if [ -f "$SPOOLMAN_CONF" ]; then
    echo "Keeping the existing $SPOOLMAN_CONF"
else
    cp "${OC_PLUGIN_DIR:-.}/moonraker/oc-spoolman.conf" "$SPOOLMAN_CONF"
    echo "Created $SPOOLMAN_CONF: put your Spoolman server's address in it."
fi

if grep -qxF "$INCLUDE" "$MOONRAKER_CONF"; then
    echo "moonraker.conf includes oc-spoolman.conf already."
else
    printf '\n%s\n' "$INCLUDE" >> "$MOONRAKER_CONF"
    echo "Added $INCLUDE to moonraker.conf"
fi
