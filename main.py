import web_scraping


print('\n+------------------------------------------------------------------------------+')
print('WEB SCRAPING PARA CONSULTA DE LEIS'.center(80))
print('+------------------------------------------------------------------------------+')
print('Informe cada um dos campos necessários para a sua consulta.'.center(80))
print('No caso de um campo não ser necessário, apenas igore a entrada pressionando Enter.'.center(80))
print('+------------------------------------------------------------------------------+')

lei = input('Lei: ')
artigo = input('Artigo: ')
parag = input('Parágrafo (No caso de um parágrafo único, digite 0): ')
inciso = input('Inciso: ')
alinea = input('Alínea: ')
item = input('Item: ')

print('+------------------------------------------------------------------------------+')

print('\n' + 'Processando consulta...'.center(80) + '\n')

web_scraping.webScraping(lei, artigo, parag, inciso, alinea, item)
print('+------------------------------------------------------------------------------+\n')

#'9503', '167', '', 'II', '', ''