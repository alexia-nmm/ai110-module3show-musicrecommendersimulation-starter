"""
Command line runner for the Music Recommender Simulation.

Run from the project root with:
    python -m src.main
"""

import os
from src.recommender import load_songs, recommend_songs


PROFILES = {
    "High-Energy Pop": {
        "genre": "pop",
        "mood": "happy",
        "target_energy": 0.85,
        "target_valence": 0.82,
        "target_acousticness": 0.15,
    },
    "Chill Lofi Study": {
        "genre": "lofi",
        "mood": "chill",
        "target_energy": 0.38,
        "target_valence": 0.58,
        "target_acousticness": 0.80,
    },
    "Deep Intense Rock": {
        "genre": "rock",
        "mood": "intense",
        "target_energy": 0.92,
        "target_valence": 0.45,
        "target_acousticness": 0.08,
    },
    # Adversarial: high energy + sad mood clash — folk is quiet, but user wants loud
    "Adversarial - Loud Sad": {
        "genre": "folk",
        "mood": "sad",
        "target_energy": 0.90,
        "target_valence": 0.25,
        "target_acousticness": 0.85,
    },
    # Adversarial: genre and mood point nowhere in catalog — tests graceful fallback
    "Adversarial - Unknown Genre": {
        "genre": "bossa nova",
        "mood": "nostalgic",
        "target_energy": 0.45,
        "target_valence": 0.65,
        "target_acousticness": 0.70,
    },
}


def print_profile_results(label: str, user_prefs: dict, songs: list) -> None:
    print(f"\n{'=' * 52}")
    print(f"PROFILE: {label}")
    print(
        f"  genre={user_prefs['genre']} | mood={user_prefs['mood']} | "
        f"energy={user_prefs['target_energy']}"
    )
    print("=" * 52)
    results = recommend_songs(user_prefs, songs, k=5)
    for rank, (song, score, reasons) in enumerate(results, start=1):
        print(f"{rank}. {song['title']}  -  {song['artist']}")
        print(f"   Score: {score:.2f}/6.00  |  {song['genre']} / {song['mood']}")
        for reason in reasons:
            print(f"     > {reason}")
        print()


def main() -> None:
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csv_path = os.path.join(base_dir, "data", "songs.csv")
    songs = load_songs(csv_path)

    for label, prefs in PROFILES.items():
        print_profile_results(label, prefs, songs)


if __name__ == "__main__":
    main()
