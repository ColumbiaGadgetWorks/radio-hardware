# Handoff: KOPN 89.5 jar radio

Notes for whoever picks this up next. They cover what isn't obvious from the repo itself. The full plan, BOM, costs and decisions are in `docs/plan_template.html`, which is published as https://claude.ai/artifact/CRWw9qmzpc6f2tXjvngTVT and rebuilt with `python3 docs/build_plan.py`.

## State

- `master` = `speaker-top-mount` = c0189be. Everything is merged.
- The board routes clean: 0 unconnected, only 2 cosmetic silk-over-pad warnings.
- The order files in `kicad/jlcpcb/` (Gerber zip, `BOM.csv`, `CPL.csv`) are current and have been sent to the user.
- The user is about to order **30 boards now and 30 later**. KOPN quote: $455 for the first 30 and $386 for the second 30 (section 05 of the plan).
- No boards have been built yet. There is no prototype run.

## Rev B bring-up (2026-11-10) and rev C changes

- **Batch 1 (rev B) boards work after a fix.** As built (R2 82k / R3 11k, ratio 0.119) they gave only static. The `87 + 21 x ratio` tuning law was a guess and is wrong. A trimmer on RV2 showed KOPN plays for TUNE2/TUNE1 ratios 0.150-0.176. Power, band select (FM3) and audio were all fine.
- **Rev B rework:** about 180-200k across the RV2 holes, square hole (TUNE1) to middle hole (TUNE2), with R2/R3 left in place. The user built (220k || 470k) + 47k = 197k and KOPN plays.
- **Rev C (board rebuilt and routed 2026-11-11 on Windows/KiCad 10; 0 unconnected, 0 silk warnings; order files regenerated, not committed):**
  - USB-C cable slot: a 14 x 7.5 mm stadium cut-out (Edge.Cuts, `gen_pcb.py` after the outline) centred at (-26.5, -17.75), long axis at 125 deg, below the CGW logo. It lets a power bank sit inside the jar with its USB-C plug fed up to J2; it takes a typical 12.3 x 6.5 mm plug overmold with ~0.5-0.8 mm per side. It is the largest slot that fits between the LiPo end, the speaker ring and the jar wall (15 x 8 does not). Bottom silk now reads rev C.
  - R2/R3 are now 51k / 10k (ratio 0.165, both Basic) in `circuit.py`. `kicad/jlcpcb/BOM.csv`, `docs/bom-check.csv` and the plan were hand-edited to match. Stock for C23196 and C25804 has not been re-checked.
  - ANT1 (whip M3 mount) moved from (22.5, 24.0) to (22.5, 23.1): only 0.64 mm further in (pad edge radius 36.15 -> ~35.5 mm). The user chose to keep the RV2 trimmer footprint, which blocks a bigger move. RV2 itself moved 0.75 mm down to (26.5, 17.38), so the rev B rework-location pictures (`docs/img/r2-r3-location.svg`, `tune-test-points.svg`) are for rev B only.
  - C22 moved 1 mm / turned 90 deg to clear the bigger J3 pad. Every other part is at its rev B spot.
  - J3 wire hole is now 2.0 mm drill / 3.4 mm pad (`Antenna_Wire_Solder_D2.0`, `fplib.ant_solder_tie`), so it fits 18 AWG and thicker.
  - **Still to do:** run `build.py --route` on a machine with KiCad and freerouting (the user's Windows PC has neither). Then export, render, `jlcdb.py check`, and rebuild the plan. RV2, D4, R1, C5 and nearby parts will be re-placed by `place.py` around the moved whip. Check that the result is sensible.
- Waiting on the user's report with batteries and the proper speakers.

## Open items before or at ordering

1. **JLC order-number mark.** There is no "JLCJLCJLCJLC" marker on the board. Either the user picks "Remove mark" at checkout, or a marker is added on the inside face (silkscreen only; re-export, no re-route). Offered to the user, no answer yet.
2. **F1 resettable fuse (optional).** If the user buys unprotected cells, swap F1's 0R (C17888) for the SMD1206B110TFT (C269119). This is a BOM-only change. Offered, no answer yet.
3. **Si4825 (C2654605) stock.** It isn't in the jlcparts mirror. The user saw 96 at JLC earlier. Pot C18213422 had about 64. Suggested pre-buying 30 of each into the user's JLC parts inventory for batch 2.
4. **JLC preview checks.** The user must check these in JLC's assembly preview:
   - J2 (PH socket) mouth faces the plug cutout. Its rotation is unverified: we had no datasheet, and the footprint is KiCad's JST S2B-PH-SM4-TB.
   - RV1 and J1 offsets (`POS_CORR` in `export_jlc.py`).
   - IC pin-1 marks (`ROT_CORR`: SOIC/ESOP −90, SOT-23 +180). The user confirmed these on an earlier revision.
5. **US duty.** The user should check whether the JLC and LCSC checkouts include it.

## Decisions and context given only in chat

- **Ordering route:** the JLC order ships to LCSC's HK warehouse via the "combine with LCSC order" option. The speakers (63× C22371323, HDK-4008BB-2) are bought on LCSC and combined. JLC's parts store is PCBA-only.
- **Battery:**
  - 102050 LiPo, 1000 mAh, on a PH2.0 plug. User quote: $47.49 for 30. Leads are long enough (confirmed).
  - Polarity is set with 1206 0R jumpers: STD = R23/R24 fitted (pin 2 = +), SWAP = R25/R26 (DNP). Fit one pair only.
  - The user may buy bare-wire cells and crimp them. Advice given: PHR-2 housings, SPH-002T terminals, Engineer PA-09 crimper, 24–26 AWG leads, crimp one wire at a time.
- **XB8089D (U6) stays fitted.** It is a full protection IC (4.25 V / 2.5 V / overcurrent / short / reverse), so unprotected cells are OK. The fuse (F1) and NTC (R20/RT1) are optional extra layers.
- **Speaker:**
  - Hand-soldered by the user, then 3 dabs of hot glue or silicone at the rim.
  - Polarity doesn't matter: one speaker driven by a bridge-tied (BTL) amp.
  - JLC could hand-solder it with a "≤3 s per joint" note, but this hasn't been chosen.
- **Antenna:**
  - No whip for now. 75 cm of 24 AWG stranded wire is soldered in J3 (ANT), hot-glued at the hole, and spiralled loosely inside the jar.
  - The ANT1 M3 whip mount is kept for later.
- **Jars:**
  - Wide-mouth **quart**, $19.99 per 12: buy 36 now and 24 later.
  - Regular-mouth jars don't fit.
- **No extra vents and don't seal.** The plug cutout gap vents the jar, which matters for LiPo safety.
- **Shopping list beyond PCBs, speakers, cells and foam tape:**
  - knobs (6 mm D-shaft, not yet in the user's budget)
  - 24 AWG stranded wire (about 25 m)
  - hot glue
  - solder
- **KOPN logo:** traced from KOPN's `.ai` (`kicad/artwork/kopn-circle-logo.ai`) with `logo2fp.py ... disc`.

## Working notes (tools and environment)

- **Building the board:** `cd kicad/scripts && FREEROUTING_JAR=<path> python3 build.py --route`, then `export_jlc.py`, `render.py`, `jlcdb.py check --qty 5 50 --csv ../../docs/bom-check.csv`, and finally `docs/build_plan.py`.
  - Freerouting 1.9 needs xvfb. The jar was kept in the session scratchpad and is not in the repo, so download Freerouting v1.9.0 again.
  - A route takes about 15–20 minutes.
- **Re-routing:** placement is deterministic, but `build.py` always rewrites the board. For a silkscreen-only change, edit the routed board with pcbnew in a fresh process instead of rebuilding.
- **Windows / KiCad 10 (used for rev C):** KiCad's own Python (`%LOCALAPPDATA%/Programs/KiCad/10.0/bin/python.exe`, with shapely, numpy, pillow, openpyxl pip-installed); `kicad-cli.exe` sits beside it and is found automatically. Freerouting 1.9 runs without xvfb on Windows; the whole route takes about 3 minutes.
  - The scripts carry compatibility shims for API changes: `SetField` (fields are hidden via `gen_pcb.set_hidden_field`, else LCSC/MPN print on the silkscreen), `SetDoNotAllowZoneFills`, `GetBoardPolygonOutlines(o, False)`, and via `GetWidth(layer)` (calling it without a layer pops a modal wx alert that hangs the script).
  - `pcbnew.WriteDRCReport` segfaults outside the GUI on KiCad 9+, so `scripts/drc.py` runs `kicad-cli pcb drc` on a scratch copy instead.
  - KiCad 10 reports about 12 copper-to-edge warnings at the USB-C and speaker cut-outs (rev B shows the same; after the cable slot the smallest is 0.25 mm, all against the J2/J4 footprint edge markers, none at the slot; fine for JLC).
- **Placement seed:** `kicad/scripts/place_seed.json` holds the shipped rev B positions. Parts in it stay put unless they hit a fixed part, a hole or a keepout (`place.legalize(trusted=...)`), so a rebuild no longer reshuffles the board. Re-export it from a new shipped board when placement changes on purpose.
- **Freerouting varies run to run:** if a VSW leftover remains, just rerun `build.py --route` (rev C: the second run was clean).
- **Router leftovers:** occasionally a VSW joint is left missing its via. Fix it by hand (add a via plus a short segment), then re-run DRC in a separate process.
- **KiCad 7 SWIG quirks:**
  - Don't `LoadBoard` twice in one process.
  - Don't remove tracks and then run DRC in the same process.
- **Killing jobs:** never use `pkill -f` with a pattern that matches your own command. Use `pgrep -f "build[.]py --route"`.
- **JLC parts database:** `~/.cache/jlcdb/cache.sqlite3`, table `jlc_components`, built with `jlcdb.py fetch`. It isn't in the repo, and its data dates from late September 2026.
- **Network:** JLC/LCSC datasheet downloads are blocked by the proxy.
