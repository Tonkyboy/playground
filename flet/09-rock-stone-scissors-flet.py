
import flet as ft
import random

def main(page: ft.Page):
    page.title = "Rock 🪨 Paper 📄 Scissors ✂️"
    page.window.width = 400
    page.window.height = 300
    page.window.resizable = False
    
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.DARK 

    # 2. The Logic
    def play(e):
        user = e.control.data 
        options = ["Rock", "Paper", "Scissors"]
        comp = random.choice(options)
        emoji_map = {"Rock": "🪨", 
                     "Paper": "📄", 
                     "Scissors": "✂️"}
        result_text.value = f"🤖 Comp chose: {emoji_map[comp]}"
        
        if user == comp:
            outcome.value = "🤝 It's a Draw!"
            outcome.color = ft.Colors.YELLOW
        elif (user == "Rock" and comp == "Scissors") or \
             (user == "Paper" and comp == "Rock") or \
             (user == "Scissors" and comp == "Paper"):
            outcome.value = "🎉 You Win!"
            outcome.color = ft.Colors.GREEN
        else:
            outcome.value = "💀 You Lose!"
            outcome.color = ft.Colors.RED

        page.update()

    result_text = ft.Text("Choose your weapon! ⚔️", size=16)
    outcome = ft.Text("", size=30, weight="bold")

    btn_rock = ft.ElevatedButton("🪨 Rock", 
                                 data="Rock", 
                                 on_click=play)
    btn_paper = ft.ElevatedButton("📄 Paper", 
                                  data="Paper", 
                                  on_click=play)
    btn_scissor = ft.ElevatedButton("✂️ Scissors", 
                                    data="Scissors", 
                                    on_click=play)

    btn_row = ft.Row([btn_rock, btn_paper, btn_scissor], 
                     alignment="center")

    page.add(result_text, outcome, btn_row)

ft.app(target=main)