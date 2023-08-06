import re
import warnings

from os             import path, environ, name as os_name
from re             import compile as re_compile
from nltk           import word_tokenize  # , internals
from nltk.corpus    import wordnet
from nltk.data      import find as nltk_find
from nltk.stem      import WordNetLemmatizer
from nltk.tag       import StanfordPOSTagger
from nltk.tag       import pos_tag


warnings.filterwarnings("ignore")

class PreProcessingService:
    def __init__(self):
        self.punctuation = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ ' 
        self.punc_split_regex = re_compile(r'[\s{}]+'.format(re.escape(self.punctuation)))

        self.EN_STOPWORDS = self._en_stopwords()
        # expr to find alphanumerics starting with alpha
        self.RE_AL_NUM = re.compile(r"([a-z]+)([0-9]+)")
        # expr to find alphanumerics starting with numerics
        self.RE_NUM_AL = re.compile(r"([0-9]+)([a-z]+)")
        # expr to find all combinations of alphanumerics
        self.RE_ALPHA_NUM = re_compile(r'(\w*\d+\w*)+(?<!\\)')

        self.RE_PUNCT = re.compile(r'([%s])+' % re.escape(r"""!"#$%&'()*+,-./:;<=>?@[]^_`{|}~"""), re.UNICODE)
        # remove numbers and return alpha string
        self.RE_NUMERIC = re.compile(r"[0-9]+")
        self.RE_NONALPHA = re.compile(r"\W")
        self.RE_WHITESPACE = re.compile(r"(\s)+")

        self.wordnet_lemmatizer = WordNetLemmatizer()
        self.synonyms = [
            "aluminum,alum,aluminium=>al",
                        "breaker=>brkr",
                        "barrel=>bbl",
                        "blowdown valve=>bdv",
                        "cam lock=>camlock",
                        "carbon steel,cstl=>cs",
                        "comp,cmpr,compr=>compressor",
                        "cpl,cplg=>coupling",
                        "crtg=>cartridge",
                        "csg=>casing",
                        "distributed control system=>dcs",
                        "electric=>elec",
                        "equipement,equip,eqpt=>equipment",
                        "ext=>external",
                        "flg=>flange",
                        "fltr=>filter",
                        "grade=>gr",
                        "gskt=>gasket",
                        "htr=>heater",
                        "hvac=>heating",
                        "hvac=>ventilation",
                        "hvac,air conditioning=>airconditioning",
                        "inner diameter,internal diameter,inside diameter=>id",
                        "inner ring,i.r.,i. r.=>ir",
                        "internal,int=>internal",
                        "left hand=>lh",
                        "long radius=>lr",
                        "min=>minimum",
                        "moly,mo=>molybdenum",
                        "n2=>nitrogen",
                        "nippel,nip,npl=>nipple",
                        "nomex,fire retardant clothing,fire resistant clothing=>frc",
                        "o ring,o-ring=>oring",
                        "ounce,oz=>ounce",
                        "outside diameter,outer diameter=>od",
                        "pmp=>pump",
                        "polyvinylchloride,polyvinyl chloride=>pvc",
                        "pounds per square inch guage=>psig",
                        "pressure safety valve,prv=>psv",
                        "raised face=>rf",
                        "rd,rnd=>round",
                        "reciprocating=>recip",
                        "right hand=>rh",
                        "safety relief valve,srv,safety valve=>sv",
                        "schedule=>sch",
                        "skt=>socket",
                        "smls=>seamless",
                        "socket weld=>sw",
                        "sodium hydroxide=>caustic",
                        "spiral wound,sprlw=>sw",
                        "spl=>spool",
                        "sprl=>spiral",
                        "sq=>square",
                        "standard cubic feet,ft3,cuft,cu ft,cu.ft.,cu. ft.=>scf",
                        "stsl,stainless steel,stainless,ss,304=>304ss",
                        "stsl,stainless steel,stainless,ss,309=>309ss",
                        "stsl,stainless steel,stainless,ss,316=>316ss",
                        "tbg=>tubing",
                        "thread,thrd,thd=>threaded",
                        "threads per inch=>tpi",
                        "trans,xfmr=>transformer",
                        "turbo=>turbocharger",
                        "vac=>vacuum",
                        "vlv=>valve",
                        "welding neck,welded neck,weld neck=>wn",
                        "wnd=>wound",
                        "working pressure=>wp",
                        "xmitter,trans=>transmitter",
                        "ml=>milliliter",
                        "mm,mil=>millimeter",
                        "yd=>yard",
                        "square foot,ft2,sq ft,sq. ft.=>sqft",
                        "gallon=>gal",
                        "w,w=>watt",
                        "double=>2",
                        "inches=>inch",
                        "cms,centimeter=>cm",
                        "foot,ft,feet=>feet",
                        "pound,pounds,pounds per square inch,lbs/in2,psi=>lb",
                        "diameter=>dia"
        ]
        
        

    def _en_stopwords(self):
        """
        list of stopwords
        :return: list of stopwords
        """
        custom_en_stopwords = []
        nltk_en_words = 'i me my myself we our ours ourselves you your yours yourself yourselves he him his himself she her ' \
                        'hers herself itself they them their theirs themselves what which who whom this that these ' \
                        'those am is are was were be been being have has had having do does did doing a an the and but if ' \
                        'or because as until while of at by for with about against between into through during before after ' \
                        'above below to from up down in out on off over under again further then once here there when where ' \
                        'why how all any both each few more most other some such no nor not only own same so than too very ' \
                        'can will just don should now nan available dummy not avaialble ' \
                        'recieve rcvd invoic value item itmes party none null invoice inviced quote no blank taxo code input other debit basis grir' \
                        ' card spend poc other miscellaneous goods Unbilled not recieve ' \
                        'received debit basis accr accrual accrued liabilities residual residuals cgst sgst deductible deduct noncurrent ' \
                        'manual liab exc prepaid blanket epro acc acct account'
        months = 'january february march april may june july august september ocotober november december jan feb mar apr jun jul aug sep sept oct nov ' \
                'dec febr'
        addn_stopwords = 'a about above across after afterwards again against all almost alone along already also although always am among amongst ' \
                        'amoungst amount an and another any anyhow anyone anything anyway anywhere are around as at back be became because become ' \
                        'becomes becoming been before beforehand behind being below beside besides between beyond bill both bottom but by call can ' \
                        'cannot cant co computer con could couldnt cry de describe detail do done down due during each eg eight either eleven else ' \
                        'elsewhere empty enough etc even ever every everyone everything everywhere except few fifteen fify fill find fire first five ' \
                        'for former formerly forty found four from front full further get give go had has hasnt have he hence her here hereafter ' \
                        'hereby herein hereupon hers herse" him himse" his how however hundred i it ie if in inc indeed interest into is itse" keep last ' \
                        'latter latterly least less ltd made many may me meanwhile might mill mine more moreover most mostly move much must my myse" ' \
                        'name namely neither never nevertheless next nine no nobody none noone nor not nothing now nowhere of off often on once one ' \
                        'only onto or other others otherwise our ours ourselves out over own part per perhaps pvt please put rather re same see seem ' \
                        'seemed seeming seems serious several she should show side since sincere six sixty so some somehow someone something sometime ' \
                        'sometimes somewhere still such system take ten than that the their them themselves then thence there thereafter thereby ' \
                        'therefore therein thereupon these they thick thin third this those though three through throughout thru thus to together too ' \
                        'top toward towards twelve twenty two un under until up upon us very via was we well were what whatever when whence whenever ' \
                        'where whereafter whereas whereby wherein whereupon wherever whether which while whither who whoever whole whom whose why ' \
                        'will with within without would yet you your yours yourself yourselves exclude unclassified exclude headquaters solutions'
        global_stopwords = 'sundry clearing deductible deduct refundable adjustment cogs payble payable ' \
                        'misc input intangible progress receivable receivables rcvd iso sgst exp N/A GR/IR GRIR ARIR IRAR IR/AR days period ' \
                        'accrued accrd nan ' \
                        'periods inv inventory qty quantity quantities goods good party parties third monthly month mnth wrong wrongly'

        custom_en_stopwords.extend(nltk_en_words.split(" "))
        # removing words less than length 3
        custom_en_stopwords.extend(global_stopwords.split(" "))
        custom_en_stopwords.extend(months.split(" "))
        custom_en_stopwords.extend(addn_stopwords.split(" "))
        return list(set(custom_en_stopwords))



    # note the difference between strip_* from remove_* methods
    def strip_numeric(self,s):
        """
        Remove numbers from input string 's'.
        :param s: string
        :return: new string
        """
        s = re.sub(r'\d+((?!\w)|(?<!\w))', '', s)
        return s


    def strip_punctuation(self,s):
        """
        Remove all punctuations from input string 's'.
        :param s: string
        :return: new string
        """
        s = re.sub(r'\\(?!\w*\d+\w*)', ' ', s)
        return self.RE_PUNCT.sub(" ", s)


    def remove_stopwords(self,s):
        """
        Remove all stopwords from input string 's'.
        :param s: string
        :return: new string
        """
        return " ".join(w for w in s.split() if w not in self.EN_STOPWORDS)


    def strip_multiple_whitespaces(self,s):
        """
        remove excess whitespace
        :param s: string
        :return: new string
        """
        return self.RE_WHITESPACE.sub(" ", s)


    def strip_short(self,s, minsize=2):
        """
        remove words <=2
        :param s: string
        :param minsize: minimum size of string
        :return: new string
        """
        return " ".join(e for e in s.split(' ') if len(e) >= minsize)


    def remove_alpha_num(self,s):
        """
        Remove alphanumerics from input string 's'.
        :param s: string
        :return: new string
        """
        return re.sub(r'\s(\w*\d+\w*)+(?<!\\)', "", s)


    def lemmatize(self,toks):
        """
        lemmatize the tokens of the sentence
        :param toks: list of tokens
        :return: lemmatized word list
        """
        lemmatized_words = [
            self.wordnet_lemmatizer.lemmatize(
                word, "n") for word in toks]
        return lemmatized_words


    DEFAULT_FILTERS = [lambda x: x.lower(), strip_punctuation,
                        strip_multiple_whitespaces,strip_numeric,
                        remove_stopwords, strip_short, word_tokenize]

    def preprocess_string(self,s,filters=DEFAULT_FILTERS):
        """
        Presprocess the string by applying functions present in list filters
        :param s: string
        :param filters: list of filters (default DEFAULT_FILTERS)
        :return: modified string
        """

        for f in filters:
            s = f(s)
        return ' '.join(s.split())

    def lemmatization(self,string):
        """
        default lemmatizer
        :param string:  string
        :return: modified string
        """
        wordnet_lemmatizer = WordNetLemmatizer()
        s = [wordnet_lemmatizer.lemmatize(i.lower(), "n") for i in string.split()]
        return ' '.join(s)


    def convert_synonyms(self,synonyms):
        converted_synonyms = {}
        for entry in synonyms:
            words, rhs = entry.split("=>")
            words = [word.strip() for word in words.split(",")]
            for word in words:
                converted_synonyms[word] = rhs.strip()
        return converted_synonyms


    def clean_description(self,cat_str):
        """
        Apply filer functions present in 'FILTERS' to the input string 'cat_str'
        :param cat_str: input string
        :return: preprocessed string 'preprocess_string'
        """
        FILTERS = [lambda x: str(x).lower(), self.strip_punctuation, self.strip_numeric, self.strip_short,
            self.remove_stopwords, self.lemmatization, self.strip_multiple_whitespaces, self.strip_short]
        preprocessedString=self.preprocess_string(cat_str, FILTERS)
        converted_synonyms = self.convert_synonyms(self.synonyms)
        converted_text = " ".join([converted_synonyms.get(word, word) for word in preprocessedString.split()])
        return converted_text






