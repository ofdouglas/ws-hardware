#!/usr/bin/env python3
"""Check KiCad's exported connectivity against the power/USB capture intent.

This is a netlist/BOM/numbered-pad check, not ERC or electrical qualification.
Run from any directory; requires KiCad 7+ and its standard footprint libraries.
"""
import csv
import json
import re
import subprocess
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CAD = ROOT / 'boards/board1/kicad'


def check():
    expected = json.loads((CAD / 'capture_manifest.json').read_text())
    bom = {r['item_id']: r for r in csv.DictReader((ROOT / 'boards/board1/bom_internal.csv').open())}
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / 'board1.xml'
        subprocess.run(['kicad-cli', 'sch', 'export', 'netlist', '--format', 'kicadxml',
                        '-o', str(path), str(CAD / 'board1.kicad_sch')], check=True)
        root = ET.parse(path).getroot()
    components = {c.get('ref'): c for c in root.findall('./components/comp')}
    assert set(components) == set(expected), 'Physical component inventory differs'
    nets = {n.get('name'): {(p.get('ref'), p.get('pin')) for p in n.findall('node')}
            for n in root.findall('./nets/net')}
    pin_net = {p: n for n, pins in nets.items() for p in pins}
    libpins = {(p.get('lib'), p.get('part')): {n.get('num') for n in p.findall('./pins/pin')}
               for p in root.findall('./libparts/libpart')}
    pin_count = 0
    for ref, spec in expected.items():
        component = components[ref]
        fields = {f.get('name'): f.text for f in component.findall('./fields/field')}
        row = bom[spec['BOM_ID']]
        assert fields['BOM_ID'] == row['item_id'] and fields['MPN'] == row['mpn'], ref
        assert component.findtext('footprint') == spec['footprint'] == row['footprint'], ref
        source = component.find('libsource')
        assert set(spec['pins']) == libpins[(source.get('lib'), source.get('part'))], ref
        library, footprint = spec['footprint'].split(':')
        fp = Path('/usr/share/kicad/footprints') / (library + '.pretty') / (footprint + '.kicad_mod')
        pads = {a or b for a, b in re.findall(r'\(pad\s+(?:"([^"]+)"|([^\s()]+))', fp.read_text())}
        assert set(spec['pins']) <= pads, f'{ref}: missing numbered footprint pads'
        for pin, intended in spec['pins'].items():
            actual = pin_net.get((ref, pin))
            if intended is None:
                assert actual is None or (actual.startswith('unconnected-') and len(nets[actual]) == 1), (ref, pin, actual)
            else:
                assert actual and actual.rsplit('/', 1)[-1] == intended, (ref, pin, intended, actual)
            pin_count += 1
    # Explicit domain/polarity assertions supplement the captured manifest.
    assert pin_net['U4', '39'] != pin_net['U6', '14']
    assert len({pin_net['U4', p] for p in ['37', '38', '39', '40']}) == 4
    assert all(pin_net['U6', p] == 'PWREN_N' for p in ['1', '4', '10', '13'])
    assert pin_net['D1', '1'] == '/VBUS_RAW' and pin_net['D1', '2'] == 'GND'
    assert pin_net['U1', '5'] == pin_net['U1', '6'] == 'USB_5V'
    assert pin_net['U2', '3'] == pin_net['L1', '2'] == '3V3_SYS'
    for bid in {s['BOM_ID'] for s in expected.values()}:
        count = sum(s['BOM_ID'] == bid for s in expected.values())
        if bid in {'B1-B026', 'B1-B036'}:
            assert count == 1 and count < int(bom[bid]['quantity'])
        else:
            assert count == int(bom[bid]['quantity']), (bid, count)
    assert all(bom[bid]['quantity'] == '0' for bid in ['B1-B017', 'B1-B062'])
    print(f'PASS: {len(components)} physical parts; {pin_count} pins checked; net intent, '
          'domain separation, BOM MPN/footprints/counts and numbered footprint pads agree. Not ERC.')


if __name__ == '__main__':
    if (CAD / 'complete_manifest.json').exists():
        # Full-board checker preserves the original 52-part contract too.
        from check_board1_complete import main
        main()
    else:
        check()
