from PyPDF2 import PdfReader
import pandas as pd
import re

reader = PdfReader('b.pdf')
num_pages=len(reader.pages)


#Extract chapter_titles
#Extract Subtitles
text_titles=""
chapters_subtitiles_dict={}
for page_num in range(4,8):
    text_titles+=reader.pages[page_num].extract_text().replace("©2009 Project Management Institute. Practice Standard for Project Risk Management","")
    chapter_titles=[element.replace(" .","").strip() for element in re.findall(r"CHAPTER[\s\S]*?[.]| CHAPTER[\s\S]*?[.]",text_titles)]
    subtitles_list=[element.replace(" .","").strip() for element in re.findall(r'\d.\d [\s\S]*?[.]|\d.\d.\d [\s\S]*?[.]',text_titles)]
chapters_subtitiles_dict=dict(zip(chapter_titles,[[] for i in range(len(chapter_titles))]))

for chapter_index in range(len(chapter_titles)):
    for item in subtitles_list :
        if item[0]==str(chapter_index+1):
            item = ' '.join(item.split())
            chapters_subtitiles_dict[chapter_titles[chapter_index]].append(item.replace("\n",""))
    #chapters_subtitiles_dict=dict(zip(chapter_titles,subtitles_list))
    #chapter_titles=[]
    #subtitles_list=[]


#Define text
text=''
for page_num in range(13,67):
    text0=reader.pages[page_num].extract_text().replace("©2009 Project Management Institute. Practice Standard for Project Risk Management","").replace("\n","")
    text0=' '.join(text0.split())
    text+=text0
text = text.replace("7.2.3 Commitment to Collecting High-Quality","7.2.3 Commitment to Collecting High Quality")


#Define text1
text1=''
for page_num in range(13,67):
    text1+=reader.pages[page_num].extract_text().replace("©2009 Project Management Institute. Practice Standard for Project Risk Management","")


#Data frame creation :

column_names = ['numChapter', 'Chapter', 'numSubChapter', 'subTitle',"content","Ref"]
df = pd.DataFrame(columns=column_names)

for chapter_name in chapters_subtitiles_dict.keys(): #column 2
    numChapter= list(chapters_subtitiles_dict).index(chapter_name) #column 1
    subtitle_names=chapters_subtitiles_dict[chapter_name] 
    for subtitle_name_index in range(len(subtitle_names)):
        third_number=subtitle_names[subtitle_name_index][4]
        numSubChapter=subtitle_names[subtitle_name_index][:4]  #column3
        if third_number.isdigit():
            numSubChapter=subtitle_names[subtitle_name_index][:4]+third_number
        curr_subtitle= subtitle_names[subtitle_name_index] #column 4 
        if subtitle_name_index!=len(subtitle_names)-1:
            next_subtitle= subtitle_names[subtitle_name_index+1]

        else:
            if (numChapter+1) !=len(chapters_subtitiles_dict.keys()):
                next_chap=list(chapters_subtitiles_dict.keys())[numChapter+1]
                next_subtitle="CHAPTER"
            else :
                next_subtitle=""
        #print(next_subtitle)

        pattern=curr_subtitle + "[\s\S]*?" + next_subtitle
        #print(pattern)
        content=(re.findall(pattern,text)) #exctration from text #column 5
 
        refs=re.findall(r'Figure\s\d+-\d+', content[0])
        temp=numChapter
        numChapter+=1
        headless_row_data=[numChapter,chapter_name,numSubChapter,curr_subtitle,
                            content,refs]
        numChapter=temp
        row_data=dict(zip(column_names,headless_row_data))
        df = pd.concat([df, pd.DataFrame([row_data])], ignore_index=True)

df.to_csv('extration_result2.csv')


#df = pd.DataFrame(columns=column_names)

