import customtkinter as ctk
from modules.clima import get_weather
from PIL import Image, ImageTk
import requests
from io import BytesIO
import os
from datetime import datetime

class WeatherApp:
    def __init__(self):
        # Configuração inicial da janela
        self.root = ctk.CTk()
        self.root.title("Segundo Cérebro - Dashboard Climático")
        self.root.geometry("600x500")
        self.root.minsize(500, 450)
        
        # Configuração do tema
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Layout principal
        self.setup_ui()
        
        # Variáveis de estado
        self.last_update = None
        self.current_city = None

    def setup_ui(self):
        """Configura todos os elementos da interface"""
        # Frame principal
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        # Cabeçalho
        self.header = ctk.CTkLabel(
            self.main_frame,
            text="Informações Climáticas",
            font=("Arial", 18, "bold")
        )
        self.header.pack(pady=(10, 20))
        
        # Entrada de cidade
        self.city_frame = ctk.CTkFrame(self.main_frame)
        self.city_frame.pack(fill="x", padx=50)
        
        self.entry_city = ctk.CTkEntry(
            self.city_frame,
            placeholder_text="Digite uma cidade...",
            width=250
        )
        self.entry_city.pack(side="left", expand=True, fill="x")
        
        self.btn_search = ctk.CTkButton(
            self.city_frame,
            text="Buscar",
            width=80,
            command=self.fetch_weather_data
        )
        self.btn_search.pack(side="right", padx=(10, 0))
        
        # Área de exibição
        self.display_frame = ctk.CTkFrame(self.main_frame)
        self.display_frame.pack(pady=20, fill="both", expand=True)
        
        # Ícone do clima
        self.icon_label = ctk.CTkLabel(self.display_frame, text="🌤️", font=("Arial", 60))
        self.icon_label.pack(pady=10)
        
        # Dados climáticos
        self.weather_data_label = ctk.CTkLabel(
            self.display_frame,
            text="Digite uma cidade para ver o clima",
            font=("Arial", 14),
            wraplength=400,
            justify="left"
        )
        self.weather_data_label.pack(fill="x", padx=20)
        
        # Rodapé
        self.footer = ctk.CTkLabel(
            self.main_frame,
            text="Última atualização: N/A",
            font=("Arial", 10)
        )
        self.footer.pack(pady=(20, 10))

    def fetch_weather_data(self):
        """Obtém e exibe os dados climáticos"""
        city = self.entry_city.get().strip()
        if not city:
            self.show_error("Por favor, digite uma cidade")
            return
        
        self.current_city = city
        self.btn_search.configure(state="disabled", text="Buscando...")
        self.root.update()
        
        try:
            weather_data = get_weather(city)
            
            if 'error' in weather_data:
                self.show_error(weather_data['error'])
                return
                
            self.display_weather(weather_data)
            self.last_update = datetime.now().strftime("%H:%M:%S")
            self.footer.configure(text=f"Última atualização: {self.last_update} | Cidade: {city}")
            
        except Exception as e:
            self.show_error(f"Erro inesperado: {str(e)}")
        finally:
            self.btn_search.configure(state="normal", text="Buscar")

    def display_weather(self, data):
        """Exibe os dados climáticos na interface"""
        # Atualiza ícone
        self.update_weather_icon(data.get('icone', ''))
        
        # Formata os dados
        weather_info = (
            f"📍 Cidade: {data.get('cidade', 'N/A')}\n"
            f"🌡 Temperatura: {data.get('temperatura', 'N/A')}°C\n"
            f"💧 Umidade: {data.get('umidade', 'N/A')}%\n"
            f"🌬 Vento: {data.get('vento', 'N/A')} m/s\n"
        )
        
        # Adiciona informações opcionais
        if 'nascer_do_sol' in data:
            weather_info += f"🌅 Nascer do sol: {data['nascer_do_sol']}\n"
        if 'por_do_sol' in data:
            weather_info += f"🌇 Pôr do sol: {data['por_do_sol']}\n"
        
        weather_info += f"📌 Condição: {data.get('descricao', 'N/A')}"
        
        self.weather_data_label.configure(text=weather_info, text_color="white")

    def update_weather_icon(self, icon_code):
        """Atualiza o ícone do clima"""
        if not icon_code:
            self.icon_label.configure(text="🌤️", image=None)
            return
            
        try:
            url = f"https://openweathermap.org/img/wn/{icon_code}@2x.png"
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            
            img = Image.open(BytesIO(response.content))
            img = img.resize((100, 100), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            
            self.icon_label.configure(image=photo, text="")
            self.icon_label.image = photo
            
        except Exception as e:
            print(f"Erro ao carregar ícone: {e}")
            self.icon_label.configure(text="🌤️", image=None)

    def show_error(self, message):
        """Exibe mensagens de erro"""
        self.weather_data_label.configure(text=f"❌ {message}", text_color="#ff4444")
        self.icon_label.configure(text="❌", image=None)
        self.footer.configure(text="Erro na última atualização")

    def run(self):
        """Inicia a aplicação"""
        self.root.mainloop()

if __name__ == "__main__":
    app = WeatherApp()
    app.run()