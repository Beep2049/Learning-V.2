from exa_py import Exa

exa = Exa('b21bc48e-8512-4610-a830-f66a75c4bf11')

query = input('Search here: ')

response = exa.search(
   query,
   num_results=10,
   type='keyword'
)

for results in response.results:
    print(f'Title: {results.title}')
    print(f'URL: {results.url}')
    print()