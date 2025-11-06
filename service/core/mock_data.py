import random

def generate_dummy_roro_result() -> dict:
    total_mentions_24h = random.randint(50, 300)
    naver_datalab_ratio = round(random.uniform(0.5, 5.0), 2)
    spotify_artist_pop = random.randint(60, 80)
    spotify_followers = random.randint(10000, 15000)
    spotify_top5_avg_pop = round(random.uniform(65.0, 75.0), 2)

    norm_mentions_score = round(random.uniform(70.0, 90.0), 2)
    norm_followers_score = round(random.uniform(80.0, 95.0), 2)

    buzz_index = round(norm_mentions_score * 0.7 + naver_datalab_ratio * 0.3, 2)
    fandom_index = round(norm_followers_score * 0.6 + spotify_artist_pop * 0.4, 2)
    total_index = round(buzz_index * 0.5 + fandom_index * 0.5, 2)

    results = {
        "total_index": total_index,
        "buzz_index": buzz_index,
        "fandom_index": fandom_index,
        "details": {
            "preprocessed": {
                "total_mentions_24h": total_mentions_24h,
                "naver_datalab_ratio": naver_datalab_ratio,
                "spotify_artist_pop": spotify_artist_pop,
                "spotify_top5_avg_pop": spotify_top5_avg_pop,
                "spotify_followers": spotify_followers
            },
            "normalized": {
                "norm_mentions_score": norm_mentions_score,
                "norm_followers_score": norm_followers_score
            }
        }
    }

    return results


if __name__ == "__main__":
    import pprint

    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(generate_dummy_roro_result())