#!/bin/sh
# Uninstall script: takes the include out of moonraker.conf. oc-spoolman.conf stays, with
# your server address in it, for a later reinstall.
CONFIG_DIR="${OC_CONFIG_DIR:?OC_CONFIG_DIR is not set}"
MOONRAKER_CONF="$CONFIG_DIR/moonraker.conf"
if [ "$OC_TUNNELED" = 1 ]; then    # nothing was set up on a tunneled printer
    echo "This printer is tunneled: Klipper and Moonraker run on the SBC, so there's nothing to undo here."
    echo "To remove Spoolman from Klipper and Moonraker, uninstall the plugin on the SBC (oc-plugin remove oc_spoolman_integration there)."
    exit 0
fi

if [ -f "$MOONRAKER_CONF" ] && grep -qxF "[include oc-spoolman.conf]" "$MOONRAKER_CONF"; then
    grep -vxF "[include oc-spoolman.conf]" "$MOONRAKER_CONF" > "$MOONRAKER_CONF.tmp"
    cat "$MOONRAKER_CONF.tmp" > "$MOONRAKER_CONF" && rm -f "$MOONRAKER_CONF.tmp"
    echo "Removed [include oc-spoolman.conf] from moonraker.conf. Restart Moonraker to disconnect from Spoolman."
else
    echo "[include oc-spoolman.conf] wasn't found in moonraker.conf: nothing was done."
fi
if [ -f "$CONFIG_DIR/oc-spoolman.conf" ]; then
    echo "Kept $CONFIG_DIR/oc-spoolman.conf for a later reinstall."
fi
