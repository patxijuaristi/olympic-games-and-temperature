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