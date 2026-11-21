"""The chapters of Supervision 5 (supervision-5.html): gases in the blood, the control of breathing, and lung disease.

The lectures are the last three of the respiration course (the transport of respiratory gases in the blood; the
regulation of respiration, acid–base balance and exercise, diving and altitude; clinical respiratory physiology);
nothing here is copied from the handout or the slides. The work to hand in is four short-answer questions
(exams/s5-saqs.json), on the three lectures. The handout doesn't suggest essay titles, so I wrote the four revision
titles (exams/s5-revision.json), which can be handed in too.

The chapters: what to do this week; two optional exercises, about half an hour in all (haemoglobin in the Molecules tab,
and its dissociation curve in R, in anaemia and carbon monoxide poisoning; the lung function tests of three patients,
with the calculator); answering the short-answer questions and handing them in; and revision titles. ALL() puts them in
order.

The numbers were worked out from the R code (the same in Python), with the handout's values (150 g/L of haemoglobin,
1.39 mL O₂ per gram, 0.03 mL/L of dissolved O₂ per mmHg) and the Hill equation (n 2.7; P50 26.8 mmHg, or 15 mmHg for the
left shift that carbon monoxide causes): from a PO₂ of 100 to 40 mmHg, each litre of blood gives up about 49 mL of O₂
normally, about 25 mL with half the haemoglobin (anaemia), and about 8 mL with half of it bound to carbon monoxide. The
spirometry: FEV₁/FVC 0.39 (A), 0.88 (B) and 0.80 (C)."""
from lib import *
from sup import (HAND_NOTE, after_note, before_you_start, handin_box, how_page_works, name_step, optional_chapter,
                 optional_note, revision_part, titles, write_steps)

N = 5
PAPER = 's5-saqs'
REVISION = 's5-revision'

R_SAT = 'sat <- function(po2, p50 = 26.8) po2^2.7 / (po2^2.7 + p50^2.7)'
R_CONTENT = 'content <- function(po2, hb = 150, p50 = 26.8) 1.39 * hb * sat(po2, p50) + 0.03 * po2'
R_CURVE = 'curve(content(x), 0, 120, ylim = c(0, 210), xlab = "PO2 (mmHg)", ylab = "O2 content (mL per litre)")'
R_MORE = 'curve(content(x, hb = 75), add = TRUE, lty = 2); curve(content(x, hb = 75, p50 = 15), add = TRUE, lty = 3)'
R_RELEASE = ('release <- function(...) content(100, ...) - content(40, ...); '
             'c(normal = release(), anaemia = release(hb = 75), CO = release(hb = 75, p50 = 15))')

PFT = '''<table class="data">
<thead><tr><th>Patient</th><th>FEV<sub>1</sub> (L)</th><th>FVC (L)</th><th>TLC (L), and predicted</th><th>Diffusing capacity for CO (% of predicted)</th></tr></thead>
<tbody>
<tr><td>A, a man of 64, breathless on exertion</td><td>1.2</td><td>3.1</td><td>7.9 (6.5)</td><td>45%</td></tr>
<tr><td>B, a woman of 58, breathless on exertion, with a dry cough</td><td>2.1</td><td>2.4</td><td>3.9 (6.4)</td><td>50%</td></tr>
<tr><td>C, a man of 30, a healthy volunteer</td><td>3.3</td><td>4.1</td><td>6.3 (6.2)</td><td>98%</td></tr>
</tbody></table>'''


def ch_week(num):
    saqs = ''.join(f'<li>{t}</li>' for t in titles(PAPER))
    box = handin_box(N, PAPER, 'Four short-answer questions', [
        f'<ol class="titles">{saqs}</ol>',
        'Each is marked out of five. You answer them in <b>Supervision work</b>, in bullet points, as you would in the '
        'exam. Two of them need a calculation or a judgement from data: chapter 3 says how to set those out.',
    ], 's5-write', noun='questions')
    body = f'''
{box}

<h2 id="w5-plan">The week, step by step</h2>
<ol class="plan">
<li>If you’d like to, start with <b>two short exercises</b>. They’re optional, and take about half an hour altogether. In chapter 1 you look at haemoglobin in the <b>Molecules</b> tab, then use <b>R</b> to find out why carbon monoxide is worse than an anaemia. In chapter 2 you interpret the lung function tests of three people, with the calculator. Both go with the questions you hand in. {goto("s5-hb", "start")}</li>
<li>Then <b>answer the four questions</b> and hand them in (chapter 3). {goto("s5-write", "go there")}</li>
<li>Chapter 4 has four essay titles on this week’s lectures, for revision. You can hand one in for feedback if you’d like to, but you don’t have to. {goto("s5-more", "go there")}</li>
</ol>
{name_step(N)}
{how_page_works("Chapters 1, 2 and 4 are")}
'''
    return chapter("s5-week", num, "This week", "exam", "Supervision 5: gases in the blood, control and disease", 5,
                   "This week’s lectures are about how O<sub>2</sub> and CO<sub>2</sub> are carried in the blood, how "
                   "breathing is controlled and copes with exercise, diving and altitude, and what goes wrong in lung "
                   "disease. This week you hand in short answers rather than an essay.", body)


def ch_hb(num):
    body = optional_chapter(f'''
{optional_note(15, "the fourth lecture, on the transport of respiratory gases in the blood")}

{activity("Haemoglobin", [
    task("hb-open", f'Open haemoglobin {pdb("4HHB", "show me")}, colour it by chain {viewer("color chain", "show me")}, and show its four haem groups as spheres {viewer("show spheres HEM", "show me")}. This is deoxyhaemoglobin: two α and two β chains, each holding a haem.', auto="viewer:loaded id~4hhb"),
])}
{q("hb-q-bpg", "In deoxyhaemoglobin there’s a cavity between the two β chains, along the central axis of the molecule, which closes up when it binds O<sub>2</sub>. 2,3-BPG binds in it. What does that do to the dissociation curve, and why does it matter at altitude and in the fetus?",
   "2,3-BPG binds to the positively charged groups lining the cavity between the β chains, but only in the deoxy (T) form, which it stabilises. That lowers haemoglobin’s affinity for O<sub>2</sub> and shifts the dissociation curve to the right (a higher P<sub>50</sub>), so more O<sub>2</sub> is given up at the PO<sub>2</sub> of the tissues. At altitude, red cells make more 2,3-BPG within a day or two, which helps unloading. Fetal haemoglobin has γ chains in place of β, which bind 2,3-BPG poorly, so its curve lies to the left of the mother’s, and O<sub>2</sub> moves from her blood to the fetus’s across the placenta (in pregnancy, maternal 2,3-BPG rises, shifting her curve further right).")}
{activity("Anaemia and carbon monoxide, in R", [
    task("hb-sat", f'Write the dissociation curve as a function, the Hill equation, with P<sub>50</sub> as an argument: {rcode(R_SAT)}', auto="r:input kind=rstudio line~sat <- function"),
    task("hb-content", f'And the O<sub>2</sub> content, in mL per litre, with the handout’s values: {rcode(R_CONTENT)}', auto="r:input kind=rstudio line~content <- function"),
    task("hb-curve", f'Plot the normal curve {rcode(R_CURVE)}, then add an anaemia with half the haemoglobin (dashed), and carbon monoxide occupying half of it, which also shifts the curve of what’s left to the left (P<sub>50</sub> about 15 mmHg; dotted): {rcode(R_MORE)}', auto="r:input kind=rstudio line~p50 = 15"),
    task("hb-release", f'How much O<sub>2</sub> does each litre of blood give up as its PO<sub>2</sub> falls from 100 mmHg (arterial) to 40 mmHg (mixed venous)? {rcode(R_RELEASE)}', auto="r:input kind=rstudio line~release <- function"),
])}
{q("hb-q-co", "How much O<sub>2</sub> does a litre of blood give up between 100 and 40 mmHg in each case, to the nearest mL? Both the anaemia and the carbon monoxide halve the O<sub>2</sub> that the arterial blood carries, so why is carbon monoxide so much worse?",
   "About 49 mL normally, about 25 mL in the anaemia, and only about 8 mL with carbon monoxide. In both, the arterial content is roughly halved. But in the anaemia the curve keeps its shape, so the blood still gives up its O<sub>2</sub> at the PO<sub>2</sub> of the tissues. Carbon monoxide binds haemoglobin about 200 times more tightly than O<sub>2</sub>, and once it occupies some haems, the remaining haems hold their O<sub>2</sub> more tightly too (the curve shifts left and loses its sigmoid shape), so very little is released until the tissue PO<sub>2</sub> falls very low. Worse, the patient doesn’t hyperventilate, because the arterial PO<sub>2</sub> and PCO<sub>2</sub> are normal, the skin looks pink, and a pulse oximeter reads carboxyhaemoglobin as oxyhaemoglobin and gives a normal saturation.",
   accept="num:8±1.5", placeholder="mL per litre with carbon monoxide")}
''')
    return chapter("s5-hb", num, "Haemoglobin", "viewer", "Optional: haemoglobin, anaemia and carbon monoxide", 15,
                   "Look at haemoglobin in 3D, then use its dissociation curve, in R, to find out why carbon monoxide "
                   "is far more dangerous than an anaemia.", body)


def ch_pft(num):
    body = optional_chapter(f'''
{optional_note(15, "the sixth lecture, on clinical respiratory physiology")}

<p>Three people had their lung function tested: spirometry (the forced expiratory volume in one second, FEV<sub>1</sub>, and the forced vital capacity, FVC), the total lung capacity (TLC, measured by plethysmography), and the diffusing capacity for carbon monoxide.</p>
{PFT}
{activity("Work out the FEV₁/FVC ratios", [
    task("pf-calc", f'Open the calculator {calc("show me")}.', auto="calc:open"),
    task("pf-a", 'Work out FEV<sub>1</sub>/FVC for patient A.', auto="calc:result value>0.38 value<0.40"),
    task("pf-b", 'And for patient B.', auto="calc:result value>0.86 value<0.89"),
    task("pf-c", 'And for patient C.', auto="calc:result value>0.79 value<0.82"),
])}
{mcq("pf-q-a", "Patient A: FEV<sub>1</sub>/FVC 0.39, a TLC above predicted, and a low diffusing capacity. What pattern is this, and what disease is most likely?", [
    ("Obstructive, with air trapping and lost alveolar surface: emphysema (COPD)", True, "Yes. A ratio below 0.7 means obstruction: the air comes out slowly. The high TLC is hyperinflation and air trapping: with the alveolar walls destroyed, the lungs are more compliant and recoil less, and the small airways, no longer tethered, collapse early in expiration (the equal pressure point moves into them). The low diffusing capacity reflects the lost surface area for gas exchange. In asthma, by contrast, the diffusing capacity is usually normal."),
    ("Restrictive: pulmonary fibrosis", False, "No. In restriction the ratio is normal or high, and the TLC low."),
    ("Normal", False, "No. A ratio of 0.39 is far below the lower limit of normal (about 0.7)."),
])}
{mcq("pf-q-b", "Patient B: FEV<sub>1</sub>/FVC 0.88, a low TLC and a low diffusing capacity. What pattern is this?", [
    ("Obstructive: chronic bronchitis", False, "No. The ratio is high, not low: the air that can be breathed out comes out quickly."),
    ("Restrictive, with a thickened barrier: pulmonary fibrosis", True, "Yes. The lungs are stiff (low compliance), so the volumes (FVC and TLC) are small, but the airways are open, and the stiff lungs’ strong recoil drives the air out fast, so the ratio is normal or high. The thickened, scarred interstitium lengthens the path for diffusion, so the diffusing capacity is low, and the PO<sub>2</sub> may fall on exercise, when blood spends less time in the capillaries."),
    ("Normal", False, "No. Her FVC and TLC are well below predicted."),
])}
{q("pf-q-dlco", "Patients A and B both have a low diffusing capacity, for different reasons. Using Fick’s law, explain the reason in each.",
   "Fick’s law: the rate of diffusion across the barrier is proportional to its area and to the difference in partial pressure, and inversely proportional to its thickness (times a constant for the gas). In emphysema (A), the walls between alveoli are destroyed, so the area for exchange (and the capillaries in it) falls. In fibrosis (B), the area may be less affected, but the barrier is thickened by scar tissue, so the distance rises. Either lowers the rate at which carbon monoxide (or O<sub>2</sub>) moves from the alveoli into the blood. The test uses carbon monoxide because it binds haemoglobin so tightly that the blood’s partial pressure stays near zero: its uptake is limited by diffusion alone, not by blood flow.")}
''')
    return chapter("s5-pft", num, "Lung function tests", "exam", "Optional: reading lung function tests", 15,
                   "Interpret the spirometry, lung volumes and diffusing capacity of three people, and work out what "
                   "each pattern means.", body)


def ch_write(num):
    good = callout("tip", "Setting out an answer that uses data", (
        "<p><b>State the result, with the working.</b> “FEV<sub>1</sub>/FVC = 1.3 / 3.4 = 0.38.”</p>"
        "<p><b>Compare it with a reference.</b> “This is below 0.7, so the pattern is obstructive.”</p>"
        "<p><b>Interpret it.</b> “Air leaves the lungs slowly: the airways are narrowed, or collapse early in "
        "expiration.”</p>"
        "<p><b>Explain the mechanism, and say what else would help.</b> “In emphysema, loss of elastic recoil and of "
        "the alveolar walls that tether the small airways moves the equal pressure point into them. A high TLC and "
        "a low diffusing capacity would support this.”</p>"
        "<p>Each line can earn a mark. Answers that jump straight to a diagnosis often earn one.</p>"))
    body = f'''
<p>This week you hand in four short answers instead of an essay. Each is marked out of five, against a list of points, so precision and coverage matter more than argument.</p>

<h2 id="es5-saq">Answering a short-answer question</h2>
<ol class="plan">
<li><b>Read the verb.</b> “Distinguish” wants the differences, side by side; “explain” wants mechanisms; “interpret” wants a judgement from the data, justified.</li>
<li><b>Count the marks.</b> Five marks means at least five separate, precise points, in bullet points.</li>
<li><b>Show your working</b> for any number, with units, and say what the number means.</li>
<li><b>Answer the question that’s asked.</b> A labelled sketch (a dissociation curve, say) can save words.</li>
</ol>
{good}
{mcq("es5-q-sat", "One question asks you to distinguish the O<sub>2</sub> content of arterial blood from its O<sub>2</sub> saturation. Which point earns a mark?", [
    ("“Content and saturation are different.”", False, "True, but it says nothing about how they differ, so it earns nothing."),
    ("“Saturation is the percentage of haemoglobin’s binding sites occupied by O<sub>2</sub> (about 97.5% at a PO<sub>2</sub> of 100 mmHg); content is the volume of O<sub>2</sub> per litre of blood, which also depends on how much haemoglobin there is (about 200 mL/L normally).”", True, "Yes. Each quantity is defined, with a typical value, and the difference that matters (the amount of haemoglobin) is stated. A second point could then show why: in anaemia the saturation is normal but the content low."),
    ("“Saturation is measured by a pulse oximeter.”", False, "True, and worth mentioning in passing (it’s why carbon monoxide poisoning is missed), but it doesn’t distinguish the two quantities."),
])}

{before_you_start()}
{write_steps(N, PAPER, 'Answer each question in bullet points, with your working for any calculation. Aim for at least five precise points for each one.', noun='questions', words=79)}
{HAND_NOTE}
{after_note('the points each answer is marked against')}
{q("es5-q-next", "Once you’ve read the marking points, which answer would have scored least, and was it missing a definition, a number, a mechanism, or the judgement the data needed?",
   "There’s no single right answer here, so bring yours to the supervision. Data questions most often lose marks by giving a diagnosis without the working or the reasoning, and definition questions by describing without defining.")}
'''
    return chapter("s5-write", num, "Your short answers", "exam", "Answer the questions, and hand them in", None,
                   "This is the work to hand in this week: four short-answer questions, written in Supervision work and "
                   "handed in from the same page.", body)


def ch_more(num):
    body = revision_part(N, REVISION,
                         'These four titles go with this week’s three lectures. It’s worth noting them down: they’re the kind of title you could meet in the exam.',
                         'The handout doesn’t suggest titles, so these are mine, based on the course’s learning outcomes.')
    return chapter("s5-more", num, "Revision titles", "exam", "Revision titles", None,
                   "This chapter is optional. It has four essay titles on this week’s lectures, for revision. You can "
                   "hand one in for feedback if you’d like to.", body)


def ALL():
    order = [ch_week, ch_hb, ch_pft, ch_write, ch_more]
    return [f(str(i)) for i, f in enumerate(order)]
