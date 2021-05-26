import os
import glob
import pandas as pd
from psychopy import core, visual, event
import random
import time

# insert subject input here
sub_id='01'
age=23
sex='f'
glasses=True

# paths to visual stimuli
img_dir = os.getcwd() + '/session_3/exp_stim/'
img_list = glob.glob(img_dir + '*.jpg')

train_img_dir = os.getcwd() + '/session_3/train_stim/'
train_img_list = glob.glob(train_img_dir + '*.jpg')

# constants 
max_train_trials = len(train_img_list)
max_trials = len(img_list)
max_blocks = 3

# keyboard input
trial_keys = ['a', 'l']
continue_key = 'space'

# stuff specific to our experiment
win = visual.Window(
    color='black',
    size=[2560, 1440],
    fullscr=True)

instructions = {
    'instructions_1' : 'Willkommen zu unserem Experiment: \n\n Human or Cat? \n\n' \
    'Mit diesem Experiment wollen wir untersuchen, wie das Gehirn Bilder von Katzen ' \
    'und Menschen unter erschwerten Bedingungen verarbeitet. \n\n'
    'Drücken Sie die Leertaste um fortzufahren ...',
    'instructions_2' : 'Im Experiment werden Ihnen pro Durchgang ' \
    'jeweils 16 visuelle Stimuli präsentiert. Dabei handelt es sich um am Computer ' \
    'erzeugte Bilder von Menschen oder Katzen. ' \
    'Zusätzlich werden diese Bilder 180° gedreht und lediglich 1,5 Sekunden präsentiert. ' \
    '\n\n Ihre Aufgabe ist es: (1) zu entscheiden, ob Ihnen ein Mensch oder eine Katze ' \
    'präsentiert wurde und (2) so schnell wie möglich auf den Stimulus zu reagieren. \n\n' \
    'Drücken Sie die Leertaste um fortzufahren ...',
    'instructions_3' : 'Bitte drücken sie die Taste (A) für Mensch und (L) für Katze. ' \
    'Legen Sie dazu nun die Finger jetzt auf die entsprechenden Tasten.' \
    'Wir beginnen das Experiment mit einigen Probedurchgängen. Anschließend bekommen Sie Feedback ' \
    'über Ihre Leistung. \n\n Erst im anschließenden Experiment' \
    'werden die Bilder gedreht. Feedback wird es dort nicht mehr geben. Viel Erfolg! \n\n' \
    'Drücken Sie die Leertaste um die Probedurchgänge zu beginnen ...'
    }

# experiment functions
def present_text(window_instance,
                 instr_text='Ich bin der Standardsatz!',
                 text_size=0.075,
                 instructions=True,
                 text_position=(0., 0.),
                 unit='norm',
                 continue_key='space'):
    
    text_stim = visual.TextStim(window_instance, 
                                height=text_size, 
                                units=unit, 
                                pos=text_position)
    text_stim.setText(instr_text)
    text_stim.draw()
    window_instance.flip()
    
    if instructions == True:
        event.waitKeys(keyList=[continue_key])
    else:
        core.wait(2)
    return None

def draw_fixation(window_instance,
                  fixation_position=(0., 0.)):
    
    fixation = visual.ShapeStim(window_instance,
                                pos=fixation_position,
                                vertices=((0, -0.025), (0, 0.025), (0,0), (-0.015,0), (0.015, 0)),
                                lineWidth=5,
                                closeShape=False,
                                lineColor='white')
    fixation.draw()
    window_instance.update()
    core.wait(1.0)
    return None

def present_img(window_instance,
                img_input,
                trial_dur=2.0,
                image_position=(0., 0.),
                training=False,
                trial_keys='space'):
    
    substring = 'cat'
    
    if training == True:
        orientation = 0.0
    else:
        orientation = 180.0
    
    image_stim = visual.ImageStim(window_instance,
                                  image=img_input,
                                  ori=orientation,
                                  pos=image_position)
    image_stim.draw()
    window_instance.flip()   
    
    # NEW: start trial timer
    start_time = time.process_time()
    
    response = event.waitKeys(maxWait=trial_dur,
                              timeStamped=False, 
                              keyList=trial_keys)
    
    # assign variable once before called
    accuracy = None

    if training == True:
        if response == ['a'] and substring in img_input:
            present_text(window_instance=win,
                         instr_text='Sie haben (A) gedrückt und eine Katze gesehen' \
                         ' ihre Antwort ist falsch!',
                         instructions=False)
            rt = (time.process_time() - start_time)
        
        elif response == ['l'] and substring in img_input:
            present_text(window_instance=win,
                         instr_text='Sie haben (L) gedrückt und eine Katze gesehen' \
                         ' ihre Antwort ist korrekt!',
                         instructions=False)
            rt = (time.process_time() - start_time)
            
        elif response == ['a'] and not substring in img_input:
            present_text(window_instance=win,
                         instr_text='Sie haben (A) gedrückt und einen Menschen gesehen' \
                         ' ihre Antwort ist korrekt!',
                         instructions=False)
            rt = (time.process_time() - start_time)
                
        elif response == ['l'] and not substring in img_input:
            present_text(window_instance=win,
                         instr_text='Sie haben (L) gedrückt und einen Menschen gesehen' \
                         ' ihre Antwort ist falsch!',
                         instructions=False)
            rt = (time.process_time() - start_time)
                
        elif response == None:
            present_text(window_instance=win,
                         instr_text='Sie haben nichts gedrückt, ihre Antwort wird' \
                         ' als falsch gewertet!',
                         instructions=False)
            rt = (time.process_time() - start_time)
    else:
        if response == ['a'] and substring in img_input:
            accuracy = False
            rt = (time.process_time() - start_time)
        
        elif response == ['l'] and substring in img_input:
            accuracy = True
            rt = (time.process_time() - start_time)
            
        elif response == ['a'] and not substring in img_input:
            accuracy = True
            rt = (time.process_time() - start_time)
                
        elif response == ['l'] and not substring in img_input:
            accuracy = False
            rt = (time.process_time() - start_time)
                
        elif response == None:
            accuracy = False
            response = 'NaN'
            rt = (time.process_time() - start_time)
    
    window_instance.flip()
    core.wait(trial_dur)
    return accuracy, response, orientation, rt

# NEW: gen file path, empty df and file
def gen_file(sub_id):
    
    output_path = os.getcwd() + f'/sub-{sub_id}'
    
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    
    behav_data = pd.DataFrame({'sub_id' : [], 
                              'age' : [],
                              'sex' : [],
                              'glasses' : [],
                              'block' : [],
                              'trial' : [],
                              'reaction_time' : [],
                              'accuracy' : [],
                              'orientation' : []})
    
    file_path = output_path + f'/sub-{sub_id}_task-catshumans.tsv'
    return behav_data, file_path

def collect_responses(sub_id,
                      age,
                      sex, 
                      glasses,
                      block,
                      trial,
                      reaction_time,
                      accuracy,
                      key_pressed,
                      orientation):
    
    trial_column = pd.DataFrame({'sub_id' : [sub_id], 
                                 'age' : [age],
                                 'sex' : [sex],
                                 'glasses' : [glasses],
                                 'block' : [block],
                                 'trial' : [trial],
                                 'reaction_time' : [reaction_time],
                                 'accuracy' : [accuracy],
                                 'key_pressed' : [key_pressed],
                                 'orientation' : [orientation]})
    return trial_column

def present_ITI(window_instance,
                duration=0.5):
    window_instance.update()
    core.wait(duration)
    return None

def start_experiment(win,
                     instruction_dict,
                     train_trial_num,
                     train_list,
                     image_list,
                     trial_num, 
                     block_num):
    
    # start with some sanity checks
    if type(image_list) != list:
        raise ValueError('Image list is not type list.')
    
    if trial_num != len(image_list):
        raise ValueError('Maximum number of trials does not match number of input stimuli.')
    
    # NEW: get empty df, file path
    sub_data, file_path = gen_file(sub_id)
    
    # begin with instructions
    for instruction_text in instructions.values():
        present_text(window_instance=win,
                     instr_text=instruction_text,
                     instructions=True,
                     continue_key=continue_key)
    
    # start practice trials
    for training_trials in range(train_trial_num):
        draw_fixation(window_instance=win,
                      fixation_position=(0., 0.))
        
        present_img(window_instance=win,
                    img_input=train_list[training_trials],
                    training=True,
                    trial_keys=trial_keys)
        
        present_ITI(window_instance=win,
                    duration=0.5)
    
    # beginning of the actual experiment
    for block in range(block_num):
        # randomly shuffle order of the image list
        shuffled_list = random.sample(img_list, len(img_list))
        
        present_text(window_instance=win,
                     instr_text=f'Starte Block Nummer: {block + 1} \n\n' \
                         'Leertaste um zu beginnen ...')
        
        for trial in range(trial_num):
            draw_fixation(window_instance=win,
                      fixation_position=(0., 0.))
            
            accuracy, response, orientation, rt = present_img(window_instance=win,
                        img_input=shuffled_list[trial],
                        training=False,
                        trial_keys=trial_keys)
            
            # NEW: write data to file
            sub_data = sub_data.append(collect_responses(sub_id=sub_id,
                                                         age=age,
                                                         sex=sex,
                                                         glasses=glasses,
                                                         block=block,
                                                         trial=trial,
                                                         reaction_time=rt,
                                                         accuracy=accuracy,
                                                         key_pressed=response,
                                                         orientation=orientation))
            try:
                sub_data.to_csv(file_path, 
                                index=False,
                                sep='\t')
            except:
                print(f'Error saving file: {file_path}')
            
            present_ITI(window_instance=win,
                    duration=0.5)
    
    # NEW: present farewell
    present_text(window_instance=win,
                     instr_text='Vielen Dank für Ihre Teilnahme! \n\n' \
                         'Das Experiment ist nun abgeschlossen.')
    return None

# finally start the experiment!
start_experiment(win=win, 
                 instruction_dict=instructions, 
                 train_trial_num=max_train_trials, 
                 train_list=train_img_list,
                 image_list=img_list,
                 trial_num=max_trials,
                 block_num=max_blocks)