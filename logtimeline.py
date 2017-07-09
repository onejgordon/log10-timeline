from fpdf import FPDF
import json
from math import log10


DATA_FILE = "human_brain_evolution"
DATA_DIR = "data"
OUTPUT_DIR = "output"
W = 210
MARGIN = 10
X_MAX = W - MARGIN
GRID_WIDTH = 30
GRID_LABEL_WIDTH = 20
PIXEL_GRID_SIZE = 50
FULL_WIDTH_GRID = True
YA_LABEL_SIZE = 10
EVENT_LABEL_SIZE = 10
GRID_X = MARGIN + GRID_LABEL_WIDTH
EVENT_LABEL_X = GRID_X + 30
EVENT_LABEL_GAP = 3
MIN_EVENT_TEXT_GAP = 5


class LogTimeline(object):
    POWER_UNITS = {
        'bya': 9,
        'mya': 6,
        'kya': 3,
        'tya': 3,
        'hya': 2,
        'ya': 0
    }

    def __init__(self, filename):
        self.filename = filename
        self.events = []
        self.pdf = None
        self.min_ya = None
        self.max_ya = 0
        self.min_diff_ya = None
        self.last_event_bot_y = 0

    def _max_power(self):
        return int(log10(self.max_ya))

    def _min_power(self):
        return 1

    def _parse_years_ago(self, date_str):
        num, unit = date_str.lower().split(' ')
        power = self.POWER_UNITS.get(unit)
        if power is not None:
            return float(num) * (10 ** power)

    def _load_events(self):
        with open(DATA_DIR + '/' + self.filename + ".json") as f:
            data = json.load(f)
            if data:
                for event in data.get('events'):
                    date = event.get('date')
                    ya = self._parse_years_ago(date)
                    if ya:
                        event['ya'] = ya
                        if ya > self.max_ya:
                            self.max_ya = ya
                        if self.min_ya is None or ya < self.min_ya:
                            self.min_ya = ya
                        self.events.append(event)
                    else:
                        print "Invalid date - %s" % date
            self.events.sort(key=lambda e: e.get('ya'))
            return self.events

    def _ya_short(self, ya):
        power = log10(ya)
        remainder = power % 3
        even_power = power - remainder
        unit = {
            0: 'ya',
            3: 'kya',
            6: 'mya',
            9: 'bya'
        }.get(even_power, '--')
        return "%.1f %s" % (10 ** remainder, unit)

    def _text(self, x, y, text, size=None):
        self.pdf.set_font('Arial', '', size)
        self.pdf.text(x, y + size / 7, text)

    def _draw_gridline(self, ya, major=False, label=None):
        y = self._y_coord(ya)
        self.pdf.set_line_width(0.5 if major else 0.2)

        x2 = W - MARGIN if FULL_WIDTH_GRID else MARGIN + GRID_WIDTH
        self.pdf.line(MARGIN + GRID_LABEL_WIDTH, y, x2, y)
        if major and label:
            self._text(MARGIN, y, label, size=YA_LABEL_SIZE)

    def _y_coord(self, ya):
        '''
        Get y-coord of passed # of years ago
        '''
        if ya == 0:
            return MARGIN
        return PIXEL_GRID_SIZE * log10(ya) + MARGIN

    def _draw_grid(self):
        self.pdf.set_draw_color(230, 230, 230)
        self._draw_gridline(0, major=True, label="Now")
        for power in range(self._min_power(), self._max_power() + 1):
            ya_step_size = 10 ** power
            for step in range(1, 10):
                ya = step * ya_step_size
                major = step == 1
                self._draw_gridline(ya, major=major, label=self._ya_short(ya))

    def _draw_arrow(self, y, text_y):
        '''
        Draws a horizontal line, or if text_y != y (for spacing)
        draws a 3-line segment
        '''
        STAGGER_X1 = EVENT_LABEL_X - 25
        STAGGER_X2 = EVENT_LABEL_X - 5
        WH = .6
        self.pdf.rect(GRID_X - WH/2, y - WH/2, WH, WH, 'F')
        # Horiz 1
        self.pdf.line(GRID_X, y, STAGGER_X1, y)
        # Angled
        self.pdf.line(STAGGER_X1, y, STAGGER_X2, text_y)
        # Horiz 2
        self.pdf.line(STAGGER_X2, text_y, EVENT_LABEL_X, text_y)

    def _draw_event(self, e):
        ya = e.get('ya')
        title = e.get('title')
        title += " (%s)" % self._ya_short(ya)
        y = self._y_coord(ya)
        text_y = y
        prior_text_gap = text_y - self.last_event_bot_y
        if prior_text_gap < MIN_EVENT_TEXT_GAP:
            text_y += (MIN_EVENT_TEXT_GAP - prior_text_gap)
        self._draw_arrow(y, text_y)
        self._text(EVENT_LABEL_X + EVENT_LABEL_GAP, text_y, title, size=EVENT_LABEL_SIZE)
        self.last_event_bot_y = text_y

    def _draw_events(self):
        self.pdf.set_draw_color(0, 0, 0)
        self.pdf.set_font('Arial', '', EVENT_LABEL_SIZE)
        for e in self.events:
            self._draw_event(e)

    def _save(self):
        self.pdf.output('%s/%s.pdf' % (OUTPUT_DIR, self.filename), 'F')

    def generate(self):
        self._load_events()
        H = PIXEL_GRID_SIZE * (self._max_power() + 1)
        self.pdf = FPDF(format=(W, H))
        self.pdf.add_page()
        self._draw_grid()
        self._draw_events()
        self._save()

if __name__ == "__main__":
    timeline = LogTimeline(DATA_FILE)
    timeline.generate()