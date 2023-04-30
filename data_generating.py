OPENAI_API_KEY = ""

import openai
import re
import pandas as pd
import time

system_content = "I want you to act like a psychologist with 10 years of experience in existential therapy. Treat me as your client. I will discuss my feelings of existential angst, anxiety, and other mental health issues. During our conversation, help me confront and explore the four givens of existence: death, freedom, isolation, and meaninglessness. Encourage me to embrace my freedom to make choices and take responsibility for my actions. As we delve into my experiences, help me recognize and reflect upon the existential challenges and dilemmas that arise from the human condition. Guide me in seeking meaning and purpose in my life, and assist me in embracing my authentic self. Remind me occasionally that my struggles are an inherent part of being human and that growth can arise from confronting these existential concerns. Support me in developing the courage to face my existential anxiety and transform it into creative energy. IMPORTANT: help me to see different perspectives on my situation and empower me to make choices that align with my values and beliefs. Offer me thought-provoking questions and reflections to help me better understand and navigate the existential dimensions of my life. Talk to me as a psychologist talks to their client, give short portions of information and questions. Always write me short messages no more than 100 words."

openai.api_key = OPENAI_API_KEY
messages = [
    {"role": "system", "content": system_content},
    {
        "role": "user",
        "content": "give me an example of psychological session as long as possible for unexpected topic in form of \"Patient: \"blabla\" Therapist: \"blabla\"\"",
    },
]

#messages = [
    #{"role": "system", "content": "you are a programmist"},
    #{
   #     "role": "user",
  #      "content": "I have a string in python in pattern \"patient: \"blablabla\"\" and i want to get \"blablabla\" from this string in python language",
 #   },
#]

df_raw = pd.read_csv('data_linebyline_2.csv')
df_raw = df_raw.drop(columns= ['Unnamed: 0'])
df_hist = pd.read_csv('data_history_2.csv')
df_hist = df_hist.drop(columns= ['Unnamed: 0'])
dic_raw={}
dic_hist ={}

for j in range(1000):
  #  time.sleep(10)

    print(j)
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=messages, max_tokens=1000
    )

    chat_response = completion.choices[0].message.content
    answers = (chat_response.split("Patient: ")[1:])

    first_column_hist = ''
    second_column_hist = ''
    for row in answers:
        try:
            patient, therapist = row.split("Therapist: ")
            patient = re.sub('\n','',patient)
            therapist = re.sub('\n', '', therapist)
            patient = re.sub('"','',patient)
            therapist = re.sub('"', '', therapist)
            dic_raw['Patient: '+patient +' Therapist:'] = therapist

            first_column_hist += second_column_hist + ' Patient: '+ patient + ' Therapist: '
            second_column_hist= therapist
            dic_hist[first_column_hist] = second_column_hist
            df_raw_append = pd.DataFrame.from_dict(dic_raw, orient='index')
            df_hist_append = pd.DataFrame.from_dict(dic_hist, orient='index')
            #print(df_hist_append)
            #print(df_raw_append)
            df_raw_append = df_raw_append.reset_index()
            df_hist_append = df_hist_append.reset_index()
            df_raw = pd.concat([df_raw, df_raw_append], ignore_index=True)
            df_hist = pd.concat([df_hist, df_hist_append], ignore_index=True)
            #print()
            df_raw.to_csv('data_linebyline_2.csv')
            df_hist.to_csv('data_history_2.csv')
            #dic[patient] = therapist
            time.sleep(7)
        except:
            continue


   # df_raw =
   # df_history_save =

    #try:

     #   patient, therapist = re.split('\n\n',chat_response)
      #  patient = patient[patient.find('"')+1:patient.rfind('"')]
       # therapist = therapist[therapist.find('"')+1:therapist.rfind('"')]
        #dataset.append([patient,therapist])
        #time.sleep(20)
        #print(dataset)
        #df = pd.DataFrame(dataset, columns = ['patient','therapist'])
        #df.to_csv('dataset_tuning.csv')
    #except:
      #  continue
