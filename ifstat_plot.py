#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  ifstat_plot.py
#
#  Copyright 2016 seb-ksl <seb@gelis.ch>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, see <http://www.gnu.org/licenses/>.
#
#

import subprocess
import sys
import logging
logging.basicConfig(level=logging.DEBUG, format="%(message)s")
logger = logging.getLogger("bandwidth_live_mon")
try:
    import matplotlib.pyplot as plt
except:
    logger.critical("Could not load matplotlib module for python3.")


INTERFACE = "eth0"


def start_ifstat():
    outf = open("ifstat.txt", "w")
    try:
        logger.debug("Running ifstat...")
        subprocess.call(["ifstat", "-ntb", "-i", INTERFACE], stdout=outf)
    except FileNotFoundError:
        logger.critical("Could not find ifstat.")
        sys.exit(1)
    except KeyboardInterrupt:
        logger.debug("Stopped ifstat.")
    finally:
        outf.close()


def graph():
    dates, rx, tx = [], [], []
    logger.debug("Parsing ifstat output.")
    with open("ifstat.txt", "r") as f:
        for l in f:
            if (not l.startswith(" ")) and (not l.startswith("H")):
                splitl = l.split()
                dates.append(splitl[0])
                rx.append(splitl[1])
                tx.append(splitl[2])

    ticks_spacing_dict = {(1800, 7199): ("00", "05", "10", "15", "20", "25",
                                         "30", "35", "40", "45", "50", "55"),
                          (7200, 17999): ("00", "15", "30", "45"),
                          (18000, 71999): ("00", "30"),
                          (72000, 1e8): ("00",)}

    ticks_spacing = ()
    for timespan in ticks_spacing_dict.keys():
        if timespan[0] < len(dates) < timespan[1]:
            ticks_spacing = ticks_spacing_dict[timespan]

    x_ticks, x_dates = [], []
    for (tick, date) in enumerate(dates):
        if len(ticks_spacing) > 0:
            if (date.split(":")[1] in ticks_spacing and
               date.split(":")[2] == "00"):
                x_ticks.append(tick)
                x_dates.append(date)
        else:
            if date.split(":")[2] == "00":
                x_ticks.append(tick)
                x_dates.append(date)

    logger.debug("Drawing figure.")
    fig = plt.figure(figsize=(10, 10))
    ax_rx = fig.add_subplot(211)
    ax_rx.set_xlabel("Time")
    ax_rx.set_xticks(x_ticks)
    ax_rx.set_xticklabels(x_dates, rotation=90)
    ax_rx.set_ylabel("RX in KB/s")

    try:
        ax_rx.plot(rx)
    except ValueError:
        logger.critical("Could not plot your stats properly. "
                        "Please check your interface ({}).".format(INTERFACE))
        sys.exit(1)

    ax_tx = fig.add_subplot(212)
    ax_tx.set_xlabel("Time")
    ax_tx.set_xticks(x_ticks)
    ax_tx.set_xticklabels(x_dates, rotation=90)
    ax_tx.set_ylabel("TX in KB/s")
    ax_tx.plot(tx)

    plt.tight_layout()
    logger.debug("Rendering figure.")
    plt.savefig("ifstat.pdf")
    logger.info("Figure saved to ifstat.pdf")


def main():
    start_ifstat()
    graph()

if __name__ == '__main__':
    main()
