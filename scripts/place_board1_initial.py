#!/usr/bin/python3
"""One-time Board 1 placement capture; native PCB becomes editing authority.

Uses a fresh KiCad schematic netlist, real library footprints, and schematic
UUID paths. Refuses to replace an existing PCB unless --replace is explicit.
No tracks, vias, copper zones, or Rev B circuitry are generated.
Run with /usr/bin/python3 (KiCad's pcbnew Python module).
"""
import argparse
import json
from pathlib import Path
import subprocess
import tempfile
import xml.etree.ElementTree as ET

import pcbnew as p
from check_board1_complete import footprint_paths

ROOT = Path(__file__).resolve().parents[1]
CAD = ROOT / 'boards/board1/kicad'
OUT = CAD / 'board1.kicad_pcb'
ORIGIN = (50, 40)
WIDTH, HEIGHT = 155, 110


def vec(x, y):
    return p.VECTOR2I(p.FromMM(x), p.FromMM(y))


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--replace', action='store_true')
    args = ap.parse_args()
    if OUT.exists() and not args.replace:
        raise SystemExit('PCB exists: edit it directly; --replace deliberately discards PCB edits.')
    with tempfile.TemporaryDirectory(prefix='board1-place-') as td:
        netfile = Path(td) / 'board1.xml'
        subprocess.run(['kicad-cli', 'sch', 'export', 'netlist', '--format', 'kicadxml',
                        '-o', str(netfile), str(CAD / 'board1.kicad_sch')], check=True)
        xml = ET.parse(netfile).getroot()

    board = p.BOARD()
    board.SetFileName(str(OUT))
    board.SetCopperLayerCount(2)  # KiCad initial default; stack-up is not frozen.
    title = board.GetTitleBlock()
    title.SetTitle('WireSpaces Board 1 - initial component placement')
    title.SetRevision('A-placement-1')
    title.SetDate('2026-09-07')
    title.SetComment(0, 'UNROUTED - provisional outline - not for fabrication')
    board.SetTitleBlock(title)
    nets, pin_nets = {}, {}
    for node in xml.findall('nets/net'):
        name = node.get('name')
        net = p.NETINFO_ITEM(board, name)
        board.Add(net)
        nets[name] = net
        for pad in node.findall('node'):
            pin_nets[pad.get('ref'), pad.get('pin')] = name
    fps, placed, metadata = {}, set(), {}
    libs = footprint_paths()
    for comp in xml.findall('components/comp'):
        ref = comp.get('ref')
        fpname = comp.findtext('footprint')
        lib, name = fpname.split(':', 1)
        fp = p.FootprintLoad(str(libs[lib]), name)
        if not fp:
            raise RuntimeError(f'{ref}: cannot load {fpname}')
        fp.SetFPID(p.LIB_ID(lib, name))
        fp.SetReference(ref)
        fp.SetValue(comp.findtext('value'))
        # Native XML sheetpath is the path KiCad uses for PCB association,
        # excluding the root document UUID and including each child sheet UUID.
        path = comp.find('sheetpath').get('tstamps') + comp.findtext('tstamps').split()[0]
        fp.SetPath(p.KIID_PATH(path))
        for prop in comp.findall('property'):
            fp.SetProperty(prop.get('name'), prop.get('value'))
        for pad in fp.Pads():
            number = pad.GetNumber()
            if (ref, number) in pin_nets:
                pad.SetNet(nets[pin_nets[ref, number]])
            elif number:
                raise RuntimeError(f'{ref}.{number}: footprint pad absent from schematic')
        fp.Value().SetVisible(False)
        fp.Reference().SetTextSize(vec(.75, .75))
        fp.Reference().SetTextThickness(p.FromMM(.12))
        board.Add(fp)
        fps[ref] = fp
        metadata[ref] = {'sheet': comp.find('sheetpath').get('names'), 'footprint': fpname}

    def put(ref, x, y, angle=0):
        assert ref not in placed, ref
        fp = fps[ref]
        fp.SetOrientationDegrees(angle)
        fp.SetPosition(vec(x + ORIGIN[0], y + ORIGIN[1]))
        placed.add(ref)
        metadata[ref].update(x_mm=x, y_mm=y, rotation_deg=angle)

    def rel(ref, center, x, y, angle=0):
        put(ref, center[0] + x, center[1] + y, angle)

    # Three repeated leaf stations. All header pin 1s have the same orientation.
    for i, x in enumerate([28, 68, 108]):
        center = (x, 33)
        put(f'U{8+i}', *center)
        put(f'J{4+2*i}', x - 8.89, 5.5, 90)
        put(f'J{5+2*i}', x - 2.54, 15.635, 90)
        cb, rb = 37 + 10*i, 25 + 10*i
        caps = [(1.75,-9.8,270), (-7,0,180), (-3.5,6.7,90),
                (6.8,-2.75,0), (-.75,-6.8,270), (7.5,-6.8,270),
                (1.75,-6.8,270), (4.25,-6.8,270), (5.05,8,90), (10.55,8,90)]
        for n, (dx,dy,a) in enumerate(caps): rel(f'C{cb+n}', center, dx,dy,a)
        resistors = [(.1,6.7,90), (2.5,6.7,90), (-9.5,-4.6,180),
                     (-9.5,-2.2,180), (-7,2.5,180), (-7,5,180),
                     (4.25,-9.8,270), (-.1,10.8,90), (-3.3,-9.8,270), (9,-.2,0)]
        for n,(dx,dy,a) in enumerate(resistors): rel(f'R{rb+n}', center,dx,dy,a)
        rel(f'Y{3+i}', center,7.8,11.2)
        rel(f'D{5+i}', center,12,-.2)
        put(f'J{14+i}', x-16,17,90)
        put(f'TP{7+2*i}',x+12.5,19)
        put(f'TP{8+2*i}',x+17,19)

    # Gateway station; direct MCU-side support placement, headers at USB edge.
    gw = (86, 87)
    put('U7', *gw)
    put('J2',77.11,104.5,90)
    put('J3',109.46,103.135,90)
    put('J13',106,91,90)
    gwparts = {
        'C25':(-11,-1,0), 'C26':(-8,-5,180), 'C27':(-8,5,180),
        'C28':(4.5,8,90), 'C29':(8,-4,0), 'C30':(-4,-8,270),
        'C31':(2,8,90), 'C32':(-.5,8,90), 'C33':(8,-7.5,0),
        'C34':(-3,8,90), 'C35':(-8,-10,0), 'C36':(-8,-7.5,0),
        'Y2':(-12.5,-7.8,90), 'R15':(7.5,7,90), 'R16':(10,3.75,0),
        'R17':(-8,0,180), 'R18':(-8,2.5,180), 'R19':(-12,2.5,180),
        'R20':(-12,5,180), 'R21':(-14.5,-1,0), 'R22':(10,7,90),
        'R23':(-1.5,-8,270), 'R24':(-5.5,8,90), 'D4':(-5.5,11,90),
        'TP5':(-20,2,0), 'TP6':(-1.5,-12,0),
    }
    for ref,(dx,dy,a) in gwparts.items(): rel(ref,gw,dx,dy,a)

    # Two clear horizontal CAN corridors. Order from fixed end to connector:
    # SAM0, SAM1, gateway, SAM2. Pads 6/7 face the intended trunk.
    for bus, row in enumerate([53,65]):
        for node, x in enumerate([88,28,68,114]):
            u = 11 + bus*4 + node
            c = 67 + bus*8 + node*2
            r = 55 + bus*6 + node
            put(f'U{u}',x,row,270)
            put(f'C{c}',x+1.6,row-5.2,0)
            put(f'C{c+1}',x-4.8,row+2,90)
            put(f'R{r}',x+4.8,row+2,90)
        put('R59' if bus==0 else 'R65',18,row+5.5,90)
    # Accessible termination jumpers next to the external connector.
    put('J10',143,21,90); put('R60',149,21,90)
    put('J11',143,28,90); put('R66',149,28,90)
    # Terminal body front faces out of the top edge; rear lies inside the PCB.
    put('J12',142.5,5.2,180)
    put('D8',142.75,16,90); put('D9',135.25,16,90); put('D10',130.25,16,90)
    put('U20',135,29,90)
    put('C84',138.8,25,90)
    put('R78',129,22,90); put('R79',129,26,90); put('R80',129,30,90)
    for ref,x in zip(['R74','R75','R76','R77'],[132,135.5,139,142.5]): put(ref,x,36,90)
    put('J18',143,42,90)
    for ref,x,y in [('TP14',131,43),('TP15',136,43),('TP16',151,34),
                    ('TP17',151,39),('TP18',124,36),('TP19',124,41)]: put(ref,x,y)

    # Central multidrop driver and shared timing bias.
    put('U19',62,76,0); put('C83',66.8,73,0)
    for ref,x,y in [('R67',57,72),('R68',57,74.5),('R69',67,78),('R70',67,75.5),
                    ('R71',62,81.5),('R72',56,20.5),('R73',56,23)]: put(ref,x,y)
    put('TP13',60,86)

    # USB mouth is local +X: rotation 270 points out of the bottom edge.
    put('J1',25,94.99,270)
    put('D2',28,91,90)
    put('U4',37,84,90)
    put('U5',48,77,0); put('C11',53,74.5,0)
    put('R7',46,82.5,0); put('R8',53,79.5,0)
    # Crystal is adjacent to FTDI pins 1/2 and remote from the buck inductor.
    put('Y1',40,98,0); put('C12',35,94,90); put('C13',45,94,90)
    for ref,x,y,a in [
        ('C14',39,77,90),('R5',41.5,77,90),('R6',36,91,90),
        ('C15',34,74,90),('C16',44,81.5,0),('C17',37,77,90),
        ('C18',31,84.5,0),('C19',34.5,90.5,90),('C20',31,79.5,0),
        ('C21',31,77,0),('C22',39.5,91,90),('C23',44,86.5,0),
        ('FB1',39.5,88,90),('FB2',44,89,0)]: put(ref,x,y,a)
    put('U6',54,91,0); put('C24',59,88.5,0)
    for ref,x,y in [('R9',60,94),('R10',60,91.5),('R11',48.5,89.5),
                    ('R12',48.5,92),('R13',54,97),('R14',58,97)]: put(ref,x,y)

    # USB input protection/ramp to the left of the connector/bridge.
    for ref,x,y,a in [
        ('D1',17,92,90),('C1',21,91,90),('R1',16,97,0),('C2',12,97,0),
        ('U1',16,86,0),('C3',11.5,85,90),('C4',20.5,85,90),('C5',20.5,81.5,90),
        ('U3',23,75,0),('C10',23,78.5,0),('R2',27.5,74,0),('R3',19,75,0),
        ('D3',10,105,0),('R4',10,102,0)]: put(ref,x,y,a)
    # Compact buck cell: VIN at top/right; SW/inductor and output above.
    for ref,x,y,a in [('U2',10,73,90),('C9',11.8,70.1,90),('C6',15,71.4,0),
                      ('C8',6.5,73,90),('L1',10,65,90),('C7',10,58.5,90)]: put(ref,x,y,a)
    put('J17',6,82,90)
    for ref,x,y in [('TP1',6,94),('TP2',6,88),('TP3',27,80),('TP4',5,76)]: put(ref,x,y)

    assert placed == set(fps), f'Unplaced: {sorted(set(fps)-placed)}'

    # Mechanical holes are PCB-only NPTH, not new electrical BOM parts.
    for index,(x,y) in enumerate([(4,4),(151,4),(4,106),(151,106)],1):
        ref = f'H{index}'
        fp = p.FootprintLoad(str(libs['MountingHole']), 'MountingHole_3.2mm_M3')
        fp.SetReference(ref); fp.SetValue('M3 NPTH')
        fp.SetFPID(p.LIB_ID('MountingHole','MountingHole_3.2mm_M3'))
        fp.SetAttributes(p.FP_EXCLUDE_FROM_POS_FILES | p.FP_EXCLUDE_FROM_BOM | p.FP_BOARD_ONLY)
        fp.Value().SetVisible(False)
        board.Add(fp); fps[ref]=fp
        metadata[ref]={'mechanical_only':True}
        put(ref,x,y)

    # Resolve initial local placement against actual footprint courtyards.
    # Component anchors stay fixed; only passives/protection move by a small
    # nearest-free grid offset. Save those offsets for review. This is packing,
    # not an autorouter or a claim of final decoupling/oscillator layout.
    def courtyard(fp, margin=0):
        boxes=[g.GetBoundingBox() for g in fp.GraphicalItems() if g.GetLayer()==p.F_CrtYd]
        if not boxes: boxes=[fp.GetBoundingBox(False,False)]
        return (min(p.ToMM(b.GetLeft()) for b in boxes)-margin,
                min(p.ToMM(b.GetTop()) for b in boxes)-margin,
                max(p.ToMM(b.GetRight()) for b in boxes)+margin,
                max(p.ToMM(b.GetBottom()) for b in boxes)+margin)

    def intersects(a,b):
        return a[0]<b[2] and a[2]>b[0] and a[1]<b[3] and a[3]>b[1]

    anchors=[ref for ref in fps if ref[0] in 'UJYLH' or ref.startswith('TP')]
    occupied=[]
    for ref in anchors:
        extra = 2 if ref in ['J3','J5','J7','J9'] else 1.2 if ref.startswith('J') else .5 if ref.startswith('TP') else .15
        # No assumption of a mating plug envelope for USB and terminal; their
        # bodies sit at board edges with outward mating/actuation access.
        if ref in ['J1','J12']: extra=.15
        occupied.append((ref,courtyard(fps[ref],extra)))
    for i,(ref,a) in enumerate(occupied):
        for other,b in occupied[i+1:]:
            if intersects(a,b): print('ANCHOR ENVELOPE OVERLAP:',ref,other)
    priority=['C8','C9','C6','C7','C12','C13','R6','C26','C35','C36',
              'C43','C44','C53','C54','C63','C64','C45','C46','C55','C56','C65','C66']
    movable=[ref for ref in priority if ref not in anchors]+[ref for ref in fps if ref not in anchors and ref not in priority]
    offsets=sorted([(dx*.25,dy*.25) for dx in range(-40,41) for dy in range(-40,41)],key=lambda z:z[0]*z[0]+z[1]*z[1])
    for ref in movable:
        fp=fps[ref]; base=fp.GetPosition(); bounds=courtyard(fp,.15)
        for dx,dy in offsets:
            box=(bounds[0]+dx,bounds[1]+dy,bounds[2]+dx,bounds[3]+dy)
            if box[0]<ORIGIN[0]+.7 or box[1]<ORIGIN[1]+.7 or box[2]>ORIGIN[0]+WIDTH-.7 or box[3]>ORIGIN[1]+HEIGHT-.7: continue
            if any(intersects(box,b) for _,b in occupied): continue
            fp.SetPosition(base+vec(dx,dy)); occupied.append((ref,box))
            metadata[ref]['x_mm']+=dx; metadata[ref]['y_mm']+=dy
            metadata[ref]['packing_offset_mm']=[dx,dy]
            if dx*dx+dy*dy>16: print(f'{ref}: local spacing shift {dx:+.2f}, {dy:+.2f} mm')
            break
        else: raise RuntimeError(f'{ref}: no plausible local placement within 10 mm')

    def line(a,b,layer,width=.15):
        s=p.PCB_SHAPE(); s.SetShape(p.SHAPE_T_SEGMENT); s.SetLayer(layer)
        s.SetStart(vec(a[0]+ORIGIN[0],a[1]+ORIGIN[1])); s.SetEnd(vec(b[0]+ORIGIN[0],b[1]+ORIGIN[1]))
        s.SetWidth(p.FromMM(width)); board.Add(s)

    def label(text,x,y,layer=p.F_SilkS,size=1):
        t=p.PCB_TEXT(board); t.SetText(text); t.SetPosition(vec(x+ORIGIN[0],y+ORIGIN[1]))
        t.SetLayer(layer); t.SetTextSize(vec(size,size)); t.SetTextThickness(p.FromMM(.15)); board.Add(t)

    for a,b in [((0,0),(WIDTH,0)),((WIDTH,0),(WIDTH,HEIGHT)),
                ((WIDTH,HEIGHT),(0,HEIGHT)),((0,HEIGHT),(0,0))]: line(a,b,p.Edge_Cuts)

    # Assembly labels and component references; detailed silk cleanup comes later.
    for fp in fps.values():
        box=fp.GetBoundingBox(False,False)
        fp.Reference().SetTextAngle(p.EDA_ANGLE(-fp.GetOrientationDegrees(),p.DEGREES_T))
        fp.Reference().SetPosition(p.VECTOR2I(box.GetCenter().x,box.GetTop()-p.FromMM(.9)))
        fp.Reference().SetTextSize(vec(.8,.8)); fp.Reference().SetTextThickness(p.FromMM(.12))
    fps['J12'].Reference().SetPosition(vec(ORIGIN[0]+120.5,ORIGIN[1]+6.5))
    fps['FB2'].Reference().SetPosition(vec(ORIGIN[0]+48.5,ORIGIN[1]+85.5))
    for ref in ['H1','H2']:
        f=fps[ref]; f.Reference().SetPosition(f.GetPosition()+vec(0,5))
    for i,x in enumerate([28,68,108]): label(f'SAM{i}  TIMING / DEBUG',x,9, size=.85)
    label('GW  TIMING / DEBUG',86,108,size=.85)
    label('GW SWD',126,103,size=.85)
    label('CAN A / CAN B / RS485',139,48,size=.8)
    label('TERM A',145,24.3,size=.8); label('TERM B',145,31.3,size=.8)
    label('USB',35,106,size=.9)
    label('WS BOARD 1 - REV A',118,87,size=1.5)
    label('INITIAL PLACEMENT / UNROUTED',122,90,p.Dwgs_User,1)

    # Non-copper planning guides only; keep both trunks and probe access visible.
    for row in [58.5,70.5]:
        end_x=148 if row<60 else 151
        line((18,row),(end_x,row),p.Dwgs_User,.12)
        line((end_x,row),(end_x,45),p.Dwgs_User,.12)
    label('CAN A routing corridor',49,58.5,p.Dwgs_User,.8)
    label('CAN B routing corridor',49,70.5,p.Dwgs_User,.8)
    label('155 x 110 mm - PROVISIONAL OUTLINE',77.5,-4,p.Dwgs_User,1)
    label('No Rev B backbone / 24 V footprints',77.5,115,p.Dwgs_User,1)

    # Keep reference text readable without hiding any references or altering
    # library copper. Silk line/connector labeling can be finalized after routing.
    def text_box(t):
        bb=t.GetBoundingBox()
        return tuple(p.ToMM(v) for v in [bb.GetLeft(),bb.GetTop(),bb.GetRight(),bb.GetBottom()])
    silk_obstacles=[courtyard(fp,.05) for fp in fps.values()]
    silk_obstacles += [text_box(d) for d in board.GetDrawings() if isinstance(d,p.PCB_TEXT) and d.GetLayer()==p.F_SilkS]
    for fp in fps.values():
        for d in fp.GraphicalItems():
            if isinstance(d,p.FP_TEXT) and d.GetLayer()==p.F_SilkS: silk_obstacles.append(text_box(d))
    text_offsets=sorted([(dx*.25,dy*.25) for dx in range(-32,33) for dy in range(-32,33)],key=lambda z:z[0]*z[0]+z[1]*z[1])
    for fp in sorted(fps.values(),key=lambda f:(f.GetReference()=='FB2',len(f.GetReference())),reverse=True):
        t=fp.Reference(); base=t.GetPosition(); bounds=text_box(t)
        for dx,dy in text_offsets:
            box=(bounds[0]+dx-.12,bounds[1]+dy-.12,bounds[2]+dx+.12,bounds[3]+dy+.12)
            if box[0]<ORIGIN[0]+.4 or box[1]<ORIGIN[1]+.4 or box[2]>ORIGIN[0]+WIDTH-.4 or box[3]>ORIGIN[1]+HEIGHT-.4: continue
            if any(intersects(box,b) for b in silk_obstacles):continue
            t.SetPosition(base+vec(dx,dy)); silk_obstacles.append(box); break
        else: print('Reference text needs later cleanup:',fp.GetReference())
    board.BuildConnectivity()
    p.SaveBoard(str(OUT),board)
    (CAD/'initial_placement.json').write_text(json.dumps({
        'stage':'initial unrouted placement; PCB is editing authority',
        'origin_mm':ORIGIN,'outline_mm':[WIDTH,HEIGHT],
        'components':metadata},indent=2)+'\n')
    print(f'Saved {OUT}: {len(fps)} footprints, {len(nets)} nets, {len(board.GetTracks())} tracks/vias.')


if __name__=='__main__': main()
