"""The physiology supervisions site: the landing page (a tile for each of the eight supervisions, each opening its own
page, with its topic, the work to hand in and the optional exercises, and nothing that gives a time for the work to
hand in; the site's name, course and supervisor; a link to the workbench's guide; the student's name, shared by every
page), the guide (the site's name in its top bar, Supervision work first among the tabs) and the site's own storage
(physsup, apart from the BMS sites'); opening them sends nothing to the hand-in script. Then Supervision 1's essay,
handed in: first with no hand-in script (config.js served with none: it is written, submitted and downloaded, and
nothing asks for a password), then with the site's own hand-in script, the address in config.js (or a stand-in's, if
it has none), answered by a stand-in for the script, so that nothing reaches Google: a wrong password, then the
receipt; what is sent (the Word document is opened and checked) and that the password is kept nowhere. Given the
hand-in password as PHYS_HANDIN_PASSWORD, it checks that it is in none of the site's files.
Run:  python3 test/t_site.py   (screenshots in test/out/site-*.png)"""
import base64
import io
import json
import os
import re
import time
import zipfile

from h import Page, check, done, OUT, SITE

NAME = 'Ada Lovelace'
E = 'MG.app.exam'
TEST_PW = 'the-stand-in-password'   # (the stand-in's: the real password is never in the tests)
SCRIPT = 'https://script.google.com/macros/s/AKfycbTEST-physiology-stand-in/exec'   # (for when config.js has none)
NOTHING = []   # what was sent to Google where nothing should be


def nowhere(route):
    """stands between the pages and Google where nothing should be sent: it keeps what was, and sends nothing on"""
    NOTHING.append((route.request.method, route.request.url))
    route.abort()


def read(path):
    return open(os.path.join(SITE, path), encoding='utf-8').read()


def no_errors(p, where):
    errs = [e for e in p.errors if 'ResizeObserver' not in e]
    check(not errs, f'no errors in the page ({where}): {errs[:3]}')
    p.errors.clear()


# ---------------------------------------------------------------------- the files themselves
cfg = read('assets/js/config.js')
check("storePrefix: 'physsup'" in cfg, 'config.js: the site saves under its own prefix, physsup')
check(re.search(r"handIn: \{\s*to: 'Tim Hearn',\s*password: true,", cfg) is not None, 'config.js: work is handed in to Tim Hearn, with a password')
# (the setting itself, at the start of its line in handIn: not the comments that mention it)
SCRIPT_RX = re.compile(r"^(\s+script: )'([^']*)'", re.M)
m = SCRIPT_RX.search(cfg)
check(m is not None and 'AKfycbxeCW2Orw3iCkQb5IPVtyGfB2' not in cfg, 'config.js: the hand-in script isn’t the BMS supervisions’ one')
LIVE = m.group(2) if m else ''
check(LIVE == '' or re.match(r'https://script\.google\.com/macros/s/[\w-]+/exec$', LIVE), f'config.js: the hand-in script is a web app of Apps Script, or not set ({LIVE[:50] or "not set"})')
cfg_none = SCRIPT_RX.sub(r"\1''", cfg)   # (config.js with no hand-in script)
for f in ('index.html', 'workbench.html'):
    t = read(f)
    check('BMS supervisions' not in t and 'bmssup' not in t and 'BMS-supervisions' not in t, f'{f} names nothing of the BMS supervisions')
PW = os.environ.get('PHYS_HANDIN_PASSWORD')
if PW:
    found = []
    for dirpath, dirs, files in os.walk(SITE):
        dirs[:] = [d for d in dirs if d not in ('.git', 'out', '__pycache__', 'slides', 'anatomy', 'sims', 'recordings', 'molecules')]
        for f in files:
            try:
                if PW in open(os.path.join(dirpath, f), encoding='utf-8', errors='ignore').read():
                    found.append(os.path.relpath(os.path.join(dirpath, f), SITE))
            except OSError:
                pass
    check(not found, f'the hand-in password is in none of the site’s files: {found}')

# ---------------------------------------------------------------------- Supervision 1's essay
ESSAY = ('In whole-body exercise the cardiac output rises about five-fold, because central command and the reset baroreflex '
         'raise the heart rate and contractility, while the dilated muscle arterioles and the muscle pump raise venous return. ')
EXTRA = {}


def write_and_submit(p, P):
    """opens the paper on the stand-in page, writes the essay and submits it"""
    p.js(f"() => {E}.openPaper('s1-essay')")
    p.wait("() => document.querySelector('.ex-startcard h2') && document.querySelector('.ex-startcard h2').textContent === 'Supervision 1 essay'", timeout=30000)
    sc = p.js("() => document.querySelector('.ex-startcard').innerText")
    P.locator('.ex-startacts .btn.primary').first.click()
    p.wait("() => document.querySelector('.ex-area')", timeout=30000)
    p.js("(t) => { const A = document.querySelector('.ex-area'); A.focus(); document.execCommand('insertText', false, t); }", (ESSAY * 4).strip())
    time.sleep(1.2)
    P.locator('.ex-tile.review').click()
    p.wait("() => document.querySelector('.ex-submit')", timeout=10000)
    P.locator('.ex-submit').click()
    time.sleep(0.3)
    mt = p.js("() => document.querySelector('.modal') ? document.querySelector('.modal').innerText : ''")
    P.locator('.modal button:has-text("Submit now")').click()
    p.wait("() => document.querySelector('.ex-receipt')", timeout=10000)
    time.sleep(0.3)
    return sc, mt


def docx_text(raw):
    return re.sub(r'<[^>]+>', '', zipfile.ZipFile(io.BytesIO(raw)).read('word/document.xml').decode('utf-8'))


# ====================================================================== the landing page
p = Page(width=1440, height=900, extra=EXTRA)
P = p.p
p.ctx.route('https://script.google.com/**', nowhere)
p.ctx.route('https://script.googleusercontent.com/**', nowhere)
p.open('index.html')
p.js("() => { localStorage.clear(); sessionStorage.clear(); }")
p.open('index.html')
check(p.js("() => document.title") == 'Physiology supervisions – NST IB Physiology', f'the title: {p.js("() => document.title")}')
check(p.js("() => document.querySelector('.hero h1').textContent") == 'Physiology supervisions'
      and p.js("() => document.querySelector('.hero-course').textContent") == 'NST IB Physiology · supervisions with Tim Hearn',
      'the landing page names the site, the course and the supervisor')
tiles = p.js("""() => [...document.querySelectorAll('.tiles .tile')].map(t => ({ n: t.dataset.sup, href: t.getAttribute('href'), ready: t.classList.contains('ready'),
    soon: t.classList.contains('soon'), kicker: t.querySelector('.tile-kicker').textContent, text: t.innerText }))""")
check([t['kicker'] for t in tiles] == [f'Supervision {i}' for i in range(1, 9)], f'eight tiles, Supervision 1 to 8: {[t["kicker"] for t in tiles]}')
check(all(t['ready'] and not t['soon'] and t['href'] == f'supervision-{i}.html' for i, t in enumerate(tiles, 1)), 'each opens its own supervision’s page')
TOPICS = ['Capillaries, arterioles and cardiac output', 'Blood pressure, stress and failure', 'Calcium, growth hormone and the adrenal gland',
          'Lung mechanics, the pulmonary circulation and V/Q', 'Gases in the blood, control and disease', 'Body fluids, filtration and water',
          'Volume, potassium and pH', 'pH, the lungs and the kidneys']
check(all(TOPICS[i] in t['text'] and 'To hand in:' in t['text'] and 'Optional exercises: about half an hour' in t['text'] for i, t in enumerate(tiles)),
      'each names its topic, the work to hand in, and about half an hour of optional exercises')
status = p.js("() => [...document.querySelectorAll('.tile .tile-essay')].map(x => x.textContent)")
check(status == ['Essay not started yet', 'Short answers not started yet', 'Essay not started yet', 'Essay not started yet', 'Short answers not started yet',
                 'Essay not started yet', 'Essay not started yet', 'Essay not started yet'], f'nothing is started: essays, and short answers in weeks 2 and 5: {status}')
handins = p.js("() => [...document.querySelectorAll('.tile-handin')].map(x => x.textContent + ' ' + x.title)")
check(not any(re.search(r'\b\d+\s*minutes?\b|time limit', h, re.I) for h in handins), 'no tile gives a time for the work to hand in')
check('Discuss the cardiovascular adjustments that occur in whole body exercise.' in handins[0], 'Supervision 1’s essay is the title given for it')
check(p.js("() => [...document.querySelectorAll('.land-info a')].map(a => a.getAttribute('href'))") == ['workbench.html'], 'the landing page links to the workbench’s guide')
foot = p.js("() => [...document.querySelectorAll('.land-foot a')].map(a => a.getAttribute('href'))")
check(foot == ['https://github.com/comparativechrono/BMS-workbench', 'https://github.com/comparativechrono/physiology-supervisions'],
      f'the footer links to the BMS workbench and to this repository: {foot}')
fav = p.js("() => decodeURIComponent(document.querySelector('link[rel=icon]').href)")
check('#13304a' in fav and '#ff8a65' in fav, 'the icon is the site’s own (navy, with a trace of the ECG)')
hero = p.js("() => getComputedStyle(document.querySelector('.hero')).backgroundImage")
check('rgb(21, 53, 79)' in hero, f'the header is the site’s navy, not the BMS plum: {hero[:60]}')
check(p.js("() => document.querySelector('[data-student-name-text]').textContent") == 'no name yet', 'there is no name yet')
p.shot('site-landing', full=True)
P.locator('[data-name-btn]').click()
P.fill('#studentNameIn', NAME)
P.locator('.user-form button[type=submit]').click()
time.sleep(0.3)
check(p.js("() => document.querySelector('[data-student-name-text]').textContent") == NAME and p.js("() => MG.user.fullName()") == NAME,
      'the name given on the landing page is shown')
keys = p.js("() => Object.keys(localStorage)")
check(keys and all(k.startswith('physsup:') for k in keys) and 'physsup:fullName' in keys, f'everything is saved under the site’s prefix: {keys}')
no_errors(p, 'the landing page')

# ====================================================================== the guide
P.locator('.land-info a[href="workbench.html"]').click()
P.wait_for_url('**/workbench.html', timeout=30000)
p.wait("() => window.MG_READY === true", timeout=60000)
check(p.js("() => location.pathname").endswith('/workbench.html'), 'the link opens the guide')
check(p.js("() => document.querySelector('.brand-title').textContent") == 'Physiology supervisions'
      and p.js("() => document.querySelector('.brand').getAttribute('href')") == 'index.html', 'the top bar names the site, and goes back to the landing page')
check(p.js("() => document.title") == 'The workbench guide – Physiology supervisions', f'the guide’s title: {p.js("() => document.title")}')
check(p.js("() => window.BMS_PAGE && window.BMS_PAGE.site") == 'Physiology supervisions', 'the page knows the site’s name')
tabs = p.js("() => [...document.querySelectorAll('.wb-tab[data-wb]')].map(t => t.dataset.wb + ':' + t.querySelector('.lbl').textContent.trim())")
check(tabs[0] == 'exam:Supervision work' and len(tabs) == 11, f'eleven tabs, Supervision work first: {tabs[:2]}')
check(p.js("() => document.querySelector('.user-name').textContent") == NAME, 'the guide shows the name given on the landing page')
top = p.js("() => getComputedStyle(document.querySelector('.topbar')).backgroundColor")
check(top == 'rgb(19, 48, 74)', f'the top bar is the site’s navy: {top}')
chs = p.js("() => document.querySelectorAll('.chapter').length")
check(chs == 12, f'the guide has its twelve chapters: {chs}')
p.shot('site-guide')
no_errors(p, 'the guide')
check(not NOTHING, f'opening the landing page and the guide sends nothing to the hand-in script: {NOTHING}')
p.close()

# ====================================================================== a paper to hand in, with no hand-in script
# (as when config.js has none: what students are told, and that they can still download their work)
p = Page(width=1440, height=900, extra=dict(EXTRA, **{'assets/js/config.js': (cfg_none, 'text/javascript')}))
P = p.p
p.ctx.route('https://script.google.com/**', nowhere)
p.ctx.route('https://script.googleusercontent.com/**', nowhere)
p.open('supervision-1.html')
p.js(f"() => MG.user.setFullName('{NAME}')")
p.js("() => MG.app.showWorkbench('exam')")
p.wait(f"() => {E} && document.querySelectorAll('.ex-card').length >= 4", timeout=30000)
cards = p.js("() => [...document.querySelectorAll('.ex-card')].map(c => c.dataset.paper + ':' + (c.querySelector('.ex-badge') ? c.querySelector('.ex-badge').textContent : ''))")
check(cards[:2] == ['s1-essay:To hand in', 's1-revision:Optional'], f'on Supervision 1’s page its essay comes first, then its revision titles: {cards[:2]}')
p.shot('site-papers')
home = p.js("() => document.querySelector('.ex-home').innerText")
check('then download it as a Word document and send it to your supervisor' in home and 'password' not in home and 'Google Drive' not in home,
      f'with no hand-in script yet, Supervision work says to download the work and send it (no password, no Drive): {home[:200]!r}')
sc, mt = write_and_submit(p, P)
check('password' not in sc.lower() and 'No time limit' in sc and not re.search(r'\\d+\\s*minutes', sc), 'the essay’s first page asks for no password, and gives no time')
check('hand it in on the next page' not in mt, f'submitting doesn’t promise a hand-in: {mt[-100:]!r}')
rc = p.js("() => document.querySelector('.ex-receipt').innerText")
check(not p.js("() => !!document.querySelector('.ex-receipt .ex-hi')") and 'Nothing has been sent anywhere. To hand your work in, download it and send it yourself.' in rc,
      'the receipt has no hand-in box: it says that nothing was sent, and to download the work')
with P.expect_download() as dl:
    P.locator('.ex-recacts .btn:has-text("Download submission")').click()
    P.locator('.popmenu button:has-text("Word document")').click()
raw = open(dl.value.path(), 'rb').read()
check(dl.value.suggested_filename == 'supervision-1-essay-ada-lovelace.docx' and NAME in docx_text(raw) and 'muscle pump' in docx_text(raw),
      f'the Word document has the student’s name and the essay: {dl.value.suggested_filename}')
st = p.js("() => MG.siteStore.get('paper:s1-essay')") or {}
check(st.get('started') and st.get('submitted') and st.get('downloaded') and not st.get('handedIn'), f'the site remembers what was done with it: {sorted(st)}')
p.shot('site-receipt-no-script')
no_errors(p, 'a paper to hand in, with no hand-in script')
check(not NOTHING, f'with no hand-in script, nothing is sent to Google: {NOTHING}')
p.close()

# ====================================================================== with the site's hand-in script
# (its address in config.js – or, if it has none, a stand-in's – answered by a stand-in for the script, so that nothing
# reaches Google: the tests hand nothing in)
URL = LIVE or SCRIPT
cfg_test = SCRIPT_RX.sub(lambda x: x.group(1) + "'" + SCRIPT + "'", cfg)
assert SCRIPT in cfg_test and len(SCRIPT_RX.findall(cfg)) == 1 and SCRIPT_RX.search(cfg_none).group(2) == ''


class Script:
    """the hand-in script, as a stand-in: it keeps what it is sent, and answers as handin/Code.gs does"""
    def __init__(self, url):
        self.url, self.calls, self.posts, self.replies, self.files = url, [], [], [], []

    def __call__(self, route):
        req = route.request
        self.calls.append((req.method, req.url))
        cors = {'Access-Control-Allow-Origin': '*'}
        if req.method != 'POST' or req.url != self.url:
            return route.fulfill(status=404, headers=cors, body='')
        d = json.loads(req.post_data)
        self.posts.append((req.headers, d))
        if d.get('password') != TEST_PW:
            r = {'ok': False, 'error': 'password', 'message': 'That isn’t the hand-in password.'}
        else:
            self.files.append(d['file']['name'])
            r = {'ok': True, 'receipt': f"S{d['week']}-Xy7Q{len(self.files):02d}", 'file': d['file']['name'], 'folder': f"Supervision {d['week']}",
                 'time': time.strftime('%Y-%m-%dT%H:%M:%S.000Z', time.gmtime())}
        self.replies.append(r)
        route.fulfill(status=200, headers=dict(cors, **{'Content-Type': 'application/json; charset=utf-8'}), body=json.dumps(r))


p = Page(width=1440, height=900, extra=EXTRA if LIVE else dict(EXTRA, **{'assets/js/config.js': (cfg_test, 'text/javascript')}))
P = p.p
S = Script(URL)
p.ctx.route('https://script.google.com/**', S)
p.ctx.route('https://script.googleusercontent.com/**', lambda r: r.abort())
p.open('supervision-1.html')
p.js(f"() => MG.user.setFullName('{NAME}')")
p.js("() => MG.app.showWorkbench('exam')")
p.wait(f"() => {E} && document.querySelectorAll('.ex-card').length >= 4", timeout=30000)
p.js(f"() => {E}.home()")
time.sleep(0.5)
home = p.js("() => document.querySelector('.ex-home').innerText")
check('then hand it in from its page. It goes straight to Tim Hearn’s Google Drive.' in home, f'with a hand-in script, Supervision work says the work goes straight to Tim Hearn’s Google Drive: {home[:200]!r}')
sc, mt = write_and_submit(p, P)
check('Then you hand it in on the next page, and it goes straight to Tim Hearn’s Google Drive.' in mt, f'Submit says how it will be handed in: {mt[-110:]!r}')
RX = '.ex-receipt .ex-hi'
hb = p.js(f"() => document.querySelector('{RX}') ? document.querySelector('{RX}').innerText : ''")
check('Now hand it in' in hb and 'Your essay goes straight from here to Tim Hearn’s Google Drive. Type in the hand-in password you were given, then press Hand it in.' in hb,
      f'the receipt hands the essay in from here, with the hand-in password: {hb[:200]!r}')


def send(pw):
    P.fill(f'{RX} .ex-hi-pw', pw)
    p.js(f"() => {{ document.querySelector('{RX} .ex-hi-msg').textContent = ''; }}")
    P.locator(f'{RX} .ex-hi-go').click()
    p.wait(f"""() => {{ const g = document.querySelector('{RX} .ex-hi-go'), m = document.querySelector('{RX} .ex-hi-msg');
        return !g || (!g.disabled && m && m.textContent && !/^Sending/.test(m.textContent)); }}""", timeout=20000)
    return p.js(f"() => document.querySelector('{RX} .ex-hi-msg') ? document.querySelector('{RX} .ex-hi-msg').textContent : ''")


p.shot('site-handin-box')
msg = send('a wrong password')
check(msg == 'That isn’t the right hand-in password. Check it with Tim Hearn and try again.' and len(S.posts) == 1, f'a wrong password is refused: {msg!r}')
send(TEST_PW)
p.wait(f"() => document.querySelector('{RX}.handed')", timeout=20000)
hdr, d = S.posts[-1]
R = S.replies[-1]
check(R.get('ok') and all(mth == 'POST' and u == URL for mth, u in S.calls) and hdr.get('content-type', '').startswith('text/plain'),
      f'the right password: it is sent to the hand-in script ({"the site’s own, in config.js" if LIVE else "a stand-in’s"}), as a POST of text (no preflight)')
check(d.get('paper') == 's1-essay' and d.get('week') == 1 and d.get('name') == NAME and d.get('site') == p.base + 'supervision-1.html' and d.get('words', 0) > 100,
      f'with the paper, its supervision, the student, the words and this site’s page: { {k: v for k, v in d.items() if k not in ("file", "password")} }')
raw = base64.b64decode((d.get('file') or {}).get('data') or '')
check(d['file'].get('name') == 'supervision-1-essay-ada-lovelace.docx' and raw[:2] == b'PK' and NAME in docx_text(raw) and 'muscle pump' in docx_text(raw),
      'and the Word document, with the student’s name and the essay')
time.sleep(0.3)
done_text = p.js(f"() => document.querySelector('{RX}').innerText")
check('Handed in to Tim Hearn' in done_text and f'Your receipt number is {R["receipt"]}.' in done_text and 'in the folder Supervision 1' in done_text,
      f'the receipt says it has arrived: {done_text[:160]!r}')
st = p.js("() => MG.siteStore.get('paper:s1-essay')") or {}
check(st.get('handedIn') == R['time'] and st.get('receipt') == R['receipt'], 'the site remembers that it was handed in, with the receipt')
kept = p.js("""async () => { const E = MG.app.exam; let t = JSON.stringify(Object.assign({}, localStorage)) + JSON.stringify(Object.assign({}, sessionStorage));
    for (const f of E._attemptFiles()) t += await E.fs.readText(f); return t; }""")
check(len(kept) > 500 and TEST_PW not in kept and 'a wrong password' not in kept, 'the password is kept nowhere: not in the browser’s storage, nor with the essay')
page = p.js(f"() => {E}.exportDocument({E}.att)")
check('Supervision 1, Physiology supervisions.' in page and 'BMS' not in page, 'the web page of the submission names this site')
p.shot('site-handed-in')
no_errors(p, 'handing in')
p.close()

# ====================================================================== on a phone
m = Page(width=390, height=844, mobile=True)
m.ctx.route('https://script.google.com/**', nowhere)
m.ctx.route('https://script.googleusercontent.com/**', nowhere)
m.open('index.html')
cols = m.js("() => getComputedStyle(document.querySelector('.tiles')).gridTemplateColumns.split(' ').length")
wide = m.js("() => document.documentElement.scrollWidth <= innerWidth + 1")
check(cols == 1 and wide, f'on a phone, the tiles are in one column and nothing is wider than the screen ({cols} column)')
m.shot('site-landing-phone')
no_errors(m, 'the landing page on a phone')
check(not NOTHING, f'nothing was sent to Google where nothing should be: {NOTHING}')
m.close()
done()
