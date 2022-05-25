from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import pandas as pd
##
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
#%%
csv_file = pd.read_csv('pass_linkedin')

email = csv_file['email'][0]

password = csv_file['password'][0]


position = "cientista de dados"
local = "brasil"

position = position.replace(' ',"%20")

#%%

driver  = webdriver.Chrome()

driver.set_window_size(1024,600)
driver.maximize_window()

##
driver.get("https://www.linkedin.com/login/pt")
time.sleep(2)

##
driver.find_element_by_id("username").send_keys(email)
driver.find_element_by_id("password").send_keys(password)
driver.find_element_by_id("password").send_keys(Keys.RETURN)

#%%
driver.get(
    f"https://www.linkedin.com/jobs/search/?currentJobId=2662929045&geoId=106057199&keywords={position}&location={local}")
time.sleep(2)    


##
job_disc_list = []

## 

for n in range(1,5):    
    button =  driver.find_element_by_xpath(f'//button[@aria-label="Página {n}"]')
    button.click()

    for job in range(1,26):
        driver.find_element_by_xpath(
                f'/html/body/div[6]/div[3]/div[3]/div[2]/div/section[1]/div/div/ul/li[{job}]/div/div/div[1]/div[2]/div[1]/a').click()
        time.sleep(1)
    
        job_desc = driver.find_element_by_class_name('jobs-search__right-rail')
        
        soup = BeautifulSoup(job_desc.get_attribute('outerHTML'), 'html.parser')
        
        job_disc_list.append(soup.text)
          
    time.sleep(2)  
#%%
jobs_df = pd.DataFrame(job_disc_list) 

#%%
#
#
jobs_df = jobs_df.replace(['\n',
                 '^.*?Expect', 
                 '^.*?Qualifications', 
                 '^.*?Required', 
                 '^.*?expected', 
                 '^.*?Responsibilities', 
                 '^.*?Requisitos', 
                 '^.*?Requirements', 
                 '^.*?Qualificações', 
                 '^.*?QualificationsRequired1', 
                 '^.*?você deve ter:', 
                 '^.*?experiência', 
                 '^.*?você:', 
                 '^.*?Desejável', 
                 '^.*?great', 
                 '^.*?Looking For', 
                 '^.*?ll Need', 
                 '^.*?Conhecimento', 
                 '^.*?se:',
                 '^.*?habilidades',                 
                 '^.*?se:',
                 '^.*?REQUISITOS'
                 ], '', regex=True)
##
#%%
stopwords = set(STOPWORDS)

badwords = {'gender', 'experience', 'application', 'Apply', 'salary', 'todos', 'os', 'company', 'identity', 'sexual', 'orientation',
          'de', 'orientação', 'sexual', 'gênero', 'committed', 'toda','client', 'conhecimento',
          'world', 'year', 'save','São', 'Paulo', 'information', 'e', 'orientação', 'sexual', 'equal', 'oppotunity', 'ambiente', 'will',
          'Experiência', 'national origin','todas', 'work', 'de', 'da', 'years', 'pessoa', 'clients', 'Plano', 'creating',
          'employer', 'saúde','em', 'working', 'pessoas', 'mais', 'data', 'people', 'dia', 'one', 'knowledges', 'plataforma',
          'ou', 'benefício', 'para', 'software', 'opportunity', 'tecnologia', 'você', 'mais', 'solution', 'national', 'origin',
          'trabalhar', 'option', 'negócio', 'empresa', 'o', 'sicence', 'team', 'é', 'veteran', 'status', 'etc', 'raça', 'cor', 'belive',
          'nossa', 'uma', 'como', 'Scientist', 'ferramenta', 'projeto', 'que', 'job', 'benefícios', 'knowledge', 'toll', 's', 'modelo',
          'desconto', 'cultura', 'serviço', 'time', 'se', 'solutions', 'mercado', 'das', 'somos', 'problema', 'mundo', 'race', 'color',
          'vaga', 'pelo', 'ser', 'show', 'Seguro', 'Se', 'um', 'Um', 'tool', 'regard', 'without', 'make', 'ao', 'técnica', 'life',
          'interested', 'diversidade', 'proud', 'ability', 'sobre', 'options', 'using', 'área', 'nosso', 'na', 'seu', 'product', 'produto',
          'building', 'skill', 'model', 'religion', 'Share', 'receive', 'consideration', 'Aqui', 'vida', 'ferramentas', 'Vale', 'Refeição',
          'Strong', 'Pay', 'range', 'available', 'part', 'trabalho', 'Alimentação', 'employment', 'qualified', 'applicants', 'gympass',
          'está', 'comprometida', 'forma', 'Transporte', 'Yes', 'gente', 'melhor', 'lugar', 'believe', 'moment', 'próximo','deasafio',
          'dos', 'oportunidade', 'idade', 'new', 'Try', 'Premium', 'deficiência', 'sempre', 'criar', 'employee', 'problemas', 'unavailable',
          'Brasil', 'dado', 'hiring', 'trends', 'equipe', 'recent', 'temos', 'build', 'career', 'nós', 'diferencial', 'ma',
           'total', 'oferecemos', 'contato', 'tem', 'não', 'free', 'Full','Salvar','opções','grátisRecrutando','agora','sua','exibir','compartilhar',
           'há semana', 'cliente','Candidatura','Exibir','soluções','desafio','por','à','Tempo integral','Compartilhar','além','Candidatar','simplificada',
           'nossos negócios','áreas','digital','técnicas','Sênior', 'negócios','nossos','Tempo integral','há semana','ex estudantes','isso', 'Tempo','candidatos',
           'dados jr','compara','ensinoVeja',"clientes"}

stopwords.update(badwords)

##
#%%
wordcloud = WordCloud(background_color='black',
                      stopwords=stopwords,
                      max_words=100,
                      max_font_size=50,
                      random_state=42).generate("".join(jobs_df[0]))

## Plot
#%%
print(wordcloud)
plt.figure(figsize=(10,5))
fig = plt.figure(1)
plt.imshow(wordcloud)
plt.axis('off')
plt.show()

   