"""The pages of the physiology supervisions site, for build/make_page.py.

index.html is the landing page: a tile for each supervision. A supervision whose work is ready has a page of its own
(supervision-N.html), made from build/template.html with the chapters of its module (build/s1.py for Supervision 1:
ALL() lists them) and its papers in exams/ (those with "week": N). A supervision that isn't ready yet opens the
workbench's guide (workbench.html: the chapters of build/chapters.py, the tour of the workbench).

To add a supervision's work: write its module of chapters (build/sN.py), its papers (exams/sN-*.json, with
"week": N), and give it an entry in READY, below, like EXAMPLE (page, module, status 'ready', the texts of its tile,
handin_paper, and handin_noun, the work to hand in as the tile's status names it: 'Essay', say); then run
python3 build/make_page.py. README.md (Changing or adding a supervision) says more."""

SITE_TITLE = 'Physiology supervisions'
COURSE = 'NST IB Physiology'
SUPERVISOR = 'Tim Hearn'
# the repository the site is published from, for the landing page's footer
REPOSITORY = 'https://github.com/comparativechrono/physiology-supervisions'

# how many supervisions the landing page has a tile for (each one 'soon' until its work is added)
COUNT = 8

# the workbench's guide: the tour of the tabs (build/chapters.py), for the supervisions that have no page yet
GUIDE = {
    'page': 'workbench.html', 'data_page': 'workbench', 'week': 0, 'module': 'chapters',
    'title': 'The workbench guide', 'subtitle': 'How each tab of the workbench works',
    'description': 'A guide to each tab of the physiology supervisions workbench: the microscope, 3D anatomy and '
                   'molecules, real recordings, the organ bath, diagrams and circuits you can run, simulations, supervision '
                   'work written as in the online exam, and R. Everything runs in your web browser.',
}

# What a supervision's entry looks like once its work is ready. (EXAMPLE itself isn't used: copy it into READY, below,
# and fill it in.)
EXAMPLE = {
    'n': 1, 'status': 'ready', 'page': 'supervision-1.html', 'data_page': 'supervision-1', 'module': 's1',
    'title': 'Supervision 1', 'topic': 'The topic, in a few words',
    'subtitle': 'Supervision 1: the topic, as the page’s top bar shows it',
    'description': 'One or two sentences for search engines and link previews: what the supervision covers, and what '
                   'there is to hand in.',
    'card': 'A sentence for the tile: the lectures the supervision covers.',
    'handin': 'The essay title, in full (shown when the pointer rests on the tile’s hand-in line).',
    'handin_short': 'an essay on …',
    'handin_paper': 's1-essay',
    'handin_noun': 'Essay',
    'time': 'About 40 minutes for the essay, and half an hour for the exercises',
}

# The supervisions whose work is ready, by number: {1: {...}, 2: {...}}, each like EXAMPLE.
OPTIONAL = 'Optional exercises: about half an hour'


def ready(n, topic, subtitle, description, card, handin, handin_short, paper, noun='Essay'):
    return {'n': n, 'status': 'ready', 'page': f'supervision-{n}.html', 'data_page': f'supervision-{n}', 'module': f's{n}',
            'title': f'Supervision {n}', 'topic': topic, 'subtitle': subtitle, 'description': description, 'card': card,
            'handin': handin, 'handin_short': handin_short, 'handin_paper': paper, 'handin_noun': noun, 'time': OPTIONAL}


READY = {sv['n']: sv for sv in [
    ready(1, 'Capillaries, arterioles and cardiac output',
          'Supervision 1: capillaries, arterioles and cardiac output',
          'Supervision 1 of NST IB Physiology covers capillary exchange, the control of the arterioles and what sets the '
          'cardiac output. There’s an essay to hand in, on the circulation in exercise, and optional exercises in the '
          'workbench.',
          'Capillary exchange and oedema, the arterioles and their local and systemic control, and the determinants of '
          'cardiac output.',
          'Discuss the cardiovascular adjustments that occur in whole body exercise.',
          'an essay on the cardiovascular adjustments in exercise', 's1-essay'),
    ready(2, 'Blood pressure, stress and failure',
          'Supervision 2: blood pressure, stress and failure',
          'Supervision 2 of NST IB Physiology covers the control of arterial blood pressure, the circulation in '
          'haemorrhage and hypoxia, and hypertension, heart failure and shock. There are four short answers to hand in, '
          'and optional exercises in the workbench.',
          'The control of arterial blood pressure; exercise, haemorrhage and hypoxia; and clinical cardiovascular '
          'physiology: hypertension, heart failure and shock.',
          'Four short-answer questions: removing the baroreceptors; haemorrhage; two responses to hypoxia; heart failure.',
          'four short answers, on the baroreflex, haemorrhage, hypoxia and heart failure', 's2-saqs', 'Short answers'),
    ready(3, 'Calcium, growth hormone and the adrenal gland',
          'Supervision 3: calcium, growth hormone and the adrenal gland',
          'Supervision 3 of NST IB Physiology covers calcium homeostasis, growth hormone and the IGFs, and the '
          'hypothalamic–pituitary–adrenal axis. There’s an essay to hand in, comparing growth hormone and cortisol, and '
          'optional exercises in the workbench.',
          'Calcium homeostasis (parathyroid hormone, vitamin D and calcitonin), growth hormone and the IGFs, and the '
          'hypothalamic–pituitary–adrenal axis.',
          'Compare and contrast the metabolic roles of growth hormone and cortisol.',
          'an essay comparing growth hormone and cortisol', 's3-essay'),
    ready(4, 'Lung mechanics, the pulmonary circulation and V/Q',
          'Supervision 4: lung mechanics, the pulmonary circulation and V/Q',
          'Supervision 4 of NST IB Physiology covers compliance, surfactant and airway resistance, the pulmonary '
          'circulation, and the matching of ventilation and perfusion. There’s an essay to hand in, on ventilation–'
          'perfusion matching, and optional exercises in the workbench.',
          'Compliance, surfactant and airway resistance; the pulmonary circulation and fluid in the lung; and the '
          'matching of ventilation and perfusion.',
          'Why are ventilation and perfusion not perfectly matched in the healthy lung? Discuss how the lung limits the '
          'mismatch, and when its response can do harm.',
          'an essay on matching ventilation and perfusion', 's4-essay'),
    ready(5, 'Gases in the blood, control and disease',
          'Supervision 5: gases in the blood, control and disease',
          'Supervision 5 of NST IB Physiology covers the transport of O₂ and CO₂ in the blood, the control of breathing '
          'in exercise, diving and altitude, and clinical respiratory physiology. There are four short answers to hand '
          'in, and optional exercises in the workbench.',
          'The transport of O₂ and CO₂ in the blood; the control of breathing, with exercise, diving and altitude; and '
          'lung disease.',
          'Four short-answer questions: oxygen content and saturation; carrying CO₂; breathing at altitude; two '
          'spirometry results.',
          'four short answers, on blood gases, altitude and spirometry', 's5-saqs', 'Short answers'),
    ready(6, 'Body fluids, filtration and water',
          'Supervision 6: body fluids, filtration and water',
          'Supervision 6 of NST IB Physiology covers the body’s fluid compartments, glomerular filtration and clearance, '
          'and how the kidney makes dilute or concentrated urine. There’s an essay to hand in, on the evidence for how '
          'urine is made, and optional exercises in the workbench.',
          'The body’s fluids and the structure of the kidney; filtration, its regulation and clearance; and water '
          'handling and the concentrating mechanism.',
          'What is the evidence that the kidneys produce urine by a process of ultrafiltration, followed by fluid '
          'reabsorption, involving expenditure by the tubule cells?',
          'an essay on the evidence for how urine is made', 's6-essay'),
    ready(7, 'Volume, potassium and pH',
          'Supervision 7: volume, potassium and pH',
          'Supervision 7 of NST IB Physiology covers the regulation of extracellular fluid volume, the responses to '
          'drinking, calcium, phosphate and potassium, and buffers and the renal handling of acid. There’s an essay to '
          'hand in, on drinking a litre of water, saline or seawater, and optional exercises in the workbench.',
          'The regulation of extracellular fluid volume and the responses to drinking; calcium, phosphate and '
          'potassium; and buffers and the kidney’s handling of acid.',
          'How does an adult human respond to the ingestion of one litre of (a) fresh water; (b) isotonic saline; '
          '(c) seawater?',
          'an essay on drinking a litre of fresh water, saline or seawater', 's7-essay'),
    ready(8, 'pH, the lungs and the kidneys',
          'Supervision 8: pH, the lungs and the kidneys',
          'Supervision 8 of NST IB Physiology covers acid–base balance and its disorders, and draws the respiratory and '
          'renal lectures together. There’s an essay to hand in, on the lungs and the kidneys in regulating pH, and '
          'optional exercises in the workbench.',
          'The kidney’s secretion of acid, the disorders of acid–base balance and their compensation: one lecture, and '
          'a synoptic essay that draws on the respiratory and renal lectures.',
          'Discuss the relative importance of respiratory system and kidneys in regulating plasma pH.',
          'an essay on the lungs and the kidneys in regulating pH', 's8-essay'),
]}


def soon(n):
    """a supervision whose work isn't here yet: its tile says it is coming soon, and opens the workbench's guide"""
    return {'n': n, 'status': 'soon', 'page': GUIDE['page'], 'title': f'Supervision {n}', 'topic': '', 'card': '', 'time': ''}


assert all(sv['n'] == n and sv['status'] == 'ready' for n, sv in READY.items()), 'each entry of READY has its own number as n'
SUPERVISIONS = [READY.get(n) or soon(n) for n in range(1, max([COUNT] + list(READY)) + 1)]
