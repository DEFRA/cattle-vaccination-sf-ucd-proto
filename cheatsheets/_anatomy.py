# Re-make of the "anatomy of a page" segmented diagram, with the why for each.
from PIL import Image, ImageDraw, ImageFont

S = 2
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONTB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
_c = {}
def F(sz, b=False):
    k = (round(sz*S), b)
    if k not in _c: _c[k] = ImageFont.truetype(FONTB if b else FONT, k[0])
    return _c[k]
def R(d,x,y,w,h,fill=None,outline=None,width=1,radius=0):
    box=[x*S,y*S,(x+w)*S,(y+h)*S]
    (d.rounded_rectangle(box,radius=radius*S,fill=fill,outline=outline,width=width) if radius
     else d.rectangle(box,fill=fill,outline=outline,width=width))
def T(d,x,y,s,size=9,fill="#000",b=False,anchor="ls"):
    d.text((x*S,y*S),s,font=F(size,b),fill=fill,anchor=anchor)
def C(d,cx,cy,r,fill=None,outline=None,width=1):
    d.ellipse([(cx-r)*S,(cy-r)*S,(cx+r)*S,(cy+r)*S],fill=fill,outline=outline,width=width)
def L(d,x1,y1,x2,y2,fill="#000",width=1):
    d.line([x1*S,y1*S,x2*S,y2*S],fill=fill,width=width)
def wrap(text,size,maxw,b=False):
    f=F(size,b); out=[]; cur=""
    for w in text.split():
        t=(cur+" "+w).strip()
        if f.getlength(t)<=maxw*S: cur=t
        else: out.append(cur); cur=w
    if cur: out.append(cur)
    return out

INK="#0b0c0c"; GREY="#5c5c5c"; BLUE="#1b96ff"; PURP="#7a52d6"
AMBER="#fde7b4"; AMBBORD="#eccf7e"; CARD="#ffffff"; CBORD="#dddddd"

W,H = 1420, 980
img = Image.new("RGB",(W*S,H*S),"#ffffff"); d=ImageDraw.Draw(img)

T(d,40,46,"Anatomy of a page — the building blocks & why",22,INK,b=True)
T(d,40,70,"Every Salesforce page is assembled from these standard segments, stacked top to bottom.",13,GREY)

def seg(y,h,num,name,why):
    R(d,40,y,1340,h,fill=AMBER,outline=AMBBORD,width=1,radius=10)
    C(d,74,y+26,13,fill="#fff",outline=AMBBORD,width=1); T(d,74,y+26,str(num),12,"#7a5b00",b=True,anchor="mm")
    T(d,98,y+22,name,14,INK,b=True)
    yy=y+42
    for ln in wrap("Why: "+why,11.5,600): T(d,98,yy,ln,11.5,"#6b5a2a"); yy+=16
    return (770, y+16, 594, h-32)   # inner example area

def inner(area):
    x,y,w,h=area; R(d,x,y,w,h,fill=CARD,outline=CBORD,width=1,radius=6); return x,y,w,h

# ---------- Segment 1: App bar ----------
a=seg(96,120,1,"App bar — service name, selector & open record tabs",
      "Switch between services and keep several records open at once, each as a closable tab (Console navigation).")
x,y,w,h=inner(a)
# waffle
for i,(dx,dy) in enumerate([(0,0),(5,0),(10,0),(0,5),(5,5),(10,5),(0,10),(5,10),(10,10)]):
    R(d,x+14+dx,y+18+dy,3,3,fill="#a0a0a0")
T(d,x+36,y+30,"APHA Services",11,INK,b=True)
T(d,x+150,y+30,"License applications",10,GREY); TRI=lambda dd,cx,cy,col:dd.polygon([((cx-3)*S,(cy-2)*S),((cx+3)*S,(cy-2)*S),(cx*S,(cy+2)*S)],fill=col)
TRI(d,x+268,y+27,"#9a9a9a")
R(d,x+290,y+14,200,h-20,fill="#eef6ff",outline="#cfe4fb",width=1,radius=4)
T(d,x+302,y+30,"Application 2UWNW21T",10,BLUE,b=True); T(d,x+470,y+30,"x",10,BLUE)
R(d,x+290,y+h-8,200,3,fill=BLUE)

# ---------- Segment 2: Page header ----------
a=seg(228,128,2,"Page header — title & key-info breakdown",
      "Confirms which record you are on and surfaces its most important fields at a glance (Highlights panel / Compact Layout).")
x,y,w,h=inner(a)
R(d,x+16,y+16,26,26,fill=PURP,radius=5)
T(d,x+52,y+24,"Case reference",8,GREY); T(d,x+52,y+40,"2UWNW21T",15,INK,b=True)
labels=["Requested","Origin name","Origin CPH","Destination CPH"]
vals=["8 May 2026","Charles Marsh","35/251/0018","15/277/0077"]
for i in range(4):
    cx=x+16+i*145
    T(d,cx,y+72,labels[i],8,GREY); T(d,cx,y+88,vals[i],9.5,INK)

# ---------- Segment 3: Status & actions ----------
a=seg(364,168,3,"Status & actions — filter (lists) or case status path (records)",
      "Shows where the case sits in its process and the single next action to take. On lists, filter tabs narrow the data (Path / List Views).")
x,y,w,h=inner(a)
# path chevrons
stg=[("Allocation","#06316b","#fff"),("Verification","#dfe3e8","#3e3e3c"),("Risk assessment","#eef0f2","#7a7a7a"),("Issuance","#eef0f2","#7a7a7a")]
px=x+14
for i,(lab,bg,fg) in enumerate(stg):
    R(d,px,y+14,118,22,fill=bg,radius=3); T(d,px+59,y+25,lab,8,fg,anchor="ms")
    px+=124
R(d,x+14,y+14,118,22,fill="#0b5394",radius=3); T(d,x+73,y+25,"Allocation",8,"#fff",anchor="ms");
R(d,x+w-150,y+13,134,24,fill=BLUE,radius=4); T(d,x+w-83,y+25,"Mark stage as Complete",7.5,"#fff",b=True,anchor="ms")
T(d,x+16,y+62,"Guidance for Verification",9,INK,b=True)
T(d,x+16,y+80,"•  Check the applicant's contact details match APHA records",8.5,GREY)
T(d,x+16,y+96,"•  Update the origin details to reflect the type of match",8.5,GREY)
R(d,x+w-150,y+58,134,22,fill="#fff",outline=BLUE,width=1,radius=4); T(d,x+w-83,y+69,"Verify applicant",8,BLUE,b=True,anchor="ms")

# ---------- Segment 4: Body (two options) ----------
T(d,40,572,"4   Body — choose the pattern that fits the job",14,INK,b=True)
# left option: tabular
R(d,40,592,650,330,fill=AMBER,outline=AMBBORD,width=1,radius=10)
T(d,64,618,"Tabular data with ordering",13,INK,b=True)
for ln,yy in zip(wrap("Why: scan, sort and triage many records — a work queue or list view.",11.5,560),[636,652]):
    T(d,64,yy,ln,11.5,"#6b5a2a")
bx,by,bw=64,680,602
R(d,bx,by,bw,224,fill=CARD,outline=CBORD,width=1,radius=6)
R(d,bx+10,by+10,bw-20,22,fill="#f3f3f3",outline="#e3e3e3",width=1)
for i,t in enumerate(["Reference","Status","Assigned to"]):
    T(d,bx+24+i*180,by+24,t,8,"#444");
pills=[("Receipt","#f3f3f3","#3e3e3c"),("Issued","#d7f5e3","#1c5a37"),("Risk assess","#fce5c4","#6b4a00"),("Rejected","#fcd9e2","#8a0b2e")]
for r in range(4):
    ry=by+44+r*42
    T(d,bx+24,ry+14,"E224CFE"+str(r),9,"#0b5cab")
    lab,bg,fg=pills[r]; R(d,bx+204,ry+4,70,18,fill=bg,radius=9); T(d,bx+239,ry+14,lab,7.5,fg,anchor="ms")
    T(d,bx+384,ry+14,["Ben Bond","S. Flint","J. Parkyn","Unassigned"][r],8.5,INK)
    L(d,bx+10,ry+30,bx+bw-10,ry+30,"#f0f0f0")

T(d,705,760,"or",13,GREY,b=True,anchor="mm")

# right option: tabbed + side panel
R(d,730,592,650,330,fill=AMBER,outline=AMBBORD,width=1,radius=10)
T(d,754,618,"Tabbed data & tasks  +  side panel",13,INK,b=True)
for ln,yy in zip(wrap("Why: group detailed fields into tabs; side panel for summary, next best action and knowledge — a record page.",11.5,560),[636,652]):
    T(d,754,yy,ln,11.5,"#6b5a2a")
# left: tabs + sections
R(d,754,680,392,224,fill=CARD,outline=CBORD,width=1,radius=6)
T(d,770,700,"Case details",9,BLUE,b=True); R(d,768,706,70,2,fill=BLUE)
T(d,856,700,"Movement",9,GREY); T(d,946,700,"Messages",9,GREY)
for i,(sec) in enumerate(["Receipting","Allocation","Validation"]):
    sy=716+i*56
    R(d,770,sy,360,18,fill="#f3f3f3",radius=3); T(d,778,sy+13,sec,8.5,"#3e3e3c")
    for c2 in range(2):
        fx=778+c2*180
        T(d,fx,sy+34,["Received by","Priority","FDA","Office","Origin"][ (i*2+c2)%5 ],7.5,GREY)
        L(d,fx,sy+42,fx+150,sy+42,"#e5e5e5")
# right: side panel cards
def panel(py,title):
    R(d,1156,py,208,h_,fill=CARD,outline=CBORD,width=1,radius=6)
    C(d,1172,py+16,7,fill=PURP); T(d,1186,py+20,title,9,INK,b=True)
h_=66; panel(680,"Next Best Action"); R(d,1172,712,176,18,fill="#fff",outline=BLUE,width=1,radius=4); T(d,1260,721,"Receipt and allocate",7.5,BLUE,b=True,anchor="ms")
h_=66; panel(752,"Case summary")
T(d,1172,786,"License type",8,GREY); R(d,1300,778,46,16,fill="#fff",outline="#c9c9c9",width=1,radius=3); T(d,1323,786,"TB15",7.5,"#444",anchor="ms")
h_=60; panel(824,"Knowledge"); T(d,1172,856,"Suggested articles",8,GREY); T(d,1172,872,"This is a policy title",8,"#0b5cab")

img.save("page-anatomy.png", optimize=True)
print("page-anatomy.png", img.size)
