# Trabalho 8 - ADS - 2023 1o semestre
# Alunos: Guilherme Barbosa, Guilherme Mutão, João Floriano e Luciano Angelo

# Instalacao imports
# pip install numpy
# pip install csv

import random
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import csv


# Importação do arquivo csv
def importar_csv(file):
    # Lista para armazenar as tuplas de aulas
    global aulas
    aulas = []
    # nome_arquivo = 'dados/' + nome_arquivo

    # Abre o arquivo CSV e lê os dados
    with open(file, 'r') as file:
        csv_reader = csv.reader(file, delimiter=';')  # Define o separador como ponto e vírgula

        # Pula o cabeçalho (se houver)
        # next(csv_reader)

        # Itera pelas linhas do arquivo CSV
        for row in csv_reader:
            # Extrai os valores de cada coluna
            id_materia = int(row[0])
            semestre = int(row[1])
            qt_aulas = int(row[2])
            id_professor = int(row[3])
            materia = row[4]
            professor = row[5]

            # Cria a tupla de aula e adiciona à lista
            aula = (id_materia, semestre, qt_aulas, id_professor, materia, professor)
            aulas.append(aula)

    return aulas


def elitismo(populacao, adaptacao, num_individuos_elitismo):
    # Ordena os indivíduos de acordo com a sua adaptação (maior é melhor)
    indices_ordenados = np.argsort(adaptacao)[::-1]

    # Seleciona os melhores indivíduos
    individuos_elitismo = [populacao[i].copy() for i in indices_ordenados[:num_individuos_elitismo]]

    return individuos_elitismo


# Função principal do algoritmo genético
def algoritmo_genetico():

    populacao = [criar_individuo() for _ in range(POPULACAO_SIZE)]
    melhor_individuo = None
    melhor_aptidao = float("-inf")
    lista_aptidoes = []
    print('ag')

    for geracao in range(NUM_GERACOES - 1):
        print(geracao)
        aptidoes = [calcular_aptidao(individuo) for individuo in populacao]
        melhor_individuo_geracao = populacao[aptidoes.index(max(aptidoes))]
        melhor_aptidao_geracao = aptidoes.index(max(aptidoes))

        if melhor_aptidao_geracao > melhor_aptidao:
            melhor_individuo = melhor_individuo_geracao
            melhor_aptidao = melhor_aptidao_geracao


        filhos = []
        selecionados = []

        if SELECAO_METODO == "roleta":
            selecionados = selecao_roleta(populacao, aptidoes)

        if SELECAO_METODO == "torneio":
            selecionados = selecao_torneio(populacao, aptidoes, TORNEIO_SIZE)

        for i in range(0, len(selecionados), 2):
            individuo1 = selecionados[i]
            if i + 1 < len(selecionados):  # Verificar se ainda há elementos suficientes na lista
                individuo2 = selecionados[i + 1]
                if random.random() < TAXA_CRUZAMENTO:
                    filho1, filho2 = cruzamento(individuo1, individuo2)
                    filhos.append(filho1)
                    filhos.append(filho2)
                else:
                    filhos.append(individuo1)
                    filhos.append(individuo2)
            else:
                filhos.append(individuo1)

        filhos_mutados = [mutacao(filho, TAXA_MUTACAO) for filho in filhos]
        elite = elitismo(populacao, aptidoes, ELITISMO_SIZE)
        populacao = elite + filhos_mutados
        print("melhor_aptidao_geracao" + str(melhor_aptidao_geracao))
        print("geracao" + str(geracao))
        print("aptidao" + str(melhor_aptidao))
        lista_aptidoes.append(melhor_aptidao)
        update_grafico1(lista_aptidoes)

    return melhor_individuo, aptidoes


# Função para criar os individuos
def criar_individuo():
    # cria o array multidimensional
    individuo = np.zeros((NUM_PERIODO, len(DIAS), len(HORARIOS)), dtype=int)

    # percore a matriz AULAS
    for aula in AULAS:
        materia = aula[0]
        periodo = aula[1] - 1
        qt_aulas = aula[2]
        professor = aula[3]

        # percore as aulas da materia para alocar na matriz
        for _ in range(qt_aulas):
            dia = random.randint(0, len(DIAS) - 1)
            horario = random.randint(0, len(HORARIOS) - 1)
            valida_horario = False

            # verifica se a matriz tem algum valor
            if len(individuo) != 0 or np.all(individuo != None):

                # verifica se no periodo, dia e horario tem alguma materia ja alocada
                if individuo[periodo][dia][horario] > 0:
                    valida_horario = True

                # verifica se em outro periodo tem aula do mesmo professor ja alocada no mesmo horario
                # percore a matriz individuo
                for ind in individuo:
                    # percore a matriz AULAS
                    for aul in AULAS:
                        mt = int(aul[0])  # materia da aul
                        pe = int(aul[1] - 1)  # periodo da aul
                        pr = aul[3]  # professor da aul
                        # valida se a aula na posicao 3 (idProfessor) é igual ao professor e se o resuldado de ind é diferente da aula na posicao 0 (idMateria)
                        if pr == professor and individuo[pe][dia][horario] != materia:
                            # valida se ind na posicao do periodo da aula, dia e horario tem materia incluida
                            if individuo[pe][dia][horario] == mt:
                                valida_horario = True

                # enquanto o valida_horario nao cumprir as regras acima, continua a sortear dia e horario
                while valida_horario:
                    dia = random.randint(0, len(DIAS) - 1)
                    horario = random.randint(0, len(HORARIOS) - 1)
                    valida_horario = False

                    # verifica se no periodo, dia e horario tem alguma materia ja alocada
                    if individuo[periodo][dia][horario] > 0:
                        valida_horario = True

                    # verifica se em outro periodo tem aula do mesmo professor ja alocada no mesmo horario
                    # percore a matriz individuo
                    for ind in individuo:
                        # percore a matriz AULAS
                        for aula in AULAS:
                            # valida se a aula na posicao 3 (idProfessor) é igual ao professor e se o resuldado de ind é diferente da aula na posicao 0 (idMateria)
                            if pr == professor and individuo[pe][dia][horario] != materia:
                                # valida se ind na posicao do periodo da aula, dia e horario tem materia incluida
                                if individuo[pe][dia][horario] == mt:
                                    valida_horario = True
            # gera o individuo
            individuo[periodo][dia][horario] = materia

    return individuo


# Função de seleção por roleta
'''def selecao_roleta(populacao, aptidoes):
    total_aptidoes = sum(aptidoes)
    probs = [aptidao / total_aptidoes for aptidao in aptidoes]
    return random.choices(populacao, weights=probs)[0]'''


def selecao_roleta(populacao, aptidoes):
    total_aptidoes = sum(aptidoes)
    probs = [aptidao / total_aptidoes for aptidao in aptidoes]
    cum_probs = np.cumsum(probs)

    selecionados = []
    for _ in range(len(populacao)):
        rand = random.random()
        for i, cum_prob in enumerate(cum_probs):
            if rand <= cum_prob:
                selecionados.append(populacao[i])
                break

    return selecionados


# Função de seleção por torneio
def selecao_torneio(populacao, aptidoes, tamanho):
    selecionados = []
    for _ in range(len(populacao)):
        competidores = random.choices(list(range(len(populacao))), k=tamanho)
        vencedor = max(competidores, key=lambda i: aptidoes[i])
        selecionados.append(populacao[vencedor])
    return selecionados


# Função de cruzamento (recombinação)
def cruzamento(matriz1, matriz2):
    filho1 = matriz1.copy()
    filho2 = matriz2.copy()
    filho3 = matriz1.copy()

    for per in range(NUM_PERIODO):
        for dia in range(len(DIAS)):
            for hor in range(len(HORARIOS)):
                if np.random.rand() < 0.5:
                    filho3[per][dia][hor] = filho1[per][dia][hor]
                    filho1[per][dia][hor] = filho2[per][dia][hor]
                    filho2[per][dia][hor] = filho3[per][dia][hor]

    filho1 = corrigir_filho(filho1)
    filho2 = corrigir_filho(filho2)
    return filho1, filho2


# Função para corrigir aulas nos filhos
import numpy as np


def corrigir_filho(filho):
    elementos, contagens = np.unique(filho, return_counts=True)
    matriz_contagem = np.column_stack((elementos, contagens))

    for aula in aulas:
        mat = int(aula[0])
        per = int(aula[1] - 1)
        qtd = int(aula[2])
        professor = int(aula[3])
        temAula = False
        for aula_filho1 in matriz_contagem:
            mat_filho = int(aula_filho1[0])
            qtd_filho = int(aula_filho1[1])

            if mat_filho == mat:
                temAula = True

            if mat > 0 and mat_filho == mat and qtd_filho > qtd:  # corrigir materias do filho que tem mais aulas que a matriz aulas
                cont_aula = 0
                for per in range(NUM_PERIODO):
                    for dia in range(len(DIAS)):
                        for hor in range(len(HORARIOS)):
                            if cont_aula >= qtd and filho[per][dia][hor] == mat_filho:
                                filho[per][dia][hor] = 0
                            elif cont_aula < qtd and filho[per][dia][hor] == mat_filho:
                                cont_aula += 1

        for aula_filho2 in matriz_contagem:
            mat_filho = int(aula_filho2[0])
            qtd_filho = int(aula_filho2[1])

            if mat_filho == mat:
                temAula = True

            if mat > 0 and mat_filho == mat and qtd_filho < qtd:
                qt_aulas = (qtd - qtd_filho)
                # percore as aulas da materia para alocar na matriz
                for _ in range(qt_aulas):
                    for p in range(NUM_PERIODO):
                        if p == per:
                            cont = 0
                            for d in range(len(DIAS)):
                                for h in range(len(HORARIOS)):
                                    if cont == 0 and filho[p][d][h] == 0:
                                        filho[p][d][h] = mat_filho
                                        cont = 1

        if temAula == False:
            for _ in range(qtd):
                for pe in range(NUM_PERIODO):
                    if pe == per:
                        cont = 0
                        for di in range(len(DIAS)):
                            for ho in range(len(HORARIOS)):
                                if cont == 0 and filho[pe][di][ho] == 0:
                                    filho[pe][di][ho] = mat
                                    cont = 1

    return filho


# Função de mutação
def mutacao(individuo, taxa_mutacao):
    individuo_mutado = individuo.copy()

    for i in range(individuo_mutado.shape[0]):
        for j in range(individuo_mutado.shape[1]):
            if np.random.rand() < taxa_mutacao:
                horarios = individuo_mutado[i, j]
                np.random.shuffle(horarios)
                individuo_mutado[i, j] = horarios

    individuo_mutado = corrigir_filho(individuo_mutado)
    return individuo_mutado


# Função de aptidão
def calcular_aptidao(individuo):
    choques = contar_choques(individuo)
    aglutinacoes = contar_aglutinacoes(individuo)
    janelas = contar_janelas(individuo)
    # print(choques, ' | ', aglutinacoes, ' | ', janelas)
    x = aglutinacoes[2]
    y = aglutinacoes[3]
    z = aglutinacoes[4]

    aptidao = ((3 * x) + (50 * y) + (2000 * z)) - ((1000 * choques) + (50 * janelas))
    # print(aptidao)
    return aptidao


# Função para contar os choques de aulas em um indivíduo
def contar_choques(individuo):
    choques = 0
    for ind in individuo:
        for per in range(NUM_PERIODO):
            for dia in range(len(DIAS)):
                for hor in range(len(HORARIOS)):
                    if individuo[per][dia][hor] is not None or individuo[per][dia][hor] != 0:
                        ind_aula = individuo[per][dia][hor]
                        for aula in AULAS:
                            if ind_aula == aula[0]:
                                professor = aula[3]
                                for aul in AULAS:
                                    if aul[3] == professor:
                                        materia = aul[0]
                                        for periodo in range(NUM_PERIODO):
                                            for dia_sem in range(len(DIAS)):
                                                for horario in range(len(HORARIOS)):
                                                    if (
                                                            per != periodo and dia != dia_sem and hor != horario) and materia == \
                                                            individuo[periodo][dia_sem][
                                                                horario] and dia == dia_sem and hor == horario:
                                                        choques += 1
    return choques


# Função para contar as aglutinações de aulas em um indivíduo
def contar_aglutinacoes(individuo):
    aglutinacoes = {2: 0, 3: 0, 4: 0}
    materia_anterior = None
    aulas_consecutivas = 1

    for periodo in range(len(individuo)):
        for dia in range(len(individuo[periodo])):
            for horario in range(len(individuo[periodo][dia])):
                if materia_anterior is not None and individuo[periodo][dia][horario] == materia_anterior:
                    aulas_consecutivas += 1
                else:
                    if aulas_consecutivas >= 2 and aulas_consecutivas <= 4:
                        aglutinacoes[aulas_consecutivas] += 1
                    aulas_consecutivas = 1
                materia_anterior = individuo[periodo][dia][horario]
    return aglutinacoes


# Função para contar as janelas em um indivíduo
def contar_janelas(individuo):
    total_janelas = 0

    for periodo in individuo:
        for dia in periodo:
            aulas = []
            for horario in dia:
                if horario:  # Verificar se o horário possui uma matéria associada
                    aulas.append(horario)

            if len(aulas) > 1:
                for i in range(len(aulas) - 2):
                    if aulas[i] != aulas[i + 1] and aulas[i] == aulas[i + 2]:
                        total_janelas += 1

    return total_janelas


# Função para exibir a tabela da grade horária
def exibir_grade_horaria(individuo):
    tabela = []
    for dia in range(len(DIAS)):
        linha = [DIAS[dia]]
        for horario in range(len(HORARIOS)):
            aula_id = individuo[dia][horario]
            if np.any(aula_id == 0):  # Usar np.any() para verificar se algum elemento é igual a 0
                linha.append("Vago")
            else:
                aula = next(aula for aula in AULAS if np.any(aula[0] == aula_id))
                linha.append(f"{aula[4]} - {aula[5]}")
        tabela.append(linha)

    horarios_ordem = {horario: index for index, horario in enumerate(HORARIOS)}
    tabela_ordenada = sorted(tabela, key=lambda x: (x[0], horarios_ordem.get(x[1], len(HORARIOS))))
    return tabela_ordenada


def retorna_aula_professor(individuo):
    aula_professor = "VAGO"
    for aula in AULAS:
        if aula[0] == individuo:
            aula_professor = aula[4] + " - " + aula[5]
            break
    return aula_professor


def exibir_tabela_melhor_individuo(melhor_individuo):
    tabela = [
        ["Período", "Horários", "Segunda", "Terça", "Quarta", "Quinta", "Sexta"]
    ]

    for periodo in range(NUM_PERIODO):
        for horario in range(len(HORARIOS)):
            linha = [
                periodo + 1,
                HORARIOS[horario],
                retorna_aula_professor(melhor_individuo[periodo][0][horario]),
                retorna_aula_professor(melhor_individuo[periodo][1][horario]),
                retorna_aula_professor(melhor_individuo[periodo][2][horario]),
                retorna_aula_professor(melhor_individuo[periodo][3][horario]),
                retorna_aula_professor(melhor_individuo[periodo][4][horario])
            ]
            tabela.append(linha)
    sg.theme("LightGrey1")
    data = tabela[1:]
    layout = [[sg.Table(values=data, headings=tabela[0], alternating_row_color='#e5e5e5', auto_size_columns=True,
                        justification='center', size=(1100, 430))]]
    window = sg.Window("Melhor Indivíduo - Grade Horária", layout, size=(1100, 430))
    window.read()
    window.close()


# Função para exibir o gráfico de aptidão
def exibir_grafico_aptidao(aptidoes):
    geracoes = range(1, len(aptidoes) + 1)
    plt.plot(geracoes, aptidoes)
    plt.xlabel("Geração")
    plt.ylabel("Aptidão")
    plt.title("Evolução da Aptidão")
    plt.show()

def update_grafico1(aptidoes):
    print("teste")
    print(aptidoes)
    geracoes = list(range(1, len(aptidoes) + 1))
    fig1.clf()
    ax1 = fig1.add_subplot(1, 1, 1)
    ax1.plot(geracoes, aptidoes)
    ax1.set_ylabel('Aptidao', color='red')
    ax1.set_xlabel('Geração', color='red')
    ax1.axis('equal')

    figure_canvas_agg1.draw()
    figure_canvas_agg1.flush_events()
    window.refresh()


aptidao_maxima = []
AULAS = '';
POPULACAO_SIZE = ''
NUM_GERACOES = ''
TAXA_CRUZAMENTO = ''
TAXA_MUTACAO = ''
ELITISMO_SIZE = ''
SELECAO_METODO = "roleta"  # "roleta" ou "torneio"
TORNEIO_SIZE = ''
DIAS = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta']
HORARIOS = ['19:00', '19:50', '20:50', '21:40']


import PySimpleGUI as sg

# Definir o layout
layout = [
    [sg.Text("Gerador Automático de Grade - ADS", font=("Arial", 20))],
    [
        sg.Frame(
            "Parâmetros",
            [
                [
                    sg.Text("Arquivo CSV:"),
                    sg.Input(size=(30, 1), key="-FILE-", default_text="C:/Users/guilherme.rocha/PycharmProjects/genetico/dados/aulas.csv"),
                    sg.FileBrowse(),
                ],
                [
                    sg.Text("Dias da Semana:"),
                    sg.Checkbox("Domingo", key="-DOMINGO-", disabled=True),
                    sg.Checkbox("Segunda", key="-SEGUNDA-", disabled=True, default=True),
                    sg.Checkbox("Terça", key="-TERCA-", disabled=True, default=True),
                    sg.Checkbox("Quarta", key="-QUARTA-", disabled=True, default=True),
                    sg.Checkbox("Quinta", key="-QUINTA-", disabled=True, default=True),
                    sg.Checkbox("Sexta", key="-SEXTA-", disabled=True, default=True),
                    sg.Checkbox("Sábado", key="-SABADO-", disabled=True),
                ],

                [
                    sg.Text("Quantidade de Aulas/Dia:", size=(20, 1)),
                    sg.Input(size=(5, 1), key="-NUM_CLASSES-", default_text='4', disabled=True),
                    sg.Text(size=(2, 1)),

                    sg.Text("Duração de cada aula:", size=(20, 1)),
                    sg.Input(size=(5, 1), key="-DURACAO_AULA-", default_text='50', disabled=True),
                    sg.Text(size=(2, 1)),

                    sg.Text("Horário de inicio:", size=(20, 1)),
                    sg.Input(size=(5, 1), key="-INICIO_AULA-", default_text='19:00', disabled=True),
                ],
                [
                    sg.Text("Tamanho da População:", size=(20, 1)),
                    sg.Input(size=(5, 1), key="-POPULACAO_SIZE-", default_text='100'),
                    sg.Text(size=(2, 1)),

                    sg.Text("Número de Gerações:", size=(20, 1)),
                    sg.Input(size=(5, 1), key="-NUM_GERACOES-", default_text='200'),
                ],
                [
                    sg.Text("Taxa de Cruzamento:", size=(20, 1)),
                    sg.Input(size=(5, 1), key="-TAXA_CRUZAMENTO-", default_text='80'),
                    sg.Text(size=(2, 1)),

                    sg.Text("Taxa de Mutação:", size=(20, 1)),
                    sg.Input(size=(5, 1), key="-TAXA_MUTACAO-", default_text='50'), sg.Text("%"),
                ],
                [
                    sg.Text("Tamanho do Elitismo:", size=(20, 1)),
                    sg.Input(size=(5, 1), key="-ELITISMO_SIZE-", default_text='1'),
                    sg.Text(size=(2, 1)),

                    sg.Text("Seleção:", size=(20, 1)),
                    sg.Radio("Roleta", "SELECAO_METODO", enable_events=True, default=True, key="-ROLETA-"),
                    sg.Radio("Torneio", "SELECAO_METODO", enable_events=True, key="-TORNEIO-"),
                    sg.Input(
                        size=(5, 1), key="-TORNEIO_SIZE-", default_text='30', disabled=True
                    ),  # Campo desabilitado inicialmente
                ],
                [sg.Button("Reiniciar Dados"), sg.Button("Gerar Horário")],
            ],
            element_justification="left",
            expand_x=True,
            expand_y=True,
        ),
        sg.Frame(
            "Aptidão",
            [[sg.Canvas(size=(500, 400), key='-CANVAS1-')]],
            element_justification="center",
            expand_x=True,
            expand_y=True,

        ),
    ],
    [
        sg.Frame(
            "Grade de Horário",
            [
                [
                    sg.Table(
                        [[]] * 25,
                        headings=["Periodo", "Horários", "Segunda", "Terça", "Quarta", "Quinta", "Sexta"],
                        justification="center",
                        auto_size_columns=False,
                        num_rows=25,
                        col_widths=[20] * 7,
                        key="-SCHEDULE-",
                    )
                ]
            ],
            expand_x=True,
            expand_y=True,
        )
    ],
    [
        sg.Frame(
            "Desenvolvedores",
            [
                [
                    sg.Text("Desenvolvido por João, Luciano, Guilherme Barbosa e Guilherme Mutão"),
                    sg.Text(size=(10, 1)),
                    sg.Text("Professor: Zequinha"),
                    sg.Text(size=(50, 1)),
                    sg.Button("Fechar")],
            ],
            expand_x=True,
            expand_y=True,
        )
    ],
]
# Criar a janela
window = sg.Window("Sistema de Grade Automática", layout, size=(1200, 800), finalize=True)
sg.theme("LightGrey1")

fig1 = plt.figure(figsize=(4.5, 5))
figure_canvas_agg1 = FigureCanvasTkAgg(fig1, master=window['-CANVAS1-'].TKCanvas)
figure_canvas_agg1.draw()
figure_canvas_agg1.get_tk_widget().pack(side='top', fill='both', expand=1)

# Loop de eventos
while True:
    event, values = window.read()

    if event == '-TORNEIO-':
        window['-TORNEIO_SIZE-'].update(disabled=False, value='')
        TORNEIO_SIZE = values['-TORNEIO_SIZE-']
    elif event == '-ROLETA-':
        window['-TORNEIO_SIZE-'].update(disabled=True, value='')
        TORNEIO_SIZE = 0

    if event == sg.Button("Gerar Horário") or event == "Gerar Horário":
        NUM_GERACOES = int(values['-NUM_GERACOES-'])
        POPULACAO_SIZE = int(values['-POPULACAO_SIZE-'])
        TAXA_CRUZAMENTO = float(values['-TAXA_CRUZAMENTO-'])
        TAXA_MUTACAO = float(values['-TAXA_MUTACAO-'])
        ELITISMO_SIZE = int(values['-ELITISMO_SIZE-'])
        ROLETA = bool(values['-ROLETA-'])
        TORNEIO = bool(values['-TORNEIO-'])

        if TORNEIO:
            TORNEIO_SIZE = int(values['-TORNEIO_SIZE-'])

        DIAS = []
        if values['-DOMINGO-']:
            DIAS.append('Domingo')
        if values['-SEGUNDA-']:
            DIAS.append('Segunda')
        if values['-TERCA-']:
            DIAS.append('Terça')
        if values['-QUARTA-']:
            DIAS.append('Quarta')
        if values['-QUINTA-']:
            DIAS.append('Quinta')
        if values['-SEXTA-']:
            DIAS.append('Sexta')
        if values['-SABADO-']:
            DIAS.append('Sábado')
        FILE = values['-FILE-']

        # nome_arquivo = 'aulas.csv'
        AULAS = importar_csv(FILE)

        PERIODOS = set()
        for linha in AULAS:
            valor = linha[1]
            PERIODOS.add(valor)
        NUM_PERIODO = len(PERIODOS)

        # print(AULAS)

        melhor_individuo, aptidoes = algoritmo_genetico()
        # # melhor_individuo = criar_individuo()
        exibir_tabela_melhor_individuo(melhor_individuo)
        exibir_grafico_aptidao(aptidoes)
        update_grafico1(aptidoes)



    if event == sg.WINDOW_CLOSED or event == "Fechar":
        break

# Fechar a janela
window.close()
