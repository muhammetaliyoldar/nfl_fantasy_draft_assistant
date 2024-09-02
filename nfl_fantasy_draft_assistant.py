import pandas as pd
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox


class FantasyDraftAssistant:
    def __init__(self, root):
        self.root = root
        self.root.title("NFL Fantasy Draft Assistant")
        self.data = None
        self.team_count = 0
        self.draft_position = 0
        self.actual_picks = []  # Gerçekleşmiş seçimleri takip etmek için liste
        self.setup_ui()

    def setup_ui(self):
        self.upload_button = tk.Button(self.root, text="XLSX Dosyasını Yükle", command=self.load_file)
        self.upload_button.pack(pady=10)

        self.draft_button = tk.Button(self.root, text="Draft Ekranına Geç", command=self.open_draft_screen,
                                      state=tk.DISABLED)
        self.draft_button.pack(pady=10)

    def load_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
        if file_path:
            self.data = self.load_all_sheets(file_path)
            if self.data is not None:
                messagebox.showinfo("Bilgi", "Dosya başarıyla yüklendi.")
                self.draft_button.config(state=tk.NORMAL)
            else:
                messagebox.showerror("Hata", "Dosya yüklenirken bir hata oluştu.")

    def load_all_sheets(self, file_path):
        try:
            sheets = pd.read_excel(file_path, sheet_name=None)
            return sheets
        except Exception as e:
            messagebox.showerror("Hata", f"Dosya yüklenirken bir hata oluştu: {e}")
            return None

    def open_draft_screen(self):
        if self.data is None:
            messagebox.showwarning("Uyarı", "Önce bir dosya yüklemelisiniz.")
            return

        self.draft_window = tk.Toplevel(self.root)
        self.draft_window.title("Draft Ekranı")
        self.draft_window.geometry("1800x700")
        self.draft_window.resizable(True, True)

        self.team_count_label = tk.Label(self.draft_window, text="Takım Sayısı:")
        self.team_count_label.grid(row=0, column=0, padx=10, pady=5)

        self.team_count_entry = tk.Entry(self.draft_window)
        self.team_count_entry.grid(row=0, column=1, padx=10, pady=5)

        self.draft_position_label = tk.Label(self.draft_window, text="Kendi Draft Sıramız:")
        self.draft_position_label.grid(row=1, column=0, padx=10, pady=5)

        self.draft_position_entry = tk.Entry(self.draft_window)
        self.draft_position_entry.grid(row=1, column=1, padx=10, pady=5)

        self.start_draft_button = tk.Button(self.draft_window, text="Başla", command=self.start_draft)
        self.start_draft_button.grid(row=1, column=2, padx=10, pady=5)

        self.position_headers = ["QB", "RB", "WR", "TE"]
        self.players_listboxes = {}

        for i, position in enumerate(self.position_headers):
            label = tk.Label(self.draft_window, text=position)
            label.grid(row=2, column=i, padx=10, pady=5)

            frame = tk.Frame(self.draft_window, width=300, height=300)
            frame.grid(row=3, column=i, padx=10, pady=5, sticky='nsew')
            listbox = tk.Listbox(frame, width=40, height=20, selectmode=tk.MULTIPLE)
            listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            listbox.config(yscrollcommand=scrollbar.set)
            scrollbar.config(command=listbox.yview)
            self.players_listboxes[position] = listbox

        self.my_team_frame = tk.Frame(self.draft_window)
        self.my_team_frame.grid(row=3, column=len(self.position_headers), padx=10, pady=5, sticky='nsew')
        self.my_team_label = tk.Label(self.my_team_frame, text="Takımım")
        self.my_team_label.pack(pady=5)
        self.my_team_listbox = tk.Listbox(self.my_team_frame, width=40, height=30)
        self.my_team_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.my_team_scrollbar = tk.Scrollbar(self.my_team_frame, orient=tk.VERTICAL)
        self.my_team_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.my_team_listbox.config(yscrollcommand=self.my_team_scrollbar.set)
        self.my_team_scrollbar.config(command=self.my_team_listbox.yview)

        self.drafted_players_frame = tk.Frame(self.draft_window)
        self.drafted_players_frame.grid(row=3, column=len(self.position_headers) + 1, padx=10, pady=5, sticky='nsew')
        self.drafted_players_label = tk.Label(self.drafted_players_frame, text="Draftlandı")
        self.drafted_players_label.pack(pady=5)
        self.drafted_players_listbox = tk.Listbox(self.drafted_players_frame, width=40, height=30)
        self.drafted_players_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.drafted_players_scrollbar = tk.Scrollbar(self.drafted_players_frame, orient=tk.VERTICAL)
        self.drafted_players_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.drafted_players_listbox.config(yscrollcommand=self.drafted_players_scrollbar.set)
        self.drafted_players_scrollbar.config(command=self.drafted_players_listbox.yview)

        self.potential_frame = tk.Frame(self.draft_window)
        self.potential_frame.grid(row=3, column=len(self.position_headers) + 2, padx=10, pady=5, sticky='nsew')
        self.potential_label = tk.Label(self.potential_frame, text="Muhtemel")
        self.potential_label.pack(pady=5)
        self.potential_listbox = tk.Listbox(self.potential_frame, width=40, height=30)
        self.potential_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.potential_scrollbar = tk.Scrollbar(self.potential_frame, orient=tk.VERTICAL)
        self.potential_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.potential_listbox.config(yscrollcommand=self.potential_scrollbar.set)
        self.potential_scrollbar.config(command=self.potential_listbox.yview)

        # Toplam puanını göstermek için bir etiket ekleyelim
        self.total_score_label = tk.Label(self.draft_window, text="Toplam Puan: 0")
        self.total_score_label.grid(row=5, column=0, padx=10, pady=5, columnspan=2, sticky='w')

        self.search_label = tk.Label(self.draft_window, text="Oyuncu Ara:")
        self.search_label.grid(row=6, column=0, padx=10, pady=5)

        self.search_entry = tk.Entry(self.draft_window)
        self.search_entry.grid(row=6, column=1, padx=10, pady=5)

        self.search_button = tk.Button(self.draft_window, text="Ara", command=self.search_player)
        self.search_button.grid(row=6, column=2, padx=10, pady=5)

        self.add_to_team_button = tk.Button(self.draft_window, text="Takıma Ekle", command=self.add_to_team)
        self.add_to_team_button.grid(row=6, column=3, padx=10, pady=5)

        self.add_to_drafted_button = tk.Button(self.draft_window, text="Draftlandı Ekle", command=self.add_to_drafted)
        self.add_to_drafted_button.grid(row=6, column=4, padx=10, pady=5)

        self.remove_from_list_button = tk.Button(self.draft_window, text="Listeden Kaldır",
                                                 command=self.remove_from_list)
        self.remove_from_list_button.grid(row=6, column=5, padx=10, pady=5)

        self.update_potential_button = tk.Button(self.draft_window, text="Güncelle", command=self.manual_update)
        self.update_potential_button.grid(row=6, column=6, padx=10, pady=5)

        self.draft_window.columnconfigure([i for i in range(len(self.position_headers) + 3)], weight=1)
        self.draft_window.rowconfigure([i for i in range(2, 7)], weight=1)

    def start_draft(self):
        try:
            self.team_count = int(self.team_count_entry.get())
            self.draft_position = int(self.draft_position_entry.get())
            if not (1 <= self.draft_position <= self.team_count):
                raise ValueError
            self.update_players_list()
            self.update_potential_players()
        except ValueError:
            messagebox.showerror("Hata", "Geçerli bir takım sayısı ve draft sırası girin.")

    def update_players_list(self):
        if self.data:
            all_sheets = self.data
            all_players = pd.concat([sheet for sheet in all_sheets.values()], ignore_index=True)

            # 'TOTAL' sütununu sayısal verilere dönüştür, hataları 'NaN' olarak işaretle
            all_players['TOTAL'] = pd.to_numeric(all_players['TOTAL'], errors='coerce')

            # 'TOTAL' değeri 'NaN' olan satırları kaldır
            all_players = all_players.dropna(subset=['TOTAL'])

            # Aynı isimli oyuncuları birleştirip ortalama puanları hesapla
            average_points = all_players.groupby(['PLAYER NAME', 'PLAYER POSITION']).agg(
                {'TOTAL': 'mean'}).reset_index().rename(columns={'TOTAL': 'Average Points'})

            # Benzersiz oyuncu listesini oluştur
            unique_players = average_points.drop_duplicates(subset=['PLAYER NAME', 'PLAYER POSITION'])

            # Pozisyon başlıkları için oyuncu listelerini güncelle
            for position in self.position_headers:
                sorted_players = unique_players[unique_players['PLAYER POSITION'] == position].sort_values(
                    by='Average Points', ascending=False)
                self.players_listboxes[position].delete(0, tk.END)
                for idx, row in sorted_players.iterrows():
                    player_info = f"{row['PLAYER NAME']} - {row['Average Points']:.2f} Puan (Ortalama)"
                    self.players_listboxes[position].insert(tk.END, player_info)

            # Muhtemel oyuncu listesini güncelle
            self.update_potential_players()

    def calculate_snake_draft_order(self):
        draft_order = []
        for round_num in range(13):  # Her takımın 13 oyuncu draft edeceğini varsayıyoruz.
            if round_num % 2 == 0:  # Çift turlar (1., 3., 5. ... tur)
                draft_order.extend(range(1, self.team_count + 1))
            else:  # Tek turlar (2., 4., 6. ... tur)
                draft_order.extend(range(self.team_count, 0, -1))
        return draft_order

    def update_potential_players(self):
        draft_order = self.calculate_snake_draft_order()
        potential_players = []

        for i in range(len(draft_order)):
            if i < len(self.actual_picks):
                potential_players.append(self.actual_picks[i])
            else:
                available_players = []
                for position in self.position_headers:
                    available_players.extend(self.players_listboxes[position].get(0, tk.END))
                available_players = sorted(available_players, key=lambda x: float(x.split('-')[-1].strip().split(' ')[0]), reverse=True)

                for player in available_players:
                    if player not in potential_players:
                        potential_players.append(player)
                        break

        self.potential_listbox.delete(0, tk.END)
        for i, player in enumerate(potential_players):
            draft_number = (i // self.team_count) + 1
            pick_number = draft_order[i]
            if i >= 7:
                status = " (Yedek)"
            else:
                status = ""
            if player in self.my_team_listbox.get(0, tk.END) or player in self.drafted_players_listbox.get(0, tk.END):
                player += " *"
            player_info = f"{draft_number}. Draft ({pick_number}. Sıra) - {player}{status}"
            self.potential_listbox.insert(tk.END, player_info)

    def manual_update(self):
        self.update_players_list()
        self.update_potential_players()

    def search_player(self):
        search_term = self.search_entry.get()
        if not search_term:
            messagebox.showwarning("Uyarı", "Arama terimi girilmelidir.")
            return

        if self.data:
            all_sheets = self.data
            all_players = pd.concat([sheet for sheet in all_sheets.values()], ignore_index=True)

            # 'TOTAL' sütununu sayısal verilere dönüştür ve 'NaN' olanları kaldır
            all_players['TOTAL'] = pd.to_numeric(all_players['TOTAL'], errors='coerce')
            all_players = all_players.dropna(subset=['TOTAL'])

            # Aynı isimli oyuncuları birleştirip ortalama puanları hesapla
            average_points = all_players.groupby(['PLAYER NAME', 'PLAYER POSITION']).agg(
                {'TOTAL': 'mean'}).reset_index().rename(columns({'TOTAL': 'Average Points'}))

            # Benzersiz oyuncu listesini oluştur
            unique_players = average_points.drop_duplicates(subset=['PLAYER NAME', 'PLAYER POSITION'])

            # Arama işlemi için 'PLAYER NAME' sütununda arama yap
            results = unique_players[unique_players['PLAYER NAME'].str.contains(search_term, case=False, na=False)]
            if results.empty:
                messagebox.showinfo("Sonuç Yok", "Aradığınız oyuncu bulunamadı.")
            else:
                self.show_search_results(results)

    def show_search_results(self, results):
        self.search_results_window = tk.Toplevel(self.root)
        self.search_results_window.title("Arama Sonuçları")

        listbox = tk.Listbox(self.search_results_window, width=100, height=20, selectmode=tk.SINGLE)
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        for idx, row in results.iterrows():
            player_info = f"{row['PLAYER NAME']} - {row['PLAYER POSITION']} - {row['Average Points']:.2f} Puan"
            listbox.insert(tk.END, player_info)

    def add_to_team(self):
        selected_position = self.get_selected_position()
        if selected_position:
            selected_items = self.players_listboxes[selected_position].curselection()
            for item in selected_items:
                player_info = self.players_listboxes[selected_position].get(item)
                self.my_team_listbox.insert(tk.END, player_info)
                self.players_listboxes[selected_position].delete(item)
                self.actual_picks.append(player_info)  # Seçimi kaydet
            self.update_total_score()
            self.update_potential_players()

    def add_to_drafted(self):
        selected_position = self.get_selected_position()
        if selected_position:
            selected_items = self.players_listboxes[selected_position].curselection()
            for item in selected_items:
                player_info = self.players_listboxes[selected_position].get(item)
                self.drafted_players_listbox.insert(tk.END, player_info)
                self.players_listboxes[selected_position].delete(item)
                self.actual_picks.append(player_info)  # Seçimi kaydet
            self.update_potential_players()

    def remove_from_list(self):
        selected_team_items = self.my_team_listbox.curselection()
        selected_drafted_items = self.drafted_players_listbox.curselection()

        for item in selected_team_items:
            player_info = self.my_team_listbox.get(item)
            self.my_team_listbox.delete(item)
            position = self.get_player_position(player_info)
            self.players_listboxes[position].insert(tk.END, player_info)

        for item in selected_drafted_items:
            player_info = self.drafted_players_listbox.get(item)
            self.drafted_players_listbox.delete(item)
            position = self.get_player_position(player_info)
            self.players_listboxes[position].insert(tk.END, player_info)

        self.update_total_score()
        self.update_potential_players()

    def get_selected_position(self):
        for position in self.position_headers:
            if self.players_listboxes[position].curselection():
                return position
        messagebox.showwarning("Uyarı", "Önce bir oyuncu seçmelisiniz.")
        return None

    def get_player_position(self, player_info):
        for position in self.position_headers:
            if position in player_info:
                return position
        return None

    def update_total_score(self):
        total_score = 0.0
        num_players = self.my_team_listbox.size()

        for i in range(num_players):
            player_info = self.my_team_listbox.get(i)
            points = float(player_info.split("-")[-1].strip().split(" ")[0])
            total_score += points

        self.total_score_label.config(text=f"Toplam Puan: {total_score:.2f}")


if __name__ == "__main__":
    root = tk.Tk()
    app = FantasyDraftAssistant(root)
    root.mainloop()
    