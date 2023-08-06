# Copyright (C) 2023 Kian-Meng Ang
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""A console program that generates yearly calendar heatmap.

  website: https://github.com/kianmeng/heatmap_cli
  issues: https://github.com/kianmeng/heatmap_cli/issues
"""

import argparse
import datetime
import logging
import sys
from typing import Dict, Optional, Sequence

import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from heatmap_cli import __version__

# Suppress logging from matplotlib in debug mode
logging.getLogger("matplotlib").propagate = False
_logger = logging.getLogger(__name__)


def _build_parser(
    _args: Optional[Sequence[str]] = None,
) -> argparse.ArgumentParser:
    """Build the CLI parser."""
    parser = argparse.ArgumentParser(
        add_help=False,
        description=__doc__,
        formatter_class=lambda prog: argparse.RawTextHelpFormatter(
            prog,
            max_help_position=25,
        ),
    )

    parser.add_argument(
        "input_filename",
        help="csv filename",
        type=argparse.FileType("rb"),
        metavar="CSV_FILENAME",
    )

    parser.add_argument(
        "-yr",
        "--year",
        dest="year",
        type=int,
        default=datetime.datetime.today().year,
        help="filter by year from the CSV file (default: '%(default)s')",
        metavar="YEAR",
    )

    parser.add_argument(
        "-wk",
        "--week",
        dest="week",
        type=int,
        default=datetime.datetime.today().strftime("%W"),
        help=(
            "filter until week of the year from the CSV file "
            "(default: '%(default)s')"
        ),
        metavar="WEEK",
    )

    parser.add_argument(
        "-d",
        "--debug",
        default=False,
        action="store_true",
        dest="debug",
        help="show debugging log and stacktrace",
    )

    parser.add_argument(
        "-v",
        "--verbose",
        default=0,
        action="count",
        dest="verbose",
        help="show verbosity of debugging log, use -vv, -vvv for more details",
    )

    parser.add_argument(
        "-h",
        "--help",
        action="help",
        default=argparse.SUPPRESS,
        help="show this help message and exit",
    )

    parser.add_argument(
        "-V", "--version", action="version", version=f"%(prog)s {__version__}"
    )

    return parser


def _setup_logging(debug: bool = False) -> None:
    """Set up logging by level."""
    conf: Dict = {
        True: {
            "level": logging.DEBUG,
            "msg": "[%(asctime)s] %(levelname)s: %(name)s: %(message)s",
        },
        False: {"level": logging.INFO, "msg": "%(message)s"},
    }

    logging.basicConfig(
        level=conf[debug]["level"],
        stream=sys.stdout,
        format=conf[debug]["msg"],
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def _massage_data(config: argparse.Namespace) -> pd.core.frame.DataFrame:
    dataframe = pd.read_csv(
        config.input_filename, header=None, names=["date", "count"]
    )
    dataframe["date"] = pd.to_datetime(dataframe["date"])
    dataframe["weekday"] = dataframe["date"].dt.weekday + 1
    dataframe["week"] = dataframe["date"].dt.strftime("%W")
    dataframe["count"] = round(dataframe["count"], -2) / 100

    steps = dataframe[
        (dataframe["date"].dt.year == config.year)
        & (dataframe["week"] <= str(config.week).zfill(2))
    ]
    if steps.empty:
        raise ValueError("no data extracted from csv file")

    _logger.debug(max(steps["date"]).date())
    missing_df = pd.DataFrame(
        {
            "date": pd.date_range(
                start=max(steps["date"]).date() + datetime.timedelta(days=1),
                end=f"{config.year}-12-31",
            )
        }
    )
    missing_df["weekday"] = missing_df["date"].dt.weekday + 1
    missing_df["week"] = missing_df["date"].dt.strftime("%W")
    missing_df["count"] = 0

    steps = pd.concat([steps, missing_df], ignore_index=True)
    year_dataframe = steps.pivot_table(
        values="count", index=["weekday"], columns=["week"], fill_value=0
    )
    return year_dataframe


def _generate_heatmap(
    config: argparse.Namespace, dataframe: pd.core.frame.DataFrame
) -> None:
    # generating matplotlib graphs without a x-server
    # see http://stackoverflow.com/a/4935945
    mpl.use("Agg")

    cmap = "RdYlGn_r"
    _fig, axis = plt.subplots(figsize=(8, 5))
    axis.tick_params(axis="both", which="major", labelsize=9)
    axis.tick_params(axis="both", which="minor", labelsize=9)
    sns.heatmap(
        dataframe,
        ax=axis,
        annot=True,
        annot_kws={"fontsize": 9},
        fmt="d",
        linewidth=0.0,
        square=True,
        cmap=cmap,
        cbar_kws={
            "orientation": "horizontal",
            "label": f"colourmap: {cmap}, count: by hundred",
            "pad": 0.15,
        },
    )

    png_filename = (
        f"{config.year}_week_{config.week}_{cmap}"
        "_annotated_heatmap_of_total_daily_walked_steps.png"
    )

    plt.title(
        (
            "Total Daily Walking Steps Count Up to Week "
            f"{config.week} {config.year} (kianmeng.org)"
        ),
        fontsize=10,
    )
    plt.tight_layout()
    plt.savefig(
        png_filename,
        bbox_inches="tight",
        transparent=False,
        dpi=76,
    )
    _logger.info("generate heatmap png file: %s", png_filename)


def _run(config: argparse.Namespace) -> None:
    """Run the main flow.

    Args:
        config (argparse.Namespace): Config from command line arguments or
        config file.
    """
    _logger.debug(config)
    dataframe = _massage_data(config)
    _generate_heatmap(config, dataframe)


def main(args: Optional[Sequence[str]] = None) -> None:
    """Run the main program flow."""
    try:
        parser = _build_parser(args)
        parsed_args = parser.parse_args(args)
        _setup_logging(parsed_args.debug)
        _run(parsed_args)
    except Exception as error:
        _logger.error(
            "error: %s", getattr(error, "message", str(error)), exc_info=True
        )
        raise SystemExit(1) from None
