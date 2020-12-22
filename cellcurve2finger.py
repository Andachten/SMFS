import os
import numpy as np
import copy
import time
import matplotlib.pyplot as plt
from scipy import signal
from scipy.ndimage import gaussian_filter
from PIL import Image
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random
import PySimpleGUI as sg
sg.ChangeLookAndFeel('DefaultNoMoreNagging')
def spring_cal(data,springconstant):
    data[:,1] = data[:,1] - data[:,0]/springconstant
    return data
def smoothing(data):
    _, ys = data[:, 1], data[:, 0]
    smoothed = gaussian_filter(ys, 17.)
    return smoothed
def fig2img(fig):
    fig.canvas.draw()
    img = Image.frombytes('RGB', fig.canvas.get_width_height(), fig.canvas.tostring_rgb())
    return img
class datapro():
    def __init__(self):
        self.log = {
                  'methods':{'src':'',
                             'todir':''},
                  'result':{}}
        self.filename_lst = []
    def GetFileName(self):
        self.filename_lst = []
        for a, b, c in os.walk(self.log['methods']['src']):
            for i in c:
                if i.endswith('txt'):
                    self.filename_lst.append(os.path.join(a,i))
    def GetData(self,index,curvetype='retract,extend'):
        filename = self.filename_lst[index]
        with open(filename,'r') as f:
            x = f.read()
        lst = x.split('\n')
        lst1 = np.array([0., 0.])
        data = np.array([0., 0.])
        j = False
        for i in lst:
            if 'springConstant' in i:
                spring_constant = float(i.split()[-1])*1e12/1e9
            if 'retract' in curvetype and '# segment: retract' ==  i:
                j = True
            if 'extend' in curvetype and '# segment: extend' == i:
                j = True
            if 'xPosition' in i:
                j = False
            if j and '#' not in i and i:
                lst1[0], lst1[1] = float(i.split(' ')[1])*-1*1e12, float(i.split(' ')[0])*1e9
                data = np.vstack((data,np.array(lst1)))
        data_dic = dict(data = data[1:], springconstant = spring_constant)
        return data_dic
    def getfinger(self,index):
        self.GetFileName()
        data_dic = self.GetData(index,'retract')
        data = data_dic['data']
        springconstant = data_dic['springconstant']
        data = spring_cal(data,springconstant)
        data_2d = np.gradient(np.gradient(smoothing(data)))[40:]
        peak = signal.find_peaks(data_2d)[0]
        peak1 = signal.find_peaks(data_2d * -1)[0]
        up = copy.deepcopy(data_2d)
        down = copy.deepcopy(data_2d)
        for i in range(len(data_2d)):
            if i not in peak:
                up[i] = 0
            if i not in peak1:
                down[i] = 0
        fig = plt.figure(figsize=(2.24, 2.24))
        fig1 = plt.figure()
        ax = fig.add_subplot(111)
        ax1=fig1.add_subplot(111)
        ax.axis('off')
        ax1.plot(data[:,1],data[:,0])
        plt.subplots_adjust(top=1, bottom=0.1, right=1, left=0.1)
        plt.gca().xaxis.set_major_locator(plt.NullLocator())
        plt.gca().yaxis.set_major_locator(plt.NullLocator())
        ax.plot(up, color='#FF0000', linewidth=0.8)
        ax.plot(down , color = '#0000FF', linewidth=0.8)
        plt.close()
        return {'finger':fig,'ori':fig1}
    def done(self):
        savedir = os.path.join(self.log['methods']['todir'],'img')
        if not os.path.exists(savedir):
            os.makedirs(savedir)
        for index,v in self.log['result'].items():
            savedir_= os.path.join(savedir,str(v))
            if not os.path.exists(savedir_):
                os.makedirs(savedir_)
            fig_dic = self.getfinger(index)
            finger = fig_dic['finger']
            img = fig2img(finger)
            img = img.resize((224,224))
            img.save(os.path.join(savedir_,str(random.randint(10,99))+str(time.time())[8:]+'.jpg'))
            plt.close()


dp = datapro()
def PyplotGGPlotSytleSheet():
    np.random.seed(19680801)

    fig, axes = plt.subplots(ncols=2, nrows=2)
    ax1, ax2, ax3, ax4 = axes.ravel()

    x, y = np.random.normal(size=(2, 200))
    ax1.plot(x, y, 'o')

    L = 2 * np.pi
    x = np.linspace(0, L)
    ncolors = len(plt.rcParams['axes.prop_cycle'])
    shift = np.linspace(0, L, ncolors, endpoint=False)
    for s in shift:
        ax2.plot(x, np.sin(x + s), '-')
    ax2.margins(0)

    x = np.arange(5)
    y1, y2 = np.random.randint(1, 25, size=(2, 5))
    width = 0.25
    ax3.bar(x, y1, width)
    ax3.bar(x + width, y2, width,
            color=list(plt.rcParams['axes.prop_cycle'])[2]['color'])
    ax3.set_xticks(x + width)
    ax3.set_xticklabels(['a', 'b', 'c', 'd', 'e'])

    for i, color in enumerate(plt.rcParams['axes.prop_cycle']):
        xy = np.random.normal(size=2)
        ax4.add_patch(plt.Circle(xy, radius=0.3, color=color['color']))
    ax4.axis('equal')
    ax4.margins(0)
    fig = plt.gcf()  # get the figure to show
    return fig


def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg


def delete_figure_agg(figure_agg):
    figure_agg.get_tk_widget().forget()
    plt.close('all')


figure_w, figure_h = 400, 500
listbox_values = []
col_listbox = [[sg.Text('Num.', size=(4, 1), font='Any 18'),sg.InputText('0', size=(4, 1),font='Any 18',key='NUM')],
    [sg.Button('A', size=(4, 1), font='Any 25'),sg.Text(' ', size=(2, 1), font='Any 18'),sg.Button('B', size=(4, 1), font='Any 25')],
    [sg.InputText('0', size=(3, 1), key='-A-', font='Any 18'),sg.Text('/0', key='-Anum-', size=(4, 1), font='Any 18'),sg.InputText('0', size=(3, 1), key='-B-', font='Any 18'),
     sg.Text('/0', key='-Bnum-', size=(4, 1), font='Any 18')],
    [sg.Text(' ', size=(4, 1), font='Any 18'), ],
[sg.Button('C', size=(4, 1), font='Any 25'),sg.Text(' ', size=(2, 1), font='Any 18'), sg.Button('D', size=(4, 1), font='Any 25')],
[sg.InputText('0', size=(3, 1), key='-C-', font='Any 18'),sg.Text('/0', key='-Cnum-', size=(4, 1), font='Any 18'),sg.InputText('0', size=(3, 1), key='-D-', font='Any 18'),
     sg.Text('/0', key='-Dnum-', size=(4, 1), font='Any 18')],
[sg.Text(' ', size=(4, 1), font='Any 18'), ],
    [sg.Button(u'⬅', size=(4, 1), font='Any 15'), sg.InputText('0', size=(3, 1), key='-INDEX-', font='Any 18'),
     sg.Text('/0', key='-COUNT-', size=(4, 1), font='Any 18'), sg.Button('➡', size=(4, 1), font='Any 15'),
     sg.Button('Goto', size=(4, 1), font='Any 15')],
[sg.Text('SRC', size=(5, 1), auto_size_text=False, justification='left',font='Any 18'),\
     sg.InputText('Default Folder',font='18',size=(17, 1)), \
     sg.FolderBrowse()],
    [sg.Text('TODIR', size=(5, 1), auto_size_text=False, justification='left',font='Any 18'),\
     sg.InputText('Default Folder',font='18',size=(17, 1)), \
     sg.FolderBrowse()],
[sg.Button('START', size=(4, 1), font='Any 15'),sg.Button('DONE', size=(4, 1), font='Any 15')],
]

col_multiline = sg.Col([[sg.MLine(size=(70, 35), key='-MULTILINE-')]])
col_canvas = sg.Col([[sg.Canvas(size=(figure_w, figure_h), key='-CANVAS-')]])
col_instructions = sg.Col([[sg.Pane([col_canvas, col_multiline], size=(700, 500))],
                           [sg.Text('Grab square above and slide upwards to view source code for graph')]])

layout = [[sg.Text('AFM Sigle Molecular Force Spectrum', font=('ANY 18'))],
          [sg.Col(col_listbox, justification='t'), col_instructions], ]
window = sg.Window('DataYEE6',
                   layout, resizable=True, finalize=True)

canvas_elem = window['-CANVAS-']
multiline_elem = window['-MULTILINE-']
figure_agg = None
while True:
    if 'site' not in dir() and 'length' not in dir():
        fig = PyplotGGPlotSytleSheet()
        figure_agg = draw_figure(
            window['-CANVAS-'].TKCanvas, fig)
    event, values = window.read()
    if event in (sg.WIN_CLOSED, 'Exit'):
        break
    if figure_agg:
        delete_figure_agg(figure_agg)
    if event == 'START':
        dp.log['methods']['src']=values['Browse']
        dp.log['methods']['todir'] = values['Browse0']
        dp.GetFileName()
        NUM = int(values['NUM'])
        length = len(dp.filename_lst)
        a,b,c,d=0,0,0,0
        index = 0
        window['-Anum-'].update('/'+str(NUM))
        window['-Bnum-'].update('/' + str(NUM))
        window['-Cnum-'].update('/' + str(NUM))
        window['-Dnum-'].update('/' + str(NUM))
        window['-INDEX-'].update(str(index+1))
        window['-COUNT-'].update(str(length))
    if 'index' in dir() and event == 'A' and a<NUM:
        dp.log['result'][index]=0
        index +=1
        a = list(dp.log['result'].values()).count(0)
    if 'index' in dir() and event == 'B' and b<NUM:
        dp.log['result'][index]=1
        index += 1
        b = list(dp.log['result'].values()).count(1)
    if 'index' in dir() and event == 'C' and c<NUM:
        dp.log['result'][index]=2
        index += 1
        c = list(dp.log['result'].values()).count(2)
    if 'index' in dir() and event == 'D' and d<NUM:
        dp.log['result'][index]=3
        index += 1
        d = list(dp.log['result'].values()).count(3)
    if 'index' in dir() and event == u'⬅':
        index = index - 1
        if index < 0:
            index = 0
    if 'index' in dir() and event == '➡':
        index = index + 1
        if index >= length:
            index = length - 1
    if 'index' in dir() and event == 'Goto':
        index = int(values['-INDEX-'])-1
        if index < 0:
            index = 0
        if index >= length:
            index = length - 1
    if 'index' in dir() and event == 'DONE':
        dp.done()
    if 'index' in dir():
        if index in dp.log['result'].keys():
            ms = str(dp.log['result'][index])
        else:
            ms = 'None'
        window['-MULTILINE-'].update(ms)
    window['-INDEX-'].update(str(index))
    window['-A-'].update(str(a))
    window['-B-'].update(str(b))
    window['-C-'].update(str(c))
    window['-D-'].update(str(d))
    if 'index' in dir() and index>=0 and index<length:
        fig_dic = dp.getfinger(index)
        finger = fig_dic['ori']
        figure_agg = draw_figure(
            window['-CANVAS-'].TKCanvas, finger)
window.close()