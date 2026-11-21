"""The chapters of Supervision 8 (supervision-8.html): pH, and the course as a whole.

The week has one lecture, the second on the physiology of pH regulation (the regulation of H+ secretion, the excretion
of non-volatile acid, HCO3- secretion and the disorders of acid-base balance), so the supervision is synoptic: the work
to hand in is an essay that needs the respiratory lectures as well as the renal ones (exams/s8-essay.json), on one of
the pH handout's titles: "Discuss the relative importance of respiratory system and kidneys in regulating plasma pH."
The handout's other titles are the revision titles (exams/s8-revision.json), which can be handed in too; the first is
corrected ("What mechanisms is ..." in the handout reads "By what mechanisms is ..." here). Nothing here is copied from
the handout or the slides.

The chapters: what to do this week, with the earlier supervisions this one draws on; two optional exercises, about
half an hour in all (pH, PCO2 and bicarbonate in R; and a flow diagram in which the lungs and the kidneys share the
work, examples/diagrams/acid-base.flow.json); writing the essay and handing it in; and revision titles. ALL() puts them
in order.

The numbers (the R code, worked out the same way in Python): ph(24, 40) = 7.40; 10 mM of strong acid gives 6.20 in a
closed system, 7.17 if the PCO2 stays at 40 mmHg, and 7.32 with respiratory compensation (PCO2 28 mmHg, the handout's
1.2 mmHg per mM); at altitude, ph(24, 30) = 7.53 and, after renal compensation (HCO3- down 4 mM per 10 mmHg),
ph(20, 30) = 7.45; the lecture's question, ph(40, 80) = 7.32. In the diagram (simulated by a copy of flow.js's model
in Python): with both systems, [H+] peaks at 1.11 within an hour, ventilation at 1.28 and PCO2 falls to 0.72, and by
6 days [H+] is 1.02, ventilation 1.05 and the kidneys' new HCO3- 1.83; with the lungs alone, [H+] stays at 1.11 and
ventilation at 1.29; with the kidneys alone, [H+] peaks at 1.38, and is back to 1.03 by 2 days."""
from lib import *
from sup import (HAND_NOTE, after_note, before_you_start, handin_box, how_page_works, name_step, optional_chapter,
                 optional_note, revision_part, titles, write_steps)

N = 8
PAPER = 's8-essay'
REVISION = 's8-revision'
ESSAY = titles(PAPER)[0]
ACIDBASE = 'example:acid-base'

R_PH = 'ph <- function(hco3, pco2) 6.1 + log10(hco3 / (0.03 * pco2))'
R_NORMAL = 'ph(24, 40)'
R_ACID = 'c(closed = 6.1 + log10(14 / (0.03 * 40 + 10)), open = ph(14, 40), compensated = ph(14, 28))'
R_PHS = 'pH <- seq(7, 7.7, by = 0.01)'
R_PLOT = ('matplot(pH, outer(10^(pH - 6.1), 0.03 * c(20, 40, 80)), type = "l", lty = 1:3, col = 1, '
          'xlab = "pH", ylab = "Plasma bicarbonate (mM)")')
R_LEGEND = 'legend("topleft", c("PCO2 20 mmHg", "40 mmHg", "80 mmHg"), lty = 1:3)'
R_POINTS = 'points(c(ph(24, 40), ph(14, 40), ph(14, 28)), c(24, 14, 14), pch = 19)'
R_ALT = 'c(acute = ph(24, 30), compensated = ph(20, 30))'
R_MCQ = 'ph(40, 80)'


def ch_week(num):
    box = handin_box(N, PAPER, f'“{ESSAY}”', [
        'You write the essay in <b>Supervision work</b>, as you will in the online exam. Plan it first, then write it '
        'in continuous prose, in your own words.',
        'It’s one of the titles in the pH handout. It needs the respiratory lectures as well as the renal ones, and it '
        'asks you to weigh the two systems, not just to describe them: chapter 3 is about how to do that.',
    ], 's8-write')
    back = callout('tip', 'Looking back', '''<p>This week has only one lecture, and its title draws on much of the course, so it’s a good time to look back:</p>
<ul>
<li><b>Supervision 5</b>: the control of breathing (the central and peripheral chemoreceptors, and what each senses), the transport of CO<sub>2</sub> and haemoglobin as a buffer, and altitude, where a respiratory alkalosis is compensated by the kidneys. <a href="supervision-5.html">Open it</a></li>
<li><b>Supervision 7</b>: the first pH lecture (buffers, the Henderson–Hasselbalch equation, and how the tubules handle H<sup>+</sup>, HCO<sub>3</sub><sup>−</sup> and NH<sub>4</sub><sup>+</sup>), and potassium and aldosterone, which affect acid–base balance too. <a href="supervision-7.html">Open it</a></li>
<li><b>Supervision 1</b>: heavy exercise, where lactic acid adds a metabolic acidosis that the lungs compensate for. <a href="supervision-1.html">Open it</a></li>
</ul>''')
    body = f'''
{box}

<h2 id="w8-plan">The week, step by step</h2>
<ol class="plan">
<li>If you’d like to, start with <b>two short exercises</b>. They’re optional, and take about half an hour altogether. In chapter 1 you use <b>R</b> to see why the bicarbonate buffer works so well although its pK is 6.1, and to draw a pH–bicarbonate diagram of three acid–base disturbances. In chapter 2 you run a <b>diagram</b> in which the lungs and the kidneys share the work of regulating pH, and take each away in turn. {goto("s8-r", "start")}</li>
<li>Then <b>write your essay</b> and hand it in (chapter 3). {goto("s8-write", "go there")}</li>
<li>Chapter 4 has the pH handout’s other titles, for revision. You can hand one in for feedback if you’d like to, but you don’t have to. {goto("s8-more", "go there")}</li>
</ol>
{back}
{name_step(N)}
{how_page_works("Chapters 1, 2 and 4 are")}
'''
    return chapter("s8-week", num, "This week", "exam", "Supervision 8: pH, the lungs and the kidneys", 5,
                   "This week’s lecture is about how the kidneys regulate their secretion of H<sup>+</sup>, how the body "
                   "gets rid of non-volatile acid, and what happens in acidosis and alkalosis. It’s the last lecture of "
                   "the course, and it draws the respiratory and renal lectures together.", body)


def ch_r(num):
    body = optional_chapter(f'''
{optional_note(15, "the second pH lecture, and the first")}

<p>The Henderson–Hasselbalch equation for the bicarbonate buffer links the three things measured in a sample of arterial blood: pH = 6.1 + log<sub>10</sub>([HCO<sub>3</sub><sup>−</sup>] / (0.03 × PCO<sub>2</sub>)), with HCO<sub>3</sub><sup>−</sup> in mM and PCO<sub>2</sub> in mmHg (0.03 is the solubility of CO<sub>2</sub>, in mM per mmHg).</p>
{activity("pH, PCO₂ and bicarbonate in R", [
    task("ab-fn", f'Write the equation as a function {rcode(R_PH)}, and try it with normal values {rcode(R_NORMAL)}.', auto="r:input kind=rstudio line~ph <- function"),
    task("ab-acid", f'Add 10 mmol of a strong acid to each litre of ECF. It reacts with HCO<sub>3</sub><sup>−</sup>, which falls from 24 to 14 mM, and makes 10 mM of CO<sub>2</sub>. Compare the pH in a <b>closed</b> system, where the CO<sub>2</sub> stays; an <b>open</b> one, where the lungs keep the PCO<sub>2</sub> at 40 mmHg; and one with <b>respiratory compensation</b>, where the PCO<sub>2</sub> falls by 1.2 mmHg for each mM that HCO<sub>3</sub><sup>−</sup> fell, to 28 mmHg: {rcode(R_ACID)}', auto="r:input kind=rstudio line~closed ="),
    task("ab-plot", f'Draw a pH–bicarbonate diagram: a range of pH {rcode(R_PHS)}, and the line for each of three PCO<sub>2</sub>s (an isobar) {rcode(R_PLOT)}, with a legend {rcode(R_LEGEND)}.', auto="r:input kind=rstudio line~matplot"),
    task("ab-points", f'Mark the normal state and the two acidoses on it {rcode(R_POINTS)}.', auto="r:input kind=rstudio line~points("),
    task("ab-alt", f'At altitude, hyperventilation lowers the PCO<sub>2</sub> to 30 mmHg; over a few days, the kidneys excrete HCO<sub>3</sub><sup>−</sup>, which falls by about 4 mM for each 10 mmHg fall in PCO<sub>2</sub>: {rcode(R_ALT)}', auto="r:input kind=rstudio line~acute ="),
    task("ab-mcq", f'The lecture’s question: a pH of 7.30, HCO<sub>3</sub><sup>−</sup> 40 mM and PCO<sub>2</sub> 80 mmHg. Check that they fit together {rcode(R_MCQ)}.', auto="r:input kind=rstudio line~ph(40, 80)"),
])}
{q("ab-q-open", "The pK of the bicarbonate buffer is 6.1, far from 7.4, so in a beaker it would be a poor buffer. What do your three numbers show about why it works so well in the body?",
   "In a closed system the pH falls to about 6.2, which is fatal: the CO<sub>2</sub> made from the HCO<sub>3</sub><sup>−</sup> stays, so the ratio of HCO<sub>3</sub><sup>−</sup> to CO<sub>2</sub> collapses from 20 to about 1.25. In the body the system is open: the lungs remove the CO<sub>2</sub> and hold the PCO<sub>2</sub> at 40 mmHg, so the pH falls only to about 7.17 (physiological buffering). The chemoreceptors then drive ventilation up, the PCO<sub>2</sub> falls to about 28 mmHg, and the pH rises to about 7.32 (respiratory compensation). The kidneys finish the job by making new HCO<sub>3</sub><sup>−</sup>, to replace what was used up. The buffer is powerful because both of its members are regulated: CO<sub>2</sub> by the lungs, HCO<sub>3</sub><sup>−</sup> by the kidneys. (In the body, about half of an acid load is buffered at first by phosphate and proteins, which this calculation leaves out.)")}
{q("ab-q-alt", "At altitude, what is the pH once the kidneys have compensated? Give it to two decimal places.",
   "About 7.45, from 7.53. The hyperventilation driven by hypoxia (through the peripheral chemoreceptors) lowers the PCO<sub>2</sub>, a respiratory alkalosis, which itself limits the hyperventilation, because the central chemoreceptors sense the alkaline CSF. Over a few days the kidneys excrete HCO<sub>3</sub><sup>−</sup> (they secrete less H<sup>+</sup>, and the type B intercalated cells secrete HCO<sub>3</sub><sup>−</sup>), so the pH returns towards normal and ventilation can rise further: ventilatory acclimatisation. On your diagram, the point moves along the isobar for the low PCO<sub>2</sub>.",
   accept="num:7.45±0.015", placeholder="pH")}
{mcq("ab-q-mcq", "A pH of 7.30, HCO<sub>3</sub><sup>−</sup> 40 mM and PCO<sub>2</sub> 80 mmHg is characteristic of:", [
    ("Compensated (chronic) respiratory acidosis", True, "Yes. The PCO<sub>2</sub> is high (the primary disturbance is respiratory: hypoventilation, as in chronic lung disease), and the pH is low, so it’s an acidosis. The HCO<sub>3</sub><sup>−</sup> is well above 24 mM: the kidneys have made new HCO<sub>3</sub><sup>−</sup> over days, bringing the pH most of the way back. Without them, a PCO<sub>2</sub> of 80 mmHg with 24 mM HCO<sub>3</sub><sup>−</sup> would give a pH of about 7.10."),
    ("Compensated (chronic) metabolic alkalosis", False, "No. A metabolic alkalosis would have a high pH. Here the pH is low, and the primary change is the high PCO<sub>2</sub>."),
    ("Primary (acute) respiratory acidosis", False, "No. In an acute respiratory acidosis the HCO<sub>3</sub><sup>−</sup> is near normal; a value of 40 mM takes days of renal compensation."),
    ("Normal acid–base balance", False, "No. All three values are abnormal."),
])}
''')
    return chapter("s8-r", num, "pH in R", "rstudio", "Optional: pH, PCO₂ and bicarbonate", 15,
                   "Use the Henderson–Hasselbalch equation in R to see why the bicarbonate buffer works so well, and "
                   "draw three acid–base disturbances on a pH–bicarbonate diagram.", body)


def ch_flow(num):
    body = optional_chapter(f'''
{optional_note(15, "the second pH lecture, and the respiratory lectures on the control of breathing")}

<p>The diagram is a simple model of a sustained extra load of non-volatile acid, which starts at 6 hours and goes on. Every level is relative to normal (1): an [H<sup>+</sup>] of 1 is 40 nM (pH 7.4), 1.1 is 44 nM (pH 7.35) and 1.4 is 56 nM (pH 7.25).</p>
{activity("The lungs and the kidneys", [
    task("fl-open", f'Open the diagram {flow(ACIDBASE, "show me")}. Follow the arrows: the acid uses up plasma HCO<sub>3</sub><sup>−</sup>, so the [H<sup>+</sup>] rises; the [H<sup>+</sup>] drives ventilation through the chemoreceptors, and the kidneys’ production of new HCO<sub>3</sub><sup>−</sup>.', auto="flow:open example=acid-base"),
    task("fl-run", f'Press <b>Run</b> {flowrun("show me")}, and watch the graphs: the first few hours, and then the days that follow. Dragging the slider under the graphs shows you the diagram at any moment of the run.', auto="flow:run name~acid blocked=0 knocked=0"),
    task("fl-lungs", 'Now let only the lungs respond. Right-click the arrow from <b>[H⁺] of the blood</b> to the kidneys (or press and hold it), choose <b>Block this arrow</b>, and run it again.', auto="flow:run name~acid blocked=1 knocked=0"),
    task("fl-kidneys", 'Now let only the kidneys respond. Unblock that arrow (right-click it again). Then click the box <b>Ventilation</b>, choose <b>Fixed: it ignores its inputs</b> in the panel on the right, set <b>Fixed at</b> to 1 (its normal level), and run it again.', auto="flow:run name~acid blocked=0 knocked>0"),
])}
{q("fl-q-both", "In the first run, what happened in the first hour, and what happened over the next few days?",
   "Within an hour, the [H<sup>+</sup>] rose by about 11% (to a pH of about 7.35), ventilation rose by nearly 30% and the PCO<sub>2</sub> fell by nearly 30%: the lungs respond in minutes, but they only limit the change in pH, they don’t correct it. Over the following days, the kidneys’ production of new HCO<sub>3</sub><sup>−</sup> rose (to nearly twice normal), so the plasma HCO<sub>3</sub><sup>−</sup> recovered, the [H<sup>+</sup>] returned almost to normal, and as it did so, ventilation and the PCO<sub>2</sub> returned towards normal too. The lungs compensate, quickly and partly; the kidneys correct, slowly and almost completely, and then the respiratory compensation is no longer needed.")}
{q("fl-q-alone", "Compare the runs with the lungs alone and with the kidneys alone. What does each show, and what does this simple model leave out?",
   "With the lungs alone, the [H<sup>+</sup>] stays about 11% high for as long as the acid load lasts, with ventilation about 30% above normal: compensation, but no correction, and at a cost (the work of breathing; a low PCO<sub>2</sub> constricts the cerebral vessels; and the PCO<sub>2</sub> can’t fall much below 10–15 mmHg however hard you breathe). With the kidneys alone, the [H<sup>+</sup>] rises by nearly 40% (to a pH of about 7.25) before the kidneys bring it back, over a day or two. So the lungs protect against the first, rapid change, and the kidneys restore the HCO<sub>3</sub><sup>−</sup>. The model leaves out a lot: it’s linear (the real Henderson–Hasselbalch relationship isn’t); the buffers other than HCO<sub>3</sub><sup>−</sup>, inside and outside cells; the liver’s switch from urea to glutamine; the limits of renal compensation (real compensation takes three to five days, and in ketoacidosis the acid can come faster than the kidneys can deal with it); and that the lungs excrete 12–15 mol of CO<sub>2</sub> a day, while the kidneys are needed every day to make the HCO<sub>3</sub><sup>−</sup> that the normal 70 mmol of non-volatile acid uses up, so in renal failure an acidosis develops without any extra load.")}
''')
    return chapter("s8-flow", num, "The lungs and the kidneys", "flow", "Optional: the lungs and the kidneys", 15,
                   "Run a diagram of an acid load in which the lungs and the kidneys share the work of regulating pH, "
                   "then take away each in turn.", body)


def ch_write(num):
    body = f'''
<p class="essay-title">“{ESSAY}”</p>

<h2 id="es8-title">Weighing, not listing</h2>
<p>A title that asks for “the relative importance” of two things wants a judgement, and an essay that describes what the lungs do and then what the kidneys do, and stops, hasn’t answered it. Decide on your answer before you write, and build the essay to support it.</p>
<ol class="plan">
<li><b>Choose your criteria.</b> How fast does each act? How much can it handle? Does it correct a disturbance, or only limit it? What does each deal with: volatile acid (CO<sub>2</sub>), non-volatile acid, base? What happens when each fails?</li>
<li><b>Weigh the two on each criterion, with evidence.</b> Disorders are the evidence here: what happens in respiratory failure, in renal failure, at altitude, in ketoacidosis, after vomiting.</li>
<li><b>Say where the answer depends on the circumstances</b>, and what it depends on: the timescale, and the source of the disturbance.</li>
<li><b>Conclude with your judgement</b>, which should follow from what you’ve written, not be a surprise.</li>
</ol>
{mcq("es8-q-judge", "Which of these sentences, from the conclusion of an essay on this title, makes a judgement?", [
    ("“The lungs regulate PCO<sub>2</sub> and the kidneys regulate HCO<sub>3</sub><sup>−</sup>.”", False, "It’s true, but it’s a description. Which matters more, and when?"),
    ("“Both systems are important in regulating plasma pH.”", False, "That avoids the question. It’s the sentence most essays on this title end with."),
    ("“Minute to minute, the lungs matter more, since they remove 12–15 mol of CO<sub>2</sub> a day and compensate within minutes; but only the kidneys can restore the HCO<sub>3</sub><sup>−</sup> that non-volatile acid uses up, so over days, and in renal failure, the kidneys are indispensable.”", True, "Yes. It weighs the two, says on what grounds and over what timescale, and could be argued with, which is what a judgement is."),
])}
{mcq("es8-q-evidence", "Which piece of evidence best supports the claim that the kidneys are essential for pH regulation?", [
    ("The lungs excrete far more acid, as CO<sub>2</sub>, than the kidneys do", False, "That supports the importance of the lungs, not of the kidneys."),
    ("In renal failure, a metabolic acidosis develops even on a normal diet, because the remaining nephrons can’t make enough new HCO<sub>3</sub><sup>−</sup> to replace what the daily load of non-volatile acid uses up", True, "Yes. It shows what happens without them, and why: no other organ can make new HCO<sub>3</sub><sup>−</sup> (by catabolising glutamine) on that scale."),
    ("The minimum pH of urine is about 4.5", False, "This is part of an argument about how the kidneys get rid of acid (not as free H<sup>+</sup>: at pH 4.5 it would take about 2300 L of urine a day), but on its own it doesn’t show that they’re essential."),
])}

{before_you_start([
    'It’s worth noting the controversy in the handout about how the body gets rid of non-volatile acid: whether the kidneys excrete it, as NH<sub>4</sub><sup>+</sup> and titratable acid, or mostly make new HCO<sub>3</sub><sup>−</sup> while the lungs excrete the acid as CO<sub>2</sub>. It bears directly on this title.',
])}
{write_steps(N, PAPER, 'Plan, then write. Decide on your judgement first, choose the criteria you’ll weigh the two systems by, support each with evidence from disorders, and end with your judgement.')}
{HAND_NOTE}
{after_note()}
{q("es8-q-next", "Once you’ve read the guidance, did your essay come to a judgement? If not, what would yours be?",
   "There’s no single right answer here, so bring yours to the supervision. A clear position, argued with evidence, matters more than which one you take.")}
'''
    return chapter("s8-write", num, "Write your essay", "exam", "Write your essay, and hand it in", None,
                   "This is the work to hand in this week. You write it in Supervision work, as you will in the online "
                   "exam, and then hand it in from the same page.", body)


def ch_more(num):
    body = revision_part(N, REVISION,
                         'These are the pH handout’s other titles. The first is how the handout’s first title should read. Several of them need the renal and respiratory lectures as well, so they make good synoptic revision. It’s worth noting them down.',
                         'For the rest of the course, the revision titles are in the earlier supervisions: Supervisions 1 and 2 (the cardiovascular system), 3 (endocrinology), 4 and 5 (respiration), and 6 and 7 (the kidney).')
    return chapter("s8-more", num, "Revision titles", "exam", "Revision titles", None,
                   "This chapter is optional. It has more essay titles on this week’s lecture, for revision. You can hand "
                   "one in for feedback if you’d like to.", body)


def ALL():
    order = [ch_week, ch_r, ch_flow, ch_write, ch_more]
    return [f(str(i)) for i, f in enumerate(order)]
