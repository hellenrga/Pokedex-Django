from django.shortcuts import render
from .models import Pokemon
import requests
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.

# Send an HTTP GET request to the API and retrieve data in JSON
def fetch_pokemon_data(pokemon_id):
    response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{pokemon_id}/')
    data = response.json()
    return data

# Get or create a Pokemon instance in the database
def create_or_get_pokemon(data):


    # Extract types from the provided data
    types = [type_info['type']['name'] for type_info in data['types']]

    # Set sprite URL, defaulting to an empty string if not present
    sprite_url = data['sprites']['front_default'] if 'sprites' in data and 'front_default' in data['sprites'] else ''

    pokemon_instance, created = Pokemon.objects.get_or_create(
        id=data['id'],
        defaults={
            'name': data['name'],
            'height': data['height'],
            'weight': data['weight'],
            'is_default': True,
            'sprite_url': sprite_url,
        }
    )

    pokemon_instance.set_types(types)

    return pokemon_instance, sprite_url
    
# Create and return a formatted dictionary containing Pokemon information   
def format_pokemon_data(pokemon_instance, sprite_url):

    type_list = pokemon_instance.get_types()

    return {
        'id': pokemon_instance.id,
        'name': pokemon_instance.name,
        'type': type_list,
        'height': pokemon_instance.height_in_meters(),
        'weight': pokemon_instance.weight_in_kilograms(),
        'is_default': pokemon_instance.is_default,
        'sprite_url': sprite_url,
    }

# Creating the first view for 50 pokémons
def get_pokemon_data(request):
    # Initialize an empty list to store Pokemon data
    pokemon_list = []

    # Pagination
    page_number = request.GET.get('page', 1)

    # Iterate through Pokemon IDs and fetchs data
    for i in range(1, 51):
        data = fetch_pokemon_data(i)
        pokemon_instance, sprite_url = create_or_get_pokemon(data)
        pokemon_data = format_pokemon_data(pokemon_instance, sprite_url) 

        # Append the formatted data to the Pokemon list
        pokemon_list.append(pokemon_data)

    # Create a Paginator object with 20 items per page
    paginator = Paginator(pokemon_list, 20)
    try:
        pokemon_list = paginator.page(page_number)
    except PageNotAnInteger:
        pokemon_list = paginator.page(1) 
    except EmptyPage:
        pokemon_list = paginator.page(paginator.num_pages)

    return render(request, 'index.html', {'pokemon_list': pokemon_list})

# Creating second view.
# Gets pokemons that weight more than 30 and less than 80
def get_pokemon_by_weight(request):
    pokemon_list = []

    # Pagination
    page_number = request.GET.get('page', 1)

    # Iterate through Pokemon IDs and fetchs data
    for i in range(1, 51):
        data = fetch_pokemon_data(i)
        weight = data['weight']
    
        if 30 < weight < 80:
            pokemon_instance, sprite_url = create_or_get_pokemon(data)
            pokemon_data = format_pokemon_data(pokemon_instance, sprite_url)
            pokemon_list.append(pokemon_data)
    
    # Create a Paginator object with 20 items per page
    paginator = Paginator(pokemon_list, 20)
    try:
        pokemon_list = paginator.page(page_number)
    except PageNotAnInteger:
        pokemon_list = paginator.page(1)
    except EmptyPage:
        pokemon_list = paginator.page(paginator.num_pages)

    return render(request, 'pokemon_by_weight.html', {'pokemon_list': pokemon_list})

# Creating third view.
# Gets all type "grass" Pokemon
def get_grass_pokemon(request):
    pokemon_list = []

    # Pagination
    page_number = request.GET.get('page', 1)

    for i in range(1, 51):
        try:
            # Makes a request to the API to obtain information about the Pokémon
            data = fetch_pokemon_data(i)

            # Checks if the Pokémon is of the "Grass" type.
            grass_type = any(type_info['type']['name'] == "grass" for type_info in data['types'])

            if grass_type:
                pokemon_instance, sprite_url = create_or_get_pokemon(data)
                pokemon_data = format_pokemon_data(pokemon_instance, sprite_url) 
                pokemon_list.append(pokemon_data)

        except requests.exceptions.RequestException:
            # Terminates the loop if an error occurs in the request.
            break

    # Create a Paginator object with 20 items per page
    paginator = Paginator(pokemon_list, 20)
    try:
        pokemon_list = paginator.page(page_number)
    except PageNotAnInteger:
        pokemon_list = paginator.page(1)
    except EmptyPage:
        pokemon_list = paginator.page(paginator.num_pages)

    return render(request, 'grass_pokemon.html', {'pokemon_list': pokemon_list})

# Creating fourth view
# All type “Flying” Pokemon that height more than 10
def get_flying_pokemon(request):
    pokemon_list = []

    # Pagination
    page_number = request.GET.get('page', 1)

    for i in range(1, 51):
        try:
            data = fetch_pokemon_data(i)

             # Checks if the Pokémon is of the "Flying" type and has a height greater than 10.
            if any(type_info['type']['name'] == "flying" for type_info in data['types']) and data['height'] > 10:
                pokemon_instance, sprite_url = create_or_get_pokemon(data)
                pokemon_data = format_pokemon_data(pokemon_instance, sprite_url) 
                pokemon_list.append(pokemon_data)

        except requests.exceptions.RequestException:
            # Terminates the loop if an error occurs in the request.
            break
    
    # Create a Paginator object with 20 items per page
    paginator = Paginator(pokemon_list, 20)
    try:
        pokemon_list = paginator.page(page_number)
    except PageNotAnInteger:
        pokemon_list = paginator.page(1)
    except EmptyPage:
        pokemon_list = paginator.page(paginator.num_pages)

    return render(request, 'flying_pokemon.html', {'pokemon_list': pokemon_list})

# Creating fifth view
# All inverted names of the Pokemon
def inverted_names(request):
    pokemon_list = []

    # Pagination
    page_number = request.GET.get('page', 1)

    for i in range(1, 51):
        try:
            data = fetch_pokemon_data(i)

            sprite_url = data['sprites']['front_default'] if 'sprites' in data and 'front_default' in data['sprites'] else ''

            # Reverse the name of the Pokemon
            inverted_name = data['name'][::-1] 

            # Append Pokemon data to the list, including ID, name, sprite URL, and inverted name
            pokemon_list.append({
                'id': data['id'],
                'name': data['name'],
                'sprite_url': sprite_url,
                'inverted_name': inverted_name,
            })

        except requests.exceptions.RequestException:
            # Break the loop if an error occurs in the request
            break
    # Create a Paginator object with 20 items per page        
    paginator = Paginator(pokemon_list, 20)
    try:
        pokemon_list = paginator.page(page_number)
    except PageNotAnInteger:
        pokemon_list = paginator.page(1)
    except EmptyPage:
        pokemon_list = paginator.page(paginator.num_pages)

    return render(request, 'inverted_names.html', {'pokemon_list': pokemon_list})

