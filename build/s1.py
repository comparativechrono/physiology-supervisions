"""The chapters of Supervision 1 (supervision-1.html): the circulation, capillaries, arterioles and cardiac output.

The lectures are Dr James Fraser's first three on the mammalian cardiovascular system (an introduction to the
circulation and capillary exchange; arterioles and the control of capillary blood flow; the determinants of cardiac
output); nothing here is copied from his handout. The work to hand in is an essay (exams/s1-essay.json), on the title I
set: "Discuss the cardiovascular adjustments that occur in whole body exercise." It draws on all three lectures, and
on his fifth. The revision titles (exams/s1-revision.json) can be handed in too, if a student wants feedback on one.

The chapters: what to do this week; two optional exercises, about half an hour in all (the endothelium of a ring of rat
aorta in the Organ bath: Furchgott's experiment, taken a step further with L-NAME and nitroprusside; and Dr Fraser's
two equations run as Guyton's model of the circulation in exercise, examples/circuits/exercise-circulation.circuit.json);
writing the essay and handing it in; and revision titles. ALL() puts them in order.

The numbers in the model answers were measured in the workbench. The ring (seed 4): phenylephrine 10⁻⁶ M, about 1.45 g;
acetylcholine 10⁻⁶ M then relaxes about 83% of that tone; after 20 minutes in L-NAME 10⁻⁴ M, 17 to 19%; nitroprusside
10⁻⁷ M, 91 to 96% (depending on when each is measured; and 94% in a ring without its endothelium, where acetylcholine
relaxes 1%). The circuit's meters: rest, 83.3 mL/s,
RAP 0, ABP 93 mmHg; the muscles' arterioles dilated, ABP 18.6; the heart alone at 417 mL/s, RAP −28; MSFP 17.5 and the
muscle pump, RAP 0 and ABP 93."""
from lib import *
from sup import (HAND_NOTE, after_note, before_you_start, handin_box, how_page_works, name_step, optional,
                 optional_chapter, optional_note, revision_part, titles, write_steps)

N = 1
PAPER = 's1-essay'
REVISION = 's1-revision'
ESSAY = titles(PAPER)[0]

RING = 'aorta?seed=4'                  # the same ring for everyone, so that the numbers match the model answers
MODEL = 'example:exercise-circulation'  # Guyton's model: VR = (MSFP − RAP) / RvR, ABP = CO × TPR


def ch_week(num):
    box = handin_box(N, PAPER, f'“{ESSAY}”', [
        'You write the essay in <b>Supervision work</b>, as you will in the online exam. Plan it first, then write it '
        'in continuous prose, in your own words.',
        'It draws on all three of this week’s lectures, and on what Dr Fraser says about exercise in his fifth.',
    ], 's1-write')
    body = f'''
{box}

<h2 id="w1-plan">The week, step by step</h2>
<ol class="plan">
<li>If you’d like to, start with <b>two short exercises</b>. They’re optional, and take about half an hour altogether. In chapter 1 you repeat, in the <b>Organ bath</b>, the experiment that discovered what the endothelium does to the smooth muscle under it, and take it a step further. In chapter 2 you run Dr Fraser’s equations as a model of the circulation in the <b>Circuits</b> tab, and find out what has to change for the cardiac output to rise five-fold in exercise. Both give you material for your essay. {goto("s1-endo", "start")}</li>
<li>Then <b>write your essay</b> and hand it in (chapter 3). {goto("s1-write", "go there")}</li>
<li>Chapter 4 has three more essay titles on this week’s lectures, for revision. You can hand one in for feedback if you’d like to, but you don’t have to. {goto("s1-more", "go there")}</li>
</ol>
{name_step(N)}
{how_page_works("Chapters 1, 2 and 4 are")}
'''
    return chapter("s1-week", num, "This week", "exam", "Supervision 1: capillaries, arterioles and cardiac output", 5,
                   "This week’s lectures are about how blood reaches the tissues: exchange across the capillaries, how "
                   "the arterioles share out the flow, and what sets the cardiac output. Your essay puts them together, "
                   "in the biggest challenge the circulation meets every day: exercise.", body)


def ch_endo(num):
    body = optional_chapter(f'''
{optional_note(15, "Dr Fraser’s second lecture, on the control of arteriolar smooth muscle")}

<p>In 1980 Robert Furchgott and John Zawadzki noticed that acetylcholine relaxed rings of rabbit aorta only if their endothelium hadn’t been rubbed off by accident. The endothelium, they concluded, releases something that relaxes the muscle under it. You can see the same thing in the <b>Organ bath</b>, and then find out what that something is. The ring here comes from a rat, and everyone gets the same one, so your numbers will match mine. An aorta has no tone of its own in the bath, so you contract it first with phenylephrine, an agonist at the α<sub>1</sub>-adrenoceptors that sympathetic noradrenaline acts on.</p>
{activity("An intact ring", [
    task("en-ring", f'Set up the ring of rat aorta {bath(RING, "show me")}. It runs 20 times faster than real time, because the aorta responds slowly.', auto="bath:setup tissue=aorta endothelium=true"),
    task("en-pe", f'Contract it with phenylephrine at 10<sup>−6</sup> M {bathdo("add phenylephrine 1e-6", "show me")}, and skip to the plateau {bathdo("plateau", "show me")}.', auto="bath:add drug=phenylephrine"),
    task("en-ach", f'Now add acetylcholine at 10<sup>−6</sup> M {bathdo("add acetylcholine 1e-6", "show me")}, skip to the plateau again, and wash the bath out {bathdo("wash", "show me")}. Washing measures the response: the table under the chart shows what fraction of the phenylephrine tone relaxed.', auto="bath:response drug=acetylcholine condition=control pct>50"),
])}
{activity("The same ring, unable to make nitric oxide", [
    task("en-lname", f'Put L-NAME, which inhibits nitric oxide synthase, into the solution you wash the bath with, at 10<sup>−4</sup> M {bathdo("antagonist lname 1e-4", "show me")}. Give it 20 minutes to act {bathdo("wait 1200", "show me")}.', auto="bath:antagonist drug=lname"),
    task("en-lname-ach", f'Contract the ring with phenylephrine again {bathdo("add phenylephrine 1e-6", "show me")}, skip to the plateau, then add acetylcholine at 10<sup>−6</sup> M again {bathdo("add acetylcholine 1e-6", "show me")} and skip to the plateau.', auto="bath:add drug=acetylcholine condition~L-NAME"),
    task("en-snp", f'Without washing, add sodium nitroprusside, which releases nitric oxide itself, at 10<sup>−7</sup> M {bathdo("add nitroprusside 1e-7", "show me")}. Skip to the plateau and wash. The table now has both responses in L-NAME.', auto="bath:response drug=nitroprusside condition~L-NAME pct>50"),
])}
{q("en-q-what", "What did acetylcholine do before and after L-NAME, and what did nitroprusside do? What do the three results show, taken together?",
   "Before L-NAME, acetylcholine relaxed about four-fifths of the phenylephrine tone (about 83%). After 20 minutes in L-NAME it relaxed less than a fifth (17 to 19%), yet nitroprusside then relaxed over 90% of it. So acetylcholine relaxes the muscle by making the endothelium produce nitric oxide: block nitric oxide synthase and the relaxation largely goes. The muscle itself can still relax perfectly well, as nitroprusside shows, because it gives the muscle nitric oxide directly, which activates soluble guanylyl cyclase, raises cGMP and lowers the Ca<sup>2+</sup> sensitivity and Ca<sup>2+</sup> of the muscle. (Acetylcholine acts on M<sub>3</sub> receptors of the endothelium, which raise its Ca<sup>2+</sup> and so activate eNOS.) A ring whose endothelium has been rubbed off behaves like the ring in L-NAME, which is the original observation. That a little relaxation survives L-NAME is consistent with the endothelium having other dilators too, such as prostacyclin and endothelium-derived hyperpolarisation.")}
{mcq("en-q-k", "In the organ bath, KCl at 60 mM contracts the aorta. Yet in exercising muscle, a rise in interstitial K<sup>+</sup> to about 10 mM within seconds dilates the arterioles, and is one of the main causes of the fast phase of functional hyperaemia. Why the difference?", [
    ("A small rise in K<sup>+</sup> hyperpolarises arteriolar smooth muscle, through inward-rectifier K<sup>+</sup> channels and the Na<sup>+</sup>/K<sup>+</sup>-ATPase. A large rise depolarises it", True, "Yes. Raised K<sup>+</sup> activates K<sub>IR</sub> channels and speeds up the Na<sup>+</sup>/K<sup>+</sup>-ATPase, and together they hyperpolarise the cell, close its voltage-gated Ca<sup>2+</sup> channels and relax it. Blocking either (with barium or ouabain) cuts the dilatation by about 60%. At 60 mM, though, E<sub>K</sub> is so much less negative that the cell depolarises whatever its channels do, and the Ca<sup>2+</sup> channels open."),
    ("K<sup>+</sup> releases nitric oxide from the endothelium of arterioles but not of the aorta", False, "No. The mechanism is in the smooth muscle itself, and it doesn’t depend on nitric oxide."),
    ("The aorta has no K<sup>+</sup> channels", False, "No. All smooth muscle has K<sup>+</sup> channels. What differs is how far the K<sup>+</sup> rises."),
])}
{q("en-q-ex", "Nitric oxide is one of many dilators released in exercising muscle. Yet blocking nitric oxide synthase alone changes the size of exercise hyperaemia surprisingly little. Why might that be, and what does it mean for how you write about the mechanisms in your essay?",
   "The maintained phase of exercise hyperaemia has several causes acting at once: K<sup>+</sup>, adenosine (acting on A<sub>2A</sub> receptors, cAMP and K<sub>ATP</sub> channels), ATP and nitric oxide released from red cells as they give up their O<sub>2</sub>, β<sub>2</sub>-adrenoceptor activation by circulating adrenaline, and nitric oxide from endothelium stimulated by the faster flow. They’re redundant: if one is blocked, the others make a bigger contribution, and some changes (a fall in P<sub>O<sub>2</sub></sub>, say) alter the others. So an experiment that blocks one mediator and sees little change doesn’t show that the mediator does nothing. In the essay, distinguish the fast phase, whose causes are clear (K<sup>+</sup> and the muscle pump), from the maintained phase, whose causes overlap, and say what kind of evidence there is for each, rather than listing dilators as if each were the cause.")}
''')
    return chapter("s1-endo", num, "The endothelium", "bath", "Optional: what the endothelium does to arterioles", 15,
                   "Repeat, in the Organ bath, the experiment that showed that the endothelium relaxes the muscle under "
                   "it, and find out how.", body)


def ch_model(num):
    body = optional_chapter(f'''
{optional_note(15, "Dr Fraser’s third lecture, on the determinants of cardiac output, and his fifth, on exercise")}

<p>Dr Fraser’s two equations make a model of the circulation that you can run. The <b>mean systemic filling pressure</b> (MSFP) is a pressure source, which drives venous return to the right atrium through the <b>resistance to venous return</b> (RvR), so that VR = (MSFP − RAP) / RvR. The heart is a flow source, which pumps into the arteries whatever flow you set. The blood flows back through the arterioles, the <b>total peripheral resistance</b> (TPR), so that ABP = CO × TPR. The tab shows pressures in mmHg, flows in mL/s (5 L/min is 83.3 mL/s) and resistances in mmHg·s/mL.</p>
{callout("tip", "A model, not a body", "<p>The veins of this model are rigid, so venous return keeps rising however far the heart pulls RAP down. Real veins collapse once the pressure in them falls 1 or 2 mmHg below zero. A real heart also sets its own output: by Starling’s law it pumps what returns to it, which keeps RAP close to zero. Here you set its output yourself.</p>")}
{activity("Rest, then exercise", [
    task("md-open", f'Open the model {circuit(MODEL, "show me")} and run it {circuitrun("show me")}. Venous return and cardiac output are both 83.3 mL/s (5 L/min), RAP is close to 0 mmHg, and ABP is 93 mmHg.', auto="circuit:run name~Guyton"),
    task("md-muscle", 'Start exercising: click the switch <b>Exercising muscles</b> to close it. That puts the working muscles’ dilated arterioles alongside the others, and TPR falls to a fifth of its resting value. Watch ABP.', auto="circuit:switch label~Exercising on=true"),
    task("md-heart", 'Can the heart put this right on its own? Click the <b>Heart</b>, and in the panel on the right set its flow to 417 mL/s, five times its resting output. Watch RAP.', auto="circuit:measure kind=ammeter label~Cardiac value>400"),
    task("md-veins", 'Now the veins. Click <b>Mean systemic filling pressure</b> and raise it from 7 to 17.5 mmHg, as sympathetic venoconstriction would. Then close the switch <b>Muscle pump</b>, which halves RvR.', auto="circuit:switch label~pump on=true"),
])}
{q("md-q-heart", "With the muscles dilated, ABP fell to about 19 mmHg. With the heart pumping 417 mL/s on its own, ABP was back to 93 mmHg, but what happened to RAP, and why couldn’t a real heart do this? What finally brought RAP back to zero?",
   "ABP = CO × TPR, so with the output unchanged ABP fell to a fifth, about 19 mmHg. Pumping five times as much restores ABP, but RAP falls to about −28 mmHg, because with MSFP and RvR unchanged, VR = (MSFP − RAP) / RvR can only rise five-fold if RAP falls that far: (7 + 28) / 0.084 = 417 mL/s. Real veins collapse long before that, so a heart that pumps harder can’t draw more blood out of them, which is why pacing the heart faster barely raises the cardiac output. Raising MSFP 2.5-fold (venoconstriction) and halving RvR (the muscle pump) lets venous return rise 2.5 × 2 = 5-fold with RAP back at zero. In the body, Starling’s law holds RAP near zero and the output follows venous return; the heart’s faster rate and greater contractility let it pump the larger return without RAP rising.")}
{q("md-q-sv", "Dr Fraser’s handout says that in intense exercise the cardiac output can rise about five-fold, with the heart rate rising about three-fold. By roughly how many times must the stroke volume rise?",
   "CO = HR × SV, so SV must rise by 5 / 3 ≈ 1.7 times. The handout’s figures of a three-fold rise in rate and a 50% rise in stroke volume give 3 × 1.5 = 4.5, close to five-fold. Stroke volume can rise because venous return and filling rise with it, and because sympathetic stimulation makes each beat more forceful, so the ventricle empties further.",
   accept="num:1.67±0.15", placeholder="times")}
{mcq("md-q-control", "In exercise, mean arterial pressure rises slightly, although TPR falls to a fifth. What drives the increase in sympathetic activity and the fall in cardiac vagal activity that achieve this?", [
    ("Mainly the baroreflex, responding to the fall in pressure as the muscles dilate", False, "No. If the baroreflex drove it, pressure would have to fall first and stay a little low. Instead it rises, and the heart rate can rise before exercise starts."),
    ("Central command from the brain, with feedback from the muscles and joints, while the baroreflex is reset to a higher set point", True, "Yes. With the neuromuscular junction blocked by curare, trying to exercise still raises the heart rate, and the rise follows the effort perceived, not the work done. The heart rate even rises in anticipation. The baroreflex still works, but around a higher pressure, which is why the pressure rises a little and stays stable."),
    ("Adrenaline from the adrenal medulla alone", False, "No. Adrenaline helps, and dilates muscle arterioles through β<sub>2</sub>-adrenoceptors, but the fast changes in heart rate and venous tone are neural."),
])}
''')
    return chapter("s1-model", num, "A model of exercise", "circuit", "Optional: exercise in a model of the circulation", 15,
                   "Run Dr Fraser’s two equations as a model of the circulation, and find out what has to change for "
                   "the cardiac output to rise five-fold without the right atrial pressure falling.", body)


def ch_write(num):
    body = f'''
<p class="essay-title">“{ESSAY}”</p>

<h2 id="es1-title">What “discuss” asks of you</h2>
<p>“Discuss” asks for an argument, not a list. A good essay on this title doesn’t just describe each change in exercise. It explains why each one is needed, how it comes about, and how the changes fit together into one response. A useful way in is to see the whole response as solving one problem: the working muscles dilate their arterioles to get the blood they need, and the rest of the circulation has to cope with the consequences.</p>
<ul>
<li><b>In the muscles.</b> How does their blood flow rise, and how fast? What do the fast and the maintained phases of functional hyperaemia depend on, and how good is the evidence for each? What happens at the capillaries?</li>
<li><b>In the whole circulation.</b> What does that do to TPR, and so to ABP? What must the cardiac output do, and how do venous return, the heart rate and the stroke volume rise to match it? Chapter 2 has numbers.</li>
<li><b>The control.</b> What drives the changes in sympathetic and vagal activity, and why couldn’t the baroreflex do it alone? What happens to the blood flow to other organs: the gut, the kidneys, the skin, the heart and the brain?</li>
<li><b>The argument.</b> What, in the end, limits how hard a fit person can exercise? Is it the same for someone with heart failure? An essay that ends on a well-argued point like this is better than one that just stops.</li>
</ul>

<h2 id="es1-slips">Three common slips</h2>
<p>Each of these sentences is the kind that essays on this title often contain. Is each one right? If not, what’s wrong with it?</p>
{mcq("es1-q-symp", "“During exercise, the sympathetic nervous system dilates the arterioles of the working muscles, which increases their blood flow.”", [
    ("It’s right. Sympathetic activity rises in exercise, and it dilates the arterioles of muscle", False, "Not quite. Sympathetic nerves constrict arterioles, through α<sub>1</sub>-adrenoceptors. The working muscles dilate theirs by local mechanisms, despite the sympathetic activity."),
    ("Functional hyperaemia is local. Sympathetic vasoconstriction acts elsewhere, and even partly opposes it in the muscles", True, "Yes. K<sup>+</sup>, adenosine and other local factors dilate the working muscles’ arterioles, and they overcome sympathetic vasoconstriction there. Elsewhere (the gut, the kidneys, inactive muscle) sympathetic vasoconstriction diverts blood towards the working muscles and holds up TPR. In humans, sympathetic cholinergic vasodilator nerves probably play no part, although they do in cats."),
    ("It’s right, but the transmitter is acetylcholine, not noradrenaline", False, "No. Sympathetic cholinergic vasodilator nerves dilate muscle arterioles in cats, but probably not in humans."),
])}
{mcq("es1-q-abp", "“Because total peripheral resistance falls, arterial blood pressure falls during exercise.”", [
    ("It’s right: ABP = CO × TPR, and TPR falls", False, "Not quite. That would be true only if the cardiac output didn’t change."),
    ("Mean ABP rises slightly, because the cardiac output rises more than TPR falls, and the baroreflex is reset to a higher set point", True, "Yes. TPR can fall to a fifth, but the cardiac output rises about five-fold, and central command resets the baroreflex, so mean pressure rises a little. Systolic pressure rises more, because the stroke volume and the force of ejection rise."),
    ("ABP falls at first, and the baroreflex then brings it back to normal", False, "No. The response is set in motion by central command, even before exercise starts. The pressure doesn’t have to fall first."),
])}
{mcq("es1-q-o2", "“In exercise, more oxygen reaches the muscles only because their blood flow rises.”", [
    ("It’s right: O<sub>2</sub> delivery is flow × the O<sub>2</sub> content of arterial blood", False, "Not quite. That’s O<sub>2</sub> delivery, but the muscles can also take more out of each litre of blood that reaches them."),
    ("The muscles also extract more of the O<sub>2</sub> from each litre of blood, so their O<sub>2</sub> uptake rises more than their flow", True, "Yes. By Fick’s principle, O<sub>2</sub> uptake = flow × (arterial − venous O<sub>2</sub> content). More capillaries are perfused, so the distances for diffusion are shorter and the area larger, and the local rise in P<sub>CO<sub>2</sub></sub>, H<sup>+</sup> and temperature shifts the dissociation curve to the right (the Bohr effect), so haemoglobin gives up more of its O<sub>2</sub>."),
    ("The muscles’ O<sub>2</sub> uptake rises only because their myoglobin releases its store", False, "No. Myoglobin buffers the O<sub>2</sub> supply for a few seconds, but its store is tiny compared with what the blood brings."),
])}

{before_you_start([
    'A diagram can help: Guyton’s curves at rest and in exercise, say, or a flow diagram of how the medulla controls the heart and the vessels. Draw it with <b>Insert drawing</b> (the pencil), or draw it on paper and add a photo of it with <b>Insert picture</b>. Type a caption under it, and refer to it in your text.',
    'Equations: type a simple one straight into your text, such as ABP = CO × TPR (× is among the special characters, under <b>Ω</b>). For one with a fraction, use the formula tool, <b>Σ</b>. Say what each equation means, and then use it.',
])}
{write_steps(N, PAPER, 'Plan, then write. Aim for an introduction that says what your essay will argue, paragraphs that each make one point and show how it helps to answer the question, and a conclusion that draws them together.')}
{HAND_NOTE}
{after_note()}
{q("es1-q-next", "Once you’ve read the guidance, which part of the response did your essay explain best, and which did it only describe?",
   "There’s no single right answer here, so bring yours to the supervision. Essays on this title most often describe the changes in the heart and the vessels without saying what drives them, or list local dilators without distinguishing the fast and the maintained phases of hyperaemia. Look for the places where you wrote what happens, and ask whether you also said why, and what the evidence is.")}
'''
    return chapter("s1-write", num, "Write your essay", "exam", "Write your essay, and hand it in", None,
                   "This is the work to hand in this week. You write it in Supervision work, as you will in the online "
                   "exam, and then hand it in from the same page.", body)


def ch_more(num):
    body = revision_part(N, REVISION,
                         'These three titles go with this week’s three lectures, one with each. It’s worth noting them down: they’re the kind of title you could meet in the exam.',
                         'Dr Fraser’s handout doesn’t suggest titles, so these are mine. Each needs the equations of the circulation, used to argue.')
    return chapter("s1-more", num, "Revision titles", "exam", "Revision titles", None,
                   "This chapter is optional. It has three more essay titles on this week’s lectures, for revision. You "
                   "can hand one in for feedback if you’d like to.", body)


def ALL():
    order = [ch_week, ch_endo, ch_model, ch_write, ch_more]
    return [f(str(i)) for i, f in enumerate(order)]
