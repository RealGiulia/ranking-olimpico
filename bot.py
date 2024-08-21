"""
WARNING:

Please make sure you install the bot dependencies with `pip install --upgrade -r requirements.txt`
in order to get all the dependencies on your Python environment.

Also, if you are using PyCharm or another IDE, make sure that you use the SAME Python interpreter
as your IDE.

If you get an error like:
```
ModuleNotFoundError: No module named 'botcity'
```

This means that you are likely using a different Python interpreter than the one used to install the dependencies.
To fix this, you can either:
- Use the same interpreter as your IDE and install your bot with `pip install --upgrade -r requirements.txt`
- Use the same interpreter as the one used to install the bot (`pip install --upgrade -r requirements.txt`)

Please refer to the documentation for more information at
https://documentation.botcity.dev/tutorials/python-automations/web/
"""


# Import p/ o web bot
from botcity.web import WebBot, Browser, By
# import do pandas para criar arquivo excel
import pandas as pd

# Função principal que contém todos os passos do processo
def main():

    # Instancie o plugin
    bot = WebBot()

    # Configura o modo headless
    bot.headless = True

    # Seleciona o browser desejado
    bot.browser = Browser.CHROME

    # indica o caminho do driver
    bot.driver_path = "drivers\chromedriver.exe"

    # Abre o site das olimpíadas
    bot.browse("https://olympics.com/pt/paris-2024/medalhas")

    # 
    bot.wait(3000) 

    # Encontra tabela com as informaç~eos dos países e ranking de medalhas
    medal_table = bot.find_element('//*[@id="p2024-main-content"]/div[1]/div[2]/div[2]/div/div[2]', By.XPATH)

    # encontra linhas da tabela com base na classe
    table_lines = medal_table.find_elements(By.CLASS_NAME, "emotion-srm-hi2jpg")[0:8]

    # cria lista para armazenar os dicionários com as informações obtidas
    medal_ranking = []

    # para cada linha da tabela, encontra as informações desejadas e adiciona na lista
    for line in table_lines:
        infos = {}
        line_content = line.find_elements_by_tag_name("span")
        country_name = line_content[2].get_property('innerText')
        qtd_gold = line_content[3].get_property('innerText')
        qtd_silver = line_content[4].get_property('innerText')
        qtd_bronze = line_content[5].get_property('innerText')
        total_medals = line_content[6].get_property('innerText')

        infos["Country"] = country_name
        infos["Gold Medals"] = qtd_gold
        infos["Silver Medals"] = qtd_silver
        infos["Bronze Medals"] = qtd_bronze
        infos["Total amount of medals"] = total_medals
        medal_ranking.append(infos)


    # Transformando lista de dicionários em um arquivo excel
    df = pd.DataFrame(medal_ranking)
    df.to_excel("ranking_olimpico.xlsx")
    # Finish and clean up the Web Browser
    # You MUST invoke the stop_browser to avoid  
    # leaving instances of the webdriver open
    bot.stop_browser()


if __name__ == '__main__':
    main()
