"""The chapters of Supervision 7 (supervision-7.html): volume, drinking, potassium and the start of pH.

The lectures are the last two of human renal physiology (the regulation of extracellular fluid volume and the
integrated responses to challenges to body fluids; calcium, phosphate and potassium) and the first on the regulation
of pH (buffers and the renal handling of H+, HCO3- and NH4+); nothing here is copied from the handouts or the slides.
The work to hand in is an essay (exams/s7-essay.json), on the title in the fourth lecture's slides: "How does an adult
human respond to the ingestion of one litre of (a) fresh water; (b) isotonic saline; (c) seawater?" The renal
handout's other titles on these lectures and its third quotation are the revision titles (exams/s7-revision.json),
which can be handed in too. The pH handout's titles are in Supervision 8.

The chapters: what to do this week; two optional exercises, about half an hour in all (where a litre goes, with the
calculator; potassium after a meal, with the calculator and the adrenal gland in the Microscope); writing the essay
and handing it in; and revision titles. ALL() puts them in order.

The numbers use the lecture's round figures: 40 L of body water at 300 mOsm/kg, 16 L of it extracellular (3 L of that
plasma) and 24 L intracellular; seawater at 1000 mOsm/L. A litre of water: 12000 / 41 = 292.7 mOsm/kg, and an ECF of
4800 / 292.7 = 16.4 L. A litre of seawater: 13000 / 41 = 317.1 mOsm/kg, and an ECF of 5800 / 317.1 = 18.3 L (the
cells lose 1.3 L). Potassium: 40 mmol in 16 L raises plasma K+ by 2.5 mM, from 4.5 to 7.0 mM, and E_K (61.5 log10
(Ko / 150)) from -93.7 to -81.9 mV."""
from lib import *
from sup import (HAND_NOTE, after_note, before_you_start, handin_box, how_page_works, name_step, optional_chapter,
                 optional_note, revision_part, titles, write_steps)

N = 7
PAPER = 's7-essay'
REVISION = 's7-revision'
ESSAY = titles(PAPER)[0]
ADRENAL = 'adrenal-gland@0.75,1.85,10x'


def ch_week(num):
    box = handin_box(N, PAPER, f'“{ESSAY}”', [
        'You write the essay in <b>Supervision work</b>, as you will in the online exam. Plan it first, then write it '
        'in continuous prose, in your own words.',
        'It’s the title in the slides of the fourth renal lecture. It has three parts, and chapter 3 is about how to '
        'shape an essay like that.',
    ], 's7-write')
    body = f'''
{box}

<h2 id="w7-plan">The week, step by step</h2>
<ol class="plan">
<li>If you’d like to, start with <b>two short exercises</b>. They’re optional, and take about half an hour altogether. In chapter 1 you use the calculator to find out where each of the three litres in your essay goes. In chapter 2 you work out what the potassium in a meal would do if your cells didn’t take it up, and find the cells that make aldosterone in the <b>Microscope</b>. {goto("s7-litre", "start")}</li>
<li>Then <b>write your essay</b> and hand it in (chapter 3). {goto("s7-write", "go there")}</li>
<li>Chapter 4 has the renal handout’s other titles on these lectures, for revision. You can hand one in for feedback if you’d like to, but you don’t have to. {goto("s7-more", "go there")}</li>
</ol>
{name_step(N)}
{how_page_works("Chapters 1, 2 and 4 are")}
'''
    return chapter("s7-week", num, "This week", "exam", "Supervision 7: volume, potassium and pH", 5,
                   "This week’s lectures are about how the body regulates the volume of its extracellular fluid, how "
                   "osmoregulation and volume regulation work together when you drink, how it handles potassium, calcium "
                   "and phosphate, and how buffers and the kidney start to regulate pH.", body)


def ch_litre(num):
    body = optional_chapter(f'''
{optional_note(15, "the fourth lecture, on extracellular fluid volume and the integrated responses")}

<p>Use the lecture’s round numbers: 40 L of body water at 300 mOsm/kg, 16 L of it outside the cells (3 L of that is plasma) and 24 L inside them. Water crosses cell membranes easily, so the fluid inside and outside the cells always ends up at the same osmolality. Na<sup>+</sup> and Cl<sup>−</sup> stay outside the cells.</p>
{activity("Where does a litre go?", [
    task("lt-calc", f'Open the calculator {calc("show me")}.', auto="calc:open"),
    task("lt-water", 'A litre of <b>fresh water</b> adds water but no solute, and spreads through all the body water. Work out the new osmolality: the body’s 40 × 300 mOsm, now in 41 L.', auto="calc:result value>292.5 value<292.9"),
    task("lt-water-ecf", 'The solute outside the cells (16 × 300 mOsm) stays there. Work out the new volume of the extracellular fluid (ECF): that solute divided by the new osmolality.', auto="calc:result value>16.35 value<16.45"),
    task("lt-saline", 'A litre of <b>isotonic saline</b> adds 300 mOsm and a litre of water, all of it to the ECF, so the osmolality doesn’t change, and no water moves into or out of the cells. Work out the rise in the volume of the ECF, as a percentage.', auto="calc:result value>6.2 value<6.3"),
    task("lt-sea", 'A litre of <b>seawater</b> adds a litre of water and about 1000 mOsm of salt, which stays in the ECF once it has been absorbed. Work out the new osmolality.', auto="calc:result value>316.9 value<317.3"),
    task("lt-sea-ecf", 'And the new volume of the ECF, which now holds 16 × 300 + 1000 mOsm.', auto="calc:result value>18.25 value<18.35"),
])}
{q("lt-q-water", "After the litre of fresh water, how much of it is in the ECF, and how much in the plasma? Which of the body’s regulatory systems will notice, and what does it do?",
   "The ECF rises from 16 to 16.4 L, so it holds 0.4 L of the litre, and the cells 0.6 L. The plasma is 3 of the 16 L of ECF, so it gains only about 75 mL: the blood volume barely changes, and the volume receptors see little (the lecture: “no volume regulatory effects”). But the osmolality falls by about 7 mOsm/kg (2.4%), and plasma osmolality is normally held within 282 to 290, so the hypothalamic osmoreceptors notice: the magnocellular neurones swell, their stretch-inactivated cation channels close, they fire less, and less ADH is released from the posterior pituitary. With little ADH, the collecting ducts lose their aquaporin-2 and become impermeable to water, so the dilute fluid leaving the loop of Henle passes on as dilute urine: a water diuresis. Because ADH is released by nerves and cleared quickly, the response is fast, and most of the litre has gone within two or three hours. Reflexes from the gut and liver begin to inhibit ADH even before the water is absorbed (feed-forward).")}
{q("lt-q-saline", "Isotonic saline expands the ECF by 6.25%, but doesn’t change its osmolality. Why is it excreted so much more slowly than fresh water?",
   "Because the fast system, osmoregulation through the osmoreceptors and ADH, isn’t engaged: nothing has changed for it to correct. Only volume regulation responds, and its output, Na<sup>+</sup> excretion, is slow. The plasma gains about 0.2 L (3/16 of the litre), which is sensed by the cardiopulmonary (atrial and great vein) receptors and the arterial baroreceptors, and by the kidney itself. The responses: less renal sympathetic activity; less renin, so less angiotensin II and less aldosterone; more atrial natriuretic peptide; a slightly higher arterial pressure (pressure natriuresis); and diluted plasma proteins, which lower the colloid osmotic pressure in the peritubular capillaries and reduce proximal reabsorption. Together they raise Na<sup>+</sup> excretion, and water follows, but aldosterone acts through gene transcription, and the excess takes many hours, up to a day or two, to excrete. Volume regulation is subordinate to osmoregulation: the ECF volume is allowed to vary, while the osmolality isn’t.")}
{q("lt-q-sea", "After the seawater, what has happened to the cells? Why does drinking seawater leave you more dehydrated than before?",
   "The osmolality rises from 300 to about 317 mOsm/kg (5.7%), so water leaves the cells: they lose 1.3 L (24 to 22.7 L), while the ECF gains 2.3 L (to 18.3 L). So the ECF is expanded but the cells are dehydrated, and osmotic thirst and maximal ADH secretion follow; osmotic thirst overrides the signals from an expanded volume. (At first, before it’s absorbed, the hypertonic seawater draws water into the gut, so the ECF shrinks and there is hypovolaemic thirst too.) To get rid of the salt, the kidney must excrete it. The most concentrated urine a human kidney can make is about 1200 mOsm/kg, but in a maximally concentrating kidney up to half of the medulla’s osmotic pressure is urea, so the NaCl in the urine can’t be as concentrated as it is in seawater. Excreting the salt of a litre of seawater takes more than a litre of urine, so the body loses water overall, and drinking more seawater makes things worse.")}
''')
    return chapter("s7-litre", num, "Where does a litre go?", "exam", "Optional: where does a litre go?", 15,
                   "Work out, with the calculator, what a litre of fresh water, isotonic saline or seawater does to the "
                   "osmolality and the volumes of the body’s fluids.", body)


def ch_k(num):
    body = optional_chapter(f'''
{optional_note(15, "the fifth lecture, on potassium, and the fourth, on aldosterone")}

<p>Plasma K<sup>+</sup> is held at about 4.5 mM, and above 5.5 mM (hyperkalaemia) it’s dangerous. There’s only about 50–70 mmol of K<sup>+</sup> in the ECF, but about 4 mol inside the cells, at 150 mM. A meal rich in fruit and vegetables can easily hold 40 mmol of K<sup>+</sup>, getting on for half a day’s intake.</p>
{activity("Potassium after a meal", [
    task("k-calc", f'Open the calculator {calc("show me")}.', auto="calc:open"),
    task("k-plasma", 'Suppose the 40 mmol were all absorbed, and stayed in the 16 L of ECF. Work out what the plasma K<sup>+</sup> would become, starting from 4.5 mM.', auto="calc:result value>6.95 value<7.05"),
    task("k-ek", 'The resting membrane potential of muscle and nerve is close to the K<sup>+</sup> equilibrium potential. Work out E<sub>K</sub> at 37 °C with a plasma K<sup>+</sup> of 7 mM and 150 mM inside: <code>61.5 × log(7 ÷ 150)</code>, in mV. (It’s about −94 mV normally, at 4.5 mM.)', auto="calc:result value>-82.2 value<-81.6"),
    task("k-open", f'Open the adrenal gland at 10× {scope(ADRENAL, "show me")}: the capsule, and the cortex just inside it.', auto="scope:open slide=adrenal-gland"),
    task("k-zg", f'Find the zona glomerulosa, which makes aldosterone {scopefind("adrenal-gland:zona-glomerulosa")}. It’s a thin, patchy layer of small cells in rounded clusters, just under the capsule, before the long, straight cords of the zona fasciculata.', auto="scope:find slide=adrenal-gland target=zona-glomerulosa ok=true"),
])}
{q("k-q-danger", "What would a plasma K<sup>+</sup> of 7 mM do, and what stops the K<sup>+</sup> in a meal from getting anywhere near it?",
   "E<sub>K</sub> would rise by about 12 mV, from about −94 to −82 mV, so excitable cells would depolarise. A small depolarisation brings cells nearer threshold, but a sustained one inactivates voltage-gated Na<sup>+</sup> channels, so excitability and conduction fall: in the heart, conduction slows, and arrhythmias and cardiac arrest can follow. What prevents it is internal balance: K<sup>+</sup> is taken up into cells, mainly muscle and liver, by the Na<sup>+</sup>/K<sup>+</sup>-ATPase, which insulin (released by the meal), adrenaline (through β<sub>2</sub> receptors) and aldosterone stimulate. 40 mmol is only 1% of the 4 mol already inside the cells. Then, over the next hours, the kidney excretes it: K<sup>+</sup> secretion by the principal cells of the distal tubule and collecting duct rises, stimulated directly by the high plasma K<sup>+</sup> and by aldosterone. Renal excretion is too slow to deal with a meal’s K<sup>+</sup> on its own, which is why people with diabetes (with little insulin) see larger rises.")}
{q("k-q-paradox", "Aldosterone promotes both Na<sup>+</sup> reabsorption and K<sup>+</sup> secretion by the same cells. So why doesn’t a fall in blood volume, which raises aldosterone, make you lose K<sup>+</sup>? And why doesn’t a water diuresis?",
   "In hypovolaemia, more Na<sup>+</sup> and water are reabsorbed earlier in the nephron (angiotensin II and the sympathetic nerves act on the proximal tubule; GFR may fall), so less fluid flows through the distal tubule and collecting duct. With a low flow, the K<sup>+</sup> secreted builds up in the lumen next to the membrane, and the gradient for further secretion falls. The low flow offsets the high aldosterone, and K<sup>+</sup> balance is kept. In a water diuresis the flow is high, which would favour K<sup>+</sup> secretion, but ADH is low, and ADH itself increases the K<sup>+</sup> permeability of the luminal membrane, so the two effects cancel. The two stimuli to aldosterone secretion differ too: angiotensin II (low volume) and a raised plasma K<sup>+</sup>, acting directly on the zona glomerulosa.")}
{mcq("k-q-adx", "Adrenalectomised animals given a constant infusion of aldosterone can regulate their ECF volume on a low-Na<sup>+</sup> diet, but not their plasma K<sup>+</sup>. What does this show?", [
    ("That changes in aldosterone matter more for K<sup>+</sup> balance than for volume, because other mechanisms can regulate Na<sup>+</sup> excretion without them", True, "Yes. Na<sup>+</sup> excretion has many controls (the Starling forces, pressure natriuresis, the renal nerves, angiotensin II on the proximal tubule, ANP), so the loss of a variable aldosterone can be made up. K<sup>+</sup> secretion depends much more on aldosterone, so with a fixed level, plasma K<sup>+</sup> isn’t well regulated."),
    ("That aldosterone has no effect on Na<sup>+</sup> reabsorption", False, "No. Aldosterone does promote Na<sup>+</sup> reabsorption (through ENaC and the Na<sup>+</sup>/K<sup>+</sup>-ATPase), and it was given here; the point is that its variation isn’t needed for volume regulation."),
    ("That the adrenal medulla regulates plasma K<sup>+</sup>", False, "No. Adrenaline does help move K<sup>+</sup> into cells, but the experiment is about varying aldosterone, from the cortex."),
])}
''')
    return chapter("s7-k", num, "Potassium after a meal", "scope", "Optional: potassium after a meal", 15,
                   "Work out what the potassium in a meal would do if it stayed in the extracellular fluid, and find the "
                   "cells that make aldosterone.", body)


def ch_write(num):
    body = f'''
<p class="essay-title">“{ESSAY}”</p>

<h2 id="es7-title">An essay in three parts</h2>
<p>A title with parts (a), (b) and (c) needs each part answered, but three separate mini-essays usually make a weak essay: they repeat themselves, and they miss the point of putting the three together. The point here is a comparison: the same body, the same volume drunk, three different disturbances, and so three different combinations of the osmoregulatory and volume-regulating systems.</p>
<ol class="plan">
<li><b>An introduction that sets up the tools.</b> The compartments and their volumes; the two systems, osmoregulation (osmoreceptors, ADH and thirst: fast, and in charge) and volume regulation (volume receptors, the renin–angiotensin–aldosterone system, ANP, the renal nerves and the physical factors: slower, and subordinate).</li>
<li><b>The same skeleton for each drink.</b> What it does to osmolality and to the volumes (with numbers); what detects it; what the effectors do; how fast; and where the body ends up.</li>
<li><b>Comparisons as you go.</b> Saline engages the system that fresh water doesn’t; seawater engages both, in opposite directions, and shows which one wins.</li>
<li><b>A conclusion that answers the question.</b> What the three cases show together about how the two systems are organised.</li>
</ol>
{mcq("es7-q-plan", "Which plan for this essay is best?", [
    ("Describe ADH, then the renin–angiotensin–aldosterone system, then ANP, and finally say which of them each drink affects", False, "This plan is organised by mechanism, not by the question. It tends to become a list of everything you know, and the three responses get squeezed into the last paragraph."),
    ("Introduce the compartments and the two regulatory systems; take each drink in turn with the same skeleton (disturbance, sensors, effectors, time course, outcome), comparing as you go; conclude on how osmoregulation and volume regulation relate", True, "Yes. It answers each part, the shared skeleton makes the comparisons easy, and the conclusion says what the three cases show."),
    ("Start with seawater, because it’s the most interesting, and mention fresh water and saline briefly at the end", False, "No. All three parts carry marks, and seawater makes most sense once fresh water and saline have been explained."),
])}
{mcq("es7-q-saline", "After a litre of isotonic saline, which of these would you <b>not</b> expect?", [
    ("Renin secretion falls", False, "You would expect it: the expanded volume reduces the renal sympathetic activity and raises the pressure at the afferent arteriole, and more NaCl reaches the macula densa."),
    ("ANP secretion rises", False, "You would expect it: the atria are stretched a little more."),
    ("ADH secretion rises", True, "Right: you wouldn’t expect it. The osmolality hasn’t changed, and the expanded volume, if anything, inhibits ADH a little. A rise in ADH would retain water, the opposite of what’s needed."),
    ("The extra Na<sup>+</sup> takes many hours to excrete", False, "You would expect it: Na<sup>+</sup> excretion responds slowly, and the excess takes up to a day or two to excrete."),
])}

{before_you_start([
    'Numbers help a lot here: the compartments, and what each litre does to them. If you did chapter 1, use your own.',
    'Flow charts like those in the lecture can go in as diagrams, but say in your text what each one shows.',
])}
{write_steps(N, PAPER, 'Plan, then write. Set up the compartments and the two regulatory systems, take each drink in turn with the same skeleton, and finish with what the three show together.')}
{HAND_NOTE}
{after_note()}
{q("es7-q-next", "Once you’ve read the guidance, which part of your essay was weakest: fresh water, saline or seawater? Why?",
   "There’s no single right answer here, so bring yours to the supervision. Essays on this title most often run out of steam on seawater, which needs both systems at once, and on the time course of the response to saline.")}
'''
    return chapter("s7-write", num, "Write your essay", "exam", "Write your essay, and hand it in", None,
                   "This is the work to hand in this week. You write it in Supervision work, as you will in the online "
                   "exam, and then hand it in from the same page.", body)


def ch_more(num):
    body = revision_part(N, REVISION,
                         'These are the renal handout’s other titles on these lectures, and the third of its quotations. Several of them overlap, as exam titles do, so planning two that look alike, and seeing how they differ, is good practice. It’s worth noting them down.',
                         'The titles on the regulation of pH are in Supervision 8.')
    return chapter("s7-more", num, "Revision titles", "exam", "Revision titles", None,
                   "This chapter is optional. It has more essay titles on this week’s lectures, for revision. You can "
                   "hand one in for feedback if you’d like to.", body)


def ALL():
    order = [ch_week, ch_litre, ch_k, ch_write, ch_more]
    return [f(str(i)) for i, f in enumerate(order)]
