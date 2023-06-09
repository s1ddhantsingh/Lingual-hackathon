from textblob import TextBlob
import nltk
import language_tool_python as ltp
from flask import Flask, request, render_template

nltk.download('wordnet')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

cliche_list = ['a chip off the old block', 'a clean slate', 'a dark and stormy night', 'a far cry', 'a fine kettle of fish', 'a good/kind soul', 'a loose cannon', 'a pain in the neck/butt', 'a penny saved is a penny earned', 'a tough row to hoe', 'a word to the wise', 'ace in the hole', 'ace up his sleeve', 'add insult to injury', 'afraid of his own shadow', 'against all odds', 'air your dirty laundry', 'all fun and games', 'all in a day\'s work', 'all talk, no action', 'all thumbs', 'all your eggs in one basket', 'all\'s fair in love and war', 'all\'s well that ends well', 'almighty dollar', 'American as apple pie', 'an axe to grind', 'another day, another dollar', 'armed to the teeth', 'as luck would have it', 'as old as time', 'as the crow flies', 'at my wits end', 'avoid like the plague', 'babe in the woods', 'back against the wall',  'back in the saddle', 'back to square one', 'back to the drawing board', 'bad to the bone', 'badge of honor', 'bald faced liar', 'banging your head against a brick wall', 'ballpark figure', 'baptism by fire', 'bark is worse than her bite', 'barking up the wrong tree', 'bat out of hell', 'be all and end all', 'beat a dead horse', 'beat around the bush', 'bee in her bonnet', 'been there, done that', 'beggars cant be choosers', 'behind the eight ball', 'bend over backwards', 'benefit of the doubt', 'bent out of shape', 'best thing since sliced bread', 'bet your bottom dollar', 'better half', 'better late than never', 'better mousetrap', 'better safe than sorry', 'between a rock and a hard place', 'beyond the pale', 'bide your time', 'big as life', 'big fish in a small pond', 'big cheese', 'big man on campus', 'bigger they are the harder they fall', 'bird in the hand', 'birds and the bees', 'bird\'s eye view', 'birds of a feather flock together', 'bite the bullet', 'bite the dust', 'bit the hand that feeds you', 'bitten off more than he can chew', 'black as coal', 'black as pitch', 'black as the ace of spades', 'blast from the past', 'bleeding heart', 'blessing in disguise', 'blind ambition', 'blind as a bat', 'blind leading the blind', 'blood is thicker than water', 'blood sweat and tears', 'blow off steam', 'blow your own horn', 'blushing bride', 'boils down to', 'bone to pick', 'bored to tears', 'bored stiff', 'bottomless pit', 'boys will be boys', 'bright and early', 'brings home the bacon', 'broad across the beam', 'broken record', 'bull by the horns', 'bull in a china shop', 'burn the midnight oil', 'burning the candle at both ends', 'burning question', 'burst your bubble', 'bury the hatchet', 'busy as a bee', 'by hook or by crook', 'call a spade a spade', "called onto the carpet", "calm before the storm", "can of worms", "can't cut the mustard", "can't hold a candle to", "case of mistaken identity", "cat got your tongue", "caught in the crossfire", "caught red-handed", "caught with his/her pants down", "checkered past", "chip on his/her shoulder", "chomping at the bit", "cleanliness is next to godliness", "clear as a bell", "clear as mud", "close to the vest", "cock and bull story", "cold shoulder", "come hell or high water", "cost a king's ransom", "cost/paid an arm and a leg", "count your blessings", "crack of dawn", "crash course", "creature comforts", "cross that bridge when you come to it", "cry her eyes out", "cry like a baby", "cry me a river", "crystal clear", "curiosity killed the cat", "cut and dried", "cut through the red tape", "cut to the chase", "cute as a bug's ear", "cute as a button", "cute as a puppy", "cuts to the quick", "dark before the dawn", "day in, day out", "dead as a doornail",  "devil is in the details", "dime a dozen", "divide and conquer", "dog and pony show", "dog days", "dog eat dog", "dog tired", "don't burn your bridges", "don't count your chickens before they're hatched", "don't look a gift horse in the mouth",  "don't rock the boat", "don't step on anyone's toes", "don't take any wooden nickels", "down and out", "down at the heels", "down in the dumps", "down on his/her luck", "down the hatch", "down to earth", "draw the line", "dressed to kill", "dressed to the nines", "drives me up the wall", "dull as dishwater", "dyed in the wool", "eagle eye", "easy as pie", "eat your heart out", "eat your words", "enough to piss off the Pope", "ear to the ground", "early bird catches the worm", "earn his/her keep", "easier said than done", "easy as 1-2-3", "easy as pie", "eleventh hour", "even the playing field", "every dog has its day", "every fiber of my being", "everything but the kitchen sink", "eye for an eye", "eyes in the back of her head", "facts of life", "fair weather friend", "fan the flames", "fair weather friend", "fall by the wayside", "feast or famine", "feather in his cap", "feather your nest", "few and far between", "fifteen minutes of fame", "filthy vermin", "fine kettle of fish", "fish out of water", "fishing for a compliment", "fit as a fiddle", "fit the bill", "fit to be tied", "flat as a pancake", "flip your lid", "flog a dead horse", "fly by night", "fly the coop", "follow your heart", "for all intents and purposes", "for the birds", "for what it's worth", "force of nature", "force to be reckoned with", "forgive and forget", "fox in the henhouse", "free and easy", "free as a bird", "fresh as a daisy", "full steam ahead", "fun in the sun", "garbage in, garbage out", "get a kick out of", "get a leg up", "get down and dirty", "get his/her back up", "get the lead out", "get to the bottom of", "get your feet wet", "gets my goat", "gilding the lily", "give and take", "go against the grain", "go for broke", "go him one better", "go the extra mile", "go with the flow", "goes without saying", "good as gold", "good deed for the day", "good things come to those who wait", "good time was had by all", "greek to me", "green thumb", "green-eyed monster", "growing like a weed", "grist for the mill", "hair of the dog", "hand to mouth", "happy as a clam", "hasn't a clue", "have a nice day", "have high hopes", "haven't got a row to hoe", "have the last laugh", "head honcho", "hear a pin drop", "heard it through the grapevine", "heart's content", "hem and haw", "high and dry", "high and mighty", "high as a kite", "hit paydirt", "hold your horses", "hold your tongue", "hold your head up high", "hold your own", "honest as the day is long", "horse of a different color", "hot under the collar", "I beg to differ", "icing on the cake", "if the shoe fits", "if the shoe were on the other foot", "in a jam", "in a jiffy", "in a nutshell", "in a pig's eye", "in a pinch", "in a word", "in his/her element", "in hot water", "in over his/her head", "in the gutter", "in the nick of time", "in the thick of it", "in this day and age", "in your dreams", "it ain't over till the fat lady sings",
               "it goes without saying", "it's a small world", "it's only a matter of time", "it takes all kinds", "it takes one to know one", "ivory tower", "Jack of all trades", "jockey for position", "jog your memory", "Johnny-come-lately", "joined at the hip", "judge a book by its cover", "jump down your throat", "jump in with both feet", "jump on the bandwagon", "jump the gun", "jump to conclusions", "just a hop, skip, and a jump", "just the ticket", "justice is blind", "keep a stiff upper lip", "keep an eye on", "keep it simple, stupid", "keep the home fires burning", "keep up with the Joneses", "keep your chin up", "keep your fingers crossed", "kick the bucket", "kick up your heels", "kick your feet up", "kid in a candy store", "kill two birds with one stone", "kick his lights out", "kick the bucket", "kiss of death", "knock his block off", "knock it out of the park", "knock on wood", "knock your socks off", "make hay while the sun shines", "make money hand over fist", "make my day""make the best of a bad situation", "make the best of it", "make your blood boil", "man of few words", "man's best friend", "mark my words", "missed the boat on that one", "moment in the sun", "moment of glory", "moment of truth", "money to burn", "more power to you", "more than one way to skin a cat", "movers and shakers", "naked as a jaybird", "naked truth", "neat as a pin", "needless to say", "neither here nor there", "never look back", "never say never", "nip and tuck", "nip it in the bud", "no guts, no glory", "no love lost", "no pain, no gain", "no skin off my back", "no stone unturned", "no time like the present", "no use crying over spilled milk", "nose to the grindstone", "not a hope in hell", "not a minute's peace", "not playing with a full deck", "not the end of the world", "not in my backyard", "not written in stone", "nothing to sneeze at", "nothing ventured nothing gained", "now we're cooking", "off the top of my head", "off the wagon", "off the wall", "older and wiser", "older than dirt", "older than Methuselah", "old hat", "on a roll", "on cloud nine", "on his/her high horse", "on pins and needles", "on the bandwagon", "on the money", "on the nose", "on the rocks", "on the spot", "on the tip of my tongue", "on the wagon", "on thin ice", "once bitten, twice shy", "one bad apple doesn't spoil the bushel", "one born every minute", "one brick short", "one foot in the grave", "one in a million", "one red cent", "only game in town", "open a can of worms", "open the flood gates", "opportunity doesn't knock twice", "over the hump", "out of pocket", "out of sight, out of mind", "out of the frying pan into the fire", "out of the woods", "out on a limb", "over a barrel", "pain and suffering", "panic button", "par for the course", "part and parcel", "party pooper", "pass the buck", "patience is a virtue", "pay through the nose", "penny pincher", "perfect storm", "pig in a poke", "pin your hopes on", "pitter patter of little feet", "plain as day", "plain as the nose on your face", "play by the rules", "play your cards right", "playing the field", "playing with fire", "pleased as punch", "plenty of fish in the sea", "poor as a church mouse", "pot calling the kettle black", "pull a fast one", "pull your punches", "pulled the wool over his/her eyes", "pulling your leg", "pure as the driven snow", "put one over on you",  "put the pedal to the metal", "put the cart before the horse", 'quick as a bunny', 'quick as a lick', 'quick as a wink', 'quick as lightning', 'quiet as a dormouse', 'rags to riches', 'raining buckets', 'raining cats and dogs', 'rank and file', 'reap what you sow', 'red as a beet', 'red herring', 'reinvent the wheel', 'rich and famous', 'rings a bell', 'ripped me off', 'rise and shine', 'road to hell is paved with good intentions', 'rob Peter to pay Paul', 'roll over in the grave', 'rub the wrong way', 'running in circles', 'salt of the earth', 'scared out of his/her wits', 'scared stiff', 'scared to death', 'sealed with a kiss', 'second to none', 'see eye to eye', 'seen the light', 'seize the day', 'set the record straight', 'set your teeth on edge', 'sharp as a tack', 'shoot the breeze', 'shoot for the moon', 'shot in the dark', 'shoulder to the wheel', 'sick as a dog', 'sigh of relief', 'signed, sealed, and delivered', 'sink or swim', 'six of one, half a dozen of another', 'skating on thin ice', 'slept like a log', 'slinging mud', 'slippery as an eel', 'slow as molasses in January', 'smooth as a babys bottom', 'snug as a bug in a rug', 'sow wild oats', 'spare the rod, spoil the child', 'speak of the devil', 'spilled the beans', 'spinning your wheels', 'spitting image of', 'spoke with relish', 'spring to life', 'stands out like a sore thumb', 'squeaky wheel gets the grease', 'start from scratch', 'stick in the mud', 'still waters run deep', 'stitch in time', 'stop and smell the roses', 'straw that broke the camels back', 'strong as an ox', 'stubborn as a mule', 'stuff that dreams are made of', 'stuffed shirt', 'sweating blood', 'sweating bullets', 'take a load off', 'take one for the team', 'take the bait', 'take the bull by the horns', 'take the plunge', 'takes one to know one', 'takes two to tango', 'the more the merrier', 'the real deal', 'the real McCoy', 'the red carpet treatment', 'the same old story', 'there is no accounting for taste', 'thick as a brick', 'thick as thieves', 'think outside of the box', 'third times the charm', 'this day and age', 'this hurts me worse than it hurts you', 'this point in time', 'three sheets to the wind', 'three strikes against him/her', 'throw in the towel', 'tie one on', 'tighter than a drum', 'time and time again', 'time is of the essence', 'tip of the iceberg', 'to each his own', 'to the best of my knowledge', 'toe the line', 'tongue-in-cheek', 'too good to be true', 'too hot to handle', 'too numerous to mention', 'touch with a ten foot pole', 'tough as nails', 'trials and tribulations', 'tried and true', 'trip down memory lane', 'twist of fate', 'two cents worth', "ugly as sin", "under his/her thumb", "under the counter", "under the gun", "under the same roof", "until the cows come home", "unvarnished truth", "up his sleeve", "up the creek", "up to his ears in trouble", "uphill battle", "upper crust", "upset the applecart", "V for victory", "vain attempt", "vain effort", "vanquish the enemy", "vested interest", "waiting for the other shoe to drop", "wakeup call", "warm welcome", "watching the clock", "watch your p's and q's", "watch your tongue", "water under the bridge", "weather the storm", "went belly up", "wet behind the ears", "weed them out", "week of Sundays", "what goes around comes around", "what you see is what you get", "when it rains, it pours", "when push comes to shove", "when the cat's away"]


def correct_spelling(word):
    blob = TextBlob(word)
    corrected = blob.correct()
    if word != str(corrected):
        return str(corrected)
    else:
        return word


def check_grammar(text):
    tool = ltp.LanguageTool('en-US')
    matches = tool.check(text)

    for match in reversed(matches):
        offsetMatch = match.offset+match.errorLength
        error = text[match.offset: offsetMatch]
        correction = match.replacements[0]
        if error != correction:
            text = text[:match.offset] + \
                correction.upper() + text[offsetMatch:]
            print(f"Error is : {error}. Correction is: {correction}")

    words = text.split()
    for i in range(len(words)):
        corrected = correct_spelling(words[i])
        if corrected != words[i]:
            words[i] = corrected

    return text


def count_repeated_words(string):
    word_counts = {}
    string = string.lower()
    words = string.split(" ")

    for word in words:
        if word in word_counts:
            word_counts[word] += 1
        else:
            word_counts[word] = 1

    repeated_words = {}

    for word, count in word_counts.items():
        if count > 1:
            repeated_words[word] = count

    return repeated_words


def is_passive_voice(sentence):
    tokens = nltk.word_tokenize(sentence)
    tagged = nltk.pos_tag(tokens)

    verb = None
    subject = None
    for word, pos in tagged:
        if pos.startswith('V'):
            verb = word
        elif pos.startswith('N'):
            subject = word

    if verb and verb.endswith('ed'):
        for i in range(len(tagged)):
            if tagged[i][0] == 'by':
                agent = tagged[i+1][0]
                return f"Passive voice. Agent: {agent}"

        return "Passive voice."

    return "Active voice."


def check_cliches(text):
    for sentence in cliche_list:
        if sentence in text:
            print(sentence + " is in text")


NLP = Flask(__name__)

@NLP.route('/')
def index():
    return render_template('lingual.html')

@NLP.route('/modify_input', methods=['POST'])
def modify_input():
    input_text = request.form['text']
    modified_grammer = check_grammar(input_text)
    modifed_cliches = check_cliches(input_text)
    voice = is_passive_voice(input_text)
    repWords = count_repeated_words(input_text)

    modifed_text = modifed_cliches + modifed_text + modified_grammer + voice + repWords

    return render_template('lingual.html', modified_text=modifed_text)


if __name__ == '__main__':
    NLP.run()