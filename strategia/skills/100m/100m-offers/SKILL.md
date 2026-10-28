---
name: 100m-offers
description: Build or critique a business offer using Alex Hormozi's $100M Offers method (Grand Slam Offer). Use this skill whenever the user wants to create, price, package, name, improve, audit, or rewrite an offer, package, program, membership, retainer, bundle, guarantee, bonus stack, or pricing for any product or service, even if they never say "Hormozi" or "Grand Slam". Also trigger on phrases like "what should I charge", "how do I make this a no-brainer", "nobody is buying", "my offer isn't converting", "help me package my service", "productize my consulting", "add a guarantee", "name my program", or when the user pastes a sales page, pricing page, or pitch and asks whether it is compelling. Produces a structured Offer Brief document.
---

# $100M Offers: Grand Slam Offer builder and critic

This skill turns Alex Hormozi's $100M Offers method (the book plus the frameworks in his handwritten $100M Journal) into a repeatable process. The output is always an **Offer Brief**: a complete, structured document the user can take straight into a sales page, pitch deck, or sales call.

Hormozi's one-line definition: make people an offer so good they would feel stupid saying no. Everything below exists to engineer that feeling on purpose rather than hoping for it.

## Two modes

Decide which mode applies from the request, then follow it. Both end with the same Offer Brief.

| Mode | When | What you do |
|---|---|---|
| **Build** | User has a product, service, or idea and wants an offer | Run the 8-stage build below |
| **Critique** | User has an existing offer, sales page, pricing page, or pitch | Score it with `references/critique-rubric.md`, then rebuild the weak parts using the same 8 stages |

If the user pastes an existing offer and asks "is this good?", that is Critique mode. If they say "help me sell X", that is Build mode.

## Ground rules (read these, they shape every output)

1. **Never invent facts.** Do not make up market sizes, conversion rates, customer quotes, testimonials, competitor prices, or results. Use only what the user gave you. Where a number is needed and missing (price anchors, cost to deliver, current close rate), either ask, or clearly label it `[assumption: ...]` so the user can replace it. A fabricated proof point inside an offer is worse than none, because it destroys the "perceived likelihood of achievement" the moment a prospect checks.
2. **Ask before you build, but not too much.** Read `references/intake.md`. Ask only the questions whose answers you cannot infer from what the user already said. If the user is clearly unavailable (scheduled run, "just draft something"), state your assumptions at the top and proceed.
3. **Psychology over logic.** Hormozi's rule: if the problem were logical it would already be solved. Approach every stage from how the prospect feels, not from a feature list.
4. **Perception is reality.** Value that is not communicated does not exist for the buyer. Every stage of the build must show up in the final brief in words the prospect would read.
5. **Write plainly.** No em dashes. No hype adjectives standing in for substance. Short sentences. The brief should read like a sharp operator wrote it, not a marketer.

## The 8-stage build

Read `references/frameworks.md` for the theory behind stages 1 to 4 and `references/enhancers.md` for stages 5 to 7. Do not skip stages; a Grand Slam Offer fails when one problem is left unsolved or one enhancer is missing.

### Stage 1. Market check (starving crowd)

Before touching the offer, confirm the market passes four tests: massive pain, purchasing power, easy to target, growing. Every durable market is a branch of health, wealth, or relationships. If the market fails a test, say so bluntly and suggest a niche that passes. Niche down: the more specific the avatar, the more you can charge (Hormozi's example ladder goes from a generic "time management course" to "time management for outbound B2B power tool sales reps", and the price rises roughly tenfold with each step of specificity).

Output for this stage: a one-paragraph avatar description and a pass/fail on the four tests.

### Stage 2. Dream outcome

People do not want the product, they want the outcome and the status it brings. Write the dream outcome in the prospect's own words, then write the status version (how will they be seen by others afterwards). Both go in the brief.

### Stage 3. Value equation audit

Value = (Dream Outcome × Perceived Likelihood of Achievement) ÷ (Time Delay × Effort and Sacrifice).

For the product as it stands today, score each of the four variables from 1 to 5 and write one sentence on why. This becomes the "before" column in the brief and tells you which levers the rest of the build must pull. The bottom two (time and effort) are the hardest to move and the most valuable when moved: "fast beats free".

### Stage 4. Problems, solutions, delivery vehicles, trim and stack

This is the core of the method and deserves the most space.

1. **List every problem** the prospect hits immediately before, during, and after using the product. Go wide: at least 10 to 15. For each, note which of the four value-equation variables it damages (for example "buying healthy food takes time" damages Time Delay and Effort).
2. **Flip each problem into a solution statement**: "How to [get the good thing] without [the pain]".
3. **Choose a delivery vehicle for each solution** using the cheat codes in `references/frameworks.md` (attention level, effort level, medium, speed of response, and the "10x price / one-tenth price" thought experiments).
4. **Trim and stack.** Plot each vehicle on the value/cost matrix. Cut low-value items regardless of cost. Keep high-value low-cost items (these are usually one-time builds like guides, calculators, templates). Keep high-value high-cost items only if you can find a way to lower their cost (group instead of 1-on-1, recorded instead of live). The survivors become the deliverables.

Give each deliverable a benefit-led name and a stated value, and justify the value in one line (time saved, money saved, what it would cost to buy separately). The sum of stated values should dwarf the price.

### Stage 5. Pricing

Read the pricing section of `references/frameworks.md`. Rules that must show up in the brief:

- Price on value delivered, not on cost or on the market average. Never be the second cheapest. If you cannot be 10x cheaper, do not compete on price.
- Raise the price until the stated value is still at least 10x the price (Hormozi's target: sell $100k of value for $10k).
- State the price anchor (what the pieces would cost separately, or what the outcome is worth) before the price.
- Decide the money model terms from the journal's list: how long, when they pay, what they get, how they know they will get it, incentive to act today, what they have to do.
- Consider tiered pricing with deliberately restricted supply at the top tier (the journal's example: 2 spots at $5,000 beats 10 at $500, and the unserved buyers become next launch's pent-up demand).

Show the virtuous cycle of price table from the frameworks file when the user pushes back on a high price.

### Stage 6. Enhancers: scarcity, urgency, bonuses

From `references/enhancers.md`:

- **Scarcity** (quantity): pick one honest mechanism. Limited spots, limited cohort size, limited bonus supply, or never-available-again. It must be true; fake scarcity destroys the guarantee's credibility too. Scarcity can only come from a constraint the user actually has (hours, seats, cohort dates, stock). If the user gave you no such constraint, do not invent one. Write the mechanism with a placeholder, for example "X seats per cohort, where X is the number of submissions you can personally review in a week", and flag it as the first thing they must fill in.
- **Urgency** (time): cohort-based rolling, seasonal deadline, price or bonus expiry, or exploding opportunity. Deadlines must be real and enforced.
- **Bonuses**: break the offer into named components and present them as bonuses rather than as one lump. Each bonus must attack one specific objection or obstacle. Name it with the benefit in the title, state its value, and if useful add other people's products at negotiated free or discounted access. Bonuses beat discounts because discounts teach prospects that the price is negotiable.

### Stage 7. Guarantee

Read the guarantee section of `references/enhancers.md` (12 guarantee types from the journal plus the four categories from the book). Use the journal's recipe: list the pains and obstacles prospects raise in the sale, reverse each one into a promise, and make it specific. Format: "If you don't achieve X in Y time, we will Z." Name the guarantee. Stack two if the risk profile warrants it (for example a results guarantee plus a service guarantee). If the product genuinely cannot be guaranteed, use the anti-guarantee and explain why it is a strength.

### Stage 8. Name it

Use the MAGIC formula and the headline formula word banks in `references/enhancers.md`. Produce 5 name options: (Enhancer) + (Avatar) + (Duration) + (Dream Outcome) + (Container word). You do not need every piece. Shorter, more specific, rhyming, or alliterative wins. Recommend one and explain why. Remind the user that when the name fatigues, they change the wrapper, not the offer ("same bundle, different wrapper").

## Output: the Offer Brief

Fill in `assets/offer-brief-template.md` exactly. Every section of the template must be present; if the user's context genuinely does not support a section, write what is missing and what they need to supply rather than dropping the heading. Deliver it as a markdown file (and as .docx or .pdf if the user asks; use the docx or pdf skills for that).

After the brief, add a short section titled **"Next 3 moves"**: the three most valuable things the user should do with this offer next (for example test the guarantee wording on five calls, build the two one-time assets, set the cohort date).

### Final self-check before delivering

The test runs of this skill kept slipping on the same three details, so check them deliberately before you hand over the brief:

1. **Every deliverable and every bonus has a stated value and a one-line justification.** Scan the two tables. A row with a name but no value is the most common miss. If a value cannot be justified (for example a turnaround promise), justify it in terms of what the delay would cost the prospect rather than leaving it blank.
2. **Every number that did not come from the user is labelled.** Read the brief once looking only at digits and percentages. Anything you introduced (hourly rates, commission sizes, industry norms, "typically", "most", "roughly") gets an `[assumption: ...]` tag inline, not just a mention in the assumptions block at the top. The assumptions block lists them; the inline tag is what stops the user pasting an invented figure into a sales page.
3. **Scarcity traces to a user-stated constraint** or is an explicit placeholder (see Stage 6).

## Critique mode specifics

1. Read `references/critique-rubric.md`.
2. Score the existing offer on every rubric line (0 to 2 each) and show the scorecard with one-line evidence per score, quoting the user's own copy where possible.
3. Identify the single biggest leak (usually one of: no clear avatar, no dream outcome stated, unsolved problems, competing on price, no risk reversal, no reason to act now).
4. Rebuild using the 8 stages, but keep what already scored 2 and say so. Users need to know what to keep as much as what to change.
5. Present a before/after table for the value equation scores.

## Worked example (compressed)

Input: "I run a bookkeeping firm for dentists, charge $400/month, and clients keep churning to cheaper providers."

Build mode. Market: dental practices, high purchasing power, easy to target via dental associations, growing, pain is real (tax surprises, cash-flow blindness). Dream outcome: "know exactly how much I can take home every month and never get a surprise tax bill again". Problems listed: late books, no cash-flow forecast, no tax planning, payroll errors, no benchmark vs other practices, owner does not understand the reports, and so on. Deliverables after trim and stack: monthly Take-Home Number report, quarterly tax projection call, dental practice benchmark comparison (one-time build, high value low cost), same-day answer policy. Pricing: reframe as "$1,200/month, anchored against the average surprise tax bill the user reported". Scarcity: 8 new practices per quarter (capacity is real). Urgency: onboarding cohorts start on the first of the month. Bonuses: Associate Dentist Hiring Cost Calculator, Equipment Purchase Tax Timing Guide. Guarantee: "If we ever hand you a tax surprise larger than $1,000 that we did not forecast, that quarter is free." Name: "The Dentist Take-Home Number System".

Note what did not happen: no invented statistics about the dental market, and every number came from the user or was labelled as an assumption.
