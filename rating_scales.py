import os
import glob
from psychopy import visual

train_img_dir = os.getcwd() + '/session_3/train_stim/'
train_img_list = glob.glob(train_img_dir + '*.jpg')

# stuff specific to our experiment
win = visual.Window(
    color='black',
    size=[2560, 1440],
    fullscr=True)

def present_img_rating(window_instance,
                       items=None):
    
    rate_me = visual.RatingScale(window_instance)
    item_1, item_2 = items[0], items[1]
    # item_1 = items[0]
    # item_2 = items[1]
    
    image_stim_1 = visual.ImageStim(window_instance,
                                  image=item_1,
                                  pos=(0.25, 0.25))
    
    image_stim_2 = visual.ImageStim(window_instance,
                                  image=item_2,
                                  pos=(-0.25, 0.25))
    
    while rate_me.noResponse:
        image_stim_1.draw()
        image_stim_2.draw()
        rate_me.draw()
        window_instance.flip()
        
    rating = rate_me.getRating()
    decisionTime = rate_me.getRT()
    choiceHistory = rate_me.getHistory()
    
    print(rating, decisionTime, choiceHistory)
    
present_img_rating(window_instance=win,
                   items=train_img_list)
