"""Exploratory unprotected cable/RC sweep; not a model of the complete Rev A input.

No TVS, switch, loads, contact bounce or layout parasitics are represented.
Run --check to reproduce the retained numerical snapshot; --output PATH to export.
"""
import argparse
from pathlib import Path
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--check', action='store_true')
parser.add_argument('--output', type=Path)
args = parser.parse_args()
import json,math
results=[]
for L in [0.2e-6,1e-6,5e-6]:
 for R in [0.05,0.25,1.0]:
  for C in [1e-6,2e-6,2.53e-6]:
   for Cd in [2.35e-6,4.7e-6,5.9455e-6]:
    h=2e-8; y=[0.,0.,0.]; peak=0.; lastbad=0.
    def f(y):
     i,v,d=y; j=(v-d)
     return [(5.5-R*i-v)/L,(i-j)/C,j/Cd]
    for n in range(15000):
     a=f(y); b=f([y[k]+h*a[k]/2 for k in range(3)]); c=f([y[k]+h*b[k]/2 for k in range(3)]); d=f([y[k]+h*c[k] for k in range(3)])
     y=[y[k]+h*(a[k]+2*b[k]+2*c[k]+d[k])/6 for k in range(3)]
     peak=max(peak,y[1])
     if abs(y[1]-5.5)>.055:lastbad=n*h
    results.append(dict(L_uH=L*1e6,R_ohm=R,C_uF=C*1e6,Cd_uF=Cd*1e6,peak_V=peak,last_outside_1pct_us=lastbad*1e6))
summary={'model':'Ideal 5.5 V step, series cable L/R, direct C, series 1 ohm + Cd shunt; no TVS, switch, loads, contact bounce or layout parasitics. Exploration only.','cases':len(results),'worst_peak':max(results,key=lambda x:x['peak_V']),'worst_settle':max(results,key=lambda x:x['last_outside_1pct_us']),'results':results}
if args.check:
    expected = json.loads(Path(__file__).with_suffix('.json').read_text())
    assert summary == expected, 'Exploratory sweep differs from retained snapshot'
    print('PASS: all 81 exploratory hotplug cases reproduced; not hardware qualification.')
if args.output:
    args.output.write_text(json.dumps(summary, indent=2) + '\n')
print(json.dumps({k:v for k,v in summary.items() if k!='results'},indent=2))
