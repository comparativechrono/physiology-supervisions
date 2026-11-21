"""The chapters of Supervision 4 (supervision-4.html): the mechanics of the lungs, the pulmonary circulation, and
matching ventilation to perfusion.

The lectures are the first three of the respiration course (an introduction and compliance; airway resistance, the
pulmonary circulation and fluid movement; ventilation and perfusion matching); nothing here is copied from the handout
or the slides. The handout doesn't suggest essay titles, so I wrote the essay's (exams/s4-essay.json), from the course's
learning outcomes for the third lecture, and four revision titles, one or two for each lecture (exams/s4-revision.json),
which can be handed in too.

The chapters: what to do this week; two optional exercises, about half an hour in all (the airways, vessels and alveoli
of the lung in the Microscope; and, in R, why blood from well-ventilated lung can't make up for blood from poorly
ventilated lung); writing the essay and handing it in; and revision titles. ALL() puts them in order.

The numbers were worked out from the equations in R's code (the same in Python): with the Hill equation (P50 26.8 mmHg,
n 2.7), 150 g/L of haemoglobin carrying 1.39 mL O₂ per gram, and 0.03 mL/L of dissolved O₂ per mmHg (the handout's
values), blood from a unit at a PO₂ of 120 mmHg holds about 208 mL/L and from one at 45 mmHg about 169 mL/L; mixed
equally, 189 mL/L, which is the content at a PO₂ of about 60 mmHg, not the 82.5 mmHg average of the two."""
from lib import *
from sup import (HAND_NOTE, after_note, before_you_start, handin_box, how_page_works, name_step, optional_chapter,
                 optional_note, revision_part, titles, write_steps)

N = 4
PAPER = 's4-essay'
REVISION = 's4-revision'
ESSAY = titles(PAPER)[0]
LUNG = 'lung@2.15,1.78,2x'

R_SAT = 'sat <- function(po2) po2^2.7 / (po2^2.7 + 26.8^2.7)'
R_CONTENT = 'content <- function(po2, hb = 150) 1.39 * hb * sat(po2) + 0.03 * po2'
R_CURVE = 'curve(content(x), 0, 150, xlab = "PO2 (mmHg)", ylab = "O2 content (mL per litre)")'
R_UNITS = 'units <- content(c(120, 45)); units'
R_MIXED = 'mixed <- mean(units); mixed'
R_PO2 = 'uniroot(function(p) content(p) - mixed, c(1, 150))$root'


def ch_week(num):
    box = handin_box(N, PAPER, f'“{ESSAY}”', [
        'You write the essay in <b>Supervision work</b>, as you will in the online exam. Plan it first, then write it '
        'in continuous prose, in your own words.',
        'The handout doesn’t suggest titles, so this one is mine. It builds on all three lectures. Chapter 3 is about '
        'using diagrams in an essay, which this title rewards.',
    ], 's4-write')
    body = f'''
{box}

<h2 id="w4-plan">The week, step by step</h2>
<ol class="plan">
<li>If you’d like to, start with <b>two short exercises</b>. They’re optional, and take about half an hour altogether. In chapter 1 you find the airways, vessels and alveoli of a human lung in the <b>Microscope</b>. In chapter 2 you use <b>R</b> to find out why blood from well-ventilated parts of the lung can’t make up for blood from poorly ventilated parts: the heart of your essay. {goto("s4-lung", "start")}</li>
<li>Then <b>write your essay</b> and hand it in (chapter 3). {goto("s4-write", "go there")}</li>
<li>Chapter 4 has four more essay titles on this week’s lectures, for revision. You can hand one in for feedback if you’d like to, but you don’t have to. {goto("s4-more", "go there")}</li>
</ol>
{name_step(N)}
{how_page_works("Chapters 1, 2 and 4 are")}
'''
    return chapter("s4-week", num, "This week", "exam", "Supervision 4: lung mechanics, the pulmonary circulation and V/Q", 5,
                   "This week’s lectures are about what it takes to move air into the lungs (compliance, surfactant and "
                   "airway resistance), the low-pressure circulation that takes blood through them, and how well the "
                   "two are matched.", body)


def ch_lung(num):
    body = optional_chapter(f'''
{optional_note(15, "the first and second lectures, on compliance, airway resistance and the pulmonary circulation")}

<p>This section of human lung has a bronchiole, the branch of the pulmonary artery that runs beside it, and alveoli all round. Some of the alveoli have collapsed, as is common in lung taken after death.</p>
{activity("Airway, artery and alveoli", [
    task("lu-open", f'Open the lung at 2× {scope(LUNG, "show me")}.', auto="scope:open slide=lung"),
    task("lu-br", f'Find the bronchiole {scopefind("lung:bronchiole")}. It’s an airway with no cartilage in its wall, so nothing but the lung round it holds it open.', auto="scope:find slide=lung target=bronchiole ok=true"),
    task("lu-sm", f'Find the smooth muscle in its wall {scopefind("lung:airway-muscle")}.', auto="scope:find slide=lung target=airway-muscle ok=true"),
    task("lu-pa", f'Find the branch of the pulmonary artery beside it {scopefind("lung:pulmonary-artery")}. Compare its wall with the lumen it surrounds.', auto="scope:find slide=lung target=pulmonary-artery ok=true"),
    task("lu-alv", f'Find some alveoli {scopefind("lung:alveoli")}, then measure the width of one open alveolus with the measuring tool {scopetool("measure", "show me")}.', auto="scope:measure slide=lung kind=length"),
])}
{q("lu-q-collapse", "The bronchiole has smooth muscle but no cartilage. What holds it open during a normal breath, and why can airways like it close during a forced expiration, or in emphysema?",
   "It’s held open by the radial traction of the lung tissue attached round it (the alveolar walls pull outwards on it, more strongly as the lung expands), and by the pressure inside it being higher than the pressure round it. In a forced expiration, pleural pressure rises above atmospheric, and the pressure inside the airway falls along its length towards the mouth because of airway resistance. At the equal pressure point the pressure inside equals the pressure outside; downstream of it, the airway is squeezed (dynamic compression), so pushing harder doesn’t raise the flow: expiratory flow becomes effort-independent. Cartilage stops this happening in the large airways, but bronchioles have none. In emphysema the alveolar walls that tether the bronchioles are destroyed, so they lose their radial traction and collapse earlier, trapping air; smooth muscle contraction (asthma) narrows them further.")}
{q("lu-q-laplace", "A water-lined alveolus of radius 100 µm would need a pressure of P = 2T / r to stay open, where T, the surface tension of water, is 0.07 N/m. Work it out in pascals. (1 cmH<sub>2</sub>O is about 98 Pa.) What does surfactant do to this, and why does it matter for small alveoli?",
   "P = 2 × 0.07 / (100 × 10<sup>−6</sup>) = 1400 Pa, about 14 cmH<sub>2</sub>O, from surface tension alone. Surfactant (dipalmitoylphosphatidylcholine, from type II pneumocytes) lowers T, and lowers it more the more the surface is compressed, so as an alveolus shrinks in expiration its surface tension falls and the pressure needed to keep it open doesn’t rise as 1/r would predict. Without surfactant, small alveoli would empty into larger ones and collapse (atelectasis), the lungs would be much stiffer (less compliant), and fluid would be drawn into the alveoli. That’s respiratory distress in premature infants, who haven’t yet made enough surfactant.",
   accept="num:1400±60", placeholder="Pa")}
{mcq("lu-q-pa", "The branch of the pulmonary artery has a thin wall for its size, compared with a systemic artery of the same diameter. Why?", [
    ("The pulmonary circulation is a low-pressure circuit: mean pulmonary arterial pressure is about 15 mmHg, against about 95 mmHg in the aorta", True, "Yes. The whole cardiac output goes through the lungs, but their vascular resistance is about a tenth of the systemic one, so the right ventricle needs only a low pressure. A low pressure needs a thinner wall (Laplace, again). A low pressure also keeps capillary pressure below the colloid osmotic pressure, which protects the lungs from oedema."),
    ("The pulmonary artery carries deoxygenated blood, which needs less muscle to pump", False, "No. The O<sub>2</sub> content of the blood has nothing to do with the pressure, or the wall."),
    ("Pulmonary arteries have no smooth muscle at all", False, "No. They do have some, and it contracts in hypoxia (hypoxic pulmonary vasoconstriction). In species with more of it, such as cattle, altitude causes serious pulmonary hypertension."),
])}
''')
    return chapter("s4-lung", num, "The lung", "scope", "Optional: airways, vessels and alveoli", 15,
                   "Find the parts of a lung that set its resistance, its compliance and its blood supply, and work out "
                   "why surfactant matters.", body)


def ch_vq(num):
    body = optional_chapter(f'''
{optional_note(15, "the third lecture, on ventilation and perfusion matching")}

<p>Imagine a lung with only two units, each receiving half of the blood. One is well ventilated for its blood flow (a high V/Q), so its blood leaves at a PO<sub>2</sub> of 120 mmHg. The other is poorly ventilated (a low V/Q), and its blood leaves at 45 mmHg. What is the PO<sub>2</sub> of the arterial blood, once the two streams have mixed? It isn’t the average of the PO<sub>2</sub>s, because blood mixes by its O<sub>2</sub> content, not its PO<sub>2</sub>. You need the dissociation curve, and R.</p>
{activity("Mixing blood from two units, in R", [
    task("vq-sat", f'Write the oxygen–haemoglobin dissociation curve as a function. This is the Hill equation, with a P<sub>50</sub> of 26.8 mmHg: {rcode(R_SAT)}', auto="r:input kind=rstudio line~sat <- function"),
    task("vq-content", f'Now the O<sub>2</sub> content, in mL per litre of blood, with 150 g/L of haemoglobin that carries 1.39 mL of O<sub>2</sub> per gram, plus what is dissolved (0.03 mL/L per mmHg): {rcode(R_CONTENT)}', auto="r:input kind=rstudio line~content <- function"),
    task("vq-curve", f'Plot it {rcode(R_CURVE)}. Notice where the curve is flat.', auto="r:input kind=rstudio line~curve(content"),
    task("vq-units", f'Work out the content of the blood leaving each unit {rcode(R_UNITS)}, and of the two mixed in equal amounts {rcode(R_MIXED)}.', auto="r:input kind=rstudio line~mean(units"),
    task("vq-po2", f'Find the PO<sub>2</sub> that gives the mixed content {rcode(R_PO2)}. (<code>uniroot</code> finds the PO<sub>2</sub> at which the content minus the mixed content is zero.)', auto="r:input kind=rstudio line~uniroot"),
])}
{q("vq-q-po2", "What is the PO<sub>2</sub> of the mixed blood, to the nearest mmHg? Why is it so much lower than 82.5 mmHg, the average of the two units’ PO<sub>2</sub>s?",
   "About 60 mmHg. The blood from the well-ventilated unit, at 120 mmHg, is on the flat top of the curve: its haemoglobin is already about 98% saturated, so its content (about 208 mL/L) is hardly more than at a normal 100 mmHg. Raising its PO<sub>2</sub> further adds almost nothing. The blood from the poorly ventilated unit, at 45 mmHg, is on the steep part, at about 80% saturation and 169 mL/L. Mixed equally, the content is about 189 mL/L, which on the curve is a PO<sub>2</sub> of about 60 mmHg. So a high V/Q unit can’t make up for a low V/Q one: any mismatch lowers the arterial PO<sub>2</sub>, and the arterial PO<sub>2</sub> is lower than the average alveolar PO<sub>2</sub>, even in a healthy lung (by a few mmHg: a PO<sub>2</sub> of about 100 mmHg in the alveolar capillaries, and about 95 in the systemic arteries).",
   accept="num:60±2", placeholder="mmHg")}
{mcq("vq-q-co2", "In the same lung, the CO<sub>2</sub> of the arterial blood can be kept normal, if the patient breathes harder. Why can high V/Q units make up for low ones for CO<sub>2</sub>, but not for O<sub>2</sub>?", [
    ("The CO<sub>2</sub> dissociation curve is nearly a straight line over the range of PCO<sub>2</sub> in the body, so extra ventilation of the good units lowers their CO<sub>2</sub> content in proportion", True, "Yes. Blowing off more CO<sub>2</sub> from the well-ventilated units lowers their blood’s CO<sub>2</sub> content, and that offsets the high content from the poorly ventilated units. For O<sub>2</sub>, extra ventilation raises the PO<sub>2</sub> of the good units but hardly their content, because haemoglobin is already nearly saturated. That’s why V/Q mismatch typically causes hypoxaemia with a normal or low PCO<sub>2</sub>."),
    ("CO<sub>2</sub> diffuses about 20 times faster than O<sub>2</sub>", False, "CO<sub>2</sub> is more soluble and so diffuses faster, but that’s about diffusion across the barrier, not about how blood from different units mixes. Even with complete equilibration in every unit, the shapes of the two curves decide the result."),
    ("CO<sub>2</sub> doesn’t depend on ventilation", False, "No. Arterial PCO<sub>2</sub> depends directly on alveolar ventilation: it is the variable that ventilation is mainly controlled to keep constant."),
])}
''')
    return chapter("s4-vq", num, "V/Q in R", "rstudio", "Optional: why mismatch lowers the arterial PO₂", 15,
                   "Mix blood from a well-ventilated and a poorly ventilated part of the lung, in R, and find out why "
                   "the good part can’t make up for the bad.", body)


def ch_write(num):
    body = f'''
<p class="essay-title">“{ESSAY}”</p>

<h2 id="es4-title">Using diagrams in an essay</h2>
<p>This title has three parts: why the mismatch exists in a healthy lung, how the lung limits it, and when the lung’s response does harm. Several of its ideas are clearer as a diagram than in words, and a good diagram, used well, earns marks. Used badly, it wastes time. A diagram earns its place when:</p>
<ul>
<li><b>it shows something words can’t do as well</b>: a gradient from the top of the lung to the bottom, the shape of a curve, or how pressures compare in West’s zones;</li>
<li><b>it’s labelled</b>: axes with their quantities and units, the regions named, the key numbers marked;</li>
<li><b>it has a caption</b>, a sentence that says what it shows;</li>
<li><b>the text refers to it and uses it</b>: “As Figure 1 shows, in zone 1 alveolar pressure exceeds arterial pressure, so…”. A diagram the text never mentions might as well not be there.</li>
</ul>
<p>Two or three diagrams are plenty. Some that would help with this title: the distribution of ventilation, blood flow and V/Q from the top of the lung to the bottom; West’s three zones, with P<sub>A</sub>, P<sub>a</sub> and P<sub>v</sub>; and the O<sub>2</sub> dissociation curve, with the two units of chapter 2 marked on it.</p>
{mcq("es4-q-diagram", "Which of these would be the best use of a diagram in this essay?", [
    ("A drawing of the whole respiratory system, from the nose to the alveoli", False, "It might look impressive, but it doesn’t help to answer the question. Nothing in the title turns on the anatomy of the upper airway."),
    ("The O<sub>2</sub> dissociation curve with two lung units marked on it, one at a high V/Q and one at a low V/Q, with the text explaining why mixing their blood lowers the arterial PO<sub>2</sub>", True, "Yes. It shows, at a glance, the point the argument turns on, it’s specific to the title, and the text uses it."),
    ("A table of the lung volumes and capacities", False, "Lung volumes don’t bear on V/Q matching, so a table of them takes time and earns nothing here."),
])}
<ul>
<li><b>Why the mismatch exists.</b> Both ventilation and blood flow increase from the top to the bottom of the upright lung, but for different reasons (the gradient of pleural pressure; hydrostatic pressure, and West’s zones), and blood flow increases more steeply. So V/Q falls from the top (about 3) to the bottom (about 0.6).</li>
<li><b>Why it matters.</b> Chapter 2: low V/Q units lower the arterial PO<sub>2</sub>, and high V/Q units can’t make up for them. Venous admixture (the bronchial circulation, and low V/Q units at the bases) is why arterial PO<sub>2</sub> is lower than alveolar.</li>
<li><b>How the lung limits it.</b> Hypoxic pulmonary vasoconstriction diverts blood from poorly ventilated regions; low PCO<sub>2</sub> constricts the airways of poorly perfused regions. Gravity, posture (prone positioning in ARDS) and disease all change the picture.</li>
<li><b>When the response does harm.</b> In generalised hypoxia (altitude, lung disease) the same vasoconstriction becomes pulmonary hypertension: right ventricular strain and failure (brisket disease in cattle), and high-altitude pulmonary oedema.</li>
</ul>

{before_you_start([
    'To draw a diagram, use <b>Insert drawing</b> (the pencil), or draw it on paper and add a photo of it with <b>Insert picture</b>. Type a caption under it, and refer to it in your text.',
])}
{write_steps(N, PAPER, 'Plan, then write. Use two or three labelled diagrams, each with a caption, and refer to each one in your text.')}
{HAND_NOTE}
{after_note()}
{q("es4-q-next", "Once you’ve read the guidance, did each of your diagrams make a point the text used? Which one could you have done without, and what was missing?",
   "There’s no single right answer here, so bring yours to the supervision. Diagrams in essays most often lose their value by being generic (a picture of the lungs), unlabelled, or never referred to in the text.")}
'''
    return chapter("s4-write", num, "Write your essay", "exam", "Write your essay, and hand it in", None,
                   "This is the work to hand in this week. You write it in Supervision work, as you will in the online "
                   "exam, and then hand it in from the same page.", body)


def ch_more(num):
    body = revision_part(N, REVISION,
                         'These four titles go with this week’s three lectures. It’s worth noting them down: they’re the kind of title you could meet in the exam.',
                         'The handout doesn’t suggest titles, so these are mine, based on the course’s learning outcomes.')
    return chapter("s4-more", num, "Revision titles", "exam", "Revision titles", None,
                   "This chapter is optional. It has four more essay titles on this week’s lectures, for revision. You "
                   "can hand one in for feedback if you’d like to.", body)


def ALL():
    order = [ch_week, ch_lung, ch_vq, ch_write, ch_more]
    return [f(str(i)) for i, f in enumerate(order)]
