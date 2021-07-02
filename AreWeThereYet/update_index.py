#!/usr/bin/env python
# coding: utf-8

# In[8]:


import pandas as pd
#import seaborn as sb


# In[9]:


from datetime import datetime
now = datetime.now()
current_time = now.strftime("%H:%M:%S")
time_now="Updated Time "+ current_time


# In[4]:


print (time_now)


# In[10]:


malaysia_covid_url='https://query.data.world/s/v55vhdiey6gg5rq6wacpo3u4umsk65'
malaysia_vaccine_url='https://raw.githubusercontent.com/CITF-Malaysia/citf-public/main/vaccination/vax_malaysia.csv'
df_my_covid = pd.read_csv(malaysia_covid_url)
df_my_vacci = pd.read_csv(malaysia_vaccine_url)


# In[5]:


df_my_covid


# In[11]:


df_cov_clean=df_my_covid[["date","new_cases","icu"]].set_index("date")
df_vacc_clean=df_my_vacci[["date","dose2_cumul"]].set_index("date")
df_comb=df_vacc_clean.join(df_cov_clean)
df_comb=df_comb.dropna()
data_analytic=df_comb.tail(7)
table=df_comb.tail(7).to_html().replace('<table border="1" class="dataframe">','<table class="table">')


# In[12]:


data_analytic.tail().to_html().replace('<table border="1" class="dataframe">','<table class="table">')


# In[53]:


round(data_analytic.new_cases.mean())


# In[82]:


date=data_analytic.tail(1).index.values[0]


# In[74]:


fully_vacc=round(data_analytic.dose2_cumul.tail(1).mean())
population=32365998
cases_7days_mean=round(data_analytic.new_cases.mean())
icu_7days_mean=round(data_analytic.icu.mean())

date=" updated at "+data_analytic.tail(1).index.values[0] +" on " +time_now

def results_covid(case,case_max,icu,icu_max,vacc):
    pstart="""<p class="lead text-white-50 font-weight-normal">"""
    pend="""</p>"""
    output=""

    if (cases_7days_mean-case_max>0):
        #print("We need to lessen average positive case by :" ,str(int(case-case_max)))
        output=output+pstart+"The Average 7 day case is : <b>"+str(int(cases_7days_mean))+"</b>"+        "<br> Our target is  : <b>" +str(int(case_max))+"</b>"+        "<br> We need to lessen average positive case by : <b>" +str(int(case-case_max))+"</b>"+pend

    else:
        #print("We Reached The Target")
        output=output+pstart+("<b>We Reached The Target.</b>"+pend)
    if (icu_7days_mean-icu_max>0):
        #print("We need to lessen average ICU case by about :" ,str(int(icu-icu_max)))
        output=output+pstart+("We need to lessen average ICU case by about : <b>" +str(int(icu-icu_max)))+"</b>"+pend
    else:
        #print("ICU seem to be in Acceptable Condition")
        output=output+pstart+"ICU seem to be in <b> Acceptable Condition  The average 7 days ICU cases is : "+ str(int(icu)) +" </b>"+pend
    #print("Our current Vaccination is about: ",str(round(vacc/population*100,2))," of the population")
    output=output+pstart+("Our current Vaccination is about: <b>"+str(round(vacc/population*100,2))+" </b>of the population")+pend
    return output

def header(phase):
    return date+"""<h1 class="display-4 font-weight-normal">"""+phase+"""</h1>"""
    

if ((cases_7days_mean<500)&((icu_7days_mean)<500)&((fully_vacc/population)>.6)):
    #print("We are in Phase 4")
    phase=header("We are in Phase 4")
    phase_text="We are in Phase 4"

elif ((cases_7days_mean<2000)&((icu_7days_mean)<700)&((fully_vacc/population)>.4)):
    #print("We are in Phase 3")
    phase=header("We are in Phase 3")
    phase_text="We are in Phase 3"
    result=results_covid(cases_7days_mean,500,icu_7days_mean,500,fully_vacc)
    #print(result)
elif ((cases_7days_mean<4000)&((icu_7days_mean)<900)&((fully_vacc/population)>.1)):
    #print("We are in Phase 2")
    phase=header("We are in Phase 2")
    phase_text="We are in Phase 2"
    result=results_covid(cases_7days_mean,2000,icu_7days_mean,700,fully_vacc)
    #print(result)
else:
    #print("We are in Phase 1")
    phase=header("We are in Phase 1")
    phase_text="We are in Phase 1"
    result=results_covid(cases_7days_mean,4000,icu_7days_mean,900,fully_vacc)
    #print(result)
result


# In[25]:





# In[ ]:





# In[76]:


template = open('template.html', 'r')
template_lines = template.readlines()
 
count = 0
# Strips the newline character
final=""
for line in template_lines:
    count += 1
    final=final+line
    #final=line.replace("<$PHASE$>",phase).replace("<$OUTPUT$>",result).replace("<$DATE$>",date).replace("<$TABLE$>",table)
    #final=final+line.replace("<$OUTPUT$>",result)
    #final=final+line.replace("<$PHASE$>",phase)
    #final=final+line.replace("<$DATE$>",date)
    #final=final+line.replace("<$TABLE$>",table)

final=final.replace("<$PHASE$>",phase_text)
final=final.replace("<$DATE$>",date)
final=final.replace("<$OUTPUT$>",result)
final=final.replace("<$TABLE$>",table)
f = open("index.html", "w")
f.write(final)
f.close()


# In[58]:


print(final)


# In[59]:


f = open("index.html", "w")
f.write(final)
f.close()

