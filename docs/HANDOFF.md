# Handoff: KOPN 89.5 jar radio

Notes for whoever picks this up next. They cover what isn't obvious from the repo itself. The full plan, BOM, costs and decisions are in `docs/plan_template.html`, which is published as https://claude.ai/artifact/CRWw9qmzpc6f2tXjvngTVT and rebuilt with `python3 docs/build_plan.py`.

## State

- `master` = `speaker-top-mount` = c0189be. Everything is merged.
- The board routes clean: 0 unconnected, only 2 cosmetic silk-over-pad warnings.
- The order files in `kicad/jlcpcb/` (Gerber zip, `BOM.csv`, `CPL.csv`) are current and have been sent to the user.
- The user is about to order **30 boards now and 30 later**. KOPN quote: $455 for the first 30 and $386 for the second 30 (section 05 of the plan).
- No boards have been built yet. There is no prototype run.

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
- **Router leftovers:** occasionally a VSW joint is left missing its via. Fix it by hand (add a via plus a short segment), then re-run DRC in a separate process.
- **KiCad 7 SWIG quirks:**
  - Don't `LoadBoard` twice in one process.
  - Don't remove tracks and then run DRC in the same process.
- **Killing jobs:** never use `pkill -f` with a pattern that matches your own command. Use `pgrep -f "build[.]py --route"`.
- **JLC parts database:** `~/.cache/jlcdb/cache.sqlite3`, table `jlc_components`, built with `jlcdb.py fetch`. It isn't in the repo, and its data dates from late September 2026.
- **Network:** JLC/LCSC datasheet downloads are blocked by the proxy.
