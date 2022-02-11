import sys
from os.path import abspath, dirname, join

paths = [
    abspath(join(dirname(dirname(__file__)), "src/jizt/summaries")),
    abspath(join(dirname(dirname(__file__)),
                 "pipeline/text_processing")),
    abspath(join(dirname(dirname(__file__)),
                 "pipeline/text_encoding")),
    abspath(join(dirname(dirname(__file__)),
                 "pipeline/text_summarization"))
]

for p in paths:
    sys.path.insert(1, p)
