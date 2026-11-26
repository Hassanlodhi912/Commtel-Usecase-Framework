import sys,os
sys.path.insert(0,sys.argv[1])
from PIL import Image,ImageDraw,ImageChops
A=sys.argv[2];B=sys.argv[3]  # input and output screenshot folders;os.makedirs(B,exist_ok=True)
Y=(255,230,0)
def mark(n,boxes,fill=True):
    i=Image.open(A+n+'.png').convert('RGB')
    if fill:
        l=Image.new('RGB',i.size,'white');d=ImageDraw.Draw(l)
        for b in boxes:d.rectangle(b,fill=Y)
        i=ImageChops.multiply(i,l)
    d=ImageDraw.Draw(i)
    for b in boxes:
        if not fill:d.rectangle(b,outline=Y,width=2)
    i.save(B+n+'.png');return i
R={'f1':([(0,y-8,415,y+7) for y in (63,77,105,133,161,175)],False),
'f2':([(420,373,472,389),(420,448,497,464),(330,598,354,614)],True),
'f3':([(44,5,245,24),(864,301,939,317),(647,336,692,352),(852,366,986,382),(841,396,908,412)],True),
'f4':([(44,6,302,25),(398,310,552,350),(398,418,552,462),(398,526,552,555),(398,633,552,672)],True),
'f5':([(50,6,422,24),(736,65,778,81),(225,303,656,319),(225,422,662,438),(225,572,662,588)],True)}
im=[mark(k,*v) for k,v in R.items()]
W=max(x.width for x in im);H=sum(x.height for x in im)
m=Image.new('RGB',(W,H),'white');y=0
for x in im:m.paste(x,(0,y));y+=x.height
m.save(sys.argv[2]);print(m.size)
