#!/usr/bin/env python3
"""Check full Board 1 native connectivity and component records.

Exports KiCad XML and checks every physical symbol pin (including explicit NCs),
fields, footprint pad coverage, and BOM inventory. This is not ERC, pin-mux
qualification, footprint dimensional qualification, or hardware validation.

Optional kicad/schematic_bom_allocations.json records BOM rows whose procurement quantity
differs from the number of CAD symbols, for example purchased strip stock and
loose shunts. Each entry is keyed by BOM ID and must contain cad_count,
bom_quantity, and reason. An optional footprints list explicitly permits multiple
cut-strip/test-access footprints for one BOM row. These exceptions never waive
the symbol-to-manifest field or numbered-pad checks.
"""

import argparse
from collections import Counter, defaultdict
import csv
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
CAD = ROOT / 'boards/board1/kicad'


class CheckFailure(Exception):
    pass


def require(condition, message):
    if not condition:
        raise CheckFailure(message)


def sexpressions(text):
    """Read library tables/footprints without matching pad-like quoted text."""
    tokens = re.findall(r'"(?:\\.|[^"\\])*"|[()]|[^\s()]+', text)
    stack, roots = [], []
    for token in tokens:
        if token == '(':
            node = []
            (stack[-1] if stack else roots).append(node)
            stack.append(node)
        elif token == ')':
            require(bool(stack), 'Unbalanced S-expression')
            stack.pop()
        else:
            require(bool(stack), 'Token outside S-expression')
            stack[-1].append(json.loads(token) if token.startswith('"') else token)
    require(not stack, 'Unterminated S-expression')
    return roots


def children(node, key):
    return [item for item in node if isinstance(item, list) and item and item[0] == key]


def footprint_paths():
    """Resolve project-local libraries first, followed by installed libraries."""
    result = {}
    version = subprocess.check_output(['kicad-cli', '--version'], text=True).split('.')[0]
    standard = Path(os.environ.get(f'KICAD{version}_FOOTPRINT_DIR', '/usr/share/kicad/footprints'))
    for folder in standard.glob('*.pretty'):
        result[folder.stem] = folder
    variables = dict(os.environ, KIPRJMOD=str(CAD))
    variables.setdefault(f'KICAD{version}_FOOTPRINT_DIR', str(standard))
    for table in [Path.home() / '.config/kicad' / f'{version}.0' / 'fp-lib-table',
                  ROOT / 'fp-lib-table', CAD / 'fp-lib-table']:
        if not table.exists():
            continue
        for form in sexpressions(table.read_text()):
            for entry in children(form, 'lib'):
                name, uri = children(entry, 'name'), children(entry, 'uri')
                if name and uri:
                    expanded = re.sub(r'\$\{([^}]+)\}', lambda m: variables.get(m[1], m[0]), uri[0][1])
                    location = Path(expanded)
                    result[name[0][1]] = location if location.is_absolute() else table.parent / location
    return result


def exported_root(netlist=None):
    if netlist:
        return ET.parse(netlist).getroot()
    with tempfile.TemporaryDirectory(prefix='board1-check-') as directory:
        path = Path(directory) / 'board1.xml'
        subprocess.run(['kicad-cli', 'sch', 'export', 'netlist', '--format', 'kicadxml',
                        '-o', str(path), str(CAD / 'board1.kicad_sch')], check=True)
        return ET.parse(path).getroot()


def inventory(expected, bom, allocations):
    counts = Counter(spec['BOM_ID'] for spec in expected.values())
    require(set(allocations) <= set(bom), 'Allocation refers to an unknown BOM ID')
    for bid, row in bom.items():
        raw_quantity = row['quantity']
        require(raw_quantity.isdecimal(), f'{bid}: resolve BOM quantity {raw_quantity!r} for complete capture')
        quantity = int(raw_quantity)
        if bid in allocations:
            entry = allocations[bid]
            require(isinstance(entry.get('cad_count'), int) and entry['cad_count'] >= 0,
                    f'{bid}: allocation requires a nonnegative cad_count')
            require(entry.get('bom_quantity') == quantity and bool(entry.get('reason', '').strip()),
                    f'{bid}: allocation quantity/reason differs from BOM')
            require(counts[bid] == entry['cad_count'],
                    f'{bid}: {counts[bid]} CAD parts, allocation requires {entry["cad_count"]}')
        else:
            require(counts[bid] == quantity, f'{bid}: {counts[bid]} CAD parts, BOM quantity {quantity}')
    require(set(counts) <= set(bom), 'CAD contains unknown BOM IDs')


def preserved_power_usb(expected):
    """Keep the completed first-stage capture intact when adding board sheets."""
    original = json.loads((CAD / 'capture_manifest.json').read_text())
    require(len(original) == 52, 'Original power/USB manifest must contain its 52 physical parts')
    for ref, before in original.items():
        require(ref in expected, f'{ref}: preserved power/USB component is missing')
        after = expected[ref]
        require({key: value for key, value in before.items() if key != 'sheet'}
                == {key: value for key, value in after.items() if key != 'sheet'},
                f'{ref}: completed power/USB component fields or pin mapping changed')
        require(after['sheet'] == ('power' if before['sheet'] == 'board1' else before['sheet']),
                f'{ref}: unexpected power/USB sheet relocation')


def semantic_checks(expected, pin_net, nets):
    """Independent architecture checks supplement generated capture intent."""
    def net(ref, pin):
        require((ref, str(pin)) in pin_net, f'{ref}.{pin}: expected a connected net')
        return pin_net[ref, str(pin)]

    def named(ref, pin, name):
        actual = net(ref, pin)
        require(actual.rsplit('/', 1)[-1] == name, f'{ref}.{pin}: expected {name}, found {actual}')

    def unconnected(ref, pin):
        actual = pin_net.get((ref, str(pin)))
        require(actual is None or (actual.startswith('unconnected-') and len(nets[actual]) == 1),
                f'{ref}.{pin}: this connector position must remain NC')

    def parts(bid, count):
        refs = [ref for ref, spec in expected.items() if spec['BOM_ID'] == bid]
        require(len(refs) == count, f'{bid}: architecture requires {count} physical parts, found {len(refs)}')
        return refs

    # Fixed references retained from the separately reviewed power/USB capture.
    require(net('U4', 39) != net('U6', 14), 'Bridge and main 3.3 V domains are joined')
    require(len({net('U4', p) for p in [37, 38, 39, 40]}) == 4,
            'FTDI VCCA/VCORE/VCCD/VREGIN must be four separate rails')
    for pin in [1, 4, 10, 13]:
        named('U6', pin, 'PWREN_N')
    named('D1', 1, 'VBUS_RAW')
    named('D1', 2, 'GND')
    for pin in [5, 6]:
        named('U1', pin, 'USB_5V')
    named('U2', 3, '3V3_SYS')
    named('L1', 2, '3V3_SYS')
    gateway = parts('B1-B001', 1)[0]
    leaves = parts('B1-B002', 3)
    can_phys = parts('B1-B003', 8)
    swd_headers = parts('B1-B009', 4)
    parts('B1-B021', 1)
    parts('B1-B066', 1)
    require(not any(s['BOM_ID'] == 'B1-B053' for s in expected.values()),
            'Deferred automated recovery parts must not be captured')
    owner_refs = {'GW': gateway}
    for ref in leaves:
        reset = net(ref, 40).rsplit('/', 1)[-1]
        match = re.fullmatch(r'(SAM[012])_RESET_N', reset)
        require(match is not None, f'{ref}.40: leaf reset must be independently named')
        require(match[1] not in owner_refs, f'{ref}: duplicated leaf identity {match[1]}')
        owner_refs[match[1]] = ref
    require(set(owner_refs) == {'GW', 'SAM0', 'SAM1', 'SAM2'}, 'Three independent SAM identities required')

    def mcu_participants(signal):
        actual = [name for name in nets if name.rsplit('/', 1)[-1] == signal]
        require(len(actual) == 1, f'{signal}: expected one native net')
        return {ref for ref, pin in nets[actual[0]] if ref in owner_refs.values()}

    swd_owners = set()
    for header in swd_headers:
        io = net(header, 2).rsplit('/', 1)[-1]
        match = re.fullmatch(r'(GW|SAM[012])_SWDIO', io)
        require(match is not None, f'{header}.2: expected independent MCU SWDIO')
        owner = match[1]
        swd_owners.add(owner)
        named(header, 1, '3V3_SYS')
        named(header, 4, f'{owner}_SWCLK')
        named(header, 10, f'{owner}_RESET_N')
        for pin in [3, 5, 9]:
            named(header, pin, 'GND')
        for pin in [6, 7, 8]:
            unconnected(header, pin)
        for suffix in ['SWDIO', 'SWCLK', 'RESET_N']:
            require(mcu_participants(f'{owner}_{suffix}') == {owner_refs[owner]},
                    f'{header}: {suffix} must connect only to its owning MCU')
    require(swd_owners == set(owner_refs), 'Each MCU requires its own independent SWD header')

    ground_headers = parts('B1-B075', 6)
    for header in ground_headers:
        require(set(expected[header]['pins']) == {'1', '2'}, f'{header}: ground header requires exactly two posts')
        named(header, 1, 'GND')
        named(header, 2, 'GND')

    headers = parts('B1-B059', 4)
    series = parts('B1-B076', 24)
    pulldowns = parts('B1-B077', 2)
    private_nets, header_owners = set(), set()
    for header in headers:
        debug_rx = net(header, 1).rsplit('/', 1)[-1]
        require(debug_rx.endswith('_DEBUG_RX_HDR'), f'{header}: pin 1 must be MCU-perspective debug RX')
        owner = debug_rx.removesuffix('_DEBUG_RX_HDR')
        require(owner in {'GW', 'SAM0', 'SAM1', 'SAM2'}, f'{header}: unknown MCU owner {owner}')
        header_owners.add(owner)
        named(header, 3, 'GND')
        named(header, 6, 'GND')
        named(header, 4, 'SYNC')
        named(header, 5, 'TRIG')
        for pin, suffix in {1: 'DEBUG_RX', 2: 'DEBUG_TX', 7: 'EVENT0', 8: 'EVENT1'}.items():
            named(header, pin, f'{owner}_{suffix}_HDR')
        for pin, suffix in {1: 'DEBUG_RX', 2: 'DEBUG_TX', 4: 'SYNC', 5: 'TRIG', 7: 'EVENT0', 8: 'EVENT1'}.items():
            other = f'{owner}_{suffix}'
            matching = [r for r in series if {net(r, 1).rsplit('/', 1)[-1], net(r, 2).rsplit('/', 1)[-1]}
                        == {net(header, pin).rsplit('/', 1)[-1], other}]
            require(len(matching) == 1, f'{header}.{pin}: require one 330 ohm branch to {other}')
            require(mcu_participants(other) == {owner_refs[owner]},
                    f'{other}: header resistor must reach only its owning MCU')
        for pin in [1, 2, 4, 5, 7, 8]:
            header_net = net(header, pin)
            branches = [r for r in series if header_net in {net(r, 1), net(r, 2)}]
            require(len(branches) == (4 if pin in [4, 5] else 1),
                    f'{header}.{pin}: incorrect number of individual 330 ohm branches')
            if pin not in [4, 5]:
                require(header_net not in private_nets, f'{header}.{pin}: private header signal is shared')
                private_nets.add(header_net)
    require(header_owners == {'GW', 'SAM0', 'SAM1', 'SAM2'}, 'Each MCU requires its own timing header')
    for signal in ['SYNC', 'TRIG']:
        pulls = [r for r in pulldowns
                 if {net(r, 1).rsplit('/', 1)[-1], net(r, 2).rsplit('/', 1)[-1]} == {signal, 'GND'}]
        require(len(pulls) == 1, f'{signal}: require exactly one header-side pull-down')
    for ref in series:
        require(net(ref, 1) != net(ref, 2), f'{ref}: header series resistor is bypassed')
    for ref in parts('B1-B066', 1):
        for pin in [2, 5, 9, 12, 7]:
            named(ref, pin, 'GND')
        for pin in [3, 6, 8, 11]:
            named(ref, pin, 'UART_MD')
        named(ref, 14, '3V3_SYS')
        require(len({net(ref, p) for p in [1, 4, 10, 13]}) == 4,
                'UART_MD output enables must have four independent MCU TX signals')
        enables = {net(ref, p).rsplit('/', 1)[-1] for p in [1, 4, 10, 13]}
        require(enables == {f'{owner}_MD_TX' for owner in owner_refs}, 'UART_MD output enables have wrong MCU signals')
    require(mcu_participants('UART_MD') == set(owner_refs.values()), 'All four MCUs must observe UART_MD')
    for owner, ref in owner_refs.items():
        require(mcu_participants(f'{owner}_MD_TX') == {ref}, f'{owner}: UART_MD TX must remain private')
    for signal, owners in {'RING_01': ['SAM0', 'SAM1'], 'RING_12': ['SAM1', 'SAM2'],
                           'RING_20': ['SAM2', 'SAM0']}.items():
        require(mcu_participants(signal) == {owner_refs[o] for o in owners},
                f'{signal}: direct ring hop must connect only its two SAM endpoints')

    # Native PHY pin functions are sourced in the exact-part local symbol notes.
    # Check CAN polarity and individual MCU channels independently of references.
    seen_channels = set()
    for ref in can_phys:
        named(ref, 2, 'GND')
        named(ref, 3, '3V3_SYS')
        named(ref, 5, '3V3_SYS')
        tx = net(ref, 1).rsplit('/', 1)[-1]
        match = re.fullmatch(r'(GW|SAM[012])_CAN_([AB])_TX', tx)
        require(match is not None, f'{ref}.1: unexpected CAN TX allocation {tx}')
        owner, bus = match.groups()
        require((owner, bus) not in seen_channels, f'{owner} CAN {bus}: duplicate PHY allocation')
        seen_channels.add((owner, bus))
        named(ref, 4, f'{owner}_CAN_{bus}_RX')
        named(ref, 8, f'{owner}_CAN_{bus}_STB')
        for suffix in ['TX', 'RX', 'STB']:
            signal = f'{owner}_CAN_{bus}_{suffix}'
            require(mcu_participants(signal) == {owner_refs[owner]}, f'{signal}: PHY must reach its owning MCU')
        named(ref, 6, f'FD_CAN_{bus}_L')
        named(ref, 7, f'FD_CAN_{bus}_H')
    require(seen_channels == {(owner, bus) for owner in ['GW', 'SAM0', 'SAM1', 'SAM2'] for bus in 'AB'},
            'Both CAN buses require one independent channel per MCU')

    def endpoints(ref):
        return {net(ref, p).rsplit('/', 1)[-1] for p in ['1', '2']}

    can_terminators, jumpers = parts('B1-B067', 4), parts('B1-B069', 2)
    used_resistors, used_jumpers = set(), set()
    for bus in 'AB':
        pair = {f'FD_CAN_{bus}_H', f'FD_CAN_{bus}_L'}
        fixed = [r for r in can_terminators if endpoints(r) == pair]
        require(len(fixed) == 1, f'CAN {bus}: require one fixed far-end terminator')
        used_resistors.update(fixed)
        paths = [(r, j) for r in can_terminators for j in jumpers
                 if len(endpoints(r) & endpoints(j)) == 1
                 and (endpoints(r) ^ endpoints(j)) == pair
                 and not (endpoints(r) & endpoints(j)) & pair]
        require(len(paths) == 1, f'CAN {bus}: require one 120 ohm plus series jumper branch')
        used_resistors.add(paths[0][0])
        used_jumpers.add(paths[0][1])
    require(used_resistors == set(can_terminators) and used_jumpers == set(jumpers),
            'CAN termination contains unallocated or shared parts')
    tvs_buses = set()
    for ref in parts('B1-B072', 2):
        h = net(ref, 1).rsplit('/', 1)[-1]
        require(h in {'FD_CAN_A_H', 'FD_CAN_B_H'}, f'{ref}: CAN TVS pin 1 must connect directly to CANH')
        bus = h.removeprefix('FD_CAN_').removesuffix('_H')
        tvs_buses.add(bus)
        named(ref, 2, f'FD_CAN_{bus}_L')
        named(ref, 3, 'GND')
    require(tvs_buses == {'A', 'B'}, 'CAN TVS arrays must cover both terminal pairs')

    phy = parts('B1-B021', 1)[0]
    for pin, signal in {1: 'GW_RS485_RX', 2: 'GW_RS485_RE_N', 3: 'GW_RS485_DE',
                        4: 'GW_RS485_TX', 5: 'GND', 6: 'RS485_A', 7: 'RS485_B', 8: '3V3_SYS'}.items():
        named(phy, pin, signal)
    require(endpoints(parts('B1-B068', 1)[0]) == {'RS485_A', 'RS485_B'},
            'RS-485 fixed local terminator must be directly across A/B')
    biases = {frozenset(endpoints(ref)) for ref in parts('B1-B071', 2)}
    require(biases == {frozenset({'3V3_SYS', 'RS485_A'}), frozenset({'RS485_B', 'GND'})},
            'RS-485 idle bias polarity must be A high / B low')
    tvs = parts('B1-B073', 1)[0]
    for pin, signal in {1: 'RS485_A', 2: 'RS485_B', 3: 'GND'}.items():
        named(tvs, pin, signal)
    terminal = parts('B1-B022', 1)[0]
    for pin, signal in enumerate(['FD_CAN_A_H', 'FD_CAN_A_L', 'GND', 'FD_CAN_B_H',
                                   'FD_CAN_B_L', 'RS485_A', 'RS485_B', 'GND'], 1):
        named(terminal, pin, signal)
    connectors = {ref for ref, spec in expected.items()
                  if spec['lib_id'].startswith('Connector') and spec['BOM_ID'] != 'B1-B011'}
    allowed_connectors = set(parts('B1-B005', 1) + swd_headers + headers + jumpers + ground_headers + [terminal])
    require(connectors == allowed_connectors, 'Unexpected or reserved connector outside captured Rev A scope')

    # SAM pin 43 is a regulator output: never tie the three core rails together.
    core_nets = {net(ref, 43).rsplit('/', 1)[-1] for ref in leaves}
    require(core_nets == {f'SAM{i}_VDDCORE' for i in range(3)}, 'SAM core outputs must remain separate')
    for bid in ['B1-B040', 'B1-B041']:
        core_caps = parts(bid, 3)
        observed = {frozenset(endpoints(ref)) for ref in core_caps}
        require(observed == {frozenset({core, 'GND'}) for core in core_nets},
                f'{bid}: each SAM core needs its own capacitor to ground')


def check(manifest=CAD / 'complete_manifest.json', allocations_path=CAD / 'schematic_bom_allocations.json', netlist=None):
    expected = json.loads(Path(manifest).read_text())
    with (ROOT / 'boards/board1/bom.csv').open() as handle:
        rows = list(csv.DictReader(handle))
    bom = {row['item_id']: row for row in rows}
    require(len(bom) == len(rows), 'Duplicate BOM IDs')
    allocations = json.loads(Path(allocations_path).read_text()) if Path(allocations_path).exists() else {}
    root = exported_root(netlist)
    component_list = root.findall('./components/comp')
    components = {comp.get('ref'): comp for comp in component_list}
    require(len(components) == len(component_list), 'Duplicate physical component references')
    require(set(components) == set(expected),
            f'Physical inventory differs: extra={sorted(set(components)-set(expected))}, '
            f'missing={sorted(set(expected)-set(components))}')
    nets, pin_net = {}, {}
    for entry in root.findall('./nets/net'):
        name = entry.get('name')
        require(name not in nets, f'Duplicate net name {name}')
        nodes = [(p.get('ref'), p.get('pin')) for p in entry.findall('node')]
        require(len(nodes) == len(set(nodes)), f'Duplicate pin on {name}')
        nets[name] = set(nodes)
        for node in nodes:
            require(node not in pin_net, f'{node} appears on multiple nets')
            pin_net[node] = name
    libpins = {(p.get('lib'), p.get('part')): {n.get('num') for n in p.findall('./pins/pin')}
               for p in root.findall('./libparts/libpart')}
    libraries, pad_cache = footprint_paths(), {}
    logical_nets = defaultdict(set)
    pin_count = 0
    for ref, spec in expected.items():
        component = components[ref]
        fields = {f.get('name'): f.text for f in component.findall('./fields/field')}
        require(spec['BOM_ID'] in bom, f'{ref}: unknown BOM ID {spec["BOM_ID"]}')
        row = bom[spec['BOM_ID']]
        require(fields.get('BOM_ID') == spec['BOM_ID'], f'{ref}: BOM_ID field differs')
        require(fields.get('MPN') == spec['MPN'] == row['mpn'], f'{ref}: MPN field differs from manifest/BOM')
        require(component.findtext('value') == spec['value'], f'{ref}: value differs from manifest')
        footprint = spec['footprint']
        require(component.findtext('footprint') == footprint, f'{ref}: footprint differs from manifest')
        permitted = allocations.get(spec['BOM_ID'], {}).get('footprints', [row['footprint']])
        require(footprint in permitted, f'{ref}: footprint differs from BOM/allocation')
        source = component.find('libsource')
        require(source is not None, f'{ref}: missing symbol source')
        key = (source.get('lib'), source.get('part'))
        require(':'.join(key) == spec['lib_id'], f'{ref}: symbol library differs from manifest')
        require(set(spec['pins']) == libpins[key], f'{ref}: not every physical symbol pin is accounted for')
        if footprint not in pad_cache:
            library, name = footprint.split(':', 1)
            require(library in libraries, f'{ref}: cannot locate footprint library {library}')
            path = libraries[library] / (name + '.kicad_mod')
            require(path.exists(), f'{ref}: footprint file missing: {path}')
            forms = sexpressions(path.read_text())
            pad_cache[footprint] = {pad[1] for form in forms for pad in children(form, 'pad') if pad[1]}
        require(set(spec['pins']) == pad_cache[footprint],
                f'{ref}: numbered footprint pads {sorted(pad_cache[footprint])} '
                f'differ from symbol pins {sorted(spec["pins"])}')
        for pin, intended in spec['pins'].items():
            actual = pin_net.get((ref, pin))
            if intended is None:
                require(actual is None or (actual.startswith('unconnected-') and len(nets[actual]) == 1),
                        f'{ref}.{pin}: intended NC is connected to {actual}')
            else:
                require(actual is not None and actual.rsplit('/', 1)[-1] == intended,
                        f'{ref}.{pin}: expected {intended}, found {actual}')
                logical_nets[intended].add(actual)
            pin_count += 1
    for intended, actual_names in logical_nets.items():
        require(len(actual_names) == 1,
                f'{intended}: disconnected same-name nets on different sheets: {sorted(actual_names)}')
    require(set(pin_net) <= {(ref, pin) for ref, spec in expected.items() for pin in spec['pins']},
            'Export contains a net node absent from the physical manifest')
    inventory(expected, bom, allocations)
    preserved_power_usb(expected)
    semantic_checks(expected, pin_net, nets)
    print(f'PASS: {len(components)} physical parts; {pin_count} pins; native net intent, '
          'NCs, symbol/MPN/value/footprint fields, numbered pad coverage, BOM quantities, '
          'preserved power/USB, SWD/timing/ground headers, core rails and bus/termination topology agree. '
          'Not ERC or hardware validation.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest', type=Path, default=CAD / 'complete_manifest.json')
    parser.add_argument('--allocations', type=Path, default=CAD / 'schematic_bom_allocations.json')
    parser.add_argument('--netlist', type=Path, help='Use an existing native KiCad XML export')
    args = parser.parse_args()
    try:
        check(args.manifest, args.allocations, args.netlist)
    except (CheckFailure, OSError, ValueError, KeyError, subprocess.CalledProcessError) as error:
        parser.exit(1, f'FAIL: {error}\n')


if __name__ == '__main__':
    main()
