from aiogram.utils.helper import Helper, HelperMode, ListItem

class States(Helper):
    mode = HelperMode.snake_case

    TEST_STATE_0 = ListItem() #Handles new good Name
    TEST_STATE_1 = ListItem() #Handles new good price
    TEST_STATE_2 = ListItem() #Handles new good description
    TEST_STATE_3 = ListItem() #Handles id of good that needed to be deleted
    TEST_STATE_4 = ListItem() #Handles an id of user that you want to send money
    TEST_STATE_5 = ListItem() #Handles a currency that you want to send to another user
    TEST_STATE_6 = ListItem() #Handles an amount of currency that you want to send
    TEST_STATE_7 = ListItem() #Handles a currency that you want to use when you are buying something
    TEST_STATE_8 = ListItem() #Handles an id of good that user is going to buy
    TEST_STATE_9 = ListItem() #
    TEST_STATE_10 = ListItem()


    