from PyPDF2 import PdfReader
import pandas as pd
import re
from tabulate import tabulate


def clean_string(string):
    words = string.split()
    return ' '.join(words)

def text_between_deleter(start,end,text):
    start_index = text.find(start)
    end_index = text.find(end)
    # Check if both "Probability" and "Impac t" are found
    if start_index != -1 and end_index != -1:
        # Extract the text before "Probability" and after "Impac t"
        before_text = text[:start_index]
        after_text = text[end_index + len("Impac t"):]
        
        # Combine the two parts to get the modified text
        modified_text = before_text + after_text
        
        return modified_text
    else:
        text


#Define pages with subchapters and subtitles : SS
big_pages=[6,14,24,33,42,54,58]

###############################################################################################################

reader = PdfReader('PMBOK6-2017 395-458.pdf')
num_pages=len(reader.pages)
LSS=[]
for num_page in big_pages:
    #Extract the content of the page
    page = reader.pages[num_page]
    #Deleting SOME unwanted sentences
    text = page.extract_text().replace("Not For Distribution, Sale or Reproduction.\n","")
    text = re.sub("Figure.*?$","",text, flags=re.MULTILINE)
    if num_page==54:
        text = re.sub("11.*?$","",text, flags=re.MULTILINE)
    
    #getting the parts regarding the Inputs/T&T/Outputs in a list l
    if num_page==6:
        l=text.split('.1 ')[2:]
    else :
        l=text.split('.1 ')[1:]


    #Deleting the • and some uneccesry text
    List=[]
    for element in l :
        while '•' in element:
            element=re.sub(r"•.*?\n",'',element)
            element=re.sub(r"•.*?$",'',element)
        if num_page==54:
            element=re.sub(r"charter[\s\S]*",'',element,flags=re.IGNORECASE)
        List.append(element)

    #Split the "cleaned" text into input/output/tools&techniques
    L=[re.sub(r'\d',"",element.replace("\n","")).split(".") for element in List]
    #print("\n ---------------\nPAGE NUMBER IS   ",num_page,"\n ----------------------- \n")


    L = [[clean_string(item) for item in sublist] for sublist in L]

    


    #Invert the order of IN/T&T/Ou
    L[0],L[1]=L[1],L[0]

    #Adding nubering for each item
    L0=[]
    for sublist in L:
        sublist0=[]
        for item in sublist:
            numbering = "11."+str(big_pages.index(num_page)+1)+"."+str(L.index(sublist)+1)+"."+str(sublist.index(item)+1)+" "
            item=numbering+item
            sublist0.append(item)
        L0.append(sublist0)


    LSS.append(L0)

#Manually fixing mistakes
#Page15
LSS[1][0][0]="11.2.1.1 Project management plan"
LSS[1][1][2]="11.2.2.3 Data analysis"
#Page25
LSS[2][1][2]="11.3.2.3 Data analysis"
#Page 43
LSS[4][1][8]="11.5.2.9 Decision making"
LSS[4][2][1]="11.5.3.2 Project management plan updates"
#Page 59
LSS[6][1][0]="11.7.2.1 Data analysis"
LSS[6][2][4]="11.7.3.5 Organizational process assets updates"


    #List of chapters titles:
L_titles=["11.1 PLAN RISK MANAGEMENT","11.2 IDENTIFY RISKS","11.3 PERFORM QUALITATIVE RISK ANALYSIS"
        ,"11.4 PERFORM QUANTITATIVE RISK ANALYSIS","11.5 PLAN RISK RESPONSES","11.6 IMPLEMENT RISK RESPONSES",
        "11.7 MONITOR RISKS"]
    
    #Dectionnary matching each title with it's subchapters
initial_dict=dict(zip(L_titles,LSS))

###############################################################################################################
#Part2 extracting text from the titles

#remove the text of unnecessary pages 
unnecessary_pages=[i for i in range(7)]+[11,14,15,24,25,33,34,42,43,54,58,59] 


text=""
for page_num in range(num_pages):
    if page_num not in unnecessary_pages:
        text0=reader.pages[page_num].extract_text().replace("Not For Distribution, Sale or Reproduction.\n","")
        #Removing figure title names from text
        text0=re.sub("Figure.*?$","",text0, flags=re.MULTILINE)
        #Remove the text from the figures
        if page_num==13:
            text0 = text_between_deleter("ProbabilityProbability","Impac t",text0)
        if page_num== 12:
            text0 = re.sub("Table.*?$","",text0, flags=re.MULTILINE)
            text0 = text_between_deleter("SCAL","K\nNo change",text0)
        if page_num ==31:
            text0 = text_between_deleter("ProximityHigh","\nacceptable",text0)
        if page_num == 38:
            text0 = text_between_deleter("shown in","Uncer tainty",text0)
        if page_num == 39:
            text0 = text_between_deleter("shown in","faults",text0)
        if page_num == 40:
            text0 = text_between_deleter("is shown in","$50M)",text0)
        
        
        text+=text0
     
        
        
        

    

# text cleaning :
#removing the number of page in the footer //Not perfect
text=re.sub(r'\b(\d{3})(\d)\b',"",text)


#remove the 1st occurence of 11.3.2.6
text=text.replace("11.3.2.6","",1)


KKK=[]
for key in  initial_dict.keys():
    KK=[]
    new_dict={}
    for list_title in initial_dict[key]:
        index_list_title = initial_dict[key].index(list_title)
        L=[]
        
        for ind_title in range(len(list_title)):
            curr_title_number=list_title[ind_title][:8]
            if ind_title!=len(list_title)-1:
                next_title_number=list_title[ind_title+1][:8]
            else :
                if curr_title_number[5]!="3":
                    next_title_number = curr_title_number[:5]+str(int(curr_title_number[5])+1)+".1"
                else:
                    next_title_number = curr_title_number[:3]+str(int(curr_title_number[3])+1)+".1.1"
            #print("Curr title   ----   ",curr_title_number)
            #print("Next title   ----   ",next_title_number,"\n")
            #Still the case of Curr title   ----    11.7.3.5 to fix later
            if curr_title_number == "11.7.3.5":
                next_title_number = "structure."
            #Create dictionnary for each title : content to replace the title only in the initial_dict
            pattern=curr_title_number+"[\s\S]*?"+next_title_number
            l=re.findall(pattern, text, re.IGNORECASE)
            #TO ADD : LINE TO DELETE THE TITLE OF THE ELEMENT FROM THE TEXT
            L.append(l)

            #PART 2 : adding the content of l to the dictionnary
        k = dict(zip(initial_dict[key][index_list_title],L))
        KK.append(k)
    KKK.append(KK)

title_keys=list(initial_dict.keys())
new_dict=dict(zip(title_keys,KKK))


#Data frame creation :
column_names = ['numChapter', 'Chapter', 'numSubChapter', 'subChapter',"Type","numSubTitle","subTitle",
                "content","Ref"]

df = pd.DataFrame(columns=column_names)



#print(new_dict[title_keys[0]])

#PART 3  : transform dictionnary to dataframe
#print(new_dict['11.1 PLAN RISK MANAGEMENT'][0])
for key in title_keys:
    num_chapter = key[:4] #1st column
    chapter_name = key  #2nd column
    #print(num_chapter,"\n -- - \n")
    #print(chapter_name,"\n -- - \n")
    for dict_sub_titles in new_dict[key]:
        iot=new_dict[key].index(dict_sub_titles)
        sub_chapter_number = num_chapter +"."+str(iot+1) # - 3rd column
        if iot==0:                # 5th column
            chapter_type = "INPUTS"
        elif iot==1:
            chapter_type = "Tools and Techniques"
        else :
            chapter_type = "OUTPUTS"
        sub_chapter_name = chapter_name +" "+chapter_type #4th column
        l_subtitles=list(dict_sub_titles.keys())
        for subtitle in l_subtitles: # 6th column
            refs=[]
            num_sub_title=subtitle[:6]#7th column
            subtitle_content = dict_sub_titles[subtitle][0] #8th column
            
            refs=re.findall(r'Section [^\s]{8}', subtitle_content) #9th column

            headless_row_data=[num_chapter,chapter_name,sub_chapter_number,sub_chapter_name,
                                chapter_type,subtitle,num_sub_title,subtitle_content,refs]
            row_data=dict(zip(column_names,headless_row_data))

            df = pd.concat([df, pd.DataFrame([row_data])], ignore_index=True)
df.to_csv('njarbou.csv')
#print(df)







