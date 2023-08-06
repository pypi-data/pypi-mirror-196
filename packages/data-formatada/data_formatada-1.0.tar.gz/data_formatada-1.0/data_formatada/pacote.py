from datetime import datetime
import abc

class DataFormatada(abc.ABC):
    """
    Uma classe voltada para trabalhar com datas/horas e suas peculiaridades

    ...

    Attributes
    ----------
   
    Methods
    -------
    data_hora(segundos=False):
        retorna uma string com a data e hora atuais
    hora():
        retorna uma string com a hora atual
    minutos():
        retorna uma string com os minutos atuais
    data():
        retorna uma string com a data atual
    dia():
        retorna uma string com o dia atual
    mes():
        retorna uma string com o mês atual
    ano():
        retorna uma string com o ano atual
    nome_mes(mes=None,abreviacao=False):
        retorna uma string com o nome do mês passado ou atual
    eh_bissexto(ano):
        retorna um booleano referente ao fato do ano ser ou não bissexto
    quantidade_dias_mes(bissexto=False):
        retorna uma lista com o total de dias de seu respectivo mês
    quantidade_dias(inicio,fim):
        retorna uma string com o total de dias contido entre duas datas
    """

    def data_hora(segundos=False):#pronta
        """
        Caso a função não receba parâmetro, a mesma retorna um string formatada com a data e hora atuais.
        ex: 02/03/2023 09:31
        Se receber um parâmetro True retorna a versão formatada incluindo segundos:
        ex: 02/03/2023 10:21:49.681464

            parameters:
                segundos {Bool} : boleano referente a retornar ou não os segundos

            return:
                {str} : Data no formato que o usuário definiu
        """
        data = str(datetime.now())
        if segundos == False:
            return f'{data[8:10]}/{data[5:7]}/{data[0:4]} {data[11:16]}'
        else:
            return f'{data[8:10]}/{data[5:7]}/{data[0:4]} {data[11::]}'

    def hora():#pronta
        """
        Retorna um string formatada com a hora atual.
        ex: 09:31    

            parameters:
                None

            return:
                {str} : Hora atual
        """
        data = str(datetime.now())
        return f'{data[11:16]}'

    def minutos():#pronta
        """
        Retorna um string formatada com os minutos atuais.
        ex: 27    

            parameters:
                None

            return:
                {str} : minutos atuais
        """
        data = str(datetime.now())
        return f'{data[14:16]}'

    def data():#pronta
        """
        Retorna um string formatada com a data atual.
        ex: 02/03/2023    

            parameters:
                None

            return:
                {str} : Data atual
        """
        data = str(datetime.now())
        return f'{data[8:10]}/{data[5:7]}/{data[0:4]}'

    def dia():#pronta
        """
        Retorna uma string com o dia atual.
        ex:02    

            parameters:
                None

            return:
                {str} : Dia atual
        """
        data = str(datetime.now())
        return f'{data[8:10]}'

    def mes():#pronto
        """
        Retorna um string com o mês atual.
        ex: 03    

            parameters:
                None

            return:
                {str} : Mês atual
        """
        data = str(datetime.now())
        return f'{data[5:7]}'

    def ano():#pronto
        """
        Retorna um string com o ano atual.
        ex: 2023    

            parameters:
                None

            return:
                {str} : Ano atual
        """
        data = str(datetime.now())
        return f'{data[0:4]}'

    def nome_mes(mes=None,abreviacao=False):#pronto
        """
        Retorna um string com o nome do mês ou sua abreviação
        se o mês não for passado como parâmetro, irá ser retornado o nome do mês atual
        se for passado o valor Booleano True para o parâmetro abrevicao, a função irá retornar o nome abreviado do respectivo mês 
        ex:09:31    

            parameters:
                mes {str} : Mês atual em formato de string ex: 01
                abreviacao {Bool} : Booleano referente ao tipo do retorno abreviado ou não 

            return:
                {str} : Nome completo ou abreviado de um determinado mês
        """
        if mes == None:
            data = str(datetime.now())
            mes = data[5:7]

        if mes == '01':
            if abreviacao == False:
                return 'Janeiro'
            else:
                return 'jan'
        elif mes == '02':
            if abreviacao == False:
                return 'Fevereiro'
            else:
                return 'fev'
        elif mes == '03':
            if abreviacao == False:
                return 'Março'
            else:
                return 'mar'
        elif mes == '04':
            if abreviacao == False:
                return 'Abril'
            else:
                return 'Abr'
        elif mes == '05':
            if abreviacao == False:
                return 'Maio'
            else:
                return 'maio'
        elif mes == '06':
            if abreviacao == False:
                return 'Junho'
            else:
                return 'jun'
        elif mes == '07':
            if abreviacao == False:
                return 'Julho'
            else:
                return 'jul'
        elif mes == '08':
            if abreviacao == False:
                return 'Agosto'
            else:
                return 'ago'
        elif mes == '09':
            if abreviacao == False:
                return 'Setembro'
            else:
                return 'set'
        elif mes == '10':
            if abreviacao == False:
                return 'Outubro'
            else:
                return 'out'
        elif mes == '11':
            if abreviacao == False:
                return 'Novembro'
            else:
                return 'nov'
        elif mes == '12':
            if abreviacao == False:
                return 'Dezembro'
            else:
                return 'dez'
        else:
            return 'ano invalido!'

    def eh_bissexto(ano):#pronto
        """
        Retorna um Booleano referente ao fato do ano passado como parâmetro ser ou não bissexto    

            parameters:
                ano {String} : Mês atual em formato de string ex: 2023

            return:
                {Bool} : Booleano referente ao fato do ano passado ser ou não bissexto.
        """
        ano = int(ano)
        if ano % 4 == 0:
            return True
        else:
            return False
    
    # esta função deve receber duas datas e retornar a quantidade de dias dentro do intervalo das datas

    def quantidade_dias_mes(bissexto=False):#pronto
        """
        Retorna uma lista de inteiros com os valores em dia de cada mês de um ano inteiro
        Se o parâmetro bissexto receber o valor True, o ano de fevereiro irá possuir valor inteiro de 29 
        

            parameters:
                bissexto {Bool} : Booleano referente ao tipo do retorno abreviado ou não 

            return:
                {list} : Lista com os valores em dia(inteiros) de todos os meses do ano
        """
        if bissexto == False:
            jan = 31
            fev = 28
            mar = 31
            Abr = 30
            maio = 31
            jun = 30
            jul = 31
            ago = 31
            set = 30
            out = 31
            nov = 30
            dez = 31
            return [jan,fev,mar,Abr,maio,jun,jul,ago,set,out,nov,dez]
        else:
            jan = 31
            fev = 29
            mar = 31
            Abr = 30
            maio= 31
            jun = 30
            jul = 31
            ago = 31
            set = 30
            out = 31
            nov = 30
            dez = 31

            return [jan,fev,mar,Abr,maio,jun,jul,ago,set,out,nov,dez]


    def quantidade_dias(inicio,fim): #pronto
        """
        Retorna uma string com a quantidade de dias dentro do intervalo aberto de duas datas
        ex: 
        inicio = 12/09/2021 
        fim = 15/10/2021
        retorno == '32'

            parameters:
                inicio {str} : String com a data do inicio do intervalo com separadores. Ex: 12/09/2021 
                fim {str} : String com a data do fim do intervalo com separadores. Ex: 15/10/2021
            return:
                {str} : String com a quantidade de dias dentro do intervalo passado
        """    
        #dados do ano inicio do intervalo
        dia_inicio = int(inicio[0:2])
        mes_inicio = int(inicio[3:5])
        ano_inicio = int(inicio[6::])
        #dados do ano fim do intervalo
        dia_fim = int(fim[0:2])
        mes_fim = int(fim[3:5])
        ano_fim = int(fim[6:10])

        

        if ano_inicio == ano_fim:

            if mes_inicio == mes_fim:#pronto
                #se o dia atual é menor que o dia final
                if dia_inicio < dia_fim:#pronto
                    #diferença de dias se calcula-> dia_final - dia_inicial - 1-> 15 - 12 -1 == 2 
                    # -1 é referente ao fato do intervalo ser aberto logo pegamos os das 13,14. Totalizando 2 dias
                    dif_dias = dia_fim - dia_inicio - 1

                    return f'{dif_dias}' #pronto
                elif dia_inicio == dia_fim:#pronto
                    return 'Erro: A data final é igual a data inicial.' #pronto

                else:#pronto
                    return 'Erro: A data final é menor que a data inicial.' #pronto

            elif mes_inicio < mes_fim:#pronta
                #criar um calendário baseado se o ano é bissexto ou não
                calendario = DataFormatada.quantidade_dias_mes(DataFormatada.eh_bissexto(ano_inicio))
                dias_restantes_mes_inicial = calendario[(mes_inicio-1)] - dia_inicio
                dias_necessarios_mes_final =  dia_fim

                #se houver apenas 1 mês de difernça
                if mes_fim - mes_inicio == 1:#pronta
                    return str(dias_restantes_mes_inicial + dias_necessarios_mes_final - 1)
                #se houver mais de 1 mês de diferença, precisamos descobrir quais são
                else:#pronta
                    total_dias = 0
                    for meses in range(mes_inicio,mes_fim+1):
                        total_dias += calendario[meses-1]

                    #funcionando, retorna o intervalo entre duas datas
                    return str(total_dias - dia_inicio - (calendario[mes_fim-1] - dias_necessarios_mes_final + 1))
         
            else:#pronta
                return 'Erro: A data final é menor que a data inicial'

        elif ano_inicio < ano_fim:#pronto
            """
            se ano_final - ano_inicial == 1:
                para resolver o caso de uma diferença de anos, preciso concluir o ano inicial e pegar apenas o necessário do ano final.
            se ano_final - ano_inicial > 1:
                pegamos o resultado anterior e somamos com o total de dias no intervalo de anos  
            """                
            if ano_fim - ano_inicio == 1:#pronto
               
                calendario = DataFormatada.quantidade_dias_mes(DataFormatada.eh_bissexto(ano_inicio))

                resto_mes_inicial = calendario[mes_inicio-1] - dia_inicio
                resto_ano_inicial = resto_mes_inicial + sum(calendario[mes_inicio:12])
                #######################################################################
                # -1 necessário para garantir o intervalo aberto 
                necessario_ano_final = 0
                if mes_fim == 1:
                    return str(resto_ano_inicial + dia_fim - 1)
                if mes_fim > 1:
                    #formular novo calendário testando se o ano final é ou não bissexto
                    calendario = DataFormatada.quantidade_dias_mes(DataFormatada.eh_bissexto(ano_fim))
                    necessario_ano_final = sum(calendario[0:mes_fim-1]) + (dia_fim-1)
                #testar se o retorno está correto
                return str(resto_ano_inicial + necessario_ano_final)
            
            elif ano_fim - ano_inicio > 1:
                """
                para encontrar a diferença útil, precisamos achar a difereça de anos e reduzir os anos que não pegaremos todos os dias
                formula: ano final - ano inicial - 1
                """
                dias_intervalo_intocado = 0
                for ano in range(ano_inicio+1,ano_fim):
                    if DataFormatada.eh_bissexto(ano):
                        dias_intervalo_intocado+=366
                    else:
                        dias_intervalo_intocado += 365

                calendario = DataFormatada.quantidade_dias_mes(DataFormatada.eh_bissexto(ano_inicio))

                resto_mes_inicial = calendario[mes_inicio-1] - dia_inicio
                resto_ano_inicial = resto_mes_inicial + sum(calendario[mes_inicio:12])
                
                necessario_ano_final = 0
                if mes_fim == 1:
                    return str(resto_ano_inicial + dia_fim - 1+ dias_intervalo_intocado)
                if mes_fim > 1:
                    #formular novo calendário testando se o ano final é ou não bissexto
                    calendario = DataFormatada.quantidade_dias_mes(DataFormatada.eh_bissexto(ano_fim))
                    necessario_ano_final = sum(calendario[0:mes_fim-1]) + (dia_fim-1)
                return str(resto_ano_inicial + necessario_ano_final+dias_intervalo_intocado)
  
        else:
            return 'Erro: A data final é menor que a data inicial'
