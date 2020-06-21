import requests
from requests_html import HTMLSession
from bs4 import BeautifulSoup
import scraping

def getHtml(url):

    '''
    * Descrição:
        - Essa função tem o objetivo de fazer a requisição de uma página através da url passada
    * Parâmetro:
        - url: endereço da página ao qual deseja-se buscar
    * Retorno:
        - se a página for encontrada: um objeto soup, da biblioteca Beatiful Soup, que contém a estruturação da página HTML requisitada
        - se a página não for encontrada: 0
    '''

    try:
        session = HTMLSession()
        response = session.get(url)
        
        if response.status_code == 200:
            response.html.render()
            soup = BeautifulSoup(response.html.html, 'lxml')
            return soup
        
        else:
            return 0
        
    except requests.exceptions.RequestException as e:
        print(e)
        return 0

def webScraping(num_lei, num_artigo, num_paragrafo, num_inciso, letra_alinea, num_item):

    '''
    * Descrição:
        - Essa é a função onde o web_scraping, de fato, é executado.
        - É aqui onde a função de requisição da página é chamada e, caso a página exista, as funções de scraping (no módudo scraping) também serão chamadas
    * Parâmetros:
        - num_lei: número da lei ao qual deseja-se buscar
        - num_artigo: número do artigo ao qual deseja-se buscar
        - num_paragrafo: número do parágrafo ao qual deseja-se buscar
        - num_inciso: número do inciso (em algarismos romanos) ao qual deseja-se buscar
        - letra_alinea: alínea ao qual deseja-se buscar
        - num_item: número do item ao qual deseja-se buscar
        
        OBS: dependendo da entrada do usuário, todos esses parâmetros podem chegar aqui vazios, por este motivo os tratamentos em relação a isso são feitos
    '''

    if(num_lei != ''):
        # Se o usuário digitou o número de uma lei, esta será buscada

        url = "http://www.planalto.gov.br/ccivil_03/leis/l" + str(num_lei) + ".htm"
        soup = getHtml(url)

        print('+------------------------------------------------------------------------------+')
        print('Resultado da sua consulta'.center(80))
        print('+------------------------------------------------------------------------------+')

        if soup:

            lei = scraping.findLei(soup)

            #Imprimindo o nome da lei
            scraping.printLine('Lei ' + num_lei + ': ', lei)

            if(num_artigo != ''):
                # Se o campo de artigo não estiver vazio, a busca será feita
                artigo = scraping.findArtigo(soup, num_artigo)

                if(artigo != -1):
                    # Significa que encontrei o artigo
                    scraping.printLine('\t', artigo)

                    if(num_paragrafo != ''):
                        # Se o campo de parágrafo não estiver vazio, a busca será feita dentro artigo

                        if(num_paragrafo == '0'):
                            # Buscando por um parágrafo único
                            paragrafo = scraping.findParagrafoUnico(artigo)

                            if(paragrafo != -1):
                                # Significa que encontrei o parágrafo único
                                scraping.printLine('\t\t', paragrafo)

                            else:
                                print('Opa, parágrafo único não encontrado!')
                        
                        else:
                            # Buscando por um parágrafo que não é único
                            paragrafo = scraping.findParagrafo(artigo, num_paragrafo)

                            if(paragrafo != -1):
                                # Significa que encontrei o parágrafo
                                scraping.printLine('\t\t', paragrafo)

                            else:
                                print('Opa, parágrafo não encontrado!')

                        if(paragrafo != -1 and num_inciso != ''):
                            # Se o parágrafo foi encontrado e o campo de inciso não está vazio, a busca por ele será feita dentro do parágrafo
                            inciso = scraping.findInciso(paragrafo, num_inciso)

                            if(inciso != -1):
                                # Significa que encontrei o inciso dentro do parágrafo
                                scraping.printLine('\t\t\t', inciso)

                                if(letra_alinea != ''):
                                    # Se o campo de alínea não estiver vazio, a busca por ela será feita dentro do inciso
                                    alinea = scraping.findAlinea(inciso, letra_alinea)

                                    if(alinea != -1):
                                        #Significa que encontrei a alínea dentro do inciso
                                        scraping.printLine('\t\t\t\t', alinea)

                                        if(num_item != ''):
                                            # Se o campo de item não estiver vazio, a busca por ele será feita dentro da alínea
                                            item = scraping.findItem(alinea, num_item)

                                            if(item != -1):
                                                #Significa que encontrei o item dentro da alína
                                                scraping.printLine('\t\t\t\t\t', item)

                                            else:
                                                print('Opa, item não encontrado!')

                                        #Se num_item == '', significa que não quero procurar itens dentro da alínea, apenas a alínea

                                    else:
                                        print('Opa, alínea não encontrada!')
                                    
                                # Se letra_alinea == '', significa que não quero procurar alíneas dentro do inciso, apenas o inciso

                            else:
                                print('Opa, inciso não encontrado!')

                        # Se num_inciso == '', significa que não quero procurar incisos dentro do parágrafo, apenas o parágrafo

                        elif(paragrafo != -1 and letra_alinea != ''):
                            # Se o parágrafo foi encontrado e o campo de alínea não está vazio, a busca por ela será feita dentro do parágrafo
                            alinea = scraping.findAlinea(paragrafo, letra_alinea)

                            if(alinea != -1):
                                #Significa que encontrei a alínea dentro do parágrafo
                                scraping.printLine('\t\t\t', alinea)

                                if(num_item != ''):
                                    # Se o campo de item não estiver vazio, a busca por ele será feita dentro da alínea
                                    item = scraping.findItem(alinea, num_item)

                                    if(item != -1):
                                        #Significa que encontrei o item dentro da alínea
                                        scraping.printLine('\t\t\t\t', item)

                                    else:
                                        print('Opa, item não encontrado!')

                                # Se num_item == '', significa que não quero procurar itens dentro da alínea, apenas a alínea

                            else:
                                print('Opa, alínea não encontrada!')

                    elif(num_inciso != ''):
                        # Se o campo de inciso não estiver vazio, a busca por ele será feita dentro do artigo
                        inciso = scraping.findInciso(artigo, num_inciso)

                        if(inciso != -1):
                            # Significa que encontrei o inciso dentro do artigo
                            scraping.printLine('\t\t', inciso)

                            if(letra_alinea != ''):
                                # Se o campo de alínea não estiver vazio, a busca por ela será feita dentro do inciso
                                alinea = scraping.findAlinea(inciso, letra_alinea)

                                if(alinea != -1):
                                    #Significa que encontrei a alínea dentro do inciso
                                    scraping.printLine('\t\t\t', alinea)

                                    if(num_item != ''):
                                        # Se o campo de item não estiver vazio, a busca por ele será feita dentro da alínea
                                        item = scraping.findItem(alinea, num_item)

                                        if(item != -1):
                                            #Significa que encontrei o item dentro da alínea
                                            scraping.printLine('\t\t\t\t', item)

                                        else:
                                            print('Opa, item não encontrado!')

                                    # Se num_item == '', significa que não quero procurar itens dentro da alínea, apenas a alínea

                                else:
                                    print('Opa, alínea não encontrada!')

                            # Se letra_alinea == '', significa que não quero procurar alíneas dentro do inciso, apenas o inciso

                        else:
                            print('Opa, inciso não encontrado!')

                    # Se num_inciso == '', significa que não quero procurar incisos ou parágrafos dentro do artigo, apenas o nome do artigo

                else:
                    print('Opa, artigo não encontrado!')

            # Se num_artigo == '', apenas o nome da lei será exibido

        else:
            print('Lei não encontrada!')

    else:
        print('+------------------------------------------------------------------------------+')
        print('Não foi possível processar sua consulta, você precisa digitar o número da lei ao qual deseja buscar!')