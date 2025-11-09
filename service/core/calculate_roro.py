from service.crawlers.dc_inside import get_dcinside_mentions_24h
from service.crawlers.spotify import load_basic_info
from service.crawlers.spotify import load_tracks
from service.crawlers.spotify import load_spotify
from service.crawlers.naver import get_naver_mentions_24h
from service.crawlers.naver import get_naver_datalab_interest
import os
import dotenv

dotenv.load_dotenv()

MAX_PERFORMANCE_SCORE = 30000

MAX_MENTIONS_24H = 1000
MAX_FOLLOWERS = 1000000

W_BUZZ_SPOTIFY_ARTIST = 0.35
W_BUZZ_SPOTIFY_SONGS = 0.30
W_BUZZ_NAVER_DATALAB = 0.25
W_BUZZ_MENTIONS = 0.10

W_TOTAL_PERFORMANCE_INDEX = 0.40
W_TOTAL_FANDOM_INDEX      = 0.35
W_TOTAL_BUZZ_INDEX        = 0.25

def calculate_performance_score(chart_songs):
    total_performance_score = 0
    if not chart_songs:
        return 0
    for song in chart_songs:
        rank = song.get('rank', 101)
        if 1 <= rank <= 100:
            score = (101 - rank) ** 2
            total_performance_score += score
    return total_performance_score

def calculate_total_index():
    spotify_client_id = os.getenv("CLIENT_ID")
    spotify_client_secret = os.getenv("CLIENT_SECRET")
    naver_client_id = os.getenv("NAVER_CLIENT_ID")
    naver_client_secret = os.getenv("NAVER_CLIENT_SECRET")

    naver_mentions = get_naver_mentions_24h("한로로", naver_client_id, naver_client_secret)
    dc_mentions = get_dcinside_mentions_24h()
    naver_datalab = get_naver_datalab_interest("한로로", naver_client_id, naver_client_secret)
    spotify_artist = load_basic_info(spotify_client_id, spotify_client_secret)
    spotify_songs = load_tracks(spotify_client_id, spotify_client_secret)
    chart_data = load_spotify(spotify_client_id, spotify_client_secret)

    raw_data = {
        "naver_mentions": naver_mentions,
        "dc_mentions": dc_mentions,
        "spotify_artist": spotify_artist,
        "spotify_songs": spotify_songs,
        "naver_datalab": naver_datalab
    }

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
    norm_followers = min((spotify_followers / MAX_FOLLOWERS) * 100, 100)
    fandom_index = norm_followers

    norm_mentions = min((total_mentions_24h / MAX_MENTIONS_24H) * 100, 100)
    buzz_index = (
            (spotify_artist_pop * W_BUZZ_SPOTIFY_ARTIST) +
            (spotify_top5_avg_pop * W_BUZZ_SPOTIFY_SONGS) +
            (naver_datalab_ratio * W_BUZZ_NAVER_DATALAB) +
            (norm_mentions * W_BUZZ_MENTIONS)
    )

    total_performance_score = calculate_performance_score(chart_data)
    norm_performance = min((total_performance_score / MAX_PERFORMANCE_SCORE) * 100, 100)
    performance_index = norm_performance

    # 4단계: 최종 종합 지수 계산
    total_index = (
            (performance_index * W_TOTAL_PERFORMANCE_INDEX) +
            (fandom_index * W_TOTAL_FANDOM_INDEX) +
            (buzz_index * W_TOTAL_BUZZ_INDEX)
    )

    print(total_index)
    results = {
        "total_index": round(total_index*100, 2),
        "details": {
            "indices": {
                "performance_index": round(performance_index*100, 2),
                "fandom_index": round(fandom_index*100, 2),
                "buzz_index": round(buzz_index*100, 2)
            },
            "preprocessed": {
                "total_mentions_24h": total_mentions_24h,
                "naver_datalab_ratio": round(naver_datalab_ratio, 2),
                "spotify_artist_pop": spotify_artist_pop,
                "spotify_top5_avg_pop": round(spotify_top5_avg_pop, 2),
                "spotify_followers": spotify_followers,
                "total_performance_score": total_performance_score,
                "chart_songs_count": len(chart_data)
            },
            "normalized": {
                "norm_mentions_score": round(norm_mentions, 2),
                "norm_followers_score": round(fandom_index, 2),
                "norm_performance_score": round(norm_performance, 2)
            }
        }
    }
    return results