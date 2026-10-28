---
name: 100m-leads
description: Build or critique a lead-generation plan using Alex Hormozi's $100M Leads method (the Core Four). Use this skill whenever the user wants to get more leads, customers, clients, appointments, or sales opportunities for any product or service, even if they never say "Hormozi" or "leads". Trigger on requests to create a lead magnet, plan outreach (warm or cold), plan content marketing, plan or fix paid ads, build a referral or affiliate program, decide which marketing channel to use, or scale an existing channel. Also trigger on phrases like "I need more clients", "how do I get customers", "my pipeline is dry", "nobody knows we exist", "should I run ads or post content", "my ads aren't profitable", "how many DMs should I send", "help me grow my audience", or when the user pastes an ad, a DM script, a content plan, or a funnel and asks why it isn't producing leads. Produces a structured Leads Brief document with a one-page advertising plan.
---

# $100M Leads: engaged-lead machine builder and critic

This skill turns Alex Hormozi's $100M Leads (Acquisition.com Volume II, 2023) into a repeatable process. The output is always a **Leads Brief**: a complete, structured document ending in a one-page advertising plan the user can execute starting tomorrow.

Hormozi's one-line thesis: **engaged leads are the true output of advertising**. A lead is just a person you can contact. An engaged lead is a person who has shown interest in what you sell. Everything below exists to produce more engaged leads on purpose, with known inputs and measured outputs.

This skill is the sibling of the `100m-offers` skill. Offers answers "what do I sell and how do I package it"; this skill answers "how do I get strangers to want it". If the user's real problem is the offer itself (nobody buys even when they hear it), say so and point at the offers method; a great advertising plan for a weak offer wastes money.

## Two modes

Decide which mode applies from the request, then follow it. Both end with the same Leads Brief.

| Mode | When | What you do |
|---|---|---|
| **Build** | User wants leads, customers, growth, or a channel plan | Run the 8-stage build below |
| **Critique** | User has existing advertising: an ad, outreach script, content plan, funnel, referral program | Score it with `references/critique-rubric.md`, then rebuild the weak parts using the same stages |

If the user pastes an ad or script and asks "why isn't this working?", that is Critique mode. If they say "I need more clients", that is Build mode.

## Ground rules (read these, they shape every output)

1. **Never invent facts.** Do not make up response rates, conversion rates, CACs, industry averages, audience sizes, or results. Use only what the user gave you, plus the book's own stated benchmarks, which must be labelled as such (for example "book benchmark: ~1 in 5 warm contacts engage"). Where a number is needed and missing, either ask or clearly label it `[assumption: ...]`.
2. **Ask before you build, but not too much.** Read `references/intake.md`. Ask only what you cannot infer. If the user is unavailable (scheduled run, "just draft something"), state assumptions at the top and proceed.
3. **Volume before cleverness.** The book's central diagnosis is that most advertising "failures" are effort failures: 300 flyers instead of 5,000 a day, 100 reach outs over six weeks instead of 100 a day. Before proposing a new channel or a clever tweak, check whether the user is doing anywhere near the required volume. "The right action in the wrong amount still fails."
4. **Inputs you control, outputs you measure.** Every recommendation must name a daily input the user controls and the output metric that tells them it is working. A plan without numbers is a wish.
5. **Give before you ask.** Lead magnets, free content, and big fast value are the engine of the whole method. When in doubt, recommend giving away more, not less: "make your lead magnets as good as your paid stuff."
6. **Write plainly.** No em dashes. No hype adjectives standing in for substance. Short sentences. The brief should read like a sharp operator wrote it, not a marketer.

## The 8-stage build

Stage 3 tells you which method reference files to read. Do not load all four method files when the plan only uses one or two.

### Stage 1. Diagnose the current state

Establish, from intake: what they sell and to whom, current price and rough lifetime gross profit per customer (LTGP: all the money a customer ever spends minus the cost to deliver it), what advertising they do today and at what daily volume, how many engaged leads and customers that produces, and whether they have more time than money or more money than time.

Compute or estimate LTGP to CAC if the data exists. The book's benchmark, stated as Hormozi's observed pattern rather than a law: businesses struggle below **3:1 LTGP to CAC** and take off above it. If CAC is more than 3x the industry average the problem is advertising; if it is within 3x, the bigger lever is the business model (raise LTGP). If engaged leads are qualified and still not buying, that is a sales problem, not an advertising problem; say so instead of prescribing more leads.

Output for this stage: a short table of current inputs, outputs, and the single constraint.

### Stage 2. Engage: design the lead magnet (or confirm the core offer)

Rule from the book: try advertising the core offer first; if engagement is too expensive or too thin, build a lead magnet. Read `references/lead-magnets.md` and run the seven steps: narrow problem, one of three types (reveal their problem, sample or trial, one step of a multi-step process), one of four delivery vehicles (software, information, service, physical product), tested name, easy to consume, so good they would pay for it, and a clear CTA with a real reason to act now. The lead magnet must reveal the next problem that the core offer solves.

### Stage 3. Pick the method(s)

The Core Four is a 2x2: warm or cold audience, one-to-one or one-to-many.

| | Warm (know you) | Cold (strangers) |
|---|---|---|
| **One-to-one** | Warm outreach | Cold outreach |
| **One-to-many** | Post free content | Paid ads |

Selection logic from the book: everyone starts with warm outreach (it is the cheapest, most reliable first customers). Then, **more time than money → post content; more money than time → cold outreach or paid ads**. Paid ads come last because they cost money and the skills from the other three transfer into them. Pick ONE primary method to maximize, keep warm outreach running, and note free content's multiplier effect: it warms up every other channel (the book's survey found 78% of buyers had consumed at least two long-form pieces before booking a call).

Read only the reference files for the chosen methods: `references/warm-outreach.md`, `references/content.md`, `references/cold-outreach.md`, `references/paid-ads.md`.

### Stage 4. Build the method playbook

For each chosen method, produce the concrete playbook from its reference file: the lists, scripts, cadences, and daily numbers, filled in with the user's avatar, offer, and constraints. Scripts must be ready to send, not templates about templates. Personalization slots stay visibly marked so the user knows what to customize per lead.

### Stage 5. Commit the volume: Rule of 100 or Open To Goal

Every plan names its daily commitment. Rule of 100: 100 primary actions per day for 100 days (100 warm or cold reach outs; 100 minutes of content creation with at least one post; 100 minutes making ads and 100 days running them). Open To Goal is the stronger version: commit to outcomes per day (for example 5 booked calls) and work until hit, however long it takes. Pick one, state it in the brief, and translate it into hours so the user sees the real cost. The book's floor when starting out: getting customers takes the majority of your time, think four hours a day minimum.

### Stage 6. Do the math: benchmarks and payback

Using the user's numbers plus labelled book benchmarks, project the funnel: actions per day → engaged leads → customers → revenue. Show the arithmetic in the brief so the user can replace any figure. Check two ratios: LTGP to CAC of at least 3:1, and 30-day cash. Client Financed Acquisition is the scaling unlock: if a new customer pays back the cost to acquire plus fulfill within 30 days (the interest-free credit-card window), money stops being the bottleneck. If the model cannot do that, propose the fix the book uses: an immediate upsell or a higher-cash front-end offer.

### Stage 7. Scale: More, Better, New (in that order)

More: double the inputs before touching anything else; the biggest gains come from advertising more. Better: find the constraint, the step in the funnel where the most leads drop off, and test one thing per week per platform against it; log every test; if four tries in a month cannot beat the control, move to the next constraint. New: only when more and better return less than a new placement would; order of adoption is new placements → new platforms → new Core Four method. Full detail in `references/scaling.md`.

### Stage 8. Lead getters (when the user is past doing it all themselves)

When the user has customers and revenue, add the people who advertise for them, in the book's natural order: customer referrals first, then employees, then agencies, then affiliates. Read `references/lead-getters.md` for the referral math and the seven ways to ask, the 3Ds training framework, the agency learn-then-internalize play with its exact script, and the six-step affiliate build with Whisper-Tease-Shout. Skip this stage for a brand-new business and say why: the roadmap's level for them is warm outreach and content, not affiliates.

## Output: the Leads Brief

Fill in `assets/leads-brief-template.md` exactly. Every section must be present; if the user's context genuinely does not support a section, write what is missing and what they need to supply rather than dropping the heading. Deliver it as a markdown file (and as .docx or .pdf if the user asks; use the docx or pdf skills for that).

The brief ends with the **One-Page Advertising Plan**: lead type targeted, Rule of 100 or Open To Goal commitment, the daily checklist, the metric reviewed weekly, and the trigger for hiring the work out ("do this daily until you can afford to pay someone else to do it, then repeat the process to get employees").

### Final self-check before delivering

1. **Every number is either the user's, a labelled book benchmark, or a labelled assumption.** Read the brief once looking only at digits and percentages. Anything you introduced gets `[assumption: ...]` or "book benchmark:" inline.
2. **Every recommended action has a daily quantity and an owner.** "Post more content" fails this check; "record one 90-second video per weekday, publish at 9am, 100 minutes total" passes.
3. **Scripts are complete.** Any script in the brief can be sent as-is after filling the marked personalization slots. No "[insert value proposition here]".
4. **The give:ask ratio survives.** If the plan involves content, count the gives and asks you scheduled; keep at least 3:1 and prefer far more give when the audience is small.

## Critique mode specifics

1. Read `references/critique-rubric.md`.
2. Identify which of the Core Four the material belongs to, and read that method's reference file.
3. Score the material on every applicable rubric line (0 to 2) with one-line evidence, quoting the user's own copy where possible.
4. Name the single biggest leak. Check volume first: most "this channel doesn't work" complaints are volume failures (the book's example: 100 reach outs over six weeks is 1/42 of the prescribed amount).
5. Rebuild the weak parts using the build stages, keep what scored 2, and say so.
6. Present a before/after: current inputs and outputs versus projected inputs and outputs with the fixes, all assumptions labelled.

## Worked example (compressed)

Input: "I run a B2B bookkeeping firm for dentists. I post on LinkedIn twice a month and get maybe one inquiry. I have about 900 LinkedIn connections and 4 hours a day I could spend. No ad budget."

Build mode. Stage 1: inputs are 2 posts/month, output ~1 engaged lead/month; constraint is volume, not channel. More time than money. Stage 2: lead magnet, type "reveal their problem": a free Practice Cash-Flow Scorecard (service delivery: he reviews their P&L and returns three findings), revealing the problem his monthly service solves. Stage 3: warm outreach (900 connections, untouched) plus content on LinkedIn. Stage 4: warm outreach playbook with the ACA framework and the book's referral-framed script filled in for dentists; content playbook of one post per weekday using hook-retain-reward with dental-specific topics. Stage 5: Rule of 100: 100 personalized reach outs a day is too many for 900 connections, so 45 reach outs a day (list exhausted in ~20 working days, follow up 3x, then recycle in 3 months, labelled as an adaptation of the book's cadence to list size) plus 100 minutes of content. Stage 6: book benchmark ~1 in 5 engage, ~1 in 5 of those take the free scorecard, 1 in 4 of those convert: 900 contacts → ~180 replies → ~36 scorecards → ~9 clients [assumption: conversion between the book's stated 1-in-4-free-offer-takers example and his close rate; replace with his real numbers after the first 100]. Stage 7: after the list is exhausted, More = second platform for the same content; Better = test the scorecard name first. Stage 8: skipped, and the brief says why: referrals become the focus at the book's Level 4, once 25% of customers come from referrals.

Note what did not happen: no invented response rates presented as facts, no paid ads recommended to a user with no budget, and no affiliate program for a solo operator.
