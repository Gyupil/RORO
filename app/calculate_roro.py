MAX_MENTIONS_24H = 1000
MAX_FOLLOWERS = 1000000

W_BUZZ_SPOTIFY_ARTIST = 0.25
W_BUZZ_SPOTIFY_SONGS = 0.25
W_BUZZ_NAVER_DATALAB = 0.30
W_BUZZ_MENTIONS = 0.20

W_TOTAL_BUZZ_INDEX = 0.70
W_TOTAL_FANDOM_INDEX = 0.30


def calculate_total_index(raw_data):
    naver_mentions = raw_data['naver_mentions'].get('naver_mentions_24h', 0)
    dc_mentions = raw_data['dc_mentions'].get('dc_mentions_24h', 0)
    total_mentions_24h = naver_mentions + dc_mentions

    naver_datalab_ratio = raw_data['naver_datalab'].get('naver_datalab_daily_ratio', 0)
    spotify_artist_pop = raw_data['spotify_artist'].get('Popularity', 0)

    spotify_top5_avg_pop = 0
    song_pop_list = [pop for name, pop in raw_data.get('spotify_songs', [])]

    if song_pop_list:
        song_pop_list.sort(reverse=True)
        top_5_songs = song_pop_list[:5]
        spotify_top5_avg_pop = sum(top_5_songs) / len(top_5_songs)

    spotify_followers = raw_data['spotify_artist'].get('Followers', 0)

    print("[Calculator] 2단계: 정규화(Normalization) 시작...")
    norm_mentions = min((total_mentions_24h / MAX_MENTIONS_24H) * 100, 100)
    norm_followers = min((spotify_followers / MAX_FOLLOWERS) * 100, 100)

    buzz_index = (
            (spotify_artist_pop * W_BUZZ_SPOTIFY_ARTIST) +
            (spotify_top5_avg_pop * W_BUZZ_SPOTIFY_SONGS) +
            (naver_datalab_ratio * W_BUZZ_NAVER_DATALAB) +
            (norm_mentions * W_BUZZ_MENTIONS)
    )

    fandom_index = norm_followers

    total_index = (
            (buzz_index * W_TOTAL_BUZZ_INDEX) +
            (fandom_index * W_TOTAL_FANDOM_INDEX)
    )

    results = {
        "total_index": round(total_index, 2),
        "buzz_index": round(buzz_index, 2),
        "fandom_index": round(fandom_index, 2),
        "details": {
            "preprocessed": {
                "total_mentions_24h": total_mentions_24h,
                "naver_datalab_ratio": round(naver_datalab_ratio, 2),
                "spotify_artist_pop": spotify_artist_pop,
                "spotify_top5_avg_pop": round(spotify_top5_avg_pop, 2),
                "spotify_followers": spotify_followers
            },
            "normalized": {
                "norm_mentions_score": round(norm_mentions, 2),
                "norm_followers_score": round(fandom_index, 2)
            }
        }
    }

    return results