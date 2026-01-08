"""
Blackjack Game - GUI Interface
Integrates with existing game files
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import sys
from io import StringIO
import os

# Import the actual game modules
try:
    from story import Player
    import blackjack
    import lists
    HAS_GAME_FILES = True
except ImportError as e:
    print(f"Warning: Could not import game files: {e}")
    HAS_GAME_FILES = False

# Main GUI Application
class BlackjackGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Blackjack: The Road to Redemption")
        self.root.geometry("1200x800")
        self.root.configure(bg="#1a1a1a")
        
        # Initialize the actual Player object
        if HAS_GAME_FILES:
            self.player = Player()
        else:
            self.player = None
            
        # GUI state
        self.current_context = "main_menu"  # Track where we are in the game
        
        self.setup_ui()
        
    def setup_ui(self):
        """Create the main UI layout"""
        
        # ===== TOP STATUS BAR =====
        status_frame = tk.Frame(self.root, bg="#2d2d2d", height=80)
        status_frame.pack(fill=tk.X, padx=10, pady=5)
        status_frame.pack_propagate(False)
        
        # Day counter
        day_label = tk.Label(status_frame, text=f"Day {self.day}", 
                            font=("Arial", 16, "bold"), fg="#00ff00", bg="#2d2d2d")
        day_label.pack(side=tk.LEFT, padx=20, pady=10)
        
        # Balance
        balance_label = tk.Label(status_frame, text=f"Balance: ${self.balance:,.2f}", 
                                font=("Arial", 16, "bold"), fg="#ffcc00", bg="#2d2d2d")
        balance_label.pack(side=tk.LEFT, padx=20, pady=10)
        self.balance_label = balance_label
        
        # Health bar
        health_frame = tk.Frame(status_frame, bg="#2d2d2d")
        health_frame.pack(side=tk.LEFT, padx=20, pady=10)
        tk.Label(health_frame, text="HP:", font=("Arial", 12), 
                fg="white", bg="#2d2d2d").pack(side=tk.LEFT)
        self.health_bar = ttk.Progressbar(health_frame, length=150, mode='determinate',
                                         maximum=100, value=self.health)
        self.health_bar.pack(side=tk.LEFT, padx=5)
        self.health_label = tk.Label(health_frame, text=f"{self.health}/100",
                                     font=("Arial", 10), fg="#ff6666", bg="#2d2d2d")
        self.health_label.pack(side=tk.LEFT, padx=5)
        
        # Sanity bar
        sanity_frame = tk.Frame(status_frame, bg="#2d2d2d")
        sanity_frame.pack(side=tk.LEFT, padx=20, pady=10)
        tk.Label(sanity_frame, text="Sanity:", font=("Arial", 12),
                fg="white", bg="#2d2d2d").pack(side=tk.LEFT)
        self.sanity_bar = ttk.Progressbar(sanity_frame, length=150, mode='determinate',
                                         maximum=100, value=self.sanity)
        self.sanity_bar.pack(side=tk.LEFT, padx=5)
        self.sanity_label = tk.Label(sanity_frame, text=f"{self.sanity}/100",
                                     font=("Arial", 10), fg="#66ccff", bg="#2d2d2d")
        self.sanity_label.pack(side=tk.LEFT, padx=5)
        
        # Rank
        rank_label = tk.Label(status_frame, text=f"Rank: {self.rank}",
                             font=("Arial", 14), fg="#cc66ff", bg="#2d2d2d")
        rank_label.pack(side=tk.RIGHT, padx=20, pady=10)
        self.rank_label = rank_label
        
        # ===== MAIN CONTENT AREA =====
        content_frame = tk.Frame(self.root, bg="#1a1a1a")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Left panel - Story/Events
        left_panel = tk.Frame(content_frame, bg="#2d2d2d", width=700)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # Story text area with custom styling
        story_label = tk.Label(left_panel, text="STORY", font=("Arial", 12, "bold"),
                              fg="#ffffff", bg="#2d2d2d")
        story_label.pack(pady=5)
        
        self.story_text = scrolledtext.ScrolledText(
            left_panel, wrap=tk.WORD, font=("Courier New", 11),
            bg="#1a1a1a", fg="#ffffff", insertbackground="white",
            relief=tk.FLAT, padx=15, pady=15, height=25
        )
        self.story_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        self.story_text.config(state=tk.DISABLED)
        
        # Right panel - Choices and Info
        right_panel = tk.Frame(content_frame, bg="#2d2d2d", width=400)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(5, 0))
        right_panel.pack_propagate(False)
        
        # Choices section
        choices_label = tk.Label(right_panel, text="CHOICES", font=("Arial", 12, "bold"),
                                fg="#ffffff", bg="#2d2d2d")
        choices_label.pack(pady=5)
        
        self.choices_frame = tk.Frame(right_panel, bg="#2d2d2d")
        self.choices_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Info section
        info_label = tk.Label(right_panel, text="QUICK INFO", font=("Arial", 10, "bold"),
                             fg="#aaaaaa", bg="#2d2d2d")
        info_label.pack(pady=(20, 5))
        
        self.info_text = tk.Text(right_panel, wrap=tk.WORD, font=("Arial", 9),
                                bg="#1a1a1a", fg="#cccccc", height=8,
                                relief=tk.FLAT, padx=10, pady=10)
        self.info_text.pack(fill=tk.X, padx=10, pady=5)
        self.info_text.config(state=tk.DISABLED)
        
        # ===== BOTTOM BUTTON BAR =====
        button_frame = tk.Frame(self.root, bg="#2d2d2d", height=60)
        button_frame.pack(fill=tk.X, padx=10, pady=5)
        button_frame.pack_propagate(False)
        
        # Main action buttons
        btn_style = {"font": ("Arial", 11, "bold"), "bg": "#4a4a4a", 
                    "fg": "white", "relief": tk.RAISED, "bd": 2,
                    "padx": 20, "pady": 10, "cursor": "hand2"}
        
        tk.Button(button_frame, text="📊 Stats", command=self.show_stats,
                 **btn_style).pack(side=tk.LEFT, padx=5, pady=10)
        
        tk.Button(button_frame, text="🎒 Inventory", command=self.show_inventory,
                 **btn_style).pack(side=tk.LEFT, padx=5, pady=10)
        
        tk.Button(button_frame, text="🐕 Companions", command=self.show_companions,
                 **btn_style).pack(side=tk.LEFT, padx=5, pady=10)
        
        tk.Button(button_frame, text="🏆 Achievements", command=self.show_achievements,
                 **btn_style).pack(side=tk.LEFT, padx=5, pady=10)
        
        tk.Button(button_frame, text="💾 Save Game", command=self.save_game,
                 **btn_style).pack(side=tk.RIGHT, padx=5, pady=10)
        
        tk.Button(button_frame, text="⚙️ Settings", command=self.show_settings,
                 **btn_style).pack(side=tk.RIGHT, padx=5, pady=10)
        
        # Initialize with welcome message
        self.show_welcome_screen()
        
    def show_welcome_screen(self):
        """Display welcome/main menu"""
        self.clear_story()
        self.add_story_text("=" * 60 + "\n", "#ffcc00")
        self.add_story_text("BLACKJACK: THE ROAD TO REDEMPTION\n", "#ffcc00", bold=True, size=16)
        self.add_story_text("=" * 60 + "\n\n", "#ffcc00")
        
        self.add_story_text("You wake up in your station wagon.\n", "#ffffff")
        self.add_story_text("The parking lot is quiet. Dawn is breaking.\n\n", "#aaaaaa")
        
        self.add_story_text("Three weeks ago, you had a home. A family. A life.\n", "#ff9999")
        self.add_story_text("Gambling took it all.\n\n", "#ff6666")
        
        self.add_story_text("Now you have $50 to your name.\n", "#ffcc00")
        self.add_story_text("And one goal: Turn it into $1,000,000.\n\n", "#00ff00", bold=True)
        
        self.add_story_text("The casino opens tonight.\n", "#66ccff")
        self.add_story_text("This is Day 1.\n\n", "#00ff00")
        
        self.add_story_text("Will you find redemption? Or lose everything?\n\n", "#cc66ff", italic=True)
        
        # Welcome choices
        self.clear_choices()
        self.add_choice_button("🎲 New Game", self.start_new_game, "#00cc00")
        self.add_choice_button("📂 Load Game", self.load_game, "#0099cc")
        self.add_choice_button("📖 How to Play", self.show_tutorial, "#cc9900")
        self.add_choice_button("❌ Exit", self.exit_game, "#cc0000")
        
        # Update info panel
        self.update_info("Welcome to the game!\n\nManage your health, sanity, and money as you gamble your way to $1M.\n\nMake choices carefully - they have consequences.")
        
    def clear_story(self):
        """Clear the story text area"""
        self.story_text.config(state=tk.NORMAL)
        self.story_text.delete(1.0, tk.END)
        self.story_text.config(state=tk.DISABLED)
        
    def add_story_text(self, text, color="#ffffff", bold=False, italic=False, size=11):
        """Add text to story area with formatting"""
        self.story_text.config(state=tk.NORMAL)
        
        # Create tag for this text
        tag_name = f"tag_{len(self.story_text.tag_names())}"
        font_style = ["Courier New", size]
        if bold:
            font_style.append("bold")
        if italic:
            font_style.append("italic")
            
        self.story_text.tag_config(tag_name, foreground=color, font=tuple(font_style))
        self.story_text.insert(tk.END, text, tag_name)
        self.story_text.see(tk.END)
        self.story_text.config(state=tk.DISABLED)
        
    def clear_choices(self):
        """Clear all choice buttons"""
        for widget in self.choices_frame.winfo_children():
            widget.destroy()
            
    def add_choice_button(self, text, command, color="#4a4a4a"):
        """Add a choice button"""
        btn = tk.Button(
            self.choices_frame, text=text, command=command,
            font=("Arial", 11), bg=color, fg="white",
            relief=tk.RAISED, bd=2, padx=15, pady=12,
            cursor="hand2", wraplength=350, justify=tk.LEFT
        )
        btn.pack(fill=tk.X, pady=5)
        
        # Hover effects
        def on_enter(e):
            btn['bg'] = self.lighten_color(color)
        def on_leave(e):
            btn['bg'] = color
            
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        
    def lighten_color(self, color):
        """Lighten a hex color"""
        if color.startswith('#'):
            r, g, b = int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)
            r, g, b = min(255, r + 30), min(255, g + 30), min(255, b + 30)
            return f"#{r:02x}{g:02x}{b:02x}"
        return color
        
    def update_info(self, text):
        """Update the info panel"""
        self.info_text.config(state=tk.NORMAL)
        self.info_text.delete(1.0, tk.END)
        self.info_text.insert(1.0, text)
        self.info_text.config(state=tk.DISABLED)
        
    def update_stats(self, health=None, sanity=None, balance=None, day=None, rank=None):
        """Update the status bar"""
        if health is not None:
            self.health = health
            self.health_bar['value'] = health
            self.health_label['text'] = f"{health}/100"
            
        if sanity is not None:
            self.sanity = sanity
            self.sanity_bar['value'] = sanity
            self.sanity_label['text'] = f"{sanity}/100"
            
        if balance is not None:
            self.balance = balance
            self.balance_label['text'] = f"Balance: ${balance:,.2f}"
            
        if day is not None:
            self.day = day
            self.root.title(f"Blackjack: The Road to Redemption - Day {day}")
            
        if rank is not None:
            self.rank = rank
            self.rank_label['text'] = f"Rank: {rank}"
            
    # ===== BUTTON ACTIONS =====
    
    def start_new_game(self):
        """Start a new game"""
        self.clear_story()
        self.add_story_text("STARTING NEW GAME...\n\n", "#00ff00", bold=True)
        self.add_story_text("You step out of your car and stretch.\n", "#ffffff")
        self.add_story_text("The sun is rising over the parking lot.\n", "#ffcc00")
        self.add_story_text("Another day to survive.\n\n", "#aaaaaa")
        
        # Show day menu
        self.show_day_menu()
        
    def show_day_menu(self):
        """Show the day actions menu"""
        self.clear_choices()
        self.add_choice_button("🏪 Visit Kyle's Store", self.visit_store, "#0099cc")
        self.add_choice_button("🔧 Go to Mechanic", self.visit_mechanic, "#cc6600")
        self.add_choice_button("🌳 Explore Area", self.explore, "#00cc66")
        self.add_choice_button("💤 Rest Until Evening", self.rest, "#6666cc")
        self.add_choice_button("📊 Check Stats", self.show_stats, "#cc9900")
        
        self.update_info(f"Day {self.day}\nBalance: ${self.balance:,.2f}\n\nWhat will you do today?")
        
    def visit_store(self):
        """Visit convenience store"""
        self.clear_story()
        self.add_story_text("KYLE'S 24-HOUR CONVENIENCE STORE\n\n", "#00ccff", bold=True)
        self.add_story_text("Kyle: ", "#ffcc00", bold=True)
        self.add_story_text('"Hey buddy! What can I get you?"\n\n', "#ffffff")
        
        self.clear_choices()
        self.add_choice_button("🌭 Hot Dog - $3", lambda: self.buy_item("Hot Dog", 3, 8), "#cc6600")
        self.add_choice_button("🥤 Energy Drink - $4", lambda: self.buy_item("Energy Drink", 4, 5), "#ff3333")
        self.add_choice_button("🍫 Protein Bar - $5", lambda: self.buy_item("Protein Bar", 5, 10), "#996633")
        self.add_choice_button("💊 Pain Killers - $8", lambda: self.buy_item("Pain Killers", 8, 10), "#ff9999")
        self.add_choice_button("← Back", self.show_day_menu, "#666666")
        
    def buy_item(self, item_name, cost, health_gain):
        """Buy an item"""
        if self.balance >= cost:
            self.balance -= cost
            self.health = min(100, self.health + health_gain)
            self.update_stats(balance=self.balance, health=self.health)
            self.add_story_text(f"\nYou bought {item_name} for ${cost}.\n", "#00ff00")
            self.add_story_text(f"HP +{health_gain}\n", "#66ff66")
        else:
            self.add_story_text(f"\nNot enough money! Need ${cost}.\n", "#ff3333")
            
    def visit_mechanic(self):
        """Visit mechanic - placeholder"""
        self.clear_story()
        self.add_story_text("MECHANIC SHOP\n\n", "#cc6600", bold=True)
        self.add_story_text("Not yet unlocked.\n", "#aaaaaa")
        self.add_story_text("(Meet Tom in story events to unlock)\n\n", "#666666", italic=True)
        
        self.clear_choices()
        self.add_choice_button("← Back", self.show_day_menu, "#666666")
        
    def explore(self):
        """Explore - trigger random event"""
        import random
        events = [
            ("You find $20 on the ground!", "#00ff00", 20, 0),
            ("A friendly dog approaches. You pet it.", "#66ccff", 0, 5),
            ("You stub your toe on a rock.", "#ff6666", 0, -5),
            ("Beautiful clouds today. Peaceful.", "#ffcc99", 0, 3),
        ]
        
        event_text, color, money, sanity = random.choice(events)
        
        self.clear_story()
        self.add_story_text("EXPLORING...\n\n", "#00cc66", bold=True)
        self.add_story_text(event_text + "\n\n", color)
        
        if money:
            self.balance += money
            self.add_story_text(f"Balance: +${money}\n", "#00ff00")
        if sanity:
            self.sanity = max(0, min(100, self.sanity + sanity))
            change = "+" if sanity > 0 else ""
            self.add_story_text(f"Sanity: {change}{sanity}\n", "#66ccff")
            
        self.update_stats(balance=self.balance, sanity=self.sanity)
        
        self.clear_choices()
        self.add_choice_button("Continue", self.show_day_menu, "#666666")
        
    def rest(self):
        """Rest until evening"""
        self.clear_story()
        self.add_story_text("You rest in your car...\n\n", "#6666cc")
        self.add_story_text("Time passes.\n\n", "#aaaaaa")
        
        # Small health gain
        self.health = min(100, self.health + 5)
        self.update_stats(health=self.health)
        
        self.add_story_text("Evening arrives. The casino is open.\n\n", "#ffcc00", bold=True)
        
        self.clear_choices()
        self.add_choice_button("🎰 Go to Casino", self.go_to_casino, "#ff0000")
        self.add_choice_button("😴 Skip Tonight", self.skip_night, "#666666")
        
    def go_to_casino(self):
        """Go to casino"""
        self.clear_story()
        self.add_story_text("=" * 60 + "\n", "#ff0000")
        self.add_story_text("THE CASINO\n", "#ff0000", bold=True, size=14)
        self.add_story_text("=" * 60 + "\n\n", "#ff0000")
        
        self.add_story_text("You walk through the doors.\n", "#ffffff")
        self.add_story_text("Smoke, lights, the sound of chips...\n\n", "#ffcc00")
        
        self.add_story_text("The Dealer nods at you.\n", "#ff6666", bold=True)
        self.add_story_text('"Back again? Take a seat."\n\n', "#ffffff")
        
        self.clear_choices()
        self.add_choice_button("♠️ Play Blackjack", self.play_blackjack, "#ff0000")
        self.add_choice_button("🚪 Leave Casino", self.leave_casino, "#666666")
        
    def play_blackjack(self):
        """Play blackjack - simplified version"""
        self.clear_story()
        self.add_story_text("BLACKJACK TABLE\n\n", "#ff0000", bold=True)
        self.add_story_text("(Full blackjack integration coming)\n\n", "#666666", italic=True)
        
        # Simplified bet system
        self.add_story_text("Place your bet:\n\n", "#ffffff")
        
        self.clear_choices()
        self.add_choice_button("$10", lambda: self.simple_hand(10), "#006600")
        self.add_choice_button("$25", lambda: self.simple_hand(25), "#009900")
        self.add_choice_button("$50", lambda: self.simple_hand(50), "#00cc00")
        self.add_choice_button("← Back", self.go_to_casino, "#666666")
        
    def simple_hand(self, bet):
        """Play a simplified blackjack hand"""
        import random
        
        if bet > self.balance:
            self.add_story_text("\nNot enough money!\n", "#ff3333")
            return
            
        self.clear_story()
        self.add_story_text(f"BET: ${bet}\n\n", "#ffcc00", bold=True)
        self.add_story_text("Cards are dealt...\n\n", "#ffffff")
        
        # Simple win/loss
        outcome = random.choice(["win", "win", "lose", "lose", "push"])
        
        if outcome == "win":
            winnings = bet
            self.balance += winnings
            self.add_story_text("YOU WIN!\n", "#00ff00", bold=True)
            self.add_story_text(f"+${winnings}\n\n", "#00ff00")
        elif outcome == "lose":
            self.balance -= bet
            self.add_story_text("You lose.\n", "#ff3333")
            self.add_story_text(f"-${bet}\n\n", "#ff3333")
        else:
            self.add_story_text("Push - bet returned.\n", "#ffcc00")
            
        self.update_stats(balance=self.balance)
        
        self.clear_choices()
        self.add_choice_button("Play Again", self.play_blackjack, "#ff0000")
        self.add_choice_button("Leave Table", self.go_to_casino, "#666666")
        
    def leave_casino(self):
        """Leave casino and end day"""
        self.clear_story()
        self.add_story_text("You leave the casino.\n\n", "#ffffff")
        self.add_story_text("Exhausted, you return to your car.\n", "#aaaaaa")
        self.add_story_text("Another day survived.\n\n", "#66ccff")
        
        self.day += 1
        self.update_stats(day=self.day)
        
        self.clear_choices()
        self.add_choice_button("Sleep (Next Day)", self.start_new_game, "#6666cc")
        
    def skip_night(self):
        """Skip casino for the night"""
        self.clear_story()
        self.add_story_text("You decide not to gamble tonight.\n\n", "#aaaaaa")
        self.add_story_text("You rest in your car and sleep.\n", "#6666cc")
        
        self.health = min(100, self.health + 10)
        self.day += 1
        self.update_stats(health=self.health, day=self.day)
        
        self.clear_choices()
        self.add_choice_button("Wake Up (Next Day)", self.start_new_game, "#00ff00")
        
    def show_stats(self):
        """Show detailed stats window"""
        stats_window = tk.Toplevel(self.root)
        stats_window.title("Player Statistics")
        stats_window.geometry("600x500")
        stats_window.configure(bg="#2d2d2d")
        
        tk.Label(stats_window, text="📊 PLAYER STATISTICS", font=("Arial", 16, "bold"),
                fg="#ffffff", bg="#2d2d2d").pack(pady=20)
        
        stats_text = scrolledtext.ScrolledText(stats_window, wrap=tk.WORD,
                                               font=("Courier New", 11),
                                               bg="#1a1a1a", fg="#ffffff",
                                               padx=20, pady=20)
        stats_text.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        stats_content = f"""
Day:           {self.day}
Balance:       ${self.balance:,.2f}
Rank:          {self.rank}

Health:        {self.health}/100
Sanity:        {self.sanity}/100

Status Effects: None
Injuries:       None
Illnesses:      None

Companions:     0
Achievements:   0/240+

Gambling Stats:
  Total Hands:  0
  Wins:         0
  Losses:       0
  Blackjacks:   0

Inventory:      Empty
        """
        
        stats_text.insert(1.0, stats_content)
        stats_text.config(state=tk.DISABLED)
        
        tk.Button(stats_window, text="Close", command=stats_window.destroy,
                 font=("Arial", 11), bg="#4a4a4a", fg="white",
                 padx=30, pady=10).pack(pady=10)
        
    def show_inventory(self):
        """Show inventory"""
        messagebox.showinfo("Inventory", "Your inventory is empty.\n\n(Full inventory system coming)")
        
    def show_companions(self):
        """Show companions"""
        messagebox.showinfo("Companions", "You have no companions yet.\n\n(Befriend animals in events)")
        
    def show_achievements(self):
        """Show achievements"""
        messagebox.showinfo("Achievements", "0/240+ Achievements Unlocked\n\n(Full achievement system coming)")
        
    def show_settings(self):
        """Show settings"""
        messagebox.showinfo("Settings", "Settings menu coming soon!\n\nPlanned:\n- Volume controls\n- Text speed\n- Auto-save")
        
    def save_game(self):
        """Save game"""
        messagebox.showinfo("Save Game", "Game saved!\n\n(Save system integration coming)")
        
    def load_game(self):
        """Load game"""
        messagebox.showinfo("Load Game", "No save file found.\n\nStart a new game!")
        
    def show_tutorial(self):
        """Show tutorial"""
        tutorial_window = tk.Toplevel(self.root)
        tutorial_window.title("How to Play")
        tutorial_window.geometry("700x600")
        tutorial_window.configure(bg="#2d2d2d")
        
        tk.Label(tutorial_window, text="📖 HOW TO PLAY", font=("Arial", 16, "bold"),
                fg="#ffffff", bg="#2d2d2d").pack(pady=20)
        
        tutorial_text = scrolledtext.ScrolledText(tutorial_window, wrap=tk.WORD,
                                                 font=("Arial", 11),
                                                 bg="#1a1a1a", fg="#ffffff",
                                                 padx=20, pady=20)
        tutorial_text.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        tutorial_content = """
OBJECTIVE:
Turn your $50 into $1,000,000 through blackjack and smart choices.

STATS TO MANAGE:
• Health (HP): Affected by injuries, illness, food
• Sanity: Affected by trauma, stress, positive events
• Balance: Your money - don't let it hit $0!

DAY/NIGHT CYCLE:
• Day: Visit shops, explore, handle events
• Night: Go to casino and gamble

IMPORTANT SYSTEMS:
• Companions: Befriend animals for bonuses and comfort
• Achievements: 240+ to unlock
• Multiple Endings: Your choices matter
• NPCs: Build relationships (Tom, Frank, Oswald, Suzy)

TIPS:
• Don't bet more than 10% of your bankroll
• Keep HP above 30 (visit doctor if needed)
• Watch your sanity - madness is real
• Be kind to Suzy (trust us)
• Save often
• Explore for items and events

ENDINGS:
There are 8 major endings based on your choices:
• Salvation: Call your family
• Millionaire: Reach $1,000,000
• Resurrection: Embrace gambling forever
• Madness: Lose your mind
• The Offer: Accept a mysterious deal
• And more...

Good luck. The house always wins... or does it?
        """
        
        tutorial_text.insert(1.0, tutorial_content)
        tutorial_text.config(state=tk.DISABLED)
        
        tk.Button(tutorial_window, text="Close", command=tutorial_window.destroy,
                 font=("Arial", 11), bg="#4a4a4a", fg="white",
                 padx=30, pady=10).pack(pady=10)
        
    def exit_game(self):
        """Exit the application"""
        if messagebox.askyesno("Exit Game", "Are you sure you want to quit?"):
            self.root.quit()


# ===== MAIN ENTRY POINT =====
def main():
    root = tk.Tk()
    app = BlackjackGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
