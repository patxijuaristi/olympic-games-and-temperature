from datetime import datetime, timezone

# Query que devuelve la temperatura media de una ciudad
# entre un rango de fechas especifico, en unidades celsius
def get_avg_temperature(client, city, start_date, end_date):

    result = client['olympics']['daily_temperature'].aggregate([
        {
            # Con el comando addFields, añadimos un campo con el datetime concatenando los tres atributos de "Year", "Month" y "Day"
            '$addFields': {
                'datetime': {
                    '$dateFromString': {
                        'dateString': {
                            '$concat': [
                                { '$toString': { '$toInt': '$Year' } },
                                '-',
                                { '$toString': { '$toInt': '$Month' } },
                                '-',
                                { '$toString': { '$toInt': '$Day' } }
                            ]
                        }
                    }
                }
            }
        }, {
            # Con el match filtramos los resultados por la ciudad y el rango de fechas
            '$match': {
                '$and': [
                    { 'City': city },
                    { 'datetime': {
                            '$gte': datetime.strptime(start_date, '%d/%m/%Y'), 
                            '$lte': datetime.strptime(end_date, '%d/%m/%Y')
                        }
                    }
                ]
            }
        }, {
            # Y con el group calculamos la temperatura media del periodo de tiempo y lo convertimos de Fahrenheit a Celsius
            '$group': {
                '_id': 0, 
                'PeriodAvgTemperature': {
                    '$avg': {
                        '$multiply': [
                            { '$divide': [
                                { '$subtract': [
                                    { '$toDouble': '$AvgTemperature' }, 32
                                ]}, 1.8
                            ]}, 1.0
                        ]
                    }
                }
            }
        }
    ])

    try:
        first_result = round(next(result)['PeriodAvgTemperature'], 2)
    except:
        first_result = None
    
    return first_result

# Para un deporte en concreto, devuelve la lista de paises que
# más medallas han conesguido en dicho deporte, incluyendo los
# tipos de medallas que se han conseguido: oro, plata y bronce.
def get_best_country_in_sport(client, sport):
    result = client['olympics']['athlete_events'].aggregate([
        {
            '$match': {
                'Sport': sport, 
                'Medal': { '$ne': 'NA' }
            }
        }, {
            '$group': {
                '_id': {
                    'Team': '$Team', 
                    'Medal': '$Medal'
                }, 
                'count': { '$sum': 1 }
            }
        }, {
            '$group': {
                '_id': '$_id.Team', 
                'medals': {
                    '$push': {
                        'medal': '$_id.Medal', 
                        'count': '$count'
                    }
                }, 
                'total': { '$sum': '$count' }
            }
        }, {
            '$project': {
                '_id': 0, 
                'country': '$_id', 
                'total_medals': '$total', 
                'medals': 1
            }
        }, {
            '$sort': { 'total_medals': -1 }
        }
    ])

    return result

# Para un país en concreto, devuelve la lista de deportes
# en los que más medallas se han conesguido, incluyendo los
# tipos de medallas que se han conseguido: oro, plata y bronce.
def get_best_sport_for_country(client, country):
    result = client['olympics']['athlete_events'].aggregate([
        {
            '$match': {
                'Team': country, 
                'Medal': { '$ne': 'NA' }
            }
        },
        {
            # Agrupar por deporte y sumar la cantidad total de medallas
            '$group': {
                '_id': {
                    'Sport': '$Sport', 
                    'Medal': '$Medal'
                }, 
                'count': { '$sum': 1 }
            }
        }, {
            '$group': {
                '_id': '$_id.Sport', 
                'medals': {
                    '$push': {
                        'medal': '$_id.Medal', 
                        'count': '$count'
                    }
                }, 
                'total': { '$sum': '$count' }
            }
        }, {
            '$project': {
                '_id': 0, 
                'sport': '$_id', 
                'total_medals': '$total', 
                'medals': 1
            }
        }, {
            '$sort': { 'total_medals': -1 }
        }
    ])

    return result

# Para un país en concreto, se muestra la cantidad de medallas que se han conseguido
#  para cada tipo de juegos (invierno y verano), junto con sus porcentajes.
def country_better_winter_or_summer(client, country):
    result = client['olympics']['athlete_events'].aggregate([
        {
            '$match': {
                'Team': country, 
                'Medal': { '$ne': 'NA' }
            }
        }, 
        {
            # Sumar cantidad total de medallas y cantidad por temporada
            '$group': {
                '_id': None, 
                'totalMedals': { '$sum': 1 }, 
                'medalsSummer': {
                    '$sum': { '$cond': [ { '$eq': [ '$Season', 'Summer' ] }, 1, 0 ] }
                }, 
                'medalsWinter': {
                    '$sum': { '$cond': [ { '$eq': [ '$Season', 'Winter' ] }, 1, 0 ] }
                }
            }
        },
        {
            # Calcular los porcentajes de medallas por temporada
            '$addFields': {
                'percentSummer': {
                    '$concat': [ { '$toString': { '$round': [ { '$multiply': [ { '$divide': [ '$medalsSummer', '$totalMedals' ] }, 100 ] }, 2 ] } }, '%' ]
                }, 
                'percentWinter': {
                    '$concat': [ { '$toString': { '$round': [ { '$multiply': [ { '$divide': [ '$medalsWinter', '$totalMedals' ] }, 100 ] }, 2 ] } }, '%' ]
                }
            }
        }, {
            '$project': {
                '_id': 0, 
                'totalMedals': 1, 
                'medalsSummer': 1, 
                'medalsWinter': 1, 
                'percentSummer': 1, 
                'percentWinter': 1
            }
        }
    ])

    return next(result)

# Consulta que devuelve la temperatura media de unos juegos olímpicos por año
def get_olimpics_avg_temperature_by_year(client, year):
    try:
        result = client['olympics']['olympics_dates'].aggregate([
            {
                '$match': { 'Year': year }
            }, {
                '$project': {
                    '_id': 0, 
                    'Avg temperature': { '$toDouble': '$Avg temperature' }
                }
            }
        ])

    
        first_result = round(next(result)['Avg temperature'], 2)
    except:
        first_result = None
    
    return first_result

# En esta consulta se obtienen las temperaturas de los juegos 
# olímpicos en los que más medallas ha conseguido un país concreto
def country_most_medals_by_temperature(client, country):
    result = client['olympics']['athlete_events'].aggregate([
        {
            '$match': { 'Team': country }
        },
        {
            # Como puede haber varios juegos en la misma ciudad o varios juegos en el mismo año,
            # el lookup tiene que comparar el año, la ciudad y la temporada
            '$lookup': {
                'from': 'olympics_dates', 
                'let': {
                    'year': '$Year', 
                    'city': '$City'
                }, 
                'pipeline': [
                    {
                        '$match': {
                            '$expr': {
                                '$and': [
                                    { '$eq': [ '$Year', '$$year' ] },
                                    { '$eq': [ '$City', '$$city' ] },
                                    { '$eq': [ '$Season', '$Season' ] }
                                ]
                            }
                        }
                    }
                ], 
                'as': 'olympics_dates'
            }
        },
        { '$unwind': '$olympics_dates' },
        {
            '$group': {
                '_id': {
                    'Year': '$Year', 
                    'City': '$City', 
                    'Season': '$Season', 
                    'Avg temperature': '$olympics_dates.Avg temperature'
                }, 
                'MedalCount': {
                    '$sum': { '$cond': [ { '$ne': [ '$Medal', 'NA' ] }, 1, 0 ] }
                }
            }
        },
        {
            '$project': {
                '_id': 0, 
                'Year': '$_id.Year', 
                'City': '$_id.City', 
                'Season': '$_id.Season', 
                'Avg_temperature': '$_id.Avg temperature', 
                'MedalCount': 1
            }
        },
        { '$sort': { 'MedalCount': -1 } }
    ])

    return result

def compare_two_country_results_by_temperature(client, country1, country2):
    result = client['olympics']['athlete_events'].aggregate([
        {
            '$match': {
                '$or': [
                    { 'Team': country1 },
                    { 'Team': country2 }
                ]
            }
        }, {
            '$lookup': {
                'from': 'olympics_dates', 
                'let': {
                    'year': '$Year', 
                    'city': '$City'
                }, 
                'pipeline': [
                    {
                        '$match': {
                            '$expr': {
                                '$and': [
                                    { '$eq': [ '$Year', '$$year' ] },
                                    { '$eq': [ '$City', '$$city' ] },
                                    { '$eq': [ '$Season', '$Season' ] }
                                ]
                            }
                        }
                    }
                ], 
                'as': 'olympics_dates'
            }
        },
        { '$unwind': '$olympics_dates' },
        {
            '$group': {
                '_id': {
                    'Year': '$Year', 
                    'City': '$City', 
                    'Avg temperature': '$olympics_dates.Avg temperature'
                }, 
                'Country1Medals': {
                    '$sum': {
                        '$cond': [
                            {
                                '$and': [
                                    { '$eq': [ '$Team', country1 ] },
                                    { '$ne': [ '$Medal', 'NA' ] }
                                ]
                            }, 1, 0
                        ]
                    }
                }, 
                'Country2Medals': {
                    '$sum': {
                        '$cond': [
                            {
                                '$and': [
                                    { '$eq': [ '$Team', country2 ] },
                                    { '$ne': [ '$Medal', 'NA' ] }
                                ]
                            }, 1, 0
                        ]
                    }
                }
            }
        },
        {
            # Resultados a mostrar convirtiendo la temperatura a double y poniendo a -99 los vacíos
            '$project': {
                '_id': 0, 
                'Year': '$_id.Year', 
                'City': '$_id.City', 
                'Avg_temperature': {
                    '$toDouble': {
                        '$cond': [ { '$eq': [ '$_id.Avg temperature', '' ] }, -99, '$_id.Avg temperature' ]
                    }
                }, 
                'Country1Medals': 1, 
                'Country2Medals': 1
            }
        }, {
            '$sort': {
                'Avg_temperature': -1
            }
        }
    ])

    return result
# Consulta que devuelve una lista con todos los juegos olímpicos
# (de invierno y de verano) junto con el país que más medallas ha 
# conseguido, la cantidad y la temperatura media que hubo en dichos juegos.
def get_best_country_by_year(client):
    result = client['olympics']['athlete_events'].aggregate([
        {
            # Quitar los eventos sin medallas
            '$match': { 'Medal': { '$ne': 'NA' } }
        },
        {
            # Agrupar los juegos (obtenidos por año y temporada) por país
            '$group': {
                '_id': {
                    'Year': '$Year', 
                    'Season': '$Season', 
                    'Team': '$Team'
                },
                # Sumar la cantidad de medallas de cada país en cada juego
                'MedalCount': { '$sum': 1 }
            }
        },
        {
            # Ordenar por año, temporada y cantidad de medalls
            '$sort': {
                '_id.Year': 1, 
                '_id.Season': 1, 
                'MedalCount': -1
            }
        }, 
        {
            # Volver a agruparlos por año y temporada y coger el primer valor de país y medallas, 
            # para así obtener el país que más medallas ha obtenido
            '$group': {
                '_id': {
                    'Year': '$_id.Year', 
                    'Season': '$_id.Season'
                }, 
                'TopTeam': {
                    '$first': '$_id.Team'
                }, 
                'MedalCount': {
                    '$first': '$MedalCount'
                }
            }
        },
        {
            # Hacer lookup con el dataset de fechas de juegos y temperatura
            '$lookup': {
                'from': 'olympics_dates', 
                'let': {
                    'year': '$_id.Year', 
                    'season': '$_id.Season'
                }, 
                'pipeline': [
                    {
                        '$match': {
                            '$expr': {
                                '$and': [
                                    { '$eq': [ '$Year', '$$year' ] },
                                    { '$eq': [ '$Season', '$$season' ] }
                                ]
                            }
                        }
                    }
                ], 
                'as': 'olympics_dates'
            }
        },
        { '$unwind': '$olympics_dates' },
        {
            # Elegir los datos a mostrar
            '$project': {
                '_id': 0, 
                'Year': '$_id.Year', 
                'Season': '$_id.Season', 
                'TopTeam': 1, 
                'MedalCount': 1, 
                'AvgTemperature': {
                    '$cond': {
                        'if': {
                            '$eq': [
                                '$olympics_dates.Avg temperature', ''
                            ]
                        }, 
                        'then': -99.0, 
                        'else': {
                            '$toDouble': '$olympics_dates.Avg temperature'
                        }
                    }
                }
            }
        },
        {
            # Ordenar por temperatura descendente
            '$sort': { 'AvgTemperature': -1 }
        }
    ])

    return result