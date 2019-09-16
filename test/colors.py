import sys

sys.path.append('../hallucinator')
import hallucinator

hallucinator.save_img(hallucinator.canvas(1000, 1000, color=(0, 0, 0)), filename='black')
'''hallucinator.save_img(hallucinator.canvas(1000, 1000, color=(0, 0, 254)), filename='almost_blue')
hallucinator.save_img(hallucinator.canvas(1000, 1000, color=(1, 0, 255)), filename='blue_with_red')
hallucinator.save_img(hallucinator.canvas(1000, 1000, color=(10, 0, 255)), filename='blue_with_more_red')'''

