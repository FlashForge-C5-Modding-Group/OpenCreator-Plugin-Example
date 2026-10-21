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

GPLv3, like Klipper and Moonraker, which these modules are loaded into.
