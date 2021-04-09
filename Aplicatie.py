import tkinter as tk
from PIL import ImageTk,Image
#import tabele
import Dep_Tabela_Calitativa.tabele as tabele           #pentru export final



class App(tk.Frame):
    def __init__(self,master):
        
        tk.Frame.__init__(self,master)
        self.grid(row=0,column=0)
        self.master.title("Tabela_Calitativa")
        self.master.geometry("1055x695")
        self.master.resizable(0, 0)
        self.master.iconbitmap('Dep_Tabela_Calitativa/icon.ico')
        self.mark1=1
        self.mark2=1
        self.mark3=1
        self.bloks =[]
        self.cadran_o={}
        self.cadran_v={}
        self.cadran_x={}

        # sectiunea superioara ##############################################################################################################################################
        self.hf_img = ImageTk.PhotoImage(Image.open('Dep_Tabela_Calitativa/b_cover.jpg').resize((1050,150)))
        self.l1_img = ImageTk.PhotoImage(Image.open('Dep_Tabela_Calitativa/TAB1.jpg'))
        self.l2_img = ImageTk.PhotoImage(Image.open('Dep_Tabela_Calitativa/TAB2.jpg'))
        self.upit = ImageTk.PhotoImage(Image.open('Dep_Tabela_Calitativa/upit.png').resize((100,100)))
        self.c_frame=tk.Canvas(master, height=150, width=1050)
        self.c_frame.create_image(0, 0, image=self.hf_img, anchor='nw')
        self.c_frame.create_image(10, 10, image=self.upit, anchor='nw')
        self.h_frame=tk.Frame(master,bg='grey', width=370, height=20)

        ######### definire fereastra informatii ########
        self.info_frame=tk.Frame(master,bg='grey', width=150, height=20)
        self.info_window=self.c_frame.create_window(830,25,height=22,width=163,window=self.info_frame, anchor='nw')
        self.autori=ImageTk.PhotoImage(Image.open('Dep_Tabela_Calitativa/autori.jpg'))
        self.tab1=ImageTk.PhotoImage(Image.open('Dep_Tabela_Calitativa/TabRelRo.jpg'))
        self.marcaje=ImageTk.PhotoImage(Image.open('Dep_Tabela_Calitativa/legenda.jpg'))
        
        self.mb=  tk.Menubutton ( self.info_frame, text="Autori", bd=2,relief='raised')
        self.mb.grid(row=0,column=0)
        self.mb.menu =  tk.Menu ( self.mb, tearoff = 1 )
        self.mb["menu"] =  self.mb.menu
        self.mb.menu.add_checkbutton ( image=self.autori)
        
        self.mb2=  tk.Menubutton ( self.info_frame, text="Eșantion", bd=2,relief='raised')
        self.mb2.grid(row=0,column=1)
        self.mb2.menu =  tk.Menu ( self.mb2, tearoff = 1 )
        self.mb2["menu"] =  self.mb2.menu
        self.mb2.menu.add_checkbutton ( image=self.tab1)

        self.mb3=  tk.Menubutton ( self.info_frame, text="Legenda", bd=2,relief='raised')
        self.mb3.grid(row=0,column=2)
        self.mb3.menu =  tk.Menu ( self.mb3, tearoff = 1 )
        self.mb3["menu"] =  self.mb3.menu
        self.mb3.menu.add_checkbutton ( image=self.marcaje)
        

        ######### definire fereastra de input ########
        tk.Label(self.h_frame,text="N = ").grid(row=0,column=0)
        self.N=tk.Spinbox(self.h_frame, from_=2, to=1000000000, command=self.update_result,width=10)
        self.N.grid(row=0,column=1)                       #
        tk.Label(self.h_frame,text="     Nivel Inspectie = ").grid(row=0,column=2)
        self.D=tk.Spinbox(self.h_frame, values=('S1','S2','S3','S4','I','II','III'), command=self.update_result,width=5,state="readonly")
        self.D.grid(row=0,column=3)
        tk.Label(self.h_frame,text="   A.Q.L. = ").grid(row=0,column=4)
        self.AQL=tk.Spinbox(self.h_frame, values=('0.010','0.015','0.025','0.040','0.065','0.10','0.15','0.25','0.40','0.65','1.0','1.5','2.5','4.0','6.5','10','15','25','40','65','100','150','250','400','650','1000'), command=self.update_result,width=5,state="readonly") ###  test
        self.AQL.grid(row=0,column=5)                                                           ###  test
        self.master.bind("<Return>",self.update_result)
        self.window_frame=self.c_frame.create_window(121,25,height=22,width=367,window=self.h_frame, anchor='nw')
        self.c_frame.grid(row=0,column=0)

        # sectiunea inferioara ##############################################################################################################################################
        self.l_frame=tk.Frame(master)
        self.l_frame.grid(row=1,column=0)

        ######### definire tabel de baza ########
        self.tabel=tk.Canvas(self.l_frame, height=536, width=910)
        self.tabel.grid(row=0,column=1)
        self.t_img = ImageTk.PhotoImage(Image.open('Dep_Tabela_Calitativa/T_COMPLET_NOU.jpg'))
        self.tabel.create_image(0, 0, image=self.t_img, anchor='nw')

        ######### definire functie scroll tabel ########
        self.ysb = tk.Scrollbar(self.l_frame, orient="vertical", command=lambda *args:[self.tabel.yview(*args),self.aql_label()])
        self.tabel.configure(yscrollcommand=self.ysb.set)
        self.tabel.configure(scrollregion=(0,0,920,5471))
        self.ysb.grid(row=0,column=2, sticky="ns")
        self.tabel.bind("<MouseWheel>",self._on_mousewheel)

        ######### definire butoane skip ########
        self.skip_frame=tk.Frame(self.l_frame)
        self.skip_frame.grid(row=0,column=0)
        tk.Button(self.skip_frame,text="Eșantionare unică\nInspecție normală",command=lambda:self.skip_to(0.0),height=2,width=15,bd=4).grid(row=0,column=0)                      #
        tk.Button(self.skip_frame,text="Eșantionare unică\nInspecție severă",command=lambda:self.skip_to(0.058124657283860355),height=2,width=15,bd=4).grid(row=1,column=0)  #
        tk.Button(self.skip_frame,text="Eșantionare unică\nInspecție redusă",command=lambda:self.skip_to(0.1259367574483641),height=2,width=15,bd=4).grid(row=2,column=0)      #
        tk.Button(self.skip_frame,text="Eșantionare dublă\nInspecție normală",command=lambda:self.skip_to(0.20380186437579967),height=3,width=15,bd=4).grid(row=3,column=0)      #
        tk.Button(self.skip_frame,text="Eșantionare dublă\nInspecție severă",command=lambda:self.skip_to(0.2898921586547249),height=3,width=15,bd=4).grid(row=4,column=0)    #
        tk.Button(self.skip_frame,text="Eșantionare dublă\nInspecție redusă",command=lambda:self.skip_to(0.37707914458051545),height=3,width=15,bd=4).grid(row=5,column=0)     #
        tk.Button(self.skip_frame,text="Eșantionare multiplă\nInspecție normală",command=lambda:self.skip_to(0.45457868762566256),height=4,width=15,bd=4).grid(row=6,column=0)    #
        tk.Button(self.skip_frame,text="Eșantionare multiplă\nInspecție severă",command=lambda:self.skip_to(0.638640102357887),height=4,width=15,bd=4).grid(row=7,column=0)   #
        tk.Button(self.skip_frame,text="Eșantionare multiplă\nInspecție redusă",command=lambda:self.skip_to(0.8227015170901115),height=4,width=15,bd=4).grid(row=8,column=0)    #

        ######### trebuie executate dupa declararea tururor variabilelor ########
        self.aql_label()
        self.error1=self.c_frame.create_text(125, 50,text="",fill='white',anchor='nw')
        
        aux=self.AQL.get()
        for i in range(9):
            if(tabele.tabel_2[i]['l']==878):
                self.cadran_v[i]=self.create_transparent(tabele.tabel_3[0]['y_baza'],tabele.tabel_2[i]['baza'],tabele.tabel_3[0][aux]+tabele.tabel_3[0]['l_aux'],tabele.tabel_2[i]['baza']+tabele.tabel_2[i]['ad_aux_y'],fill='blue',alpha=.2)
            else:
                self.cadran_v[i]=self.create_transparent(tabele.tabel_3[1]['y_baza'],tabele.tabel_2[i]['baza'],tabele.tabel_3[1][aux]+tabele.tabel_3[1]['l_aux'],tabele.tabel_2[i]['baza']+tabele.tabel_2[i]['ad_aux_y'],fill='blue',alpha=.2)
                print("nothing else")

        self.update_result()

    def _on_mousewheel(self, event):
        self.tabel.yview_scroll(int(-1*(event.delta/120)), "units")
        print(self.ysb.get())                ###  test
        print(self.ysb.get()[0])             ###  test
        print(int(-1*(event.delta/120)))     ###  test
        self.aql_label()

    def skip_to (self,x):
        self.tabel.yview_scroll(int((x-self.ysb.get()[0])/0.0095), "units")
        print(int((0.20380186437579967-self.ysb.get()[0])/0.0095))       ###  test
        print(x)                                                         ###  test
        self.ysb.set(x,x+0.09797112045329921)
        self.aql_label()

    def aql_label(self):
        self.mark2=self.mark1
        if(self.ysb.get()[0]>0.20380186437579967):
            self.mark1=1
        else:
            self.mark1=0

        if(self.mark1!=self.mark2):
            if(self.mark1==1):
                try:
                    self.c_frame.delete(self.label)
                except:
                    pass
                self.label=self.c_frame.create_image(121, 109, image=self.l2_img, anchor='nw')
                print('switch')                                               ###  test
            else:
                try:
                    self.c_frame.delete(self.label)
                except:
                    pass
                self.label=self.c_frame.create_image(121, 80, image=self.l1_img, anchor='nw')
                print('switch')                                               ###  test

    def create_transparent(self,x1, y1, x2, y2, **kwargs):
        print((x2-x1, y2-y1))                                               ###  test
        alpha = int(kwargs.pop('alpha') * 255)
        fill = kwargs.pop('fill')
        fill = root.winfo_rgb(fill) + (alpha,)
        image = Image.new('RGBA', (x2-x1, y2-y1), fill)
        self.bloks.append(ImageTk.PhotoImage(image))
        return self.tabel.create_image(x1, y1, image=self.bloks[-1], anchor='nw')
    
    def update_result(self,event=0):
        x=int(self.N.get())

        if((x>1000000000000)or(x<2)):
            self.c_frame.itemconfig(self.error1,text="N out of range ( 2 - 1000000000000 )")
            x=2
        else:
            self.c_frame.itemconfig(self.error1,text="")
        
        y=self.D.get()
        z=self.AQL.get()
        print(self.N.get())                                           ###  test

        ################# aflare litera de cod ######################
        for i in range(15):
            if ((x>=tabele.tabel_1[i+1]['lim_i'])&(x<=tabele.tabel_1[i+1]['lim_s'])):
                print("Grad severitate {}".format(tabele.tabel_1[i+1]['dup_severitate'][y]))   ###  test
                aux1=tabele.tabel_1[i+1]['dup_severitate'][y]
                print(aux1)                                          ###  test

        ################# trasare cadrane ############################
        for i in range(9):
            aux2=tabele.tabel_2[i]

            ################# cadrane orizontale ###############
            if (aux2['ad_aux']!=aux2[aux1]['ad']):
                try:
                    self.tabel.delete(self.cadran_o[i])
                except:
                    pass
                self.cadran_o[i]=self.create_transparent(0,aux2[aux1]['x'],aux2['l'],aux2[aux1]['x']+aux2[aux1]['ad'],fill='blue',alpha=.2)
                print(self.cadran_o[i])                                          ###  test
            else:
                self.tabel.move(self.cadran_o[i],0,aux2[aux1]['x']-aux2['x_aux'])

            ################# cadrane verticale ###############
            if(aux2['l']==878):
                self.mark3=0
            else:
                self.mark3=1

            self.tabel.move(self.cadran_v[i],tabele.tabel_3[self.mark3][z]-tabele.tabel_3[self.mark3]['y_aux'],0)

            ################# cadrane centrale ###############
            if (aux2['ad_aux']!=aux2[aux1]['ad']):
                try:
                    self.tabel.delete(self.cadran_x[i])
                except:
                    pass
                self.cadran_x[i]=self.tabel.create_rectangle(tabele.tabel_3[self.mark3][z],aux2[aux1]['x'],tabele.tabel_3[self.mark3][z]+tabele.tabel_3[self.mark3]['l_aux'],aux2[aux1]['x']+aux2[aux1]['ad'],width=2,outline='white')
            else:
                self.tabel.move(self.cadran_x[i],tabele.tabel_3[self.mark3][z]-tabele.tabel_3[self.mark3]['y_aux'],aux2[aux1]['x']-aux2['x_aux'])

            aux2['ad_aux']=aux2[aux1]['ad']
            aux2['x_aux']=aux2[aux1]['x']

        tabele.tabel_3[0]['y_aux']=tabele.tabel_3[0][z]
        tabele.tabel_3[1]['y_aux']=tabele.tabel_3[1][z]
                


if __name__=='__main__':
    root=tk.Tk()
    app=App(root)
    app.mainloop()
