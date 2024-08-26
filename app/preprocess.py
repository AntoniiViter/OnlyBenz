import json


NORMALIZER = 1000000



def normalize(testdata, configuration, parameterToNormalize):
    maxValue = 0.001
    minValue = 1000

    for car in testdata:
        if car[parameterToNormalize] > maxValue:
            maxValue = car[parameterToNormalize]
        if car[parameterToNormalize] < minValue:
            minValue = car[parameterToNormalize]

    if configuration[parameterToNormalize] is None:
        configuration[parameterToNormalize] = (maxValue - minValue) / 2
    if parameterToNormalize != 'is4Matic':
        configuration[parameterToNormalize] = configuration[parameterToNormalize] = (1 + (9 / (maxValue - minValue))
                                                                                     * (configuration[
                                                                                            parameterToNormalize] - minValue))

    for car in testdata:
        if parameterToNormalize == 'budget':
            car[parameterToNormalize] = 1 + (9 / (maxValue - minValue)) * (car['priceMin'] - minValue)
        else:
            car[parameterToNormalize] = 1 + (9 / (maxValue - minValue)) * (car[parameterToNormalize] - minValue)

    return testdata, configuration


def matchCars(weights, configuration):
    with open('app/db_new.json', 'r') as config_file:
        testdata = json.load(config_file)
    final_dictionary = {}
    propertiesToProcess = {"horsepower", "consumption", "chargeTime", "range", "budget", "size", "is4Matic"}


    for prop in propertiesToProcess:
        res = normalize(testdata, configuration, prop)
        configuration = res[1]

    for car in testdata:
        deviation = 0
        for prop in propertiesToProcess:
            deviation += weights[prop] * abs(configuration[prop] - car[prop]) / NORMALIZER
        final_dictionary.update({deviation: car})

    ranked_dict = dict(sorted(final_dictionary.items()))

    result_str = 'I have found following cars for you: \n\n\n'
    suggested_cars = []
    for i in range(0, 3):
        suggested_car = ranked_dict[list(ranked_dict.keys())[i]]
        car = None

        with open('app/db_new.json', 'r') as config_file:
            old_data = json.load(config_file)
        for entry in old_data:
            if entry['name'] == suggested_car.get('name'):
                car = entry
                break

        formatic = "4Matic\n" if car.get("is4Matic") else ""
        suggested_cars.append(car.get("name"))
        suggestion = (car.get("name") + "\nstarting from " + str(car.get("priceMin")) + " EUR \n"
                      + str(car.get("horsepower")) + " HP \n" + str(car.get("consumption")) + " W/100km \n"
                      + str(car.get("range")) + " km range" + '\n' + str(car.get("seats")) + " seats \n") + formatic + "\n"
        result_str += suggestion

    result_str += "\nIf you like one of these cars, let me know!"

    return result_str, suggested_cars


def get_matching_names(model_name):
    with open('app/db_new.json', 'r') as config_file:
        data = json.load(config_file)

    possible_cars = []
    for entry in data:
        if model_name in entry['name']:
            possible_cars.append(entry)

    result_str = 'I have found following cars for you: \n\n\n'
    suggested_cars = []
    for car in possible_cars:
        suggested_cars.append(car.get("name"))
        formatic = "4Matic\n" if car.get("is4Matic") else ""
        suggestion = (car.get("name") + "\nstarting from " + str(car.get("priceMin")) + " EUR \n"
                      + str(car.get("horsepower")) + " HP \n" + str(car.get("consumption")) + " W/100km \n"
                      + str(car.get("range")) + " km range" + '\n' + str(
                car.get("seats")) + " seats \n") + formatic + "\n"
        result_str += suggestion

    result_str += "\nIf you like one of these cars, let me know!"

    return result_str, suggested_cars

def get_links(prefered_models):
    with open('app/db_new.json', 'r') as config_file:
        data = json.load(config_file)

    print("preprocess")
    print(prefered_models)

    result_str = 'Configurator link for the following car(s): \n\n\n'
    for entry in data:
        if entry['name'] in prefered_models:
            suggestion = entry.get("name") + "\n" + str(entry.get("configLink")) + "\n\n"
            result_str += suggestion

    result_str += "\nThank you so much for your choice! Glad to see you again next time!"

    return result_str
