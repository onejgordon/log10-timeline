from fpdf import FPDF
import json
from math import log10


DATA_FILE = "human_brain_evolution"
OUTPUT_DIR = "output"


class LogTimeline(object):

    def __init__(self, filename):
        self.filename = filename

    def generate(self):
        with open(self.filename + ".json") as f:
            data = json.loads(f)
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font('Arial', 'B', 16)
            for e in data.get('events'):
                pdf.cell(40, 10, e.get('title'))

            pdf.output('%s/%s.pdf' % (OUTPUT_DIR, self.filename), 'F')


if __name__ == "__main__":
    timeline = LogTimeline(DATA_FILE)
    timeline.generate()