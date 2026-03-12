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

class IllnessMixin:
    """Illness events: All illnesses, injuries, and medical conditions"""

    # ==========================================
    # DISPATCHER — called by the event system
    # ==========================================

    def random_illness(self):
        """Pick a rank-appropriate illness at random and trigger it."""
        rank = self.get_rank()

        minor = [
            self.contract_cold, self.contract_flu, self.contract_strep_throat,
            self.contract_ear_infection, self.contract_sinus_infection,
            self.contract_pink_eye, self.contract_ringworm, self.contract_scabies,
            self.contract_uti, self.migraine_severe, self.vertigo_episode,
            self.asthma_attack, self.dirty_needle_stick, self.unclean_water,
            self.mold_exposure, self.bee_sting_allergy, self.bad_oysters,
            self.rat_bite, self.bad_mushrooms, self.slip_in_shower,
            self.fall_down_stairs, self.kitchen_accident, self.bar_fight_aftermath,
            self.severe_anxiety_attack, self.severe_depression_episode,
            self.insomnia_chronic, self.stress_breakdown, self.trauma_flashback,
            self.dislocated_shoulder, self.broken_wrist, self.broken_nose,
            self.deep_laceration, self.whiplash_injury, self.broken_hand,
        ]
        moderate = [
            self.contract_pneumonia, self.contract_bronchitis, self.contract_stomach_flu,
            self.contract_mono, self.contract_shingles, self.contract_lyme_disease,
            self.contract_tetanus, self.contract_rabies_scare, self.contract_staph_infection,
            self.develop_diabetes_symptoms, self.high_blood_pressure_crisis,
            self.severe_allergic_reaction, self.kidney_stones, self.gallbladder_attack,
            self.appendicitis_attack, self.blood_clot_in_leg, self.seizure_episode,
            self.pancreatitis_attack, self.severe_burn_injury, self.concussion_injury,
            self.broken_ribs_injury, self.broken_ankle, self.torn_acl,
            self.herniated_disc, self.puncture_wound, self.frostbite,
            self.heat_stroke, self.hypothermia, self.second_degree_burns,
            self.electrical_burn, self.chemical_burn, self.crush_injury,
            self.gym_accident, self.lead_poisoning, self.asbestos_exposure,
            self.mercury_poisoning, self.dental_disaster, self.dog_attack_severe,
            self.ptsd_flashback, self.food_truck_nightmare, self.public_pool_infection,
            self.homeless_shelter_outbreak, self.bad_tattoo_infection, self.wasp_nest_encounter,
        ]
        severe = [
            self.contract_measles, self.skull_fracture, self.collapsed_lung,
            self.ruptured_spleen, self.liver_laceration, self.detached_retina,
            self.gangrene_infection, self.drug_overdose_survival, self.botched_surgery,
            self.covid_complications, self.earthquake_injury, self.explosion_nearby,
            self.coma_awakening, self.prison_shiv_wound, self.sleep_deprivation_crisis,
            self.caught_in_fire, self.frozen_outdoors, self.heat_exhaustion_collapse,
            self.mma_fight_aftermath, self.motorcycle_crash, self.pool_diving_accident,
            self.electric_shock, self.assault_aftermath, self.workplace_injury,
        ]

        # Severity weights per rank: [minor, moderate, severe]
        # Rank 0=poor, 1=cheap, 2=modest, 3=rich, 4=doughman, 5=nearly
        severity_weights = [
            [8, 2, 0],  # poor: mostly minor ailments
            [6, 3, 1],  # cheap: starting to see real problems
            [4, 4, 2],  # modest: balanced danger
            [2, 4, 4],  # rich: serious injuries more common
            [1, 3, 6],  # doughman: life-threatening events dominate
            [1, 2, 7],  # nearly: severe and life-threatening
        ]
        weights = severity_weights[min(rank, 5)]
        severity = random.choices(["minor", "moderate", "severe"], weights=weights, k=1)[0]
        if severity == "minor":
            random.choice(minor)()
        elif severity == "moderate":
            random.choice(moderate)()
        else:
            random.choice(severe)()

    # ==========================================
    # BASIC COMMON ILLNESSES (also in minor pool)
    # ==========================================

    def contract_cold(self):
        type.type("It started with a tickle in your throat. Then the sniffles. Then the coughing.")
        print("\n")
        type.type("Your nose is running like a faucet. Your head feels stuffed with cotton.")
        print("\n")
        type.type("Just a common " + red("cold") + ". Nothing serious, but you feel miserable.")
        self.add_status("Cold")
        self.hurt(5)
        self.start_night()

    def contract_flu(self):
        type.type("It hits you like a truck. One moment you're fine, the next you can barely move.")
        print("\n")
        type.type("Fever. Chills. Body aches so severe you can't get comfortable in any position.")
        print("\n")
        type.type("Your throat is raw. Your cough is painful. This is the " + red("flu") + " - the real deal.")
        self.add_status("Flu")
        self.hurt(12)
        self.lose_sanity(1)
        self.start_night()

    def contract_pneumonia(self):
        # EVENT: Contract pneumonia from exposure/weakened immune system
        # EFFECTS: Adds "Pneumonia" status, 15 damage, 2 sanity loss
        # NOTE: Requires doctor visit to treat
        type.type("You wake up coughing. Deep, rattling coughs that feel like they're coming from the bottom of your lungs.")
        print("\n")
        type.type("Your chest hurts. Every breath is a struggle. You're burning up with fever but shivering uncontrollably.")
        print("\n")
        type.type("This isn't just a cold. This is " + red("pneumonia") + ".")
        print("\n")
        type.type("You need a doctor. Soon.")
        self.add_status("Pneumonia")
        self.hurt(15)
        self.lose_sanity(2)
        self.start_night()

    def contract_bronchitis(self):
        # EVENT: Contract bronchitis - persistent coughing with mucus
        # EFFECTS: Adds "Bronchitis" status, 8 damage
        type.type("The coughing started a few days ago. Now it won't stop.")
        print("\n")
        type.type("Every cough produces thick, yellow mucus. Your throat is raw. Your chest aches.")
        print("\n")
        type.type("You can barely speak without triggering another coughing fit.")
        print("\n")
        type.type(red("Bronchitis") + " has set in.")
        self.add_status("Bronchitis")
        self.hurt(8)
        self.start_night()

    def contract_strep_throat(self):
        # EVENT: Contract strep throat - severe throat infection
        # EFFECTS: Adds "Strep Throat" status, 10 damage; needs antibiotics
        type.type("Your throat feels like it's being scraped with broken glass.")
        print("\n")
        type.type("Swallowing is agony. Your tonsils are swollen and covered in white patches.")
        print("\n")
        type.type("Fever. Headache. Body aches. This is " + red("strep throat") + ".")
        print("\n")
        type.type("Without antibiotics, this could get much, much worse.")
        self.add_status("Strep Throat")
        self.hurt(10)
        self.start_night()

    def contract_stomach_flu(self):
        # EVENT: Contract stomach flu - violent gastrointestinal distress
        # EFFECTS: Adds "Stomach Flu" status, 12 damage, 1 sanity loss
        type.type("It started with nausea. Then came the vomiting. Then the other end started.")
        print("\n")
        type.type("You've spent the last several hours in the bathroom, alternating between the toilet and the cold floor.")
        print("\n")
        type.type("Your body is expelling everything. You're getting dehydrated fast.")
        print("\n")
        type.type(red("Stomach flu") + " has you in its grip.")
        self.add_status("Stomach Flu")
        self.hurt(12)
        self.lose_sanity(1)
        self.start_night()

    def contract_ear_infection(self):
        # EVENT: Contract ear infection - painful infection with hearing loss
        # EFFECTS: Adds "Ear Infection" status, 5 damage
        type.type("The pain in your ear is unbearable. A deep, throbbing ache that radiates through your skull.")
        print("\n")
        type.type("You can barely hear out of that side. Everything sounds muffled, underwater.")
        print("\n")
        type.type("Yellow fluid is starting to leak out.")
        print("\n")
        type.type(red("Ear infection") + ". Nasty one.")
        self.add_status("Ear Infection")
        self.hurt(5)
        self.start_night()

    def contract_sinus_infection(self):
        # EVENT: Contract sinus infection - severe facial pressure and mucus
        # EFFECTS: Adds "Sinus Infection" status, 6 damage
        type.type("Your face feels like it's going to explode. The pressure behind your eyes, your cheeks, your forehead - it's immense.")
        print("\n")
        type.type("Thick green mucus drains down your throat constantly. Your head pounds with every heartbeat.")
        print("\n")
        type.type("The " + red("sinus infection") + " has fully taken hold.")
        self.add_status("Sinus Infection")
        self.hurt(6)
        self.start_night()

    def contract_uti(self):
        # EVENT: Contract urinary tract infection - painful and potentially serious
        # EFFECTS: Adds "UTI" status, 8 damage; can spread to kidneys if untreated
        type.type("It started as a slight burning sensation. Now every trip to the bathroom is torture.")
        print("\n")
        type.type("You have to go constantly, but barely anything comes out. What does is cloudy and smells wrong.")
        print("\n")
        type.type("Your lower back aches. You might have a fever.")
        print("\n")
        type.type(red("Urinary tract infection") + ". If it spreads to your kidneys...")
        self.add_status("UTI")
        self.hurt(8)
        self.start_night()

    def contract_pink_eye(self):
        # EVENT: Contract conjunctivitis (pink eye) - contagious eye infection
        # EFFECTS: Adds "Pink Eye" status, 3 damage
        type.type("You wake up and can't open your left eye. It's crusted shut with dried discharge.")
        print("\n")
        type.type("Once you manage to pry it open, you see the white of your eye is bright pink. Bloodshot veins everywhere.")
        print("\n")
        type.type("It itches like crazy. Tears stream down constantly.")
        print("\n")
        type.type(red("Conjunctivitis") + ". Pink eye. Extremely contagious.")
        self.add_status("Pink Eye")
        self.hurt(3)
        self.start_night()

    def contract_mono(self):
        # EVENT: Contract mononucleosis - extreme fatigue for months
        # EFFECTS: Adds "Mononucleosis" status, 20 damage, 3 sanity loss
        type.type("The exhaustion is unlike anything you've ever felt. You slept fourteen hours and woke up more tired than when you went to bed.")
        print("\n")
        type.type("Your throat is sore. Your lymph nodes are swollen. Your spleen aches.")
        print("\n")
        type.type("The doctor would tell you it's " + red("mononucleosis") + ". The kissing disease.")
        print("\n")
        type.type("It could take months to fully recover.")
        self.add_status("Mononucleosis")
        self.hurt(20)
        self.lose_sanity(3)
        self.start_night()

    def contract_shingles(self):
        # EVENT: Shingles outbreak from dormant chickenpox virus
        # EFFECTS: Adds "Shingles" status, 18 damage, 2 sanity loss; can cause permanent nerve damage
        type.type("The rash appeared yesterday. Today, it's on fire.")
        print("\n")
        type.type("Blisters have formed in a band across your torso, following the path of a nerve. The pain is excruciating.")
        print("\n")
        type.type("Burning. Stabbing. Constant. You had chickenpox as a kid - the virus never left.")
        print("\n")
        type.type(red("Shingles") + ". And without treatment, the nerve damage could be permanent.")
        self.add_status("Shingles")
        self.hurt(18)
        self.lose_sanity(2)
        self.start_night()

    def contract_lyme_disease(self):
        # EVENT: Contract Lyme disease from tick bite
        # EFFECTS: Adds "Lyme Disease" status, 15 damage, 2 sanity loss; devastating if untreated
        type.type("You notice the rash first. A perfect bullseye - red ring, clear center, red outer ring.")
        print("\n")
        type.type("Then come the joint pains. The fatigue. The brain fog that makes it hard to think.")
        print("\n")
        type.type("You must have been bitten by a tick at some point. Didn't even notice.")
        print("\n")
        type.type(red("Lyme disease") + ". Caught early, treatable. Left untreated... devastating.")
        self.add_status("Lyme Disease")
        self.hurt(15)
        self.lose_sanity(2)
        self.start_night()

    def contract_ringworm(self):
        # EVENT: Contract ringworm fungal infection
        # EFFECTS: Adds "Ringworm" status, 3 damage; contagious and spreading
        type.type("The itchy patch on your arm has grown. What started as a small red spot is now a perfect red ring.")
        print("\n")
        type.type("It's not actually a worm - it's a fungal infection. But that doesn't make it less disgusting.")
        print("\n")
        type.type(red("Ringworm") + ". Contagious. Spreading. Needs treatment.")
        self.add_status("Ringworm")
        self.hurt(3)
        self.start_night()

    def contract_scabies(self):
        # EVENT: Contract scabies - mites burrowing under skin
        # EFFECTS: Adds "Scabies" status, 5 damage, 2 sanity loss; maddening itch
        type.type("The itching is maddening. Especially at night. Tiny burrows appearing between your fingers, on your wrists, in your armpits.")
        print("\n")
        type.type("Microscopic mites have burrowed into your skin. They're laying eggs under your flesh.")
        print("\n")
        type.type("You scratch until you bleed, but the relief is only momentary.")
        print("\n")
        type.type(red("Scabies") + ". Your skin is infested.")
        self.add_status("Scabies")
        self.hurt(5)
        self.lose_sanity(2)
        self.start_night()

    def contract_staph_infection(self):
        # EVENT: Contract staph infection from wound - potentially fatal
        # EFFECTS: Adds "Staph Infection" status, 20 damage, 1 sanity loss; can kill if reaches bloodstream
        type.type("What started as a small cut has become something much worse.")
        print("\n")
        type.type("The wound is hot, swollen, and filled with pus. Red streaks are spreading outward from the site.")
        print("\n")
        type.type("The area around it is hard to the touch. You're developing a fever.")
        print("\n")
        type.type(red("Staph infection") + ". If it gets into your bloodstream, it could kill you.")
        self.add_status("Staph Infection")
        self.hurt(20)
        self.lose_sanity(1)
        self.start_night()

    def contract_tetanus(self):
        # EVENT: Contract tetanus (lockjaw) from rusty wound - life threatening
        # EFFECTS: Adds "Tetanus" status, 25 damage, 3 sanity loss; needs antitoxin or death
        type.type("You stepped on that rusty nail a few days ago. You thought it was fine.")
        print("\n")
        type.type("Now your jaw is stiffening. Your muscles are cramping. You're having trouble swallowing.")
        print("\n")
        type.type("Your back arches involuntarily. Spasms rack your body.")
        print("\n")
        type.type(red("Tetanus") + ". Lockjaw. Without antitoxin, the spasms will get worse until you can't breathe.")
        self.add_status("Tetanus")
        self.hurt(25)
        self.lose_sanity(3)
        self.start_night()

    def contract_rabies_scare(self):
        # EVENT: Possible rabies infection from animal bite - almost always fatal once symptoms appear
        # EFFECTS: Adds "Possible Rabies" status, 10 damage, 5 sanity loss; time-critical treatment needed
        type.type("That animal that bit you last week - you never did find out if it was rabid.")
        print("\n")
        type.type("Now you're having headaches. Fever. You feel anxious, confused.")
        print("\n")
        type.type("Is it just paranoia? Or is the virus already in your brain?")
        print("\n")
        type.type("Once symptoms appear, " + red("rabies") + " is almost always fatal. But maybe there's still time...")
        self.add_status("Possible Rabies")
        self.hurt(10)
        self.lose_sanity(5)
        self.start_night()

    def contract_measles(self):
        # EVENT: Contract measles - serious viral infection with rash and fever
        # EFFECTS: Adds "Measles" status, 18 damage, 2 sanity loss
        type.type("The rash covers your entire body now. Red, blotchy, spreading across your face and trunk.")
        print("\n")
        type.type("Your eyes are red and watering. Light is painful. You've had a high fever for days.")
        print("\n")
        type.type("Small white spots have appeared inside your mouth.")
        print("\n")
        type.type(red("Measles") + ". You thought it was eradicated. You were wrong.")
        self.add_status("Measles")
        self.hurt(18)
        self.lose_sanity(2)
        self.start_night()

    # CHRONIC CONDITIONS
    def develop_diabetes_symptoms(self):
        # EVENT: Develop uncontrolled diabetes symptoms
        # EFFECTS: Adds "Uncontrolled Diabetes" status, 15 damage; needs medication
        type.type("You've been drinking water constantly. Gallons a day. And yet your mouth is always dry.")
        print("\n")
        type.type("You're losing weight despite eating more than ever. You're exhausted. Your vision is blurry.")
        print("\n")
        type.type("You've been urinating constantly. The symptoms point to one thing.")
        print("\n")
        type.type(red("Diabetes") + ". Your blood sugar is out of control. You need medication.")
        self.add_status("Uncontrolled Diabetes")
        self.hurt(15)
        self.start_night()

    def high_blood_pressure_crisis(self):
        # EVENT: Hypertensive crisis - dangerously high blood pressure
        # EFFECTS: Adds "Blood Pressure Crisis" status, 20 damage, 2 sanity loss; stroke risk
        type.type("The headache hits like a hammer. Your vision swims. You feel your pulse pounding in your temples.")
        print("\n")
        type.type("Your face is flushed. Nosebleed starts. You're dizzy, disoriented.")
        print("\n")
        type.type("This is a " + red("hypertensive crisis") + ". Your blood pressure is dangerously high.")
        print("\n")
        type.type("Without intervention, you could stroke out any minute.")
        self.add_status("Blood Pressure Crisis")
        self.hurt(20)
        self.lose_sanity(2)
        self.start_night()

    def severe_allergic_reaction(self):
        # EVENT: Anaphylactic shock - life-threatening allergic reaction
        # EFFECTS: Adds "Anaphylaxis" status, 30 damage, 3 sanity loss; needs epinephrine immediately
        type.type("It happens fast. One moment you're fine. The next, your throat is closing.")
        print("\n")
        type.type("Hives break out across your body. Your face swells. Your lips balloon.")
        print("\n")
        type.type("You can barely breathe. The wheezing gets louder.")
        print("\n")
        type.type(red("Anaphylaxis") + ". You need epinephrine. NOW.")
        self.add_status("Anaphylaxis")
        self.hurt(30)
        self.lose_sanity(3)
        self.start_night()

    def asthma_attack(self):
        # EVENT: Severe asthma attack - can't breathe
        # EFFECTS: Adds asthma status, needs nebulizer treatment; life-threatening
        type.type("You can't breathe. You can't breathe. YOU CAN'T BREATHE.")
        print("\n")
        type.type("Your airways have constricted. Every breath is a whistle, a wheeze, barely any air getting through.")
        print("\n")
        type.type("Your lips are turning blue. You're panicking, which makes it worse.")
        print("\n")
        type.type(red("Asthma attack") + ". Severe one. You need a nebulizer treatment.")
        self.add_status("Severe Asthma")
        self.hurt(20)
        self.lose_sanity(3)
        self.start_night()

    def kidney_stones(self):
        type.type("The pain is unlike anything you've ever experienced.")
        print("\n")
        type.type("It started in your back and radiated around to your front, down toward your groin. Waves of agony.")
        print("\n")
        type.type("You're vomiting from the pain. There's blood in your urine.")
        print("\n")
        type.type(red("Kidney stone") + ". Trying to pass through a tube not meant for jagged rocks.")
        self.add_status("Kidney Stones")
        self.hurt(25)
        self.lose_sanity(4)
        self.start_night()

    def gallbladder_attack(self):
        type.type("After that greasy meal, the pain starts. Upper right abdomen, radiating to your back and shoulder blade.")
        print("\n")
        type.type("It's constant, not crampy. You're nauseous, sweating. The pain lasts for hours.")
        print("\n")
        type.type("Your gallbladder is full of stones. And one is blocking the duct.")
        print("\n")
        type.type(red("Gallbladder attack") + ". You might need surgery.")
        self.add_status("Gallbladder Attack")
        self.hurt(20)
        self.lose_sanity(2)
        self.start_night()

    def appendicitis_attack(self):
        type.type("It started around your belly button. Dull ache. Now it's moved to your lower right side.")
        print("\n")
        type.type("The pain is sharp, constant, getting worse by the hour. You can't stand up straight.")
        print("\n")
        type.type("Pressing on your abdomen makes it worse. Releasing quickly - even worse.")
        print("\n")
        type.type(red("Appendicitis") + ". If it ruptures, you'll die of sepsis.")
        self.add_status("Appendicitis")
        self.hurt(30)
        self.lose_sanity(3)
        self.start_night()

    def blood_clot_in_leg(self):
        type.type("Your calf is swollen, red, and warm to the touch. It aches deeply.")
        print("\n")
        type.type("You've been sitting too much. Not moving enough. The blood pooled and clotted.")
        print("\n")
        type.type(red("Deep vein thrombosis") + ". A blood clot in your leg.")
        print("\n")
        type.type("If it breaks loose and travels to your lungs, it's called a pulmonary embolism. And it can kill you in seconds.")
        self.add_status("DVT")
        self.hurt(15)
        self.lose_sanity(3)
        self.start_night()

    def migraine_severe(self):
        type.type("The aura started an hour ago. Zigzag lines dancing across your vision.")
        print("\n")
        type.type("Now the pain has arrived. A sledgehammer behind your left eye. Light is agony. Sound is torture.")
        print("\n")
        type.type("You're nauseous. Vomiting. Lying in darkness, praying for it to end.")
        print("\n")
        type.type(red("Migraine") + ". Severe. You're completely incapacitated.")
        self.add_status("Severe Migraine")
        self.hurt(10)
        self.lose_sanity(4)
        self.start_night()

    def vertigo_episode(self):
        type.type("The room is spinning. No - YOU'RE spinning. Everything is tilted, rotating, impossible to focus on.")
        print("\n")
        type.type("You can't stand. You can't walk. Moving your head makes it exponentially worse.")
        print("\n")
        type.type("You vomit from the dizziness. This isn't just being lightheaded.")
        print("\n")
        type.type(red("Vertigo") + ". Something is wrong with your inner ear.")
        self.add_status("Vertigo")
        self.hurt(5)
        self.lose_sanity(3)
        self.start_night()

    def seizure_episode(self):
        type.type("You feel it coming. The strange taste in your mouth. The déjà vu. The rising sense of dread.")
        print("\n")
        type.type("Then everything goes blank.")
        print("\n")
        type.type("...")
        print("\n")
        type.type("You wake up on the ground. Your tongue is bloody where you bit it. Your pants are wet.")
        print("\n")
        type.type("People are staring. Paramedics are being called.")
        print("\n")
        type.type(red("Seizure") + ". Grand mal. You don't know when the next one will come.")
        self.add_status("Seizure Disorder")
        self.hurt(20)
        self.lose_sanity(5)
        self.start_night()

    def pancreatitis_attack(self):
        type.type("The pain is centered in your upper abdomen and radiates straight through to your back.")
        print("\n")
        type.type("It's constant, severe, made worse by eating. You're vomiting, running a fever.")
        print("\n")
        type.type("You've been drinking too much. Or maybe it's gallstones. Either way...")
        print("\n")
        type.type(red("Pancreatitis") + ". Your pancreas is inflamed. It's eating itself.")
        self.add_status("Pancreatitis")
        self.hurt(25)
        self.lose_sanity(3)
        self.start_night()

    # INJURIES AND TRAUMA
    def severe_burn_injury(self):
        type.type("The burn covers a large portion of your arm. The skin is blistered, weeping, raw.")
        print("\n")
        type.type("Some areas are white and waxy - third degree. You can't feel those parts. That's not a good sign.")
        print("\n")
        type.type("The pain in the surrounding areas is excruciating.")
        print("\n")
        type.type(red("Severe burns") + ". Risk of infection. Possible need for skin grafts.")
        self.add_injury("Severe Burns")
        self.hurt(25)
        self.lose_sanity(3)
        self.start_night()

    def concussion_injury(self):
        type.type("Your head hit hard. Too hard.")
        print("\n")
        type.type("Now everything is fuzzy. Light hurts. Sound hurts. You can't remember what happened before the impact.")
        print("\n")
        type.type("Nausea. Dizziness. You're not supposed to fall asleep, but you're so tired...")
        print("\n")
        type.type(red("Concussion") + ". Your brain bounced around inside your skull.")
        self.add_injury("Concussion")
        self.hurt(15)
        self.lose_sanity(4)
        self.start_night()

    def broken_ribs_injury(self):
        type.type("Every breath is agony. You can feel the bones grinding against each other in your chest.")
        print("\n")
        type.type("Three ribs, at least. Maybe more. You can't take a deep breath without crying out.")
        print("\n")
        type.type("Laughing, coughing, sneezing - all torture. Sleeping is nearly impossible.")
        print("\n")
        type.type(red("Broken ribs") + ". Nothing to do but wait for them to heal. And pray they don't puncture a lung.")
        self.add_injury("Broken Ribs")
        self.hurt(20)
        self.lose_sanity(2)
        self.start_night()

    def dislocated_shoulder(self):
        type.type("Your arm is hanging at a wrong angle. The shoulder joint has popped out of its socket.")
        print("\n")
        type.type("The pain is overwhelming. You can't move the arm at all. Every jostle is excruciating.")
        print("\n")
        type.type("Someone needs to put it back in. The longer you wait, the worse the muscle damage.")
        print("\n")
        type.type(red("Dislocated shoulder") + ". Needs reduction immediately.")
        self.add_injury("Dislocated Shoulder")
        self.hurt(18)
        self.lose_sanity(2)
        self.start_night()

    def broken_hand(self):
        type.type("Your hand is swelling up like a balloon. The fingers are bent at unnatural angles.")
        print("\n")
        type.type("Multiple metacarpal fractures. You can see the bones misaligned under the skin.")
        print("\n")
        type.type("Picking up anything is impossible. Making a fist is impossible. Doing anything is impossible.")
        print("\n")
        type.type(red("Broken hand") + ". Going to need surgery to pin those bones.")
        self.add_injury("Broken Hand")
        self.hurt(15)
        self.lose_sanity(2)
        self.start_night()

    def broken_wrist(self):
        type.type("You landed wrong. All your weight came down on your outstretched hand.")
        print("\n")
        type.type("Your wrist is already purple and misshapen. You can feel the bones grinding.")
        print("\n")
        type.type("Moving it sends bolts of white-hot pain up your arm.")
        print("\n")
        type.type(red("Broken wrist") + ". Colles fracture. Classic. Painful.")
        self.add_injury("Broken Wrist")
        self.hurt(12)
        self.lose_sanity(1)
        self.start_night()

    def broken_ankle(self):
        type.type("You heard the snap when it happened. Felt it too.")
        print("\n")
        type.type("Your ankle is already swelling, turning purple. You can't put any weight on it at all.")
        print("\n")
        type.type("Walking is out of the question. You're going to need crutches. Maybe a boot. Maybe surgery.")
        print("\n")
        type.type(red("Broken ankle") + ". You're not going anywhere fast.")
        self.add_injury("Broken Ankle")
        self.hurt(15)
        self.lose_sanity(2)
        self.start_night()

    def torn_acl(self):
        type.type("You pivoted wrong and felt the pop. Knew immediately something was very wrong.")
        print("\n")
        type.type("Your knee buckled. You went down. Now the joint is swelling rapidly.")
        print("\n")
        type.type("The knee feels unstable. Like it could give out at any moment.")
        print("\n")
        type.type(red("Torn ACL") + ". Going to need reconstruction surgery. And months of rehab.")
        self.add_injury("Torn ACL")
        self.hurt(20)
        self.lose_sanity(3)
        self.start_night()

    def herniated_disc(self):
        type.type("You lifted something heavy and felt your back give out.")
        print("\n")
        type.type("Now there's shooting pain down your leg. Numbness. Tingling. Weakness.")
        print("\n")
        type.type("The disc between your vertebrae has ruptured, pressing on your spinal nerves.")
        print("\n")
        type.type(red("Herniated disc") + ". Every movement is agony. You might need surgery.")
        self.add_injury("Herniated Disc")
        self.hurt(18)
        self.lose_sanity(3)
        self.start_night()

    def deep_laceration(self):
        type.type("The cut is deep. Really deep. You can see layers of tissue you're not supposed to see.")
        print("\n")
        type.type("Blood is pulsing out in rhythm with your heartbeat. That means an artery.")
        print("\n")
        type.type("You're applying pressure, but it keeps seeping through. You need stitches. Many of them.")
        print("\n")
        type.type(red("Deep laceration") + ". Maybe nicked an artery. Definitely needs sutures.")
        self.add_injury("Deep Laceration")
        self.hurt(22)
        self.start_night()

    def puncture_wound(self):
        type.type("The object went in clean. Small entry wound. But the damage is internal.")
        print("\n")
        type.type("Blood is pooling inside. You can feel things that shouldn't be damaged... damaged.")
        print("\n")
        type.type("The wound is barely bleeding on the outside. That's actually worse.")
        print("\n")
        type.type(red("Puncture wound") + ". Internal bleeding likely. Needs imaging. Needs surgery maybe.")
        self.add_injury("Puncture Wound")
        self.hurt(25)
        self.lose_sanity(2)
        self.start_night()

    def second_degree_burns(self):
        type.type("The blisters cover your forearm. Large, fluid-filled, ready to pop.")
        print("\n")
        type.type("The skin around them is angry red. The pain is constant, throbbing.")
        print("\n")
        type.type("Every accidental brush against anything makes you gasp.")
        print("\n")
        type.type(red("Second degree burns") + ". Going to scar. Risk of infection is high.")
        self.add_status("Second Degree Burns")
        self.hurt(15)
        self.start_night()

    def frostbite(self):
        type.type("Your fingers and toes have gone white. Then grayish-blue. Now they're turning black at the tips.")
        print("\n")
        type.type("At first they hurt. Then they went numb. Now the feeling is coming back - and it's agony.")
        print("\n")
        type.type("Blood blisters are forming. The tissue is dying.")
        print("\n")
        type.type(red("Frostbite") + ". You might lose those extremities.")
        self.add_injury("Frostbite")
        self.hurt(20)
        self.lose_sanity(3)
        self.start_night()

    def heat_stroke(self):
        type.type("You stopped sweating an hour ago. That was the first sign.")
        print("\n")
        type.type("Your skin is hot and dry. Your temperature is spiking - 104, 105, climbing.")
        print("\n")
        type.type("You're confused, disoriented. Your heart is racing. Muscles cramping.")
        print("\n")
        type.type(red("Heat stroke") + ". Your body can't cool itself. You're cooking from the inside.")
        self.add_status("Heat Stroke")
        self.hurt(25)
        self.lose_sanity(4)
        self.start_night()

    def hypothermia(self):
        type.type("You can't stop shivering. No, wait - you stopped shivering. That's worse.")
        print("\n")
        type.type("Your fingers are clumsy, numb. Your thoughts are slowing. Everything seems so... far away.")
        print("\n")
        type.type("You're so tired. Just want to lie down. Just for a minute...")
        print("\n")
        type.type(red("Hypothermia") + ". Your core temperature is dropping. You're dying of cold.")
        self.add_status("Hypothermia")
        self.hurt(25)
        self.lose_sanity(5)
        self.start_night()

    def crush_injury(self):
        type.type("The weight came down on your leg. You were trapped for hours before help came.")
        print("\n")
        type.type("Now that you're free, the real danger begins. Crush syndrome.")
        print("\n")
        type.type("Toxins from your damaged muscles are flooding your bloodstream. Your kidneys are failing.")
        print("\n")
        type.type(red("Crush injury") + ". You need dialysis. You need it now.")
        self.add_injury("Crush Injury")
        self.hurt(35)
        self.lose_sanity(5)
        self.start_night()

    def chemical_burn(self):
        type.type("The substance ate through your clothes and into your skin.")
        print("\n")
        type.type("The burning sensation won't stop. You've rinsed it but the damage is done.")
        print("\n")
        type.type("The affected area is white, then red, then blistering. Layers of skin sloughing off.")
        print("\n")
        type.type(red("Chemical burn") + ". Acid or base, it doesn't matter. The tissue is destroyed.")
        self.add_injury("Chemical Burn")
        self.hurt(22)
        self.lose_sanity(2)
        self.start_night()

    def electrical_burn(self):
        type.type("The entry wound is small. The exit wound is larger. But the real damage is inside.")
        print("\n")
        type.type("The current passed through your body, cooking tissue from within.")
        print("\n")
        type.type("Your heart rhythm was disrupted. You're still feeling palpitations. Muscles ache deeply.")
        print("\n")
        type.type(red("Electrical burn") + ". Internal damage unknown. Cardiac monitoring required.")
        self.add_injury("Electrical Burns")
        self.hurt(28)
        self.lose_sanity(3)
        self.start_night()

    def whiplash_injury(self):
        type.type("The impact threw your head forward, then back, violently.")
        print("\n")
        type.type("Now your neck is stiff, painful. You can barely turn your head.")
        print("\n")
        type.type("Headaches. Dizziness. Your shoulders ache. Symptoms might last months.")
        print("\n")
        type.type(red("Whiplash") + ". Neck sprain. Might be worse - need imaging to know.")
        self.add_injury("Whiplash")
        self.hurt(12)
        self.lose_sanity(1)
        self.start_night()

    def jaw_fracture(self):
        type.type("Your jaw won't close properly. Pain radiates through your face with every movement.")
        print("\n")
        type.type("You can feel the bones grinding against each other. The swelling is massive.")
        print("\n")
        type.type("Eating is impossible. Talking is agony.")
        print("\n")
        type.type(red("Fractured jaw") + ". Going to need wiring. Liquid diet for weeks.")
        self.add_injury("Fractured Jaw")
        self.hurt(18)
        self.lose_sanity(2)
        self.start_night()

    def skull_fracture(self):
        type.type("You can feel the depression in your skull where the bone gave way.")
        print("\n")
        type.type("Clear fluid is leaking from your nose and ear. That's cerebrospinal fluid. That's bad.")
        print("\n")
        type.type("Your pupils are different sizes. You're losing consciousness intermittently.")
        print("\n")
        type.type(red("Skull fracture") + ". Brain swelling likely. Emergency surgery required.")
        self.add_injury("Skull Fracture")
        self.hurt(40)
        self.lose_sanity(6)
        self.start_night()

    def collapsed_lung(self):
        type.type("You can only breathe with half your lungs. The other half has collapsed.")
        print("\n")
        type.type("Sharp chest pain. Shortness of breath. Your oxygen is dropping.")
        print("\n")
        type.type("The trauma to your chest forced air into the space around your lung.")
        print("\n")
        type.type(red("Pneumothorax") + ". Collapsed lung. Needs a chest tube. Now.")
        self.add_injury("Collapsed Lung")
        self.hurt(30)
        self.lose_sanity(4)
        self.start_night()

    def ruptured_spleen(self):
        type.type("The blow to your abdomen didn't seem that bad at first.")
        print("\n")
        type.type("But now your left shoulder hurts - referred pain. Your abdomen is rigid, distended.")
        print("\n")
        type.type("You're getting pale, sweaty, heart racing. Internal bleeding.")
        print("\n")
        type.type(red("Ruptured spleen") + ". You're bleeding out internally. Surgery. Immediately.")
        self.add_injury("Ruptured Spleen")
        self.hurt(35)
        self.lose_sanity(4)
        self.start_night()

    def liver_laceration(self):
        type.type("Right upper quadrant pain. Severe. Getting worse by the minute.")
        print("\n")
        type.type("You're bleeding internally. The liver is one of the most vascular organs.")
        print("\n")
        type.type("Blood pressure dropping. Consciousness fading. You need an OR. NOW.")
        print("\n")
        type.type(red("Liver laceration") + ". Every second counts.")
        self.add_injury("Liver Laceration")
        self.hurt(40)
        self.lose_sanity(5)
        self.start_night()

    def ruptured_eardrum(self):
        type.type("The explosion of pain in your ear was followed by sudden deafness.")
        print("\n")
        type.type("Blood and fluid are draining out. The ringing is constant, overwhelming.")
        print("\n")
        type.type("You're dizzy, nauseous. Your balance is off.")
        print("\n")
        type.type(red("Ruptured eardrum") + ". May heal on its own. May need surgery. Hearing loss possible.")
        self.add_injury("Ruptured Eardrum")
        self.hurt(10)
        self.lose_sanity(3)
        self.start_night()

    def detached_retina(self):
        type.type("It started with flashing lights in your vision. Then floating spots.")
        print("\n")
        type.type("Now there's a shadow creeping across your visual field. A curtain closing.")
        print("\n")
        type.type("Your retina is peeling away from the back of your eye.")
        print("\n")
        type.type(red("Retinal detachment") + ". Without surgery, permanent blindness in that eye.")
        self.add_injury("Detached Retina")
        self.hurt(8)
        self.lose_sanity(5)
        self.start_night()

    def orbital_fracture(self):
        type.type("The blow to your face was devastating.")
        print("\n")
        type.type("The bone around your eye socket has fractured. Your eye is sunken, not tracking properly.")
        print("\n")
        type.type("Double vision. Numbness in your cheek. Blood pooling in the white of your eye.")
        print("\n")
        type.type(red("Orbital fracture") + ". Your eye socket is broken. Reconstructive surgery needed.")
        self.add_injury("Orbital Fracture")
        self.hurt(20)
        self.lose_sanity(4)
        self.start_night()

    def broken_nose(self):
        type.type("The crunch was audible. Blood immediately poured from both nostrils.")
        print("\n")
        type.type("Your nose is clearly bent to one side now. Swelling is distorting your face.")
        print("\n")
        type.type("Breathing through your nose is impossible. The pain throbs with every heartbeat.")
        print("\n")
        type.type(red("Broken nose") + ". Needs to be set before it heals crooked.")
        self.add_injury("Broken Nose")
        self.hurt(8)
        self.lose_sanity(1)
        self.start_night()

    def broken_collarbone(self):
        type.type("You can see the bump where your collarbone is no longer aligned.")
        print("\n")
        type.type("Moving your arm on that side is excruciating. The bone grinds audibly.")
        print("\n")
        type.type("Your shoulder is drooping forward. Supporting the arm helps the pain.")
        print("\n")
        type.type(red("Broken clavicle") + ". Going to need a sling for weeks. Maybe surgery.")
        self.add_injury("Broken Collarbone")
        self.hurt(15)
        self.lose_sanity(2)
        self.start_night()

    def tooth_abscess(self):
        type.type("The toothache has become unbearable. Throbbing, constant, radiating through your jaw.")
        print("\n")
        type.type("Your face is swelling. You can taste the infection - pus draining into your mouth.")
        print("\n")
        type.type("Fever. Chills. The infection is spreading.")
        print("\n")
        type.type(red("Tooth abscess") + ". If it reaches your bloodstream or your brain, you're dead.")
        self.add_status("Tooth Abscess")
        self.hurt(15)
        self.lose_sanity(3)
        self.start_night()

    def blood_poisoning(self):
        type.type("That wound got infected. And now the infection is in your blood.")
        print("\n")
        type.type("Red streaks are spreading from the site. You're burning with fever, shaking with chills.")
        print("\n")
        type.type("Your heart is racing. Blood pressure dropping. Organs starting to fail.")
        print("\n")
        type.type(red("Sepsis") + ". Blood poisoning. Without IV antibiotics, you'll be dead within hours.")
        self.add_status("Sepsis")
        self.hurt(35)
        self.lose_sanity(5)
        self.start_night()

    def severe_dehydration(self):
        type.type("Your mouth is bone dry. Your skin has lost elasticity - when pinched, it stays tented.")
        print("\n")
        type.type("You're dizzy, confused. Heart racing. Haven't urinated in hours.")
        print("\n")
        type.type("Your blood is thickening. Your kidneys are shutting down.")
        print("\n")
        type.type(red("Severe dehydration") + ". You need IV fluids. Lots of them.")
        self.add_status("Severe Dehydration")
        self.hurt(20)
        self.lose_sanity(3)
        self.start_night()

    def malnutrition(self):
        type.type("You've been eating poorly. Or not at all. For too long.")
        print("\n")
        type.type("Your hair is falling out. Your nails are brittle. Wounds won't heal.")
        print("\n")
        type.type("You're exhausted, weak. Your immune system is compromised.")
        print("\n")
        type.type(red("Malnutrition") + ". Your body is eating itself to survive.")
        self.add_status("Malnutrition")
        self.hurt(15)
        self.lose_sanity(2)
        self.start_night()

    def nerve_damage(self):
        type.type("The injury damaged something important. A nerve bundle.")
        print("\n")
        type.type("Parts of your body are numb. Other parts are on fire with phantom pain.")
        print("\n")
        type.type("Some muscles won't respond at all. The signals just don't get through.")
        print("\n")
        type.type(red("Nerve damage") + ". May be permanent. May need surgery. May never fully recover.")
        self.add_injury("Nerve Damage")
        self.hurt(12)
        self.lose_sanity(4)
        self.start_night()

    def tendon_rupture(self):
        type.type("You felt the snap. Like a rubber band breaking inside your limb.")
        print("\n")
        type.type("The muscle bunched up, detached from where it should connect.")
        print("\n")
        type.type("You can't move the affected part. The power just isn't there.")
        print("\n")
        type.type(red("Ruptured tendon") + ". Needs surgical reattachment. Months of recovery.")
        self.add_injury("Ruptured Tendon")
        self.hurt(18)
        self.lose_sanity(2)
        self.start_night()

    def muscle_tear(self):
        type.type("The pop in your leg was followed by searing pain.")
        print("\n")
        type.type("A lump has formed where the muscle has bunched up. The area is bruising rapidly.")
        print("\n")
        type.type("Walking is nearly impossible. Every step is agony.")
        print("\n")
        type.type(red("Muscle tear") + ". Grade III. Complete rupture. Surgery likely.")
        self.add_injury("Muscle Tear")
        self.hurt(15)
        self.lose_sanity(1)
        self.start_night()

    def gangrene_infection(self):
        type.type("The wound has turned black. The tissue is dying, rotting while still attached to your body.")
        print("\n")
        type.type("The smell is unmistakable. Sweet, sickly, the odor of death.")
        print("\n")
        type.type("It's spreading. Every hour, more tissue dies.")
        print("\n")
        type.type(red("Gangrene") + ". Amputation may be the only option to save your life.")
        self.add_status("Gangrene")
        self.hurt(30)
        self.lose_sanity(6)
        self.start_night()

    # MENTAL HEALTH CONDITIONS (Doctor can help with these too)
    def severe_anxiety_attack(self):
        type.type("Your heart is pounding out of your chest. You can't breathe. You're dying - you're sure of it.")
        print("\n")
        type.type("Except you're not. This is a panic attack. But it feels like death.")
        print("\n")
        type.type("Trembling, sweating, derealization. The world doesn't feel real.")
        print("\n")
        type.type(red("Severe anxiety disorder") + ". You need medication. Therapy. Something.")
        self.add_status("Anxiety Disorder")
        self.lose_sanity(5)
        self.start_night()

    def severe_depression_episode(self):
        type.type("You can't get out of bed. Not 'don't want to' - literally cannot.")
        print("\n")
        type.type("Everything is gray. Nothing matters. You haven't showered in days. Eaten in longer.")
        print("\n")
        type.type("The weight on your chest is crushing. You're drowning in numbness.")
        print("\n")
        type.type(red("Major depressive episode") + ". You need help. If you can just reach out...")
        self.add_status("Severe Depression")
        self.lose_sanity(8)
        self.start_night()

    def insomnia_chronic(self):
        type.type("You haven't slept properly in weeks. Months maybe. The hours blur together.")
        print("\n")
        type.type("Your eyes burn. Your thoughts are sluggish. You're making mistakes constantly.")
        print("\n")
        type.type("Every night you lie there, exhausted but wired, watching the hours tick by.")
        print("\n")
        type.type(red("Chronic insomnia") + ". Your body is breaking down without rest.")
        self.add_status("Chronic Insomnia")
        self.hurt(10)
        self.lose_sanity(5)
        self.start_night()

    def ptsd_flashback(self):
        type.type("The sound triggers it. Or was it a smell? Suddenly you're THERE again.")
        print("\n")
        type.type("Not a memory - you're LIVING it. The fear is immediate, overwhelming.")
        print("\n")
        type.type("Your body reacts as if the trauma is happening NOW. Heart racing. Sweating. Shaking.")
        print("\n")
        type.type("When you come back to the present, you're curled on the floor. Hours have passed.")
        print("\n")
        type.type(red("PTSD flashback") + ". The trauma lives in your body. You need specialized help.")
        self.add_status("PTSD")
        self.lose_sanity(7)
        self.start_night()

    # EVENTS THAT CAUSE THESE CONDITIONS
    def dirty_needle_stick(self):
        type.type("You weren't paying attention. The needle went right into your hand.")
        print("\n")
        type.type("It wasn't clean. Rusty. Used. You don't know where it came from.")
        print("\n")
        type.type("Blood is beading at the puncture site. Your heart is racing with dread.")
        print("\n")
        type.type("What was on that needle? Hepatitis? HIV? " + red("Tetanus") + "?")
        print("\n")
        type.type("You need to get to a doctor. Get tested. Get prophylaxis. NOW.")
        self.add_status("Needle Exposure")
        self.add_danger("Possible Blood Disease")
        self.hurt(5)
        self.lose_sanity(4)
        self.start_night()

    def bad_oysters(self):
        type.type("The oysters tasted... off. You ate them anyway.")
        print("\n")
        type.type("Big mistake.")
        print("\n")
        type.type("Within hours, you're violently ill. Vomiting, diarrhea, fever, chills.")
        print("\n")
        type.type(red("Shellfish poisoning") + ". Vibrio bacteria. Could be fatal without treatment.")
        self.add_status("Shellfish Poisoning")
        self.hurt(20)
        self.lose_sanity(2)
        self.start_night()

    def rat_bite(self):
        type.type("The rat came out of nowhere. Cornered, scared, it bit down HARD on your hand.")
        print("\n")
        type.type("The wound is deep, ragged. Rat teeth are dirty - full of bacteria.")
        print("\n")
        type.type("Within days, you're running a fever. Red streaks spreading from the bite.")
        print("\n")
        type.type(red("Rat bite fever") + ". Without antibiotics, this could kill you.")
        self.add_status("Rat Bite Fever")
        self.add_injury("Rat Bite")
        self.hurt(15)
        self.start_night()

    def bad_mushrooms(self):
        type.type("You thought they were the safe kind. They were not.")
        print("\n")
        type.type("First came the nausea. Then the vomiting. Then the liver failure symptoms.")
        print("\n")
        type.type("Your skin is turning yellow. Your urine is dark brown. You're dying.")
        print("\n")
        type.type(red("Amanita poisoning") + ". Death cap mushroom. You need a liver transplant or you're dead.")
        self.add_status("Mushroom Poisoning")
        self.hurt(40)
        self.lose_sanity(5)
        self.start_night()

    def unclean_water(self):
        type.type("The water looked clear. But it was from a contaminated source.")
        print("\n")
        type.type("Giardia. Cryptosporidium. E. coli. Something got into your gut.")
        print("\n")
        type.type("The cramping is severe. The diarrhea is watery, foul. You're getting dehydrated fast.")
        print("\n")
        type.type(red("Waterborne illness") + ". You need treatment before you lose too many fluids.")
        self.add_status("Waterborne Illness")
        self.hurt(18)
        self.start_night()

    def mold_exposure(self):
        # EVENT: Toxic black mold exposure - chronic respiratory and cognitive issues
        # EFFECTS: Adds "Mold Toxicity" status, 12 damage, 3 sanity loss
        type.type("The building you stayed in was full of black mold. You didn't realize until too late.")
        print("\n")
        type.type("Now you're coughing constantly. Wheezing. Your sinuses are on fire.")
        print("\n")
        type.type("Headaches. Fatigue. Brain fog. Memory problems.")
        print("\n")
        type.type(red("Toxic mold exposure") + ". The spores are in your lungs. This could be chronic.")
        self.add_status("Mold Toxicity")
        self.hurt(12)
        self.lose_sanity(3)
        self.start_night()

    def bee_sting_allergy(self):
        # EVENT: Severe allergic reaction to bee sting - anaphylaxis
        # EFFECTS: Adds "Anaphylaxis" status, 30 damage, 3 sanity loss; needs EpiPen immediately
        type.type("One sting. That's all it took.")
        print("\n")
        type.type("Your throat is closing. Hives everywhere. Heart racing, blood pressure dropping.")
        print("\n")
        type.type("You're going into anaphylactic shock. Without an EpiPen, you have minutes.")
        print("\n")
        type.type(red("Severe bee allergy") + ". You need epinephrine NOW.")
        self.add_status("Anaphylaxis")
        self.hurt(30)
        self.lose_sanity(3)
        self.start_night()

    def lead_poisoning(self):
        # EVENT: Lead poisoning from old paint/pipes - neurological damage
        # EFFECTS: Adds "Lead Poisoning" status, 15 damage, 4 sanity loss; needs chelation therapy
        type.type("The paint was old. The pipes were ancient. You didn't think about it.")
        print("\n")
        type.type("But the lead built up in your system over time. Now the symptoms are showing.")
        print("\n")
        type.type("Abdominal pain. Confusion. Fatigue. The blue-gray line on your gums.")
        print("\n")
        type.type(red("Lead poisoning") + ". Your brain is being damaged. You need chelation therapy.")
        self.add_status("Lead Poisoning")
        self.hurt(15)
        self.lose_sanity(4)
        self.start_night()

    def asbestos_exposure(self):
        # EVENT: Asbestos fiber inhalation - permanent lung damage and cancer risk
        # EFFECTS: Adds "Asbestos Damage" status + "Cancer Risk" danger, 15 damage, 5 sanity loss
        type.type("You worked in that old building for months. Inhaling the dust.")
        print("\n")
        type.type("Now you're coughing. Short of breath. Chest pain.")
        print("\n")
        type.type("The X-ray shows scarring in your lungs. Plaques on your pleura.")
        print("\n")
        type.type(red("Asbestos exposure") + ". The fibers are embedded in your lungs forever. Mesothelioma is possible.")
        self.add_status("Asbestos Damage")
        self.add_danger("Cancer Risk")
        self.hurt(15)
        self.lose_sanity(5)
        self.start_night()

    def mercury_poisoning(self):
        # EVENT: Mercury poisoning from fish consumption - neurological damage
        # EFFECTS: Adds "Mercury Poisoning" status, 18 damage, 4 sanity loss; may be permanent
        type.type("You've been eating too much fish. The wrong kind. Mercury-laden.")
        print("\n")
        type.type("The tremors started first. Then the numbness in your hands and feet.")
        print("\n")
        type.type("Memory problems. Mood swings. Your vision is narrowing.")
        print("\n")
        type.type(red("Mercury poisoning") + ". Heavy metal toxicity. Neurological damage may be permanent.")
        self.add_status("Mercury Poisoning")
        self.hurt(18)
        self.lose_sanity(4)
        self.start_night()

    # ============================================
    # SITUATIONAL MEDICAL EVENTS - THINGS THAT CAUSE CONDITIONS
    # Accidents and injuries that result from everyday activities
    # ============================================

    def gym_accident(self):
        # EVENT: Weight lifting accident - herniated disc from ego lifting
        # EFFECTS: Adds "Herniated Disc" injury, 20 damage, 3 sanity loss
        type.type("You decide to hit the gym. Get in shape. How hard could it be?")
        print("\n")
        type.type("You load up the barbell with way too much weight. Ego lifting.")
        print("\n")
        type.type("On the third rep, something gives. Your back spasms. You drop the weight.")
        print("\n")
        type.type("You're on the ground, unable to move. People are gathering around.")
        print("\n")
        type.type(red("Herniated disc") + ". Your gym career is over before it started.")
        self.add_injury("Herniated Disc")
        self.hurt(20)
        self.lose_sanity(3)
        self.start_night()

    def slip_in_shower(self):
        # EVENT: Slip and fall in shower - concussion and head laceration
        # EFFECTS: Adds "Concussion" + "Deep Laceration" injuries, 25 damage, 3 sanity loss
        type.type("The shower floor is wet. Obviously. You reach for the shampoo...")
        print("\n")
        type.type("Your foot slips. You go down HARD.")
        print("\n")
        type.type("Your head bounces off the tile. Everything goes dark for a moment.")
        print("\n")
        type.type("You wake up with water pelting your face, blood mixing with the drain.")
        print("\n")
        type.type(red("Concussion") + " and a nasty gash on your head.")
        self.add_injury("Concussion")
        self.add_injury("Deep Laceration")
        self.hurt(25)
        self.lose_sanity(3)
        self.start_night()

    def fall_down_stairs(self):
        # EVENT: Fall down a flight of stairs - broken collarbone and ribs
        # EFFECTS: Adds "Broken Collarbone" + "Broken Ribs" injuries, 30 damage, 3 sanity loss
        type.type("You miss the top step. Just one moment of inattention.")
        print("\n")
        type.type("You tumble down the entire flight, hitting every step on the way.")
        print("\n")
        type.type("When you reach the bottom, you can't move your arm. Your ribs scream with every breath.")
        print("\n")
        type.type(red("Broken collarbone") + ". Possibly broken ribs too.")
        self.add_injury("Broken Collarbone")
        self.add_injury("Broken Ribs")
        self.hurt(30)
        self.lose_sanity(3)
        self.start_night()

    def car_accident_minor(self):
        # EVENT: Minor car accident - whiplash and possible broken ribs
        # EFFECTS: Adds "Whiplash" injury + 33% chance "Broken Ribs", 22 damage, 2 sanity loss
        type.type("The other car comes out of nowhere. You slam on the brakes but it's too late.")
        print("\n")
        type.type("CRUNCH. Your airbag deploys, slamming into your face.")
        print("\n")
        type.type("You're alive. But your neck... your neck won't turn. The seat belt bruised your chest badly.")
        print("\n")
        type.type(red("Whiplash") + " and possible broken ribs from the impact.")
        self.add_injury("Whiplash")
        if random.randint(1, 3) == 1:
            self.add_injury("Broken Ribs")
            type.type(" Those ribs are definitely cracked.")
        self.hurt(22)
        self.lose_sanity(2)
        self.start_night()

    def construction_site_accident(self):
        # EVENT: Fall into construction pit - broken ankle
        # EFFECTS: Adds "Broken Ankle" injury, 18 damage, 2 sanity loss
        type.type("You're walking past a construction site when the barrier gives way.")
        print("\n")
        type.type("You fall into the pit. It's not deep, but your ankle folds under you.")
        print("\n")
        type.type("The snap echoes off the concrete walls. You scream.")
        print("\n")
        type.type(red("Broken ankle") + ". The workers rush over, but the damage is done.")
        self.add_injury("Broken Ankle")
        self.hurt(18)
        self.lose_sanity(2)
        self.start_night()

    def bar_fight_aftermath(self):
        type.type("You don't remember who started it. You remember the fist connecting with your face.")
        print("\n")
        type.type("Blood sprays from your nose. You go down. Someone stomps on your hand.")
        print("\n")
        type.type("When security finally breaks it up, you're a mess.")
        print("\n")
        type.type(red("Broken nose") + ". " + red("Broken hand") + ". Maybe a black eye too.")
        self.add_injury("Broken Nose")
        self.add_injury("Broken Hand")
        self.hurt(25)
        self.lose_sanity(3)
        self.start_night()

    def kitchen_accident(self):
        type.type("You're chopping vegetables when your phone buzzes. You look away for one second...")
        print("\n")
        type.type("The knife goes straight through your finger. You can see bone.")
        print("\n")
        type.type("Blood is everywhere. You're going to need stitches. Probably surgery.")
        print("\n")
        type.type(red("Deep laceration") + ". Nearly severed your finger.")
        self.add_injury("Deep Laceration")
        self.hurt(15)
        self.start_night()

    def grease_fire(self):
        type.type("You're frying something when the oil catches fire. Panicking, you throw water on it.")
        print("\n")
        type.type("The fireball that erupts catches you full in the face and arms.")
        print("\n")
        type.type("You scream as your skin blisters and chars.")
        print("\n")
        type.type(red("Second degree burns") + " covering your arms. Some might be third degree.")
        self.add_status("Second Degree Burns")
        self.hurt(25)
        self.lose_sanity(4)
        self.start_night()

    def sports_injury(self):
        type.type("You're playing basketball when you pivot to shoot...")
        print("\n")
        type.type("POP.")
        print("\n")
        type.type("You heard it before you felt it. Your knee buckles. You go down clutching your leg.")
        print("\n")
        type.type(red("Torn ACL") + ". Season over. Maybe career over.")
        self.add_injury("Torn ACL")
        self.hurt(20)
        self.lose_sanity(3)
        self.start_night()

    def motorcycle_crash(self):
        type.type("The car didn't see you. Pulled right out in front of you.")
        print("\n")
        type.type("You lay the bike down, sliding across the pavement. Your leg gets trapped under the motorcycle.")
        print("\n")
        type.type("Road rash everywhere. But worse - your leg is mangled. You can see the bone.")
        print("\n")
        type.type(red("Broken leg") + ". " + red("Severe burns") + " from the friction and exhaust.")
        self.add_injury("Broken Leg")
        self.add_injury("Severe Burns")
        self.hurt(40)
        self.lose_sanity(5)
        self.start_night()

    def dog_attack_severe(self):
        type.type("The dog was loose. No leash. No owner in sight.")
        print("\n")
        type.type("It lunges at you before you can react. Teeth sink into your forearm.")
        print("\n")
        type.type("You fight it off but the damage is done. Your arm is torn to shreds.")
        print("\n")
        type.type(red("Deep lacerations") + ". Possible " + red("rabies exposure") + ". Definitely need stitches.")
        self.add_injury("Deep Laceration")
        self.add_status("Possible Rabies")
        self.hurt(28)
        self.lose_sanity(4)
        self.start_night()

    def pool_diving_accident(self):
        type.type("The pool looked deeper than it was. You dive in headfirst.")
        print("\n")
        type.type("Your head hits the bottom. Your neck compresses. Everything goes numb for a terrifying moment.")
        print("\n")
        type.type("You surface, panicking, but find you can still move. Barely.")
        print("\n")
        type.type(red("Fractured spine") + ". You're lucky you're not paralyzed.")
        self.add_injury("Fractured Spine")
        self.hurt(35)
        self.lose_sanity(6)
        self.start_night()

    def chemical_spill(self):
        type.type("The bottle wasn't labeled. You opened it and it splashed on your skin.")
        print("\n")
        type.type("Immediately, burning. Intense, searing burning. Your skin is bubbling.")
        print("\n")
        type.type("You rinse and rinse but the damage is done.")
        print("\n")
        type.type(red("Chemical burn") + ". Whatever that was, it ate through your flesh.")
        self.add_injury("Chemical Burn")
        self.hurt(22)
        self.lose_sanity(3)
        self.start_night()

    def electric_shock(self):
        type.type("The wire was exposed. You didn't see it.")
        print("\n")
        type.type("The jolt throws you across the room. Your heart stutters. Your muscles seize.")
        print("\n")
        type.type("You come to on the floor, smoking slightly, your hand charred where you touched it.")
        print("\n")
        type.type(red("Electrical burns") + ". Internal damage unknown. Your heart is still skipping beats.")
        self.add_injury("Electrical Burns")
        self.hurt(30)
        self.lose_sanity(4)
        self.start_night()

    def workplace_injury(self):
        type.type("The machinery caught your arm. Before you could pull away, it crushed everything.")
        print("\n")
        type.type("Bones shattered. Muscles pulped. You screamed until you passed out.")
        print("\n")
        type.type("When you wake up in the hospital, your arm is heavily bandaged. The doctor looks grim.")
        print("\n")
        type.type(red("Crush injury") + ". They saved the arm. Barely. Function uncertain.")
        self.add_injury("Crush Injury")
        self.hurt(40)
        self.lose_sanity(6)
        self.start_night()

    def assault_aftermath(self):
        type.type("They came out of nowhere. Multiple attackers. You didn't stand a chance.")
        print("\n")
        type.type("The beating was brutal. When they left, you couldn't move.")
        print("\n")
        type.type("Broken ribs. Concussion. Internal bleeding. You're barely conscious when help arrives.")
        print("\n")
        type.type(red("Multiple injuries") + ". You might have a " + red("ruptured spleen") + ".")
        self.add_injury("Broken Ribs")
        self.add_injury("Concussion")
        if random.randint(1, 2) == 1:
            self.add_injury("Ruptured Spleen")
        self.hurt(45)
        self.lose_sanity(7)
        self.start_night()

    def caught_in_fire(self):
        type.type("The building is on fire. You're trapped.")
        print("\n")
        type.type("You run through the flames, your clothes igniting. The smoke fills your lungs.")
        print("\n")
        type.type("You make it out. Barely. Your skin is charred. You can't stop coughing.")
        print("\n")
        type.type(red("Severe burns") + ". Smoke inhalation. " + red("Collapsed lung") + " from the heat damage.")
        self.add_injury("Severe Burns")
        self.add_injury("Collapsed Lung")
        self.hurt(45)
        self.lose_sanity(6)
        self.start_night()

    def frozen_outdoors(self):
        type.type("You got lost. The temperature dropped. You couldn't find shelter.")
        print("\n")
        type.type("By the time they found you, your extremities were black. Your core temperature was dangerously low.")
        print("\n")
        type.type("You survived. But your fingers and toes...")
        print("\n")
        type.type(red("Frostbite") + ". Amputation might be necessary. " + red("Hypothermia") + " damage to your organs.")
        self.add_injury("Frostbite")
        self.add_status("Hypothermia")
        self.hurt(35)
        self.lose_sanity(5)
        self.start_night()

    def heat_exhaustion_collapse(self):
        type.type("You were outside too long. Too hot. Not enough water.")
        print("\n")
        type.type("First you stopped sweating. Then you got dizzy. Then you collapsed.")
        print("\n")
        type.type("When you wake up, you're in an ambulance, ice packs covering your body.")
        print("\n")
        type.type(red("Heat stroke") + ". Your body temperature hit 106. You're lucky to be alive.")
        self.add_status("Heat Stroke")
        self.hurt(30)
        self.lose_sanity(4)
        self.start_night()

    def drug_overdose_survival(self):
        type.type("You took too much. You knew immediately.")
        print("\n")
        type.type("Your heart raced. Or maybe it slowed. You couldn't tell. Everything was wrong.")
        print("\n")
        type.type("You woke up in the ER with someone pulling a tube out of your throat.")
        print("\n")
        type.type(red("Overdose") + ". They gave you Narcan. Or charcoal. Whatever it took to save your life.")
        self.add_status("Severe Dehydration")
        self.add_status("Seizure Disorder")
        self.hurt(35)
        self.lose_sanity(8)
        self.start_night()

    def allergic_reaction_restaurant(self):
        type.type("They said there were no nuts in the dish. They lied.")
        print("\n")
        type.type("Within minutes, your throat is closing. Hives everywhere. You can't breathe.")
        print("\n")
        type.type("Someone stabs you with an EpiPen. You're rushed to the hospital.")
        print("\n")
        type.type(red("Anaphylaxis") + ". Severe allergic reaction. You almost died in that restaurant.")
        self.add_status("Anaphylaxis")
        self.hurt(25)
        self.lose_sanity(5)
        self.start_night()

    def botched_surgery(self):
        type.type("The surgery was supposed to be routine. It wasn't.")
        print("\n")
        type.type("When you wake up, something is wrong. Terribly wrong.")
        print("\n")
        type.type("They nicked an artery. They left something inside. Something went septic.")
        print("\n")
        type.type(red("Surgical complications") + ". Now you're fighting for your life instead of recovering.")
        self.add_status("Sepsis")
        self.add_injury("Puncture Wound")
        self.hurt(40)
        self.lose_sanity(6)
        self.start_night()

    def dental_disaster(self):
        type.type("You've been ignoring that toothache for weeks. Months. It's gotten worse.")
        print("\n")
        type.type("Now your face is swollen. You can feel pus draining into your mouth. The fever is high.")
        print("\n")
        type.type("The infection is spreading toward your brain.")
        print("\n")
        type.type(red("Tooth abscess") + " gone systemic. " + red("Sepsis") + " is setting in.")
        self.add_status("Tooth Abscess")
        self.add_status("Sepsis")
        self.hurt(35)
        self.lose_sanity(5)
        self.start_night()

    def gym_collapse(self):
        type.type("You're on the treadmill, pushing hard. Too hard.")
        print("\n")
        type.type("Your chest tightens. Your left arm goes numb. You stumble off the machine.")
        print("\n")
        type.type("Is this... a heart attack? At your age?")
        print("\n")
        type.type(red("Cardiac event") + ". You need help. NOW.")
        self.add_status("Blood Pressure Crisis")
        self.add_danger("Heart Condition")
        self.hurt(30)
        self.lose_sanity(5)
        self.start_night()

    def food_truck_nightmare(self):
        type.type("The food truck looked sketchy but you were hungry. Big mistake.")
        print("\n")
        type.type("Hours later, you're praying to the porcelain god. Both ends. Simultaneously.")
        print("\n")
        type.type("The cramping is severe. There's blood in the diarrhea. This is serious.")
        print("\n")
        type.type(red("Severe food poisoning") + ". E. coli or Salmonella. You need IV fluids.")
        self.add_status("Stomach Flu")
        self.add_status("Severe Dehydration")
        self.hurt(25)
        self.lose_sanity(3)
        self.start_night()

    def public_pool_infection(self):
        type.type("The public pool was crowded. Too crowded. The water was... questionable.")
        print("\n")
        type.type("A week later, your ear is killing you. Burning when you urinate. Eye is crusty.")
        print("\n")
        type.type("You picked up everything in that cesspool.")
        print("\n")
        type.type(red("Ear infection") + ". " + red("Pink eye") + ". Possibly a " + red("UTI") + ".")
        self.add_status("Ear Infection")
        self.add_status("Pink Eye")
        if random.randint(1, 2) == 1:
            self.add_status("UTI")
        self.hurt(12)
        self.start_night()

    def hiking_disaster(self):
        type.type("The hike was supposed to be easy. Then the trail gave way.")
        print("\n")
        type.type("You tumbled down the ravine, bouncing off rocks, trying to protect your head.")
        print("\n")
        type.type("When you stop falling, you can't move your ankle. Your wrist is bent wrong. You're bleeding from somewhere.")
        print("\n")
        type.type(red("Broken ankle") + ". " + red("Broken wrist") + ". Miles from help.")
        self.add_injury("Broken Ankle")
        self.add_injury("Broken Wrist")
        self.hurt(30)
        self.lose_sanity(4)
        self.start_night()

    def wasp_nest_encounter(self):
        type.type("You didn't see the nest. Not until it was too late.")
        print("\n")
        type.type("The swarm descends on you. Stings everywhere. You run, but they follow.")
        print("\n")
        type.type("By the time you escape, you've been stung dozens of times. Your throat is tightening...")
        print("\n")
        type.type(red("Multiple wasp stings") + ". Possible " + red("anaphylaxis") + ".")
        self.add_status("Anaphylaxis")
        self.hurt(30)
        self.lose_sanity(4)
        self.start_night()

    def camping_tick_bite(self):
        type.type("You find the tick embedded in your skin days after the camping trip.")
        print("\n")
        type.type("It's engorged. Been feeding for a while. You pull it out, but the damage is done.")
        print("\n")
        type.type("Weeks later, the symptoms start. Joint pain. Fatigue. The telltale rash.")
        print("\n")
        type.type(red("Lyme disease") + ". That one tick has changed your life.")
        self.add_status("Lyme Disease")
        self.hurt(15)
        self.lose_sanity(3)
        self.start_night()

    def homeless_shelter_outbreak(self):
        type.type("You stayed at the shelter when you had nowhere else to go.")
        print("\n")
        type.type("The beds were close together. Too close. Someone was coughing all night.")
        print("\n")
        type.type("Within days, you're coughing too. Deep, rattling coughs. Fever. Night sweats.")
        print("\n")
        type.type(red("Pneumonia") + ". Maybe something worse. The conditions were ripe for disease.")
        self.add_status("Pneumonia")
        self.hurt(18)
        self.lose_sanity(2)
        self.start_night()

    def prison_shiv_wound(self):
        type.type("Wrong place. Wrong time. Wrong look at the wrong guy.")
        print("\n")
        type.type("The sharpened toothbrush went into your gut before you even saw it coming.")
        print("\n")
        type.type("You're on the ground, holding your intestines in, as guards finally respond.")
        print("\n")
        type.type(red("Puncture wound") + ". Perforated bowel. " + red("Sepsis") + " is a certainty without immediate surgery.")
        self.add_injury("Puncture Wound")
        self.add_status("Sepsis")
        self.hurt(45)
        self.lose_sanity(6)
        self.start_night()

    def daycare_plague(self):
        type.type("Your kid brought home something from daycare. Now everyone has it.")
        print("\n")
        type.type("First the stomach flu spread through the family. Then the ear infections. Then the pink eye.")
        print("\n")
        type.type("You're exhausted, sick, and covered in various bodily fluids.")
        print("\n")
        type.type(red("Multi-infection") + ". Kids are disease vectors. You're patient zero's victim.")
        self.add_status("Stomach Flu")
        self.add_status("Ear Infection")
        self.add_status("Pink Eye")
        self.hurt(20)
        self.lose_sanity(3)
        self.start_night()

    def bad_tattoo_infection(self):
        type.type("The tattoo parlor was cheap. Too cheap. Now you know why.")
        print("\n")
        type.type("The fresh ink is swollen, oozing pus. Red lines spreading outward.")
        print("\n")
        type.type("The artist didn't sterilize properly. Or used contaminated ink.")
        print("\n")
        type.type(red("Staph infection") + " from a dirty needle. Your new tattoo might kill you.")
        self.add_status("Staph Infection")
        self.hurt(18)
        self.lose_sanity(2)
        self.start_night()

    def mma_fight_aftermath(self):
        type.type("You thought you could handle yourself in a fight. You were wrong.")
        print("\n")
        type.type("The armbar hyperextended your elbow. The chokehold knocked you out. The ground and pound did the rest.")
        print("\n")
        type.type("You leave the cage on a stretcher.")
        print("\n")
        type.type(red("Dislocated shoulder") + ". " + red("Concussion") + ". " + red("Broken ribs") + ".")
        self.add_injury("Dislocated Shoulder")
        self.add_injury("Concussion")
        self.add_injury("Broken Ribs")
        self.hurt(40)
        self.lose_sanity(5)
        self.start_night()

    def covid_complications(self):
        type.type("It started like a cold. Then you couldn't breathe.")
        print("\n")
        type.type("Your oxygen levels dropped. Your lungs filled with fluid. You were intubated for two weeks.")
        print("\n")
        type.type("You survived. But the damage...")
        print("\n")
        type.type(red("Severe respiratory infection") + ". " + red("DVT") + " from lying in bed. Long-term effects unknown.")
        self.add_status("Pneumonia")
        self.add_status("DVT")
        self.hurt(35)
        self.lose_sanity(6)
        self.start_night()

    def earthquake_injury(self):
        type.type("The building shook. The ceiling came down.")
        print("\n")
        type.type("You were trapped under debris for hours. Concrete pinning your legs.")
        print("\n")
        type.type("When they pulled you out, the real danger began - crush syndrome.")
        print("\n")
        type.type(red("Crush injury") + ". Toxins flooding your system. Kidneys failing.")
        self.add_injury("Crush Injury")
        self.hurt(40)
        self.lose_sanity(7)
        self.start_night()

    def carnival_ride_accident(self):
        type.type("The ride malfunctioned. The safety bar wasn't locked properly.")
        print("\n")
        type.type("You were thrown from the car, hitting multiple surfaces on the way down.")
        print("\n")
        type.type("The crowd screams. You can't feel your legs.")
        print("\n")
        type.type(red("Fractured spine") + ". " + red("Broken collarbone") + ". Internal injuries unknown.")
        self.add_injury("Fractured Spine")
        self.add_injury("Broken Collarbone")
        self.hurt(45)
        self.lose_sanity(8)
        self.start_night()

    def window_crash(self):
        type.type("Someone pushed you. Or you fell. The glass shattered around you.")
        print("\n")
        type.type("You're covered in cuts. Some are deep - arterial spurting. Glass is embedded everywhere.")
        print("\n")
        type.type("You're losing blood fast.")
        print("\n")
        type.type(red("Multiple lacerations") + ". " + red("Puncture wounds") + " from glass shards.")
        self.add_injury("Deep Laceration")
        self.add_injury("Puncture Wound")
        self.hurt(35)
        self.lose_sanity(4)
        self.start_night()

    def trampoline_disaster(self):
        type.type("You're never too old for trampolines. That's what you told yourself.")
        print("\n")
        type.type("You landed wrong. Your knee went in a direction knees don't go.")
        print("\n")
        type.type("The pop was audible. The pain was indescribable.")
        print("\n")
        type.type(red("Torn ACL") + ". Also " + red("dislocated kneecap") + ". Reconstruction required.")
        self.add_injury("Torn ACL")
        self.hurt(25)
        self.lose_sanity(3)
        self.start_night()

    def explosion_nearby(self):
        type.type("The explosion threw you ten feet. Your ears are ringing. Blood coming from everywhere.")
        print("\n")
        type.type("Shrapnel. Burns. Concussion. You don't know which direction is up.")
        print("\n")
        type.type("Everything is muffled. Everything hurts.")
        print("\n")
        type.type(red("Ruptured eardrums") + ". " + red("Concussion") + ". " + red("Second degree burns") + ". " + red("Shrapnel wounds") + ".")
        self.add_injury("Ruptured Eardrum")
        self.add_injury("Concussion")
        self.add_status("Second Degree Burns")
        self.add_injury("Puncture Wound")
        self.hurt(45)
        self.lose_sanity(7)
        self.start_night()

    def botched_piercing(self):
        type.type("The piercing didn't heal right. It got infected. Then REALLY infected.")
        print("\n")
        type.type("Your ear is swollen, hot, draining pus. The cartilage might be damaged.")
        print("\n")
        type.type("All for a little hole.")
        print("\n")
        type.type(red("Staph infection") + " from improper aftercare. Possible permanent ear deformity.")
        self.add_status("Staph Infection")
        self.hurt(12)
        self.lose_sanity(2)
        self.start_night()

    def weight_dropping(self):
        type.type("You're spotting someone at the gym. They lose control of the weight.")
        print("\n")
        type.type("The barbell comes down on your hand before you can move.")
        print("\n")
        type.type("You hear the bones crack before you feel it.")
        print("\n")
        type.type(red("Broken hand") + ". Multiple metacarpal fractures. Surgical repair needed.")
        self.add_injury("Broken Hand")
        self.hurt(18)
        self.lose_sanity(2)
        self.start_night()

    def bad_sushi(self):
        type.type("The sushi was a day old. Maybe two. You ate it anyway.")
        print("\n")
        type.type("The food poisoning hits hard. But there's something else. Parasites.")
        print("\n")
        type.type("You can feel something moving in your gut. Something alive.")
        print("\n")
        type.type(red("Parasitic infection") + ". Anisakis worms from raw fish. They're eating you from inside.")
        self.add_status("Waterborne Illness")
        self.add_status("Stomach Flu")
        self.hurt(22)
        self.lose_sanity(5)
        self.start_night()

    def coma_awakening(self):
        type.type("You don't remember the accident. You don't remember the last three weeks.")
        print("\n")
        type.type("You wake up in a hospital bed, tubes everywhere. Muscles atrophied. Confused.")
        print("\n")
        type.type("The doctors tell you you're lucky to be alive. You don't feel lucky.")
        print("\n")
        type.type(red("Severe injuries") + " from an event you can't recall. " + red("Nerve damage") + ". " + red("DVT") + " from bed rest.")
        self.add_injury("Nerve Damage")
        self.add_status("DVT")
        self.add_status("Malnutrition")
        self.hurt(30)
        self.lose_sanity(8)
        self.start_night()

    def stress_breakdown(self):
        type.type("It's all too much. The gambling. The stress. The fear. The debt.")
        print("\n")
        type.type("Your heart starts racing and won't stop. You can't breathe. You're dying. You're sure of it.")
        print("\n")
        type.type("Hours later, still trembling, you realize it was a panic attack. But it felt real.")
        print("\n")
        type.type(red("Severe anxiety disorder") + ". " + red("Chronic insomnia") + ". Your mind is breaking.")
        self.add_status("Anxiety Disorder")
        self.add_status("Chronic Insomnia")
        self.lose_sanity(10)
        self.start_night()

    def trauma_flashback(self):
        type.type("Something triggers it. A sound. A smell. Suddenly you're THERE again.")
        print("\n")
        type.type("The casino. The Dealer. The losses. The fear. You relive it all in an instant.")
        print("\n")
        type.type("When you come back to reality, you're curled on the floor, shaking.")
        print("\n")
        type.type(red("PTSD episode") + ". The trauma is embedded in your nervous system.")
        self.add_status("PTSD")
        self.lose_sanity(8)
        self.start_night()

    def sleep_deprivation_crisis(self):
        type.type("How long since you slept? Three days? Four? You've lost count.")
        print("\n")
        type.type("You're seeing things. Hearing things. Your thoughts don't connect properly.")
        print("\n")
        type.type("Your body is shutting down from lack of rest.")
        print("\n")
        type.type(red("Chronic insomnia") + " induced psychosis. " + red("Severe depression") + ". You need medical intervention.")
        self.add_status("Chronic Insomnia")
        self.add_status("Severe Depression")
        self.hurt(15)
        self.lose_sanity(12)
        self.start_night()

    # BASIC COMMON ILLNESSES

