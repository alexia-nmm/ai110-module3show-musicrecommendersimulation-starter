import csv
from dataclasses import asdict, dataclass
from typing import Dict, List, Tuple


@dataclass
class Song:
    """Represents a song and its audio attributes."""
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float


@dataclass
class UserProfile:
    """Represents a user's taste preferences."""
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool


class Recommender:
    """OOP wrapper that scores and ranks Song objects for a given UserProfile."""

    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top k Song objects ranked highest to lowest score."""
        song_dicts = [asdict(s) for s in self.songs]
        user_dict = _profile_to_dict(user)
        ranked = recommend_songs(user_dict, song_dicts, k)
        id_to_song = {s.id: s for s in self.songs}
        return [id_to_song[entry[0]["id"]] for entry in ranked]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a human-readable explanation for why this song was recommended."""
        _, reasons = score_song(_profile_to_dict(user), asdict(song))
        return "; ".join(reasons)


def _profile_to_dict(user: UserProfile) -> Dict:
    """Convert a UserProfile into the dict format expected by score_song."""
    return {
        "genre": user.favorite_genre,
        "mood": user.favorite_mood,
        "target_energy": user.target_energy,
        "target_valence": 0.6,
        "target_acousticness": 0.8 if user.likes_acoustic else 0.2,
    }


def load_songs(csv_path: str) -> List[Dict]:
    """Read songs.csv and return a list of dicts with numeric fields cast to float/int."""
    float_fields = {"energy", "valence", "danceability", "acousticness"}
    int_fields = {"id", "tempo_bpm"}
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            for field in float_fields:
                row[field] = float(row[field])
            for field in int_fields:
                row[field] = int(row[field])
            songs.append(row)
    print(f"Loaded {len(songs)} songs from {csv_path}")
    return songs


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score one song against user preferences; returns (total_score, reasons list)."""
    score = 0.0
    reasons = []

    # --- Categorical matches ---
    if song["genre"] == user_prefs.get("genre", ""):
        score += 2.0
        reasons.append(f"genre match: {song['genre']} (+2.0)")

    if song["mood"] == user_prefs.get("mood", ""):
        score += 1.0
        reasons.append(f"mood match: {song['mood']} (+1.0)")

    # --- Numerical proximity: 1 - |song_val - target| rewards closeness ---
    target_energy = user_prefs.get("target_energy", 0.5)
    energy_pts = round((1.0 - abs(song["energy"] - target_energy)) * 1.5, 2)
    score += energy_pts
    reasons.append(
        f"energy {song['energy']:.2f} vs target {target_energy:.2f} (+{energy_pts:.2f})"
    )

    target_valence = user_prefs.get("target_valence", 0.6)
    valence_pts = round((1.0 - abs(song["valence"] - target_valence)) * 1.0, 2)
    score += valence_pts
    reasons.append(
        f"valence {song['valence']:.2f} vs target {target_valence:.2f} (+{valence_pts:.2f})"
    )

    target_acousticness = user_prefs.get("target_acousticness", 0.5)
    acoustic_pts = round((1.0 - abs(song["acousticness"] - target_acousticness)) * 0.5, 2)
    score += acoustic_pts
    reasons.append(
        f"acousticness {song['acousticness']:.2f} vs target {target_acousticness:.2f} (+{acoustic_pts:.2f})"
    )

    return round(score, 2), reasons


def recommend_songs(
    user_prefs: Dict, songs: List[Dict], k: int = 5
) -> List[Tuple[Dict, float, List[str]]]:
    """Score every song and return the top k as (song, score, reasons) sorted high to low.

    Uses sorted() rather than list.sort() so the original songs list is never mutated.
    sorted() always returns a new list; .sort() modifies the list in place.
    """
    scored = [(song, *score_song(user_prefs, song)) for song in songs]
    return sorted(scored, key=lambda entry: entry[1], reverse=True)[:k]
