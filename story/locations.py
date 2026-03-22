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

class LocationsMixin:
    """Locations: Afternoon choices, doctor, witch doctor, mechanics, convenience store, Marvin, pawn shop, loan shark"""

    def afternoon(self):
        self.update_status()
        self.update_rank()
        self.update_convenience_store_inventory()

        # Wind Restriction (1,000-10,000)
        if self.has_travel_restriction("Wind"):
            random_chance = random.randrange(3)
            if random_chance == 0:
                type.type("You watch the wind pull twigs and branches from the trees all afternoon.")
            elif random_chance == 1:
                type.type("One branch falls, and lands on the hood of your wagon. Had it been any bigger, that could've been bad.")
            elif random_chance == 2:
                type.type("You hear a loud crash in the distance. A tree must've fallen nearby.")
            else:
                type.type("The wind pushes the light gray clouds across the sky, and you watch them all afternoon.")

            print("\n")

            type.type("As the sun begins to fall, you collect your money, and leave the warmth of your wagon. You barrel out into the wind, trudging your way to the casino.")

            print("\n")
            random_chance = random.randrange(4)
            if random_chance == 1:
                type.slow(red("It's a windy one today. Now, let us gamble."))
            elif random_chance == 2:
                type.slow(red("Surprised you made it here in one piece, given the weather. It's time to bet."))
            elif random_chance == 3:
                type.slow(red("It's nice to see you tonight. Shows commitment. You ready?"))
            else:
                type.slow(red("Wind didn't blow any of your money away, did it? Anyways, let's play."))
            print("\n")

        # Rain Restriction (500,000-900,000)
        elif self.has_travel_restriction("Rain"):
            type.type("You watch, as the rain pours, and pours, and pours. ")
            type.type("By nightfall, the rain hasn't let up, and the flooding in the streets has only gotten worse. ")
            type.type("Unfortunately, you're gonna have to skip out on Blackjack for the night.")
            print("\n")
            type.type("You get cozy in your car, and begin to doze off. That's all for " + bright(yellow("Day " + str(self._day))) + ".")
            print("\n")
            type.type("As you sleep, you dream and dream about the sand beneath your feet, ")
            type.type("the waterfall above you raining water down, splashing in the river, ")
            type.type("leading out to the ocean and the horizon before you. ")
            type.type("The sun looks so bright in the fading orange sky, and the hot sand began to cool below you. ")
            type.type("Before you get the chance to say goodbye, you wake up, having slept through all of " + bright(yellow("Day " + str(self._day + 1))) + " and " + bright(yellow("Day " + str(self._day + 2))) + ".")
            random_chance = random.randrange(2)
            if random_chance == 0:
                self._day += 3
            else:
                type.type(" And even " + bright(yellow("Day " + str(self._day + 3))))
                self._day += 4
            print("\n")
            type.type("As you awake on " + bright(yellow("Day " + str(self._day))) + ", you notice the raindrops begin to slow down, ")
            type.type("clouds begin to clear, and a golden ray of sunshine fills your soaked wagon. ")
            type.type("Looking in the seat next to you, your pile of green bills brings a sparkle to your eyes. ")
            type.type("You hear the money call to you. It's time. Let's go win some hands.")

            print("\n")

            type.type("As the sun begins to fall, you collect your money, and leave the safety of your wagon. ")
            type.type("You barrel out into the damp air, up the muddy dirt road, and into the casino.")

            print("\n")
            random_chance = random.randrange(4)
            if random_chance == 1:
                type.slow(red("Wipe those shoes. It's difficult to wash these carpets."))
            elif random_chance == 2:
                type.slow(red("Long time no see, yeah? Let's get back to it."))
            elif random_chance == 3:
                type.slow(red("You broke the streak you had going. Wanna make up for it in bets?"))
            else:
                type.slow(red("Glad the rain didn't permanently wash you away. That would have been a shame."))
            print("\n")

        elif any(self.has_travel_restriction(r) for r in [
            "Battery", "Engine", "Car Trouble", "Dead Battery", "Car Won't Start",
            "Dead Car", "Totaled Car", "Destroyed Engine", "No Engine", "Flat Tire",
            "Brake Failure", "Dead Alternator", "Radiator Failure", "No Headlights"
        ]):
            restriction_messages = {
                "Battery": "Your battery gives out before you can go anywhere useful.",
                "Engine": "Your engine won't turn over. The afternoon disappears while you fight with it.",
                "Car Trouble": "Your car acts up so badly you lose the whole afternoon dealing with it.",
                "Dead Battery": "Click. Click. Nothing. Your battery is dead again.",
                "Car Won't Start": "No matter what you try, your car refuses to start.",
                "Dead Car": "Your car is completely dead. You're not driving anywhere today.",
                "Totaled Car": "Your car is in no condition to drive. The afternoon is gone.",
                "Destroyed Engine": "The engine is beyond repair for now. You're stranded for the afternoon.",
                "No Engine": "No engine means no driving. You're stuck where you are.",
                "Flat Tire": "A flat tire kills your plans for the afternoon.",
                "Brake Failure": "Driving with failed brakes isn't an option. You stay put.",
                "Dead Alternator": "The alternator is dead, and so are your travel plans.",
                "Radiator Failure": "The cooling system fails before you can get moving.",
                "No Headlights": "Without headlights, you're not taking that risk on the road."
            }

            active_restriction = None
            for restriction in [
                "Battery", "Engine", "Car Trouble", "Dead Battery", "Car Won't Start",
                "Dead Car", "Totaled Car", "Destroyed Engine", "No Engine", "Flat Tire",
                "Brake Failure", "Dead Alternator", "Radiator Failure", "No Headlights"
            ]:
                if self.has_travel_restriction(restriction):
                    active_restriction = restriction
                    break

            if active_restriction is None:
                type.type("Your car trouble eats up the whole afternoon.")
            else:
                type.type(restriction_messages[active_restriction])
            print("\n")
            type.type("You lose the afternoon to car trouble and head straight to the casino at dusk.")
            print("\n")

            if active_restriction is not None and self.has_travel_restriction(active_restriction):
                self.remove_travel_restriction(active_restriction)
            if self.has_travel_restriction("Wasted Afternoon"):
                self.remove_travel_restriction("Wasted Afternoon")

            self.start_night()
            return

        elif self.check_for_car_trouble():
            print("\n")
            type.type("You head straight to the casino, hoping for better luck at the tables than you had with your car.")
            print("\n")
            self.start_night()
            return

        elif self.has_travel_restriction("Wasted Afternoon"):
            print("\n")
            type.type("You head straight to the casino, hoping for better luck at the tables than you had with your car.")
            print("\n")
            self.remove_travel_restriction("Wasted Afternoon")
            self.start_night()
            return

        # MILLIONAIRE AFTERNOON - Special choices after the visitor
        elif self.was_millionaire_visited() and self._balance >= 1000000:
            self.millionaire_afternoon()
        elif self.has_item("Car"):
            if len(self.get_all_companions()) > 0:
                if self.has_travel_restriction("Skip Companion Dialogue"):
                    type.type("Your companions keep their distance today. They don't seem ready to talk.")
                    print("\n")
                    self.remove_travel_restriction("Skip Companion Dialogue")
                else:
                    print("\n")
                    answer = ask.yes_or_no("Spend time with your companions? ")
                    if answer == "yes":
                        self.companion_afternoon_dialogue()
                        return
                    print("\n")

            shops = self._lists.make_shop_list()
            adventure_areas = self.get_unlocked_adventure_areas()

            type.type("Would you like to spend your day driving somewhere? ")
            print()

            for i in range(len(shops)):
                type.type(str(i+1) + ". " + shops[i])
                time.sleep(0.5)
                print()

            adventure_start = len(shops)
            if len(adventure_areas) > 0:
                type.type(yellow("--- Adventure Destinations ---"))
                print()
                for i, (area_name, _) in enumerate(adventure_areas):
                    type.type(str(adventure_start + i + 1) + ". Drive to " + area_name)
                    time.sleep(0.5)
                    print()

            stay_home_num = len(shops) + len(adventure_areas) + 1
            type.type(str(stay_home_num) + ". Stay Home")
            time.sleep(0.5)
            print()

            type.type("Choose a number: ")

            choice = None
            while True:
                while choice is None:
                    try:
                        choice = int(input())
                    except ValueError:
                        type.type("Choose a number: ")
                if 1 <= choice <= len(shops):
                    shop = shops[choice-1]
                    break
                elif len(shops) < choice <= len(shops) + len(adventure_areas):
                    area_index = choice - len(shops) - 1
                    area_name, area_func = adventure_areas[area_index]
                    if self.has_danger("Busted Kneecaps"):
                        type.type("You take two steps toward " + area_name + ", feel Tony's work in both knees, and immediately reconsider.")
                        print("\n")
                        type.type(quote("Yeah, no. You can't walk that much right now."))
                        print("\n")
                        choice = None
                        type.type("Choose a number: ")
                        continue
                    type.type("You fire up the wagon and head for " + area_name + ".")
                    print("\n")
                    adventure = getattr(self, area_func)
                    adventure()
                    self.update_rank()
                    self.start_night()
                    return
                elif choice == stay_home_num:
                    shop = "Home"
                    break
                else:
                    choice = None
                    type.type("That number's not a choice!")
                    print()
                    type.type("Choose a number: ")
            print()

            if shop == "Doctor's Office": self.visit_doctor()
            elif shop == "Witch Doctor's Tower": self.visit_witch_doctor()
            elif shop == "Trusty Tom's Trucks and Tires": self.visit_tom()
            elif shop == "Filthy Frank's Flawless Fixtures": self.visit_frank()
            elif shop == "Oswald's Optimal Outoparts": self.visit_oswald()
            elif shop == "Convenience Store": self.visit_convenience_store()
            elif shop == "Marvin's Mystical Merchandise": self.visit_marvin()
            elif shop == "Grimy Gus's Pawn Emporium": self.visit_pawn_shop()
            elif shop == "Vinnie's Back Alley Loans": self.visit_loan_shark()
            elif shop == "Airport": self.visit_airport()
            elif shop == "Make a Phone Call": self.visit_phone_call()
            elif shop == "Tanya's Office": self.visit_tanya()
            elif shop == "Car Workbench": self.visit_workbench()
            else: self.night_event()

        else:
            shops = self._lists.make_shop_list(on_foot=True)

            if len(shops) == 0:
                self.night_event()
                return

            type.type("Your wagon isn't road-ready, but there are still places you can reach before sundown.")
            print()
            type.type("Would you like to spend your day driving somewhere? ")
            print()

            for i in range(len(shops)):
                type.type(str(i+1) + ". " + shops[i])
                time.sleep(0.5)
                print()

            stay_home_num = len(shops) + 1
            type.type(str(stay_home_num) + ". Stay Home")
            time.sleep(0.5)
            print()

            type.type("Choose a number: ")

            choice = None
            while True:
                while choice is None:
                    try:
                        choice = int(input())
                    except ValueError:
                        type.type("Choose a number: ")
                if 1 <= choice <= len(shops):
                    shop = shops[choice-1]
                    break
                if choice == stay_home_num:
                    shop = "Home"
                    break
                choice = None
                type.type("That number's not a choice!")
                print()
                type.type("Choose a number: ")
            print()

            if shop == "Doctor's Office": self.visit_doctor()
            elif shop == "Witch Doctor's Tower": self.visit_witch_doctor()
            elif shop == "Trusty Tom's Trucks and Tires": self.visit_tom()
            elif shop == "Filthy Frank's Flawless Fixtures": self.visit_frank()
            elif shop == "Oswald's Optimal Outoparts": self.visit_oswald()
            elif shop == "Convenience Store": self.visit_convenience_store()
            elif shop == "Marvin's Mystical Merchandise": self.visit_marvin()
            elif shop == "Grimy Gus's Pawn Emporium": self.visit_pawn_shop()
            elif shop == "Vinnie's Back Alley Loans": self.visit_loan_shark()
            elif shop == "Make a Phone Call": self.visit_phone_call()
            elif shop == "Tanya's Office": self.visit_tanya()
            else: self.night_event()

    #Doctor's Office Interaction    
    def visit_doctor(self):
        self.increment_statistic("doctor_visits")
        type.type("You get in your car and drive to the Doctor's Office. ")
        if not self.has_met("Doctor's Office"):
            self.meet("Doctor's Office")
            type.type("As you pull up closer to the bright blue building, you notice that the parking lot is concerningly empty. ")
            type.type("You park your wagon right up front next to the entrance, and step out towards the doors. ")
            print("\n")
            type.type("When you enter into the lobby, you're immediately hit with the strong smell of hand sanitizer in the air. ")
            type.type("The carpets are dull and brown, the light above you is flickering, ")
            type.type("and the walls are filled with posters telling you to 'Floss More Often!' and 'Wash Your Hands Before You Eat!' ")
            type.type("If you didn't know any better, you would have guessed you were on a movie set.")
            print("\n")
            type.type("Walking towards the front desk, you see a cheery old lady, who looks up from her computer to smile at you. ")
            type.type("Her gray hair covers her glasses, and her hand trembles as she hands you a pen and a clipboard with some paperwork. ")
            type.type("Of course it's paperwork.")
            print("\n")
            type.type("After filling out your information, you walk back to the front desk, and hand the lady the clipboard. She smiles, and begins to speak to you.")
        print("\n")
        type.type("I see you're here for a checkup. The Doctor will see you now.")
        print("\n")
        type.type("Hey there champ! How are you? Doing all right? Let's check you out and make sure you're all up to snuff.")
        print()
        
        # Doctor comments on player's mental state (implicit sanity warning)
        if self._sanity < 30:
            type.type("You know... I've seen a lot of patients, and you've got that look. The distant eyes. The shaking hands. ")
            type.type("I patch up bodies, not minds. You should talk to someone. Not me. A professional. Someone who knows about... this kind of thing.")
            print()
        elif self._sanity < 50:
            type.type("You seem... off today. Stressed maybe? I can stitch cuts and set bones, but whatever's weighing on you, that's not my department.")
            print()
        
        if (self.len_status() == 0) and (self._health == 100):
            type.type("Why, you look just as healthy as the day I met you, fresh from your mother's womb! Let me just give you this lollipop and you'll be free to go.")
        elif (self.len_status() == 0):
            type.type("Why, you don't seem to really need my help. You appear a little worse for wear, but this medicine should do the trick.")
            print("\n")
        else:
            self._clear_status = True
            
            # RESPIRATORY CONDITIONS
            if self.has_status("Pneumonia"):
                type.type("Oh my. That cough sounds terrible. Let me listen to your lungs... ")
                type.type("Yes, definitely " + red("pneumonia") + ". I'm starting you on strong antibiotics immediately.")
                print()
            if self.has_status("Bronchitis"):
                type.type("That rattling cough? Classic " + red("bronchitis") + ". Here's an inhaler and some cough suppressant. Rest up.")
                print()
            if self.has_status("Severe Asthma"):
                type.type("You're wheezing badly. Let's get you on the nebulizer right away. " + red("Asthma") + " attack - severe one. Breathe deep.")
                print()
            
            # INFECTIONS
            if self.has_status("Spider Bite"):
                type.type("I see you have a nasty spider bite. That thing looks gross. Let me get that cleaned up for you.")
                print()
            if self.has_status("Strep Throat"):
                type.type("Open wide... yep, those white patches on your tonsils are unmistakable. " + red("Strep") + ". Ten days of antibiotics for you.")
                print()
            if self.has_status("Ear Infection"):
                type.type("Let me look in that ear... whoa. That's infected alright. " + red("Ear infection") + " - I'll prescribe antibiotic drops.")
                print()
            if self.has_status("Sinus Infection"):
                type.type("Your sinuses are completely blocked. I can see the inflammation from here. " + red("Sinusitis") + ". Antibiotics and decongestants.")
                print()
            if self.has_status("UTI"):
                type.type("The urine sample confirms it - " + red("urinary tract infection") + ". Very common. Antibiotics will clear it up in a few days.")
                print()
            if self.has_status("Pink Eye"):
                type.type("That's a textbook case of " + red("conjunctivitis") + ". Very contagious! Here are antibiotic eye drops. Wash your hands constantly.")
                print()
            if self.has_status("Staph Infection"):
                type.type("This wound is badly infected. I see red streaking - that's the " + red("staph") + " spreading. We need to drain this and get you on IV antibiotics.")
                print()
            if self.has_status("Tetanus"):
                type.type("Jaw stiffness, muscle spasms... this is " + red("tetanus") + ". You need antitoxin immediately. This is very serious.")
                print()
            if self.has_status("Rat Bite Fever"):
                type.type("That rat bite has given you an infection. " + red("Rat bite fever") + " - dangerous but treatable. High-dose penicillin for you.")
                print()
            if self.has_status("Ringworm"):
                type.type("That's " + red("ringworm") + " - fungal infection, not actually a worm. Antifungal cream should clear it up in a few weeks.")
                print()
            if self.has_status("Scabies"):
                type.type("The itching, the burrows between your fingers... you have " + red("scabies") + ". Mites. We'll treat you and you'll need to wash everything you own.")
                print()
            if self.has_status("Lyme Disease"):
                type.type("That bullseye rash is classic " + red("Lyme disease") + ". Good thing you came in - we can treat this with doxycycline before it gets serious.")
                print()
            if self.has_status("Shingles"):
                type.type("This painful rash following a nerve path - " + red("shingles") + ". The chickenpox virus reactivated. Antiviral medication will help.")
                print()
            if self.has_status("Mononucleosis"):
                type.type("Your fatigue, swollen lymph nodes... blood test confirms " + red("mono") + ". Bad news - no cure, just rest. Good news - it'll pass eventually.")
                print()
            if self.has_status("Measles"):
                type.type("This rash, the fever, the light sensitivity... " + red("measles") + ". I'll have to report this to the health department. Just supportive care for now.")
                print()
            
            # GASTROINTESTINAL
            if self.has_status("Stomach Flu"):
                type.type("You're very dehydrated from all that vomiting and diarrhea. " + red("Gastroenteritis") + ". IV fluids will help. And anti-nausea medication.")
                print()
            if self.has_status("Shellfish Poisoning"):
                type.type("Contaminated shellfish - " + red("Vibrio") + " infection most likely. We need to flush your system and give you supportive care.")
                print()
            if self.has_status("Mushroom Poisoning"):
                type.type("This is extremely serious - " + red("amatoxin poisoning") + " from toxic mushrooms. ")
                type.type("You need activated charcoal, liver monitoring, possibly a transplant list...")
                print()
            if self.has_status("Waterborne Illness"):
                type.type("Parasites or bacteria from contaminated water. " + red("Giardia") + " perhaps. Antibiotics and lots of fluids.")
                print()
            if self.has_status("Appendicitis"):
                type.type("Your appendix is inflamed and possibly about to rupture. " + red("Appendicitis") + ". You need emergency surgery - NOW.")
                print()
            if self.has_status("Gallbladder Attack"):
                type.type("Gallstones blocking your bile duct. " + red("Cholecystitis") + ". Pain management now, surgery to remove the gallbladder later.")
                print()
            if self.has_status("Pancreatitis"):
                type.type("Your pancreas is severely inflamed. " + red("Pancreatitis") + ". Nothing by mouth, IV fluids, and pray it doesn't get worse.")
                print()
            
            # KIDNEY/URINARY
            if self.has_status("Kidney Stones"):
                type.type("The CT scan shows a large stone in your ureter. " + red("Kidney stone") + ". We can try to let you pass it with pain meds, or blast it with ultrasound.")
                print()
            
            # CARDIOVASCULAR
            if self.has_status("Blood Pressure Crisis"):
                type.type("Your blood pressure is dangerously high. " + red("Hypertensive emergency") + ". IV medication to bring it down slowly. Any faster and you could stroke.")
                print()
            if self.has_status("DVT"):
                type.type("Ultrasound shows a blood clot in your leg. " + red("Deep vein thrombosis") + ". Blood thinners immediately. If it moves to your lungs, it's fatal.")
                print()
            
            # ALLERGIC
            if self.has_status("Anaphylaxis"):
                type.type("You're in anaphylactic shock! Epinephrine NOW! Airway management! " + red("Severe allergic reaction") + " - this is life or death!")
                print()
            
            # NEUROLOGICAL
            if self.has_status("Severe Migraine"):
                type.type("This migraine has you completely incapacitated. " + red("Status migrainosus") + ". Dark room, IV anti-inflammatories, anti-nausea medication.")
                print()
            if self.has_status("Vertigo"):
                type.type("The spinning sensation, the nausea... " + red("Vestibular disorder") + ". Could be inner ear, could be neurological. Let's do some tests.")
                print()
            if self.has_status("Seizure Disorder"):
                type.type("You had a grand mal seizure. This is serious - " + red("epilepsy") + " perhaps. We need an EEG, brain imaging, and to start you on anti-seizure medication.")
                print()
            
            # METABOLIC
            if self.has_status("Uncontrolled Diabetes"):
                type.type("Your blood sugar is through the roof. " + red("Diabetic ketoacidosis") + " if we don't act. Insulin, fluids, monitoring.")
                print()
            if self.has_status("Severe Dehydration"):
                type.type("You're dangerously dehydrated. Skin turgor is poor, heart is racing. " + red("Severe dehydration") + ". Multiple IV bags for you.")
                print()
            if self.has_status("Malnutrition"):
                type.type("You're severely malnourished. Vitamin deficiencies, muscle wasting... " + red("Malnutrition") + ". We need to refeed you carefully to avoid complications.")
                print()
            if self.has_status("Heat Stroke"):
                type.type("Your body temperature is critical. " + red("Heat stroke") + ". Ice packs, cooling blankets, IV fluids. We need to get you down below 104.")
                print()
            if self.has_status("Hypothermia"):
                type.type("Core temperature is dangerously low. " + red("Hypothermia") + ". Warm IV fluids, heating blankets. Slowly - too fast can stop your heart.")
                print()
            
            # TOXICOLOGY
            if self.has_status("Needle Exposure"):
                type.type("Needlestick injury - we need to test you for HIV, Hepatitis B and C. " + red("Post-exposure prophylaxis") + " if indicated. Follow-up testing for months.")
                print()
            if self.has_status("Mold Toxicity"):
                type.type("Chronic mold exposure. " + red("Toxic mold syndrome") + ". Remove yourself from the source, antifungals, and hope the lung damage isn't permanent.")
                print()
            if self.has_status("Lead Poisoning"):
                type.type("Your blood lead levels are toxic. " + red("Lead poisoning") + ". Chelation therapy to remove the heavy metal from your body.")
                print()
            if self.has_status("Asbestos Damage"):
                type.type("The fibers are embedded in your lungs. " + red("Asbestosis") + ". No cure. We monitor for mesothelioma and manage symptoms.")
                print()
            if self.has_status("Mercury Poisoning"):
                type.type("Mercury toxicity confirmed. " + red("Heavy metal poisoning") + ". Chelation therapy and pray the neurological damage isn't permanent.")
                print()
            
            # DENTAL
            if self.has_status("Tooth Abscess"):
                type.type("That abscess in your tooth is spreading. " + red("Dental infection") + ". Antibiotics, pain management, and you need a dentist to drain it.")
                print()
            
            # SEVERE INFECTIONS
            if self.has_status("Sepsis"):
                type.type("You're going septic. Blood pressure dropping, fever spiking. " + red("SEPSIS") + ". Broad-spectrum antibiotics, ICU admission. This kills people.")
                print()
            if self.has_status("Gangrene"):
                type.type("That tissue is dead and rotting. " + red("Gangrene") + ". We need to debride or... amputation may be the only option to save your life.")
                print()
            if self.has_status("Possible Rabies"):
                type.type("If you're showing symptoms, it may be too late. But let's try. " + red("Rabies") + " post-exposure treatment - series of shots. Pray it works.")
                print()
            
            # BURNS
            if self.has_status("Second Degree Burns"):
                type.type("These blisters are painful but should heal. " + red("Second degree burns") + ". Burn cream, bandaging, pain management. Watch for infection.")
                print()
            
            # MENTAL HEALTH
            if self.has_status("Anxiety Disorder"):
                type.type("Panic attacks, constant worry... " + red("Generalized anxiety disorder") + ". I can prescribe anti-anxiety medication and refer you to a therapist.")
                print()
            if self.has_status("Severe Depression"):
                type.type("This level of depression is serious. " + red("Major depressive disorder") + ". ")
                type.type("Antidepressants, therapy, and if you're having thoughts of self-harm, please tell me.")
                print()
            if self.has_status("Chronic Insomnia"):
                type.type("Chronic sleep deprivation is destroying your health. " + red("Insomnia") + ". Sleep study, sleep hygiene counseling, possibly medication.")
                print()
            if self.has_status("PTSD"):
                type.type("What you're experiencing - the flashbacks, the hypervigilance - it's " + red("PTSD") + ". Trauma therapy, possibly EMDR, medication to help manage symptoms.")
                print()
                
            # COMMON AILMENTS
            if self.has_status("Cold"):
                type.type("Just a common " + red("cold") + ". Rest, fluids, and you'll be fine in a week.")
                print()
            if self.has_status("Flu"):
                type.type("The " + red("flu") + " has got you. Antivirals if we caught it early, otherwise just rest and fluids.")
                print()
            if self.has_status("Sore Throat"):
                type.type("Your throat is inflamed. Just a " + red("sore throat") + ", not strep. Salt water gargles and rest.")
                print()
            if self.has_status("Ant Bites"):
                type.type("Those " + red("ant bites") + " look uncomfortable. Antihistamine cream should help with the itching.")
                print()
            
            print()
            type.type("Well, that seems to be everything. You still appear a little worse for wear, but this medicine should do the trick.")

        # Injury treatment - doctor removes one injury per visit
        if len(self._injuries) > 0:
            injury = random.choice(list(self._injuries))
            print()
            type.type("Hold on, let me take a closer look... that " + red(injury.lower()) + " needs attention.")
            print()
            type.type("Let me patch you up as best I can.")
            self.heal_injury(injury)
            if len(self._injuries) > 0:
                print()
                type.type("I've treated the worst of it. Your other injuries will need more visits, but you're heading in the right direction.")
            print()

        print("\n")
        self.heal(100)
        self.restore_sanity(random.choice([1, 2, 3]))  # Restores sanity
        type.type("You walk back to the front desk to checkout.")
        print("\n")
        cost = int((random.randint(30, 50)/100)*self._balance)
        if self.has_item("Flask of Anti-Virus"):
            type.type("You hand over the " + cyan(bright("Flask of Anti-Virus")) + ". The doctor holds it to the light.")
            print("\n")
            type.type(quote("This is... more advanced than anything we have here. I'd like to keep this for study."))
            print("\n")
            type.type("He scribbles something on your bill. Twenty percent off. You'll take it.")
            print("\n")
            cost = int(cost * 0.8)
        if self.has_item("First Aid Kit"):
            type.type("You set your " + cyan(bright("First Aid Kit")) + " on the examination table. The doctor raises an eyebrow.")
            print("\n")
            type.type(quote("You came prepared. Let's use what you've got — save the good stuff for someone who needs it."))
            print("\n")
            type.type("He patches you up with both kits. You leave feeling a little better than usual.")
            self.heal(10)
            print("\n")
        type.type("That will be " + bright(green("${:,}".format(cost))))
        if self.has_item("Real Insurance"):
            print("\n")
            type.type("You confidently present your " + bright(cyan("Real Insurance")) + " card to the receptionist.")
            print("\n")
            type.type("Oh, you have premium coverage! That covers everything. You're all set!")
            print()
            type.type("You walk out without paying a dime.")
            self.restore_sanity(10)
            self.update_faulty_insurance_durability()
            self.start_night()
            return
        elif self.has_item("Faulty Insurance"):
            print("\n")
            type.type("You show off your " + bright(magenta("Faulty Insurance")) + " to the lady, and put a convincing smile on your face. ")
            random_chance = random.randrange(10)
            if random_chance < 2:
                self.add_danger("Doctor Ban")
                print("\n")
                self.use_item("Faulty Insurance")
                type.type("Is this supposed to fool me? A fake insurance card? That's it, I'm calling the cops!")
                print("\n")
                type.type("Without hesitation, you turn, and run far, far away from the hospital, knowing that your face can't be seen there again.")
                print("\n")
                self.start_night()
                return
            else:
                print("\n")
                type.type("I see, you have insurance. Well, that should give you quite the discount.")
                print()
                cost = int((random.randint(10, 30)/100)*self._balance)
                type.type("That will be " + bright(green("${:,}".format(cost))))
                self.change_balance(-cost)
                self.update_faulty_insurance_durability()
                self.start_night()
                return
        else:
            self.change_balance(-cost)
            self.start_night()
            return


    # Witch Doctor's shop and interactions
    def visit_witch_doctor(self):
        self.increment_statistic("witch_doctor_visits")
        potions = self._lists.make_witch_inventory()
        type.type("You get in your car and drive to the Witch Doctor's Tower. ")
        print("\n")
        type.type("Muahahahahaha, hahahahahaha, HAHAHAHAHA!")
        print()
        type.type("Would you like me to HEAL you, HUMAN? ")
        while(True):
            yes_or_no = input("").lower()
            print()
            if((yes_or_no == "y") or (yes_or_no == "yes")):
                type.type("Now THATS what I LIKE to hear!")
                print("\n")
                type.type("You watch as the Witch goes from shelf to shelf, grabbing frog legs and horse hairs and bee carcasses, ")
                type.type("throwing them all into the black boiling pot. It begins to glow green, and the Witch looks pleased. ")
                print("\n")
                type.type("HAHAHAHAHA! DRINK this, my DEAR!")
                print("\n")
                type.type("You drink the strange concoction, and it burns in your stomach. Hopefully, it makes you feel better.")
                
                print("\n")

                random_chance = random.randrange(10)
                if random_chance < 5:
                    self._clear_status = True
                elif random_chance == 5:
                    self._clear_all_status = True

                random_chance = random.randrange(2)
                if random_chance == 0:
                    self.heal(100)
                
                cost = int((random.randint(5, 25)/100)*self._balance)
                type.type("YOU owe ME some of your green BILLS! I THINK that " + bright(green("${:,}".format(cost))) + " would SUFFICE!")
                self.change_balance(-cost)
                if len(potions)==0:
                    type.type("SORRY FOR YOU, but I'm simply out of FLASKS. No FLASKS means no POTIONS. Maybe try COMING BACK another DAY!")
                    print("\n")
                    self.start_night()
                    return
                else:
                    type.type("NOW, while I have YOU here, care to PURCHASE any of my POWERFUL POTIONS?")
                break
            elif((yes_or_no == "n") or (yes_or_no == "no")):
                type.type("HAHAH-oh what? You don't want MY help? That's QUITE UNFORTUNATE!")
                print("\n")
                if len(potions)==0:
                    type.type("SORRY FOR YOU, but I'm simply out of FLASKS. No FLASKS means no POTIONS. Maybe try COMING BACK another DAY!")
                    print("\n")
                    self.start_night()
                    return
                else:
                    type.type("WELL, are YOU in the MOOD to spend some MONEY on my MAGIC POTIONS?")
                    break
            else:
                type.type("WHAT did you SAY? ")

        print()

        no_bust_price = 0
        imminent_blackjack_price = 0
        dealers_whispers_price = 0
        bonus_fortune_price = 0
        antivenom_price = 0
        antivirus_price = 0
        fortunate_day_price = 0
        fortunate_night_price = 0
        second_chance_price = 0
        split_serum_price = 0
        dealers_hesitation_price = 0
        pocket_aces_price = 0
        while(True):
            for i in range(len(potions)+1):
                if(i<len(potions)):
                    type.type(str(i+1) + ". Flask of " + potions[i])
                    time.sleep(0.5)
                    print()
                else:
                    type.type(str(i+1) + ". I'm not buying anything")
                    time.sleep(0.5)
                    print()

            if(self.len_flasks()==1):
                type.type("NOW, I'm not ONE to JUDGE, but MIXING potions can be RISKY BUSINESS. Don't BLAME ME if you feel SICK.")
                print()
            elif(self.len_flasks()==2):
                type.type("SO, you're TEETERING on DANGEROUS levels of potion in your BLOOD. Proceed with CAUTON.")
                print()
            elif(self.len_flasks()>=3):
                type.type("ANY additional POTIONS in YOUR SYSTEM is ENTIRELY YOUR DECISION, and A BAD ONE AT THAT BUT I'M NOT YOU. Just please don't DIE on my CARPETS.")
                print()
            type.type("CHOOSE a number: ")
            while True:
                choice = None
                while choice is None:
                    try:
                        choice = int(input())
                    except ValueError:
                        type.type("Choose A number: ")
                if(1<=choice<=len(potions)):
                    potion = potions[choice-1]
                    break
                elif choice==len(potions)+1:
                    potion = "Home"
                    break
                else:
                    choice = None
                    type.type("I DONT have that NUMBER!")
                    print()
                    type.type("Choose a NUMBER: ")

            print()

            if potion == "No Bust":
                type.type("AHHH, so YOU WANT the Flask of No Bust?")
                if no_bust_price == 0:
                    no_bust_price = random.choice([10000, 12000, 14000])
                price = no_bust_price
            elif potion == "Imminent Blackjack":
                type.type("I SEE, so YOU WANT the Flask of Imminent Blackjack?")
                if imminent_blackjack_price == 0:
                    imminent_blackjack_price = random.choice([16000, 19000, 22000])
                price = imminent_blackjack_price
            elif potion == "Dealer's Whispers":
                type.type("HAHAHA, so YOU WANT the Flask of Dealer's Whispers?")
                if dealers_whispers_price == 0:
                    dealers_whispers_price = random.choice([10000, 12000, 14000])
                price = dealers_whispers_price
            elif potion == "Bonus Fortune":
                type.type("OOOOOOOOHHH, so YOU WANT the Flask of Bonus Fortune?")
                if bonus_fortune_price == 0:
                    bonus_fortune_price = random.choice([13000, 16000, 19000])
                price = bonus_fortune_price
            elif potion == "Anti-Venom":
                type.type("OF COURSEEEE, YOU WANT the Flask of Anti-Venom?")
                if antivenom_price == 0:
                    antivenom_price = random.choice([9000, 10000, 12000])
                price = antivenom_price
            elif potion == "Anti-Virus":
                type.type("AH-HA, YOU WANT the Flask of Anti-Virus?")
                if antivirus_price == 0:
                    antivirus_price = random.choice([10000, 11000, 12000])
                price = antivirus_price
            elif potion == "Fortunate Day":
                type.type("HEHEHAHAIHEHIA, so YOU WANT the Flask of Fortunate Day?")
                if fortunate_day_price == 0:
                    fortunate_day_price = random.choice([4000, 5000, 6000])
                price = fortunate_day_price
            elif potion == "Fortunate Night":
                type.type("MUAHAHAHAHA, so YOU WANT the Flask of Fortunate Night?")
                if fortunate_night_price == 0:
                    fortunate_night_price = random.choice([4000, 5000, 7000])
                price = fortunate_night_price
            elif potion == "Second Chance":
                type.type("OHOHOHOHO, so YOU WANT the Flask of Second Chance?")
                if second_chance_price == 0:
                    second_chance_price = random.choice([11000, 13000, 15000])
                price = second_chance_price
            elif potion == "Split Serum":
                type.type("YESYESYES, so YOU WANT the Flask of Split Serum?")
                if split_serum_price == 0:
                    split_serum_price = random.choice([11000, 14000, 16000])
                price = split_serum_price
            elif potion == "Dealer's Hesitation":
                type.type("MUEHEHEHE, so YOU WANT the Flask of Dealer's Hesitation?")
                if dealers_hesitation_price == 0:
                    dealers_hesitation_price = random.choice([8000, 9000, 11000])
                price = dealers_hesitation_price
            elif potion == "Pocket Aces":
                type.type("OOOOOH LALA, so YOU WANT the Flask of Pocket Aces?")
                if pocket_aces_price == 0:
                    pocket_aces_price = random.choice([17000, 19000, 22000])
                price = pocket_aces_price
            else: 
                type.type("Then OUR BUSINESS has been SETTLED. Be GONE. GOODBYE! COME AGAIN!")
                print("\n")
                self.start_night()
                return

            print()

            type.type("I SUPPOSE I can PART WAYS with THIS for " + green(bright("${:,}".format(price))) + ". What do YOU think? ")
            
            while True:
                yes_or_no = input("").lower()
                if ((yes_or_no == "y") or (yes_or_no == "yes")) and (self._balance<price):
                    print()
                    type.type("YOUR WALLETS are far too SMALL for this TRANSACTION.")
                    print("\n")
                    type.type("PERHAPS one of the OTHER potions?")
                    break
                elif (yes_or_no == "y") or (yes_or_no == "yes"):
                    print()
                    type.type("HAHAHAHAHAHAHAHAHA! YES! YES!")
                    self.change_balance(-price)
                    self.add_flask(potion)
                    potions.pop(choice-1)
                    type.type("You got the " + magenta(bright("Flask of " + potion)) + "!")
                    print()
                    type.type("Description: " + self.get_item_desc(potion))
                    print("\n")
                    if(self.len_flasks()==1):
                        type.type("You chug the potion, and begin to feel warm inside.")
                        print("\n")
                    elif(self.len_flasks()==2):
                        type.type("You chug the potion, and feel a bit dizzy. Maybe no more potions.")
                        print("\n")
                    elif(self.len_flasks()>=3):
                        type.type("You chug the potion, and feel really, really awful.")
                        random_chance = random.randrange(2)
                        if random_chance == 0:
                            self._flask_effects = set()
                            print("\n")
                            type.type("You stumble back and forth, on the verge of fainting. You puke all over the floor.")
                            print("\n")
                            type.type("NOOOO, NOT ON THE CARPETS! WHAT did I SAY! NO MORE. NO MORE. YOU are DONE for TODAY. OUT, NOW.")
                            print("\n")
                            type.type("As you walk out, you feel your body begin to weaken. ")
                            type.type("After all that, it seems the potions you had injested are now laying in a puddle on the floor of the Witch Doctor's tower. ")
                            print("\n")
                            self.start_night()
                            return
                        
                        damage = random.choice([10, 12, 15, 20, 30, 40])
                        if damage >= self._health:
                            print("\n")
                            type.slow(red("Your vision starts turning red, then green, then purple. "))
                            type.slow(red("Panicking, you run around the room, desperate to find an antidote. "))
                            type.slow(red("You begin drinking potion, after potion, to no avail. "))
                            type.slow(red("You can hear the Witch cackling in the background of your ringing ears, and slowly, you fall to the ground. "))
                            type.slow(red("Your face rests on the soft carpet. It's so cozy. Too cosy. "))
                            type.slow(red("Is that God? Yes, I think I can hear him! God! God! "))
                            type.slow(red("My goodness, he's real! God begins to decend from the roof hundreds of feet above you, and as he slowly glides down the tower, "))
                            type.slow(red("you get a closer look at his figure. A golden ring surrounds his body, and his white cloak is long and elegant. "))
                            print("\n")
                            type.slow(red(bright("As God decends, he looks you in the eyes, and you watch his face melt in front of you, his skin dripping onto your skin. ")))
                            type.slow(red(bright("It burns, and all you can do is sit with the pain and agony as your body slowly shuts down.")))
                            self.kill()
                        else:
                            print("\n")
                            self.hurt(damage)
                            self.lose_sanity(random.choice([4, 5, 6]))  # Potion-induced hallucinations drain sanity

                    if len(potions)==0:
                        type.type("YOU bought EVERYTHING! How EXCITING! I suppose we're DONE exchanging GOODS! GOODBYE NOW!")
                        print("\n")
                        self.start_night()
                        return
                    else:
                        type.type("OOOOH YES! Capitalism is FUN! I WANT MORE! MORE!")
                        print()
                    break
                elif (yes_or_no == "n") or (yes_or_no == "no"):
                    print()
                    type.type("OK OK I see how IT IS! ")
                    print("\n")
                    type.type("PERHAPS a DIFFERENT potion?")
                    print()
                    break
                else:
                    print()
                    type.type("GIVE me an ANSWER! ")


    # Tom's shop and interactions
    def tom_dialogue(self):
        if self._mechanic_visits == 0:
            type.type(quote("Well howdy there, stranger! Name's Tom. Welcome to Tom's Trusty Trucks and Tires!"))
            print("\n")
            type.type("The old mechanic wipes his hands on a rag that's seen better days. ")
            type.type("His eyes are kind, but tired. The kind of tired that comes from years of hard work and harder choices.")
            print("\n")
            type.type(quote("You got the look of a man runnin' from somethin'. I seen it before. Hell, I been there myself."))
            print("\n")
            type.type("He gestures to a faded photograph on the wall. A younger Tom, standing with a woman and two small children.")
            print("\n")
            type.type(quote("Family's a funny thing, yunno? You don't realize what you got 'til it's gone. "))
            type.type(quote("Spent years chasin' money, chasin' dreams. Almost lost everything that mattered."))
            print("\n")
            type.type("He taps the photo frame with a calloused finger.")
            print("\n")
            type.type(quote("But it ain't never too late to go back. That's what I learned. It ain't never too late to pick up the phone and say sorry."))
            print("\n")
            type.type("He looks at you with something like recognition.")
            print("\n")
            type.type(quote("Anyway. What can I do for ya today?"))
        elif self._mechanic_visits == 1:
            type.type(quote("Hey there! Good to see ya again. You stayin' outta trouble?"))
            print("\n")
            type.type("Tom chuckles, but there's concern in his eyes.")
            print("\n")
            type.type(quote("You know, I been meanin' to ask... you got anyone waitin' for ya back home? Someone who might be worryin'?"))
        elif self._mechanic_visits == 2:
            type.type(quote("There he is! My favorite customer!"))
            print("\n")
            type.type("Tom's smile fades slightly as he looks at you.")
            print("\n")
            type.type(quote("You look tired, friend. Real tired. You been sleepin' alright? Eatin'?"))
            print("\n")
            type.type("He shakes his head.")
            print("\n")
            type.type(quote("I worry about you, yunno. Reminds me of myself, back when I was lost. Just... don't forget what's important, alright?"))
        elif self._mechanic_visits >= 3:
            type.type(quote("Welcome back, friend."))
            print("\n")
            type.type("Tom's voice is softer now. More serious.")
            print("\n")
            type.type(quote("Listen... I found somethin' the other day. A phone. Fell outta your car when you was here last. Someone's been callin' it. A lot."))
            print("\n")
            type.type("He looks at you with those tired, kind eyes.")
            print("\n")
            type.type(quote("I ain't one to pry, but... whoever's callin', they sound real worried. Real sad. Maybe you should think about pickin' up."))

    def visit_tom(self):
        self.increment_statistic("mechanic_visits")
        days_elapsed = self.get_days_elapsed("Mechanic")
        self.mark_day("Mechanic")
        type.type("You get in your car and drive to Tom's Trusty Trucks and Tires. ")
        print("\n")
        self.tom_dialogue()
        print("\n")
        repairing_items_len = len(self._repairing_inventory)
        if(repairing_items_len>0):
            if days_elapsed == 3:
                type.type("You've been gone a while. Honestly, I forgot about ya stuff. Just come back soon, and I'll get to it.")
                print("\n")
            else:
                type.type("You left me some items to fix up since I last saw you. Here's the rundown:")
                print("\n")
                repairing_items = self._lists.make_repairing_items_list()
                for item in repairing_items:
                    if item == "Delight Indicator":
                        random_chance = random.randrange(2)
                        if random_chance == 0:
                            type.type("I managed to get this Delight Indicator up and running for ya. Just took a few new wires.")
                            self.fix_item(item)
                            print("\n")
                            type.type("Your " + magenta(bright(item)) + " has been fixed!")
                            print("\n")
                    elif item == "Health Indicator":
                        random_chance = random.randrange(2)
                        if random_chance == 0:
                            type.type("I somehow managed to get this Health Indicator workin'. Just took a few new screws.")
                            self.fix_item(item)
                            print("\n")
                            type.type("Your " + magenta(bright(item)) + " has been fixed!")
                            print("\n")
                    elif item == "Dirty Old Hat":
                        random_chance = random.randrange(2)
                        if random_chance == 0:
                            type.type("This Dirty Old Hat has never looked cleaner! If that's what you want, at least.")
                            self.fix_item(item)
                            print("\n")
                            type.type("Your " + magenta(bright(item)) + " has been fixed!")
                            print("\n")
                    elif item == "Golden Watch":
                        random_chance = random.randrange(2)
                        if random_chance == 0:
                            type.type("I put new gears in your Golden Watch. Should tell the time now.")
                            self.fix_item(item)
                            print("\n")
                            type.type("Your " + magenta(bright(item)) + " has been fixed!")
                            print("\n")
                    elif item == "Faulty Insurance":
                        random_chance = random.randrange(2)
                        if random_chance == 0:
                            type.type("Against my better judgement, I touched up your Faulty Insurance card. If it'll work, well, my guess is as good as yours.")
                            self.fix_item(item)
                            print("\n")
                            type.type("Your " + magenta(bright(item)) + " has been fixed!")
                            print("\n")
                    elif item == "Sneaky Peeky Shades":
                        random_chance = random.randrange(2)
                        if random_chance == 0:
                            type.type("I replaced the frame in your Sneaky Peeky Shades, so now you can see out of them.")
                            self.fix_item(item)
                            print("\n")
                            type.type("Your " + magenta(bright(item)) + " have been fixed!")
                            print("\n")
                    elif item == "Quiet Sneakers":
                        random_chance = random.randrange(2)
                        if random_chance == 0:
                            type.type("I relaced these Quiet Sneakers, so you can run again.")
                            self.fix_item(item)
                            print("\n")
                            type.type("Your " + magenta(bright(item)) + " have been fixed!")
                            print("\n")
                    elif item == "Lucky Coin":
                        random_chance = random.randrange(2)
                        if random_chance == 0:
                            type.type("Gave this Lucky Coin a good polish. She's shining bright again!")
                            self.fix_item(item)
                            print("\n")
                            type.type("Your " + magenta(bright(item)) + " has been fixed!")
                            print("\n")
                    elif item == "Worn Gloves":
                        random_chance = random.randrange(2)
                        if random_chance == 0:
                            type.type("I patched up these Worn Gloves with some spare leather I had lyin' around.")
                            self.fix_item(item)
                            print("\n")
                            type.type("Your " + magenta(bright(item)) + " have been fixed!")
                            print("\n")
                    elif item == "Tattered Cloak":
                        random_chance = random.randrange(2)
                        if random_chance == 0:
                            type.type("My wife sewed up all the holes in your Tattered Cloak. Good as new, yunno!")
                            self.fix_item(item)
                            print("\n")
                            type.type("Your " + magenta(bright(item)) + " has been fixed!")
                            print("\n")
                    elif item == "Rusty Compass":
                        random_chance = random.randrange(2)
                        if random_chance == 0:
                            type.type("I oiled up this Rusty Compass and replaced the glass. Points north again!")
                            self.fix_item(item)
                            print("\n")
                            type.type("Your " + magenta(bright(item)) + " has been fixed!")
                            print("\n")
                    elif item == "Pocket Watch":
                        random_chance = random.randrange(2)
                        if random_chance == 0:
                            type.type("I tinkered with your Pocket Watch and got all the gears turnin' again.")
                            self.fix_item(item)
                            print("\n")
                            type.type("Your " + magenta(bright(item)) + " has been fixed!")
                            print("\n")

                if len(self._repairing_inventory) == repairing_items_len:
                    type.type("Yesterday was a long one, and I retired to home early to see my wife and the girlies. ")
                    type.type("Didn't get much progress on your things, but I assure you, they'll be fixed before you know it.")
                elif len(self._repairing_inventory) > 1:
                    type.type("I've still got " + str(len(self._repairing_inventory)) + " items of yours that I'm still looking at. ")
                    type.type("Just swing by tomorrow, and hopefully I'll have them done.")
                elif len(self._repairing_inventory) == 1:
                    type.type("I've still got " + str(len(self._repairing_inventory)) + " item of yours that I'm still looking at. ")
                    type.type("Just swing by tomorrow, and hopefully I'll have it done.")
                elif len(self._repairing_inventory) == 0:
                    type.type("That should be everything you left with me. Hopefully everything's up to snuff and good as new, ya know!")
                print("\n")

        if(len(self._broken_inventory)>0):
            broken_items = self._lists.make_broken_items_list()
            delight_indicator_price = 0
            health_indicator_price = 0
            dirty_old_hat_price = 0
            golden_watch_price = 0
            faulty_insurance_price = 0
            sneaky_peeky_glasses_price = 0
            quiet_sneakers_price = 0
            lucky_coin_price = 0
            worn_gloves_price = 0
            tattered_cloak_price = 0
            rusty_compass_price = 0
            pocket_watch_price = 0
            type.type("I see you came in here with some broken valuables. Mind if I take a look at em?")
            print()
            while(True):
                for i in range(len(broken_items)+1):
                    if(i<len(broken_items)):
                        type.type(str(i+1) + ". " + broken_items[i])
                        time.sleep(0.5)
                        print()
                    else:
                        type.type(str(i+1) + ". I'm all set")
                        time.sleep(0.5)
                        print()
                type.type("Choose a number: ")
                while True:
                    choice = None
                    while choice is None:
                        try:
                            choice = int(input())
                        except ValueError:
                            type.type("Choose a number: ")
                    if(1<=choice<=len(broken_items)):
                        item = broken_items[choice-1]
                        break
                    elif choice==len(broken_items)+1:
                        item = "Home"
                        break
                    else:
                        choice = None
                        type.type("You don't have an item with that number!")
                        print()
                        type.type("Choose a number: ")

                print()

                if item == "Delight Indicator":
                    type.type("You want me to fix that Delight Indicator of yours?")
                    if delight_indicator_price == 0:
                        delight_indicator_price = random.choice([4500, 5500, 6000])
                    price = delight_indicator_price
                elif item == "Health Indicator":
                    type.type("You want me to fix that Health Indicator for ya?")
                    if health_indicator_price == 0:
                        health_indicator_price = random.choice([4000, 4500, 5500])
                    price = health_indicator_price
                elif item == "Dirty Old Hat":
                    type.type("You want me to fix that Dirty Old Hat you got there?")
                    if dirty_old_hat_price == 0:
                        dirty_old_hat_price = random.choice([12500, 14000, 15000])
                    price = dirty_old_hat_price
                elif item == "Golden Watch":
                    type.type("You want me to fix that Golden Watch you're wearin'?")
                    if golden_watch_price == 0:
                        golden_watch_price = random.choice([15000, 16000, 17500])
                    price = golden_watch_price
                elif item == "Faulty Insurance":
                    type.type("Uhm, you want me to fix your Faulty Insurance card?")
                    if faulty_insurance_price == 0:
                        faulty_insurance_price = random.choice([5000, 5500, 6000])
                    price = faulty_insurance_price
                elif item == "Sneaky Peeky Shades":
                    type.type("You want me to fix those Sneaky Peeky Shades on your head?")
                    if sneaky_peeky_glasses_price == 0:
                        sneaky_peeky_glasses_price = random.choice([17000, 18000, 20000])
                    price = sneaky_peeky_glasses_price
                elif item == "Quiet Sneakers":
                    type.type("You want me to fix them there Quiet Sneakers you're rockin'?")
                    if quiet_sneakers_price == 0:
                       quiet_sneakers_price = random.choice([7500, 9000, 10000])
                    price = quiet_sneakers_price
                elif item == "Lucky Coin":
                    type.type("You want me to fix that Lucky Coin of yours?")
                    if lucky_coin_price == 0:
                        lucky_coin_price = random.choice([6000, 7000, 8000])
                    price = lucky_coin_price
                elif item == "Worn Gloves":
                    type.type("You want me to fix them Worn Gloves you got?")
                    if worn_gloves_price == 0:
                        worn_gloves_price = random.choice([9000, 10000, 11000])
                    price = worn_gloves_price
                elif item == "Tattered Cloak":
                    type.type("You want me to fix that Tattered Cloak of yours?")
                    if tattered_cloak_price == 0:
                        tattered_cloak_price = random.choice([11000, 12500, 14000])
                    price = tattered_cloak_price
                elif item == "Rusty Compass":
                    type.type("You want me to fix that Rusty Compass you're carryin'?")
                    if rusty_compass_price == 0:
                        rusty_compass_price = random.choice([4000, 5000, 6000])
                    price = rusty_compass_price
                elif item == "Pocket Watch":
                    type.type("You want me to fix that Pocket Watch of yours?")
                    if pocket_watch_price == 0:
                        pocket_watch_price = random.choice([10000, 11500, 13000])
                    price = pocket_watch_price
                else: 
                    type.type("Well then, I hope you have a great rest of your night. Stay safe now.")
                    print("\n")
                    self.start_night()
                    return

                print()

                if self.has_item("Tom's Wrench") and not self.has_met("Tom Wrench Discount"):
                    self.mark_met("Tom Wrench Discount")
                    type.type("Tom glances over at the " + magenta(bright("Tom's Wrench")) + " sitting in your bag. He does a slow double-take.")
                    print("\n")
                    type.type(quote("Hey... that's mine. Well — it was. How'd you end up with that?") + " He waves a hand before you can answer. " + quote("Nevermind. Keep it. 50% off today, just for bringin' her home."))
                    print("\n")
                    price = price // 2

                type.type("It'll take me a couple days, but I can do that for ya for " + green(bright("${:,}".format(price))) + ". Whaddya say? ")
                
                while True:
                    yes_or_no = input("").lower()
                    if ((yes_or_no == "y") or (yes_or_no == "yes")) and (self._balance<price):
                        print()
                        type.type("Aww man, sorry to tell you, but you just don't got enough funds for this, yunno?")
                        print("\n")
                        random_chance = random.randrange(2)
                        if random_chance == 0:
                            type.type("Ugh, man, I just hate seein' people in need of help and not gettin' it, ya hear? ")
                            type.type("Tell ya what, limited time offer, I'm giving out a special discount, just for you. ")
                            discount = random.choice([20, 25, 30, 35])
                            price = int(price - (price*(discount/100)))
                            type.type("Say yes right now, and I'll take " + str(discount) + "%" + " off your order.")
                            print("\n")
                            type.type("That means you're only payin' " + green(bright("${:,}".format(price))) + ". Could ya do that? ")

                            while True:
                                yes_or_no_2 = input("").lower()
                                if ((yes_or_no_2 == "y") or (yes_or_no_2 == "yes")) and (self._balance<price):
                                    print()
                                    type.type("Still can't afford it? That's tough luck, man. I really wish there was more I could do, ya know?")
                                    print("\n")
                                    type.type("Maybe you can fix up something else.")
                                    print()
                                    break
                                elif (yes_or_no == "y") or (yes_or_no == "yes"):
                                    print()
                                    type.type("Really? Awesome. Just leave this here with me, and let me wrench that baby back to life for ya.")
                                    self.change_balance(-price)
                                    self.repair_item(item)
                                    broken_items.pop(choice-1)
                                    type.type("Your " + magenta(bright(item)) + " is safe with Tom. Come back later to see if it's fixed!")
                                    print("\n")
                                    if len(broken_items)==0:
                                        type.type("Well, that appears to be everything, doesn't it? Thanks for letting me help ya out. Have a nice day, now.")
                                        print("\n")
                                        self.start_night()
                                        return
                                    else:
                                        type.type("Got anything else for me?")
                                        print()
                                        break
                                elif (yes_or_no_2 == "n") or (yes_or_no_2 == "no"):
                                    type.type("Really? Even with the discount? You do you, I suppose.")
                                    print("\n")
                                    type.type("Is there anything else I can fix for ya?")
                                    print()
                                    break
                                else:
                                    print()
                                    type.type("Couldn't hear ya. Whaddya say? ")
                            break
                        else:
                            broken_items.pop(choice-1)
                            type.type("Maybe you can afford to fix up somethin' else?")
                            print()
                        break
                    elif (yes_or_no == "y") or (yes_or_no == "yes"):
                        print()
                        type.type("Really? Awesome. Just leave this here with me, and let me wrench that baby back to life for ya.")
                        self.change_balance(-price)
                        self.repair_item(item)
                        broken_items.pop(choice-1)
                        type.type("Your " + magenta(bright(item)) + " is safe with Tom. Come back later to see if it's fixed!")
                        print("\n")
                        if len(broken_items)==0:
                            type.type("Well, that appears to be everything, doesn't it? Thanks for letting me help ya out. Have a nice day, now.")
                            print("\n")
                            self.start_night()
                            return
                        else:
                            type.type("Got anything else for me?")
                            print()
                        break
                    elif (yes_or_no == "n") or (yes_or_no == "no"):
                        print()
                        type.type("No dice? ")
                        random_chance = random.randrange(10)
                        if random_chance == 0:
                            type.type("You don't say. I mean, my prices are unbeatable. You know what, I'll prove it!")
                            print("\n")
                            type.type("Tell ya what, limited time offer, I'm giving out a special discount, just for you. ")
                            discount = random.choice([15, 20, 25])
                            price = int(price - (price*(discount/100)))
                            type.type("Say yes right now, and I'll take " + str(discount) + "%" + " off your order.")
                            print("\n")
                            type.type("That means you're only payin' " + green(bright("${:,}".format(price))) + ". You interested? ")
                            while True:
                                yes_or_no_2 = input("").lower()
                                if ((yes_or_no_2 == "y") or (yes_or_no_2 == "yes")) and (self._balance<price):
                                    print()
                                    type.type("You can't afford it? Really? That's tough luck, man. I really wish there was more I could do, ya know?")
                                    print("\n")
                                    type.type("Maybe you can fix up something else.")
                                    print()
                                    break
                                elif (yes_or_no_2 == "y") or (yes_or_no_2 == "yes"):
                                    print()
                                    type.type("Really? Awesome. Just leave this here with me, and let me wrench that baby back to life for ya.")
                                    self.change_balance(-price)
                                    self.repair_item(item)
                                    broken_items.pop(choice-1)
                                    type.type("Your " + magenta(bright(item)) + " is safe with Tom. Come back later to see if it's fixed!")
                                    print("\n")
                                    if len(broken_items)==0:
                                        type.type("Well, that appears to be everything, doesn't it? Thanks for letting me help ya out. Have a nice day, now.")
                                        print("\n")
                                        self.start_night()
                                        return
                                    else:
                                        type.type("Got anything else for me?")
                                        print()
                                        break
                                elif (yes_or_no_2 == "n") or (yes_or_no_2 == "no"):
                                    type.type("Really? No interest, whatsoever? Even with the discount? You do you, I suppose.")
                                    print("\n")
                                    type.type("Want me to fix anything else?")
                                    print()
                                    break
                                else:
                                    print()
                                    type.type("Couldn't hear ya. Whaddya say? ")
                            break
                        else:
                            type.type("That's alright, now.")
                            print("\n")
                            type.type("What about your other wares?")
                            print()
                            break
                    else:
                        print()
                        type.type("Couldn't hear ya. Whaddya say? ")

        self.start_night()
        return


    # Frank's shop and interactions
    def frank_dialogue(self):
        if self._mechanic_visits == 0:
            type.type(quote("The hell you want?"))
            print("\n")
            type.type("The man behind the counter doesn't look up from his newspaper. ")
            type.type("He's got tattoos crawling up his arms - some faded, some fresh. ")
            type.type("You catch a glimpse of something that looks like lightning bolts before he shifts his sleeve.")
            print("\n")
            type.type(quote("Name's Frank. This is my shop. My rules. You want somethin' fixed, I'll fix it. You want conversation, go find a therapist."))
            print("\n")
            type.type("He finally looks at you. His eyes are cold. Calculating.")
            print("\n")
            type.type(quote("You ain't from around here, are ya? Nah, I can tell. Got that look. The 'I'm just passin' through' look."))
            print("\n")
            type.type("He spits into a cup on the counter.")
            print("\n")
            type.type(quote("Well, long as you're passin' through MY town, you follow MY rules. "))
            type.type(quote("We got a way of doin' things here. A way of keepin' things... pure. Clean. You understand what I'm sayin'?"))
            print("\n")
            type.type("He doesn't wait for an answer.")
            print("\n")
            type.type(quote("That casino up on the hill. You been there, right? 'Course you have. Everyone goes there eventually. "))
            type.type(quote("That glass-eyed freak runnin' the place... he ain't one of us. Never will be. "))
            type.type(quote("Came here from God knows where, settin' up shop like he owns the place."))
            print("\n")
            type.type("Frank's jaw tightens.")
            print("\n")
            type.type(quote("One of these days, someone's gonna do somethin' about him. Someone's gonna remind him that this is OUR town."))
            print("\n")
            type.type("He waves his hand dismissively.")
            print("\n")
            type.type(quote("Anyway. What do you need?"))
        elif self._mechanic_visits == 1:
            type.type(quote("Oh, it's you again."))
            print("\n")
            type.type("Frank barely acknowledges you. In the back of the shop, you hear voices. Laughter. The rumble of motorcycle engines.")
            print("\n")
            type.type(quote("Got some friends over. Business associates, you might say. We're plannin' somethin' big."))
            print("\n")
            type.type("He grins. It's not a nice grin.")
            print("\n")
            type.type(quote("You keep comin' around, maybe I'll introduce you. Could always use another pair of hands. Another... believer."))
        elif self._mechanic_visits == 2:
            type.type(quote("Back again, huh? You're persistent, I'll give you that."))
            print("\n")
            type.type("Frank's watching you more carefully now. Like he's sizing you up.")
            print("\n")
            type.type(quote("You know, I been thinkin'. You and me, we ain't so different. "))
            type.type(quote("We both know what it's like to be overlooked. To be treated like shit by people who think they're better than us."))
            print("\n")
            type.type("He leans in closer. His breath smells like cigarettes and something sour.")
            print("\n")
            type.type(quote("The Dealer. He looks at you like you're nothin'. Like you're just another mark, another sucker to bleed dry. "))
            type.type(quote("Don't that make you angry? Don't that make you want to DO somethin' about it?"))
        elif self._mechanic_visits >= 3:
            type.type(quote("Well, well, well. Look who keeps crawlin' back."))
            print("\n")
            type.type("Frank's demeanor has changed. He's more confident. More dangerous.")
            print("\n")
            type.type(quote("You know, I been watchin' you. Talkin' to the boys about you. We think you got potential."))
            print("\n")
            type.type("He pulls out a worn leather jacket from under the counter. You can see patches on it. Symbols that make your stomach turn.")
            print("\n")
            type.type(quote("When you're ready to stop bein' a victim and start bein' a winner, you come find me. We'll take care of that Dealer problem once and for all."))
            print("\n")
            type.type("He tosses the jacket back under the counter.")
            print("\n")
            type.type(quote("Think about it."))

    def visit_frank(self):
        self.increment_statistic("mechanic_visits")
        days_elapsed = self.get_days_elapsed("Mechanic")
        self.mark_day("Mechanic")
        type.type("You get in your car and drive to Filthy Frank's Flawless Fixtures. ")
        print("\n")
        self.frank_dialogue()
        print("\n")
        if self.has_item("Frank's Flask") and not self.has_met("Frank Flask Bonus"):
            self.mark_met("Frank Flask Bonus")
            type.type("Frank's eyes drop to the " + magenta(bright("Frank's Flask")) + " on your belt. His jaw tightens.")
            print("\n")
            type.type(quote("Is that — ") + " He stops himself. Stares for a long beat. " + quote("Where'd you get that?"))
            print("\n")
            type.type("He clears his throat and looks away, like he didn't almost just have a moment.")
            print("\n")
            type.type(quote("Nevermind. Forget I said anything. ") + " He slides some folded bills across the counter without another word. " + quote("Call it a finder's fee."))
            print("\n")
            self.change_balance(100)
            self.restore_sanity(3)
            type.type(green("Frank gives you $100. ") + "Something about that flask mattered to him.")
            print("\n")
        repairing_items_len = len(self._repairing_inventory)
        if(repairing_items_len>0):
            if days_elapsed == 2:
                type.type("You didn't show up yesterday. That means I haven't looked at your stuff. Come back soon, and maybe I will have made some progress, yeah?")
                print("\n")
            else:
                type.type("You left me some of your trinkets. This is what I've got for you:")
                print("\n")
                repairing_items = self._lists.make_repairing_items_list()
                for item in repairing_items:
                    if item == "Delight Indicator":
                        random_chance = random.randrange(5)
                        if random_chance < 3:
                            type.type("With a couple new wires I got your Delight Indicator working.")
                            self.fix_item(item)
                            print("\n")
                            type.type("Your " + magenta(bright(item)) + " has been fixed!")
                            print("\n")
                        elif random_chance == 3:
                            type.type("Honestly, after one look at this Delight Indicator thingy, I gave up entirely. Take it back. No refunds.")
                            self.return_item(item)
                            print("\n")
                            type.type(red("Your broken " + (item) + " has been returned."))
                            print("\n")
                    elif item == "Health Indicator":
                        random_chance = random.randrange(5)
                        if random_chance < 3:
                            type.type("Tighted some screws and the Health Indicator started up again. Seems good? Just take it.")
                            self.fix_item(item)
                            print("\n")
                            type.type("Your " + magenta(bright(item)) + " has been fixed!")
                            print("\n")
                        elif random_chance == 3:
                            type.type("Get that the fuck out my face with that fancy wizard crap. This Health Indicator thing is too complicated. No refunds.")
                            self.return_item(item)
                            print("\n")
                            type.type(red("Your broken " + (item) + " has been returned."))
                            print("\n")
                    elif item == "Dirty Old Hat":
                        random_chance = random.randrange(5)
                        if random_chance < 3:
                            type.type("I gave this Dirty Old Hat to my wife, and after enough convincing, she sewed it back up.")
                            self.fix_item(item)
                            print("\n")
                            type.type("Your " + magenta(bright(item)) + " has been fixed!")
                            print("\n")
                        elif random_chance == 3:
                            type.type("You gave me a Dirty Old Hat and asked me to fix it. What did you expect? No refunds.")
                            self.return_item(item)
                            print("\n")
                            type.type(red("Your broken " + (item) + " has been returned."))
                            print("\n")
                    elif item == "Golden Watch":
                        random_chance = random.randrange(5)
                        if random_chance < 3:
                            type.type("All I had to do was tap the watch face with my finger and it started ticking again, so I'd say that's a job well done.")
                            self.fix_item(item)
                            print("\n")
                            type.type("Your " + magenta(bright(item)) + " has been fixed!")
                            print("\n")
                        elif random_chance == 3:
                            type.type("I looked at the watch, spun all the gears and clicked all the buttons, but nothing worked. Sorry dude. No refunds.")
                            self.return_item(item)
                            print("\n")
                            type.type(red("Your broken " + (item) + " has been returned."))
                            print("\n")
                    elif item == "Faulty Insurance":
                        random_chance = random.randrange(5)
                        if random_chance < 3:
                            type.type("My guy was around last night, and he looked at your Faulty Insurance card. Should work again.")
                            self.fix_item(item)
                            print("\n")
                            type.type("Your " + magenta(bright(item)) + " has been fixed!")
                            print("\n")
                        elif random_chance == 3:
                            type.type("I've been calling my guy, but he won't answer. I can't fix your Faulty Insurance card. Take it back. No refunds.")
                            self.return_item(item)
                            print("\n")
                            type.type(red("Your broken " + (item) + " has been returned."))
                            print("\n")
                    elif item == "Sneaky Peeky Shades":
                        random_chance = random.randrange(5)
                        if random_chance < 3:
                            type.type("A little mouth water vapor and my shirt was more than enough to polish up the Sneaky Peeky Shades you gave me.")
                            self.fix_item(item)
                            print("\n")
                            type.type("Your " + magenta(bright(item)) + " have been fixed!")
                            print("\n")
                        elif random_chance == 3:
                            type.type("I ain't no opotometigist. These Sneaky Peeky Shades, well, they are glasses. I fix cars. No refunds.")
                            self.return_item(item)
                            print("\n")
                            type.type(("Your broken " + red(bright(item)) + " have been returned."))
                            print("\n")
                    elif item == "Quiet Sneakers":
                        random_chance = random.randrange(5)
                        if random_chance < 3:
                            type.type("I gave your Quiet Sneakers to my son Kyle, and ran around the yard all day yesterday. Should've broken them in for ya.")
                            self.fix_item(item)
                            print("\n")
                            type.type("Your " + magenta(bright(item)) + " have been fixed!")
                            print("\n")
                        elif random_chance == 3:
                            type.type("These Quiet Sneakers reek like hell. Please take them. No refunds.")
                            self.return_item(item)
                            print("\n")
                            type.type(red("Your broken " + (item) + " have been returned."))
                            print("\n")
                    elif item == "Lucky Coin":
                        random_chance = random.randrange(5)
                        if random_chance < 3:
                            type.type("I let Kyle use your Lucky Coin for his piggy bank for a bit. He cried when I took it back. You're welcome.")
                            self.fix_item(item)
                            print("\n")
                            type.type("Your " + magenta(bright(item)) + " has been fixed!")
                            print("\n")
                        elif random_chance == 3:
                            type.type("I tried flipping this Lucky Coin and it landed in a storm drain. Fished it out but now it smells like sewer. No refunds.")
                            self.return_item(item)
                            print("\n")
                            type.type(red("Your broken " + (item) + " has been returned."))
                            print("\n")
                    elif item == "Worn Gloves":
                        random_chance = random.randrange(5)
                        if random_chance < 3:
                            type.type("I been using these Worn Gloves to change oil all week. They're real broken in now. Might smell a little funky.")
                            self.fix_item(item)
                            print("\n")
                            type.type("Your " + magenta(bright(item)) + " have been fixed!")
                            print("\n")
                        elif random_chance == 3:
                            type.type("I ain't no seamstress. These Worn Gloves got fingers falling off. That's a wife problem. She said no. No refunds.")
                            self.return_item(item)
                            print("\n")
                            type.type(red("Your broken " + (item) + " have been returned."))
                            print("\n")
                    elif item == "Tattered Cloak":
                        random_chance = random.randrange(5)
                        if random_chance < 3:
                            type.type("Kyle's been using your Tattered Cloak as a superhero cape. Duct taped the holes shut. Kid knows what he's doing.")
                            self.fix_item(item)
                            print("\n")
                            type.type("Your " + magenta(bright(item)) + " has been fixed!")
                            print("\n")
                        elif random_chance == 3:
                            type.type("My dog got ahold of this Tattered Cloak and made it worse. Way worse. I'm not apologizing. No refunds.")
                            self.return_item(item)
                            print("\n")
                            type.type(red("Your broken " + (item) + " has been returned."))
                            print("\n")
                    elif item == "Rusty Compass":
                        random_chance = random.randrange(5)
                        if random_chance < 3:
                            type.type("I dunked this Rusty Compass in a bucket of Coca-Cola overnight. Don't ask why it works, it just does.")
                            self.fix_item(item)
                            print("\n")
                            type.type("Your " + magenta(bright(item)) + " has been fixed!")
                            print("\n")
                        elif random_chance == 3:
                            type.type("This Rusty Compass keeps pointing at my fridge. I think it's haunted. Get it outta here. No refunds.")
                            self.return_item(item)
                            print("\n")
                            type.type(red("Your broken " + (item) + " has been returned."))
                            print("\n")
                    elif item == "Pocket Watch":
                        random_chance = random.randrange(5)
                        if random_chance < 3:
                            type.type("I smacked your Pocket Watch against the counter real hard and it started ticking again. That'll be full price.")
                            self.fix_item(item)
                            print("\n")
                            type.type("Your " + magenta(bright(item)) + " has been fixed!")
                            print("\n")
                        elif random_chance == 3:
                            type.type("I opened up this Pocket Watch and a bunch of tiny gears flew everywhere. Kyle vacuumed 'em up. No refunds.")
                            self.return_item(item)
                            print("\n")
                            type.type(red("Your broken " + (item) + " has been returned."))
                            print("\n")

                if len(self._repairing_inventory) == repairing_items_len:
                    type.type("I didn't fix a damn thing of yours, and I ain't afraid to show it. ")
                    type.type("Look at this box. It has all the stuff you gave me. It hasn't moved since you gave me it. Now scram, hard work takes time.")
                elif len(self._repairing_inventory) > 1:
                    type.type("That leaves " + str(len(self._repairing_inventory)) + " items of yours still in my posession. ")
                    type.type("Just swing by tomorrow, and I'll do my best to finish them up.")
                elif len(self._repairing_inventory) == 1:
                    type.type("That leaves " + str(len(self._repairing_inventory)) + " item of yours still in my posession. Just swing by tomorrow, and I'll do my best to finish it up.")
                elif len(self._repairing_inventory) == 0:
                    type.type("That's all your junk, fixed better than the best. Enjoy it while it lasts.")
                print("\n")

        if(len(self._broken_inventory)>0):
            broken_items = self._lists.make_broken_items_list()
            delight_indicator_price = 0
            health_indicator_price = 0
            dirty_old_hat_price = 0
            golden_watch_price = 0
            faulty_insurance_price = 0
            sneaky_peeky_glasses_price = 0
            quiet_sneakers_price = 0
            lucky_coin_price = 0
            worn_gloves_price = 0
            tattered_cloak_price = 0
            rusty_compass_price = 0
            pocket_watch_price = 0
            type.type("You have some broken things for me. Come on, don't be shy. Let me take a whack at them.")
            print()
            while(True):
                for i in range(len(broken_items)+1):
                    if(i<len(broken_items)):
                        type.type(str(i+1) + ". " + broken_items[i])
                        time.sleep(0.5)
                        print()
                    else:
                        type.type(str(i+1) + ". I'm all set")
                        time.sleep(0.5)
                        print()
                type.type("Choose a number: ")
                while True:
                    choice = None
                    while choice is None:
                        try:
                            choice = int(input())
                        except ValueError:
                            type.type("Choose a number: ")
                    if(1<=choice<=len(broken_items)):
                        item = broken_items[choice-1]
                        break
                    elif choice==len(broken_items)+1:
                        item = "Home"
                        break
                    else:
                        choice = None
                        type.type("Did I stutter?")
                        print()
                        type.type("Choose a number: ")

                print()

                if item == "Delight Indicator":
                    type.type("You need me to repair your Delight Indicator?")
                    if delight_indicator_price == 0:
                        delight_indicator_price = random.choice([4000, 4250, 4500, 5500, 6000, 9000])
                    price = delight_indicator_price
                elif item == "Health Indicator":
                    type.type("You need me to repair that Health Indicator?")
                    if health_indicator_price == 0:
                        health_indicator_price = random.choice([3000, 3200, 4000, 4500, 5500, 7000])
                    price = health_indicator_price
                elif item == "Dirty Old Hat":
                    type.type("You need me to repair the Dirty Old Hat you have?")
                    if dirty_old_hat_price == 0:
                        dirty_old_hat_price = random.choice([10000, 10500, 12500, 14000, 15000, 17000])
                    price = dirty_old_hat_price
                elif item == "Golden Watch":
                    type.type("You need me to repair that Golden Watch on your wrist?")
                    if golden_watch_price == 0:
                        golden_watch_price = random.choice([13000, 14000, 15000, 16000, 17500, 19500])
                    price = golden_watch_price
                elif item == "Faulty Insurance":
                    type.type("You need me to touch up your Faulty Insurance card?")
                    if faulty_insurance_price == 0:
                        faulty_insurance_price = random.choice([3500, 4000, 5000, 5500, 6000, 7000])
                    price = faulty_insurance_price
                elif item == "Sneaky Peeky Shades":
                    type.type("You need me to repair those Sneaky Peeky Shades over your eyes?")
                    if sneaky_peeky_glasses_price == 0:
                        sneaky_peeky_glasses_price = random.choice([15500, 16500, 17000, 18000, 20000, 25000])
                    price = sneaky_peeky_glasses_price
                elif item == "Quiet Sneakers":
                    type.type("You need me to repair those Quiet Sneakers you're wearing?")
                    if quiet_sneakers_price == 0:
                       quiet_sneakers_price = random.choice([6000, 6500, 7500, 9000, 10000, 12000])
                    price = quiet_sneakers_price
                elif item == "Lucky Coin":
                    type.type("You need me to buff out that Lucky Coin?")
                    if lucky_coin_price == 0:
                        lucky_coin_price = random.choice([5000, 5500, 6000, 7000, 8000, 10000])
                    price = lucky_coin_price
                elif item == "Worn Gloves":
                    type.type("You need me to patch up those Worn Gloves?")
                    if worn_gloves_price == 0:
                        worn_gloves_price = random.choice([7500, 8000, 9000, 10000, 11000, 13000])
                    price = worn_gloves_price
                elif item == "Tattered Cloak":
                    type.type("You need me to stitch up that Tattered Cloak?")
                    if tattered_cloak_price == 0:
                        tattered_cloak_price = random.choice([9000, 10000, 11000, 12500, 14000, 16000])
                    price = tattered_cloak_price
                elif item == "Rusty Compass":
                    type.type("You need me to oil up that Rusty Compass?")
                    if rusty_compass_price == 0:
                        rusty_compass_price = random.choice([3000, 3500, 4000, 5000, 6000, 7500])
                    price = rusty_compass_price
                elif item == "Pocket Watch":
                    type.type("You need me to tinker with that Pocket Watch?")
                    if pocket_watch_price == 0:
                        pocket_watch_price = random.choice([8500, 9000, 10000, 11500, 13000, 15000])
                    price = pocket_watch_price
                else: 
                    type.type("Well then I've done all I can do. Stay out of trouble, now.")
                    print("\n")
                    self.start_night()
                    return
                
                print()

                type.type("I can fix this up for like " + green(bright("${:,}".format(price))) + ". You game? ")
                
                while True:
                    yes_or_no = input("").lower()
                    if ((yes_or_no == "y") or (yes_or_no == "yes")) and (self._balance<price):
                        print()
                        type.type("Are you tryna rip me off? Nah man, I'm just kidding. But seriously, don't mess with me like that.")
                        print("\n")
                        broken_items.pop(choice-1)
                        type.type("Am I repairing something for you or what?")
                        break
                    elif (yes_or_no == "y") or (yes_or_no == "yes"):
                        print()
                        type.type("Darn tootin! Lemme just take this from you, and sooner or later I'll wield my hammer and do my thing.")
                        self.change_balance(-price)
                        self.repair_item(item)
                        broken_items.pop(choice-1)
                        type.type("Your " + magenta(bright(item)) + " is in Frank's possession. Come back tomorrow to see if it's fixed!")
                        print("\n")
                        if len(broken_items)==0:
                            type.type("Well I'd say that's all you've got that I could fix. Just check in tomorrow and hopefully it'll be to your liking.")
                            print("\n")
                            self.start_night()
                            return
                        else:
                            type.type("Got anything else I can repair?")
                            print()
                        break
                    elif (yes_or_no == "n") or (yes_or_no == "no"):
                        print()
                        type.type("What?! Why'd you ask, then. God, that's just annoying. You bug me sometimes, man.")
                        print("\n")
                        type.type("Anything you actually want me to repair?")
                        print()
                        break
                    else:
                        print()
                        type.type("Speak up! You're mumbling. ")
        self.start_night()
        return


    # Oswald's shop and interactions
    def oswald_dialogue(self):
        if self._mechanic_visits == 0:
            type.type(quote("Oh my! A customer! A real, live, breathing customer!"))
            print("\n")
            type.type("A man in an impeccably clean suit practically bounces toward you. His smile is so wide it looks painful. ")
            type.type("Behind him, a hulking figure in overalls works silently on a car engine.")
            print("\n")
            type.type(quote("Welcome, welcome, welcome to Oswald's Optimal Outoparts! "))
            type.type(quote("I'm Oswald, and that magnificent specimen of mechanical mastery is Stuart. Say hello, Stuart!"))
            print("\n")
            type.type("Stuart grunts without looking up.")
            print("\n")
            type.type(quote("Isn't he wonderful? Best mechanic this side of anywhere! "))
            type.type(quote("Of course, he wouldn't be where he is today without my business acumen. My entrepreneurial spirit! My VISION!"))
            print("\n")
            type.type("Oswald gestures grandly around the shop.")
            print("\n")
            type.type(quote("You see, I'm not just a mechanic. I'm a businessman! An investor! "))
            type.type(quote("I see opportunity where others see obstacles. "))
            type.type(quote("Why, just last week I was thinking about expanding into the entertainment industry. "))
            type.type(quote("Casinos! Gambling! There's SO much money to be made!"))
            print("\n")
            type.type("His eyes glitter with something between excitement and obsession.")
            print("\n")
            type.type(quote("But enough about my brilliant plans! What can we do for you today, my new friend?"))
        elif self._mechanic_visits == 1:
            type.type(quote("AH! You've returned! Splendid, simply splendid!"))
            print("\n")
            type.type("Oswald rushes over, practically vibrating with energy.")
            print("\n")
            type.type(quote("I've been doing some research since we last spoke. "))
            type.type(quote("This gambling thing - it's FASCINATING. The mathematics! The psychology! The sheer volume of money changing hands!"))
            print("\n")
            type.type("He pulls out a notebook filled with calculations.")
            print("\n")
            type.type(quote("Did you know that casinos have an average profit margin of 15-25%? That's REMARKABLE! "))
            type.type(quote("And it's all legal! All you need is the right location, the right equipment, and the right... person."))
            print("\n")
            type.type("He looks at you with unsettling intensity.")
            print("\n")
            type.type(quote("Someone who UNDERSTANDS the game. Someone with EXPERIENCE."))
        elif self._mechanic_visits == 2:
            type.type(quote("My favorite gambler! How goes the card-slapping?"))
            print("\n")
            type.type("Oswald's smile is even wider today. Almost manic.")
            print("\n")
            type.type(quote("I've been making some calls. Talking to some investors. "))
            type.type(quote("The casino idea is really taking shape! Stuart's been helping me with the technical aspects. "))
            type.type(quote("Show them the blueprints, Stuart!"))
            print("\n")
            type.type("Stuart silently holds up a crude drawing of a building. ")
            type.type("It's covered in Oswald's handwriting - profit projections, seating arrangements, something about 'automatic shufflers'.")
            print("\n")
            type.type(quote("Magnificent, isn't it? Of course, we'll need someone to run it. Someone with your... expertise. Your PASSION for the game!"))
            print("\n")
            type.type("He winks at you.")
            print("\n")
            type.type(quote("Think about it, won't you? We could make beautiful music together. Beautiful, PROFITABLE music."))
        elif self._mechanic_visits >= 3:
            type.type(quote("YOU! Perfect timing!"))
            print("\n")
            type.type("Oswald grabs your arm with surprising strength.")
            print("\n")
            type.type(quote("The plans are nearly complete. Stuart's been working day and night on some... special modifications. "))
            type.type(quote("Upgrades, you might say. Technology that will give us an EDGE."))
            print("\n")
            type.type("He leans in close. His eyes have a strange gleam.")
            print("\n")
            type.type(quote("What if I told you we could transcend the limitations of mere flesh? "))
            type.type(quote("What if we could become MORE than human? Faster, stronger, smarter? The perfect gambling machine!"))
            print("\n")
            type.type("He laughs, but it doesn't quite reach his eyes.")
            print("\n")
            type.type(quote("Just kidding, of course! Ha ha! Unless... no, no, we'll talk about that later. When you're ready. When we're BOTH ready."))
            print("\n")
            type.type("Stuart looks up from his work. For just a moment, you could swear you see something mechanical glinting beneath his sleeve.")

    def visit_oswald(self):
        self.increment_statistic("mechanic_visits")
        type.type("You get in your car and drive to Oswald's Optimal Outoparts. ")
        print("\n")
        self.oswald_dialogue()
        print("\n")
        if self.has_item("Oswald's Dice") and not self.has_met("Oswald Dice Bonus"):
            self.mark_met("Oswald Dice Bonus")
            type.type("Oswald's gaze drops to the " + magenta(bright("Oswald's Dice")) + " in your pocket. He goes very still.")
            print("\n")
            type.type(quote("You know those are weighted, right? I used them for testing.") + " He winks slowly. " + quote("Don't tell anyone."))
            print("\n")
            type.type("You feel luckier just knowing the truth.")
            print("\n")
            self.add_status("Oswald's Luck")
            self.restore_sanity(5)
            type.type(green("You feel a subtle shift in fortune. ") + yellow("Oswald's Luck") + " is with you.")
            print("\n")

        storyline_event = self._storyline_system.check_for_location_storyline_event("oswald")
        if storyline_event is not None:
            storyline_event()
            self.update_rank()
            self.start_night()
            return

        if(len(self._broken_inventory)>0):
            broken_items = self._lists.make_broken_items_list()
            tips = 0
            free_money = 0
            delight_indicator_price = 0
            health_indicator_price = 0
            dirty_old_hat_price = 0
            golden_watch_price = 0
            faulty_insurance_price = 0
            sneaky_peeky_glasses_price = 0
            quiet_sneakers_price = 0
            lucky_coin_price = 0
            worn_gloves_price = 0
            tattered_cloak_price = 0
            rusty_compass_price = 0
            pocket_watch_price = 0
            type.type("It appears that you possess some valuables in need of attention. Oh Stuart!")
            print("\n")
            type.type("Is there anything you would like Stuart to fix?")
            print()
            while(True):
                for i in range(len(broken_items)+1):
                    if(i<len(broken_items)):
                        type.type(str(i+1) + ". " + broken_items[i])
                        time.sleep(0.5)
                        print()
                    else:
                        type.type(str(i+1) + ". I'm all set")
                        time.sleep(0.5)
                        print()
                type.type("Choose a number: ")
                while True:
                    choice = None
                    while choice is None:
                        try:
                            choice = int(input())
                        except ValueError:
                            type.type("Choose a number: ")
                    if(1<=choice<=len(broken_items)):
                        item = broken_items[choice-1]
                        break
                    elif choice==len(broken_items)+1:
                        item = "Home"
                        break
                    else:
                        choice = None
                        type.type("Did you comprehend that?")
                        print()
                        type.type("Choose a number: ")

                print()

                if item == "Delight Indicator":
                    type.type("You'd like Stuart to repair your Delight Indicator?")
                    if delight_indicator_price == 0:
                        delight_indicator_price = random.choice([5500, 6000, 9000, 10000])
                    price = delight_indicator_price
                elif item == "Health Indicator":
                    type.type("You'd like Stuart to repair your Health Indicator?")
                    if health_indicator_price == 0:
                        health_indicator_price = random.choice([4500, 5500, 7000, 9000, 11000])
                    price = health_indicator_price
                elif item == "Dirty Old Hat":
                    type.type("You'd like Stuart to repair the cloth on your Dirty Old Hat?")
                    if dirty_old_hat_price == 0:
                        dirty_old_hat_price = random.choice([14000, 15000, 17000, 20000])
                    price = dirty_old_hat_price
                elif item == "Golden Watch":
                    type.type("You'd like Stuart to repair that Golden Watch you possess?")
                    if golden_watch_price == 0:
                        golden_watch_price = random.choice([16000, 17500, 18000, 20000, 30000])
                    price = golden_watch_price
                elif item == "Faulty Insurance":
                    type.type("You'd like Stuart to restore your Faulty Insurance card?")
                    if faulty_insurance_price == 0:
                        faulty_insurance_price = random.choice([5500, 6000, 7000, 9000, 10000])
                    price = faulty_insurance_price
                elif item == "Sneaky Peeky Shades":
                    type.type("You'd like Stuart to fix up those Sneaky Peeky Shades on top of your eyelids?")
                    if sneaky_peeky_glasses_price == 0:
                        sneaky_peeky_glasses_price = random.choice([18000, 20000, 25000, 30000])
                    price = sneaky_peeky_glasses_price
                elif item == "Quiet Sneakers":
                    type.type("You'd like Stuart to sew up those Quiet Sneakers on your feet?")
                    if quiet_sneakers_price == 0:
                       quiet_sneakers_price = random.choice([9000, 10000, 12000])
                    price = quiet_sneakers_price
                elif item == "Lucky Coin":
                    type.type("You'd like Stuart to polish that Lucky Coin of yours?")
                    if lucky_coin_price == 0:
                        lucky_coin_price = random.choice([7000, 8000, 10000])
                    price = lucky_coin_price
                elif item == "Worn Gloves":
                    type.type("You'd like Stuart to mend those Worn Gloves you carry?")
                    if worn_gloves_price == 0:
                        worn_gloves_price = random.choice([10000, 11000, 13000])
                    price = worn_gloves_price
                elif item == "Tattered Cloak":
                    type.type("You'd like Stuart to weave together that Tattered Cloak?")
                    if tattered_cloak_price == 0:
                        tattered_cloak_price = random.choice([12500, 14000, 16000])
                    price = tattered_cloak_price
                elif item == "Rusty Compass":
                    type.type("You'd like Stuart to restore that Rusty Compass?")
                    if rusty_compass_price == 0:
                        rusty_compass_price = random.choice([5000, 6000, 7500])
                    price = rusty_compass_price
                elif item == "Pocket Watch":
                    type.type("You'd like Stuart to recalibrate that Pocket Watch?")
                    if pocket_watch_price == 0:
                        pocket_watch_price = random.choice([11500, 13000, 15000])
                    price = pocket_watch_price
                else: 
                    type.type("Welp, then I've done all I can possibly do. Good day, my friend.")
                    print("\n")
                    self.start_night()
                    return
                
                print()

                type.type("Stuart will be able to fix this, for say, " + green(bright("${:,}".format(price))) + ". Do you accept? ")
                
                while True:
                    yes_or_no = input("").lower()
                    if ((yes_or_no == "y") or (yes_or_no == "yes")) and (self._balance<price):
                        print()
                        type.type("Oh dear! I'm afraid you can't afford this purchase.")
                        if tips <= 2:
                            random_chance = random.randrange(2)
                            print("\n")
                            if random_chance <= 1:
                                type.type("Here, take this as a pick me up, hopefully it helps. Try again?")
                                self.change_balance(random.choice([50, 100, 200, 300, 400, 500]))
                                tips += 1
                            else:
                                broken_items.pop(choice-1)
                                type.type("Maybe give me something else to fix.")
                        else:
                            broken_items.pop(choice-1)  
                            print("\n")
                            type.type("Shall Stuart repair something else?")
                        break
                    elif (yes_or_no == "y") or (yes_or_no == "yes"):
                        print()
                        type.type("Jolly good! Stuart!")
                        random_chance = random.randrange(2)
                        if random_chance == 0:
                            print("\n")
                            type.type("Yes! Yes! Work your magic, you little man.")
                            self.change_balance(-price)
                            self.fix_item(item)
                            broken_items.pop(choice-1)
                            if item=="Sneaky Peeky Shades" or item=="Quiet Sneakers":
                                type.type("Your " + magenta(bright(item)) + " have been fixed!")
                            else:
                                type.type("Your " + magenta(bright(item)) + " has been fixed!")
                            print("\n")
                        else:
                            print("\n")
                            type.type("Okay, Stuart. What are you doing? It appears that Stuart has gotten stuck whilst trying to fix your thingy. ")
                            type.type("No matter! Stuart, will you please stop? Here, friend, I am giving you your item back. I won't even charge you.")
                            print("\n")
                            broken_items.pop(choice-1)
                            if free_money < 2:
                                random_chance = random.randrange(2)
                                if random_chance == 0:
                                    type.type("In fact, here, just take it, this is yours now.")
                                    self.change_balance(random.choice([50, 100, 200, 500, 1000]))
                                    free_money += 1
                                else:
                                    type.type("I'm so sorry that Stuart was unable to help. My deepest condolences.")
                                    print("\n")
                            else:
                                type.type("Honestly, Stuart is trying his best, and you shouldn't get mad at him.")
                                print("\n")

                            
                        if len(broken_items)==0:
                            type.type("My my, that's everything! Please come again soon, and we can continue performing business!")
                            print("\n")
                            self.start_night()
                            return
                        else:
                            type.type("Is there anything else Stuart can help you with?")
                            print()
                        break
                    elif (yes_or_no == "n") or (yes_or_no == "no"):
                        print()
                        type.type("Really? Nevermind Stuart, you aren't going to fix this. I apologise, but they simply don't want you to. Blame them.")
                        print("\n")
                        type.type("Are you done teasing Stuart? Have anything else for him?")
                        print()
                        break
                    else:
                        print()
                        type.type("Come again? ")
        
        # Oswald's Upgrade Shop
        self.oswald_upgrade_shop()
        return

    def oswald_upgrade_shop(self):
        # Check if player has visited mechanics enough times and has items
        if not self.can_access_upgrades():
            visits = self.get_mechanic_visits()
            if visits < 3:
                remaining = 3 - visits
                type.type("Oswald glances at Stuart, then back at you.")
                print("\n")
                if remaining == 2:
                    type.type(quote("You know, Stuart has been developing some... special skills lately. "))
                    type.type(quote("Come back a few more times, and perhaps we can discuss something more... permanent."))
                elif remaining == 1:
                    type.type(quote("Ah, I can see you're becoming a regular! One more visit and Stuart might have something truly special for you..."))
                else:
                    type.type(quote("Come back when we know each other a bit better, yes? Trust is built over time!"))
                print("\n")
            elif len(self._inventory) < 1:
                type.type(quote("Hmm, it appears you have nothing for Stuart to work on! Come back when you've acquired some proper equipment!"))
                print("\n")
            self.start_night()
            return
        
        # First time accessing upgrades - special dialogue
        if not self.has_met("Oswald Upgrades Unlocked"):
            self.meet("Oswald Upgrades Unlocked")
            print("\n")
            type.type(quote("Ah, my friend! You've proven yourself a loyal customer!"))
            print("\n")
            type.type("Oswald's eyes gleam with an unsettling enthusiasm.")
            print("\n")
            type.type(quote("Stuart, come here! Yes, yes, show them what you can REALLY do!"))
            print("\n")
            type.type("Stuart hobbles over, and for the first time, you see his hands clearly. They're not quite... human. Gears and pistons where knuckles should be.")
            print("\n")
            type.type(quote("You see, Stuart doesn't just FIX things. He IMPROVES them. ENHANCES them. Makes them... MORE."))
            print("\n")
            type.type("Oswald leans in close.")
            print("\n")
            type.type(quote("And someday, perhaps, he could do the same for YOU."))
            print("\n")
        
        # Get list of base items that can be upgraded
        upgradeable_items = []
        base_items = ["Delight Indicator", "Health Indicator", "Dirty Old Hat", 
                     "Golden Watch", "Sneaky Peeky Shades", "Quiet Sneakers",
                     "Faulty Insurance", "Lucky Coin", "Worn Gloves",
                     "Tattered Cloak", "Rusty Compass", "Pocket Watch",
                     "Gambler's Chalice", "Twin's Locket", "White Feather",
                     "Dealer's Grudge", "Gambler's Grimoire"]
        
        for item in base_items:
            if self.can_upgrade(item):
                upgradeable_items.append(item)
        
        # Count how many items have been upgraded
        upgraded_count = self.count_upgraded_items()
        total_upgradeable = self.count_total_upgradeable()
        
        if len(upgradeable_items) == 0:
            if self.all_items_upgraded():
                self.oswald_final_revelation()
                return
            else:
                type.type("It appears you have nothing that Stuart can upgrade at this time. Do come back when you have more items!")
                print("\n")
            self.start_night()
            return
        
        print("\n")
        
        # Show upgrade progress
        if upgraded_count > 0:
            type.type(quote("Ah, my favorite client! Stuart has been quite busy with your equipment."))
            print("\n")
            if upgraded_count >= 12:
                type.type(quote("My word, look at you! You're practically more machine than man now!"))
            elif upgraded_count >= 8:
                type.type(quote("Stuart is doing magnificent work on you! Just a few more pieces and you'll be... complete."))
            elif upgraded_count >= 5:
                type.type(quote("The transformation is well underway! I can see the power in your eyes already!"))
            elif upgraded_count >= 3:
                type.type(quote("Excellent progress! Stuart's enhancements are really coming together!"))
            else:
                type.type(quote("A few upgrades under your belt! Stuart is just getting started!"))
            print("\n")
        
        type.type("Now then! Stuart has been developing quite the skillset lately. He can " + cyan(bright("UPGRADE")) + " your items to make them even more powerful!")
        print("\n")
        type.type("Of course, such enhancements don't come cheap. But you look like someone who appreciates quality, yes?")
        print("\n")
        
        while len(upgradeable_items) > 0:
            type.type("Which item would you like Stuart to upgrade?")
            print()
            
            # Display upgradeable items with their upgraded versions
            for i in range(len(upgradeable_items) + 1):
                if i < len(upgradeable_items):
                    item = upgradeable_items[i]
                    upgraded = self.get_upgraded_version(item)
                    type.type(str(i+1) + ". " + item + " → " + cyan(upgraded))
                    time.sleep(0.3)
                    print()
                else:
                    type.type(str(i+1) + ". I'm finished")
                    time.sleep(0.3)
                    print()
            
            type.type("Choose a number: ")
            while True:
                choice = None
                while choice is None:
                    try:
                        choice = int(input())
                    except ValueError:
                        type.type("Choose a number: ")
                if 1 <= choice <= len(upgradeable_items):
                    item = upgradeable_items[choice-1]
                    break
                elif choice == len(upgradeable_items) + 1:
                    type.type("Very well! Do come again when you desire further enhancements!")
                    print("\n")
                    self.start_night()
                    return
                else:
                    choice = None
                    type.type("I beg your pardon?")
                    print()
                    type.type("Choose a number: ")
            
            print()
            
            # Upgrade prices
            prices = {
                "Delight Indicator": 150000, "Health Indicator": 150000, "Dirty Old Hat": 200000,
                "Golden Watch": 300000, "Sneaky Peeky Shades": 400000, "Quiet Sneakers": 250000,
                "Faulty Insurance": 120000, "Lucky Coin": 200000, "Worn Gloves": 250000,
                "Tattered Cloak": 300000, "Rusty Compass": 160000, "Pocket Watch": 350000,
                "Gambler's Chalice": 350000, "Twin's Locket": 400000, "White Feather": 280000,
                "Dealer's Grudge": 320000, "Gambler's Grimoire": 250000
            }
            price = prices.get(item, 200000)
            upgraded = self.get_upgraded_version(item)
            
            type.type("Ah, the " + magenta(bright(item)) + "! A fine choice.")
            print("\n")
            type.type("Stuart can transform this into the " + cyan(bright(upgraded)) + " for " + green(bright("${:,}".format(price))) + ".")
            print("\n")
            
            type.type("Do you accept this offer?")
            print()
            
            while True:
                yes_or_no = input("").lower()
                if (yes_or_no == "y" or yes_or_no == "yes") and self._balance < price:
                    print()
                    type.type("Oh dear! It appears your funds are insufficient for this particular enhancement.")
                    print("\n")
                    type.type("Perhaps save up a bit more and return? Stuart will be waiting!")
                    print()
                    break
                elif yes_or_no == "y" or yes_or_no == "yes":
                    print()
                    type.type("Splendid! Stuart, work your magic!")
                    print("\n")
                    self.change_balance(-price)
                    new_item = self.perform_upgrade(item)
                    type.type("Stuart's tiny hands move with incredible precision. Sparks fly, gears turn, and...")
                    print("\n")
                    type.type("Your " + magenta(bright(item)) + " has become the " + cyan(bright(new_item)) + "!")
                    print("\n")
                    
                    # Enhancement flavor text
                    enhancement_messages = [
                        "Oswald watches with gleaming eyes. " + quote("Oh, how MAGNIFICENT! You're becoming something GREATER!")
                        , "Stuart nods approvingly, gears whirring in his mechanical fingers."
                        , "Oswald claps his hands together. " + quote("Yes, YES! The power suits you!")
                        , "You feel the upgrade humming with energy. It feels... right."
                        , "Oswald mutters something about 'transcending limitations' as Stuart works."
                        , "For a moment, you swear you can feel the machinery becoming part of you."
                    ]
                    type.type(random.choice(enhancement_messages))
                    print("\n")
                    
                    upgradeable_items.remove(item)
                    
                    # Check if this was the LAST upgrade
                    if self.all_items_upgraded():
                        print("\n")
                        self.oswald_final_revelation()
                        return
                    
                    if len(upgradeable_items) > 0:
                        type.type("Would you like Stuart to upgrade anything else?")
                        print()
                    break
                elif yes_or_no == "n" or yes_or_no == "no":
                    print()
                    type.type("No? Well, perhaps another time then. Stuart doesn't judge.")
                    print("\n")
                    type.type("Anything else catch your eye?")
                    print()
                    break
                else:
                    print()
                    type.type("I'm terribly sorry, I didn't quite catch that. ")
        
        if len(upgradeable_items) == 0 and not self.all_items_upgraded():
            type.type("That's all Stuart can upgrade for now. Do return when you have more items!")
            print("\n")
        
        self.start_night()
        return

    def count_upgraded_items(self):
        """Count how many items the player has in upgraded form"""
        upgraded_items = ["Delight Manipulator", "Health Manipulator", "Unwashed Hair",
                         "Sapphire Watch", "Sneaky Peeky Goggles", "Quiet Bunny Slippers",
                         "Real Insurance", "Lucky Medallion", "Velvet Gloves",
                         "Invisible Cloak", "Golden Compass", "Grandfather Clock",
                         "Overflowing Goblet", "Mirror of Duality", "Phoenix Feather",
                         "Dealer's Mercy", "Oracle's Tome"]
        count = 0
        for item in upgraded_items:
            if self.has_item(item):
                count += 1
        return count

    def count_total_upgradeable(self):
        """Count total items that could potentially be upgraded"""
        base_items = ["Delight Indicator", "Health Indicator", "Dirty Old Hat", 
                     "Golden Watch", "Sneaky Peeky Shades", "Quiet Sneakers",
                     "Faulty Insurance", "Lucky Coin", "Worn Gloves",
                     "Tattered Cloak", "Rusty Compass", "Pocket Watch",
                     "Gambler's Chalice", "Twin's Locket", "White Feather",
                     "Dealer's Grudge", "Gambler's Grimoire"]
        count = 0
        for item in base_items:
            if self.has_item(item) or self.has_item(self.get_upgraded_version(item)):
                count += 1
        return count

    def oswald_final_revelation(self):
        """The moment all items are upgraded - reveal what you've become"""
        print("\n")
        type.slow(cyan(bright("═══════════════════════════════════════════════════")))
        print()
        type.slow(cyan(bright("              FINAL UPGRADE COMPLETE               ")))
        print()
        type.slow(cyan(bright("═══════════════════════════════════════════════════")))
        print("\n")
        
        type.slow("Stuart steps back from his workbench.")
        print("\n")
        
        type.slow("For a long moment, he just stares at you.")
        print("\n")
        
        type.slow("Then, in that impossibly deep voice:")
        print("\n")
        
        type.slow(quote("Yo. You're not human anymore."))
        print("\n")
        
        type.slow("Oswald pushes Stuart aside, his eyes wide with wonder and terror.")
        print("\n")
        
        type.slow(quote("My word! Look at you! Every single item... upgraded to perfection!"))
        print("\n")
        
        type.slow("He circles you like a vulture, examining every piece of enhanced equipment fused to your body.")
        print("\n")
        
        type.slow(quote("The Mood Ring that reads minds... The All-Seeing Shades that pierce through deception... The Shadow Steps that make no sound... The Fortune's Favor that bends luck itself..."))
        print("\n")
        
        type.slow("His voice drops to a whisper.")
        print("\n")
        
        type.slow(quote("You're not a gambler anymore. You're a GOD."))
        print("\n")
        
        type.slow("Stuart grunts. " + quote("That's tight, yo. But also kind of messed up."))
        print("\n")
        
        type.slow("Oswald's expression shifts. The wonder fades. Something darker takes its place.")
        print("\n")
        
        type.slow(quote("And with your funding... my Grand Casino is COMPLETE!"))
        print("\n")
        
        type.slow("He spreads his arms wide, laughing maniacally.")
        print("\n")
        
        type.slow(quote("OSWALD'S GRAND CASINO opens TONIGHT! And YOU, my monstrous friend, will be its first guest!"))
        print("\n")
        
        type.slow("He slaps an ornate invitation into your enhanced palm.")
        print("\n")
        
        type.slow(quote("Consider it... a thank you. For everything you've contributed."))
        print("\n")
        
        type.slow("His smile is too wide. His eyes are too bright.")
        print("\n")
        
        type.slow(quote("I'll see you there. Don't be late."))
        print("\n")
        
        type.slow("He practically skips out of the shop, cackling.")
        print("\n")
        
        type.slow("Stuart watches him go, then turns to you.")
        print("\n")
        
        type.slow(quote("Yo. That dude's lost it. But you..."))
        print("\n")
        
        type.slow("He looks you up and down.")
        print("\n")
        
        type.slow(quote("You could probably destroy that whole casino with your bare hands now. Just saying."))
        print("\n")
        
        type.slow("He shrugs and walks back to his workbench.")
        print("\n")
        
        type.slow(quote("Do what you gotta do, homie."))
        print("\n")
        
        type.slow("You look down at your hands. Metal and flesh intertwined. Power humming through synthetic veins.")
        print("\n")
        
        type.slow("You look at the invitation. Gold letters on black paper.")
        print("\n")
        
        type.slow(cyan(bright("OSWALD'S GRAND CASINO - GRAND OPENING - TONIGHT ONLY")))
        print("\n")
        
        type.slow("There's only one way this ends.")
        print("\n")
        
        type.slow(yellow(bright("You get in your car and drive to Oswald's Grand Casino...")))
        print("\n")
        
        time.sleep(2)
        
        self.eternity()


    # Convenience Store
    def update_convenience_store_inventory(self):
        if self._day == 2: self._convenience_store_inventory = self._lists.make_convenience_store_inventory()
        if (self._day % 7) == 0:
            self._convenience_store_inventory = self._lists.make_convenience_store_inventory()

    def get_kyle_greeting(self):
        """Kyle notices your condition and comments on it"""
        # Kyle reacts to visible injuries first
        if self.has_injury("Broken Leg") or self.has_injury("Broken Ankle"):
            return quote("Dude, why are you even walking? Your leg looks... wrong. Here, lemme get you a chair or something. Nah, just kidding, we don't have chairs. One-item limit. Manager's orders.")
        if self.has_injury("Broken Arm") or self.has_injury("Broken Wrist") or self.has_injury("Broken Hand"):
            return quote("Whoa, that arm looks gnarly. How you gonna carry stuff? Whatever. One-item limit anyway. Manager's orders.")
        if self.has_injury("Severe Burns") or self.has_danger("Burn Scars"):
            return quote("Holy crap, what happened to you? You look like you fought a dragon and lost. One-item limit. Manager's orders.")
        if self.has_injury("Deep Laceration"):
            return quote("Yo, you're like... bleeding. On my floor. That's gonna be a whole thing to clean up. One-item limit, manager's orders, and maybe see a doctor?")
        if self.has_injury("Concussion"):
            return quote("You okay? You look kinda... out of it. Like more than usual. Eyes all weird and stuff. One-item limit. Manager's orders.")
        if self.has_injury("Fractured Jaw"):
            return quote("Dude, your face is all swollen. You get in a fight or something? Cool. One-item limit. Manager's orders.")
        if self.has_injury("Broken Nose"):
            return quote("Your nose is like... not where it should be. That's rough, buddy. Anyway, one-item limit. Manager's orders.")
        if self.has_injury("Black Eye"):
            return quote("Nice shiner. Whoever did that got you good. One-item limit. Manager's orders.")
        
        # Kyle reacts to visible sickness
        if self.has_status("Measles"):
            return quote("Bro, you're covered in spots. Stay back, I don't want whatever that is. One-item limit, and like, stay six feet away. Manager's orders.")
        if self.has_status("Ringworm"):
            return quote("What's that on your skin? That's disgusting, man. No offense. One-item limit. Manager's orders.")
        if self.has_status("Pink Eye"):
            return quote("Your eyes are like... pink and crusty. Super gross. Don't touch anything. One-item limit. Manager's orders.")
        if self.has_status("Shingles"):
            return quote("That rash looks painful. My grandma had that. She said it was the worst. One-item limit. Manager's orders.")
        if self.has_status("Cold") or self.has_status("Flu"):
            return quote("*sniff* You sound sick. Don't breathe on me. One-item limit. Manager's orders. Also there's tissues in aisle... wait, no, we sold those.")
        if self.has_status("Pneumonia") or self.has_status("Bronchitis"):
            return quote("Dude, that cough sounds terrible. Like you're dying or something. One-item limit. Manager's orders. Maybe get that checked.")
        if self.has_status("Food Poisoning") or self.has_status("Stomach Flu"):
            return quote("You look green. Like actually green. Bathroom's in the back but it's employees only so... don't puke on the floor. One-item limit. Manager's orders.")
        if self.has_status("Heat Stroke"):
            return quote("You're sweating like crazy. AC's broken here too, I feel you. One-item limit. Manager's orders.")
        if self.has_status("Hypothermia"):
            return quote("Bro, you're shaking. And blue. That's not normal. One-item limit. Manager's orders. Also maybe stand by the heating vent.")
        
        # Kyle reacts to mental state
        if self.get_sanity() < 15:
            return quote("Uh... you okay, man? You're like, talking to yourself. And twitching. One-item limit. Manager's orders. Please don't murder me.")
        if self.get_sanity() < 30:
            return quote("You look stressed. Like REALLY stressed. Take a breath. One-item limit. Manager's orders. Deep breaths.")
        
        # Kyle reacts to health
        if self.get_health() < 20:
            return quote("Dude, you look like death warmed over. Seriously. Should you be walking around? One-item limit. Manager's orders. Maybe sit down. Wait, no chairs.")
        if self.get_health() < 40:
            return quote("You don't look so good. Like, at all. One-item limit. Manager's orders.")
        
        # Kyle reacts to items/wealth
        if self.has_item("Gold Chain"):
            return quote("Nice chain. That real gold? Cool. Anyway, one-item limit. Manager's orders. Baller.")
        if self.has_item("Fancy Cigars"):
            return quote("You got cigars? Can't smoke in here, fire code or whatever. One-item limit. Manager's orders.")
        if self.has_item("Vintage Wine"):
            return quote("Oh, you got that wine from last time? Classy. One-item limit. Manager's orders. Fancy pants.")
        if self.has_danger("Soulless"):
            return quote("...something's different about you. Can't put my finger on it. You got like... empty eyes or something. Creepy. One-item limit. Manager's orders.")
        if self.get_balance() >= 400000:
            return quote("Back again, Mr. Money Bags? One-item limit still applies. Manager doesn't care how rich you are. Manager's orders.")
        if self.get_balance() < 50:
            return quote("You look broke. Brooooke. We got some cheap stuff if you dig around. One-item limit. Manager's orders.")
        
        # Default greeting
        return quote("Sup. Name's Kyle. Got a one-item limit. Manager's orders. I don't make the rules.")

    # ==========================================
    # CAR WORKBENCH - CRAFTING SYSTEM
    # ==========================================

    def visit_workbench(self):
        if not self.has_met("Car Workbench"):
            self.meet("Car Workbench")
            type.type("You pop the trunk of your wagon and dig around until you find the " + magenta(bright("Tool Kit")) + ". ")
            type.type("Setting it on the hood, you flip it open. Wrenches, pliers, a hammer, screwdrivers, duct tape scraps. ")
            type.type("It's not much, but it's a workbench.")
            print("\n")
            type.type("You look at your pile of junk — sorry, " + cyan("inventory") + " — and start to wonder... ")
            type.type("Could you " + bright("combine") + " some of this stuff into something actually useful?")
            print("\n")
            type.type("You crack your knuckles. Let's see what you can build.")
            print("\n")
        else:
            greetings = [
                "You pull out your " + magenta(bright("Tool Kit")) + " and set up shop on the hood of the wagon. Time to tinker.",
                "The hood of the car doubles as your workbench. You lay out your tools. What are we building today?",
                "You spread your tools across the trunk. The creative juices are flowing.",
                "Workbench mode: engaged. You roll up your sleeves and survey your materials.",
                "You open the " + magenta(bright("Tool Kit")) + " and inhale that metallic smell. Time to create.",
                "Your makeshift workshop awaits. The wagon hood, your tools, and whatever garbage you've collected.",
            ]
            type.type(random.choice(greetings))
            print("\n")

        while True:
            # Get available recipes
            available = self._lists.get_available_recipes(self)
            all_recipes = self._lists.get_crafting_recipes()

            # Count what player has crafted
            crafted_count = sum(1 for name in all_recipes if self.has_item(name))

            type.type(yellow(bright("=== CAR WORKBENCH ===")))
            print()
            type.type("Crafted items: " + cyan(str(crafted_count)) + "/" + cyan(str(len(all_recipes))))
            print()

            # Recipe hint system — scales with crafting experience
            uncrafted = [name for name, recipe in all_recipes.items() if not self.has_item(name)]
            if uncrafted:
                hint_recipe_name = random.choice(uncrafted)
                hint_recipe = all_recipes[hint_recipe_name]
                hint_tier = hint_recipe.get("tier", 1)
                if crafted_count <= 2:
                    # Vague hints — cryptic, no item names
                    hint_text = hint_recipe.get("hint_vague", "Something useful can be made here...")
                elif crafted_count <= 9:
                    # Suggestive hints — category + partial ingredient
                    hint_text = hint_recipe.get("hint_suggestive", "Something in the " + hint_recipe.get("category", "unknown") + " family...")
                elif crafted_count <= 19:
                    # Clear hints — full ingredients, no result name
                    hint_text = " + ".join(hint_recipe["ingredients"]) + " = ???"
                elif crafted_count <= 39:
                    # Expert hints — full recipe revealed
                    hint_text = " + ".join(hint_recipe["ingredients"]) + " = " + hint_recipe_name
                else:
                    # Master hints — reveal higher tier recipes
                    tier2_uncrafted = [n for n in uncrafted if all_recipes[n].get("tier", 1) >= 2]
                    if tier2_uncrafted:
                        hint_recipe_name = random.choice(tier2_uncrafted)
                        hint_recipe = all_recipes[hint_recipe_name]
                    hint_text = " + ".join(hint_recipe["ingredients"]) + " = " + hint_recipe_name + " — " + hint_recipe.get("description", "a masterwork")
                type.type(yellow("💡 ") + italic(hint_text))
                print()
            else:
                type.type(italic("You've mastered every recipe known. Legend status."))
                print()
            print()

            type.type("1. " + bright("Craft Something") + " (" + green(str(len(available))) + " recipes available)")
            print()
            type.type("2. " + bright("Browse All Recipes") + " (see what you could make)")
            print()
            type.type("3. " + bright("Inspect Crafted Items") + " (check your creations)")
            print()
            type.type("4. " + bright("Disassemble") + " (break down a crafted item)")
            print()
            type.type("5. " + bright("Pack Up") + " (leave the workbench)")
            print()
            type.type("Choose a number: ")

            choice = None
            while choice is None:
                try:
                    choice = int(input())
                except ValueError:
                    type.type("Pick a number, handyman: ")

            if choice == 1:
                self.workbench_craft(available)
            elif choice == 2:
                self.workbench_browse(all_recipes)
            elif choice == 3:
                self.workbench_inspect()
            elif choice == 4:
                self.workbench_disassemble()
            elif choice == 5:
                pack_up_texts = [
                    "You pack everything up and close the trunk. Back to life.",
                    "You wipe your hands on your jeans and put the tools away. Good session.",
                    "Tools down. You actually feel productive for once.",
                    "You snap the " + magenta(bright("Tool Kit")) + " shut. Time to move on.",
                    "Workshop closed. The wagon hood looks relieved.",
                ]
                type.type(random.choice(pack_up_texts))
                print("\n")
                break
            else:
                type.type("That's not a workbench option.")
                print()

        self.start_night()

    def workbench_craft(self, available):
        """Craft an item from available recipes"""
        print()
        if len(available) == 0:
            no_recipes_texts = [
                "You stare at your inventory. Nothing combines into anything useful right now. You need more materials.",
                "You try to mash two random items together. Nothing happens. You need the right ingredients.",
                "Your creative well is dry. Collect more items and come back.",
                "You hold up each item one by one, squinting at them. Nope. Nothing works together. Yet.",
            ]
            type.type(random.choice(no_recipes_texts))
            print("\n")
            return

        recipe_names = list(available.keys())
        type.type(yellow("Available recipes:"))
        print()
        for i, name in enumerate(recipe_names, 1):
            recipe = available[name]
            ingredients_str = " + ".join([magenta(ing) for ing in recipe["ingredients"]])
            type.type(str(i) + ". " + bright(cyan(name)) + " ← " + ingredients_str)
            print()
            type.type("   " + italic(recipe["description"]))
            print()

        cancel_num = len(recipe_names) + 1
        type.type(str(cancel_num) + ". Never mind")
        print()
        type.type("What do you want to craft? ")

        choice = None
        while choice is None:
            try:
                choice = int(input())
            except ValueError:
                type.type("Pick a number: ")

        if choice == cancel_num:
            type.type("You put the tools down. Maybe later.")
            print("\n")
            return

        if 1 <= choice <= len(recipe_names):
            name = recipe_names[choice - 1]
            recipe = available[name]

            # Confirm craft
            ingredients_str = " and ".join([magenta(bright(ing)) for ing in recipe["ingredients"]])
            type.type("Combine " + ingredients_str + " into a " + bright(cyan(name)) + "?")
            print()
            confirm = input("(yes/no): ").strip().lower()

            if confirm in ("y", "yes"):
                print()
                # Remove ingredients
                for ingredient in recipe["ingredients"]:
                    self.use_item(ingredient)

                # Crafting animation
                type.slow("...")
                time.sleep(0.5)
                type.slow("......")
                time.sleep(0.5)
                print()

                # Craft text
                type.type(recipe["craft_text"])
                print("\n")

                # Add crafted item
                self.add_item(name)
                type.type(bright(yellow("★")) + " " + bright(cyan(name)) + " " + bright("crafted!") + " " + bright(yellow("★")))
                print("\n")

                # Check crafting milestones
                all_recipes = self._lists.get_crafting_recipes()
                crafted_total = sum(1 for n in all_recipes if self.has_item(n))
                if crafted_total == 1:
                    type.type(yellow("First craft! You're handy with a tool kit. Who knew?"))
                    print("\n")
                elif crafted_total == 5:
                    type.type(yellow("Five crafted items. You're basically a blacksmith now..."))
                    print("\n")
                elif crafted_total == 10:
                    type.type(yellow("Ten crafted items! Your car looks like a mad scientist's laboratory."))
                    print("\n")
                elif crafted_total == 15:
                    type.type(yellow("Fifteen items. You could teach a survival course."))
                    print("\n")
                elif crafted_total == 20:
                    type.type(yellow("Twenty items. The workbench groans under the weight of your ambition."))
                    print("\n")
                elif crafted_total == 25:
                    type.type(yellow("Twenty-five. You've crafted more than most people own."))
                    print("\n")
                    self.restore_sanity(3)
                elif crafted_total == 30:
                    type.type(yellow("Thirty! Your car is a mobile workshop, pharmacy, and armory combined."))
                    print("\n")
                    self.check_achievement("craftsman")
                elif crafted_total == 40:
                    type.type(yellow("Forty items... When did you become an engineer?"))
                    print("\n")
                    self.check_achievement("master_craftsman")
                elif crafted_total == 50:
                    type.type(yellow("Fifty. Half the things in your car didn't exist yesterday."))
                    print("\n")
                    self.check_achievement("inventor")
                elif crafted_total == 67:
                    type.type(yellow("Every Tier 1 recipe mastered. The workbench hums with potential."))
                    print("\n")
                elif crafted_total == 80:
                    type.type(yellow("Eighty items. Your car is worth more than the casino."))
                    print("\n")
                    self.change_balance(5000)
                    type.type(yellow("You find $5,000 in a loose dashboard compartment you never noticed before."))
                    print("\n")
                elif crafted_total == 92:
                    type.type(yellow("Every Tier 2 recipe complete. You see combinations in everything."))
                    print("\n")
                    self.check_achievement("expert")
                elif crafted_total == 100:
                    type.type(yellow("One hundred crafted items. You started with nothing. Look at you now."))
                    print("\n")
                    self.check_achievement("centurion")
                    self.restore_sanity(15)
                    self.heal(20)
                elif crafted_total == 104:
                    type.type(yellow("Every Tier 3 masterwork forged. You've bent the world to your will."))
                    print("\n")
                    self.check_achievement("artificer")
                elif crafted_total == len(all_recipes):
                    type.type(bright(yellow("★★★ MASTER CRAFTSMAN ★★★")))
                    print()
                    type.type(yellow("Every recipe. Every combination. Every possibility."))
                    print("\n")
                    self.check_achievement("grand_artificer")
            else:
                type.type("You set the ingredients back down. Not today.")
                print("\n")
        else:
            type.type("That's not an option.")
            print("\n")

    def workbench_browse(self, all_recipes):
        """Browse all recipes, grouped by category"""
        print()
        categories = self._lists.get_craftable_categories()
        category_names = {
            "weapon": "⚔️  Weapons",
            "trap": "🪤 Traps",
            "remedy": "💊 Remedies",
            "tool": "🔧 Tools",
            "charm": "✨ Charms",
            "survival": "🏕️  Survival",
            "companion": "🐾 Companion",
            "gadget": "📡 Gadgets",
            "disguise": "🎭 Disguises",
            "tonic": "🧪 Tonics & Consumables",
            "dark_arts": "🕯️  Dark Arts",
            "luxury": "💎 Luxury",
            "vehicle": "🚗 Vehicle Upgrades",
            "legendary": "👑 Legendary",
        }

        for cat in categories:
            cat_recipes = self._lists.get_recipes_by_category(cat)
            type.type(yellow(bright(category_names.get(cat, cat.upper()))))
            print()
            for name, recipe in cat_recipes.items():
                # Check if player has all ingredients
                has_all = all(self.has_item(ing) for ing in recipe["ingredients"])
                # Check if already crafted
                already_crafted = self.has_item(name)

                if already_crafted:
                    status = green(" [CRAFTED]")
                elif has_all:
                    status = cyan(" [READY]")
                else:
                    status = red(" [MISSING MATERIALS]")

                ingredients_str = ", ".join(recipe["ingredients"])
                type.type("  " + bright(name) + status)
                print()
                type.type("    Needs: " + magenta(ingredients_str))
                print()
                type.type("    " + italic(recipe["description"]))
                print()
            print()

        type.type("Press Enter to go back...")
        input()
        print()

    def workbench_inspect(self):
        """Inspect crafted items you currently own"""
        print()
        all_recipes = self._lists.get_crafting_recipes()
        owned_crafted = [name for name in all_recipes if self.has_item(name)]

        if len(owned_crafted) == 0:
            type.type("You haven't crafted anything yet. Get to work!")
            print("\n")
            return

        type.type(yellow("Your crafted items:"))
        print()
        for i, name in enumerate(owned_crafted, 1):
            description = self._lists.get_crafted_item_description(name)
            recipe = all_recipes[name]
            type.type(str(i) + ". " + bright(cyan(name)) + " (" + recipe["category"] + ")")
            print()
            type.type("   " + description)
            print()
            pawn_value = self._lists.get_pawn_price(name)
            if pawn_value > 0:
                type.type("   Pawn value: " + green("${:,}".format(pawn_value)))
                print()
            print()

        type.type("Press Enter to go back...")
        input()
        print()

    def workbench_disassemble(self):
        """Break down a crafted item back into its ingredients"""
        print()
        all_recipes = self._lists.get_crafting_recipes()
        owned_crafted = [name for name in all_recipes if self.has_item(name)]

        if len(owned_crafted) == 0:
            type.type("You don't have any crafted items to take apart.")
            print("\n")
            return

        type.type(yellow("Disassemble which item?") + " (You'll get the ingredients back)")
        print()
        for i, name in enumerate(owned_crafted, 1):
            recipe = all_recipes[name]
            ingredients_str = " + ".join([magenta(ing) for ing in recipe["ingredients"]])
            type.type(str(i) + ". " + bright(cyan(name)) + " → " + ingredients_str)
            print()

        cancel_num = len(owned_crafted) + 1
        type.type(str(cancel_num) + ". Never mind")
        print()
        type.type("Choose: ")

        choice = None
        while choice is None:
            try:
                choice = int(input())
            except ValueError:
                type.type("Pick a number: ")

        if choice == cancel_num:
            type.type("You leave everything assembled. Smart.")
            print("\n")
            return

        if 1 <= choice <= len(owned_crafted):
            name = owned_crafted[choice - 1]
            recipe = all_recipes[name]

            disassemble_texts = [
                "You carefully take the " + cyan(bright(name)) + " apart, salvaging the components.",
                "With a sigh, you dismantle the " + cyan(bright(name)) + ". The ingredients are recovered.",
                "You reverse-engineer your own creation. The " + cyan(bright(name)) + " is no more.",
                "Piece by piece, you break down the " + cyan(bright(name)) + ". Back to raw materials.",
            ]

            self.use_item(name)
            for ingredient in recipe["ingredients"]:
                self.add_item(ingredient)

            type.type(random.choice(disassemble_texts))
            print()
            ingredients_str = ", ".join([magenta(bright(ing)) for ing in recipe["ingredients"]])
            type.type("Recovered: " + ingredients_str)
            print("\n")
        else:
            type.type("That's not an option.")
            print("\n")

    def visit_convenience_store(self):
        type.type("You get in your car and drive to the Convenience Store. ")
        if not self.has_met("Convenience Store"):
            self.meet("Convenience Store")
            type.type("When pulling into the parking lot, you have to grip the wheel tightly to keep control of the wagon, ")
            type.type("as the concrete beneath you is littered with potholes. ")
            type.type("As you drive closer to bright red brick building, you begin to read the sign 'Convenience Store' written in bold. ")
            type.type("Really? This place really called 'Convenience Store'? They couldn't have come up with anything more creative? ")
            type.type("You park nearby, and get out, being sure not to trip on the loose chunks of road. ")
            print("\n")
            type.type("Walking closer to the store, you notice there's a poster with a smiling dude on it, holding his thumbs up, ")
            type.type("with the caption 'We Love our Customers! That's why we're limiting each customer to one item per visit. ")
            type.type("That means there's more for everyone! Sharing is caring!' ")
            type.type("Looking through the window, the store is barren, with only a few items on the shelf. ")
            type.type("If not for someone standing at the register, you would have thought the place to be abandoned.")
            print("\n")
            type.type("When you open the glass door, you notice a bell above you ring. ")
            type.type("There's a teenager on his phone, sitting with his feet up on the counter. ")
            type.type("His face is covered with pimples, and he's in the middle of blowing a bubble with the gum in his mouth.")
            print("\n")
            type.type("You get closer to the boy, and he finally notices you, and puts his phone down.")
        print("\n")

        storyline_event = self._storyline_system.check_for_location_storyline_event("convenience_store")
        if storyline_event is not None:
            storyline_event()
            self.update_rank()
            self.start_night()
            return

        if(len(self._convenience_store_inventory)==0):
            type.type("As you walk up to the store, you see a white sign hanging on the front door. They're closed. Bummer.")
            print("\n")
            self.start_night()
            return
        
        # === KYLE RECOGNIZES YOUR CONDITION ===
        kyle_greeting = self.get_kyle_greeting()
        type.type(kyle_greeting)
        print("\n")
        items_bought = 0
        while True:
            choice = None
            items = self._convenience_store_inventory
            if items_bought == 0:
                type.type("What do you want?")
            else:
                type.type("What else you want?")
            print()
            for i in range(len(items)+1):
                if(i<len(items)):
                    type.type(str(i+1) + ". " + items[i][0] + " - " + green(bright("${:,}".format(items[i][1]))))
                    print()
                else:
                    type.type(str(i+1) + ". I'm not buying anything")
                    time.sleep(0.5)
                    print()
            type.type("Choose a number: ")
            while True:
                while choice is None:
                    try:
                        choice = int(input())
                    except ValueError:
                        type.type("C'mon I don't have all day just pick something: ")
                if(1<=choice<=len(items)):
                    item = items[choice-1][0]
                    price = items[choice-1][1]
                    if(price<=self._balance):
                        break
                    else:
                        type.type("Dude, you obviously can't afford that. Try again, buddy: ")
                elif choice==len(items)+1:
                    item = "Home"
                    break
                else:
                    choice = None
                    type.type("We clearly don't have that in right now.")
                    print()
                    type.type("It's not hard, just choose a number: ")
            print()

            if choice!=len(items)+1:
                items.pop(choice-1)

            # === FOOD ITEMS (Eat now or save for later) ===
            if self.is_food_item(item):
                type.type("You got a " + bright(magenta(item + "!")))
                print()
                type.type("Eat it now, or save it for later?")
                print()
                action = input("(eat/save): ").strip().lower()
                if action == "s" or action == "save":
                    self.add_item(item)
                    save_texts = [
                        "You tuck the " + magenta(item) + " away for later. Smart move.",
                        "You slide the " + magenta(item) + " into your pocket. For a rainy day.",
                        "You stash the " + magenta(item) + " in the car. Future you will be grateful.",
                        "Into the glovebox it goes. The " + magenta(item) + " will keep.",
                        "You resist the urge to eat it right now. Willpower!",
                    ]
                    type.type(random.choice(save_texts))
                else:
                    self.eat_food(item)
                print()
            
            # === COMMON UTILITY ITEMS ===
            elif item == "Deck of Cards":
                type.type(bright(magenta("You got a Deck of Cards!")))
                print()
                type.type("Maybe you can practice your shuffling.")
                self.add_item("Deck of Cards")
            elif item == "Pest Control":
                type.type(bright(magenta("You got Pest Control!")))
                print()
                type.type("This should help with any unwanted critters in your car.")
                self.add_item("Pest Control")
            elif item == "Cough Drops":
                type.type(bright(magenta("You got Cough Drops!")))
                print()
                type.type("Mentholyptus flavor. Your throat thanks you in advance.")
                self.add_item("Cough Drops")
            elif item == "Dog Treat":
                type.type(bright(magenta("You got a Dog Treat!")))
                print()
                type.type("Bacon flavored. For dogs. Probably.")
                self.add_item("Dog Treat")
            elif item == "Spare Tire":
                type.type(bright(magenta("You got a Spare Tire!")))
                print()
                type.type("It's small and a bit worn, but it'll do in a pinch.")
                self.add_item("Spare Tire")
            elif item == "Flashlight":
                type.type(bright(magenta("You got a Flashlight!")))
                print()
                type.type("Batteries included. Surprisingly.")
                self.add_item("Flashlight")
            elif item == "First Aid Kit":
                type.type(bright(magenta("You got a First Aid Kit!")))
                print()
                type.type("Band-aids, antiseptic, the works. Could save your life someday.")
                self.add_item("First Aid Kit")
            elif item == "Umbrella":
                type.type(bright(magenta("You got an Umbrella!")))
                print()
                type.type("Compact and flimsy, but it'll keep you dry.")
                self.add_item("Umbrella")
            elif item == "Sunglasses":
                type.type(bright(magenta("You got Sunglasses!")))
                print()
                type.type("Cheap knockoffs, but they look cool enough.")
                self.add_item("Sunglasses")
            elif item == "Lighter":
                type.type(bright(magenta("You got a Lighter!")))
                print()
                type.type("A simple Bic lighter. Fire is useful.")
                self.add_item("Lighter")
            elif item == "Duct Tape":
                type.type(bright(magenta("You got Duct Tape!")))
                print()
                type.type("If you can't fix it with duct tape, you're not using enough duct tape.")
                self.add_item("Duct Tape")
            elif item == "Pocket Knife":
                type.type(bright(magenta("You got a Pocket Knife!")))
                print()
                type.type("A small Swiss Army style knife. Has a tiny scissor and everything.")
                self.add_item("Pocket Knife")
            elif item == "Bag of Acorns":
                type.type("You got a " + bright(magenta("Bag of Acorns!")))
                print()
                type.type("Perfect for feeding squirrels. Or throwing at people, I guess.")
                self.add_item("Bag of Acorns")
            elif item == "Can of Tuna":
                type.type("You got a " + bright(magenta("Can of Tuna!")))
                print()
                type.type("Chunk light in water. Cats love this stuff.")
                self.add_item("Can of Tuna")
            elif item == "Lettuce":
                type.type("You got some " + bright(magenta("Lettuce!")))
                print()
                type.type("A sad, wilted head of iceberg lettuce. Kyle looks at you weird.")
                self.add_item("Lettuce")
            elif item == "Binoculars":
                type.type(bright(magenta("You got Binoculars!")))
                print()
                type.type("See things far away. Very far away. Creepily far away.")
                self.add_item("Binoculars")
            
            # === SPECIAL ITEMS ===
            elif item == "LifeAlert":
                type.type(bright(magenta("You got LifeAlert!")))
                print()
                type.type("'Help, I've fallen and I can't get up!' Now you're prepared for the worst.")
                self.add_item("LifeAlert")
            elif item == "Lottery Ticket":
                type.type(bright(magenta("You got a Lottery Ticket!")))
                print()
                lottery_result = random.randrange(100)
                if lottery_result == 0:
                    winnings = random.randint(1000, 5000)
                    type.type("Holy crap! You scratch it right there and... " + green(bright("YOU WON ${:,}!".format(winnings))))
                    self.change_balance(winnings)
                elif lottery_result < 10:
                    winnings = random.randint(10, 50)
                    type.type("You scratch it and win " + green(bright("${:,}".format(winnings))) + ". Not bad!")
                    self.change_balance(winnings)
                else:
                    type.type("You scratch it eagerly... nothing. As expected.")
            elif item == "Lucky Penny":
                type.type(bright(magenta("You got a Lucky Penny!")))
                print()
                type.type("Heads up! That's good luck, right?")
                self.add_item("Lucky Penny")
            elif item == "Lucky Rabbit Foot":
                type.type(bright(magenta("You got a Lucky Rabbit Foot!")))
                print()
                type.type("Dyed purple and attached to a little chain. Wasn't so lucky for the rabbit.")
                self.add_item("Lucky Rabbit Foot")
            
            # === PREMIUM ITEMS ===
            elif item == "Expensive Cologne":
                type.type(bright(magenta("You got Expensive Cologne!")))
                print()
                type.type("Smells like money and bad decisions. Perfect for the casino.")
                self.add_item("Expensive Cologne")
            elif item == "Fancy Cigars":
                type.type(bright(magenta("You got Fancy Cigars!")))
                print()
                type.type("Cuban, apparently. Kyle says he 'knows a guy.'")
                self.add_item("Fancy Cigars")
            elif item == "Gold Chain":
                type.type(bright(magenta("You got a Gold Chain!")))
                print()
                type.type("Thick and gaudy. You look like a rapper from 2005.")
                self.add_item("Gold Chain")
            elif item == "Vintage Wine":
                type.type(bright(magenta("You got Vintage Wine!")))
                print()
                type.type("1987. A good year, apparently. You wouldn't know.")
                self.add_item("Vintage Wine")
            
            # === TRAP/CURSED ITEMS ===
            elif item == "Necronomicon":
                type.type(bright(magenta("You got a ") + red("Necronomicon!")))
                print()
                type.type("Kyle looks genuinely disturbed that you bought this. " + quote("Dude, that thing gives me the creeps. Take it and go."))
                self.add_item("Necronomicon")
                self.lose_sanity(5)  # Immediate sanity hit
            elif item == "Cursed Coin":
                type.type(bright(magenta("You got a ") + red("Cursed Coin!")))
                print()
                type.type("It's cold to the touch. Unnaturally cold. The face on it seems to be... frowning?")
                self.add_item("Cursed Coin")
                # Cursed coin has bad effects later
            
            # === RARE MYSTERY ITEMS ===
            elif item == "Mysterious Envelope":
                type.type(bright(magenta("You got a Mysterious Envelope!")))
                print()
                type.type("Sealed with red wax. Kyle says it's been in the lost and found for years.")
                self.add_item("Mysterious Envelope")
            elif item == "Old Photograph":
                type.type(bright(magenta("You got an Old Photograph!")))
                print()
                type.type("Black and white. Shows a family standing in front of... wait, is that the casino?")
                self.add_item("Old Photograph")
            elif item == "Broken Compass":
                type.type(bright(magenta("You got a Broken Compass!")))
                print()
                type.type("The needle spins wildly, never settling. Useless for directions, but... interesting.")
                self.add_item("Broken Compass")
            
            # === RANK 0 ITEMS ===
            elif item == "Cheap Sunscreen":
                type.type(bright(magenta("You got Cheap Sunscreen!")))
                print()
                type.type("SPF 15. Better than nothing, probably.")
                self.add_item("Cheap Sunscreen")
            elif item == "Plastic Poncho":
                type.type(bright(magenta("You got a Plastic Poncho!")))
                print()
                type.type("Clear plastic, one size fits most. Crinkles when you walk.")
                self.add_item("Plastic Poncho")
            elif item == "Breath Mints":
                type.type(bright(magenta("You got Breath Mints!")))
                print()
                type.type("Extra strong. Your breath could use some help after living in a car.")
                self.add_item("Breath Mints")
            elif item == "Rubber Bands":
                type.type(bright(magenta("You got Rubber Bands!")))
                print()
                type.type("A ball of various rubber bands. You never know when you'll need one.")
                self.add_item("Rubber Bands")
            
            # === RANK 1 ITEMS ===
            elif item == "Bug Spray":
                type.type(bright(magenta("You got Bug Spray!")))
                print()
                type.type("Industrial strength. Mosquitoes fear you now.")
                self.add_item("Bug Spray")
            elif item == "Disposable Camera":
                type.type(bright(magenta("You got a Disposable Camera!")))
                print()
                type.type("27 exposures. Capture some memories... or evidence.")
                self.add_item("Disposable Camera")
            elif item == "Road Flares":
                type.type(bright(magenta("You got Road Flares!")))
                print()
                type.type("For emergencies. Or starting fires. No judgment here.")
                self.add_item("Road Flares")
            elif item == "Air Freshener":
                type.type(bright(magenta("You got an Air Freshener!")))
                print()
                type.type("Pine scent. Your car desperately needs this.")
                self.add_item("Air Freshener")
            
            # === RANK 2 ITEMS ===
            elif item == "Padlock":
                type.type(bright(magenta("You got a Padlock!")))
                print()
                type.type("Combination lock. 4 digits. You set it to something you'll remember... hopefully.")
                self.add_item("Padlock")
            elif item == "Fishing Line":
                type.type(bright(magenta("You got Fishing Line!")))
                print()
                type.type("50 yards of monofilament. Strong enough to catch a big one.")
                self.add_item("Fishing Line")
            elif item == "Super Glue":
                type.type(bright(magenta("You got Super Glue!")))
                print()
                type.type("Bonds in seconds. Kyle warns you not to glue your fingers together. Voice of experience.")
                self.add_item("Super Glue")
            elif item == "Hand Warmers":
                type.type(bright(magenta("You got Hand Warmers!")))
                print()
                type.type("Just snap 'em and they heat up. Good for cold nights.")
                self.add_item("Hand Warmers")
            
            # === RANK 3 ITEMS ===
            elif item == "Leather Gloves":
                type.type(bright(magenta("You got Leather Gloves!")))
                print()
                type.type("Soft Italian leather. Makes you feel like a professional at... something.")
                self.add_item("Leather Gloves")
            elif item == "Silver Flask":
                type.type(bright(magenta("You got a Silver Flask!")))
                print()
                type.type("Engraved with initials. Not yours, but that's fine.")
                self.add_item("Silver Flask")
            elif item == "Fancy Pen":
                type.type(bright(magenta("You got a Fancy Pen!")))
                print()
                type.type("A Mont Blanc knockoff. Still writes nicely though.")
                self.add_item("Fancy Pen")
            
            # === RANK 4+ ITEMS ===
            elif item == "Silk Handkerchief":
                type.type(bright(magenta("You got a Silk Handkerchief!")))
                print()
                type.type("Embroidered edges. Very classy. You stuff it in your pocket.")
                self.add_item("Silk Handkerchief")
            elif item == "Monogrammed Lighter":
                type.type(bright(magenta("You got a Monogrammed Lighter!")))
                print()
                type.type("Gold-plated Zippo. Has someone else's initials, but fire is fire.")
                self.add_item("Monogrammed Lighter")
            elif item == "Antique Pocket Watch":
                type.type(bright(magenta("You got an Antique Pocket Watch!")))
                print()
                type.type("Victorian era, supposedly. Ticks with a satisfying rhythm.")
                self.add_item("Antique Pocket Watch")
            
            # === CAR MAINTENANCE ITEMS ===
            elif item == "Jumper Cables":
                type.type(bright(magenta("You got Jumper Cables!")))
                print()
                type.type("Red and black. 12 feet long. Dead battery? Not your problem anymore.")
                self.add_item("Jumper Cables")
            elif item == "Portable Battery Charger":
                type.type(bright(magenta("You got a Portable Battery Charger!")))
                print()
                type.type("Compact and powerful. No more flagging down strangers.")
                self.add_item("Portable Battery Charger")
            elif item == "Spare Fuses":
                type.type(bright(magenta("You got Spare Fuses!")))
                print()
                type.type("Assorted sizes. Electrical problems, meet your match.")
                self.add_item("Spare Fuses")
            elif item == "Spare Headlight Bulbs":
                type.type(bright(magenta("You got Spare Headlight Bulbs!")))
                print()
                type.type("H7 bulbs. No more driving blind at night.")
                self.add_item("Spare Headlight Bulbs")
            elif item == "Motor Oil":
                type.type(bright(magenta("You got Motor Oil!")))
                print()
                type.type("5W-30. The lifeblood of your engine.")
                self.add_item("Motor Oil")
            elif item == "Coolant":
                type.type(bright(magenta("You got Coolant!")))
                print()
                type.type("Green antifreeze. Keeps your engine from overheating. Or freezing.")
                self.add_item("Coolant")
            elif item == "Antifreeze":
                type.type(bright(magenta("You got Antifreeze!")))
                print()
                type.type("Same as coolant, really. Your engine will thank you.")
                self.add_item("Antifreeze")
            elif item == "Brake Fluid":
                type.type(bright(magenta("You got Brake Fluid!")))
                print()
                type.type("DOT 3. Because stopping is important.")
                self.add_item("Brake Fluid")
            elif item == "Power Steering Fluid":
                type.type(bright(magenta("You got Power Steering Fluid!")))
                print()
                type.type("Makes turning the wheel less of a workout.")
                self.add_item("Power Steering Fluid")
            elif item == "Transmission Fluid":
                type.type(bright(magenta("You got Transmission Fluid!")))
                print()
                type.type("ATF. Red and slippery. Keeps your gears happy.")
                self.add_item("Transmission Fluid")
            elif item == "Water Bottles":
                type.type(bright(magenta("You got Water Bottles!")))
                print()
                type.type("A pack of six. For drinking or emergency radiator use.")
                self.add_item("Water Bottles")
            elif item == "Fix-a-Flat":
                type.type(bright(magenta("You got Fix-a-Flat!")))
                print()
                type.type("Spray foam tire sealant. A temporary fix for flat tires.")
                self.add_item("Fix-a-Flat")
            elif item == "Tire Patch Kit":
                type.type(bright(magenta("You got a Tire Patch Kit!")))
                print()
                type.type("Rubber patches, adhesive, and tools. Fix flats like a pro.")
                self.add_item("Tire Patch Kit")
            elif item == "Car Jack":
                type.type(bright(magenta("You got a Car Jack!")))
                print()
                type.type("Scissor style. Makes changing tires actually possible.")
                self.add_item("Car Jack")
            elif item == "Gas Can":
                type.type(bright(magenta("You got a Gas Can!")))
                print()
                type.type("One gallon capacity. Empty now, but fill it for emergencies.")
                self.add_item("Gas Can")
            elif item == "Tool Kit":
                type.type(bright(magenta("You got a Tool Kit!")))
                print()
                type.type("Wrenches, screwdrivers, pliers. Everything a car person needs.")
                self.add_item("Tool Kit")
            elif item == "WD-40":
                type.type(bright(magenta("You got WD-40!")))
                print()
                type.type("If it moves and shouldn't, use duct tape. If it doesn't move and should, use WD-40.")
                self.add_item("WD-40")
            elif item == "Bungee Cords":
                type.type(bright(magenta("You got Bungee Cords!")))
                print()
                type.type("Stretchy and strong. Hold anything to anything.")
                self.add_item("Bungee Cords")
            elif item == "Rope":
                type.type(bright(magenta("You got Rope!")))
                print()
                type.type("50 feet of nylon rope. Useful for... many things.")
                self.add_item("Rope")
            elif item == "Exhaust Tape":
                type.type(bright(magenta("You got Exhaust Tape!")))
                print()
                type.type("Heat-resistant tape for exhaust repairs. Band-aid for your muffler.")
                self.add_item("Exhaust Tape")
            elif item == "Radiator Stop Leak":
                type.type(bright(magenta("You got Radiator Stop Leak!")))
                print()
                type.type("Pour it in, hope for the best. A temporary solution.")
                self.add_item("Radiator Stop Leak")
            elif item == "Oil Stop Leak":
                type.type(bright(magenta("You got Oil Stop Leak!")))
                print()
                type.type("Conditions seals to slow oil leaks. Buys you time.")
                self.add_item("Oil Stop Leak")
            elif item == "Lock De-Icer":
                type.type(bright(magenta("You got Lock De-Icer!")))
                print()
                type.type("Spray it in frozen locks. Winter's not gonna lock you out.")
                self.add_item("Lock De-Icer")
            elif item == "Fuel Line Antifreeze":
                type.type(bright(magenta("You got Fuel Line Antifreeze!")))
                print()
                type.type("Prevents fuel lines from freezing. Essential for cold weather.")
                self.add_item("Fuel Line Antifreeze")
            elif item == "Garbage Bag":
                type.type(bright(magenta("You got a Garbage Bag!")))
                print()
                type.type("Heavy duty. Good for trash or temporary window replacement.")
                self.add_item("Garbage Bag")
            elif item == "Plastic Wrap":
                type.type(bright(magenta("You got Plastic Wrap!")))
                print()
                type.type("Cling wrap. Cover things. Protect things. Improvise things.")
                self.add_item("Plastic Wrap")
            elif item == "OBD Scanner":
                type.type(bright(magenta("You got an OBD Scanner!")))
                print()
                type.type("Plug it in, read the codes. Know what's wrong before the mechanic lies to you.")
                self.add_item("OBD Scanner")
            elif item == "Spare Spark Plugs":
                type.type(bright(magenta("You got Spare Spark Plugs!")))
                print()
                type.type("Four pack. When your engine misfires, you're ready.")
                self.add_item("Spare Spark Plugs")
            elif item == "Serpentine Belt":
                type.type(bright(magenta("You got a Serpentine Belt!")))
                print()
                type.type("The squeal-stopper. When your belt goes, you'll be glad you have this.")
                self.add_item("Serpentine Belt")
            elif item == "Fuel Filter":
                type.type(bright(magenta("You got a Fuel Filter!")))
                print()
                type.type("Keeps the crud out of your engine. A small part with a big job.")
                self.add_item("Fuel Filter")
            elif item == "Thermostat":
                type.type(bright(magenta("You got a Thermostat!")))
                print()
                type.type("Regulates engine temperature. Cheap insurance against overheating.")
                self.add_item("Thermostat")
            elif item == "Brake Pads":
                type.type(bright(magenta("You got Brake Pads!")))
                print()
                type.type("Front set. When the squealing starts, you're prepared.")
                self.add_item("Brake Pads")
            elif item == "Worn Map":
                type.type(bright(magenta("You got a Worn Map!")))
                print()
                type.type("It's old. Hand-drawn. The ink is faded but you can make out trails, landmarks, and... an X.")
                self.add_item("Worn Map")
            elif item == "Dog Whistle":
                type.type(bright(magenta("You got a Dog Whistle!")))
                print()
                type.type("You blow it. Nothing happens. Or does it? You can't hear it, but something out there can.")
                self.add_item("Dog Whistle")
            elif item == "Welding Goggles":
                type.type(bright(magenta("You got Welding Goggles!")))
                print()
                type.type("Heavy-duty. Makes you look like a post-apocalyptic mechanic. Which... isn't far off.")
                self.add_item("Welding Goggles")
            elif item == "Signal Booster":
                type.type(bright(magenta("You got a Signal Booster!")))
                print()
                type.type("A small antenna attachment. Boosts radio reception. Who knows what you'll pick up.")
                self.add_item("Signal Booster")
            
            elif item == "Home":
                type.type("Suit yourself.")
                print("\n")
                self.start_night()
                return
            
            # Track purchase and check for gift system unlock
            items_bought += 1
            self.change_balance(-price)
            gift_unlocked = self.increment_store_purchases()
            
            # Check if gift wrapping system just unlocked
            if gift_unlocked:
                print("\n")
                time.sleep(1)
                type.slow("Kyle puts down his phone and looks at you seriously.")
                print("\n")
                type.slow(quote("Hey, uh... you've been coming here a lot."))
                print("\n")
                type.slow(quote("I've noticed you're doing better. Got more money now, huh?"))
                print("\n")
                type.slow(quote("Listen, I got a side business. Gift wrapping. Classy stuff."))
                print("\n")
                type.slow(quote("You want me to wrap something? Make it look all fancy?"))
                print("\n")
                type.slow(quote("Costs ten bucks. But hey, presentation matters, right?"))
                print("\n")
                type.slow(yellow(bright("GIFT WRAPPING UNLOCKED! You can now wrap items at Kyle's store.")))
                print("\n")
                time.sleep(1)
            
            # Offer gift wrapping if system is unlocked and item is wrappable
            if self.is_gift_system_unlocked() and not self.has_gift_wrapped():
                print("\n")
                wrap_choice = ask.yes_or_no("Want me to gift wrap that for you? ($10) ")
                if wrap_choice == "yes" and self._balance >= 10:
                    if self.wrap_item_as_gift(item, 10):
                        type.type("Kyle wraps it up nice. Real professional-like.")
                        print("\n")
                        type.type(yellow("You now have a wrapped gift. It will automatically be given to the Dealer at the casino."))
                        print("\n")
                elif wrap_choice == "yes":
                    type.type("You don't have enough for the wrapping. Sorry, dude.")
                    print("\n")
            
            print("\n")

            if items_bought == 1:
                random_chance = random.randrange(5)
                if random_chance < 2:
                    type.type("You know what? Rules are made to be broken. I mean, screw em! I hate my manager anyways. ")
                    type.type("You can have one more item, just don't tell anyone I let you do this.")
                    print("\n")
                else:
                    type.type("Welp. There you go. That's your item. Weird thing to buy, if you ask me. Now get lost, I'm going on break.")
                    print("\n")
                    self.start_night()
                    return
            else:
                type.type("Welp. There you go. Two whole items. Wow. Now get lost. I've got a girl to text. She's super hot.")
                print("\n")
                self.start_night()
                return

    # Marvin's Shop and interactions
    def visit_marvin(self):
        self.increment_statistic("marvin_visits")
        type.type("You get in your car and drive to Marvin's Mystical Merchandise. ")
        print("\n")
        inventory = self._lists.make_marvin_inventory()
        if len(inventory) == 0:
            type.type("Sorry man, I've got no product for you tonight. Maybe try coming back another day. ")
            return
        else:
            type.type("Welcome, welcome. I've got some very valuable stuff in stock, just for a fine gambler like you.")
            print("\n")
            type.type("While I won't get bogged down in the details of how I got my hands on it, I think you'll wanna check these out:")
            print("\n")
            if self.has_item("Old Money Identity") or self.has_item("Aristocrat's Touch"):
                luxury_item = "Old Money Identity" if self.has_item("Old Money Identity") else "Aristocrat's Touch"
                type.type("Marvin looks you up and down. A slow, appraising sweep.")
                print("\n")
                type.type(quote("Well, well. Someone's come up in the world.") + " He straightens. Reaches for a shelf you've never noticed before.")
                print("\n")
                type.type("He opens a drawer below the counter, behind a velvet curtain.")
                print("\n")
                type.type(quote("Perhaps you'd be interested in something... premium? Not everything I carry goes on the regular shelf.") + " He slides two extra items into the display with a knowing nod.")
                print("\n")
            if self.has_item("Silver Flask") and not self.has_met("Gave Marvin Flask"):
                type.type("Marvin's eyes land on the " + magenta(bright("Silver Flask")) + " in your pack. He leans forward.")
                print("\n")
                type.type(quote("That's a fine flask. Real silver. I'd take it off your hands — twenty percent off your next purchase, what do you say?"))
                print("\n")
                answer = ask.yes_or_no("Give Marvin the Silver Flask? ")
                if answer == "yes":
                    self.use_item("Silver Flask")
                    self.mark_met("Gave Marvin Flask")
                    self.add_status("Marvin Discount")
                    type.type(quote("Pleasure doing business. The discount is yours."))
                    print("\n")
                else:
                    type.type(quote("Another time, then."))
                    print("\n")

        for item_number in range(len(inventory)):
            item = inventory[item_number]
            if (item_number==0) and (len(inventory)==1):
                type.type("The only item I've got right now is the " + self._lists.get_marvin_adjective() + " " + magenta(bright(item)))
            elif (item_number==0):
                type.type("The first item I've got is the " + self._lists.get_marvin_adjective() + " " + magenta(bright(item)))
            elif item_number==len(inventory)-1:
                type.type("The last item I've got is the " + self._lists.get_marvin_adjective() + " " + magenta(bright(item)))
            else:
                type.type("The next item I've got is the " + self._lists.get_marvin_adjective() + " " + magenta(bright(item)))

            print()

            if item == "Delight Indicator":
                type.type("With this little device, you can read how happy anyone is, just by pointing it at them! Could get you out of a lot of trouble.")
                price = random.choice([3000, 4000, 5000])
            elif item == "Health Indicator":
                type.type("This gadget lets you see how healthy you are at any given moment. It's great for knowing how imminent a trip to the ER is.")
                price = random.choice([3000, 4000, 5000])
            elif item == "Dirty Old Hat":
                type.type("By wearing this, you're telling the whole world \"I'm poor and I'm not afraid to show it!\" It's a foolproof way for people to take pity on you.")
                price = random.choice([9000, 11000, 13000])
            elif item == "Golden Watch":
                type.type("This watch was my grandfathers at one point. It's a beauty. If you're a gambling man, anyone in their right mind would wanna see you betting on their table.")
                price = random.choice([11000, 13000, 15000])
            elif item == "Faulty Insurance":
                type.type("I got this thing forged by a buddy of mine. It's a fake insurance card. I've used it to get out of so many hospital bills, and you could too!")
                price = random.choice([4000, 5000, 6000])
            elif item == "Enchanting Silver Bar":
                type.type("Listen, I know this silver bar looks a bit useless, but I swear, it's awesome. ")
                type.type("Look at the stock market, this thing is only gonna get more and more expensive. ")
                type.type("And if I sell it to you, you can sell it off later and make some money.")
                price = 4000
            elif item == "Sneaky Peeky Shades":
                type.type("These aren't your ordinary pair of glasses. Put them on, and you'll catch glimpses that others can't see. ")
                type.type("But use them wisely; you only get one peek per night.")
                price = random.choice([14000, 16000, 18000])
            elif item == "Quiet Sneakers":
                type.type("Sometimes, the best move is to walk away. Use this when you feel trouble brewing, and avoid the day's misfortunes.")
                price = random.choice([5000, 7000, 9000])
            elif item == "Lucky Coin":
                type.type("This here's an old coin with a four-leaf clover on it. ")
                type.type("My grandma used to say it could turn bad luck into no luck at all. ")
                type.type("Lost a hand? Flip this, and maybe you'll get your bet back.")
                price = random.choice([4000, 5000, 6000])
            elif item == "Worn Gloves":
                type.type("These gloves are pretty beat up, but trust me, they've got some magic left in 'em. ")
                type.type("Wear these when you play, and you'll feel the cards better. Might just get luckier draws.")
                price = random.choice([7000, 8000, 10000])
            elif item == "Tattered Cloak":
                type.type("Don't let the moth holes fool ya. This cloak's got some sneaky enchantment. Dealers sometimes just... forget to collect when you lose. Weird, right?")
                price = random.choice([8000, 10000, 12000])
            elif item == "Rusty Compass":
                type.type("The glass is cracked and it's missing a few screws, but this compass still points to opportunity. ")
                type.type("Carry it around, and you might stumble upon something unexpected.")
                price = random.choice([3000, 4000, 5000])
            elif item == "Pocket Watch":
                type.type("This brass beauty is always running a bit slow, but hey, that works in your favor. Flash it at the table, and you might squeeze in an extra round.")
                price = random.choice([9000, 11000, 13000])
            elif item == "Marvin's Monocle":
                type.type("A polished monocle with a smoky lens and tiny etched markings around the rim. Slip it on, and you can tell exactly how much of your bankroll is hot.")
                type.type("Useful knowledge. Dangerous knowledge. Marvin seems very proud of that distinction.")
                price = random.choice([5000, 7000, 9000])
            # New mystical gambling items
            elif item == "Gambler's Chalice":
                type.type("Ah, the Chalice! Legend says a desperate gambler drank from this cup and doubled his fortune in one night. ")
                type.type("The catch? You can only use its power once per visit. Raise your bet, draw one more card, and pray.")
                price = random.choice([11000, 13000, 15000])
            elif item == "Twin's Locket":
                type.type("This locket contains portraits of twins who could never agree on anything—except cards. ")
                type.type("When you're dealt a pair, this little beauty lets you split 'em and play two hands. Double the risk, double the reward.")
                price = random.choice([14000, 17000, 20000])
            elif item == "White Feather":
                type.type("Plucked from a chicken that ran from every fight—but lived to tell the tale. ")
                type.type("When a hand looks hopeless, wave this feather and surrender with dignity. ")
                type.type("You'll lose half your bet, but keep your pride. Sort of.")
                price = random.choice([5000, 7000, 9000])
            elif item == "Dealer's Grudge":
                type.type("The Dealer dropped this jade pendant years ago. It still pulses with his essence. ")
                type.type("When he shows an Ace, you can invoke the Grudge—take a side bet against his Blackjack. ")
                type.type("If he gets it, you get paid. If not... well, you lose the side bet.")
                price = random.choice([8000, 10000, 12000])
            elif item == "Gambler's Grimoire":
                type.type("This tattered book has a mind of its own. ")
                type.type("It watches every hand you play, tracking your wins, losses, streaks, and failures. ")
                type.type("When you break a record—good or bad—it'll let you know. Sarcastically. Very sarcastically.")
                price = random.choice([3000, 4000, 5000])
            elif item == "Animal Whistle":
                type.type("Marvin lowers his voice, glancing around conspiratorially.")
                print("\n")
                type.type(quote("This... this is special. Very special. I don't show this to just anyone."))
                print("\n")
                type.type("He produces a small silver whistle, carved with intricate animal shapes.")
                print("\n")
                type.type(quote("Blow this, and any creature will trust you. Dog, cat, crow, rat—doesn't matter. "))
                type.type(quote("They'll follow you to the ends of the earth. They'll be your family."))
                print("\n")
                type.type(quote("But here's the secret—if you gather enough of them... if you truly become their shepherd... "))
                type.type(quote("Something magical happens. I've heard stories of people who left this place with an ark of their own."))
                price = 30000

            print()

            if self.has_status("Marvin Discount"):
                discounted_price = int(price * 0.8)
                type.type("Marvin glances at you with a small nod — remembering the flask. " + quote("Twenty percent off, as promised."))
                print("\n")
                price = discounted_price

            type.type("For " + green(bright("${:,}".format(price))) + ", it can be all yours. You buying? ")
            while True:
                yes_or_no = input("").lower()
                if ((yes_or_no == "y") or (yes_or_no == "yes")) and (self._balance<price):
                    print()
                    type.type("Cmon man, you can't afford this.")
                    print("\n")
                    break
                if (yes_or_no == "y") or (yes_or_no == "yes"):
                    print()
                    type.type("Great! It's all yours.")
                    self.change_balance(-price)
                    if self.has_status("Marvin Discount"):
                        self.remove_status("Marvin Discount")
                    self.add_item(item)
                    type.type("You got the " + magenta(bright(item)) + "!")
                    print()
                    type.type("Description: " + self.get_item_desc(item))
                    print("\n")
                    break
                elif (yes_or_no == "n") or (yes_or_no == "no"):
                    print()
                    type.type("Not your thing, huh? Well that's ok. ")
                    break
                else:
                    print()
                    type.type("What was that? ")

        type.type("That's all I've got to sell you tonight. Maybe try coming back another day. ")
        self.start_night()

    # Loan Shark Interaction
    def visit_loan_shark(self):
        self.increment_statistic("loan_shark_visits")
        type.type("You drive to the seediest part of town, down a narrow alley behind a row of shuttered businesses. ")
        print("\n")
        
        if self.has_item("Marvin's Monocle") and not self._loan_shark_monocle_penalty_triggered:
            type.type("Vinnie's stare catches on the monocle perched on your face, and his smile vanishes.")
            print("\n")
            type.type(quote("So Marvin sold you one of those. Means you can tell good paper from bad."))
            print("\n")
            type.type(quote("Knowledge like that comes with a service charge."))
            print("\n")
            self._loan_shark_interest_rate = max(self._loan_shark_interest_rate, 0.35)
            self._loan_shark_fee_rate = max(self._loan_shark_fee_rate, 0.10)
            self._loan_shark_monocle_penalty_triggered = True
            if self.get_loan_shark_debt() > 0:
                surcharge = max(100, int(self.get_loan_shark_debt() * 0.10))
                self._loan_shark_debt += surcharge
                type.type("Vinnie adds a knowing fee of " + red(bright("${:,}".format(surcharge))) + ".")
                print("\n")
            type.type(quote("From now on, the vig's steeper. For smart people, especially."))
            print("\n")
        
        if not self.has_met("Vinnie"):
            self.meet("Vinnie")
            type.type("At the end of the alley, a black sedan idles with its headlights off. ")
            type.type("Leaning against it is a man in a dark leather jacket, gold chain glinting around his neck. ")
            type.type("He's got slicked-back hair and the kind of smile that never reaches his eyes.")
            print("\n")
            type.type("As you approach, he straightens up and looks you over like a butcher sizing up a cut of meat.")
            print("\n")
            type.type(quote("Fresh face. I like fresh faces. Name's Vinnie. And you look like someone who could use some... financial assistance."))
            print("\n")
            type.type("He gestures to the trunk of his car, which is suspiciously open just enough to reveal stacks of cash.")
            print("\n")
            type.type(quote("Simple terms. I give you money. You pay me back. Plus interest. 20% a week. Compound. Miss a payment... well."))
            print("\n")
            type.type("He cracks his knuckles meaningfully.")
            print("\n")
            type.type(quote("Let's just say my associate Tony handles the collections. You don't want to meet Tony."))
            print("\n")
        else:
            # Get greeting based on warning level
            warning_level = self.get_loan_shark_warning_level()
            debt = self.get_loan_shark_debt()
            
            if debt > 0:
                if warning_level >= 4:
                    dialogue = self._lists.get_loan_shark_dialogue("collecting")
                elif warning_level >= 3:
                    dialogue = self._lists.get_loan_shark_dialogue("violence")
                elif warning_level >= 2:
                    dialogue = self._lists.get_loan_shark_dialogue("threat")
                elif warning_level >= 1:
                    dialogue = self._lists.get_loan_shark_dialogue("warning_2")
                else:
                    dialogue = self._lists.get_loan_shark_dialogue("warning_1")
                type.type(dialogue)
                print("\n")
            else:
                type.type(self._lists.get_loan_shark_dialogue("greeting"))
                print("\n")
        
        self.visit_loan_shark_menu()
    
    def visit_loan_shark_menu(self):
        debt = self.get_loan_shark_debt()
        warning_level = self.get_loan_shark_warning_level()
        balance = self.get_balance()
        
        # Show current debt status
        if debt > 0:
            type.type("Current debt: " + red(bright("${:,}".format(debt))))
            print()
            if warning_level > 0:
                status_colors = [yellow, yellow, red, red]
                status_names = ["Overdue", "Very Overdue", "DANGER", "CRITICAL"]
                type.type("Status: " + status_colors[min(warning_level-1, 3)](bright(status_names[min(warning_level-1, 3)])))
                print()
            print()
        if self.has_item("Marvin's Monocle"):
            type.type("Monocle read: " + yellow(bright("${:,}".format(self.get_fraudulent_cash()))) + yellow(" hot cash in circulation"))
            print()
            if self.get_loan_shark_fee_rate() > 0:
                type.type("Knowing fee active: " + red(bright(f"{int(self.get_loan_shark_fee_rate() * 100)}%")) + red(" on new loans"))
                print()
            print()
        
        # Menu options
        type.type("What would you like to do?")
        print()
        if debt == 0 or warning_level < 3:  # Can only borrow if not in too much trouble
            type.type("1. Borrow money")
            print()
        if debt > 0:
            type.type("2. Repay debt")
            print()
        type.type("3. Leave")
        print()
        
        choice = input("Choose: ").strip()
        
        if choice == "1" and (debt == 0 or warning_level < 3):
            self.visit_loan_shark_borrow()
        elif choice == "2" and debt > 0:
            self.visit_loan_shark_repay()
        else:
            if debt > 0 and warning_level >= 2:
                type.type(quote("Running away won't save you. I know where you sleep."))
            else:
                type.type(quote("Don't be a stranger. Money's always available for friends."))
            print("\n")
            self.start_night()
    
    def visit_loan_shark_borrow(self):
        warning_level = self.get_loan_shark_warning_level()
        current_debt = self.get_loan_shark_debt()
        
        # Determine max loan based on reputation and current debt
        if current_debt > 0:
            max_loan = 5000 - current_debt  # Can't owe more than $5000 total
            if max_loan <= 0:
                type.type(quote("You're already in deep enough. Pay off what you owe first."))
                print("\n")
                self.visit_loan_shark_menu()
                return
        else:
            # First-timers or clean records get more options
            max_loan = 5000
        
        type.type(self._lists.get_loan_shark_dialogue("offer"))
        print("\n")
        
        # Loan options
        loan_options = []
        if max_loan >= 100:
            loan_options.append(100)
        if max_loan >= 500:
            loan_options.append(500)
        if max_loan >= 1000:
            loan_options.append(1000)
        if max_loan >= 2500:
            loan_options.append(2500)
        if max_loan >= 5000 and current_debt == 0:
            loan_options.append(5000)
        
        for i, amount in enumerate(loan_options, 1):
            total_owed = amount + int(amount * self.get_loan_shark_fee_rate())
            if total_owed > amount:
                type.type(str(i) + ". Borrow " + green("${:,}".format(amount)) + " (owe " + red("${:,}".format(total_owed)) + ")")
            else:
                type.type(str(i) + ". Borrow " + green("${:,}".format(amount)))
            print()
        type.type(str(len(loan_options) + 1) + ". Never mind")
        print()
        
        try:
            choice = int(input("Choose: ").strip())
            if 1 <= choice <= len(loan_options):
                amount = loan_options[choice - 1]
                type.type(quote("Smart move. Or stupid. We'll see which."))
                print("\n")
                self.take_loan(amount)
                print("\n")
                type.type(quote("Remember. The vig compounds every week."))
                print("\n")
                type.type(quote("And if you can't pay... Tony will explain the alternatives."))
                print("\n")
            else:
                type.type(quote("Cold feet? That's probably smart."))
                print("\n")
        except ValueError:
            type.type(quote("What was that? Speak up."))
            print("\n")
        
        self.visit_loan_shark_menu()
    
    def visit_loan_shark_repay(self):
        debt = self.get_loan_shark_debt()
        balance = self.get_balance()
        
        type.type(quote("Finally doing the right thing, huh? You owe me ") + red(bright("${:,}".format(debt))) + quote("."))
        print("\n")
        
        if balance <= 0:
            type.type(quote("But you're broke. Why are you wasting my time?"))
            print("\n")
            self.visit_loan_shark_menu()
            return
        
        # Repayment options
        type.type("How much do you want to pay?")
        print()
        repay_options = []
        
        if balance >= debt:
            repay_options.append(("Pay in full", debt))
        if balance >= debt // 2 and debt // 2 > 0:
            repay_options.append(("Pay half", debt // 2))
        if balance >= 100:
            repay_options.append(("Pay $100", 100))
        if balance >= 500 and balance < debt:
            repay_options.append(("Pay $500", 500))
        if balance >= 1000 and balance < debt:
            repay_options.append(("Pay $1,000", 1000))
        
        for i, (name, amount) in enumerate(repay_options, 1):
            type.type(str(i) + ". " + name + " (" + green("${:,}".format(amount)) + ")")
            print()
        type.type(str(len(repay_options) + 1) + ". Never mind")
        print()
        
        try:
            choice = int(input("Choose: ").strip())
            if 1 <= choice <= len(repay_options):
                name, amount = repay_options[choice - 1]
                self.repay_loan(amount)
            else:
                if self.get_loan_shark_warning_level() >= 2:
                    type.type(quote("You come here, waste my time, and don't pay? Bold."))
                else:
                    type.type(quote("Make up your mind."))
                print("\n")
        except ValueError:
            type.type(quote("Numbers. I'm looking for numbers."))
            print("\n")
        
        self.visit_loan_shark_menu()

    def loan_shark_encounter(self):
        """Random encounter when loan shark debt is high - DANGEROUS"""
        warning_level = self.get_loan_shark_warning_level()
        debt = self.get_loan_shark_debt()
        
        print("\n")
        type.slow(red(bright("═══════════════════════════════════════")))
        print()
        type.slow(red(bright("         VINNIE WANTS HIS MONEY        ")))
        print()
        type.slow(red(bright("═══════════════════════════════════════")))
        print("\n")
        
        if warning_level >= 4:
            # DEATH TERRITORY
            type.type("You're getting into your car when a van screeches up behind you.")
            print("\n")
            type.type("Men in dark suits pile out. You recognize Tony—Vinnie's enforcer.")
            print("\n")
            type.type("He's carrying a baseball bat. The others have worse.")
            print("\n")
            type.type(quote("Vinnie's done waiting. You owe him ") + red(bright("${:,}".format(debt))) + quote(". Today."))
            print("\n")
            
            if self.get_balance() >= debt:
                answer = ask.option("What do you do? ", ["pay everything", "fight", "beg"])
                if answer == "pay everything":
                    type.type("You hand over every last dollar you owe. Tony counts it, nods.")
                    print("\n")
                    type.type(quote("Smart choice. Vinnie says you're clear. For now."))
                    self.repay_loan(debt)
                    print("\n")
                elif answer == "fight":
                    self.loan_shark_fight()
                else:
                    type.type("You drop to your knees. Tears streaming. Begging for your life.")
                    print("\n")
                    if random.randrange(4) == 0:
                        type.type("Tony hesitates. Something flickers in his eyes.")
                        print("\n")
                        type.type(quote("...One more week. But the interest doubles. And next time, I won't be so nice."))
                        self._loan_shark_debt = int(self._loan_shark_debt * 1.5)
                        self._loan_shark_days_overdue = 14  # Reset to threat level
                        self.lose_sanity(20)
                    else:
                        type.type("Tony shrugs. " + quote("Nothing personal."))
                        self.loan_shark_violence()
            else:
                answer = ask.option("You don't have enough. What do you do? ", ["pay what you have", "fight", "beg"])
                if answer == "pay what you have":
                    balance = self.get_balance()
                    type.type("You empty your pockets. " + green("${:,}".format(balance)) + ". It's not enough.")
                    print("\n")
                    self.repay_loan(balance)
                    type.type(quote("This covers the interest. But you still owe us. We'll be back."))
                    self.hurt(30)  # They rough you up anyway
                    self.lose_sanity(15)
                    print("\n")
                elif answer == "fight":
                    self.loan_shark_fight()
                else:
                    type.type(quote("Begging? Really?"))
                    self.loan_shark_violence()
            print("\n")
            
        elif warning_level >= 3:
            # VIOLENCE TERRITORY
            type.type("You're walking to the casino when a black sedan pulls up beside you.")
            print("\n")
            type.type("The window rolls down. Tony's face appears. He's not smiling.")
            print("\n")
            type.type(quote("Boss says you've been avoiding him. That's not smart."))
            print("\n")
            type.type("Before you can respond, he's out of the car. His fist connects with your stomach.")
            print("\n")
            type.type("You double over. He hits you again. And again.")
            print("\n")
            if random.randrange(3) == 0:
                type.type("Tony kicks the side of your knee. Then the other one. A wet pop. You scream.")
                print("\n")
                type.type(quote("Reminder's over. Next stop is your kneecaps."))
                self.add_danger("Busted Kneecaps")
            else:
                type.type(quote("That's a reminder. Next time, we take something you can't grow back."))
            print("\n")
            self.hurt(35)
            self.lose_sanity(15)
            print("\n")
            
        elif warning_level >= 2:
            # THREAT TERRITORY
            type.type("There's a note tucked under your windshield wiper.")
            print("\n")
            type.type("It reads: " + red(quote("WE KNOW WHERE YOU SLEEP.")))
            print("\n")
            type.type("Below it, a photo. You, in your car. Last night. Taken from outside.")
            print("\n")
            type.type("Someone was watching you. Someone is always watching you.")
            print("\n")
            self.lose_sanity(12)
            print("\n")
            
        else:
            # WARNING TERRITORY
            type.type("Your phone buzzes. Unknown number.")
            print("\n")
            type.type(quote("Don't forget. You owe Vinnie. He doesn't like to wait."))
            print("\n")
            type.type("The line goes dead before you can respond.")
            self.lose_sanity(5)
            print("\n")
    
    def loan_shark_fight(self):
        """Fight Tony and the goons - VERY DANGEROUS"""
        type.type("You throw a punch at Tony. It connects. He staggers back, surprised.")
        print("\n")
        type.type("Then the other two are on you. Fists. Boots. Something metal.")
        print("\n")
        
        chance = random.randrange(10)
        if chance < 2:
            # You somehow win
            type.type("Adrenaline surges through you. You fight like a cornered animal.")
            print("\n")
            type.type("Somehow—SOMEHOW—you take them down. All three. You're covered in blood.")
            print("\n")
            type.type("Tony is unconscious. You grab his wallet. " + green(bright("$500")) + " and a gun.")
            print("\n")
            type.type("You've made a terrible enemy. But you're alive.")
            self.change_balance(500)
            self.add_item("Tony's Gun")
            self.add_danger("Vinnie's Enemy")
            self.hurt(40)
            self.lose_sanity(20)
            self._loan_shark_debt = 0  # Debt cleared through violence
            self._loan_shark_warning_level = 0
        elif chance < 5:
            # You escape
            type.type("You manage to break free. Run. Don't stop running.")
            print("\n")
            type.type("They're shouting behind you. Something about finding you. About your kneecaps.")
            print("\n")
            type.type("You hide for hours. Shaking. Waiting for them to find you.")
            self.hurt(25)
            self.lose_sanity(20)
        else:
            # You lose badly
            self.loan_shark_violence()
    
    def loan_shark_violence(self):
        """Tony and the goons beat you - GRAPHIC"""
        type.type("They don't hold back.")
        print("\n")
        type.type("The first blow breaks something. You hear it crack.")
        print("\n")
        type.type("You're on the ground. Curled up. Trying to protect your head.")
        print("\n")
        type.type("Boots. Over and over. Your ribs. Your back. Your face.")
        print("\n")
        time.sleep(1)
        type.type("...")
        print("\n")
        time.sleep(1)
        
        chance = random.randrange(10)
        if chance < 3:
            # You survive, barely
            type.type("You wake up in an alley. Sun is coming up.")
            print("\n")
            type.type("Everything hurts. You can barely move. But you're alive.")
            print("\n")
            type.type("They left a message carved into your arm: " + red(quote("PAY")))
            print("\n")
            self.hurt(60)
            self.lose_sanity(30)
            self.add_status("Broken Ribs")
            self.add_status("Concussion")
            self.add_danger("Scarred")
        elif chance < 7:
            # You survive, they take something
            type.type("Tony leans down. His face is inches from yours.")
            print("\n")
            type.type(quote("Consider this a payment plan."))
            print("\n")
            if random.randrange(2) == 0:
                type.type("He pulls out a knife. Grabs your left hand.")
                print("\n")
                type.slow(red("..."))
                print("\n")
                type.type("You wake up in a hospital. Missing a finger. They found you in a dumpster.")
                self.add_danger("Missing Finger")
            else:
                type.type("Tony plants one boot on your thigh and raises the bat over your knee.")
                print("\n")
                type.slow(red("CRACK."))
                print("\n")
                type.type("Then the other side. Just to make the lesson symmetrical.")
                print("\n")
                type.type("You wake up in a hospital doped to the eyeballs, both knees wrapped like gifts.")
                self.add_danger("Busted Kneecaps")
            print("\n")
            type.type("The debt is halved. The message is clear.")
            self._loan_shark_debt = self._loan_shark_debt // 2
            self.hurt(50)
            self.lose_sanity(40)
            self.add_status("Severe Trauma")
        else:
            # You don't survive
            type.type("Tony's boot comes down one final time.")
            print("\n")
            type.type("You don't feel it.")
            print("\n")
            type.type("You don't feel anything anymore.")
            print("\n")
            self.kill("beaten to death by loan sharks")

    # Pawn Shop Interaction
    def visit_pawn_shop(self):
        self.increment_statistic("pawn_shop_visits")
        type.type("You get in your car and drive down a winding backstreet to Grimy Gus's Pawn Emporium. ")
        print("\n")
        if not self.has_met("Pawn Shop"):
            self.meet("Pawn Shop")
            type.type("The shop is tucked between a boarded-up laundromat and a place that just says 'MEAT' in flickering neon. ")
            type.type("The windows are blacked out, and the door looks like it hasn't been painted since the Cold War.")
            print("\n")
            type.type("You push inside. The smell hits you first-mothballs, old leather, and something vaguely chemical. ")
            type.type("Every surface is covered in dusty trinkets, tarnished jewelry, and items that probably have stories you don't want to hear.")
            print("\n")
            type.type("In the corner, you notice a strange contraption-rusted pipes, grinding gears, and a funnel on top. A sign reads: " + cyan(bright("\"THE GARBLE MACHINE\"")))
            print("\n")
            type.type("Grimy Gus sits behind a counter made of stacked milk crates, reading a newspaper from three weeks ago. He looks up and grins, revealing those yellow teeth.")
            print("\n")
            type.type(quote("Ah, you came! I knew you would. People like us... we understand each other."))
            print("\n")
        else:
            type.type(quote("Back again, eh? Let's see what treasures you've dug up this time."))
            print("\n")
        
        # Get collectible prices
        collectible_prices = self.get_collectible_prices()
        all_collectibles = self.get_all_collectibles_list()
        total_collectibles = len(all_collectibles)
        items_sold = self.get_gus_items_sold()
        
        if self.has_item("Kingpin Look"):
            type.type("Gus looks up. His eyes track the gold chain, the cigar, the way you fill the doorframe.")
            print("\n")
            type.type(quote("Oh. OH. Sir, I — I didn't realize. Please.") + " Gus's hands are trembling as he straightens up behind the counter. " + quote("Premium prices for you. Whatever you need."))
            print("\n")
            type.type("You notice the shaking doesn't quite stop. Criminal heat has a way of preceding you now.")
            self.add_status("Kingpin Reputation")
            collectible_prices = {item: int(price * 1.25) for item, price in collectible_prices.items()}
            print("\n")
        
        if self.has_item("Binding Portrait"):
            type.type("You set the " + cyan(bright("Binding Portrait")) + " on the counter while digging through your bag. Gus glances at it.")
            print("\n")
            type.type("His pupils dilate. His voice drops to a register that isn't entirely his.")
            print("\n")
            type.type(quote("I'll give you whatever you want,") + " he says, flatly. Then he blinks hard and shakes his head, pretending that didn't happen.")
            self.lose_sanity(1)
            print("\n")
        
        # Gus's hints about collecting everything
        if items_sold >= 5 and items_sold < total_collectibles - 10:
            type.type("Gus scratches his chin thoughtfully.")
            print("\n")
            type.type(quote("You know... I'm working on something. Something special. "))
            type.type(quote("If you keep bringing me treasures, ALL the treasures... I might just share my most precious grime with you."))
            print("\n")
        elif items_sold >= total_collectibles - 10 and items_sold < total_collectibles - 5:
            remaining = total_collectibles - items_sold
            type.type("Gus's eyes gleam with anticipation.")
            print("\n")
            type.type(quote("You're getting close, friend. Real close. "))
            type.type(quote("Only about ") + yellow(bright(str(remaining))) + quote(" more unique items and you'll see something nobody else has ever seen."))
            print("\n")
        elif items_sold >= total_collectibles - 5 and items_sold < total_collectibles:
            remaining = total_collectibles - items_sold
            type.type("Gus is practically vibrating with excitement.")
            print("\n")
            type.type(quote("Just ") + yellow(bright(str(remaining))) + quote(" more! Just ") + yellow(bright(str(remaining))) + quote(" more unique treasures and the GRIME will be yours!"))
            print("\n")
        
        # Find what player can sell
        sellable_items = []
        for item, price in collectible_prices.items():
            if self.has_item(item):
                sellable_items.append((item, price))
        
        # Menu options
        type.type("What would you like to do?")
        print()
        type.type("1. See what I can sell")
        print()
        type.type("2. Start selling")
        print()
        
        # DARK OPTION: Sell companions (only if you have 3+)
        companion_count = len(self.get_all_companions())
        if companion_count >= 3:
            type.type("3. Ask about... other merchandise")
            print()
            type.type("4. Leave")
            print()
        else:
            type.type("3. Leave")
            print()
        
        choice = input("Choose: ").strip()
        
        if choice == "1":
            # List what player has
            print("\n")
            if len(sellable_items) == 0:
                type.type(quote("You got nothing I want right now. Come back when you've found some treasures out in the world."))
                print("\n")
            else:
                type.type(quote("Let me see here... you've got some interesting stuff:"))
                print("\n")
                for item, price in sellable_items:
                    already_sold = " " + yellow("(already sold one)") if self.has_sold_to_gus(item) else ""
                    type.type("  • " + cyan(bright(item)) + " - " + green("${:,}".format(price)) + already_sold)
                    print()
                print()
                type.type(quote("That's ") + yellow(bright(str(len(sellable_items)))) + quote(" items I'd be willing to take off your hands."))
                print("\n")
                type.type(quote("I've bought ") + yellow(bright(str(items_sold))) + quote(" unique collectibles from you so far. "))
                type.type(quote("Out of... well, let's just say there's a LOT more out there."))
                print("\n")
            
            # Recurse back to menu
            self.visit_pawn_shop_menu(sellable_items, collectible_prices)
            return
        
        elif choice == "2":
            if len(sellable_items) == 0:
                type.type(quote("You got nothing I want. Come back when you've got something interesting."))
                print("\n")
                self.start_night()
                return
            self.visit_pawn_shop_sell(sellable_items, collectible_prices)
            return
        
        elif choice == "3":
            # Check if this is the "other merchandise" option or leave option
            companion_count = len(self.get_all_companions())
            if companion_count >= 3:
                # Dark option - sell companions
                self.pawn_shop_dark_option()
                return
            else:
                # Regular leave option
                type.type(quote("Come back when you've got the goods."))
                print("\n")
                self.start_night()
                return
        
        elif choice == "4":
            type.type(quote("Come back when you've got the goods."))
            print("\n")
            self.start_night()
            return
        
        else:
            type.type(quote("Come back when you've got the goods."))
            print("\n")
            self.start_night()
            return
    
    def visit_pawn_shop_menu(self, sellable_items, collectible_prices):
        """Return to pawn shop menu after viewing inventory"""
        type.type("What would you like to do?")
        print()
        type.type("1. Start selling")
        print()
        type.type("2. Leave")
        print()
        
        choice = input("Choose: ").strip()
        
        if choice == "1":
            if len(sellable_items) == 0:
                type.type(quote("You got nothing I want. Come back when you've got something interesting."))
                print("\n")
                self.start_night()
                return
            self.visit_pawn_shop_sell(sellable_items, collectible_prices)
        else:
            type.type(quote("Come back when you've got the goods."))
            print("\n")
            self.start_night()
    
    def visit_pawn_shop_sell(self, sellable_items, collectible_prices):
        """Handle the selling process at Gus's shop"""
        type.type(quote("Let me take a look at what you've got..."))
        print("\n")
        
        sold_something = False
        total_collectibles = self.get_gus_total_collectibles()
        
        # Gus's unique descriptions for items
        gus_descriptions = {
            # Underwater Legendary
            "Golden Trident": "Sweet mother of Neptune! A GOLDEN TRIDENT! The kind of thing kings kill for. The kind of thing that makes men mad.",
            "Kraken Pearl": "This... this came from a KRAKEN? Do you have ANY idea how many sailors are at the bottom of the ocean because of these things?",
            "Mermaid Crown": "Royalty of the deep. The fish-ladies don't just GIVE these away. Someone's gonna be looking for this.",
            "Kraken's Memory": "I can feel it... pulsing. Like it's remembering something terrible. I LOVE it.",
            "Ancient Sea Map": "Maps to places that ain't supposed to exist anymore. Or places that never should've existed at all.",
            "Deep Stone": "Heavy. Too heavy for its size. Like it's got the whole ocean compressed into it.",
            "Pirate Treasure": "YARR! Just kidding. But seriously, this is the real deal. Probably has a curse on it.",
            "Treasure Coordinates": "Numbers that lead to riches. Or death. Usually both.",
            "Captain's Compass": "Points somewhere, but not north. Somewhere more... interesting.",
            "Cannon Gem": "Pulled from a sunken warship? These absorb the violence of their history.",
            "Sailor's Lockbox": "Sailors kept their deepest secrets in these. Their real names. Their real sins.",
            "Mermaid's Pearl": "From a mermaid's own collection. They say these grant wishes. They also say wishes have prices.",
            "Mermaid Pearl": "Pretty thing. Probably worth more than my whole shop. Probably cursed too.",
            "Matched Pearls": "A matching pair! The ocean hates giving up pairs. You must've impressed someone down there.",
            "Pink Pearl": "Pink for love, they say. Or pink for blood diluted in seawater. Depends who you ask.",
            "Giant Oyster": "Still sealed? Bold. Could be a pearl in there. Could be a tiny angry crab.",
            "Live Fish": "A LIVE fish? In your pocket? HOW? You know what, I don't wanna know. Tank's in the back.",
            "Moon Shard": "This fell from the MOON? It's humming. It's HUMMING. I'm both terrified and fascinated.",
            # Beach Events
            "Golden Shovel": "Solid gold? For DIGGING? Someone had more money than sense. My kind of customer.",
            "Underwater Camera": "Full of someone else's memories. I'll sell 'em to the highest bidder.",
            "Crab Racing Trophy": "First place in CRAB RACING? This is a thing? I love this world.",
            "Championship Medal": "You won something! Or you stole this. Either way, I'm buying.",
            "Antique Ring": "Engagement ring, by the looks of it. Sad story here. I can sell sad stories.",
            "Treasure Chest": "The whole chest? With actual treasure? Christmas came early.",
            "Midnight Rose": "A rose that blooms at midnight? Either magic or very confused. Both valuable.",
            # Woodlands
            "Hunter's Mark": "The hunters gave you this? You must've killed something impressive. Or stupid.",
            "Bear King's Respect": "THE Bear King? As in the giant nightmare bear? And you have its RESPECT?",
            "Giant Bear Tooth": "This tooth is bigger than my hand. The bear it came from must be the size of a truck.",
            "Bear's Gold Coin": "Bears don't use currency. Which means this came from someone the bear ATE.",
            "Witch's Favor": "A favor from a witch. Dangerous to keep. Dangerous to sell. I'll take that risk.",
            "Magic Acorn": "Plant this and who knows what grows? A money tree? A murder tree? Only one way to find out.",
            "Fairy's Secret Map": "Fairies guard their secrets jealously. This map is probably booby-trapped.",
            "Captured Fairy": "A LIVE FAIRY? In a jar? This is either very valuable or very illegal. Probably both.",
            # Swamp
            "Gator Tooth Necklace": "Gator teeth. Strung together by someone who lived in the swamp too long.",
            "Tortoise Trophy": "First place in TORTOISE RACING? These swamp folks are wild.",
            "Ogre's Gemstone": "From an actual ogre? These things are worth a fortune. The ogre probably wasn't happy.",
            "Ogre's Gift": "The ogre GAVE you this? What did you do, compliment its cooking?",
            "Swamp Gold": "Gold from the swamp. Probably pulled off a corpse. I don't judge.",
            "Witch's Riddle": "A riddle from a witch. Answer it wrong and bad things happen. Not my problem anymore.",
            "Witch's Ward": "Protection magic. Good stuff. Someone out there is now unprotected.",
            "Voodoo Doll": "Ooh, careful with this one. Stick a pin in the wrong place and someone has a VERY bad day.",
            "Lucky Lure": "Lucky for fishing. Unlucky for fish. The circle of life.",
            "Earl's Lucky Lure": "Earl's personal lure? Earl must be either dead or very generous.",
            "Granny's Swamp Nectar": "Swamp granny moonshine. This stuff could strip paint. Or cure diseases. Same thing.",
            # City
            "Key to the City": "They gave you a KEY TO THE CITY? You're either a hero or a really good liar.",
            "Hero Medal": "For heroism? In THIS economy? You must've done something actually good.",
            "Fight Champion Belt": "Underground fighting? You've got more guts than brains. I respect that.",
            "Stolen Watch": "I'm not gonna ask where this came from. That's not how Gus does business.",
            "Suspicious Package": "I'm DEFINITELY not gonna ask about this one. Just give it here.",
            # Rabbit
            "Lucky Penny": "A penny for luck. Five bucks for your penny. That's the Gus markup.",
            "Lucky Rabbit Foot": "Wasn't lucky for the rabbit. But it might be lucky for me.",
            "Carrot": "A... carrot. You're bringing me a carrot. Fine. FINE. I'll take the stupid carrot.",
            "Rabbit's Blessing": "The rabbit BLESSED you? That's not a normal rabbit. This blessing might actually be worth something.",
            # Misc
            "Mysterious Lockbox": "Locked box, no key. The mystery is half the value.",
            "Mysterious Key": "A key with no lock. Someone out there is very frustrated.",
            "Mysterious Code": "Numbers and symbols that mean something to someone. Not me. But someone.",
            "Fountain Water": "From the Fountain of Youth? Either this is priceless or you got scammed.",
            "Treasure Map": "X marks the spot. Or X marks the trap. One way to find out.",
            "Joe's Treasure Map": "Joe's map specifically? Joe's dead, isn't he? Don't answer that.",
            # Secret
            "Dealer's Joker": "This... this came from HIM? The Dealer? I've heard stories. This card shouldn't exist.",
            "Ace of Spades": "The death card. The money card. The Gus-wants-it card.",

            # ═══════ CRAFTED ITEMS — TIER 1 GADGETS ═══════
            "Headlamp": "A flashlight taped to your FACE? That's not a gadget, that's a cry for help. But I know a guy who mines at night. He'd pay for this.",
            "Spotlight": "Flashlight binoculars? You built a... light cannon? I don't know what to call this but it WORKS and that means it SELLS.",
            "Evidence Kit": "A camera that transmits? To WHERE? You know what, don't tell me. The less I know the less I testify.",
            "Radio Jammer": "This thing kills ALL signals? As in phones? Police scanners? Ankle monitors? I'm asking for a friend.",
            "EMP Device": "You built an EMP in a GAS STATION? How are you not in jail? How is the gas station not on FIRE?",
            "Distress Beacon": "Three-county range? The GOVERNMENT doesn't have three-county range. Who ARE you?",
            "Security Bypass": "Picks any lock? Any lock at all? ...How much did you say you wanted for this again?",

            # ═══════ CRAFTED ITEMS — TIER 1 DISGUISES ═══════
            "Low-Profile Outfit": "Sunglasses under a poncho. You look like nobody. I LOVE nobody. Nobody never gets caught.",
            "Beach Bum Disguise": "Tourist camouflage. Smart. Nobody robs a tourist — too much paperwork for the cops.",
            "Gas Mask": "Custom filtration! Made from... air freshener? It smells like a rental car but it'll save your lungs.",
            "Storm Suit": "An umbrella SUIT? You look like a tent with legs. But rain bounces right off. Engineering!",
            "Brass Knuckles": "A padlock in a glove. Elegant. Brutal. Elegantly brutal. My three favorite words.",
            "Gentleman's Charm": "You smell like a department store and look like you own one. This cologne trick is GOOD.",
            "Forged Documents": "Fake papers? There's a BALLPOINT PEN government seal on this? You know what, it's close enough. Government seals all look fake anyway.",

            # ═══════ CRAFTED ITEMS — TIER 1 TONICS ═══════
            "Antacid Brew": "Baking soda water? My grandmother made this! Cured everything. Gas, heartburn, existential dread.",
            "Trail Mix Bomb": "Seeds and matches? A birdseed BOMB? What kind of chaotic genius... Actually, I know a guy. He'll buy six.",
            "Animal Bait": "This ziplock bag just attracted THREE squirrels through the WALL. Whatever you mixed in there, it's working.",
            "Stink Bomb": "I can smell it through the JAR. My eyes are watering through the JAR. I'll take it. From a distance.",
            "Voice Soother": "Your voice dropped two octaves while explaining this. The product IS the demonstration.",
            "Outdoor Shield": "Bug proof AND sun proof? In ONE bottle? Congratulations, you just replaced two industries.",
            "Cool Down Kit": "Cold sunscreen water. Simple. Effective. Sometimes the best inventions are the dumbest ones.",
            "Smoke Flare": "Thick smoke in a bag? You could signal a rescue. Or commit a heist. I'm not judging either way.",
            "Vermin Bomb": "Nuclear pest control? In a CUP? My exterminator charges $200 an hour. You just put him out of business.",

            # ═══════ CRAFTED ITEMS — TIER 1 DARK ARTS ═══════
            "Eldritch Candle": "Why is the flame GREEN? Why does it RELIGHT ITSELF? Why is my shop suddenly COLD? Get this thing OUT. ...Wait. How much?",
            "Binding Portrait": "The photograph just BLINKED. I saw that. IT BLINKED. I'm charging extra for the nightmares I'm about to have.",
            "Blackmail Letter": "Beautiful penmanship for a threat letter. Very classy. Very terrifying. Very sellable to the right buyer.",
            "Devil's Deck": "The face cards are LOOKING AT ME. The jokers are GRINNING. I'll buy it but I'm not touching it with my bare hands.",
            "Fortune Cards": "The cards just shuffled BY THEMSELVES on my counter. I'm putting these in the back. The very far back.",

            # ═══════ CRAFTED ITEMS — TIER 1 LUXURY ═══════
            "Kingpin Look": "Gold chain and cigars? You look like you own this parking lot. Hell, you look like you own THIS BLOCK.",
            "Enchanted Vintage": "Wine in a silver flask that gets BETTER? I took one sip and I saw God. Then I saw the price tag. Then I saw God again.",
            "Heirloom Set": "A watch and pen with fake family initials? I'm not crying. I'm APPRAISING. These look like real generational wealth.",
            "Aristocrat's Touch": "Silk pocket square, leather gloves. You look like you've never worked a day in your life. The HIGHEST compliment.",
            "Power Move Kit": "The lighter snap, the cigar lean — you practiced, didn't you? Don't tell me. The mystique is the VALUE.",
            "Animal Magnetism": "Cologne on leather gloves? I just shook your hand and almost AGREED to a lower price. This stuff is DANGEROUS.",
            "Luck Totem": "Two lucky charms fused? This thing just SWUNG toward my safe. I'm taking that as a VERY good sign.",

            # ═══════ CRAFTED ITEMS — TIER 1 VEHICLE ═══════
            "Tire Ready Kit": "Pre-assembled roadside rescue? My mechanic charges $150 for this. You built it for what, eight bucks?",
            "Power Grid": "It says 'NOT A BOMB' in Sharpie. That's either very reassuring or very concerning. But the jumpstart works.",
            "Miracle Lube": "The color of this liquid does NOT exist in nature. But the hinge on my door hasn't squeaked since you showed me. I'll take twelve.",
            "Mobile Workshop": "Tools organized by 'panic frequency'? That's not engineering, that's SURVIVAL INSTINCT. I respect it deeply.",
            "Pursuit Package": "Dog whistle and running shoes? Either you're chasing something or running from something. Either way, you need both.",

            # ═══════ CRAFTED ITEMS — TIER 2 ═══════
            "Assassin's Kit": "Shiv AND spray in one grip? This is a felony I can HOLD. I know buyers. Dangerous buyers. The best kind.",
            "Fire Launcher": "A slingshot that launches FIRE? You set a DUMPSTER on fire from HOW far? I want three.",
            "Tear Gas": "You made a CHEMICAL WEAPON in a SANDWICH BAG? My eyes are watering from HERE. Geneva would like a WORD.",
            "Street Fighter Set": "Blade and knuckles? Full melee loadout? You don't fight — you PRESENT OPTIONS.",
            "Survival Bivouac": "Better shelter than my APARTMENT? Made from a blanket? I need to rethink my life choices.",
            "Hydration Station": "Clean water, forever? You just solved a problem that governments can't. From a tarp.",
            "Provider's Kit": "Land AND sea food? You're basically a supermarket with legs. A one-man grocery chain.",
            "Fortified Perimeter": "Fifty-foot kill zone around your CAR? The military should be STUDYING you.",
            "All-Weather Armor": "HAZMAT beach vacation? You're immune to EVERYTHING and you look RIDICULOUS and I LOVE IT.",
            "Master Key": "Opens ANYTHING in under five seconds? Please stop demonstrating on MY locks.",
            "Night Scope": "You can see a raccoon's FACE at 100 yards in the DARK? What are you, a government satellite?",
            "SOS Kit": "Eleven-minute rescue time? You're better than 911 and you built this from a MIRROR.",
            "Intelligence Dossier": "A dossier that could fool the CIA. Made from a camera and a ballpoint pen. The CIA should be embarrassed.",
            "Surveillance Suite": "See everything, hear nothing. Counter-intelligence from a SPOTLIGHT. The spies are crying.",
            "Mind Shield": "Anxiety behind a wall? Sleep with no nightmares? Are you selling PEACE? Name your price.",
            "Fortune's Favor": "Stacked luck? Every coin lands heads? I just flipped one. Heads. Again. HEADS. Take my money.",
            "Fate Reader": "Cards that read the FUTURE? The Past card showed my first marriage. I don't want to see the Future card.",
            "Lucid Dreaming Kit": "CONTROL your dreams? The dream asks YOUR permission? That's not a kit, that's a SUPERPOWER.",
            "Old Money Identity": "You look like PREP SCHOOL? You came in here in a PONCHO yesterday! How? HOW?",
            "New Identity": "Complete fresh start? New name, new face, new everything? I know people who'd KILL for this. Literally.",
            "Beast Tamer Kit": "Every animal LINES UP and SITS? You're not a person anymore, you're a DISNEY MOVIE.",
            "Cheater's Insurance": "Cheat AND document it as FAIR PLAY? This is the most evil thing I've ever loved.",
            "Roadside Shield": "Flat tire AND dead battery? Fixed in FIVE MINUTES? My mechanic would weep.",
            "Auto Mechanic": "Your car PURRS now? It hasn't purred since the DEALERSHIP? You scratched the dashboard? ...Adorable.",
            "Rolling Fortress": "Car bunker. Sixty MPH. Alarms on every door. Mad Max would take NOTES.",

            # ═══════ CRAFTED ITEMS — TIER 3 MASTERWORKS ═══════
            "Road Warrior Armor": "Three weapons in a HARNESS? You're not a person, you're a WEAPONS PLATFORM. I'm scared to haggle.",
            "Third Eye": "You can see the FUTURE? Before it HAPPENS? I'm not selling this. I'm USING it. ...Okay fine, name a price.",
            "Nomad's Camp": "Self-sufficient camp? Food, water, shelter, forever? You don't need civilization anymore. That's beautiful and terrifying.",
            "All-Access Pass": "Every lock opens? Every secret revealed? You're not a thief, you're a GOD with a key ring.",
            "Master of Games": "Casino PERFECTION? You could buy a casino with a SMILE? Don't tell me more. I'll just take the money.",
            "Immortal Vehicle": "Self-diagnosing, self-defending? It starts BEFORE you turn the key? Your car is ALIVE and I'm not okay with that.",
            "Gambler's Aura": "Plus fifteen PERCENT? The universe owes you? I dropped a coin and it landed ON ITS EDGE. Twice.",
            "Ark Master's Horn": "Animals ATTEND when you call? Fish jump INTO your hands? You're Noah. You're actual NOAH.",
            "Guardian Angel": "CANNOT DIE? Triple redundancy? Eight-minute rescue? You're not protected, you're IMMORTAL ADJACENT.",
            "Hazmat Suit": "Immune to weather, gas, acid, AND social interaction? That last one might be the biggest perk.",
            "Ghost Protocol": "Nobody can SEE you? Cameras don't FOCUS? You're not invisible, you're IRRELEVANT. That's somehow scarier.",
            "Dark Pact Reliquary": "It WHISPERS. It knows your NAME. The temperature just dropped. I'll give you whatever you want. TAKE IT AWAY.",

            # ═══════ CRAFTED ITEMS — TIER 4 LEGENDARY ═══════
            "Beastslayer Mantle": "You're telling me you're PHYSICALLY INVINCIBLE? That you killed a GATOR to make this? I'm not even haggling. Name your price. I'll pay it. I'll pay DOUBLE. And I'll throw in a hug.",
            "Seer's Chronicle": "A book that WRITES ITSELF? That knows the FUTURE? The pages went blank when I tried to read ahead. It told me I wasn't READY. A BOOK told ME I wasn't ready. I need to sit down.",
            "Wanderer's Rest": "The walking stick GREW ROOTS? And then it grew a TOMATO? One perfect tomato? This isn't crafting, this is CREATION.",
            "Skeleton Key": "The door's lock EXPLAINS ITSELF to you? Why it was locked? What it's PROTECTING? That's not a key, that's UNDERSTANDING. I can't put a price on understanding. But I will.",
            "King of the Road": "Every NPC DEFERS? Every game FAVORS you? A THOUSAND dollars a DAY? You don't need my shop. I need YOUR shop.",
            "War Wagon": "Your car is AWAKE? It ADJUSTS to your hands? The engine BREATHES? I'm not buying a car. I'm adopting a CREATURE.",
            "Moonlit Fortune": "The MATH changed? Permanent twenty percent? Luck became PHYSICS? I'm canceling my retirement fund and following you to a casino.",
            "Leviathan's Call": "Something answered from the DEEP? The fish ATTENDED? Like a COURT? You're king of the OCEAN and you're in my pawn shop?",
            "Last Breath Locket": "TRUE IMMORTALITY? HP cannot reach ZERO? Death goes through the LOCKET? I'm not worthy of touching this. But I'll buy it.",
            "Phantom Rose": "A metal flower that BLOOMS? A mirror to a hallway between SEEN and UNSEEN? You're a LEGEND and legends don't sell at pawn shops. ...But if you're going to, sell to GUS.",
            "Soul Forge": "REWRITE HISTORY? Change ANY past event? One-time use? This is the most powerful thing that has ever been on my counter. I need a moment.",
        }
        
        for item, price in sellable_items:
            type.type("Gus picks up your " + cyan(bright(item)) + " and examines it closely, turning it over in his grimy fingers.")
            print("\n")
            
            # Get Gus's description
            if item in gus_descriptions:
                type.type(quote(gus_descriptions[item]))
            else:
                type.type(quote("Interesting piece you've got here. Very interesting indeed."))
            
            print("\n")
            type.type(quote("I'll give you ") + green(bright("${:,}".format(price))) + quote(" for it. Cash in hand. Right now. What do you say?"))
            print("\n")
            
            answer = ask.yes_or_no("Sell the " + item + "? ")
            if answer == "yes":
                self.lose_item(item)
                self.change_balance(price)
                self.increment_statistic("items_sold")
                sold_something = True
                
                # Track if this is a new unique item sold
                is_new_collectible = not self.has_sold_to_gus(item)
                if is_new_collectible:
                    self.sell_item_to_gus(item)
                
                # THE GARBLE MACHINE RITUAL
                type.type("Gus snatches the " + cyan(bright(item)) + " and scurries over to the Garble Machine.")
                print("\n")
                type.type("He drops it into the funnel on top. The machine groans to life.")
                print("\n")
                time.sleep(0.5)
                type.type(cyan("*GRRRRRIND*"))
                print()
                time.sleep(0.5)
                type.type(cyan("*GARBLE GARBLE GARBLE*"))
                print()
                time.sleep(0.5)
                type.type("The " + cyan(bright(item)) + " is garbled till it's " + yellow("guck") + " and it's " + yellow("goo") + "...")
                print()
                time.sleep(0.5)
                type.type("Then the " + yellow("gunk") + " is turned to " + magenta(bright("GRIME")) + ".")
                print("\n")
                type.type("A tiny bit of dark, shimmering grime drips into a jar behind the counter. Gus watches it with reverent eyes.")
                print("\n")
                type.type(quote("Beautiful. Just beautiful."))
                print("\n")
                
                # Check if all collectibles have been sold
                items_sold_now = self.get_gus_items_sold()
                if items_sold_now == total_collectibles:
                    self.gus_complete_collection()
                    return
                
            else:
                type.type("Gus shrugs and hands it back to you.")
                print("\n")
                type.type(quote("Your loss. Or maybe your gain. The grime will wait."))
                print("\n")
        
        if sold_something:
            items_sold_now = self.get_gus_items_sold()
            type.type("Gus counts out your money with practiced fingers, then slides it across the counter.")
            print("\n")
            type.type(quote("Pleasure doing business. That's ") + yellow(bright(str(items_sold_now))) + quote(" unique treasures you've brought me now. Keep 'em coming."))
        else:
            type.type(quote("Changed your mind on everything, huh? That's fine. The grime can wait."))
        
        print("\n")
        self.start_night()
    
    def gus_complete_collection(self):
        """Called when player has sold every unique collectible to Gus"""
        print("\n")
        type.type(yellow(bright("=== THE COLLECTION IS COMPLETE ===")))
        print("\n")
        type.type("Gus freezes. His whole body trembles. Tears stream down his grimy face.")
        print("\n")
        type.type(quote("You... you did it. You actually did it. Every treasure. Every trinket. Every... everything."))
        print("\n")
        type.type("He reaches under the counter with shaking hands and pulls out a small, ornate jar. Inside, something dark and shimmering swirls like a living shadow.")
        print("\n")
        type.type(quote("My most precious grime. Years of garbling. YEARS. Every item I ever bought, ground down, reduced, purified into this."))
        print("\n")
        type.type("He holds it out to you, his yellow teeth visible in the widest smile you've ever seen.")
        print("\n")
        type.type(quote("It's yours. You've earned it. The ") + magenta(bright("GUS'S PRECIOUS GRIME")) + quote(". Cherish it. CHERISH IT."))
        print("\n")
        type.type("You take the jar. It's warm. It pulses faintly. You have absolutely no idea what to do with it.")
        print("\n")
        self.add_item("Gus's Precious Grime")
        type.type(yellow(bright("You got Gus's Precious Grime!")))
        print("\n")
        type.type("Gus wipes his tears on his stained trench coat.")
        print("\n")
        type.type(quote("Now get out of my shop. I need to be alone with my feelings."))
        print("\n")
        self.start_night()
    
    def pawn_shop_dark_option(self):
        """Selling companions one by one to Gus"""
        print("\n")
        type.type("You hesitate. Your mouth feels dry. The words come out quieter than you intended.")
        print("\n")
        type.type(quote("What about... I mean... do you buy..."))
        print("\n")
        type.type("Gus looks up from his newspaper. His yellow teeth disappear. For once, he's not smiling.")
        print("\n")
        type.type(quote("Animals?"))
        print("\n")
        type.type("The word hangs in the air like a noose.")
        print("\n")
        type.type("You nod.")
        print("\n")
        type.type("Gus sets down his paper very slowly. He studies you with eyes that have seen too much.")
        print("\n")
        type.type(quote("I do. Exotic pet trade. Research facilities. Some questions-not-asked situations."))
        print("\n")
        type.type("He drums his grimy fingers on the counter.")
        print("\n")
        type.type(quote("Payment depends on the animal. Rarity. Condition. Temperament. Bring 'em in one at a time and we'll talk numbers."))
        print("\n")
        type.type("Your stomach churns.")
        print("\n")
        
        answer = ask.yes_or_no("Continue? ")
        
        if answer != "yes":
            type.type("You step back from the counter.")
            print("\n")
            type.type(quote("I... I can't. They're not merchandise."))
            print("\n")
            type.type("Gus nods slowly. Something like respect crosses his face.")
            print("\n")
            type.type(quote("Good. GOOD. Maybe you're not as far gone as I thought."))
            print("\n")
            self.restore_sanity(10)
            self.start_night()
            return
        
        # Show companion selling menu
        self.pawn_shop_sell_companions()
    
    def pawn_shop_sell_companions(self):
        """Menu for selling companions one by one"""
        living_companions = self.get_all_companions()
        
        if len(living_companions) == 0:
            type.type(quote("You got no animals left. Funny how that happened."))
            print("\n")
            type.type("The shop feels colder than it should.")
            print("\n")
            self.start_night()
            return
        
        print("\n")
        type.type(yellow(bright("═══ YOUR COMPANIONS ═══")))
        print("\n")
        
        companion_list = list(living_companions.items())
        for i, (name, data) in enumerate(companion_list, 1):
            comp_type = data['type']
            type.type(f"{i}. {cyan(name)} ({comp_type})")
            print()
        
        type.type(f"{len(companion_list) + 1}. Leave")
        print("\n")
        
        choice = input("Who do you want to sell? ").strip()
        
        try:
            choice_num = int(choice)
            if choice_num == len(companion_list) + 1:
                type.type("You leave quickly, before you can change your mind.")
                print("\n")
                self.start_night()
                return
            elif 1 <= choice_num <= len(companion_list):
                name, data = companion_list[choice_num - 1]
                self.sell_single_companion(name, data)
                return
        except:
            pass
        
        type.type("Invalid choice.")
        print("\n")
        self.pawn_shop_sell_companions()
    
    def sell_single_companion(self, name, data):
        """Sell a single companion to Gus"""
        comp_type = data['type']
        
        print("\n")
        type.type(f"You bring {cyan(bright(name))} to the counter.")
        print("\n")
        type.type("Gus examines them with cold, professional eyes.")
        print("\n")
        
        # Gus's fun/dark descriptions for each animal type
        gus_descriptions = {
            "Cat": "A cat, huh? Research labs love these. Something about their nervous systems. I don't ask questions.",
            "Dog": "Three-legged dog? That actually INCREASES the value. Sympathy buyers pay more. Don't look at me like that.",
            "Alligator": "An ALLIGATOR? In a WAGON? You're crazier than I thought. But I know a guy who runs a roadside zoo...",
            "Deer": "Deer with FAWNS? Oh man. Some rich guy's gonna put this in his private menagerie. Easy sale.",
            "Brown Bear": "A bear. A whole bear. You understand this is several kinds of illegal, right? ...I'll give you cash.",
            "Giant Bear": "A GIANT BEAR? The Bear King himself? Do you know what collectors will pay for this? Do you WANT to know?",
            "Seagull": "It's a seagull. A SEAGULL. You want money for a SEAGULL? ...Fine. Pest control will take it.",
            "Racing Crab": "Racing crab, purple shell, championship bloodline. Underground crab fighting circuit wants this bad.",
            "Tortoise": "Slow, steady, probably gonna outlive both of us. Exotic pet market. Easy money.",
            "Snake": "Living scarf, huh? Snake handler I know will take it. He's only missing three fingers. You'll be fine.",
            "Sea Otter": "Otters are endangered. That means VALUABLE. I know a private aquarium in Dubai...",
            "Giant Octopus": "A KRAKEN? AN ACTUAL KRAKEN? I... I need to make some calls. Don't go anywhere.",
            "Duck Commander": "Thirty trained ducks? THIRTY? There's a circus that'll pay top dollar for this act.",
            "Turtle": "Ancient turtle, probably wise, definitely valuable. Collectors love the mystical angle.",
            "Squirrel": "You're selling Squirrelly? The squirrel that's been with you since the start? ...Your choice, friend.",
            "Pigeon Boss": "Organized pigeon mafia? That's... actually incredible. I know a guy who trains birds for movies.",
            "Horse": "Beautiful horse, strong bloodline. Rancher up north wants breeding stock. Won't ask how you got it.",
            "Cow": "A cow that used to charge money? That's hilarious. Dairy farm will take it. Probably.",
            "Moon Rabbit": "This rabbit GLOWS. It GLOWS. Magic is real and I'm holding it. How much do I pay for MAGIC?",
            "Koi Fish": "Koi fish, golden scales. Feng shui consultants pay stupid money for these. Your loss.",
            "Rabbit": "Fluffy rabbit, good temperament. Pet store will take it. Kids love rabbits. Until they don't.",
            "Raccoon Boss": "Raccoon mafia don? Complete with gang? I've seen everything now. This is worth $3000 easy.",
            "Opossum": "Opossum that plays dead? They all do that. But this one's trained? Neat trick. I'll take it.",
            "Dolphin": "A DOLPHIN? That follows your CAR? The marine park will pay ANYTHING for this. ANYTHING.",
        }
        
        # Get description
        description = gus_descriptions.get(comp_type, "Interesting creature. I know buyers for this sort of thing.")
        type.type(quote(description))
        print("\n")
        
        # Calculate value based on type
        if comp_type in ["Giant Octopus", "Giant Bear", "Moon Rabbit", "Dolphin"]:
            value = random.randint(15000, 30000)
        elif comp_type in ["Brown Bear", "Horse", "Kraken", "Deer"]:
            value = random.randint(5000, 12000)
        elif comp_type in ["Alligator", "Snake", "Racing Crab", "Sea Otter", "Raccoon Boss", "Duck Commander"]:
            value = random.randint(2000, 6000)
        else:
            value = random.randint(500, 3000)
        
        type.type(quote("I'll give you ") + green(bright("${:,}".format(value))) + quote(" for it. Cash. Right now."))
        print("\n")
        
        answer = ask.yes_or_no(f"Sell {name}? ")
        
        if answer != "yes":
            type.type(f"You pull {name} back. Not yet. Maybe not ever.")
            print("\n")
            self.restore_sanity(5)
            self.pawn_shop_sell_companions()
            return
        
        # THE SALE
        print("\n")
        type.slow("Gus makes a phone call. A van arrives within minutes.")
        print("\n")
        type.slow(f"{name} looks at you as they're taken away.")
        print("\n")
        
        # Specific reactions for memorable companions
        if name == "Lucky":
            type.slow("Lucky's tail wags once. Still trusting. Even now.")
        elif name == "Whiskers":
            type.slow("Whiskers hisses and fights. The last sound you hear is her screaming.")
        elif name == "Grace":
            type.slow("Grace's eyes hold yours. The fawns cry out. You look away first.")
        elif name == "Kraken":
            type.slow("The Kraken's ancient eyes judge you. You will be remembered.")
        elif name == "Thunder":
            type.slow("Thunder whinnies once. A sound of betrayal. Of broken trust.")
        elif name == "Squirrelly":
            type.slow("Squirrelly drops the acorn they were holding. It rolls toward you. You don't pick it up.")
        elif name == "Don Coo":
            type.slow("Don Coo's pigeons scatter in panic. The boss never panics. But he looks back. Once.")
        else:
            type.slow("They don't understand. They probably never will.")
        
        print("\n")
        type.slow("The van drives away.")
        print("\n")
        
        # Remove companion and give money
        self.companion_dies(name, "sold")
        self.change_balance(value)
        self.lose_sanity(15)
        
        # Track sales
        self._companions_sold_count += 1
        sold_count = self._companions_sold_count
        
        # Progressive Gus dialogue based on how many sold
        print("\n")
        if sold_count == 1:
            type.type("Gus counts out the money. His hands are steady. Professional.")
            print("\n")
            type.type(quote("First time's always the hardest. Gets easier after this."))
            print("\n")
            self.unlock_achievement("first_sale")
        elif sold_count == 3:
            type.type("Gus counts out the money, then pauses.")
            print("\n")
            type.type(quote("You know what I do with these, right? The animals?"))
            print("\n")
            type.type("You don't answer.")
            print("\n")
            type.type(quote("Processing plant. Out west. They turn 'em into... product."))
            print("\n")
            type.type("Product. The word hangs in the air.")
            print("\n")
            self.unlock_achievement("three_sales")
        elif sold_count == 5:
            type.type("Gus slides the money across the counter slowly.")
            print("\n")
            type.type(quote("Five. That's enough for a batch."))
            print("\n")
            type.type("You look at him.")
            print("\n")
            type.type(quote("Meat cubes. That's what they call it. Little frozen cubes. Pet food, mostly. But some of it... other uses."))
            print("\n")
            type.type("Your stomach turns.")
            print("\n")
            type.type(quote("Don't look at me like that. You BROUGHT them here. I'm just the middleman."))
            print("\n")
            self.unlock_achievement("five_sales")
        elif sold_count == 7:
            type.type("Gus doesn't look at you as he counts the money.")
            print("\n")
            type.type(quote("The plant pays extra for variety. Different animals make different... flavors."))
            print("\n")
            type.type("You feel sick.")
            print("\n")
            type.type(quote("Alligator's got a kick to it. Bear's rich, gamey. The little ones - rabbits, cats - those are tender."))
            print("\n")
            type.type("He's DESCRIBING them. Like a menu.")
            print("\n")
            self.unlock_achievement("seven_sales")
        elif sold_count == 10:
            type.type("Gus pulls out a business card. Hands it to you.")
            print("\n")
            type.type("It reads: " + yellow("'CUBE PROCESSING INC. - Pet Nutrition Solutions'"))
            print("\n")
            type.type(quote("Ten animals. That's a full production run. They're gonna send you a thank you card."))
            print("\n")
            type.type("A thank you card. For murder.")
            print("\n")
            type.type(quote("Keep bringing them. The plant's always hungry."))
            print("\n")
            self.unlock_achievement("ten_sales")
        elif sold_count >= 15:
            # Trigger the ending at 15
            self.betrayal_ending_meat_cubes()
            return
        else:
            type.type("Gus counts out the money. His face is blank.")
            print("\n")
            type.type(quote("Anything else you want to sell?"))
            print("\n")
        
        # Check companion achievement milestones
        self.check_betrayal_achievements()
        
        # Continue the menu
        self.pawn_shop_sell_companions()
    
    def check_betrayal_achievements(self):
        """Check and unlock betrayal milestone achievements"""
        count = self._companions_sold_count
        if count >= 1 and not self.has_achievement("first_sale"):
            self.unlock_achievement("first_sale")
        if count >= 3 and not self.has_achievement("three_sales"):
            self.unlock_achievement("three_sales")
        if count >= 5 and not self.has_achievement("five_sales"):
            self.unlock_achievement("five_sales")
        if count >= 7 and not self.has_achievement("seven_sales"):
            self.unlock_achievement("seven_sales")
        if count >= 10 and not self.has_achievement("ten_sales"):
            self.unlock_achievement("ten_sales")
        if count >= 15 and not self.has_achievement("cube_master"):
            self.unlock_achievement("cube_master")
    
    def betrayal_ending_meat_cubes(self):
        """Ending triggered after selling 15 companions - the meat cube factory revelation"""
        print("\n")
        type.slow(red(bright("═" * 50)))
        type.slow(red(bright("           THE FACTORY")))
        type.slow(red(bright("═" * 50)))
        print("\n")
        
        time.sleep(1)
        
        type.slow("Gus sets down the money. Then he pulls out a folder.")
        print("\n")
        type.slow(quote("Fifteen. That's the threshold."))
        print("\n")
        type.slow("He opens the folder. Inside are photos.")
        print("\n")
        type.slow(quote("Cube Processing Inc. They want to meet you. Personally."))
        print("\n")
        
        time.sleep(2)
        
        type.slow("The first photo: A massive industrial building. Gray. Windowless.")
        print("\n")
        type.slow("The second photo: A production line. Stainless steel. Machinery. Conveyor belts.")
        print("\n")
        type.slow("The third photo: Boxes. Thousands of boxes. Each labeled " + yellow("'Premium Pet Nutrition Cubes'."))
        print("\n")
        
        time.sleep(2)
        
        type.slow(quote("They process about 200 animals a month. Your contributions have been... significant."))
        print("\n")
        type.slow("You stare at the photos. You can't look away.")
        print("\n")
        type.slow(quote("The company wants to offer you a partnership. Supply chain coordinator. You'd get a percentage of sales."))
        print("\n")
        
        time.sleep(2)
        
        type.slow("Your hands are shaking.")
        print("\n")
        type.slow(quote("Think about it. You've already proven you have the stomach for it. Fifteen animals. That's more than most people manage in a lifetime."))
        print("\n")
        type.slow("He slides a business card across the counter.")
        print("\n")
        type.slow(yellow("'CUBE PROCESSING INC. - Industrial Facility #7'"))
        print("\n")
        type.slow(yellow("'WHERE ANIMALS BECOME PRODUCT'"))
        print("\n")
        
        time.sleep(3)
        
        type.slow("You take the card. You don't know why. Your fingers move on their own.")
        print("\n")
        type.slow(quote("The van comes tonight. They'll pick up the last batch. Then... well. The door's open if you want it."))
        print("\n")
        
        
        type.slow("You drive to the casino. You don't know what else to do.")
        print("\n")
        type.slow("The Dealer looks up as you sit down. His jade eye catches the light.")
        print("\n")
        type.slow(red(self._lists.get_dealer_betrayal_dialogue()))
        print("\n")
        type.slow("You look at your hands.")
        print("\n")
        type.slow(red(self._lists.get_dealer_betrayal_dialogue()))
        print("\n")
        type.slow("He doesn't touch the cards. He just watches you.")
        print("\n")
        type.slow(red(self._lists.get_dealer_betrayal_dialogue()))
        print("\n")
        
        time.sleep(2)
        
        type.slow("You open your mouth to explain. To justify. To—")
        print("\n")
        type.slow(red(self._lists.get_dealer_betrayal_dialogue()))
        print("\n")
        type.slow("The business card burns in your pocket.")
        print("\n")
        type.slow(red(self._lists.get_dealer_betrayal_dialogue()))
        print("\n")
        
        time.sleep(3)
        
        type.slow("You want to leave. But your legs won't move.")
        print("\n")
        type.slow("The Dealer finally picks up the cards. Shuffles. Slow. Deliberate.")
        print("\n")
        type.slow(red(self._lists.get_dealer_betrayal_dialogue()))
        print("\n")
        type.slow(red(self._lists.get_dealer_betrayal_dialogue()))
        print("\n")
        
        time.sleep(2)
        
        type.slow("Days blur together. Weeks. Months.")
        print("\n")
        type.slow("You never call the number on the card. But you never throw it away either.")
        print("\n")
        type.slow("Sometimes, late at night, you hear machinery. Grinding. Processing. Cubing.")
        print("\n")
        type.slow("It's not real. You know it's not real.")
        print("\n")
        type.slow("But you hear it anyway.")
        print("\n")
        
        time.sleep(3)
        
        type.slow("The scratching at your car door has stopped.")
        print("\n")
        type.slow("They're not coming back.")
        print("\n")
        type.slow("They've been processed.")
        print("\n")
        
        time.sleep(2)
        
        type.slow(red(bright("You fed fifteen living creatures into an industrial meat grinder.")))
        print("\n")
        type.slow(red(bright("For money. For cards. For nothing.")))
        print("\n")
        type.slow(red(bright("The factory is always hungry.")))
        print("\n")
        type.slow(red(bright("And you know where to find more.")))
        print("\n")
        
        # Unlock final achievement
        self.unlock_achievement("cube_master")
        self.display_final_achievements()
        
        type.slow(bright(yellow("~ ~ ~ THE END ~ ~ ~")))
        print("\n")
        type.slow("Thank you for playing.")
        quit()

    # ============================================
    # TANYA'S THERAPY OFFICE
    # ============================================

    def visit_tanya(self):
        """Visit Tanya the therapist. Sarcastic dialogue that evolves with visits."""
        visits = self.get_visited_tanya()
        self.increment_visited_tanya()
        visits += 1  # current visit number
        
        cost = 50 if visits <= 3 else 75 if visits <= 6 else 100
        
        if self.get_balance() < cost:
            type.type("You drive to Tanya's office, but when you check your wallet, you realize you can't afford the session.")
            print("\n")
            type.type("You sit in the parking lot for a while, then drive back.")
            print("\n")
            return
        
        type.type("You park outside the strip mall and walk into Tanya's office.")
        print("\n")
        
        if visits == 1:
            # FIRST REAL VISIT
            type.type("The white noise machine is still humming. Tanya is at her desk, eating a granola bar.")
            print("\n")
            type.slow(cyan("\"Oh, you actually came back. I owe myself five bucks. Sit down.\""))
            print("\n")
            type.type("You sit. She finishes her granola bar, brushes crumbs off her blouse, and pulls out a notepad.")
            print("\n")
            type.slow(cyan("\"Alright. Last time you gave me the highlights. This time, give me the lowlights. Start from the beginning. Why are you living in a car and gambling every night?\""))
            print("\n")
            type.type("You tell her about Grandma's fifty dollars. About the dealer with the jade eye. About the nights that blur together.")
            print("\n")
            type.slow(cyan("\"So your grandmother dies, leaves you fifty bucks, and instead of buying groceries you drove to a casino run by a one-eyed cowboy. That's... honestly impressive in its stupidity.\""))
            print("\n")
            type.type("She writes something down.")
            print("\n")
            type.slow(cyan("\"I'm writing 'impulse control issues.' Don't take it personally. That's on literally everyone's file here.\""))
            print("\n")
            type.slow(cyan("\"Here's your homework: next time you sit at that table, I want you to notice how your body feels right before you bet. Not what you're thinking - what you're FEELING. In your chest. Your hands. Your gut.\""))
            print("\n")
            type.slow(cyan("\"That'll be $" + str(cost) + ". I accept cash, checks, and silent weeping.\""))
            print("\n")
        elif visits == 2:
            type.slow(cyan("\"Welcome back. How'd the homework go?\""))
            print("\n")
            type.type(quote("I... forgot to do it."))
            print("\n")
            type.slow(cyan("\"Shocking. Absolutely no one could have predicted that.\""))
            print("\n")
            type.type("She takes a sip of coffee.")
            print("\n")
            type.slow(cyan("\"Let me ask you something. Before all this - before the car, the casino, the whole mess - what was your life like? Did you have people?\""))
            print("\n")
            type.type("You start to talk. About Rebecca, about Nathan.")
            print("\n")
            type.slow(cyan("\"There it is. You left a wife and a kid. And you're playing cards in a shack on a hill.\"\n"))
            type.type("She doesn't say it mean. She says it like she's reading a weather report. Just facts.")
            print("\n")
            type.slow(cyan("\"You know what an addiction is, right? It's not the thing you're addicted to. It's the thing you're running FROM. The cards aren't the problem. The cards are the solution you found for a problem you're too scared to look at.\""))
            print("\n")
            type.slow(cyan("\"We'll get there. $" + str(cost) + ". Same deal as last time.\""))
            print("\n")
        elif visits == 3:
            type.slow(cyan("\"Hey. You look different today. Not good-different, but... awake-different.\""))
            print("\n")
            type.type("You tell her about your week. The events. The casino. The people you've met on the road.")
            print("\n")
            type.slow(cyan("\"You know what I notice? When you talk about the casino, your voice gets flat. Like you're reading from a script. But when you talk about Tom - the mechanic? You light up.\""))
            print("\n")
            type.type(quote("Tom's a good guy."))
            print("\n")
            type.slow(cyan("\"Tom IS a good guy. And you know what good guys do? They stick around. They don't run. Think about that.\""))
            print("\n")
            type.slow(cyan("\"We're making progress. And by 'we' I mean you. I'm just drinking coffee and asking questions. $" + str(cost) + ".\""))
            print("\n")
        elif visits == 4:
            type.slow(cyan("\"Four visits. You know most of my gambling clients don't make it past two? You're either brave or stubborn. Probably stubborn.\""))
            print("\n")
            type.type("You laugh. Actually laugh. When was the last time that happened?")
            print("\n")
            type.slow(cyan("\"I want to talk about something uncomfortable. I want to talk about what you're afraid of.\""))
            print("\n")
            type.type(quote("I'm not afraid of anything."))
            print("\n")
            type.slow(cyan("\"Bull. Shit. You're afraid of going home. You're afraid that if you show up at your wife's door with a suitcase full of casino money, she'll look at you and see exactly what you see in the mirror every morning.\""))
            print("\n")
            type.type("The room gets very quiet.")
            print("\n")
            type.slow(cyan("\"That's the thing about therapy. We don't fix you. We just hold up a mirror and make you look at it until you stop flinching. $" + str(cost) + ".\""))
            print("\n")
        elif visits == 5:
            type.slow(cyan("\"Five. I should get you a loyalty card. Tenth session free. I'm kidding. Nothing is free. Especially emotional labor.\""))
            print("\n")
            type.type("She's different today. Softer, maybe. Or maybe you're just better at seeing it.")
            print("\n")
            type.slow(cyan("\"I need to tell you something, and you're not going to like it. Ready?\""))
            print("\n")
            type.type("You nod.")
            print("\n")
            type.slow(cyan("\"You're getting better. And that terrifies you. Because if you get better, you don't have an excuse to stay out here anymore. You'll have to face the music - go home, face your wife, be a father. And the part of you that's been hiding in this car for months would rather keep gambling than deal with any of that.\""))
            print("\n")
            type.type("You don't say anything for a long time.")
            print("\n")
            type.type(quote("...yeah."))
            print("\n")
            type.slow(cyan("\"That 'yeah' is worth more than every dollar you've put on a blackjack table. $" + str(cost) + ". And do the homework this time.\""))
            print("\n")
        elif visits >= 6:
            # Recurring visits after the initial arc
            late_dialogues = [
                "\"You're back. Good. Consistency is the unsexy secret to not being a disaster. Let's talk about triggers.\"",
                "\"How are the nights? Still feel the pull?\" She already knows the answer. She asks anyway.",
                "\"Progress isn't linear. Some days you'll feel great. Some days you'll want to bet your whole bankroll on a single hand. Both are normal. Neither defines you.\"",
                "\"You know what I like about you? You keep showing up. Most people don't. Most people quit when it gets hard. You're still here.\"",
                "\"I've been thinking about your case. And I realize something: you're not addicted to winning. You're addicted to the POSSIBILITY of winning. There's a difference. A big one.\"",
                "\"Let me ask you this: if you could snap your fingers and be home right now, with your wife and kid, no gambling debt, no baggage - would you do it?\" You hesitate. She notices. \"We'll work on the hesitation.\"",
            ]
            dialogue = random.choice(late_dialogues)
            type.slow(cyan(dialogue))
            print("\n")
            type.type("The session goes on. It's becoming routine. And that's the point - routine is the opposite of chaos.")
            print("\n")
            type.slow(cyan("\"$" + str(cost) + ". Same time next week. Or whenever your car brings you back. I'll be here.\""))
            print("\n")
        
        self.change_balance(-cost)
        
        # Sanity restoration scales with visits
        sanity_gain = min(5 + visits * 2, 20)
        self.restore_sanity(sanity_gain)
        
        # After 3+ visits, there's a chance you'll skip gambling tonight
        if visits >= 3 and random.randrange(3) == 0:
            self.set_tanya_skip_night(True)
            print()
            type.slow(cyan("\"Hey. One more thing. Tonight, instead of driving to the casino... just don't. Stay in your car. Read something. Stare at the ceiling. Anything but cards.\""))
            print("\n")
            type.type("You nod. And for once, you mean it.")
            print("\n")
        
        # After 5+ visits, higher chance of skipping
        elif visits >= 5 and random.randrange(2) == 0:
            self.set_tanya_skip_night(True)
            print()
            type.slow(cyan("\"No casino tonight. Doctor's orders. And before you say I'm not that kind of doctor - I know. Just humor me.\""))
            print("\n")

        # After 7+ visits with very low sanity, trigger the exhaust ending check
        if visits >= 7 and self.get_sanity() <= 20:
            type.type("As you walk to your car, Tanya calls after you.")
            print("\n")
            type.slow(cyan("\"Hey. I mean it. Don't do anything stupid tonight. Promise me.\""))
            print("\n")
            type.type("Her voice is different. No sarcasm. No jokes. Just concern.")
            print("\n")
            type.type("You don't promise. She notices.")
            print("\n")
            self.add_danger("Tanya Exhaust Warning")
