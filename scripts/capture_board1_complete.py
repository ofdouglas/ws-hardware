#!/usr/bin/env python3
"""One-time full-board native capture. Source CAD is authoritative after capture.

Uses preserved power/USB files; never regenerate over subsequent manual edits.
"""
import copy
import csv
import json
from pathlib import Path
import capture_board1_power_usb as c

ROOT=c.ROOT;OUT=c.OUT;A=c.Atom
NEWROOT=c.uid('complete-root')
NODES=['GW','SAM0','SAM1','SAM2']
PAGES=[('power','USB input and power'),('usb_bridge','USB bridge and VCP'),
       ('gateway','Gateway STM32G474'),('sam0','SAM0'),('sam1','SAM1'),('sam2','SAM2'),
       ('can_a','CAN A'),('can_b','CAN B'),('interfaces','UART and external terminals'),('access','Test access')]
COUNTERS={'U':6,'C':24,'R':14,'D':3,'J':1,'Y':1,'TP':0}
def ref(prefix):COUNTERS[prefix]+=1;return prefix+str(COUNTERS[prefix])
original_lib=c.lib
def lib(lid):
    if lid in c.cache:return c.cache[lid]
    if lid=='MCU_ST_STM32G4:STM32G474RBTx':
        tree=c.parse((c.SYS/'MCU_ST_STM32G4.kicad_sym').read_text())
        child=next(x for x in c.items(tree,'symbol') if x[1]=='STM32G474RBTx')
        parent=c.item(child,'extends')[1]
        s=copy.deepcopy(next(x for x in c.items(tree,'symbol') if x[1]==parent));s[1]=lid
        s=[v for v in s if not(isinstance(v,list) and v[0]=='property')]
        s+=copy.deepcopy(c.items(child,'property'))
        for unit in c.items(s,'symbol'):unit[1]=unit[1].replace(parent,'STM32G474RBTx')
        c.cache[lid]=s;return s
    return original_lib(lid)
c.lib=lib

class Sheet(c.Sheet):
    def __init__(self,name,title,page):
        super().__init__(name,'Board 1 - '+title,page)
        self.path='/'+NEWROOT+'/'+c.uid(name+'-sheet')
    def net(self,ref,pin,net,length=7.62,glob=False):
        pin=str(pin);p,a=self.pins[ref,pin];rad=c.math.radians(a)
        end=(round(p[0]-length*c.math.cos(rad),4),round(p[1]+length*c.math.sin(rad),4))
        self.wire(p,end)
        angle={0:180,180:0,270:90,90:270}[a]
        if net=='GND' and a in (90,270):self.ground(end)
        else:self.label(net,end,angle,glob or net=='GND')
        c.manifest[ref]['pins'][pin]=net
        return end
    def save(self):
        super().save();p=OUT/(self.name+'.kicad_sch')
        p.write_text(p.read_text().replace('Power / USB capture only - no PCB layout','Rev A complete schematic draft - no PCB layout'))

def sym(s,lid,prefix,x,y,bid,**kw):
    r=ref(prefix);s.symbol(lid,r,x,y,bid,**kw);return r
def passive(s,kind,x,y,bid,value,n1,n2,angle=0):
    r=ref(kind);s.passive(kind,r,x,y,bid,value,n1,n2,angle=angle,fp=c.RES if kind=='R' else c.CAP,glob=True);return r
def cap(s,x,y,bid,v,n='3V3_SYS'):return passive(s,'C',x,y,bid,v,n,'GND')
def pull(s,x,y,bid,n,down=False):return passive(s,'R',x,y,bid,'10k',n if down else '3V3_SYS','GND' if down else n)
def supplies(s,r,ps,n):
    # Shared bus for top/bottom supply pins; stacked pins remain explicitly mapped.
    coords=sorted(set(s.pt(r,p) for p in ps));directions={s.pins[r,str(p)][1] for p in ps}
    if directions=={270.0} or directions=={90.0}:
        dy=-5.08 if 270.0 in directions else 5.08;y=round(coords[0][1]+dy,4)
        for p in coords:s.wire(p,(p[0],y));s.junction((p[0],y))
        s.wire((coords[0][0],y),(coords[-1][0],y))
        if n=='GND':s.ground((coords[-1][0],y))
        else:s.label(n,(coords[-1][0],y),90,True)
        s.mark(r,ps,n)
    else:
        for p in ps:s.net(r,p,n,5.08,True)

def norm(n):
    return n.replace('_MCU','').replace('_FD_CAN_','_CAN_').replace('_UART_MD_TX','_MD_TX') if n else None

def mcu(node,plan,page):
    name='gateway' if node=='GW' else node.lower();s=Sheet(name,node+' MCU, debug and timing',page)
    s.text(node+' / '+plan['mpn'],20,20,2)
    s.text('TIMING / TEXT DEBUG',218,20,1.7);s.text('INDEPENDENT SWD',318,126,1.6)
    r=sym(s,plan['symbol'],'U',100,107,'B1-B001' if node=='GW' else 'B1-B002',fp=plan['footprint'],show=((78,45),(120,45),''))
    pins={int(p['pad']):norm(p['net']) for p in plan['pins']}
    for p,n in pins.items():
        if n is None:s.noconnect(r,p)
        elif n not in ['GND','3V3_SYS']:s.net(r,p,n,7.62,True)
    for net in ['3V3_SYS','GND']:
        top=[p for p,n in pins.items() if n==net and s.pins[r,str(p)][1] in [270,90]]
        supplies(s,r,top,net)
        for p,n in pins.items():
            if n==net and p not in top:s.net(r,p,n,7.62,True)
    # Exact resistor on every header signal; MCU and header nets stay separate.
    order=['DEBUG_RX','DEBUG_TX','SYNC','TRIG','EVENT0','EVENT1']
    for i,signal in enumerate(order):
        header=signal if signal in ['SYNC','TRIG'] else node+'_'+signal+'_HDR'
        passive(s,'R',242,47+20*i,'B1-B076','330R',node+'_'+signal,header,90)
    j=sym(s,'Connector_Generic:Conn_01x08','J',354,72,'B1-B059',fp='Connector_PinHeader_2.54mm:PinHeader_1x08_P2.54mm_Vertical',show=((343,49),(343,52),'left'),val=node+' timing/debug')
    for p,n in {1:node+'_DEBUG_RX_HDR',2:node+'_DEBUG_TX_HDR',3:'GND',4:'SYNC',5:'TRIG',6:'GND',7:node+'_EVENT0_HDR',8:node+'_EVENT1_HDR'}.items():s.net(j,p,n,10.16,True)
    s.text('330R at each MCU pad. Header is 3.3 V logic.\nRX/TX names use the MCU perspective.\nOne external source per global SYNC / TRIG.\nDrive only while SYS is on; disconnect before suspend.',291,94,1.1)
    # Conventional independent reset; BOOT0 only on the gateway.
    pull(s,175,54,'B1-B080',node+'_RESET_N')
    cap(s,175,94,'B1-B081' if node=='GW' else 'B1-B082','100n' if node=='GW' else '10n',node+'_RESET_N')
    pull(s,175,140,'B1-B060',node+'_DEBUG_RX')
    if node=='GW':pull(s,200,180,'B1-B080','GW_BOOT0',True)
    else:pull(s,200,180,'B1-B080',node+'_SWCLK')
    j=sym(s,'Connector_Generic:Conn_02x05_Odd_Even','J',346,156,'B1-B009',fp='Board1:CNC_Tech_3220-10-0100-00_2x05_P1.27mm_Vertical',val=node+' SWD',show=((346,139),(346,142),''))
    for p,n in {1:'3V3_SYS',2:node+'_SWDIO',3:'GND',4:node+'_SWCLK',5:'GND',9:'GND',10:node+'_RESET_N'}.items():s.net(j,p,n,7.62,True)
    for p in [6,7,8]:s.noconnect(j,p)
    s.text('VTref is sense only; probe must not power target.\n6 SWO / 8 TDI unused; 7 is NC / key position.\nConfirm cable key before insertion. Reset on pin 10.',291,178,1.1)
    # Per-pin bypass + accepted local bulk. STM32 VREFBUF must be high impedance.
    s.text('LOCAL SUPPLIES',20,181,1.5)
    bypass=[16,32,48,64,28,1] if node=='GW' else [6,17,36,44]
    for i,p in enumerate(bypass):
        x=25+i*27;cap(s,x,202,'B1-B036','100n');s.text('pin '+str(p),x-3,216,1.0)
    cap(s,25,244,'B1-B037','1u')
    if node=='GW':
        cap(s,65,244,'B1-B038','4u7');cap(s,105,244,'B1-B039','10n')
        s.text('1u shared VDDA/VREF+ bulk; 10n at VDDA pin29.\nVREFBUF disabled / high-Z; VBAT tied to main rail.\nRetain NRST function / normal Flash boot option bytes.',20,266,1.1)
        xin,xout='GW_HSE_IN','GW_HSE_OUT'
    else:
        cap(s,65,244,'B1-B040','1u',node+'_VDDCORE');cap(s,105,244,'B1-B041','100n',node+'_VDDCORE')
        s.text('1u main bulk; separate VDDCORE output capacitors.\nNever join core rails or connect them to 3V3_SYS.\nEIC: synchronous mode; clear flags after enabling.',20,266,1.1)
        xin,xout=node+'_XIN',node+'_XOUT'
    y=sym(s,'Device:Crystal','Y',231,222,'B1-B019' if node=='GW' else 'B1-B020',fp='Crystal:Crystal_SMD_ECS_CSM3X-2Pin_7.6x4.1mm',val='12MHz / CL20p')
    s.net(y,1,xin,7.62,True);s.net(y,2,xout,7.62,True)
    cap(s,212,246,'B1-B042' if node=='GW' else 'B1-B043','33p C0G',xin);cap(s,252,246,'B1-B042' if node=='GW' else 'B1-B043','33p C0G',xout)
    ledR=sym(s,'Device:R','R',344,211,'B1-B026',val='3k3',fp=c.RES);s.net(ledR,1,node+'_LED',3.81,True)
    d=sym(s,'Device:LED','D',344,237,'B1-B024',angle=90,fp='LED_SMD:LED_0603_1608Metric',val='Orange',show=((349,235),(349,238),'left'))
    s.wire(s.pt(ledR,2),s.pt(d,2));s.mark(ledR,[2],node+'_LED_A');s.mark(d,[2],node+'_LED_A');s.label(node+'_LED_A',(344,225),0,True);s.net(d,1,'GND',5.08)
    s.save()

def can(which,page):
    s=Sheet('can_'+which.lower(),'CAN '+which+' / four independent PHYs',page)
    s.text('FD_CAN_'+which+'  /  GW + SAM0 + SAM1 + SAM2',20,20,2)
    for i,node in enumerate(NODES):
        x=85+200*(i%2);y=75+98*(i//2)
        r=sym(s,'TCAN3413DR:TCAN3413DR','U',x,y,'B1-B003',show=((x-8,y-28),(x+12,y-25),''))
        for p,n in {1:node+'_CAN_'+which+'_TX',4:node+'_CAN_'+which+'_RX',8:node+'_CAN_'+which+'_STB',6:'FD_CAN_'+which+'_L',7:'FD_CAN_'+which+'_H'}.items():s.net(r,p,n,10.16,True)
        supplies(s,r,[3,5],'3V3_SYS');s.net(r,2,'GND',5.08)
        cap(s,x+56,y-2,'B1-B036','100n');cap(s,x+88,y-2,'B1-B036','100n')
        s.text('VCC pin3',x+48,y+12,1.0);s.text('VIO pin5',x+82,y+12,1.0)
        pull(s,x-44,y+31,'B1-B083',node+'_CAN_'+which+'_STB')
        s.text(node,x-25,y-30,1.4)
    # Two endpoint terminations; terminal-side jumper is series with its resistor.
    s.text('LINEAR TRUNK: far onboard end -> four short PHY branches -> terminal / cable end',56,222,1.2)
    passive(s,'R',48,245,'B1-B067','120R','FD_CAN_'+which+'_H','FD_CAN_'+which+'_L')
    r=passive(s,'R',156,245,'B1-B067','120R','FD_CAN_'+which+'_H','CAN_'+which+'_TERM_RETURN')
    j=sym(s,'Connector_Generic:Conn_01x02','J',228,245,'B1-B069',fp='Connector_PinHeader_2.54mm:PinHeader_1x02_P2.54mm_Vertical',val='TERM '+which,show=((228,235),(228,238),''))
    s.net(j,1,'CAN_'+which+'_TERM_RETURN',7.62,True);s.net(j,2,'FD_CAN_'+which+'_L',7.62,True)
    s.text('Fixed far end',25,266,1.2);s.text('Fit shunt for board-only; remove when cable extends this end.\nRemote cable endpoint must have its own 120R termination.',170,267,1.1)
    s.text('STB defaults high: standby.\nSet TX idle high before enabling PHY.\nNo additional CAN channels or chokes.',285,227,1.1)
    s.save()

def interfaces(page):
    s=Sheet('interfaces','UART multidrop, RS-485 and terminals',page)
    s.text('ONBOARD OPEN-DRAIN UART',20,20,1.8)
    u=ref('U');gates=[(1,2,3,1),(2,5,6,4),(3,9,8,10),(4,12,11,13)]
    for i,(unit,ap,yp,oe) in enumerate(gates):
        x=66+125*(i%2);y=65+78*(i//2)
        s.symbol('SN74LV125APWR:SN74LV125APWR',u,x,y,'B1-B066',unit=unit,show=((x+12,y-22),(x+12,y-19),''))
        s.net(u,ap,'GND',5.08);s.net(u,yp,'UART_MD',10.16,True);s.net(u,oe,NODES[i]+'_MD_TX',5.08,True)
        pull(s,x+47,y,'B1-B008',NODES[i]+'_MD_TX')
    s.symbol('SN74LV125APWR:SN74LV125APWR',u,64,228,'B1-B066',unit=5,show=((80,209),(80,212),''))
    s.net(u,14,'3V3_SYS',5.08,True);s.net(u,7,'GND',5.08);cap(s,112,228,'B1-B036','100n')
    passive(s,'R',167,228,'B1-B074','470R','3V3_SYS','UART_MD')
    for i,n in enumerate(['SYNC','TRIG']):passive(s,'R',220+40*i,228,'B1-B077','10k',n,'GND')
    s.text('All four RX inputs observe UART_MD.\nTX high releases; TX low sinks. No active-high drivers.\nRate depends on measured rise time; firmware arbitrates.',20,266,1.1)
    s.text('EXTERNAL RS-485',270,20,1.8)
    u=sym(s,'ST3485EBDR:ST3485EBDR','U',324,65,'B1-B021',show=((335,36),(335,39),''))
    for p,n in {1:'GW_RS485_RX',2:'GW_RS485_RE_N',3:'GW_RS485_DE',4:'GW_RS485_TX',6:'RS485_A',7:'RS485_B',8:'3V3_SYS',5:'GND'}.items():s.net(u,p,n,7.62,True)
    for i,(n,down) in enumerate([('GW_RS485_DE',True),('GW_RS485_RE_N',False),('GW_RS485_TX',False),('GW_RS485_RX',False)]):pull(s,282+32*i,110,'B1-B023',n,down)
    cap(s,380,65,'B1-B036','100n')
    passive(s,'R',286,169,'B1-B071','330R','3V3_SYS','RS485_A')
    passive(s,'R',321,169,'B1-B068','120R','RS485_A','RS485_B')
    passive(s,'R',356,169,'B1-B071','330R','RS485_B','GND')
    s.text('DE low / RE_N high: reset shutdown.\nFixed local termination; remote end also needs 120R.\nBoth wires within +/-5.5 V of board GND (ADR-038).',272,198,1.1)
    s.text('Manual bench: disable / disconnect the RS-485 peer\nbefore USB power-off or suspend; bias can feed SYS.\nNo automatic isolation or bias switch fitted.',272,214,1.1)
    s.text('Terminal block and TVS are on the test-access sheet.',272,238,1.1)
    s.save()

def access(page):
    s=Sheet('access','External terminal block, protection and test access',page)
    s.text('EXTERNAL BUS TERMINALS',20,20,1.8)
    u=sym(s,'Connector_Generic:Conn_01x08','J',85,70,'B1-B022',fp='Board1:PhoenixContact_PTSA_0.5_8-2.5-F_1989803',val='1989803 / bus terminals',show=((85,43),(85,46),''))
    for p,n in enumerate(['FD_CAN_A_H','FD_CAN_A_L','GND','FD_CAN_B_H','FD_CAN_B_L','RS485_A','RS485_B','GND'],1):s.net(u,p,n,15.24,True)
    for i,(bid,lid,a,b) in enumerate([('B1-B072','ESD2CAN24DBZRQ1:ESD2CAN24DBZRQ1','FD_CAN_A_H','FD_CAN_A_L'),('B1-B072','ESD2CAN24DBZRQ1:ESD2CAN24DBZRQ1','FD_CAN_B_H','FD_CAN_B_L'),('B1-B073','ESDS452DBZR:ESDS452DBZR','RS485_A','RS485_B')]):
        x=177+90*i;r=sym(s,lid,'D',x,70,bid,show=((x,43),(x,46),''))
        for p,n in {1:a,2:b,3:'GND'}.items():s.net(r,p,n,7.62,True)
    s.text('TVS channels stay connected when CAN termination shunts are removed. Place all three arrays at terminal entry.',20,112,1.2)
    s.text('FITTED SCOPE GROUND POSTS',20,134,1.6)
    for i,place in enumerate(['GW','SAM0','SAM1','SAM2','POWER','BUS']):
        x=45+63*i;j=sym(s,'Connector_Generic:Conn_01x02','J',x,161,'B1-B075',fp='Connector_PinHeader_2.54mm:PinHeader_1x02_P2.54mm_Vertical',val=place+' GND',show=((x,145),(x,148),''))
        supplies(s,j,[1,2],'GND')
    s.text('Six dedicated 1x2 headers, both contacts grounded. Place near the named circuit with room for a scope clip.',20,181,1.15)
    s.text('PCB TEST PADS (NO PURCHASED PART)',20,200,1.6)
    nets=['VBUS_RAW','USB_5V','FTDI_3V3','3V3_SYS','GW_RESET_N','GW_BOOT0','SAM0_RESET_N','SAM0_VDDCORE','SAM1_RESET_N','SAM1_VDDCORE','SAM2_RESET_N','SAM2_VDDCORE','UART_MD','RS485_A','RS485_B','FD_CAN_A_H','FD_CAN_A_L','FD_CAN_B_H','FD_CAN_B_L']
    for i,n in enumerate(nets):
        x=30+(i%10)*36;y=214+(i//10)*27
        r=sym(s,'Connector:TestPoint','TP',x,y,'B1-B011',fp='TestPoint:TestPoint_Pad_D2.0mm',val=n,show=((x,y-6),(x,y-3),''),fields={'MPN':'NA','Manufacturer':'NA'})
        pt=s.pt(r,1);end=(x+2.54,y+9);s.wire(pt,(x,y+9),end);s.label(n,end,0,True);s.mark(r,[1],n)
    s.save()

def relocate_existing():
    # Only change hierarchy/metadata of the captured power and USB circuitry.
    p=OUT/'power.kicad_sch'
    if not p.exists():p.write_bytes((OUT/'board1.kicad_sch').read_bytes())
    for name in ['power','usb_bridge']:
        p=OUT/(name+'.kicad_sch');tree=c.parse(p.read_text())
        tree=[x for x in tree if not(isinstance(x,list) and x[0] in ['sheet','sheet_instances'])]
        def visit(x):
            if not isinstance(x,list):return
            if x and x[0]=='path' and len(x)>2 and isinstance(x[1],str):x[1]='/'+NEWROOT+'/'+c.uid(name+'-sheet')
            if x and x[0]=='comment' and x[1]=='1':x[2]='Rev A complete schematic draft - no PCB layout'
            if x and x[0]=='text':x[1]=x[1].replace('These four GW nets end at the next capture stage.','These four GW nets connect to the gateway MCU sheet.')
            for y in x:visit(y)
        visit(tree)
        # Old root's child-sheet note/partial-scope text no longer belongs here.
        tree=[x for x in tree if not(isinstance(x,list) and x[0]=='text' and ('Cross-sheet connections' in x[1] or 'Power/USB capture ends' in x[1]))]
        if name=='power':
            for x in c.items(tree,'label'):
                if x[1]=='VBUS_RAW':
                    x[0]=A('global_label');x.insert(2,[A('shape'),A('input')])
            for x in c.items(tree,'global_label'):
                if x[1]=='VBUS_RAW':
                    angle=int(c.item(x,'at')[3])
                    x[:]=[v for v in x if not(isinstance(v,list) and v[0]=='effects')]
                    x.append(c.parse(c.effects(1.0,'left' if angle in (0,90) else 'right')))
        p.write_text(c.dump(tree)+'\n')
    original=json.loads((OUT/'capture_manifest.json').read_text())
    for r,v in original.items():
        if v['sheet']=='board1':v['sheet']='power'
    c.manifest.update(original)

def overview():
    s=Sheet('board1','Rev A system overview',1);s.id=NEWROOT
    s.text('WIRESPACES  /  BOARD 1 REV A',22,22,2.5)
    s.text('Four MCU bench prototype: two shared CAN-FD buses, multidrop UART and SAM ring.\nActive PC USB power, 500 mA configured budget. Independent FTDI controls the main 3.3 V rail.',22,36,1.5)
    for i,(name,title) in enumerate(PAGES):
        x=25+(i%3)*128;y=63+(i//3)*43
        s.add(f'(sheet (at {x} {y}) (size 112 27) (stroke (width 0) (type solid)) (fill (color 0 0 0 0)) (uuid {c.uid(name+"-sheet")}) (property "Sheetname" {c.q(title)} (at {x} {y-1} 0) {c.effects(1.27,"left bottom")}) (property "Sheetfile" {c.q(name+".kicad_sch")} (at {x} {y+28} 0) {c.effects(1.0,"left top")}) (instances (project "board1" (path "/{NEWROOT}" (page "{i+2}")))))')
        s.text(f'{i+2:02d}  '+title,x+5,y+9,1.4)
    s.text('CAN A/B: GW + SAM0 + SAM1 + SAM2, eight PHYs.\nUART_MD: four receivers; one LV125 channel per transmitter.\nSAM ring: SAM0 -> SAM1 -> SAM2 -> SAM0.\nEach MCU: SWD, private debug UART, SYNC/TRIG and EVENT0/1.',155,201,1.35)
    s.text('Named global nets join sheets; local analog nets stay within their sheet.\nReview PDF and checks describe draft-capture evidence. ERC, layout/DRC\nand hardware bring-up are separate stages. No PCB layout yet.',25,256,1.2)
    s.save()
    project=json.loads((OUT/'board1.kicad_pro').read_text());project['sheets']=[[NEWROOT,'System overview']]+[[c.uid(n+'-sheet'),t] for n,t in PAGES]
    project['text_variables']['CAPTURE_SCOPE']='Complete Rev A schematic draft'
    (OUT/'board1.kicad_pro').write_text(json.dumps(project,indent=2)+'\n')

def main():
    relocate_existing()
    plan=json.loads((ROOT/'boards/board1/mcu_capture_plan.json').read_text())
    for i,n in enumerate(NODES):mcu(n,plan['nodes'][n],i+4)
    can('A',8);can('B',9);interfaces(10);access(11);overview()
    m={r:v for r,v in c.manifest.items() if not r.startswith('#')}
    (OUT/'complete_manifest.json').write_text(json.dumps(m,indent=2)+'\n')
    print(f'Captured complete Board1: {len(m)} physical symbols, 11 sheets.')

if __name__=='__main__':main()
