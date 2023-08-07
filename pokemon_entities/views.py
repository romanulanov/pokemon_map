import folium
from django.utils.timezone import localtime, now
from django.http import HttpResponseNotFound
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from .models import Pokemon, PokemonEntity
from pytz import timezone


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    entities = PokemonEntity.objects.filter(appeared_at__lt=localtime(now()), disappeared_at__gt=localtime(now())
                                  )
    for entity in entities:
        add_pokemon(
            folium_map, pokemon.lat,
            pokemon.lon,
            request.build_absolute_uri(pokemon.pokemon.photo.url)
        )

    pokemons_on_page = []
    for pokemon in Pokemon.objects.all():
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': request.build_absolute_uri(pokemon.photo.url),
            'title_ru': pokemon.title,
        })
    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    
    pokemon = get_object_or_404(Pokemon, pk=pokemon_id)
    previous_evolution, next_evolution = {}, {}
    if pokemon.previous_evolution:
        previous_evolution = {"title_ru": pokemon.previous_evolution.title,
                              "pokemon_id": pokemon.previous_evolution.pk,
                              "img_url": request.build_absolute_uri(pokemon.previous_evolution.photo.url),
                              }
    if pokemon.next_gen.first():
        next_gen = pokemon.next_gen.first()
        next_evolution = {"title_ru": next_gen.title,
                          "pokemon_id": next_gen.pk,
                          "img_url": request.build_absolute_uri(next_gen.photo.url),
                          }

    requested_pokemon = {"pokemon_id": pokemon.pk,
                         "title_ru": pokemon.title,
                         "title_en": pokemon.title_en,
                         "title_jp": pokemon.title_jp,
                         "img_url": request.build_absolute_uri(pokemon.photo.url),
                         "description": pokemon.description,
                         "previous_evolution": previous_evolution,
                         "next_evolution": next_evolution
                         }
    

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    for pokemon_entity in PokemonEntity.objects.filter(pokemon=pokemon):
        add_pokemon(
            folium_map, pokemon_entity.lat,
            pokemon_entity.lon,
            request.build_absolute_uri(pokemon_entity.pokemon.photo.url)
        )

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': requested_pokemon
    })
