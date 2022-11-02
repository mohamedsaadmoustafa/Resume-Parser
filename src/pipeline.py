# from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import spacy
from urlextract import URLExtract
import logging
from constants import *

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')
nltk.download('stopwords')
nltk.download('names')
nltk.download('wordnet')
nltk.download('omw-1.4')

# load pre-trained model
nlp = spacy.load('en_core_web_sm')

# logging configuration
logging.basicConfig(level=logging.INFO)


class ResumeParser(object):
    def __init__(self, text=''):
        self.text = text

    @property
    def parse(self):
        return {
            'Name': self.extract_name,
            'Email': self.extract_emails,
            'Phone': self.extract_phones,
            'Linkedin': self.extract_linkedin,
            'Links': self.extract_links,
            'Gender': self.extract_gender,
            'Zip Code': self.extract_zip_code,
            'ٍSkills': self.extract_skills,
            'Education': self.extract_education
        }

    @property
    def extract_name(self):
        logging.info('Extracting Name')
        sentences = nltk.sent_tokenize(self.text)
        sentences = [nltk.word_tokenize(sent) for sent in sentences]
        sentences = [nltk.pos_tag(sent) for sent in sentences]
        full_name = []
        for item in sentences[0]:
            # convert tuple to list
            item_list = list(item)
            # Search consecutive Proper Noun
            if 'NNP' in item_list and (item_list[0].istitle() or str(item_list[0]).isupper()):
                full_name.append(item_list[0])
        return ' '.join(full_name[:3])

    @property
    def extract_emails(self):
        logging.info('Extracting Emails')
        email = re.findall(EMAIL_REG, self.text)
        if email:
            email = ''.join(email[0])
            if self.text.find(email) and len(email):
                return email

    @property
    def extract_phones(self):
        logging.info('Extracting Phone numbers')
        phone = re.findall(PHONE_REG, self.text)
        if phone:
            number = ''.join(phone[0])
            number = number.replace(" ", "")
            if self.text.find(number) and len(number):
                return number
        return None

    @property
    def extract_linkedin(self):
        logging.info('Extracting Phone numbers')
        urls = re.findall(LINKEDON_URL_REGEX, self.text)
        return list(set(urls))[0] if urls else None

    @property
    def extract_links(self):
        logging.info('Extracting Links')
        #urls = re.findall(URL_REGEX, self.text)
        extractor = URLExtract()
        urls = extractor.find_urls(self.text)
        return list(set(urls))

    @property
    def extract_gender(self):
        logging.info('Extracting Gender')

        gender = re.findall(r'\b(gentleman|man|male|female|woman|girl)\b', self.text)  # 'fff male female')
        if gender:
            gender = gender[0]
            gender_dict = {"male": ["gentleman", "man", "male"],
                           "female": ["female", "woman", "girl"]}
            gender_aux = []
            if gender in gender_dict['male']:
                gender_aux.append('male')
            elif gender in gender_dict['female']:
                gender_aux.append('female')

            return gender_aux[0]

        else:
            return None

    @property
    def extract_zip_code(self):
        logging.info('Extracting Zip code')

        zip = re.findall(ZIP_CODE_REGEX, self.text)
        return list(set(zip))[0] if zip else None

    @property
    def extract_skills(self):
        logging.info('Extracting Skills')

        stop_words = set(nltk.corpus.stopwords.words('english'))
        word_tokens = nltk.tokenize.word_tokenize(self.text)
        # remove the stop words and remove the punctuation
        filtered_tokens = [token for token in word_tokens if token not in stop_words and token.isalpha()]
        # generate bigrams and trigrams (such as machine learning)
        bigrams_trigrams = list(
            map(' '.join, nltk.everygrams(filtered_tokens, 2, 3))
        )
        # we create a set to keep the results in.
        found_skills = set()
        # we search for each token in our skills database
        for token in filtered_tokens:
            if token.lower() in SKILLS_DB:
                found_skills.add(token)
        # we search for each bigram and trigram in our skills database
        for ngram in bigrams_trigrams:
            if ngram.lower() in SKILLS_DB:
                found_skills.add(ngram)
        return list(found_skills)

    @property
    def extract_education(self):
        logging.info('Extracting education')

        education = {}
        # Splitting on the basis of newlines
        text = [el.strip() for el in self.text.split("\n") if len(el) > 0]
        # Tokenize the individual lines
        text = [nltk.word_tokenize(el) for el in text]
        # Extract education degree
        for index, text in enumerate(text):
            for t in text:
                t = re.sub(r'[?|$|.|!|,]', r'', t)
                # Replace all special symbols
                if t.upper() in EDUCATION_DEGREES and t not in STOPWORDS:
                    text = ' '.join(text)
                    text = re.sub(r'[?|$|.|!|,]', r'', text)
                    education[t] = text
        return education
