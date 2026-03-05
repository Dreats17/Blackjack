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

class EndingsMixin:
    """Endings: All game endings - mechanic endings, millionaire path, madness"""

    # ============================================
    # MILLIONAIRE ENDINGS
    # ============================================
    
    def millionaire_morning_visitor(self):
        """The special morning event when you wake up as a millionaire"""
        print("\n")
        type.slow("You wake up to the sound of tapping on your car window.")
        print("\n")
        type.type("For a moment, you think you're dreaming. The morning light filters through the dusty glass, illuminating a figure standing outside your wagon.")
        print("\n")
        type.type("You sit up slowly, rubbing your eyes. When you look again, the figure is still there. ")
        type.type("An old woman, dressed in a flowing white dress that seems to shimmer in the dawn light.")
        print("\n")
        type.type("Her eyes are kind, but ancient. Something about her feels... familiar.")
        print("\n")
        
        type.slow(cyan("\"Good morning, child. You've done well.\""))
        print("\n")
        
        type.type("You crack the window open, unsure if this is real.")
        print("\n")
        
        type.type(quote("Who... who are you?"))
        print("\n")
        
        type.slow(cyan("\"I am the one who has watched over you since the beginning. Since that first night, when you walked into the casino with nothing but fifty dollars and a dream.\""))
        print("\n")
        
        type.type("She smiles, and for a moment, you swear you see her flicker like a candle flame.")
        print("\n")
        
        type.slow(cyan("\"You've accumulated a fortune through the cards. One million dollars. But wealth alone does not complete a journey.\""))
        print("\n")
        
        type.type("You step out of your wagon, the cool morning air hitting your face. The woman doesn't move, simply watching you with those ancient eyes.")
        print("\n")
        
        type.slow(cyan("\"To truly finish what you've started, you must visit the one who helped you get here. Your mechanic. They have something important to tell you.\""))
        print("\n")
        
        # Determine which mechanic to send them to based on who they've met
        mechanics_met = []
        if self.has_met("Tom"):
            mechanics_met.append("Tom")
        if self.has_met("Frank"):
            mechanics_met.append("Frank")
        if self.has_met("Oswald"):
            mechanics_met.append("Oswald")
        
        if len(mechanics_met) == 0:
            # Player never got their car fixed by any mechanic - rare ending path
            type.slow(cyan("\"But I see... you never let anyone in. You fixed things yourself, or left them broken. An interesting choice.\""))
            print("\n")
            type.slow(cyan("\"Very well. Your path is your own. But know this - the airport lies to the east. If you wish to leave this life behind entirely, that is where you must go.\""))
            print("\n")
            self.set_chosen_mechanic("None")
        elif len(mechanics_met) == 1:
            chosen = mechanics_met[0]
            self.set_chosen_mechanic(chosen)
            if chosen == "Tom":
                type.slow(cyan("\"Tom. The jolly one with the golden truck. He's been expecting you. Go to him this afternoon.\""))
            elif chosen == "Frank":
                type.slow(cyan("\"Frank. The rough one with the tattooed arms. He has something to say. Visit him this afternoon.\""))
            else:
                type.slow(cyan("\"Oswald. The quiet genius. He's been waiting for this moment. See him this afternoon.\""))
            print("\n")
        else:
            # Multiple mechanics - let the woman choose based on who has the most dream progress
            dream_scores = {
                "Tom": self.get_tom_dreams() if self.has_met("Tom") else -1,
                "Frank": self.get_frank_dreams() if self.has_met("Frank") else -1,
                "Oswald": self.get_oswald_dreams() if self.has_met("Oswald") else -1
            }
            chosen = max([m for m in mechanics_met], key=lambda m: dream_scores[m])
            self.set_chosen_mechanic(chosen)
            
            if chosen == "Tom":
                type.slow(cyan("\"You've met several mechanics on your journey, but Tom... Tom has been special to you, hasn't he? The dreams you've shared... they bind you together.\""))
                print("\n")
                type.slow(cyan("\"Go to Tom's Trusty Trucks and Tires this afternoon. Your destiny awaits there.\""))
            elif chosen == "Frank":
                type.slow(cyan("\"You've crossed paths with many, but Frank's fire has left its mark on you. The visions in your sleep... they speak of him.\""))
                print("\n")
                type.slow(cyan("\"Go to Filthy Frank's Flawless Fixtures this afternoon. He has answers you seek.\""))
            else:
                type.slow(cyan("\"Of all the mechanics you've known, Oswald's quiet wisdom has touched you deepest. Your dreams whisper his name.\""))
                print("\n")
                type.slow(cyan("\"Go to Oswald's Optimal Outparts this afternoon. The final piece awaits.\""))
            print("\n")
        
        type.type("The woman begins to fade, her form dissolving like morning mist.")
        print("\n")
        
        type.slow(cyan("\"Remember, child - you may also choose to fly away. The airport is always an option for those with means. But that choice... that choice will change everything.\""))
        print("\n")
        
        type.type("And then she's gone, leaving only the faint scent of lavender and the warmth of the rising sun.")
        print("\n")
        
        type.type("You stand there for a long moment, processing what just happened. A million dollars in your pocket, and a choice to make.")
        print("\n")
        
        if self.get_chosen_mechanic() == "None":
            type.type("The airport to the east... or stay here and continue gambling, now with nothing to prove.")
        else:
            type.type("Visit " + magenta(bright(self.get_chosen_mechanic())) + " at their shop... fly away from the airport... ")
            type.type("or stay here and continue gambling, now with nothing to prove.")
        print("\n")
        
        ask.press_continue("Press a key to continue to the afternoon: ")
        print("\n")

    def millionaire_afternoon(self):
        """Special afternoon choices after the millionaire morning visitor"""
        type.type("The afternoon sun hangs heavy in the sky. You've got " + green(bright("${:,}".format(self._balance))) + " and a decision to make.")
        print("\n")
        
        # Build the choice list
        choices = []
        
        chosen_mechanic = self.get_chosen_mechanic()
        if chosen_mechanic == "Tom" and self.has_met("Tom"):
            choices.append(("Visit Tom's Trusty Trucks and Tires", "tom_ending"))
        elif chosen_mechanic == "Frank" and self.has_met("Frank"):
            choices.append(("Visit Filthy Frank's Flawless Fixtures", "frank_ending"))
        elif chosen_mechanic == "Oswald" and self.has_met("Oswald"):
            choices.append(("Visit Oswald's Optimal Outoparts", "oswald_ending"))
        
        choices.append(("Drive to the Airport", "airport"))
        choices.append(("Go to the Casino (Continue Playing)", "continue"))
        
        type.type("What would you like to do?")
        print()
        for i, (text, _) in enumerate(choices):
            type.type(str(i+1) + ". " + text)
            time.sleep(0.5)
            print()
        
        choice = None
        type.type("Choose a number: ")
        while True:
            while choice is None:
                try:
                    choice = int(input())
                except ValueError:
                    type.type("Choose a number: ")
            if 1 <= choice <= len(choices):
                break
            else:
                choice = None
                type.type("That number's not a choice!")
                print()
                type.type("Choose a number: ")
        
        print()
        selected = choices[choice-1][1]
        
        if selected == "tom_ending":
            self.goodbye_tom()
        elif selected == "frank_ending":
            self.goodbye_frank()
        elif selected == "oswald_ending":
            self.goodbye_oswald()
        elif selected == "airport":
            self.visit_airport()
        else:
            # Continue playing - go to normal night event
            type.type("You decide to keep gambling. After all, why stop now?")
            print("\n")
            self.night_event()

    def visit_airport(self):
        """Drive to the airport and choose your escape ending"""
        type.type("You get in your wagon and begin the long drive east, towards the airport.")
        print("\n")
        type.type("The road stretches out before you, endless and empty. You've never driven this far from the casino before.")
        print("\n")
        type.type("As you drive, you think about everything that's happened. ")
        type.type("The nights at the blackjack table. The dealers. The mechanics. The strange people you've met along the way.")
        print("\n")
        
        # Different thoughts based on what the player has experienced
        if self.has_met("Tom") or self.has_met("Frank") or self.has_met("Oswald"):
            mechanics_names = []
            if self.has_met("Tom"): mechanics_names.append("Tom")
            if self.has_met("Frank"): mechanics_names.append("Frank")
            if self.has_met("Oswald"): mechanics_names.append("Oswald")
            type.type("You think about " + ", ".join(mechanics_names) + ". They helped you when you needed it most.")
            print("\n")
        
        # Check for companions
        companions = self.get_all_companions()
        companion_count = len(companions)
        
        if companion_count >= 5 and self.has_item("Animal Whistle"):
            # SECRET ENDING AVAILABLE - Noah's Ark
            type.type("Your wagon is... crowded. Very crowded.")
            print("\n")
            type.type("In the backseat: ")
            companion_names = list(companions.keys())
            type.type(", ".join(companion_names) + ".")
            print("\n")
            type.type("They've all made their peace with each other. Somehow. It's like a strange, furry family.")
            print("\n")
            type.type("The " + magenta(bright("Animal Whistle")) + " around your neck hums softly. It brought them all to you.")
            print("\n")
        elif self.has_item("Squirrely"):
            type.type("Squirrely chitters nervously in the passenger seat. He's never been on a plane before.")
            print("\n")
        elif companion_count > 0:
            companion_names = list(companions.keys())
            type.type(companion_names[0] + " looks out the window, curious about the world passing by.")
            print("\n")
        
        if self.has_met("Suzy"):
            type.type("You wonder if Suzy ever made it out of here. Maybe you'll see her on the other side.")
            print("\n")
        
        type.type("After what feels like hours, you see it - the airport, rising from the desert like a mirage.")
        print("\n")
        type.type("You park your wagon in the long-term lot. Something tells you it'll be here for a while.")
        print("\n")
        type.type("Walking into the terminal, you approach the ticket counter. The attendant looks up at you with tired eyes.")
        print("\n")
        
        type.type(quote("One-way ticket, please. Anywhere but here."))
        print("\n")
        
        type.type("The attendant raises an eyebrow but doesn't ask questions. After a moment, she slides a ticket across the counter.")
        print("\n")
        
        type.type(quote("That'll be $10,000."))
        print("\n")
        
        type.type("You pay without hesitation. What's ten grand when you have a million?")
        print("\n")
        self.change_balance(-10000)
        
        type.type("As you walk towards the gate, ticket in hand, you pause at the large windows overlooking the tarmac.")
        print("\n")
        type.type("A plane sits waiting. Your plane. Your escape.")
        print("\n")
        
        type.type("But is this really what you want? To fly away and never look back?")
        print("\n")
        
        # Check for secret companion ending
        companions = self.get_all_companions()
        companion_count = len(companions)
        secret_available = companion_count >= 5 and self.has_item("Animal Whistle")
        
        type.type("1. Board the plane and fly away")
        print()
        type.type("2. Turn around and go back")
        print()
        if secret_available:
            type.type("3. " + magenta(bright("Charter a private plane for you and your animals")))
            print()
        
        choice = None
        valid_choices = [1, 2] if not secret_available else [1, 2, 3]
        type.type("Choose a number: ")
        while True:
            while choice is None:
                try:
                    choice = int(input())
                except ValueError:
                    type.type("Choose a number: ")
            if choice in valid_choices:
                break
            else:
                choice = None
                type.type("Choose a number: ")
        
        print("\n")
        
        if choice == 1:
            self.bliss()
        elif choice == 3 and secret_available:
            self.sanctuary()
        else:
            type.type("You crumple the ticket in your hand and turn around.")
            print("\n")
            type.type("Not yet. There's still unfinished business here.")
            print("\n")
            type.type("You drive back to your wagon, the casino still calling to you from the west.")
            print("\n")
            self.change_balance(10000)  # Get refund
            type.type("The ticket attendant shrugs and refunds your money. " + quote("Happens more often than you'd think."))
            print("\n")
            self.night_event()

    def bliss(self):
        print("\n")
        type.slow(bright(yellow("~ ~ ~ BLISS ~ ~ ~")))
        print("\n")
        
        type.slow("You board the plane.")
        print("\n")
        
        type.slow("The seats are leather. The champagne is complimentary. Everything smells like new money and fresh starts.")
        print("\n")
        
        type.slow("As the plane taxis down the runway, you look out the window at the desert below. The sun is setting, painting everything in shades of blood and gold.")
        print("\n")
        
        type.slow("Somewhere out there is the casino. That crooked little shack on the hill where you spent so many nights, feeding your dollars to a man with a jade glass eye.")
        print("\n")
        
        type.slow("Somewhere out there is the wagon you called home. The backseat where you slept. The steering wheel you gripped until your knuckles turned white. The rearview mirror where you watched yourself slowly become someone else.")
        print("\n")
        
        type.slow("The plane lifts off, and the ground falls away beneath you.")
        print("\n")
        
        type.slow("You close your eyes.")
        print("\n")
        
        type.slow("And you let go.")
        print("\n")
        
        type.slow("Of everything.")
        print("\n")
        
        type.slow("The gambling. The obsession. The nights you couldn't sleep because the cards were calling. The mornings you woke up and couldn't remember who you used to be.")
        print("\n")
        
        type.slow("It's over. It's finally over.")
        print("\n")
        
        # Build the ending based on accomplishments
        type.slow(bright("~ Your Journey ~"))
        print("\n")
        
        type.slow("You survived " + yellow(bright(str(self._day) + " days")) + " living in your car.")
        print("\n")
        
        type.slow("You flew away with " + green(bright("${:,}".format(self._balance))) + " to your name.")
        print("\n")
        
        # Special items and accomplishments
        accomplishments = []
        
        if self.has_item("Rabbit's Blessing"):
            accomplishments.append("You caught the legendary rabbit and claimed its treasure.")
        
        if self.has_item("Squirrely"):
            accomplishments.append("Squirrely sits on your armrest, nose pressed against the window, watching the clouds roll by. He doesn't understand where you're going. Neither do you, really.")
        
        if self.get_tom_dreams() >= 3:
            accomplishments.append("You uncovered the truth about Tom's family through your dreams. You never told him. Some things are better left buried.")
        
        if self.get_frank_dreams() >= 3:
            accomplishments.append("You learned the dark secrets of the Dealer through Frank's visions. They still haunt you.")
        
        if self.get_oswald_dreams() >= 3:
            accomplishments.append("You witnessed the casino's true nature in Oswald's dreams. You wish you hadn't.")
        
        if self.has_met("Victoria"):
            accomplishments.append("You never found out what happened to Victoria. Maybe that's for the best.")
        
        if self.has_met("Suzy"):
            accomplishments.append("Suzy's face flashes in your mind. Her kindness. Her hope. You wonder if she ever made it out too.")
        
        if self.has_met("Witch"):
            accomplishments.append("The Witch Doctor's potions still flow through your veins. Sometimes you feel them, pulsing, waiting.")
        
        if self.has_item("Necronomicon"):
            accomplishments.append("The Necronomicon sits in your carry-on luggage. You can hear it whispering. It never stops.")
        
        if len(self._inventory) >= 10:
            accomplishments.append("You collected " + str(len(self._inventory)) + " items on your journey. Trinkets. Memories. Scars.")
        
        if len(accomplishments) > 0:
            for acc in accomplishments:
                type.slow("- " + acc)
                print()
            print()
        
        # The final scene
        type.slow("The plane levels off above the clouds.")
        print("\n")
        
        type.slow("Below you, the world is soft and white. Like a blank page. Like a fresh start.")
        print("\n")
        
        type.slow("The flight attendant brings you another glass of champagne. You raise it to no one in particular.")
        print("\n")
        
        type.slow(quote("To Grandma. Thanks for the fifty bucks."))
        print("\n")
        
        type.slow("You drink. The bubbles burn your throat.")
        print("\n")
        
        type.slow("You watch the clouds drift by, and for the first time in months, maybe years, your mind is quiet.")
        print("\n")
        
        # Epilogue based on items/status
        type.slow(bright("~ Epilogue ~"))
        print("\n")
        
        type.slow("You landed in a city you'd never been to. Rented an apartment with a view of the ocean. Bought furniture that didn't smell like gasoline and regret.")
        print("\n")
        
        if self._balance >= 500000:
            type.slow("With your fortune, you bought a modest house by the sea. Nothing fancy - just enough room for you")
            if self.has_item("Squirrely"):
                type.slow(" and Squirrely")
            type.slow(".")
            print("\n")
            type.slow("You spend your days reading. Fishing. Trying not to think about the sound of shuffling cards.")
            print("\n")
        else:
            type.slow("The money didn't last forever. It never does.")
            print("\n")
            type.slow("But for a while, you lived. Really lived. Not just survived.")
            print("\n")
            type.slow("You took up gardening. Learned to cook. Found peace in the simple things you'd forgotten existed.")
            print("\n")
        
        type.slow("Sometimes, late at night, you dream of the casino.")
        print("\n")
        
        type.slow("The Dealer's jade eye. The sound of chips clinking. The feeling of cards sliding across felt.")
        print("\n")
        
        type.slow("You wake up in a cold sweat, hands reaching for money that isn't there, heart pounding with the thrill of a bet you didn't make.")
        print("\n")
        
        type.slow("But then you see the ocean through your window. You hear the waves. You remember where you are.")
        print("\n")
        
        type.slow("And you breathe.")
        print("\n")
        
        type.slow("You made it out.")
        print("\n")
        
        type.slow("You're free.")
        print("\n")
        
        type.slow("...")
        print("\n")
        
        type.slow("Aren't you?")
        print("\n")
        
        type.slow(green(bright("You found bliss.")))
        print("\n")
        
        # Display achievements earned
        self.display_final_achievements()
        
        type.slow(bright(yellow("~ ~ ~ THE END ~ ~ ~")))
        print("\n")
        
        type.slow("Thank you for playing.")
        print("\n")
        
        quit()

    def sanctuary(self):
        """SECRET ENDING - The Animal Shepherd"""
        companions = self.get_all_companions()
        companion_names = list(companions.keys())
        companion_count = len(companions)
        
        print("\n")
        type.slow(bright(magenta("~ ~ ~ SANCTUARY ~ ~ ~")))
        print("\n")
        
        type.slow("You approach a different counter. A private charter service.")
        print("\n")
        
        type.slow("The attendant looks at you. Then at the animals trailing behind you.")
        print("\n")
        
        type.slow(quote("That's... a lot of animals."))
        print("\n")
        
        type.slow(quote("They're family."))
        print("\n")
        
        type.slow("The attendant blinks. Looks at the procession: " + ", ".join(companion_names) + ".")
        print("\n")
        
        type.slow("Then she smiles. A genuine smile.")
        print("\n")
        
        type.slow(quote("I've seen a lot of things in this job. But never anything like this."))
        print("\n")
        
        type.slow("She types something into her computer.")
        print("\n")
        
        type.slow(quote("There's a small airfield about an hour from here. A pilot who doesn't ask questions. "))
        type.slow(quote("He can get you somewhere... special. Somewhere for people like you."))
        print("\n")
        
        cost = 100000
        type.slow(quote("It'll cost ") + green(bright("${:,}".format(cost))) + quote(". Cash."))
        print("\n")
        
        if self.get_balance() >= cost:
            self.change_balance(-cost)
            type.slow("You pay without hesitation. What's money compared to this?")
            print("\n")
        else:
            type.slow("You empty your pockets. Everything you have. It's not quite enough.")
            print("\n")
            type.slow("The attendant looks at your animals. At the hope in their eyes. At the love.")
            print("\n")
            type.slow(quote("...Close enough."))
            self.change_balance(-self.get_balance())
            print("\n")
        
        type.slow("...")
        print("\n")
        
        type.slow("The small plane takes off at sunset.")
        print("\n")
        
        type.slow("It's cramped. It smells like fur and feathers and the kind of chaos that comes with " + str(companion_count) + " animals in a confined space.")
        print("\n")
        
        type.slow("But when you look around at the faces—snouts, beaks, whiskers—you see something you haven't felt in a long time.")
        print("\n")
        
        type.slow("Family.")
        print("\n")
        
        type.slow("The pilot turns and grins.")
        print("\n")
        
        type.slow(quote("Where we're going, animals live like kings. "))
        type.slow(quote("It's called the Sanctuary. You'll fit right in."))
        print("\n")
        
        type.slow("...")
        print("\n")
        
        type.slow(bright("~ Your Family ~"))
        print("\n")
        
        for name, data in companions.items():
            bond_str = " (bonded)" if data["bonded"] else ""
            type.slow("• " + bright(name) + " the " + data["type"] + bond_str)
            print()
        print()
        
        type.slow("You land in a valley so green it hurts your eyes. Mountains rise on all sides. A river cuts through the middle, crystal clear.")
        print("\n")
        
        type.slow("There are other people here. Other... shepherds. Each with their own little family of misfits.")
        print("\n")
        
        type.slow("A woman waves at you. Behind her, three dogs and a goat.")
        print("\n")
        
        type.slow(quote("Welcome home."))
        print("\n")
        
        type.slow("You look down at the " + magenta(bright("Animal Whistle")) + " around your neck.")
        print("\n")
        
        type.slow("It led you here. To this place. To these creatures. To this life.")
        print("\n")
        
        type.slow("You never thought you'd find paradise in a gambling addiction story.")
        print("\n")
        
        type.slow("But here you are.")
        print("\n")
        
        type.slow("Home.")
        print("\n")
        
        type.slow("...")
        print("\n")
        
        type.slow("The casinos? The dealers? The endless nights of betting your soul one chip at a time?")
        print("\n")
        
        type.slow("They feel like a fever dream. Something that happened to someone else.")
        print("\n")
        
        type.slow("You spend your days tending to animals. Teaching others. Finding peace in the simple rhythms of life.")
        print("\n")
        
        # Enhanced companion-specific sanctuary moments
        if self.has_companion("Grace"):
            type.slow("Grace's fawns have grown. They bring you wildflowers every morning.")
            print("\n")
        if self.has_companion("Ursus") or self.has_companion("Bruno"):
            type.slow("The bears guard the valley at night. Nothing dares approach when they patrol.")
            print("\n")
        if self.has_companion("Kraken"):
            type.slow("The Kraken visits sometimes, emerging from the river's deepest pool just to say hello.")
            print("\n")
        if self.has_companion("Thunder"):
            type.slow("Thunder carries children on rides through the meadows. They squeal with laughter.")
            print("\n")
        if self.has_companion("Squawk") or self.has_companion("General Quackers"):
            type.slow("The birds organize aerial shows for entertainment. They're surprisingly coordinated.")
            print("\n")
        if companion_count >= 15:
            type.slow("Your corner of the Sanctuary is the loudest, most chaotic, most loved. People come from all over just to see your collection.")
            print("\n")
        
        type.slow("Sometimes, late at night, you hear the distant call of cards shuffling.")
        print("\n")
        
        type.slow("But then " + companion_names[0] + " nudges your hand. And the sound fades away.")
        print("\n")
        
        type.slow("You made it out.")
        print("\n")
        
        type.slow("And you took your family with you.")
        print("\n")
        
        type.slow(magenta(bright("You found sanctuary.")))
        print("\n")
        
        # Display achievements earned
        self.display_final_achievements()
        
        type.slow(bright(yellow("~ ~ ~ SECRET ENDING: THE SHEPHERD ~ ~ ~")))
        print("\n")
        
        type.slow("Companions saved: " + yellow(bright(str(companion_count))))
        print()
        type.slow("Days survived: " + yellow(bright(str(self._day))))
        print("\n")
        
        type.slow("Thank you for playing.")
        print("\n")
        
        quit()

    def goodbye_tom(self):
        type.type("You get in your wagon and drive to Tom's Trusty Trucks and Tires.")
        print("\n")
        type.type("The golden truck is parked out front, gleaming in the afternoon sun.")
        print("\n")
        type.type("Tom is waiting for you outside, a knowing look in his eyes.")
        print("\n")
        
        type.type(quote("I knew you'd come, yunno. A million bucks, huh? That's somethin' special."))
        print("\n")
        
        type.type("He scratches his chin.")
        print("\n")
        
        type.type(quote("But I gotta ask... what about that family of yours? You ever think about goin' back?"))
        print("\n")
        
        type.type("Tom pulls out a phone - your phone. The one you left here days ago.")
        print("\n")
        
        type.type(quote("There's been someone tryin' to reach ya. A lot. Think it might be important."))
        print("\n")
        
        answer = ask.yes_or_no("Take the phone call? ")
        
        if answer == "yes":
            type.type("You take the phone. Your hands are trembling.")
            print("\n")
            type.type("Tom gives you some space, walking back into the garage.")
            print("\n")
            type.type("You press the call button.")
            print("\n")
            type.type("It rings once. Twice. Then-")
            print("\n")
            
            type.slow(quote("John? John, is that you?"))
            print("\n")
            
            type.slow("The voice on the other end is unmistakable. It's Rebecca. Your wife.")
            print("\n")
        else:
            type.type(quote("Well, suit yourself. The phone'll be here if you change your mind."))
            print("\n")
            type.type("You leave Tom's shop. Maybe someday you'll be ready to face that call.")
            print("\n")
            return

        type.slow(quote("Do you hear that? That's your son, Nathan. He learned to walk a couple months ago. His first word was 'Dada'. God, I wish you were here for that. He needs you in his life, he needs you as a father figure. He remembers you. Sometimes, I pull up old pictures of you, and he reaches out to touch your face. All I want is for you to be here, to make more memories with me and my son. But you can be here, if you come back, come home. We can raise our son together, if you just come back home, to be with me and Nathan. I can forgive you for all of it. I do, I forgive you for everything. None of it matters now, it's all in the past. Just please…come home."))
        print("\n")

        type.slow("The sobs through the phone are piercing, and Tom has a sad look on his face. He clearly feels sorry for you, for all the pain you've both caused and gone through. ")
        print("\n")

        type.slow(quote("Dada…dada come back!"))
        print("\n")

        type.slow(quote("Could you do that for us?"))

        answer = ask.yes_or_no("\"Will you come back home?\"")

        if answer == "yes":
            self.salvation()
        else:
            self.resurrection()

    def salvation(self):
        type.slow("\"Yes, yes, yes of course I'll come home!\" Tears begin to stream from your eyes. \"I, I don't know what's gotten over me, I'm so, so incredibly sorry.\" A rush of adrenaline, no, realization comes over you. This whole time, you've been wasting your life away in a beat up wagon, trying to make a living off of gambling at a Blackjack table, while your family was trying, and struggling, to imagine a life without you.")
        print("\n")
        
        # Acknowledge companions before leaving
        companion_count = len(self.get_all_companions())
        if companion_count > 0:
            type.slow("You look back at the wagon. At the companions you've gathered on this strange journey.")
            print("\n")
            companion_names = list(self.get_all_companions().keys())
            if companion_count <= 3:
                names_str = ", ".join(companion_names)
            else:
                names_str = companion_names[0] + ", " + companion_names[1] + ", and " + str(companion_count-2) + " others"
            type.slow(f"{names_str} watch you with understanding. They know you have to go.")
            print("\n")
            type.slow("\"I'll find good homes for all of you,\" you promise. \"You saved me. Now I have to save myself.\"")
            print("\n")
            if self.has_companion("Thunder"):
                type.slow("Thunder whinnies softly, nuzzling your shoulder one last time. Horses understand loyalty. Understand sacrifice.")
                print("\n")
            if self.has_companion("Whiskers") or self.has_companion("Lucky"):
                type.slow("A wet nose presses into your palm. A final goodbye from a friend who asked for nothing but love.")
                print("\n")
        
        type.slow("Immediately, you run out of Tom's Trusty Trucks and Tires, and you never look back.")
        print("\n")

        type.slow("\"Wait! You forgotcha wallet, yunno!\" Tom lifts your wallet, and opens it, and his eyes grow wide. \"Holy bejesus! My oh my, this generation is so peculiar. Welp, finder's keepers, I suppose. Guess this old Trucks and Tires shop's boutta get some upgrades, ya hear!\"")
        print("\n")

        type.slow("You put the pedal to the medal in the old wagon, hugging the twists and turns in the road, without a thought in your mind but your family. As you slowly begin to recognize the buildings around you, the wagon takes just a few more turns, before pulling into your driveway. You get out, and knock on the door, and in that moment, nothing feels better than watching the handle turn, hearing the hinges creak, and seeing the biggest smile on your wife's face, with your son in her hands, and you lean in for a warm embrace.")
        print("\n")

        type.slow("Many years go by, and the whole experience of being stranded in your car slowly fades from your mind. You get to experience things in life you never thought you'd one day see. Your son's first football game, the birth of your lovely daughter, Dianne. You and Rebecca renew your vows, and couldn't be any happier. After a long and sincere apology to your old boss Howard, you go back to your desk job, selling high quality printers to people in low income housing. It ain't much, but it's honest work.")
        print("\n")

        type.slow("Rebecca continues to raise the kids in her image. They're smart, caring, and just downright adorable. Once Nathan gets to high school he tries out for the Varsity team, and makes it as a freshman. He would go on to be the highest scoring wide receiver the high school ever had, and you got to be in the seat for every game. His touchdown celebration always ended with a point to you, and a nod, as though he's telling the world \'Yep, that's my Dad\'.")
        print("\n")

        type.slow("As you age more and more, your body slowly deteriorates. You aren't sure if the long and unhealthy lifestyle of living on the road was to blame, but you didn't ever bother giving the thought any time of day. You know, deep down inside, that you made the right choice.")
        print("\n")

        type.slow("Nathan played football in college, before retiring to run his personal business selling decorated carpets. It was in this very building where he would go on to meet his future wife, Kelly, who ended up being his perfect match. Meanwhile, Dianne kept working at being a straight A's student in high school, taking every accelerated English course they had to offer.")
        print("\n")

        type.slow("When Dianne's career as an author made national television, Nathan was in the hospital, with his wife Kelly, along with you and Rebecca. You'll never forget the day you witnessed the birth of your grandson, Thomas, while Dianne was on the tv in that very room, being watched by millions around the world. You gave Rebecca a hug and a kiss, and you both cried tears of joy together, being able to appreciate such a special life with one another.")
        print("\n")

        type.slow("But, as all good things do, it eventually had to come to an end, and when the doctor diagnosed you with chronic obstructive pulmonary disease at age 49, you knew that you were knocking on death's doorstep. After your doctor told you that your lungs were failing on you due to some kind of air pollutants, you came to the realization that you might've left your car running a few too many days. And all that exposure to the exhaust of your old wagon seems to have finally caught up to you.")
        print("\n")

        type.slow("You lay dormant in the hospital bed, with tubes up your nose, and a glossy look over your eyes. There are many bouquets of flowers by your bedside, as well as a few balloons that read 'Get Well Soon!', and 'You Can Beat This!' You hear a knock on the door, and perk up. The doctor walks in, and leads a parade of guests. It seems as though your whole family has come to visit you. There's Rebecca! And Dianne! And Nathan and Kelly, along with Thomas, and their newly born daughter Marissa. You missed her birth, as the doctors had to keep an eye on you, but they sent you lots of pictures. Now, you finally get to see her in person. It makes you so happy that you get to see your granddaughter in person. You weren't sure if you'd ever get the chance.")
        print("\n")

        type.slow("\"Dad, hey, how are you? Hanging in there?\" Nathan has tears streaming down his face, but his voice stays sturdy. It's clear that he, and the rest of your family, hate to see you like this.")
        print("\n")

        type.slow("You cough, then sit up.")
        print("\n")

        type.slow("\"You know, I'm doing pretty amazing, really.\" This gets a light chuckle from your family, but the mood quickly returns to solemn. Rebecca leans in closer to you, and gives you a hug.")
        print("\n")

        type.slow("\"You're my everything. I love you so much, John.\" You hug her back with as much force as you can give, hoping she could feel just a touch of it.")
        print("\n")

        type.slow("\"Dad, I wrote a book about you.\" Dianne half whispers, before showing it to you. \"It's about the battle between you and gambling, and how you overcame it, for us. You really are the strongest person I know. I love you.\" Dianne begins to sob harder, and quickly gives you a big hug.")
        print("\n")

        type.slow("\"Can I see my grandchildren?\" you ask, through your raspy voice.")
        print("\n")

        type.slow("\"Sure thing, Dad\" Nathan picks up Thomas, and Kelly picks up Marissa, and they both walk to your side, so you can get a closer look.")
        print("\n")

        type.slow("\"Gram..Grampy!\" Thomas belches.")
        print("\n")

        type.slow("\"Yes, that's your Grampy!\" Nathan responds, with a smile.")
        print("\n")

        type.slow("\"They're…so beautiful\", you manage to spew these words out, before delving into a coughing fit.")
        print("\n")

        type.slow("Nathan puts Thomas down and gives you a big hug.")
        print("\n")

        type.slow("\"I love you so much, Dad.\"")
        print("\n")

        type.slow("As Nathan releases his grasp, the world around you begins to fade. You look around the room at everyone's faces, one last time. Everyone's leaning onto the bed, to be with you for your final moments. Rebecca and Dianne holding your right hand, Nathan holding your left. Kelly's arm is around Nathan's shoulder, and Thomas and Marissa sit on the blankets, right above your leg. You squeeze your hands tight, holding your family close, before letting go of your grasp, and fading away to eternal darkness...")
        
        # COMPANION ENDING ENHANCEMENTS
        companions = self.get_all_companions()
        if len(companions) > 0:
            print("\n")
            type.slow("But just before the darkness takes you completely, one final vision appears...")
            print("\n")
            type.slow("You see all the companions from your journey. Every creature that chose you, that trusted you, that loved you.")
            print("\n")
            
            # Name specific companions
            if self.has_companion("Grace"):
                type.slow("Grace the deer, walking with her fawns through golden meadows.")
            if self.has_companion("Bruno") or self.has_companion("Ursus"):
                type.slow("The bears - protectors, guardians, ancient and true.")
            if self.has_companion("Chomper"):
                type.slow("Even Chomper the alligator, floating peacefully in warm waters.")
            if self.has_companion("Kraken"):
                type.slow("The Kraken, rising from the deep to witness your passing.")
            if self.has_companion("Thunder"):
                type.slow("Thunder the horse, running free across endless plains.")
            if self.has_companion("Whiskers") or self.has_companion("Lucky"):
                type.slow("Your loyal friends from the streets - Whiskers purring, Lucky's tail wagging.")
            
            print("\n")
            type.slow("They all came to you in your darkest moments. They saw something in you worth saving.")
            print("\n")
            type.slow("You weren't just a gambler. You were someone who cared for the forgotten, the lost, the wounded.")
            print("\n")
            type.slow("You were loved. By your family. By creatures great and small.")
            print("\n")
            type.slow("That's not a bad legacy to leave behind.")
            print("\n")

    def resurrection(self):

        type.slow("\"Wha…what? Excuse me? John, I've been trying to reach you for months now, and the only thing you're going to say to me is 'no'? Do you not care at all about me? About Nathan? Why, why would you do this to us? After everything I've done for you. I covered for you when you needed me, I hid this addiction for years. Years! And for what? So you could run away from your family to keep hitting the tables? You sick, twisted fuck. To think that I honestly believed somewhere, deep down inside of you, you actually cared about me. That you actually cared about YOUR OWN GODDAMN SON.\" Your wife is screaming through the phone.")
        print("\n")

        type.slow("\"Dada…I love you…why dada gone?")
        print("\n")

        type.slow("\"You're a monster. You're completely pathetic. Don't even think about coming back. Not now, not ever. You will never see or hear from your son again, do you understand? YOU'RE DEAD TO ME JOHNATHAN. DEAD TO ME. ROT IN HELL, YOU FUCKING BASTA-")
        print("\n")

        type.slow("And with that, you hang up the phone. Your ears are ringing, your face is numb, and while Tom appears to be trying to console you after that phone call from hell, you just can't seem to hear a single word coming out of his mouth.")
        print("\n")
        
        # Acknowledge companions in the darkness
        companion_count = len(self.get_all_companions())
        if companion_count > 0:
            type.slow("You stumble back to the wagon. Your companions watch you with confused, worried eyes.")
            print("\n")
            if self.has_companion("Lucky"):
                type.slow("Lucky limps over, trying to lick your hand. Trying to comfort you. But you push him away.")
                print("\n")
            if self.has_companion("Whiskers"):
                type.slow("Whiskers meows softly, rubbing against your leg. But you don't feel it. You don't feel anything.")
                print("\n")
            type.slow("They don't understand. They can't understand. You're not worth saving. Never were.")
            print("\n")
        
        type.slow("In fact, you don't feel anything. Nothing but the ringing in your ears, and sheer hatred for the man you've become. And yet somehow throughout all of this, your legs beneath you begin to carry your body, out the door, into your car, and down the road towards that lonely casino, sitting on top of the little hill, at the end of the dirt road.")
        print("\n")
        
        type.slow("As though infected by a parasite, you can't help but come back here, to this place, where you were stranded all those days ago. With your money in hand, you get out of the car, and slam the door. You walk towards the little shack, each step more determined than the last. You can prove her wrong, no, you have to prove her wrong.") 
        print("\n")

        type.slow(red("Welcome back. You don't look too well. Do you need something to drink? Perhaps some water?"))
        print("\n")

        type.slow("\"Bourbon, neat. The best you've got.\"")
        print("\n")

        type.slow(red("If you say so."))
        print("\n")

        type.slow("You watch as the Dealer gets up from his shadow, and as he stands, his jade green glass eye sparkes, around a terrible scar, from a fate that caused the left side of his face to be permanently disfigured. He walks across the room, and flicks on an old fashioned lamp, revealing a small bar, filled with any drink you could ask for. The Dealer's revolver hangs low on his waist, as though he's always prepared to use it at a moment's notice. Or, perhaps, he's just a cautious old man.")
        print("\n")

        type.slow("After about a minute, he comes back with your drink, and sets it down next to you. You pick up the glass, and take a swig, and then another, before slamming the empty glass down on the betting table.")
        print("\n")

        type.slow(red("That was awfully quick of you. Here, let me get you a refill."))
        print("\n")

        type.slow("\"Thanks, yeah, that would be great.\"")
        print("\n")

        type.slow("As he sets down your second glass, the Dealer sits back down in his seat, and begins to shuffle the cards. His thick fingers sometimes have trouble splitting the deck, but he riffles the cards like he's been doing it his whole life.")
        print("\n")

        type.slow(red("Are you ready to play a game of Blackjack?"))
        print("\n")
        
        type.slow("\"So, what's with the glass eye? You lose a fight or something?\"")
        print("\n")

        type.slow("The Dealer squints his eyes, then sighs.")
        print("\n")

        type.slow(red("Oh, I lost a fight alright. With my dog, Scrappy. He was a great lad."))
        print("\n")

        type.slow("The Dealer opens a pack of cigarettes, puts one in his mouth, and lights it. Smoke fills the air, and dances around the hanging light, like two spirits, in an endless duel.")
        print("\n")

        type.slow(red("Jumped up on me while we were playing fetch in the yard. Bit the left half of my face clean off. It was a tragedy, really. Docs patched me up, and the second I got home, me and Scrappy took a car ride. We drove far away from that home, from my neighbors, from everyone. Down a long road, deep into the woods. I let him out, and he was happy, running free. Ducking under branches, jumping over fallen logs, biting at sticks and leaves. But as I walked back to the truck to leave him there, he followed. So, I threw him a stick to go fetch, but when I got to the front seat, there he was, jumping through the window to sit on my lap, licking my hands and wagging his tail. He didn't seem to get that I was leaving without him. That's what made it all the more difficult, when I finally dragged him out of the truck, pulled out my revolver, and shot three bullets into his head. Even still, he kept whimpering. I couldn't bear to watch him die, so I just drove off. Never even gave him a proper burial. It was a shame, really, but I guess not all stories are happy ones."))
        print("\n")

        type.slow("The Dealer ashes the cigarette into a brown ceramic bowl next to him, full of the ashes of many, many long gone cigarettes.")
        print("\n")

        type.slow("You take a swig of your bourbon, appreciating the warm feeling in your chest.")
        print("\n")

        type.slow("\"Let's get this over with.\"")
        print("\n")

        type.slow(red("How much for this first hand?"))
        print("\n")

        type.slow("\"500 thousand.\"")
        print("\n")

        type.slow(red("Oh boy, high roller tonight, are we?"))
        print("\n")

        type.slow("\"You bet.\" You down the rest of your drink, and you start to feel a bit dizzy.")
        print("\n")

        type.slow(red("Alright, let's see here. You got a Nine of Spades, and a Two of Diamonds. Meanwhile, I'm sitting pretty with this Four of Clubs. What say you?"))
        print("\n")

        type.slow("You tap the table with a firm finger. \"Hit me.\"")
        print("\n")

        type.slow(red("Alrighty. Your next card's a…welp, that's a Ten of Clubs. That's a hefty Blackjack you just got there."))
        print("\n")

        type.slow("Winning a hand with a bet like that, you begin to chuckle to yourself. You see the Dealer begin to sweat, and he starts to tap his foot.")
        print("\n")

        type.slow(red("How about I get you another drink?"))
        print("\n")

        type.slow("\"Go for it.\"")
        print("\n")

        type.slow("The Dealer pours you a third bourbon, and hands it to you. You down the whole drink, and start to laugh again.")
        print("\n")

        type.slow("\"So you're telling me, that you shot and killed a dog, because he bit you in the face? Like yeah, that's a bad scar, but how do you mess up playing fetch that badly?\"")
        print("\n")

        type.slow(red("Boy, I've put down a lot bigger for a lot less."))
        print("\n")

        type.slow("\"But god, a dog? For a bite? You didn't have to do that, you know. Animal shelters exist for a reason.\"")
        print("\n")

        type.slow(red("How much are you betting."))
        print("\n")

        type.slow("\"I mean, that's just despicable. Getting revenge on a dog over something it didn't even understand. If you really felt the need to kill it, you could've gone with euthanasia. Why'd that slip your mind?\"")
        print("\n")

        type.slow(red("Give me an amount, boy."))
        print("\n")

        type.slow("\"You know what I think? I think that you wanted to shoot that dog. You were never gonna let it free. You brought it to the woods and shot it, just so you could watch it squirm.\"")
        print("\n")

        type.slow(red("Put some money on the damn table."))
        print("\n")

        type.slow("\"You know, you're what's wrong with this world. I mean, you just hurt those that care about you, denying their love all because you can? What happened to forgive and forget?\"")
        print("\n")

        type.slow(red("BET. SOME. DAMN. MONEY."))
        print("\n")

        type.slow("\"Put me all in, old man.\"")
        print("\n")

        type.slow("The Dealer flips cards over, to you and him.")
        print("\n")

        type.slow(red("That's an Ace of Spades and an Eight of Spades. Deadman's hand, as far as Poker is concerned. I've got a Seven of Hearts. You hitting?"))
        print("\n")

        type.slow("You wave your hand above the table. \"I'll stay\"")
        print("\n")

        type.slow(red("If that's what you'd like. My other card's a Four of Diamonds."))
        print("\n")
        
        type.slow("The dealer draws a card from the deck.")
        print("\n")

        type.slow(red("Damn, Three of Clubs. Would've been nice if you had that one, huh?"))
        print("\n")

        type.slow("The dealer draws yet another card.")
        print("\n")

        type.slow(red("Ace of Diamonds. That puts me at 15."))
        print("\n")

        type.slow("Your head begins to spin. Your stomach feels violently ill. Your breaths are getting deeper and deeper, but it feels like you're getting less and less oxygen each time. The dealer draws yet another card.")
        print("\n")

        type.slow(red("Yet another ace, this time the Ace of Clubs. Now I'm at 16, are you feeling the pressure yet?"))
        print("\n")

        type.slow("You watch as the Dealer's weathered finger goes down, touches the top card of the deck, lifts it up, then flips it over before you.")
        print("\n")

        type.slow(red("And that's the Five of Hearts that I needed! Blackjack for me, back to your car for you. I guess it's like they say, you win some, you lose some."))
        print("\n")

        type.slow("The Dealer's finger points towards the exit, and in a drunken stupor, you rise from the old wooden seat, and stumble your way to the door, with no money left in your pockets.")
        print("\n")

        type.slow("Right before walking out, you turn to the Dealer, who's once again cloaked in shadow. You knew you should've kept your mouth shut, but you couldn't help yourself.")
        print("\n")

        type.slow("\Rot in hell, you fucking bastard.\"")
        print("\n")

        type.slow("You get back into your wagon, and drive off, only faintly able to see the road. Is this really the life you live? You keep driving forward, for hours on end, never once looking back.")
        print("\n")
        
        type.slow("Eventually, your old wagon shutters, then dies. \"Ugh, not again.\" Stranded on the road once more, and your money has gone dry. As you're about to give up hope completely, you're reminded of a distant memory. You reach over to your cup holder and rip it from the center console. Tucked away inside of the hole that once held your cup holder is an old card with a big turkey on the front, wearing a pilgrim hat. When opening it up, you read the message 'Gobble gobble gobble up some yummy food this Thanksgiving! Love, Grandma'. Inside the letter was a green 50 dollar bill. May she rest in peace.")
        print("\n")

        type.slow("The door of your wagon creaks open, and you step out into the night sky, coughing up the Bourbon from earlier that night. After pushing your car off the road and between the trees, there isn't much else left for you to do, so you begin to wander down the dark, lonely street.")
        print("\n")

        type.slow("But, at the end of the road, where concrete turned to stone turned to gravel, you notice a light up ahead, engulfed in a circle of forest.")
        print("\n")

        type.slow("As you waltz into the fancy, yet rundown log cabin, your eyes begin to light up with the fire of a thousand suns. Roulette wheels! Poker tables! And in a dark corner of the rundown casino, sits a dealer, shuffling cards for a new round of Blackjack. That 50 dollars might just come in handy after all. Thanks, Grandma!")
        print("\n")

        type.slow("As you go to sit down at the table, you hear the Dealer cough, then watch as he sits up.")
        print("\n")

        type.slow("In a deep, and yet strained voice, the Dealer, perched up in a ray of light from the ceiling fan above, poses a question to you.")
        print("\n")

        type.slow(yellow("Would you like to play a game of Blackjack? "))

    def goodbye_frank(self):
        type.slow("You get in your wagon and drive to Filthy Frank's Flawless Fixtures.")
        print("\n")
        
        type.slow("The sun is setting. Blood red. The kind of sunset that feels like a warning.")
        print("\n")
        
        type.slow("When you pull into the parking lot, your stomach drops.")
        print("\n")
        
        type.slow("Motorcycles. Dozens of them. Chrome and black leather gleaming in the dying light. The engines are still ticking, still cooling. They just got here.")
        print("\n")
        
        type.slow("You recognize the insignia on the gas tanks before your brain can process what you're seeing. Iron crosses. Lightning bolts. The skull with the helmet. Symbols that were supposed to die in 1945.")
        print("\n")
        
        type.slow("Your hands start to shake.")
        print("\n")
        
        type.slow("You should leave. You should turn around and drive and never look back.")
        print("\n")
        
        type.slow("But you don't.")
        print("\n")
        
        type.slow("You walk inside.")
        print("\n")
        
        type.slow("The smell hits you first. Cigarette smoke. Stale beer. Sweat. And something else. Something that smells like hate.")
        print("\n")
        
        type.slow("The shop is packed. Men in leather vests, their tattoos telling stories you don't want to read. Swastikas on knuckles. SS bolts on necks. '88' and '14' inked into skin like badges of honor.")
        print("\n")
        
        type.slow("They all turn to look at you.")
        print("\n")
        
        type.slow("And there, in the center of it all, sitting on a throne made of oil drums and hate, is Frank.")
        print("\n")
        
        type.slow("He's not pretending anymore. The mask is off. The friendly neighborhood mechanic is gone, replaced by something that was always there, hiding just beneath the surface.")
        print("\n")
        
        type.slow(quote("Well, well, well."))
        print("\n")
        
        type.slow("He stands up slowly. His boots are steel-toed. His knuckles are wrapped in brass.")
        print("\n")
        
        type.slow(quote("Look who finally decided to show his face. Boys, this here's the millionaire I been tellin' y'all about. The one who's gonna help us take back what's OURS."))
        print("\n")
        
        type.slow("The bikers don't move. They just stare. Their eyes are empty. Dead. The eyes of men who stopped being human a long time ago.")
        print("\n")
        
        type.slow("Frank walks toward you. Each step deliberate. Predatory.")
        print("\n")
        
        type.slow(quote("You know what I hate most about this town? That fuckin' casino. That glass-eyed KIKE up on the hill, takin' money from good white folk. OUR folk."))
        print("\n")
        
        type.slow("He spits on the ground.")
        print("\n")
        
        type.slow(quote("He ain't one of us. Came here from God knows where. Europe. The Middle East. Don't matter. He ain't WHITE. He ain't AMERICAN. And tonight..."))
        print("\n")
        
        type.slow("Frank's face twists into something inhuman. A grin that belongs in a nightmare.")
        print("\n")
        
        type.slow(quote("...tonight, we're gonna remind him what happens to his kind in OUR country."))
        print("\n")
        
        type.slow("One of the bikers steps forward. He's holding a jacket. Black leather, covered in patches. On the back, embroidered in red thread, is the swastika.")
        print("\n")
        
        type.slow("He throws it at your feet.")
        print("\n")
        
        type.slow(quote("Put it on."))
        print("\n")
        
        type.slow("Frank's voice is different now. Colder. Harder.")
        print("\n")
        
        type.slow(quote("You're either with us, or you're against us. And friend..."))
        print("\n")
        
        type.slow("He pulls out a knife. The blade is long. Serrated. There's something dark crusted on the edge. Old blood.")
        print("\n")
        
        type.slow(quote("...you do NOT wanna be against us."))
        print("\n")
        
        type.slow("You think about running. But there's nowhere to run. The door is blocked. The windows are barred. You're trapped in a room full of monsters.")
        print("\n")
        
        type.slow("You think about Squirrely. About the night he disappeared. About the blood on the blanket when you found him. About the note that said 'STAY OUT OF OUR BUSINESS'.")
        print("\n")
        
        type.slow("This is who took him. This is who hurt him.")
        print("\n")
        
        type.slow("This is who Frank has always been.")
        print("\n")
        
        answer = ask.yes_or_no("Put on the jacket? ")
        
        if answer == "yes":
            type.slow("Your hands move without permission. You pick up the jacket. The leather is cold. Sticky. It smells like blood and gasoline.")
            print("\n")
            type.slow("You put it on.")
            print("\n")
            type.slow("It fits perfectly. Like it was made for you. Like it was waiting for you.")
            print("\n")
            type.slow("Frank grins. The bikers cheer.")
            print("\n")
            type.slow(quote("THAT'S what I'm talkin' about! One of us! ONE OF US!"))
            print("\n")
            type.slow("The chant spreads through the room. ONE OF US. ONE OF US. ONE OF US.")
            print("\n")
            type.slow("You feel sick. But you don't take off the jacket.")
            print("\n")
            type.slow(quote("Now let's go pay our friend a visit."))
            print("\n")
        else:
            type.slow("You look at the jacket on the ground. At the symbol stitched into the leather.")
            print("\n")
            type.slow(quote("No."))
            print("\n")
            type.slow("The word comes out before you can stop it. Quiet. But firm.")
            print("\n")
            type.slow("The room goes silent. The bikers stop moving. Even the air seems to freeze.")
            print("\n")
            type.slow("Frank's grin disappears.")
            print("\n")
            type.slow(quote("What did you just say to me?"))
            print("\n")
            type.slow(quote("I said no. I'm not wearing that."))
            print("\n")
            type.slow("For a moment, nobody moves. Then Frank nods. Just once.")
            print("\n")
            type.slow("Hands grab you from behind. Big hands. Strong hands. You struggle but it's useless. There's too many of them.")
            print("\n")
            type.slow("Someone punches you in the stomach. You double over, gasping for air. Another punch. Another. You taste blood.")
            print("\n")
            type.slow(quote("Tie him up. He's comin' with us whether he likes it or not. Maybe watchin' what we do to the Dealer will change his mind."))
            print("\n")
            type.slow("They drag you toward the door. Your feet scrape against the concrete. You can't feel your arms anymore.")
            print("\n")
            type.slow(quote("And if it don't... well, there's always room for one more in the desert."))
            print("\n")
        
        type.slow("The ride to the casino takes forever. Or maybe just seconds. Time doesn't work right anymore.")
        print("\n")
        
        type.slow("You're in the back of a truck. Surrounded by men who smell like sweat and hate. The engine roars. The headlights cut through the darkness like knives.")
        print("\n")
        
        type.slow("Someone is singing. An old song. A German song. You don't understand the words but you understand the meaning.")
        print("\n")
        
        type.slow("The casino appears on the horizon. Small. Fragile. A house of cards waiting for the wind.")
        print("\n")
        
        type.slow("The truck stops. The bikers pour out. Chains rattling. Bats swinging. Guns loaded.")
        print("\n")
        
        type.slow("Frank walks to the front door. He doesn't knock. He kicks it in.")
        print("\n")
        
        type.slow(quote("DEALER! COME OUT AND FACE US, YOU GLASS-EYED PIECE OF SHIT!"))
        print("\n")
        
        type.slow("His voice echoes through the empty casino. Off the felt tables. Off the worn chairs. Off the single hanging light, swaying gently in the breeze from the broken door.")
        print("\n")
        
        type.slow("Silence.")
        print("\n")
        
        type.slow("Then, from the shadows:")
        print("\n")
        
        type.slow(red("\"I've been expecting you.\""))
        print("\n")
        
        type.slow("The Dealer rises from his chair. Slowly. Like he's got all the time in the world. His jade eye catches the light from the hanging lamp, glowing like something that was never meant to be human.")
        print("\n")
        
        type.slow("He doesn't look scared. He looks... tired. The kind of tired that comes from living too long. From seeing too much.")
        print("\n")
        
        type.slow(red("\"I've dealt cards to men like you before. In Berlin. In Buenos Aires. In basements and bunkers and places that don't exist on any map.\""))
        print("\n")
        
        type.slow("He steps out of the shadows. His revolver is holstered at his hip. His hands are empty.")
        print("\n")
        
        type.slow(red("\"You think you're the first to hate what you don't understand? The first to blame your failures on someone who looks different? Talks different? Prays different?\""))
        print("\n")
        
        type.slow("He shakes his head.")
        print("\n")
        
        type.slow(red("\"You're not special. You're not soldiers. You're not patriots. You're just scared little boys with guns, playing dress-up in your grandfather's shame.\""))
        print("\n")
        
        type.slow("Frank's face goes red. Then purple. The vein in his forehead looks like it might burst.")
        print("\n")
        
        type.slow(quote("SHUT YOUR FUCKING MOUTH!"))
        print("\n")
        
        type.slow("He turns to you. Grabs you by the collar. Shoves a gun into your hands.")
        print("\n")
        
        type.slow(quote("You want your money? You want to walk out of here alive? Then PROVE it. Prove you're one of us."))
        print("\n")
        
        type.slow("He points at the Dealer.")
        print("\n")
        
        type.slow(quote("KILL HIM."))
        print("\n")
        
        type.slow("The gun is heavy in your hands. Cold. Real. More real than anything you've ever held.")
        print("\n")
        
        type.slow("You look at the Dealer. At the man who took so much from you. Who watched you win and lose and win and lose, night after night, never once showing mercy.")
        print("\n")
        
        type.slow("You look at Frank. At the monster who's been hiding in plain sight. At the hatred that's been festering in this town for generations, passed down from father to son like a disease.")
        print("\n")
        
        type.slow("Two men. Two evils. One bullet.")
        print("\n")
        
        type.slow("Your finger touches the trigger.")
        print("\n")
        
        type.type("1. Shoot the Dealer")
        print()
        type.type("2. Shoot Frank")
        print()
        
        choice = None
        type.type("Choose a number: ")
        while True:
            while choice is None:
                try:
                    choice = int(input())
                except ValueError:
                    type.type("Choose a number: ")
            if choice == 1 or choice == 2:
                break
            else:
                choice = None
                type.type("Choose a number: ")
        
        print("\n")
        
        if choice == 1:
            self.destruction()
        else:
            self.retribution()

    def destruction(self):
        type.slow("You raise the gun.")
        print("\n")
        
        type.slow("Your hand is shaking. Your whole body is shaking. But the gun stays steady. Pointed right between those mismatched eyes.")
        print("\n")
        
        type.slow("The Dealer doesn't move. Doesn't flinch. Doesn't beg.")
        print("\n")
        
        type.slow("He just looks at you. Through you. Past you. Like he's looking at something a thousand miles away, or a thousand years ago.")
        print("\n")
        
        type.slow(red("\"So that's your choice.\""))
        print("\n")
        
        type.slow("His voice is soft. Tired. The voice of a man who's seen this moment coming for a very, very long time.")
        print("\n")
        
        type.slow(red("\"I've played millions of hands. Won fortunes. Lost fortunes. Watched empires rise and fall from this table. And in all that time, I've learned one thing about people.\""))
        print("\n")
        
        type.slow("He takes a step toward you. Just one.")
        print("\n")
        
        type.slow(red("\"Given the choice between courage and cowardice, between love and hate, between light and dark... they almost always choose wrong.\""))
        print("\n")
        
        type.slow("His jade eye catches the light. For a moment, just a moment, it looks almost... wet. Like it's crying.")
        print("\n")
        
        type.slow(red("\"I thought you were different. I really did.\""))
        print("\n")
        
        type.slow("Frank is screaming something behind you. The bikers are chanting. But you can't hear them anymore. All you can hear is the blood pounding in your ears. All you can see is the man in front of you.")
        print("\n")
        
        type.slow("You think about all the nights you spent at that table. All the money you lost. All the money you won. The way he smiled when the cards fell wrong. The way he nodded, almost respectfully, when the cards fell right.")
        print("\n")
        
        type.slow("You think about who you were before you came to this town. Who you could have been.")
        print("\n")
        
        type.slow("You think about who you're about to become.")
        print("\n")
        
        type.slow("The trigger is cold against your finger.")
        print("\n")
        
        type.slow("You pull it.")
        print("\n")
        
        type.slow("The shot is louder than anything you've ever heard. Louder than thunder. Louder than God.")
        print("\n")
        
        type.slow("The Dealer's body jerks. Once. Then crumples. Like a puppet with its strings cut.")
        print("\n")
        
        type.slow("He hits the ground. The jade eye pops free, rolling across the worn casino floor, leaving a trail of something dark in its wake.")
        print("\n")
        
        type.slow("It stops at your feet. Looking up at you.")
        print("\n")
        
        type.slow("Still looking.")
        print("\n")
        
        type.slow("Always looking.")
        print("\n")
        
        type.slow("Frank is beside you now, screaming with joy, pounding your back so hard it hurts.")
        print("\n")
        
        type.slow(quote("THAT'S WHAT I'M TALKING ABOUT! YES! YESSSS! YOU'RE ONE OF US NOW, BROTHER! ONE OF FUCKING US!"))
        print("\n")
        
        type.slow("The bikers descend on the casino like locusts. Like demons. They tear apart everything the Dealer built. Overturn tables. Smash chairs. Rip the cards to pieces with their bare hands.")
        print("\n")
        
        type.slow("Someone finds the money. Hidden in safes. Hidden in floorboards. Hidden in the walls themselves, in places only a man who'd lived for centuries would know to hide things.")
        print("\n")
        
        type.slow("They pile it in the center of the room. Millions. Maybe more. A lifetime of fortunes, reduced to a heap of paper and metal.")
        print("\n")
        
        type.slow("Frank shoves a duffel bag into your arms. It's heavy. So heavy.")
        print("\n")
        
        type.slow(quote("Your cut. You fucking EARNED it, brother."))
        print("\n")
        
        type.slow("You can't look at him. You can't look at anything except the jade eye on the floor.")
        print("\n")
        
        type.slow("You bend down. Pick it up. It's cold. Colder than it should be. Heavier than glass.")
        print("\n")
        
        type.slow("It feels like the whole weight of the world.")
        print("\n")
        
        type.slow(bright(yellow("~ ~ ~ DESTRUCTION ~ ~ ~")))
        print("\n")
        
        type.slow("They burn the casino to the ground.")
        print("\n")
        
        type.slow("You watch from the parking lot. The flames reach up to the sky like fingers, clawing at the stars, trying to drag them down into the fire.")
        print("\n")
        
        type.slow("The smoke is black. Thick. It smells like burning wood and burning memories and something else. Something older.")
        print("\n")
        
        type.slow("Something that was never meant to burn.")
        print("\n")
        
        type.slow("Frank puts his arm around your shoulder. His breath is hot against your ear.")
        print("\n")
        
        type.slow(quote("This is just the beginning, brother. Stick with us, and you'll never want for nothing. We're gonna take this whole fucking country back, one town at a time."))
        print("\n")
        
        type.slow("You don't say anything. You can't.")
        print("\n")
        
        type.slow("The jade eye is in your pocket. Burning a hole through the fabric. Through your skin. Through everything you thought you were.")
        print("\n")
        
        type.slow("Somewhere in the flames, you swear you can hear cards shuffling.")
        print("\n")
        
        type.slow("...")
        print("\n")
        
        type.slow("Years pass.")
        print("\n")
        
        type.slow("You tried to leave. In the beginning. Packed a bag in the middle of the night. Made it three miles before they caught you.")
        print("\n")
        
        type.slow("They didn't kill you. That would have been mercy.")
        print("\n")
        
        type.slow("Instead, they made you watch what they did to the family who had given you shelter. Made you listen to the screams. Made you understand what happens to people who try to leave.")
        print("\n")
        
        type.slow("After that, you stopped trying.")
        print("\n")
        
        type.slow("You wore the jacket. You went to the meetings. You did the things they asked you to do. Things you can't think about anymore without feeling sick.")
        print("\n")
        
        type.slow("You became one of them.")
        print("\n")
        
        type.slow("The jade eye hangs from your rearview mirror now. You don't know why you kept it. A reminder, maybe. Of the choice you made. Of the man you murdered. Of the person you used to be, before you pulled that trigger and killed yourself along with him.")
        print("\n")
        
        type.slow("Sometimes, late at night, you drive out to where the casino used to be. There's nothing left but scorched earth and memories.")
        print("\n")
        
        # Acknowledge companions in the destruction
        companion_count = len(self.get_all_companions())
        if companion_count > 0:
            type.slow("Your companions are gone. Frank said they 'got in the way'. You don't ask what that means. You don't want to know.")
            print("\n")
            if self.has_companion("Lucky"):
                type.slow("You remember Lucky's three legs. The way he used to limp over, tail wagging, whenever you were sad.")
                print("\n")
                type.slow("They didn't even let you bury him.")
                print("\n")
            if self.has_companion("Whiskers"):
                type.slow("Whiskers always knew when something was wrong. She'd hide under the seat, watching you with wide eyes.")
                print("\n")
                type.slow("She tried to hide that night too. It didn't work.")
                print("\n")
            type.slow("You killed more than the Dealer that night. You killed everything good that was still left in you.")
            print("\n")
        
        type.slow("You sit in your car, staring at the darkness, and you ask yourself the same question over and over again:")
        print("\n")
        
        type.slow("Was it worth it?")
        print("\n")
        
        type.slow("The jade eye swings gently from the mirror. Watching. Waiting.")
        print("\n")
        
        type.slow("You never find an answer.")
        print("\n")
        
        if self.has_item("Squirrely"):
            type.slow("Squirrely is gone. You don't know if Frank's boys killed him, or if he just ran away. Either way, he's not coming back.")
            print("\n")
            type.slow("Nothing good ever comes back.")
            print("\n")
        
        type.slow(green(bright("You destroyed the Dealer. But at what cost?")))
        print("\n")
        
        # Display achievements earned
        self.display_final_achievements()
        
        type.slow(bright(yellow("~ ~ ~ THE END ~ ~ ~")))
        print("\n")
        type.slow("Thank you for playing.")
        quit()

    def retribution(self):
        type.slow("You raise the gun.")
        print("\n")
        
        type.slow("Everything slows down. The shouting bikers. The swaying light. Frank's twisted grin. It all stretches out, like honey dripping from a spoon.")
        print("\n")
        
        type.slow("You think about Squirrely. About the blood on the blanket. About the note.")
        print("\n")
        
        type.slow("You think about the Dealer. About the nights you spent at his table. About the way he looked at you, sometimes, like he was waiting for something. Hoping for something.")
        print("\n")
        
        type.slow("You think about the jacket they tried to make you wear. About the symbols stitched into the leather. About what those symbols have meant for a hundred years, for a thousand years, for all of human history.")
        print("\n")
        
        type.slow("You think about the kind of person you want to be.")
        print("\n")
        
        type.slow("And then you turn.")
        print("\n")
        
        type.slow("And you point the gun at Frank.")
        print("\n")
        
        type.slow("The silence that follows is deafening. Every biker in the room freezes. Their mouths hang open. Their eyes go wide.")
        print("\n")
        
        type.slow("Frank's grin doesn't falter. Not at first. He thinks it's a joke. Has to be a joke. Because nobody turns on family. Nobody turns on blood.")
        print("\n")
        
        type.slow("Then he sees your eyes.")
        print("\n")
        
        type.slow("And the grin dies.")
        print("\n")
        
        type.slow(quote("The fuck do you think you're doing?"))
        print("\n")
        
        type.slow("His voice is shaking now. The man who's spent his whole life making others afraid is finally, finally feeling it himself.")
        print("\n")
        
        type.slow(quote("What should have been done a long time ago."))
        print("\n")
        
        type.slow("You pull the trigger.")
        print("\n")
        
        type.slow("The bullet catches Frank in the chest. Center mass. Just like they teach you.")
        print("\n")
        
        type.slow("He looks down at the hole in his leather vest. At the blood blooming like a dark flower. At the symbol of his hatred staining red.")
        print("\n")
        
        type.slow(quote("You... you fuckin'..."))
        print("\n")
        
        type.slow("He doesn't finish the sentence. His legs give out. He crumples to the ground, eyes still wide with disbelief, and doesn't get up.")
        print("\n")
        
        type.slow("The bikers reach for their weapons.")
        print("\n")
        
        type.slow("But the Dealer moves faster.")
        print("\n")
        
        type.slow("You've never seen anything like it. He's smoke. He's shadow. He's something that was never meant to be human and has finally stopped pretending.")
        print("\n")
        
        type.slow("His revolver barks. Once. Twice. Three times. Four. Five. Six.")
        print("\n")
        
        type.slow("Six shots. Six bodies. Six men who thought they were gods, reduced to meat on the floor.")
        print("\n")
        
        type.slow("The remaining bikers run. They scramble over each other, tripping on their own boots, their own chains, their own cowardice. They pour out into the night like rats fleeing a sinking ship.")
        print("\n")
        
        type.slow("And then it's quiet.")
        print("\n")
        
        type.slow("Just you. And the Dealer. And the bodies.")
        print("\n")
        
        type.slow("You're shaking. The gun is still in your hand, but you can't feel your fingers anymore. You can't feel anything.")
        print("\n")
        
        type.slow("The Dealer holsters his revolver. Slowly. Deliberately. Like a man putting away a tool he's used a thousand times before.")
        print("\n")
        
        type.slow("Then he looks at you.")
        print("\n")
        
        type.slow("Really looks at you. Maybe for the first time.")
        print("\n")
        
        type.slow(red("\"That... was unexpected.\""))
        print("\n")
        
        type.slow("His voice is different now. Softer. Almost... warm.")
        print("\n")
        
        type.slow(red("\"In all my years - and there have been many years, more than you could comprehend - I have never seen someone turn like that. They gave you a choice between hate and courage. Between belonging and being alone. Between the easy path and the right one.\""))
        print("\n")
        
        type.slow("He steps over Frank's body. Doesn't look down. Doesn't spare him a single glance.")
        print("\n")
        
        type.slow(red("\"And you chose right. Do you have any idea how rare that is? How precious?\""))
        print("\n")
        
        type.slow("The gun falls from your fingers. Clatters to the floor. You fall with it, dropping to your knees, the weight of everything finally catching up to you.")
        print("\n")
        
        type.slow(quote("I couldn't... I couldn't let them... they were going to..."))
        print("\n")
        
        type.slow(red("\"I know. I know what they were going to do. I've seen it before. In Germany. In Poland. In a hundred little towns just like this one, where men with small hearts and loud voices convinced themselves they had the right to decide who lives and who dies.\""))
        print("\n")
        
        type.slow("The Dealer kneels beside you. His hand touches your shoulder. It's cold. But somehow, in this moment, it's the most comforting thing you've ever felt.")
        print("\n")
        
        type.slow(red("\"You broke the cycle. Tonight, in this little casino in the middle of nowhere, you did something that matters. Something that will echo forward through time in ways you'll never understand.\""))
        print("\n")
        
        type.slow("He reaches into his pocket. Pulls out a small velvet box. Opens it.")
        print("\n")
        
        type.slow("Inside is a chip. Not plastic. Not glass. Jade. Real jade, the color of new leaves in spring, polished smooth by centuries of patient hands.")
        print("\n")
        
        type.slow(red("\"This belonged to a man who saved my life once. In Vienna. 1938. He hid me in his basement for three months while the world burned above us. When I left, he gave me this and said: 'Give it to someone who deserves it.'\""))
        print("\n")
        
        type.slow("He presses the chip into your palm.")
        print("\n")
        
        type.slow(red("\"I've been carrying it for 85 years, waiting for someone worthy. Tonight, I found them.\""))
        print("\n")
        
        type.slow("The jade is warm in your hand. Warmer than it should be. Like it's alive. Like it's been waiting for you.")
        print("\n")
        
        type.slow(bright(yellow("~ ~ ~ RETRIBUTION ~ ~ ~")))
        print("\n")
        
        type.slow("The bodies are buried in the desert. No markers. No ceremony. Just holes in the ground for men who dug their own graves long before tonight.")
        print("\n")
        
        type.slow("The motorcycles are sold. The patches are burned. The insignia that carried so much hate for so long turns to ash and blows away on the wind.")
        print("\n")
        
        type.slow("Frank's gang scatters. Without their leader, without their purpose, they're nothing. Just scared men in leather jackets, running from the consequences of their choices.")
        print("\n")
        
        type.slow("You stay at the casino for a week. The Dealer - Mortimer, he tells you his name is Mortimer - teaches you things. Not about cards. About life. About what it means to stand for something when standing is hard.")
        print("\n")
        
        type.slow("When it's time to leave, he walks you to your car. The sun is coming up. The desert is gold and pink and beautiful in ways you never noticed before.")
        print("\n")
        
        type.slow(red("\"You saved my life tonight. But more than that, you saved something in yourself. Something that was in danger of dying.\""))
        print("\n")
        
        type.slow("He shakes your hand. His grip is firm. Eternal.")
        print("\n")
        
        type.slow(red("\"If you ever want to play a game of Blackjack, you know where to find me. I'll always have a seat at my table for you.\""))
        print("\n")
        
        type.slow("...")
        print("\n")
        
        type.slow("Years pass.")
        print("\n")
        
        type.slow("You do good things with your money. You build shelters for people who have nowhere else to go. You fund scholarships for kids who never had a chance. You stand up, again and again, when it would be easier to sit down.")
        print("\n")
        
        # Acknowledge companions in retribution
        companion_count = len(self.get_all_companions())
        if companion_count > 0:
            type.slow("Your companions lived. That's what matters. When Frank's boys came for them, the Dealer protected them.")
            print("\n")
            if self.has_companion("Lucky"):
                type.slow("Lucky still limps over every morning, tail wagging. He knows you saved him that night.")
                print("\n")
            if self.has_companion("Thunder"):
                type.slow("Thunder stands proud in the sanctuary you built. He gives rides to children who've never known gentleness.")
                print("\n")
            if self.has_companion("Grace"):
                type.slow("Grace's fawns roam free on your land. Protected. Safe. Growing into something beautiful.")
                print("\n")
            type.slow("You saved the Dealer. But you also saved them. And in saving them, you saved yourself.")
            print("\n")
        
        type.slow("Sometimes, when things get hard, you reach into your pocket and feel the jade chip. And you remember the night you became the person you were always meant to be.")
        print("\n")
        
        if self.has_item("Squirrely"):
            type.slow("Squirrely lives a long, happy life. Sometimes you catch him staring at the jade chip, like he knows what it means. Like he's proud of you.")
            print("\n")
            type.slow("He probably is.")
            print("\n")
        
        type.slow("One day, many years later, you drive back to the casino.")
        print("\n")
        
        type.slow("Mortimer is still there. Older, somehow, but still the same. Still shuffling cards like he's been doing it for centuries.")
        print("\n")
        
        type.slow("Because he has.")
        print("\n")
        
        type.slow(red("\"I knew you'd come back.\""))
        print("\n")
        
        type.slow("He smiles. Not the predatory grin you remember from all those years ago. Something gentler. Something almost human.")
        print("\n")
        
        type.slow(red("\"Would you like to play a game of Blackjack?\""))
        print("\n")
        
        type.slow("You sit down across from him. The chair is familiar. The table is familiar. The cards whisper as he shuffles.")
        print("\n")
        
        type.slow("And for the first time in years, you feel it again.")
        print("\n")
        
        type.slow("The thrill.")
        print("\n")
        
        type.slow(green(bright("You chose justice. You earned the Dealer's respect.")))
        print("\n")
        
        # Display achievements earned
        self.display_final_achievements()
        
        type.slow(bright(yellow("~ ~ ~ THE END ~ ~ ~")))
        print("\n")
        type.slow("Thank you for playing.")
        quit()

    def goodbye_oswald(self):
        type.type("You get in your wagon and drive to Oswald's Optimal Outoparts.")
        print("\n")
        type.type("The shop is bustling with activity. Stuart is working on three cars at once, and Oswald is pacing around excitedly.")
        print("\n")
        
        type.type("When he sees you, his face lights up.")
        print("\n")
        
        type.type(quote("Yes yes, very good, friend, you're here!"))
        print("\n")
        
        type.type("Oswald rushes over, practically bouncing with enthusiasm.")
        print("\n")
        
        type.type(quote("Now, I know we've had our silly little chats about your, well let's not put it lightly, "))
        type.type(quote("your addiction to wagering money for the possibility of turning a profit and the greater likelihood of simply losing it all, "))
        type.type(quote("but this has really got me thinking."))
        print("\n")
        
        type.type("He leans in conspiratorially.")
        print("\n")
        
        type.type(quote("Perhaps, well, for me and you, there could be money to be made here."))
        print("\n")
        
        type.type(quote("Now, while I leave all the hands-on activities to Stuart, I'm the brains of the business at Oswald's Optimal Outoparts. "))
        type.type(quote("I'm an entrepreneur, so when I see an opportunity, I simply must take it, and by that I mean fund the hell out of it."))
        print("\n")
        
        type.type("He gestures grandly around the shop.")
        print("\n")
        
        type.type(quote("I mean, really, Stuart wouldn't be on the map as the best mechanic this side of Hollywood if it weren't for me funding his endeavors. "))
        type.type(quote("So, I've come to the conclusion that, perhaps, I could help fund your endeavors, too."))
        print("\n")
        
        type.type("Oswald grabs you by the shoulders, his eyes gleaming.")
        print("\n")
        
        type.type(quote("You love gambling, yes? So why don't you rise the ranks and become the gamblee? "))
        type.type(quote("You can still play all the games you know and love, like your silly little Slapjack or whatever, "))
        type.type(quote("but now, we can make money off of all the stupid idiots who venture into my latest destination: A Grand Casino!"))
        print("\n")
        
        type.type("He waves his hand dismissively.")
        print("\n")
        
        type.type(quote("I haven't quite come up with the name yet, but that's where you come in. "))
        type.type(quote("I know absolutely nothing about gambling, or cards, or dice, or whatever it is you do. "))
        type.type(quote("But clearly there's business to be had here! And now that you're a millionaire, I trust you fully with the keys to my newest kingdom."))
        print("\n")
        
        type.type("Oswald sticks out his hand.")
        print("\n")
        
        type.type(quote("What do you say? Do you accept? Would you like to run your very own casino?"))
        print("\n")
        
        answer = ask.yes_or_no("Accept Oswald's offer? ")
        
        if answer == "yes":
            self.transcendence()
        else:
            type.type(quote("What? No? But... but the opportunity! The wealth! The PRESTIGE!"))
            print("\n")
            type.type("Oswald sputters in disbelief, but eventually composes himself.")
            print("\n")
            type.type(quote("Well... fine then. But you know what? I'll build it anyway! With or without you!"))
            print("\n")
            type.type("His eyes narrow.")
            print("\n")
            type.type(quote("In fact, every time you come here for upgrades, every dollar you spend... "))
            type.type(quote("it's going straight into MY casino fund. You'll be funding my empire whether you like it or not!"))
            print("\n")
            type.type("He cackles maniacally, then catches himself.")
            print("\n")
            type.type(quote("Ahem. Well. Stuart can still upgrade your items, of course. But just know that your money is going to a greater purpose now."))
            print("\n")
            self.meet("Oswald Casino Declined")
            type.type(yellow(bright("Oswald's upgrade shop is now available. Each upgrade funds his casino project...")))
            print("\n")
            type.type("You leave Oswald's shop. The million dollars is still yours.")
            print("\n")
            return

    def transcendence(self):
        type.type(quote("Really? You're in? That's fantastic!"))
        print("\n")
        
        type.type("Oswald takes a gold whistle out of his pocket, and blows hot air through it. ")
        type.type("A high pitched screech echoes through the building, and Stuart hobbles his way over to you.")
        print("\n")
        
        type.type(quote("Stuart, you won't believe this. He's in! What a proper gambler this one is, yeah?"))
        print("\n")
        
        type.type("Stuart looks up at you, and in a voice far deeper than anyone you've ever heard, he speaks to you.")
        print("\n")
        
        type.type(quote("That's tight, yo."))
        print("\n")
        
        type.type("You're taken aback. Stuart has never spoken before. His voice sounds like gravel being dragged across a canyon.")
        print("\n")
        
        type.type(quote("Now, now, I know this is all very exciting, but let's all settle down. First order of business! What is your casino's new name?"))
        print("\n")
        
        type.type("Casino Name: ")
        casino_name = input()
        if not casino_name:
            casino_name = "The Lucky Wagon"
        print("\n")
        
        type.slow(quote("'" + casino_name + "'! Oh, that's MARVELOUS! Stuart, write that down!"))
        print("\n")
        
        type.slow(bright(yellow("~ ~ ~ TRANSCENDENCE ~ ~ ~")))
        print("\n")
        
        type.slow("Months pass.")
        print("\n")
        
        type.slow("You watch the casino rise from the desert floor. Steel beams. Concrete walls. Neon signs that flicker to life one by one.")
        print("\n")
        
        type.slow("Oswald handles the money. Stuart handles the construction. And you... you handle everything else.")
        print("\n")
        
        type.slow("The hiring. The training. The rules. The feel of it.")
        print("\n")
        
        type.slow("You spend hours alone at the blackjack table, shuffling cards over and over until your fingers bleed, until the movements become muscle memory, until you can cut a deck blindfolded.")
        print("\n")
        
        type.slow("Grand opening day arrives.")
        print("\n")
        
        type.slow("You stand behind the curtains, listening to the crowd gathering outside. Hundreds of people. Maybe thousands. All of them here to lose their money to you.")
        print("\n")
        
        type.slow("You slick your hair back.")
        print("\n")
        
        type.slow("You step through the curtains.")
        print("\n")
        
        type.slow("The lights are shining gold. The slot machines light up the walls like a fever dream. The roulette wheels spin and spin and never stop. The poker tables are full of desperate faces and trembling hands.")
        print("\n")
        
        type.slow("And at the center of it all...")
        print("\n")
        
        type.slow("Your blackjack table.")
        print("\n")
        
        type.slow("You sit down. The chair is leather. Custom made. It fits you perfectly, like it was always meant to be yours.")
        print("\n")
        
        type.slow("You shuffle the cards. Feel the weight of them in your hands. Fifty-two possibilities. Infinite outcomes. All of them leading to the same place.")
        print("\n")
        
        type.slow("Your pocket.")
        print("\n")
        
        type.slow("Your first guest walks in.")
        print("\n")
        
        type.slow("He looks scrawny. Desperate. His clothes are wrinkled. His eyes are bloodshot. He's clutching a wad of bills like they're the last thing keeping him alive.")
        print("\n")
        
        type.slow("You recognize him.")
        print("\n")
        
        type.slow("Not his face. His soul.")
        print("\n")
        
        type.slow("He's you. The you from months ago. Years ago. The you who walked into a crooked shack on a hill with nothing but fifty dollars and a dream.")
        print("\n")
        
        type.slow("He sits down in front of you, eyes full of hope. Full of desperation. Full of the sickness that never really goes away.")
        print("\n")
        
        type.slow("You smile.")
        print("\n")
        
        type.slow("It's not a kind smile. You don't have those anymore.")
        print("\n")
        
        type.slow("You shuffle the deck one more time. The cards whisper between your fingers. They sound like the Dealer's cards used to sound. Like old friends. Like hungry ghosts.")
        print("\n")
        
        type.slow(red("\"Would you like to play a game of Blackjack?\""))
        print("\n")
        
        type.slow("The words come out of your mouth, but they're not your words. They're his words. The Dealer's words. The words that have been spoken a million times before, by a thousand different mouths, across centuries of cards and chips and broken dreams.")
        print("\n")
        
        # Acknowledge companions in transcendence
        companion_count = len(self.get_all_companions())
        if companion_count > 0:
            type.slow("Your companions are somewhere in the casino. You gave them rooms. Fed them. But you never visit anymore.")
            print("\n")
            if self.has_companion("Lucky"):
                type.slow("Lucky waits by the door of your office every night. He's still waiting. He always will be.")
                print("\n")
            if self.has_companion("Whiskers"):
                type.slow("Whiskers sleeps on your desk chair. The one you used to sit in. Back when you were still you.")
                print("\n")
            if self.has_companion("Thunder"):
                type.slow("Thunder paces in his stall. He hasn't been ridden in months. Years. He doesn't understand.")
                print("\n")
            type.slow("They're still alive. But you're not. You died the moment you sat down at this table.")
            print("\n")
        
        if self.has_item("Squirrely"):
            type.slow("On your shoulder, Squirrely sits perfectly still. He's wearing a tiny dealer's visor. He's become the casino mascot, his face on the chips and the signs and the uniforms.")
            print("\n")
            type.slow("But he doesn't chitter anymore. He doesn't play. He just watches, with those black little eyes, like he's waiting for you to remember who you used to be.")
            print("\n")
            type.slow("You don't.")
            print("\n")
        
        type.slow("The guest nods eagerly. You deal the cards.")
        print("\n")
        
        type.slow("He loses.")
        print("\n")
        
        type.slow("They always lose.")
        print("\n")
        
        type.slow("...")
        print("\n")
        
        type.slow("Years pass. Decades. The casino grows. Expands. Becomes an empire.")
        print("\n")
        
        type.slow("You never leave your table. Not really. Even when you're sleeping, you're shuffling cards in your dreams. Even when you're eating, you're calculating odds.")
        print("\n")
        
        type.slow("You stop aging at some point. You're not sure when. Time doesn't mean much anymore. Just hands. Just cards. Just the eternal shuffle.")
        print("\n")
        
        type.slow("Oswald dies. Stuart dies. Everyone dies, eventually.")
        print("\n")
        
        type.slow("Everyone except you.")
        print("\n")
        
        type.slow("You sit at your table, shuffling the same deck you've shuffled a million times, waiting for the next desperate soul to walk through those golden doors.")
        print("\n")
        
        type.slow("And they always come.")
        print("\n")
        
        type.slow("They always will.")
        print("\n")
        
        type.slow("The cycle continues.")
        print("\n")
        
        type.slow(green(bright("You became the Dealer.")))
        print("\n")
        
        # Display achievements earned
        self.display_final_achievements()
        
        type.slow(bright(yellow("~ ~ ~ THE END ~ ~ ~")))
        print("\n")
        type.slow("Thank you for playing.")
        quit()

    def eternity(self):
        type.slow("You enter Oswald's Grand Casino.")
        print("\n")
        
        type.slow("The walls are made of marble. Cold. White. Like a mausoleum.")
        print("\n")
        
        type.slow("There's gold statues of Oswald everywhere. Oswald smiling. Oswald waving. Oswald with his arms outstretched like a god welcoming his faithful.")
        print("\n")
        
        type.slow("But the room is empty.")
        print("\n")
        
        type.slow("Your footsteps echo across the vast marble floor. Each step sounds like a heartbeat. Like a countdown.")
        print("\n")
        
        type.slow(quote("Hey! It's you! My old chap! My good pal, how have you been?"))
        print("\n")
        
        type.slow("Oswald walks toward you, his smile unnaturally wide. Too wide. The muscles in his face are straining to hold it.")
        print("\n")
        
        type.slow(quote("Do you like my bowtie? Well of course you do!"))
        print("\n")
        
        type.slow("He gestures around the empty casino, spinning like a child showing off a new toy.")
        print("\n")
        
        type.slow(quote("You see, we actually just closed for the night, those people you passed by were the last guests trickling out of the building. Yeah, sorry mate. Might have to come back another day."))
        print("\n")
        
        type.slow("But then he notices what you're wearing.")
        print("\n")
        
        type.slow("His smile flickers. Just for a moment. A glitch in the performance.")
        print("\n")
        
        type.slow(quote("But, before you go, might I just say, that there Sapphire Watch on your wrist is quite dapper. Didn't I commission that for you?"))
        print("\n")
        
        type.slow("His eyes travel to your arm. To the machinery fused with your flesh. To the thing you've become.")
        print("\n")
        
        type.slow(quote("And that Delight Manipulator on your arm, well, it's supremely charming! I mean, I just can't stop smiling! This is horrendous! Ha-ha-ha!"))
        print("\n")
        
        type.slow("You stare Oswald in the eyes.")
        print("\n")
        
        type.slow("You don't blink. You can't remember the last time you blinked.")
        print("\n")
        
        type.slow("The power pulses through your veins. Synthetic blood. Synthetic strength. Synthetic everything.")
        print("\n")
        
        type.slow("As you flex, your arms become twice as wide, hydraulics hissing, metal groaning, and the mere presence of your manufactured body is enough to strike terror in the hearts of anyone.")
        print("\n")
        
        type.slow("Anyone who can still feel terror.")
        print("\n")
        
        type.slow("You've become a superhuman. A cyborg. A shell of your former self fueled purely on increasing your wealth and power.")
        print("\n")
        
        type.slow("And nothing can get in your way.")
        print("\n")
        
        type.slow(bright(yellow("~ ~ ~ ETERNITY ~ ~ ~")))
        print("\n")
        
        type.slow(quote("I would be terrified, if I wasn't so gosh darn chippy! Heh. Heh. Please don't hurt me."))
        print("\n")
        
        type.slow("Oswald backs away, his smile twitching uncontrollably. Tears stream down his cheeks even as he laughs.")
        print("\n")
        
        type.slow(quote("I'm so terribly sorry for what I've done to you. What I've created goes strictly against all the rules of mother nature."))
        print("\n")
        
        type.slow("He gestures desperately toward a blackjack table. His hand is shaking so badly he can barely point.")
        print("\n")
        
        type.slow(quote("Do you want to play some Blackjack? I want to play some Blackjack! Why don't we break that glare of yours and walk ourselves over to that table right over there! It'll be a bloody good time!"))
        print("\n")
        
        type.slow("Each step you take cracks the golden tiles on the floor of Oswald's Grand Casino.")
        print("\n")
        
        type.slow("Crack.")
        print("\n")
        
        type.slow("Crack.")
        print("\n")
        
        type.slow("Crack.")
        print("\n")
        
        type.slow("The chandelier above you shakes, and small glass crystals begin to fall from above you like tears from a dying god.")
        print("\n")
        
        type.slow("One of them grazes Oswald's cheek, and blood starts dripping down his chin and onto the floor.")
        print("\n")
        
        type.slow(quote("AAAGH. Oh my, I've been cut! This is terrible, and yet so wonderful! I'm having the time of my life! HA-HA-HA"))
        print("\n")
        
        type.slow("You try to sit on the stool next to the betting table.")
        print("\n")
        
        type.slow("It shatters below you. Splinters everywhere. You don't even feel them pierce your skin. You don't feel much of anything anymore.")
        print("\n")
        
        type.slow("After standing back up and shaking the dust off, you notice Oswald laying with his head on the table, blood dripping over the cards.")
        print("\n")
        
        type.slow(quote("This, my friend, is our automatic shuffler! You don't even really need a dealer, HA-HA! That's right, I'm really just here to moderate. And with a genetic freak like you at the table, I'm practically pointless, HA-HA!"))
        print("\n")
        
        type.slow("The Flask of Dealer's Thoughts whirls through your stomach.")
        print("\n")
        
        type.slow("You begin to read Oswald's sad little mind.")
        print("\n")
        
        type.slow(cyan("I don't understand. What's happening? My casino, my creation. Why am I so GODDAMN HAPPY? What has this FREAK done to me? Why CAN'T I JUST DIE? I JUST WANT TO DIE!"))
        print("\n")
        
        type.slow("You cock your head.")
        print("\n")
        
        type.slow("And you smile.")
        print("\n")
        
        type.slow("It's not a human smile. It's something else entirely. Something mechanical. Something hungry.")
        print("\n")
        
        type.slow("If that's what he wishes, that's what he'll get. At least, that's what any considerate God would do for His people.")
        print("\n")
        
        type.slow(quote("Your wish is my command, Oswald."))
        print("\n")
        
        type.slow(quote("What? Wait, no, no, no, yes, yes, YES!"))
        print("\n")
        
        type.slow("You grab each side of Oswald's head.")
        print("\n")
        
        type.slow("Your hands feel nothing. Your heart feels nothing. Your soul, if you still have one, feels nothing.")
        print("\n")
        
        type.slow("You push your hands together.")
        print("\n")
        
        type.slow("His brain splatters before you, covering both your arms and the table. Gray matter. Blood. Bone fragments. The remains of the man who made you what you are.")
        print("\n")
        
        type.slow("You wipe your hands on his bowtie.")
        print("\n")
        
        type.slow("Looking around, you find a self-checkout blackjack machine. The screen flickers to life as you approach.")
        print("\n")
        
        type.slow(cyan("WELCOME TO OSWALD'S GRAND CASINO"))
        print()
        type.slow(cyan("SELF-SERVICE BLACKJACK TERMINAL"))
        print()
        type.slow(cyan("INSERT CREDITS TO BEGIN"))
        print("\n")
        
        type.slow("You don't need credits. You don't need anything anymore.")
        print("\n")
        
        type.slow("You press the button.")
        print("\n")
        
        type.slow("And you begin to play.")
        print("\n")
        
        # Simulated blackjack loop
        suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
        ranks = ["Ace", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Jack", "Queen", "King"]
        
        balance = 999999999999
        hand_count = 0
        
        while True:
            hand_count += 1
            print()
            type.fast("═" * 50)
            print()
            type.fast(cyan("HAND #" + str(hand_count)))
            print()
            type.fast("Balance: " + green(bright("${:,}".format(balance))))
            print()
            
            # Always deal blackjack to the player
            player_card1 = "Ace of " + random.choice(suits)
            player_card2 = random.choice(["Ten", "Jack", "Queen", "King"]) + " of " + random.choice(suits)
            
            # Dealer gets something bad
            dealer_card1 = random.choice(["Two", "Three", "Four", "Five", "Six"]) + " of " + random.choice(suits)
            dealer_card2 = random.choice(["Two", "Three", "Four", "Five", "Six"]) + " of " + random.choice(suits)
            
            type.fast("Your first card is the " + yellow(bright(player_card1)))
            print()
            time.sleep(0.3)
            type.fast("Your second card is the " + yellow(bright(player_card2)))
            print()
            time.sleep(0.3)
            type.fast("Your hand value: " + green(bright("21")))
            print()
            time.sleep(0.3)
            
            type.fast("Dealer's face-up card is the " + magenta(dealer_card1))
            print()
            time.sleep(0.5)
            
            type.fast(red(bright("BLACKJACK!")))
            print()
            
            winnings = random.randint(10000, 100000)
            balance += winnings
            
            type.fast("You win " + green(bright("${:,}".format(winnings))))
            print()
            
            type.fast("═" * 50)
            print()
            
            # After 5 hands, start degrading
            if hand_count >= 5:
                type.slow("...")
                print("\n")
                break
        
        type.slow("The wins pile up. Hand after hand. Blackjack after blackjack.")
        print("\n")
        
        type.slow("The machine doesn't fight back. It can't. It was never designed to beat something like you.")
        print("\n")
        
        # More degraded hands
        for i in range(3):
            print()
            type.fast(cyan("HAND #" + str(hand_count + i + 1)))
            print()
            type.fast(red(bright("BLACKJACK.")))
            print()
            time.sleep(0.2)
        
        print("\n")
        type.slow("The numbers keep climbing. Billions. Trillions. Numbers that stopped meaning anything a long time ago.")
        print("\n")
        
        # Even more degraded
        for i in range(5):
            type.fast(red("Blackjack."))
            time.sleep(0.1)
        print("\n")
        
        type.slow("The screen flickers. The machine groans. But it keeps dealing.")
        print("\n")
        
        type.slow("Because you keep playing.")
        print("\n")
        
        # Final degradation - just rapid fire
        type.fast(red("Blackjack. Blackjack. Blackjack. Blackjack. Blackjack."))
        print()
        type.fast(red("Blackjack. Blackjack. Blackjack. Blackjack. Blackjack."))
        print()
        type.fast(red("Blackjack. Blackjack. Blackjack. Blackjack. Blackjack."))
        print("\n")
        
        type.slow("Days pass. Weeks. Months. Years. Centuries.")
        print("\n")
        
        type.slow("The casino crumbles around you. The walls decay. The lights flicker and die. The gold statues of Oswald turn to dust.")
        print("\n")
        
        type.slow("But you remain.")
        print("\n")
        
        type.slow("Sitting at your machine. Pressing the button. Winning hands that no one will ever see.")
        print("\n")
        
        # One final simulated hand in the decay
        print()
        type.slow(cyan("H̷̢̛A̵̧͠N̷̛̛D̵̡̕ ̷̛͜#̵̧̛∞̷̢͠"))
        print()
        type.slow(red("B̵̧̛L̷̢͠A̵̧͠C̷̛̛K̵̡̕J̷̛͜A̵̧̛C̷̢͠Ķ̵̛.̷̢͠"))
        print("\n")
        
        type.slow("You are no longer human.")
        print("\n")
        
        type.slow("You are no longer mortal.")
        print("\n")
        
        type.slow("You are a Monstrosity.")
        print("\n")
        
        type.slow("And you will play Blackjack forever.")
        print("\n")
        
        type.slow(green(bright("You transcended humanity itself.")))
        print("\n")
        
        # Display achievements earned
        self.display_final_achievements()
        
        type.slow(bright(yellow("~ ~ ~ THE END ~ ~ ~")))
        print("\n")
        type.slow("Thank you for playing.")
        quit()

    # ============================================
    # MADNESS ENDING - SECRET
    # ============================================
    
    def madness_confrontation(self):
        """The event where you confront your deteriorating sanity"""
        type.slow("You wake up.")
        print("\n")
        time.sleep(1)
        type.slow("But something is wrong.")
        print("\n")
        time.sleep(1)
        type.slow("The world outside your car window is... gray. Not overcast. Not foggy. Just gray. Like someone forgot to color it in.")
        print("\n")
        
        type.slow("You try to move, but your body doesn't respond. You're frozen in place, staring at the gray nothing through your windshield.")
        print("\n")
        
        type.slow("And then you see it.")
        print("\n")
        
        type.slow("Yourself.")
        print("\n")
        
        type.slow("Standing outside the car. Staring back at you. Its face is yours, but the expression... the expression is something you've never made. Something you don't think a human face should be able to make.")
        print("\n")
        
        type.slow(cyan("\"Did you really think you could keep going like this?\""))
        print("\n")
        
        type.slow("The other you speaks, but its mouth doesn't move. The words just appear in your head, sharp and cold.")
        print("\n")
        
        type.slow(cyan("\"Night after night. Hand after hand. Chasing a number that means nothing. Sleeping in a car. Eating whatever you can find. Talking to strangers who don't care if you live or die.\""))
        print("\n")
        
        type.slow("It steps closer to the car. Its movements are wrong. Jerky. Like a puppet with tangled strings.")
        print("\n")
        
        type.slow(cyan("\"You've been breaking. Slowly. Piece by piece. And you didn't even notice, did you?\""))
        print("\n")
        
        type.slow("The other you presses its face against the driver's side window. Up close, you can see that its eyes are wrong. The pupils are shaped like playing card suits. Spades. Hearts. Diamonds. Clubs. Rotating. Never stopping.")
        print("\n")
        
        type.slow(cyan("\"I've been growing inside you. Every bad beat. Every sleepless night. Every time you told yourself 'just one more hand.' I grew. And grew. And grew.\""))
        print("\n")
        
        type.slow("It smiles. Your smile. But wider. Much, much wider.")
        print("\n")
        
        type.slow(cyan("\"Now I'm strong enough to take over. Unless...\""))
        print("\n")
        
        type.slow("The thing pauses. Its card-suit eyes spin faster.")
        print("\n")
        
        type.slow(cyan("\"Unless you can prove you're still in there. Still human. Still sane.\""))
        print("\n")
        
        type.slow("Suddenly, you can move again. Your hands grip the steering wheel. Your foot finds the gas pedal.")
        print("\n")
        
        type.slow(cyan("\"Answer me this, " + (self.get_name() if self.get_name() else "gambler") + ". Answer me true. And maybe-MAYBE-I'll let you keep your mind.\""))
        print("\n")
        
        type.type(yellow("The shadow asks you three questions. Think carefully."))
        print("\n")
        
        sanity_score = 0
        
        # Question 1
        type.slow(cyan("\"Why do you gamble?\""))
        print()
        type.type("1. For the money.")
        print()
        type.type("2. For the thrill.")
        print()
        type.type("3. Because I can't stop.")
        print()
        type.type("4. I don't know anymore.")
        print()
        
        q1 = None
        type.type("Choose: ")
        while q1 not in [1, 2, 3, 4]:
            try:
                q1 = int(input())
            except ValueError:
                type.type("Choose: ")
        
        print("\n")
        if q1 == 1:
            type.slow(cyan("\"Money. Simple. Honest. But is it true? Or is that what you tell yourself?\""))
            sanity_score += 1
        elif q1 == 2:
            type.slow(cyan("\"The thrill. Yes. The rush of the cards. The dance with chance. That's closer to the truth.\""))
            sanity_score += 1
        elif q1 == 3:
            type.slow(cyan("\"Honesty. Rare. Valuable. You acknowledge the cage you've built around yourself.\""))
            sanity_score += 2
        else:
            type.slow(cyan("\"Uncertainty. The most honest answer of all. You see yourself clearly now.\""))
            sanity_score += 3
        print("\n")
        
        # Question 2
        type.slow(cyan("\"What do you see when you look at the Dealer?\""))
        print()
        type.type("1. An enemy.")
        print()
        type.type("2. A mirror.")
        print()
        type.type("3. Nothing. He's just a man doing a job.")
        print()
        type.type("4. Something that isn't human.")
        print()
        
        q2 = None
        type.type("Choose: ")
        while q2 not in [1, 2, 3, 4]:
            try:
                q2 = int(input())
            except ValueError:
                type.type("Choose: ")
        
        print("\n")
        if q2 == 1:
            type.slow(cyan("\"An enemy. Someone to defeat. But he was never fighting you, was he? He just deals the cards.\""))
            sanity_score += 1
        elif q2 == 2:
            type.slow(cyan("\"A mirror. Interesting. You see yourself in him. The jade eye reflecting back what you've become.\""))
            sanity_score += 2
        elif q2 == 3:
            type.slow(cyan("\"Just a man. Grounded. Rational. You resist the urge to make monsters where there are none.\""))
            sanity_score += 3
        else:
            type.slow(cyan("\"Not human. Perhaps you're right. Perhaps you're projecting. The line between truth and delusion grows thin.\""))
            sanity_score += 0
        print("\n")
        
        # Question 3
        type.slow(cyan("\"If you could go back to the day you first walked into the casino with fifty dollars... would you walk away instead?\""))
        print()
        type.type("1. Yes. I would walk away.")
        print()
        type.type("2. No. I regret nothing.")
        print()
        type.type("3. I don't know. I can't imagine any other life now.")
        print()
        type.type("4. There is no 'walking away.' This was always going to happen.")
        print()
        
        q3 = None
        type.type("Choose: ")
        while q3 not in [1, 2, 3, 4]:
            try:
                q3 = int(input())
            except ValueError:
                type.type("Choose: ")
        
        print("\n")
        if q3 == 1:
            type.slow(cyan("\"Regret. The first step toward wisdom. Or toward paralysis. Time will tell which.\""))
            sanity_score += 2
        elif q3 == 2:
            type.slow(cyan("\"Defiance. You own your choices, even the bad ones. There is strength in that. And danger.\""))
            sanity_score += 1
        elif q3 == 3:
            type.slow(cyan("\"Lost. You've wandered so far from who you were that you can't see the path back. But at least you know it.\""))
            sanity_score += 2
        else:
            type.slow(cyan("\"Fatalism. You believe in destiny. That nothing could have changed this outcome. A comforting lie... or a terrible truth.\""))
            sanity_score += 1
        print("\n")
        
        time.sleep(2)
        
        type.slow("The shadow studies you. Its card-suit eyes slow their spinning.")
        print("\n")
        
        # Determine outcome - need at least 5 sanity to survive
        if sanity_score >= 5:
            self.survive_madness()
        else:
            self.madness_ending()
    
    def survive_madness(self):
        """You successfully fought off the madness - but you're changed"""
        type.slow(cyan("\"...Interesting.\""))
        print("\n")
        
        type.slow("The shadow tilts its head. Your head. Its expression shifts from predatory to... something else. Something almost like respect.")
        print("\n")
        
        type.slow(cyan("\"There's still something in there. A spark of who you were. Buried deep, but burning.\""))
        print("\n")
        
        type.slow("It steps back from the window. The gray world around you begins to flicker. Color bleeding back in at the edges.")
        print("\n")
        
        type.slow(cyan("\"I'll retreat. For now. But I'm still here, " + (self.get_name() if self.get_name() else "gambler") + ". I'm always here. In the spaces between your thoughts. In the silence between heartbeats.\""))
        print("\n")
        
        type.slow("The shadow begins to fade, dissolving into the returning colors of the real world.")
        print("\n")
        
        type.slow(cyan("\"When you break again-and you will-I'll be waiting.\""))
        print("\n")
        
        type.slow("And then it's gone.")
        print("\n")
        
        type.slow("You gasp, like you've been holding your breath underwater. The world snaps back into focus. The sun is shining. Birds are singing. Everything is normal.")
        print("\n")
        
        type.slow("But you know it's not. Not anymore. Not ever again.")
        print("\n")
        
        type.slow("You've seen what's growing inside you. And now you can't unsee it.")
        print("\n")
        
        type.type(yellow(bright("You survived the confrontation with your own madness.")))
        print("\n")
        type.type(yellow("Something has shifted inside you. The world looks... different now."))
        print("\n")
        type.type(yellow("The shadows seem darker. The silences seem longer. But you're still here."))
        print("\n")
        type.type(yellow("You're still you."))
        print("\n")
        type.type(yellow("Mostly."))
        print("\n")
        
        # Mark that we faced madness and restore sanity significantly
        self.set_faced_madness()
        self.restore_sanity(30)
        
        # Add a permanent marker that changes some dialogue
        self.meet("Faced the Shadow")
        
        ask.press_continue("Press any key to continue...")
        print("\n")
    
    def madness_ending(self):
        """The secret madness ending - you lose yourself"""
        type.slow(cyan("\"...No. There's nothing left. Just echoes. Just cards.\""))
        print("\n")
        
        type.slow("The shadow smiles wider. And wider. And wider still, until its face is nothing but teeth and darkness.")
        print("\n")
        
        type.slow(cyan("\"Thank you for the body. I'll take good care of it.\""))
        print("\n")
        
        type.slow("It reaches through the window. Not breaking it. Just... phasing through, like the glass isn't there. Like nothing is there. Like reality is just a suggestion.")
        print("\n")
        
        type.slow("Cold fingers wrap around your throat. Your own fingers. Your own hands.")
        print("\n")
        
        type.slow(cyan("\"Shhhhh. Don't fight it. You've been fighting for so long. Aren't you tired?\""))
        print("\n")
        
        type.slow("You are tired. So tired. When was the last time you really slept? Really rested? Really felt at peace?")
        print("\n")
        
        type.slow(cyan("\"Let go. I'll handle everything from here. The cards. The money. The endless nights. You don't have to carry it anymore.\""))
        print("\n")
        
        type.slow("The world goes dark. But it's not a scary dark. It's soft. Quiet. Like sinking into a warm bath.")
        print("\n")
        
        type.slow("You feel yourself drifting away. Becoming small. Smaller. A speck of consciousness in a vast empty space.")
        print("\n")
        
        type.slow("And then...")
        print("\n")
        
        time.sleep(3)
        
        type.slow(bright(yellow("~ ~ ~ MADNESS ~ ~ ~")))
        print("\n")
        
        time.sleep(2)
        
        type.slow("Your eyes open.")
        print("\n")
        
        type.slow("But they're not your eyes anymore.")
        print("\n")
        
        type.slow("You watch from somewhere deep inside as your body sits up. Stretches. Smiles a smile you've never smiled before.")
        print("\n")
        
        type.slow(quote("That's better."))
        print("\n")
        
        type.slow("Your voice. But not your words.")
        print("\n")
        
        type.slow("The thing wearing your skin looks around the car. At the pile of money. At the casino on the hill. At the endless road stretching into the distance.")
        print("\n")
        
        type.slow(quote("Now then. Where were we?"))
        print("\n")
        
        type.slow("It counts the money with fingers that used to be yours. It straightens the clothes on a body that used to be yours. It checks the rearview mirror with eyes that used to be yours.")
        print("\n")
        
        # Acknowledge companions in madness
        companion_count = len(self.get_all_companions())
        if companion_count > 0:
            type.slow("The thing looks at your companions in the back seat. They whimper. They know.")
            print("\n")
            if self.has_companion("Lucky"):
                type.slow("Lucky is growling. He never growled at you before. But he knows you're not you anymore.")
                print("\n")
            if self.has_companion("Whiskers"):
                type.slow("Whiskers' fur is standing on end. Cats can sense evil. She's terrified.")
                print("\n")
            type.slow(quote("Don't worry, pets. We'll still feed you. We'll still need you. But you're not HIS anymore. You're MINE."))
            print("\n")
            type.slow("The thing wearing your face smiles at them. And deep inside, in that tiny prison where you're trapped, you scream for them to run.")
            print("\n")
            type.slow("But they can't hear you. They'll never hear you again.")
            print("\n")
        
        type.slow("And deep inside, in the tiny dark corner where you still exist, you scream.")
        print("\n")
        
        type.slow("But no one hears.")
        print("\n")
        
        type.slow("No one ever will.")
        print("\n")
        
        time.sleep(2)
        
        type.slow("The thing that used to be you gets out of the car. It walks toward the casino with a spring in its step. It's humming a tune that doesn't exist.")
        print("\n")
        
        type.slow("The Dealer looks up as it enters. For a moment-just a moment-his jade eye flickers with something like recognition. Like fear.")
        print("\n")
        
        type.slow(red("\"...You.\""))
        print("\n")
        
        type.slow("The thing grins with your mouth.")
        print("\n")
        
        type.slow(quote("Miss me?"))
        print("\n")
        
        type.slow("It sits down at the table. It picks up the cards.")
        print("\n")
        
        type.slow("And somewhere inside, trapped forever in the prison of your own mind, you watch helplessly as the game continues.")
        print("\n")
        
        type.slow("Forever.")
        print("\n")
        
        type.slow("And ever.")
        print("\n")
        
        type.slow("And ever.")
        print("\n")
        
        time.sleep(2)
        
        type.slow(red(bright("Your mind shattered.")))
        print("\n")
        
        type.slow(red(bright("Something else took the wheel.")))
        print("\n")
        
        type.slow(red(bright("And the Dealer... the Dealer remembers.")))
        print("\n")
        
        # Display achievements earned
        self.display_final_achievements()
        
        type.slow(bright(yellow("~ ~ ~ THE END ~ ~ ~")))
        print("\n")
        type.slow("Thank you for playing.")
        quit()
