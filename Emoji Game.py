import os
from random import shuffle, randint
from guizero import App, Box, Picture, PushButton, Text, MenuBar, info

# set up functions
def match_emoji(matched):
    if matched:
        result.text_color = 'white'
        result.value = "Correct"
        score.value = int(score.value) + 1
    else:
        result.text_color = 'red'
        result.value = "Incorrect"
        score.value = int(score.value) - 1
    setup_round()
    
def setup_round():
    # set the path to the emoji folder on your computer
    emojis_dir = "emojis"

    # create a list of the locations of the emoji images
    emojis = [os.path.join(emojis_dir, f) for f in os.listdir(emojis_dir) if os.path.isfile(os.path.join(emojis_dir, f))]

    # shuffle the emojis
    shuffle(emojis)
        
    # for each picture in the list
    for picture in pictures:
        # make the picture a random emoji
        picture.image = emojis.pop()

    for button in buttons:
        # make the image feature of the PushButton a random emoji
        button.image = emojis.pop()
        # set the command to be called and pass False, as these emoji wont be the matching ones
        button.update_command(match_emoji, [False])

    # choose a new emoji
    matched_emoji = emojis.pop()

    # select a number at random
    random_picture = randint(0,8)
    
    # change the image feature of the Picture with this index in the list of pictures to the new emoji
    pictures[random_picture].image = matched_emoji

    random_button = randint(0,8)
    
    # change the image feature of the PushButton with this index in the list of buttons to the new emoji
    buttons[random_button].image = matched_emoji

    # set the command to be called and pass True, as this is the matching emoji
    buttons[random_button].update_command(match_emoji, [True])

def counter():
    timer.value = int(timer.value) - 1
    if int(timer.value) == 0:
        timer.cancel(counter)
        # reset the timer
        result.value = "Game Over"
        exit_window = app.yesno("Warning", "Times Up!! Your final score is " + str(score.value) + ". Would you like to play again?")     
        if exit_window == False:
            app.destroy()
        else:
            result.value = 'Get Ready'
            score.value = 0
            # start new round
            setup_round()
        # reset timer
        timer.value = "20"
        # reset result
        result.value = ""
        #restart timer
        timer.repeat(1000, counter)

    
# setup the app
app = App("emoji match")

extra_features = Box(app, width = 'fill')

# set up the result display
result = Text(extra_features, text = 'Get Ready')
result.bg = 'light blue'
result.text_color = 'white'
result.text_size = 16

# set up the timer
timer = Text(extra_features, text = 'Get Ready', align = 'right')
timer.value = 30
timer.repeat(1000, counter)

# set up score display
score = Text(extra_features, text = '0', align = 'left')

# create a box to house the grids
game_box = Box(app)

# create a box to house the pictures
pictures_box = Box(game_box, align = 'left', layout="grid")

# create a box to house the buttons
buttons_box = Box(game_box, align = 'right', layout="grid")

# create the an empty lists to add the buttons and pictures to
buttons = []
pictures = []

# create 9 PushButtons with a different grid coordinate and add to the list
for x in range(0,3):
    for y in range(0,3):
        # put the pictures and buttons into the lists
        picture = Picture(pictures_box, grid=[x,y])
        pictures.append(picture)
        button = PushButton(buttons_box, grid=[x,y])
        button.bg = 'grey'
        buttons.append(button)


setup_round()

app.display()
