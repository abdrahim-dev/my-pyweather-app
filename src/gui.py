import customtkinter as ctk


class WeatherApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("WeatherApp")
        self.geometry("500x500")

        # Entry field for city name
        self.city_entry = ctk.CTkEntry(self, placeholder_text="Enter a city", justify="left", font=ctk.CTkFont(size=20, weight="normal"), corner_radius=10)
        self.city_entry.pack(padx=20, pady=20)

        # Search button
        self.search_button = ctk.CTkButton(self, text="Search", width=200, height=30, font=ctk.CTkFont(size=20, weight="bold"), command=self.on_search_click)
        self.search_button.pack(padx=20, pady=20)

        # Four separate output labels
        self.city_label = ctk.CTkLabel(self, text="City")
        self.city_label.pack()

        self.temperature_label = ctk.CTkLabel(self, text="Temperature")
        self.temperature_label.pack()

        self.conditions_label = ctk.CTkLabel(self, text="Conditions")
        self.conditions_label.pack()

        self.humidity_label = ctk.CTkLabel(self, text="Humidity")
        self.humidity_label.pack()

    def on_search_click(self):
        print("button 'Search' was clicked")


if __name__ == "__main__":
    app = WeatherApp()
    app.mainloop()