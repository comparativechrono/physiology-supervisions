"""What the physiology supervisions' pages share (build/s1.py to s8.py use it): the box with the work to hand in, the
week's plan, optional chapters and parts, the steps of writing and handing in, and the chapter of revision titles,
read from the supervision's papers in exams/ (so that a title is written in one place only: its paper).

The supervisions are written in Tim Hearn's voice, in the first person ("the hand-in password I give you"). Nothing
here, or in any supervision, tells students how long to spend on the work they hand in: the papers to hand in have no
time limit and suggest no time."""
import json
import os
import re

from lib import activity, callout, exam, goto, task

EXAMS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'exams')


def paper(pid):
    """a paper of Supervision work (exams/<pid>.json)"""
    with open(os.path.join(EXAMS, pid + '.json'), encoding='utf-8') as f:
        return json.load(f)


def titles(pid):
    """the titles (the questions) of a paper, as HTML without their paragraphs, in order"""
    out = []
    for q in paper(pid)['questions']:
        if q.get('type') == 'info':
            continue
        t = re.sub(r'<p class="muted">.*?</p>', '', q['text'], flags=re.S)
        out.append(re.sub(r'</?p>', ' ', t).strip())
    return out


HANDIN_LINE = ('Once you’ve submitted it, <b>hand it in</b> from the same page before your supervision. You’ll need the '
               '<b>hand-in password</b> I give you, and your work then goes straight into my Google Drive.')

HAND_NOTE = callout('info', 'Handing in', '<p>Your work goes straight from this page into my Google Drive, and you don’t '
                    'need a Google account for that. The hand-in password I give you stops anyone else from handing work '
                    'in, so please keep it to yourself. Once it has arrived, the page tells you so and gives you a receipt. '
                    'If it can’t be handed in, the page will tell you why. If you try again and it still won’t go, '
                    'download a copy and send it to me some other way.</p>')


def handin_box(n, pid, title, points, go_to, noun='essay'):
    """the work to hand in, as the first thing the student sees: its title, a few points about it, and buttons"""
    lis = ''.join(f'<li>{x}</li>' for x in list(points) + [HANDIN_LINE])
    return f'''<div class="handin-box">
  <div class="hb-k">To hand in this week</div>
  <p class="hb-title">{title}</p>
  <ul>{lis}</ul>
  <p class="hb-acts">{goto(go_to, "how to write it and hand it in")} {exam(pid, "open the " + noun)}</p>
</div>'''


def optional(body, title='If you have time', hid=None):
    i = f' id="{hid}"' if hid else ''
    return f'<div class="optional">\n<h2{i}>{title}</h2>\n{body}\n</div>'


def optional_chapter(body):
    """a whole chapter that's optional: none of its steps or questions count towards finishing the page"""
    return f'<div class="optional whole">\n{body}\n</div>'


def optional_note(minutes, lectures):
    """the box at the top of an optional exercise"""
    return callout('info', f'Optional, about {minutes} minutes', f'<p>This exercise isn’t part of the work to hand in, and '
                   f'its steps don’t count towards finishing the page. It goes with {lectures}.</p>')


def name_step(n):
    return activity('Before you start', [
        task(f'w{n}-name', 'Check that your name is at the top of the page. If it says <b>Your name</b>, click it and add '
             'yours. It goes at the top of the work you hand in, and every supervision’s page shares it.', check='named'),
    ])


def how_page_works(optional_chapters):
    return f'''<h2>How this page works</h2>
<ul>
<li>The steps tick themselves off as you do them, the buttons do things for you in the workbench on the right, and every question has a <b>model answer</b> you can look at once you’ve had a go.</li>
<li>{optional_chapters} optional, so their steps don’t count towards finishing the page. The rest do.</li>
<li>If you haven’t used one of the workbench’s tabs before, the <a href="workbench.html" target="_blank" rel="noopener">workbench guide</a> shows you how it works.</li>
</ul>'''


def write_steps(n, pid, write_text, noun='essay', words=299):
    """the steps of writing a paper to hand in, submitting it, handing it in and keeping a copy"""
    return activity('Write it, and hand it in', [
        task(f'es{n}-start', f'Open the {noun} {exam(pid, "show me")}, read its first page, and press <b>Start</b> when '
             'you’re ready to write.', auto=f'exam:start paper={pid}', check=f'paper:{pid}.started'),
        task(f'es{n}-write', write_text, auto=f'exam:words paper={pid} words>{words}'),
        task(f'es{n}-submit', 'When you’ve finished, go to the submission page (the ✓ tile at the bottom right), check '
             'your work and submit it.', auto=f'exam:submit paper={pid}', check=f'paper:{pid}.submitted'),
        task(f'es{n}-send', 'Hand it in on the page that comes up next. Type in the hand-in password and press <b>Hand it '
             'in</b>. The page shows you a receipt once your work has arrived.',
             auto=f'exam:handin paper={pid} step=confirmed', check=f'paper:{pid}.handedIn'),
        task(f'es{n}-word', 'To keep a copy, press <b>Download your copy</b>. Before you hand in, the same button is under '
             'the password box, and it’s called <b>Download a copy for yourself</b>. The copy is saved as a Word '
             'document, usually in your Downloads folder.', auto=f'exam:download paper={pid} format=docx',
             check=f'paper:{pid}.downloaded'),
    ])


def after_note(what='the ground a good answer covers'):
    return callout('info', 'After you’ve handed it in', f'<p>Once you’ve submitted, <b>Review my answers</b> shows you '
                   f'{what}. Read it after you’ve handed your work in, and make a note of what you’d add or change. '
                   'That’s what we’ll talk about in the supervision.</p><p>Your work is kept in this browser, in Files → '
                   '<code>essays</code>. It won’t be there on another computer, and some shared computers clear it when '
                   'you log out, so download a copy before you finish.</p>')


def before_you_start(extra=()):
    """the usual points before writing (nothing about how long to spend)"""
    lis = [
        'Look back at the feedback on your earlier work, and pick one thing to do better this time.',
        'Make sure you have the <b>hand-in password</b> I gave you, because you’ll need it at the end. You won’t find it '
        'anywhere on this site.',
        'Your work saves itself in this browser as you type, so you can stop and come back to it. Submit it once it’s '
        'finished.',
    ] + list(extra)
    return '<h2>Before you start</h2>\n<ul>\n' + '\n'.join(f'<li>{x}</li>' for x in lis) + '\n</ul>'


def revision_part(n, pid, intro, lecturer_note):
    """the revision titles (the questions of the paper pid), with an optional hand-in"""
    rev = ''.join(f'<li>{t}</li>' for t in titles(pid))
    return f'''<h2 id="m{n}-rev">Essay titles for revision</h2>
<p>{intro}</p>
<ol class="titles">{rev}</ol>
<p>{lecturer_note}</p>
<p>Planning an answer to each one (your argument, your evidence, and the order you’d put them in) is good revision. If you’d like feedback on one, write it in Supervision work {exam(pid, "open them")} and <b>hand it in</b>, in the same way as the work for this week. That’s optional: choose the title you want to write, and leave the others blank. After you submit, the guidance shows you the ground each title should cover.</p>
{optional(activity("If you want the practice", [
    task(f"m{n}-plan", 'Plan an answer to one of the revision titles. Sum up your position in a sentence, then jot down the three or four points, with the evidence for each, that would support it.'),
    task(f"m{n}-rev", 'Write one of them up in Supervision work, submit it, and hand it in if you’d like my feedback on it.', auto=f"exam:submit paper={pid}"),
]), title='Practice')}'''
