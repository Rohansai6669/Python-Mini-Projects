from tkinter import *

exp=""
def press(num):
    global exp
    exp = exp + str(num)
    equation.set(exp)
def equal():
    try:
        global exp
        total=str(eval(exp))
        equation.set(total)
        exp=""
    except:
        equation.set("error")
def clear():
    global exp
    exp = ""
    equation.set("")
def delete():
    global exp
    l=len(exp)
    exp=exp[:l-1]
    equation.set(exp)
    
root=Tk()
root.title("Calculator")
root.configure(bg="#EFBC9B")
root.geometry('280x520')
equation=StringVar()
txt=Entry(root,textvariable=equation,font=("Arial", 14),bg="#F5F7F8")
txt.grid(columnspan=6,rowspan=2,ipadx=10,ipady=30,padx=20,pady=20)
w=6

button1=Button(root,text='1',fg='black',relief='flat',command=lambda:press(1),height=3,width=w ,background="#FBF3D5",borderwidth=3)
button1.grid(row=5,column=1,pady=10)

button2=Button(root,text='2',fg='black',relief='flat',command=lambda:press(2),height=3,width=w,background="#FBF3D5")
button2.grid(row=5,column=2)

button3=Button(root,text='3',fg='black',relief='flat',command=lambda:press(3),height=3,width=w,background="#FBF3D5")
button3.grid(row=5,column=3)

button4=Button(root,text='4',fg='black',relief='flat',command=lambda:press(4),height=3,width=w,background="#FBF3D5")
button4.grid(row=4,column=1,pady=10)

button5=Button(root,text='5',fg='black',relief='flat',command=lambda:press(5),height=3,width=w,background="#FBF3D5")
button5.grid(row=4,column=2)

button6=Button(root,text='6',fg='black',relief='flat',command=lambda:press(6),height=3,width=w,background="#FBF3D5")
button6.grid(row=4,column=3)

button7=Button(root,text='7',fg='black',relief='flat',command=lambda:press(7),height=3,width=w,background="#FBF3D5")
button7.grid(row=3,column=1,pady=10)

button8=Button(root,text='8',fg='black',relief='flat',command=lambda:press(8),height=3,width=w,background="#FBF3D5")
button8.grid(row=3,column=2)

button9=Button(root,text='9',fg='black',relief='flat',command=lambda:press(9),height=3,width=w,background="#FBF3D5")
button9.grid(row=3,column=3)

button0=Button(root,text='0',fg='black',relief='flat',command=lambda:press(0),height=3,width=w,background="#FBF3D5")
button0.grid(row=6,column=2,pady=10)

button_dot=Button(root,text='.',fg='black',relief='flat',command=lambda:press(0),height=3,width=w,background="#FBF3D5")
button_dot.grid(row=6,column=1)

button_OB=Button(root,text='(',fg='black',relief='flat',command=lambda:press('('),height=3,width=w,background="#FBF3D5")
button_OB.grid(row=2,column=1,pady=10)

button_CB=Button(root,text=')',fg='black',relief='flat',command=lambda:press(')'),height=3,width=w,background="#FBF3D5")
button_CB.grid(row=2,column=2)

# +-*/
button_add=Button(root,text='+',fg='black',relief='flat',command=lambda:press('+'),height=3,width=w,background="#D6DAC8")
button_add.grid(row=3,column=4)

button_sub=Button(root,text='-',fg='black',relief='flat',command=lambda:press('-'),height=3,width=w,background="#D6DAC8")
button_sub.grid(row=4,column=4)

button_mul=Button(root,text='*',fg='black',relief='flat',command=lambda:press('*'),height=3,width=w,background="#D6DAC8")
button_mul.grid(row=5,column=4)

button_mul=Button(root,text='/',fg='black',relief='flat',command=lambda:press('/'),height=3,width=w,background="#D6DAC8")
button_mul.grid(row=6,column=4)

button_eq=Button(root,text='=',fg='black',relief='flat',command=lambda:equal(),height=3,width=w,background="#9CAFAA")
button_eq.grid(row=6,column=3)

button_clr=Button(root,text='C',fg='black',relief='flat',command=lambda:clear(),height=3,width=w,background="#9CAFAA")
button_clr.grid(row=2,column=3)

button_del=Button(root,text='D',fg='black',relief='flat',command=lambda:delete(),height=3,width=w,background="#9CAFAA")
button_del.grid(row=2,column=4)

root.mainloop()