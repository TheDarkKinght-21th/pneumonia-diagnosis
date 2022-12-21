import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2

my_w = tk.Tk()
my_w.geometry("650x500")  # Size of the window
my_w.title('Penuemonia Classifier')
my_font1=('times', 18, 'bold')
frm1 = tk.LabelFrame(my_w, text="폐렴 진단기", pady=15, padx=15)
frm1.grid(row=0, column=0, pady=10, padx=10, sticky="nswe")
my_w.columnconfigure(0, weight=1)   # 프레임 (0,0)은 크기에 맞춰 늘어나도록
my_w.rowconfigure(0, weight=1)

lb1 = tk.Label(frm1,text='Add X-ray Photo',width=20,font=my_font1)
lb1.grid(row=0,column=0)
image_x=0

listb1 = tk.Listbox(frm1,width=60,height=1)
listb1.grid(row=1, column=0,padx = 10, pady=10)

b1 = tk.Button(frm1, text='사진 올리기',
   width=20,command = lambda:upload_file())
b1.grid(row=1,column=1)

frm2 = tk.LabelFrame(frm1, text="사진", pady=15, padx=15,width=250,height=250)
frm2.grid(row=2, column=0, pady=10, padx=10, sticky="nswe")

frm3 = tk.LabelFrame(frm1, text="결과", pady=15, padx=15,width=250,height=2)
frm3.grid(row=3, column=0, pady=10, padx=10, sticky="nswe")

lb2 = tk.Label(frm3, text="진단결과 : ", width=15, height=1)
lb2.grid(row=0, column=0)

listb2 = tk.Listbox(frm3, width=35, height=1)
listb2.grid(row=0, column=1)

from keras.models import load_model

model = load_model('C:\\Users\\Mr.wi\\Desktop\\long\\cnn_model.h5')
print("log : model upload complete")

def upload_file():
    global img
    global img2
    print("log : clicked upload button")

    f_types = [('Jpeg Files', '*.jpeg')]
    filename = filedialog.askopenfilename(filetypes=f_types)
    listb1.delete(0,"end")
    listb1.insert(0,filename)

    image = Image.open(filename)
    # The (450, 350) is (height, width)
    img2 = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
    img2 = cv2.resize(img2, (160,160))
    img2 = img2/255
    img2 = img2.reshape(1,160,160,1)
    image = image.resize((200, 200), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(image)


    b2 =tk.Label(frm2,image=img,width=200,height=200) # using Button
    b2.grid(row=0,column=0)

    res = model.predict(img2,verbose = 1)
    print("log : Diagnosis complete")
    res = res[0][0]
    if res <= 0.5:
        listb2.delete(0, "end")
        listb2.insert(0,("폐렴 (정상 : {0:.2f}%, 폐렴 : {1:.2f}%)".format(res*100,(1-res)*100)))
        print("log : Diagnosis => 폐렴")
    elif res > 0.5:
        listb2.delete(0, "end")
        listb2.insert(0,("정상 (정상 : {0:.2f}%, 폐렴 : {1:.2f}% )".format(res*100,(1-res)*100)))
        print("log : Diagnosis => 정상")

my_w.mainloop()  # Keep the window open
print("log : app exit")



