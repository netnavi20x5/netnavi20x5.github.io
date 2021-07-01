#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
#import seaborn as sb


# In[102]:


from datetime import datetime
now = datetime.now()
current_time = now.strftime("%H:%M:%S")
time_now="Updated Time "+ current_time


# In[103]:


print (time_now)


# In[3]:


malaysia_covid_url='https://query.data.world/s/v55vhdiey6gg5rq6wacpo3u4umsk65'
malaysia_vaccine_url='https://raw.githubusercontent.com/CITF-Malaysia/citf-public/main/vaccination/vax_malaysia.csv'
df_my_covid = pd.read_csv(malaysia_covid_url)
df_my_vacci = pd.read_csv(malaysia_vaccine_url)


# In[5]:


df_my_covid


# In[73]:


df_cov_clean=df_my_covid[["date","new_cases","icu"]].set_index("date")
df_vacc_clean=df_my_vacci[["date","dose2_cumul"]].set_index("date")
df_comb=df_vacc_clean.join(df_cov_clean)
df_comb=df_comb.dropna()
data_analytic=df_comb.tail(7)
table=df_comb.tail(7).to_html().replace('<table border="1" class="dataframe">','<table class="table">')


# In[74]:


data_analytic.tail().to_html().replace('<table border="1" class="dataframe">','<table class="table">')


# In[53]:


round(data_analytic.new_cases.mean())


# In[82]:


date=data_analytic.tail(1).index.values[0]


# In[106]:


fully_vacc=round(data_analytic.dose2_cumul.tail(1).mean())
population=32365998
cases_7days_mean=round(data_analytic.new_cases.mean())
icu_7days_mean=round(data_analytic.icu.mean())
date=" updated at "+data_analytic.tail(1).index.values[0] +" on " +time_now

def results_covid(case,case_max,icu,icu_max,vacc):
    pstart="""<p class="lead font-weight-normal">"""
    pend="""</p>"""
    output=""

    if (cases_7days_mean-case_max>0):
        #print("We need to lessen average positive case by :" ,str(int(case-case_max)))
        output=output+pstart+"The Average 7 day case is : <b>"+str(int(cases_7days_mean))+"</b>"+        "<br> Our target is  : <b>" +str(int(case_max))+"</b>"+        "<br> We need to lessen average positive case by : <b>" +str(int(case-case_max))+"</b>"+pend

    else:
        #print("We Reached The Target")
        output=output+pstart+("<b>We Reached The Target</b>")+pend
    if (icu_7days_mean-icu_max>0):
        #print("We need to lessen average ICU case by about :" ,str(int(icu-icu_max)))
        output=output+pstart+("We need to lessen average ICU case by about : <b>" +str(int(icu-icu_max)))+"</b>"+pend
    else:
        #print("ICU seem to be in Acceptable Condition")
        output=output+pstart+"ICU seem to be in <b> Acceptable Condition</b>"+pend
    #print("Our current Vaccination is about: ",str(round(vacc/population*100,2))," of the population")
    output=output+pstart+("Our current Vaccination is about: <b>"+str(round(vacc/population*100,2))+" </b>of the population")+pend
    return output

def header(phase):
    return date+"""<h1 class="display-4 font-weight-normal">"""+phase+"""</h1>"""
    

if ((cases_7days_mean<500)&((icu_7days_mean)<500)&((fully_vacc/population)>.6)):
    #print("We are in Phase 4")
    phase=header("We are in Phase 4")
elif ((cases_7days_mean<2000)&((icu_7days_mean)<700)&((fully_vacc/population)>.4)):
    #print("We are in Phase 3")
    phase=header("We are in Phase 3")
    result=results_covid(cases_7days_mean,500,icu_7days_mean,500,fully_vacc)
    #print(result)
elif ((cases_7days_mean<4000)&((icu_7days_mean)<800)&((fully_vacc/population)>.1)):
    #print("We are in Phase 2")
    phase=header("We are in Phase 2")
    result=results_covid(cases_7days_mean,2000,icu_7days_mean,700,fully_vacc)
    #print(result)
else:
    #print("We are in Phase 1")
    phase=header("We are in Phase 1")
    result=results_covid(cases_7days_mean,4000,icu_7days_mean,1000,fully_vacc)
    #print(result)


# In[107]:


pstart="""<p class="lead font-weight-normal">"""
pend="""</p>"""


source="""
<b>Sources</b>

<br>COVID-19 MY PROJECT BY ARIFIN WAN NOR
<a href="https://data.world/wnarifin/covid-19-my">Link</a>

<br>CITF-Malaysia
Official Github account of the National Covid-19 Immunisation Program (PICK) in Malaysia. Powered by MySejahtera.
<a href="https://github.com/CITF-Malaysia">Link</a>
"""


upperhalf="""
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no" />
        <meta name="description" content="" />
        <meta name="author" content="" />
        <title>Are We There Yet? </title>
        <!-- Favicon-->
        <link rel="icon" type="image/x-icon" href="assets/favicon.ico" />
        <!-- Core theme CSS (includes Bootstrap)-->
        <link href="css/styles.css" rel="stylesheet" />
    </head>
    <body>
        <!-- Responsive navbar-->
        <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
            <div class="container">
                <a class="navbar-brand" href="#">Are We There Yet? MCO 3.0 Phases</a>
                <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation"><span class="navbar-toggler-icon"></span></button>
                <div class="collapse navbar-collapse" id="navbarSupportedContent">
                    <ul class="navbar-nav ms-auto mb-2 mb-lg-0">
                        <li class="nav-item"><a class="nav-link active" aria-current="page" href="#">Home</a></li>
                        <li class="nav-item"><a class="nav-link" href="#">Link</a></li>
                        <!---
                        <li class="nav-item dropdown">
                            <a class="nav-link dropdown-toggle" id="navbarDropdown" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">Dropdown</a>
                            <ul class="dropdown-menu dropdown-menu-end" aria-labelledby="navbarDropdown">
                                <li><a class="dropdown-item" href="#">Action</a></li>
                                <li><a class="dropdown-item" href="#">Another action</a></li>
                                <li><hr class="dropdown-divider" /></li>
                                <li><a class="dropdown-item" href="#">Something else here</a></li>
                            </ul>
                        </li>
                        --->
                    </ul>
                </div>
            </div>
        </nav>
        <!-- Page content-->
        <div class="container">
            <div class="text-center mt-5">
              <div class="col-md-5 p-lg-5 mx-auto my-5">
"""

mid=""
mid=phase+result
mid=mid+source
mid=mid+table#phase+result



lowerhalf="""
</div>
</div>
</div>
<!-- Bootstrap core JS-->
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js"></script>
<!-- Core theme JS-->
<script src="js/scripts.js"></script>
</body>
</html>
"""

final=upperhalf+mid+lowerhalf
#print (final)

f = open("/home/faridil/netnavi20x5.github.io/AreWeThereYet/index.html", "w")
f.write(final)
f.close()


# In[ ]:




