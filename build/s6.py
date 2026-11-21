"""The chapters of Supervision 6 (supervision-6.html): body fluids, filtration, clearance and water.

The lectures are the first three of human renal physiology (body fluids and the structure of the kidney; filtration,
its regulation and clearance; water handling and the concentrating mechanism); nothing here is copied from the handout
or the slides. The work to hand in is an essay (exams/s6-essay.json), on one of the titles the handout suggests, which
draws on the evidence in all three lectures: "What is the evidence that the kidneys produce urine by a process of
ultrafiltration, followed by fluid reabsorption, involving expenditure by the tubule cells?" The handout's other titles
on these lectures, the old IA question on the second lecture's slides and two of the handout's three quotations are the
revision titles (exams/s6-revision.json), which can be handed in too.

The chapters: what to do this week; two optional exercises, about half an hour in all (the renal cortex in the
Microscope; clearance, the transport maximum and the old IA question about glucose, inulin and PAH, in R); writing the
essay and handing it in; and revision titles. ALL() puts them in order.

The numbers were worked out from the R code (the same in Python): with a GFR of 125 mL/min and a glucose Tmax of
375 mg/min (the handout's values), an effective renal plasma flow of 650 mL/min and a PAH Tmax of 80 mg/min (typical
values), glucose first appears in the urine at 3 mg/mL in this model (no splay), and at 10 mg/mL the clearances are
125 (inulin), 87.5 (glucose) and 133 mL/min (PAH)."""
from lib import *
from sup import (HAND_NOTE, after_note, before_you_start, handin_box, how_page_works, name_step, optional_chapter,
                 optional_note, revision_part, titles, write_steps)

N = 6
PAPER = 's6-essay'
REVISION = 's6-revision'
ESSAY = titles(PAPER)[0]
CORTEX = 'kidney-cortex@2.9,1.1,4x'

R_VALUES = 'gfr <- 125; erpf <- 650; tm_glucose <- 375; tm_pah <- 80'
R_P = 'P <- seq(0.05, 10, by = 0.05)'
R_CLEAR = 'glucose <- pmax(0, gfr * P - tm_glucose) / P; pah <- pmin(erpf * P, gfr * P + tm_pah) / P'
R_PLOT = ('matplot(P, cbind(gfr, glucose, pah), type = "l", lty = 1:3, col = 1, '
          'xlab = "Plasma concentration (mg/mL)", ylab = "Clearance (mL/min)")')
R_LEGEND = 'legend("right", c("inulin", "glucose", "PAH"), lty = 1:3)'
R_END = 'round(c(inulin = gfr, glucose = tail(glucose, 1), pah = tail(pah, 1)), 1)'


def ch_week(num):
    box = handin_box(N, PAPER, f'“{ESSAY}”', [
        'You write the essay in <b>Supervision work</b>, as you will in the online exam. Plan it first, then write it '
        'in continuous prose, in your own words.',
        'It’s one of the titles in the handout, and it asks for evidence: the experiments of all three lectures. '
        'Chapter 3 is about how to use experimental evidence in an essay.',
    ], 's6-write')
    body = f'''
{box}

<h2 id="w6-plan">The week, step by step</h2>
<ol class="plan">
<li>If you’d like to, start with <b>two short exercises</b>. They’re optional, and take about half an hour altogether. In chapter 1 you find renal corpuscles and proximal tubules in the <b>Microscope</b>, and measure one. In chapter 2 you use <b>R</b> to answer an exam question from the days of IA Physiology: why the clearances of glucose, inulin and PAH come together at high plasma concentrations. {goto("s6-cortex", "start")}</li>
<li>Then <b>write your essay</b> and hand it in (chapter 3). {goto("s6-write", "go there")}</li>
<li>Chapter 4 has the handout’s other titles on these lectures, for revision. You can hand one in for feedback if you’d like to, but you don’t have to. {goto("s6-more", "go there")}</li>
</ol>
{name_step(N)}
{how_page_works("Chapters 1, 2 and 4 are")}
'''
    return chapter("s6-week", num, "This week", "exam", "Supervision 6: body fluids, filtration and water", 5,
                   "This week’s lectures are about the body’s fluid compartments, how the kidney filters 180 litres of "
                   "plasma a day and reabsorbs almost all of it, how clearance measures what it does, and how it makes "
                   "urine more or less concentrated than plasma.", body)


def ch_cortex(num):
    body = optional_chapter(f'''
{optional_note(15, "the first lecture, on the structure of the kidney and filtration")}

{activity("The renal cortex", [
    task("cx-open", f'Open the renal cortex at 4× {scope(CORTEX, "show me")}.', auto="scope:open slide=kidney-cortex"),
    task("cx-glom", f'Find a renal corpuscle and click on it {scopefind("kidney-cortex:glomerulus")}: a knot of capillaries, the glomerulus, in a cup, Bowman’s capsule.', auto="scope:find slide=kidney-cortex target=glomerulus ok=true"),
    task("cx-bow", f'Find Bowman’s space, between the glomerulus and the capsule, where the filtrate collects {scopefind("kidney-cortex:bowmans-space")}.', auto="scope:find slide=kidney-cortex target=bowmans-space ok=true"),
    task("cx-pct", f'Find a proximal convoluted tubule {scopefind("kidney-cortex:pct")}. Its cells are tall and stain pink, and its lumen looks fuzzy, because of the brush border.', auto="scope:find slide=kidney-cortex target=pct ok=true"),
    task("cx-measure", f'Measure the diameter of a renal corpuscle with the measuring tool {scopetool("measure", "show me")}.', auto="scope:measure slide=kidney-cortex kind=length"),
])}
{q("cx-q-each", "Your renal corpuscle is probably about 200 µm across. A human kidney has about a million of them, so the two kidneys about two million. If the GFR is 125 mL/min, how much does each glomerulus filter, in nanolitres a minute?",
   "125 mL/min ÷ 2,000,000 = 62.5 × 10<sup>−6</sup> mL/min, about 60 nL a minute for each glomerulus (the number of nephrons varies a lot between people, so this is only a guide). That’s why micropuncture, collecting nanolitres of fluid from single nephrons, was the key to finding out what the tubules do.",
   accept="num:62.5±8", placeholder="nL per minute")}
{q("cx-q-pct", "The cells of the proximal tubule stain pink with eosin largely because they’re packed with mitochondria, and they have a brush border of microvilli. How do these features fit what the proximal tubule does, and what has this to do with the “expenditure by the tubule cells” in your essay’s title?",
   "The proximal tubule reabsorbs about two-thirds of the filtered water and Na<sup>+</sup>, and nearly all the glucose, amino acids and much of the bicarbonate. The brush border gives a huge apical surface area for the transporters (Na<sup>+</sup>-glucose cotransporters, Na<sup>+</sup>/H<sup>+</sup> exchangers). The mitochondria provide ATP for the basolateral Na<sup>+</sup>/K<sup>+</sup>-ATPase, which keeps the cell’s Na<sup>+</sup> low, so Na<sup>+</sup> enters across the apical membrane down its gradient, bringing other solutes with it, and water follows osmotically. So reabsorption is driven by active transport, and it costs energy: the kidneys use 7–10% of the body’s O<sub>2</sub> at rest, and their O<sub>2</sub> consumption rises in proportion to the Na<sup>+</sup> they reabsorb. In stopped-flow perfusions, metabolic poisons (2,4-dinitrophenol) and ouabain cut the reabsorption of fluid from the proximal tubule by about two-thirds (Schatzmann and colleagues, 1958).")}
''')
    return chapter("s6-cortex", num, "The renal cortex", "scope", "Optional: the renal cortex", 15,
                   "Find a renal corpuscle and a proximal tubule in the Microscope, measure the corpuscle, and work out "
                   "what each glomerulus filters.", body)


def ch_clear(num):
    body = optional_chapter(f'''
{optional_note(15, "the second lecture, on clearance and the transport maximum")}

<p>Dr Sage’s slides include “an exam question from the good old days (of IA Physiology)”: <i>why is it that at high plasma concentrations the clearances of glucose, inulin and para-aminohippuric acid are similar?</i> You can see the answer by working out the three clearances in R, over a wide range of plasma concentrations. All three are freely filtered. Inulin is neither reabsorbed nor secreted, glucose is reabsorbed by a carrier with a transport maximum (T<sub>max</sub>), and PAH is secreted by one.</p>
{activity("Three clearances, in R", [
    task("cl-values", f'Set the values: a GFR of 125 mL/min, an effective renal plasma flow of 650 mL/min, and the T<sub>max</sub> of glucose (375 mg/min, from the handout) and of PAH (about 80 mg/min): {rcode(R_VALUES)}', auto="r:input kind=rstudio line~tm_pah <- 80"),
    task("cl-p", f'A range of plasma concentrations, in mg/mL: {rcode(R_P)}', auto="r:input kind=rstudio line~P <- seq"),
    task("cl-calc", f'Work out the clearances of glucose and PAH. Clearance is the rate of excretion divided by the plasma concentration. Glucose excreted is what is filtered (GFR × P) beyond the T<sub>max</sub>; PAH excreted is what is filtered plus what is secreted, up to all of the plasma that flows past the tubules: {rcode(R_CLEAR)}', auto="r:input kind=rstudio line~pmax(0"),
    task("cl-plot", f'Plot all three {rcode(R_PLOT)}, and add a legend {rcode(R_LEGEND)}.', auto="r:input kind=rstudio line~matplot"),
    task("cl-end", f'What are the three clearances at the highest concentration, 10 mg/mL? {rcode(R_END)}', auto="r:input kind=rstudio line~tail(glucose"),
])}
{q("cl-q-why", "Why do the three clearances converge at high plasma concentrations? Answer the old exam question.",
   "At 10 mg/mL they’re 125 (inulin), 87.5 (glucose) and 133 mL/min (PAH), and they’d come closer still at higher concentrations. Inulin’s clearance is the GFR whatever its concentration, because it’s only filtered. Glucose is filtered and reabsorbed by carriers that saturate at their T<sub>max</sub>; at high concentrations the filtered load is far above the T<sub>max</sub>, so the reabsorbed part becomes a small fraction of what’s filtered, and the clearance rises towards the GFR. PAH is filtered and secreted by carriers that also saturate; at low concentrations nearly all of it is cleared from the plasma flowing past the tubules (its clearance is the effective renal plasma flow, 650 mL/min), but at high concentrations the secreted part becomes small beside what is filtered, so its clearance falls towards the GFR. Carrier-mediated transport is limited, filtration isn’t, so at high concentrations filtration dominates for all three.")}
{q("cl-q-threshold", "In this model, at what plasma glucose concentration, in mg/mL, does glucose first appear in the urine? The handout says glucose appears at about 2 mg/mL in a real person. Why the difference?",
   "In the model, glucose is excreted once the filtered load exceeds the T<sub>max</sub>: GFR × P > 375, so P > 375 / 125 = 3 mg/mL (about 17 mM). Real kidneys show splay: the curves of reabsorption and excretion bend gradually instead of meeting the T<sub>max</sub> sharply, because nephrons differ (in length, in the number of carriers, and in their GFR), so some saturate at lower plasma concentrations than others. Glucose therefore starts to appear in the urine at a lower concentration, the renal threshold, of about 2 mg/mL (10–11 mM). That’s why glucosuria is a sign of poorly controlled diabetes.",
   accept="num:3±0.1", placeholder="mg/mL")}
''')
    return chapter("s6-clear", num, "Clearance in R", "rstudio", "Optional: clearance and the transport maximum", 15,
                   "Work out the clearances of inulin, glucose and PAH over a range of plasma concentrations, and answer "
                   "an old exam question.", body)


def ch_write(num):
    body = f'''
<p class="essay-title">“{ESSAY}”</p>

<h2 id="es6-title">Using experimental evidence</h2>
<p>This title asks for <b>evidence</b>, so an essay that describes how the kidney works, however accurately, misses the point. Every paragraph should rest on an experiment or an observation, and say what it shows. A useful pattern, for each piece of evidence:</p>
<ol class="plan">
<li><b>The claim</b> it supports: “The fluid in Bowman’s space is an ultrafiltrate of plasma.”</li>
<li><b>The experiment</b>, briefly: who, on what, and what they did. “Wearn and Richards (1924) collected fluid from Bowman’s capsule of frogs by micropuncture.”</li>
<li><b>The result</b>, with a number if there is one. “It had the composition of plasma, but almost no protein.”</li>
<li><b>The inference</b>: why the result supports the claim, and what else it rules out.</li>
<li><b>Its limits</b>, where they matter: frogs aren’t mammals; one nephron isn’t the whole kidney.</li>
</ol>
<p>The title has three claims, so the essay can take them in turn: <b>ultrafiltration</b> (micropuncture of the capsule; the dependence of filtration on pressure; the structure of the barrier), <b>reabsorption</b> (GFR, measured with inulin, is 125 mL/min but urine flow about 1; changes in the composition of the fluid along the tubule; inulin concentration rising along the proximal tubule while the osmolality stays the same; the split-oil-drop experiments), and <b>expenditure by the tubule cells</b> (reabsorption against gradients, metabolic poisons and ouabain cutting fluid reabsorption, the O<sub>2</sub> the kidney consumes).</p>
{mcq("es6-q-evidence", "Which sentence uses evidence best?", [
    ("“The proximal tubule reabsorbs about two-thirds of the filtrate.”", False, "It’s true, but it’s a statement of fact, not evidence. How do we know?"),
    ("“In micropuncture samples, the concentration of inulin rises about three-fold along the proximal tubule while the osmolality stays equal to plasma’s. Inulin isn’t reabsorbed, so about two-thirds of the filtered water, and with it an isosmotic amount of solute, must have been reabsorbed by the end of the proximal tubule.”", True, "Yes. It gives the measurement, the reason inulin is a valid marker, and the inference, and the inference follows from the numbers."),
    ("“Many experiments have shown that the kidney reabsorbs water.”", False, "No. It’s vague: which experiments, and what did they show?"),
])}
{mcq("es6-q-energy", "Schatzmann and colleagues (1958) perfused single proximal tubules with fluid held between oil drops. In 20 minutes, 27% of the fluid was reabsorbed normally, but only about 10% with 2,4-dinitrophenol or with ouabain. What does this show?", [
    ("That fluid reabsorption depends on metabolism and on the Na<sup>+</sup>/K<sup>+</sup>-ATPase: active transport of Na<sup>+</sup> drives the reabsorption of water", True, "Yes. DNP uncouples oxidative phosphorylation, and ouabain blocks the Na<sup>+</sup>/K<sup>+</sup>-ATPase; both cut reabsorption by about two-thirds. So the tubule cells spend energy to reabsorb, and that energy goes into pumping Na<sup>+</sup>: water follows the solute osmotically. Some reabsorption remains, which a good essay could discuss."),
    ("That water is pumped actively across the tubule", False, "No. There’s no water pump. The poisons stop Na<sup>+</sup> transport, and water follows the solute."),
    ("That ultrafiltration needs energy", False, "No. These were perfusions of single tubules, so filtration wasn’t involved; the energy for filtration comes from the heart, as the pressure in the glomerular capillaries."),
])}

{before_you_start([
    'Name experiments by their authors and dates where you can, as in the lectures, but don’t worry if you can’t remember a date: what was done and what it showed matter more.',
])}
{write_steps(N, PAPER, 'Plan, then write. Take the title’s three claims in turn, and make each paragraph rest on a piece of evidence: the experiment, the result and what it shows.')}
{HAND_NOTE}
{after_note()}
{q("es6-q-next", "Once you’ve read the guidance, which of your paragraphs described the kidney without giving the evidence for what it said?",
   "There’s no single right answer here, so bring yours to the supervision. Essays on this title most often slip from evidence into description, especially on reabsorption, and give the experiments without saying what each one rules in or out.")}
'''
    return chapter("s6-write", num, "Write your essay", "exam", "Write your essay, and hand it in", None,
                   "This is the work to hand in this week. You write it in Supervision work, as you will in the online "
                   "exam, and then hand it in from the same page.", body)


def ch_more(num):
    body = revision_part(N, REVISION,
                         'These are the handout’s other titles on this week’s lectures, the old IA question from the second lecture’s slides (which you answered in R in chapter 2, if you did it), and two of the handout’s three quotations. It’s worth noting them down.',
                         'The handout’s titles on the next two renal lectures (extracellular fluid volume, sodium, calcium and potassium), and its third quotation, are in Supervision 7.')
    return chapter("s6-more", num, "Revision titles", "exam", "Revision titles", None,
                   "This chapter is optional. It has more essay titles on this week’s lectures, for revision. You can "
                   "hand one in for feedback if you’d like to.", body)


def ALL():
    order = [ch_week, ch_cortex, ch_clear, ch_write, ch_more]
    return [f(str(i)) for i, f in enumerate(order)]
