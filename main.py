import customtkinter as ctk
from PIL import Image, ImageTk
import requests
from io import BytesIO
import mysql.connector
from datetime import datetime
from dotenv import load_dotenv
import os
from modules.moedas import CurrencyConverter

# Carrega variáveis de ambiente
load_dotenv()

class SecondBrainApp:
    def __init__(self):
        # Configuração inicial
        self.root = ctk.CTk()
        self.root.title("Segundo Cérebro - Dashboard Completo")
        self.root.geometry("1000x700")
        
        # Configuração do tema
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Conexão com o banco de dados
        self.db_connection = self.create_db_connection()
        
        self.currency_converter = CurrencyConverter()  # Esta linha deve existir
        self.setup_ui()

        # Interface principal
        self.setup_ui()
        
        # Dados iniciais
        self.current_city = None
        self.last_updates = {
            'clima': None,
            'tarefas': None,
            'investimentos': None,
            'moedas': None
        }

    def create_db_connection(self):
        """Cria conexão com o MySQL"""
        try:
            return mysql.connector.connect(
                host=os.getenv('DB_HOST'),
                user=os.getenv('DB_USER'),
                password=os.getenv('DB_PASSWORD'),
                database=os.getenv('DB_NAME')
            )
        except Exception as e:
            print(f"Erro ao conectar ao banco: {e}")
            return None

    def setup_ui(self):
        """Configura a interface principal"""
        # Tabview (Abas principais)
        self.tabview = ctk.CTkTabview(self.root)
        self.tabview.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Adiciona as abas
        self.tabview.add("Clima")
        self.tabview.add("Tarefas")
        self.tabview.add("Investimentos")
        self.tabview.add("Moedas")
        
        # Configura cada aba
        self.setup_clima_tab()
        self.setup_tarefas_tab()
        self.setup_investimentos_tab()
        self.setup_moedas_tab()
        
        # Status bar
        self.status_bar = ctk.CTkLabel(
            self.root,
            text="Sistema iniciado | Banco de dados: " + 
                 ("Conectado" if self.db_connection else "Desconectado"),
            font=("Arial", 10)
        )
        self.status_bar.pack(side="bottom", fill="x", pady=5)

    # ================== ABA CLIMA ==================
    def setup_clima_tab(self):
        """Configura a aba de clima"""
        tab = self.tabview.tab("Clima")
        
        # Frame de entrada
        input_frame = ctk.CTkFrame(tab)
        input_frame.pack(pady=10, fill="x")
        
        self.clima_entry = ctk.CTkEntry(
            input_frame,
            placeholder_text="Digite uma cidade...",
            width=300
        )
        self.clima_entry.pack(side="left", padx=5)
        
        ctk.CTkButton(
            input_frame,
            text="Buscar",
            command=self.update_weather
        ).pack(side="left")
        
        # Display do clima
        self.weather_display = ctk.CTkFrame(tab)
        self.weather_display.pack(fill="both", expand=True, pady=10)
        
        # Colunas
        left_col = ctk.CTkFrame(self.weather_display)
        left_col.pack(side="left", fill="y", padx=10)
        
        right_col = ctk.CTkFrame(self.weather_display)
        right_col.pack(side="right", fill="both", expand=True, padx=10)
        
        # Ícone do clima
        self.weather_icon = ctk.CTkLabel(left_col, text="🌤️", font=("Arial", 80))
        self.weather_icon.pack(pady=20)
        
        # Dados climáticos
        self.weather_info = ctk.CTkLabel(
            right_col,
            text="Informações climáticas aparecerão aqui...",
            font=("Arial", 14),
            justify="left",
            wraplength=400
        )
        self.weather_info.pack(anchor="w", pady=20)
        
        # Detalhes extras
        self.weather_details = ctk.CTkLabel(
            right_col,
            text="",
            font=("Arial", 12),
            justify="left"
        )
        self.weather_details.pack(anchor="w")

    def update_weather(self):
        """Atualiza os dados climáticos"""
        city = self.clima_entry.get().strip()
        if not city:
            self.weather_info.configure(text="Digite uma cidade válida", text_color="red")
            return
        
        try:
            # Simulação de dados - substitua pela sua API real
            weather_data = {
                'cidade': city,
                'temperatura': 25.3,
                'descricao': "Céu limpo",
                'umidade': 65,
                'vento': 12.4,
                'nascer_do_sol': "06:15",
                'por_do_sol': "18:45",
                'icone': "01d"
            }
            
            # Atualiza UI
            self.display_weather_data(weather_data)
            self.last_updates['clima'] = datetime.now().strftime("%H:%M:%S")
            self.update_status_bar()
            
        except Exception as e:
            self.weather_info.configure(text=f"Erro: {str(e)}", text_color="red")

    def display_weather_data(self, data):
        """Exibe os dados climáticos na interface"""
        # Atualiza ícone
        self.update_weather_icon(data.get('icone', ''))
        
        # Informações principais
        main_info = (
            f"📍 {data.get('cidade', 'N/A')}\n"
            f"🌡 {data.get('temperatura', 'N/A')}°C | "
            f"💧 {data.get('umidade', 'N/A')}%\n"
            f"🌬 {data.get('vento', 'N/A')} m/s\n"
            f"📌 {data.get('descricao', 'N/A')}"
        )
        self.weather_info.configure(text=main_info, text_color="white")
        
        # Detalhes extras
        details = (
            f"🌅 Nascer do sol: {data.get('nascer_do_sol', 'N/A')}\n"
            f"🌇 Pôr do sol: {data.get('por_do_sol', 'N/A')}"
        )
        self.weather_details.configure(text=details)

    def update_weather_icon(self, icon_code):
        """Atualiza o ícone do clima"""
        # Implemente o carregamento real de ícones aqui
        self.weather_icon.configure(text="🌤️")

    # ================== ABA TAREFAS ==================
    def setup_tarefas_tab(self):
        """Configura a aba de tarefas"""
        tab = self.tabview.tab("Tarefas")
        
        # Frame de entrada
        input_frame = ctk.CTkFrame(tab)
        input_frame.pack(pady=10, fill="x")
        
        self.tarefa_entry = ctk.CTkEntry(
            input_frame,
            placeholder_text="Nova tarefa...",
            width=300
        )
        self.tarefa_entry.pack(side="left", padx=5)
        
        ctk.CTkButton(
            input_frame,
            text="Adicionar",
            command=self.add_task
        ).pack(side="left")
        
        # Lista de tarefas
        self.tasks_frame = ctk.CTkScrollableFrame(tab)
        self.tasks_frame.pack(fill="both", expand=True, pady=10)
        
        # Carrega tarefas iniciais
        self.load_tasks()

    def add_task(self):
        """Adiciona uma nova tarefa"""
        task_text = self.tarefa_entry.get().strip()
        if not task_text:
            return
        
        # Aqui você implementaria a lógica para salvar no banco de dados
        print(f"Tarefa adicionada: {task_text}")
        self.tarefa_entry.delete(0, "end")
        self.load_tasks()

    def load_tasks(self):
        """Carrega as tarefas do banco de dados"""
        # Limpa tarefas existentes
        for widget in self.tasks_frame.winfo_children():
            widget.destroy()
        
        # Simulação de dados - substitua pelo seu código real
        sample_tasks = [
            {"id": 1, "texto": "Reunião com equipe", "concluida": False},
            {"id": 2, "texto": "Fazer compras", "concluida": True},
            {"id": 3, "texto": "Estudar Python", "concluida": False}
        ]
        
        for task in sample_tasks:
            self.create_task_widget(task)

    def create_task_widget(self, task):
        """Cria um widget de tarefa na interface"""
        frame = ctk.CTkFrame(self.tasks_frame)
        frame.pack(fill="x", pady=2)
        
        # Checkbox
        ctk.CTkCheckBox(
            frame,
            text="",
            width=30,
            command=lambda: self.toggle_task(task['id'])
        ).pack(side="left", padx=5)
        
        # Texto da tarefa
        task_text = ctk.CTkLabel(
            frame,
            text=task['texto'],
            font=("Arial", 12),
            wraplength=600
        )
        task_text.pack(side="left", fill="x", expand=True, padx=5)
        
        # Botão de exclusão
        ctk.CTkButton(
            frame,
            text="✕",
            width=30,
            fg_color="transparent",
            hover_color="#ff4444",
            command=lambda: self.delete_task(task['id'])
        ).pack(side="right", padx=5)
        
        # Estilo para tarefas concluídas
        if task['concluida']:
            task_text.configure(text_color="#aaaaaa")

    def toggle_task(self, task_id):
        """Alterna o status da tarefa"""
        print(f"Alternando tarefa {task_id}")
        self.load_tasks()

    def delete_task(self, task_id):
        """Remove uma tarefa"""
        print(f"Removendo tarefa {task_id}")
        self.load_tasks()

    # ================== ABA INVESTIMENTOS ==================
    def setup_investimentos_tab(self):
        """Configura a aba de investimentos"""
        tab = self.tabview.tab("Investimentos")
        
        # Frame de entrada
        input_frame = ctk.CTkFrame(tab)
        input_frame.pack(pady=10, fill="x")
        
        # Campos de entrada
        ctk.CTkLabel(input_frame, text="Ativo:").pack(side="left", padx=5)
        self.ativo_entry = ctk.CTkEntry(input_frame, width=100)
        self.ativo_entry.pack(side="left", padx=5)
        
        ctk.CTkLabel(input_frame, text="Valor:").pack(side="left", padx=5)
        self.valor_entry = ctk.CTkEntry(input_frame, width=100)
        self.valor_entry.pack(side="left", padx=5)
        
        ctk.CTkButton(
            input_frame,
            text="Adicionar",
            command=self.add_investment
        ).pack(side="left", padx=10)
        
        # Gráfico e lista
        self.investments_frame = ctk.CTkFrame(tab)
        self.investments_frame.pack(fill="both", expand=True, pady=10)
        
        # Placeholder para o gráfico
        ctk.CTkLabel(
            self.investments_frame,
            text="Gráfico de Investimentos (será implementado)",
            font=("Arial", 14)
        ).pack(pady=50)
        
        # Lista de investimentos
        self.load_investments()

    def add_investment(self):
        """Adiciona um novo investimento"""
        ativo = self.ativo_entry.get().strip()
        valor = self.valor_entry.get().strip()
        
        if not ativo or not valor:
            return
        
        # Aqui você implementaria a lógica para salvar no banco de dados
        print(f"Investimento adicionado: {ativo} - R${valor}")
        self.ativo_entry.delete(0, "end")
        self.valor_entry.delete(0, "end")
        self.load_investments()

    def load_investments(self):
        """Carrega os investimentos do banco de dados"""
        # Simulação de dados
        sample_data = [
            {"id": 1, "ativo": "PETR4", "valor": 1500.00},
            {"id": 2, "ativo": "BTC", "valor": 3200.50},
            {"id": 3, "ativo": "IVVB11", "valor": 245.75}
        ]
        
        # Aqui você implementaria a exibição real dos dados

    # ================== ABA MOEDAS ==================
    def setup_moedas_tab(self):

        """Configura a aba de conversão de moedas"""
        tab = self.tabview.tab("Moedas")
    
    # Frame de conversão
        conversion_frame = ctk.CTkFrame(tab)
        conversion_frame.pack(pady=20, padx=20, fill="x")
    
    # Entrada de valor
        ctk.CTkLabel(conversion_frame, text="Valor:").pack(side="left")
        self.amount_entry = ctk.CTkEntry(conversion_frame, width=100)
        self.amount_entry.pack(side="left", padx=5)
    
    # Moeda de origem
        self.from_currency = ctk.CTkComboBox(
        conversion_frame,
        values=["USD", "EUR", "GBP", "BRL", "JPY", "CAD", "AUD", "CHF"],
        width=70
    )
        self.from_currency.set("USD")
        self.from_currency.pack(side="left", padx=5)
    
    # Para
        ctk.CTkLabel(conversion_frame, text="→").pack(side="left", padx=5)
    
    # Moeda de destino
        self.to_currency = ctk.CTkComboBox(
        conversion_frame,
        values=["USD", "EUR", "GBP", "BRL", "JPY", "CAD", "AUD", "CHF"],
        width=70
    )
        self.to_currency.set("BRL")
        self.to_currency.pack(side="left", padx=5)
    
    # Botão de conversão
        ctk.CTkButton(
        conversion_frame,
        text="Converter",
        command=self.convert_currency).pack(side="left", padx=10)
    
    # Resultado
        self.conversion_result = ctk.CTkLabel(
        tab,
        text="Digite um valor e selecione as moedas",
        font=("Arial", 16, "bold")
    )
        self.conversion_result.pack(pady=10)
    
    # Frame do histórico
        history_frame = ctk.CTkFrame(tab)
        history_frame.pack(fill="both", expand=True, padx=20, pady=10)
    
        ctk.CTkLabel(
        history_frame,
        text="Últimas Conversões",
        font=("Arial", 14, "bold")
        ).pack(pady=5)
    
        self.history_table = ctk.CTkScrollableFrame(history_frame, height=150)
        self.history_table.pack(fill="both", expand=True)
    
    # Carrega histórico inicial
        self.load_conversion_history()

def convert_currency(self):
    """Realiza a conversão de moedas"""
    try:
        # Obtém os valores da interface
        amount = float(self.amount_entry.get())
        from_curr = self.from_currency.get()
        to_curr = self.to_currency.get()
        
        if amount <= 0:
            raise ValueError("O valor deve ser positivo")
            
        # Realiza a conversão
        result = self.currency_converter.convert_currency(amount, from_curr, to_curr)
        
        if "error" in result:
            self.conversion_result.configure(
                text=f"Erro: {result['error']}",
                text_color="red"
            )
        else:
            # Formata o resultado
            formatted_result = (
                f"{result['original_amount']:.2f} {result['from_currency']} = "
                f"{result['converted_amount']:.2f} {result['to_currency']}\n"
                f"Taxa: 1 {result['from_currency']} = {result['rate']:.6f} {result['to_currency']}"
            )
            self.conversion_result.configure(
                text=formatted_result,
                text_color="white"
            )
            
    except ValueError as e:
        self.conversion_result.configure(
            text=f"Erro: {str(e)}",
            text_color="red"
        )
    except Exception as e:
        self.conversion_result.configure(
            text=f"Erro inesperado: {str(e)}",
            text_color="red"
        )

def load_conversion_history(self):
    """Carrega o histórico de conversões"""
    # Limpa a tabela atual
    for widget in self.history_table.winfo_children():
        widget.destroy()
    
    # Obtém os dados
    history = self.currency_converter.get_conversion_history(limit=5)
    
    if not history:
        ctk.CTkLabel(
            self.history_table,
            text="Nenhuma conversão registrada ainda",
            text_color="gray"
        ).pack()
        return
    
    # Cabeçalho
    header_frame = ctk.CTkFrame(self.history_table)
    header_frame.pack(fill="x")
    
    headers = ["Data", "De", "Para", "Valor", "Resultado"]
    for i, header in enumerate(headers):
        ctk.CTkLabel(
            header_frame,
            text=header,
            font=("Arial", 12, "bold"),
            width=100 if i > 0 else 120
        ).pack(side="left", padx=2)
    
    # Dados
    for item in history:
        row_frame = ctk.CTkFrame(self.history_table)
        row_frame.pack(fill="x", pady=1)
        
        # Formata a data
        conv_date = item['data_conversao'].strftime("%d/%m %H:%M")
        
        # Adiciona as colunas
        columns = [
            conv_date,
            item['moeda_origem'],
            item['moeda_destino'],
            f"{item['valor_origem']:.2f}",
            f"{item['valor_convertido']:.2f}"
        ]
        
        for i, col in enumerate(columns):
            ctk.CTkLabel(
                row_frame,
                text=col,
                width=100 if i > 0 else 120
            ).pack(side="left", padx=2)

    # ================== FUNÇÕES GERAIS ==================
    def update_status_bar(self):
        """Atualiza a barra de status"""
        status_text = "Status: "
        status_text += f"Clima: {self.last_updates['clima'] or 'N/A'} | "
        status_text += f"Tarefas: {self.last_updates['tarefas'] or 'N/A'} | "
        status_text += f"Banco: {'Conectado' if self.db_connection else 'Desconectado'}"
        
        self.status_bar.configure(text=status_text)

    def run(self):
        """Inicia a aplicação"""
        self.root.mainloop()

if __name__ == "__main__":
    app = SecondBrainApp()
    app.run()