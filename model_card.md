# Model Card: Music Recommender Simulation

## 1. Model Name

**VibeFinder 1.0**

---

## 2. Intended Use

VibeFinder suggests up to 5 songs from an 18-song catalog based on a user's stated genre, mood, and three numeric audio preferences (energy, valence, acousticness). It is built for classroom exploration of how content-based recommenders work. It is not intended for real deployment — the catalog is tiny, there are no real users, and no behavioral data is involved.

The system assumes the user can describe their preferences in advance. This is a key difference from real-world systems, which infer preferences silently from listening behavior.

---

## 3. How the Model Works

Think of VibeFinder like a music critic who reads a single note you hand them: "I want chill lofi music with low energy." For each song in the catalog, the critic awards points in two ways.

First, they check for exact labels: does the song's genre match yours? Does the mood label match? If yes, those are bonus points — genre is worth two points, mood is worth one. These are the biggest scores available because they define the broadest "world" of music you want to be in.

Second, they look at the audio numbers. For energy, valence, and acousticness, the closer the song's value is to your target, the more points it earns. A song that is far from your energy target loses most of those points; one that is exactly on target earns the maximum. This is called proximity scoring.

After every song has been scored, they hand you the five highest-scoring songs. That is your recommendation.

---

## 4. Data

The catalog contains 18 songs stored in `data/songs.csv`. The original starter file had 10 songs covering pop, lofi, rock, ambient, jazz, synthwave, and indie pop. Eight additional songs were added to expand diversity: hip-hop, classical, R&B, country, metal, electronic, folk, and K-pop.

Each song has 10 fields: id, title, artist, genre, mood, energy (0–1), tempo_bpm, valence (0–1), danceability (0–1), and acousticness (0–1).

Moods represented: happy, chill, intense, relaxed, focused, moody, energetic, peaceful, romantic, melancholic, angry, euphoric, sad, uplifting.

Gaps in the data: no Latin, reggae, blues, or soul genres. Pop and lofi appear three times each, making them over-represented. All songs are in English by implied convention — no metadata represents language, region, or cultural context. Whose taste shaped the energy/valence values is unknown; they were assigned for simulation purposes.

---

## 5. Strengths

- Works well for users whose taste matches the most common catalog genres. A pop/happy user immediately gets Sunrise City as #1 (5.92/6.00), which is musically accurate.
- Works well for users with a well-defined numerical profile. Chill Lofi Study returns three lofi songs in the top three with tightly clustered high scores (5.91, 5.87, 4.95), which matches real listening behavior.
- Transparent by design: every recommendation includes a per-feature breakdown showing exactly which signals drove the score. You can always explain why a song appeared.
- Degrades gracefully for unknown genres: when a user asks for "bossa nova" (not in the catalog), the system returns songs by pure numerical proximity without crashing or returning empty results.

---

## 6. Limitations and Bias

**Genre dominance creates a filter bubble.** At 2.0 points, a genre match alone is worth more than the maximum energy proximity (1.5 points). This means a bad song in the right genre can beat a perfect song in the wrong genre. For the "Deep Intense Rock" profile, Break the Walls (metal/angry) — which would likely appeal to a rock fan — ranks third behind a pop song because "metal" does not string-match to "rock." A user who likes intense guitar music but whose exact genre label is not in the catalog will consistently receive lower-quality results.

**Mood labels are treated as unrelated strings.** "Chill," "relaxed," and "focused" feel similar to a human but score zero for each other. A jazz track labeled "relaxed" will never earn a mood point for a "chill" user, even though the experience of listening is nearly identical. This means any user whose preferred mood is adjacent to a catalog mood is structurally penalized.

**The catalog is too small and unevenly distributed.** Pop and lofi each appear three times; classical, metal, folk, and several others appear once. A "classical/peaceful" user can only ever match one song on both genre and mood labels. Their recommendations will be padded with unrelated songs that happened to have similar audio numbers.

**The system ignores the energy contradiction in adversarial profiles.** When a user specifies folk/sad with energy 0.90, the system returns Empty Porch (folk/sad, energy 0.22) as #1 because genre+mood points (3.0) overwhelm the energy penalty (only 0.48 instead of max 1.5). The system cannot detect that this is a self-contradictory request.

**No diversity enforcement.** The ranking rule always picks the most similar songs. For well-represented genres, all five results can feel nearly identical — useful for focus sessions, poor for discovery.

---

## 7. Evaluation

Five user profiles were tested: High-Energy Pop, Chill Lofi Study, Deep Intense Rock, Adversarial Loud Sad, and Adversarial Unknown Genre.

**What matched intuition:** Pop/happy and Lofi/chill profiles both produced sensible, confident results. The top song in each case was the obvious choice, and scores dropped cleanly as songs diverged from the profile.

**What surprised:** The Deep Intense Rock profile exposes the genre-string problem most clearly. Break the Walls (metal/angry) — probably the song most likely to satisfy a rock fan emotionally — only ranks third because "metal" != "rock" and "angry" != "intense." Gym Hero (a pop track about working out) ranks second because it matched the mood label "intense." The algorithm sees labels, not music.

**Experiment — halved genre weight, doubled energy weight:** Changing genre from +2.0 to +1.0 and energy from ×1.5 to ×3.0 moved Break the Walls from 2.78 to 4.20 for the rock profile, surfacing it as a more legitimate #3. The gap between #1 and #2 shrank from 2.30 to 1.30, making the ranking feel less like a runaway genre match and more like a real comparison. However, for the Loud Sad adversarial profile, Empty Porch still ranked first: even with doubled energy weight, the quiet folk song's genre+mood advantage (2.0 points) held. The experiment revealed that the system is more accurate with lower genre weight — but also that no weight change alone fixes the fundamental problem of treating labels as unrelated strings.

---

## 8. Future Work

- Replace exact-match genre scoring with a genre similarity matrix (e.g., metal and rock should be close neighbors, not strangers).
- Add mood clustering so that "chill," "relaxed," and "peaceful" can earn partial credit rather than zero.
- Enforce a diversity rule: if two top songs share a genre, the second one's score is penalized slightly to encourage variety.
- Add a "minimum energy threshold" check: if the user's target energy differs from the song's energy by more than 0.5, cap the categorical bonus at 50% to prevent energy-contradicting results.
- Grow the catalog to at least 50–100 songs with balanced genre representation before drawing any conclusions about the system's accuracy.

---

## 9. Personal Reflection

Building VibeFinder made the hidden structure of recommender systems visible in a way that reading about them does not. The biggest lesson was how much weight a simple string comparison carries — two letters separate "rock" from "folk," and the algorithm treats them as completely unrelated, even though a human listener would hear obvious similarities in some cases. Real platforms like Spotify avoid this by using audio fingerprints and collaborative signals rather than trusting labels alone.

The adversarial profiles were the most revealing part of the evaluation. A "loud, sad folk" user is a real type of listener — think of loud, distorted folk-punk — but the scoring logic cannot model internal contradictions in a profile. It just averages them out, which produces a result that is technically optimal under the scoring rules but feels wrong to a human. That gap between "optimal by the rules" and "right for the user" is exactly what human editorial curation and real machine learning are trying to close.

