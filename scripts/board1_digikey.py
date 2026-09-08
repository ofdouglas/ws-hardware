#!/usr/bin/env python3
"""Audit the purchase CSV and optionally refresh its assembly references.

DigiKey catalog matching and stock are external checks, not asserted here.
"""
import argparse
import csv
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from board1_documents import quantities

BOARD = Path(__file__).resolve().parents[1] / 'boards/board1'

def compact(refs):
    groups = defaultdict(list)
    for ref in set(refs):
        match = re.fullmatch(r'([A-Z]+)(\d+)', ref)
        assert match, f'Invalid designator: {ref}'
        groups[match[1]].append(int(match[2]))
    out = []
    for prefix, values in sorted(groups.items()):
        values.sort()
        start = end = values[0]
        for value in values[1:] + [None]:
            if value == end + 1:
                end = value
                continue
            out.append(f'{prefix}{start}' if start == end else f'{prefix}{start}-{prefix}{end}')
            start = end = value
    return ', '.join(out)

def run(write=False):
    with (BOARD / 'bom_internal.csv').open(newline='') as f:
        internal = list(csv.DictReader(f))
    path = BOARD / 'bom_digikey.csv'
    with path.open(newline='') as f:
        purchase = list(csv.DictReader(f))
        fields = list(purchase[0])
    rules = json.loads((BOARD / 'bom_quantity_rules.json').read_text())
    manifest = json.loads((BOARD / 'kicad/complete_manifest.json').read_text())
    expected, refs, ids = Counter(), defaultdict(list), defaultdict(list)
    for row in internal:
        buy, _, _ = quantities(row, rules)
        if int(buy):
            expected[row['mpn']] += int(buy)
            ids[row['mpn']].append(row['item_id'])
    for ref, part in manifest.items():
        if part['MPN'] in expected:
            refs[part['MPN']].append(ref)
    assert len(purchase) == len({r['Manufacturer Part Number'] for r in purchase}), 'Duplicate MPN purchase rows'
    actual = Counter({r['Manufacturer Part Number']: int(r['Quantity']) for r in purchase})
    assert actual == expected, f'Purchase mismatch: excess={actual-expected}, missing={expected-actual}'
    for row in purchase:
        mpn = row['Manufacturer Part Number']
        if mpn == 'SPC02SYAN':
            headers = [ref for ref, p in manifest.items() if p['BOM_ID'] == 'B1-B069']
            label = 'Shunts for ' + compact(headers)
        elif mpn == 'PRPC040SAAN-RC':
            label = compact(refs[mpn]) + ' (cut 4x8)'
        else:
            assert len(refs[mpn]) == actual[mpn], f'{mpn}: reference count mismatch'
            label = compact(refs[mpn])
        assert len(label) <= 255, f'{mpn}: reference too long'
        if write:
            row['Customer Reference'] = label
        else:
            assert row['Customer Reference'] == label, f'{mpn}: stale customer reference'
    if write:
        with path.open('w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()
            writer.writerows(purchase)
    print(f'PASS: {len(purchase)} unique MPNs; {sum(actual.values())} purchased units; all quantities and customer references reconciled.')
    print(f'Maximum customer reference length: {max(len(r["Customer Reference"]) for r in purchase)} characters.')
    print(f'{sum(not r["DigiKey Part Number"] for r in purchase)} rows use MPN-only matching; live DigiKey match/stock review remains.')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', action='store_true', help='Refresh customer references after auditing purchase quantities')
    run(parser.parse_args().write)
