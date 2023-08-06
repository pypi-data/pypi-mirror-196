import pandas as pd
import spacy


class SpanConverter:
    """
    Instantinate a converter of given spans to sequence of BIO.
    Allow spans to overlap. In that case it is treated as a continuation i.e no new B tag is added, just I.
    In lang is specified it works for Polish and English.
    You can specify another spacy model.

    :param lang: Languenge of text. en- English, pl-Polish,  default: en
    :type  lang: string

    :param spacy_model: specify name of spacy model that you want to use if not using Polish or English

    """

    def __init__(self, lang="en", spacy_model=None):
        self.lang = lang

        self.nlp = ""
        if self.lang == "en":
            self.nlp = spacy.load("en_core_web_sm")
        if self.lang == "pl":
            self.nlp = spacy.load("pl_core_news_sm")
        if spacy_model:
            self.nlp = spacy.load(spacy_model)

    def convert(self, text, spans):
        '''
        Convert given text into sequence of BIO tags with labels based on given spans
        If more than

        :param lang: language of text
        :type lang: string

        :param text: text that will be converted
        :type text: string

        :param spans: list of spans where single span is provided in format {start:... , end:..., label: ...}
        :type: list

        :return: seqience of BIO tags for given text
        '''

        doc = self.nlp(text)
        token_list = []
        tag = []

        for token in doc:
            token_list.append(str(token.text))
        # print(token_list)

        if len(spans) == 0:

            for j in range(0, len(token_list)):
                tag.append("O")
        else:
            start = 0
            endprev = 0  # endign of previous tag
            ann_mani = pd.DataFrame(spans)
            ann_mani = ann_mani.sort_values("start")
            token_idx = 0  # count tokend

            for j, ann in ann_mani.iterrows():
                tag_idx = 0
                token_idx = ann["start"]
                for token in self.nlp(text[start:ann["start"]].strip()):
                    tag.append("O")
                    token_idx += 1
                for token in self.nlp(text[ann["start"]:ann["end"]].strip()):
                    if start <= ann["start"]:  # if end of previous is span is earlier
                        start = ann["end"]
                        tag_idx = 0

                    else:
                        tag_idx += 1
                        token_idx += 1  # if token is before end of prev we should count it
                    if (tag_idx == 0):
                        tag.append("B-" + ann["label"])
                        token_idx += 1

                    elif endprev < token_idx:  # append new I only if prevoious tag end
                        tag.append("I-" + ann["label"])
                        token_idx += 1
                    else:
                        token_idx += 1  # count tokens inside previous tag

                    tag_idx += 1
                start = ann["end"]  # set start at the end of tag sequence
                endprev = ann["end"]

            for token in self.nlp(text[start:].strip()):
                tag.append("O")

        return tag
