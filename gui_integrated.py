"""
Blackjack Game - Integrated GUI
Connects to existing story.py and blackjack.py
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import sys
import os

# Import the actual game modules
try:
    from story import Player
    import blackjack as bj_game
    import lists
    HAS_GAME_FILES = True
except ImportError as e:
    print(f"ERROR: Could not import game files: {e}")
    print("Make sure story.py, blackjack.py, and lists.py are in the same directory")
    HAS_GAME_FILES = False


class BlackjackGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Blackjack: The Road to Redemption")
        self.root.geometry("1200x800")
        self.root.configure(bg="#1a1a1a")
        
        if not HAS_GAME_FILES:
            self.show_error_and_exit()
            return
            
        # Initialize the actual Player object from story.py
        self.player = Player()
        self.player.first_setup()  # Run the initial setup if it exists
        
        # GUI state
        self.current_menu = "main"
        
        self.setup_ui()
        self.refresh_stats()
        self.show_welcome_screen()
        
    def show_error_and_exit(self):
        """Show error if game files not found"""
        error_label = tk.Label(self.root, 
                              text="ERROR: Game files not found!\n\nMake sure story.py, blackjack.py, and lists.py\nare in the same directory as this GUI.",
                              font=("Arial", 14), fg="#ff0000", bg="#1a1a1a",
                              justify=tk.CENTER)
        error_label.pack(expand=True)
        
    def setup_ui(self):
        """Create the main UI layout"""
        
        # ===== TOP STATUS BAR =====
        self.status_frame = tk.Frame(self.root, bg="#2d2d2d", height=80)
        self.status_frame.pack(fill=tk.X, padx=10, pady=5)
        self.status_frame.pack_propagate(False)
        
        # Day counter
        self.day_label = tk.Label(self.status_frame, text="Day 1", 
                                  font=("Arial", 16, "bold"), fg="#00ff00", bg="#2d2d2d")
        self.day_label.pack(side=tk.LEFT, padx=20, pady=10)
        
        # Balance
        self.balance_label = tk.Label(self.status_frame, text="Balance: $50.00", 
                                      font=("Arial", 16, "bold"), fg="#ffcc00", bg="#2d2d2d")
        self.balance_label.pack(side=tk.LEFT, padx=20, pady=10)
        
        # Health bar
        health_frame = tk.Frame(self.status_frame, bg="#2d2d2d")
        health_frame.pack(side=tk.LEFT, padx=20, pady=10)
        tk.Label(health_frame, text="HP:", font=("Arial", 12), 
                fg="white", bg="#2d2d2d").pack(side=tk.LEFT)
        self.health_bar = ttk.Progressbar(health_frame, length=150, mode='determinate',
                                         maximum=100, value=100)
        self.health_bar.pack(side=tk.LEFT, padx=5)
        self.health_label = tk.Label(health_frame, text="100/100",
                                     font=("Arial", 10), fg="#ff6666", bg="#2d2d2d")
        self.health_label.pack(side=tk.LEFT, padx=5)
        
        # Sanity bar  
        sanity_frame = tk.Frame(self.status_frame, bg="#2d2d2d")
        sanity_frame.pack(side=tk.LEFT, padx=20, pady=10)
        tk.Label(sanity_frame, text="Sanity:", font=("Arial", 12),
                fg="white", bg="#2d2d2d").pack(side=tk.LEFT)
        self.sanity_bar = ttk.Progressbar(sanity_frame, length=150, mode='determinate',
                                         maximum=100, value=100)
        self.sanity_bar.pack(side=tk.LEFT, padx=5)
        self.sanity_label = tk.Label(sanity_frame, text="100/100",
                                     font=("Arial", 10), fg="#66ccff", bg="#2d2d2d")
        self.sanity_label.pack(side=tk.LEFT, padx=5)
        
        # Rank
        self.rank_label = tk.Label(self.status_frame, text="Rank: Poor",
                                   font=("Arial", 14), fg="#cc66ff", bg="#2d2d2d")
        self.rank_label.pack(side=tk.RIGHT, padx=20, pady=10)
        
        # ===== MAIN CONTENT AREA =====
        content_frame = tk.Frame(self.root, bg="#1a1a1a")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Left panel - Story/Events
        left_panel = tk.Frame(content_frame, bg="#2d2d2d", width=700)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # Story text area
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
        
        # Right panel - Choices
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
        info_label = tk.Label(right_panel, text="INFO", font=("Arial", 10, "bold"),
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
        
        btn_style = {"font": ("Arial", 11, "bold"), "bg": "#4a4a4a", 
                    "fg": "white", "relief": tk.RAISED, "bd": 2,
                    "padx": 20, "pady": 10, "cursor": "hand2"}
        
        tk.Button(button_frame, text="📊 Stats", command=self.show_full_stats,
                 **btn_style).pack(side=tk.LEFT, padx=5, pady=10)
        
        tk.Button(button_frame, text="🎒 Inventory", command=self.show_inventory,
                 **btn_style).pack(side=tk.LEFT, padx=5, pady=10)
        
        tk.Button(button_frame, text="🐕 Companions", command=self.show_companions_window,
                 **btn_style).pack(side=tk.LEFT, padx=5, pady=10)
        
        tk.Button(button_frame, text="🏆 Achievements", command=self.show_achievements_window,
                 **btn_style).pack(side=tk.LEFT, padx=5, pady=10)
        
    def refresh_stats(self):
        """Update all status displays from player object"""
        self.day_label['text'] = f"Day {self.player.get_day()}"
        self.balance_label['text'] = f"Balance: ${self.player.get_balance():,.2f}"
        
        hp = self.player.get_health()
        self.health_bar['value'] = hp
        self.health_label['text'] = f"{hp}/100"
        
        sanity = self.player.get_sanity()
        self.sanity_bar['value'] = sanity
        self.sanity_label['text'] = f"{sanity}/100"
        
        rank_names = ["Poor", "Modest", "Comfortable", "Wealthy", "Rich", "Millionaire"]
        rank = rank_names[min(self.player.get_rank(), 5)]
        self.rank_label['text'] = f"Rank: {rank}"
        
    def clear_story(self):
        """Clear story text"""
        self.story_text.config(state=tk.NORMAL)
        self.story_text.delete(1.0, tk.END)
        self.story_text.config(state=tk.DISABLED)
        
    def add_story(self, text, color="#ffffff"):
        """Add text to story area"""
        self.story_text.config(state=tk.NORMAL)
        tag = f"tag_{len(self.story_text.tag_names())}"
        self.story_text.tag_config(tag, foreground=color)
        self.story_text.insert(tk.END, text, tag)
        self.story_text.see(tk.END)
        self.story_text.config(state=tk.DISABLED)
        
    def clear_choices(self):
        """Clear choice buttons"""
        for widget in self.choices_frame.winfo_children():
            widget.destroy()
            
    def add_choice(self, text, command, color="#4a4a4a"):
        """Add a choice button"""
        btn = tk.Button(
            self.choices_frame, text=text, command=command,
            font=("Arial", 11), bg=color, fg="white",
            relief=tk.RAISED, bd=2, padx=15, pady=12,
            cursor="hand2", wraplength=350, justify=tk.LEFT
        )
        btn.pack(fill=tk.X, pady=5)
        
    def update_info(self, text):
        """Update info panel"""
        self.info_text.config(state=tk.NORMAL)
        self.info_text.delete(1.0, tk.END)
        self.info_text.insert(1.0, text)
        self.info_text.config(state=tk.DISABLED)
        
    def show_welcome_screen(self):
        """Initial welcome screen"""
        self.clear_story()
        self.add_story("=" * 60 + "\n", "#ffcc00")
        self.add_story("BLACKJACK: THE ROAD TO REDEMPTION\n", "#ffcc00")
        self.add_story("=" * 60 + "\n\n", "#ffcc00")
        
        self.add_story("You wake up in your station wagon.\n")
        self.add_story("The parking lot is quiet. Dawn is breaking.\n\n", "#aaaaaa")
        self.add_story("You have $50. Your goal: $1,000,000.\n\n", "#00ff00")
        
        self.clear_choices()
        self.add_choice("🎲 Start Game", self.start_day, "#00cc00")
        self.add_choice("📖 How to Play", self.show_tutorial, "#cc9900")
        self.add_choice("❌ Exit", self.root.quit, "#cc0000")
        
    def start_day(self):
        """Start a day - call player's start_day"""
        self.clear_story()
        self.add_story(f"=== DAY {self.player.get_day()} ===\n\n", "#00ff00")
        
        # Try to call the actual start_day method
        try:
            # Redirect stdout to capture game output
            import io
            old_stdout = sys.stdout
            sys.stdout = buffer = io.StringIO()
            
            # Call the actual game's start_day
            self.player.start_day()
            
            # Get the output
            output = buffer.getvalue()
            sys.stdout = old_stdout
            
            if output:
                self.add_story(output)
        except Exception as e:
            self.add_story(f"Error calling start_day: {e}\n", "#ff0000")
            
        # Show day menu
        self.show_day_menu()
        self.refresh_stats()
        
    def show_day_menu(self):
        """Show day action choices"""
        self.clear_choices()
        
        # Check what's available based on player state
        self.add_choice("🏪 Visit Store", self.visit_store, "#0099cc")
        
        if self.player.get_mechanic_visits() > 0:
            self.add_choice("🔧 Visit Mechanic", self.visit_mechanic, "#cc6600")
            
        self.add_choice("🌳 Explore", self.explore_random, "#00cc66")
        self.add_choice("📊 Check Status", lambda: self.player.status(), "#cc9900")
        self.add_choice("⏩ End Day", self.end_day, "#6666cc")
        
    def visit_store(self):
        """Visit convenience store"""
        self.clear_story()
        self.add_story("KYLE'S 24-HOUR CONVENIENCE STORE\n\n", "#00ccff")
        
        # Try to call visit_convenience_store
        try:
            import io
            old_stdout = sys.stdout
            sys.stdout = buffer = io.StringIO()
            
            self.player.visit_convenience_store()
            
            output = buffer.getvalue()
            sys.stdout = old_stdout
            
            if output:
                self.add_story(output)
        except Exception as e:
            self.add_story(f"Store system: {e}\n", "#ffcc00")
            self.add_story("(Basic store - full integration coming)\n\n", "#666666")
            
        self.refresh_stats()
        self.clear_choices()
        self.add_choice("← Back", self.show_day_menu, "#666666")
        
    def visit_mechanic(self):
        """Visit mechanic"""
        self.clear_story()
        try:
            # Try Tom first
            import io
            old_stdout = sys.stdout
            sys.stdout = buffer = io.StringIO()
            
            self.player.visit_tom()
            
            output = buffer.getvalue()
            sys.stdout = old_stdout
            
            if output:
                self.add_story(output)
        except Exception as e:
            self.add_story(f"Mechanic not yet available: {e}\n", "#ffcc00")
            
        self.refresh_stats()
        self.clear_choices()
        self.add_choice("← Back", self.show_day_menu, "#666666")
        
    def explore_random(self):
        """Trigger random day event"""
        self.clear_story()
        try:
            import io
            old_stdout = sys.stdout
            sys.stdout = buffer = io.StringIO()
            
            self.player.day_event()
            
            output = buffer.getvalue()
            sys.stdout = old_stdout
            
            if output:
                self.add_story(output)
            else:
                self.add_story("Nothing interesting happens.\n", "#aaaaaa")
        except Exception as e:
            self.add_story(f"Exploration: {e}\n", "#ff0000")
            
        self.refresh_stats()
        self.clear_choices()
        self.add_choice("Continue", self.show_day_menu, "#666666")
        
    def end_day(self):
        """End day and go to night"""
        self.clear_story()
        try:
            import io
            old_stdout = sys.stdout
            sys.stdout = buffer = io.StringIO()
            
            self.player.end_day()
            
            output = buffer.getvalue()
            sys.stdout = old_stdout
            
            if output:
                self.add_story(output)
        except Exception as e:
            self.add_story(f"Day ended.\n", "#aaaaaa")
            
        self.add_story("\nEvening approaches. Casino is opening...\n\n", "#ffcc00")
        
        self.refresh_stats()
        self.clear_choices()
        self.add_choice("🎰 Go to Casino", self.start_night, "#ff0000")
        self.add_choice("😴 Skip Tonight", self.skip_night, "#666666")
        
    def start_night(self):
        """Start night/casino"""
        self.clear_story()
        self.add_story("=" * 60 + "\n", "#ff0000")
        self.add_story("THE CASINO\n", "#ff0000")
        self.add_story("=" * 60 + "\n\n", "#ff0000")
        
        try:
            import io
            old_stdout = sys.stdout
            sys.stdout = buffer = io.StringIO()
            
            self.player.start_night()
            
            output = buffer.getvalue()
            sys.stdout = old_stdout
            
            if output:
                self.add_story(output)
        except Exception as e:
            self.add_story("You enter the casino...\n")
            
        self.clear_choices()
        self.add_choice("♠️ Play Blackjack", self.play_blackjack, "#ff0000")
        self.add_choice("🚪 Leave", self.leave_casino, "#666666")
        
    def play_blackjack(self):
        """Start blackjack game"""
        self.clear_story()
        self.add_story("BLACKJACK TABLE\n\n", "#ff0000")
        
        # Try to start actual blackjack game
        try:
            # This would integrate with blackjack.py
            self.add_story("(Integrating with blackjack.py...)\n\n", "#ffcc00")
            self.add_story(f"Your balance: ${self.player.get_balance():,.2f}\n\n")
            
            # Placeholder for now
            self.add_story("Full blackjack integration coming.\n", "#666666")
            self.add_story("Will use your existing blackjack.py logic.\n\n", "#666666")
            
        except Exception as e:
            self.add_story(f"Blackjack error: {e}\n", "#ff0000")
            
        self.clear_choices()
        self.add_choice("← Back to Casino", self.start_night, "#666666")
        
    def leave_casino(self):
        """Leave casino"""
        self.clear_story()
        self.add_story("You leave the casino and return to your car.\n\n")
        
        # Increment day
        try:
            self.player.increment_day()
        except:
            pass
            
        self.refresh_stats()
        self.clear_choices()
        self.add_choice("💤 Sleep (Next Day)", self.start_day, "#6666cc")
        
    def skip_night(self):
        """Skip casino"""
        self.clear_story()
        self.add_story("You decide not to gamble tonight.\n", "#aaaaaa")
        
        try:
            self.player.increment_day()
        except:
            pass
            
        self.refresh_stats()
        self.clear_choices()
        self.add_choice("💤 Sleep (Next Day)", self.start_day, "#6666cc")
        
    def show_full_stats(self):
        """Show stats window"""
        stats_win = tk.Toplevel(self.root)
        stats_win.title("Statistics")
        stats_win.geometry("600x500")
        stats_win.configure(bg="#2d2d2d")
        
        tk.Label(stats_win, text="📊 PLAYER STATISTICS", font=("Arial", 16, "bold"),
                fg="#ffffff", bg="#2d2d2d").pack(pady=20)
        
        stats_text = scrolledtext.ScrolledText(stats_win, wrap=tk.WORD,
                                               font=("Courier New", 11),
                                               bg="#1a1a1a", fg="#ffffff",
                                               padx=20, pady=20)
        stats_text.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Get actual stats from player
        try:
            import io
            old_stdout = sys.stdout
            sys.stdout = buffer = io.StringIO()
            
            self.player.status()
            
            output = buffer.getvalue()
            sys.stdout = old_stdout
            
            stats_text.insert(1.0, output if output else "Stats loading...")
        except Exception as e:
            stats_text.insert(1.0, f"Stats: {e}")
            
        stats_text.config(state=tk.DISABLED)
        
        tk.Button(stats_win, text="Close", command=stats_win.destroy,
                 font=("Arial", 11), bg="#4a4a4a", fg="white",
                 padx=30, pady=10).pack(pady=10)
        
    def show_inventory(self):
        """Show inventory"""
        try:
            import io
            old_stdout = sys.stdout
            sys.stdout = buffer = io.StringIO()
            
            # Try to display inventory
            print(f"Balance: ${self.player.get_balance():,.2f}\n")
            print("Items: (Inventory system integrating...)")
            
            output = buffer.getvalue()
            sys.stdout = old_stdout
            
            messagebox.showinfo("Inventory", output)
        except Exception as e:
            messagebox.showinfo("Inventory", f"Inventory: {e}")
            
    def show_companions_window(self):
        """Show companions"""
        try:
            import io
            old_stdout = sys.stdout
            sys.stdout = buffer = io.StringIO()
            
            self.player.show_companions()
            
            output = buffer.getvalue()
            sys.stdout = old_stdout
            
            messagebox.showinfo("Companions", output if output else "No companions yet")
        except Exception as e:
            messagebox.showinfo("Companions", "No companions yet")
            
    def show_achievements_window(self):
        """Show achievements"""
        try:
            import io
            old_stdout = sys.stdout
            sys.stdout = buffer = io.StringIO()
            
            self.player.show_achievements()
            
            output = buffer.getvalue()
            sys.stdout = old_stdout
            
            messagebox.showinfo("Achievements", output if output else "No achievements yet")
        except Exception as e:
            messagebox.showinfo("Achievements", "Achievement system loading...")
            
    def show_tutorial(self):
        """Show tutorial"""
        tut_win = tk.Toplevel(self.root)
        tut_win.title("How to Play")
        tut_win.geometry("700x600")
        tut_win.configure(bg="#2d2d2d")
        
        tk.Label(tut_win, text="📖 HOW TO PLAY", font=("Arial", 16, "bold"),
                fg="#ffffff", bg="#2d2d2d").pack(pady=20)
        
        tut_text = scrolledtext.ScrolledText(tut_win, wrap=tk.WORD,
                                            font=("Arial", 11),
                                            bg="#1a1a1a", fg="#ffffff",
                                            padx=20, pady=20)
        tut_text.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        tutorial = """
OBJECTIVE:
Turn your $50 into $1,000,000 through blackjack and survival.

STATS:
• HP: Your health. Don't let it hit 0.
• Sanity: Your mental state. Low sanity = madness.
• Balance: Your money. Manage it wisely.

GAMEPLAY:
• Day: Visit stores, mechanics, explore
• Night: Go to casino and gamble
• Make choices that affect your story

TIPS:
• Manage your health and sanity carefully
• Don't bet more than you can afford to lose
• Build relationships with NPCs
• There are 8 different endings based on your choices

Good luck!
        """
        
        tut_text.insert(1.0, tutorial)
        tut_text.config(state=tk.DISABLED)
        
        tk.Button(tut_win, text="Close", command=tut_win.destroy,
                 font=("Arial", 11), bg="#4a4a4a", fg="white",
                 padx=30, pady=10).pack(pady=10)


# ===== MAIN ENTRY POINT =====
def main():
    root = tk.Tk()
    app = BlackjackGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
