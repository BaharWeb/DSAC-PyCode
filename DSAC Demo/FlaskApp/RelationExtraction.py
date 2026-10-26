import spacy

# Load the spaCy English model
nlp = spacy.load("en_core_web_sm")


def extract_relations(text):
    doc = nlp(text)

    relations = []

    # Iterate over the sentences in the document
    for sent in doc.sents:
        # Identify named entities
        entities = [(ent.text, ent.label_) for ent in sent.ents]
        print(f"Entities found: {entities}")  # Debug: show found entities

        # Iterate over the tokens in the sentence to find relations
        for token in sent:
            # Check if the token is a verb (potential relation)
            if token.dep_ == 'ROOT':  # We are mainly interested in the main verb
                # Find subjects related to the verb
                subject = [w for w in token.subtree if w.dep_ == 'nsubj']
                # Find direct objects related to the verb
                obj = [w for w in token.subtree if w.dep_ == 'dobj']

                # Debug: show found subjects and objects
                print(f"Token: {token.text}, Subjects: {[s.text for s in subject]}, Objects: {[o.text for o in obj]}")

                # Create relations based on found entities
                for subj in subject:
                    # Check for matching named entities
                    entity1 = next((ent[0] for ent in entities if ent[0] == subj.text), None)
                    # If no entity found, check if it's a common noun
                    if entity1 is None:
                        entity1 = subj.text  # Fallback to the noun itself
                        print(f"No matching entity found for subject: {subj.text}. Using common noun instead.")

                    for ob in obj:
                        entity2 = next((ent[0] for ent in entities if ent[0] == ob.text), None)
                        # If no entity found, check if it's a common noun
                        if entity2 is None:
                            entity2 = ob.text  # Fallback to the noun itself
                            print(f"No matching entity found for object: {ob.text}. Using common noun instead.")

                        # Add the relation if both entities are found
                        relations.append((entity1, token.lemma_, entity2))
                        print(f"Relation found: {entity1} {token.lemma_} {entity2}")  # Debug: show found relation

    return relations


# Example usage
#text = "Alice gave a presentation at the conference. The speaker discussed important trends in Web Engineering."
text = "semantic web is a web engineering topic. This conference has sessions on semantic web"
relations = extract_relations(text)
print("Extracted Relations:")
print(relations)
