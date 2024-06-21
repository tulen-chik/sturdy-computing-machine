import aiohttp
import pandas as pd
import asyncio

api_key = '76a7118e53e8c9168b7e3ce2c0f0c9e6'
base_url = 'https://api.themoviedb.org/3'
search_endpoint = '/search/movie'


async def main():
    async def movie(session, name):
        search_params = {'api_key': api_key, 'query': name}
        async with session.get(f'{base_url}{search_endpoint}', params=search_params) as response:
            search_results = await response.json()
        try:
            movie_id = search_results['results'][0]['id']
        except IndexError:
            return []
        credits_endpoint = f'/movie/{movie_id}/credits'
        credits_params = {'api_key': api_key}
        async with session.get(f'{base_url}{credits_endpoint}', params=credits_params) as response:
            credits = await response.json()
        writing_roles = ['Screenplay', 'Writer', 'Story', 'Dialogue Writer', 'Author', 'Adaptation', 'Original Idea',
                         'Script Supervisor', 'Script Editor', 'Script Consultant']
        writers = [crew for crew in credits['crew'] if crew['job'] in writing_roles]
        print(writers)
        return [(writer['gender'], writer['name']) for writer in writers]

    async with aiohttp.ClientSession() as session:
        async with session.get('https://bechdeltest.com/api/v1/getAllMovies') as response:
            movies = await response.json()
        movies = [{'name': movie['title'], 'year': movie['year']} for movie in movies]
        for movie_ in movies:
            movie_['screenwriter'] = await movie(session, movie_['name'])
        # Convert the list of dictionaries to a DataFrame
        df = pd.DataFrame(movies)
        # Write the DataFrame to an Excel file
        df.to_excel('movies.xlsx', index=False)


asyncio.run(main())
