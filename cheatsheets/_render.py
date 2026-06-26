# Render the three cheatsheets to high-res PNG (for Mural) using PIL.
from PIL import Image, ImageDraw, ImageFont

S = 2  # supersample for crispness
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONTB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
_cache = {}
def F(sz, bold=False):
    key = (round(sz * S), bold)
    if key not in _cache:
        _cache[key] = ImageFont.truetype(FONTB if bold else FONT, key[0])
    return _cache[key]

def R(d, x, y, w, h, fill=None, outline=None, width=1, radius=0):
    box = [x*S, y*S, (x+w)*S, (y+h)*S]
    if radius:
        d.rounded_rectangle(box, radius=radius*S, fill=fill, outline=outline, width=width)
    else:
        d.rectangle(box, fill=fill, outline=outline, width=width)
def T(d, x, y, s, size=9, fill="#000", bold=False, anchor="ls"):
    d.text((x*S, y*S), s, font=F(size, bold), fill=fill, anchor=anchor)
def C(d, cx, cy, r, fill=None, outline=None, width=1):
    d.ellipse([(cx-r)*S, (cy-r)*S, (cx+r)*S, (cy+r)*S], fill=fill, outline=outline, width=width)
def L(d, x1, y1, x2, y2, fill="#000", width=1):
    d.line([x1*S, y1*S, x2*S, y2*S], fill=fill, width=width)
def TRI(d, cx, cy, color="#888", s=4):
    d.polygon([((cx-s)*S, (cy-s/2)*S), ((cx+s)*S, (cy-s/2)*S), (cx*S, (cy+s/2)*S)], fill=color)
def PIN(d, cx, cy, num, color, r=11, size=11):
    C(d, cx, cy, r, fill=color)
    T(d, cx, cy, str(num), size=size, fill="#fff", bold=True, anchor="mm")

def new():
    img = Image.new("RGB", (1140*S, 720*S), "#ffffff")
    return img, ImageDraw.Draw(img)

GREEN="#2e844a"; AMBER="#9a6a00"; RED="#ba0517"; INK="#0b0c0c"; GREY="#5c5c5c"

def legend_header(d):
    T(d, 660, 86, "What you can change", 13, INK, bold=True)
    C(d, 666, 104, 6, fill=GREEN); T(d, 678, 108, "Configurable", 10, "#444")
    C(d, 788, 104, 6, fill=AMBER); T(d, 800, 108, "Partial", 10, "#444")
    C(d, 880, 104, 6, fill=RED);   T(d, 892, 108, "Needs code", 10, "#444")

def legend_item(d, cy, color, num, label, desc):
    PIN(d, 668, cy, num, color, r=10, size=10)
    T(d, 688, cy-3, label, 11.5, INK, bold=True)
    T(d, 688, cy+12, desc, 11.5, GREY)

def notebox(d, x, y, w, h, title, lines):
    R(d, x, y, w, h, fill="#fef6f6", outline="#f3c4c4", width=1, radius=6)
    T(d, x+16, y+22, title, 11.5, RED, bold=True)
    yy = y+40
    for ln in lines:
        T(d, x+16, yy, ln, 11, GREY); yy += 16

# ---------------- nav helper ----------------
def green_nav(d, tabs=True):
    R(d, 24, 110, 600, 30, fill="#008938")
    T(d, 40, 129, "Bovine TB", 12, "#fff", bold=True)
    for i,(bx,by) in enumerate([(132,120),(137,120),(142,120),(132,125),(137,125),(142,125),(132,130),(137,130),(142,130)]):
        R(d, bx, by, 3, 3, fill="#fff")
    T(d, 170, 129, "Cattle", 10, "#fff", bold=True); R(d,168,137,40,2,fill="#fff")
    T(d, 224, 129, "Vaccinations", 10, "#d6f0e6"); T(d,300,129,"Reports",10,"#d6f0e6")
    T(d, 352, 129, "Styleguide", 10, "#d6f0e6"); T(d,416,129,"Configurable",10,"#d6f0e6")

# ============================================================ CATTLE LIST
def cattle():
    img, d = new()
    T(d,24,34,"Cheatsheet — Cattle List View",20,INK,bold=True)
    T(d,24,54,"What a designer can change with standard Salesforce config (no code).",12,GREY)
    R(d,24,70,600,624,fill="#f3f4f4",outline="#c9c9c9",width=1,radius=6)
    R(d,24,70,600,40,fill="#fff",outline="#e3e3e3",width=1,radius=6)
    R(d,40,80,4,20,fill="#008938")
    T(d,50,86,"Animal &",7,INK,bold=True); T(d,50,94,"Plant Health",7,INK,bold=True); T(d,50,102,"Agency",7,INK,bold=True)
    R(d,210,80,230,20,fill="#f3f3f3",outline="#d8d8d8",width=1,radius=10)
    C(d,224,90,4,outline="#9a9a9a",width=1); T(d,236,93,"Search Bovine TB and more…",9,"#9a9a9a")
    C(d,600,90,9,fill="#c9c9c9")
    green_nav(d)
    R(d,40,156,568,522,fill="#fff",outline="#ddd",width=1,radius=4)
    R(d,52,168,26,26,fill="#008938",radius=4)
    T(d,88,180,"Cattle",13,INK,bold=True); T(d,88,192,"All Cattle • List View • 5 items",8,GREY)
    R(d,430,168,116,22,fill="#008938",radius=4); T(d,488,183,"Log a Vaccination",9,"#fff",bold=True,anchor="ms")
    R(d,552,168,44,22,fill="#fff",outline="#b9b9b9",width=1,radius=4); T(d,574,183,"New",9,INK,anchor="ms")
    R(d,52,206,230,22,fill="#fff",outline="#c9c9c9",width=1,radius=4); C(d,66,217,4,outline="#9a9a9a",width=1); T(d,78,220,"Search by ear tag…",9,"#9a9a9a")
    R(d,52,244,544,22,fill="#fafafa",outline="#ececec",width=1)
    R(d,60,251,9,9,fill="#fff",outline="#b9b9b9",width=1,radius=2)
    for tx,lbl in [(80,"EAR TAG NUMBER"),(220,"TB VAX"),(300,"DOB"),(380,"SEX"),(450,"BREED")]:
        T(d,tx,258,lbl,8.5,"#444",bold=True)
    TRI(d,568,255,"#888")
    L(d,52,266,596,266,"#ececec")
    rows=[(282,"UK58291000125","Vaccinated","14 Mar 2021","Female","HER"),
          (305,"UK58291000126","Due Soon","02 Jun 2022","Female","BALX"),
          (328,"UK58291000129","Overdue","30 Jul 2021","Female","LIMX")]
    R(d,52,290,544,22,fill="#f8f8f8")
    for (ry,tag,st,dob,sx,br) in rows:
        T(d,80,ry,tag,9,INK); T(d,220,ry,st,9,INK); T(d,300,ry,dob,9,INK); T(d,380,ry,sx,9,INK); T(d,450,ry,br,9,INK); TRI(d,568,ry-3,"#888")
    for (cx,cy,n,c) in [(44,74,1,GREEN),(206,80,2,RED),(40,124,3,GREEN),(52,162,4,AMBER),(430,160,5,AMBER),(52,206,6,GREEN),(120,244,7,GREEN),(220,276,8,RED),(596,276,9,GREEN)]:
        PIN(d,cx,cy,n,c)
    legend_header(d)
    items=[(138,GREEN,1,"Logo","Setup → Themes and Branding → Logo image."),
           (178,RED,2,"Global search","Always present — position & style are fixed; can’t move it."),
           (218,GREEN,3,"Brand colour + app name & tabs","Themes & Branding (colour) · App Manager (name, nav items)."),
           (258,AMBER,4,"List title + object icon","Rename object label · icon from standard set (Tab Style)."),
           (298,AMBER,5,"Page buttons (actions)","Create Actions/Buttons (Object Manager). Colour is automatic."),
           (338,GREEN,6,"Search this list","Standard list-view search — appears automatically."),
           (378,GREEN,7,"Columns, sort & filter","List View Controls → Select Fields to Display / Filters."),
           (418,RED,8,"Status value","Plain text (picklist/formula). Coloured badge needs code."),
           (458,GREEN,9,"Row action menu","Configure list-view row actions (View, Edit, custom).")]
    for it in items: legend_item(d,*it)
    notebox(d,660,500,452,86,"Can’t change without code",
            ["• Reposition elements freely / custom grid or column widths",
             "• Move or restyle the global search",
             "• Coloured status badges, custom fonts, link colours"])
    return img

# ============================================================ COW RECORD
def cow():
    img, d = new()
    T(d,24,34,"Cheatsheet — Cattle Record Page",20,INK,bold=True)
    T(d,24,54,"What a designer can change with standard Salesforce config (no code).",12,GREY)
    R(d,24,70,600,624,fill="#f3f4f4",outline="#c9c9c9",width=1,radius=6)
    R(d,24,70,600,28,fill="#008938")
    T(d,40,88,"Bovine TB",11,"#fff",bold=True); T(d,150,88,"Cattle",9,"#fff",bold=True); T(d,210,88,"Vaccinations",9,"#d6f0e6"); T(d,290,88,"Reports",9,"#d6f0e6")
    R(d,40,110,120,20,fill="#fff",outline="#b9b9b9",width=1,radius=4); T(d,100,124,"← Back to Cattle",9,INK,anchor="ms")
    R(d,40,142,568,96,fill="#fff",outline="#ddd",width=1,radius=4)
    R(d,54,154,30,30,fill="#008938",radius=4)
    T(d,96,166,"Cattle",8,GREY); T(d,96,182,"UK58291000125",14,INK,bold=True)
    R(d,430,156,74,22,fill="#fff",outline="#b9b9b9",width=1,radius=4); T(d,467,171,"Edit",9,INK,anchor="ms")
    R(d,508,156,92,22,fill="#008938",radius=4); T(d,554,171,"Log a Vaccination",8.5,"#fff",bold=True,anchor="ms")
    L(d,54,200,594,200,"#eee")
    for tx,lbl in [(60,"EAR TAG NUMBER"),(200,"TB VAX"),(320,"BREED"),(440,"LAST VACCINATED")]:
        T(d,tx,214,lbl,8,GREY)
    for tx,val in [(60,"UK58291000125"),(200,"Vaccinated"),(320,"HER"),(440,"02 Apr 2026")]:
        T(d,tx,228,val,9.5,INK)
    T(d,54,262,"Details",10,INK,bold=True); R(d,50,268,46,2,fill="#008938"); T(d,120,262,"Vaccination History",10,GREY)
    for tx,lbl in [(56,"EAR TAG NUMBER"),(330,"DATE OF BIRTH")]: T(d,tx,292,lbl,8,GREY)
    for tx,lbl in [(56,"BREED"),(330,"SEX")]: T(d,tx,330,lbl,8,GREY)
    for tx,val in [(56,"UK58291000125"),(330,"14 Mar 2021")]: T(d,tx,305,val,9.5,INK)
    for tx,val in [(56,"HER"),(330,"Female")]: T(d,tx,343,val,9.5,INK)
    for (a,b) in [(56,290),(330,560)]: pass
    L(d,56,315,290,315,"#eee"); L(d,330,315,560,315,"#eee"); L(d,56,353,290,353,"#eee"); L(d,330,353,560,353,"#eee")
    R(d,40,372,568,300,fill="#fff",outline="#ddd",width=1,radius=4)
    R(d,54,384,22,22,fill="#9050e9",radius=4); T(d,86,399,"Vaccinations (3)",11,INK,bold=True)
    R(d,556,384,40,20,fill="#fff",outline="#b9b9b9",width=1,radius=4); T(d,576,398,"New",8.5,INK,anchor="ms")
    R(d,54,416,540,20,fill="#fafafa",outline="#ececec",width=1)
    for tx,lbl in [(62,"DATE"),(146,"VACCINATED BY"),(266,"VACCINE BATCH"),(372,"VAC EXPIRY"),(446,"DILUENT BATCH"),(540,"DIL EXP")]:
        T(d,tx,429,lbl,7.5,"#444",bold=True)
    rel=[(450,"02 Apr 26","A. Patel MRCVS","125007G","05 2029","37925B","05 29"),
         (470,"10 Oct 25","A. Patel MRCVS","118842F","11 2028","33010A","11 28")]
    for (ry,dt,by,vb,ve,db,de) in rel:
        T(d,62,ry,dt,8,INK); T(d,146,ry,by,8,INK); T(d,266,ry,vb,8,INK); T(d,372,ry,ve,8,INK); T(d,446,ry,db,8,INK); T(d,540,ry,de,8,INK)
    for (cx,cy,n,c) in [(100,110,1,GREEN),(54,150,2,GREEN),(508,148,3,AMBER),(200,208,4,RED),(54,256,5,GREEN),(160,300,6,GREEN),(54,378,7,GREEN),(300,416,8,GREEN)]:
        PIN(d,cx,cy,n,c)
    legend_header(d)
    items=[(138,GREEN,1,"Back / navigation","Standard record navigation — appears automatically."),
           (178,GREEN,2,"Highlights panel (header fields)","Setup → Object Manager → Compact Layout (key fields)."),
           (218,AMBER,3,"Action buttons (Edit, Log a Vaccination)","Create Actions (Object Manager) + order. Colour auto."),
           (258,RED,4,"Status value","Plain text (picklist/formula). Coloured badge needs code."),
           (298,GREEN,5,"Tabs","Lightning App Builder → Tabs component (add/name/order)."),
           (338,GREEN,6,"Detail fields & layout","Dynamic Forms — fields, sections, columns, visibility."),
           (378,GREEN,7,"Related list (Vaccinations)","Page Layout → Related Lists; columns & New action."),
           (418,GREEN,8,"Related list columns","Choose & order the fields shown in the table.")]
    for it in items: legend_item(d,*it)
    notebox(d,660,470,452,104,"Can’t change without code",
            ["• Coloured status badges / conditional cell colouring",
             "• Custom button colours, fonts, link colours",
             "• Free-form placement outside the standard regions",
             "• Editable inline grids for creating many child records"])
    return img

# ============================================================ FLOW
def flow():
    img, d = new()
    T(d,24,34,"Cheatsheet — Log a Vaccination (Screen Flow)",20,INK,bold=True)
    T(d,24,54,"What a designer can change with standard Salesforce config (no code).",12,GREY)
    R(d,24,70,600,624,fill="#f3f4f4",outline="#c9c9c9",width=1,radius=6)
    R(d,24,70,600,28,fill="#008938"); T(d,40,88,"Bovine TB",11,"#fff",bold=True)
    R(d,140,118,368,552,fill="#fff",outline="#cfcfcf",width=1,radius=6)
    R(d,140,118,368,48,fill="#f3f3f3",radius=6)
    R(d,156,130,22,22,fill="#9050e9",radius=4)
    T(d,188,140,"Log a Vaccination",12,INK,bold=True); T(d,188,154,"Step 1 of 2 · Vaccination details",8.5,GREY)
    C(d,300,184,5,fill="#008938"); L(d,305,184,345,184,"#d8d8d8",2); C(d,350,184,5,fill="#fff",outline="#b9b9b9",width=1)
    R(d,156,200,336,30,fill="#f3f3f3",outline="#e3e3e3",width=1,radius=4); T(d,166,213,"ANIMAL",7.5,GREY); T(d,166,225,"UK58291000125 · HER · Female",9.5,INK)
    T(d,156,252,"* Who vaccinated the cattle?",9,INK); R(d,156,258,336,22,fill="#fff",outline="#b9b9b9",width=1,radius=4); T(d,166,273,"I did (Dave)",9,INK); TRI(d,482,270,"#888")
    T(d,156,300,"* Date of vaccination",9,INK); R(d,156,306,150,22,fill="#fff",outline="#b9b9b9",width=1,radius=4); T(d,166,321,"12/06/2026",9,INK); R(d,286,311,12,11,outline="#9a9a9a",width=1); L(d,286,315,298,315,"#9a9a9a")
    T(d,156,350,"VACCINE BATCH DETAILS",8.5,GREY,bold=True); L(d,156,356,492,356,"#e3e3e3")
    T(d,156,374,"* Vaccine batch number",9,INK); R(d,156,380,200,22,fill="#fff",outline="#b9b9b9",width=1,radius=4); T(d,166,395,"For example, 125007G",9,"#9a9a9a")
    T(d,156,422,"* Vaccine expiry date",9,INK)
    R(d,156,428,96,22,fill="#fff",outline="#b9b9b9",width=1,radius=4); T(d,166,443,"Month",9,INK); TRI(d,238,440,"#888")
    R(d,258,428,96,22,fill="#fff",outline="#b9b9b9",width=1,radius=4); T(d,268,443,"Year",9,INK); TRI(d,340,440,"#888")
    T(d,156,464,"For example, 05 2029",8,"#9a9a9a")
    T(d,156,488,"DILUENT BATCH DETAILS",8.5,GREY,bold=True); L(d,156,494,492,494,"#e3e3e3")
    T(d,156,512,"* Diluent batch number",9,INK); R(d,156,518,200,22,fill="#fff",outline="#b9b9b9",width=1,radius=4); T(d,166,533,"For example, 37925B",9,"#9a9a9a")
    T(d,156,560,"* Diluent expiry date",9,INK)
    R(d,156,566,96,22,fill="#fff",outline="#b9b9b9",width=1,radius=4); T(d,166,581,"Month",9,INK); TRI(d,238,578,"#888")
    R(d,258,566,96,22,fill="#fff",outline="#b9b9b9",width=1,radius=4); T(d,268,581,"Year",9,INK); TRI(d,340,578,"#888")
    L(d,140,624,508,624,"#e3e3e3")
    R(d,156,636,60,22,fill="#fff",outline="#b9b9b9",width=1,radius=4); T(d,186,651,"Cancel",9,INK,anchor="ms")
    R(d,380,636,56,22,fill="#fff",outline="#b9b9b9",width=1,radius=4); T(d,408,651,"Previous",9,INK,anchor="ms")
    R(d,442,636,50,22,fill="#008938",radius=4); T(d,467,651,"Next",9,"#fff",bold=True,anchor="ms")
    for (cx,cy,n,c) in [(140,118,1,GREEN),(188,128,2,GREEN),(325,184,3,AMBER),(156,200,4,GREEN),(500,269,5,GREEN),(324,434,6,AMBER),(156,344,7,GREEN),(467,636,8,GREEN)]:
        PIN(d,cx,cy,n,c)
    legend_header(d)
    items=[(138,GREEN,1,"The whole flow","Build it in Flow Builder (Screen Flow) — entirely no-code."),
           (178,GREEN,2,"Flow / screen title","Set the screen label and headings in Flow Builder."),
           (218,AMBER,3,"Progress indicator","Optional — toggle “show progress” / add stages."),
           (258,GREEN,4,"Read-only context","Display the launched record’s fields (Display Text)."),
           (298,GREEN,5,"Fields, labels, required, help text","Add components; mark required; set “For example…” help."),
           (338,AMBER,6,"Date & picklist inputs","Rendered by field type. No month-only picker → two picklists."),
           (378,GREEN,7,"Section headings / grouping","Section components group fields on the screen."),
           (418,GREEN,8,"Navigation footer","Previous / Next / Finish are standard and automatic.")]
    for it in items: legend_item(d,*it)
    notebox(d,660,468,452,120,"Can’t change without code",
            ["• Three-box Day/Month/Year date entry (GOV.UK style)",
             "• A true month-only or custom date control",
             "• Toggle switches (checkbox fields render as checkboxes)",
             "• Custom field layout, colours, or fonts on the screen",
             "• Inline-editable grid to log many animals at once"])
    return img

for name, fn in [("cheatsheet-cattle-list", cattle), ("cheatsheet-cow-record", cow), ("cheatsheet-log-vaccination", flow)]:
    im = fn()
    im.save(name + ".png", optimize=True)
    print(name + ".png", im.size)
