# Model Card: VibeFinder 1.0

---

## 1. Model Name

**VibeFinder 1.0** — a small content-based music recommender built as a classroom simulation.

---

## 2. Goal / Task

VibeFinder's job is simple: given a user's music preferences, find the songs in a catalog that best match what they're looking for and explain why each one made the list.

It doesn't predict the future or learn from behavior. It just reads a preference profile you hand it — genre, mood, and a few audio targets — and scores every song in the catalog against those preferences. The five highest-scoring songs are your recommendations.

Think of it less like Spotify and more like a very opinionated friend who's heard all 18 songs in their collection and will match you to the ones that fit your vibe.

---

## 3. Data Used

The catalog lives in `data/songs.csv` and has 18 songs.

The starter file came with 10 tracks covering pop, lofi, rock, ambient, jazz, synthwave, and indie pop. I added 8 more to get better genre coverage: hip-hop, classical, R&B, country, metal, electronic, folk, and K-pop.

Each song has these fields:
- Basic info: id, title, artist, genre, mood
- Audio numbers (all 0.0 to 1.0): energy, valence, danceability, acousticness
- Tempo in BPM

**What the data is missing:**
- No Latin, reggae, blues, or soul — big gaps for a lot of listeners
- Pop and lofi each appear 3 times, so they're over-represented
- The audio values (like energy 0.82) were assigned manually for this simulation — they're reasonable estimates, not real Spotify API measurements
- No language, region, or cultural metadata at all

Basically: it's a small, Western-leaning catalog built for demonstration, not real use.

---

## 4. Algorithm Summary

Here's how the scoring works, no code involved.

When you submit your preferences, VibeFinder goes through every song in the catalog and awards it points across five categories:

1. **Genre match (+2.0 pts):** Does the song's genre label exactly match yours? This is the biggest reward because genre is the broadest way to define what kind of music you want.

2. **Mood match (+1.0 pts):** Does the mood label match? Not as much weight as genre, but still meaningful.

3. **Energy proximity (0 to 1.5 pts):** How close is the song's energy to your target? A song that's exactly at your energy level gets the full 1.5. One that's completely opposite gets almost zero. There's no reward for being "high" or "low" — only for being *close*.

4. **Valence proximity (0 to 1.0 pts):** Same idea, applied to valence (how musically positive or happy the song feels).

5. **Acousticness proximity (0 to 0.5 pts):** Same idea, applied to acousticness (organic/instrument-heavy vs electronic).

After scoring every song, VibeFinder sorts them from highest to lowest and hands you the top 5. Max possible score is 6.0.

The "proximity" scoring is intentional — it rewards songs that are *near* what you want rather than just songs that happen to score high on any single feature.

---

## 5. Observed Behavior / Biases

**The genre label is too powerful.** Since a genre match is worth 2.0 points — more than the entire energy range — a song in the right genre can beat a much better match just because its label matches. I tested this with a "Deep Intense Rock" profile: Break the Walls (metal/angry) only ranked third, behind a pop song, because "metal" doesn't string-match "rock." Those genres are obviously related to a human, but the algorithm treats them as completely different.

**Mood labels are all-or-nothing.** "Chill," "relaxed," and "focused" feel pretty similar, but VibeFinder gives zero mood points if the label doesn't match exactly. A jazz track labeled "relaxed" won't score any mood points for a "chill" user, even though a person would probably say those feel the same.

**The catalog isn't balanced.** Pop and lofi show up 3 times each; classical, folk, metal, and several others only appear once. If your preferred genre is rare in the catalog, the system runs out of real matches quickly and starts padding results with songs that just happen to have similar audio numbers.

**It can't detect contradictory preferences.** I tried a "loud sad folk" profile (genre=folk, mood=sad, energy=0.9). The system gave me Empty Porch — a quiet, gentle folk song — as #1, because it was the only folk/sad song in the catalog. The genre+mood match (3.0 pts) outweighed the energy mismatch. The algorithm isn't wrong by its own rules, but the result feels wrong. It has no way to say "these preferences kind of contradict each other."

**No variety built in.** VibeFinder always picks the most similar songs. For well-stocked genres, you might get 5 nearly identical results. That's fine for a study playlist, but it's bad for discovery.

---

## 6. Evaluation Process

I tested five profiles to see how the system behaved across different use cases:

- **High-Energy Pop** (genre=pop, mood=happy, energy=0.85) — the "easy" case. Worked great, obvious results, scores made sense.
- **Chill Lofi Study** (genre=lofi, mood=chill, energy=0.38) — also worked well. Top 3 were all lofi, which is exactly right.
- **Deep Intense Rock** (genre=rock, mood=intense, energy=0.92) — revealed the genre-string bias. Storm Runner was the clear winner, but the falloff after that was rough because there's only one rock song.
- **Adversarial: Loud Sad Folk** (genre=folk, mood=sad, energy=0.9) — the contradiction test. Empty Porch won despite having the "wrong" energy. Interesting failure mode.
- **Adversarial: Unknown Genre** (genre=bossa nova, mood=nostalgic) — the "genre doesn't exist" test. Scores maxed out at ~2.86/6.00 and the top four songs were within 0.14 points of each other. Basically a coin flip at the top.

**Experiment I ran:** I tried halving the genre weight (+2.0 → +1.0) and doubling the energy weight (×1.5 → ×3.0). For the rock profile, Break the Walls jumped from 2.78 to 4.20 — a more musically honest result. But for the Loud Sad adversarial profile, Empty Porch still won. The lesson: you can tune the weights to improve specific cases, but no weight change fixes the fundamental problem of treating genre labels as unrelated strings.

---

## 7. Intended Use / Non-Intended Use

**What this is for:**
- Learning how content-based filtering works by building a small example from scratch
- Exploring how scoring and ranking decisions affect what a user sees
- Classroom discussion about AI bias, transparency, and recommender design

**What this is NOT for:**
- Recommending music to real users — the catalog is 18 songs, which is basically nothing
- Drawing any conclusions about which genres or moods are "better" for users
- Replacing or mimicking a real streaming platform's recommendation engine
- Any kind of production use

If you ran this on your actual Spotify history, it would miss almost everything you care about. That's by design — the point was to understand the mechanics, not to ship a product.

---

## 8. Ideas for Improvement

**Genre and mood similarity instead of exact match.** Right now "rock" and "metal" are treated as completely unrelated. A simple similarity table — where rock/metal/punk are neighbors and ambient/classical are their own cluster — would fix a lot of the weird rankings I saw during testing.

**Partial mood credit.** Instead of 0 or 1.0 for mood, moods could earn partial points based on how emotionally close they are. "Chill" and "relaxed" might both earn 0.7 points when matched with each other, rather than zero.

**Contradiction detection.** If the user's genre/mood preferences historically map to low-energy music (like folk/sad) but they set a high energy target, the system should flag this instead of silently resolving it in favor of the labels. A warning like "no songs in our catalog match all of your preferences — here's the closest we have" would be more honest than a confident-looking list.

---

## 9. Personal Reflection

The biggest thing I took away from this project is how much the *design of the scoring system* determines what the recommendations "feel" like — and how that design always carries hidden assumptions.

When I first wrote the genre weight as +2.0, it seemed reasonable: genre is the most obvious way people describe their taste. But then I ran the adversarial profiles and watched a pop workout track (Gym Hero) beat a metal song for a "rock/intense" user because the mood label happened to match. The algorithm was following the rules perfectly. It just turns out that "following the rules perfectly" and "making sense to a listener" can be pretty far apart.

Using AI tools during this project helped a lot with the boilerplate — structuring the CSV reader, setting up the dataclasses, formatting the terminal output. But I had to be careful not to just accept the first suggestions. A few times the AI gave me code that technically worked but didn't match the scoring logic I'd designed: it would use a simple subtraction instead of a proximity score, or return just the score without the reasons list. Having a clear design written down before writing code made it easier to catch those mismatches.

What genuinely surprised me was how fast the system starts to *feel* like a recommendation engine even with 18 songs and addition/subtraction math. When the Lofi profile returned Library Rain and Midnight Coding at the top, it felt right — not because the algorithm is smart, but because the data was set up in a way that made the right answer fall out. That made me think harder about how much of what feels "intelligent" in a real system is actually just good data and good feature selection, not sophisticated model architecture.

If I kept going with this, I'd want to try two things. First, add a genre similarity matrix and see how much it changes the adversarial results. Second, try running this with real Spotify audio feature data instead of manually assigned values — I suspect the recommendations would get a lot more interesting (and a lot more unpredictable) once the numbers are grounded in actual audio analysis.

