import re

def isInciso(string):
    # Nessa função eu uso uma expressão regular para verificar se os caracteres antes de um traço ou espaço são algarismos romanos representando uma seção
    # Pode acontecer isso: XX- ou isso XX – ou XX -

    string = string.split(' ')[0].strip()

    if string[-1] == '-':
        string = string.split('-')[0]

    return bool(re.search(r"^M{0,3}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})$",string))

def isAlinea(string):
    # Nessa função eu verifico se na string existe apenas um caractere antes do parêntese e se ele é um caractere do alfabeto
    string = string.split(')')[0].strip()
    return (len(string) == 1 and string.isalpha())

def isItem(string):
    # Nessa função eu verifico se na string existe um número antes do parêntese ou ponto ou traço
    # Um item pode ser 1) ou 1. ou 1 -
    string1 = string.split(')')[0].strip()
    string2 = string.split('.')[0].strip()
    string3 = string.split('-')[0].strip()
    return string1.isnumeric() or string2.isnumeric() or string3.isnumeric()

def isParagrafo(string):
    # Nessa função eu verifico se a primeira posição é um carcatere '§'
    return string.strip()[0] == '§'

def isParagrafoUnico(string):
    # Nessa função eu  verifico se 'Parágrafo único' faz parte dessos primeiros 20 caracteres da string
    return 'Parágrafo único.' in string.strip()[:20]

def isPenas(string):
    # Nessa função eu verifico se a string antes do caractere - se trata de 'Penas' de um artigo
    string = string.split('-')[0].strip()
    return string == 'Penas'

def isPenalidade(string):
    # Nessa função eu verifico se a string se refere à uma infração, penalidade ou medida administrativa
    string = string.split(' ')[0].strip()
    if(string == 'Infração' or string == 'Penalidade' or string == 'Medida'):
        return 1
    return 0

def findLei(soup):

    '''
    * Descrição:
        - Nessa função eu busco o nome da lei a partir da estruturação da página html fornecida pelo soup
    * Parâmetro:
        - soup: objeto da biblioteca Beautiful Soup, instaciado a partir da página html requisitada
    * Retorno:
        - Uma string contendo o nome da lei
    '''

    lei = soup.find_all('table')
    #lei = lei[-1].find_all('p')
    lei = lei[1].find_all('p')

    return lei[-1].get_text().strip()

def findArtigo(soup, num_artigo):

    '''
    * Descrição:
        - Nessa função eu busco um artigo específico dentro da página html, através do objeto soup
    * Parâmetros:
        - num_artigo: número do artigo que desejo buscar
        - soup: objeto da biblioteca Beautiful Soup, instaciado a partir da página html requisitada
    * Retorno:
        - se o artigo for encontrado: uma lista contendo o artigo e todos os elementos presentes nele, ou seja, todo o encadeamento
        - se o artigo não for encontrado: -1
    '''

    p = soup.find_all('p')

    art = []

    for i in range(len(p)):

        string = p[i].get_text().strip()

        if ('Art. ' + str(num_artigo) + '.') in string or \
            ('Art. ' + str(num_artigo) + 'º') in string or \
            ('Art . ' + str(num_artigo) + 'º') in string or \
            ('Art ' + str(num_artigo) + '.') in string or \
            ('Art . ' + str(num_artigo) + '.') in string or \
            ('Art. ' + str(num_artigo) + 'o') in string or \
            ('Art . ' + str(num_artigo) + 'o') in string:

            art.append(string)

            for j in range(i+1, len(p)):
                sub_string = p[j].get_text().strip()

                if(isParagrafo(sub_string) or isInciso(sub_string) or isAlinea(sub_string) or isParagrafoUnico(sub_string) or isPenas(sub_string) or isPenalidade(sub_string) or isItem(sub_string)):
                    art.append(sub_string)
                
                else:
                    break
            break

    if(len(art) > 0):
        return art
    else:
        return -1

def findParagrafo(artigo, num_parag):

    '''
    * Descrição:
        - Nessa função eu busco um parágrafo específico dentro de um artigo
    * Parâmetros:
        - artigo: lista contendo todas as linhas presentes no artigo (ex: parágrafos, incisos, alíneas, etc)
        - num_parag: número do parágrafo que desejo buscar
    * Retorno:
        - se o parágrafo for encontrado: uma lista contendo o parágrafo e todo os elementos dentro dele (ex: incisos, alíneas, etc, caso existam no parágrafo)
        - se o parágrafo não for encontrado: -1
    '''

    parag = []

    for i in range(len(artigo)):
        string = artigo[i].strip()

        if ('§ ' + str(num_parag) + 'º') in string or \
            ('§ ' + str(num_parag) + 'o') in string or \
            ('§ ' + str(num_parag) + '.') in string:
            parag.append(string)

            for j in range(i+1, len(artigo)):
                sub_string = artigo[j].strip()

                if(not isParagrafo(sub_string)):
                    parag.append(sub_string)
                
                else:
                    break
            break

    if(len(parag) > 0):
        return parag
    else:
        return -1

def findParagrafoUnico(artigo):

    '''
    * Descrição:
        - Nessa função eu busco um parágrafo único dentro de um artigo
    * Parâmetro:
        - artigo: lista contendo todas as linhas presentes no artigo (ex: parágrafos, incisos, alíneas, etc)
    * Retorno:
        - se o parágrafo único for encontrado: uma lista contendo o parágrafo único e todos os elementos presentes nele, ou seja, alíneas e itens, caso existam
        - se o parágrafo único não for encontrado: -1
    '''

    parag = []

    for i in range(len(artigo)):
        string = artigo[i].strip()

        if isParagrafoUnico(string):
            parag.append(string)

            for j in range(i+1, len(artigo)):
                sub_string = artigo[j].strip()

                if(isAlinea(sub_string) or isItem(sub_string)):
                    parag.append(sub_string)
                
                else:
                    break
            break

    if(len(parag) > 0):
        return parag
    else:
        return -1

def findInciso(lista, num_inciso):
    
    '''
    * Descrição:
        - Nessa função eu busco um inciso específico dentro de um artigo ou parágrafo, dependendo da consulta
    * Parâmetros:
        - lista: pode ser um artigo ou um parágrafo, dependendo do tipo de busca ao qual deve ser feita
        - num_inciso: número do inciso ao qual desejo buscar
    * Retorno:
        - se o inciso for encontrado: uma lista contendo o inciso e todos os elementos dentro dele, se existirem
        - se o inciso não for encontrado: -1
    '''

    inciso = []

    for i in range(len(lista)):
        string = lista[i].strip()

        if (isInciso(string)) and (string.split(' ')[0].strip() == str(num_inciso) or string.split('-')[0].strip() == str(num_inciso)):

            inciso.append(string)

            for j in range(i+1, len(lista)):
                sub_string = lista[j].strip()

                if(isAlinea(sub_string) or isPenas(sub_string) or isPenalidade(sub_string) or isItem(sub_string)):
                    inciso.append(sub_string)
                
                else:
                    break
            break

    if(len(inciso) > 0):
        return inciso
    else:
        return -1

def findAlinea(lista, letra_alinea):
    '''
    * Descrição:
        - Nessa função eu busco uma alínea específica dentro de um artigo, parágrafo, parágrafo único ou inciso
    * Parâmetros:
        - lista: pode ser um artigo, parágrafo, parágrafo único ou inciso, dependendo do tipo de busca ao qual deve ser feita
        - letra_alinea: letra que deve ser buscada
    * Retorno:
        - se a alínea for encontrada: uma lista contendo a alínea e todos os elementos dentro dela (ex: itens, infração, penalidade, penas, etc.), caso existam
        - se a alínea não for encontrada: -1
    '''

    alineas = []

    for i in range(len(lista)):
        string = lista[i].strip()

        if (isAlinea(string)) and (str(letra_alinea) in string.split(')')[0].strip()):

            alineas.append(string)

            for j in range(i+1, len(lista)):
                sub_string = lista[j].strip()

                if(isItem(sub_string) or isPenas(sub_string) or isPenalidade(sub_string)):
                    alineas.append(sub_string)
                
                else:
                    break
            break

    if(len(alineas) > 0):
        return alineas
    else:
        return -1

def findItem(lista, num_item):
    '''
    * Descrição:
        - Nessa função eu busco um item específico dentro de uma alínea
    * Parâmetros:
        - lista: pode ser um artigo, parágrafo, parágrafo único ou inciso, dependendo do tipo de busca ao qual deve ser feita
        - letra_alinea: letra que deve ser buscada
    * Retorno:
        - se o item for encontrado: uma string com o item
        - se o item não for encontrado: -1
    '''

    for i in range(len(lista)):
        string = lista[i].strip()

        if (isItem(string)) and (str(num_item) in string.split(' ')[0].strip()):

            return string

    return -1

def printLine(indent, line):

    '''
    * Descrição:
        - Essa função tem o objetivo de personalizar a impressão das linhas
        - Por exemplo, eu utilizo ela para que eu consiga printar corretamente uma única string (ex: item) ou uma lista (ex: um inciso que contém infração, penalidades e medidas administrativas)
        - Também utilizo essa função para, em cada linha, substituir \n por espaço, para que a saída fique mais organizada
        - Além disso, também utilizo essa função para conseguir indentar os prints de forma hierárquica, por exemplo:
            Lei:
                Artigo:
                    Parágrafo:
                        Inciso:
                            Alínea:
                                Item:
    * Parâmetros:
        - indent: refere-se ao recuo que deve ser feito no print ou qualquer outra string que eu queira inserir antes de mostrar a linha
        - line: linha que eu desejo exibir no print, pode ser um item, um artigo, um inciso, um parágrafo, o nome de uma lei, etc.
    '''

    if(isinstance(line, list)):

        #Preciso mostrar a primeira posição da lista, que é a descrição do artigo/parágrafo/inciso/alínea/item
        print(indent + line[0].replace('\n', ' '))

        #Também preciso mostrar quando aparecem as palavras "PENAS", Infração", "Penalidade" e "Medida administrativa"
        for item in line[1:]:

            if(isParagrafo(item) or isInciso(item) or isAlinea(item) or isItem(item) or isParagrafoUnico(item)):
                break

            print(indent + item.replace('\n', ' '))

    else:
        print(indent + line.replace('\n', ' '))