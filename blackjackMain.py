import blackjack
import story

def main():
    player = story.Player()
    blackjackGame = blackjack.Blackjack(player)
    # player.first_setup()
    player.opening_lines()
    while(True):
        blackjackGame.play_round()
        player.end_day()
        player.start_day()
        player.afternoon()


if __name__ == "__main__":
    main()