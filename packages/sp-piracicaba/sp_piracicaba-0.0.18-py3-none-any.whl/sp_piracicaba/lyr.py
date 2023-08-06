"""
Plano Diretor de Piracicaba
Configura Layers

"""

import os
import folium
import webbrowser
import geopandas as gpd
from open_geodata import geo


def macrozona():
    # Input
    gdf = geo.load_dataset_from_package('sp_piracicaba', 'geo.macrozonas')
    gdf = gdf.to_crs(epsg=4326)

    # Set dictionary
    colors = {
        'MADE': '#0173b2',
        'MANU': '#de8f05',
        'MAPH': '#029e73',
        'MCU': '#d55e00',
        'MRU': '#cc78bc',
        'MUC': '#ca9161'
    }

    # Popup
    gdf['PopUp'] = gdf.apply(popup_macrozona, axis=1)

    # Layer
    return folium.features.GeoJson(
        gdf,
        name='Macrozoneamento',
        style_function=lambda x: {
            'fillColor': colors[x['properties']['Macrozona']],
            'color': colors[x['properties']['Macrozona']],
            'weight': 0,
            'fillOpacity': 0.3
        },
        popup=folium.GeoJsonPopup(
            fields=['PopUp'],
            aliases=['Macrozona'],
            labels=False,
            sticky=True,
            localize=True,
            style=f"""
            background-color: #F0EFEF;
            """,
            parse_html=True,
            max_width=400,
        ),
        tooltip=folium.features.GeoJsonTooltip(
            fields=['Macrozona', ],
            aliases=['Macrozona', ],
            labels=True,
            sticky=True,
            opacity=0.9,
            direction='auto',
        ),
        highlight_function=lambda x: {
            'weight': 3
        },
        embed=False,
        zoom_on_click=False,
        control=True,
        show=False,
    )


# PopUp
def popup_macrozona(row):
    descriptions = {
        'MADE': 'Macrozona de Desenvolvimento Rural',
        'MANU': 'Macrozona de Núcleos Urbanos Isolados',
        'MAPH': 'Macrozona de Proteção Hídrica e Ambiental',
        'MCU': 'Macrozona de Contenção Urbana',
        'MRU': 'Macrozona de Restrição Urbana',
        'MUC': 'Macrozona de Urbanização Consolidada',
    }
    macrozona = row['Macrozona']
    description = descriptions[macrozona]
    return f"""
    <div>
    <h4>Plano Diretor de Piracicaba</h4>
    <h5>Lei Complementar nº 405/2019</h5>
    <b>{description}</b>
    </div>    
    """
    


def perimetro_urbano():
    # Input
    gdf = geo.load_dataset_from_package('sp_piracicaba', 'geo.divisa_perimetro')
    gdf = gdf.to_crs(epsg=4326)

    # Layer
    return folium.features.GeoJson(
        gdf,
        name='Perimetro Urbano',
        style_function=lambda x: {
            'fillColor': '#E1E1E1',
            'color': '#E1E1E1',
            'weight': 2,
            'fillOpacity': 0.5,
        },
        tooltip=folium.features.GeoJsonTooltip(
            fields=['Nome', ],
            aliases=['Nome', ],
            labels=True,
            sticky=True,
            opacity=0.9,
            direction='auto',
        ),
        embed=False,
        zoom_on_click=False,
        control=True,
        show=False,
    )


def divisa_municipal():
    # Input
    gdf = geo.load_dataset_from_package('sp_piracicaba', 'geo.divisa_municipal')
    gdf = gdf.to_crs(epsg=4326)

    # Layer
    return folium.features.GeoJson(
        gdf,
        name='Divisão Municipal',
        style_function=lambda x: {
            'fillColor': '#FAE878',
            'color': '#FAE878',
            'weight': 2,
            'fillOpacity': 0.0,
        },
        embed=False,
        zoom_on_click=False,
        control=True,
        show=True,
    )


def divisa_urbano_rural():
    # Input
    gdf = geo.load_dataset_from_package('sp_piracicaba', 'geo.divisa_urbanorural')
    gdf = gdf.to_crs(epsg=4326)

    # Set dictionary
    colors = {
        'Área Rural': '#F1A51F',
        'Área Urbana': '##E1E1E1',
    }

    # Layer
    return folium.features.GeoJson(
        gdf,
        name='Divisão Urbano Rural',
        style_function=lambda x: {
            'fillColor': colors[x['properties']['Area']],
            'color': colors[x['properties']['Area']],
            'weight': 1,
            'fillOpacity': 0.3
        },
        embed=False,
        zoom_on_click=False,
        control=True,
        show=False,
    )


def divisa_abairramento():
    # Input
    gdf = geo.load_dataset_from_package('sp_piracicaba', 'geo.divisa_abairramento')
    gdf = gdf.to_crs(epsg=4326)

    # Layer
    return folium.features.GeoJson(
        gdf,
        name='Divisão Abairramento',
        style_function=lambda x: {
            'fillColor': '#CFCFCF',
            'color': '#CFCFCF',
            'weight': 1,
            'fillOpacity': 0.3
        },
        tooltip=folium.features.GeoJsonTooltip(
            fields=['NomeBairro'],
            aliases=['Bairro'],
            labels=True,
            sticky=True,
            opacity=0.9,
            direction='auto',
        ),
        highlight_function=lambda x: {
            'weight': 3
        },
        embed=False,
        zoom_on_click=False,
        control=True,
        show=False,
    )


if __name__ == '__main__':
    from open_geodata import geo, lyr

    # Create Maps
    m = folium.Map(
        location=[-23.9619271, -46.3427499],
        zoom_start=10,
    )

    # Add Layers
    m.add_child(macrozona())
    m.add_child(divisa_abairramento())

    # Save/Open Map
    down_path = os.path.join(os.path.expanduser('~'), 'Downloads')
    map_file = os.path.join(down_path, 'map_example.html')
    m.save(map_file)
    webbrowser.open(map_file)
    