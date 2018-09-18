#python 3.7
#MovieFinder.py - GUI for top movies finder

from tkinter import *
import logging, topMovies,threading
from time import strftime



global searching
searching=False


def printReasults(Movies):
    searching=False
    logging.debug('printing results')
    #TODO: implement this function properly
    for i in Movies:
        print (i.getName().encode('utf-8'))

def checkRequest(year,amount):
    try:
        if year==None:
            logging.warning('Year not entered')
            messagebox.showinfo('Missing Year','Please enter a year')
            return False

        year=int(year)
        if year<1900 or year>int(strftime('%Y')):
            logging.warning('year value out of range')
            messagebox.showinfo('Year Invalid','Years must be between 1900 and {0}'.format(strftime('%Y')))
            return False

    except ValueError:
        logging.warning('year value not a number')
        messagebox.showinfo('Year Invalid','Year must be a number')
        return False

    except Exception as exc:
        logging.critical('Unknown error: '+str(exc))
        messagebox.showinfo('Unknown Error','Program has encountered an unknown error.\n (Please contact the developer(p.s it\'s Guy))')
        return False

    try:
        if amount==None:
            logging.warning('No amount entered')
            messagebox.showinfo('Missing amount','Please enter amount of movies to display')
        amount=int(amount)
        if amount<0 or amount>50:
            logging.warning('amount value out of range')
            messagebox.showinfo('Invalid amount','Amount has to be between 1 and 50')
            return False

    except ValueError:
        logging.warning('amount value not a number')
        messagebox.showinfo('Invalid amount','Amount has to be a number')
        return False
    except exception as exc:
        logging.critical('Unknown error: '+str(exc))
        messagebox.showinfo('Unknown Error','Program has encountered an unknown error.\n (Please contact the developer(p.s it\'s Guy))')
        return False

    return True

def getMovies():
    """
    retrieve movies
    """
    numOfMovies=int(moviesNum.get())
    logging.debug('rerieving movies for year:{0} ,type:{1}'.format(movieYear.get(),mediaType.get()))
    printReasults(topMovies.getMovies(mediaType.get(),movieYear.get(),10))



def startThread():
    global searching
    if checkRequest(movieYear.get(),moviesNum.get()):
        if not searching:
            logging.info('request details valid')
            searching=True
            t=threading.Thread(target=getMovies)
            t.start()
    logging.debug('request details not valid')



def setupResultGUI(root):
    pass
    """ setup GUI for results window"""
    # TODO: check this part
    #add listbox for movies and textbox for more information
    logging.debug('setting up Result window GUI')
    bottomFrame=Frame(root)
    bottomFrame.pack(side=BOTTOM)
    moviesFrame=Frame(bottomFrame)
    moviesFrame.pack(side=LEFT)
    scrollbarMovies=Scrollbar(moviesFrame)
    scrollbarMovies.pack(side=RIGHT,fill=Y)
    global movies
    movies=Listbox(moviesFrame,selectmode=SINGLE,height=10,yscrollcommand=scrollbarMovies.set)
    movies.pack(side=LEFT)
    scrollbarMovies.config(command=movies.yview)
    logging.debug('added movies listbox and scrollbar')
    global movieVar
    movieVar=StringVar()
    movieDetails=Message(bottomFrame,textvariable=movieVar,width=200,padx=25)
    movieDetails.pack(side=RIGHT)
    logging.debug('added movie details message')

    logging.debug('result window GUI setup finished')



def setupMainGUI(root):
    """setup GUI for main window
    adds textboxes and labels for amount of movies and movie year
    adds labelFrame for radiobuttons for selecting media type
    adds submit button
    """
    try:

        logging.debug('created TK object')
        topFrame=Frame(root)
        topFrame.pack()

        #add textBox for number of movies
        movieAmount=Frame(topFrame)
        movieAmount.pack(side=TOP)
        numLbl=Label(movieAmount,text='Amount:')
        numLbl.pack(side=TOP)
        global moviesNum
        moviesNum=Entry(movieAmount,width=10)
        moviesNum.pack(side=LEFT)
        logging.debug('added entry for number of movies')

        #add spacer
        spacer1=Label(topFrame,text='    ')
        spacer1.pack(side=BOTTOM)

        #add textbox for the movie year
        moviesYear=Frame(topFrame)
        moviesYear.pack(side=BOTTOM)
        yearLbl=Label(moviesYear,text='Year:')
        yearLbl.pack(side=TOP)
        global movieYear
        movieYear=Entry(moviesYear,width=10)
        movieYear.pack(side=LEFT)
        logging.debug('added Entry for the movie year')


        #create frame and radiobuttons for selecting media type
        typeFrame=LabelFrame(root,text='Choose type:')
        typeFrame.pack(fill='both',expand='yes')
        logging.debug('added labelFrame')

        mediaFrame=Frame(typeFrame)
        mediaFrame.pack(side=LEFT)
        global mediaType
        mediaType=StringVar()
        R1=Radiobutton(mediaFrame,text='Shows',value='1',variable=mediaType)
        R1.pack()
        R2=Radiobutton(mediaFrame,text='Movies',value='2',variable=mediaType)
        R2.pack()
        R3=Radiobutton(mediaFrame,text='Animated',value='3',variable=mediaType)
        R3.pack()
        R1.select()
        logging.debug('added media radiobuttons')



        #add submit button
        subBtn=Button(root,command=startThread,text='   Search   ')
        subBtn.pack(side=BOTTOM)
        logging.debug('added submit button')

        #add spacer
        spacer2=Label(root,text='    ')
        spacer2.pack(side=BOTTOM)



    except Exception as exc:
        logging.critical('exception occured: '+str(exc))


def main():
    """main() - handles all functions
    seting up GUI, getting Movies list and then printing it"""
    logging.info('\n\n\n\n\n\n\n\n\n\n\n ##########program start##########')
    #set up GUI
    root=Tk()
    setupMainGUI(root)
    logging.info('main GUI setup finished')
    root.mainloop()




if __name__=='__main__':
    #set up logging
    logging.basicConfig(filename='guiLog.txt',level=logging.INFO, format='%(pathname)s : %(lineno)s - %(asctime)s - %(levelname)s - %(message)s')
    main()
