from aiogram.utils.helper import Helper, HelperMode, ListItem

class States(Helper):
    mode = HelperMode.snake_case

    goodNameListeningState = ListItem()
    goodPriceListeningState = ListItem()
    goodDescriptionListeningState = ListItem()


    