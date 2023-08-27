'''
Retrieves movie posters and IMDB page URLs for each movie title
listed in a text file and uses the data to create database seeds
'''
import os
from tmdbv3api import TMDb, Movie
from dotenv import load_dotenv

load_dotenv()

tmdb = TMDb()
tmdb.api_key = os.getenv('TMDB_API_KEY')

INPUT_FILE_PATH = 'movie_list.txt'
SEEDS_FILE_PATH = 'seeds.rb'

def read_movie_titles(file_path):
    '''read movie titles defined in text file; movie_list.txt'''
    with open(file_path, 'r') as file:
        return [line.strip() for line in file]

def read_existing_titles(file_path):
    '''check if movie title already exists in seed file; seeds.rb'''
    existing_titles = []
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            for line in file:
                if line.strip().startswith('Movie.create(title:'):
                    title = line.strip().split('"')[1]
                    existing_titles.append(title)
    return existing_titles

def main():
    '''get poster and IMDB page URL, write seeds to file'''
    movie_titles = read_movie_titles(INPUT_FILE_PATH)
    existing_titles = read_existing_titles(SEEDS_FILE_PATH)

    movie_api = Movie()

    with open(SEEDS_FILE_PATH, 'a') as seed_file:
        for title in movie_titles:
            if title not in existing_titles:
                search_results = movie_api.search(title)
                if search_results:
                    try:
                        first_result = search_results[0]
                        movie_details = movie_api.details(first_result.id)
                        poster_url = f"https://image.tmdb.org/t/p/w500{movie_details.poster_path}"
                        imdb_url = f"https://www.imdb.com/title/{movie_details.imdb_id}/"
                        entry = (
                            f'Movie.create(title:"{title}", '
                            f'poster_img_url:"{poster_url}", '
                            f'imdb_page:"{imdb_url}")\n'
                        )
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
