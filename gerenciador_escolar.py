import customtkinter as ctk
import json
import os

# =================== Funções de Dados =================== #

def carregar_dados(nome_arquivo):
    """Carrega dados de um arquivo JSON e retorna lista segura"""
    if os.path.exists(nome_arquivo):
        with open(nome_arquivo, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def salvar_dados(nome_arquivo, dados):
    """Salva dados no arquivo JSON"""
    with open(nome_arquivo, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)


# =================== Funções de Dados =================== #


def criar_secao_lancamento_notas(frame, alunos):
    notas = carregar_dados("notas.json")

    ctk.CTkLabel(frame, text="Lançamento de Notas (NP1, NP2, PIM)", font=("Arial", 18)).pack(pady=10)

    if alunos and isinstance(alunos[0], dict):
        nomes_alunos = [a.get("nome", "") for a in alunos if "nome" in a]
    else:
        nomes_alunos = alunos 

    aluno_var = ctk.StringVar()
    ctk.CTkLabel(frame, text="Selecione o aluno:").pack(pady=5)
    combo_alunos = ctk.CTkComboBox(frame, values=nomes_alunos, variable=aluno_var)
    combo_alunos.pack(pady=5)

    entradas = {}
    for campo in ["NP1", "NP2", "PIM"]:
        ctk.CTkLabel(frame, text=f"{campo}:").pack(pady=3)
        entradas[campo] = ctk.CTkEntry(frame)
        entradas[campo].pack(pady=3)

    mensagem = ctk.CTkLabel(frame, text="")
    mensagem.pack(pady=10)

    def salvar_notas():
        aluno = aluno_var.get()
        if aluno not in combo_alunos.cget("values"):
            mensagem.configure(text="Selecione um aluno válido.", text_color="red")
            return

        try:
            np1 = float(entradas["NP1"].get().strip())
            np2 = float(entradas["NP2"].get().strip())
            pim = float(entradas["PIM"].get().strip())
        except ValueError:
            mensagem.configure(text="Digite apenas números válidos.", text_color="red")
            return

        if not all(0 <= n <= 10 for n in [np1, np2, pim]):
            mensagem.configure(text="As notas devem estar entre 0 e 10.", text_color="red")
            return

        media = round((4 * np1 + 4 * np2 + 2 * pim) / 10, 2)
        situacao = "Aprovado" if media >= 7 else "Exame"

        registro = {
            "aluno": aluno,
            "np1": np1,
            "np2": np2,
            "pim": pim,
            "media": media,
            "situacao": situacao
        }

        for i, r in enumerate(notas):
            if r["aluno"] == aluno:
                notas[i] = registro
                break
        else:
            notas.append(registro)

        salvar_dados("notas.json", notas)
        mensagem.configure(
            text=f"Notas lançadas para {aluno} (Média: {media} - {situacao})",
            text_color="green"
        )

        for e in entradas.values():
            e.delete(0, ctk.END)

    ctk.CTkButton(frame, text="Salvar Notas", command=salvar_notas).pack(pady=10)
    

    def atualizar_alunos():
        novos_alunos = carregar_dados("alunos.json")
       
        if novos_alunos and isinstance(novos_alunos[0], dict):
            combo_alunos.configure(values=[a.get("nome", "") for a in novos_alunos])
        else:
            combo_alunos.configure(values=novos_alunos)
        mensagem.configure(text="Lista de alunos atualizada!", text_color="green")

    ctk.CTkButton(frame, text="Atualizar Lista de Alunos", command=atualizar_alunos).pack(pady=5)


# =================== TELA DE LOGIN =================== #


def tela_login():
    janela_login = ctk.CTk()
    janela_login.geometry("400x350")
    janela_login.title("Login")

    texto_login = ctk.CTkLabel(janela_login , text="Login" , font=("Ariar" , 24 , "bold"))
    texto_login.pack(pady=10)

    label_usuario = ctk.CTkLabel(janela_login, text="Usuário:")
    label_usuario.pack(pady=10)
    entrada_usuario = ctk.CTkEntry(janela_login)
    entrada_usuario.pack(pady=5)

    label_senha = ctk.CTkLabel(janela_login, text="Senha:")
    label_senha.pack(pady=10)
    entrada_senha = ctk.CTkEntry(janela_login, show="*")
    entrada_senha.pack(pady=5)

    mensagem = ctk.CTkLabel(janela_login, text="")
    mensagem.pack(pady=10)

    def logar():
        usuario = entrada_usuario.get().strip()
        senha = entrada_senha.get().strip()
        usuarios = carregar_dados("usuarios.json")

        for u in usuarios:
            if u["usuario"] == usuario and u["senha"] == senha:
                nivel = u.get("nivel", "Aluno")  # obtém o nível do usuário
                mensagem.configure(text="Login efetuado com sucesso!", text_color="green")
                janela_login.after(
                    1000,
                    lambda: [janela_login.destroy(), abrir_gerenciador_completo(usuario, nivel)]
                )
                return

        mensagem.configure(text="Usuário ou senha incorretos.", text_color="red")

    ctk.CTkButton(janela_login, text="Entrar", command=logar).pack(pady=10)
    janela_login.bind('<Return>', lambda event: logar())


    ctk.CTkButton(
        janela_login,
        text="Não tem cadastro? Clique aqui",
        fg_color="transparent",
        hover_color="#333333",
        text_color="lightblue",
        command=lambda: [janela_login.destroy(), tela_cadastro()]
    ).pack(pady=5)

    janela_login.mainloop()


# =================== TELA DE CADASTRO =================== #


def tela_cadastro():
    janela_cadastro = ctk.CTk()
    janela_cadastro.geometry("350x450")
    janela_cadastro.title("Cadastro de Usuário")

    texto_cadastro = ctk.CTkLabel(janela_cadastro , text="Cadastro" , font=("Ariar" , 24 , "bold"))
    texto_cadastro.pack(pady=10)

          # 🔹 Campo de seleção do nível
    texto_nivel = ctk.CTkLabel(janela_cadastro, text="Nível de acesso:")
    texto_nivel.pack(pady=10)
    nivel_var = ctk.StringVar(value="Aluno")
    campo_nivel = ctk.CTkComboBox(janela_cadastro, values=["Aluno", "Professor", "Administrador"], variable=nivel_var)
    campo_nivel.pack(pady=5)

    texto_usuario = ctk.CTkLabel(janela_cadastro, text="Usuário:")
    texto_usuario.pack(pady=10)
    campo_usuario = ctk.CTkEntry(janela_cadastro)
    campo_usuario.pack(pady=5)

    label_senha = ctk.CTkLabel(janela_cadastro, text="Senha:")
    label_senha.pack(pady=10)
    campo_senha = ctk.CTkEntry(janela_cadastro, show="*")
    campo_senha.pack(pady=5)

    mensagem = ctk.CTkLabel(janela_cadastro, text="")
    mensagem.pack(pady=10)

    def cadastrar():
        usuario = campo_usuario.get().strip()
        senha = campo_senha.get().strip()
        nivel = nivel_var.get()

        if not usuario or not senha:
            mensagem.configure(text="Preencha todos os campos.", text_color="red")
            return

        usuarios = carregar_dados("usuarios.json")
        if any(u["usuario"] == usuario for u in usuarios):
            mensagem.configure(text="Usuário já existe.", text_color="red")
            return

        usuarios.append({"usuario": usuario, "senha": senha, "nivel": nivel})
        salvar_dados("usuarios.json", usuarios)
        mensagem.configure(text="Cadastro realizado com sucesso!", text_color="green")
        janela_cadastro.after(1500, lambda: [janela_cadastro.destroy(), tela_login()])

    ctk.CTkButton(janela_cadastro, text="Cadastrar", command=cadastrar).pack(pady=10)
    janela_cadastro.bind('<Return>', lambda event: cadastrar())


    ctk.CTkButton(
        janela_cadastro,
        text="Já tem login? Clique aqui",
        fg_color="transparent",
        hover_color="#333333",
        text_color="lightblue",
        command=lambda: [janela_cadastro.destroy(), tela_login()]
    ).pack(pady=5)

    janela_cadastro.mainloop()


# =================== GERENCIADOR COMPLETO ===================


def abrir_gerenciador_completo(usuario_logado, nivel):
    print(f"Abrindo gerenciador para {usuario_logado} ({nivel})")

    janela = ctk.CTk()
    janela.geometry("750x620")
    janela.title(f"Gerenciador da Escola - {usuario_logado} ({nivel})")

    tabview = ctk.CTkTabview(janela, width=720, height=580)
    tabview.pack(pady=20, padx=20)


    # 🔹 Controle de acesso por nível

    if nivel == "Administrador":
        abas = ["Turmas", "Alunos", "Aulas", "Atividades", "Lançamento de Notas", "Notas", "Exames"]
    elif nivel == "Professor":
        abas = ["Aulas", "Alunos", "Atividades", "Lançamento de Notas", "Notas", "Exames"]
    else:  # Aluno
        abas = ["Notas"]

    # Cria as abas

    for a in abas:
        tabview.add(a)

    # Preenche as seções de acordo com o nível

    if "Turmas" in abas:
        turmas = carregar_dados("turmas.json")
        criar_secao_lista(tabview.tab("Turmas"), "turmas.json", "Nome da Turma", turmas, "Turma")

    if "Alunos" in abas:
        alunos = carregar_dados("alunos.json")
        criar_secao_lista(tabview.tab("Alunos"), "alunos.json", "Nome do Aluno", alunos, "Aluno")
    else:
        alunos = carregar_dados("alunos.json")

    if "Aulas" in abas:
        aulas = carregar_dados("aulas.json")
        criar_secao_lista(tabview.tab("Aulas"), "aulas.json", "Descrição da Aula", aulas, "Aula")

    if "Atividades" in abas:
        atividades = carregar_dados("atividades.json")
        criar_secao_lista(tabview.tab("Atividades"), "atividades.json", "Descrição da Atividade", atividades, "Atividade")

    if "Lançamento de Notas" in abas:
        criar_secao_lancamento_notas(tabview.tab("Lançamento de Notas"), alunos)

    if "Notas" in abas:
        criar_secao_resultado_notas(tabview.tab("Notas"))

    if "Exames" in abas:
        criar_secao_exame(tabview.tab("Exames"))

    print("Gerenciador carregado com sucesso!")
    janela.mainloop()




def criar_secao_exame(frame):

    """Aba Exames — permite digitar nota de exame e recalcular média final."""

    notas = carregar_dados("notas.json")
    alunos = carregar_dados("alunos.json")

    ctk.CTkLabel(frame, text="Lançar Nota de Exame", font=("Arial", 18)).pack(pady=10)

    # 🔹 Obter nomes dos alunos

    if alunos and isinstance(alunos[0], dict):
        nomes_alunos = [a.get("nome", "").strip() for a in alunos if "nome" in a]
    else:
        nomes_alunos = [str(a).strip() for a in alunos]

    aluno_var = ctk.StringVar()
    ctk.CTkLabel(frame, text="Selecione o aluno:").pack(pady=5)
    combo_alunos = ctk.CTkComboBox(frame, values=nomes_alunos, variable=aluno_var, width=250)
    combo_alunos.pack(pady=5)

    mensagem = ctk.CTkLabel(frame, text="")
    mensagem.pack(pady=5)

    ctk.CTkLabel(frame, text="Nota do Exame:").pack(pady=5)
    campo_exame = ctk.CTkEntry(frame)
    campo_exame.pack(pady=5)

    resultado_label = ctk.CTkLabel(frame, text="", font=("Arial", 14))
    resultado_label.pack(pady=10)

    def calcular_exame():
        aluno = aluno_var.get().strip()
        if not aluno:
            mensagem.configure(text="Selecione um aluno válido.", text_color="red")
            return

        try:
            nota_exame = float(campo_exame.get().strip())
        except ValueError:
            mensagem.configure(text="Digite um número válido para o exame.", text_color="red")
            return

        if not 0 <= nota_exame <= 10:
            mensagem.configure(text="A nota deve estar entre 0 e 10.", text_color="red")
            return

        notas = carregar_dados("notas.json")  # recarrega para garantir que está atualizado
        encontrado = False

        for r in notas:
            nome_registro = r.get("aluno", "").strip().lower()
            aluno_selecionado = aluno.strip().lower()
            if nome_registro == aluno_selecionado:
                antiga_media = r.get("media", 0)
                nova_media = round((antiga_media + nota_exame) / 2, 2)
                situacao_final = "Aprovado" if nova_media >= 5 else "Reprovado"


                # Atualiza os campos
                r["exame"] = nota_exame
                r["nova_media"] = nova_media
                r["situacao_final"] = situacao_final

                salvar_dados("notas.json", notas)
                resultado_label.configure(
                    text=f"Nova Média: {nova_media} - {situacao_final}",
                    text_color="green" if situacao_final == "Aprovado" else "red"
                )
                mensagem.configure(text=f"Nota de exame lançada para {aluno}.", text_color="green")
                campo_exame.delete(0, ctk.END)
                encontrado = True
                break

        if not encontrado:
            mensagem.configure(
                text=f"O aluno '{aluno}' ainda não tem notas lançadas na aba 'Lançamento de Notas'.",
                text_color="red"
            )


    ctk.CTkButton(frame, text="Calcular Nova Média", command=calcular_exame).pack(pady=10)

    # 🔁 Atualizar lista

    def atualizar_lista():
        novos_dados = carregar_dados("alunos.json")
        if novos_dados and isinstance(novos_dados[0], dict):
            novos_nomes = [a.get("nome", "").strip() for a in novos_dados if "nome" in a]
        else:
            novos_nomes = [str(a).strip() for a in novos_dados]
        combo_alunos.configure(values=novos_nomes)
        mensagem.configure(text="Lista de alunos atualizada!", text_color="green")

    ctk.CTkButton(frame, text="Atualizar Lista de Alunos", command=atualizar_lista).pack(pady=5)


# =================== COMPONENTES AUXILIARES ===================


def criar_secao_lista(frame, arquivo, placeholder, lista, tipo):
    label = ctk.CTkLabel(frame, text=f"Gerenciar {tipo}s", font=("Arial", 18))
    label.pack(pady=10)

    entrada = ctk.CTkEntry(frame, placeholder_text=placeholder)
    entrada.pack(pady=10)

    texto = ctk.CTkTextbox(frame, width=600, height=200)
    texto.pack(pady=10)
    texto.configure(state="disabled")

    mensagem = ctk.CTkLabel(frame, text="")
    mensagem.pack(pady=5)

    def atualizar():
        texto.configure(state="normal")
        texto.delete("0.0", ctk.END)
        if lista:
            for i, item in enumerate(lista, 1):
                texto.insert(ctk.END, f"{i}. {item}\n")
        else:
            texto.insert(ctk.END, f"Nenhum {tipo.lower()} cadastrado.")
        texto.configure(state="disabled")

    def adicionar():
        nome = entrada.get().strip()
        if nome:
            lista.append(nome)
            salvar_dados(arquivo, lista)
            atualizar()
            entrada.delete(0, ctk.END)
            mensagem.configure(text=f"{tipo} adicionado com sucesso!", text_color="green")
        else:
            mensagem.configure(text="Digite um nome válido.", text_color="red")

    ctk.CTkButton(frame, text=f"Adicionar {tipo}", command=adicionar).pack(pady=5)
    atualizar()


# =================== ABA LANÇAMENTO DE NOTAS ===================   


def criar_secao_resultado_notas(frame):
    texto = ctk.CTkTextbox(frame, width=650, height=400)
    texto.pack(pady=10)
    texto.configure(state="disabled")

    def atualizar_lista():
        notas = carregar_dados("notas.json")
        texto.configure(state="normal")
        texto.delete("0.0", ctk.END)
        if notas:
            for i, r in enumerate(notas, 1):
                exame = r.get("exame", "-")
                nova_media = r.get("nova_media", "-")
                # 🔹 Usa a situação final se existir, senão a inicial
                situacao = r.get("situacao_final", r.get("situacao", "-"))

                texto.insert(
                    ctk.END,
                    f"{i}. {r['aluno']} - NP1: {r['np1']} | NP2: {r['np2']} | PIM: {r['pim']} | "
                    f"Média: {r['media']} | Exame: {exame} | Nova Média: {nova_media} - Situação: {situacao}\n"
                )
        else:
            texto.insert(ctk.END, "Nenhuma nota lançada.")
        texto.configure(state="disabled")

    ctk.CTkLabel(frame, text="Resultados dos Alunos", font=("Arial", 18)).pack(pady=10)
    ctk.CTkButton(frame, text="Atualizar Lista", command=atualizar_lista).pack(pady=5)
    atualizar_lista()


# =================== EXECUÇÃO ===================


ctk.set_appearance_mode("dark")
tela_login()
