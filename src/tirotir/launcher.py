"""Launcher module used by the EXE Builder and installed packages."""
import os, sys
from tirotir.cli import main

def run():
    entry=os.environ.get('TIROTIR_ENTRY')
    argv=['run',entry] if entry else sys.argv[1:]
    return main(argv)

if __name__=='__main__':
    raise SystemExit(run())
