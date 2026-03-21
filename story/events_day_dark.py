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

class DayDarkMixin:
    """Dark events: addiction, crime, violence, and horror"""

    def loan_shark_visit(self):
        # EVENT: A loan shark you borrowed from finds you - demands payment with interest
        # CONDITION: Balance >= $100,000 (you look like you have money now)
        # EFFECTS: Pay = lose large sum; Refuse = brutal beating, possible death
        # BRUTAL: Can result in missing finger or death
        if self.get_balance() < 100000:
            self.day_event()
            return
        type.type("A black SUV pulls up next to your car. Two men get out. You recognize the tattoos.")
        print("\n")
        type.type("Before you can react, they're dragging you out of your car.")
        print("\n")
        type.type(quote("Remember us? Remember the money you borrowed to start this little gambling hobby of yours?"))
        print("\n")
        type.type("You don't remember. But looking at their faces, you're starting to.")
        print("\n")
        type.type(quote("$50,000. Plus interest. That's $75,000 now. You got two days."))
        print("\n")
        type.type("One of them pulls out a pair of bolt cutters. " + quote("Or we start taking fingers."))
        print("\n")
        answer = ask.option("What do you do? ", ["pay now", "beg for time", "refuse"])
        if answer == "pay now":
            if self.get_balance() >= 75000:
                type.type("You hand over " + red(bright("$75,000")) + ". Every dollar feels like a piece of your soul.")
                self.change_balance(-75000)
                print("\n")
                type.type(quote("Pleasure doing business. Don't borrow again unless you can pay."))
                print("\n")
                type.type("They leave. You're poorer, but you have all your fingers.")
                self.lose_sanity(15)
            else:
                type.type(quote("That's not enough. You're short."))
                print("\n")
                type.type("Before you can explain, one of them grabs your hand and spreads your fingers on the hood of your car.")
                print("\n")
                type.type(red(bright("CRUNCH.")))
                print("\n")
                type.type("You scream. Your pinky finger is gone. Blood pools on the hood.")
                print("\n")
                type.type(quote("That's the interest. Now pay the rest, or lose more."))
                taken = self.get_balance()
                self.change_balance(-taken)
                self.hurt(40)
                self.lose_sanity(30)
                self.add_status("Missing Finger")
                self.add_danger("Severed Finger")
        elif answer == "beg for time":
            type.type(quote("Please, I just need a few more days. I'm so close to a big win-"))
            print("\n")
            type.type("The bigger one punches you in the stomach. You double over, gasping.")
            print("\n")
            type.type(quote("Two days. Not three. Two. And we're adding another 10K for wasting our time."))
            print("\n")
            type.type("They get back in the SUV and drive away. You have 48 hours.")
            self.hurt(20)
            self.lose_sanity(20)
            self.add_danger("Loan Shark Deadline")
        else:
            type.type(quote("I'm not paying you anything. I don't even remember borrowing-"))
            print("\n")
            type.type("The bolt cutters flash. Pain explodes in your hand.")
            print("\n")
            type.type(red(bright("Your ring finger hits the pavement with a wet sound.")))
            print("\n")
            type.type("You scream. They keep hitting you. Ribs crack. Teeth loosen.")
            print("\n")
            if random.random() < 0.3:
                type.type("One of them stomps on your head. Everything goes dark.")
                print("\n")
                type.type("You don't wake up.")
                self.kill("Beat to death by loan sharks. They took your fingers as souvenirs.")
                return
            else:
                type.type("Eventually, they stop. You're lying in a pool of your own blood.")
                print("\n")
                type.type(quote("We'll be back. And next time, we take the whole hand."))
                self.hurt(70)
                self.lose_sanity(40)
                self.add_status("Missing Finger")
                self.add_danger("Loan Shark Revenge")
        print("\n")

    def the_desperate_gambler(self):
        # EVENT: A man begs you for money - he's in deep to the wrong people
        # EFFECTS: Help = lose money but save a life (or be scammed); Refuse = witness his fate
        # DARK: Witness suicide if you refuse
        type.type("A man approaches your car. He's shaking. Crying. Desperate.")
        print("\n")
        type.type(quote("Please. Please, you have to help me. I owe them money. So much money."))
        print("\n")
        type.type(quote("If I don't pay by midnight, they're going to kill me. Please. I have a daughter."))
        print("\n")
        type.type("He shows you a photo. A little girl with pigtails and a gap-toothed smile.")
        print("\n")
        answer = ask.yes_or_no("Give him money? ")
        if answer == "yes":
            amount = min(self.get_balance(), random.randint(500, 2000))
            type.type("You hand over " + red(bright("$" + str(amount))) + ". It's a lot. But his eyes...")
            self.change_balance(-amount)
            print("\n")
            if random.random() < 0.7:
                type.type(quote("Thank you. Thank you so much. You saved my life. I'll pay you back someday."))
                print("\n")
                type.type("He runs off. You never see him again. But you hope he made it.")
                self.restore_sanity(10)
                self.meet("The Desperate Man")
            else:
                type.type("He takes the money... and laughs.")
                print("\n")
                type.type(quote("Sucker. There's one born every minute."))
                print("\n")
                type.type("He walks away, counting the bills. The photo was probably fake too.")
                self.lose_sanity(15)
        else:
            type.type(quote("I'm sorry. I can't. I need every dollar I have."))
            print("\n")
            type.type("The man's face crumbles. " + quote("Then I'm already dead."))
            print("\n")
            type.type("He walks away. Toward the bridge.")
            print("\n")
            type.type("...")
            print("\n")
            type.type("An hour later, you hear sirens. You don't look. You can't look.")
            print("\n")
            type.type("But you know.")
            self.lose_sanity(25)
            self.add_status("Witnessed Death")
        print("\n")

    def withdrawal_nightmare(self):
        # EVENT: Severe gambling withdrawal - your body and mind rebel
        # CONDITION: Sanity below 30
        # EFFECTS: Physical and mental symptoms, risk of self-harm
        if self.get_sanity() >= 30:
            self.day_event()
            return
        type.type("You're drenched in sweat in your car seat. Your hands are shaking. Your heart is racing.")
        print("\n")
        type.type("You NEED to gamble. The urge is overwhelming. It's not a want. It's a NEED.")
        print("\n")
        type.type("But the casino is closed. It's 3 AM. You can't. You CAN'T.")
        print("\n")
        type.type("Your skin crawls. You scratch your arms until they bleed. It doesn't help.")
        print("\n")
        type.type("You punch the steering wheel. Again. Again. Your knuckles split open.")
        print("\n")
        answer = ask.option("What do you do? ", ["ride it out", "drive to casino anyway", "hurt yourself more"])
        if answer == "ride it out":
            type.type("You grip the steering wheel until your fingers go white. You breathe. In. Out. In. Out.")
            print("\n")
            type.type("Hours pass. The sun rises. The shaking stops, eventually.")
            print("\n")
            type.type("You survived. But you know it'll happen again.")
            self.hurt(10)
            self.lose_sanity(10)
        elif answer == "drive to casino anyway":
            type.type("You drive. 90 miles an hour. Running red lights. You don't care.")
            print("\n")
            type.type("The casino is dark. Closed. You pound on the doors until security comes.")
            print("\n")
            type.type(quote("Sir, we're closed. You need to leave or we'll call the police."))
            print("\n")
            type.type("You sit in the parking lot until they open. Four hours. Just waiting.")
            self.lose_sanity(20)
        else:
            type.type("You need to feel something else. Anything else.")
            print("\n")
            type.type("The pain helps, for a moment. Then it doesn't.")
            print("\n")
            type.type("You look at your arms. At the blood. At what you've become.")
            self.hurt(25)
            self.lose_sanity(15)
            self.add_danger("Self-Harm Wounds")
        print("\n")

    def organ_harvester(self):
        # EVENT: Someone offers to buy your kidney - you're worth more in parts
        # CONDITION: Balance below $1,000 (desperate) OR health below 30
        # EFFECTS: Accept = money but permanent health loss; Refuse = nothing
        # DARK: Selling body parts for gambling money
        if self.get_balance() >= 1000 and self.get_health() >= 30:
            self.day_event()
            return
        type.type("A clean-looking van pulls up. A man in scrubs steps out. He's smiling.")
        print("\n")
        type.type(quote("You look like someone who could use some money. Am I right?"))
        print("\n")
        type.type("He pulls out a business card. 'ORGAN SOLUTIONS - We Pay Top Dollar.'")
        print("\n")
        type.type(quote("One kidney. $40,000. Cash. Tonight. You won't even miss it."))
        print("\n")
        answer = ask.yes_or_no("Sell your kidney? ")
        if answer == "yes":
            type.type("You get in the van. Part of you knows this is insane. The rest of you needs the money.")
            print("\n")
            type.type("...")
            print("\n")
            type.type("You wake up in a motel room. There's a fresh scar on your side. An envelope on the nightstand.")
            print("\n")
            type.type(green(bright("$40,000")) + " in cash. Just like they promised.")
            self.change_balance(40000)
            print("\n")
            type.type("You're lighter now. In more ways than one. Your maximum health is permanently reduced.")
            self.hurt(30)
            self.add_status("One Kidney")
            self.lose_sanity(20)
        else:
            type.type(quote("No thanks. I'm not that desperate yet."))
            print("\n")
            type.type("The man shrugs. " + quote("Yet. I like that word. Here's my card if you change your mind."))
            print("\n")
            type.type("He drives away. You throw the card in the trash. Then you fish it back out.")
            print("\n")
            type.type("Just in case.")
        print("\n")

    def casino_overdose(self):
        # EVENT: Find someone ODing in the casino bathroom
        # EFFECTS: Help = risk getting blamed, possibly save a life; Ignore = they die, lose sanity
        # DARK: Drug use and death in casinos
        type.type("You head into the casino and walk into the bathroom. You freeze.")
        print("\n")
        type.type("Someone's on the floor. Blue lips. Needle still in their arm. Foam at the mouth.")
        print("\n")
        type.type("They're not breathing. Or barely breathing. You can't tell.")
        print("\n")
        answer = ask.option("What do you do? ", ["call for help", "try to help yourself", "walk away"])
        if answer == "call for help":
            type.type("You run out screaming for help. Security comes. Paramedics arrive.")
            print("\n")
            if random.random() < 0.6:
                type.type("They stabilize her. She's going to make it. Barely.")
                print("\n")
                type.type("A security guard pats you on the shoulder. " + quote("You saved her life."))
                self.restore_sanity(5)
            else:
                type.type("It's too late. She's gone before the paramedics even arrive.")
                print("\n")
                type.type("You watch them cover her body with a sheet. She was young. Maybe 25.")
                self.lose_sanity(20)
                self.add_status("Witnessed Death")
        elif answer == "try to help yourself":
            type.type("You check for a pulse. Faint. You start CPR, trying to remember how it works.")
            print("\n")
            type.type("Chest compressions. Mouth to mouth. Chest compressions. Her lips are cold.")
            print("\n")
            if random.random() < 0.4:
                type.type("She gasps. Coughs. Vomits. But she's BREATHING.")
                print("\n")
                type.type("Someone finally notices and calls 911. By the time they arrive, she's conscious.")
                print("\n")
                type.type(quote("You... saved me...") + " she whispers. Her eyes are hollow. But alive.")
                self.restore_sanity(15)
                self.meet("Casino Survivor")
            else:
                type.type("She doesn't respond. You keep trying. Keep pushing. Keep breathing.")
                print("\n")
                type.type("But she's gone. You feel the moment she leaves.")
                print("\n")
                type.type("Her eyes are still open. Staring at nothing.")
                self.lose_sanity(30)
                self.add_status("CPR Failure")
        else:
            type.type("You back out slowly. Pretend you didn't see anything. It's not your problem.")
            print("\n")
            type.type("You go back to the tables. Try to focus on the cards. Try not to think about it.")
            print("\n")
            type.type("An hour later, you hear the sirens. Too late. You know it's too late.")
            print("\n")
            type.type("You keep playing. What else can you do?")
            self.lose_sanity(25)
            self.add_status("Ignored Death")
        print("\n")

    def cancer_diagnosis(self):
        # EVENT: A cough that won't go away leads to a devastating diagnosis
        # CONDITION: Health below 50 OR has "Chronic Cough" status
        # EFFECTS: Major health reduction, sanity loss, expensive treatment choice
        # MEDICAL: Terminal illness
        if self.get_health() >= 50 and not self.has_status("Chronic Cough"):
            self.day_event()
            return
        type.type("Sitting in your car, the cough has been getting worse. You finally drive to a clinic.")
        print("\n")
        type.type("X-rays. Blood tests. Waiting. So much waiting.")
        print("\n")
        type.type("The doctor sits down. She doesn't meet your eyes.")
        print("\n")
        type.type(quote("I'm sorry. It's cancer. Stage 3 lung cancer."))
        print("\n")
        type.type("The world goes silent. Your ears ring. This isn't real.")
        print("\n")
        type.type(quote("Without treatment, you have maybe six months. With treatment... maybe two years."))
        print("\n")
        type.type(quote("Treatment will cost around $50,000. We can discuss payment plans..."))
        print("\n")
        answer = ask.option("What do you do? ", ["pay for treatment", "refuse treatment", "break down"])
        if answer == "pay for treatment":
            if self.get_balance() >= 50000:
                type.type("You hand over " + red(bright("$50,000")) + ". Your life savings. For a chance at life.")
                self.change_balance(-50000)
                self.add_status("Chemotherapy")
                type.type(" The chemotherapy starts next week.")
            else:
                type.type(quote("I... I don't have enough."))
                print("\n")
                type.type("The doctor sighs. " + quote("There are... other options. Experimental treatments. Clinical trials."))
                print("\n")
                type.type("You sign up for everything. Anything.")
                self.add_status("Experimental Treatment")
            self.lose_sanity(30)
        elif answer == "refuse treatment":
            type.type(quote("No. No treatment. If I'm going to die, I'm going to die on my terms."))
            print("\n")
            type.type("The doctor nods. She's seen this before. " + quote("It's your choice. I'm sorry."))
            print("\n")
            type.type("You walk out. Six months. Maybe less. Better make it count.")
            self.lose_sanity(25)
            self.add_status("Terminal")
            self.add_danger("Cancer Untreated")
        else:
            type.type("You break down. Right there in the office. Sobbing. Screaming.")
            print("\n")
            type.type("The doctor holds your hand. Lets you cry. She's seen this before too.")
            print("\n")
            type.type("Eventually, the tears stop. You're empty. Hollow.")
            print("\n")
            type.type(quote("Take some time. Think about it. Come back when you're ready."))
            self.lose_sanity(40)
        print("\n")

    def the_bridge_call(self):
        # EVENT: At your lowest point, the bridge calls to you
        # CONDITION: Sanity below 15
        # EFFECTS: Player must make a choice - potentially fatal
        # MENTAL HEALTH: Suicidal ideation - explicit content warning
        if self.get_sanity() >= 15:
            self.day_event()
            return
        type.type("You start your car and drive. You don't know where. Just... driving.")
        print("\n")
        type.type("The bridge appears ahead. The big one. The one over the gorge.")
        print("\n")
        type.type("Your car slows. Stops in the middle. You get out.")
        print("\n")
        type.type("The wind is cold. The water is far below. Black and quiet.")
        print("\n")
        type.type("It would be so easy. Just climb over the railing. One step.")
        print("\n")
        type.type("No more gambling. No more losing. No more living in a car like an animal.")
        print("\n")
        type.type("No more...")
        print("\n")
        answer = ask.option("", ["climb the railing", "call someone", "walk away"])
        if answer == "climb the railing":
            type.type("You climb over the railing. The metal is cold. The wind pushes at you.")
            print("\n")
            type.type("You look down. It's so far. So final.")
            print("\n")
            if random.random() < 0.6:
                type.type("A car stops. A woman runs toward you.")
                print("\n")
                type.type(quote("DON'T! Please! Please don't!"))
                print("\n")
                type.type("She's crying. A stranger, crying for you. When did you last have someone cry for you?")
                print("\n")
                type.type("She talks you down. Holds your hand. Calls for help.")
                print("\n")
                type.type("Hours later, you're in a hospital bed. Alive. You're not sure how you feel about that.")
                self.add_status("Survived Attempt")
                self.lose_sanity(10)
                self.meet("Bridge Angel")
            else:
                type.type("You lean forward. Let go.")
                print("\n")
                type.type("The fall is longer than you expected. Almost peaceful.")
                print("\n")
                type.type("The last thing you see is the stars above, spinning.")
                self.kill("Jumped from the bridge. The chase for a million ended here.")
                return
        elif answer == "call someone":
            type.type("You pull out your phone. Who do you even call?")
            print("\n")
            type.type("You dial the suicide hotline. Your hands are shaking so bad you can barely hit the numbers.")
            print("\n")
            type.type("Someone answers. A voice. Calm. Kind.")
            print("\n")
            type.type(quote("Hello. You've reached the crisis line. You're not alone. Can you tell me your name?"))
            print("\n")
            type.type("You talk. For hours. Until the sun comes up.")
            print("\n")
            type.type("You're still here. Still breathing. That's something.")
            self.restore_sanity(10)
            self.add_status("Called for Help")
        else:
            type.type("You step back. Get in your car. Drive away.")
            print("\n")
            type.type("Not tonight. Not like this.")
            print("\n")
            type.type("You don't know why. You don't feel better. You don't feel anything.")
            print("\n")
            type.type("But you're still here. And tomorrow is another day.")
            self.restore_sanity(5)
        print("\n")

    def the_relapse(self):
        # EVENT: After a big win, the addiction demands MORE
        # CONDITION: Won big recently (balance increased by 50K+ today)
        # EFFECTS: Risk losing everything chasing the high
        # ADDICTION: The insatiable need for more
        if not hasattr(self, '_today_winnings') or self._today_winnings < 50000:
            self.day_event()
            return
        type.type("You're sitting in your car outside the casino. You won big today. Really big. You should walk away.")
        print("\n")
        type.type("But the cards are still there. The dealer is waiting. The chips are calling.")
        print("\n")
        type.type("Just one more hand. One more. You're HOT right now.")
        print("\n")
        type.type("Your hands are shaking. Not from fear. From NEED.")
        print("\n")
        answer = ask.yes_or_no("Go back to the tables? ")
        if answer == "yes":
            type.type("You sit back down. The dealer smiles. " + quote("Back for more?"))
            print("\n")
            type.type("Hours pass. You don't notice. The world shrinks to just you and the cards.")
            print("\n")
            outcome = random.randint(1, 10)
            if outcome <= 3:
                winnings = random.randint(10000, 50000)
                type.type("Lady luck is still with you. You walk out with another " + green(bright("$" + str(winnings))) + "!")
                self.change_balance(winnings)
                type.type(" The high is incredible. Nothing else matters.")
                self.lose_sanity(10)
            elif outcome <= 7:
                losses = random.randint(20000, 60000)
                actual_loss = min(self.get_balance(), losses)
                type.type("It all goes wrong. Every hand. Every bet. You can't stop.")
                print("\n")
                type.type("When you finally stand up, you've lost " + red(bright("$" + str(int(actual_loss)))) + ".")
                self.change_balance(-actual_loss)
                self.lose_sanity(20)
            else:
                type.type("You don't stop. You CAN'T stop. Hand after hand. Bet after bet.")
                print("\n")
                type.type("When security finally kicks you out, you're broke. Everything. Gone.")
                print("\n")
                type.type(quote("I'll win it back. I'll win it all back tomorrow."))
                self.change_balance(-self.get_balance())
                self.lose_sanity(35)
        else:
            type.type("You force yourself to walk away. Every step is agony.")
            print("\n")
            type.type("The cards call to you. The chips whisper your name.")
            print("\n")
            type.type("But you keep walking. Tonight, you won.")
            print("\n")
            type.type("The battle, at least. The war continues.")
            self.restore_sanity(15)
        print("\n")

    def casino_hitman(self):
        # EVENT: You've won too much - the casino sends someone to "talk" to you
        # CONDITION: Balance >= $800,000
        # EFFECTS: Various outcomes including death, injury, or escape
        # VIOLENCE: Professional intimidation/assassination
        if self.get_balance() < 800000:
            self.day_event()
            return
        type.type("You're at the casino bar when a man sits down next to you. You didn't hear him approach.")
        print("\n")
        type.type(quote("That's a lot of money you've won. Almost a million. Impressive."))
        print("\n")
        type.type("He's not smiling. His eyes are dead. Professional.")
        print("\n")
        type.type(quote("The house doesn't like to lose. You understand that, right?"))
        print("\n")
        type.type("Under the bar, you feel something cold press against your ribs. A gun.")
        print("\n")
        type.type(quote("You have two choices. Walk away now. Leave the state. Never come back."))
        type.type(quote(" Or..."))
        print("\n")
        type.type("He doesn't finish the sentence. He doesn't have to.")
        print("\n")
        answer = ask.option("What do you do? ", ["agree to leave", "offer money", "fight back"])
        if answer == "agree to leave":
            type.type(quote("Smart. I like smart people. They live longer."))
            print("\n")
            type.type("He stands up. The gun disappears.")
            print("\n")
            type.type(quote("You have 24 hours to leave. Take your money. Don't come back."))
            print("\n")
            type.type("You watch him walk away. Your hands won't stop shaking.")
            self.lose_sanity(25)
            self.add_danger("Casino Exile")
        elif answer == "offer money":
            type.type(quote("How much to make this go away?"))
            print("\n")
            type.type("He considers. " + quote("$200,000. Now. And you don't come back for a year."))
            print("\n")
            if self.get_balance() >= 200000:
                answer2 = ask.yes_or_no("Pay $200,000? ")
                if answer2 == "yes":
                    type.type("You transfer the money. He checks his phone. Nods.")
                    self.change_balance(-200000)
                    print("\n")
                    type.type(quote("Pleasure doing business. See you in a year."))
                    self.lose_sanity(15)
                else:
                    type.type("His expression doesn't change. The gun presses harder.")
                    print("\n")
                    type.type(quote("Wrong answer."))
                    print("\n")
                    type.type(red(bright("BANG.")))
                    print("\n")
                    type.type("The bar goes silent. You're on the floor. Blood pooling beneath you.")
                    print("\n")
                    if self.has_item("Phoenix Feather") or self.has_item("White Feather"):
                        feather = "Phoenix Feather" if self.has_item("Phoenix Feather") else "White Feather"
                        type.type("Something in your pocket blazes with sudden heat. The " + cyan(bright(feather)) + " ignites.")
                        print("\n")
                        type.type("Amber light floods through your chest. The bullet wounds seal themselves. The feather disintegrates into ash.")
                        print("\n")
                        type.type("The hitman is already walking away. He thinks you're dead. You give yourself thirty seconds on the floor, then you run.")
                        self.use_item(feather)
                        self.hurt(20)
                        self.lose_sanity(20)
                    elif random.random() < 0.4:
                        type.type("The last thing you hear is screaming. It might be yours.")
                        self.kill("Shot by casino enforcement. The house always wins.")
                        return
                    else:
                        type.type("You survive. Barely. The bullet missed anything vital.")
                        print("\n")
                        type.type("Weeks later, you wake up in a hospital. Your money is gone. All of it.")
                        self.change_balance(-self.get_balance())
                        self.hurt(80)
                        self.lose_sanity(40)
            else:
                type.type(quote("I don't have that much."))
                print("\n")
                type.type(quote("Then I guess we go with option two."))
                print("\n")
                if random.random() < 0.5:
                    type.type("The gun fires. You don't even feel it.")
                    self.kill("Executed by the casino. Too successful for your own good.")
                    return
                else:
                    type.type("But he pauses. Sighs. " + quote("Get out. Now. Before I change my mind."))
                    print("\n")
                    type.type("You run. You've never run so fast in your life.")
                    self.lose_sanity(30)
        else:
            type.type("You knock the gun away and throw a punch.")
            print("\n")
            chance = random.randint(1, 10)
            if chance <= 2:
                type.type("The hit connects. He staggers. You grab a bottle and swing.")
                print("\n")
                type.type("He goes down. People are screaming. You run.")
                print("\n")
                type.type("You don't know if he's dead. You don't want to know.")
                self.hurt(15)
                self.lose_sanity(20)
                self.add_danger("Casino Enemy")
            elif chance <= 6:
                type.type("He's faster. The gun comes up and fires.")
                print("\n")
                type.type("Your shoulder explodes in pain. You hit the floor.")
                print("\n")
                type.type("He stands over you, gun aimed at your head.")
                print("\n")
                type.type(quote("Stupid."))
                print("\n")
                type.type("But he doesn't fire again. Just walks away. A warning.")
                self.hurt(50)
                self.lose_sanity(30)
                self.add_danger("Gunshot Wound")
            else:
                type.type("He's faster. Much faster.")
                print("\n")
                type.type("Three shots. Chest. Chest. Head.")
                print("\n")
                type.type("You're dead before you hit the floor.")
                self.kill("Killed by a professional. The casino doesn't forgive.")
                return
        print("\n")

    def the_confession(self):
        # EVENT: A dying man confesses his sins to you - you're the only one who will listen
        # EFFECTS: Hear terrible things, gain money, lose sanity
        # DARK: Hearing about horrible deeds
        type.type("An old man grabs your sleeve in the casino parking lot. He's pale. Sweating.")
        print("\n")
        type.type(quote("Please. I need to tell someone. Before I die. I need to confess."))
        print("\n")
        type.type("He looks like death. His grip is surprisingly strong.")
        print("\n")
        answer = ask.yes_or_no("Listen to him? ")
        if answer == "yes":
            type.type("He talks. For an hour. Two. You wish you hadn't listened.")
            print("\n")
            type.type("Murder. Fraud. Things you can't unhear. Victims you can't forget.")
            print("\n")
            type.type("When he's done, he presses a key into your hand.")
            print("\n")
            type.type(quote("Storage unit. 47B. Take it all. I don't need it anymore."))
            print("\n")
            type.type("He walks away. You find the storage unit. Inside: " + green(bright("$150,000")) + " in cash.")
            self.change_balance(150000)
            print("\n")
            type.type("Blood money. Does it matter? Money is money.")
            print("\n")
            type.type("But you can't forget what he told you. You never will.")
            self.lose_sanity(25)
            self.add_status("Confessor's Burden")
        else:
            type.type(quote("I'm sorry. I can't."))
            print("\n")
            type.type("His face falls. " + quote("Then it dies with me. All of it."))
            print("\n")
            type.type("He walks away. You never see him again.")
            print("\n")
            type.type("Part of you wonders what he would have said.")
            print("\n")
            type.type("Most of you is glad you don't know.")
            self.restore_sanity(5)
        print("\n")

    def the_high_roller_suicide(self):
        # EVENT: Witness a high roller's complete breakdown and suicide
        # CONDITION: Balance >= $400,000 (you're in the high roller areas)
        # EFFECTS: Witness death, major sanity loss
        # MENTAL HEALTH: Witnessing suicide
        if self.get_balance() < 400000:
            self.day_event()
            return
        type.type("You head to the casino. In the high roller room, a man starts laughing. It's not a happy sound.")
        print("\n")
        type.type("He's lost everything. EVERYTHING. His chips are gone. His marker is maxed.")
        print("\n")
        type.type(quote("Twenty million. I lost TWENTY MILLION DOLLARS."))
        print("\n")
        type.type("He's still laughing. Crying too. Security approaches carefully.")
        print("\n")
        type.type(quote("My wife will leave me. My kids won't... they won't understand."))
        print("\n")
        type.type("He pulls out a gun. Everyone screams. Dives for cover.")
        print("\n")
        type.type("But he doesn't aim at anyone else.")
        print("\n")
        type.type(quote("This is what gambling does. Remember that."))
        print("\n")
        type.type(red(bright("BANG.")))
        print("\n")
        type.type("The room goes silent. He falls. It's over that fast.")
        print("\n")
        type.type("You can't move. Can't look away. His blood spreads across the green felt.")
        print("\n")
        type.type("Security rushes in. Someone throws a jacket over him. The game is over.")
        print("\n")
        type.type("But you can still hear the shot. You'll always hear the shot.")
        self.lose_sanity(40)
        self.add_status("Witnessed Suicide")
        print("\n")

    def the_anniversary_loss(self):
        # SECRET: Lost someone close - anniversary of their death
        if not self.has_status("Widowed") and not self.has_status("Lost Child"):
            self.day_event()
            return
        type.type("You sit up in your car. You immediately know what day it is.")
        print("\n")
        type.type("The anniversary. One year since they died.")
        print("\n")
        type.type("You try to distract yourself. Casino. Cards. Anything.")
        print("\n")
        type.type("But you see their face everywhere. In strangers. In reflections.")
        print("\n")
        type.type("By evening, you're crying in the parking lot. Alone. Always alone.")
        self.lose_sanity(20)
        print("\n")

    def survivor_guilt(self):
        # SECRET: Survived something others didn't
        if not self.has_status("Witnessed Death") and not self.has_status("Survivor's Resolve"):
            self.day_event()
            return
        type.type("You sit in your car and the faces come back. The ones who didn't make it.")
        print("\n")
        type.type("Why you? Why did YOU survive when they didn't?")
        print("\n")
        type.type("You don't deserve this. Any of this. The money, the life, any of it.")
        print("\n")
        type.type("...But maybe that's why you keep gambling. Waiting to lose it all.")
        print("\n")
        type.type("Waiting to get what you deserve.")
        self.lose_sanity(15)
        print("\n")

    def the_scar_story(self):
        # SECRET: Have a scar-related status - someone asks about it
        if not self.has_status("Missing Finger") and not self.has_status("Burn Scars") and not self.has_danger("Knife Wound"):
            self.day_event()
            return
        type.type("You step out of your car. A child points at your scars. " + quote("What happened to you?"))
        print("\n")
        type.type("Their mother pulls them away, apologizing. But the damage is done.")
        print("\n")
        type.type("What DID happen to you? How did you end up here? Scarred, gambling, living in a car?")
        print("\n")
        type.type("You remember every wound. Every story. Every mistake.")
        print("\n")
        type.type("The scars are just the ones you can see.")
        self.lose_sanity(8)
        print("\n")

    def the_winning_streak_paranoia(self):
        # SECRET: Won more than $100,000 in a single day
        if not hasattr(self, '_today_winnings') or self._today_winnings < 100000:
            self.day_event()
            return
        type.type("You're wide awake in your car. Too much adrenaline. Too much paranoia.")
        print("\n")
        type.type("That's a lot of money. People kill for less.")
        print("\n")
        type.type("Every noise is a threat. Every shadow is an enemy.")
        print("\n")
        type.type("You clutch your cash like a lifeline. Eyes darting. Heart pounding.")
        print("\n")
        type.type("Is that car following you? Was that footsteps?")
        print("\n")
        type.type("Morning comes. You're exhausted but alive. Was anyone ever really after you?")
        print("\n")
        type.type("Does it matter? The fear was real.")
        self.lose_sanity(10)
        print("\n")

    def old_gambling_buddy(self):
        # SECRET: Day 200+ - run into someone from your past gambling life
        if self._day < 200:
            self.day_event()
            return
        type.type("You step out of your car when a voice calls your name. Your REAL name. One you haven't heard in months.")
        print("\n")
        type.type("You turn and see a face from another life. An old gambling buddy.")
        print("\n")
        type.type(quote("I can't believe it's you! We all thought you were dead! Or in prison!"))
        print("\n")
        type.type("He looks good. Clean. Healthy. Normal.")
        print("\n")
        type.type(quote("I quit, you know. Two years clean. Got a job, a family. Real life stuff."))
        print("\n")
        type.type("He looks at you. At your car. At your clothes. At what you've become.")
        print("\n")
        type.type(quote("Oh. You're still...") + " He trails off. The pity in his eyes is worse than any insult.")
        print("\n")
        type.type(quote("Good luck, man. I hope you find your way out."))
        print("\n")
        type.type("He walks away. Back to his normal life. You stay.")
        self.lose_sanity(15)
        print("\n")

    # ==========================================
    # ==========================================
    # BRUTAL EVENTS - DEATH POSSIBLE
    # These events can result in player death. High risk, high stakes encounters.
    # ==========================================

    def back_alley_shortcut(self):
        # EVENT: Mugged in a dark alley with three armed men
        # EFFECTS: Comply = lose $100-500 + 15 damage + 10 sanity; Run = escape or die; Fight = win or die
        # COMPANION INTEGRATION: danger_warning companions detect the ambush, protection companions fight
        # DEATH POSSIBLE - Mugging gone wrong
        
        # COMPANION: Danger warning check (Whiskers, Slick)
        warner = self._lists.has_companion_with_bonus(self, "danger_warning")
        if warner and self.get_companion(warner)["status"] == "alive":
            type.type("You're about to take a shortcut through a dark alley when " + bright(warner) + " goes absolutely crazy.")
            print("\n")
            if "Cat" in self.get_companion(warner).get("type", ""):
                type.type(warner + " arches their back and hisses at the alley entrance. Ears flat. Tail puffed.")
            elif "Rat" in self.get_companion(warner).get("type", ""):
                type.type(warner + " starts squeaking frantically, biting your collar, pulling you backward.")
            else:
                type.type(warner + " makes alarmed sounds, physically trying to stop you from entering.")
            print("\n")
            type.type("You hesitate. Peer into the darkness. And you see them.")
            print("\n")
            type.type("Three figures. Waiting. One has something that catches the streetlight. A knife.")
            print("\n")
            type.type("You back away slowly. They don't see you. " + warner + " just saved you from a mugging.")
            print("\n")
            type.type(green(warner + "'s danger sense kicked in! Ambush avoided!"))
            self.restore_sanity(5)
            self.pet_companion(warner)
            print("\n")
            return
        
        # ITEM: Tattered Cloak / Invisible Cloak - slip through unseen
        if self.has_item("Tattered Cloak") or self.has_item("Invisible Cloak"):
            cloak = "Tattered Cloak" if self.has_item("Tattered Cloak") else "Invisible Cloak"
            type.type("You step into the alley and pull the " + cyan(bright(cloak)) + " tight.")
            print("\n")
            type.type("Halfway through, three shapes materialize from the shadows. Hoodies. A knife. They're scanning the darkness for a target.")
            print("\n")
            type.type("Their eyes slide right past you. " + quote("Where'd he go?") + " one mutters.")
            print("\n")
            type.type("You walk out the far end without making a sound. They never saw you. You exist in a frequency they can't tune to.")
            self.restore_sanity(8)
            print("\n")
            return
        
        type.type("You step out of your car and decide to take a shortcut through a dark alley. Faster than going around.")
        print("\n")
        type.type("Halfway through, you hear footsteps behind you. Heavy. Fast. Getting closer.")
        print("\n")
        type.type("You turn around. Three men. Hoodies pulled low. One has a knife that catches the streetlight.")
        print("\n")
        type.type(quote("Wallet. Phone. Everything. Now."))
        print("\n")
        answer = ask.option("What do you do? ", ["comply", "run", "fight"])
        print("\n")
        if answer == "comply":
            stolen = min(self.get_balance(), random.randint(100, 500))
            type.type("You hand over everything. They rifle through your pockets, take what they want.")
            print("\n")
            type.type("One of them punches you in the gut anyway. Just because he can.")
            print("\n")
            type.type(quote("Stay down. Count to a hundred. Don't look at our faces."))
            print("\n")
            type.type("You do what they say. When you finally look up, they're gone.")
            print("\n")
            type.type("You lost " + red(bright("$" + str(int(stolen)))) + ".")
            self.change_balance(-stolen)
            self.hurt(15)
            self.lose_sanity(10)
        elif answer == "run":
            type.type("You bolt. Legs pumping. Heart screaming. The alley seems to stretch forever.")
            print("\n")
            chance = random.randrange(10)
            if chance < 6:
                type.type("You burst onto the main street. People. Cars. Safety.")
                print("\n")
                type.type("You don't stop running for three blocks. When you finally look back, no one's following.")
                print("\n")
                type.type("Your lungs burn. Your hands shake. But you're alive. You're alive.")
                self.hurt(5)
                self.lose_sanity(8)
            elif chance < 9:
                type.type("You trip. Garbage bag. Your ankle twists and you go down hard.")
                print("\n")
                type.type("They're on you in seconds. Kicks. Punches. The knife flashes.")
                print("\n")
                type.type("You curl into a ball and take it. It feels like forever.")
                print("\n")
                type.type("When they finally leave, you're bleeding from a gash on your arm. Your ribs scream.")
                stolen = min(self.get_balance(), random.randint(200, 800))
                type.type(" They took " + red(bright("$" + str(int(stolen)))) + ".")
                self.change_balance(-stolen)
                self.hurt(35)
                self.lose_sanity(15)
                self.add_danger("Knife Wound")
            else:
                type.type("You don't make it.")
                print("\n")
                type.type("The knife catches you between the shoulder blades. You feel the cold before the pain.")
                print("\n")
                type.type("Your legs stop working. The ground rushes up to meet you.")
                print("\n")
                type.type("The last thing you see is the dirty concrete. The last thing you hear is their footsteps fading.")
                print("\n")
                type.type("The last thing you think is: " + italic("I should have just given them the money."))
                print("\n")
                self.kill("Stabbed in a back alley. Another body. Another statistic.")
                return
        else:  # fight
            # COMPANION: Protection check (Lucky)
            protector = self._lists.has_companion_with_bonus(self, "protection")
            if protector and self.get_companion(protector)["status"] == "alive":
                type.type("Something snaps inside you. And " + bright(protector) + " feels it too.")
                print("\n")
                type.type(protector + " launches at the nearest mugger. Snarling. Biting. Three legs of fury.")
                print("\n")
                type.type("The mugger screams. His buddies hesitate. You grab a trash can lid and swing.")
                print("\n")
                type.type("Between you and " + protector + ", the three of them decide it's not worth it. They run.")
                print("\n")
                type.type("You stand there, chest heaving. " + protector + " stands beside you, growling at the empty alley.")
                print("\n")
                type.type(green(protector + " fought alongside you! Together you're unstoppable."))
                self.hurt(5)
                self.restore_sanity(5)
                self.pet_companion(protector)
                # Lucky might get hurt
                if random.randrange(3) == 0:
                    type.type(protector + " took a kick in the side. They're limping a little. But they're okay.")
                    self._companions[protector]["happiness"] = max(0, self._companions[protector]["happiness"] - 5)
            else:
                type.type("Something snaps inside you. You're tired. Tired of being afraid. Tired of being nothing.")
            print("\n")
            type.type("You charge at them, screaming. Pure animal rage.")
            print("\n")
            chance = random.randrange(10)
            if chance < 2:
                type.type("They weren't expecting that. The first one goes down when your fist connects with his nose.")
                print("\n")
                type.type("Blood sprays. The other two hesitate. You grab a trash can lid and swing.")
                print("\n")
                type.type("They run. They actually run. You stand there, chest heaving, covered in someone else's blood.")
                print("\n")
                type.type("You won. Somehow. You have no idea how.")
                self.hurt(10)
                self.restore_sanity(5)  # Cathartic
            elif chance < 7:
                type.type("You get one good hit in. Then the knife finds your stomach.")
                print("\n")
                type.type("It doesn't hurt at first. Just pressure. Then heat. Then agony.")
                print("\n")
                type.type("You collapse. They take everything and run.")
                print("\n")
                type.type("You drag yourself to the street, leaving a trail of blood. Someone calls an ambulance.")
                stolen = self.get_balance()
                self.change_balance(-stolen)
                self.hurt(60)
                self.lose_sanity(20)
                self.add_danger("Gut Wound")
                if self.has_item("Health Indicator") or self.has_item("Health Manipulator"):
                    indicator = "Health Indicator" if self.has_item("Health Indicator") else "Health Manipulator"
                    type.type("The " + cyan(bright(indicator)) + " pulses at your wrist, flooding adrenaline into the wound site. The damage is real, but your body's response is extraordinary.")
                    print("\n")
                    type.type("You'll live.")
                    self.heal(25)
            else:
                type.type("The knife goes into your throat before you can even swing.")
                print("\n")
                type.type("You try to scream but it comes out as a gurgle. Blood. So much blood.")
                print("\n")
                type.type("You fall. The world tilts. The stars above blur into smears of light.")
                print("\n")
                type.type("Your last thought is that you never got to make your million.")
                print("\n")
                if self.has_item("Phoenix Feather") or self.has_item("White Feather"):
                    feather = "Phoenix Feather" if self.has_item("Phoenix Feather") else "White Feather"
                    type.type("Then — warmth. A burst of amber light erupts from your pocket.")
                    print("\n")
                    type.type("The " + cyan(bright(feather)) + " ignites. Heat floods through you like sunrise. The wound seals with a hiss.")
                    print("\n")
                    type.type("You gasp and roll over. The muggers have fled — they saw the light and ran.")
                    print("\n")
                    type.type("The feather is ash. But you are not.")
                    self.use_item(feather)
                    self.hurt(35)
                    self.lose_sanity(20)
                else:
                    self.kill("Bled out in an alley. The muggers split your cash three ways.")
                return
        print("\n")

    def gas_station_robbery(self):
        # EVENT: Caught in a gas station during an armed robbery
        # EFFECTS: Comply = potential hostage situation; Hide = escape or get caught; Hero = save day or die
        # COMPANION INTEGRATION: danger_warning companions give early warning, Slick finds escape route
        # DEATH POSSIBLE - Wrong place, wrong time
        
        # COMPANION: Danger warning check - avoid the situation entirely
        warner = self._lists.has_companion_with_bonus(self, "danger_warning")
        if warner and self.get_companion(warner)["status"] == "alive" and random.randrange(3) == 0:
            type.type("You're about to walk into the gas station when " + bright(warner) + " starts acting strange.")
            print("\n")
            type.type("Agitated. Pulling at you. Refusing to let you go in.")
            print("\n")
            type.type("You hesitate at the door. Then you hear it from inside: " + quote("EVERYBODY ON THE GROUND!"))
            print("\n")
            type.type("Your blood goes cold. There's a robbery happening. Right now. Right where you almost walked in.")
            print("\n")
            type.type("You back away slowly. Call 911 from the parking lot. The police handle it.")
            print("\n")
            type.type(green(warner + " sensed the danger! You avoided the robbery entirely!"))
            self.pet_companion(warner)
            self.restore_sanity(5)
            print("\n")
            return
        
        type.type("You drive your car to a gas station for supplies. Just snacks. Maybe some coffee.")
        print("\n")
        type.type("You're browsing the chips when the door slams open.")
        print("\n")
        type.type(quote("EVERYBODY ON THE GROUND! NOW!"))
        print("\n")
        type.type("A man with a shotgun. Ski mask. Shaking hands. This is really happening.")
        print("\n")
        type.type("The cashier freezes. A mother clutches her child. An old man drops his coffee.")
        print("\n")
        type.type("The robber swings the gun around, wild-eyed.")
        print("\n")
        answer = ask.option("What do you do? ", ["comply", "hide", "hero"])
        print("\n")
        if answer == "comply":
            type.type("You drop to the floor. Face down. Hands visible. Make yourself small.")
            print("\n")
            type.type("The robber empties the register. Grabs cigarettes. His eyes keep darting to the door.")
            print("\n")
            type.type("He's scared. That makes him dangerous.")
            print("\n")
            chance = random.randrange(10)
            if chance < 8:
                type.type("Sirens in the distance. He panics. Runs. Gone.")
                print("\n")
                type.type("You stay on the floor for a long time after. Just breathing. Just existing.")
                self.lose_sanity(12)
            else:
                type.type("He decides he needs a hostage. His hand grabs your collar.")
                print("\n")
                type.type("You're dragged toward the door. The shotgun barrel is cold against your temple.")
                print("\n")
                type.type("Outside. Police lights. He's screaming. They're screaming. Everyone's screaming.")
                print("\n")
                chance2 = random.randrange(3)
                if chance2 == 0:
                    type.type("The sniper takes the shot. The robber's head snaps back.")
                    print("\n")
                    type.type("His blood is in your mouth. On your face. You're screaming.")
                    print("\n")
                    type.type("They pry you from his body. You can't stop shaking for hours.")
                    self.lose_sanity(30)
                    self.hurt(5)
                else:
                    type.type("His finger twitches. The gun goes off.")
                    print("\n")
                    type.type("The world goes white. Then nothing.")
                    print("\n")
                    self.kill("Wrong place. Wrong time. Hostage situation gone wrong.")
                    return
        elif answer == "hide":
            type.type("You duck behind a shelf. Slowly, carefully, you crawl toward the back.")
            print("\n")
            type.type("The robber is focused on the register. You're almost to the storage room...")
            print("\n")
            chance = random.randrange(10)
            if chance < 7:
                type.type("You make it. Hide behind boxes of toilet paper and canned goods.")
                print("\n")
                type.type("You can hear everything. The shouting. The crying. The crash of the register hitting the floor.")
                print("\n")
                type.type("Then sirens. Running footsteps. Silence.")
                print("\n")
                type.type("The police find you an hour later, still hiding. Curled up like a child.")
                self.lose_sanity(15)
            else:
                type.type("A chip bag crinkles under your knee. The robber spins.")
                print("\n")
                type.type(quote("I SEE YOU! GET OUT HERE!"))
                print("\n")
                type.type("The shotgun is pointed right at you. You raise your hands and step out.")
                print("\n")
                type.type(quote("Think you're smart? Think you can hide from me?"))
                print("\n")
                type.type("He hits you with the stock. Your vision explodes into stars.")
                self.hurt(25)
                self.lose_sanity(15)
        else:  # hero
            type.type("There's a fire extinguisher on the wall. Three feet away. You could make it.")
            print("\n")
            type.type("The robber's back is turned. Yelling at the cashier. Now or never.")
            print("\n")
            chance = random.randrange(10)
            if chance < 3:
                type.type("You grab it. Swing. Connect with his skull. He goes down like a sack of meat.")
                print("\n")
                type.type("The shotgun clatters to the floor. You kick it away. Stand over him, chest heaving.")
                print("\n")
                type.type("The other customers stare at you like you're insane. Maybe you are.")
                print("\n")
                type.type("The police call you a hero. The cashier gives you $100 from his own pocket.")
                self.change_balance(100)
                self.restore_sanity(10)
                self.meet("Gas Station Hero")
            elif chance < 7:
                type.type("He turns too fast. Sees you reaching. The shotgun comes up.")
                print("\n")
                type.type("BANG.")
                print("\n")
                type.type("The blast catches your shoulder. You spin. Hit the floor. The pain is unreal.")
                print("\n")
                type.type("But you're alive. He runs. Sirens are close.")
                print("\n")
                type.type("You'll never have full use of that arm again.")
                self.hurt(50)
                self.lose_sanity(20)
                self.add_danger("Shoulder Destroyed")
            else:
                type.type("You're too slow. Way too slow.")
                print("\n")
                type.type("The shotgun blast takes you in the chest. The world goes red, then black.")
                print("\n")
                type.type("You tried to be a hero. Heroes die young.")
                print("\n")
                self.kill("Shot trying to stop a robbery. They put your picture on the news.")
                return
        print("\n")

    def carbon_monoxide(self):
        # EVENT: Carbon monoxide leak while sleeping in car
        # EFFECTS: First exposure always survives but adds "Damaged Exhaust"; repeat exposure can still kill
        # BRUTAL: Pushes the lethal risk into the follow-up exhaust chain instead of a one-off instant death spike
        type.type("A pounding headache. The worst you've ever had.")
        print("\n")
        type.type("Your thoughts are sluggish. Thick. Like wading through mud.")
        print("\n")
        type.type("Something's wrong. The car smells... off. Exhaust. How long have you been breathing this?")
        print("\n")
        type.type("Your hands feel so far away. Moving them takes forever.")
        print("\n")
        chance = random.randrange(10)
        repeat_exposure = self.has_danger("Damaged Exhaust")
        if chance < 5:
            type.type("Some survival instinct kicks in. You fumble for the door handle. Miss. Try again.")
            print("\n")
            type.type("The door opens. Fresh air hits your face. You fall out onto the pavement.")
            print("\n")
            type.type("You lay there, gasping, staring at the sky, for what feels like hours.")
            print("\n")
            type.type("Your exhaust pipe has a hole. It's been leaking carbon monoxide into the car.")
            print("\n")
            type.type("You almost died in your sleep. You almost didn't wake up at all.")
            self.hurt(30)
            self.lose_sanity(20)
            self.add_danger("Damaged Exhaust")
        elif chance < 8:
            type.type("You try to move but your body won't cooperate. Too tired. Just... so tired.")
            print("\n")
            type.type("Maybe if you close your eyes for just a second...")
            print("\n")
            type.type("...")
            print("\n")
            type.type("A tap on the window. Muffled shouting. Someone's breaking the glass.")
            print("\n")
            type.type("Fresh air. Screaming sirens. The inside of an ambulance.")
            print("\n")
            type.type("The doctors say you were minutes away from brain damage. Or death.")
            self.hurt(45)
            self.lose_sanity(25)
            self.add_danger("Damaged Exhaust")
            if self.get_balance() >= 500:
                type.type("Hospital bill: " + red(bright("$500")) + ". They saved your life, so.")
                self.change_balance(-500)
        elif repeat_exposure:
            type.type("You're so tired. The headache is fading. Everything is fading.")
            print("\n")
            type.type("This isn't so bad. Peaceful, almost. Like sinking into warm water.")
            print("\n")
            type.type("Your eyes close. Your breathing slows. Your heart follows.")
            print("\n")
            type.type("They find your body two days later. The car is still running.")
            print("\n")
            self.kill("Carbon monoxide poisoning. They say it's painless. They hope it's painless.")
            return
        else:
            type.type("You black out halfway to the door and wake up sprawled across the front seat, windows fogged, lungs burning.")
            print("\n")
            type.type("You cough hard enough to taste blood before you manage to kill the engine and crawl outside.")
            print("\n")
            type.type("The exhaust is shot. If you sleep in here again without fixing it, you might not wake up.")
            self.hurt(25)
            self.lose_sanity(12)
            self.add_danger("Damaged Exhaust")
        print("\n")

    def drowning_dream(self):
        # EVENT: Surreal drowning nightmare that may become reality
        # BRUTAL: Dream-like sequence with potential death
        # DEATH POSSIBLE - Dream or reality?
        self.meet("Drowning Dream")
        type.type("Sitting in your car, your mind drifts. You dream of water. Dark water. Deep water. Rising water.")
        print("\n")
        type.type("You're in a car—your car—and water is pouring in through every crack.")
        print("\n")
        type.type("You can't open the doors. The pressure is too much. The windows won't break.")
        print("\n")
        type.type("The water reaches your waist. Your chest. Your neck. Your mouth.")
        print("\n")
        type.type("You scream but water fills your lungs instead of air.")
        print("\n")
        type.type("...")
        print("\n")
        chance = random.randrange(10)
        if chance < 7:
            type.type("You wake up GASPING. Clawing at your throat. Soaking wet with sweat.")
            print("\n")
            type.type("Just a dream. Just a dream. Just a—")
            print("\n")
            type.type("Your feet are wet. You look down.")
            print("\n")
            type.type("Rain. It's raining. Water leaked through a crack in your window.")
            print("\n")
            type.type("Just rain. You're fine. You're fine. You're fine.")
            self.lose_sanity(15)
            self.hurt(5)
        elif chance < 9:
            type.type("You wake up underwater.")
            print("\n")
            type.type("THIS ISN'T A DREAM. Your car is IN THE RIVER. You must have rolled down the embankment while sleeping.")
            print("\n")
            type.type("The water is at your waist. Rising fast. You fumble for the window crank.")
            print("\n")
            type.type("It's stuck. You slam your elbow against the glass. Again. Again. AGAIN.")
            print("\n")
            type.type("It cracks. Shatters. Water rushes in but you have an opening.")
            print("\n")
            type.type("You squeeze through, cutting yourself on the glass, and kick toward the surface.")
            print("\n")
            type.type("Air. Sweet, precious air. You drag yourself onto the bank and collapse.")
            print("\n")
            type.type("By morning, the wagon is a drowned wreck-half-sunk, flooded through, and useless as transportation.")
            print("\n")
            type.type("You can salvage your life, but not your ride. Most of what you kept inside is ruined or swept away. But you're alive.")
            self.hurt(40)
            self.lose_sanity(25)
            self.remove_item("Car")
            lost = self.get_balance() * 0.3
            self.change_balance(-lost)
        else:
            type.type("You never wake up.")
            print("\n")
            type.type("The car rolled into the river while you slept. By the time the water woke you, it was too late.")
            print("\n")
            type.type("You fight. God, how you fight. But the doors won't open and the windows won't break.")
            print("\n")
            type.type("Your last breath comes as a desperate gasp. Water fills the void.")
            print("\n")
            type.type("They find the car three days later. Your hands are still on the door handle.")
            print("\n")
            self.kill("Drowned in your car. Some nightmares are real.")
            return
        print("\n")

    def heart_attack_scare(self):
        # EVENT: Stress-induced cardiac event while walking to casino
        # EFFECTS: 50% panic attack (15 dmg + 20 sanity + $300); 30% mild heart attack (40 dmg + "Heart Condition" + $2000); 20% death
        # BRUTAL: Can result in instant death from massive heart attack
        # DEATH POSSIBLE - The stress catches up
        type.type("You step out of your car and head toward the casino when it hits. Pain. Crushing pain in your chest.")
        print("\n")
        type.type("You can't breathe. Your left arm is tingling. Your vision is going gray at the edges.")
        print("\n")
        type.type("This is it. This is how it ends. Not at the table. In a parking lot.")
        print("\n")
        type.type("You collapse against your car. Hand clutching your chest. People are staring.")
        print("\n")
        chance = random.randrange(10)
        if chance < 5:
            type.type("Someone calls 911. Paramedics. Hospital. Tests.")
            print("\n")
            type.type("It wasn't a heart attack. Panic attack. Severe anxiety. Stress.")
            print("\n")
            type.type("The doctor looks at you with something like pity.")
            print("\n")
            type.type(quote("Sir, if you keep living like this, next time it WILL be a heart attack."))
            print("\n")
            type.type("He gives you pills. You can't afford to fill the prescription.")
            self.hurt(15)
            self.lose_sanity(20)
            if self.get_balance() >= 300:
                type.type("ER visit: " + red(bright("$300")) + ".")
                self.change_balance(-300)
        elif chance < 8:
            type.type("It IS a heart attack. A mild one, they say. Like that's supposed to be comforting.")
            print("\n")
            type.type("You spend three days in the hospital. They put a stent in your artery.")
            print("\n")
            type.type("The doctor tells you to change your lifestyle. Eat better. Stress less. Exercise.")
            print("\n")
            type.type("You're a homeless gambling addict. Lifestyle changes aren't really an option.")
            self.hurt(40)
            self.lose_sanity(25)
            self.add_danger("Heart Condition")
            if self.get_balance() >= 2000:
                type.type("Hospital bill: " + red(bright("$2000")) + ". Worth it to be alive, you guess.")
                self.change_balance(-2000)
        else:
            type.type("It's a heart attack. A big one. The kind that kills people.")
            print("\n")
            type.type("You try to call for help but no sound comes out. Your body won't cooperate.")
            print("\n")
            type.type("People walk past. They think you're drunk. Or crazy. They don't stop.")
            print("\n")
            type.type("The world gets very small. Just you and the pain and the fading light.")
            print("\n")
            type.type("Your last thought is about cards. You were so close. So close.")
            print("\n")
            self.kill("Heart attack. The stress finally won. The house always wins.")
            return
        print("\n")

    def drug_dealer_encounter(self):
        # EVENT: Drug dealers mistake you for a buyer/informant
        # EFFECTS: Various - can buy cocaine ($500), get beaten (15-45 damage), or shot and killed
        # BRUTAL: Running has high death chance; can acquire "Bag of Cocaine" item
        # DEATH POSSIBLE - Wrong crowd
        type.type("A car pulls up next to you. Windows tinted black. Engine rumbling.")
        print("\n")
        type.type("The window rolls down. A face stares out. Cold eyes. Gold teeth.")
        print("\n")
        type.type(quote("You the one been asking around? Looking for... product?"))
        print("\n")
        type.type("You haven't been asking around. This is a case of mistaken identity.")
        print("\n")
        answer = ask.option("What do you say? ", ["wrong person", "play along", "run"])
        print("\n")
        if answer == "wrong person":
            type.type(quote("I think you've got the wrong guy. I don't—"))
            print("\n")
            type.type("He cuts you off. " + quote("Don't play dumb. Marcus said you was looking."))
            print("\n")
            type.type("You don't know any Marcus. Your heart is pounding.")
            print("\n")
            chance = random.randrange(10)
            if chance < 6:
                type.type(quote("Nah, this ain't him.") + " The passenger leans over, squinting. " + quote("Wrong car. My bad."))
                print("\n")
                type.type("The window rolls up. The car drives away. You nearly collapse with relief.")
                self.lose_sanity(10)
            else:
                type.type("He doesn't believe you. Door opens. He gets out. He's holding something metal.")
                print("\n")
                type.type(quote("You talked to the cops, didn't you? You a snitch?"))
                print("\n")
                type.type("Before you can answer, his fist connects with your face. Then again. Then the metal thing—a pipe.")
                print("\n")
                type.type("You go down. They beat you until you stop moving. Take your wallet. Leave you bleeding.")
                self.hurt(45)
                self.lose_sanity(20)
                stolen = min(self.get_balance(), random.randint(200, 500))
                self.change_balance(-stolen)
        elif answer == "play along":
            type.type("Some insane survival instinct kicks in. You play along.")
            print("\n")
            type.type(quote("Yeah, that's me. What you got?"))
            print("\n")
            type.type("He grins. Shows you a bag of white powder. Wants $500.")
            print("\n")
            if self.get_balance() >= 500:
                answer2 = ask.yes_or_no("Buy the drugs? ($500) ")
                if answer2 == "yes":
                    type.type("You hand over the money. Take the bag. The car drives away.")
                    print("\n")
                    type.type("You're holding cocaine. What the hell are you supposed to do with cocaine?")
                    print("\n")
                    self.change_balance(-500)
                    self.add_item("Bag of Cocaine")
                else:
                    type.type(quote("Actually, I'm good. Changed my mind."))
                    print("\n")
                    type.type("His face hardens. " + quote("You wasting my time?"))
                    print("\n")
                    chance = random.randrange(3)
                    if chance == 0:
                        type.type("He spits on your car and drives off. Lucky.")
                        self.lose_sanity(8)
                    else:
                        type.type("He gets out. Punches you once, hard. " + quote("Don't waste my time again."))
                        self.hurt(15)
                        self.lose_sanity(12)
            else:
                type.type(quote("I don't have enough cash on me right now..."))
                print("\n")
                type.type(quote("Then why you wastin' my time?"))
                print("\n")
                type.type("He slaps you across the face and drives off. You got off easy.")
                self.hurt(5)
                self.lose_sanity(10)
        else:  # run
            type.type("You turn and bolt. Stupid. So stupid. But instinct takes over.")
            print("\n")
            type.type("Behind you, car doors open. Footsteps. Shouting.")
            print("\n")
            chance = random.randrange(10)
            if chance < 4:
                type.type("You're faster than you thought. Or they're lazier than expected.")
                print("\n")
                type.type("You cut through an alley, over a fence, through someone's yard.")
                print("\n")
                type.type("When you finally stop running, you're lost. But alive. Definitely alive.")
                self.hurt(5)
                self.lose_sanity(12)
            elif chance < 8:
                type.type("They catch you in thirty seconds. You're not fast. You're not young.")
                print("\n")
                type.type("The beating is methodical. Professional. They know how to hurt without killing.")
                print("\n")
                type.type("When they leave, you crawl to a gas station and call for help.")
                self.hurt(40)
                self.lose_sanity(20)
                stolen = self.get_balance()
                self.change_balance(-stolen)
            else:
                type.type("You hear the gunshot before you feel it. Your leg goes out from under you.")
                print("\n")
                type.type("Then another. Your back. Hot and wet and wrong.")
                print("\n")
                type.type("You hit the ground. The sky is very blue today, you notice.")
                print("\n")
                type.type("Footsteps approach. A face looks down at you. Disappointed, almost.")
                print("\n")
                type.type(quote("Shouldn't have run."))
                print("\n")
                type.type("One more shot. The sky goes dark.")
                print("\n")
                self.kill("Shot while running from drug dealers. Wrong place. Wrong time. Wrong identity.")
                return
        print("\n")

    def bridge_contemplation(self):
        # EVENT: Dark suicidal thoughts at a bridge (low sanity trigger)
        # CONDITION: Sanity must be <= 30
        # EFFECTS: Step back = restore sanity; Stay = stranger saves you; Call hotline = restore 25 sanity
        # NOTE: Sensitive mental health content handled respectfully
        # DEATH POSSIBLE - Dark thoughts
        if self.get_sanity() > 30:
            self.day_event()
            return
        type.type("You find yourself on a bridge. You don't remember leaving your car.")
        print("\n")
        type.type("You're standing at the railing. Looking down at the water. So far down.")
        print("\n")
        type.type("Your hands are on the cold metal. When did you get out of the car?")
        print("\n")
        type.type("The water looks peaceful. Dark and cold and peaceful. No more debt. No more hunger.")
        print("\n")
        type.type("No more losing. No more trying. Just... nothing.")
        print("\n")
        type.type("A voice in your head says: " + italic("It would be so easy. Just let go."))
        print("\n")
        answer = ask.option("What do you do? ", ["step back", "stay", "call for help"])
        print("\n")
        if answer == "step back":
            type.type("You force yourself to step back. One step. Then another.")
            print("\n")
            type.type("Your hands are shaking. You're crying. When did you start crying?")
            print("\n")
            type.type("You get back in your car. You drive away. You don't look back.")
            print("\n")
            type.type("You're not okay. But you're alive. Today, that's enough.")
            self.lose_sanity(10)
            self.restore_sanity(15)  # Net positive for choosing life
        elif answer == "stay":
            type.type("You stay at the railing. Minutes pass. Maybe hours.")
            print("\n")
            type.type("A car stops. Someone gets out. A woman's voice, soft and scared.")
            print("\n")
            type.type(quote("Hey. Hey there. Are you okay? Please step back from the edge."))
            print("\n")
            type.type("You look at her. She looks terrified. Terrified for YOU.")
            print("\n")
            type.type("When's the last time anyone was scared for you? When's the last time anyone cared?")
            print("\n")
            type.type("You step back. She holds you while you cry. A stranger. Holding you while you fall apart.")
            self.restore_sanity(20)
            self.meet("Bridge Angel")
        else:  # call for help
            type.type("With shaking hands, you pull out your phone. 988. The suicide hotline.")
            print("\n")
            type.type("A voice answers. Calm. Kind. They talk to you for an hour.")
            print("\n")
            type.type("They don't judge. They don't tell you you're being stupid. They just... listen.")
            print("\n")
            type.type("When you finally hang up, you're sitting in your car. Still on the bridge. But back from the edge.")
            print("\n")
            type.type("You're not fixed. But you're here. That matters.")
            self.restore_sanity(25)
        print("\n")

    def food_poisoning(self):
        # EVENT: Severe food poisoning from gas station food
        # EFFECTS: 60% survive (25 dmg + 10 sanity); 30% hospitalized (45 dmg + $800 + "Weakened Immune System"); 10% death from sepsis
        # BRUTAL: Can cause death from bacterial sepsis
        # DEATH POSSIBLE - Bad luck
        type.type("You're hunched over in your car seat. You ate something from a gas station. In retrospect, that was a mistake.")
        print("\n")
        type.type("The first cramp hits around 2 AM. Then another. Then the real fun begins.")
        print("\n")
        type.type("You're vomiting. You're... the other thing too. Your body is emptying itself from both ends.")
        print("\n")
        type.type("The pain is unreal. Your stomach feels like it's being stabbed from the inside.")
        print("\n")
        chance = random.randrange(10)
        if chance < 6:
            type.type("It goes on for hours. You lose count of how many times you throw up.")
            print("\n")
            type.type("But by dawn, it's fading. Your body has expelled the poison.")
            print("\n")
            type.type("You lie on the cold ground next to your car, exhausted, dehydrated, but alive.")
            print("\n")
            type.type("You'll never eat gas station sushi again. Lesson learned.")
            self.hurt(25)
            self.lose_sanity(10)
        elif chance < 9:
            type.type("By morning, you're seeing double. Your heart is racing. This is bad. Really bad.")
            print("\n")
            type.type("Someone finds you passed out next to your car and calls 911.")
            print("\n")
            type.type("The hospital pumps your stomach. IV fluids. They say you had severe dehydration.")
            print("\n")
            type.type("Two more hours and your organs would have started failing.")
            self.hurt(45)
            self.lose_sanity(15)
            self.add_danger("Weakened Immune System")
            if self.get_balance() >= 800:
                type.type("Hospital bill: " + red(bright("$800")) + ".")
                self.change_balance(-800)
        else:
            type.type("The vomiting stops. That's not a good sign. Your body has given up fighting.")
            print("\n")
            type.type("You can't move. Can't speak. Can barely see.")
            print("\n")
            type.type("The bacteria has reached your bloodstream. Sepsis. Multiple organ failure.")
            print("\n")
            type.type("You die in your car, alone, because you ate a $3.99 egg salad sandwich.")
            print("\n")
            self.kill("Food poisoning. Death by gas station sushi. An ignoble end.")
            return
        print("\n")

    def attacked_by_dog(self):
        # DEATH POSSIBLE - Animal attack
        # COMPANION INTEGRATION: Lucky/protection companion fights the stray
        
        # COMPANION: Lucky specifically can fight off the dog
        if self.has_companion("Lucky") and self.get_companion("Lucky")["status"] == "alive":
            type.type("You step out of your car when you hear growling. A big stray dog. Teeth bared.")
            print("\n")
            type.type("Before you can react, " + bright("Lucky") + " is already between you and the stray.")
            print("\n")
            type.type("Three-legged but fearless. Lucky stands his ground, growling back.")
            print("\n")
            type.type("The two dogs have a standoff. Circling. Snarling. Your heart is in your throat.")
            print("\n")
            if random.randrange(3) != 0:
                type.type("Lucky barks once. A sharp, commanding sound. The stray flinches.")
                print("\n")
                type.type("Then the stray backs down. Tucks its tail. Trots away.")
                print("\n")
                type.type("Lucky doesn't relax until the stray is completely out of sight. Then he turns to you and wags his tail.")
                print("\n")
                type.type(green("Lucky protected you from the stray! Best boy."))
                self.pet_companion("Lucky")
                self.restore_sanity(5)
            else:
                type.type("The stray lunges. Lucky meets it head-on. Fur flies. Blood draws.")
                print("\n")
                type.type("It's over in seconds. The stray yelps and runs. Lucky stands victorious.")
                print("\n")
                type.type("But he's hurt. A gash on his side. He limps over to you, tail still wagging.")
                print("\n")
                type.type("You patch him up. He licks your hand. This dog would die for you.")
                self.hurt(5)  # You got scratched too
                self._companions["Lucky"]["happiness"] = max(0, self._companions["Lucky"]["happiness"] - 5)
                self.pet_companion("Lucky")
                self.pet_companion("Lucky")
                self.restore_sanity(3)
            print("\n")
            return
        
        type.type("You step out of your car and head toward a convenience store when you hear it. Growling. Deep and low.")
        print("\n")
        type.type("A dog. Big. Rottweiler or pit bull, you can't tell. No leash. No owner. Just teeth.")
        print("\n")
        type.type("It's staring at you. Hackles raised. Drool dripping from its jaws.")
        print("\n")
        type.type("You freeze. Don't run. Don't make eye contact. You remember reading that somewhere.")
        print("\n")
        chance = random.randrange(10)
        if chance < 4:
            type.type("The dog watches you. Sniffs the air. Decides you're not worth the effort.")
            print("\n")
            type.type("It trots away, looking for something more interesting.")
            print("\n")
            type.type("You don't move for five minutes. Then you walk VERY quickly to your car.")
            self.lose_sanity(8)
        elif chance < 8:
            type.type("It charges. Ninety pounds of muscle and fury coming right at you.")
            print("\n")
            type.type("You throw your arms up. Its jaws close on your forearm. You SCREAM.")
            print("\n")
            type.type("It shakes its head, tearing flesh. You punch it. Kick it. Nothing works.")
            print("\n")
            type.type("Someone runs over with a stick. Beats the dog off you. It finally lets go and runs.")
            print("\n")
            type.type("Your arm is a mess of blood and torn muscle. You can see bone.")
            if self.has_item("Scrap Armor"):
                type.type(" The makeshift padding took the worst of it.")
                self.hurt(20)
            else:
                self.hurt(40)
            self.lose_sanity(15)
            self.add_danger("Dog Bite Wound")
            if self.get_balance() >= 600:
                type.type("ER stitches: " + red(bright("$600")) + ".")
                self.change_balance(-600)
        else:
            type.type("It goes for your throat. Instinct. Predator targeting the kill zone.")
            print("\n")
            type.type("You get your arm up just in time. It bites deep. You fall.")
            print("\n")
            type.type("Then it's on top of you. Biting. Tearing. You're screaming. So much blood.")
            print("\n")
            type.type("It finds your throat eventually. They always do.")
            print("\n")
            type.type("Your last sight is the blue sky through red haze. Your last sound is growling.")
            print("\n")
            self.kill("Mauled to death by a stray dog. Not every monster is human.")
            return
        print("\n")

    def electrocution_hazard(self):
        # DEATH POSSIBLE - Freak accident
        type.type("It's raining hard. You jump out of your car and run for cover under an awning.")
        print("\n")
        type.type("There's a puddle. A big one. And an old electrical box on the wall, sparking.")
        print("\n")
        type.type("You don't notice until it's too late. Your foot hits the water.")
        print("\n")
        chance = random.randrange(10)
        if chance < 5:
            type.type("A jolt runs through you. Painful but brief. The breaker must have tripped.")
            print("\n")
            type.type("You jump back, heart pounding. That could have killed you.")
            print("\n")
            type.type("You report the hazard to the shop owner. They seem unimpressed.")
            if self.has_item("Scrap Armor"):
                type.type(" Your jury-rigged gear absorbed some of the shock.")
                self.hurt(4)
            else:
                self.hurt(10)
            self.lose_sanity(8)
        elif chance < 8:
            type.type("The current grabs you. Your muscles seize. You can't move. Can't breathe.")
            print("\n")
            type.type("Someone tackles you away from the puddle. A stranger. Saved your life.")
            print("\n")
            type.type("Your heart is racing. Irregular. Your hands won't stop shaking.")
            print("\n")
            type.type("The hospital keeps you overnight for observation. Arrhythmia.")
            if self.has_item("Scrap Armor"):
                type.type(" Your armor took some of the brunt.")
                self.hurt(18)
            else:
                self.hurt(35)
            self.lose_sanity(15)
            if self.get_balance() >= 500:
                type.type("Hospital: " + red(bright("$500")) + ".")
                self.change_balance(-500)
        else:
            type.type("The current hits you like a freight train. Every muscle in your body contracts at once.")
            print("\n")
            type.type("You can't scream. Can't move. Just the electricity, burning through you.")
            print("\n")
            type.type("Your heart stops. It tries to start again. Stops. Starts. Stops.")
            print("\n")
            type.type("By the time someone kicks you free of the puddle, you're gone.")
            print("\n")
            self.kill("Electrocution. A faulty wire and a puddle. That's all it took.")
            return
        print("\n")

    def car_explosion(self):
        # DEATH POSSIBLE - Mechanical failure
        type.type("You turn the key in the ignition. The engine makes a strange noise. A ticking.")
        print("\n")
        type.type("Something smells wrong. Gas. Strong and getting stronger.")
        print("\n")
        type.type("Instinct screams at you: GET OUT. GET OUT NOW.")
        print("\n")
        answer = ask.option("What do you do? ", ["bail out", "investigate", "ignore it"])
        print("\n")
        if answer == "bail out":
            type.type("You throw yourself out of the car and run. Don't look back. Just run.")
            print("\n")
            chance = random.randrange(3)
            if chance == 0:
                type.type("You're ten feet away when the engine catches fire. Fifteen when it explodes.")
                print("\n")
                type.type("The shockwave knocks you flat. Heat washes over you. Debris rains down.")
                print("\n")
                type.type("Your car—your home—is a fireball. Everything you owned is gone.")
                print("\n")
                type.type("But you're alive. Somehow. Alive.")
                self.hurt(20)
                self.lose_sanity(25)
                self.remove_item("Car")
                lost = self.get_balance() * 0.2
                self.change_balance(-lost)
            else:
                type.type("Nothing explodes. The engine just... dies. Smoke pours out.")
                print("\n")
                type.type("False alarm. Fuel line leak. Bad, but not explosive.")
                print("\n")
                type.type("You feel foolish. But also glad you trusted your gut.")
                self.add_danger("Fuel Leak")
                self.lose_sanity(10)
        elif answer == "investigate":
            type.type("You pop the hood. Lean in to look. The gas smell is overwhelming.")
            print("\n")
            chance = random.randrange(10)
            if chance < 7:
                type.type("There's the problem. A cracked fuel line. Gas dripping onto hot metal.")
                print("\n")
                type.type("You back away slowly. Very slowly. Get some distance.")
                print("\n")
                type.type("You disconnect the battery and let it cool down. Crisis averted.")
                self.add_danger("Fuel Leak")
                self.lose_sanity(10)
            else:
                type.type("The spark happens while you're leaning over the engine.")
                print("\n")
                type.type("The last thing you see is a flash of orange. The last thing you feel is heat.")
                print("\n")
                type.type("They find your body twenty feet from the wreckage.")
                print("\n")
                self.kill("Car explosion. Mechanical failure meets human curiosity. Boom.")
                return
        else:  # ignore it
            type.type("It's probably nothing. This car always makes weird noises.")
            print("\n")
            type.type("You turn the key again. The ticking gets louder.")
            print("\n")
            chance = random.randrange(10)
            if chance < 4:
                type.type("The engine catches. Runs rough, but runs. The smell fades.")
                print("\n")
                type.type("You should really get that checked out. You won't, but you should.")
                self.add_danger("Fuel Leak")
            else:
                type.type("The fireball is instantaneous. You don't even have time to scream.")
                print("\n")
                type.type("Glass and metal and fire, all at once. The car becomes your coffin.")
                print("\n")
                self.kill("Died in a car explosion. Should have bailed. Should have investigated. Did neither.")
                return
        print("\n")

    def knife_wound_infection(self):
        # CONDITIONAL DEATH - Consequence of earlier event
        if not self.has_danger("Knife Wound"):
            self.day_event()
            return
        type.type("You check yourself in the car mirror. That knife wound from the mugging isn't healing right.")
        print("\n")
        type.type("It's red. Swollen. Hot to the touch. Pus oozing from the edges.")
        print("\n")
        type.type("You're running a fever. Shaking. This is bad.")
        print("\n")
        chance = random.randrange(10)
        if chance < 5:
            type.type("You drag yourself to a free clinic. They take one look and rush you to a hospital.")
            print("\n")
            type.type("Antibiotics. IV drip. They save your arm. Barely.")
            self.hurt(25)
            self.remove_danger("Knife Wound")
        elif chance < 8:
            type.type("The infection has spread. Sepsis. Your blood is poisoned.")
            print("\n")
            type.type("Three days in the ICU. They're not sure you're going to make it.")
            print("\n")
            type.type("You do. Barely. But you'll never forget how close you came.")
            self.hurt(50)
            self.lose_sanity(20)
            self.remove_danger("Knife Wound")
            if self.get_balance() >= 3000:
                type.type("Hospital bill: " + red(bright("$3000")) + ".")
                self.change_balance(-3000)
        else:
            type.type("You wait too long. The infection reaches your heart.")
            print("\n")
            type.type("Endocarditis. By the time the ambulance arrives, you're barely conscious.")
            print("\n")
            type.type("You die on the operating table. A stupid knife wound. A stupid delay.")
            print("\n")
            self.kill("Died from an infected knife wound. Should have seen a doctor sooner.")
            return
        print("\n")

    def gut_wound_complications(self):
        # CONDITIONAL DEATH - Consequence of earlier event
        if not self.has_danger("Gut Wound"):
            self.day_event()
            return
        type.type("You shift in your car seat and wince. Your gut wound has been getting worse. Much worse.")
        print("\n")
        type.type("The stitches popped. You can see... things you shouldn't be seeing.")
        print("\n")
        type.type("The pain is constant now. You can't eat. Can barely drink.")
        print("\n")
        chance = random.randrange(10)
        if chance < 6:
            type.type("You make it to an ER. Emergency surgery. They have to remove part of your intestine.")
            print("\n")
            type.type("Recovery takes weeks. But you survive. Somehow.")
            self.hurt(40)
            self.lose_sanity(20)
            self.remove_danger("Gut Wound")
        else:
            type.type("The wound has gone septic. Your organs are failing.")
            print("\n")
            type.type("You die in the back of your car, alone, holding your stomach together with your hands.")
            print("\n")
            self.kill("Gut wound complications. Internal bleeding. Organ failure. Game over.")
            return
        print("\n")

    def devils_bargain_consequence(self):
        # CONDITIONAL EVENT - The devil collects
        if not self.has_danger("Devil's Bargain"):
            self.day_event()
            return
        if self.has_met("Devil's Collection"):
            self.day_event()
            return
        self.meet("Devil's Collection")
        type.type("The stranger from before is back. Standing by your car. Waiting.")
        print("\n")
        type.type(quote("You've done well. Very well. But it's time to pay what you owe."))
        print("\n")
        type.type("You try to run but your legs won't move. You try to scream but nothing comes out.")
        print("\n")
        type.type("He walks toward you. Slowly. That smile never reaching those dark, dead eyes.")
        print("\n")
        type.type(quote("Don't worry. This won't hurt."))
        print("\n")
        type.type("He reaches into your chest. No wound. No blood. Just... cold.")
        print("\n")
        type.type("When he withdraws his hand, he's holding something small and bright. Your... something.")
        print("\n")
        type.type(quote("A pleasure doing business."))
        print("\n")
        type.type("He's gone. You feel... empty. Hollow. Like a part of you is missing.")
        print("\n")
        type.type("You'll never feel truly happy again. That was the price.")
        self.lose_sanity(50)
        self.add_danger("Soulless")
        print("\n")

    # ==========================================
    # CONNECTED & CONDITIONAL EVENTS - MEGA BATCH
    # ==========================================

    # === SOULLESS CONSEQUENCES (Devil's Bargain Chain) ===

    def soulless_emptiness(self):
        if not self.has_danger("Soulless"):
            self.day_event()
            return
        type.type("You leave your car and head to the casino. You win at the tables. The dealer pushes chips toward you.")
        print("\n")
        type.type("You should feel something. Joy. Triumph. Relief. Anything.")
        print("\n")
        type.type("You feel nothing. Absolutely nothing. Just... hollow.")
        print("\n")
        type.type("The other gamblers are celebrating, crying, raging. You just exist.")
        print("\n")
        type.type("Is this what you traded for? Was it worth it?")
        self.lose_sanity(5)
        print("\n")

    def soulless_mirror(self):
        if not self.has_danger("Soulless"):
            self.day_event()
            return
        type.type("You catch your reflection in your car window. Something's wrong.")
        print("\n")
        type.type("Your eyes. They're darker than they should be. Empty. Dead.")
        print("\n")
        type.type("You look away quickly. You don't want to see what you've become.")
        self.lose_sanity(8)
        print("\n")

    def soulless_recognition(self):
        if not self.has_danger("Soulless"):
            self.day_event()
            return
        type.type("A child points at you from across the parking lot.")
        print("\n")
        type.type("Their mother pulls them close, hurrying away. But you heard what the kid said:")
        print("\n")
        type.type(quote("Mommy, why doesn't that man have a shadow?"))
        print("\n")
        type.type("You look down. Your shadow is... faint. Barely there. Flickering.")
        print("\n")
        type.type("When did that start happening?")
        self.lose_sanity(12)
        print("\n")

    # === DOG BITE WOUND CHAIN ===

    def dog_bite_rabies_scare(self):
        if not self.has_danger("Dog Bite Wound"):
            self.day_event()
            return
        type.type("You look at your arm in the car. Your dog bite wound is healing, but something else is wrong.")
        print("\n")
        type.type("You're feverish. Light hurts your eyes. Water makes you gag.")
        print("\n")
        type.type("Oh God. Rabies. The dog had rabies.")
        print("\n")
        type.type("You race to the hospital. They test you. Hours of waiting.")
        print("\n")
        chance = random.randrange(10)
        if chance < 8:
            type.type("Negative. No rabies. Just a regular infection and paranoia.")
            print("\n")
            type.type("They give you antibiotics and tell you to calm down.")
            self.hurt(10)
            self.lose_sanity(15)
        else:
            type.type("Positive. The dog had rabies. You have rabies.")
            print("\n")
            type.type("They start the shots immediately. Painful. Expensive. Necessary.")
            print("\n")
            type.type("You'll live, but you'll never forget the two weeks of waiting to die.")
            self.hurt(30)
            self.lose_sanity(25)
            if self.get_balance() >= 2000:
                type.type("Rabies treatment: " + red(bright("$2000")) + ".")
                self.change_balance(-2000)
        self.remove_danger("Dog Bite Wound")
        print("\n")

    # === FUEL LEAK CHAIN ===

    def fuel_leak_fire(self):
        if not self.has_danger("Fuel Leak"):
            self.day_event()
            return
        type.type("You smell gas again. Stronger this time. Much stronger.")
        print("\n")
        type.type("Then you see the spark. A wire rubbing against metal.")
        print("\n")
        type.type("You have maybe three seconds to react.")
        print("\n")
        chance = random.randrange(10)
        if chance < 6:
            type.type("You bail out. Hit the ground rolling. Keep going.")
            print("\n")
            type.type("The car doesn't explode. But it does catch fire. Your home is burning.")
            print("\n")
            type.type("You watch helplessly as everything you own goes up in flames.")
            self.remove_item("Car")
            self.remove_danger("Fuel Leak")
            self.lose_sanity(30)
            lost = self.get_balance() * 0.25
            self.change_balance(-lost)
        else:
            type.type("Too slow. The fire starts before you're out.")
            print("\n")
            type.type("Your clothes catch. Your hair. You're screaming and rolling on the ground.")
            print("\n")
            type.type("Someone puts you out with a fire extinguisher. But the damage is done.")
            self.hurt(50)
            self.lose_sanity(35)
            self.remove_item("Car")
            self.remove_danger("Fuel Leak")
            self.add_danger("Burn Scars")
        print("\n")

    def fuel_leak_fixed(self):
        if not self.has_danger("Fuel Leak"):
            self.day_event()
            return
        if self.get_balance() < 150:
            self.day_event()
            return
        type.type("A mechanic notices your car leaking gas in the parking lot.")
        print("\n")
        type.type(quote("Hey buddy, you know your fuel line is busted? That's a fire hazard."))
        print("\n")
        type.type(quote("I can fix it for $150. Cash. Right now. Before you blow yourself up."))
        print("\n")
        answer = ask.yes_or_no("Pay the mechanic? ($150) ")
        if answer == "yes":
            type.type("He works for an hour. Gets covered in grease. But he fixes it.")
            print("\n")
            type.type(quote("There. No more kaboom.") + " He grins.")
            self.change_balance(-150)
            self.remove_danger("Fuel Leak")
        else:
            type.type("He shrugs. " + quote("Your funeral, man."))
            self.lose_sanity(5)
        print("\n")

    # === HEART CONDITION CHAIN ===

    def heart_condition_flare(self):
        if not self.has_danger("Heart Condition"):
            self.day_event()
            return
        type.type("You grip the steering wheel. Your chest tightens. Not again. Not now.")
        print("\n")
        type.type("You fumble for the pills the doctor gave you. Can't find them.")
        print("\n")
        type.type("The pain spreads. Down your arm. Up your jaw. Can't breathe.")
        print("\n")
        chance = random.randrange(10)
        if chance < 6:
            type.type("Found them. You swallow two dry and wait.")
            print("\n")
            type.type("Slowly, the pain fades. The pressure eases. You're okay. This time.")
            self.hurt(15)
            self.lose_sanity(10)
        elif chance < 9:
            type.type("Someone sees you clutching your chest. Calls 911.")
            print("\n")
            type.type("Hospital. Another stent. Another lecture about stress.")
            self.hurt(35)
            self.lose_sanity(15)
            if self.get_balance() >= 1500:
                type.type("Bill: " + red(bright("$1500")) + ".")
                self.change_balance(-1500)
        else:
            type.type("This one is worse. Much worse. The big one.")
            print("\n")
            type.type("You collapse. Everything goes gray. Then black.")
            print("\n")
            self.kill("Heart attack. Your body couldn't take the stress anymore.")
            return
        print("\n")

    # === SHOULDER DESTROYED CHAIN ===

    def shoulder_chronic_pain(self):
        if not self.has_danger("Shoulder Destroyed"):
            self.day_event()
            return
        type.type("You try to adjust your car seat and wince. Your shoulder is on fire today. Some days are worse than others.")
        print("\n")
        type.type("You can barely lift your arm. Simple things—opening doors, reaching for chips—agony.")
        print("\n")
        type.type("This is your life now. Chronic pain. Forever.")
        self.hurt(10)
        self.lose_sanity(5)
        print("\n")

    def shoulder_painkiller_addiction(self):
        if not self.has_danger("Shoulder Destroyed"):
            self.day_event()
            return
        if self.has_met("Painkiller Offer"):
            self.day_event()
            return
        self.meet("Painkiller Offer")
        type.type("A guy in the parking lot notices you wincing, rubbing your shoulder.")
        print("\n")
        type.type(quote("Bad injury? I got something for that. Take the edge off."))
        print("\n")
        type.type("He shows you a bottle of pills. Oxycodone. Not his prescription.")
        print("\n")
        if self.get_balance() >= 100:
            answer = ask.yes_or_no("Buy the painkillers? ($100) ")
            if answer == "yes":
                type.type("You hand over the money. Pop two pills.")
                print("\n")
                type.type("Twenty minutes later, the pain is... gone. Just warmth and peace.")
                print("\n")
                type.type("This is dangerous. You know this is dangerous. But God, it feels good.")
                self.change_balance(-100)
                self.hurt(-20)  # Heals temporarily
                self.restore_sanity(15)
                self.add_danger("Painkiller Dependency")
            else:
                type.type("You shake your head. He shrugs and walks away.")
        else:
            type.type("You can't afford them anyway. Small mercies.")
        print("\n")

    # === PAINKILLER DEPENDENCY CHAIN ===

    def painkiller_withdrawal(self):
        if not self.has_danger("Painkiller Dependency"):
            self.day_event()
            return
        type.type("You're sitting in your car, shaking. You're out of pills. Have been for two days.")
        print("\n")
        type.type("Your body is screaming. Sweating. Shaking. Nausea. Everything hurts MORE than before.")
        print("\n")
        type.type("This is withdrawal. This is what addiction feels like.")
        print("\n")
        self.hurt(25)
        self.lose_sanity(20)
        print("\n")

    def painkiller_dealer_returns(self):
        if not self.has_danger("Painkiller Dependency"):
            self.day_event()
            return
        type.type("A tap on your car window - the pill guy is back. Like he knew you'd need him.")
        print("\n")
        type.type(quote("Looking rough, friend. Need a refill?"))
        print("\n")
        if self.get_balance() >= 150:
            answer = ask.yes_or_no("Buy more pills? ($150 - prices went up) ")
            if answer == "yes":
                type.type("You pay. You take. The pain goes away. The cycle continues.")
                self.change_balance(-150)
                self.hurt(-15)
                self.restore_sanity(10)
            else:
                type.type("You say no. It's the hardest thing you've ever done.")
                print("\n")
                type.type("He'll be back. They always come back.")
        else:
            type.type("You don't have the money. He walks away. The withdrawal continues.")
            self.hurt(10)
            self.lose_sanity(10)
        print("\n")

    def painkiller_overdose(self):
        if not self.has_danger("Painkiller Dependency"):
            self.day_event()
            return
        type.type("Sitting in your car, you take an extra pill. Then another. The pain is so bad today.")
        print("\n")
        type.type("Then another. When did you take the last one? You can't remember.")
        print("\n")
        type.type("Everything feels slow. Warm. Your breathing is shallow.")
        print("\n")
        chance = random.randrange(10)
        if chance < 7:
            type.type("You fall asleep. Wake up twelve hours later, covered in sweat, but alive.")
            print("\n")
            type.type("That was close. Too close. Maybe you should stop.")
            self.hurt(20)
            self.lose_sanity(15)
        else:
            type.type("You stop breathing. Simple as that. The pills take you under and you don't come back up.")
            print("\n")
            self.kill("Overdose. Another statistic. Another preventable death.")
            return
        print("\n")

    # === BURN SCARS CHAIN ===

    def burn_scars_stares(self):
        if not self.has_danger("Burn Scars"):
            self.day_event()
            return
        type.type("You step out of your car. People stare at your scars. They try to hide it, but they stare.")
        print("\n")
        type.type("Children point. Adults look away too quickly. Nobody meets your eyes.")
        print("\n")
        type.type("You used to be invisible. Now you're a spectacle.")
        self.lose_sanity(8)
        print("\n")

    def burn_scars_infection(self):
        if not self.has_danger("Burn Scars"):
            self.day_event()
            return
        type.type("You check yourself in the car mirror. Your burn scars are weeping. Infected, probably. You can't afford proper care.")
        print("\n")
        type.type("You clean them with water and hope. That's all you have.")
        print("\n")
        chance = random.randrange(5)
        if chance == 0:
            type.type("The infection spreads. You need real help.")
            self.hurt(30)
            self.add_danger("Infected Burns")
        else:
            type.type("It seems to be okay. For now.")
            self.hurt(10)
        print("\n")

    # === ATM THEFT CHAIN ===

    def weakened_immune_cold(self):
        if not self.has_danger("Weakened Immune System"):
            self.day_event()
            return
        type.type("Sitting in your car, you catch a cold. Nothing serious, normally.")
        print("\n")
        type.type("But with your weakened immune system, it hits hard. Very hard.")
        print("\n")
        type.type("You're bedridden for a week. In your car. Miserable.")
        self.hurt(25)
        self.lose_sanity(10)
        print("\n")

    def weakened_immune_pneumonia(self):
        if not self.has_danger("Weakened Immune System"):
            self.day_event()
            return
        type.type("You're shivering in your car. That cold turned into something worse. Pneumonia.")
        print("\n")
        type.type("You can't breathe. You're coughing blood. This is bad.")
        print("\n")
        chance = random.randrange(10)
        if chance < 7:
            type.type("Hospital. Antibiotics. Oxygen. They save you.")
            self.hurt(40)
            self.lose_sanity(15)
            if self.get_balance() >= 1000:
                type.type(" Bill: " + red(bright("$1000")) + ".")
                self.change_balance(-1000)
        else:
            type.type("Your lungs fill with fluid. You drown in your own body.")
            print("\n")
            self.kill("Pneumonia. Your immune system couldn't fight anymore.")
            return
        print("\n")

    # === COCAINE CHAIN (from drug dealer event) ===

    def cocaine_temptation(self):
        if not self.has_item("Bag of Cocaine"):
            self.day_event()
            return
        type.type("You're sitting in your car. You still have that bag of cocaine. It's been staring at you.")
        print("\n")
        type.type("You've never tried it. But you're tired. So tired. And it promises energy.")
        print("\n")
        answer = ask.option("What do you do? ", ["try it", "sell it", "throw it away"])
        print("\n")
        if answer == "try it":
            type.type("You snort a line. Your first time.")
            print("\n")
            type.type("...")
            print("\n")
            type.type("Oh. OH. This is... this is AMAZING.")
            print("\n")
            type.type("Colors are brighter. You're invincible. Every problem seems solvable.")
            print("\n")
            type.type("You don't sleep for 36 hours. When you crash, you crash HARD.")
            self.hurt(-30)  # Temporary boost
            self.restore_sanity(20)  # Temporary
            self.remove_item("Bag of Cocaine")
            self.add_danger("Cocaine User")
        elif answer == "sell it":
            type.type("You find a buyer. Some desperate guy in the casino bathroom.")
            print("\n")
            type.type("You sell it for $300. Not a great deal, but you're not a drug dealer.")
            self.change_balance(300)
            self.remove_item("Bag of Cocaine")
        else:
            type.type("You flush it. Watch it swirl away. Good riddance.")
            print("\n")
            type.type("Part of you wonders what it would have been like. Most of you is relieved.")
            self.remove_item("Bag of Cocaine")
            self.restore_sanity(5)
        print("\n")

    def cocaine_crash(self):
        if not self.has_danger("Cocaine User"):
            self.day_event()
            return
        type.type("You're slumped in your car seat. The crash comes. And it's BRUTAL.")
        print("\n")
        type.type("Depression. Paranoia. Your teeth won't stop chattering.")
        print("\n")
        type.type("You need more. Your body NEEDS more. But you don't have any.")
        self.hurt(30)
        self.lose_sanity(25)
        print("\n")

    def cocaine_heart_attack(self):
        if not self.has_danger("Cocaine User"):
            self.day_event()
            return
        type.type("You're gripping the steering wheel. Your heart is racing. Has been for hours. Something's wrong.")
        print("\n")
        type.type("Chest pain. Arm pain. The cocaine was cut with something. Something bad.")
        print("\n")
        chance = random.randrange(10)
        if chance < 6:
            type.type("It passes. Slowly. You lie in your car, convinced you're dying, but you don't.")
            self.hurt(35)
            self.lose_sanity(20)
            self.remove_danger("Cocaine User")
        else:
            type.type("Your heart gives out. Cocaine-induced cardiac arrest.")
            print("\n")
            self.kill("Drug overdose. The coke was cut with fentanyl. You never had a chance.")
            return
        print("\n")

    # === STRAY CAT FRIEND CHAIN ===

    def bridge_angel_returns(self):
        if not self.has_met("Bridge Angel"):
            self.day_event()
            return
        if self.has_met("Bridge Angel Returns"):
            self.day_event()
            return
        self.meet("Bridge Angel Returns")
        type.type("You step out of your car and see her again. The woman from the bridge. The one who stopped you.")
        print("\n")
        type.type("She recognizes you too. Walks over. Smiles.")
        print("\n")
        type.type(quote("Hey. You're still here. I'm glad."))
        print("\n")
        type.type("She gives you her number. " + quote("If you ever need to talk. About anything. Call me."))
        print("\n")
        type.type("You put it in your pocket. It feels like it weighs a hundred pounds.")
        self.add_item("Angel's Number")
        self.restore_sanity(15)
        self._storyline_system.advance("bridge_angel")
        print("\n")

    def call_bridge_angel(self):
        if not self.has_item("Angel's Number"):
            self.day_event()
            return
        type.type("Bad day. Really bad. Sitting in your car, you dig out that number. Your hands are shaking.")
        print("\n")
        type.type("She answers on the second ring.")
        print("\n")
        type.type(quote("Hey. I was hoping you'd call. Talk to me. What's going on?"))
        print("\n")
        type.type("You talk for two hours. About everything. The gambling. The car. The fear.")
        print("\n")
        type.type("She doesn't judge. Doesn't lecture. Just listens.")
        print("\n")
        type.type(quote("You're stronger than you think. I believe in you."))
        self.restore_sanity(30)
        self._storyline_system.complete("bridge_angel")
        print("\n")

    # === GAS STATION HERO CHAIN ===

    def gas_station_hero_recognized(self):
        if not self.has_met("Gas Station Hero"):
            self.day_event()
            return
        type.type("You head out from your car to a convenience store. Someone points at you.")
        print("\n")
        type.type(quote("That's him! That's the guy who stopped the robbery!"))
        print("\n")
        type.type("People start clapping. The cashier gives you free coffee.")
        print("\n")
        type.type("You feel like a fraud. You just reacted. Didn't think. Could have died.")
        print("\n")
        type.type("But the coffee is nice.")
        self.restore_sanity(10)
        print("\n")

    def gas_station_hero_interview(self):
        if not self.has_met("Gas Station Hero"):
            self.day_event()
            return
        if self.has_met("Hero Interview"):
            self.day_event()
            return
        self.meet("Hero Interview")
        type.type("You're sitting in your car when a news van pulls up. A local station wants to interview you about the robbery.")
        print("\n")
        answer = ask.yes_or_no("Do the interview? ")
        if answer == "yes":
            type.type("They film you by your car. Which is... not a great look.")
            print("\n")
            type.type("The segment runs on the evening news. " + quote("Local Homeless Man Stops Armed Robbery!"))
            print("\n")
            type.type("The comments online are split between calling you a hero and mocking your living situation.")
            self.restore_sanity(5)
            self.lose_sanity(5)  # Mixed feelings
            self.meet("Media Known")
        else:
            type.type("You decline. You're not a hero. You just did what anyone would do.")
        print("\n")

    # === VOODOO DOLL ===

    def voodoo_doll_temptation(self):
        """The Voodoo Doll calls out to be used. Powerful, but costs sanity."""
        if not self.has_item("Voodoo Doll"):
            self.day_event()
            return
        if self.has_met("Voodoo Doll Used"):
            self.day_event()
            return
        self.meet("Voodoo Doll Used")
        type.type("The " + cyan(bright("Voodoo Doll")) + " has been sitting in your bag. A small wax figure, handmade, crude.")
        print("\n")
        type.type("You take it out. It's warm in your hand. Warmer than it should be.")
        print("\n")
        type.type("The swamp witch said: " + quote("You know what to do with this.") + " Do you?")
        print("\n")
        action = ask.option("What do you do with it?", ["stick a pin in it", "burn it", "keep it safe"])
        print("\n")
        if action == "stick a pin in it":
            type.type("You find a pin. You push it in slowly.")
            print("\n")
            type.type("...")
            print("\n")
            type.type("Somewhere across town, someone stubs their toe. You can't know this. But you do.")
            print("\n")
            type.type("More importantly: a rival gambler who had it out for you is suddenly... distracted tonight.")
            self.change_balance(random.randint(200, 800))
            self.lose_sanity(random.choice([8, 10, 15]))
            type.type("The doll crumbles to wax dust in your hands. The deed is done.")
            self.use_item("Voodoo Doll")
        elif action == "burn it":
            type.type("You hold the doll over your lighter. It resists, hissing and spitting black smoke.")
            print("\n")
            type.type("Then it goes. Fast. Too fast. A flash of heat and it's ash.")
            print("\n")
            type.type("You smell something you can't place. Not unpleasant. Like turned earth after rain.")
            print("\n")
            type.type("Your hands stop shaking. For the first time in weeks.")
            self.restore_sanity(random.choice([15, 20]))
            self.heal(10)
            self.use_item("Voodoo Doll")
        else:
            type.type("You put it back. Some things are better left undone.")
            print("\n")
            type.type("But it's warmer now than when you picked it up. Like it noticed you almost went through with it.")
            self.lose_sanity(3)
        print("\n")

    # === HIGH ROLLER KEYCARD CHAIN ===


