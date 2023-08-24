import os
from tmdbv3api import TMDb
from tmdbv3api import Movie

tmdb = TMDb()
tmdb.api_key = os.environ['TMDB_API_KEY']

def read_movie_titles(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines()]

def read_existing_titles(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return [line.strip().split('"')[1] for line in file.readlines() if line.strip().startswith('Movie.create(title:')]
    return []

def main():
    file_path = 'movie_list.txt'
    seeds_path = 'seeds.rb'

    movie_titles = read_movie_titles(file_path)
    existing_titles = read_existing_titles(seeds_path)

    movie = Movie()

    with open(seeds_path, 'a') as seed_file:
        for title in movie_titles:
            if title not in existing_titles:
                search_results = movie.search(title)
                if search_results:
                    try:
                        first_result = search_results[0]
                        movie_details = movie.details(first_result.id)
                        poster_url = f"https://image.tmdb.org/t/p/w500{movie_details.poster_path}"
                        imdb_url = f"https://www.imdb.com/title/{movie_details.imdb_id}/"

                        entry = f'Movie.create(title:"{title}", poster_img_url:"{poster_url}", imdb_page:"{imdb_url}")\n'
                        seed_file.write(entry)
                        print(f"Seed added for: {title}")
                    except Exception as e:
                        print(f"Error processing: {title} - {e}")
                else:
                    print(f"No TMDb information found for: {title}")
            else:
                print(f"Skipping existing entry: {title}")

if __name__ == "__main__":
    main()

