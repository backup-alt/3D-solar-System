#!/usr/bin/env python3
"""Print every known exoplanet that lies in its star's habitable zone.

By default the script queries the NASA Exoplanet Archive ``pscomppars``
table live, computes the habitable-zone (HZ) flux limits from the host
star's effective temperature with the Kopparapu et al. (2013/2014)
parameterisation, and prints a sorted table.  If the network is not
available it falls back to a bundled snapshot so the script still works
offline.

The HZ is model dependent, so each planet is labelled either
``conservative`` (runaway greenhouse to maximum greenhouse) or
``optimistic`` (recent Venus to early Mars).

Examples
--------
    python3 habitable_zone_planets.py
    python3 habitable_zone_planets.py --zone conservative
    python3 habitable_zone_planets.py --offline --max-distance 50
    python3 habitable_zone_planets.py --csv habitable_worlds.csv
"""

from __future__ import annotations

import argparse
import csv
import io
import math
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import date

TAP_URL = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync"
TAP_QUERY = (
    "select pl_name,hostname,disc_year,discoverymethod,pl_orbper,"
    "pl_orbsmax,pl_rade,pl_eqt,pl_insol,st_teff,st_rad,st_lum,"
    "st_spectype,sy_dist from pscomppars"
)
PARSEC_TO_LY = 3.26156
SOLAR_TEFF = 5772.0

SEFF_COEFFICIENTS = {
    "recent_venus": (1.7763, 1.4335e-4, 3.3954e-9, -7.6364e-12, -1.1950e-15),
    "runaway_greenhouse": (1.0385, 1.2456e-4, 1.4612e-8, -7.6345e-12, -1.7511e-15),
    "maximum_greenhouse": (0.3507, 5.9578e-5, 1.6707e-9, -3.0058e-12, -5.1925e-16),
    "early_mars": (0.3207, 5.4471e-5, 1.5275e-9, -2.1709e-12, -3.8282e-16),
}

FALLBACK_CATALOG = [
    {"name": "Proxima Centauri b", "host": "Proxima Centauri", "ly": 4.24, "period": 11.19, "radius": 1.27, "teff": 3042, "method": "Radial Velocity", "year": 2016, "zone": "conservative"},
    {"name": "Ross 128 b", "host": "Ross 128", "ly": 11.01, "period": 9.87, "radius": 1.10, "teff": 3192, "method": "Radial Velocity", "year": 2017, "zone": "optimistic"},
    {"name": "GJ 273 b", "host": "Luyten's Star", "ly": 12.20, "period": 18.65, "radius": 1.18, "teff": 3382, "method": "Radial Velocity", "year": 2017, "zone": "optimistic"},
    {"name": "Teegarden's Star b", "host": "Teegarden's Star", "ly": 12.50, "period": 4.91, "radius": 1.05, "teff": 2904, "method": "Radial Velocity", "year": 2019, "zone": "conservative"},
    {"name": "Teegarden's Star c", "host": "Teegarden's Star", "ly": 12.50, "period": 11.41, "radius": 1.11, "teff": 2904, "method": "Radial Velocity", "year": 2019, "zone": "optimistic"},
    {"name": "Wolf 1061 c", "host": "Wolf 1061", "ly": 14.05, "period": 17.87, "radius": 1.66, "teff": 3342, "method": "Radial Velocity", "year": 2015, "zone": "optimistic"},
    {"name": "GJ 1002 b", "host": "GJ 1002", "ly": 15.80, "period": 10.35, "radius": 1.08, "teff": 3024, "method": "Radial Velocity", "year": 2022, "zone": "conservative"},
    {"name": "GJ 1002 c", "host": "GJ 1002", "ly": 15.80, "period": 21.20, "radius": 1.03, "teff": 3024, "method": "Radial Velocity", "year": 2022, "zone": "optimistic"},
    {"name": "GJ 667 C c", "host": "GJ 667 C", "ly": 23.62, "period": 28.14, "radius": 1.54, "teff": 3350, "method": "Radial Velocity", "year": 2012, "zone": "optimistic"},
    {"name": "TRAPPIST-1 d", "host": "TRAPPIST-1", "ly": 40.66, "period": 4.05, "radius": 0.79, "teff": 2566, "method": "Transit", "year": 2016, "zone": "optimistic"},
    {"name": "TRAPPIST-1 e", "host": "TRAPPIST-1", "ly": 40.66, "period": 6.10, "radius": 0.92, "teff": 2566, "method": "Transit", "year": 2017, "zone": "conservative"},
    {"name": "TRAPPIST-1 f", "host": "TRAPPIST-1", "ly": 40.66, "period": 9.21, "radius": 1.05, "teff": 2566, "method": "Transit", "year": 2017, "zone": "conservative"},
    {"name": "TRAPPIST-1 g", "host": "TRAPPIST-1", "ly": 40.66, "period": 12.35, "radius": 1.15, "teff": 2566, "method": "Transit", "year": 2017, "zone": "conservative"},
    {"name": "HD 40307 g", "host": "HD 40307", "ly": 41.84, "period": 197.80, "radius": 7.09, "teff": 4977, "method": "Radial Velocity", "year": 2012, "zone": "optimistic"},
    {"name": "LHS 1140 b", "host": "LHS 1140", "ly": 48.86, "period": 24.74, "radius": 1.73, "teff": 3131, "method": "Transit", "year": 2017, "zone": "optimistic"},
    {"name": "TOI-700 d", "host": "TOI-700", "ly": 101.40, "period": 37.43, "radius": 1.19, "teff": 3480, "method": "Transit", "year": 2020, "zone": "conservative"},
    {"name": "K2-18 b", "host": "K2-18", "ly": 124.20, "period": 32.94, "radius": 2.61, "teff": 3457, "method": "Transit", "year": 2015, "zone": "optimistic"},
    {"name": "TOI-715 b", "host": "TOI-715", "ly": 137.00, "period": 19.29, "radius": 1.55, "teff": 3070, "method": "Transit", "year": 2024, "zone": "conservative"},
    {"name": "Kepler-1649 c", "host": "Kepler-1649", "ly": 301.00, "period": 19.54, "radius": 1.06, "teff": 3240, "method": "Transit", "year": 2020, "zone": "conservative"},
    {"name": "Kepler-186 f", "host": "Kepler-186", "ly": 579.00, "period": 129.94, "radius": 1.17, "teff": 3755, "method": "Transit", "year": 2014, "zone": "conservative"},
    {"name": "Kepler-1229 b", "host": "Kepler-1229", "ly": 769.00, "period": 86.83, "radius": 1.40, "teff": 3784, "method": "Transit", "year": 2016, "zone": "conservative"},
    {"name": "Kepler-62 f", "host": "Kepler-62", "ly": 980.00, "period": 267.29, "radius": 1.46, "teff": 4925, "method": "Transit", "year": 2013, "zone": "conservative"},
    {"name": "Kepler-442 b", "host": "Kepler-442", "ly": 1206.00, "period": 112.31, "radius": 1.34, "teff": 4402, "method": "Transit", "year": 2015, "zone": "conservative"},
    {"name": "Kepler-452 b", "host": "Kepler-452", "ly": 1800.00, "period": 384.84, "radius": 1.63, "teff": 5757, "method": "Transit", "year": 2015, "zone": "conservative"},
    {"name": "Kepler-1638 b", "host": "Kepler-1638", "ly": 2860.00, "period": 259.87, "radius": 1.87, "teff": 5713, "method": "Transit", "year": 2016, "zone": "conservative"},
]


def as_float(value):
    if value is None:
        return None
    text = str(value).strip()
    if not text or text.lower() in {"nan", "null", "none", ""}:
        return None
    try:
        number = float(text)
    except ValueError:
        return None
    return number if math.isfinite(number) else None


def hz_flux_limits(teff):
    teff = min(max(teff, 2600.0), 7200.0)
    t = teff - SOLAR_TEFF
    limits = {}
    for name, coefficients in SEFF_COEFFICIENTS.items():
        limits[name] = sum(c * t ** i for i, c in enumerate(coefficients))
    return limits


def stellar_flux(insol, semi_major_axis, teff, radius, log_luminosity):
    if insol is not None and insol > 0:
        return insol
    if semi_major_axis is None or semi_major_axis <= 0:
        return None
    if log_luminosity is not None:
        luminosity = 10.0 ** log_luminosity
    elif radius is not None and teff is not None:
        luminosity = radius ** 2 * (teff / SOLAR_TEFF) ** 4
    else:
        return None
    return luminosity / semi_major_axis ** 2


def classify_zone(flux, teq, teff):
    if flux is not None and teff is not None:
        limits = hz_flux_limits(teff)
        if limits["runaway_greenhouse"] >= flux >= limits["maximum_greenhouse"]:
            return "conservative"
        if limits["recent_venus"] >= flux >= limits["early_mars"]:
            return "optimistic"
        return None
    if teq is not None:
        if 180.0 <= teq <= 310.0:
            return "conservative"
        if 150.0 <= teq <= 330.0:
            return "optimistic"
    return None


def fetch_live(timeout):
    params = urllib.parse.urlencode({"query": TAP_QUERY, "format": "csv"})
    request = urllib.request.Request(
        f"{TAP_URL}?{params}",
        headers={"User-Agent": "habitable-zone-planets/1.0"},
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        text = response.read().decode("utf-8", "replace")

    lines = [line for line in text.splitlines() if line.strip()]
    try:
        start = next(i for i, line in enumerate(lines) if "pl_name" in line)
    except StopIteration:
        raise RuntimeError("Unexpected response from the NASA Exoplanet Archive")

    planets = []
    for row in csv.DictReader(io.StringIO("\n".join(lines[start:]))):
        teff = as_float(row.get("st_teff"))
        flux = stellar_flux(
            as_float(row.get("pl_insol")),
            as_float(row.get("pl_orbsmax")),
            teff,
            as_float(row.get("st_rad")),
            as_float(row.get("st_lum")),
        )
        teq = as_float(row.get("pl_eqt"))
        zone = classify_zone(flux, teq, teff)
        if zone is None:
            continue
        distance_pc = as_float(row.get("sy_dist"))
        planets.append(
            {
                "name": (row.get("pl_name") or "").strip(),
                "host": (row.get("hostname") or "").strip(),
                "ly": distance_pc * PARSEC_TO_LY if distance_pc else None,
                "period": as_float(row.get("pl_orbper")),
                "radius": as_float(row.get("pl_rade")),
                "teff": teff,
                "method": (row.get("discoverymethod") or "").strip(),
                "year": int(as_float(row.get("disc_year")) or 0) or None,
                "zone": zone,
            }
        )
    return planets


def fallback_planets():
    return [dict(planet) for planet in FALLBACK_CATALOG]


def filter_planets(planets, args):
    selected = []
    for planet in planets:
        if args.zone == "conservative" and planet["zone"] != "conservative":
            continue
        if args.min_year and (planet["year"] or 0) < args.min_year:
            continue
        if args.max_distance is not None:
            if planet["ly"] is None or planet["ly"] > args.max_distance:
                continue
        selected.append(planet)

    selected.sort(key=lambda p: (p["ly"] is None, p["ly"] if p["ly"] is not None else 0.0, p["name"]))
    for index, planet in enumerate(selected, start=1):
        planet["index"] = index
    if args.limit:
        selected = selected[: args.limit]
    return selected


def text(value, digits=1, suffix=""):
    if value is None:
        return "-"
    if isinstance(value, int):
        return f"{value}{suffix}"
    return f"{value:.{digits}f}{suffix}"


def print_table(planets, source):
    if not planets:
        print("No planets matched the requested filters.")
        return

    headers = ("#", "Planet", "Host star", "Distance", "Period", "Radius", "Teff", "Method", "Year", "HZ zone")
    rows = []
    for planet in planets:
        rows.append(
            (
                str(planet["index"]),
                planet["name"],
                planet["host"],
                text(planet["ly"], 2, " ly"),
                text(planet["period"], 2, " d"),
                text(planet["radius"], 2),
                text(int(planet["teff"]) if planet["teff"] else None, 0, " K"),
                planet["method"] or "-",
                text(planet["year"], 0),
                planet["zone"],
            )
        )

    widths = [max(len(headers[i]), *(len(row[i]) for row in rows)) for i in range(len(headers))]
    widths = [min(width, 34) for width in widths]

    def fmt(row):
        cells = []
        for value, width in zip(row, widths):
            if len(value) > width:
                value = value[: width - 1] + "\u2026"
            cells.append(value.ljust(width))
        return "  ".join(cells).rstrip()

    conservative = sum(1 for planet in planets if planet["zone"] == "conservative")
    optimistic = len(planets) - conservative

    print(f"Habitable-zone planets - {source}")
    print(f"Generated {date.today().isoformat()} | {len(planets)} worlds "
          f"({conservative} conservative, {optimistic} optimistic)")
    print()
    print(fmt(headers))
    print(fmt(tuple("-" * width for width in widths)))
    for row in rows:
        print(fmt(row))
    print()
    print("Conservative: runaway-greenhouse to maximum-greenhouse flux limits.")
    print("Optimistic:   recent-Venus to early-Mars limits. Radii in Earth radii.")


def write_csv(path, planets):
    with open(path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["planet", "host_star", "distance_ly", "period_days", "radius_earth", "teff_k", "method", "year", "hz_zone"])
        for planet in planets:
            writer.writerow([
                planet["name"],
                planet["host"],
                planet["ly"],
                planet["period"],
                planet["radius"],
                planet["teff"],
                planet["method"],
                planet["year"],
                planet["zone"],
            ])


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        description="List known exoplanets inside their host star's habitable zone.",
    )
    parser.add_argument("--offline", action="store_true", help="skip the live NASA query and use the bundled snapshot")
    parser.add_argument("--zone", choices=("optimistic", "conservative"), default="optimistic",
                        help="which habitable-zone definition to use (default: optimistic, includes conservative)")
    parser.add_argument("--min-year", type=int, default=None, help="only include planets discovered in this year or later")
    parser.add_argument("--max-distance", type=float, default=None, help="only include planets within this many light-years")
    parser.add_argument("--limit", type=int, default=None, help="print at most this many planets")
    parser.add_argument("--timeout", type=float, default=30.0, help="live query timeout in seconds (default: 30)")
    parser.add_argument("--csv", metavar="PATH", help="also write the results to a CSV file")
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    source = "NASA Exoplanet Archive (live)"
    planets = None

    if not args.offline:
        try:
            planets = fetch_live(args.timeout)
        except (urllib.error.URLError, TimeoutError, RuntimeError, OSError) as exc:
            print(f"Live query unavailable ({exc}); using the bundled snapshot.", file=sys.stderr)

    if not planets:
        planets = fallback_planets()
        source = "bundled snapshot (may be outdated; run online for current data)"

    selected = filter_planets(planets, args)
    print_table(selected, source)

    if args.csv:
        write_csv(args.csv, selected)
        print(f"\nSaved {len(selected)} rows to {args.csv}")


if __name__ == "__main__":
    main()
