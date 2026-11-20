"""The pages of the physiology supervisions site, for build/make_page.py.

index.html is the landing page: a tile for each supervision. A supervision whose work is ready has a page of its own
(supervision-N.html), made from build/template.html with the chapters of its module (build/s1.py for Supervision 1:
ALL() lists them) and its papers in exams/ (those with "week": N). A supervision that isn't ready yet opens the
workbench's guide (workbench.html: the chapters of build/chapters.py, the tour of the workbench).

To add a supervision's work: write its module of chapters (build/sN.py), its papers (exams/sN-*.json, with
"week": N), and give it an entry in READY, below, like EXAMPLE (page, module, status 'ready', the texts of its tile,
handin_paper, and handin_noun, the work to hand in as the tile's status names it: 'Essay', say); then run
python3 build/make_page.py. README.md (Adding a supervision) says more."""

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
READY = {}


def soon(n):
    """a supervision whose work isn't here yet: its tile says it is coming soon, and opens the workbench's guide"""
    return {'n': n, 'status': 'soon', 'page': GUIDE['page'], 'title': f'Supervision {n}', 'topic': '', 'card': '', 'time': ''}


assert all(sv['n'] == n and sv['status'] == 'ready' for n, sv in READY.items()), 'each entry of READY has its own number as n'
SUPERVISIONS = [READY.get(n) or soon(n) for n in range(1, max([COUNT] + list(READY)) + 1)]
