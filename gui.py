import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk
import game_logic as gl
from math import sqrt

# Definições padrão
tamanho_matriz = 4
dificuldade = 0
tamanhos = [4, 9, 16]  # Adicionando tamanhos padrão globalmente

def validate_input(P):
    return P.isdigit() or P == ""

def set_dificuldade(nova_dificuldade):
    global dificuldade
    dificuldade = nova_dificuldade
    for btn in dificuldade_buttons:
        btn.config(bootstyle="secondary")
    if dificuldade < len(dificuldade_buttons):
        dificuldade_buttons[dificuldade].config(bootstyle="success")

def set_tamanho_matriz(novo_tamanho):
    global tamanho_matriz
    tamanho_matriz = novo_tamanho
    for btn in tamanho_buttons:
        btn.config(bootstyle="secondary")
    if novo_tamanho in tamanhos:
        tamanho_buttons[tamanhos.index(novo_tamanho)].config(bootstyle="success")

def ajustar_tamanho_janela(jogo_window):
    jogo_window.geometry("1920x1080")  # Ajusta o tamanho da janela para Full HD
    # Centraliza a janela no canto superior esquerdo da tela
    jogo_window.geometry(f"1920x1080+0+0")

def iniciar_jogo():
    global tamanho_matriz, dificuldade, root

    root.withdraw()
    
    jogo_window = tk.Toplevel(root)
    jogo_window.title("Sudoku")
    ajustar_tamanho_janela(jogo_window)  # Ajusta o tamanho da janela

    def fechar_jogo():
        jogo_window.destroy()
        root.deiconify()
    
    jogo_window.protocol("WM_DELETE_WINDOW", fechar_jogo)

    if tamanho_matriz not in tamanhos:
        tamanho_matriz = 4  # Valor padrão
    
    sudoku_matrix = gl.Gerar_sudoku(tamanho_matriz)
    
    nums_faltando = {
        0: int(tamanho_matriz ** 2 * 0.25),
        1: int(tamanho_matriz ** 2 * 0.5),
        2: int(tamanho_matriz ** 2 * 0.75)
    }
    gl.Remover_nums(sudoku_matrix, nums_faltando[dificuldade])

    entries = []
    validate_cmd = (jogo_window.register(validate_input), '%P')
    
    frame_sudoku = ttk.Frame(jogo_window)
    frame_sudoku.pack(expand=True, side='left', anchor='center')

    cell_size = 50  # Tamanho das células
    for i in range(tamanho_matriz):
        row_entries = []
        for j in range(tamanho_matriz):
            entry = ttk.Entry(frame_sudoku, width=2, justify='center', validate='key', validatecommand=validate_cmd)
            entry.grid(row=i, column=j, padx=4, pady=4, sticky='nsew')
            
            # Ajusta o tamanho das células
            frame_sudoku.grid_rowconfigure(i, weight=1)
            frame_sudoku.grid_columnconfigure(j, weight=1)
            
            if sudoku_matrix[i][j] != 0:
                entry.insert(0, str(sudoku_matrix[i][j]))
                entry.config(state='disabled', font=('Helvetica', 20, 'bold'), foreground='white')  # Fonte e cor dos números pré-preenchidos
            else:
                entry.config(font=('Helvetica', 20, 'bold'), foreground='lime')  # Fonte das células que serão preenchidas
            
            row_entries.append(entry)
        entries.append(row_entries)

    def verificar_sudoku(sudoku_matrix):
        tamanho = len(sudoku_matrix)
        numeros_validos = set(range(1, tamanho + 1))

        # Verificar linhas
        for row in sudoku_matrix:
            if set(row) != numeros_validos:
                return False

        # Verificar colunas
        for col in range(tamanho):
            coluna = [sudoku_matrix[row][col] for row in range(tamanho)]
            if set(coluna) != numeros_validos:
                return False

        # Verificar subgrades
        tamanho_subgrade = int(sqrt(tamanho))
        for i in range(0, tamanho, tamanho_subgrade):
            for j in range(0, tamanho, tamanho_subgrade):
                subgrade = []
                for r in range(tamanho_subgrade):
                    for c in range(tamanho_subgrade):
                        subgrade.append(sudoku_matrix[i + r][j + c])
                if set(subgrade) != numeros_validos:
                    return False

        return True

    def check_solution():
        try:
            user_matrix = []
            for i in range(tamanho_matriz):
                row = []
                for j in range(tamanho_matriz):
                    value = entries[i][j].get()
                    if value == "":
                        messagebox.showwarning("Verificação", "Existem células vazias no tabuleiro.")
                        return
                    row.append(int(value))
                user_matrix.append(row)
            
            if verificar_sudoku(user_matrix):
                messagebox.showinfo("Verificação", "Parabéns! Você conseguiu completar o Sudoku!")
                fechar_jogo()
            else:
                messagebox.showerror("Verificação", "A solução está incorreta. Tente novamente.")
        
        except ValueError:
            messagebox.showerror("Erro", "Entrada inválida. Certifique-se de que todas as células contêm números válidos.")

    def clear_board():
        for i in range(tamanho_matriz):
            for j in range(tamanho_matriz):
                if sudoku_matrix[i][j] == 0:
                    entries[i][j].config(state='normal')
                    entries[i][j].delete(0, tk.END)

    # Criar um frame para os botões
    button_frame = ttk.Frame(jogo_window)
    button_frame.pack(pady=5, side='right', anchor='center')

    # Adicionar botões ao frame
    check_button = ttk.Button(button_frame, text="Verificar", command=check_solution, width=30)
    check_button.grid(row=0, column=0, padx=150, pady=5)  # Alinha à esquerda

    clear_button = ttk.Button(button_frame, text="Limpar", command=clear_board, width=30)
    clear_button.grid(row=3, column=0, padx=150, pady=8)  # Alinha à direita

def voltar_ao_menu():
    global root
    root.deiconify()
    if janela_dificuldade:
        janela_dificuldade.destroy()

def mostrar_menu():
    global root

    if 'root' in globals() and root.winfo_exists():
        return
    
    root = ttk.Window(themename="superhero")
    root.title("Sudoku")
    root.geometry("400x400")  # Define o tamanho da janela

    ttk.Label(root, text="Sudoku", font=("Helvetica", 24)).pack(pady=10)
    ttk.Label(root, text="by: JBA", font=("Helvetica", 14)).pack(pady=5)

    ttk.Button(root, text="JOGAR", command=iniciar_jogo, bootstyle="success", width=20).pack(pady=10)
    ttk.Button(root, text="DIFICULDADE", command=lambda: dificuldade_menu(root), bootstyle="primary", width=20).pack(pady=10)
    ttk.Button(root, text="COMO JOGAR?", command=mostrar_instrucoes, bootstyle="warning", width=20).pack(pady=10)

    root.mainloop()

def dificuldade_menu(janela):
    global dificuldade_buttons, tamanho_buttons, tamanhos, janela_dificuldade

    janela_dificuldade = tk.Toplevel(janela)
    janela_dificuldade.title("Dificuldade")
    janela_dificuldade.geometry("400x400")  # Define o tamanho da janela
    
    janela_dificuldade.transient(janela)
    janela_dificuldade.grab_set()

    ttk.Label(janela_dificuldade, text="Escolha a Dificuldade e o Tamanho", font=("Helvetica", 16)).pack(pady=10)

    menu_frame = ttk.Frame(janela_dificuldade)
    menu_frame.pack(expand=True, pady=20)

    dificuldade_buttons = []
    tamanho_buttons = []

    dificuldade_frame = ttk.Frame(menu_frame)
    dificuldade_frame.grid(row=0, column=0, padx=10)

    dificuldades = ["Fácil", "Médio", "Difícil"]
    for i, nome in enumerate(dificuldades):
        btn = ttk.Button(dificuldade_frame, text=nome, command=lambda i=i: set_dificuldade(i), bootstyle="secondary", width=20)
        btn.pack(pady=5)
        dificuldade_buttons.append(btn)

    tamanho_frame = ttk.Frame(menu_frame)
    tamanho_frame.grid(row=0, column=1, padx=10)

    for tam in tamanhos:
        btn = ttk.Button(tamanho_frame, text=f"{tam}x{tam}", command=lambda tam=tam: set_tamanho_matriz(tam), bootstyle="secondary", width=20)
        btn.pack(pady=5)
        tamanho_buttons.append(btn)

    set_dificuldade(dificuldade)
    set_tamanho_matriz(tamanho_matriz)

    voltar_button = ttk.Button(janela_dificuldade, text="Voltar ao Menu", command=voltar_ao_menu, bootstyle="danger", width=20)
    voltar_button.pack(pady=10)

def mostrar_instrucoes():
    instrucoes_window = tk.Toplevel(root)
    instrucoes_window.title("Como Jogar")
    instrucoes_window.geometry("400x400")  # Define o tamanho da janela
    
    instrucoes_window.transient(root)
    instrucoes_window.grab_set()

    instrucoes_texto = (
        "Instruções para Jogar Sudoku:\n\n"
        "1. O Sudoku é um quebra-cabeça de números que deve ser preenchido em uma grade.\n"
        "2. Cada número deve aparecer apenas uma vez em cada linha, coluna e subgrade.\n"
        "3. O Sudoku está completo quando todas as regras são atendidas.\n"
        "4. Use os botões para verificar sua solução ou limpar o tabuleiro.\n"
        "5. Escolha a dificuldade e o tamanho no menu para diferentes desafios."
    )

    ttk.Label(instrucoes_window, text=instrucoes_texto, font=11, wraplength=350).pack(pady=20)

    voltar_button = ttk.Button(instrucoes_window, text="Voltar", command=instrucoes_window.destroy, bootstyle="danger", width=20)
    voltar_button.pack(pady=10)


