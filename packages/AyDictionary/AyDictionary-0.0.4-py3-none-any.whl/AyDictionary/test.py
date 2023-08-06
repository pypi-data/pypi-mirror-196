try:
    from .utils import _get_soup_object
except:
    from utils import _get_soup_object
term = "flower"
data = _get_soup_object("https://www.synonym.com/synonyms/{0}".format(term))
section = data.find('div', {'data-section': 'synonyms'})
# print(section)
spans = section.findAll('a')
synonyms = [span.text.strip() for span in spans]
print(synonyms)
