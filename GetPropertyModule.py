# install jproperties package using pip
# import and instantiate property object and put the response in config

from jproperties import Properties

config = Properties()


def get_property(key):
    # load the property into our Properties object
    with open('app-details.properties', 'rb') as config_file:
        config.load(config_file)
        prop_value = config.get(key).data
        return prop_value
