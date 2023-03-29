

def get_avg_temperature(client, city, start_date, end_date):
    splitted_start_date = start_date.split('/')
    splitted_end_date = start_date.split('/') 

    return client['olympics']['daily_temperature'].aggregate([
        {
            '$match': {
                'City': city, 
                '$and': [
                    {'$expr': {'$gte': [{'$toInt': '$Year'}, 1996]}
                    }, {'$expr': {'$lte': [{'$toInt': '$Year'}, 1996]}
                    }, {'$expr': {'$gte': [{'$toInt': '$Month'}, 1]}
                    }, {'$expr': {'$lte': [{'$toInt': '$Month'}, 12]}
                    }, {'$expr': {'$gte': [{'$toInt': '$Day'}, 1]}
                    }, {'$expr': {'$lte': [{'$toInt': '$Day'}, 31]}
                    }
                ]
            }
        }, {
            '$group': {
                '_id': None, 
                'AvgTemperature': {
                    '$avg': {'$toDouble': '$AvgTemperature'}
                }
            }
        }
    ]).next()