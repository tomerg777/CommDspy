from enum import Enum
from matplotlib.colors import LinearSegmentedColormap

class PrbsEnum(Enum):
    PRBS7  = 7
    PRBS9  = 9
    PRBS11 = 11
    PRBS13 = 13
    PRBS15 = 15
    PRBS31 = 31


class ConstellationEnum(Enum):
    NRZ  = 0
    OOK  = 1
    PAM3 = 2
    PAM4 = 3


EYE_COLORMAP = LinearSegmentedColormap("",{
    'red':   [(  0.0,     0.0,    0.0),
              ( 1/30,  50/255, 50/255),
              ( 1/24,  16/255, 16/255),
              ( 1/22, 236/255, 236/255),
              ( 1/18, 191/255, 191/255),
              ( 2/12, 233/255, 233/255),
              ( 4/10, 244/255, 244/255),
              (11/11, 255/255, 255/255)],
    'green': [(  0.0,     0.0,     0.0),
              ( 1/30, 194/255, 194/255),
              ( 1/24,  69/255,  69/255),
              ( 1/22,  47/255,  47/255),
              ( 1/18,  21/255,  21/255),
              ( 2/12, 168/255, 168/255),
              ( 4/10, 234/255, 234/255),
              (11/11, 255/255, 255/255)],
    'blue': [(   0.0,     0.0,     0.0),
              ( 1/30,  45/255,  45/255),
              ( 1/24, 201/255, 201/255),
              ( 1/22, 173/255, 173/255),
              ( 1/18,  17/255,  17/255),
              ( 2/12,   0/255,   0/255),
              ( 4/10, 146/255, 146/255),
              (11/11, 255/255, 255/255)]})

