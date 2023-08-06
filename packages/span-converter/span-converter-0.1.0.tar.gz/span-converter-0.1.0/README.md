#Span converter

Convert a given text with spans to BIO tags.
Allows overlapping spans. 

### Installation
`pip install span-converter
`

### Get started
`
from span_converter import SpanConverter

converter=SpanConverter("pl")

result=converter.convert("tu mam tekst, kolejny już.", [{'start': 14, 'end': 21, 'label': 'uuu'}])

`
