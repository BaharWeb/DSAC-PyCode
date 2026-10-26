import spacy
nlp = spacy.load('en_core_web_sm')

word = "pageToken"
wordset = ['City', 'Code', 'Credits', 'RelativeHumidity', 'State', 'TempC', 'TempF', 'VisibilityMiles', 'Weather', 'WindDir', 'WindMPH']


wtoken = nlp(word)
wtoken2 = nlp('City')

print(wtoken.similarity(wtoken2))