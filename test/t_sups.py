"""The eight supervisions' pages (supervision-1.html to supervision-8.html), as a student would use them.

For each page: its five chapters (this week, two optional exercises, the work to hand in, and revision titles), with
only the name and the work to hand in counting towards finishing it; Supervision work with that week's paper to hand
in first (no time limit, and none suggested: nothing on the page or in the paper gives a time for the work to hand in)
and its revision titles next (optional, and they can be handed in too), listed in the last chapter as in the paper;
every step that ticks itself names an event the workbench sends, every link goes somewhere, every multiple-choice
question has one right option that is marked right, and every question with a number accepts the model answer's.

Then each optional exercise, done as a student would do it, step by step, each step ticking, with the numbers in its
model answers checked against what the workbench shows: the organ bath and Guyton's model (1), the baroreflex in the
Recorder and shock in the model (2), the adrenal gland, the HPA axis and hormones in 3D (3), the lung and V/Q in R (4),
haemoglobin in 3D and in R, and the calculator (5), the renal cortex and clearance in R (6), the calculator and the
adrenal gland (7), and pH in R and the acid-base diagram (8).

Then work handed in, to a stand-in for the hand-in script (nothing reaches Google): Supervision 2's four short answers,
Supervision 8's essay, and Supervision 7's revision essays with only one of their titles written.
Run:  python3 test/t_sups.py   (screenshots in test/out/sups-*.png; R is downloaded from the internet)"""
import base64
import html as H
import io
import json
import os
import re
import time
import zipfile

from h import Page, check, done, SITE

NAME = 'Ada Lovelace'
E = 'MG.app.exam'
RC = 'MG.app.recorder'
CI = 'MG.app.circuit'
F = 'MG.app.flow'
S = 'MG.app.scope'
TEST_PW = 'the-stand-in-password'   # (the stand-in's: the real password is never in the tests)
NOTHING = []

# the events a step can tick on: what the workbench's tools send (see each tool's header)
EVENTS = {'bath:setup', 'bath:add', 'bath:response', 'bath:antagonist', 'circuit:run', 'circuit:switch', 'circuit:measure',
          'rec:open', 'rec:measure', 'scope:open', 'scope:find', 'scope:measure', 'flow:open', 'flow:run', 'viewer:loaded',
          'viewer:molecule', 'r:input', 'calc:open', 'calc:result', 'exam:start', 'exam:words', 'exam:submit', 'exam:handin',
          'exam:download'}


def read(path):
    return open(os.path.join(SITE, path), encoding='utf-8').read()


def paper(pid):
    return json.loads(read(f'exams/{pid}.json'))


class Script:
    """the hand-in script, as a stand-in: it keeps what it is sent, and answers as handin/Code.gs does"""
    def __init__(self):
        self.posts, self.replies = [], []

    def __call__(self, route):
        req = route.request
        cors = {'Access-Control-Allow-Origin': '*'}
        if req.method != 'POST':
            return route.fulfill(status=404, headers=cors, body='')
        d = json.loads(req.post_data)
        self.posts.append(d)
        if d.get('password') != TEST_PW:
            r = {'ok': False, 'error': 'password', 'message': 'That isn’t the hand-in password.'}
        else:
            r = {'ok': True, 'receipt': f"S{d['week']}-T{len(self.posts):03d}", 'file': d['file']['name'], 'folder': f"Supervision {d['week']}",
                 'time': time.strftime('%Y-%m-%dT%H:%M:%S.000Z', time.gmtime())}
        self.replies.append(r)
        route.fulfill(status=200, headers=dict(cors, **{'Content-Type': 'application/json; charset=utf-8'}), body=json.dumps(r))


SCRIPT = Script()
p = Page(width=1500, height=950)
P = p.p
p.ctx.route('https://script.google.com/**', SCRIPT)
p.ctx.route('https://script.googleusercontent.com/**', lambda r: (NOTHING.append(r.request.url), r.abort()))


# ---------------------------------------------------------------------- helpers
def click(sel):
    P.locator(sel).first.click()


def ticked(tid):
    return bool(p.js(f"() => !!(MG.tutorial && MG.tutorial.state.tasks['{tid}'])"))


def wait_ticked(tid, s=20):
    for _ in range(int(s * 4)):
        if ticked(tid):
            return True
        time.sleep(0.25)
    return False


def answered(qid):
    return bool(p.js(f"() => !!(MG.tutorial.state.answers['{qid}'] || {{}}).done"))


def chapter(cid):
    p.js(f"() => MG.app.showChapter('{cid}', true)")
    time.sleep(0.6)


def btn(where, attr, value):
    """clicks the button of a chapter with data-<attr>="<value>" """
    ok = p.js("([w, a, v]) => { const b = [...document.querySelectorAll(`#${w} button[data-${a}]`)].find(x => x.getAttribute(`data-${a}`) === v); "
              "if (!b) return false; b.scrollIntoView({block: 'center'}); b.click(); return true; }", [where, attr, value])
    check(ok, f'the chapter {where} has a button for {attr}={value}')
    time.sleep(0.3)


def mcq_right(qid):
    P.locator(f'.q[data-q="{qid}"] .mcq label[data-correct]').click()
    time.sleep(0.15)
    fb = p.js(f"() => document.querySelector('.q[data-q=\"{qid}\"] .q-feedback').textContent")
    return answered(qid) and fb.startswith('✓')


def short(qid, text):
    q = P.locator(f'.q[data-q="{qid}"]')
    q.locator('input[type=text]').fill(text)
    q.locator('button:has-text("Check")').click()
    time.sleep(0.2)
    return answered(qid)


def model(qid):
    """the text of a question's model answer"""
    return H.unescape(re.sub(r'<[^>]+>', '', p.js(f"() => document.querySelector('.q[data-q=\"{qid}\"] .q-model') ? document.querySelector('.q[data-q=\"{qid}\"] .q-model').innerHTML : ''")))


def listen():
    p.js("() => { window.__ev = []; MG.bus.on('*', (d, t) => { try { window.__ev.push([t, JSON.parse(JSON.stringify(d || {}, (k, v) => k === 'st' ? undefined : v))]); } catch (e) {} }); }")


def evs(kind, cond='true'):
    return p.js(f"() => (window.__ev || []).filter(e => e[0] === '{kind}' && (d => {cond})(e[1])).map(e => e[1])")


def no_errors(where):
    errs = [e for e in p.errors if 'ResizeObserver' not in e]
    check(not errs, f'no errors in the page ({where}): {errs[:3]}')
    p.errors.clear()


def near(a, b, tol):
    return a is not None and abs(a - b) <= tol


# the microscope
def find_click(key):
    """goes to a labelled structure of the open slide, and clicks on it, as a student would to find it"""
    p.js(f"() => {{ const L = {S}.slide.info.labels.find(l => (l.key || l.id) === '{key}'); {S}._goTo(L, 10); }}")
    time.sleep(1.5)
    pt = p.js(f"""() => {{ const L = {S}.slide.info.labels.find(l => (l.key || l.id) === '{key}');
        const s = {S}._screen(L.x, L.y), r = {S}.view.getBoundingClientRect(); return {{x: r.left + s.x, y: r.top + s.y}}; }}""")
    P.mouse.click(pt['x'], pt['y'])
    time.sleep(0.4)


def scope_find(where, slide, key, tid):
    btn(where, 'scope-find', f'{slide}:{key}')
    time.sleep(0.4)
    find_click(key)
    check(wait_ticked(tid, 5), f'finding the {key.replace("-", " ")} ticks {tid}')


def measure_drag(px=200):
    """a length measured by dragging across the middle of the view"""
    r = p.js(f"() => {{ const r = {S}.view.getBoundingClientRect(); return {{x: r.left, y: r.top, w: r.width, h: r.height}}; }}")
    x0, y0 = r['x'] + r['w'] * 0.3, r['y'] + r['h'] * 0.5
    P.mouse.move(x0, y0)
    P.mouse.down()
    for k in range(1, 11):
        P.mouse.move(x0 + px * k / 10, y0, steps=1)
    P.mouse.up()
    time.sleep(0.5)


def scope_open(where, spec, slide, tid):
    btn(where, 'scope', spec)
    p.wait(f"() => {S} && {S}.current() === '{slide}'", timeout=30000)
    check(wait_ticked(tid, 10), f'the slide {slide} opens ({tid})')


# R
def console():
    return p.js("() => { const c = MG.app.rstudio && MG.app.rstudio.cv && MG.app.rstudio.cv.out; return c ? c.textContent : ''; }")


def r_idle():
    return p.js("() => { const R = MG.app.rstudio; return R && R.S ? R.S.state : ''; }")


def run_r(where, code, wait_for=None, timeout=120):
    """clicks the show-me button that types code into the Console, and presses Enter; what R printed"""
    before = len(console())
    btn(where, 'rcon', code)
    time.sleep(0.6)
    P.keyboard.press('Enter')
    for _ in range(timeout * 4):
        time.sleep(0.25)
        out = console()[before:]
        if r_idle() == 'idle' and (wait_for is None or re.search(wait_for, out)):
            return out
    return console()[before:]


def numbers(text):
    return [float(x) for x in re.findall(r'-?\d+(?:\.\d+)?', text)]


# the calculator
def calc(expr):
    p.js("(x) => { const C = MG.Calculator; C.input.value = x; C._equals(); }", expr)
    time.sleep(0.2)
    r = evs('calc:result')
    return r[-1]['value'] if r else None


# the circuit
def el(i):
    return f"{CI}.doc.elements.find(e => e.id === '{i}')"


def meters():
    last = {}
    for e in evs('circuit:measure'):
        last[e['label']] = e['value']
    return last


def settle(label, test, s=8):
    for _ in range(int(s * 4)):
        v = meters().get(label)
        if v is not None and test(v):
            return v
        time.sleep(0.25)
    return meters().get(label)


def open_model(where, tid):
    btn(where, 'circuit', 'example:exercise-circulation')
    p.wait(f"() => {CI} && {CI}.doc && /Guyton/.test({CI}.doc.title)", timeout=30000)
    click(f'#{where} button[data-circuit-run]')
    check(wait_ticked(tid, 10), f'the model of the circulation opens and runs ({tid})')
    abp = settle('ABP', lambda v: abs(v - 93) < 0.5)
    mt = meters()
    check(near(mt.get('Cardiac output'), 83.3, 0.1) and near(mt.get('RAP'), 0, 0.1) and near(abp, 93, 0.5) and near(mt.get('MSFP'), 7, 0.01),
          f'at rest: 83.3 mL/s, RAP 0 and ABP 93 mmHg, as the step says: {mt}')


# the flow diagrams
def flow_result():
    return p.js(f"""() => {{ const r = {F}.result; return {{ finals: r.finals, max: Object.fromEntries(Object.entries(r.series).map(([k, s]) => [k, Math.max(...s)])),
        min: Object.fromEntries(Object.entries(r.series).map(([k, s]) => [k, Math.min(...s)])), times: r.times, series: r.series }}; }}""")


def at(res, node, t):
    ts = res['times']
    k = min(range(len(ts)), key=lambda j: abs(ts[j] - t))
    return res['series'][node][k]


def flow_run():
    n = len(evs('flow:run'))
    p.js(f"() => {F}.run()")
    for _ in range(40):
        time.sleep(0.25)
        if len(evs('flow:run')) > n:
            break
    p.js(f"() => {F}.stopAnim(true)")
    time.sleep(0.3)
    return flow_result()


# the recorder
def calipers(lane, ta, tb):
    n = len(evs('rec:measure'))
    y = p.js(f"(l) => {RC}._clientY(l)", lane)
    xa, xb = p.js(f"(b) => [{RC}._clientX(b[0]), {RC}._clientX(b[1])]", [ta, tb])
    P.mouse.move(xa, y)
    P.mouse.down()
    for k in range(1, 9):
        P.mouse.move(xa + (xb - xa) * k / 8, y)
    P.mouse.up()
    time.sleep(0.4)
    got = evs('rec:measure')
    if len(got) <= n:
        return None
    st = p.js(f"() => {{ const m = {RC}.measurement(); return m && m.stats; }}")
    return dict(got[-1], stats=st)


# ====================================================================== every page
HAND = {1: 's1-essay', 2: 's2-saqs', 3: 's3-essay', 4: 's4-essay', 5: 's5-saqs', 6: 's6-essay', 7: 's7-essay', 8: 's8-essay'}
OPTIONAL = {1: ('s1-endo', 's1-model'), 2: ('s2-stand', 's2-model'), 3: ('s3-hpa', 's3-mol'), 4: ('s4-lung', 's4-vq'),
            5: ('s5-hb', 's5-pft'), 6: ('s6-cortex', 's6-clear'), 7: ('s7-litre', 's7-k'), 8: ('s8-r', 's8-flow')}
TIME = re.compile(r'\b\d+\s*(minutes?|mins?|hours?)\b|time limit|timed', re.I)


def parse_auto(spec):
    out = []
    for one in spec.split('||'):
        parts = re.split(r'\s+(?=[a-zA-Z_][a-zA-Z0-9_]*[=~<>])', one.strip())
        out.append((parts[0], parts[1:]))
    return out


def open_week(n):
    p.open(f'supervision-{n}.html')
    listen()
    hand, rev = HAND[n], f's{n}-revision'
    hp, rp = paper(hand), paper(rev)
    chs = p.js("() => [...document.querySelectorAll('.chapter')].map(c => c.id)")
    check(chs == [f's{n}-week', *OPTIONAL[n], f's{n}-write', f's{n}-more'], f'Supervision {n} has its five chapters: {chs}')
    check(p.js("() => document.body.dataset.week") == str(n) and p.js("() => MG.app.currentBench") == 'exam', f'the page knows it is week {n}, and opens on Supervision work')
    check(p.js("() => document.title") == f'Supervision {n} – Physiology supervisions', f'its title: {p.js("() => document.title")}')
    # only the name and the work to hand in count
    counted = p.js("() => [...document.querySelectorAll('[data-task], .q[data-q]')].filter(x => !x.closest('.optional')).map(x => x.dataset.task || x.dataset.q)")
    check(counted[0] == f'w{n}-name' and all(c.startswith(f'es{n}-') for c in counted[1:]) and len(counted) >= 7,
          f'only the name and the work to hand in count towards finishing the page: {counted}')
    for cid in OPTIONAL[n]:
        check(p.js(f"() => !!document.querySelector('#{cid} .optional.whole')") and 'Optional, about 15 minutes' in p.js(f"() => document.querySelector('#{cid}').innerText"),
              f'{cid} says it is optional, and about 15 minutes')
    # every step's tick names an event the workbench sends; ids are unique
    autos = p.js("() => [...document.querySelectorAll('[data-task][data-auto]')].map(t => [t.dataset.task, t.dataset.auto])")
    bad = [(t, a) for t, a in autos for ev, conds in parse_auto(a) if ev not in EVENTS or any(not re.match(r'^[a-zA-Z_]\w*[=~<>].+$', c) for c in conds)]
    check(not bad, f'every step that ticks itself names an event the workbench sends: {bad}')
    ids = p.js("() => [...document.querySelectorAll('[data-task]')].map(t => t.dataset.task).concat([...document.querySelectorAll('.q[data-q]')].map(q => q.dataset.q))")
    check(len(ids) == len(set(ids)), f'every step and question has its own id: {[i for i in ids if ids.count(i) > 1]}')
    links = p.js("() => [...document.querySelectorAll('.chapter a[href]')].map(a => a.getAttribute('href'))")
    check(all(os.path.exists(os.path.join(SITE, l.split('#')[0])) for l in links if not l.startswith('http')), f'every link goes to a page of the site: {links}')
    # Supervision work: the paper to hand in first, then the revision titles
    p.wait("() => MG.app.exam && document.querySelectorAll('.ex-card').length >= 4", timeout=30000)
    cards = p.js("() => [...document.querySelectorAll('.ex-card')].filter(c => !c.closest('details')).map(c => c.dataset.paper + ':' + (c.querySelector('.ex-badge') ? c.querySelector('.ex-badge').textContent : ''))")
    check(cards[:2] == [f'{hand}:To hand in', f'{rev}:Optional'], f'this week’s paper to hand in comes first, and its revision titles next: {cards[:2]}')
    meta = p.js(f"() => document.querySelector('.ex-card[data-paper=\"{hand}\"] .ex-cmeta').textContent")
    check(meta.startswith('No time limit') and 'suggest' not in meta and 'minute' not in meta, f'the work to hand in has no time limit, and no time suggested: {meta}')
    check(hp['week'] == n and hp['required'] is True and hp.get('handIn') is True and hp['minutes'] is None and hp['suggestedMinutes'] is None,
          f'{hand}: week {n}, required, handed in, with no time limit and none suggested')
    check(rp['week'] == n and rp['required'] is False and rp.get('handIn') is True and rp['minutes'] is None and rp['suggestedMinutes'] is None,
          f'{rev}: week {n}, optional, but it can be handed in')
    words = json.dumps(hp, ensure_ascii=False)
    check(not TIME.search(H.unescape(re.sub(r'<[^>]+>', ' ', hp['instructions'] + ' '.join(q['text'] for q in hp['questions'])))),
          f'{hand}: its instructions and questions give no time')
    check('BMS' not in words, f'{hand} is this site’s own')
    # nothing gives a time for the work to hand in
    box = p.js(f"() => document.querySelector('#s{n}-week .handin-box').innerText")
    write = p.js(f"() => document.querySelector('#s{n}-write').innerText")
    hb_title = p.js(f"() => document.querySelector('#s{n}-week .handin-box .hb-title').textContent")
    first = H.unescape(re.sub(r'<[^>]+>', '', hp['questions'][0]['text'].split('<p class="muted">')[0])).strip()
    if hp['questions'][0]['type'] == 'essay':
        check(hb_title == f'“{first}”', f'This week shows the essay’s title, as in the paper: {hb_title[:80]!r}')
    check(not TIME.search(box) and 'Google Drive' in box and 'hand-in password' in box, f'the box with the work to hand in gives no time, and says how it is handed in: {box[-160:]!r}')
    check(not p.js(f"() => !!document.querySelector('#s{n}-write .pill.time')"), f'the chapter on the work to hand in has no time on it')
    plain = re.sub(r'In 20 minutes, 27%', '', write)   # (Schatzmann's experiment, in Supervision 6: not a time to write in)
    check(not TIME.search(plain), f'nor does anything in it give a time: {TIME.search(plain).group(0) if TIME.search(plain) else ""}')
    # the revision titles, as in the paper
    chapter(f's{n}-more')
    lis = p.js(f"() => [...document.querySelectorAll('#s{n}-more ol.titles li')].map(l => l.innerText.replace(/\\s+/g, ' ').trim())")
    want = [' '.join(H.unescape(re.sub(r'<[^>]+>', '', re.sub(r'<br\s*/?>|</?p>', ' ', q['text']))).split()) for q in rp['questions']]
    check(len(lis) == len(want) and all(a == b for a, b in zip(lis, want)), f'the revision titles are listed as in the paper ({len(lis)} of {len(want)})')
    # every multiple-choice question has one right option, marked right; every number is accepted
    for qid in p.js("() => [...document.querySelectorAll('.q[data-type=mcq]')].map(q => q.dataset.q)"):
        nright = p.js(f"() => document.querySelectorAll('.q[data-q=\"{qid}\"] .mcq label[data-correct]').length")
        cid = p.js(f"() => document.querySelector('.q[data-q=\"{qid}\"]').closest('.chapter').id")
        chapter(cid)
        check(nright == 1 and mcq_right(qid), f'{qid}: one right option, marked right')
    for qid, acc in p.js("() => [...document.querySelectorAll('.q[data-accept]')].map(q => [q.dataset.q, q.dataset.accept])"):
        m = re.match(r'num:(-?[\d.]+)±([\d.]+)$', acc)
        check(m is not None, f'{qid} accepts a number: {acc}')
        cid = p.js(f"() => document.querySelector('.q[data-q=\"{qid}\"]').closest('.chapter').id")
        chapter(cid)
        check(short(qid, m.group(1)), f'{qid} accepts {m.group(1)}')
    chapter(f's{n}-week')
    check(wait_ticked(f'w{n}-name', 5), f'the name ticks w{n}-name')
    no_errors(f'opening Supervision {n}')
    return hp, rp


# ====================================================================== the landing page
p.open('index.html')
p.js("() => { localStorage.clear(); sessionStorage.clear(); }")
p.open('index.html')
p.js(f"() => MG.user.setFullName('{NAME}')")

# ====================================================================== Supervision 1
open_week(1)
W = 's1-endo'
chapter(W)
check(p.js("() => MG.app.currentBench") == 'bath', 'chapter 1 opens the Organ bath')
btn(W, 'bath', 'aorta?seed=4')
p.wait("() => MG.app.bath && MG.app.bath.ready", timeout=60000)
check(wait_ticked('en-ring', 10), 'a ring of aorta with its endothelium is set up (en-ring)')
# (the student skips to the plateau after each drug, with the bath's own button or the step's)
for value, tid in (('add phenylephrine 1e-6', 'en-pe'), ('plateau', None), ('add acetylcholine 1e-6', None), ('plateau', None), ('wash', 'en-ach'),
                   ('antagonist lname 1e-4', 'en-lname'), ('wait 1200', None), ('add phenylephrine 1e-6', None), ('plateau', None),
                   ('add acetylcholine 1e-6', 'en-lname-ach'), ('plateau', None), ('add nitroprusside 1e-7', None), ('plateau', None), ('wash', 'en-snp')):
    btn(W, 'bath-do', value)
    time.sleep(1.2)
    if tid:
        check(wait_ticked(tid, 20), f'{value} ticks {tid}')
resp = {(d.get('drug'), d.get('condition', '')): d.get('pct') for d in evs('bath:response')}
ach = [v for (dr, c), v in resp.items() if dr == 'acetylcholine' and c == 'control']
achl = [v for (dr, c), v in resp.items() if dr == 'acetylcholine' and 'L-NAME' in (c or '')]
snp = [v for (dr, c), v in resp.items() if dr == 'nitroprusside']
check(ach and 75 < ach[0] < 90 and achl and 10 < achl[0] < 25 and snp and snp[0] > 90,
      f'acetylcholine relaxes it by about four-fifths, by less than a fifth in L-NAME, and nitroprusside by over 90%, as the model answer says: {resp}')
p.shot('sups-1-bath')
no_errors('the organ bath')
W = 's1-model'
chapter(W)
open_model(W, 'md-open')
p.js(f"() => {CI}.toggleSwitch({el('S2')})")
check(wait_ticked('md-muscle', 5), 'closing Exercising muscles ticks md-muscle')
abp = settle('ABP', lambda v: v < 25)
check(near(abp, 18.6, 0.3), f'ABP falls to about 19 mmHg, as the model answer says: {abp}')
p.js(f"() => {CI}.setProp({el('I1')}, 'value', 417)")
check(wait_ticked('md-heart', 5), 'a heart pumping 417 mL/s ticks md-heart')
rap = settle('RAP', lambda v: v < -20)
check(near(rap, -28, 0.3) and near(settle('ABP', lambda v: v > 90), 93, 0.5), f'ABP is back to 93 mmHg, but RAP falls to about −28: {rap}')
p.js(f"() => {CI}.setProp({el('V1')}, 'value', 17.5)")
p.js(f"() => {CI}.toggleSwitch({el('S1')})")
check(wait_ticked('md-veins', 5), 'raising MSFP and closing Muscle pump ticks md-veins')
rap = settle('RAP', lambda v: abs(v) < 0.2)
check(near(rap, 0, 0.2) and near(meters().get('Venous return'), 417, 0.5), f'417 mL/s returns with RAP back at 0: {meters()}')
p.shot('sups-1-model')
no_errors('the model of exercise')

# ====================================================================== Supervision 2
open_week(2)
W = 's2-stand'
chapter(W)
btn(W, 'rec', 'bp-standing@25,75')
p.wait(f"() => {RC} && {RC}.R && {RC}.R.id === 'bp-standing' && !{RC}._raf", timeout=30000)
check(wait_ticked('st-open', 5), 'the recording of standing up opens (st-open)')
btn(W, 'rec-tool', 'calipers')
m = calipers('BP', 32.85, 33.64)
check(m and wait_ticked('st-before', 5) and near(m['stats']['max'], 97, 2) and near(m['stats']['min'], 53, 2) and near(m['stats']['mean'], 65, 1.5),
      f'a beat before he stands: about 97/53, mean 65 (st-before): {m and m["stats"]}')
m = calipers('BP', 45.38, 45.99)
check(m and wait_ticked('st-low', 5) and near(m['stats']['max'], 84, 2) and near(m['stats']['min'], 38, 2) and near(m['stats']['mean'], 51, 1.5),
      f'a beat at the lowest pressure: about 84/38, mean 51 (st-low): {m and m["stats"]}')
bp = p.js(f"""() => {{ const R = {RC}.R, fs = R.fs, b = R.data[0]; let mx = -1e9, mn = 1e9;
    for (let i = Math.round(53 * fs); i < Math.round(60 * fs); i++) {{ mx = Math.max(mx, b[i]); }}
    for (let i = Math.round(54 * fs); i < Math.round(58 * fs); i++) {{ mn = Math.min(mn, b[i]); }} return [mx, mn]; }}""")
hr = p.js(f"() => {RC}.R.hr.map(x => [x.t, x.v])")
before = [v for t, v in hr if 30 < t < 40]
peak = max(v for t, v in hr if 41 < t < 54)
dip = min(v for t, v in hr if 54 < t < 60)
check(near(sum(before) / len(before), 77, 3) and near(peak, 105, 3) and dip < 85 and near(bp[0], 132, 5) and near(bp[1], 70, 4),
      f'his heart rate rises from about 77 to about 105, the pressure overshoots to about 130/70 and the rate falls back, as the model answer says: {sum(before) / len(before):.0f}, {peak:.0f}, {dip:.0f}, {bp}')
check('from about 77 to about 105' in p.js("() => document.querySelector('.q[data-q=\"st-q-reflex\"] .q-text').textContent") and 'about 130/70' in model('st-q-reflex'),
      'the question and its model answer have those numbers')
p.shot('sups-2-standing')
no_errors('standing up')
W = 's2-model'
chapter(W)
open_model(W, 'md-open')
p.js(f"() => {CI}.setProp({el('V1')}, 'value', 3.5)")
check(wait_ticked('md-bleed', 5), 'MSFP set to 3.5 mmHg ticks md-bleed')
check(near(settle('RAP', lambda v: v < -3), -3.5, 0.1), 'with the heart still at 83.3 mL/s, RAP is negative (−3.5 mmHg)')
p.js(f"() => {CI}.setProp({el('I1')}, 'value', 41.7)")
check(wait_ticked('md-bleed-co', 5), 'the heart at 41.7 mL/s ticks md-bleed-co')
rap, abp = settle('RAP', lambda v: abs(v) < 0.1), settle('ABP', lambda v: v < 50)
check(near(rap, 0, 0.1) and near(abp, 46.5, 0.2), f'RAP back to 0, ABP 46.5 mmHg, as the model answer says: {rap}, {abp}')
p.js(f"() => {CI}.setProp({el('V1')}, 'value', 7)")
p.js(f"() => {CI}.setProp({el('I1')}, 'value', 50)")
check(wait_ticked('md-fail', 5), 'the failing heart (50 mL/s) ticks md-fail')
rap, abp = settle('RAP', lambda v: v > 2), settle('ABP', lambda v: v > 50)
check(near(rap, 2.8, 0.1) and near(abp, 55.8, 0.2), f'RAP 2.8 and ABP 55.8 mmHg, as the model answer says: {rap}, {abp}')
p.js(f"() => {CI}.setProp({el('V1')}, 'value', 14)")
check(wait_ticked('md-fail-msfp', 5), 'MSFP raised to 14 mmHg ticks md-fail-msfp')
rap = settle('RAP', lambda v: v > 9)
check(near(rap, 9.8, 0.1) and near(meters().get('Cardiac output'), 50, 0.1), f'RAP rises to 9.8 mmHg, and the output stays at 50 mL/s: {rap}')
p.shot('sups-2-model')
no_errors('shock and failure')

# ====================================================================== Supervision 3
open_week(3)
W = 's3-hpa'
chapter(W)
scope_open(W, 'adrenal-gland@1.6,2.4,2x', 'adrenal-gland', 'hp-open')
scope_find(W, 'adrenal-gland', 'zona-fasciculata', 'hp-zf')
scope_find(W, 'adrenal-gland', 'medulla', 'hp-med')
btn(W, 'flow', 'example:hpa-axis')
p.wait(f"() => {F} && {F}.D && /adrenal/.test({F}.D.title)", timeout=30000)
btn(W, 'flow-run', '1')
check(wait_ticked('hp-run', 10), 'running the HPA axis ticks hp-run')
p.js(f"() => {F}.intervene('tg', 'knock')")
r = flow_run()
check(wait_ticked('hp-knock', 5), 'knocking out the adrenal cortex and running it again ticks hp-knock')
th_k = r['finals']['th']
p.js(f"() => {F}.intervene('tg', null)")
p.js(f"() => {F}.intervene('tg', 'fix', 3)")
r = flow_run()
th_f = r['finals']['th']
p.js(f"() => {F}.intervene('tg', null)")
check(near(th_k, 2.7, 0.06) and near(th_f, 0.17, 0.02), f'ACTH settles at about 2.7 with no cortisol, and about 0.17 with cortisol fixed at 3, as the model answer says: {th_k:.3f}, {th_f:.3f}')
p.shot('sups-3-hpa')
no_errors('the adrenal gland and the HPA axis')
W = 's3-mol'
chapter(W)
btn(W, 'pdb', '3HHR')
check(wait_ticked('mo-gh', 60), 'growth hormone with its receptors opens (mo-gh)')
btn(W, 'viewer', 'color chain')
btn(W, 'pdb', '1M2Z')
check(wait_ticked('mo-gr', 60), 'the glucocorticoid receptor opens (mo-gr)')
btn(W, 'viewer', 'show spheres DEX')
for b in p.js(f"() => [...document.querySelectorAll('#{W} button[data-viewer^=\"clear; molecule\"]')].map(x => x.dataset.viewer)"):
    btn(W, 'viewer', b)
    time.sleep(2)
check(wait_ticked('mo-cort', 60), 'cortisol and aldosterone open (mo-cort)')
p.shot('sups-3-molecules')
no_errors('hormones in 3D')

# ====================================================================== Supervision 4
open_week(4)
W = 's4-lung'
chapter(W)
scope_open(W, 'lung@2.15,1.78,2x', 'lung', 'lu-open')
for key, tid in (('bronchiole', 'lu-br'), ('airway-muscle', 'lu-sm'), ('pulmonary-artery', 'lu-pa')):
    scope_find(W, 'lung', key, tid)
btn(W, 'scope-find', 'lung:alveoli')
find_click('alveoli')
btn(W, 'scope-tool', 'measure')
measure_drag()
check(wait_ticked('lu-alv', 5), 'measuring an alveolus ticks lu-alv')
p.js(f"() => {S}.tool('pan')")
no_errors('the lung')
W = 's4-vq'
chapter(W)
codes = p.js(f"() => [...document.querySelectorAll('#{W} button[data-rcon]')].map(b => b.dataset.rcon)")
outs = [run_r(W, c, wait_for=(r'\$root|\[1\]' if 'uniroot' in c else None)) for c in codes]
for tid in ('vq-sat', 'vq-content', 'vq-curve', 'vq-units', 'vq-po2'):
    check(wait_ticked(tid, 10), f'the R step ticks {tid}')
units, mixed, po2 = numbers(outs[3]), numbers(outs[4]), numbers(outs[5])
check(len(units) >= 3 and near(units[-2], 208.5, 0.5) and near(units[-1], 168.6, 0.5) and near(mixed[-1], 188.6, 0.5) and near(po2[-1], 59.5, 0.5),
      f'R gives the contents of the two units, their mixture and its PO₂ of about 60 mmHg: {outs[3:]!r}')
txt = model('vq-q-po2')
check(all(x in txt for x in ('about 208 mL/L', '169 mL/L', 'about 189 mL/L', 'about 60 mmHg')), 'the model answer has R’s numbers')
p.shot('sups-4-vq')
no_errors('V/Q in R')

# ====================================================================== Supervision 5
open_week(5)
W = 's5-hb'
chapter(W)
btn(W, 'pdb', '4HHB')
check(wait_ticked('hb-open', 60), 'haemoglobin opens (hb-open)')
for b in ('color chain', 'show spheres HEM'):
    btn(W, 'viewer', b)
    time.sleep(1)
codes = p.js(f"() => [...document.querySelectorAll('#{W} button[data-rcon]')].map(b => b.dataset.rcon)")
outs = [run_r(W, c) for c in codes]
for tid in ('hb-sat', 'hb-content', 'hb-curve', 'hb-release'):
    check(wait_ticked(tid, 10), f'the R step ticks {tid}')
rel = numbers(outs[-1])
check(len(rel) >= 3 and near(rel[-3], 49, 2) and near(rel[-2], 25, 2) and near(rel[-1], 8, 2), f'the O₂ released at the tissues: about 49, 25 and 8 mL/L: {outs[-1]!r}')
txt = model('hb-q-co')
check(all(x in txt for x in ('49', '25', '8')), 'the model answer has the three numbers')
p.shot('sups-5-hb')
no_errors('haemoglobin')
W = 's5-pft'
chapter(W)
btn(W, 'calc', '1')
check(wait_ticked('pf-calc', 5), 'the calculator opens (pf-calc)')
for expr, tid in (('1.2/3.1', 'pf-a'), ('2.1/2.4', 'pf-b'), ('3.3/4.1', 'pf-c')):
    calc(expr)
    check(wait_ticked(tid, 5), f'{expr} ticks {tid}')
p.js("() => MG.Calculator.close()")
no_errors('lung function tests')

# ====================================================================== Supervision 6
open_week(6)
W = 's6-cortex'
chapter(W)
scope_open(W, 'kidney-cortex@2.9,1.1,4x', 'kidney-cortex', 'cx-open')
for key, tid in (('glomerulus', 'cx-glom'), ('bowmans-space', 'cx-bow'), ('pct', 'cx-pct')):
    scope_find(W, 'kidney-cortex', key, tid)
btn(W, 'scope-tool', 'measure')
measure_drag()
check(wait_ticked('cx-measure', 5), 'measuring a renal corpuscle ticks cx-measure')
p.js(f"() => {S}.tool('pan')")
check('62.5' in model('cx-q-each') and 'about 60 nL' in model('cx-q-each'), 'the model answer works out about 60 nL a minute for each glomerulus')
p.shot('sups-6-cortex')
no_errors('the renal cortex')
W = 's6-clear'
chapter(W)
codes = p.js(f"() => [...document.querySelectorAll('#{W} button[data-rcon]')].map(b => b.dataset.rcon)")
outs = [run_r(W, c) for c in codes]
for tid in ('cl-values', 'cl-p', 'cl-calc', 'cl-plot', 'cl-end'):
    check(wait_ticked(tid, 10), f'the R step ticks {tid}')
end = numbers(outs[-1])
check(len(end) >= 3 and end[-3:] == [125.0, 87.5, 133.0], f'at 10 mg/mL the clearances are 125, 87.5 and 133 mL/min, as the model answer says: {outs[-1]!r}')
check('125 (inulin), 87.5 (glucose) and 133 mL/min (PAH)' in model('cl-q-why') and '375 / 125 = 3 mg/mL' in model('cl-q-threshold'), 'the model answers have those numbers, and the threshold of 3 mg/mL')
p.shot('sups-6-clearance')
no_errors('clearance in R')

# ====================================================================== Supervision 7
open_week(7)
W = 's7-litre'
chapter(W)
btn(W, 'calc', '1')
check(wait_ticked('lt-calc', 5), 'the calculator opens (lt-calc)')
for expr, tid, want in (('40 × 300 ÷ 41', 'lt-water', 292.68), ('16 × 300 ÷ 292.68', 'lt-water-ecf', 16.4), ('1 ÷ 16 × 100', 'lt-saline', 6.25),
                        ('(40 × 300 + 1000) ÷ 41', 'lt-sea', 317.07), ('(16 × 300 + 1000) ÷ 317.07', 'lt-sea-ecf', 18.29)):
    v = calc(expr)
    check(near(v, want, 0.01) and wait_ticked(tid, 5), f'{expr} = {v} ticks {tid}')
txt = model('lt-q-sea')
check('317' in txt and '1.3 L' in txt and '2.3 L' in txt and '16.4' in model('lt-q-water'), 'the model answers have the calculator’s numbers')
p.js("() => MG.Calculator.close()")
no_errors('where a litre goes')
W = 's7-k'
chapter(W)
btn(W, 'calc', '1')
check(wait_ticked('k-calc', 5), 'the calculator opens (k-calc)')
v = calc('4.5 + 40 ÷ 16')
check(near(v, 7, 0.001) and wait_ticked('k-plasma', 5), f'4.5 + 40 ÷ 16 = {v} ticks k-plasma')
v = calc('61.5 × log(7 ÷ 150)')
v0 = calc('61.5 × log(4.5 ÷ 150)')
check(near(v, -81.9, 0.05) and near(v0, -93.7, 0.05) and wait_ticked('k-ek', 5), f'E_K is −81.9 mV at 7 mM (−93.7 at 4.5): {v}, {v0} (k-ek)')
check('−94 to −82 mV' in model('k-q-danger') and 'about 12 mV' in model('k-q-danger'), 'the model answer has the change in E_K')
p.js("() => MG.Calculator.close()")
scope_open(W, 'adrenal-gland@0.75,1.85,10x', 'adrenal-gland', 'k-open')
scope_find(W, 'adrenal-gland', 'zona-glomerulosa', 'k-zg')
p.shot('sups-7-zg')
no_errors('potassium after a meal')

# ====================================================================== Supervision 8
open_week(8)
W = 's8-r'
chapter(W)
codes = p.js(f"() => [...document.querySelectorAll('#{W} button[data-rcon]')].map(b => b.dataset.rcon)")
outs = {c: run_r(W, c) for c in codes}
for tid in ('ab-fn', 'ab-acid', 'ab-plot', 'ab-points', 'ab-alt', 'ab-mcq'):
    check(wait_ticked(tid, 10), f'the R step ticks {tid}')
o = lambda c: [round(x, 2) for x in numbers(outs[c])]
check(o('ph(24, 40)')[-1] == 7.4, f'normal values give a pH of 7.40: {outs["ph(24, 40)"]!r}')
acid = numbers(outs[[c for c in codes if c.startswith('c(closed')][0]])
check([round(x, 2) for x in acid[-3:]] == [6.2, 7.17, 7.32], f'closed 6.20, open 7.17, compensated 7.32, as the model answer says: {acid[-3:]}')
alt = numbers(outs[[c for c in codes if c.startswith('c(acute')][0]])
check([round(x, 2) for x in alt[-2:]] == [7.53, 7.45], f'at altitude 7.53, and 7.45 once the kidneys compensate: {alt[-2:]}')
check(o('ph(40, 80)')[-1] == 7.32, f'the lecture’s question: 7.32, about the 7.30 given: {outs["ph(40, 80)"]!r}')
txt = model('ab-q-open')
check(all(x in txt for x in ('6.2', '7.17', '7.32')), 'the model answer has the three pHs')
p.shot('sups-8-r')
no_errors('pH in R')
W = 's8-flow'
chapter(W)
check(p.js("() => MG.app.currentBench") == 'flow', 'chapter 2 opens Diagrams')
btn(W, 'flow', 'example:acid-base')
p.wait(f"() => {F} && {F}.D && /acid/i.test({F}.D.title)", timeout=30000)
check(wait_ticked('fl-open', 5), 'the acid–base diagram opens (fl-open)')
btn(W, 'flow-run', '1')
check(wait_ticked('fl-run', 10), 'running it ticks fl-run')
p.js(f"() => {F}.stopAnim(true)")
time.sleep(0.3)
r = flow_result()
check(near(r['max']['h'], 1.11, 0.01) and near(r['max']['vent'], 1.28, 0.01) and near(r['min']['pco2'], 0.72, 0.01) and near(at(r, 'h', 7), 1.11, 0.01),
      f'both systems: [H⁺] peaks at about 1.11 within an hour, ventilation at 1.28 and PCO₂ falls to 0.72: {r["max"]["h"]:.3f}, {r["max"]["vent"]:.3f}, {r["min"]["pco2"]:.3f}')
check(near(r['finals']['h'], 1.02, 0.01) and near(r['finals']['vent'], 1.05, 0.01) and near(r['finals']['kid'], 1.83, 0.02),
      f'and by 6 days the kidneys’ new HCO₃⁻ has nearly doubled, [H⁺] is back near 1, and ventilation too: {r["finals"]}')
p.js(f"() => {F}.setEdge('e-kid', {{ blocked: true }})")
r = flow_run()
check(wait_ticked('fl-lungs', 5), 'with the arrow to the kidneys blocked, running it ticks fl-lungs')
check(near(r['finals']['h'], 1.11, 0.01) and near(r['finals']['vent'], 1.29, 0.01) and near(r['finals']['kid'], 1, 0.001),
      f'the lungs alone: [H⁺] stays about 11% high, and ventilation about 29% up: {r["finals"]}')
p.js(f"() => {F}.setEdge('e-kid', {{ blocked: false }})")
p.js(f"() => {F}.intervene('vent', 'fix', 1)")
r = flow_run()
check(wait_ticked('fl-kidneys', 5), 'with the arrow unblocked and ventilation fixed at 1, running it ticks fl-kidneys')
check(near(r['max']['h'], 1.38, 0.01) and near(at(r, 'h', 48), 1.03, 0.01) and near(r['finals']['h'], 1.02, 0.01),
      f'the kidneys alone: [H⁺] rises by nearly 40%, and is back near normal within two days: {r["max"]["h"]:.3f}, {at(r, "h", 48):.3f}')
txt = model('fl-q-both') + model('fl-q-alone')
check('about 11%' in txt and 'nearly 40%' in txt and 'nearly twice normal' in txt, 'the model answers have those numbers')
p.js(f"() => {F}.intervene('vent', null)")
p.shot('sups-8-flow')
no_errors('the lungs and the kidneys')


# ====================================================================== handing in, to a stand-in for the hand-in script
def start_paper(n, pid, title, where=None):
    where = where or f's{n}-write'
    p.open(f'supervision-{n}.html')
    listen()
    chapter(where)
    btn(where, 'exam', pid)
    p.wait(f"() => document.querySelector('.ex-startcard h2') && document.querySelector('.ex-startcard h2').textContent === '{title}'", timeout=30000)
    sc = p.js("() => document.querySelector('.ex-startcard').innerText")
    check('No time limit' in sc and not re.search(r'\d+\s*minutes', sc) and 'Tim Hearn’s Google Drive' in sc,
          f'{title}: its first page says there is no time limit, gives no time, and says where the work goes: {sc[:160]!r}')
    click('.ex-startacts .btn.primary')
    p.wait("() => document.querySelector('.ex-area')", timeout=30000)


def write_here(text):
    p.js("(t) => { const A = document.querySelector('.ex-area'); A.focus(); document.execCommand('insertText', false, t); }", text)
    time.sleep(1.2)


def submit_and_hand_in():
    click('.ex-tile.review')
    p.wait("() => document.querySelector('.ex-submit')", timeout=10000)
    sub = p.js("() => document.querySelector('.ex-subhead').innerText")
    click('.ex-submit')
    time.sleep(0.3)
    click('.modal button:has-text("Submit now")')
    p.wait("() => document.querySelector('.ex-receipt')", timeout=10000)
    RX = '.ex-receipt .ex-hi'
    P.fill(f'{RX} .ex-hi-pw', TEST_PW)
    n = len(SCRIPT.posts)
    click(f'{RX} .ex-hi-go')
    p.wait(f"() => document.querySelector('{RX}.handed')", timeout=20000)
    time.sleep(0.3)
    d = SCRIPT.posts[n] if len(SCRIPT.posts) > n else {}
    raw = base64.b64decode((d.get('file') or {}).get('data') or '')
    doc = re.sub(r'<[^>]+>', ' ', zipfile.ZipFile(io.BytesIO(raw)).read('word/document.xml').decode('utf-8')) if raw[:2] == b'PK' else ''
    return sub, d, ' '.join(doc.split()), p.js(f"() => document.querySelector('{RX}').innerText")


# Supervision 2: four short answers
start_paper(2, 's2-saqs', 'Supervision 2 short answers')
check(wait_ticked('es2-start', 5), 'starting the short answers ticks es2-start')
ANS = ['Sinoaortic denervation: the mean pressure is unchanged, but it varies far more, because nothing buffers its changes.',
       'Haemorrhage: MSFP falls, so venous return, cardiac output and pressure fall; the baroreflex restores them within seconds.',
       'Hypoxia dilates systemic arterioles but constricts the pulmonary ones, which diverts blood from poorly ventilated lung.',
       'Heart failure: the cardiac output is low and RAP high; the body retains salt and water, which raises MSFP and causes oedema.']
for i, a in enumerate(ANS):
    if i:
        click('.ex-fab.next')
        time.sleep(0.4)
    write_here(' '.join([a] * 5))
check(wait_ticked('es2-write', 5), 'writing ticks es2-write')
sub, d, doc, rc = submit_and_hand_in()
check('You have attempted all questions in this test.' in sub, f'all four are answered: {sub[:80]!r}')
check(d.get('paper') == 's2-saqs' and d.get('week') == 2 and d.get('name') == NAME and d['file']['name'] == 'supervision-2-short-answers-ada-lovelace.docx'
      and all(a[:40] in doc for a in ANS) and 'Removing the baroreceptors' in doc and NAME in doc,
      f'the four short answers are handed in as one Word document, with the questions: {d.get("file", {}).get("name")}')
check('Handed in to Tim Hearn' in rc and wait_ticked('es2-submit', 5) and wait_ticked('es2-send', 5), 'the receipt says it has arrived, and es2-submit and es2-send tick')
p.shot('sups-2-handed-in')
no_errors('handing in the short answers')

# Supervision 8: the essay
start_paper(8, 's8-essay', 'Supervision 8 essay')
ESSAY = ('The lungs excrete twelve to fifteen moles of carbon dioxide a day and adjust ventilation within minutes, but only the kidneys '
         'can make the new bicarbonate that non-volatile acid uses up, so over days, and in renal failure, the kidneys are indispensable. ')
write_here((ESSAY * 9).strip())
check(wait_ticked('es8-write', 5), 'an essay of more than 300 words ticks es8-write')
sub, d, doc, rc = submit_and_hand_in()
check(d.get('paper') == 's8-essay' and d['file']['name'] == 'supervision-8-essay-ada-lovelace.docx' and 'Discuss the relative importance of respiratory system and kidneys' in doc
      and 'twelve to fifteen moles' in doc, f'the essay is handed in, with its title: {d.get("file", {}).get("name")}')
check(wait_ticked('es8-send', 5), 'handing it in ticks es8-send')
st = p.js("() => MG.siteStore.get('paper:s8-essay')") or {}
check(st.get('handedIn') and st.get('receipt'), 'the site remembers that it was handed in')
no_errors('handing in the essay')

# Supervision 7: the revision essays, with only one title written
start_paper(7, 's7-revision', 'Supervision 7 revision essays', 's7-more')
nq = len(paper('s7-revision')['questions'])
click('.ex-fab.next')
time.sleep(0.3)
qt = p.js("() => document.querySelector('.ex-q').innerText")
check('Discuss the regulation of the extracellular fluid volume.' in qt, f'the second title is the regulation of ECF volume: {qt[:80]!r}')
REV = 'Volume regulation is subordinate to osmoregulation: the ECF volume is set by its sodium content, which the kidney adjusts. '
write_here((REV * 4).strip())
sub, d, doc, rc = submit_and_hand_in()
check(f'You have {nq - 1} unattempted questions.' in sub, f'only one of the {nq} titles is written: {sub[:120]!r}')
check(d.get('paper') == 's7-revision' and d.get('week') == 7 and 'subordinate to osmoregulation' in doc and 'Handed in to Tim Hearn' in rc,
      f'the revision essays can be handed in with only one title written: {d.get("file", {}).get("name")}')
check(wait_ticked('m7-rev', 5), 'and submitting them ticks m7-rev (optional)')
no_errors('handing in a revision essay')

# ====================================================================== the landing page afterwards
p.open('index.html')
st = p.js("() => [...document.querySelectorAll('.tile')].map(t => t.querySelector('.tile-essay').textContent)")
check(st[1].startswith('✓ Short answers handed in') and st[7].startswith('✓ Essay handed in') and st[6] == 'Essay not started yet' and st[2] == 'Essay not started yet',
      f'the tiles say what has been handed in: {st}')
no_errors('the landing page')
check(not NOTHING, f'nothing went anywhere but the stand-in: {NOTHING}')
p.close()
done()
