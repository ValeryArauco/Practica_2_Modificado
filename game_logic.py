import game_control
import card_logic
import display_funct
import pygame


########################################################
def select_choose(player, board, selected=0):
    player.play_card(board, selected)
    selected = None
    return selected


def select_move(select_L, select_R, allowed_card_list, selected):
    if selected is None:
        selected = 0
    if select_R:
        selected += 1
        if selected >= len(allowed_card_list):  # catch
            selected = len(allowed_card_list) - 1
            return selected
    elif select_L:
        selected -= 1
        if selected < 0:  # catch
            selected = 0
            return selected
    return selected
########################################################


def card_allowed(board, player):  # return list of cards allowed to be played
    i = 0
    allowed = []

    for card in player.hand:
        if board.card_stack == [] or board.color == "w":
            allowed = range(len(player.hand))
            return allowed
        if card.color == "w":
            allowed.append(i)
        elif card.type == board.type or card.color == board.color:
            allowed.append(i)
        i += 1
    return allowed


def player_LR_selection_hand(player, selected, board=None, allowed_card_list=None):
    '''
    Function that is a modification of player_LR_selection that decides the card
    the player is hovering over, additionally if the player selects the card
    they are hovering over; turn_done will be turned to true allowing for further
    progress within outside functions.

    '''
    select_L = False
    select_R = False
    select_UP = False
    update = False
    turn_done = False

    for event in pygame.event.get():
        (select_L, select_R, select_UP) = game_control.get_keypress(event)

    if select_R or select_L:  # if  keystoke to pick card was entered

        selectednew = select_move(
            select_L, select_R, allowed_card_list, selected)

        if selected == selectednew:
            pass
        else:
            selected = selectednew
            update = True

        select_L = False
        select_R = False

    elif select_UP:  # if  keystoke to play card was entered
        if selected is None:  # catch for index nonetype error in allowed_card_list
            selected = 0

        selected = select_choose(player, board, allowed_card_list[selected])
        update = True
        turn_done = True

    return (update, selected, turn_done)

########################################################


def player_turn(board, deck, player, allowed_card_list, selected):
    update = False
    if allowed_card_list == []:
        player.grab_card(deck)
        selected = None
        update = True
        turn_done = True
        return (update, selected, turn_done)

    while not update:
        (update, selected, turn_done) = player_LR_selection_hand(
            player, selected, board, allowed_card_list)

    return (update, selected, turn_done)


def game_loop(board, deck, players):  # gameplay loop structure
    '''
    main logic and turn loop that controlls the game.

    args:
        board: a game_classes.py board class in which the cards within the game
        will be played on. The board class is used within some internal logic
        decisions and thus is needed.

        deck: a game_classes.py deck class to be used as the deck to have cards
        drawn from.

        players: a game_classes.py player that will iterate through allowing for
        turns with each player.
    '''
    turn_iterator = 1
    turn = 0
    turn_tot = 0
    drop_again = False
    while True:

        for player in range(len(players)):
            player = players[turn]
            print("Turn number:", turn_tot)
            print("Players", turn + 1, "turn")
            print("PLAYER: ", player.name, "TURN")

            if player.skip:
                print("skipping", player.name, "turn")
                player.skip = False

            else:
                turn_done = False
                selected = None

                allowed_card_list = card_allowed(board, player)
                print("allowed cards: ", allowed_card_list)

                display_funct.redraw_screen([(player, None)], board, players)

                while not turn_done:
                    (update, selected, turn_done) = player_turn(
                        board, deck, player, allowed_card_list, selected)

                    if player.hand == []:  # conditions for winning!
                        print(str(player.name), "wins!!")
                        while 1:
                            for event in pygame.event.get():
                                game_control.get_keypress(event)

                    if update:
                        update = False
                        if selected is None:
                            display_funct.redraw_screen(
                                [(player, None)], board, players)
                        else:
                            display_funct.redraw_screen(
                                [(player, allowed_card_list[selected])], board, players)

                (turn_iterator, drop_again) = card_logic.card_played_type(
                    board, deck, player, players, turn_iterator)

            if drop_again:  # if the player plays a drop agian card dont iterate turn
                drop_again = False
                continue
            else:
                turn = turn + turn_iterator
                # catch to reloop overs players array
                if turn < 0:
                    turn = len(players) - 1
                elif turn >= len(players):
                    turn = 0
                print("Turn iterator: ", turn_iterator)
                print("Turn end \n\n")
                turn_tot += 1
########################################################
