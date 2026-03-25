import random
import time
import sys
import typer
import msvcrt
from colorama import Fore, Back, Style, init
init(convert=True)

PAR = "\n"

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
        if self.has_item("King of the Road"):
            type.type(cyan(bright("King of the Road")) + " enters the room. The loan shark straightens up. Someone of this... stature? Owing them money? It doesn't compute.")
            print(PAR)
            type.type(quote("Forget it,") + " he says. " + quote("Consider it a gift."))
            self.restore_sanity(10)
            return
        if self.has_item("Master of Games"):
            type.type("The " + cyan(bright("Master of Games")) + " aura fills the room. Wine in hand, heirloom watch on wrist, every con in the book loaded.")
            print(PAR)
            type.type("You negotiate the debt into a profitable arrangement. They owe YOU by the end.")
            self.change_balance(500)
            return
        type.type("A black SUV pulls up beside your car. Two men get out, unhurried, and you recognize the tattoos before you recognize the faces — the kind of tattoos that tell a story you don't want to hear. Before you can process what's happening, they're dragging you out of your car by your collar and setting you against the hood like luggage.")
        print(PAR)
        type.type(quote("Remember us? Remember the money you borrowed to start this little gambling hobby of yours?"))
        print(PAR)
        type.type("You don't remember. But looking at their faces — at the very specific stillness behind their eyes — you're starting to. One of them places a pair of bolt cutters on the hood of your car with quiet, deliberate care. Not threatening. Just present.")
        print(PAR)
        type.type(quote("$50,000. Plus interest. That's $75,000 now. You got two days.") + " He doesn't raise his voice. He doesn't need to. " + quote("Or we start taking fingers."))
        print(PAR)
        if self.has_item("Gold Chain"):
            type.type("Their eyes drift to your neck. Your " + cyan(bright("Gold Chain")) + " catches the light from the streetlamp.")
            print(PAR)
            type.type(quote("That's real gold. Custom links. Maybe fourteen hundred, fifteen hundred worth.") + " He tilts his head. " + quote("That buys you goodwill. Not time. Goodwill."))
            print(PAR)
            chain_answer = ask.yes_or_no("Hand over the Gold Chain to ease the tension? ")
            if chain_answer == "yes":
                type.type("You unclasp it and hold it out. He takes it without reaching — you have to step forward and place it in his palm.")
                print(PAR)
                type.type(quote("Smart. You've got two days. Same as before. But now I believe you intend to pay."))
                print(PAR)
                type.type("The bolt cutters go back in the trunk. They leave without touching you.")
                print(PAR)
                type.type("You stand in the empty lot, collarless, poorer, intact. That last part is the one that matters.")
                # Alternative resolution: debt deferred, not erased. Danger still added.
                self.use_item("Gold Chain")
                self.lose_sanity(10)
                self.add_danger("Loan Shark Deadline")
                print(PAR)
                return
        answer = ask.option("What do you do? ", ["pay now", "beg for time", "refuse"])
        if answer == "pay now":
            if self.get_balance() >= 75000:
                type.type("You hand over " + red(bright("$75,000")) + ". Every bill feels like a small death. The kind of money you'd spent months accumulating, gone in thirty seconds while a man with bolt cutters watches.")
                self.change_balance(-75000)
                print(PAR)
                type.type(quote("Pleasure doing business. Don't borrow again unless you can pay."))
                print(PAR)
                type.type("They leave. You're poorer and intact, which is the best outcome available to you right now.")
                self.lose_sanity(15)
            else:
                type.type(quote("That's not enough. You're short."))
                print(PAR)
                type.type("Before you can explain, one of them grabs your hand and spreads your fingers on the hood of your car.")
                print(PAR)
                type.type(red(bright("CRUNCH.")))
                print(PAR)
                type.type("You scream. Your pinky finger is gone. Blood pools on the hood.")
                print(PAR)
                type.type(quote("That's the interest. Now pay the rest, or lose more."))
                taken = self.get_balance()
                self.change_balance(-taken)
                self.hurt(40)
                self.lose_sanity(30)
                self.add_status("Missing Finger")
                self.add_danger("Severed Finger")
        elif answer == "beg for time":
            type.type(quote("Please, I just need a few more days. I'm so close to a big win-"))
            print(PAR)
            type.type("The bigger one punches you in the stomach. You double over, gasping.")
            print(PAR)
            type.type(quote("Two days. Not three. Two. And we're adding another 10K for wasting our time."))
            print(PAR)
            type.type("They get back in the SUV and drive away. You have 48 hours.")
            self.hurt(20)
            self.lose_sanity(20)
            self.add_danger("Loan Shark Deadline")
        else:
            type.type(quote("I'm not paying you anything. I don't even remember borrowing-"))
            print(PAR)
            type.type("The bolt cutters flash. Pain explodes in your hand.")
            print(PAR)
            type.type(red(bright("Your ring finger hits the pavement with a wet sound.")))
            print(PAR)
            type.type("You scream. They keep hitting you. Ribs crack. Teeth loosen.")
            print(PAR)
            if random.random() < 0.3:
                type.type("One of them stomps on your head. Everything goes dark.")
                print(PAR)
                type.type("You don't wake up.")
                self.kill("Beat to death by loan sharks. They took your fingers as souvenirs.")
                return
            else:
                type.type("Eventually, they stop. You're lying in a pool of your own blood.")
                print(PAR)
                type.type(quote("We'll be back. And next time, we take the whole hand."))
                self.hurt(70)
                self.lose_sanity(40)
                self.add_status("Missing Finger")
                self.add_danger("Loan Shark Revenge")
        print(PAR)

        print(PAR)
        return
    def the_desperate_gambler(self):
        # EVENT: A man begs you for money - he's in deep to the wrong people
        # EFFECTS: Help = lose money but save a life (or be scammed); Refuse = witness his fate
        # DARK: Witness suicide if you refuse
        type.type("A man approaches your car from the sidewalk — shaking, crying, wearing the particular expression of someone who has run out of all other options and arrived at you. He knocks on your window with a trembling fist.")
        print(PAR)
        type.type(quote("Please. Please, you have to help me. I owe them money. So much money. If I don't pay by midnight, they're going to kill me. Please. I have a daughter."))
        print(PAR)
        type.type("He shows you a photo through the glass. A little girl with pigtails and a gap-toothed smile, squinting into the sun like the world is too bright and she loves it anyway.")
        print(PAR)
        if self.has_item("Voice Soother"):
            type.type("You uncap the " + cyan(bright("Voice Soother")) + ", take a sip. Your voice becomes velvet.")
            print(PAR)
            type.type(quote("Come here. We'll figure this out.") + " He listens. He steps back. He collapses into your arms sobbing.")
            print(PAR)
            type.type("You saved a life with cough drops dissolving in minty water. How is this real?")
            self.restore_sanity(10)
            self.use_item("Voice Soother")
            self.meet("The Desperate Man")
            print(PAR)
            return
        if self.has_item("Flask of Split Serum"):
            type.type("The " + cyan(bright("Flask of Split Serum")) + " warms in your pocket. For a moment, you see two paths: one where you help, one where you don't. Both feel real.")
            print(PAR)
        answer = ask.yes_or_no("Give him money? ")
        if answer == "yes":
            if self.has_item("Phoenix Feather") or self.has_item("White Feather"):
                feather = "Phoenix Feather" if self.has_item("Phoenix Feather") else "White Feather"
                if feather == "Phoenix Feather":
                    amount = min(self.get_balance(), random.randint(150, 500))
                    type.type("The " + cyan(bright("Phoenix Feather")) + " in your pocket runs hot against your leg. When you pull it out, the man stops shaking long enough to stare.")
                    print(PAR)
                    type.type("A curl of heat coils off the feather's tip. Not fire. Promise. Survival. He looks at the little flare like it's permission to believe he'll see morning.")
                    print(PAR)
                    type.type("You hand over " + red(bright("$" + str(amount))) + ". Somehow it feels like enough. More than enough.")
                else:
                    amount = min(self.get_balance(), random.randint(250, 900))
                    type.type("The " + cyan(bright("White Feather")) + " slips loose when you reach for your wallet and drifts into his trembling hands.")
                    print(PAR)
                    type.type("He goes quiet. The panic doesn't vanish, but it narrows into something survivable. You hand over " + red(bright("$" + str(amount))) + ", and for once mercy feels practical instead of naive.")
                self.update_white_feather_durability()
            else:
                amount = min(self.get_balance(), random.randint(500, 2000))
                type.type("You hand over " + red(bright("$" + str(amount))) + ". It's a lot. But his eyes looked real. The photograph looked real. The trembling was real — you know what fake desperation looks like, and this wasn't it.")
            self.change_balance(-amount)
            self._total_given_away += amount
            print(PAR)
            if random.random() < 0.7:
                type.type(quote("Thank you. Thank you so much. You saved my life. I'll pay you back someday, I swear it."))
                print(PAR)
                type.type("He runs. You never see him again. But you hope he made it to midnight.")
                self.restore_sanity(14 if self.has_item("Phoenix Feather") else 10)
                self.meet("The Desperate Man")
            else:
                type.type("He takes the money. He counts it, right there in front of you. Then he looks up and laughs — the uncomplicated laugh of a man who just got what he came for.")
                print(PAR)
                type.type(quote("Sucker. There's one born every minute."))
                print(PAR)
                type.type("He walks away, still counting. The photograph was probably a prop. The little girl with the pigtails was probably a stock photo. You sit in your car for a long time, deciding whether to feel stupid or just sad.")
                self.lose_sanity(15)
        else:
            type.type(quote("I'm sorry. I can't. I need every dollar I have."))
            print(PAR)
            type.type("The man's face goes through about six emotions in two seconds before settling on something hollow. " + quote("Then I'm already dead."))
            print(PAR)
            type.type("He walks away. Toward the bridge. You watch him go until he rounds a corner.")
            print(PAR)
            type.type("...")
            print(PAR)
            type.type("An hour later, you hear sirens in the direction of the bridge. You don't drive that way. You can't look. But you know — the way you always know the things you didn't want to know — what those sirens are for.")
            self.lose_sanity(25)
            self.add_status("Witnessed Death")
        print(PAR)

        print(PAR)
        return
    def withdrawal_nightmare(self):
        # EVENT: Severe gambling withdrawal - your body and mind rebel
        # CONDITION: Sanity below 30
        # EFFECTS: Physical and mental symptoms, risk of self-harm
        if self.get_sanity() >= 30:
            self.day_event()
            return
        type.type("You're soaked through in your car seat, your hands shaking badly enough that you can't hold the steering wheel, your heart trying to punch its way out of your chest like it finally figured out this situation is not okay. You NEED to gamble. The urge isn't a want — it's a physical law, gravity pulling at every cell.")
        print(PAR)
        type.type("The casino is closed. It's 3 AM. You can't. You CAN'T.")
        print(PAR)
        type.type("Your skin crawls like something's trying to get out. You scratch your arms until they bleed. It doesn't help. You punch the steering wheel once, twice, a third time so hard the horn bleats into the empty parking lot. Your knuckles split open. That helps, a little. Then it doesn't.")
        print(PAR)
        answer = ask.option("What do you do? ", ["ride it out", "drive to casino anyway", "hurt yourself more"])
        if answer == "ride it out":
            type.type("You grip the steering wheel until your knuckles go white and your forearms shake. You breathe. In. Out. In. Out. The rhythm is the only thing that feels real.")
            print(PAR)
            type.type("Hours pass. The parking lot lightens. The shaking gets worse before it gets better. Then, eventually, it gets better. You survived tonight. You know it'll happen again.")
            self.hurt(10)
            self.lose_sanity(10)
        elif answer == "drive to casino anyway":
            type.type("You drive. Ninety miles an hour, running lights, jaw clenched, like arriving ten minutes faster will change the fact that the doors are locked.")
            print(PAR)
            type.type("The casino is dark. Silent. You pound on the glass doors until a security guard materializes from somewhere.")
            print(PAR)
            type.type(quote("Sir, we're closed. You need to leave or we'll call the police."))
            print(PAR)
            type.type("You sit in the parking lot for four hours, watching the sky lighten, waiting for them to open. Just waiting. It's the most honest thing you've done in weeks.")
            self.lose_sanity(20)
        else:
            type.type("You need to feel something else. Anything that isn't this.")
            print(PAR)
            type.type("The pain helps, briefly — a clean sharp thing you chose, which is more than you can say for the rest of it. Then it doesn't help. Then it just hurts.")
            print(PAR)
            type.type("You look at your arms in the pale dashboard light. At the blood, at the evidence of what this thing has made you. You sit with that knowledge for a long time.")
            self.hurt(25)
            self.lose_sanity(15)
            self.add_danger("Self-Harm Wounds")
        print(PAR)

        print(PAR)
        return
    def organ_harvester(self):
        # EVENT: Someone offers to buy your kidney - you're worth more in parts
        # CONDITION: Balance below $1,000 (desperate) OR health below 30
        # EFFECTS: Accept = money but permanent health loss; Refuse = nothing
        # DARK: Selling body parts for gambling money
        if self.get_balance() >= 1000 and self.get_health() >= 30:
            self.day_event()
            return
        if self.has_item("Third Eye"):
            type.type("The " + cyan(bright("Third Eye")) + " pulses a warning. Danger here. Five seconds. You step left. You cross the street.")
            print(PAR)
            type.type("Three men exit the building. They look right where you were standing.")
            self.restore_sanity(10)
            return
        if self.has_item("Ghost Protocol"):
            type.type(cyan(bright("Ghost Protocol")) + " makes you invisible to targeting. They can't focus on you.")
            print(PAR)
            type.type("They walk past you three times. Eventually give up.")
            self.restore_sanity(5)
            return
        type.type("A clean-looking van pulls up. A man in scrubs steps out. He's smiling.")
        print(PAR)
        type.type(quote("You look like someone who could use some money. Am I right?"))
        print(PAR)
        type.type("He pulls out a business card. 'ORGAN SOLUTIONS - We Pay Top Dollar.'")
        print(PAR)
        type.type(quote("One kidney. $40,000. Cash. Tonight. You won't even miss it."))
        print(PAR)
        answer = ask.yes_or_no("Sell your kidney? ")
        if answer == "yes":
            type.type("You get in the van. Part of you knows this is insane. The rest of you needs the money.")
            print(PAR)
            type.type("...")
            print(PAR)
            type.type("You wake up in a motel room. There's a fresh scar on your side. An envelope on the nightstand.")
            print(PAR)
            type.type(green(bright("$40,000")) + " in cash. Just like they promised.")
            self.change_balance(40000)
            print(PAR)
            type.type("You're lighter now. In more ways than one. Your maximum health is permanently reduced.")
            self.hurt(30)
            self.add_status("One Kidney")
            self.lose_sanity(20)
        else:
            type.type(quote("No thanks. I'm not that desperate yet."))
            print(PAR)
            type.type("The man shrugs. " + quote("Yet. I like that word. Here's my card if you change your mind."))
            print(PAR)
            type.type("He drives away. You throw the card in the trash. Then you fish it back out.")
            print(PAR)
            type.type("Just in case.")
        print(PAR)

        print(PAR)
        return
    def casino_overdose(self):
        # EVENT: Find someone ODing in the casino bathroom
        # EFFECTS: Help = risk getting blamed, possibly save a life; Ignore = they die, lose sanity
        # DARK: Drug use and death in casinos
        type.type("You head into the casino and walk into the bathroom. You freeze.")
        print(PAR)
        type.type("Someone's on the floor. Blue lips. Needle still in their arm. Foam at the mouth.")
        print(PAR)
        type.type("They're not breathing. Or barely breathing. You can't tell.")
        print(PAR)
        answer = ask.option("What do you do? ", ["call for help", "try to help yourself", "walk away"])
        if answer == "call for help":
            type.type("You run out screaming for help. Security comes. Paramedics arrive.")
            print(PAR)
            if random.random() < 0.6:
                type.type("They stabilize her. She's going to make it. Barely.")
                print(PAR)
                type.type("A security guard pats you on the shoulder. " + quote("You saved her life."))
                self.restore_sanity(5)
            else:
                type.type("It's too late. She's gone before the paramedics even arrive.")
                print(PAR)
                type.type("You watch them cover her body with a sheet. She was young. Maybe 25.")
                self.lose_sanity(20)
                self.add_status("Witnessed Death")
        elif answer == "try to help yourself":
            type.type("You check for a pulse. Faint. You start CPR, trying to remember how it works.")
            print(PAR)
            type.type("Chest compressions. Mouth to mouth. Chest compressions. Her lips are cold.")
            print(PAR)
            if self.has_item("Flask of Second Chance"):
                type.type("The " + cyan(bright("Flask of Second Chance")) + " cracks in your hand. Time hiccups.")
                print(PAR)
                type.type("You feel it rewind. Her eyes flutter open. She gasps.")
                print(PAR)
                type.type(quote("What... happened?") + " She sits up, confused but alive.")
                self.use_item("Flask of Second Chance")
                self.restore_sanity(20)
                self.meet("Rewound Survivor")
        elif answer == "try to help yourself":
            type.type("You check for a pulse. Faint. You start CPR, trying to remember how it works.")
            print(PAR)
            type.type("Chest compressions. Mouth to mouth. Chest compressions. Her lips are cold.")
            print(PAR)
            if self.has_item("Flask of Second Chance"):
                type.type("The " + cyan(bright("Flask of Second Chance")) + " cracks in your hand. Time hiccups.")
                print(PAR)
                type.type("You feel it rewind. Her eyes flutter open. She gasps.")
                print(PAR)
                type.type(quote("What... happened?") + " She sits up, confused but alive.")
                self.use_item("Flask of Second Chance")
                self.restore_sanity(20)
                self.meet("Rewound Survivor")
            elif random.random() < 0.4:
                type.type("She gasps. Coughs. Vomits. But she's BREATHING.")
                print(PAR)
                type.type("Someone finally notices and calls 911. By the time they arrive, she's conscious.")
                print(PAR)
                type.type(quote("You... saved me...") + " she whispers. Her eyes are hollow. But alive.")
                self.restore_sanity(15)
                self.meet("Casino Survivor")
                if self.has_item("Evidence Kit"):
                    type.type("You snap a quick photo with your " + cyan(bright("Evidence Kit")) + " before the paramedics arrive.")
                    print(PAR)
                    type.type("Later, you could sell this evidence to the police or a reporter for $200-500.")
                    self.add_item("Casino OD Evidence")
            else:
                type.type("She doesn't respond. You keep trying. Keep pushing. Keep breathing.")
                print(PAR)
                type.type("But she's gone. You feel the moment she leaves.")
                print(PAR)
                type.type("Her eyes are still open. Staring at nothing.")
                self.lose_sanity(30)
                self.add_status("CPR Failure")
        else:
            type.type("You back out slowly. Pretend you didn't see anything. It's not your problem.")
            print(PAR)
            type.type("You go back to the tables. Try to focus on the cards. Try not to think about it.")
            print(PAR)
            type.type("An hour later, you hear the sirens. Too late. You know it's too late.")
            print(PAR)
            type.type("You keep playing. What else can you do?")
            self.lose_sanity(25)
            self.add_status("Ignored Death")
        print(PAR)

        print(PAR)
        return
    def cancer_diagnosis(self):
        # EVENT: A cough that won't go away leads to a devastating diagnosis
        # CONDITION: Health below 50 OR has "Chronic Cough" status
        # EFFECTS: Major health reduction, sanity loss, expensive treatment choice
        # MEDICAL: Terminal illness
        if self.get_health() >= 50 and not self.has_status("Chronic Cough"):
            self.day_event()
            return
        type.type("Sitting in your car, the cough has been getting worse. You finally drive to a clinic.")
        print(PAR)
        type.type("X-rays. Blood tests. Waiting. So much waiting.")
        print(PAR)
        type.type("The doctor sits down. She doesn't meet your eyes.")
        print(PAR)
        type.type(quote("I'm sorry. It's cancer. Stage 3 lung cancer."))
        print(PAR)
        type.type("The world goes silent. Your ears ring. This isn't real.")
        print(PAR)
        type.type(quote("Without treatment, you have maybe six months. With treatment... maybe two years."))
        print(PAR)
        type.type(quote("Treatment will cost around $50,000. We can discuss payment plans..."))
        print(PAR)
        answer = ask.option("What do you do? ", ["pay for treatment", "refuse treatment", "break down"])
        if answer == "pay for treatment":
            if self.get_balance() >= 50000:
                type.type("You hand over " + red(bright("$50,000")) + ". Your life savings. For a chance at life.")
                self.change_balance(-50000)
                self.add_status("Chemotherapy")
                type.type(" The chemotherapy starts next week.")
            else:
                type.type(quote("I... I don't have enough."))
                print(PAR)
                type.type("The doctor sighs. " + quote("There are... other options. Experimental treatments. Clinical trials."))
                print(PAR)
                type.type("You sign up for everything. Anything.")
                self.add_status("Experimental Treatment")
            self.lose_sanity(30)
        elif answer == "refuse treatment":
            type.type(quote("No. No treatment. If I'm going to die, I'm going to die on my terms."))
            print(PAR)
            type.type("The doctor nods. She's seen this before. " + quote("It's your choice. I'm sorry."))
            print(PAR)
            type.type("You walk out. Six months. Maybe less. Better make it count.")
            self.lose_sanity(25)
            self.add_status("Terminal")
            self.add_danger("Cancer Untreated")
        else:
            type.type("You break down. Right there in the office. Sobbing. Screaming.")
            print(PAR)
            type.type("The doctor holds your hand. Lets you cry. She's seen this before too.")
            print(PAR)
            type.type("Eventually, the tears stop. You're empty. Hollow.")
            print(PAR)
            type.type(quote("Take some time. Think about it. Come back when you're ready."))
            self.lose_sanity(40)
        print(PAR)

        print(PAR)
        return
    def the_bridge_call(self):
        # EVENT: At your lowest point, the bridge calls to you
        # CONDITION: Sanity below 15
        # EFFECTS: Player must make a choice - potentially fatal
        # MENTAL HEALTH: Suicidal ideation - explicit content warning
        if self.get_sanity() >= 15:
            self.day_event()
            return
        type.type("You start your car and drive. You don't know where. Just... driving.")
        print(PAR)
        type.type("The bridge appears ahead. The big one. The one over the gorge.")
        print(PAR)
        type.type("Your car slows. Stops in the middle. You get out.")
        print(PAR)
        type.type("The wind is cold. The water is far below. Black and quiet.")
        print(PAR)
        type.type("It would be so easy. Just climb over the railing. One step.")
        print(PAR)
        type.type("No more gambling. No more losing. No more living in a car like an animal.")
        print(PAR)
        type.type("No more...")
        print(PAR)
        if self.has_item("Flask of Second Chance"):
            print(PAR)
            type.type("The " + cyan(bright("Flask of Second Chance")) + " burns hot against your chest. A reminder: you've been given another shot. Don't waste it.")
            self.restore_sanity(3)
            print(PAR)
        answer = ask.option("", ["climb the railing", "call someone", "walk away"])
        if answer == "climb the railing":
            type.type("You climb over the railing. The metal is cold. The wind pushes at you.")
            print(PAR)
            type.type("You look down. It's so far. So final.")
            print(PAR)
            if random.random() < 0.6:
                type.type("A car stops. A woman runs toward you.")
                print(PAR)
                type.type(quote("DON'T! Please! Please don't!"))
                print(PAR)
                type.type("She's crying. A stranger, crying for you. When did you last have someone cry for you?")
                print(PAR)
                type.type("She talks you down. Holds your hand. Calls for help.")
                print(PAR)
                type.type("Hours later, you're in a hospital bed. Alive. You're not sure how you feel about that.")
                self.add_status("Survived Attempt")
                self.lose_sanity(10)
                self.meet("Bridge Angel")
            else:
                type.type("You lean forward. Let go.")
                print(PAR)
                type.type("The fall is longer than you expected. Almost peaceful.")
                print(PAR)
                type.type("The last thing you see is the stars above, spinning.")
                self.kill("Jumped from the bridge. The chase for a million ended here.")
                return
        elif answer == "call someone":
            type.type("You pull out your phone. Who do you even call?")
            print(PAR)
            type.type("You dial the suicide hotline. Your hands are shaking so bad you can barely hit the numbers.")
            print(PAR)
            type.type("Someone answers. A voice. Calm. Kind.")
            print(PAR)
            type.type(quote("Hello. You've reached the crisis line. You're not alone. Can you tell me your name?"))
            print(PAR)
            type.type("You talk. For hours. Until the sun comes up.")
            print(PAR)
            type.type("You're still here. Still breathing. That's something.")
            self.restore_sanity(10)
            self.add_status("Called for Help")
        else:
            type.type("You step back. Get in your car. Drive away.")
            print(PAR)
            type.type("Not tonight. Not like this.")
            print(PAR)
            type.type("You don't know why. You don't feel better. You don't feel anything.")
            print(PAR)
            type.type("But you're still here. And tomorrow is another day.")
            self.restore_sanity(5)
        print(PAR)

        print(PAR)
        return
    def the_relapse(self):
        # EVENT: After a big win, the addiction demands MORE
        # CONDITION: Won big recently (balance increased by 50K+ today)
        # EFFECTS: Risk losing everything chasing the high
        # ADDICTION: The insatiable need for more
        if not hasattr(self, '_today_winnings') or self._today_winnings < 50000:
            self.day_event()
            return
        type.type("You're sitting in your car outside the casino. You won big today. Really big. You should walk away.")
        print(PAR)
        type.type("But the cards are still there. The dealer is waiting. The chips are calling.")
        print(PAR)
        type.type("Just one more hand. One more. You're HOT right now.")
        print(PAR)
        if self.has_item("Flask of Imminent Blackjack"):
            type.type("The " + cyan(bright("Flask of Imminent Blackjack")) + " hums in your pocket. A vision flashes: the dealer burns a card. Blackjack. Yours.")
            print(PAR)
            type.type("The high is already there. You know what's coming.")
            self.restore_sanity(5)
        type.type("Your hands are shaking. Not from fear. From NEED.")
        print(PAR)
        answer = ask.yes_or_no("Go back to the tables? ")
        if answer == "yes":
            type.type("You sit back down. The dealer smiles. " + quote("Back for more?"))
            print(PAR)
            if self.has_item("Flask of Pocket Aces"):
                type.type("The " + cyan(bright("Flask of Pocket Aces")) + " burns in your pocket. You feel them before you see them — two aces, waiting in the deck.")
                print(PAR)
                type.type("The first hand is yours.")
                self.restore_sanity(5)
            type.type("Hours pass. You don't notice. The world shrinks to just you and the cards.")
            print(PAR)
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
                print(PAR)
                type.type("When you finally stand up, you've lost " + red(bright("$" + str(int(actual_loss)))) + ".")
                self.change_balance(-actual_loss)
                self.lose_sanity(20)
            else:
                type.type("You don't stop. You CAN'T stop. Hand after hand. Bet after bet.")
                print(PAR)
                type.type("When security finally kicks you out, you're broke. Everything. Gone.")
                print(PAR)
                type.type(quote("I'll win it back. I'll win it all back tomorrow."))
                self.change_balance(-self.get_balance())
                self.lose_sanity(35)
        else:
            type.type("You force yourself to walk away. Every step is agony.")
            print(PAR)
            type.type("The cards call to you. The chips whisper your name.")
            print(PAR)
            if self.has_item("Flask of Dealer's Whispers"):
                type.type("The " + cyan(bright("Flask of Dealer's Whispers")) + " vibrates in your pocket. A whisper, clear as day: " + italic("Walk away now. The house is rigged.") + " Or is it " + italic("Stay. The odds are in your favor.") + "?")
                print(PAR)
                type.type("The flask's voice cuts through the compulsion, ambiguous but insistent.")
                self.restore_sanity(3)
                print(PAR)
            type.type("But you keep walking. Tonight, you won.")
            print(PAR)
            type.type("The battle, at least. The war continues.")
            self.restore_sanity(15)
        print(PAR)

        print(PAR)
        return
    def casino_hitman(self):
        # EVENT: You've won too much - the casino sends someone to "talk" to you
        # CONDITION: Balance >= $800,000
        # EFFECTS: Various outcomes including death, injury, or escape
        # VIOLENCE: Professional intimidation/assassination
        if self.get_balance() < 800000:
            self.day_event()
            return
        if self.has_item("Last Breath Locket"):
            type.type("The hitman takes the shot. The " + cyan(bright("Last Breath Locket")) + " ignites. White fire.")
            print(PAR)
            type.type("Your body knits back together. You stand up. The hitman runs.")
            print(PAR)
            type.type("Death looked at you, confused, and walked away.")
            self.restore_sanity(10)
            return
        if self.has_item("Ghost Protocol"):
            type.type(cyan(bright("Ghost Protocol")) + " — you don't exist. The hitman found the right address but the wrong person.")
            print(PAR)
            type.type("They stand there, confused. You watch from two blocks away.")
            self.restore_sanity(8)
            return
        if self.has_item("Road Warrior Armor"):
            type.type("The hitman unloads. Every impact registers. None penetrate the " + cyan(bright("Road Warrior Armor")) + ".")
            print(PAR)
            type.type("They empty their weapon. You walk toward them. They run.")
            self.restore_sanity(5)
            return
        if self.has_item("Dealer's Mercy") or self.has_item("Dealer's Grudge"):
            item_name = "Dealer's Mercy" if self.has_item("Dealer's Mercy") else "Dealer's Grudge"
            type.type("The man at the bar gets close enough to press the gun into your ribs. Then his eyes drop to the " + cyan(bright(item_name)) + ".")
            print(PAR)
            type.type("Whatever he sees there hits him harder than fear. He freezes. His knuckles go white around the grip.")
            print(PAR)
            type.type(quote("No.") + " It's barely a whisper. " + quote("The house said nothing about you belonging to Him."))
            print(PAR)
            type.type("He stands, leaves cash on the bar, and walks out without looking back. You stay very still until the door closes.")
            self.restore_sanity(10)
            self.update_dealers_grudge_durability()
            print(PAR)
            return
        type.type("You're at the casino bar when a man sits down next to you. You didn't hear him approach.")
        print(PAR)
        type.type(quote("That's a lot of money you've won. Almost a million. Impressive."))
        print(PAR)
        type.type("He's not smiling. His eyes are dead. Professional.")
        print(PAR)
        type.type(quote("The house doesn't like to lose. You understand that, right?"))
        print(PAR)
        type.type("Under the bar, you feel something cold press against your ribs. A gun.")
        print(PAR)
        type.type(quote("You have two choices. Walk away now. Leave the state. Never come back."))
        type.type(quote(" Or..."))
        print(PAR)
        type.type("He doesn't finish the sentence. He doesn't have to.")
        print(PAR)
        if self.has_item("Shiv"):
            print(PAR)
            type.type("Your hand finds the " + cyan(bright("Shiv")) + " in your pocket. The blade is small but the message is clear: you're not defenseless.")
            self.restore_sanity(3)
            print(PAR)
        answer = ask.option("What do you do? ", ["agree to leave", "offer money", "fight back"])
        if answer == "agree to leave":
            type.type(quote("Smart. I like smart people. They live longer."))
            print(PAR)
            type.type("He stands up. The gun disappears.")
            print(PAR)
            type.type(quote("You have 24 hours to leave. Take your money. Don't come back."))
            print(PAR)
            type.type("You watch him walk away. Your hands won't stop shaking.")
            self.lose_sanity(25)
            self.add_danger("Casino Exile")
        elif answer == "offer money":
            type.type(quote("How much to make this go away?"))
            print(PAR)
            type.type("He considers. " + quote("$200,000. Now. And you don't come back for a year."))
            print(PAR)
            if self.get_balance() >= 200000:
                answer2 = ask.yes_or_no("Pay $200,000? ")
                if answer2 == "yes":
                    type.type("You transfer the money. He checks his phone. Nods.")
                    self.change_balance(-200000)
                    print(PAR)
                    type.type(quote("Pleasure doing business. See you in a year."))
                    self.lose_sanity(15)
                else:
                    type.type("His expression doesn't change. The gun presses harder.")
                    print(PAR)
                    type.type(quote("Wrong answer."))
                    print(PAR)
                    type.type(red(bright("BANG.")))
                    print(PAR)
                    type.type("The bar goes silent. You're on the floor. Blood pooling beneath you.")
                    print(PAR)
                    if self.has_item("Phoenix Feather") or self.has_item("White Feather"):
                        feather = "Phoenix Feather" if self.has_item("Phoenix Feather") else "White Feather"
                        type.type("Something in your pocket blazes with sudden heat. The " + cyan(bright(feather)) + " ignites.")
                        print(PAR)
                        type.type("Amber light floods through your chest. The bullet wounds seal themselves. The feather disintegrates into ash.")
                        print(PAR)
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
                        print(PAR)
                        type.type("Weeks later, you wake up in a hospital. Your money is gone. All of it.")
                        self.change_balance(-self.get_balance())
                        self.hurt(80)
                        self.lose_sanity(40)
            else:
                type.type(quote("I don't have that much."))
                print(PAR)
                type.type(quote("Then I guess we go with option two."))
                print(PAR)
                if random.random() < 0.5:
                    type.type("The gun fires. You don't even feel it.")
                    self.kill("Executed by the casino. Too successful for your own good.")
                    return
                else:
                    type.type("But he pauses. Sighs. " + quote("Get out. Now. Before I change my mind."))
                    print(PAR)
                    type.type("You run. You've never run so fast in your life.")
                    self.lose_sanity(30)
        else:
            type.type("You knock the gun away and throw a punch.")
            print(PAR)
            chance = random.randint(1, 10)
            if chance <= 2:
                type.type("The hit connects. He staggers. You grab a bottle and swing.")
                print(PAR)
                type.type("He goes down. People are screaming. You run.")
                print(PAR)
                type.type("You don't know if he's dead. You don't want to know.")
                self.hurt(15)
                self.lose_sanity(20)
                self.add_danger("Casino Enemy")
            elif chance <= 6:
                type.type("He's faster. The gun comes up and fires.")
                print(PAR)
                type.type("Your shoulder explodes in pain. You hit the floor.")
                print(PAR)
                type.type("He stands over you, gun aimed at your head.")
                print(PAR)
                type.type(quote("Stupid."))
                print(PAR)
                type.type("But he doesn't fire again. Just walks away. A warning.")
                self.hurt(50)
                self.lose_sanity(30)
                self.add_danger("Gunshot Wound")
            else:
                type.type("He's faster. Much faster.")
                print(PAR)
                type.type("Three shots. Chest. Chest. Head.")
                print(PAR)
                type.type("You're dead before you hit the floor.")
                self.kill("Killed by a professional. The casino doesn't forgive.")
                return
        print(PAR)

        print(PAR)
        return
    def the_confession(self):
        # EVENT: A dying man confesses his sins to you - you're the only one who will listen
        # EFFECTS: Hear terrible things, gain money, lose sanity
        # DARK: Hearing about horrible deeds
        type.type("An old man grabs your sleeve in the casino parking lot. He's pale. Sweating.")
        print(PAR)
        type.type(quote("Please. I need to tell someone. Before I die. I need to confess."))
        print(PAR)
        type.type("He looks like death. His grip is surprisingly strong.")
        print(PAR)
        answer = ask.yes_or_no("Listen to him? ")
        if answer == "yes":
            type.type("He talks. For an hour. Two. You wish you hadn't listened.")
            print(PAR)
            type.type("Murder. Fraud. Things you can't unhear. Victims you can't forget.")
            print(PAR)
            type.type("When he's done, he presses a key into your hand.")
            print(PAR)
            type.type(quote("Storage unit. 47B. Take it all. I don't need it anymore."))
            print(PAR)
            type.type("He walks away. You find the storage unit. Inside: " + green(bright("$150,000")) + " in cash.")
            self.change_balance(150000)
            print(PAR)
            type.type("Blood money. Does it matter? Money is money.")
            print(PAR)
            type.type("But you can't forget what he told you. You never will.")
            self.lose_sanity(25)
            self.add_status("Confessor's Burden")
        else:
            type.type(quote("I'm sorry. I can't."))
            print(PAR)
            type.type("His face falls. " + quote("Then it dies with me. All of it."))
            print(PAR)
            type.type("He walks away. You never see him again.")
            print(PAR)
            type.type("Part of you wonders what he would have said.")
            print(PAR)
            type.type("Most of you is glad you don't know.")
            self.restore_sanity(5)
        print(PAR)

        print(PAR)
        return
    def the_high_roller_suicide(self):
        # EVENT: Witness a high roller's complete breakdown and suicide
        # CONDITION: Balance >= $400,000 (you're in the high roller areas)
        # EFFECTS: Witness death, major sanity loss
        # MENTAL HEALTH: Witnessing suicide
        if self.get_balance() < 400000:
            self.day_event()
            return
        type.type("You head to the casino. In the high roller room, a man starts laughing. It's not a happy sound.")
        print(PAR)
        type.type("He's lost everything. EVERYTHING. His chips are gone. His marker is maxed.")
        print(PAR)
        type.type(quote("Twenty million. I lost TWENTY MILLION DOLLARS."))
        print(PAR)
        type.type("He's still laughing. Crying too. Security approaches carefully.")
        print(PAR)
        type.type(quote("My wife will leave me. My kids won't... they won't understand."))
        print(PAR)
        type.type("He pulls out a gun. Everyone screams. Dives for cover.")
        print(PAR)
        type.type("But he doesn't aim at anyone else.")
        print(PAR)
        type.type(quote("This is what gambling does. Remember that."))
        print(PAR)
        type.type(red(bright("BANG.")))
        print(PAR)
        type.type("The room goes silent. He falls. It's over that fast.")
        print(PAR)
        type.type("You can't move. Can't look away. His blood spreads across the green felt.")
        print(PAR)
        type.type("Security rushes in. Someone throws a jacket over him. The game is over.")
        print(PAR)
        type.type("But you can still hear the shot. You'll always hear the shot.")
        self.lose_sanity(40)
        self.add_status("Witnessed Suicide")
        print(PAR)

        print(PAR)
        return
    def the_anniversary_loss(self):
        # SECRET: Lost someone close - anniversary of their death
        if not self.has_status("Widowed") and not self.has_status("Lost Child"):
            self.day_event()
            return
        type.type("You sit up in your car. You immediately know what day it is.")
        print(PAR)
        type.type("The anniversary. One year since they died.")
        print(PAR)
        type.type("You try to distract yourself. Casino. Cards. Anything.")
        print(PAR)
        type.type("But you see their face everywhere. In strangers. In reflections.")
        print(PAR)
        type.type("By evening, you're crying in the parking lot. Alone. Always alone.")
        self.lose_sanity(20)
        print(PAR)

        print(PAR)
        return
    def survivor_guilt(self):
        # SECRET: Survived something others didn't
        if not self.has_status("Witnessed Death") and not self.has_status("Survivor's Resolve"):
            self.day_event()
            return
        type.type("You sit in your car and the faces come back. The ones who didn't make it.")
        print(PAR)
        type.type("Why you? Why did YOU survive when they didn't?")
        print(PAR)
        type.type("You don't deserve this. Any of this. The money, the life, any of it.")
        print(PAR)
        type.type("...But maybe that's why you keep gambling. Waiting to lose it all.")
        print(PAR)
        type.type("Waiting to get what you deserve.")
        self.lose_sanity(15)
        print(PAR)

        print(PAR)
        return
    def the_scar_story(self):
        # SECRET: Have a scar-related status - someone asks about it
        if not self.has_status("Missing Finger") and not self.has_status("Burn Scars") and not self.has_danger("Knife Wound"):
            self.day_event()
            return
        type.type("You step out of your car. A child points at your scars. " + quote("What happened to you?"))
        print(PAR)
        type.type("Their mother pulls them away, apologizing. But the damage is done.")
        print(PAR)
        type.type("What DID happen to you? How did you end up here? Scarred, gambling, living in a car?")
        print(PAR)
        type.type("You remember every wound. Every story. Every mistake.")
        print(PAR)
        type.type("The scars are just the ones you can see.")
        self.lose_sanity(8)
        print(PAR)

        print(PAR)
        return
    def the_winning_streak_paranoia(self):
        # SECRET: Won more than $100,000 in a single day
        if not hasattr(self, '_today_winnings') or self._today_winnings < 100000:
            self.day_event()
            return
        type.type("You're wide awake in your car. Too much adrenaline. Too much paranoia.")
        print(PAR)
        type.type("That's a lot of money. People kill for less.")
        print(PAR)
        type.type("Every noise is a threat. Every shadow is an enemy.")
        print(PAR)
        type.type("You clutch your cash like a lifeline. Eyes darting. Heart pounding.")
        print(PAR)
        type.type("Is that car following you? Was that footsteps?")
        print(PAR)
        type.type("Morning comes. You're exhausted but alive. Was anyone ever really after you?")
        print(PAR)
        type.type("Does it matter? The fear was real.")
        if self.has_item("Worry Stone"):
            print(PAR)
            type.type("You grip the " + cyan(bright("Worry Stone")) + " in your pocket. Thumb finds the groove. Round and round.")
            print(PAR)
            type.type("The panic doesn't vanish — but it shrinks. Manageable. You breathe.")
            self.lose_sanity(3)
            print(PAR)
            return
        self.lose_sanity(10)
        print(PAR)

        print(PAR)
        return
    def old_gambling_buddy(self):
        # SECRET: Day 200+ - run into someone from your past gambling life
        if self._day < 200:
            self.day_event()
            return
        type.type("You step out of your car when a voice calls your name. Your REAL name. One you haven't heard in months.")
        print(PAR)
        type.type("You turn and see a face from another life. An old gambling buddy.")
        print(PAR)
        type.type(quote("I can't believe it's you! We all thought you were dead! Or in prison!"))
        print(PAR)
        type.type("He looks good. Clean. Healthy. Normal.")
        print(PAR)
        type.type(quote("I quit, you know. Two years clean. Got a job, a family. Real life stuff."))
        print(PAR)
        type.type("He looks at you. At your car. At your clothes. At what you've become.")
        print(PAR)
        type.type(quote("Oh. You're still...") + " He trails off. The pity in his eyes is worse than any insult.")
        print(PAR)
        type.type(quote("Good luck, man. I hope you find your way out."))
        print(PAR)
        type.type("He walks away. Back to his normal life. You stay.")
        self.lose_sanity(15)
        print(PAR)

    # ==========================================
    # ==========================================
    # BRUTAL EVENTS - DEATH POSSIBLE
    # These events can result in player death. High risk, high stakes encounters.
    # ==========================================

        print(PAR)
        return
    def back_alley_shortcut(self):
        # EVENT: Mugged in a dark alley with three armed men
        # EFFECTS: Comply = lose $100-500 + 15 damage + 10 sanity; Run = escape or die; Fight = win or die
        # COMPANION INTEGRATION: danger_warning companions detect the ambush, protection companions fight
        # DEATH POSSIBLE - Mugging gone wrong

        if self.has_item("Guardian Angel"):
            type.type(cyan(bright("Guardian Angel")) + " activates. SOS fires, beacon screams, perimeter deploys. You are untouchable.")
            print(PAR)
            type.type("Sirens wail in the distance. Lights flood the alley. The muggers scatter like roaches.")
            self.restore_sanity(10)
            self.heal(10)
            print(PAR)
            return

        if self.has_item("Skeleton Key"):
            type.type("The " + cyan(bright("Skeleton Key")) + " doesn't just open locks. It opens possibilities.")
            print(PAR)
            type.type("A wall shifts. A door appears where there wasn't one. You step through into safety.")
            print(PAR)
            type.type("Behind the door: a hidden room. Someone's stash. You help yourself.")
            self.change_balance(random.randint(200, 600))
            self.restore_sanity(8)
            print(PAR)
            return

        # ── PLAYER CHOICE: multiple T2 items ──
        # When the player has several crafted items that could help,
        # let them choose their approach instead of auto-picking.
        _t2_options = [
            ("Master Key", "Pick the lock and slip away"),
            ("Fire Launcher", "Clear a path with fire"),
            ("Tear Gas", "Gas them and run"),
            ("Street Fighter Set", "Fight your way out"),
            ("Night Scope", "Use darkness to your advantage"),
            ("Intelligence Dossier", "Leverage what you know"),
            ("Surveillance Suite", "Counter their tech"),
            ("Mind Shield", "Resist their intimidation"),
            ("Fate Reader", "Foresee the danger"),
            ("Cheater's Insurance", "Turn their evidence against them"),
            ("Rolling Fortress", "Retreat to your car"),
            ("Lucid Dreaming Kit", "Negotiate better terms"),
        ]
        _available = [(n, d) for n, d in _t2_options if self.has_item(n)]
        if len(_available) >= 2:
            _chosen = self._offer_item_choice(_available)
            if _chosen == "Master Key":
                type.type("The " + magenta(bright("Master Key")) + " opens anything. Doors. Safes. Cuffs. Vaults. Click.")
                print(PAR)
                type.type("You find the maintenance door, unlock it, slip through before anyone reacts. You're gone.")
                self.restore_sanity(5)
                print(PAR)
                return
            elif _chosen == "Fire Launcher":
                type.type("The " + magenta(bright("Fire Launcher")) + " hurls burning projectiles. The fence line becomes a wall of fire.")
                print(PAR)
                type.type("Area denied. Nobody crosses that line.")
                self.use_item("Fire Launcher")
                self.restore_sanity(5)
                print(PAR)
                return
            elif _chosen == "Tear Gas":
                type.type("One " + magenta(bright("Tear Gas")) + " canister clears the street. Eyes streaming, lungs burning. They scatter.")
                print(PAR)
                self.use_item("Tear Gas")
                self.restore_sanity(5)
                print(PAR)
                return
            elif _chosen == "Street Fighter Set":
                type.type(magenta(bright("Street Fighter Set")) + " — blade and bruise. The fight ends before the other guy processes what happened.")
                print(PAR)
                type.type("Instant win.")
                self.restore_sanity(5)
                print(PAR)
                return
            elif _chosen == "Night Scope":
                type.type("The " + magenta(bright("Night Scope")) + " pierces the abandoned building's darkness. You see them before they see you.")
                print(PAR)
                type.type("Stealth advantage. You slip away unseen.")
                self.restore_sanity(5)
                print(PAR)
                return
            elif _chosen == "Intelligence Dossier":
                type.type("The " + magenta(bright("Intelligence Dossier")) + " has everything. Photos, records, secrets. You own this person.")
                print(PAR)
                type.type("They back off the moment you mention what you know.")
                self.restore_sanity(5)
                print(PAR)
                return
            elif _chosen == "Surveillance Suite":
                type.type("The " + magenta(bright("Surveillance Suite")) + " detects their bugs and kills their signal. You're clean.")
                print(PAR)
                type.type("Counter-surveillance complete. They never see you coming.")
                self.restore_sanity(5)
                print(PAR)
                return
            elif _chosen == "Mind Shield":
                type.type("The " + magenta(bright("Mind Shield")) + " deflects the horror. Your mind is a fortress.")
                print(PAR)
                type.type("They try to intimidate you. It doesn't work.")
                self.restore_sanity(8)
                print(PAR)
                return
            elif _chosen == "Fate Reader":
                type.type("The " + magenta(bright("Fate Reader")) + " warns of danger ahead. You change course. The danger passes.")
                print(PAR)
                self.restore_sanity(5)
                print(PAR)
                return
            elif _chosen == "Cheater's Insurance":
                type.type("You cheated them. They caught you. Then you show the evidence from your " + magenta(bright("Cheater's Insurance")) + ".")
                print(PAR)
                type.type("Mutual destruction assured. They let you go.")
                self.restore_sanity(5)
                print(PAR)
                return
            elif _chosen == "Rolling Fortress":
                type.type("The " + magenta(bright("Rolling Fortress")) + " is impenetrable. Car theft? Chase? Not tonight.")
                print(PAR)
                type.type("They try the doors. Nothing. They try the windows. Nothing. They leave.")
                self.restore_sanity(8)
                print(PAR)
                return
            elif _chosen == "Lucid Dreaming Kit":
                type.type("Under the blood moon, the " + magenta(bright("Lucid Dreaming Kit")) + " lets you negotiate with the dream. Better terms.")
                print(PAR)
                self.restore_sanity(5)
                print(PAR)
                return

        # Single T2 item — auto-triggers (no choice needed)
        if self.has_item("Master Key"):
            type.type("The " + magenta(bright("Master Key")) + " opens anything. Doors. Safes. Cuffs. Vaults. Click.")
            print(PAR)
            type.type("You find the maintenance door, unlock it, slip through before anyone reacts. You're gone.")
            print(PAR)
            self.restore_sanity(5)
            print(PAR)
            return

        if self.has_item("Fire Launcher"):
            type.type("The " + magenta(bright("Fire Launcher")) + " hurls burning projectiles. The fence line becomes a wall of fire.")
            print(PAR)
            type.type("Area denied. Nobody crosses that line.")
            self.use_item("Fire Launcher")
            self.restore_sanity(5)
            print(PAR)
            return

        if self.has_item("Tear Gas"):
            type.type("One " + magenta(bright("Tear Gas")) + " canister clears the street. Eyes streaming, lungs burning. They scatter.")
            print(PAR)
            self.use_item("Tear Gas")
            self.restore_sanity(5)
            print(PAR)
            return

        if self.has_item("Street Fighter Set"):
            type.type(magenta(bright("Street Fighter Set")) + " — blade and bruise. The fight ends before the other guy processes what happened.")
            print(PAR)
            type.type("Instant win.")
            self.restore_sanity(5)
            print(PAR)
            return

        if self.has_item("Night Scope"):
            type.type("The " + magenta(bright("Night Scope")) + " pierces the abandoned building's darkness. You see them before they see you.")
            print(PAR)
            type.type("Stealth advantage. You slip away unseen.")
            self.restore_sanity(5)
            print(PAR)
            return

        if self.has_item("Intelligence Dossier"):
            type.type("The " + magenta(bright("Intelligence Dossier")) + " has everything. Photos, records, secrets. You own this person.")
            print(PAR)
            type.type("They back off the moment you mention what you know.")
            self.restore_sanity(5)
            print(PAR)
            return

        if self.has_item("Surveillance Suite"):
            type.type("The " + magenta(bright("Surveillance Suite")) + " detects their bugs and kills their signal. You're clean.")
            print(PAR)
            type.type("Counter-surveillance complete. They never see you coming.")
            self.restore_sanity(5)
            print(PAR)
            return

        if self.has_item("Mind Shield"):
            type.type("The " + magenta(bright("Mind Shield")) + " deflects the horror. Your mind is a fortress.")
            print(PAR)
            type.type("They try to intimidate you. It doesn't work.")
            self.restore_sanity(8)
            print(PAR)
            return

        if self.has_item("Fate Reader"):
            type.type("The " + magenta(bright("Fate Reader")) + " warns of danger ahead. You change course. The danger passes.")
            print(PAR)
            self.restore_sanity(5)
            print(PAR)
            return

        if self.has_item("Cheater's Insurance"):
            type.type("You cheated them. They caught you. Then you show the evidence from your " + magenta(bright("Cheater's Insurance")) + ".")
            print(PAR)
            type.type("Mutual destruction assured. They let you go.")
            self.restore_sanity(5)
            print(PAR)
            return

        if self.has_item("Rolling Fortress"):
            type.type("The " + magenta(bright("Rolling Fortress")) + " is impenetrable. Car theft? Chase? Not tonight.")
            print(PAR)
            type.type("They try the doors. Nothing. They try the windows. Nothing. They leave.")
            self.restore_sanity(8)
            print(PAR)
            return

        if self.has_item("Lucid Dreaming Kit"):
            type.type("Under the blood moon, the " + magenta(bright("Lucid Dreaming Kit")) + " lets you negotiate with the dream. Better terms.")
            print(PAR)
            self.restore_sanity(5)
            print(PAR)
            return

        # COMBO: Forged Documents + Kingpin Look = The Federal Agent
        if self.has_item("Forged Documents") and self.has_item("Kingpin Look"):
            type.type("FORGED DOCUMENTS that say FBI. " + cyan(bright("Kingpin Look")) + " that says 'believe me.' You flash the badge. " + quote("Federal investigation. Everyone out."))
            print(PAR)
            type.type("The criminals run. For ten minutes, you ARE the law.")
            print(PAR)
            if random.randrange(5) == 0:
                type.type("A real federal agent double-takes at your badge.")
                print(PAR)
                type.type(quote("Sir, that's a crayon drawing on a napkin."))
                print(PAR)
                self.add_danger("Impersonating Fed")
                type.type("You run. You run hard.")
                self.change_balance(-100)
            else:
                self.change_balance(300)
                type.type("You pocket $300 in confiscated 'evidence' and walk away clean.")
            print(PAR)
            return

        if self.has_item("Improvised Trap"):
            type.type("You set your " + cyan(bright("Improvised Trap")) + " at the alley entrance before entering.")
            print(PAR)
            type.type("CLANG-CLANG-CLANG! The cans rattle violently as three figures trigger it.")
            print(PAR)
            type.type("They freeze, surprised. You have seconds to react.")
            print(PAR)
            type.type("You turn and run back the way you came. They shout but don't pursue — too confused by the noise.")
            print(PAR)
            type.type("Close call. The trap bought you time to escape.")
            self.restore_sanity(5)
            print(PAR)
            return

        # COMBO: Scrap Armor + Road Flare Torch = Blazing Knight
        if self.has_item("Scrap Armor") and self.has_item("Road Flare Torch"):
            type.type("You light the " + cyan(bright("Road Flare Torch")) + " and hold it high. The " + cyan(bright("Scrap Armor")) + " catches the flickering red glow.")
            print(PAR)
            type.type("You look like a knight who crawled out of a junkyard bonfire. The muggers take one look and decide they have somewhere else to be.")
            print(PAR)
            type.type("Nobody fights the burning man in homemade plate mail. Nobody.")
            self.use_item("Road Flare Torch")
            self.restore_sanity(10)
            print(PAR)
            return

        # COMBO: Shiv + Scrap Armor = Armed and Armored
        if self.has_item("Shiv") and self.has_item("Scrap Armor"):
            type.type("Blade in one hand. " + cyan(bright("Scrap Armor")) + " covering your vitals. The " + cyan(bright("Shiv")) + " catches the streetlight.")
            print(PAR)
            type.type("The three men reassess the situation. You're armed. You're armored. You're not afraid.")
            print(PAR)
            type.type(quote("Not worth it,") + " the leader mutters. They melt back into the darkness.")
            self.restore_sanity(8)
            print(PAR)
            return

        if self.has_item("Worn Gloves") or self.has_item("Velvet Gloves"):
            gloves = "Velvet Gloves" if self.has_item("Velvet Gloves") else "Worn Gloves"
            type.type("Gloved fingers leave no prints. The " + cyan(bright(gloves)) + " ensure your touch is invisible.")
            print(PAR)
            type.type(quote("Nothing here links you to anything,") + " the detective admits.")
            self.restore_sanity(5)
            print(PAR)
            return

        if self.has_item("Flask of Second Chance"):
            self.use_item("Flask of Second Chance")
            type.type("The alley goes wrong. Footsteps behind you. Knife ahead. Then time stutters.")
            print(PAR)
            type.type("You feel the " + cyan(bright("Flask of Second Chance")) + " crack in your pocket and the moment rewinds one breath.")
            print(PAR)
            type.type("Now you already know where they are. You take the side gate before the ambush closes and vanish into traffic.")
            self.restore_sanity(6)
            print(PAR)
            return

        # COMPANION: Danger warning check (Whiskers, Slick)
        warner = self._lists.has_companion_with_bonus(self, "danger_warning")
        if warner and self.get_companion(warner)["status"] == "alive":
            type.type("You're about to take a shortcut through a dark alley when " + bright(warner) + " goes absolutely crazy.")
            print(PAR)
            if "Cat" in self.get_companion(warner).get("type", ""):
                type.type(warner + " arches their back and hisses at the alley entrance. Ears flat. Tail puffed.")
            elif "Rat" in self.get_companion(warner).get("type", ""):
                type.type(warner + " starts squeaking frantically, biting your collar, pulling you backward.")
            else:
                type.type(warner + " makes alarmed sounds, physically trying to stop you from entering.")
            print(PAR)
            type.type("You hesitate. Peer into the darkness. And you see them.")
            print(PAR)
            type.type("Three figures. Waiting. One has something that catches the streetlight. A knife.")
            print(PAR)
            type.type("You back away slowly. They don't see you. " + warner + " just saved you from a mugging.")
            print(PAR)
            type.type(green(warner + "'s danger sense kicked in! Ambush avoided!"))
            self.restore_sanity(5)
            self.pet_companion(warner)
            print(PAR)
            return
        
        # ITEM: Tattered Cloak / Invisible Cloak - slip through unseen
        if self.has_item("Tattered Cloak") or self.has_item("Invisible Cloak"):
            cloak = "Tattered Cloak" if self.has_item("Tattered Cloak") else "Invisible Cloak"
            type.type("You step into the alley and pull the " + cyan(bright(cloak)) + " tight.")
            print(PAR)
            type.type("Halfway through, three shapes materialize from the shadows. Hoodies. A knife. They're scanning the darkness for a target.")
            print(PAR)
            type.type("Their eyes slide right past you. " + quote("Where'd he go?") + " one mutters.")
            print(PAR)
            type.type("You walk out the far end without making a sound. They never saw you. You exist in a frequency they can't tune to.")
            self.restore_sanity(8)
            print(PAR)
            return

        # ITEM: Gentleman's Charm - defuse the situation with impossible charisma
        if self.has_item("Gentleman's Charm"):
            type.type("You step into the alley. Three men materialize from the darkness. Knives. Hoodies. The full package.")
            print(PAR)
            type.type("You straighten your collar and walk toward them.")
            print(PAR)
            type.type(quote("Gentlemen. Rough night?"))
            print(PAR)
            type.type("There's a long silence. The lead mugger opens his mouth. Closes it.")
            print(PAR)
            type.type("You smile. Something about the smile — the cufflinks, the bearing, the sheer absurd confidence — short-circuits their entire plan.")
            print(PAR)
            type.type(quote("We, uh... thought you were someone else."))
            print(PAR)
            type.type("They step aside. You walk through.")
            print(PAR)
            type.type("You're almost at the far end when you hear one of them mutter: " + quote("Who WAS that?"))
            self.restore_sanity(6)
            print(PAR)
            return

        # ITEM: Assassin's Kit - total threat nullification
        if self.has_item("Assassin's Kit"):
            type.type("You step into the alley. Three shapes close in from the shadows.")
            print(PAR)
            type.type("Your hand moves once. Barely.")
            print(PAR)
            type.type("The lead mugger freezes mid-step, staring at the thing you're holding. His friends see it too.")
            print(PAR)
            type.type("Nobody says a word. Nobody has to.")
            print(PAR)
            type.type("They back away slowly. Then they turn and walk very quickly in the other direction.")
            print(PAR)
            type.type("You pocket the " + cyan(bright("Assassin's Kit")) + " and continue through. Thirty seconds, start to finish.")
            self.restore_sanity(10)
            print(PAR)
            return

        if self.has_item("Pepper Spray"):
            type.type("You step into the alley. Three shapes close in from the shadows.")
            print(PAR)
            type.type("You whip out the " + cyan(bright("Pepper Spray")) + " and give them a wide blast before they can react.")
            print(PAR)
            type.type("Screams echo off the walls. Eyes clawing. Stumbling blindly. You slip past while they're incapacitated.")
            print(PAR)
            type.type("The alley is yours. The spray is spent, but you're safe.")
            self.use_item("Pepper Spray")
            self.restore_sanity(7)
            print(PAR)
            return

        # ITEM: Necronomicon - dark entities give you safe passage
        if self.has_item("Necronomicon"):
            self._necronomicon_readings += 1
            type.type("You step into the alley clutching the " + cyan(bright("Necronomicon")) + ".")
            print(PAR)
            type.type("The muggers emerge from the shadows — and stop. Something about you. Something wrong. Something they can't name.")
            print(PAR)
            type.type("They back away from the book like it's a loaded gun aimed at their souls.")
            print(PAR)
            type.type("You walk through the alley alone. The book is warm in your hands.")
            self.restore_sanity(2)
            print(PAR)
            return

        # ITEM: Running Shoes - outrun the ambush entirely
        if self.has_item("Running Shoes"):
            type.type("You start down the alley. Halfway through, you clock them — three figures peeling from the shadows. Hoodies. A knife.")
            print(PAR)
            type.type("Your " + cyan(bright("Running Shoes")) + " grip the pavement before your brain finishes the thought.")
            print(PAR)
            type.type("You are already gone. Full sprint. The walls blur. They shout. They don't even get close.")
            print(PAR)
            type.type("You burst onto the street, lungs burning, still counting your fingers. All present. All correct.")
            self.restore_sanity(6)
            print(PAR)
            return

        # ITEM: Quiet Sneakers / Quiet Bunny Slippers - avoid the ambush by never being heard
        if self.has_item("Quiet Sneakers") or self.has_item("Quiet Bunny Slippers"):
            shoes = "Quiet Bunny Slippers" if self.has_item("Quiet Bunny Slippers") else "Quiet Sneakers"
            type.type("You hear the first scuff of a shoe behind you and stop moving entirely.")
            print(PAR)
            type.type("With the " + cyan(bright(shoes)) + ", your next step makes no sound at all.")
            print(PAR)
            if shoes == "Quiet Bunny Slippers":
                type.type("You drift to the side of the alley like a soft rumor. Three men pass within arm's length and never register you.")
                self.restore_sanity(8)
            else:
                type.type("You pivot into a recessed doorway, then slip out through a service gate before the muggers find your last position.")
                self.restore_sanity(5)
            self.update_quiet_sneakers_durability()
            print(PAR)
            return

        # ITEM: Miracle Lube - silence every hinge, ghost through unseen
        if self.has_item("Miracle Lube"):
            type.type("You step into the alley and pause at the old chain-link gate halfway through. It would screech loud enough to wake the block.")
            print(PAR)
            type.type("A drop of " + cyan(bright("Miracle Lube")) + " on each hinge. You open the gate in absolute silence. You open a door at the far end in absolute silence.")
            print(PAR)
            type.type("Three figures materialize from the shadows behind you. They heard nothing. They see nothing. You exit the alley in perfect silence, a ghost in a city that never knew you passed through.")
            self.restore_sanity(7)
            print(PAR)
            return

        if self.has_item("Smelling Salts"):
            type.type("You step into the alley. Halfway through, three shapes materialize. Hoodies. A knife.")
            print(PAR)
            type.type("One of them cracks you in the back of the head. Your vision goes dark. You start to fall.")
            print(PAR)
            type.type("But the " + cyan(bright("Smelling Salts")) + " in your pocket crack on impact. The ammonia jolt hits your brain like lightning.")
            print(PAR)
            type.type("Your eyes snap open. You're on the ground but AWAKE. You roll, scramble, sprint.")
            print(PAR)
            type.type("They didn't expect you to get up. By the time they react, you're gone.")
            self.hurt(8)
            self.restore_sanity(3)
            print(PAR)
            return

        # ITEM: Low-Profile Outfit - mistaken identity turns emotional
        if self.has_item("Low-Profile Outfit"):
            type.type("You step into the alley. Halfway through, three shapes materialize. Hoodies. A knife.")
            print(PAR)
            type.type("The mugger looks at your " + cyan(bright("Low-Profile Outfit")) + ". Pauses. 'Marcus? Holy crap, Marcus? It's me, Danny from juvie!'")
            print(PAR)
            type.type("He thinks you're someone he knows. He puts the knife away and starts CRYING. 'I thought you were dead, man.'")
            print(PAR)
            answer = ask.option("What do you do? ", ["Play along as Marcus", "Admit you're not Marcus", "Hug him silently"])
            print(PAR)
            if answer == "Play along as Marcus":
                type.type("You nod solemnly. 'Danny. Been a long time.' He gives you $30 and a phone number. 'Call me. We gotta catch up.'")
                print(PAR)
                type.type("Danny becomes a contact who knows the criminal underworld. Future discounts on shady deals.")
                self.change_balance(30)
                self.add_danger("Criminal Contact")
                self.restore_sanity(5)
            elif answer == "Admit you're not Marcus":
                type.type("Danny's grief turns to rage. 'Who the hell are you?' He swings. You dodge and run.")
                print(PAR)
                type.type("He doesn't chase far. But he remembers your face.")
                self.hurt(5)
                self.add_danger("Angry Danny")
            else:  # Hug him silently
                type.type("You hug him. He sobs on your shoulder. Then gives you $30 and walks away happy.")
                self.change_balance(30)
                self.restore_sanity(8)
            print(PAR)
            return

        # ITEM: Beach Bum Disguise - tourists aren't worth mugging
        if self.has_item("Beach Bum Disguise"):
            type.type("You step into the alley in the " + cyan(bright("Beach Bum Disguise")) + ". Halfway through, three shapes materialize.")
            print(PAR)
            type.type("They look you up and down. Sunglasses. Cheap sunscreen. Poncho. 'Just a tourist,' one mutters.")
            print(PAR)
            type.type("They look for richer targets. You walk through untouched.")
            self.restore_sanity(6)
            print(PAR)
            return

        # ITEM: Stink Bomb - nuclear option against muggers
        if self.has_item("Stink Bomb"):
            type.type("You crack the " + cyan(bright("Stink Bomb")) + ". The mugger gags. You gag. EVERYONE gags.")
            print(PAR)
            type.type("A woman across the street vomits into her purse. A dog faints. The mugger drops his knife and crawls away.")
            print(PAR)
            type.type("The smell spreads. Police respond to a 'gas leak.' You're four blocks away before the air clears.")
            print(PAR)
            type.type("The knife is still on the ground.")
            self.restore_sanity(5)
            self.use_item("Stink Bomb")
            print(PAR)
            return

        type.type("You step out of your car and decide to take a shortcut through a dark alley. Faster than going around.")
        print(PAR)
        type.type("Halfway through, you hear footsteps behind you. Heavy. Fast. Getting closer.")
        print(PAR)
        type.type("You turn around. Three men. Hoodies pulled low. One has a knife that catches the streetlight.")
        print(PAR)
        type.type(quote("Wallet. Phone. Everything. Now."))
        print(PAR)
        answer = ask.option("What do you do? ", ["comply", "run", "fight"])
        print(PAR)
        if answer == "comply":
            stolen = min(self.get_balance(), random.randint(100, 500))
            type.type("You hand over everything. They rifle through your pockets, take what they want.")
            print(PAR)
            type.type("One of them punches you in the gut anyway. Just because he can.")
            print(PAR)
            type.type(quote("Stay down. Count to a hundred. Don't look at our faces."))
            print(PAR)
            type.type("You do what they say. When you finally look up, they're gone.")
            print(PAR)
            type.type("You lost " + red(bright("$" + str(int(stolen)))) + ".")
            self.change_balance(-stolen)
            self.hurt(15)
            self.lose_sanity(10)
        elif answer == "run":
            type.type("You bolt. Legs pumping. Heart screaming. The alley seems to stretch forever.")
            print(PAR)
            chance = random.randrange(10)
            if chance < 6:
                type.type("You burst onto the main street. People. Cars. Safety.")
                print(PAR)
                type.type("You don't stop running for three blocks. When you finally look back, no one's following.")
                print(PAR)
                type.type("Your lungs burn. Your hands shake. But you're alive. You're alive.")
                self.hurt(5)
                self.lose_sanity(8)
            elif chance < 9:
                type.type("You trip. Garbage bag. Your ankle twists and you go down hard.")
                print(PAR)
                type.type("They're on you in seconds. Kicks. Punches. The knife flashes.")
                print(PAR)
                type.type("You curl into a ball and take it. It feels like forever.")
                print(PAR)
                type.type("When they finally leave, you're bleeding from a gash on your arm. Your ribs scream.")
                stolen = min(self.get_balance(), random.randint(200, 800))
                type.type(" They took " + red(bright("$" + str(int(stolen)))) + ".")
                self.change_balance(-stolen)
                self.hurt(35)
                self.lose_sanity(15)
                self.add_danger("Knife Wound")
            else:
                type.type("You don't make it.")
                print(PAR)
                type.type("The knife catches you between the shoulder blades. You feel the cold before the pain.")
                print(PAR)
                type.type("Your legs stop working. The ground rushes up to meet you.")
                print(PAR)
                type.type("The last thing you see is the dirty concrete. The last thing you hear is their footsteps fading.")
                print(PAR)
                type.type("The last thing you think is: " + italic("I should have just given them the money."))
                print(PAR)
                self.kill("Stabbed in a back alley. Another body. Another statistic.")
                return
        else:  # fight
            # COMPANION: Protection check (Lucky)
            protector = self._lists.has_companion_with_bonus(self, "protection")
            if protector and self.get_companion(protector)["status"] == "alive":
                type.type("Something snaps inside you. And " + bright(protector) + " feels it too.")
                print(PAR)
                type.type(protector + " launches at the nearest mugger. Snarling. Biting. Three legs of fury.")
                print(PAR)
                type.type("The mugger screams. His buddies hesitate. You grab a trash can lid and swing.")
                print(PAR)
                type.type("Between you and " + protector + ", the three of them decide it's not worth it. They run.")
                print(PAR)
                type.type("You stand there, chest heaving. " + protector + " stands beside you, growling at the empty alley.")
                print(PAR)
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
            print(PAR)
            # ITEM: Brass Knuckles - instant deterrence, no fight needed
            if self.has_item("Brass Knuckles"):
                type.type("You raise your fist. The brass knuckles catch the streetlight at exactly the right angle.")
                print(PAR)
                type.type("The mugger looks at your hand, then at your face, then makes a quiet decision about his life goals.")
                print(PAR)
                type.type("He leaves. Fast. His friends follow.")
                print(PAR)
                type.type("You stand alone in the alley. Your fist is still raised.")
                self.restore_sanity(8)
                print(PAR)
                return
            type.type("You charge at them, screaming. Pure animal rage.")
            print(PAR)
            chance = random.randrange(10)
            if chance < 2:
                type.type("They weren't expecting that. The first one goes down when your fist connects with his nose.")
                print(PAR)
                type.type("Blood sprays. The other two hesitate. You grab a trash can lid and swing.")
                print(PAR)
                type.type("They run. They actually run. You stand there, chest heaving, covered in someone else's blood.")
                print(PAR)
                type.type("You won. Somehow. You have no idea how.")
                self.hurt(10)
                if self.has_item("Splint"):
                    type.type("Your wrist throbs from the punches. You reach for your " + cyan(bright("Splint")) + " and brace it tightly.")
                    print(PAR)
                    type.type("The support helps. The injury won't worsen.")
                    self.heal(5)
                    print(PAR)
                self.restore_sanity(5)  # Cathartic
            elif chance < 7:
                type.type("You get one good hit in. Then the knife finds your stomach.")
                print(PAR)
                type.type("It doesn't hurt at first. Just pressure. Then heat. Then agony.")
                print(PAR)
                type.type("You collapse. They take everything and run.")
                print(PAR)
                type.type("You drag yourself to the street, leaving a trail of blood. Someone calls an ambulance.")
                stolen = self.get_balance()
                self.change_balance(-stolen)
                self.hurt(60)
                if self.has_item("Wound Salve"):
                    type.type("Even as you drag yourself, you fumble for the " + cyan(bright("Wound Salve")) + ". You smear it over the wound.")
                    print(PAR)
                    type.type("The salve stings, then numbs. The bleeding slows. It won't fix this, but it helps.")
                    self.heal(15)
                    self.use_item("Wound Salve")
                    print(PAR)
                self.lose_sanity(20)
                self.add_danger("Gut Wound")
                if self.has_item("Health Indicator") or self.has_item("Health Manipulator"):
                    indicator = "Health Indicator" if self.has_item("Health Indicator") else "Health Manipulator"
                    type.type("The " + cyan(bright(indicator)) + " pulses at your wrist, flooding adrenaline into the wound site. The damage is real, but your body's response is extraordinary.")
                    print(PAR)
                    type.type("You'll live.")
                    self.heal(25)
            else:
                type.type("The knife goes into your throat before you can even swing.")
                print(PAR)
                type.type("You try to scream but it comes out as a gurgle. Blood. So much blood.")
                print(PAR)
                type.type("You fall. The world tilts. The stars above blur into smears of light.")
                print(PAR)
                type.type("Your last thought is that you never got to make your million.")
                print(PAR)
                if self.has_item("Phoenix Feather") or self.has_item("White Feather"):
                    feather = "Phoenix Feather" if self.has_item("Phoenix Feather") else "White Feather"
                    type.type("Then — warmth. A burst of amber light erupts from your pocket.")
                    print(PAR)
                    type.type("The " + cyan(bright(feather)) + " ignites. Heat floods through you like sunrise. The wound seals with a hiss.")
                    print(PAR)
                    type.type("You gasp and roll over. The muggers have fled — they saw the light and ran.")
                    print(PAR)
                    type.type("The feather is ash. But you are not.")
                    self.use_item(feather)
                    self.hurt(35)
                    self.lose_sanity(20)
                elif self.has_item("Flask of No Bust"):
                    self.use_item("Flask of No Bust")
                    type.type("Then — something shifts. A cold clarity cuts through the pain.")
                    print(PAR)
                    type.type("The " + cyan(bright("Flask of No Bust")) + " disagrees with death on your behalf.")
                    print(PAR)
                    type.type("Your body refuses to fail. The bleeding slows. Not enough to kill you. Not today.")
                    print(PAR)
                    type.type("You drag yourself to the street. Someone calls an ambulance.")
                    self.hurt(50)
                    self.lose_sanity(25)
                else:
                    self.kill("Bled out in an alley. The muggers split your cash three ways.")
                return
        print(PAR)

        print(PAR)
        return
    def gas_station_robbery(self):
        # EVENT: Caught in a gas station during an armed robbery
        # EFFECTS: Comply = potential hostage situation; Hide = escape or get caught; Hero = save day or die
        # COMPANION INTEGRATION: danger_warning companions give early warning, Slick finds escape route
        # DEATH POSSIBLE - Wrong place, wrong time
        
        # COMPANION: Danger warning check - avoid the situation entirely
        if self.has_item("Ghost Protocol"):
            type.type(cyan(bright("Ghost Protocol")) + " active. Cameras see nothing, records say nothing. You walk through the robbery scene as an invisible presence.")
            print(PAR)
            type.type("You're not here. You were never here. The robbers flee from... nothing.")
            self.restore_sanity(5)
            return
        if self.has_item("Road Warrior Armor"):
            type.type("The robbers look at the " + cyan(bright("Road Warrior Armor")) + ". They look at each other.")
            print(PAR)
            type.type("They leave. All of them. Without saying a word.")
            self.restore_sanity(8)
            return
        if self.has_item("All-Access Pass"):
            type.type("The " + cyan(bright("All-Access Pass")) + " identifies you as something official. The robbers scatter.")
            print(PAR)
            type.type("You're not a victim here — you're an authority.")
            self.restore_sanity(5)
            self.change_balance(200)
            return
        if self.has_item("Sneaky Peeky Goggles") or self.has_item("Sneaky Peeky Shades"):
            lenses = "Sneaky Peeky Goggles" if self.has_item("Sneaky Peeky Goggles") else "Sneaky Peeky Shades"
            type.type("Your " + cyan(bright(lenses)) + " catch a reflection — someone's crouching behind the counter with a weapon.")
            print(PAR)
            type.type("You quietly back out of the gas station before the situation unfolds. Crisis averted.")
            self.restore_sanity(5)
            print(PAR)
            return
        warner = self._lists.has_companion_with_bonus(self, "danger_warning")
        if warner and self.get_companion(warner)["status"] == "alive" and random.randrange(3) == 0:
            type.type("You're about to walk into the gas station when " + bright(warner) + " starts acting strange.")
            print(PAR)
            type.type("Agitated. Pulling at you. Refusing to let you go in.")
            print(PAR)
            type.type("You hesitate at the door. Then you hear it from inside: " + quote("EVERYBODY ON THE GROUND!"))
            print(PAR)
            type.type("Your blood goes cold. There's a robbery happening. Right now. Right where you almost walked in.")
            print(PAR)
            type.type("You back away slowly. Call 911 from the parking lot. The police handle it.")
            print(PAR)
            type.type(green(warner + " sensed the danger! You avoided the robbery entirely!"))
            self.pet_companion(warner)
            self.restore_sanity(5)
            print(PAR)
            return
        
        type.type("You drive your car to a gas station for supplies. Just snacks. Maybe some coffee.")
        print(PAR)
        type.type("You're browsing the chips when the door slams open.")
        print(PAR)
        type.type(quote("EVERYBODY ON THE GROUND! NOW!"))
        print(PAR)
        type.type("A man with a shotgun. Ski mask. Shaking hands. This is really happening.")
        print(PAR)
        type.type("The cashier freezes. A mother clutches her child. An old man drops his coffee.")
        print(PAR)
        type.type("The robber swings the gun around, wild-eyed.")
        print(PAR)
        if self.has_item("Marvin's Eye"):
            type.type(magenta(bright("Marvin's Eye")) + " sees the threads of fate unravel. The outcomes appear like ghost images:")
            print(PAR)
            type.type(magenta("  COMPLY: You live. He takes $50-200 from you. Nobody dies."))
            print(PAR)
            type.type(magenta("  HIDE: 50/50. Either clean escape or he finds you."))
            print(PAR)
            type.type(magenta("  HERO: High risk. Glory or the hospital."))
            print(PAR)
        answer = ask.option("What do you do? ", ["comply", "hide", "hero"])
        print(PAR)
        # COMBO: Forged Documents + Kingpin Look = The Federal Agent
        if self.has_item("Forged Documents") and self.has_item("Kingpin Look"):
            type.type("You reach into your jacket. The " + cyan(bright("Kingpin Look")) + " demands respect. The " + cyan(bright("Forged Documents")) + " say FBI.")
            print(PAR)
            type.type(quote("Federal investigation. Everyone out. NOW."))
            print(PAR)
            type.type("The robber freezes. The other customers run. The cashier ducks.")
            print(PAR)
            type.type("The robber drops the shotgun, turns, and sprints. You pocket $300 in 'confiscated evidence' from the counter.")
            self.change_balance(300)
            self.restore_sanity(15)
            print(PAR)
            return
        # ITEM: Forged Documents - flash fake credentials, walk out clean
        if self.has_item("Forged Documents"):
            type.type("You reach slowly into your pocket. The robber spins.")
            print(PAR)
            type.type(quote("HANDS WHERE I CAN SEE THEM!"))
            print(PAR)
            type.type("You hold up the " + cyan(bright("Forged Documents")) + ". Badge. Federal credentials. Everything laminated.")
            print(PAR)
            type.type(quote("Sir, I'm going to need you to lower the weapon. Quietly. Right now."))
            print(PAR)
            type.type("The robber stares. His hand shakes. Then he drops the gun, turns, and sprints out the back.")
            print(PAR)
            type.type("The cashier stares at you. The mother stares at you. The old man picks up his coffee.")
            print(PAR)
            type.type("You pocket the documents, nod once, and walk out before anyone starts asking questions.")
            self.restore_sanity(10)
            print(PAR)
            return
        if answer == "comply":
            type.type("You drop to the floor. Face down. Hands visible. Make yourself small.")
            print(PAR)
            type.type("The robber empties the register. Grabs cigarettes. His eyes keep darting to the door.")
            print(PAR)
            type.type("He's scared. That makes him dangerous.")
            print(PAR)
            chance = random.randrange(10)
            if chance < 8:
                type.type("Sirens in the distance. He panics. Runs. Gone.")
                print(PAR)
                type.type("You stay on the floor for a long time after. Just breathing. Just existing.")
                self.lose_sanity(12)
            else:
                type.type("He decides he needs a hostage. His hand grabs your collar.")
                print(PAR)
                type.type("You're dragged toward the door. The shotgun barrel is cold against your temple.")
                print(PAR)
                type.type("Outside. Police lights. He's screaming. They're screaming. Everyone's screaming.")
                print(PAR)
                chance2 = random.randrange(3)
                if chance2 == 0:
                    type.type("The sniper takes the shot. The robber's head snaps back.")
                    print(PAR)
                    type.type("His blood is in your mouth. On your face. You're screaming.")
                    print(PAR)
                    type.type("They pry you from his body. You can't stop shaking for hours.")
                    self.lose_sanity(30)
                    self.hurt(5)
                else:
                    type.type("His finger twitches. The gun goes off.")
                    print(PAR)
                    type.type("The world goes white. Then nothing.")
                    print(PAR)
                    self.kill("Wrong place. Wrong time. Hostage situation gone wrong.")
                    return
        elif answer == "hide":
            type.type("You duck behind a shelf. Slowly, carefully, you crawl toward the back.")
            print(PAR)
            type.type("The robber is focused on the register. You're almost to the storage room...")
            print(PAR)
            chance = random.randrange(10)
            if chance < 7:
                type.type("You make it. Hide behind boxes of toilet paper and canned goods.")
                print(PAR)
                type.type("You can hear everything. The shouting. The crying. The crash of the register hitting the floor.")
                print(PAR)
                type.type("Then sirens. Running footsteps. Silence.")
                print(PAR)
                type.type("The police find you an hour later, still hiding. Curled up like a child.")
                self.lose_sanity(15)
            else:
                type.type("A chip bag crinkles under your knee. The robber spins.")
                print(PAR)
                type.type(quote("I SEE YOU! GET OUT HERE!"))
                print(PAR)
                type.type("The shotgun is pointed right at you. You raise your hands and step out.")
                print(PAR)
                type.type(quote("Think you're smart? Think you can hide from me?"))
                print(PAR)
                type.type("He hits you with the stock. Your vision explodes into stars.")
                self.hurt(25)
                self.lose_sanity(15)
        else:  # hero
            type.type("There's a fire extinguisher on the wall. Three feet away. You could make it.")
            print(PAR)
            type.type("The robber's back is turned. Yelling at the cashier. Now or never.")
            print(PAR)
            chance = random.randrange(10)
            if chance < 3:
                type.type("You grab it. Swing. Connect with his skull. He goes down like a sack of meat.")
                print(PAR)
                type.type("The shotgun clatters to the floor. You kick it away. Stand over him, chest heaving.")
                print(PAR)
                type.type("The other customers stare at you like you're insane. Maybe you are.")
                print(PAR)
                type.type("The police call you a hero. The cashier gives you $100 from his own pocket.")
                self.change_balance(100)
                self.restore_sanity(10)
                self.meet("Gas Station Hero")
            elif chance < 7:
                type.type("He turns too fast. Sees you reaching. The shotgun comes up.")
                print(PAR)
                type.type("BANG.")
                print(PAR)
                type.type("The blast catches your shoulder. You spin. Hit the floor. The pain is unreal.")
                print(PAR)
                type.type("But you're alive. He runs. Sirens are close.")
                print(PAR)
                type.type("You'll never have full use of that arm again.")
                self.hurt(50)
                self.lose_sanity(20)
                self.add_danger("Shoulder Destroyed")
            else:
                type.type("You're too slow. Way too slow.")
                print(PAR)
                type.type("The shotgun blast takes you in the chest. The world goes red, then black.")
                print(PAR)
                type.type("You tried to be a hero. Heroes die young.")
                print(PAR)
                self.kill("Shot trying to stop a robbery. They put your picture on the news.")
                return
        print(PAR)

        print(PAR)
        return
    def carbon_monoxide(self):
        # EVENT: Carbon monoxide leak while sleeping in car
        # EFFECTS: First exposure always survives but adds "Damaged Exhaust"; repeat exposure can still kill
        # BRUTAL: Pushes the lethal risk into the follow-up exhaust chain instead of a one-off instant death spike
        type.type("A pounding headache. The worst you've ever had.")
        print(PAR)
        type.type("Your thoughts are sluggish. Thick. Like wading through mud.")
        print(PAR)
        type.type("Something's wrong. The car smells... off. Exhaust. How long have you been breathing this?")
        print(PAR)
        type.type("Your hands feel so far away. Moving them takes forever.")
        print(PAR)
        chance = random.randrange(10)
        repeat_exposure = self.has_danger("Damaged Exhaust")
        if chance < 5:
            type.type("Some survival instinct kicks in. You fumble for the door handle. Miss. Try again.")
            print(PAR)
            type.type("The door opens. Fresh air hits your face. You fall out onto the pavement.")
            print(PAR)
            type.type("You lay there, gasping, staring at the sky, for what feels like hours.")
            print(PAR)
            type.type("Your exhaust pipe has a hole. It's been leaking carbon monoxide into the car.")
            print(PAR)
            type.type("You almost died in your sleep. You almost didn't wake up at all.")
            self.hurt(30)
            self.lose_sanity(20)
            self.add_danger("Damaged Exhaust")
        elif chance < 8:
            type.type("You try to move but your body won't cooperate. Too tired. Just... so tired.")
            print(PAR)
            type.type("Maybe if you close your eyes for just a second...")
            print(PAR)
            type.type("...")
            print(PAR)
            type.type("A tap on the window. Muffled shouting. Someone's breaking the glass.")
            print(PAR)
            type.type("Fresh air. Screaming sirens. The inside of an ambulance.")
            print(PAR)
            type.type("The doctors say you were minutes away from brain damage. Or death.")
            self.hurt(45)
            self.lose_sanity(25)
            self.add_danger("Damaged Exhaust")
            if self.has_item("Real Insurance"):
                print(PAR)
                type.type("You manage to flash your " + cyan(bright("Real Insurance")) + " card before the oxygen mask goes on. Billing gets sorted before you can even panic about it.")
                print(PAR)
                type.type("No ambulance bill. No ER ambush. Just survival.")
                self.restore_sanity(8)
                self.update_faulty_insurance_durability()
            elif self.has_item("Faulty Insurance"):
                print(PAR)
                type.type("You hand over the " + magenta(bright("Faulty Insurance")) + " card with fingers that barely work. The paramedic squints at it, the admissions clerk shrugs, and somehow the moment passes without anyone pushing harder.")
                print(PAR)
                type.type("The bill still comes, but it's lighter than it should have been. Sometimes fake confidence really is a medical intervention.")
                reduced_bill = 150
                type.type("Hospital bill: " + red(bright("$150")) + ".")
                self.change_balance(-min(self.get_balance(), reduced_bill))
                self.update_faulty_insurance_durability()
            elif self.get_balance() >= 500:
                type.type("Hospital bill: " + red(bright("$500")) + ". They saved your life, so.")
                self.change_balance(-500)
        elif repeat_exposure:
            type.type("You're so tired. The headache is fading. Everything is fading.")
            print(PAR)
            type.type("This isn't so bad. Peaceful, almost. Like sinking into warm water.")
            print(PAR)
            type.type("Your eyes close. Your breathing slows. Your heart follows.")
            print(PAR)
            type.type("They find your body two days later. The car is still running.")
            print(PAR)
            self.kill("Carbon monoxide poisoning. They say it's painless. They hope it's painless.")
            return
        else:
            type.type("You black out halfway to the door and wake up sprawled across the front seat, windows fogged, lungs burning.")
            print(PAR)
            type.type("You cough hard enough to taste blood before you manage to kill the engine and crawl outside.")
            print(PAR)
            type.type("The exhaust is shot. If you sleep in here again without fixing it, you might not wake up.")
            self.hurt(25)
            self.lose_sanity(12)
            self.add_danger("Damaged Exhaust")
        print(PAR)

        print(PAR)
        return
    def drowning_dream(self):
        # EVENT: Surreal drowning nightmare that may become reality
        # BRUTAL: Dream-like sequence with potential death
        # DEATH POSSIBLE - Dream or reality?
        self.meet("Drowning Dream")
        type.type("Sitting in your car, your mind drifts. You dream of water. Dark water. Deep water. Rising water.")
        print(PAR)
        type.type("You're in a car—your car—and water is pouring in through every crack.")
        print(PAR)
        type.type("You can't open the doors. The pressure is too much. The windows won't break.")
        print(PAR)
        type.type("The water reaches your waist. Your chest. Your neck. Your mouth.")
        print(PAR)
        type.type("You scream but water fills your lungs instead of air.")
        print(PAR)
        type.type("...")
        print(PAR)
        chance = random.randrange(10)
        if chance < 7:
            type.type("You wake up GASPING. Clawing at your throat. Soaking wet with sweat.")
            print(PAR)
            type.type("Just a dream. Just a dream. Just a—")
            print(PAR)
            type.type("Your feet are wet. You look down.")
            print(PAR)
            type.type("Rain. It's raining. Water leaked through a crack in your window.")
            print(PAR)
            type.type("Just rain. You're fine. You're fine. You're fine.")
            self.lose_sanity(15)
            self.hurt(5)
        elif chance < 9:
            type.type("You wake up underwater.")
            print(PAR)
            type.type("THIS ISN'T A DREAM. Your car is IN THE RIVER. You must have rolled down the embankment while sleeping.")
            print(PAR)
            type.type("The water is at your waist. Rising fast. You fumble for the window crank.")
            print(PAR)
            type.type("It's stuck. You slam your elbow against the glass. Again. Again. AGAIN.")
            print(PAR)
            type.type("It cracks. Shatters. Water rushes in but you have an opening.")
            print(PAR)
            type.type("You squeeze through, cutting yourself on the glass, and kick toward the surface.")
            print(PAR)
            type.type("Air. Sweet, precious air. You drag yourself onto the bank and collapse.")
            print(PAR)
            type.type("By morning, the wagon is a drowned wreck-half-sunk, flooded through, and useless as transportation.")
            print(PAR)
            type.type("You can salvage your life, but not your ride. Most of what you kept inside is ruined or swept away. But you're alive.")
            self.hurt(40)
            self.lose_sanity(25)
            self.remove_item("Car")
            lost = self.get_balance() * 0.3
            self.change_balance(-lost)
        else:
            if self.has_item("Distress Beacon"):
                type.type("In your final moment, you activate the " + cyan(bright("Distress Beacon")) + ". A piercing signal cuts through the night.")
                print(PAR)
                type.type("Help arrives just in time. Fishermen pull you from the wreck, gasping but alive.")
                print(PAR)
                type.type("You're down to 1 HP, but breathing. The beacon saved you.")
                self.use_item("Distress Beacon")
                self.set_health(1)
                self.lose_sanity(30)
                self.remove_item("Car")
                lost = self.get_balance() * 0.3
                self.change_balance(-lost)
                return
            type.type("You never wake up.")
            print(PAR)
            type.type("The car rolled into the river while you slept. By the time the water woke you, it was too late.")
            print(PAR)
            type.type("You fight. God, how you fight. But the doors won't open and the windows won't break.")
            print(PAR)
            type.type("Your last breath comes as a desperate gasp. Water fills the void.")
            print(PAR)
            type.type("They find the car three days later. Your hands are still on the door handle.")
            print(PAR)
            self.kill("Drowned in your car. Some nightmares are real.")
            return
        print(PAR)

        print(PAR)
        return
    def heart_attack_scare(self):
        # EVENT: Stress-induced cardiac event while walking to casino
        # EFFECTS: 50% panic attack (15 dmg + 20 sanity + $300); 30% mild heart attack (40 dmg + "Heart Condition" + $2000); 20% death
        # BRUTAL: Can result in instant death from massive heart attack
        # DEATH POSSIBLE - The stress catches up
        type.type("You step out of your car and head toward the casino when it hits. Pain. Crushing pain in your chest.")
        print(PAR)
        type.type("You can't breathe. Your left arm is tingling. Your vision is going gray at the edges.")
        print(PAR)
        type.type("This is it. This is how it ends. Not at the table. In a parking lot.")
        print(PAR)
        type.type("You collapse against your car. Hand clutching your chest. People are staring.")
        print(PAR)
        chance = random.randrange(10)
        if chance < 5:
            type.type("Someone calls 911. Paramedics. Hospital. Tests.")
            print(PAR)
            type.type("It wasn't a heart attack. Panic attack. Severe anxiety. Stress.")
            print(PAR)
            type.type("The doctor looks at you with something like pity.")
            print(PAR)
            type.type(quote("Sir, if you keep living like this, next time it WILL be a heart attack."))
            print(PAR)
            type.type("He gives you pills. You can't afford to fill the prescription.")
            self.hurt(15)
            self.lose_sanity(20)
            if self.get_balance() >= 300:
                type.type("ER visit: " + red(bright("$300")) + ".")
                self.change_balance(-300)
        elif chance < 8:
            type.type("It IS a heart attack. A mild one, they say. Like that's supposed to be comforting.")
            print(PAR)
            type.type("You spend three days in the hospital. They put a stent in your artery.")
            print(PAR)
            type.type("The doctor tells you to change your lifestyle. Eat better. Stress less. Exercise.")
            print(PAR)
            type.type("You're a homeless gambling addict. Lifestyle changes aren't really an option.")
            self.hurt(40)
            self.lose_sanity(25)
            self.add_danger("Heart Condition")
            if self.get_balance() >= 2000:
                type.type("Hospital bill: " + red(bright("$2000")) + ". Worth it to be alive, you guess.")
                self.change_balance(-2000)
        else:
            type.type("It's a heart attack. A big one. The kind that kills people.")
            print(PAR)
            type.type("You try to call for help but no sound comes out. Your body won't cooperate.")
            print(PAR)
            type.type("People walk past. They think you're drunk. Or crazy. They don't stop.")
            print(PAR)
            type.type("The world gets very small. Just you and the pain and the fading light.")
            print(PAR)
            type.type("Your last thought is about cards. You were so close. So close.")
            print(PAR)
            self.kill("Heart attack. The stress finally won. The house always wins.")
            return
        print(PAR)

        print(PAR)
        return
    def drug_dealer_encounter(self):
        # EVENT: Drug dealers mistake you for a buyer/informant
        # EFFECTS: Various - can buy cocaine ($500), get beaten (15-45 damage), or shot and killed
        # BRUTAL: Running has high death chance; can acquire "Bag of Cocaine" item
        # DEATH POSSIBLE - Wrong crowd

        # COMBO: New Identity + Blackmail Letter = The Disappearing Act
        if self.has_item("New Identity") and self.has_item("Blackmail Letter"):
            type.type("Step one: the " + cyan(bright("New Identity")) + " erases who you were.")
            print(PAR)
            type.type("Step two: the " + cyan(bright("Blackmail Letter")) + " ensures anyone who remembers stays quiet.")
            print(PAR)
            type.type("You don't just disappear — you disappear retroactively. The wanted poster comes down.")
            print(PAR)
            for danger_name in ["Casino Heat", "Police Heat", "Criminal Heat", "Impersonating Fed"]:
                if self.has_danger(danger_name):
                    self.lose_danger(danger_name)
            self.add_status("Ghost")
            self.restore_sanity(10)
            return

        type.type("A car pulls up next to you. Windows tinted black. Engine rumbling.")
        print(PAR)
        type.type("The window rolls down. A face stares out. Cold eyes. Gold teeth.")
        print(PAR)
        type.type(quote("You the one been asking around? Looking for... product?"))
        print(PAR)
        type.type("You haven't been asking around. This is a case of mistaken identity.")
        print(PAR)
        if self.has_item("Enchanted Vintage"):
            type.type("Before you can open your mouth to explain, you reach into your bag. Your hand finds the " + cyan(bright("Enchanted Vintage")) + " before your brain does.")
            print(PAR)
            type.type("You offer it through the window. Against all reason, he takes it. Takes a sip.")
            print(PAR)
            type.type("A long pause. His expression shifts — the cold anger dissolving into something genuinely confused and peaceful.")
            print(PAR)
            type.type(quote("I don't... I don't know why I was upset.") + " He hands the bottle back. " + quote("Drive safe, man."))
            print(PAR)
            type.type("The window rolls up. The car pulls away. The Enchanted Vintage is gone but you're alive and intact.")
            self.use_item("Enchanted Vintage")
            self.restore_sanity(5)
            print(PAR)
            return
        answer = ask.option("What do you say? ", ["wrong person", "play along", "run"])
        print(PAR)
        if answer == "wrong person":
            type.type(quote("I think you've got the wrong guy. I don't—"))
            print(PAR)
            type.type("He cuts you off. " + quote("Don't play dumb. Marcus said you was looking."))
            print(PAR)
            type.type("You don't know any Marcus. Your heart is pounding.")
            print(PAR)
            chance = random.randrange(10)
            if chance < 6:
                type.type(quote("Nah, this ain't him.") + " The passenger leans over, squinting. " + quote("Wrong car. My bad."))
                print(PAR)
                type.type("The window rolls up. The car drives away. You nearly collapse with relief.")
                self.lose_sanity(10)
            else:
                type.type("He doesn't believe you. Door opens. He gets out. He's holding something metal.")
                print(PAR)
                type.type(quote("You talked to the cops, didn't you? You a snitch?"))
                print(PAR)
                type.type("Before you can answer, his fist connects with your face. Then again. Then the metal thing—a pipe.")
                print(PAR)
                type.type("You go down. They beat you until you stop moving. Take your wallet. Leave you bleeding.")
                self.hurt(45)
                self.lose_sanity(20)
                stolen = min(self.get_balance(), random.randint(200, 500))
                self.change_balance(-stolen)
        elif answer == "play along":
            type.type("Some insane survival instinct kicks in. You play along.")
            print(PAR)
            type.type(quote("Yeah, that's me. What you got?"))
            print(PAR)
            type.type("He grins. Shows you a bag of white powder. Wants $500.")
            print(PAR)
            if self.get_balance() >= 500:
                answer2 = ask.yes_or_no("Buy the drugs? ($500) ")
                if answer2 == "yes":
                    type.type("You hand over the money. Take the bag. The car drives away.")
                    print(PAR)
                    type.type("You're holding cocaine. What the hell are you supposed to do with cocaine?")
                    print(PAR)
                    self.change_balance(-500)
                    self.add_item("Bag of Cocaine")
                else:
                    type.type(quote("Actually, I'm good. Changed my mind."))
                    print(PAR)
                    type.type("His face hardens. " + quote("You wasting my time?"))
                    print(PAR)
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
                print(PAR)
                type.type(quote("Then why you wastin' my time?"))
                print(PAR)
                type.type("He slaps you across the face and drives off. You got off easy.")
                self.hurt(5)
                self.lose_sanity(10)
        else:  # run
            type.type("You turn and bolt. Stupid. So stupid. But instinct takes over.")
            print(PAR)
            type.type("Behind you, car doors open. Footsteps. Shouting.")
            print(PAR)
            
            if self.has_item("Running Shoes"):
                type.type("Your " + cyan(bright("Running Shoes")) + " catch traction with every stride. Your body remembers how to move fast.")
                print(PAR)
                type.type("The dealers shout behind you, but the gap widens. You're not slowing down. You're ACCELERATING.")
                print(PAR)
                type.type("They get back in the car. You cut through an alley. They try to follow. You vault a fence. The car can't.")
                print(PAR)
                type.type("When you finally stop running, your legs are burning but your heart is still alive. Your heart is very, very alive.")
                self.hurt(3)
                self.restore_sanity(5)
                print(PAR)
                return
            
            if self.has_item("Tire Ready Kit"):
                type.type("They get back in the car. Tires squeal. They're coming for you.")
                print(PAR)
                type.type("You grab the spare tire from your " + cyan(bright("Tire Ready Kit")) + " and hurl it at the windshield mid-stride.")
                print(PAR)
                type.type("It bounces off the pavement, clips the hood, smashes through the glass. The car swerves hard and buries itself in a ditch.")
                print(PAR)
                type.type("You don't stop running for six blocks. But you make it. Every part of you makes it.")
                self.restore_sanity(4)
                print(PAR)
                return
            chance = random.randrange(10)
            if chance < 4:
                type.type("You're faster than you thought. Or they're lazier than expected.")
                print(PAR)
                type.type("You cut through an alley, over a fence, through someone's yard.")
                print(PAR)
                type.type("When you finally stop running, you're lost. But alive. Definitely alive.")
                self.hurt(5)
                self.lose_sanity(12)
            elif chance < 8:
                type.type("They catch you in thirty seconds. You're not fast. You're not young.")
                print(PAR)
                type.type("The beating is methodical. Professional. They know how to hurt without killing.")
                print(PAR)
                type.type("When they leave, you crawl to a gas station and call for help.")
                self.hurt(40)
                self.lose_sanity(20)
                stolen = self.get_balance()
                self.change_balance(-stolen)
            else:
                type.type("You hear the gunshot before you feel it. Your leg goes out from under you.")
                print(PAR)
                type.type("Then another. Your back. Hot and wet and wrong.")
                print(PAR)
                type.type("You hit the ground. The sky is very blue today, you notice.")
                print(PAR)
                type.type("Footsteps approach. A face looks down at you. Disappointed, almost.")
                print(PAR)
                type.type(quote("Shouldn't have run."))
                print(PAR)
                type.type("One more shot. The sky goes dark.")
                print(PAR)
                self.kill("Shot while running from drug dealers. Wrong place. Wrong time. Wrong identity.")
                return
        print(PAR)

        print(PAR)
        return
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
        print(PAR)
        type.type("You're standing at the railing. Looking down at the water. So far down.")
        print(PAR)
        type.type("Your hands are on the cold metal. When did you get out of the car?")
        print(PAR)
        type.type("The water looks peaceful. Dark and cold and peaceful. No more debt. No more hunger.")
        print(PAR)
        type.type("No more losing. No more trying. Just... nothing.")
        print(PAR)
        type.type("A voice in your head says: " + italic("It would be so easy. Just let go."))
        print(PAR)
        answer = ask.option("What do you do? ", ["step back", "stay", "call for help"])
        print(PAR)
        if answer == "step back":
            type.type("You force yourself to step back. One step. Then another.")
            print(PAR)
            type.type("Your hands are shaking. You're crying. When did you start crying?")
            print(PAR)
            type.type("You get back in your car. You drive away. You don't look back.")
            print(PAR)
            type.type("You're not okay. But you're alive. Today, that's enough.")
            self.lose_sanity(10)
            self.restore_sanity(15)  # Net positive for choosing life
        elif answer == "stay":
            type.type("You stay at the railing. Minutes pass. Maybe hours.")
            print(PAR)
            type.type("A car stops. Someone gets out. A woman's voice, soft and scared.")
            print(PAR)
            type.type(quote("Hey. Hey there. Are you okay? Please step back from the edge."))
            print(PAR)
            type.type("You look at her. She looks terrified. Terrified for YOU.")
            print(PAR)
            type.type("When's the last time anyone was scared for you? When's the last time anyone cared?")
            print(PAR)
            type.type("You step back. She holds you while you cry. A stranger. Holding you while you fall apart.")
            self.restore_sanity(20)
            self.meet("Bridge Angel")
        else:  # call for help
            type.type("With shaking hands, you pull out your phone. 988. The suicide hotline.")
            print(PAR)
            type.type("A voice answers. Calm. Kind. They talk to you for an hour.")
            print(PAR)
            type.type("They don't judge. They don't tell you you're being stupid. They just... listen.")
            print(PAR)
            type.type("When you finally hang up, you're sitting in your car. Still on the bridge. But back from the edge.")
            print(PAR)
            type.type("You're not fixed. But you're here. That matters.")
            self.restore_sanity(25)
        print(PAR)

        print(PAR)
        return
    def food_poisoning(self):
        # EVENT: Severe food poisoning from gas station food
        # EFFECTS: 60% survive (25 dmg + 10 sanity); 30% hospitalized (45 dmg + $800 + "Weakened Immune System"); 10% death from sepsis
        # BRUTAL: Can cause death from bacterial sepsis
        # DEATH POSSIBLE - Bad luck
        type.type("You're hunched over in your car seat. You ate something from a gas station. In retrospect, that was a mistake.")
        print(PAR)
        type.type("The first cramp hits around 2 AM. Then another. Then the real fun begins.")
        print(PAR)
        type.type("You're vomiting. You're... the other thing too. Your body is emptying itself from both ends.")
        print(PAR)
        type.type("The pain is unreal. Your stomach feels like it's being stabbed from the inside.")
        print(PAR)
        chance = random.randrange(10)
        if chance < 6:
            type.type("It goes on for hours. You lose count of how many times you throw up.")
            print(PAR)
            type.type("But by dawn, it's fading. Your body has expelled the poison.")
            print(PAR)
            type.type("You lie on the cold ground next to your car, exhausted, dehydrated, but alive.")
            print(PAR)
            type.type("You'll never eat gas station sushi again. Lesson learned.")
            self.hurt(25)
            self.lose_sanity(10)
        elif chance < 9:
            type.type("By morning, you're seeing double. Your heart is racing. This is bad. Really bad.")
            print(PAR)
            type.type("Someone finds you passed out next to your car and calls 911.")
            print(PAR)
            type.type("The hospital pumps your stomach. IV fluids. They say you had severe dehydration.")
            print(PAR)
            type.type("Two more hours and your organs would have started failing.")
            self.hurt(45)
            self.lose_sanity(15)
            self.add_danger("Weakened Immune System")
            if self.get_balance() >= 800:
                type.type("Hospital bill: " + red(bright("$800")) + ".")
                self.change_balance(-800)
        else:
            type.type("The vomiting stops. That's not a good sign. Your body has given up fighting.")
            print(PAR)
            type.type("You can't move. Can't speak. Can barely see.")
            print(PAR)
            type.type("The bacteria has reached your bloodstream. Sepsis. Multiple organ failure.")
            print(PAR)
            type.type("You die in your car, alone, because you ate a $3.99 egg salad sandwich.")
            print(PAR)
            self.kill("Food poisoning. Death by gas station sushi. An ignoble end.")
            return
        print(PAR)

        print(PAR)
        return
    def attacked_by_dog(self):
        # DEATH POSSIBLE - Animal attack
        # COMPANION INTEGRATION: Lucky/protection companion fights the stray
        
        # COMPANION: Lucky specifically can fight off the dog
        if self.has_companion("Lucky") and self.get_companion("Lucky")["status"] == "alive":
            type.type("You step out of your car when you hear growling. A big stray dog. Teeth bared.")
            print(PAR)
            type.type("Before you can react, " + bright("Lucky") + " is already between you and the stray.")
            print(PAR)
            type.type("Three-legged but fearless. Lucky stands his ground, growling back.")
            print(PAR)
            type.type("The two dogs have a standoff. Circling. Snarling. Your heart is in your throat.")
            print(PAR)
            if random.randrange(3) != 0:
                type.type("Lucky barks once. A sharp, commanding sound. The stray flinches.")
                print(PAR)
                type.type("Then the stray backs down. Tucks its tail. Trots away.")
                print(PAR)
                type.type("Lucky doesn't relax until the stray is completely out of sight. Then he turns to you and wags his tail.")
                print(PAR)
                type.type(green("Lucky protected you from the stray! Best boy."))
                self.pet_companion("Lucky")
                self.restore_sanity(5)
            else:
                type.type("The stray lunges. Lucky meets it head-on. Fur flies. Blood draws.")
                print(PAR)
                type.type("It's over in seconds. The stray yelps and runs. Lucky stands victorious.")
                print(PAR)
                type.type("But he's hurt. A gash on his side. He limps over to you, tail still wagging.")
                print(PAR)
                type.type("You patch him up. He licks your hand. This dog would die for you.")
                self.hurt(5)  # You got scratched too
                self._companions["Lucky"]["happiness"] = max(0, self._companions["Lucky"]["happiness"] - 5)
                self.pet_companion("Lucky")
                self.pet_companion("Lucky")
                self.restore_sanity(3)
            print(PAR)
            return
        
        type.type("You step out of your car and head toward a convenience store when you hear it. Growling. Deep and low.")
        print(PAR)
        type.type("A dog. Big. Rottweiler or pit bull, you can't tell. No leash. No owner. Just teeth.")
        print(PAR)
        type.type("It's staring at you. Hackles raised. Drool dripping from its jaws.")
        print(PAR)

        # ITEM: Dog Whistle - sonic authority over the pack
        if self.has_item("Dog Whistle"):
            type.type("You blow the " + cyan(bright("Dog Whistle")) + ". The frequency is too high for human hearing but perfect for canine authority.")
            print(PAR)
            type.type("The dog freezes. Then sits. You walk past it calmly.")
            print(PAR)
            type.type("It watches you go with confused, respectful eyes. You are the alpha now, apparently.")
            self.restore_sanity(5)
            print(PAR)
            return

        type.type("You freeze. Don't run. Don't make eye contact. You remember reading that somewhere.")
        print(PAR)
        chance = random.randrange(10)
        if chance < 4:
            type.type("The dog watches you. Sniffs the air. Decides you're not worth the effort.")
            print(PAR)
            type.type("It trots away, looking for something more interesting.")
            print(PAR)
            type.type("You don't move for five minutes. Then you walk VERY quickly to your car.")
            self.lose_sanity(8)
        elif chance < 8:
            type.type("It charges. Ninety pounds of muscle and fury coming right at you.")
            print(PAR)
            type.type("You throw your arms up. Its jaws close on your forearm. You SCREAM.")
            print(PAR)
            type.type("It shakes its head, tearing flesh. You punch it. Kick it. Nothing works.")
            print(PAR)
            type.type("Someone runs over with a stick. Beats the dog off you. It finally lets go and runs.")
            print(PAR)
            type.type("Your arm is a mess of blood and torn muscle. You can see bone.")
            if self.has_item("Scrap Armor") or self.has_item("Plated Vest") or self.has_item("Road Warrior Plate"):
                armor_name = "Scrap Armor" if self.has_item("Scrap Armor") else ("Plated Vest" if self.has_item("Plated Vest") else "Road Warrior Plate")
                type.type(" The makeshift padding took the worst of it.")
                self.hurt(20)
                evolved = self.track_item_use(armor_name)
                if evolved:
                    print(PAR)
                    type.type(cyan(bright(self.get_evolution_text(evolved[0], evolved[1]))))
            else:
                self.hurt(40)
            self.lose_sanity(15)
            self.add_danger("Dog Bite Wound")
            if self.get_balance() >= 600:
                type.type("ER stitches: " + red(bright("$600")) + ".")
                self.change_balance(-600)
        else:
            type.type("It goes for your throat. Instinct. Predator targeting the kill zone.")
            print(PAR)
            type.type("You get your arm up just in time. It bites deep. You fall.")
            print(PAR)
            type.type("Then it's on top of you. Biting. Tearing. You're screaming. So much blood.")
            print(PAR)
            type.type("It finds your throat eventually. They always do.")
            print(PAR)
            type.type("Your last sight is the blue sky through red haze. Your last sound is growling.")
            print(PAR)
            self.kill("Mauled to death by a stray dog. Not every monster is human.")
            return
        print(PAR)

        print(PAR)
        return
    def electrocution_hazard(self):
        # DEATH POSSIBLE - Freak accident
        type.type("It's raining hard. You jump out of your car and run for cover under an awning.")
        print(PAR)
        type.type("There's a puddle. A big one. And an old electrical box on the wall, sparking.")
        print(PAR)
        type.type("You don't notice until it's too late. Your foot hits the water.")
        print(PAR)
        chance = random.randrange(10)

        if self.has_item("Quiet Sneakers") or self.has_item("Quiet Bunny Slippers"):
            shoes = "Quiet Bunny Slippers" if self.has_item("Quiet Bunny Slippers") else "Quiet Sneakers"
            type.type("Your sole hits the edge of the puddle, but the " + cyan(bright(shoes)) + " catches for you before your full weight commits.")
            print(PAR)
            if shoes == "Quiet Bunny Slippers":
                type.type("You spring sideways in one perfectly silent movement. The water crackles where you would have been.")
                self.restore_sanity(6)
            else:
                type.type("You stumble back, heart slamming. One wet lace and you'd be dead.")
                self.restore_sanity(3)
            self.update_quiet_sneakers_durability()
            print(PAR)
            return

        if chance < 5:
            type.type("A jolt runs through you. Painful but brief. The breaker must have tripped.")
            print(PAR)
            type.type("You jump back, heart pounding. That could have killed you.")
            print(PAR)
            type.type("You report the hazard to the shop owner. They seem unimpressed.")
            if self.has_item("Scrap Armor") or self.has_item("Plated Vest") or self.has_item("Road Warrior Plate"):
                armor_name = "Scrap Armor" if self.has_item("Scrap Armor") else ("Plated Vest" if self.has_item("Plated Vest") else "Road Warrior Plate")
                type.type(" Your jury-rigged gear absorbed some of the shock.")
                self.hurt(4)
                evolved = self.track_item_use(armor_name)
                if evolved:
                    print(PAR)
                    type.type(cyan(bright(self.get_evolution_text(evolved[0], evolved[1]))))
            else:
                self.hurt(10)
            self.lose_sanity(8)
        elif chance < 8:
            type.type("The current grabs you. Your muscles seize. You can't move. Can't breathe.")
            print(PAR)
            type.type("Someone tackles you away from the puddle. A stranger. Saved your life.")
            print(PAR)
            type.type("Your heart is racing. Irregular. Your hands won't stop shaking.")
            print(PAR)
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
            print(PAR)
            type.type("You can't scream. Can't move. Just the electricity, burning through you.")
            print(PAR)
            type.type("Your heart stops. It tries to start again. Stops. Starts. Stops.")
            print(PAR)
            type.type("By the time someone kicks you free of the puddle, you're gone.")
            print(PAR)
            self.kill("Electrocution. A faulty wire and a puddle. That's all it took.")
            return
        print(PAR)

        print(PAR)
        return
    def car_explosion(self):
        # DEATH POSSIBLE - Mechanical failure
        type.type("You turn the key in the ignition. The engine makes a strange noise. A ticking.")
        print(PAR)
        type.type("Something smells wrong. Gas. Strong and getting stronger.")
        print(PAR)
        type.type("Instinct screams at you: GET OUT. GET OUT NOW.")
        print(PAR)
        answer = ask.option("What do you do? ", ["bail out", "investigate", "ignore it"])
        print(PAR)
        if answer == "bail out":
            type.type("You throw yourself out of the car and run. Don't look back. Just run.")
            print(PAR)
            chance = random.randrange(3)
            if chance == 0:
                type.type("You're ten feet away when the engine catches fire. Fifteen when it explodes.")
                print(PAR)
                type.type("The shockwave knocks you flat. Heat washes over you. Debris rains down.")
                print(PAR)
                type.type("Your car—your home—is a fireball. Everything you owned is gone.")
                print(PAR)
                type.type("But you're alive. Somehow. Alive.")
                self.hurt(20)
                self.lose_sanity(25)
                self.remove_item("Car")
                lost = self.get_balance() * 0.2
                self.change_balance(-lost)
            else:
                type.type("Nothing explodes. The engine just... dies. Smoke pours out.")
                print(PAR)
                type.type("False alarm. Fuel line leak. Bad, but not explosive.")
                print(PAR)
                type.type("You feel foolish. But also glad you trusted your gut.")
                self.add_danger("Fuel Leak")
                self.lose_sanity(10)
        elif answer == "investigate":
            type.type("You pop the hood. Lean in to look. The gas smell is overwhelming.")
            print(PAR)
            chance = random.randrange(10)
            if chance < 7:
                type.type("There's the problem. A cracked fuel line. Gas dripping onto hot metal.")
                print(PAR)
                type.type("You back away slowly. Very slowly. Get some distance.")
                print(PAR)
                type.type("You disconnect the battery and let it cool down. Crisis averted.")
                self.add_danger("Fuel Leak")
                self.lose_sanity(10)
            else:
                type.type("The spark happens while you're leaning over the engine.")
                print(PAR)
                type.type("The last thing you see is a flash of orange. The last thing you feel is heat.")
                print(PAR)
                type.type("They find your body twenty feet from the wreckage.")
                print(PAR)
                self.kill("Car explosion. Mechanical failure meets human curiosity. Boom.")
                return
        else:  # ignore it
            type.type("It's probably nothing. This car always makes weird noises.")
            print(PAR)
            type.type("You turn the key again. The ticking gets louder.")
            print(PAR)
            chance = random.randrange(10)
            if chance < 4:
                type.type("The engine catches. Runs rough, but runs. The smell fades.")
                print(PAR)
                type.type("You should really get that checked out. You won't, but you should.")
                self.add_danger("Fuel Leak")
            else:
                type.type("The fireball is instantaneous. You don't even have time to scream.")
                print(PAR)
                type.type("Glass and metal and fire, all at once. The car becomes your coffin.")
                print(PAR)
                self.kill("Died in a car explosion. Should have bailed. Should have investigated. Did neither.")
                return
        print(PAR)

        print(PAR)
        return
    def knife_wound_infection(self):
        # CONDITIONAL DEATH - Consequence of earlier event
        if not self.has_danger("Knife Wound"):
            self.day_event()
            return
        if self.has_item("Wound Salve"):
            type.type("You check the knife wound in the car mirror. It's angry. Red. But you have the " + cyan(bright("Wound Salve")) + ".")
            print(PAR)
            type.type("You slather it on thick. It stings — then soothes. The swelling fades within the hour.")
            print(PAR)
            type.type("Not a hospital. But maybe you don't need one.")
            self.use_item("Wound Salve")
            self.hurt(10)
            self.remove_danger("Knife Wound")
            print(PAR)
            return
        type.type("You check yourself in the car mirror. That knife wound from the mugging isn't healing right.")
        print(PAR)
        type.type("It's red. Swollen. Hot to the touch. Pus oozing from the edges.")
        print(PAR)
        type.type("You're running a fever. Shaking. This is bad.")
        print(PAR)
        chance = random.randrange(10)
        if chance < 5:
            type.type("You drag yourself to a free clinic. They take one look and rush you to a hospital.")
            print(PAR)
            type.type("Antibiotics. IV drip. They save your arm. Barely.")
            self.hurt(25)
            self.remove_danger("Knife Wound")
        elif chance < 8:
            type.type("The infection has spread. Sepsis. Your blood is poisoned.")
            print(PAR)
            type.type("Three days in the ICU. They're not sure you're going to make it.")
            print(PAR)
            type.type("You do. Barely. But you'll never forget how close you came.")
            self.hurt(50)
            self.lose_sanity(20)
            self.remove_danger("Knife Wound")
            if self.get_balance() >= 3000:
                type.type("Hospital bill: " + red(bright("$3000")) + ".")
                self.change_balance(-3000)
        else:
            type.type("You wait too long. The infection reaches your heart.")
            print(PAR)
            type.type("Endocarditis. By the time the ambulance arrives, you're barely conscious.")
            print(PAR)
            type.type("You die on the operating table. A stupid knife wound. A stupid delay.")
            print(PAR)
            self.kill("Died from an infected knife wound. Should have seen a doctor sooner.")
            return
        print(PAR)

        print(PAR)
        return
    def gut_wound_complications(self):
        # CONDITIONAL DEATH - Consequence of earlier event
        if not self.has_danger("Gut Wound"):
            self.day_event()
            return
        type.type("You shift in your car seat and wince. Your gut wound has been getting worse. Much worse.")
        print(PAR)
        type.type("The stitches popped. You can see... things you shouldn't be seeing.")
        print(PAR)
        type.type("The pain is constant now. You can't eat. Can barely drink.")
        print(PAR)
        chance = random.randrange(10)
        if chance < 6:
            type.type("You make it to an ER. Emergency surgery. They have to remove part of your intestine.")
            print(PAR)
            type.type("Recovery takes weeks. But you survive. Somehow.")
            self.hurt(40)
            self.lose_sanity(20)
            self.remove_danger("Gut Wound")
        else:
            type.type("The wound has gone septic. Your organs are failing.")
            print(PAR)
            type.type("You die in the back of your car, alone, holding your stomach together with your hands.")
            print(PAR)
            self.kill("Gut wound complications. Internal bleeding. Organ failure. Game over.")
            return
        print(PAR)

        print(PAR)
        return
    def devils_bargain_consequence(self):
        # CONDITIONAL EVENT - The devil collects
        if not self.has_danger("Devil's Bargain"):
            self.day_event()
            return
        if self.has_met("Devil's Collection"):
            self.day_event()
            return
        if self.has_item("Dark Pact Reliquary"):
            type.type("The " + cyan(bright("Dark Pact Reliquary")) + " glows. The devil recognizes the toolkit.")
            print(PAR)
            type.type(quote("You've done your homework,") + " he says. " + quote("Fine. New terms."))
            print(PAR)
            type.type("The original deal dissolves. In its place: something far more favorable. You keep your soul. He keeps his pride.")
            self.restore_sanity(15)
            self.remove_danger("Devil's Bargain")
            self.meet("Devil's Collection")
            print(PAR)
            return
        self.meet("Devil's Collection")
        type.type("The stranger from before is back. Standing by your car. Waiting.")
        print(PAR)
        type.type(quote("You've done well. Very well. But it's time to pay what you owe."))
        print(PAR)
        type.type("You try to run but your legs won't move. You try to scream but nothing comes out.")
        print(PAR)
        type.type("He walks toward you. Slowly. That smile never reaching those dark, dead eyes.")
        print(PAR)
        type.type(quote("Don't worry. This won't hurt."))
        print(PAR)
        type.type("He reaches into your chest. No wound. No blood. Just... cold.")
        print(PAR)
        type.type("When he withdraws his hand, he's holding something small and bright. Your... something.")
        print(PAR)
        type.type(quote("A pleasure doing business."))
        print(PAR)
        type.type("He's gone. You feel... empty. Hollow. Like a part of you is missing.")
        print(PAR)
        type.type("You'll never feel truly happy again. That was the price.")
        self.lose_sanity(50)
        self.add_danger("Soulless")
        print(PAR)

    # ==========================================
    # CONNECTED & CONDITIONAL EVENTS - MEGA BATCH
    # ==========================================

    # === SOULLESS CONSEQUENCES (Devil's Bargain Chain) ===

        print(PAR)
        return
    def soulless_emptiness(self):
        if not self.has_danger("Soulless"):
            self.day_event()
            return
        type.type("You leave your car and head to the casino. You win at the tables. The dealer pushes chips toward you.")
        print(PAR)
        type.type("You should feel something. Joy. Triumph. Relief. Anything.")
        print(PAR)
        type.type("You feel nothing. Absolutely nothing. Just... hollow.")
        print(PAR)
        type.type("The other gamblers are celebrating, crying, raging. You just exist.")
        print(PAR)
        type.type("Is this what you traded for? Was it worth it?")
        self.lose_sanity(5)
        print(PAR)

        print(PAR)
        return
    def soulless_mirror(self):
        if not self.has_danger("Soulless"):
            self.day_event()
            return
        type.type("You catch your reflection in your car window. Something's wrong.")
        print(PAR)
        type.type("Your eyes. They're darker than they should be. Empty. Dead.")
        print(PAR)
        type.type("You look away quickly. You don't want to see what you've become.")
        self.lose_sanity(8)
        print(PAR)

        print(PAR)
        return
    def soulless_recognition(self):
        if not self.has_danger("Soulless"):
            self.day_event()
            return
        type.type("A child points at you from across the parking lot.")
        print(PAR)
        type.type("Their mother pulls them close, hurrying away. But you heard what the kid said:")
        print(PAR)
        type.type(quote("Mommy, why doesn't that man have a shadow?"))
        print(PAR)
        type.type("You look down. Your shadow is... faint. Barely there. Flickering.")
        print(PAR)
        type.type("When did that start happening?")
        self.lose_sanity(12)
        print(PAR)

    # === DOG BITE WOUND CHAIN ===

        print(PAR)
        return
    def dog_bite_rabies_scare(self):
        if not self.has_danger("Dog Bite Wound"):
            self.day_event()
            return
        type.type("You look at your arm in the car. Your dog bite wound is healing, but something else is wrong.")
        print(PAR)
        type.type("You're feverish. Light hurts your eyes. Water makes you gag.")
        print(PAR)
        type.type("Oh God. Rabies. The dog had rabies.")
        print(PAR)
        type.type("You race to the hospital. They test you. Hours of waiting.")
        print(PAR)
        chance = random.randrange(10)
        if chance < 8:
            type.type("Negative. No rabies. Just a regular infection and paranoia.")
            print(PAR)
            type.type("They give you antibiotics and tell you to calm down.")
            self.hurt(10)
            self.lose_sanity(15)
        else:
            type.type("Positive. The dog had rabies. You have rabies.")
            print(PAR)
            type.type("They start the shots immediately. Painful. Expensive. Necessary.")
            print(PAR)
            type.type("You'll live, but you'll never forget the two weeks of waiting to die.")
            self.hurt(30)
            self.lose_sanity(25)
            if self.get_balance() >= 2000:
                type.type("Rabies treatment: " + red(bright("$2000")) + ".")
                self.change_balance(-2000)
        self.remove_danger("Dog Bite Wound")
        print(PAR)

    # === FUEL LEAK CHAIN ===

        print(PAR)
        return
    def fuel_leak_fire(self):
        if not self.has_danger("Fuel Leak"):
            self.day_event()
            return
        if self.has_item("Gas Mask"):
            type.type("You smell the gas. Strong this time. You see the spark a half-second before it catches.")
            print(PAR)
            type.type("You pull on the " + cyan(bright("Gas Mask")) + " and walk toward the burning car while everyone else runs the other direction.")
            print(PAR)
            type.type("Through the smoke and flame, you spot a small safe bolted under the back seat. Didn't know it was there.")
            print(PAR)
            answer = ask.option("What do you do? ", ["grab the safe", "save the cat"])
            print(PAR)
            if answer == "grab the safe":
                type.type("You haul it out. The metal is hot through your gloves. You drag it clear before the tank goes.")
                print(PAR)
                type.type("BOOM. The car becomes a fireball behind you. The safe pops open on impact with the asphalt. " + green(bright("+$400")))
                self.change_balance(400)
                self.remove_danger("Fuel Leak")
                self.add_status("Cold Operator")
            else:
                type.type("A cat is trapped inside, screaming. You pull open the door and it bolts into your arms.")
                print(PAR)
                type.type("You stumble clear. The car explodes behind you. The building manager saw the whole thing. Gives you a key.")
                print(PAR)
                type.type(green("The building manager owes you one."))
                self.remove_danger("Fuel Leak")
                self.add_status("Cat Hero")
                self.add_item("Building Manager Key")
            print(PAR)
            return
        type.type("You smell gas again. Stronger this time. Much stronger.")
        print(PAR)
        type.type("Then you see the spark. A wire rubbing against metal.")
        print(PAR)
        type.type("You have maybe three seconds to react.")
        print(PAR)
        chance = random.randrange(10)
        if chance < 6:
            type.type("You bail out. Hit the ground rolling. Keep going.")
            print(PAR)
            type.type("The car doesn't explode. But it does catch fire. Your home is burning.")
            print(PAR)
            type.type("You watch helplessly as everything you own goes up in flames.")
            self.remove_item("Car")
            self.remove_danger("Fuel Leak")
            self.lose_sanity(30)
            lost = self.get_balance() * 0.25
            self.change_balance(-lost)
        else:
            type.type("Too slow. The fire starts before you're out.")
            print(PAR)
            type.type("Your clothes catch. Your hair. You're screaming and rolling on the ground.")
            print(PAR)
            type.type("Someone puts you out with a fire extinguisher. But the damage is done.")
            self.hurt(50)
            self.lose_sanity(35)
            self.remove_item("Car")
            self.remove_danger("Fuel Leak")
            self.add_danger("Burn Scars")
        print(PAR)

        print(PAR)
        return
    def fuel_leak_fixed(self):
        if not self.has_danger("Fuel Leak"):
            self.day_event()
            return
        if self.get_balance() < 150:
            self.day_event()
            return
        type.type("A mechanic notices your car leaking gas in the parking lot.")
        print(PAR)
        type.type(quote("Hey buddy, you know your fuel line is busted? That's a fire hazard."))
        print(PAR)
        type.type(quote("I can fix it for $150. Cash. Right now. Before you blow yourself up."))
        print(PAR)
        answer = ask.yes_or_no("Pay the mechanic? ($150) ")
        if answer == "yes":
            type.type("He works for an hour. Gets covered in grease. But he fixes it.")
            print(PAR)
            type.type(quote("There. No more kaboom.") + " He grins.")
            self.change_balance(-150)
            self.remove_danger("Fuel Leak")
        else:
            type.type("He shrugs. " + quote("Your funeral, man."))
            self.lose_sanity(5)
        print(PAR)

    # === HEART CONDITION CHAIN ===

        print(PAR)
        return
    def heart_condition_flare(self):
        if not self.has_danger("Heart Condition"):
            self.day_event()
            return
        type.type("You grip the steering wheel. Your chest tightens. Not again. Not now.")
        print(PAR)
        type.type("You fumble for the pills the doctor gave you. Can't find them.")
        print(PAR)
        type.type("The pain spreads. Down your arm. Up your jaw. Can't breathe.")
        print(PAR)
        chance = random.randrange(10)
        if chance < 6:
            type.type("Found them. You swallow two dry and wait.")
            print(PAR)
            type.type("Slowly, the pain fades. The pressure eases. You're okay. This time.")
            self.hurt(15)
            self.lose_sanity(10)
        elif chance < 9:
            type.type("Someone sees you clutching your chest. Calls 911.")
            print(PAR)
            type.type("Hospital. Another stent. Another lecture about stress.")
            self.hurt(35)
            self.lose_sanity(15)
            if self.get_balance() >= 1500:
                type.type("Bill: " + red(bright("$1500")) + ".")
                self.change_balance(-1500)
        else:
            type.type("This one is worse. Much worse. The big one.")
            print(PAR)
            type.type("You collapse. Everything goes gray. Then black.")
            print(PAR)
            self.kill("Heart attack. Your body couldn't take the stress anymore.")
            return
        print(PAR)

    # === SHOULDER DESTROYED CHAIN ===

        print(PAR)
        return
    def shoulder_chronic_pain(self):
        if not self.has_danger("Shoulder Destroyed"):
            self.day_event()
            return
        type.type("You try to adjust your car seat and wince. Your shoulder is on fire today. Some days are worse than others.")
        print(PAR)
        type.type("You can barely lift your arm. Simple things—opening doors, reaching for chips—agony.")
        print(PAR)
        type.type("This is your life now. Chronic pain. Forever.")
        self.hurt(10)
        self.lose_sanity(5)
        print(PAR)

        print(PAR)
        return
    def shoulder_painkiller_addiction(self):
        if not self.has_danger("Shoulder Destroyed"):
            self.day_event()
            return
        if self.has_met("Painkiller Offer"):
            self.day_event()
            return
        self.meet("Painkiller Offer")
        type.type("A guy in the parking lot notices you wincing, rubbing your shoulder.")
        print(PAR)
        type.type(quote("Bad injury? I got something for that. Take the edge off."))
        print(PAR)
        type.type("He shows you a bottle of pills. Oxycodone. Not his prescription.")
        print(PAR)
        if self.get_balance() >= 100:
            answer = ask.yes_or_no("Buy the painkillers? ($100) ")
            if answer == "yes":
                type.type("You hand over the money. Pop two pills.")
                print(PAR)
                type.type("Twenty minutes later, the pain is... gone. Just warmth and peace.")
                print(PAR)
                type.type("This is dangerous. You know this is dangerous. But God, it feels good.")
                self.change_balance(-100)
                self.hurt(-20)  # Heals temporarily
                self.restore_sanity(15)
                self.add_danger("Painkiller Dependency")
            else:
                type.type("You shake your head. He shrugs and walks away.")
        else:
            type.type("You can't afford them anyway. Small mercies.")
        print(PAR)

    # === PAINKILLER DEPENDENCY CHAIN ===

        print(PAR)
        return
    def painkiller_withdrawal(self):
        if not self.has_danger("Painkiller Dependency"):
            self.day_event()
            return
        type.type("You're sitting in your car, shaking. You're out of pills. Have been for two days.")
        print(PAR)
        type.type("Your body is screaming. Sweating. Shaking. Nausea. Everything hurts MORE than before.")
        print(PAR)
        type.type("This is withdrawal. This is what addiction feels like.")
        print(PAR)
        self.hurt(25)
        self.lose_sanity(20)
        print(PAR)

        print(PAR)
        return
    def painkiller_dealer_returns(self):
        if not self.has_danger("Painkiller Dependency"):
            self.day_event()
            return
        type.type("A tap on your car window - the pill guy is back. Like he knew you'd need him.")
        print(PAR)
        type.type(quote("Looking rough, friend. Need a refill?"))
        print(PAR)
        if self.get_balance() >= 150:
            answer = ask.yes_or_no("Buy more pills? ($150 - prices went up) ")
            if answer == "yes":
                type.type("You pay. You take. The pain goes away. The cycle continues.")
                self.change_balance(-150)
                self.hurt(-15)
                self.restore_sanity(10)
            else:
                type.type("You say no. It's the hardest thing you've ever done.")
                print(PAR)
                type.type("He'll be back. They always come back.")
        else:
            type.type("You don't have the money. He walks away. The withdrawal continues.")
            self.hurt(10)
            self.lose_sanity(10)
        print(PAR)

        print(PAR)
        return
    def painkiller_overdose(self):
        if not self.has_danger("Painkiller Dependency"):
            self.day_event()
            return
        type.type("Sitting in your car, you take an extra pill. Then another. The pain is so bad today.")
        print(PAR)
        type.type("Then another. When did you take the last one? You can't remember.")
        print(PAR)
        type.type("Everything feels slow. Warm. Your breathing is shallow.")
        print(PAR)
        chance = random.randrange(10)
        if chance < 7:
            type.type("You fall asleep. Wake up twelve hours later, covered in sweat, but alive.")
            print(PAR)
            type.type("That was close. Too close. Maybe you should stop.")
            self.hurt(20)
            self.lose_sanity(15)
        else:
            type.type("You stop breathing. Simple as that. The pills take you under and you don't come back up.")
            print(PAR)
            self.kill("Overdose. Another statistic. Another preventable death.")
            return
        print(PAR)

    # === BURN SCARS CHAIN ===

        print(PAR)
        return
    def burn_scars_stares(self):
        if not self.has_danger("Burn Scars"):
            self.day_event()
            return
        type.type("You step out of your car. People stare at your scars. They try to hide it, but they stare.")
        print(PAR)
        type.type("Children point. Adults look away too quickly. Nobody meets your eyes.")
        print(PAR)
        type.type("You used to be invisible. Now you're a spectacle.")
        self.lose_sanity(8)
        print(PAR)

        print(PAR)
        return
    def burn_scars_infection(self):
        if not self.has_danger("Burn Scars"):
            self.day_event()
            return
        type.type("You check yourself in the car mirror. Your burn scars are weeping. Infected, probably. You can't afford proper care.")
        print(PAR)
        type.type("You clean them with water and hope. That's all you have.")
        print(PAR)
        chance = random.randrange(5)
        if chance == 0:
            type.type("The infection spreads. You need real help.")
            self.hurt(30)
            self.add_danger("Infected Burns")
        else:
            type.type("It seems to be okay. For now.")
            self.hurt(10)
        print(PAR)

    # === ATM THEFT CHAIN ===

        print(PAR)
        return
    def weakened_immune_cold(self):
        if not self.has_danger("Weakened Immune System"):
            self.day_event()
            return
        type.type("Sitting in your car, you catch a cold. Nothing serious, normally.")
        print(PAR)
        type.type("But with your weakened immune system, it hits hard. Very hard.")
        print(PAR)
        type.type("You're bedridden for a week. In your car. Miserable.")
        self.hurt(25)
        self.lose_sanity(10)
        print(PAR)

        print(PAR)
        return
    def weakened_immune_pneumonia(self):
        if not self.has_danger("Weakened Immune System"):
            self.day_event()
            return
        type.type("You're shivering in your car. That cold turned into something worse. Pneumonia.")
        print(PAR)
        type.type("You can't breathe. You're coughing blood. This is bad.")
        print(PAR)
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
            print(PAR)
            self.kill("Pneumonia. Your immune system couldn't fight anymore.")
            return
        print(PAR)

    # === COCAINE CHAIN (from drug dealer event) ===

        print(PAR)
        return
    def cocaine_temptation(self):
        if not self.has_item("Bag of Cocaine"):
            self.day_event()
            return
        type.type("You're sitting in your car. You still have that bag of cocaine. It's been staring at you.")
        print(PAR)
        type.type("You've never tried it. But you're tired. So tired. And it promises energy.")
        print(PAR)
        answer = ask.option("What do you do? ", ["try it", "sell it", "throw it away"])
        print(PAR)
        if answer == "try it":
            type.type("You snort a line. Your first time.")
            print(PAR)
            type.type("...")
            print(PAR)
            type.type("Oh. OH. This is... this is AMAZING.")
            print(PAR)
            type.type("Colors are brighter. You're invincible. Every problem seems solvable.")
            print(PAR)
            type.type("You don't sleep for 36 hours. When you crash, you crash HARD.")
            self.hurt(-30)  # Temporary boost
            self.restore_sanity(20)  # Temporary
            self.remove_item("Bag of Cocaine")
            self.add_danger("Cocaine User")
        elif answer == "sell it":
            type.type("You find a buyer. Some desperate guy in the casino bathroom.")
            print(PAR)
            type.type("You sell it for $300. Not a great deal, but you're not a drug dealer.")
            self.change_balance(300)
            self.remove_item("Bag of Cocaine")
        else:
            type.type("You flush it. Watch it swirl away. Good riddance.")
            print(PAR)
            type.type("Part of you wonders what it would have been like. Most of you is relieved.")
            self.remove_item("Bag of Cocaine")
            self.restore_sanity(5)
        print(PAR)

        print(PAR)
        return
    def cocaine_crash(self):
        if not self.has_danger("Cocaine User"):
            self.day_event()
            return
        type.type("You're slumped in your car seat. The crash comes. And it's BRUTAL.")
        print(PAR)
        type.type("Depression. Paranoia. Your teeth won't stop chattering.")
        print(PAR)
        type.type("You need more. Your body NEEDS more. But you don't have any.")
        self.hurt(30)
        self.lose_sanity(25)
        print(PAR)

        print(PAR)
        return
    def cocaine_heart_attack(self):
        if not self.has_danger("Cocaine User"):
            self.day_event()
            return
        type.type("You're gripping the steering wheel. Your heart is racing. Has been for hours. Something's wrong.")
        print(PAR)
        type.type("Chest pain. Arm pain. The cocaine was cut with something. Something bad.")
        print(PAR)
        chance = random.randrange(10)
        if chance < 6:
            type.type("It passes. Slowly. You lie in your car, convinced you're dying, but you don't.")
            self.hurt(35)
            self.lose_sanity(20)
            self.remove_danger("Cocaine User")
        else:
            type.type("Your heart gives out. Cocaine-induced cardiac arrest.")
            print(PAR)
            self.kill("Drug overdose. The coke was cut with fentanyl. You never had a chance.")
            return
        print(PAR)

    # === STRAY CAT FRIEND CHAIN ===

        print(PAR)
        return
    def bridge_angel_returns(self):
        if not self.has_met("Bridge Angel"):
            self.day_event()
            return
        if self.has_met("Bridge Angel Returns"):
            self.day_event()
            return
        self.meet("Bridge Angel Returns")
        type.type("You step out of your car and see her again. The woman from the bridge. The one who stopped you.")
        print(PAR)
        type.type("She recognizes you too. Walks over. Smiles.")
        print(PAR)
        type.type(quote("Hey. You're still here. I'm glad."))
        print(PAR)
        type.type("She gives you her number. " + quote("If you ever need to talk. About anything. Call me."))
        print(PAR)
        type.type("You put it in your pocket. It feels like it weighs a hundred pounds.")
        self.add_item("Angel's Number")
        self.restore_sanity(15)
        self._storyline_system.advance("bridge_angel")
        print(PAR)

        print(PAR)
        return
    def call_bridge_angel(self):
        if not self.has_item("Angel's Number"):
            self.day_event()
            return
        type.type("Bad day. Really bad. Sitting in your car, you dig out that number. Your hands are shaking.")
        print(PAR)
        type.type("She answers on the second ring.")
        print(PAR)
        type.type(quote("Hey. I was hoping you'd call. Talk to me. What's going on?"))
        print(PAR)
        type.type("You talk for two hours. About everything. The gambling. The car. The fear.")
        print(PAR)
        type.type("She doesn't judge. Doesn't lecture. Just listens.")
        print(PAR)
        type.type(quote("You're stronger than you think. I believe in you."))
        self.restore_sanity(30)
        self._storyline_system.complete("bridge_angel")
        print(PAR)

    # === GAS STATION HERO CHAIN ===

        print(PAR)
        return
    def gas_station_hero_recognized(self):
        if not self.has_met("Gas Station Hero"):
            self.day_event()
            return
        type.type("You head out from your car to a convenience store. Someone points at you.")
        print(PAR)
        type.type(quote("That's him! That's the guy who stopped the robbery!"))
        print(PAR)
        type.type("People start clapping. The cashier gives you free coffee.")
        print(PAR)
        type.type("You feel like a fraud. You just reacted. Didn't think. Could have died.")
        print(PAR)
        type.type("But the coffee is nice.")
        self.restore_sanity(10)
        print(PAR)

        print(PAR)
        return
    def gas_station_hero_interview(self):
        if not self.has_met("Gas Station Hero"):
            self.day_event()
            return
        if self.has_met("Hero Interview"):
            self.day_event()
            return
        self.meet("Hero Interview")
        type.type("You're sitting in your car when a news van pulls up. A local station wants to interview you about the robbery.")
        print(PAR)
        answer = ask.yes_or_no("Do the interview? ")
        if answer == "yes":
            type.type("They film you by your car. Which is... not a great look.")
            print(PAR)
            type.type("The segment runs on the evening news. " + quote("Local Homeless Man Stops Armed Robbery!"))
            print(PAR)
            type.type("The comments online are split between calling you a hero and mocking your living situation.")
            self.restore_sanity(5)
            self.lose_sanity(5)  # Mixed feelings
            self.meet("Media Known")
        else:
            type.type("You decline. You're not a hero. You just did what anyone would do.")
        print(PAR)

    # === VOODOO DOLL ===

        print(PAR)
        return
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
        print(PAR)
        type.type("You take it out. It's warm in your hand. Warmer than it should be.")
        print(PAR)
        type.type("The swamp witch said: " + quote("You know what to do with this.") + " Do you?")
        print(PAR)
        action = ask.option("What do you do with it?", ["stick a pin in it", "burn it", "keep it safe"])
        print(PAR)
        if action == "stick a pin in it":
            type.type("You find a pin. You push it in slowly.")
            print(PAR)
            type.type("...")
            print(PAR)
            type.type("Somewhere across town, someone stubs their toe. You can't know this. But you do.")
            print(PAR)
            type.type("More importantly: a rival gambler who had it out for you is suddenly... distracted tonight.")
            self.change_balance(random.randint(200, 800))
            self.lose_sanity(random.choice([8, 10, 15]))
            type.type("The doll crumbles to wax dust in your hands. The deed is done.")
            self.use_item("Voodoo Doll")
        elif action == "burn it":
            type.type("You hold the doll over your lighter. It resists, hissing and spitting black smoke.")
            print(PAR)
            type.type("Then it goes. Fast. Too fast. A flash of heat and it's ash.")
            print(PAR)
            type.type("You smell something you can't place. Not unpleasant. Like turned earth after rain.")
            print(PAR)
            type.type("Your hands stop shaking. For the first time in weeks.")
            self.restore_sanity(random.choice([15, 20]))
            self.heal(10)
            self.use_item("Voodoo Doll")
        else:
            type.type("You put it back. Some things are better left undone.")
            print(PAR)
            type.type("But it's warmer now than when you picked it up. Like it noticed you almost went through with it.")
            self.lose_sanity(3)
        print(PAR)

    # ==========================================
    # WRONG ITEM COMEDY EVENTS
    # ==========================================

        print(PAR)
        return
    def wrong_item_road_flares_stealth(self):
        if not self.has_item("Road Flares"):
            self.day_event()
            return
        type.type("You're sneaking through a dark area when you realize you can't see. Naturally, you light a " + cyan(bright("Road Flare")) + ".")
        print(PAR)
        type.type("Every creature, person, and possibly satellite in a one-mile radius turns toward the bright red glow.")
        print(PAR)
        type.type("So much for stealth.")
        print(PAR)
        self.lose_sanity(10)
        type.type("A raccoon stares at you from ten feet away, completely unafraid. You've ruined the concept of darkness.")
        print(PAR)

        print(PAR)
        return
    def wrong_item_necronomicon_loan_shark(self):
        if not self.has_item("Necronomicon"):
            self.day_event()
            return
        self._necronomicon_readings += 1
        type.type("The loan shark demands payment. You reach into your bag for collateral.")
        print(PAR)
        type.type("You pull out the " + cyan(bright("Necronomicon")) + ".")
        print(PAR)
        type.type("The loan shark's eyes go white. His mouth hangs open.")
        print(PAR)
        type.type("The book opens by itself. A page turns. The loan shark reads the first line.")
        print(PAR)
        type.type("He tears up the contract. " + quote("We're even,") + " he whispers. " + quote("Please leave."))
        print(PAR)
        self.change_balance(200)
        self.lose_sanity(15)
        type.type("You close the book. Something inside it chuckles. That can't be right.")
        print(PAR)

        print(PAR)
        return
    def necronomicon_reading(self):
        # EVENT: Reading the Necronomicon reveals dark secrets
        # CONDITION: Must have Necronomicon
        # EFFECTS: Sanity loss scales with cumulative readings (madness mechanic)
        if not self.has_item("Necronomicon"):
            self.day_event()
            return
        
        readings = self._necronomicon_readings
        self._necronomicon_readings += 1
        
        if readings == 0:
            type.type("You find yourself alone in a quiet moment. The " + cyan(bright("Necronomicon")) + " calls to you from your bag.")
            print(PAR)
            type.type("You open it. The text writhes on the page, alive and hungry.")
            print(PAR)
            type.type("You can't look away. The words burn themselves into your mind.")
            print(PAR)
            type.type("You learn a dark secret: the true nature of luck, the Dealer's weakness, the way fate can be bent.")
            print(PAR)
            self.lose_sanity(10)
            self.add_status("Dark Knowledge")
            self.mark_day("Dark Knowledge")
            type.type("You close the book. The secret is yours now, but so is the madness.")
        elif readings == 1:
            type.type("The " + cyan(bright("Necronomicon")) + " is open again. You don't remember opening it.")
            print(PAR)
            type.type("The ink is darker this time. Thicker. The words don't just enter your mind — they rearrange it.")
            print(PAR)
            type.type("You glimpse the architecture of probability itself. Every coin flip, every card dealt, every step taken — all predetermined.")
            print(PAR)
            self.lose_sanity(15)
            self.add_status("Dark Knowledge")
            type.type("Your nose is bleeding. That's new.")
        elif readings == 2:
            type.type("The " + cyan(bright("Necronomicon")) + " opens to a page you haven't seen before. It wasn't there yesterday.")
            print(PAR)
            type.type("The text is in your handwriting. ")
            type.type("You read your own account of events that haven't happened yet.")
            print(PAR)
            type.type("Most of them are terrible.")
            print(PAR)
            self.lose_sanity(20)
            self.add_status("Dark Knowledge")
            self.add_status("Necronomicon Madness")
            type.type("The book slams shut. Your hands won't stop shaking. You can hear the pages whispering even when it's closed.")
        else:
            type.type("You open the " + cyan(bright("Necronomicon")) + " again. By now it opens to whatever you need.")
            print(PAR)
            type.type("The problem is that what you need and what the book wants are becoming the same thing.")
            print(PAR)
            sanity_cost = 10 + readings * 5
            self.lose_sanity(sanity_cost)
            self.add_status("Dark Knowledge")
            self.add_status("Necronomicon Madness")
            if readings >= 4:
                type.type("You can hear the book even when your eyes are closed. Even when you're sleeping. Especially when you're sleeping.")
                print(PAR)
                type.type("Something on the other side of those pages knows your name now.")
            else:
                type.type("The madness deepens. The knowledge is power, but the price is steeper each time.")
        print(PAR)

    # === HIGH ROLLER KEYCARD CHAIN ===


        print(PAR)
        return
