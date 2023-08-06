# Para calcular dias úteis Brasil, excluindo feriados nacionais e finais de semana.

from datetime import date, datetime

class Dia_util:
    def __init__(self):
        pass

    ano_atual = int(datetime.now().strftime('%Y'))
    dd = int(datetime.now().strftime('%d'))
    mm = int(datetime.now().strftime('%m'))
    yyyy = int(datetime.now().strftime('%Y'))
      
      
    def feriados_nacionais(self, ano= ano_atual, retorna=True):
        self.ano = int(ano)
        datas_arr = []
        datas_dict = {}
        self.calculo_pascoa()
        
        # Monta a data exata da Páscoa no Ano
        dtPA = date(ano, self.mes, self.dia)
        # Carnaval ocorre 47 dias antes da páscoa
        dtCN = date.fromordinal(dtPA.toordinal() - 47)
        # Corpus Christ ocorre 60 dias depois da páscoa
        dtCC = date.fromordinal(dtPA.toordinal() + 60)
        # Sexta-feira Santa ocorre 2 dias antes da páscoa
        dtSS = date.fromordinal(dtPA.toordinal() - 2)
        
        # Ano Novo
        dt_aux = f'01/01/{self.ano}'
        datas_arr.append(dt_aux)
        datas_dict.update({dt_aux : 'Confraternização - Ano Novo'})
        
        # Carnaval
        dt_aux = dtCN.strftime('%d/%m/%Y')
        datas_arr.append(dt_aux)
        datas_dict.update({dt_aux : 'Carnaval - facultativo'})
        
        # Sexta-feira Santa
        dt_aux = dtSS.strftime('%d/%m/%Y')
        datas_arr.append(dt_aux)
        datas_dict.update({dt_aux : 'Sexta-feira Santa'})
        
        # Pascoa
        dt_aux = dtPA.strftime('%d/%m/%Y')
        datas_arr.append(dt_aux)
        datas_dict.update({dt_aux : 'Pascoa'})
        
        # Tiradentes
        dt_aux = f'21/04/{self.ano}'
        datas_arr.append(dt_aux)
        datas_dict.update({dt_aux : 'Tiradentes'})
        
        # Dia do Trabalho
        dt_aux = f'01/05/{self.ano}'
        datas_arr.append(dt_aux)
        datas_dict.update({dt_aux : 'Dia do Trabalho'})
        
        # Corpus Christ
        dt_aux = dtCC.strftime('%d/%m/%Y')
        datas_arr.append(dt_aux)
        datas_dict.update({dt_aux : 'Corpus Christ - facultativo'})
        
        # 07 de Setembro - Independencia do Brasil
        dt_aux = f'07/09/{self.ano}'
        datas_arr.append(dt_aux)
        datas_dict.update({dt_aux : '07 Setembro - Independencia do Brasil'})
        
        # 12 de Outubro - Nossa Sra Aparecida
        dt_aux = f'12/10/{self.ano}'
        datas_arr.append(dt_aux)
        datas_dict.update({dt_aux : '12 de Outubro - Nossa Sra Aparecida'})
        
        # 02 de Novembro - Finados
        dt_aux = f'02/11/{self.ano}'
        datas_arr.append(dt_aux)
        datas_dict.update({dt_aux : '02 de Novembro - Finados'})
        
        # 15 de Novembro - Proclamação da República
        dt_aux = f'15/11/{self.ano}'
        datas_arr.append(dt_aux)
        datas_dict.update({dt_aux : '15 de Novembro - Proclamação da República'})
        
        # Natal
        dt_aux = f'25/12/{self.ano}'
        datas_arr.append(dt_aux)
        datas_dict.update({dt_aux : 'Natal'})
                   
        self.feriados = datas_arr
        if retorna:
            # Imprimir data e descrição
            for dt, descr in datas_dict.items():
                print(dt, descr)
                if 'Sexta-feira' in str(descr):
                    print()
            # return datas_dict
            return datas_arr
    
    
    
    def dias_uteis_mes(self, mes=mm, ano=yyyy, imprime=True):
        mes = int(mes)
        ano = int(ano)
        import calendar
        calc_dias = calendar.monthrange(ano, mes)
        total_dias_mes = calc_dias[1] 
        
        semana = [
            'Segunda-feira',
            'Terça-feira',
            'Quarta-feira',
            'Quinta-Feira',
            'Sexta-feira',
            'Sábado',
            'Domingo'
            ]
        
        self.feriados_nacionais(ano, False)
        feriados = self.feriados
        dias_uteis_br = []
        dias_uteis_us = []
        
        for x in range(1, total_dias_mes+1):
            dia_us = date(ano, mes, x)
            dia_br = str(x).zfill(2) + '/' + str(mes).zfill(2) + '/' + str(ano).zfill(4)
            indice_semana = dia_us.weekday()
            dia_da_semana = semana[indice_semana]
            if dia_da_semana != 'Sábado' and dia_da_semana != 'Domingo':
                if dia_br not in feriados:
                    if imprime:
                        print(dia_br, dia_da_semana)
                        if 'Sexta-feira' in str(dia_da_semana):
                            print()
                    dias_uteis_br.append(dia_br)
                    dias_uteis_us.append(str(ano).zfill(4) + '/' + str(mes).zfill(2) + '/' + str(x).zfill(2))
        
        # return dias_uteis_us
        return dias_uteis_br

    
    
    def hoje_eh_dia_util(self, dia=dd, mes=mm, ano=yyyy):
        hoje = str(dia).zfill(2) + '/' + str(mes).zfill(2) + '/' + str(ano).zfill(4)
        dias_uteis_br = self.dias_uteis_mes(mes, ano, False)
        print()
        print('hoje: ', hoje)
        if hoje in dias_uteis_br:
            print('OK - Hoje eh dia útil')
            util_day = True
        else:
            print('NAO - Hoje não eh dia útil')
            util_day = False
        return util_day
            


    def calculo_pascoa(self):
        p1 = (19 * (self.ano % 19) + 24) % 30
        p2 = (2 * (self.ano % 4) + 4 * (self.ano % 7) + 6 * p1 + 5) % 7
        res = p1 + p2
        if res > 9:
            self.dia = res - 9
            self.mes = 4
        else:
            self.dia = res + 22
            self.mes = 3


class imprima():
    
    def __init__(self):
        pass
    
    def data_de_hoje(self):
        hj = datetime.now().strftime('%d/%m/%Y')
        print('hoje', hj)
        return hj
    

########### como chamar e utilizar a classe ###################
# Dia_util = Dia_util()
# res = Dia_util.feriados_nacionais(2022)    
# res = Dia_util.dias_uteis_mes(11, 2022)
# res = Dia_util.hoje_eh_dia_util(25, 12, 2022)
# print(res)





