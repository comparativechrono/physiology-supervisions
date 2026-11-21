"""The chapters of Supervision 2 (supervision-2.html): blood pressure, the circulation under stress, and when its
control fails.

The lectures are Dr James Fraser's fourth and fifth on the mammalian cardiovascular system (the control of arterial
blood pressure; exercise, haemorrhage and hypoxia) and his lecture on clinical cardiovascular physiology (hypertension,
heart failure, arrhythmia and shock); nothing here is copied from his handouts. The work to hand in is four
short-answer questions (exams/s2-saqs.json), one or two on each lecture. Four revision essay titles
(exams/s2-revision.json) can be handed in too, if a student wants feedback on one.

The chapters: what to do this week; two optional exercises, about half an hour in all (the baroreflex as a young man
stands up, in the Recorder; haemorrhage and heart failure in Guyton's model, examples/circuits/exercise-circulation);
answering the short-answer questions and handing them in; and revision titles. ALL() puts them in order.

The numbers in the model answers were measured in the workbench. The standing-up recording: a beat before he stands
(about 97/53 mmHg, mean 65) and at the lowest pressure after (about 84/38, mean 51), his heart rate rising from about 77
to about 105 a minute. The circuit's meters: a haemorrhage (MSFP 3.5 mmHg) with the heart at 83.3 mL/s, RAP −3.5; at
41.7 mL/s, RAP 0 and ABP 46.5; a failing heart at 50 mL/s with MSFP 7, RAP 2.8 and ABP 55.8; with MSFP raised to 14,
RAP 9.8 and ABP still 55.8."""
from lib import *
from sup import (HAND_NOTE, after_note, before_you_start, handin_box, how_page_works, name_step, optional_chapter,
                 optional_note, revision_part, titles, write_steps)

N = 2
PAPER = 's2-saqs'
REVISION = 's2-revision'
STANDING = 'bp-standing@25,75'       # blood pressure (finger) and heart rate as a young man stands up, at 41 s
MODEL = 'example:exercise-circulation'


def ch_week(num):
    saqs = ''.join(f'<li>{t}</li>' for t in titles(PAPER))
    box = handin_box(N, PAPER, 'Four short-answer questions', [
        f'<ol class="titles">{saqs}</ol>',
        'Each is marked out of five. You answer them in <b>Supervision work</b>, in bullet points, as you would in the '
        'exam. Chapter 3 says what makes a short answer score well.',
    ], 's2-write', noun='questions')
    body = f'''
{box}

<h2 id="w2-plan">The week, step by step</h2>
<ol class="plan">
<li>If you’d like to, start with <b>two short exercises</b>. They’re optional, and take about half an hour altogether. In chapter 1 you watch the baroreflex at work, in the <b>Recorder</b>, as a young man stands up. In chapter 2 you bleed and then weaken the heart of Dr Fraser’s model of the circulation, in the <b>Circuits</b> tab, and see why the right atrial pressure tells the two apart. Both go with the questions you hand in. {goto("s2-stand", "start")}</li>
<li>Then <b>answer the four questions</b> and hand them in (chapter 3). {goto("s2-write", "go there")}</li>
<li>Chapter 4 has four essay titles on this week’s lectures, for revision. You can hand one in for feedback if you’d like to, but you don’t have to. {goto("s2-more", "go there")}</li>
</ol>
{name_step(N)}
{how_page_works("Chapters 1, 2 and 4 are")}
'''
    return chapter("s2-week", num, "This week", "exam", "Supervision 2: blood pressure, stress and failure", 5,
                   "This week’s lectures are about how the arterial blood pressure is controlled, how the circulation "
                   "copes with exercise, haemorrhage and hypoxia, and what happens when the control fails: hypertension, "
                   "heart failure and shock. This week you hand in short answers rather than an essay.", body)


def ch_stand(num):
    body = optional_chapter(f'''
{optional_note(15, "Dr Fraser’s fourth lecture, on the control of arterial blood pressure, and with postural hypotension in his clinical lecture")}

<p>When you stand up, about half a litre of blood pools in the veins of your legs. In this recording a healthy young man stood up by himself from lying flat on a tilt table (the table didn’t move), with his blood pressure measured beat by beat at a finger, and an ECG.</p>
{activity("The baroreflex, beat by beat", [
    task("st-open", f'Open the recording, from 16 s before he stands up to 34 s after {rec(STANDING)}. A flag marks the moment he stands up, and his heart rate is at the bottom. The pressure rises for a beat or two just before the flag, as he braces himself to get up.', auto="rec:open id=bp-standing"),
    task("st-before", f'Choose the <b>Calipers</b> {rectool("calipers", "show me")}. Drag across one beat of the blood pressure from before he stands up, from the lowest point of one pulse to the lowest point of the next, choosing a beat before 37 s. The bar above the traces shows the minimum pressure (the diastolic), the maximum (the systolic) and the mean.', auto="rec:measure id=bp-standing signal=bp to<41 dt>0.5 dt<1.3"),
    task("st-low", 'Do the same for a beat at the lowest pressure, a few seconds after he stands up.', auto="rec:measure id=bp-standing signal=bp from>42 to<50 dt>0.4 dt<1.3"),
])}
{q("st-q-fall", "By how much did his mean pressure fall, and how long did it take to come back? In terms of ABP = CO × TPR and VR = (MSFP − RAP) / RvR, why did it fall?",
   "His mean pressure fell from about 65 mmHg (a beat of about 97/53) to about 51 mmHg (about 84/38) within a few seconds, and it was back within about ten seconds of his standing up. He stood up by himself, so in the first seconds the leg muscles that lifted him dilated their arterioles, as at the start of exercise, and TPR fell. Then, as he stayed upright, about half a litre of blood pooled in the veins of his legs, where the hydrostatic pressure is now high. That blood no longer contributes to filling the heart: venous return and RAP fall, by Starling’s law each beat ejects less, and CO falls.")}
{q("st-q-reflex", "His heart rate rose from about 77 to about 105 a minute within about ten seconds. Which receptors detected the change, by what pathway did the heart rate rise, and what else did the reflex do? Why did the pressure then overshoot for a few beats?",
   "The arterial baroreceptors of the carotid sinus and aortic arch fired less as the pressure fell, and so did the low-pressure receptors of the great veins and atria as central blood volume fell. Less inhibition of the medullary vasomotor areas meant less vagal activity to the sinoatrial node (the fast part of the rise in rate, within a beat or two) and more sympathetic activity: to the heart (rate and contractility), to the arterioles (raising TPR) and to the veins (raising MSFP, and so venous return). The pressure overshot to about 130/70 mmHg because the reflex has delays: the sympathetic constriction of the vessels builds up over several seconds and outlasts the fall it was correcting, so the baroreflex then worked the other way, and his heart rate fell back for a few beats, before both settled, with his heart rate higher than when he lay down.")}
{mcq("st-q-pot", "Postural hypotension is a fall in pressure on standing that the reflex doesn’t correct fast enough. Dr Fraser points out that its key symptom comes from the brain, whereas in a long-lasting hypotension, such as after a haemorrhage, the brain is usually spared. Why the difference?", [
    ("In postural hypotension the brain is above the heart, and its perfusion pressure falls before the reflex can act; in prolonged hypotension, sympathetic vasoconstriction elsewhere diverts flow to the brain, whose own vessels it hardly constricts", True, "Yes. Standing adds a hydrostatic fall of pressure between the heart and the brain, so a transient fall in ABP briefly lowers cerebral perfusion pressure below what autoregulation can cope with: dizziness or syncope. When hypotension lasts, generalised sympathetic vasoconstriction of the gut, kidney, skin and muscle spares the brain, heart and lungs, whose flow is controlled locally."),
    ("Cerebral autoregulation doesn’t work in postural hypotension", False, "No. It works, but only over a range of perfusion pressure, and on standing the pressure at the level of the brain can fall below it for a few seconds."),
    ("The brain has more sympathetic innervation than other organs", False, "No, the opposite: cerebral vessels are hardly constricted by sympathetic activity, which is why sympathetic vasoconstriction elsewhere diverts flow towards the brain."),
])}
''')
    return chapter("s2-stand", num, "Standing up", "recorder", "Optional: the baroreflex as someone stands up", 15,
                   "Measure, in the Recorder, how the blood pressure falls when someone stands up, and how the "
                   "baroreflex brings it back.", body)


def ch_model(num):
    body = optional_chapter(f'''
{optional_note(15, "Dr Fraser’s fifth lecture, on haemorrhage, and his clinical lecture, on heart failure and shock")}

<p>This is the model of the circulation from Supervision 1: MSFP drives venous return through RvR, so that VR = (MSFP − RAP) / RvR, the heart (a flow source) pumps whatever you set, and ABP = CO × TPR. Pressures are in mmHg, flows in mL/s (83.3 mL/s is 5 L/min). A real heart pumps what returns to it (Starling’s law), so in the body RAP stays close to zero; here you set the heart’s output yourself, which lets you see what the body has to do.</p>
{activity("A haemorrhage", [
    task("md-open", f'Open the model {circuit(MODEL, "show me")} and run it {circuitrun("show me")}. At rest, 83.3 mL/s returns and is pumped, RAP is about 0 mmHg and ABP 93 mmHg.', auto="circuit:run name~Guyton"),
    task("md-bleed", 'Lose about a tenth of the blood. Only about the last fifth of the blood volume stretches the vessels’ walls, so without venoconstriction that roughly halves MSFP. Click <b>Mean systemic filling pressure</b> and set it to 3.5 mmHg.', auto="circuit:measure kind=voltmeter label~MSFP value>3 value<4"),
    task("md-bleed-co", 'With the heart still pumping 83.3 mL/s, RAP is now negative, which real veins wouldn’t allow. Click the <b>Heart</b> and set the output that brings RAP back to zero: 41.7 mL/s.', auto="circuit:measure kind=ammeter label~Cardiac value>41 value<42.5"),
])}
{activity("A failing heart", [
    task("md-fail", 'Now put the volume back (MSFP 7 mmHg) and weaken the heart instead. Set the <b>Heart</b> to 50 mL/s (3 L/min), as a failing heart that can’t pump more.', auto="circuit:measure kind=ammeter label~Cardiac value>49 value<51"),
    task("md-fail-msfp", 'The body sees a low pressure and responds as it would to any fall in pressure: venoconstriction, and the kidneys retain salt and water, which raises the blood volume. Raise MSFP to 14 mmHg, and keep the heart at 50 mL/s. Watch RAP.', auto="circuit:measure kind=voltmeter label~MSFP value>13.5 value<14.5"),
])}
{q("md-q-shock", "Compare the haemorrhage (MSFP 3.5 mmHg, heart at 41.7 mL/s) with the failing heart (heart at 50 mL/s, MSFP 14 mmHg). What are ABP and RAP in each? How would measuring RAP help a doctor tell hypovolaemic from cardiogenic shock?",
   "After the haemorrhage, the output that keeps RAP at zero is only 41.7 mL/s (2.5 L/min), so ABP = CO × TPR falls to about 46.5 mmHg, with RAP about 0. With the failing heart, ABP is also low, about 55.8 mmHg (50 mL/s × 1.116), but RAP is high: about 2.8 mmHg with MSFP at 7, and about 9.8 mmHg once MSFP rises to 14. So both are shock (a low pressure and cardiac output), but in hypovolaemic shock RAP (or central venous pressure) is low, because there isn’t enough blood returning, and in cardiogenic shock it’s high, because the heart can’t pump what returns. That decides the treatment: fluid for the first, and not for the second, where more volume would only raise RAP further.")}
{q("md-q-fail", "In the failing heart, raising MSFP from 7 to 14 mmHg didn’t raise the cardiac output at all; it only raised RAP. Why is that a problem, and what does it suggest about how heart failure should be treated?",
   "VR = (MSFP − RAP) / RvR, and if the heart can’t pump more, the output stays at 50 mL/s, so a higher MSFP can only be balanced by a higher RAP: RAP = MSFP − CO × RvR = 14 − 4.2 = 9.8 mmHg. In a real failing heart the Starling curve is flattened, so a large rise in RAP gives only a small rise in output. Raised venous and atrial pressures raise capillary pressure upstream (it follows venous pressure), so fluid filters into the tissues and lungs: oedema, a hallmark of heart failure. Arteriolar constriction also raises TPR, which makes a failing heart work harder and can lower its output further. So the body’s normal responses to a low pressure make heart failure worse, and most drugs for it block them: diuretics and ACE inhibitors (or angiotensin receptor blockers) lower volume and MSFP, β-blockers reduce sympathetic drive, and vasodilators lower TPR.")}
''')
    return chapter("s2-model", num, "Shock and failure", "circuit", "Optional: haemorrhage and heart failure in a model", 15,
                   "Bleed, and then weaken the heart of the model of the circulation, and find out why the right "
                   "atrial pressure tells the two kinds of shock apart.", body)


def ch_write(num):
    good = callout("tip", "Two answers to the same question", (
        "<p><b>“Outline the responses to a haemorrhage.”</b></p>"
        "<p><b>Answer A:</b> “The baroreceptors detect the fall in blood pressure. The sympathetic nervous system is "
        "activated, and the heart rate and blood pressure increase. The kidneys retain water.”</p>"
        "<p><b>Answer B:</b> “• Lost volume lowers MSFP, so venous return, CO and ABP fall. • Seconds: arterial and "
        "low-pressure baroreceptors fire less; less vagal and more sympathetic activity raise heart rate, "
        "contractility, TPR and (by venoconstriction) MSFP. • Minutes: lower capillary pressure draws 0.5–1 L of "
        "tissue fluid into the blood (autotransfusion), so the haematocrit falls. • Tens of minutes: renin, "
        "angiotensin II, aldosterone and ADH, with thirst, restore volume. • Days: plasma proteins (24–48 h) and red "
        "cells (erythropoietin, 5–7 days).”</p>"
        "<p>A has three points, none of them wrong, but none precise. B has more than five, each a mechanism with its "
        "direction and its timescale, and a number where one helps. That’s what earns the marks.</p>"))
    body = f'''
<p>This week you hand in four short answers instead of an essay. A short-answer question is marked against a list of points, so it rewards precision and coverage rather than argument. Each of these is marked out of five.</p>

<h2 id="es2-saq">Answering a short-answer question</h2>
<ol class="plan">
<li><b>Read the verb.</b> “Explain” wants mechanisms (why); “outline” wants the main points, in order; “distinguish” wants the differences, side by side.</li>
<li><b>Count the marks.</b> Five marks means at least five separate, precise points. Bullet points are fine, and quicker to mark.</li>
<li><b>Make each point earn its mark.</b> A mechanism with its direction (“less vagal activity to the sinoatrial node raises the heart rate”), a number (“0.5–1 L of tissue fluid”), or an equation used (“RAP = MSFP − CO × RvR”) is worth more than a general statement (“the body compensates”).</li>
<li><b>Answer the question that’s asked.</b> Don’t write everything you know about the topic. A diagram can save words, if it’s labelled.</li>
</ol>
{good}
{mcq("es2-q-points", "One of the questions asks you to explain why removing the arterial baroreceptors doesn’t raise the mean pressure for long. Which of these is the strongest single point?", [
    ("“The baroreceptors are important in controlling blood pressure.”", False, "It’s true, but it doesn’t answer the question, and it would earn nothing."),
    ("“The baroreflex buffers moment-to-moment changes, but the long-term level of the pressure is set mainly by the kidneys, through the excretion of salt and water.”", True, "Yes. That’s the point the question turns on, stated precisely. A good answer would then add the evidence: after denervation the mean pressure is near normal, but much more variable."),
    ("“Without baroreceptors, the pressure goes up.”", False, "No. That’s what the question asks you to explain doesn’t happen, at least not for long."),
])}

{before_you_start()}
{write_steps(N, PAPER, 'Answer each question in bullet points. Aim for at least five precise points for each one.', noun='questions', words=79)}
{HAND_NOTE}
{after_note('the points each answer is marked against')}
{q("es2-q-next", "Once you’ve read the marking points, which of your answers would have scored least, and what was it missing: a mechanism, a number, or the point the question turned on?",
   "There’s no single right answer here, so bring yours to the supervision. Short answers most often lose marks by staying general (“the body compensates”), by describing what happens without saying how, or by answering a broader question than the one set.")}
'''
    return chapter("s2-write", num, "Your short answers", "exam", "Answer the questions, and hand them in", None,
                   "This is the work to hand in this week: four short-answer questions, written in Supervision work and "
                   "handed in from the same page.", body)


def ch_more(num):
    body = revision_part(N, REVISION,
                         'These four titles go with this week’s three lectures. It’s worth noting them down: they’re the kind of title you could meet in the exam.',
                         'Dr Fraser’s handouts don’t suggest titles, so these are mine. Each needs the equations of the circulation, used to argue.')
    return chapter("s2-more", num, "Revision titles", "exam", "Revision titles", None,
                   "This chapter is optional. It has four essay titles on this week’s lectures, for revision. You can "
                   "hand one in for feedback if you’d like to.", body)


def ALL():
    order = [ch_week, ch_stand, ch_model, ch_write, ch_more]
    return [f(str(i)) for i, f in enumerate(order)]
