#!/usr/bin/env python3
"""Initial Board 1 power/USB capture. Native KiCad 7 schematics; no PCB layout.

The .kicad_sch files become the editing authority after capture. This script is
retained as capture provenance; do not rerun over subsequent manual CAD edits.
"""
import csv, json, math, re, uuid, copy
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'boards/board1/kicad'
SYS=Path('/usr/share/kicad/symbols')
class Atom(str): pass
def parse(s):
    ts=re.findall(r'"(?:\\.|[^"\\])*"|[()]|[^\s()]+',s); i=0
    def one():
        nonlocal i
        t=ts[i]; i+=1
        if t=='(':
            a=[]
            while ts[i]!=')':a.append(one())
            i+=1;return a
        return json.loads(t) if t.startswith('"') else Atom(t)
    return one()
def dump(x):
    if isinstance(x,list):return '('+' '.join(map(dump,x))+')'
    if isinstance(x,Atom):return x
    return json.dumps(x,ensure_ascii=False)
def items(x,k):return [a for a in x if isinstance(a,list) and a and a[0]==k]
def item(x,k):return items(x,k)[0]
def uid(s):return str(uuid.uuid5(uuid.NAMESPACE_URL,'ws-hardware/board1/reva/power-usb/'+s))
def q(s):return json.dumps(str(s),ensure_ascii=False)
def fmt(x):return f'{x:.4f}'.rstrip('0').rstrip('.') if isinstance(x,float) else str(x)
def xy(p):return f'{fmt(p[0])} {fmt(p[1])}'
def effects(size=1.0,justify='',hide=False):
    return f'(effects (font (size {size} {size}))'+(f' (justify {justify})' if justify else '')+(' hide' if hide else '')+')'

rows={r['item_id']:r for r in csv.DictReader((ROOT/'boards/board1/bom.csv').open())}
cache={}
def lib(libid):
    if libid not in cache:
        if libid=='Board1:FT232HL_BusPowered':
            symbol=copy.deepcopy(lib('Interface_USB:FT232H'));symbol[1]=libid
            for part in items(symbol,'symbol'):
                part[1]=part[1].replace('FT232H_', 'FT232HL_BusPowered_')
                for p in items(part,'pin'):
                    n=item(p,'number')[1]
                    if n in ['39','44','45']:p[1]=Atom({'39':'power_out','44':'output','45':'bidirectional'}[n])
            cache[libid]=symbol
            return symbol
        a,b=libid.split(':');p=ROOT/f'libraries/symbols/{a}/{a}.kicad_sym'
        if not p.exists():p=SYS/f'{a}.kicad_sym'
        symbol=copy.deepcopy(next(s for s in items(parse(p.read_text()),'symbol') if s[1]==b))
        assert not items(symbol,'extends'),libid
        symbol[1]=libid;cache[libid]=symbol
    return cache[libid]

manifest={}; counts={}
class Sheet:
    def __init__(self,name,title,page):
        self.name=name;self.title=title;self.page=page;self.id=uid(name);self.body=[];self.wires=[];self.libs=set();self.components={};self.pins={};self.nc=set();self.serial=0
        self.path='/'+uid('board1')+(('/'+uid('usb-sheet')) if name!='board1' else '')
    def unique(self,kind):self.serial+=1;return uid(self.name+kind+str(self.serial))
    def add(self,s):self.body.append(s)
    def wire(self,*pts):
        for a,b in zip(pts,pts[1:]):
            if a==b:continue
            assert a[0]==b[0] or a[1]==b[1],(a,b)
            self.wires.append((a,b))
    def junction(self,p):self.add(f'(junction (at {xy(p)}) (diameter 0) (color 0 0 0 0) (uuid {self.unique("j")}))')
    def text(self,s,x,y,size=1.4):self.add(f'(text {q(s)} (at {x} {y} 0) {effects(size,"left top")} (uuid {self.unique("txt")}))')
    def label(self,net,p,angle=0,glob=False):
        if glob:
            self.add(f'(global_label {q(net)} (shape input) (at {xy(p)} {angle}) {effects(1.0,"left" if angle in (0,90) else "right")} (uuid {self.unique("gl")}))')
        else:self.add(f'(label {q(net)} (at {xy(p)} {angle}) {effects(1.0,"left bottom")} (uuid {self.unique("label")}))')
    def symbol(self,libid,ref,x,y,bom=None,val=None,angle=0,unit=1,fp=None,fields=None,show=None):
        l=lib(libid);self.libs.add(libid);rootname=libid.split(':')[1]
        props={s[1]:s[2] for s in items(l,'property')}
        r=rows.get(bom,{})
        value=val or r.get('mpn') or props.get('Value',rootname)
        foot=fp if fp is not None else props.get('Footprint','')
        if foot=='TBD':foot=''
        instuid=uid(f'{self.name}/{ref}/{unit}')
        # Component data fields are in the native CAD and exported BOM.
        props={'Reference':ref,'Value':value,'Footprint':foot,'Datasheet':props.get('Datasheet','')}
        if bom:props.update({'BOM_ID':bom,'MPN':r.get('mpn',value),'Manufacturer':r.get('manufacturer','TBD')})
        if fields:props.update(fields)
        if ref.startswith('#'):ib='no'; ob='no'
        else:ib=ob='yes'
        ss=[f'(symbol (lib_id {q(libid)}) (at {x} {y} {angle}) (unit {unit}) (in_bom {ib}) (on_board {ob}) (dnp no) (uuid {instuid})']
        if show is None:
            if ref.startswith(('R','C','L','FB','Y','D')):show=((x+3.2,y-1.5),(x+3.2,y+1.5),'left') if angle==0 else ((x,y-5.2),(x,y-2.6),'')
            else:show=((x,y-19),(x,y-16),'')
        for idx,(key,v) in enumerate(props.items()):
            if key in ('Reference','Value'):
                pos=show[0 if key=='Reference' else 1];eff=effects(1.15 if key=='Reference' else 1.0,show[2],hide=ref.startswith('#') and key=='Reference')
            else:pos=(x,y);eff=effects(1.0,hide=True)
            ss.append(f'(property {q(key)} {q(v)} (at {xy(pos)} {angle % 180}) {eff})')
        pins=[]
        for part in items(l,'symbol'):
            match=re.search(r'_(\d+)_(\d+)$',part[1])
            if match and int(match[1]) in (0,unit):pins+=items(part,'pin')
        for p in pins:
            n=item(p,'number')[1];a=item(p,'at');px,py,pa=map(float,a[1:4]);rad=math.radians(angle)
            loc=(round(x+px*math.cos(rad)-py*math.sin(rad),4),round(y-px*math.sin(rad)-py*math.cos(rad),4))
            self.pins[(ref,n)]=(loc,(pa+angle)%360)
            ss.append(f'(pin {q(n)} (uuid {uid(ref+"/pin/"+n)}))')
        ss.append(f'(instances (project "board1" (path {q(self.path)} (reference {q(ref)}) (unit {unit})))) )')
        self.add('\n'.join(ss));self.components[ref]={'lib_id':libid,'BOM_ID':bom,'MPN':props.get('MPN',value),'value':value,'footprint':foot,'sheet':self.name}
        manifest.setdefault(ref,dict(self.components[ref],pins={}))
        return ref
    def pt(self,ref,pin):return self.pins[(ref,str(pin))][0]
    def net(self,ref,pin,net,length=7.62,glob=False):
        pin=str(pin);p,a=self.pins[(ref,pin)];rad=math.radians(a)
        end=(round(p[0]-length*math.cos(rad),4),round(p[1]+length*math.sin(rad),4))
        self.wire(p,end)
        if net=='GND':self.ground(end)
        else:self.label(net,end,90 if a==270 else 270 if a==90 else 0,glob)
        manifest[ref]['pins'][pin]=net
        return end
    def mark(self,ref,pins,net):
        for pin in pins:manifest[ref]['pins'][str(pin)]=net
    def noconnect(self,ref,pin):
        p=self.pt(ref,pin);self.add(f'(no_connect (at {xy(p)}) (uuid {self.unique("nc")}))');self.nc.add((ref,str(pin)));manifest[ref]['pins'][str(pin)]=None
    def ground(self,p):
        self.serial+=1;ref=f'#PWR{self.page}{self.serial:03}'
        self.symbol('power:GND',ref,*p,val='GND',show=((p[0],p[1]+5),(p[0],p[1]+5),''))
    def passive(self,kind,ref,x,y,bom,value,net1,net2,angle=0,fp=None,glob=False):
        self.symbol('Device:'+kind,ref,x,y,bom,val=value,angle=angle,fp=fp)
        self.net(ref,1,net1,3.81,glob);self.net(ref,2,net2,3.81,glob)
    def save(self):
        # KiCad connectivity requires segments to terminate at each T junction.
        ends={p for ab in self.wires for p in ab}|{v[0] for v in self.pins.values()}
        for a,b in self.wires:
            pts=sorted(p for p in ends if min(a[0],b[0])<=p[0]<=max(a[0],b[0]) and min(a[1],b[1])<=p[1]<=max(a[1],b[1]))
            for p1,p2 in zip(pts,pts[1:]):
                self.add(f'(wire (pts (xy {xy(p1)}) (xy {xy(p2)})) (stroke (width 0) (type default)) (uuid {self.unique("wire")}))')
        libtext='\n'.join(dump(cache[n]) for n in sorted(self.libs))
        header=f'(kicad_sch (version 20230121) (generator ws_hardware_capture) (uuid {self.id}) (paper "A3")\n(title_block (title {q(self.title)}) (date "2026-09-07") (rev "A-draft") (company "WireSpaces") (comment 1 "Power / USB capture only - no PCB layout"))\n(lib_symbols\n{libtext}\n)\n'
        if self.page==1:self.add('(sheet_instances (path "/" (page "1")))')
        (OUT/(self.name+'.kicad_sch')).write_text(header+'\n'.join(self.body)+'\n)\n')

CAP='Capacitor_SMD:C_0805_2012Metric';RES='Resistor_SMD:R_0805_2012Metric'
R1206='Resistor_SMD:R_1206_3216Metric';C1206='Capacitor_SMD:C_1206_3216Metric';C1210='Capacitor_SMD:C_1210_3225Metric'
def cap(s,ref,x,y,bid,value,net,fp=CAP,glob=True):s.passive('C',ref,x,y,bid,value,net,'GND',fp=fp,glob=glob)
def pull(s,ref,x,y,bid,rail,net):s.passive('R',ref,x,y,bid,'10k',rail,net,fp=RES,glob=True)
def flag(s,x,y,net,glob=False):
    ref='#FLG'+str(s.page)+str(s.serial)
    s.symbol('power:PWR_FLAG',ref,x,y,val='PWR_FLAG',show=((x,y-5),(x,y-5),''));s.net(ref,1,net,5.08,glob)

def capture():
    OUT.mkdir(parents=True,exist_ok=True)
    s=Sheet('board1','Board 1 - USB input and main power',1)
    s.text('USB-B INPUT AND ATTACHMENT RAMP',20,20,2)
    s.text('3.3 V MAIN BUCK',263,20,2)
    s.symbol('Connector:USB_B','J1',35,65,'B1-B005',fp='Connector_USB:USB_B_OST_USB-B1HSxx_Horizontal',show=((30,51),(30,54),'left'))
    s.symbol('TPS22810DBVT:TPS22810DBVT','U1',175,65,'B1-B044',show=((175,43),(175,46),''))
    s.symbol('Device:D','D1',70,85,'B1-B006',angle=270,fp='Diode_SMD:D_SOD-123F',show=((74,83),(74,86),'left'))
    s.symbol('Device:C','C1',95,85,'B1-B045',val='1u / 25V',fp=CAP)
    s.symbol('Device:R','R1',120,82,'B1-B047',val='1R / pulse',fp=R1206)
    s.symbol('Device:C','C2',120,103,'B1-B046',val='4u7 / 50V',fp=CAP)
    s.symbol('Device:C','C3',150,95,'B1-B048',val='47n',fp=CAP)
    rail_y=s.pt('J1',1)[1]
    s.wire(s.pt('J1',1),(150,rail_y),s.pt('U1',1))
    for ref in ['D1','C1','R1']:
        a=s.pt(ref,1);s.wire(a,(a[0],rail_y));s.junction((a[0],rail_y));s.mark(ref,[1],'VBUS_RAW')
    s.label('VBUS_RAW',(80,rail_y))
    s.wire(s.pt('U1',3),(150,65),(150,rail_y));s.junction((150,rail_y));s.mark('J1',[1],'VBUS_RAW');s.mark('U1',[1,3],'VBUS_RAW')
    s.wire(s.pt('R1',2),s.pt('C2',1));s.mark('R1',[2],'VBUS_DAMP');s.mark('C2',[1],'VBUS_DAMP')
    s.label('VBUS_DAMP',(120,92))
    for ref,pin in [('D1',2),('C1',2),('C2',2),('C3',2),('U1',2)]:s.net(ref,pin,'GND',5.08)
    s.wire(s.pt('J1',5),(32.46,82),(35,82),s.pt('J1',4));s.ground((35,82));s.mark('J1',[4,5],'GND')
    s.wire(s.pt('U1',4),(150,70.08),s.pt('C3',1));s.mark('U1',[4],'IN_CT');s.mark('C3',[1],'IN_CT');s.label('IN_CT',(150,80))
    s.wire(s.pt('U1',6),(245,rail_y));s.wire(s.pt('U1',5),(205,65),(205,rail_y));s.junction((205,rail_y));s.mark('U1',[5,6],'USB_5V');s.label('USB_5V',(215,rail_y),glob=True)
    for ref,x,bid,v in [('C4',220,'B1-B063','4u7'),('C5',243,'B1-B061','100n')]:
        s.symbol('Device:C',ref,x,85,bid,val=v,fp=CAP);s.wire(s.pt(ref,1),(x,rail_y));s.junction((x,rail_y));s.mark(ref,[1],'USB_5V');s.net(ref,2,'GND',5.08)
    s.text('C4/C5: place at FTDI VREGIN (U4 pin 40).',205,104,1.15)
    s.net('J1',2,'USB_DM',20.32,True);s.net('J1',3,'USB_DP',20.32,True)
    s.text('USB shield bonds directly to GND at entry.',20,112,1.15)
    s.text('USB DATA ESD',20,126,1.6)
    s.symbol('RCLAMP0504S.TCT:RCLAMP0504S.TCT','D2',65,158,'B1-B018',show=((78,138),(78,141),'left'))
    s.net('D2',1,'USB_DM',10.16,True);s.net('D2',3,'USB_DP',10.16,True);s.net('D2',2,'GND')
    for p in [4,5,6]:s.noconnect('D2',p)
    s.text('Pin 5 VREF unconnected: internal TVS mode.\nUnused channels 4/6 unconnected. Place at J1.\nRoute USB differential pair directly; avoid stubs.',20,179,1.1)
    s.symbol('TPS560430X3FDBVR:TPS560430X3FDBVR','U2',300,65,'B1-B012',show=((300,39),(300,42),''))
    s.wire((245,rail_y),s.pt('U2',5));s.mark('U2',[5],'USB_5V')
    s.symbol('Device:C','C6',270,85,'B1-B029',val='10u / 35V',fp=C1206);s.wire(s.pt('C6',1),(270,rail_y));s.mark('C6',[1],'USB_5V');s.junction((270,rail_y));s.net('C6',2,'GND')
    cap(s,'C9',290,115,'B1-B052','100n','USB_5V')
    s.symbol('Device:L','L1',345,65,'B1-B028',val='12uH',angle=90,fp='Inductor_SMD:L_Bourns_SRN6045TA')
    s.wire(s.pt('U2',6),s.pt('L1',1));s.mark('U2',[6],'BUCK_SW');s.mark('L1',[1],'BUCK_SW')
    s.symbol('Device:C','C8',327.94,48,'B1-B031',val='100n',angle=90,fp=CAP)
    s.wire(s.pt('U2',1),(315.24,48),s.pt('C8',1));s.mark('U2',[1],'BUCK_CB');s.mark('C8',[1],'BUCK_CB')
    s.wire(s.pt('C8',2),(335.28,48),(335.28,65));s.junction((335.28,65));s.mark('C8',[2],'BUCK_SW')
    s.label('BUCK_SW',(319,65));s.label('BUCK_CB',(315.24,48))
    s.wire(s.pt('L1',2),(380,65));s.mark('L1',[2],'3V3_SYS');s.label('3V3_SYS',(380,65),glob=True)
    s.symbol('Device:C','C7',375,85,'B1-B030',val='22u / 16V',fp=C1210);s.wire(s.pt('C7',1),(375,65));s.mark('C7',[1],'3V3_SYS');s.junction((375,65));s.net('C7',2,'GND')
    s.wire(s.pt('U2',3),(365,70.08),(365,65));s.junction((365,65));s.mark('U2',[3],'3V3_SYS');s.net('U2',2,'GND')
    s.net('U2',4,'BUCK_EN',7.62,True)
    s.text('Fixed X3F: FB senses output directly.\nKeep CB-SW loop short; quiet FB route.\nNo divider, catch diode or external compensation.',310,108,1.1)
    s.text('USB CONFIGURATION / SUSPEND CONTROL',155,133,1.6)
    s.symbol('MC74HC1G14DBVT1G:MC74HC1G14DBVT1G','U3',235,168,'B1-B015',show=((248,148),(248,151),''))
    s.net('U3',2,'PWREN_N',10.16,True);s.net('U3',4,'BUCK_EN',10.16,True);s.net('U3',5,'FTDI_3V3',5.08,True);s.net('U3',3,'GND');s.noconnect('U3',1)
    pull(s,'R2',180,166,'B1-B054','FTDI_3V3','PWREN_N')
    s.passive('R','R3',280,178,'B1-B055','47k','BUCK_EN','GND',fp=RES,glob=True)
    cap(s,'C10',310,178,'B1-B061','100n','FTDI_3V3')
    s.text('PWREN_N low: main rail ON, VCP buffers enabled.\nHigh / floating: main rail OFF (ADR-040).',155,199,1.15)
    s.text('POWER INDICATOR',343,133,1.5)
    s.symbol('Device:R','R4',360,158,'B1-B026',val='3k3',fp=RES);s.net('R4',1,'3V3_SYS',5.08,True)
    s.symbol('Device:LED','D3',360,177,'B1-B025',val='Orange',angle=90,fp='LED_SMD:LED_0603_1608Metric',show=((364,175),(364,178),'left'))
    s.wire(s.pt('R4',2),s.pt('D3',2));s.mark('R4',[2],'PWR_LED_A');s.mark('D3',[2],'PWR_LED_A');s.label('PWR_LED_A',(360,168));s.net('D3',1,'GND',5.08)
    s.add(f'(sheet (at 25 223) (size 105 30) (stroke (width 0) (type solid)) (fill (color 0 0 0 0)) (uuid {uid("usb-sheet")}) (property "Sheetname" "USB bridge and VCP" (at 25 222 0) {effects(1.27,"left bottom")}) (property "Sheetfile" "usb_bridge.kicad_sch" (at 25 254 0) {effects(1.27,"left top")}) (instances (project "board1" (path "/{uid("board1")}" (page "2")))))')
    s.text('USB_5V / USB_DM / USB_DP\nFTDI_3V3 / PWREN_N / 3V3_SYS\nCross-sheet connections use named global nets.',30,229,1.25)
    s.text('USB-only, active-PC bench operation. 500 mA configured input budget.\nPower/USB capture ends at GW_VCP_TX/RX/RTS_N/CTS_N.\nMCU, CAN, RS-485 and timing-header sections are not captured.\nNo external reset supervisor or CBUS recovery circuitry.',155,222,1.3)
    flag(s,160,266,'VBUS_RAW');flag(s,205,266,'GND');flag(s,250,266,'3V3_SYS',True)
    s.save()

    s=Sheet('usb_bridge','Board 1 - FT232HL, EEPROM and isolated VCP',2)
    s.text('INDEPENDENT USB BRIDGE',20,20,2)
    s.text('CONFIGURATION EEPROM',175,20,1.8)
    s.text('VCP POWER-OFF ISOLATION',270,20,1.8)
    s.symbol('Board1:FT232HL_BusPowered','U4',100,100,'B1-B004',val='FT232HL-REEL',fp='Package_QFP:LQFP-48_7x7mm_P0.5mm',show=((78,64),(112,64),''))
    for p,n in {40:'USB_5V',39:'FTDI_3V3',38:'FTDI_VCORE',37:'FTDI_VCCA',6:'USB_DM',7:'USB_DP',34:'FTDI_RESET_N',5:'FTDI_REF',45:'EECS',44:'EECLK',43:'EEDATA',1:'XTIN',2:'XTOUT'}.items():s.net('U4',p,n,20.32,n in ['USB_5V','FTDI_3V3','USB_DM','USB_DP'])
    for p,n in {13:'FTDI_TX',14:'FTDI_RX',15:'FTDI_RTS_N',16:'FTDI_CTS_N',21:'PWREN_N'}.items():s.net('U4',p,n,10.16,True)
    for p in [17,18,19,20,25,26,27,28,29,30,31,32,33]:s.noconnect('U4',p)
    for p in [3,8]:s.net('U4',p,'FTDI_VPHY' if p==3 else 'FTDI_VPLL',15.24)
    for p in [12,24,46]:s.net('U4',p,'FTDI_3V3',7.62,True)
    for p in [4,9,10,11,22,23,35,36,41,47,48]:
        pt=s.pt('U4',p);s.wire(pt,(pt[0],145.72));s.mark('U4',[p],'GND')
    s.wire((89.84,145.72),(115.24,145.72));s.ground((102.54,145.72))
    for p in [9,10,11,22,23,35,36,41,47]:s.junction((s.pt('U4',p)[0],145.72))
    s.net('U4',42,'GND',5.08)
    s.text('Unused ADBUS/ACBUS pins: no connection.\nACBUS5/6 recovery deferred to Rev B.\nVCCA and VCORE each bypass only; never join.',160,110,1.15)
    # Local crystal and reset/reference networks.
    s.symbol('Device:Crystal','Y1',35,135,'B1-B014',val='12MHz / CL18p',fp='Crystal:Crystal_SMD_HC49-SD')
    s.net('Y1',1,'XTIN',7.62);s.net('Y1',2,'XTOUT',7.62)
    cap(s,'C12',20,155,'B1-B058','27p C0G','XTIN',glob=False);cap(s,'C13',48,155,'B1-B058','27p C0G','XTOUT',glob=False)
    s.symbol('Device:R','R5',25,58,'B1-B051',val='10k',fp=RES);s.net('R5',1,'FTDI_3V3',3.81,True)
    s.symbol('Device:C','C14',25,91,'B1-B064',val='10n',fp=CAP);s.net('C14',2,'GND',3.81)
    s.wire(s.pt('R5',2),s.pt('C14',1));s.label('FTDI_RESET_N',(25,75));s.mark('R5',[2],'FTDI_RESET_N');s.mark('C14',[1],'FTDI_RESET_N')
    s.passive('R','R6',47,91,'B1-B057','12k 1%','FTDI_REF','GND',fp=RES)
    s.symbol('AT93C56B-SSHM-B:AT93C56B-SSHM-B','U5',215,75,'B1-B013',show=((228,44),(228,47),''))
    for p,n in {1:'EECS',2:'EECLK',3:'EEDATA',6:'FTDI_3V3',8:'FTDI_3V3'}.items():s.net('U5',p,n,7.62,p in[6,8])
    s.net('U5',5,'GND');s.noconnect('U5',7)
    s.symbol('Device:R','R7',246,72.46,'B1-B056',val='2k2',angle=90,fp=RES)
    s.wire(s.pt('U5',4),s.pt('R7',1));s.mark('U5',[4],'EE_DO');s.mark('R7',[1],'EE_DO');s.label('EE_DO',(232,72.46));s.net('R7',2,'EEDATA',5.08)
    pull(s,'R8',246,95,'B1-B065','FTDI_3V3','EE_DO')
    s.text('ORG=VCC: 128 x 16 words.\nEEDATA to DI; DO through 2k2.\n10k pull-up belongs on DO side.',170,136,1.15)
    # Reference-circuit capacitor population, intentionally omitting optional bulk after beads.
    s.text('FTDI LOCAL SUPPLY DECOUPLING',20,174,1.5)
    for ref,x,bid,v,n in [('C15',25,'B1-B063','4u7','FTDI_3V3'),('C16',52,'B1-B061','100n','FTDI_3V3'),('C17',85,'B1-B061','100n','FTDI_3V3'),('C18',115,'B1-B061','100n','FTDI_3V3'),('C19',145,'B1-B061','100n','FTDI_3V3'),('C20',180,'B1-B061','100n','FTDI_VCORE'),('C21',215,'B1-B061','100n','FTDI_VCCA'),('C11',246,'B1-B061','100n','FTDI_3V3')]:cap(s,ref,x,197,bid,v,n,glob=n=='FTDI_3V3')
    s.text('VCCD pin 39',20,211,1.1);s.text('VCCIO pins 12 / 24 / 46',82,211,1.1);s.text('38',177,211,1.1);s.text('37',212,211,1.1);s.text('U5 pin 8',239,211,1.1)
    for ref,x,y,n,cref in [('FB1',50,233,'FTDI_VPHY','C22'),('FB2',180,233,'FTDI_VPLL','C23')]:
        s.symbol('Device:FerriteBead',''+ref,x,y,'B1-B078',val='600R @ 100MHz',angle=90,fp='Inductor_SMD:L_0805_2012Metric',fields={'MPN':'BLM21AG601SN1D','Manufacturer':'Murata'})
        s.net(ref,1,'FTDI_3V3',10.16,True);s.net(ref,2,n,12.7)
        cap(s,cref,x+35,244,'B1-B061','100n',n,glob=False)
    s.text('Separate ferrite + 100n at VPHY pin 3 and VPLL pin 8.\nFTDI Fig.6.1 optional post-bead bulk not fitted; no DNP footprints.\nAll AGND/GND pins join the board ground plane.',20,261,1.1)
    flag(s,120,239,'FTDI_VPHY');flag(s,245,239,'FTDI_VPLL')
    # One quad buffer; both directions use receiving-domain defaults.
    gates=[(1,65,2,3,1,'FTDI_TX','GW_VCP_RX'),(2,108,5,6,4,'FTDI_RTS_N','GW_VCP_CTS_N'),(3,151,9,8,10,'GW_VCP_TX','FTDI_RX'),(4,194,12,11,13,'GW_VCP_RTS_N','FTDI_CTS_N')]
    for un,y,ap,yp,oe,inn,outn in gates:
        s.symbol('SN74LV125APWR:SN74LV125APWR','U6',310,y,'B1-B016',unit=un,show=((336,y-18),(336,y-15),''))
        s.net('U6',ap,inn,12.7,True);s.net('U6',yp,outn,12.7,True);s.net('U6',oe,'PWREN_N',5.08,True)
        pull(s,'R'+str(8+un),370,y,'B1-B079','3V3_SYS' if un<=2 else 'FTDI_3V3',outn)
    pull(s,'R13',270,151,'B1-B079','3V3_SYS','GW_VCP_TX')
    pull(s,'R14',270,194,'B1-B079','3V3_SYS','GW_VCP_RTS_N')
    s.symbol('SN74LV125APWR:SN74LV125APWR','U6',345,228,'B1-B016',unit=5,show=((361,213),(361,216),''))
    s.net('U6',14,'3V3_SYS',5.08,True);s.net('U6',7,'GND',5.08);cap(s,'C24',385,233,'B1-B036','100n','3V3_SYS')
    s.text('GW_* directions are from the MCU. TX/RX idle high; CTS_N inactive high.\nAll /OE pins directly use PWREN_N (ADR-040).\nThese four GW nets end at the next capture stage.',152,153,1.0)
    s.save()
    custom=copy.deepcopy(cache['Board1:FT232HL_BusPowered']);custom[1]='FT232HL_BusPowered'
    (OUT/'board1_symbols.kicad_sym').write_text('(kicad_symbol_lib (version 20220914) (generator ws_hardware_capture)\n'+dump(custom)+'\n)\n')
    project=json.loads(Path('/usr/share/kicad/template/kicad.kicad_pro').read_text())
    project['meta']['filename']='board1.kicad_pro';project['sheets']=[[uid('board1'),'USB input and power'],[uid('usb_bridge'),'USB bridge and VCP']]
    project['text_variables']={'ASSEMBLY_REV':'A-draft','CAPTURE_SCOPE':'Power and USB only'}
    (OUT/'board1.kicad_pro').write_text(json.dumps(project,indent=2)+'\n')
    # Export complete component/pin intent for checking the independently parsed KiCad netlist.
    manifest_real={r:v for r,v in manifest.items() if not r.startswith('#')}
    (OUT/'capture_manifest.json').write_text(json.dumps(manifest_real,indent=2)+'\n')
    print(f'Captured {len(manifest_real)} physical parts in two native schematic sheets.')

if __name__=='__main__':capture()
