"""
Command line runner for the Music Recommender Simulation.

Run from the project root with:
    python -m src.main
"""

import os
from src.recommender import load_songs, recommend_songs


def main() -> None:
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csv_path = os.path.join(base_dir, "data", "songs.csv")
    songs = load_songs(csv_path)

    user_prefs = {
        "genre": "pop",
        "mood": "happy",
        "target_energy": 0.8,
        "target_valence": 0.8,
        "target_acousticness": 0.2,
    }

    print(
        f"\nUser profile: genre={user_prefs['genre']} | "
        f"mood={user_prefs['mood']} | "
        f"energy={user_prefs['target_energy']}"
    )
    print("\nTop recommendations:")
    print("-" * 52)

    recommendations = recommend_songs(user_prefs, songs, k=5)

    for rank, (song, score, reasons) in enumerate(recommendations, start=1):
        print(f"{rank}. {song['title']}  -  {song['artist']}")
        print(f"   Score: {score:.2f}/6.00  |  {song['genre']} / {song['mood']}")
        for reason in reasons:
            print(f"     > {reason}")
        print()


if __name__ == "__main__":
    main()
