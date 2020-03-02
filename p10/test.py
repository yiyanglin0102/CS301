#!/usr/bin/python

import json
import os
import sys
import re, ast, math
from collections import namedtuple, OrderedDict, defaultdict
from bs4 import BeautifulSoup
from datetime import datetime
import nbconvert
import nbformat

try:
    from lint import lint
except ImportError:
    err_msg = """Please download lint.py and place it in this directory for 
    the tests to run correctly. If you haven't yet looked at the linting module, 
    it is designed to help you improve your code so take a look at: 
    https://github.com/tylerharter/cs301-projects/tree/master/linter"""
    raise FileNotFoundError(err_msg)

ALLOWED_LINT_ERRS = {
  "W0703": "broad-except",
  "R1716": "chained-comparison",
  "E0601": "used-before-assignment",
  "W0105": "pointless-string-statement",
  "E1135": "unsupported-membership-test",
  "R1711": "useless-return",
  "W0143": "comparison-with-callable",
  "E1102": "not-callable",
  "W0107": "unnecessary-pass",
  "W0301": "unnecessary-semicolon",
  "W0404": "reimported",
  "W0101": "unreachable",
  "R1714": "consider-using-in",
  "W0311": "bad-indentation",
  "E0102": "function-redefined",
  "E0602": "undefined-variable",
  "W0104": "pointless-statement",
  "W0622": "redefined-builtin",
  "W0702": "bare-except",
  "R1703": "simplifiable-if-statement",
  "W0631": "undefined-loop-variable",
}

PASS = 'PASS'
FAIL_STDERR = 'Program produced an error - please scroll up for more details.'
FAIL_JSON = 'Expected program to print in json format. Make sure the only print statement is a print(json.dumps...)!'
EPSILON = 0.0001


TEXT_FORMAT = "text"
PNG_FORMAT = "png"
HTML_FORMAT = "html"
Question = namedtuple("Question", ["number", "weight", "format"])

questions = [
    # stage 1
    Question(number=1, weight=1, format=TEXT_FORMAT),
    Question(number=2, weight=1, format=TEXT_FORMAT),
    Question(number=3, weight=1, format=TEXT_FORMAT),
    Question(number=4, weight=1, format=TEXT_FORMAT),
    Question(number=5, weight=1, format=TEXT_FORMAT),
    Question(number=6, weight=1, format=TEXT_FORMAT),
    Question(number=7, weight=1, format=TEXT_FORMAT),
    Question(number=8, weight=1, format=HTML_FORMAT),
    Question(number=9, weight=1, format=HTML_FORMAT),
    Question(number=10, weight=1, format=TEXT_FORMAT),
    Question(number=11, weight=1, format=TEXT_FORMAT),
    Question(number=12, weight=1, format=TEXT_FORMAT),
    Question(number=13, weight=1, format=TEXT_FORMAT),
    Question(number=14, weight=1, format=TEXT_FORMAT),
    Question(number=15, weight=1, format=HTML_FORMAT),
    Question(number=16, weight=1, format=HTML_FORMAT),
    Question(number=17, weight=1, format=TEXT_FORMAT),
    Question(number=18, weight=1, format=TEXT_FORMAT),
    Question(number=19, weight=1, format=HTML_FORMAT),
    Question(number=20, weight=1, format=HTML_FORMAT),
    # stage 2
    Question(number=21, weight=1, format=HTML_FORMAT),
    Question(number=22, weight=1, format=PNG_FORMAT),
    Question(number=23, weight=1, format=HTML_FORMAT),
    Question(number=24, weight=1, format=PNG_FORMAT),
    Question(number=25, weight=1, format=HTML_FORMAT),
    Question(number=26, weight=1, format=HTML_FORMAT),
    Question(number=27, weight=1, format=PNG_FORMAT),
    Question(number=28, weight=1, format=HTML_FORMAT),
    Question(number=29, weight=1, format=PNG_FORMAT),
    Question(number=30, weight=1, format=PNG_FORMAT),
    Question(number=31, weight=1, format=HTML_FORMAT),
    Question(number=32, weight=1, format=TEXT_FORMAT),
    Question(number=33, weight=1, format=PNG_FORMAT),
    Question(number=34, weight=1, format=TEXT_FORMAT),
    Question(number=35, weight=1, format=PNG_FORMAT),
    Question(number=36, weight=1, format=PNG_FORMAT),
    Question(number=37, weight=1, format=PNG_FORMAT),
    Question(number=38, weight=1, format=PNG_FORMAT),
    Question(number=39, weight=1, format=TEXT_FORMAT),
    Question(number=40, weight=1, format=PNG_FORMAT)
]
question_nums = set([q.number for q in questions])

expected_json = {
    "1": 174,
    "2": 127170843,
    "3": ['Afghanistan',
         'Albania',
         'Algeria',
         'Anguilla',
         'Argentina',
         'Armenia',
         'Aruba',
         'Australia',
         'Austria',
         'Azerbaijan',
         'Bahrain',
         'Bangladesh',
         'Barbados',
         'Belarus',
         'Belgium',
         'Belize',
         'Benin',
         'Bermuda',
         'Bhutan',
         'Bolivia',
         'Botswana',
         'Brazil',
         'Bulgaria',
         'Burkina Faso',
         'Burundi',
         'Cambodia',
         'Cameroon',
         'Canada',
         'Cape Verde',
         'Cayman Islands',
         'Chad',
         'Chile',
         'China',
         'Colombia',
         'Comoros',
         'Costa Rica',
         'Croatia',
         'Cuba',
         'Czech Republic',
         'Denmark',
         'Djibouti',
         'Dominica',
         'Dominican Republic',
         'Ecuador',
         'Egypt',
         'El Salvador',
         'Equatorial Guinea',
         'Eritrea',
         'Estonia',
         'Ethiopia',
         'Fiji',
         'Finland',
         'France',
         'French Polynesia',
         'Gabon',
         'Georgia',
         'Germany',
         'Ghana',
         'Greece',
         'Grenada',
         'Guam',
         'Guatemala',
         'Guinea',
         'Guinea-Bissau',
         'Guyana',
         'Haiti',
         'Honduras',
         'Hungary',
         'Iceland',
         'India',
         'Indonesia',
         'Iran',
         'Iraq',
         'Ireland',
         'Israel',
         'Italy',
         'Jamaica',
         'Japan',
         'Jordan',
         'Kazakhstan',
         'Kenya',
         'Kuwait',
         'Kyrgyzstan',
         'Laos',
         'Latvia',
         'Lebanon',
         'Lesotho',
         'Liberia',
         'Libya',
         'Liechtenstein',
         'Lithuania',
         'Luxembourg',
         'Madagascar',
         'Malawi',
         'Malaysia',
         'Maldives',
         'Mali',
         'Malta',
         'Marshall Islands',
         'Mauritania',
         'Mauritius',
         'Mexico',
         'Moldova',
         'Monaco',
         'Mongolia',
         'Morocco',
         'Mozambique',
         'Namibia',
         'Nepal',
         'Netherlands',
         'New Caledonia',
         'New Zealand',
         'Nicaragua',
         'Niger',
         'Nigeria',
         'Norway',
         'Oman',
         'Pakistan',
         'Palau',
         'Panama',
         'Papua New Guinea',
         'Paraguay',
         'Peru',
         'Philippines',
         'Poland',
         'Portugal',
         'Puerto Rico',
         'Qatar',
         'Romania',
         'Russia',
         'Rwanda',
         'Saint Helena',
         'Saint Lucia',
         'Saint Vincent and the Grenadines',
         'Samoa',
         'San Marino',
         'Saudi Arabia',
         'Senegal',
         'Seychelles',
         'Sierra Leone',
         'Singapore',
         'Slovenia',
         'Somalia',
         'South Africa',
         'Spain',
         'Sri Lanka',
         'Sudan',
         'Suriname',
         'Swaziland',
         'Sweden',
         'Switzerland',
         'Syria',
         'Taiwan',
         'Tajikistan',
         'Tanzania',
         'Thailand',
         'Togo',
         'Tonga',
         'Tunisia',
         'Turkey',
         'Turkmenistan',
         'Uganda',
         'Ukraine',
         'United Arab Emirates',
         'United Kingdom',
         'United States',
         'Uruguay',
         'Uzbekistan',
         'Vanuatu',
         'Venezuela',
         'Vietnam',
         'Yemen',
         'Zambia',
         'Zimbabwe'],
    "4": "Havana",
    "5": 'Georgia',
    "6": ['New Zealand',
         'Australia',
         'Uruguay',
         'Argentina',
         'Chile',
         'Lesotho',
         'Swaziland'],
    "7": ['Iceland', 'Finland', 'Norway', 'Estonia', 'Sweden'],
    "10": 'Belarus',
    "11": 'Kazakhstan',
    "12": 'Afghanistan',
    "13": 1.433899492072933,
    "14": 6032.330932363535,
    "17": 'Vanuatu',
    "18": 'French Polynesia',
    "32": 0.3965086117752512,
    "34": 0.8786946640591312,
    "39": (1.8365703926233426e-06, 0.03916624252079352)
        }

def parse_df_html_table(html, question=None):
    soup = BeautifulSoup(html, 'html.parser')

    if question == None:
        tables = soup.find_all('table')
        assert(len(tables) == 1)
        table = tables[0]
    else:
        # find a table that looks like this:
        # <table data-question="6"> ...
        table = soup.find('table', {"data-question": str(question)})

    rows = []
    for tr in table.find_all('tr'):
        rows.append([])
        for cell in tr.find_all(['td', 'th']):
            rows[-1].append(cell.get_text())

    cells = {}
    for r in range(1, len(rows)):
        for c in range(1, len(rows[0])):
            rname = rows[r][0]
            cname = rows[0][c]
            cells[(rname,cname)] = rows[r][c]
    return cells

# find a comment something like this: #q10
def extract_question_num(cell):
    for line in cell.get('source', []):
        line = line.strip().replace(' ', '').lower()
        m = re.match(r'\#q(\d+)', line)
        if m:
            return int(m.group(1))
    return None


# rerun notebook and return parsed JSON
def rerun_notebook(orig_notebook):
    new_notebook = 'cs-301-test.ipynb'

    # re-execute it from the beginning
    with open(orig_notebook) as f:
        nb = nbformat.read(f, as_version=nbformat.NO_CONVERT)
    ep = nbconvert.preprocessors.ExecutePreprocessor(timeout=120, kernel_name='python3')
    try:
        out = ep.preprocess(nb, {'metadata': {'path': os.getcwd()}})
    except nbconvert.preprocessors.CellExecutionError:
        out = None
        msg = 'Error executing the notebook "%s".\n\n' % orig_notebook
        msg += 'See notebook "%s" for the traceback.' % new_notebook
        print(msg)
        raise
    finally:
        with open(new_notebook, mode='w', encoding='utf-8') as f:
            nbformat.write(nb, f)

    # Note: Here we are saving and reloading, this isn't needed but can help student's debug

    # parse notebook
    with open(new_notebook,encoding='utf-8') as f:
        nb = json.load(f)
    return nb

def normalize_json(orig):
    try:
        return json.dumps(json.loads(orig.strip("'")), indent=2, sort_keys=True)
    except:
        return 'not JSON'


def check_cell_text(qnum, cell):
    outputs = cell.get('outputs', [])
    if len(outputs) == 0:
        return 'no outputs in an Out[N] cell'
    actual_lines = outputs[0].get('data', {}).get('text/plain', [])
    actual = ''.join(actual_lines)
    jbn = [6,7,8,9,10,11,12,18,19,20,30]
    if qnum in jbn:
        actual = (eval(compile(ast.parse(actual, mode='eval'), '', 'eval')))
    else:
        try:
            actual = ast.literal_eval(actual)
        except Exception as e:
            print("COULD NOT PARSE THIS CELL:")
            print(actual)
            raise e
    expected = expected_json[str(qnum)]

    expected_mismatch = False

    if type(expected) != type(actual):
        return "expected an answer of type %s but found one of type %s" % (type(expected), type(actual))
    elif type(expected) == float:
        if not math.isclose(actual, expected, rel_tol=1e-02, abs_tol=1e-02):
            expected_mismatch = True
    elif type(expected) == list:
        try:
            extra = set(actual) - set(expected)
            missing = set(expected) - set(actual)
            if missing:
                return "missing %d entries list, such as: %s" % (len(missing), repr(list(missing)[0]))
            elif extra:
                return "found %d unexpected entries, such as: %s" % (len(extra), repr(list(extra)[0]))
            elif len(actual) != len(expected):
                return "expected %d entries in the list but found %d" % (len(expected), len(actual))
            else:
                for i,(a,e) in enumerate(zip(actual, expected)):
                    if a != e:
                        return "found %s at position %d but expected %s" % (str(a), i, str(e))
        except TypeError:
            if len(actual) != len(expected):
                return "expected %d entries in the list but found %d" % (len(expected), len(actual))
            for i,(a,e) in enumerate(zip(actual, expected)):
                if a != e:
                    return "found %s at position %d but expected %s" % (str(a), i, str(e))            # this happens when the list contains dicts.  Just do a simple comparison
    elif type(expected) == tuple:
        if len(expected) != len(actual):
            expected_mismatch = True
        try:
            for idx in range(len(expected)):
                if not math.isclose(actual[idx], expected[idx], rel_tol=1e-02, abs_tol=1e-02):
                    expected_mismatch = True
        except:
            expected_mismatch = True

    else:
        if expected != actual:
            expected_mismatch = True

    if expected_mismatch:
        return "found {} in cell {} but expected {}".format(actual, qnum, expected)

    return PASS

def diff_df_cells(actual_cells, expected_cells):
    for location, expected in expected_cells.items():
        location_name = "column {} at index {}".format(location[1], location[0])
        actual = actual_cells.get(location, None)
        if actual == None:
            return 'value missing for ' + location_name
        try:
            actual_float = float(actual)
            expected_float = float(expected)
            if math.isnan(actual_float) and math.isnan(expected_float):
                return PASS
            if not math.isclose(actual_float, expected_float, rel_tol=1e-02, abs_tol=1e-02):
                print(type(actual_float), actual_float)
                return "found {} in {} but it was not close to expected {}".format(actual, location_name, expected)
        except Exception as e:
            if actual != expected:
                return "found '{}' in {} but expected '{}'".format(actual, location_name, expected)
    return PASS

def check_cell_html(qnum, cell):
    outputs = cell.get('outputs', [])
    if len(outputs) == 0:
        return 'no outputs in an Out[N] cell'
    actual_lines = outputs[0].get('data', {}).get('text/html', [])
    try:
        actual_cells = parse_df_html_table(''.join(actual_lines))
    except Exception as e:
        print("ERROR!  Could not find table in notebook")
        raise e

    try:
        with open('expected.html') as f:
            expected_cells = parse_df_html_table(f.read(), qnum)
    except Exception as e:
        print("ERROR!  Could not find table in expected.html")
        raise e

    return diff_df_cells(actual_cells, expected_cells)

def check_cell_png(qnum, cell):
    if qnum == 21:
        print('here')
        print(cell)
    for output in cell.get('outputs', []):
        if qnum == 21:
            print(output.get('data', {}).keys())
        if 'image/png' in output.get('data', {}):
            return PASS
    return 'no plot found'


def check_cell(question, cell):
    print('Checking question %d' % question.number)
    if question.format == TEXT_FORMAT:
        return check_cell_text(question.number, cell)
    elif question.format == PNG_FORMAT:
        return check_cell_png(question.number, cell)
    elif question.format == HTML_FORMAT:
        return check_cell_html(question.number,cell)
    raise Exception("invalid question type")


def grade_answers(cells):
    results = {'score':0, 'tests': [], 'lint': [], "date":datetime.now().strftime("%m/%d/%Y")}

    for question in questions:
        cell = cells.get(question.number, None)
        status = "not found"

        if question.number in cells:
            # does it match the expected output?
            status = check_cell(question, cells[question.number])

        row = {"test": question.number, "result": status, "weight": question.weight}
        results['tests'].append(row)

    return results


def main():
    # rerun everything
    orig_notebook = 'main.ipynb'
    if len(sys.argv) > 2:
        print("Usage: test.py main.ipynb")
        return
    elif len(sys.argv) == 2:
        orig_notebook = sys.argv[1]

    # make sure directories are properly setup

    nb = rerun_notebook(orig_notebook)

    # extract cells that have answers
    answer_cells = {}
    for cell in nb['cells']:
        q = extract_question_num(cell)
        if q == None:
            continue
        if not q in question_nums:
            print('no question %d' % q)
            continue
        answer_cells[q] = cell

    # do grading on extracted answers and produce results.json
    results = grade_answers(answer_cells)
    passing = sum(t['weight'] for t in results['tests'] if t['result'] == PASS)
    total = sum(t['weight'] for t in results['tests'])

    lint_msgs = lint(orig_notebook, verbose=1, show=False)
    lint_msgs = filter(lambda msg: msg.msg_id in ALLOWED_LINT_ERRS, lint_msgs)
    lint_msgs = list(lint_msgs)
    results["lint"] = [str(l) for l in lint_msgs]

    functionality_score = 100.0 * passing / total
    linting_score = min(10.0, len(lint_msgs))
    results['score'] = max(functionality_score - linting_score, 0.0)

    print("\nSummary:")
    for test in results["tests"]:
        print("  Question %d: %s" % (test["test"], test["result"]))

    if len(lint_msgs) > 0:
        msg_types = defaultdict(list)
        for msg in lint_msgs:
            msg_types[msg.category].append(msg)
        print("\nLinting Summary:")
        for msg_type, msgs in msg_types.items():
            print('  ' + msg_type.title() + ' Messages:')
            for msg in msgs:
                print('    ' + str(msg))

    print('\nTOTAL SCORE: %.2f%%' % results['score'])
    with open('result.json', 'w') as f:
        f.write(json.dumps(results, indent=2))


if __name__ == '__main__':
    main()
