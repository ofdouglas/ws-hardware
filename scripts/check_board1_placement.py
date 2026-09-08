#!/usr/bin/python3
"""Check native unrouted Board 1 placement against a fresh schematic netlist.

This is an initial-placement gate, not fabrication DRC approval. The report
retains expected unrouted nets and the existing 0.17 mm intra-SWD pad gaps
against the default 0.20 mm rule. Any other electrical/placement DRC error fails.
"""
from collections import Counter
import json
import math
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
CAD=ROOT/'boards/board1/kicad'
os.environ.setdefault('KICAD7_FOOTPRINT_DIR','/usr/share/kicad/footprints')
os.environ['KIPRJMOD']=str(CAD)
import pcbnew as p


def require(ok,message):
    if not ok: raise AssertionError(message)


def main():
    with tempfile.TemporaryDirectory(prefix='board1-placement-check-') as td:
        netfile=Path(td)/'board1.xml'
        subprocess.run(['kicad-cli','sch','export','netlist','--format','kicadxml',
                        '-o',str(netfile),str(CAD/'board1.kicad_sch')],check=True)
        xml=ET.parse(netfile).getroot()
    board=p.LoadBoard(str(CAD/'board1.kicad_pcb'))
    fps={f.GetReference():f for f in board.GetFootprints()}
    require(len(fps)==len(board.GetFootprints()),'Duplicate PCB references')
    components={c.get('ref'):c for c in xml.findall('components/comp')}
    require(set(fps)-set(components)=={'H1','H2','H3','H4'},'Unexpected PCB-only footprints')
    require(set(components)<=set(fps),'Schematic components missing from PCB')
    pin_nets={}
    for net in xml.findall('nets/net'):
        for node in net.findall('node'):
            pin_nets[node.get('ref'),node.get('pin')]=net.get('name')
    actual={}
    for ref,comp in components.items():
        fp=fps[ref]
        require(fp.GetValue()==comp.findtext('value'),f'{ref}: value differs')
        fid=fp.GetFPID()
        require(f'{fid.GetLibNickname()}:{fid.GetLibItemName()}'==comp.findtext('footprint'),f'{ref}: footprint differs')
        path=comp.find('sheetpath').get('tstamps')+comp.findtext('tstamps').split()[0]
        require(fp.GetPath().AsString()==path,f'{ref}: schematic UUID association differs')
        for prop in comp.findall('property'):
            require(fp.GetProperty(prop.get('name'))==prop.get('value'),f'{ref}: property {prop.get("name")} differs')
        require(fp.GetLayer()==p.F_Cu,f'{ref}: unexpected back-side placement')
        for pad in fp.Pads():
            number=pad.GetNumber()
            if not number: continue
            key=ref,number
            require(key in pin_nets,f'{ref}.{number}: extra numbered pad')
            require(pad.GetNetname()==pin_nets[key],f'{ref}.{number}: net differs')
            actual[key]=pad.GetNetname()
    require(actual==pin_nets,'Some schematic pins missing on PCB')
    for ref in ['H1','H2','H3','H4']:
        fp=fps[ref]
        for flag in [p.FP_BOARD_ONLY,p.FP_EXCLUDE_FROM_BOM,p.FP_EXCLUDE_FROM_POS_FILES]:
            require(fp.GetAttributes() & flag,f'{ref}: mechanical-only flag missing')
        require(all(pad.GetAttribute()==p.PAD_ATTRIB_NPTH and not pad.GetNetname()
                    and not pad.GetNumber() for pad in fp.Pads()),f'{ref}: unexpected mounting-hole copper/net')
    require(len(board.GetTracks())==0,'Tracks or vias have been added')
    require(len(board.Zones())==0,'Zones have been added')
    require(all(d.GetLayer() not in [p.F_Cu,p.B_Cu] for d in board.GetDrawings()),'Copper drawing added')
    edges=[d for d in board.GetDrawings() if d.GetLayer()==p.Edge_Cuts]
    require(len(edges)==4,'Expected provisional rectangular outline')
    edgepoints=[(v.x,v.y) for d in edges for v in [d.GetStart(),d.GetEnd()]]
    require(all(n==2 for n in Counter(edgepoints).values()) and len(set(edgepoints))==4,'Outline not closed')
    xmin,xmax=min(x for x,y in edgepoints),max(x for x,y in edgepoints)
    ymin,ymax=min(y for x,y in edgepoints),max(y for x,y in edgepoints)
    for fp in fps.values():
        for pad in fp.Pads():
            box=pad.GetBoundingBox()
            require(box.GetLeft()>xmin and box.GetRight()<xmax and box.GetTop()>ymin and box.GetBottom()<ymax,
                    f'{fp.GetReference()}.{pad.GetNumber()}: pad outside outline')
    require(fps['J1'].GetOrientationDegrees()==-90 and fps['J12'].GetOrientationDegrees()==180,
            'USB/terminal outward orientation changed; recheck mouth geometry')
    require(fps['J1'].GetPosition().y>fps['J12'].GetPosition().y,'External connectors not on opposite edges')
    for ref in ['J2','J4','J6','J8','J3','J5','J7','J9']:
        require(fps[ref].GetOrientationDegrees()==90,f'{ref}: header orientation inconsistent')
    for ref in ['U11','U12','U13','U14','U15','U16','U17','U18']:
        require(fps[ref].GetOrientationDegrees()==-90,f'{ref}: CAN bus pad direction differs')

    access=json.loads((CAD/'testpoint_access.json').read_text())
    require({r['reference'] for r in access}=={f'TP{i}' for i in range(1,13)} and len(access)==12,
            'Testpoint access record must cover all 12 pads exactly once')
    silk=[d for d in board.GetDrawings() if isinstance(d,p.PCB_TEXT) and d.GetLayer()==p.F_SilkS]
    ground_refs=['J13','J14','J15','J16','J17','J18']
    ground_distances=[]
    for record in access:
        ref=record['reference'];fp=fps[ref];xy=p.ToMM(fp.GetPosition())
        require(next(iter(fp.Pads())).GetNetname()==record['net'],f'{ref}: function record has wrong net')
        labels=[t for t in silk if t.GetText()==record['silkscreen']]
        require(len(labels)==1,f'{ref}: missing or duplicate function silkscreen')
        require(math.dist(xy,p.ToMM(labels[0].GetPosition()))<=6,f'{ref}: label too far from pad')
        require(p.ToMM(labels[0].GetTextHeight())>=.8,f'{ref}: function label too small')
        nearest=min((min(math.dist(xy,p.ToMM(pad.GetPosition())) for pad in fps[g].Pads()),g) for g in ground_refs)
        require(nearest[0]<=15,f'{ref}: ground post farther than the 15 mm placement allowance')
        require(nearest[1]==record['nearest_ground'] and abs(nearest[0]-record['ground_distance_mm'])<.02,
                f'{ref}: ground access record is stale')
        require(abs(xy[0]-50-record['x_mm'])<.01 and abs(xy[1]-40-record['y_mm'])<.01,
                f'{ref}: access coordinates are stale')
        ground_distances.append(nearest[0])
    tp_positions=[p.ToMM(fps[r['reference']].GetPosition()) for r in access]
    tp_spacing=min(math.dist(a,c) for i,a in enumerate(tp_positions) for c in tp_positions[i+1:])
    require(tp_spacing>=6,'Testpoints closer than the 6 mm center-spacing allowance')

    communication=json.loads((CAD/'communication_header_access.json').read_text())
    require({r['reference'] for r in communication}=={f'J{i}' for i in range(19,26)},'Communication header inventory differs')
    for record in communication:
        fp=fps[record['reference']]
        require({pad.GetNumber():pad.GetNetname() for pad in fp.Pads()}==record['pins'],'Communication pin order differs')
        require(any(t.GetText()==record['silkscreen'] and math.dist(p.ToMM(t.GetPosition()),p.ToMM(fp.GetPosition()))<5 for t in silk),'Missing communication function label')
        require(fp.GetOrientationDegrees()==record['rotation'],'Communication orientation differs')

    report=CAD/'review/board1-initial-placement-drc.txt'
    # Use a fresh pcbnew process for DRC so inspection of SWIG proxy objects
    # above cannot affect the rule-engine state. This matches a direct load/run.
    subprocess.run([sys.executable,'-c',
        'import sys,pcbnew as p; b=p.LoadBoard(sys.argv[1]); '
        'assert p.WriteDRCReport(b,sys.argv[2],p.EDA_UNITS_MILLIMETRES,False)',
        str(CAD/'board1.kicad_pcb'),str(report)],check=True)
    raw=report.read_text()
    counts=Counter(re.findall(r'^\[([^]]+)\]',raw,re.M))
    for block in re.split(r'(?=^\[)',raw,flags=re.M):
        if not block.startswith('['): continue
        code=block.split(']',1)[0][1:]
        if code in ['unconnected_items','silk_overlap','silk_over_copper','silk_edge_clearance','text_height']: continue
        if code=='clearance':
            refs=re.findall(r'of (J\d+)\b',block)
            require(len(refs)==2 and refs[0]==refs[1] and refs[0] in ['J3','J5','J7','J9']
                    and 'actual 0.1700 mm' in block,'Unexpected clearance violation:\n'+block)
        else: raise AssertionError('Unexpected DRC finding:\n'+block)
    summary={
        'stage':'initial placement only; not a clean fabrication DRC',
        'schematic_components':len(components),'schematic_pins':len(actual),
        'physical_numbered_pads':sum(bool(pad.GetNumber()) for f in fps.values() for pad in f.Pads()),
        'mechanical_NPTH_holes':4,'tracks_and_vias':len(board.GetTracks()),'zones':len(board.Zones()),
        'outline_mm':[p.ToMM(xmax-xmin),p.ToMM(ymax-ymin)],
        'testpoint_function_labels':len(access),'communication_headers':len(communication),
        'testpoint_min_center_spacing_mm':round(tp_spacing,2),
        'testpoint_max_ground_distance_mm':round(max(ground_distances),2),
        'drc_counts':dict(sorted(counts.items())),
        'remaining':'Unrouted connections expected. SWD internal pad clearance and USB outline silkscreen require layout-release disposition.'}
    (CAD/'review/board1-initial-placement-checks.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2))
    print('PASS: native schematic/PCB association, inventory and pad nets; no placement collisions or inter-component clearance errors. Full DRC is not clean because routing and the listed rule decisions remain.')


if __name__=='__main__':main()
