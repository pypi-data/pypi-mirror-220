def main():
    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk,GdkPixbuf,GLib
    from os import path as pathtodir
    from os import makedirs
    from numpy import array,transpose,column_stack,copy,row_stack,ptp,argwhere,linspace,ravel,vstack
    from numpy import abs as npabs
    from matplotlib.pyplot import subplots
    from pandas import DataFrame,read_csv
    import datetime
    from base64 import b64decode
    def mainfn(mod,mod1,path):

        thrupt=[]
        d_obj = []
        d_time =[]
        # Loading data with exit module
        for i in range(0,4):
            path1=path[i]        
            path2=path[i+4]        
            th,obj,time,savecsv=dataextraction(i,mod,path1,path2)        
            d_obj.append(obj)
            d_time.append(time)
            thrupt.append(th)
            dg = DataFrame(savecsv)
            dg.to_csv('data/result'+str(i+1)+'.csv',header=["Time","object","time in min","Total time spent"],index=False)
        # making a copy of data
        actthrpt=[]
        actthrpt=thrupt.copy()
        obj=array(d_obj[0])
        obj1=d_obj.copy()
        time1=d_time.copy()
        # making a statistical data

        d1=transpose(array([[DataFrame(d_time[0][:thrupt[0]]).describe(include="all")] for _ in range(1)])).ravel().astype(int)
        d2=transpose(array([[DataFrame(d_time[1][:thrupt[1]]).describe(include="all")] for _ in range(1)])).ravel().astype(int)
        d3=transpose(array([[DataFrame(d_time[2][:thrupt[2]]).describe(include="all")] for _ in range(1)])).ravel().astype(int)
        d4=transpose(array([[DataFrame(d_time[3][:thrupt[3]]).describe(include="all")] for _ in range(1)])).ravel().astype(int)

        # combineing statistical data with other identifiers 
        L=["count","mean","std","min","25%","50%","75%","max"]
        v=column_stack((array(L),d1,d2,d3,d4))
        arr=["","case 1","case 2","case 3","case 4"]
        v1=copy(v)
        a=copy(array(v[1:,1:]))
        v[1:,1:]=[[str(datetime.timedelta(seconds=int(x))) for  x  in a[i]] for i in range(7)]
        arr=row_stack((arr,v))

        result = ""
        for row in arr:
          for col in row:
            if len(col)<20:
              if col=="mean":
                result=result+col+" "*(18-len(col))  
              if col=="std":
                result=result+col+" "*(22-len(col))            
              else:
                if col!="mean":
                  result=result+col+" "*(20-len(col))
            else:
              result=result+col
          result=result+"\n\n"

        labels=["case 1","case 2","case 3","case 4"]
        dg = DataFrame(arr)
        # Saving statistical data for exit module
        dg.to_csv("data/result.csv",index=False)
        # color prefernces for ploting
        colors=["red","orange","blue","green"]
        del d_obj
        del d_time
        del v
        del arr
        d_obj = []
        d_time =[]
        # Loading data with entry module
        for i in range(0,4):
            path1=path[i]        
            path2=path[i+4]        
            th,obj,time,savecsv=dataextraction(i,mod1,path1,path2)        
            d_obj.append(obj)
            d_time.append(time)

        obj=array(d_obj[0])
        thrupt=actthrpt
      # making a statistical data for entry module

        d1=transpose(array([[DataFrame(d_time[0][:thrupt[0]]).describe(include="all")] for _ in range(1)])).ravel().astype(int)
        d2=transpose(array([[DataFrame(d_time[1][:thrupt[1]]).describe(include="all")] for _ in range(1)])).ravel().astype(int)
        d3=transpose(array([[DataFrame(d_time[2][:thrupt[2]]).describe(include="all")] for _ in range(1)])).ravel().astype(int)
        d4=transpose(array([[DataFrame(d_time[3][:thrupt[3]]).describe(include="all")] for _ in range(1)])).ravel().astype(int)

      # combineing statistical data with other identifiers for entry module
        L=["count","mean","std","min","25%","50%","75%","max"]
        v=column_stack((array(L),d1,d2,d3,d4))
        arr=["","case 1","case 2","case 3","case 4"]
        a=copy(array(v[1:,1:]))
        v[1:,1:]=[[str(datetime.timedelta(seconds=int(x))) for  x  in a[i]] for i in range(7)]
        arr=row_stack((arr,v))
        qresult = ""
        for row in arr:
          for col in row:
            if len(col)<20:
              if col=="mean":
                qresult=qresult+col+" "*(18-len(col))  
              if col=="std":
                qresult=qresult+col+" "*(22-len(col))            
              else:
                if col!="mean":
                  qresult=qresult+col+" "*(20-len(col))

            else:
              qresult=qresult+col

          qresult=qresult+"\n\n"

        dg = DataFrame(arr)
        # Saving statistical data for entry module
        dg.to_csv("data/queueresult.csv",index=False)


        return result,obj1,time1,colors,thrupt,v1,labels,qresult
    def gen(persons,Simulation_time,path,time_slot):
        tp=[] # total people per case
        for i in range(1,5):
            # initialize raw string
            s="""COM	time	Objecttyp	Order Nr(A)"""+"\n"+"""GEN			"""

            arr_time=[]    
            x=0
            value=0
            while((value)<Simulation_time):
                s=s+"\n"+str(value)+"\t"+str(x+1)+"\t"+str(x+1)+"\t"
                arr_time.append(value)
                x=x+1
                if x%persons[i-1]==0:
                    value=value+time_slot
            tp.append(len(arr_time))

            save_location=str(path)+"/Data"+str(i)+".txt"

            with open(save_location, "w") as f:
                f.write(s)

        return "All data files have been generated !",tp

    def dataextraction(case,mod,path1,path2):
     # The data from .tra file is extracted with slicing and wrote to input.csv file
      dg=DataFrame()
      file_path = path1
      with open(file_path, "r") as file:
          contents = file.readlines()
          arr = []      
          for line in contents[3:]:
              elements = line.strip().split()
              arr.append([element for element in elements])      
          title = contents[2].strip().split()      
          title_arr = [element for element in title]      
          title_arr.append("0")
          title_arr.append("0")
          dg = DataFrame(arr)  
      dg.to_csv('data/input'+str(case+1)+'.csv',header=title_arr,index=False)



      # Total time, list of module, list of objects, throughtput time and arrival intervel stored to variables

      df =DataFrame(read_csv('data/input'+str(case+1)+'.csv')) # tra file dataframe
      df=df.fillna(0)
      df=df[df['BST+']=='B-']  # slicing tra file dataframe based on event object module exit

      # New data frame formed with time,object corresponding to desired module
      arvl = read_csv(path2, sep='\t') #loading Arrival dataframe
      arvl=arvl.fillna(0)

      data1=array(df[df["ETT+"]==mod]['FLAGS']).astype(int)  # module exit time array
      data2=array(df[df["ETT+"]==mod]['OID-']).astype(int)   # object array 
      data3=data1/60
      data3=[int(x) for x in data3] # module exit time array in minutes
      data4=data1-array(arvl[arvl["Objecttyp"].isin(array(df[df["ETT+"]==mod]['OID-'].astype(float)))]["COM"]).astype(int)  # total time spent by object in the system
      result=column_stack((data1,data2,data3,data4)) # dataframe to write to csv 
      return len(data4),data2,data4,result

    def fn(case):

        df =DataFrame(read_csv('data/input'+str(case)+'.csv',low_memory=False))
        b_plus=df[df['BST+']=='B+']
        b_minus=df[df['BST+']=='B-']
        mod=list(set(b_plus['ETT+']))
        modlis=[1,4,5,6,7,8,9,10,11,22,12,13,14,15,16,17,21,18,19,23]
        dict=['ein','An','L1','Reg','L2','PreV_e','PreV_1','PreV_2','PreV_3','PreV_4','PreV_a','L3','Vacc_e','Vacc_1','Vacc_2','Vacc_3','Vacc_4','Vacc_a','L4','aus']
        values =[[x for x in dict]for _ in range(0,1)]
        values.append([0 for _ in range(0,len(modlis))])
        values=transpose(array(values))

        for x in mod:
            nw1=b_minus[b_minus['ETT+']==x]
            nw2=b_plus[b_plus['ETT+']==x] 

            max_diff = ptp(npabs((array(nw1[['FLAGS']]).flatten())-array(nw2[nw2['OID-'].isin(nw1['OID-'])]['FLAGS'])))

            t=argwhere(array(modlis) == x)[0][0]

            values[t][1]=int(max_diff/60)

        return values

    def qmod():
        a=[]
        mod=[]
        for i in range(0,4):
            temp=fn(i+1)
            a.append(temp[:,1])
            mod=temp[:,0]
        v=vstack((mod,a))
        dg = DataFrame(transpose(v))
        dg.to_csv('data/queue.csv',header=["Module","1","2","3","4"],index=False)
        return v


    # Icon image data in base64 to avoid external dependency
    image_data = "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"
    # Decode the Base64 string
    decoded_data = b64decode(image_data)
    # Using image loader
    loader = GdkPixbuf.PixbufLoader.new()
    loader.write(decoded_data)
    loader.close()
    pixbuf = loader.get_pixbuf()
    qlegend="""ein 		Entrance

    An 			Sign Up

    L1 			Lane 

    Reg 		Registration

    L2 			Lane 2

    PreV_e 	Pre Vaccination Enter

    PreV_1	Pre Vaccination Counter 1

    PreV_2	Pre Vaccination Counter 2

    PreV_3	Pre Vaccination Counter 3

    PreV_4	Pre Vaccination Counter 4

    PreV_a	Pre Vaccination Exit

    L3			Lane 3

    Vacc_e 	Vaccination Entrance

    Vacc_1 	Vaccination Counter 1

    Vacc_2 	Vaccination Counter 2

    Vacc_3 	Vaccination Counter 3

    Vacc_4 	Vaccination Counter 4

    Vacc_a 	Vaccination Exit

    L4 			Lane 4

    aus 		Exit"""
    # GTK GUI in xml stored as Raw string, embedded to avoid external dependency
    xml="""<interface>
    <requires lib="gtk+" version="3.24"/>
    <object class="GtkFileFilter" id="tra">
        <patterns>
        <pattern>*.tra</pattern>
        </patterns>
    </object>
    <object class="GtkFileFilter" id="txt">
        <patterns>
        <pattern>*.txt</pattern>
        </patterns>
    </object>
    <object class="GtkWindow" id="my_window">
        <property name="can-focus">False</property>
        <property name="resizable">False</property>
        <property name="window-position">center</property>
        <property name="default-width">1440</property>
        <property name="default-height">810</property>

        <property name="urgency-hint">True</property>
        <property name="gravity">center</property>
        <property name="has-resize-grip">True</property>
        <child>
        <object class="GtkScrolledWindow">
            <property name="visible">True</property>
            <property name="can-focus">True</property>
            <property name="shadow-type">in</property>
            <child>
            <object class="GtkViewport">
                <property name="visible">True</property>
                <property name="can-focus">False</property>
                <child>
                <object class="GtkFixed">
                    <property name="visible">True</property>
                    <property name="can-focus">False</property>
                    <child>
                    <object class="GtkLabel">
                        <property name="name">label</property>
                        <property name="width-request">50</property>
                        <property name="height-request">170</property>
                        <property name="visible">True</property>
                        <property name="can-focus">False</property>
                        <property name="label" translatable="yes">Case 1


    Case 2


    Case 3


    Case 4</property>
                    </object>
                    <packing>
                        <property name="x">76</property>
                        <property name="y">233</property>
                    </packing>
                    </child>
                    <child>
                    <object class="GtkFileChooserButton" id="t2">
                        <property name="width-request">200</property>
                        <property name="height-request">34</property>
                        <property name="visible">True</property>
                        <property name="can-focus">False</property>
                        <property name="filter">tra</property>
                        <property name="title" translatable="yes">Case 1</property>
                    </object>
                    <packing>
                        <property name="x">134</property>
                        <property name="y">276</property>
                    </packing>
                    </child>
                    <child>
                    <object class="GtkFileChooserButton" id="t3">
                        <property name="width-request">200</property>
                        <property name="height-request">34</property>
                        <property name="visible">True</property>
                        <property name="can-focus">False</property>
                        <property name="filter">tra</property>
                        <property name="title" translatable="yes">Case 1</property>
                    </object>
                    <packing>
                        <property name="x">134</property>
                        <property name="y">325</property>
                    </packing>
                    </child>
                    <child>
                    <object class="GtkFileChooserButton" id="t4">
                        <property name="width-request">200</property>
                        <property name="height-request">34</property>
                        <property name="visible">True</property>
                        <property name="can-focus">False</property>
                        <property name="filter">tra</property>
                        <property name="title" translatable="yes">Case 1</property>
                    </object>
                    <packing>
                        <property name="x">134</property>
                        <property name="y">374</property>
                    </packing>
                    </child>
                    <child>
                    <object class="GtkLabel">
                        <property name="name">label</property>
                        <property name="width-request">50</property>
                        <property name="height-request">170</property>
                        <property name="visible">True</property>
                        <property name="can-focus">False</property>
                        <property name="label" translatable="yes">Case 1


    Case 2


    Case 3


    Case 4</property>
                    </object>
                    <packing>
                        <property name="x">67</property>
                        <property name="y">445</property>
                    </packing>
                    </child>
                    <child>
                    <object class="GtkFileChooserButton" id="d1">
                        <property name="width-request">200</property>
                        <property name="height-request">34</property>
                        <property name="visible">True</property>
                        <property name="can-focus">False</property>
                        <property name="halign">start</property>
                        <property name="filter">txt</property>
                        <property name="title" translatable="yes">Case 1</property>
                    </object>
                    <packing>
                        <property name="x">134</property>
                        <property name="y">440</property>
                    </packing>
                    </child>
                    <child>
                    <object class="GtkFileChooserButton" id="d2">
                        <property name="width-request">200</property>
                        <property name="height-request">34</property>
                        <property name="visible">True</property>
                        <property name="can-focus">False</property>
                        <property name="filter">txt</property>
                        <property name="title" translatable="yes">Case 1</property>
                    </object>
                    <packing>
                        <property name="x">134</property>
                        <property name="y">489</property>
                    </packing>
                    </child>
                    <child>
                    <object class="GtkFileChooserButton" id="d3">
                        <property name="width-request">200</property>
                        <property name="height-request">34</property>
                        <property name="visible">True</property>
                        <property name="can-focus">False</property>
                        <property name="filter">txt</property>
                        <property name="title" translatable="yes">Case 1</property>
                    </object>
                    <packing>
                        <property name="x">134</property>
                        <property name="y">538</property>
                    </packing>
                    </child>
                    <child>
                    <object class="GtkFileChooserButton" id="d4">
                        <property name="width-request">200</property>
                        <property name="height-request">34</property>
                        <property name="visible">True</property>
                        <property name="can-focus">False</property>
                        <property name="filter">txt</property>
                        <property name="title" translatable="yes">Case 1</property>
                    </object>
                    <packing>
                        <property name="x">134</property>
                        <property name="y">587</property>
                    </packing>
                    </child>
                    <child>
                    <object class="GtkEntry" id="txt1">
                        <property name="width-request">98</property>
                        <property name="height-request">34</property>
                        <property name="visible">True</property>
                        <property name="can-focus">True</property>
                        <property name="tooltip-text" translatable="yes">Only enter integer</property>
                        <property name="width-chars">10</property>
                        <property name="input-purpose">number</property>
                    </object>
                    <packing>
                        <property name="x">238</property>
                        <property name="y">643</property>
                    </packing>
                    </child>
                    <child>
                    <object class="GtkEntry" id="txt2">
                        <property name="name">dfewg</property>
                        <property name="width-request">98</property>
                        <property name="height-request">34</property>
                        <property name="visible">True</property>
                        <property name="can-focus">True</property>
                        <property name="tooltip-text" translatable="yes">Only enter integer</property>
                        <property name="width-chars">10</property>
                        <property name="input-purpose">number</property>
                    </object>
                    <packing>
                        <property name="x">237</property>
                        <property name="y">694</property>
                    </packing>
                    </child>
                    <child>
                    <object class="GtkLabel">
                        <property name="width-request">227</property>
                        <property name="height-request">80</property>
                        <property name="visible">True</property>
                        <property name="can-focus">False</property>
                        <property name="label" translatable="yes">enter the module at object exits


    enter the module at object enters</property>
                    </object>
                    <packing>
                        <property name="y">641</property>
                    </packing>
                    </child>
                    <child>
                    <object class="GtkButton" id="gen">
                        <property name="label" translatable="yes">Generate  Statistics</property>
                        <property name="width-request">165</property>
                        <property name="height-request">34</property>
                        <property name="visible">True</property>
                        <property name="can-focus">True</property>
                        <property name="receives-default">True</property>
                        <property name="halign">center</property>
                        <property name="valign">center</property>
                        <signal name="clicked" handler="on_button_clicked" swapped="no"/>
                    </object>
                    <packing>
                        <property name="x">169</property>
                        <property name="y">749</property>
                    </packing>
                    </child>
                    <child>
                    <object class="GtkLabel" id="result">
                        <property name="width-request">300</property>
                        <property name="height-request">300</property>
                        <property name="visible">True</property>
                        <property name="can-focus">False</property>
                    </object>
                    <packing>
                        <property name="x">369</property>
                        <property name="y">44</property>
                    </packing>
                    </child>
                    <child>
                    <object class="GtkEntry" id="int">
                        <property name="width-request">50</property>
                        <property name="height-request">34</property>
                        <property name="visible">True</property>
                        <property name="can-focus">True</property>
                        <property name="tooltip-text" translatable="yes">Persons/slot</property>
                        <property name="width-chars">5</property>
                        <property name="primary-icon-tooltip-text" translatable="yes">Persons/slot</property>
                        <property name="input-purpose">number</property>
                    </object>
                    <packing>
                        <property name="x">7</property>
                        <property name="y">25</property>
                    </packing>
                    </child>
                    <child>
                    <object class="GtkButton" id="datagen">
                        <property name="label" translatable="yes">Data Gen</property>
                        <property name="width-request">95</property>
                        <property name="height-request">34</property>
                        <property name="visible">True</property>
                        <property name="can-focus">True</property>
                        <property name="receives-default">True</property>
                        <signal name="clicked" handler="datagenerator" swapped="no"/>
                    </object>
                    <packing>
                        <property name="x">255</property>
                        <property name="y">25</property>
                    </packing>
                    </child>
                    <child>
                    <object class="GtkEntry" id="simu">
                        <property name="width-request">60</property>
                        <property name="height-request">34</property>
                        <property name="visible">True</property>
                        <property name="can-focus">True</property>
                        <property name="tooltip-text" translatable="yes">simulation time</property>
                        <property name="width-chars">7</property>
                        <property name="input-purpose">number</property>
                    </object>
                    <packing>
                        <property name="x">6</property>
                        <property name="y">67</property>
                    </packing>
                    </child>
                    <child>
                    <object class="GtkFileChooserButton" id="dirselect">
                        <property name="width-request">164</property>
                        <property name="height-request">34</property>
                        <property name="visible">True</property>
                        <property name="can-focus">False</property>
                        <property name="tooltip-text" translatable="yes">Select Folder to Save Files</property>
                        <property name="action">select-folder</property>
                        <property name="title" translatable="yes">Case 1</property>
                    </object>
                    <packing>
                        <property name="x">180</property>
                        <property name="y">67</property>
                    </packing>
                    </child>
                    <child>
                    <object class="GtkEntry" id="int1">
                        <property name="width-request">58</property>
                        <property name="height-request">34</property>
                        <property name="visible">True</property>
                        <property name="can-focus">True</property>
                        <property name="tooltip-text" translatable="yes">Persons/slot</property>
                        <property name="width-chars">5</property>
                        <property name="primary-icon-tooltip-markup" translatable="yes">Persons/slot</property>
                        <property name="input-purpose">number</property>
                    </object>
                    <packing>
                        <property name="x">69</property>
                        <property name="y">25</property>
                    </packing>
                    </child>
                    <child>
                    <object class="GtkEntry" id="int2">
                        <property name="width-request">58</property>
                        <property name="height-request">34</property>
                        <property name="visible">True</property>
                        <property name="can-focus">True</property>
                        <property name="tooltip-text" translatable="yes">Persons/slot</property>
                        <property name="width-chars">5</property>
                        <property name="primary-icon-tooltip-text" translatable="yes">Persons/slot</property>
                        <property name="input-purpose">number</property>
                    </object>
                    <packing>
                        <property name="x">131</property>
                        <property name="y">25</property>
                    </packing>
                    </child>
                    <child>
                    <object class="GtkEntry" id="int3">
                        <property name="width-request">58</property>
                        <property name="height-request">34</property>
                        <property name="visible">True</property>
                        <property name="can-focus">True</property>
                        <property name="tooltip-text" translatable="yes">Persons/slot</property>
                        <property name="width-chars">5</property>
                        <property name="primary-icon-tooltip-text" translatable="yes">Persons/slot</property>
                        <property name="input-purpose">number</property>
                    </object>
                    <packing>
                        <property name="x">193</property>
                        <property name="y">25</property>
                    </packing>
                    </child>
                    <child>
                    <object class="GtkLabel" id="result1">
                        <property name="width-request">300</property>
                        <property name="height-request">300</property>
                        <property name="visible">True</property>
                        <property name="can-focus">False</property>
                    </object>
                    <packing>
                        <property name="x">865</property>
                        <property name="y">44</property>
                    </packing>
                    </child>
                    <child>
                    <object class="GtkLabel">
                        <property name="width-request">50</property>
                        <property name="height-request">110</property>
                        <property name="visible">True</property>
                        <property name="can-focus">False</property>
                        <property name="label" translatable="yes">Select .tra files</property>
                        <property name="angle">90</property>
                        <attributes>
                        <attribute name="weight" value="bold"/>
                        <attribute name="scale" value="1"/>
                        </attributes>
                    </object>
                    <packing>
                        <property name="x">13</property>
                        <property name="y">271</property>
                    </packing>
                    </child>
                    <child>
                    <object class="GtkLabel">
                        <property name="width-request">50</property>
                        <property name="height-request">111</property>
                        <property name="visible">True</property>
                        <property name="can-focus">False</property>
                        <property name="label" translatable="yes">Select .txt files</property>
                        <property name="angle">90</property>
                        <attributes>
                        <attribute name="weight" value="bold"/>
                        <attribute name="scale" value="1"/>
                        </attributes>
                    </object>
                    <packing>
                        <property name="x">13</property>
                        <property name="y">478</property>
                    </packing>
                    </child>
                    <child>
                    <object class="GtkLabel">
                        <property name="name">label</property>
                        <property name="width-request">181</property>
                        <property name="height-request">30</property>
                        <property name="visible">True</property>
                        <property name="can-focus">False</property>
                        <property name="label" translatable="yes">Case 1       Case 2       Case 3       Case 4</property>
                    </object>
                    <packing>
                        <property name="x">12</property>
                    </packing>
                    </child>
                    <child>
                    <object class="GtkLabel" id="status">
                        <property name="width-request">260</property>
                        <property name="height-request">25</property>
                        <property name="visible">True</property>
                        <property name="can-focus">False</property>
                        <attributes>
                        <attribute name="foreground" value="#08a6ffff0000"/>
                        </attributes>
                    </object>
                    <packing>
                        <property name="x">37</property>
                        <property name="y">105</property>
                    </packing>
                    </child>
                    <child>
                    <object class="GtkLabel" id="Dwell">
                        <property name="width-request">176</property>
                        <property name="height-request">20</property>
                        <property name="visible">True</property>
                        <property name="can-focus">False</property>
                        <attributes>
                        <attribute name="foreground" value="#08a6ffff0000"/>
                        </attributes>
                    </object>
                    <packing>
                        <property name="x">457</property>
                        <property name="y">10</property>
                    </packing>
                    </child>
                    <child>
                    <object class="GtkLabel" id="Queue">
                        <property name="width-request">150</property>
                        <property name="height-request">20</property>
                        <property name="visible">True</property>
                        <property name="can-focus">False</property>
                        <attributes>
                        <attribute name="foreground" value="#08a6ffff0000"/>
                        </attributes>
                    </object>
                    <packing>
                        <property name="x">960</property>
                        <property name="y">11</property>
                    </packing>
                    </child>
                    <child>
                    <object class="GtkImage" id="drw">
                        <property name="width-request">1000</property>
                        <property name="height-request">562</property>
                        <property name="visible">True</property>
                        <property name="can-focus">False</property>
                    </object>
                    <packing>
                        <property name="x">349</property>
                        <property name="y">393</property>
                    </packing>
                    </child>
                    <child>
                    <object class="GtkLabel" id="plot">
                        <property name="width-request">260</property>
                        <property name="height-request">25</property>
                        <property name="visible">True</property>
                        <property name="can-focus">False</property>
                        <attributes>
                        <attribute name="foreground" value="#08a6ffff0000"/>
                        </attributes>
                    </object>
                    <packing>
                        <property name="x">704</property>
                        <property name="y">354</property>
                    </packing>
                    </child>
                    <child>
                    <object class="GtkImage" id="modq">
                        <property name="width-request">1000</property>
                        <property name="height-request">562</property>
                        <property name="visible">True</property>
                        <property name="can-focus">False</property>
                    </object>
                    <packing>
                        <property name="x">351</property>
                        <property name="y">1031</property>
                    </packing>
                    </child>
                    <child>
                    <object class="GtkLabel" id="qlegend">
                        <property name="width-request">300</property>
                        <property name="height-request">700</property>
                        <property name="visible">True</property>
                        <property name="can-focus">False</property>
                    </object>
                    <packing>
                        <property name="x">26</property>
                        <property name="y">1030</property>
                    </packing>
                    </child>
                    <child>
                    <object class="GtkLabel" id="qplot">
                        <property name="width-request">325</property>
                        <property name="height-request">25</property>
                        <property name="visible">True</property>
                        <property name="can-focus">False</property>
                        <attributes>
                        <attribute name="foreground" value="#08a6ffff0000"/>
                        </attributes>
                    </object>
                    <packing>
                        <property name="x">770</property>
                        <property name="y">986</property>
                    </packing>
                    </child>
                    <child>
                    <object class="GtkEntry" id="timeslot">
                        <property name="width-request">74</property>
                        <property name="height-request">34</property>
                        <property name="visible">True</property>
                        <property name="can-focus">True</property>
                        <property name="tooltip-text" translatable="yes">Enter the time between each slots</property>
                        <property name="width-chars">7</property>
                        <property name="input-purpose">number</property>
                    </object>
                    <packing>
                        <property name="x">91</property>
                        <property name="y">67</property>
                    </packing>
                    </child>
                    <child>
                    <object class="GtkFileChooserButton" id="t1">
                        <property name="width-request">200</property>
                        <property name="height-request">34</property>
                        <property name="visible">True</property>
                        <property name="can-focus">True</property>
                        <property name="filter">tra</property>
                        <property name="show-hidden">True</property>
                        <property name="title" translatable="yes">Case 1</property>
                    </object>
                    <packing>
                        <property name="x">134</property>
                        <property name="y">227</property>
                    </packing>
                    </child>
                    <child>
                    <object class="GtkLabel" id="datagenresults">
                        <property name="width-request">360</property>
                        <property name="height-request">80</property>
                        <property name="visible">True</property>
                        <property name="can-focus">False</property>
                    </object>
                    <packing>
                        <property name="y">137</property>
                    </packing>
                    </child>
                </object>
                </child>
            </object>
            </child>
        </object>
        </child>
    </object>
    </interface>"""


    # Arriaval data generator  
    def datagenerator(case):
        persons=[]
        ch="int"
        for i in range (0,4):
            if i!=0:
              if builder.get_object(ch+str(i)).get_property("text")=="":
                 return 0
              else: 
                 persons.append(int(builder.get_object(ch+str(i)).get_property("text")))
            else:
              if builder.get_object(ch).get_property("text")=="":
                 return 0
              else:
                 persons.append(int(builder.get_object(ch).get_property("text")))

        if builder.get_object("timeslot").get_property("text")=="":
           return 0
        else:
           time_slot=int(builder.get_object("timeslot").get_property("text"))

        if builder.get_object("simu").get_property("text")=="":
           return 0
        else:
           Simulation_time=int(builder.get_object("simu").get_property("text"))

        if builder.get_object("dirselect").get_filename()==None:
           return 0
        path=str(builder.get_object("dirselect").get_filename())
        status,tp=gen(persons,Simulation_time,path,time_slot)
        datagenresults="""				Case 1		Case 2		Case 3 	Case 4

    Total People	   """+str(tp[0])+"""		   """+str(tp[1])+"""		    """+str(tp[2])+"""		   """+str(tp[3])+"""	"""
        builder.get_object("datagenresults").set_property("label",datagenresults)
        builder.get_object("status").set_property("label",status)

    def zcom(t1,t2,path):
        stat,d_obj,d_time,colors,thrupt,v,labels,qresult=mainfn(int(t1),int(t2),path)
        label1=builder.get_object("result")
        label1.set_property("label", stat)
        label2=builder.get_object("Dwell")
        label2.set_property("label", "Total Dwell Time Statistics")
        label3=builder.get_object("result1")
        label3.set_property("label", qresult)
        label4=builder.get_object("Queue")
        label4.set_property("label", "Queue Time Statistics")
        drw=builder.get_object("drw")
        fig, ax = subplots(figsize=(16, 9))
        for i in range(0,4):
            ax.plot(d_obj[i],d_time[i],color=colors[i],label=labels[i])
            ax.plot(linspace(0,thrupt[i], thrupt[i]),[int(v[1][i+1])]*len(linspace(0,thrupt[i], thrupt[i])),color=colors[i],linestyle='--')

        ax.set_xlabel('Number of People')
        ax.set_ylabel('Time spent in sec')
        ax.legend()
        ax.grid(True)
        fig.savefig('data/plot.png', dpi=(1000/fig.get_figwidth()))

        pixbuf = GdkPixbuf.Pixbuf.new_from_file("data/plot.png")
        drw.set_from_pixbuf(pixbuf)
        builder.get_object("plot").set_property("label","Generated from Dwell Time")
        v=qmod()
        ls=[[0 for _ in range(20)] for _ in range(4)]
        for x in range(0,4):
            ls[x]=list(int(i) for i in (v[x+1]))
        fig,ax = subplots(figsize=(16, 9))
        ax.bar(v[0], ls[0], color=colors[0],label=labels[0])
        ax.bar(v[0], ls[1],bottom=ls[0], color=colors[1],label=labels[1])
        ax.bar(v[0], ls[2], bottom=[sum(x) for x in zip(ls[0], ls[1])], color=colors[2],label=labels[2])
        ax.bar(v[0], ls[3], bottom=[sum(x) for x in zip(ls[0], ls[1],ls[2])], color=colors[3],label=labels[3])
        for i, v in enumerate(ls[0]):
            if v != 0:
                ax.text(i, v/2, str(v), ha='center', va='center')
            if ls[1][i] != 0:
                ax.text(i, v+ls[1][i]/2, str(ls[1][i]), ha='center', va='center')
            if ls[2][i] != 0:
                ax.text(i, v+ls[1][i]+ls[2][i]/2, str(ls[2][i]), ha='center', va='center')
            if ls[3][i] != 0:
                ax.text(i, v+ls[1][i]+ls[2][i]+ls[3][i]/2, str(ls[3][i]), ha='center', va='center')
        ax.set_title('Stack bar graph of waiting time at modules')
        ax.set_xlabel('\nModules')
        ax.set_ylabel('Waiting Time/ Case')
        ax.legend()
        fig.savefig('data/plotq.png', dpi=(1000/fig.get_figwidth()))
        modq=builder.get_object("modq")
        pixq = GdkPixbuf.Pixbuf.new_from_file("data/plotq.png")
        modq.set_from_pixbuf(pixq)
        builder.get_object("qplot").set_property("label","Stack bar graph of waiting time at modules")
        builder.get_object("qlegend").set_property("label",qlegend)


    def on_button_clicked(case):
        path=[]
        txt1=builder.get_object("txt1")
        if txt1.get_property("text")=="":
           return 0
        t1=txt1.get_property("text")
        txt2=builder.get_object("txt2")
        if txt2.get_property("text")=="":
           return 0
        t2=txt2.get_property("text")

        t="t"


        for i in range(0,4):
           if builder.get_object(t+str(i+1)).get_filename()==None:
              return 0
           else:
              path.append(builder.get_object(t+str(i+1)).get_filename()) # .tra files

        t="d"

        for i in range(0,4):
           if builder.get_object(t+str(i+1)).get_filename()==None:
              return 0
           else:
              path.append(builder.get_object(t+str(i+1)).get_filename()) # # .txt files


        folder_name = 'data'
        if not pathtodir.exists(folder_name):
          makedirs(folder_name)


        zcom(t1,t2,path)

    builder = Gtk.Builder()
    builder.add_from_string(xml)
    builder.connect_signals({"on_button_clicked": on_button_clicked,"datagenerator":datagenerator})
    datagen= builder.get_object("datagen")
    window = builder.get_object("my_window")
    window.set_title("Vaccination center Simulation")
    window.set_position(Gtk.WindowPosition.CENTER)
    window.set_icon(pixbuf)
    window.connect("delete-event", Gtk.main_quit)
    window.show_all()
    Gtk.main()
