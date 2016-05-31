Purpose
-------

ifstat_plot is a small wrapper that comes on top of [ifstat](http://gael.roualland.free.fr/ifstat/) to plot bandwidth
usage (both download and upload) over time.

Usage
-----

1. Change the variable `INTERFACE` to the interface you want to monitor.
2. Run `./ifstat_plot.py` to start monitoring traffic with ifstat.
3. Stop monitoring by hitting `Ctrl+C`.
4. The output table of ifstat is stored in `ifstat.txt` and the cognate plot
in `ifstat.pdf`.

Dependences
-----------
- ifstat
- python3
- python3-matplotlib

License
-------
[GPL v3](http://www.gnu.org/licenses/gpl.html).
