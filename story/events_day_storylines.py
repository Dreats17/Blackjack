import random
import time
import sys
import typer
import msvcrt
from colorama import Fore, Back, Style, init
init(convert=True)

PAR = "\n\n"

type = typer.Type()
ask = typer.Ask()

# all the pretty colors
def red(text):
    return (Fore.RED + text + Fore.WHITE)

def green(text):
    return (Fore.GREEN + text + Fore.WHITE)
            
def magenta(text):
    return (Fore.MAGENTA + text + Fore.WHITE)

def yellow(text):
    return (Fore.YELLOW + text + Fore.WHITE)

def cyan(text):
    return (Fore.CYAN + text + Fore.WHITE)
            
def bright(text):
    return (Style.BRIGHT + text + Style.NORMAL)

def italic(text):
    return (Style.DIM + text + Style.NORMAL)

def item(text):
    return magenta(bright(text))

def open_quote(text):
    return ("\"" + text)

def close_quote(text):
    return (text + "\"")

def quote(text):
    return ("\"" + text + "\"")

def space_quote(text):
    return ("\"" + text + "\" ")

class DayStorylinesMixin:
    """Storyline events: multi-part chain events and crossovers"""

    def gift_from_suzy(self):
        # EVENT: Suzy's GOOD ending - she gives you a handmade stuffed animal gift
        # CONDITION: Must have completed Suzy storyline (has favorite animal) AND not met "Suzy Finale"
        # EFFECTS: Receive "Suzy's Gift" item + restore 5-8 sanity; emotional farewell as Suzy moves away
        # CHAIN: Suzy Storyline GOOD FINALE
        # Only triggers if Suzy storyline is complete (has favorite animal)
        # This is the GOOD ending - requires having been kind to Suzy
        if self.get_favorite_animal() == None or self.has_met("Suzy Finale"):
            self.day_event()
            return
        
        self.meet("Suzy Finale")
        
        type.type("An unusual sound-not sneakers on concrete, but the crunch of grass. ")
        type.type("You sit up and see Suzy standing outside your wagon, holding something behind her back.")
        print("\n")
        type.type("She's not jump roping. For the first time ever, she's standing completely still.")
        print("\n")
        type.type(quote("Hi, " + self._name + ". I made you something."))
        print("\n")
        type.type("Suzy pulls out a small stuffed animal from behind her back. ")
        type.type("It's a " + self.get_favorite_animal() + ", crudely sewn together with mismatched fabric, but clearly made with love. ")
        type.type("The fabric is " + self.get_favorite_color() + ", your favorite color.")
        print("\n")
        type.type(quote("I remembered everything you told me. Your favorite color, your favorite animal. I made it myself! Do you like it?"))
        print("\n")
        type.type("You take the stuffed " + self.get_favorite_animal() + ". Despite its imperfect stitching, it's one of the most thoughtful gifts anyone has ever given you.")
        print("\n")
        type.type(quote("I wanted to say thank you. For always being nice to me. "))
        type.type(quote("Most grown-ups ignore me, or tell me to go away. But you always talked to me like I was a real person."))
        print("\n")
        type.type("Suzy sniffles a little.")
        print("\n")
        type.type(quote("I hope you find what you're looking for, " + self._name + ". I really do."))
        print("\n")
        type.type("Before you can respond, Suzy picks up her jump rope and starts bouncing away.")
        print("\n")
        type.type(quote("Bye bye! Maybe I'll see you again someday! But probably not. "))
        type.type(quote("I'm moving away with my aunt. She found me! She's really nice. "))
        type.type(quote("I'll think of you when I see " + self.get_favorite_animal() + "s!"))
        print("\n")
        type.type("And with that, Suzy jump ropes into the distance for the last time, disappearing around the corner. ")
        type.type("You look down at the stuffed " + self.get_favorite_animal() + " in your hands.")
        print("\n")
        type.type(yellow(bright("Some goodbyes are harder than others.")))
        self.add_item("Suzy's Gift")
        self.restore_sanity(random.choice([5, 6, 7, 8]))  # Deeply restores sanity
        print("\n")

    def suzy_the_snitch(self):
        # EVENT: Suzy's BAD ending - she reports you to police using info you shared
        # CONDITION: Must have completed Suzy storyline (has favorite animal) AND not met "Suzy Finale"
        # EFFECTS: INSTANT DEATH - arrested and jailed based on info you told Suzy
        # CHAIN: Suzy Storyline BAD FINALE
        # BRUTAL: Causes death
        # Only triggers if Suzy storyline is complete AND this is checked
        # This is the BAD ending - happens if player was mean to Suzy
        if self.get_favorite_animal() == None or self.has_met("Suzy Finale"):
            self.day_event()
            return
        
        self.meet("Suzy Finale")
        
        type.type("A car engine and flashing lights. Right outside. A police cruiser has pulled up right next to your wagon. Your heart sinks.")
        print("\n")
        type.type("A cop steps out, notepad in hand. And there, in the passenger seat of the cruiser, sits Suzy, still holding her jump rope.")
        print("\n")
        type.type("The cop approaches your window.")
        print("\n")
        type.type(quote("Are you " + self._name + "? This young lady here says she knows you."))
        print("\n")
        type.type("Suzy waves at you through the window, an innocent smile on her face.")
        print("\n")
        type.type(quote("That's him, officer! The homeless man I told you about! "))
        type.type(quote("His favorite color is " + self.get_favorite_color() + " and his favorite animal is a " + self.get_favorite_animal() + "! He told me EVERYTHING!"))
        print("\n")
        type.type("The cop looks at his notepad, then back at you.")
        print("\n")
        type.type(quote("Sir, we've had reports of someone matching your description involved in some... questionable activities in this area. "))
        type.type(quote("We're going to need you to come with us for questioning."))
        print("\n")
        type.type("Suzy presses her face against the police car window.")
        print("\n")
        type.type(quote("Bye bye, " + self._name + "! I hope you enjoy jail! They probably have " + self.get_favorite_animal() + "s there! Maybe!"))
        print("\n")
        type.type("Before you can protest or explain, you're in handcuffs and being led to the back of the cruiser. Suzy waves at you the whole time.")
        print("\n")
        type.slow(red(bright("You spend the rest of your days in a cell, thinking about how you probably shouldn't have trusted a jump-roping little girl with all your personal information. The last thing you remember before everything fades to black is the distant sound of sneakers on concrete, and a jump rope hitting the ground.")))
        print("\n")
        self.kill()


    # ADDITIONAL NEW EVENTS
    # ==========================================

    # POOR DAY EVENTS - Everytime

    def hermit_trail_discovery(self):
        """First event: finding the trail marked on the Worn Map"""
        if not self.has_item("Worn Map"):
            self.day_event()
            return
        if self.has_met("Hermit Trail Found"):
            self.day_event()
            return
        
        type.type("You're parked near the edge of town when you remember the " + cyan(bright("Worn Map")) + " you bought.")
        print("\n")
        type.type("You unfold it on the hood. The paper is brittle, the ink faded to brown. ")
        type.type("But the trails are clear — someone drew these from memory, over and over, perfecting the routes.")
        print("\n")
        type.type("One trail is marked with a star. Just a few miles from here.")
        print("\n")
        type.type("1. Follow the trail")
        print()
        type.type("2. Not worth the risk")
        print()
        type.type("Choose: ")
        choice = None
        while choice is None:
            try:
                choice = int(input())
            except ValueError:
                type.type("Pick a number: ")
        print()
        
        if choice == 1:
            type.type("You lock the car and head into the woods. The trail is overgrown but followable.")
            print("\n")
            type.type("After twenty minutes of pushing through brush, you find it: a small clearing. ")
            type.type("There's a fire pit, long cold. A lean-to made of branches and tarp. ")
            type.type("Someone lived here. For a long time.")
            print("\n")
            type.type("On a flat rock near the fire pit, weighted down with a stone, is a leather-bound journal.")
            print("\n")
            type.type("You pick it up. It's dense with handwriting. Drawings. Recipes. Survival notes.")
            print("\n")
            type.type("You found the " + cyan(bright("Hermit's Journal")) + ".")
            self.add_item("Hermit's Journal")
            self.meet("Hermit Trail Found")
            self.add_danger("Hermit Camp Return")
            self.restore_sanity(5)
            print("\n")
        else:
            type.type("You fold the map back up. Maybe another day.")
            print("\n")

    def hermit_camp_return(self):
        """Second event: returning to the camp and finding a walking stick"""
        if not self.has_met("Hermit Trail Found") or not self.has_danger("Hermit Camp Return"):
            self.day_event()
            return
        
        type.type("Something's been nagging at you. The hermit's camp. There was more to find there.")
        print("\n")
        type.type("You drive back to the trailhead and follow the path again. Easier this time — you know the way.")
        print("\n")
        type.type("The camp looks different in this light. You notice things you missed before.")
        print("\n")
        type.type("Leaning against the lean-to is a hand-carved walking stick. ")
        type.type("The wood is smooth, polished by years of use. There are notches carved into it — ")
        type.type("hundreds of them. Days? Miles? Memories?")
        print("\n")
        type.type("You take the " + cyan(bright("Carved Walking Stick")) + ". It feels right in your hand.")
        self.add_item("Carved Walking Stick")
        self.lose_danger("Hermit Camp Return")
        self.add_danger("Hermit Journal Study")
        self.restore_sanity(3)
        print("\n")
        
        type.type("As you leave, you notice boot prints in the mud. Fresh ones. ")
        type.type("Someone else has been here recently.")
        self.lose_sanity(2)
        print("\n")

    def hermit_journal_study(self):
        """Third event: reading the journal reveals herbal medicine knowledge"""
        if not self.has_item("Hermit's Journal") or not self.has_danger("Hermit Journal Study"):
            self.day_event()
            return
        
        type.type("You spend the morning reading the " + cyan(bright("Hermit's Journal")) + " in the front seat of your car.")
        print("\n")
        type.type("The handwriting changes over the years. Starts shaky, gets confident, then shaky again.")
        print("\n")
        type.type("The hermit was a pharmacist. Before everything fell apart. ")
        type.type("The journal is full of herbal remedy recipes — plants that grow wild around here.")
        print("\n")
        type.type("You tear out a few pages of instructions and gather what you can from the roadside:")
        print("\n")
        type.type("Plantain leaves for cuts. Willow bark for pain. Chamomile for sleep. ")
        type.type("You bundle them into a cloth and tie it shut.")
        print("\n")
        type.type("You made a " + cyan(bright("Herbal Pouch")) + ".")
        self.add_item("Herbal Pouch")
        self.lose_danger("Hermit Journal Study")
        self.add_danger("Hermit Trail Stranger")
        self.heal(10)
        self.restore_sanity(5)
        print("\n")
        
        type.type("The last entry in the journal reads: " + quote("If you found this, check the hollow oak. Third trail marker. I left something for the next one."))
        print("\n")

    def hermit_trail_stranger(self):
        """Fourth event: encountering someone else who's been following the trail"""
        if not self.has_danger("Hermit Trail Stranger"):
            self.day_event()
            return
        
        type.type("You're heading back to the hermit trail when you see someone already there.")
        print("\n")
        type.type("A woman in a park ranger jacket, kneeling at the fire pit. She's studying it.")
        print("\n")
        type.type("She sees you and stands up fast. Her hand goes to her belt.")
        print("\n")
        type.type(quote("This is private land. What are you doing out here?"))
        print("\n")
        
        has_journal = self.has_item("Hermit's Journal")
        has_stick = self.has_item("Carved Walking Stick")
        
        if has_journal and has_stick:
            type.type("She notices the " + cyan(bright("Carved Walking Stick")) + " in your hand. Her expression changes.")
            print("\n")
            type.type(quote("Wait. You have his walking stick? And the journal?"))
            print("\n")
            type.type("She relaxes. Sits down on a rock. Looks tired.")
            print("\n")
            type.type(quote("His name was Edgar. He was my father. He disappeared three years ago."))
            print("\n")
            type.type(quote("I've been looking for his camp for months. You found it before I did."))
            print("\n")
            type.type("1. Give her the journal")
            print()
            type.type("2. Keep it (you need it more)")
            print()
            type.type("Choose: ")
            choice = None
            while choice is None:
                try:
                    choice = int(input())
                except ValueError:
                    type.type("Pick a number: ")
            print()
            
            if choice == 1:
                type.type("You hand her the journal. She holds it like it's made of glass.")
                print("\n")
                type.type(quote("Thank you. You have no idea what this means to me."))
                print("\n")
                type.type("She reaches into her pack and pulls out a pair of " + cyan(bright("Night Vision Scope")) + ".")
                print("\n")
                type.type(quote("My dad's. He used them for stargazing. Take them. Please."))
                self.use_item("Hermit's Journal")
                self.add_item("Night Vision Scope")
                self.meet("Hermit Daughter Met")
                self.restore_sanity(10)
                print("\n")
            else:
                type.type("You shake your head. " + quote("I'm sorry. I need this. Survival stuff."))
                print("\n")
                type.type("She stares at you. Not angry. Just... sad.")
                print("\n")
                type.type(quote("I understand. You're living out here too, aren't you?"))
                print("\n")
                type.type("She tells you about the hollow oak anyway. Third trail marker.")
                self.lose_sanity(3)
                print("\n")
        else:
            type.type(quote("I'm just passing through,") + " you say.")
            print("\n")
            type.type("She doesn't believe you. But she doesn't press it.")
            print("\n")
            type.type(quote("Well, if you see anything unusual out here — journals, campsites — let me know. ") +
                      quote("I'm looking for someone."))
            print("\n")
            type.type("She hands you a card. " + yellow("Ranger Diana Marsh."))
            self.meet("Ranger Diana")
            print("\n")
        
        self.lose_danger("Hermit Trail Stranger")
        self.add_danger("Hermit Hollow Oak")

    def hermit_hollow_oak(self):
        """Fifth event (finale): finding the hollow oak stash"""
        if not self.has_danger("Hermit Hollow Oak"):
            self.day_event()
            return
        if self.has_met("Hollow Oak Found"):
            self.day_event()
            return
        
        type.type("Third trail marker. You've been counting.")
        print("\n")
        type.type("There it is — a massive oak tree, split by lightning long ago. The trunk is hollow.")
        print("\n")
        
        if self.has_item("Carved Walking Stick"):
            type.type("You use the " + cyan(bright("Carved Walking Stick")) + " to poke inside the hollow. ")
            type.type("Nothing bites you. Good start.")
            print("\n")
        
        type.type("You reach inside. Your hand closes around a waterproof bag, wedged deep in the bark.")
        print("\n")
        type.type("Inside the bag:")
        print("\n")
        
        cash = random.randint(100, 300)
        type.type("• " + green("${:,}".format(cash)) + " in weathered bills")
        print()
        type.type("• A small survival tin with matches, wire, and a compass")
        print()
        type.type("• A note: " + quote("For whoever needs this next. Pass it on. — E."))
        print("\n")
        
        self.change_balance(cash)
        self.add_item("Hollow Tree Stash")
        self.meet("Hollow Oak Found")
        self.lose_danger("Hermit Hollow Oak")
        self.restore_sanity(8)
        
        if self.has_met("Hermit Daughter Met"):
            type.type("You think about Diana. Her father left this for strangers. ")
            type.type("He spent his last years taking care of people he'd never meet.")
            print("\n")
            type.type("You sit at the base of the oak for a while. The world feels a little less cruel.")
            self.restore_sanity(5)
        else:
            type.type("You sit at the base of the oak. The forest is quiet. The money helps. ")
            type.type("But the note helps more.")
        print("\n")

    # ==========================================
    # CHAIN 2: THE MIDNIGHT RADIO (5 events)
    # Signal Booster → strange broadcast → 
    # Strange Frequency Dial → Static Recorder →
    # Pirate Radio Flyer → Tinfoil Hat
    # ==========================================

    def midnight_radio_signal(self):
        """First event: picking up a strange broadcast"""
        if not self.has_item("Signal Booster"):
            self.day_event()
            return
        if self.has_met("Midnight Radio"):
            self.day_event()
            return
        
        type.type("As the sun goes down, you're fiddling with your car radio. The " + cyan(bright("Signal Booster")) + " you attached is pulling in stations from miles away.")
        print("\n")
        type.type("Classical music. Talk radio. Static. Static. More static.")
        print("\n")
        type.type("Then — something. Between stations. A voice, calm and measured:")
        print("\n")
        type.type(quote("...if you can hear this, you're closer than you think. Frequency 108.7. Midnight. Every night..."))
        print("\n")
        type.type("The signal cuts out. Just static again.")
        print("\n")
        type.type("You try to find it again. Gone. But you remember the number: " + yellow(bright("108.7")) + ".")
        print("\n")
        self.meet("Midnight Radio")
        self.add_danger("Midnight Radio Frequency")
        self.lose_sanity(2)
        self.restore_sanity(4)  # Net positive — curiosity is exciting
        print("\n")

    def midnight_radio_frequency(self):
        """Second event: tuning in at midnight"""
        if not self.has_danger("Midnight Radio Frequency"):
            self.day_event()
            return
        
        type.type("Midnight. You tune to 108.7. Your hands are shaking slightly. Why are you nervous?")
        print("\n")
        type.type("Static. Static. Then...")
        print("\n")
        type.type("The voice returns. Clearer this time.")
        print("\n")
        type.type(quote("Welcome back, night owl. You found us again. That means you're listening."))
        print("\n")
        type.type(quote("This is Radio Nowhere. We broadcast for the ones who can't sleep. ") +
                  quote("The ones living in their cars, their couches, their failures."))
        print("\n")
        type.type(quote("Tonight's topic: what do you hold onto when everything else is gone?"))
        print("\n")
        type.type("The broadcast continues for an hour. Stories from callers. Anonymous voices sharing their truths.")
        print("\n")
        type.type("At the end, the host says: " + quote("If you want to find us, check the telephone pole on 5th and Birch. We left you something."))
        print("\n")
        
        type.type("A small " + cyan(bright("Strange Frequency Dial")) + " is taped to your antenna when you wake up.")
        print("\n")
        type.type("Someone was here. While you slept. They knew where you were.")
        self.add_item("Strange Frequency Dial")
        self.lose_danger("Midnight Radio Frequency")
        self.add_danger("Midnight Radio Pole")
        self.lose_sanity(3)
        print("\n")

    def midnight_radio_pole(self):
        """Third event: checking the telephone pole"""
        if not self.has_danger("Midnight Radio Pole"):
            self.day_event()
            return
        
        type.type("5th and Birch. You drive there in the afternoon. It's a normal intersection.")
        print("\n")
        type.type("Except for the telephone pole. It's covered in layers of old flyers, stapled over each other.")
        print("\n")
        type.type("You peel them back. Under decades of yard sale ads and lost cat posters, you find it:")
        print("\n")
        type.type("A " + cyan(bright("Pirate Radio Flyer")) + ". Hand-drawn. It shows a map to a building downtown.")
        print("\n")
        type.type(quote("Radio Nowhere. We see you. Come see us. Bring the dial."))
        print("\n")
        self.add_item("Pirate Radio Flyer")
        self.lose_danger("Midnight Radio Pole")
        self.add_danger("Midnight Radio Visit")
        self.restore_sanity(2)
        print("\n")

    def midnight_radio_visit(self):
        """Fourth event: visiting the pirate radio station"""
        if not self.has_danger("Midnight Radio Visit"):
            self.day_event()
            return
        if not self.has_item("Pirate Radio Flyer") or not self.has_item("Strange Frequency Dial"):
            self.day_event()
            return
        
        type.type("You follow the map on the " + cyan(bright("Pirate Radio Flyer")) + ". ")
        type.type("It leads to a condemned building downtown. Boarded windows. Graffiti.")
        print("\n")
        type.type("There's a door in the back. You knock.")
        print("\n")
        type.type("A slot opens. Eyes peer out.")
        print("\n")
        type.type(quote("You got the dial?"))
        print("\n")
        type.type("You hold up the " + cyan(bright("Strange Frequency Dial")) + ". The slot closes. The door opens.")
        print("\n")
        type.type("Inside: a full pirate radio setup. Speakers, wires, a mixing board made of scrap parts. ")
        type.type("Three people sit around a microphone. They look like you — tired, worn, but alive.")
        print("\n")
        type.type("The host — a woman with silver hair and kind eyes — stands and extends her hand.")
        print("\n")
        type.type(quote("I'm Vera. Welcome to Radio Nowhere. We've been hoping you'd come."))
        print("\n")
        type.type(quote("Everyone who listens long enough, finds us. That's how we know you're one of us."))
        print("\n")
        
        type.type("They offer you something to eat. Real food. Hot coffee.")
        print("\n")
        type.type("For the first time in a long time, you feel like you belong somewhere.")
        print("\n")
        
        type.type("Vera gives you a " + cyan(bright("Static Recorder")) + " — a small device for recording messages to broadcast.")
        print("\n")
        type.type(quote("Record something when you're ready. Your story. Your truth. Whenever you need to be heard."))
        self.add_item("Static Recorder")
        self.meet("Radio Nowhere Member")
        self.lose_danger("Midnight Radio Visit")
        self.add_danger("Midnight Radio Broadcast")
        self.heal(10)
        self.restore_sanity(15)
        print("\n")

    def midnight_radio_broadcast(self):
        """Fifth event (finale): recording your own broadcast"""
        if not self.has_danger("Midnight Radio Broadcast"):
            self.day_event()
            return
        if not self.has_item("Static Recorder"):
            self.day_event()
            return
        if self.has_met("Radio Broadcast Done"):
            self.day_event()
            return
        
        type.type("It's evening. You're sitting in the car. The " + cyan(bright("Static Recorder")) + " is in your hand.")
        print("\n")
        type.type("You've been staring at it for twenty minutes. The red record button glows in the dark.")
        print("\n")
        type.type("1. Record your story")
        print()
        type.type("2. Not ready yet (skip for now)")
        print()
        type.type("Choose: ")
        choice = None
        while choice is None:
            try:
                choice = int(input())
            except ValueError:
                type.type("Pick a number: ")
        print()
        
        if choice == 2:
            type.type("You put the recorder down. Not tonight. Maybe tomorrow.")
            print("\n")
            return  # Don't remove the danger — event can fire again
        
        type.type("You press record. The light turns solid red.")
        print("\n")
        type.type("And you talk.")
        print("\n")
        type.type("You talk about the car. The blackjack tables. The convenience store kid who knows your name. ")
        type.type("The animal you adopted. The things you've lost. The things you've found.")
        print("\n")
        type.type("You talk about the nights when you couldn't sleep and the mornings when you couldn't wake up.")
        print("\n")
        chain_details = []
        if self.has_met("Hermit Trail Found"):
            chain_details.append("the map")
        if self.has_met("Junkyard Artisan Met"):
            chain_details.append("the junkyard")
        if self.has_met("Missing Dogs Found"):
            chain_details.append("the dogs")
        if chain_details:
            type.type("You talk about " + ", ".join(chain_details) + ". Things you've seen out here.")
            print("\n")
        type.type("When you stop, the recorder clicks off automatically. You're crying. When did that start?")
        print("\n")
        type.type("Later that night, you tune to 108.7. And you hear yourself.")
        print("\n")
        type.type("Your voice, out there in the dark, reaching whoever needs it. The next one. The next person in their car.")
        print("\n")
        
        type.type("Vera's voice follows yours: " + quote("That was our newest member. You're not alone out there. Radio Nowhere. Signing off."))
        print("\n")
        
        type.type("You also find a " + cyan(bright("Tinfoil Hat")) + " in your glove compartment with a note from Vera: ")
        type.type(quote("For the bad signal days. — V"))
        self.add_item("Tinfoil Hat")
        self.meet("Radio Broadcast Done")
        self.lose_danger("Midnight Radio Broadcast")
        self.restore_sanity(20)
        print("\n")

    # ==========================================
    # CHAIN 3: THE JUNKYARD ARTISAN (5 events)
    # Welding Goggles → meet artisan → learn craft →
    # Scrap Metal Rose → Artisan's Toolkit → Junkyard Crown
    # ==========================================

    def junkyard_artisan_meet(self):
        """First event: discovering the artisan at the junkyard"""
        if not self.has_item("Welding Goggles"):
            self.day_event()
            return
        if self.has_met("Junkyard Artisan Met"):
            self.day_event()
            return
        
        type.type("You're poking around the junkyard behind the shopping plaza, looking for useful scraps.")
        print("\n")
        type.type("That's when you hear it — a rhythmic clanging. Metal on metal. Someone's working back here.")
        print("\n")
        type.type("You follow the sound to a corner of the yard where an old man is bent over a workbench. ")
        type.type("He's welding something. Sparks fly like fireflies.")
        print("\n")
        type.type("He doesn't look up. " + quote("You gonna stand there or you gonna make yourself useful?"))
        print("\n")
        type.type("He glances at your " + cyan(bright("Welding Goggles")) + ". His eyebrows go up.")
        print("\n")
        type.type(quote("Well, well. You came prepared. That's more than most. Name's Gideon."))
        print("\n")
        type.type("He shows you what he's making: a bird made entirely of bent nails and bottle caps. It's beautiful.")
        print("\n")
        type.type(quote("Junk becomes art if you care enough. Most people don't. Do you?"))
        print("\n")
        type.type("1. " + quote("Teach me."))
        print()
        type.type("2. " + quote("I'm just looking for scrap."))
        print()
        type.type("Choose: ")
        choice = None
        while choice is None:
            try:
                choice = int(input())
            except ValueError:
                type.type("Pick a number: ")
        print()
        
        if choice == 1:
            type.type("Gideon smiles. It transforms his whole face.")
            print("\n")
            type.type(quote("Good answer. Come back when you're ready to learn. Bring something to work with."))
            self.meet("Junkyard Artisan Met")
            self.add_danger("Junkyard Lesson One")
            self.restore_sanity(5)
        else:
            type.type(quote("Fair enough. But the offer stands. I'm here every day."))
            self.meet("Junkyard Artisan Met")
            self.add_danger("Junkyard Lesson One")
        print("\n")

    def junkyard_lesson_one(self):
        """Second event: first lesson — making a scrap metal rose"""
        if not self.has_danger("Junkyard Lesson One"):
            self.day_event()
            return
        
        type.type("You find Gideon at his workbench, sanding a piece of copper pipe. He nods when he sees you.")
        print("\n")
        type.type(quote("Today's lesson: beauty from nothing. We're making a rose."))
        print("\n")
        type.type("He hands you a hammer, tin snips, and a piece of sheet metal. ")
        type.type("For the next two hours, he guides you through cutting petals, curving them, layering them.")
        print("\n")
        type.type("Your hands hurt. Your fingers get nicked. But slowly, impossibly, a rose takes shape.")
        print("\n")
        type.type("It's rough. Imperfect. But it's yours.")
        print("\n")
        type.type("You made a " + cyan(bright("Scrap Metal Rose")) + ".")
        self.add_item("Scrap Metal Rose")
        self.lose_danger("Junkyard Lesson One")
        self.add_danger("Junkyard Lesson Two")
        self.restore_sanity(8)
        print("\n")
        
        type.type("Gideon looks at it critically. Then nods.")
        print("\n")
        type.type(quote("Not bad. Not good either. But not bad. Come back. We'll make you better."))
        print("\n")

    def junkyard_lesson_two(self):
        """Third event: second lesson — real craftsmanship, earns Artisan's Toolkit"""
        if not self.has_danger("Junkyard Lesson Two"):
            self.day_event()
            return
        
        type.type("Gideon has a new project today. He's building a lamp from old car parts.")
        print("\n")
        type.type(quote("You made a flower last time. Today, we make something functional. ") +
                  quote("Art that works. That's the goal."))
        print("\n")
        type.type("He teaches you about joints, rivets, load-bearing connections. ")
        type.type("How to read metal — which pieces flex, which shatter, which hold.")
        print("\n")
        type.type("By the end, you haven't just made a lamp. You've learned a philosophy.")
        print("\n")
        type.type(quote("Things break. People break. But breaking isn't ending. ") +
                  quote("It's just... disassembly before reassembly."))
        print("\n")
        type.type("Gideon pulls out a leather roll of tools — hammers, files, pliers, a small welding torch.")
        print("\n")
        type.type(quote("These were mine when I was learning. Now they're yours."))
        print("\n")
        type.type("You got the " + cyan(bright("Artisan's Toolkit")) + ".")
        self.add_item("Artisan's Toolkit")
        self.lose_danger("Junkyard Lesson Two")
        self.add_danger("Junkyard Gideon Story")
        self.restore_sanity(10)
        self.heal(3)
        print("\n")

    def junkyard_gideon_story(self):
        """Fourth event: Gideon's backstory and a deeper connection"""
        if not self.has_danger("Junkyard Gideon Story"):
            self.day_event()
            return
        
        type.type("When you arrive at the junkyard, Gideon isn't working. He's sitting in a lawn chair, staring at the sky.")
        print("\n")
        type.type("He doesn't greet you. Just says:")
        print("\n")
        type.type(quote("Sit down. I want to tell you something."))
        print("\n")
        type.type("You sit. He talks.")
        print("\n")
        type.type(quote("I had a shop once. Twenty employees. Custom metalwork. Rich people paid me thousands ") +
                  quote("for gates, railings, sculptures."))
        print("\n")
        type.type(quote("Then my wife got sick. Then my business got sued. Then I got evicted. ") +
                  quote("Lost everything in eighteen months."))
        print("\n")
        type.type(quote("I lived in a van for three years. Right here in this junkyard. The owner let me stay ") +
                  quote("if I kept the scrap organized."))
        print("\n")
        type.type(quote("I started making things again because I had to do SOMETHING or my brain would eat itself alive."))
        print("\n")
        type.type("He looks at you.")
        print("\n")
        type.type(quote("Sound familiar?"))
        print("\n")
        type.type("You nod. It sounds very familiar.")
        print("\n")
        type.type(quote("You're gonna be okay. You know how I know? Because you're still showing up. ") +
                  quote("That's the whole secret. Just keep showing up."))
        print("\n")
        self.lose_danger("Junkyard Gideon Story")
        self.add_danger("Junkyard Masterpiece")
        self.restore_sanity(15)
        print("\n")

    def junkyard_masterpiece(self):
        """Fifth event (finale): creating a masterpiece together"""
        if not self.has_danger("Junkyard Masterpiece"):
            self.day_event()
            return
        if self.has_met("Junkyard Crown Made"):
            self.day_event()
            return
        
        type.type("Gideon greets you with something you've never seen from him: excitement.")
        print("\n")
        type.type(quote("I've been saving the good scrap. The chrome bumper pieces. The copper wire. ") +
                  quote("The brass fittings from that old boat engine."))
        print("\n")
        type.type(quote("Today, we make a masterpiece. Together."))
        print("\n")
        type.type("You work side by side for four hours. Cutting, bending, welding, polishing.")
        print("\n")
        type.type("What emerges is extraordinary: a crown. Made of twisted metal, gears, springs, and wire. ")
        type.type("It catches the light like jewelry. It weighs almost nothing.")
        print("\n")
        type.type("Gideon places it on your head.")
        print("\n")
        type.type(quote("Every king started as a pauper. You're not where you were. Remember that."))
        print("\n")
        type.type("You got the " + cyan(bright("Junkyard Crown")) + ".")
        self.add_item("Junkyard Crown")
        self.meet("Junkyard Crown Made")
        self.lose_danger("Junkyard Masterpiece")
        self.restore_sanity(20)
        self.heal(5)
        print("\n")
        
        if self.has_item("Scrap Metal Rose"):
            type.type("Gideon looks at the " + cyan(bright("Scrap Metal Rose")) + " you still carry.")
            print("\n")
            type.type(quote("You kept that? From your first lesson?"))
            print("\n")
            type.type("You nod.")
            print("\n")
            type.type("He looks away. You pretend not to see him wipe his eyes.")
            self.restore_sanity(5)
            print("\n")

    # ==========================================
    # CHAIN 4: THE LOST DOG FLYERS (5 events)
    # Dog Whistle → Stack of Flyers → find first dog →
    # find second dog → Torn Collar mystery →
    # Reunion Photo
    # ==========================================

    def lost_dog_flyers_found(self):
        """First event: finding lost dog flyers everywhere"""
        if self.has_met("Lost Dog Flyers"):
            self.day_event()
            return
        
        type.type("They're everywhere. Taped to lampposts, pinned to bulletin boards, shoved under windshield wipers.")
        print("\n")
        type.type("Lost dog flyers. Five different dogs. All missing from the same neighborhood.")
        print("\n")
        type.type("Each flyer has a phone number. Each number is the same: a local shelter.")
        print("\n")
        type.type("You grab a " + cyan(bright("Stack of Flyers")) + ". Something about this doesn't feel right. ")
        type.type("Five dogs from one block? That's not coincidence. That's a pattern.")
        self.add_item("Stack of Flyers")
        self.meet("Lost Dog Flyers")
        self.add_danger("Lost Dog Investigation")
        print("\n")

    def lost_dog_investigation(self):
        """Second event: investigating the disappearances"""
        if not self.has_danger("Lost Dog Investigation"):
            self.day_event()
            return
        
        type.type("You drive to the neighborhood from the flyers. Nice street. Manicured lawns. Quiet.")
        print("\n")
        type.type("Too quiet, actually. No barking. No dogs at all.")
        print("\n")
        type.type("You knock on a door. A worried-looking woman answers.")
        print("\n")
        type.type(quote("Are you from the shelter? Did you find Biscuit?"))
        print("\n")
        type.type("You show her the flyers. She tears up immediately.")
        print("\n")
        type.type(quote("Biscuit disappeared Tuesday. Mrs. Huang's poodle was gone Monday. The Petersons' lab — Wednesday. ") +
                  quote("Something is taking them. At night."))
        print("\n")
        
        if self.has_item("Dog Whistle"):
            type.type("You mention your " + cyan(bright("Dog Whistle")) + ". Her eyes light up.")
            print("\n")
            type.type(quote("Try the park behind the community center. If they're nearby, maybe they'll hear it. ") +
                      quote("Dogs can hear that thing from blocks away."))
            self.add_danger("Lost Dog Whistle Search")
        else:
            type.type("She gives you a description of each dog. You promise to keep an eye out.")
            self.add_danger("Lost Dog Whistle Search")
        
        self.lose_danger("Lost Dog Investigation")
        print("\n")

    def lost_dog_whistle_search(self):
        """Third event: searching for the dogs"""
        if not self.has_danger("Lost Dog Whistle Search"):
            self.day_event()
            return
        
        type.type("The park behind the community center. It's dusk. The grass is wet.")
        print("\n")
        
        if self.has_item("Dog Whistle"):
            type.type("You blow the " + cyan(bright("Dog Whistle")) + ". ")
            type.type("The sound is silent to you, but you feel the vibration in your teeth.")
            print("\n")
            type.type("Thirty seconds pass. Nothing.")
            print("\n")
            type.type("Then — barking. Distant, muffled, but unmistakable. Coming from under the old utility shed.")
            print("\n")
            type.type("You pull open the shed door. Inside, huddled together in the dark: three dogs. ")
            type.type("A poodle, a chocolate lab, and a small beagle. Skinny, scared, but alive.")
            print("\n")
            type.type("They've been trapped in here. The door locks from the outside.")
            print("\n")
            type.type("This wasn't an accident. Someone locked them in.")
            print("\n")
            type.type("On the ground near the dogs, you find a " + cyan(bright("Torn Collar")) + " — ")
            type.type("ripped off violently. The tag reads " + yellow("BISCUIT") + ".")
            self.add_item("Torn Collar")
            self.meet("Dogs Rescued")
            self.restore_sanity(10)
        else:
            type.type("You search the park for an hour. Calling. Looking. Nothing.")
            print("\n")
            type.type("As you're about to leave, you hear whimpering from the utility shed. The door is jammed.")
            print("\n")
            if self.has_item("Pocket Knife") or self.has_item("Tool Kit"):
                tool = "Pocket Knife" if self.has_item("Pocket Knife") else "Tool Kit"
                type.type("You use your " + item(tool) + " to pry the latch. Inside: three dogs, scared but alive.")
                self.meet("Dogs Rescued")
                self.restore_sanity(8)
            else:
                type.type("You can't get it open. You call the number on the flyer and leave a message about the shed.")
                type.type(" Hopefully someone gets there in time.")
                self.lose_sanity(3)
        
        self.lose_danger("Lost Dog Whistle Search")
        self.add_danger("Lost Dog Culprit")
        print("\n")

    def lost_dog_culprit(self):
        """Fourth event: discovering who was taking the dogs"""
        if not self.has_danger("Lost Dog Culprit"):
            self.day_event()
            return
        
        if self.has_met("Dogs Rescued"):
            type.type("The neighborhood is buzzing. Three of the five dogs are back home safe. Two are still missing.")
            print("\n")
            type.type("But now people are talking. And they're angry.")
            print("\n")
            type.type("You drive past the park and see a crowd gathered around the utility shed. Police are there.")
            print("\n")
            type.type("A teenager in a hoodie is sitting on the curb, handcuffed. He looks terrified.")
            print("\n")
            type.type("One of the officers approaches you.")
            print("\n")
            type.type(quote("You the one who found the dogs? We got a tip from the shelter."))
            print("\n")
            type.type("The kid wasn't trying to hurt them. He was hoarding them. Taking them home, one by one, ")
            type.type("because his parents wouldn't let him have a pet. Keeping them in the shed with food and water.")
            print("\n")
            type.type("Stupid. Dangerous. But not malicious. Just a lonely kid who wanted someone to love him back.")
            print("\n")
            
            if self.has_item("Torn Collar"):
                type.type("You hand the officer the " + cyan(bright("Torn Collar")) + ". " + quote("This belongs to Biscuit."))
                print("\n")
                type.type(quote("We'll get it back to the family. Thank you."))
                print("\n")
                self.use_item("Torn Collar")
        else:
            type.type("You hear through the neighborhood grapevine: the dogs were found. A teenager had them.")
            print("\n")
            type.type("A lonely kid hoarding pets because his parents wouldn't let him have one. ")
            type.type("The dogs are safe. The kid is in trouble. The story is sadder than you expected.")
        
        self.lose_danger("Lost Dog Culprit")
        self.add_danger("Lost Dog Reunion")
        self.restore_sanity(3)
        print("\n")

    def lost_dog_reunion(self):
        """Fifth event (finale): the neighborhood reunion"""
        if not self.has_danger("Lost Dog Reunion"):
            self.day_event()
            return
        if self.has_met("Missing Dogs Found"):
            self.day_event()
            return
        
        type.type("You get a call. Somehow, the shelter got your number from the flyers. ")
        type.type("All five dogs are home safe. The neighborhood wants to say thank you.")
        print("\n")
        type.type("You drive back to the block. And you can't believe what you see.")
        print("\n")
        type.type("They set up a party. A " + yellow(bright("block party")) + ". For YOU.")
        print("\n")
        type.type("Dogs running everywhere. Kids with balloons. Biscuit the beagle runs straight to you ")
        type.type("and nearly knocks you over with love.")
        print("\n")
        
        if self.has_met("Dogs Rescued"):
            type.type("Mrs. Huang presses a plate of homemade dumplings into your hands. ")
            type.type("The Petersons give you a blanket — a real one, thick and warm. ")
            type.type("Someone hands you " + green("${:,}".format(150)) + " in a card that says 'THANK YOU, DOG HERO.'")
            self.change_balance(150)
            self.add_item("Blanket") if not self.has_item("Blanket") else None
            self.heal(15)
        else:
            type.type("They thank you for caring. For trying. For making those calls. ")
            type.type("Someone hands you " + green("$50") + " and a plate of food.")
            self.change_balance(50)
            self.heal(10)
        
        print("\n")
        type.type("As you're leaving, Biscuit's owner runs up to you with a camera.")
        print("\n")
        type.type(quote("One picture! Please! For the community board!"))
        print("\n")
        type.type("You pose with five dogs piled around you. Everyone's smiling. Even you.")
        print("\n")
        type.type("She gives you a copy: the " + cyan(bright("Reunion Photo")) + ". ")
        type.type("You tuck it into your visor. Best picture you've ever been in.")
        self.add_item("Reunion Photo")
        self.meet("Missing Dogs Found")
        self.lose_danger("Lost Dog Reunion")
        self.restore_sanity(20)
        print("\n")

    # ==========================================
    # INTERCONNECTED BONUS EVENTS
    # Events that fire when you have items/flags
    # from MULTIPLE chains
    # ==========================================

    def crossover_radio_hermit(self):
        """If you've done both the Radio and Hermit chains"""
        if not self.has_met("Radio Broadcast Done") or not self.has_met("Hermit Trail Found"):
            self.day_event()
            return
        if self.has_met("Radio Hermit Crossover"):
            self.day_event()
            return
        
        type.type("You tune to 108.7. Vera is interviewing someone.")
        print("\n")
        type.type(quote("...and my father, Edgar, lived in the woods for years. A listener found his camp, his journal. ") +
                  quote("They even found a stash he left behind. For strangers. That was my dad."))
        print("\n")
        type.type("It's Diana. Ranger Diana. On Radio Nowhere.")
        print("\n")
        type.type("Vera asks: " + quote("What would you say to the person who found it?"))
        print("\n")
        type.type("Diana pauses. Then: " + quote("Thank you. For not just walking past it. For caring about a dead man's story."))
        print("\n")
        type.type("You're sitting in the dark, in your car, listening to someone talk about you on the radio. ")
        type.type("They don't know you're listening. But you are. And it matters.")
        self.meet("Radio Hermit Crossover")
        self.restore_sanity(10)
        print("\n")

    def crossover_artisan_rose_gift(self):
        """If you have the Scrap Metal Rose and meet someone from another chain"""
        if not self.has_item("Scrap Metal Rose"):
            self.day_event()
            return
        if not self.has_met("Radio Nowhere Member") and not self.has_met("Missing Dogs Found"):
            self.day_event()
            return
        if self.has_met("Rose Gift Given"):
            self.day_event()
            return
        
        if self.has_met("Radio Nowhere Member"):
            type.type("You're at Radio Nowhere. Vera is having a rough night.")
            print("\n")
            type.type(quote("Some nights I wonder if anyone's actually listening. If this matters."))
            print("\n")
            type.type("You pull the " + cyan(bright("Scrap Metal Rose")) + " from your pocket. You set it on the mixing board.")
            print("\n")
            type.type("Vera picks it up. Turns it over. Traces the petals.")
            print("\n")
            type.type(quote("You made this?"))
            print("\n")
            type.type("You nod. " + quote("Someone taught me that junk can become art. If you care enough."))
            print("\n")
            type.type("She puts it next to the microphone. It stays there permanently.")
        else:
            type.type("You drive past the neighborhood where you found the dogs. ")
            type.type("Biscuit's owner is sitting on her porch, looking tired.")
            print("\n")
            type.type("You hand her the " + cyan(bright("Scrap Metal Rose")) + ".")
            print("\n")
            type.type(quote("What's this for?"))
            print("\n")
            type.type(quote("For being part of the good part of this story."))
            print("\n")
            type.type("She smiles. First real smile you've seen from her.")
        
        self.use_item("Scrap Metal Rose")
        self.meet("Rose Gift Given")
        self.restore_sanity(12)
        print("\n")

    def crossover_night_vision_bonus(self):
        """Night Vision Scope helps in other situations"""
        if not self.has_item("Night Vision Scope"):
            self.day_event()
            return
        if self.has_met("Night Vision Bonus Used"):
            self.day_event()
            return
        
        type.type("Something is moving near your car in the pitch black. Again.")
        print("\n")
        type.type("But this time you have the " + cyan(bright("Night Vision Scope")) + " from Edgar's daughter.")
        print("\n")
        type.type("You press it to your eye. The world turns green and sharp.")
        print("\n")
        
        sight = random.randrange(4)
        if sight == 0:
            type.type("It's a deer. A beautiful doe, picking through the garbage cans delicately. ")
            type.type("She looks up, right at you, then goes back to eating. Not afraid. Just... existing.")
            self.restore_sanity(5)
        elif sight == 1:
            type.type("A person. Casing cars. Trying door handles one by one.")
            print("\n")
            type.type("They try yours. Locked. They move on. You got the plate number.")
            self.restore_sanity(3)
        elif sight == 2:
            type.type("Raccoons. An army of them. Having what can only be described as a board meeting around a dumpster.")
            print("\n")
            type.type("You watch them for twenty minutes. It's the best TV you've seen in months.")
            self.restore_sanity(4)
        else:
            type.type("Nothing. Nothing at all. But now you KNOW it's nothing. ")
            type.type("And knowing is the difference between fear and peace.")
            self.restore_sanity(3)
        
        self.meet("Night Vision Bonus Used")
        print("\n")

    def crossover_all_chains_complete(self):
        """Special event if you've completed all 4 chains"""
        if not self.has_met("Hollow Oak Found"):
            self.day_event()
            return
        if not self.has_met("Radio Broadcast Done"):
            self.day_event()
            return
        if not self.has_met("Junkyard Crown Made"):
            self.day_event()
            return
        if not self.has_met("Missing Dogs Found"):
            self.day_event()
            return
        if self.has_met("All Chains Complete"):
            self.day_event()
            return
        
        type.type("You're sitting on the hood of your car at sunset. Taking stock.")
        print("\n")
        type.type("The " + cyan(bright("Junkyard Crown")) + " sits on the dashboard.") if self.has_item("Junkyard Crown") else None
        type.type(" The " + cyan(bright("Reunion Photo")) + " is tucked in the visor.") if self.has_item("Reunion Photo") else None
        type.type(" Radio Nowhere plays softly from the speakers.")
        print("\n")
        type.type("You think about the hermit who left a stash for strangers. ")
        type.type("About Gideon, who taught you that breaking isn't ending. ")
        type.type("About Vera, who gave you a voice. ")
        type.type("About five dogs and one lonely kid.")
        print("\n")
        type.type("You came to this town with nothing. Living in your car. Playing blackjack to survive.")
        print("\n")
        type.type("You still live in your car. You still play blackjack.")
        print("\n")
        type.type("But you're not nothing anymore. You're the person who shows up. ")
        type.type("The person who follows the map, answers the radio, picks up the tools, and finds the dogs.")
        print("\n")
        type.type(yellow(bright("You are somebody. You always were.")))
        print("\n")
        
        reward = random.randint(200, 500)
        type.type("A " + green("${:,}".format(reward)) + " tip shows up from a stranger at the casino who heard your broadcast.")
        self.change_balance(reward)
        self.meet("All Chains Complete")
        self.restore_sanity(25)
        self.heal(10)
        print("\n")

    # ==========================================
    # RECURRING CHAIN ITEM EVENTS
    # Passive bonuses from chain items
    # ==========================================

