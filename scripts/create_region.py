import cv2
import numpy as np
import sys

ima00 = np.zeros((360,386), dtype=np.uint8)
ima01 = np.ones((360,386), dtype=np.uint8) * 10
ima02 = np.zeros((360,386), dtype=np.uint8)
ima03 = np.zeros((360,386), dtype=np.uint8)
ima04 = np.zeros((360,386), dtype=np.uint8)
ima05 = np.zeros((360,386), dtype=np.uint8)
ima06 = np.zeros((360,386), dtype=np.uint8)
ima07 = np.zeros((360,386), dtype=np.uint8)
ima08 = np.zeros((360,386), dtype=np.uint8)
ima09 = np.zeros((360,386), dtype=np.uint8)
ima10 = np.zeros((360,386), dtype=np.uint8)
ima11 = np.zeros((360,386), dtype=np.uint8)
ima12 = np.zeros((360,386), dtype=np.uint8)
ima13 = np.zeros((360,386), dtype=np.uint8)
ima14 = np.zeros((360,386), dtype=np.uint8)


pol1  = np.array([[0,  272],[26, 272],[26, 360],[0,  360]])
pol2  = np.array([[360,272],[385,272],[385,360],[360,360]])
pol3  = np.array([[25, 320],[132,320],[132,360],[25, 360]])
pol4  = np.array([[253,320],[360,320],[360,360],[253,360]])
pol5  = np.array([[133,320],[193,320],[193,360],[133,360]])
pol6  = np.array([[194,320],[252,320],[252,360],[194,360]])
tri1  = np.array([[193,319],[385,150],[385,319]])
tri2  = np.array([[193,319],[0,  319],[0,  150]])
tri3  = np.array([[193,319],[345,100],[345,319]])
tri4  = np.array([[193,319],[40, 100],[40 ,319]])
trap1 = np.array([[0,  147],[193,147],[193,70],[126,70]])
trap2 = np.array([[194,147],[385,147],[260,100],[194,70]])
pol10 = np.array([[0,  0], [24, 0],[24, 271],[0,271]])
pol11 = np.array([[361,0], [385,0],[385,271],[361,271]])
poly5e = np.array([[132,260],[193,260],[193,360],[132,360]])
poly6e = np.array([[194,260],[253,260],[253,360],[194,360]])

half   = np.array([[194,0],[385,0],[385,360],[194,360]])

centre = (193,320)
radi1 = 60
radi2 = 173
#radi2 = 177
cv2.fillPoly(ima01,pts=[half],color=(50))
cv2.circle(ima05, centre, radi1, (10), -1)
cv2.fillPoly(ima06, pts =[pol5,pol6], color=(5))


#cv2.fillPoly(ima01, pts =[pol6], color=(3))
cv2.fillPoly(ima03, pts =[poly5e], color=(2))
cv2.fillPoly(ima04, pts =[poly6e], color=(3))

cv2.fillPoly(ima02, pts=[tri3,tri4], color=(4))
ima01 = ima01 + ima02 + ima03 + ima04 + ima05 + ima06

ima00[ima01==22] = 25
ima00[ima01==63] = 25
ima00[ima01==17] = 15
ima00[ima01==26] = 15
ima00[ima01==27] = 15
ima00[ima01==58] = 35
ima00[ima01==67] = 35
ima00[ima01==68] = 35


ima01[:,:] = 10
ima02[:,:] = 0
ima03[:,:] = 0
ima04[:,:] = 0
ima05[:,:] = 0
ima06[:,:] = 0

cv2.fillPoly(ima01,pts=[half],color=(50))
cv2.circle(ima02, centre, radi2, (1), -1)

pol3e  = np.array([[25, 147],[132,147],[132,360],[25, 360]])
pol4e  = np.array([[253,147],[360,147],[360,360],[253,360]])

cv2.fillPoly(ima03,pts=[pol3e,pol4e],color=((2)))
cv2.fillPoly(ima04,pts=[tri1,tri2],color=((3)))
cv2.fillPoly(ima04,pts=[pol3,pol4],color=((4)))
cv2.fillPoly(ima05,pts=[pol10,pol11],color=((5)))

ima01 = ima01 + ima02 + ima03 + ima04 + ima05


ima01[ima00 != 0] = ima00[ima00 != 0]

'''
print (ima01[345][100])
print (ima01[450][100])
print (ima01[360][165])

print (ima01[345][378])
print (ima01[450][378])
print (ima01[360][343])

print (ima01[250][130])
print (ima01[250][200])

print (ima01[250][379])
print (ima01[250][308])
'''

ima00[ima01==14] = 45
ima00[ima01==16] = 45
ima00[ima01==17] = 45

ima00[ima01==54] = 55
ima00[ima01==56] = 55
ima00[ima01==57] = 55

ima00[ima01==11] = 65
ima00[ima01==13] = 65

ima00[ima01==51] = 75
ima00[ima01==53] = 75

cv2.fillPoly(ima00,pts=[pol1],color=((85)))
cv2.fillPoly(ima00,pts=[pol2],color=((95)))


trap3 = np.array([[0,  147],[77, 98],[193,320],[0,  320]])
trap4 = np.array([[385,147],[308,98],[193,320],[385,320]])

ima01[:,:] = 0
cv2.fillPoly(ima01,pts=[trap3],color=(105))
cv2.fillPoly(ima01,pts=[trap4],color=(115))
ima01[ima00 != 0] = ima00[ima00!= 0]

trap5 = np.array([[126,70],[193,70],[193,167],[113,167],[77, 98]])
trap6 = np.array([[260,70],[194,70],[194,167],[272,167],[308,98]])



ima00[:,:] = 0
cv2.fillPoly(ima00,pts=[trap5],color=(125))
cv2.fillPoly(ima00,pts=[trap6],color=(135))
ima00[ima01 != 0] = ima01[ima01!= 0]





#cv2.fillPoly(ima01, pts=[trap5], color=(100))
#cv2.fillPoly(ima01, pts=[trap3], color=(200))
#cv2.circle(ima01, centre, radi2, (255), -1)

cv2.imwrite('data/shot_chart/prova.png',ima00)


cv2.imshow('data/shot_chart/prova.png',ima00)
cv2.waitKey(0)
cv2.destroyAllWindows()


sys.exit()
