"""The chapters of Supervision 3 (supervision-3.html): calcium, growth hormone and the adrenal gland.

The lectures are the three of the endocrinology course (calcium homeostasis: parathyroid hormone, vitamin D and
calcitonin; growth hormone and the IGFs; the hypothalamic–pituitary–adrenal axis); nothing here is copied from the
lecture notes. The work to hand in is an essay (exams/s3-essay.json), on one of the titles the notes suggest, which
draws on the second and third lectures: "Compare and contrast the metabolic roles of growth hormone and cortisol." The
other eight titles the notes suggest are the revision titles (exams/s3-revision.json), which can be handed in too.

The chapters: what to do this week; two optional exercises, about half an hour in all (the adrenal gland in the
Microscope and the HPA axis as a diagram that runs, examples/diagrams/hpa-axis.flow.json; growth hormone with its two
receptors, the glucocorticoid receptor, and cortisol beside aldosterone in the Molecules tab); writing the essay and
handing it in; and revision titles. ALL() puts them in order.

The numbers in the model answers were measured in the workbench: the diagram's levels are relative to rest (1). Stress
alone: cortisol settles at about 1.5, ACTH peaks at about 1.7. Cortisol knocked out: ACTH rises to about 2.7. Cortisol
fixed at 3: ACTH falls to about 0.17. ACTH knocked out: cortisol falls to 0, and CRH rises to about 2.8."""
from lib import *
from sup import (HAND_NOTE, after_note, before_you_start, handin_box, how_page_works, name_step, optional_chapter,
                 optional_note, revision_part, titles, write_steps)

N = 3
PAPER = 's3-essay'
REVISION = 's3-revision'
ESSAY = titles(PAPER)[0]
ADRENAL = 'adrenal-gland@1.6,2.4,2x'
HPA = 'example:hpa-axis'


def ch_week(num):
    box = handin_box(N, PAPER, f'“{ESSAY}”', [
        'You write the essay in <b>Supervision work</b>, as you will in the online exam. Plan it first, then write it '
        'in continuous prose, in your own words.',
        'It’s one of the titles in the lecture notes, and it draws on the second and third lectures. Chapter 3 is about '
        'how to write a comparison.',
    ], 's3-write')
    body = f'''
{box}

<h2 id="w3-plan">The week, step by step</h2>
<ol class="plan">
<li>If you’d like to, start with <b>two short exercises</b>. They’re optional, and take about half an hour altogether. In chapter 1 you find the zones of the adrenal cortex in the <b>Microscope</b>, then run the HPA axis as a diagram in the <b>Diagrams</b> tab, and break it as diseases and drugs do. In chapter 2 you look at growth hormone holding its receptors, and at the steroids, in the <b>Molecules</b> tab. {goto("s3-hpa", "start")}</li>
<li>Then <b>write your essay</b> and hand it in (chapter 3). {goto("s3-write", "go there")}</li>
<li>Chapter 4 has the other eight titles from the lecture notes, for revision. You can hand one in for feedback if you’d like to, but you don’t have to. {goto("s3-more", "go there")}</li>
</ol>
{name_step(N)}
{how_page_works("Chapters 1, 2 and 4 are")}
'''
    return chapter("s3-week", num, "This week", "exam", "Supervision 3: calcium, growth hormone and the adrenal gland", 5,
                   "This week’s lectures are about three hormone systems: the control of plasma calcium, growth hormone "
                   "and the IGFs, and the hypothalamic–pituitary–adrenal axis. Your essay compares the two hormones "
                   "that both raise blood glucose in a fast, for different reasons and on different timescales.", body)


def ch_hpa(num):
    body = optional_chapter(f'''
{optional_note(15, "the third lecture, on the hypothalamic–pituitary–adrenal axis")}

<h2 id="hp-gland">The adrenal gland</h2>
{activity("Where cortisol is made", [
    task("hp-open", f'Open the adrenal gland at 2× {scope(ADRENAL, "show me")}. You’re looking at a slice across the gland: a capsule, the cortex inside it, and the medulla in the middle.', auto="scope:open slide=adrenal-gland"),
    task("hp-zf", f'Find the zona fasciculata, which makes cortisol, and click on it {scopefind("adrenal-gland:zona-fasciculata")}. Its cells are in long columns, and look pale and foamy because they’re full of lipid droplets: cholesterol ester, the raw material of steroids.', auto="scope:find slide=adrenal-gland target=zona-fasciculata ok=true"),
    task("hp-med", f'Now find the medulla {scopefind("adrenal-gland:medulla")}.', auto="scope:find slide=adrenal-gland target=medulla ok=true"),
])}
{q("hp-q-flow", "Blood flows inwards, from the capsule through the cortex to the veins of the medulla. Why might it matter that the chromaffin cells of the medulla receive blood that has just passed through the zona fasciculata?",
   "The blood reaching the medulla carries a high concentration of cortisol, much higher than in the general circulation. Cortisol induces PNMT, the enzyme that methylates noradrenaline to adrenaline, so the portal arrangement helps the medulla make adrenaline rather than noradrenaline. It ties the two parts of the gland, of different embryological origins (mesoderm and neural crest), into one stress organ: the medulla answers within seconds to sympathetic preganglionic nerves, and the cortex within minutes to ACTH.")}

<h2 id="hp-axis">The axis as a diagram</h2>
<p>The diagram has the three hormones of the axis, each at its resting level (1). Stress drives CRH from the hypothalamus, which drives ACTH, which drives cortisol, and cortisol feeds back on both the hypothalamus and the pituitary.</p>
{activity("Run it, then break it", [
    task("hp-run", f'Open the diagram {flow(HPA, "show me")} and run it {flowrun("show me")}. Stress starts at 2 hours.', auto="flow:run name~adrenal knocked=0"),
    task("hp-knock", 'Destroy the adrenal cortex, as in Addison’s disease. Click the box <b>Cortisol</b>, choose <b>Knocked out</b> for it in the panel on the right, and run it again. Then put it back to normal, choose <b>Fixed</b> for it instead, at a level of 3, as in a patient taking a glucocorticoid drug, and run it again.', auto="flow:run name~adrenal knocked>0"),
])}
{q("hp-q-addison", "With the adrenal cortex knocked out, what happened to ACTH, and with cortisol fixed at 3? What would you see in a patient with each condition, and why?",
   "With no cortisol, there’s no negative feedback, so CRH and ACTH rise: ACTH settles at about 2.7 times its resting level in the diagram. In Addison’s disease the high ACTH (and other products of pro-opiomelanocortin, POMC, the precursor it’s cut from, including MSH) darkens the skin. The patient also lacks aldosterone, because the whole cortex is destroyed: salt loss, a low blood volume and pressure, and a high plasma K<sup>+</sup>. Without cortisol they can’t maintain blood glucose in a fast or exercise, nor vascular responsiveness to catecholamines (a permissive effect), so a stress such as an infection can cause a fatal collapse. With cortisol fixed at 3, the feedback suppresses ACTH to about a sixth of its resting level (0.17). In a patient on glucocorticoids, the low ACTH lets the zona fasciculata atrophy (ACTH is trophic to it), so stopping the drug suddenly leaves them without cortisol until the axis recovers, which can take months. That’s why the dose is tapered.")}
{mcq("hp-q-evidence", "Which observation from the lecture is the best evidence that cortisol controls ACTH by negative feedback?", [
    ("Removing one adrenal gland makes the other enlarge, slowly; repeated injections of cortisol make the adrenal cortex shrink", True, "Yes. Removing one gland lowers cortisol, so ACTH rises and stimulates the remaining cortex to grow (ACTH is trophic). Giving cortisol suppresses ACTH, and the cortex atrophies. Both changes go in the direction feedback predicts, in opposite directions."),
    ("Cortisol is released in pulses that follow the pulses of ACTH", False, "No. That shows ACTH drives cortisol, the forward part of the axis, not that cortisol feeds back."),
    ("Cortisol has a circadian rhythm, with a surge before waking", False, "No. The rhythm comes from the clock driving CRH, not from feedback."),
])}
''')
    return chapter("s3-hpa", num, "The HPA axis", "scope", "Optional: the adrenal gland and the HPA axis", 15,
                   "Find where cortisol is made, then run the hypothalamic–pituitary–adrenal axis as a diagram, and "
                   "break it as Addison’s disease and glucocorticoid drugs do.", body)


def ch_mol(num):
    body = optional_chapter(f'''
{optional_note(15, "the second and third lectures")}

{activity("Growth hormone and its receptors", [
    task("mo-gh", f'Open growth hormone with its receptors {pdb("3HHR", "show me")}, and colour it by chain {viewer("color chain", "show me")}. One chain is growth hormone, a bundle of four helices. The other two are the parts of two receptor molecules that stick out of the cell.', auto="viewer:loaded id~3hhr"),
])}
{q("mo-q-gh", "One molecule of growth hormone binds two receptors, using two different sites on its surface. The lecture says that the receptors exist as pre-formed dimers. What does the hormone do to them, and how is the signal passed into the cell? Can you think how a drug might block the receptor using this structure?",
   "Growth hormone binds first through a high-affinity site (site 1) to one receptor, then through a second site (site 2) to the other. Because the two receptors are already paired, the hormone doesn’t bring them together so much as rotate and reposition them relative to each other. That moves their intracellular parts so that the JAK2 kinases bound to them phosphorylate each other and the receptor’s tyrosines, which recruits STAT5 and other signalling proteins (and the growth effects partly through IGF-1). A drug can exploit the two sites: pegvisomant is growth hormone with site 1 strengthened and site 2 disabled, so it occupies the receptor pair without activating it. It is used to treat acromegaly.")}
{activity("The steroids", [
    task("mo-gr", f'Open the glucocorticoid receptor’s hormone-binding part, holding dexamethasone {pdb("1M2Z", "show me")}, and show the drug as spheres {viewer("show spheres DEX", "show me")}. It sits deep inside the protein, which closes round it.', auto="viewer:loaded id~1m2z"),
    task("mo-cort", f'Now compare cortisol {viewer("clear; molecule cortisol; only ballstick; color cpk", "show me")} with aldosterone {viewer("clear; molecule aldosterone; only ballstick; color cpk", "show me")}. Look at carbons 11 and 18: cortisol has an OH on carbon 11, and aldosterone has an aldehyde (CHO) on carbon 18 as well.', auto="viewer:molecule name=Aldosterone"),
])}
{q("mo-q-mr", "The mineralocorticoid receptor binds cortisol as well as aldosterone, and there’s far more cortisol in the plasma. How do the cells of the collecting duct respond to aldosterone and not to cortisol? Why can eating a lot of liquorice raise the blood pressure?",
   "The cells of the distal tubule and collecting duct express 11β-hydroxysteroid dehydrogenase type 2 (11β-HSD2), which oxidises the 11-OH of cortisol to a keto group, making cortisone, which doesn’t bind the receptor. Aldosterone escapes, because its 18-aldehyde folds onto its 11-OH (forming a hemiacetal), which protects it from the enzyme. So the receptor in these cells sees aldosterone. Liquorice contains glycyrrhetinic acid, which inhibits 11β-HSD2: cortisol then occupies the mineralocorticoid receptor, the cells reabsorb too much Na<sup>+</sup> (and lose K<sup>+</sup>), extracellular volume rises, and so does the blood pressure, with renin and aldosterone suppressed (apparent mineralocorticoid excess).")}
{mcq("mo-q-steroid", "Cortisol binds a receptor inside the cell, and growth hormone a receptor in the membrane. What follows from that for how quickly each acts?", [
    ("Cortisol’s effects mostly take hours, because the receptor regulates gene transcription; growth hormone’s signalling starts within minutes, although its effects on growth take much longer", True, "Yes. The lecture notes say cortisol may take hours or days to act, as the hormone–receptor complex moves to the nucleus and changes gene expression. That’s why cortisol matters more in long fasts than in the first minutes of hypoglycaemia, where adrenaline and glucagon act fast. Growth hormone’s receptor activates JAK2 at once, but growth itself is slow."),
    ("Cortisol acts faster, because steroids cross membranes easily", False, "Not quite. Crossing the membrane is fast, but what follows, changes in transcription and in protein levels, is slow."),
    ("Both act within seconds", False, "No. Neither is a fast-acting hormone in that sense; adrenaline is."),
])}
''')
    return chapter("s3-mol", num, "Hormones in 3D", "viewer", "Optional: growth hormone and the steroids, in 3D", 15,
                   "See how one growth hormone molecule switches on a pair of receptors, and why the kidney can tell "
                   "aldosterone from cortisol.", body)


def ch_write(num):
    body = f'''
<p class="essay-title">“{ESSAY}”</p>

<h2 id="es3-title">Writing a comparison</h2>
<p>“Compare and contrast” asks for similarities <i>and</i> differences, and the best essays also explain them: why two hormones that both raise blood glucose in a fast should differ in when, and how, they act. Two ways to organise it:</p>
<ul>
<li><b>Hormone by hormone</b>: all about growth hormone, then all about cortisol, then a comparison at the end. It’s easy to write, but the comparison tends to be squeezed into the last paragraph, or left to the reader.</li>
<li><b>Point by point</b>: each paragraph takes one aspect (what triggers secretion, the effects on glucose, on fat, on protein, the timescale, what happens in excess or deficiency) and compares the two hormones on it. It’s harder to plan, but every paragraph compares, so it usually scores better.</li>
</ul>
<p>Whichever you choose, plan it as a table first: one row for each aspect, a column for each hormone, and a column for why they’re alike or differ. Then write from the table.</p>
<ul>
<li><b>What triggers them?</b> Both rise in hypoglycaemia and in stress or exercise. What else releases each one: amino acids, low free fatty acids, sleep, the time of day?</li>
<li><b>Glucose, fat and protein.</b> Both antagonise insulin and spare glucose for the brain. Where do they differ, above all over protein?</li>
<li><b>The paradox.</b> Growth hormone is released in fasting yet makes things grow. How does the body stop it promoting growth when there’s no food? (Insulin, IGF-1 and its binding proteins, FGF21, thyroid hormone.)</li>
<li><b>Timescale and mechanism.</b> A membrane receptor and JAK2, against an intracellular receptor and transcription. Pulses, half-lives and binding proteins.</li>
<li><b>What goes wrong.</b> Acromegaly and Cushing’s syndrome both cause diabetes. Deficiency of both, in a fast or strenuous exercise, can cause fatal hypoglycaemia.</li>
</ul>
{mcq("es3-q-comp", "Which of these is the strongest sentence for a comparison essay?", [
    ("“Growth hormone raises blood glucose. Cortisol also raises blood glucose.”", False, "It states a similarity, but says nothing about how or why. Two facts side by side aren’t yet a comparison."),
    ("“Both hormones spare glucose for the brain in a fast, but in opposite ways for protein: growth hormone conserves muscle protein and draws on fat, whereas cortisol breaks down muscle protein to supply amino acids for gluconeogenesis.”", True, "Yes. It names the shared role, the difference, the mechanism of each, and implies why it matters (growth hormone protects lean tissue; cortisol spends it). That’s a comparison doing work."),
    ("“Cortisol is a steroid hormone made in the zona fasciculata from cholesterol.”", False, "It’s true, but it’s about one hormone only. Unless it’s used to explain a difference (cortisol acts slowly through transcription), it doesn’t compare anything."),
])}

{before_you_start([
    'A table can go into the essay itself, if it helps (the table button in the toolbar). But don’t let a table replace the argument: the prose should still explain the differences.',
])}
{write_steps(N, PAPER, 'Plan, then write. Make every paragraph compare the two hormones on one aspect, and end with a conclusion that says what the comparison shows.')}
{HAND_NOTE}
{after_note()}
{q("es3-q-next", "Once you’ve read the guidance, which aspect of the comparison did your essay handle best, and where did it describe one hormone without comparing it with the other?",
   "There’s no single right answer here, so bring yours to the supervision. Comparison essays most often lose their way by describing each hormone in turn and leaving the comparison to the conclusion, or by listing similarities without explaining the differences.")}
'''
    return chapter("s3-write", num, "Write your essay", "exam", "Write your essay, and hand it in", None,
                   "This is the work to hand in this week. You write it in Supervision work, as you will in the online "
                   "exam, and then hand it in from the same page.", body)


def ch_more(num):
    body = revision_part(N, REVISION,
                         'These are the other titles in the lecture notes: three for each lecture. It’s worth noting them down; several are past Tripos questions.',
                         'The calcium titles go with the first lecture, and come back in the renal lectures, when you meet the kidney’s handling of calcium and phosphate.')
    return chapter("s3-more", num, "Revision titles", "exam", "Revision titles", None,
                   "This chapter is optional. It has the other eight essay titles from the lecture notes, for "
                   "revision. You can hand one in for feedback if you’d like to.", body)


def ALL():
    order = [ch_week, ch_hpa, ch_mol, ch_write, ch_more]
    return [f(str(i)) for i, f in enumerate(order)]
