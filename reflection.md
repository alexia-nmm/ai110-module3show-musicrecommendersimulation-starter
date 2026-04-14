# Reflection: Comparing User Profiles

## High-Energy Pop vs. Chill Lofi Study

These two profiles produce completely different top results, which is reassuring — it shows the system is actually doing something meaningful rather than returning the same list every time.

The Pop profile ranks Sunrise City #1 (5.92/6.00): it matches on both genre and mood, and its energy (0.82) is close to the target (0.85). The Lofi profile ranks Library Rain #1 (5.91/6.00) for the same structural reasons but with completely different songs.

What makes sense: the top three results for each profile all share the target genre. Energy and valence work as tiebreakers within the genre group. This is exactly how a "more of what you like" recommender should behave — it is useful for someone who already knows what they want.

What is limited: neither profile would surface something unexpected. A pop fan will never see a folk song in their top 5, even if that folk song happens to be upbeat and energetic. The system optimizes for similarity, not discovery.

---

## Chill Lofi Study vs. Deep Intense Rock

These profiles are near opposites on the energy axis (0.38 vs. 0.92) and they produce no overlap in their top 5 results. That is a strength — the recommender correctly identifies them as different listeners.

The interesting observation is the confidence gap. The Lofi profile's top two songs are very close in score (5.91 vs. 5.87) because there are three lofi songs in the catalog and they are all similar. The Rock profile's top song (Storm Runner, 5.94) is far ahead of #2 (Gym Hero, 3.64) because there is only one rock/intense song in the catalog. After the obvious match, the system runs out of good options and starts recommending pop and metal as substitutes.

Plain language version: imagine you ask a record store employee for "intense rock." They hand you the one rock album in the store, then start pointing at workout pop because it is energetic, and a metal album because it is loud. That is not bad judgment — it is just a small store. The catalog size is the real limitation, not the algorithm.

---

## Deep Intense Rock vs. Adversarial Loud Sad (folk, sad, energy 0.9)

This comparison shows the most interesting failure mode.

The rock profile resolves cleanly: one dominant match (Storm Runner), then a falloff. The Loud Sad profile produces a contradictory result: Empty Porch (folk/sad, energy 0.22) ranks #1 despite having the opposite energy from what the user asked for.

Why does this happen? The genre and mood match together contribute 3.0 points. The energy mismatch only costs about 1.0 point (the song earns 0.48 out of a maximum 1.5 energy points). So the system "decides" that being in the right genre and mood is more important than the energy being completely wrong.

This is not a bug in the code — it is a deliberate design choice that happens to fail here. Genre and mood are weighted high because they are usually the most defining features. But for this edge case, a user who wants loud and sad music is asking for something the catalog genuinely cannot provide. The system makes the least-wrong choice given what is available, but it cannot tell the user that.

A real recommender would handle this by either broadening the search or telling the user "we couldn't find a perfect match."

---

## Adversarial Unknown Genre (bossa nova/nostalgic)

When the genre and mood do not exist in the catalog, the system scores every song at 0 for categorical matches and ranks entirely by numerical proximity. The top results cluster around lofi and ambient songs — not because they are "bossa nova adjacent" in any musical sense, but because their energy (0.38–0.42) and acousticness (0.71–0.92) happen to be numerically close to the target.

The max achievable score for this profile is 3.0 out of 6.0, and the actual top scores are 2.86, 2.82, 2.72, 2.72 — four songs within 0.14 points of each other. The ranking becomes almost arbitrary at that closeness.

Plain language: this is like asking a food recommendation app for "Peruvian fusion" in a city that only has Italian and Japanese restaurants. It might suggest Japanese because both cuisines use rice, but that connection is superficial. The user would be better served by a message saying "we don't have that" than by a confident-looking list of loosely related alternatives.

