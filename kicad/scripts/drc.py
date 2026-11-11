"""DRC report that works on KiCad 7 through 10.

KiCad 10's pcbnew.WriteDRCReport needs the full app running and crashes a
plain Python script, so there the board is saved to a scratch copy next to
the project (to pick up its rules) and checked with kicad-cli instead."""
import os, shutil, subprocess
import pcbnew


def report(board, rpt):
    if int(pcbnew.GetMajorMinorVersion().split('.')[0]) < 9:
        units = getattr(pcbnew, 'EDA_UNITS_MILLIMETRES', getattr(pcbnew, 'EDA_UNITS_MM', None))
        return pcbnew.WriteDRCReport(board, rpt, units, True)
    from export_jlc import _cli
    src = board.GetFileName()
    d, stem = os.path.dirname(src), os.path.splitext(os.path.basename(src))[0]
    tmp = os.path.join(d, '_drc_tmp')
    for ext in ('.kicad_pro', '.kicad_dru'):
        if os.path.exists(os.path.join(d, stem + ext)):
            shutil.copy(os.path.join(d, stem + ext), tmp + ext)
    try:
        pcbnew.SaveBoard(tmp + '.kicad_pcb', board)
        board.SetFileName(src)
        subprocess.run([_cli(), 'pcb', 'drc', '-o', rpt, tmp + '.kicad_pcb'], capture_output=True, check=True)
    finally:
        for ext in ('.kicad_pcb', '.kicad_pro', '.kicad_dru', '.kicad_prl'):
            if os.path.exists(tmp + ext):
                os.remove(tmp + ext)
    return True
