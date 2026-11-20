# OpenCreator plugin example

A small, working OpenCreator plugin to copy when you make your own. It adds:

- **`OC_HELLO [NAME=...]`**: a G-code command from a Klippy module (`klippy/oc_hello.py`) that replies with
  the active extruder and its temperature. The module also has a status object, `printer.oc_hello`, with
  `greeting` and `count`.
- **`OC_HELLO_TOOL`**: a macro from the plugin's config (`config/hello.cfg`).
- **`GET /server/oc_hello`**: a Moonraker endpoint (`moonraker/oc_hello.py`), configured in `moonraker/hello.conf`.

## Install

On the printer (SSH):

```sh
oc-plugin install https://github.com/FlashForge-C5-Modding-Group/OpenCreator-Plugin-Example.git
```

Klipper and Moonraker restart by themselves, unless the printer is printing. Then try `OC_HELLO` in the
console, or open `http://<printer>/server/oc_hello`.

Updates show up in Fluidd/Mainsail's update manager as **oc-plugin-hello**, or run `oc-plugin update hello`.
`oc-plugin remove hello` removes it again.

## Layout

```
opencreator-plugin.json   the manifest (required)
klippy/oc_hello.py        Klippy module, loaded as [oc_hello]
config/hello.cfg          Klipper config, included while the plugin is enabled
moonraker/oc_hello.py     Moonraker component, loaded as [oc_hello]
moonraker/hello.conf      Moonraker config for it
```

Only the manifest is required. The folder names are up to you; the manifest says where things are.

## Manifest

```json
{
  "id": "hello",
  "name": "Hello OpenCreator",
  "version": "1.0.0",
  "description": "Example plugin: a Klippy module, a macro and a Moonraker endpoint.",
  "klippy_extras": ["klippy/oc_hello.py"],
  "klipper_config": "config/hello.cfg",
  "moonraker_components": ["moonraker/oc_hello.py"],
  "moonraker_config": "moonraker/hello.conf"
}
```

| Key | Required | |
| --- | --- | --- |
| `id` | yes | 2-41 lowercase letters, digits, `-` or `_`. The install folder and config names use it. |
| `name`, `version` | yes | Shown by `oc-plugin list`. Bump `version` with each release. |
| `description`, `author`, `homepage` | no | For people reading the manifest. |
| `klippy_extras` | no | Klippy modules (`.py` files). Each is loaded by the `[section]` of the same name. |
| `klipper_config` | no | One Klipper config file, included after the rest of `printer.cfg`. |
| `moonraker_components` | no | Moonraker components (`.py` files), loaded by the `[section]` of the same name. |
| `moonraker_config` | no | Moonraker config: your components' sections. |
| `restart` | no | Extra services to restart after install/update (`klipper`, `moonraker`). The ones your files need are restarted anyway. |
| `startup` | no | Programs started at boot and kept running: see **Startup items** below. |
| `scripts` | no | `install`, `update` and `uninstall` scripts: see **Install scripts** below. |
| `requires` | no | The printers and installs the plugin is made for: see **Compatibility** below. |

## Startup items

```json
"startup": [
  { "name": "server", "exec": "bin/server.sh", "type": "service" },
  { "name": "cleanup", "exec": "bin/cleanup.sh", "type": "once", "delay": 30, "args": ["--quick"] }
]
```

- `name`: 2-41 lowercase letters, digits, `-` or `_`, unique in the plugin.
- `exec`: a file in the plugin. `.sh` files run with `sh`, others have to be executable.
- `type`: `service` (default) is started again when it exits: 5 s later, doubling up to a minute while it keeps
  failing within a minute. `once` runs at boot and that's it.
- `args`: extra arguments. `delay`: seconds to wait before starting (0-600).

They start when the plugin is installed or enabled and at every boot (`startup.sh` runs `oc-plugin boot` after
OpenCreator's own startup scripts), stop when it's disabled or removed, and are restarted around an update.
Each item logs to `/tmp/oc-plugin-<id>-<name>.log`, which `oc-plugin logs <id> [name]` shows (`-f` to follow).
On the printer `/tmp` is in RAM, so a log is moved to `.log.1` once it passes 512 KB, when the item starts or
restarts. By hand: `oc-plugin status`, `oc-plugin start|stop|restart <id> [name]`.

## Install scripts

```json
"scripts": { "install": "bin/install.sh", "update": "bin/install.sh", "uninstall": "bin/uninstall.sh" }
```

- `install` runs once the plugin is in place, before anything is linked or started. If it fails, the plugin isn't installed.
- `update` runs after `oc-plugin update` pulled a new version; `uninstall` before `oc-plugin remove` deletes it.
  A failure there is only a warning.
- Up to 15 minutes each; their output is shown.

Scripts and startup items run in the plugin folder with these set:

| Variable | |
| --- | --- |
| `OC_PLUGIN_ID`, `OC_PLUGIN_DIR` | the plugin's id and folder |
| `OC_PLUGIN_DATA` | a folder for the plugin's own files (settings, downloads). Kept across updates; `oc-plugin remove` deletes it unless given `--keep-data` |
| `OC_CONFIG_DIR`, `OC_KLIPPER_DIR`, `OC_MOONRAKER_URL` | where Klipper's config and Kalico are, and Moonraker's address |

`/opt/bin` is on the `PATH`. Keep anything a user changes in `OC_PLUGIN_DATA`: the plugin folder is a git
checkout that updates replace.

## Compatibility

```json
"requires": { "models": ["Creator5Pro"], "modes": ["soc"] }
```

- `models`: `Creator5`, `Creator5Pro`. For hardware only one of them has, like the Pro's chamber heater.
- `modes`: `soc` (Klipper on the printer itself) or `sbc` (Klipper on a Raspberry Pi or other SBC). A printer
  tunneled to an SBC counts as `sbc`. There, only startup items and scripts run on the printer, with
  `OC_TUNNELED=1`, and `OC_MOONRAKER_URL` is the SBC's Moonraker (`oc-plugin moonraker --find`).

Leave a key out to allow everything. `oc-plugin install` refuses a plugin that isn't made for the printer, and
`oc-plugin update` keeps the old version if a new one isn't (or its manifest is broken). `--force` installs it
anyway. If the model can't be told, it only warns.

## Getting into the catalog

`oc-plugin search` lists the plugin catalog, `catalog.json` in
[opencreator-fs](https://github.com/FlashForge-C5-Modding-Group/opencreator-fs) under
`fs/usr/data/opencreator/plugin-manager/`. Open a pull request adding your plugin there:

```json
{
  "id": "hello",
  "name": "Hello OpenCreator",
  "official": false,
  "author": "You",
  "description": "One line on what it does.",
  "url": "https://github.com/you/your-plugin.git",
  "requires": { "modes": ["soc"] },
  "note": "Optional: anything people need to do after installing."
}
```

The `id` must match your manifest's. `official` is only set for plugins the OpenCreator team makes or checks.

Module names must be unique: a module named like one of Kalico's own (or another plugin's) is refused.
Prefix yours (this one uses `oc_hello`).

## Developing

Copy this repo, change `id`, `name` and the module names, and install your working folder straight from disk
to try it:

```sh
oc-plugin install /usr/data/my-plugin --no-restart
oc-plugin remove my-plugin
```

A folder install is a copy, so reinstall it after changes. It also isn't offered in the update manager; that needs
a git URL.

The full plugin system documentation is on the OpenCreator docs site, under **Plugins**.

## License

Any license, just needs to be compatible with GPLv3 as Klipper uses it
