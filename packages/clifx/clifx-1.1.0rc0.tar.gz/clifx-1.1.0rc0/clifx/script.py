# built in
import json
from pathlib import Path

# site 
import click
from lifxlan import LifxLAN

# package
from .lan import fetch_device
from .__version__ import __version__

DEFAULT_RETRY_MAX_ATTEMPTS = 5
DEFAULT_RETRY_WAIT_PERIOD = 0.5  # in seconds
TMP_FILE_FILEPATH = '/tmp/CLIFX-tmp'
EMOJIS = True

defaults = {
    "label": "Strip",
    "hue": 0,
    "saturation": 0,
    "value": 10,
    "kelvin": 3500
}

if Path(TMP_FILE_FILEPATH).exists():
    with open(TMP_FILE_FILEPATH, 'r') as f:
        _prev_command_config = json.load(f)["previous_command_config"]
        for key in _prev_command_config:
            defaults[key] = _prev_command_config[key]

@click.command()
@click.option(
    "--label",
    "-l",
    prompt=f"{'🏷️  ' if EMOJIS else ''}Device label (case sensitive)",
    help="Label of the device to update",
    default=defaults["label"],
)
@click.option(
    "--hue",
    "-h",
    prompt=f"{'🌈 ' if EMOJIS else ''}Hue",
    help="New hue",
    default=defaults["hue"],
    type=click.IntRange(-1, 100, clamp=True),
    show_choices=True,
)
@click.option(
    "--saturation",
    "-s",
    prompt=f"{'💧 ' if EMOJIS else ''}Saturation",
    default=defaults["saturation"],
    help="New saturation",
    type=click.IntRange(-1, 100, clamp=True),
)
@click.option(
    "--value",
    "-v",
    prompt=f"{'💡 ' if EMOJIS else ''}Value",
    help="New value (brightness)",
    default=defaults["value"],
    type=click.IntRange(-1, 100, clamp=True),
)
@click.option(
    "--kelvin",
    "-k",
    prompt=f"{'🌡️  ' if EMOJIS else ''}Kelvin",
    help="New kelvin",
    default=defaults["kelvin"],
    type=click.IntRange(1500, 9000, clamp=True),
)
@click.version_option(
    None,
    '--version',
    '-V',
    message=f"%(package)s {__version__} from {__file__}",
)
def setColor(label, hue, saturation, value, kelvin):
    """Set the color of a device by label."""
    # instantiate lifxlan object
    with open(TMP_FILE_FILEPATH, 'w') as f:
        json.dump({
            "previous_command_config": {
                "label": label,
                "hue": hue,
                "saturation": saturation,
                "value": value,
                "kelvin": kelvin
            }
        }, f)

    _lan = LifxLAN()

    click.echo(f"searching for device '{label}'...")
    _device = fetch_device(
        _lan,
        label,
        DEFAULT_RETRY_MAX_ATTEMPTS,
        DEFAULT_RETRY_WAIT_PERIOD
    )

    click.echo(f"getting color of '{label}'...")
    old_color = _device.get_color()
    click.echo(f"setting color of '{label}'...")
    new_color = [
        old_color[0] if hue == -1 else (hue / 100) * 65535,
        old_color[1] if saturation == -1 else (saturation / 100) * 65535,
        old_color[2] if value == -1 else (value / 100) * 65535,
        old_color[3] if kelvin == -1 else kelvin,  # FIXME: kelvin can't be -1 as option type is a clamped int range
    ]

    _device.set_power(1)
    _device.set_color(new_color)

def main():
    setColor()
