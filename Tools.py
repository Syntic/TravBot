from bs4 import BeautifulSoup
import time

#Auction price grabber
#looks for timer=0:00:00 and puts silver price in an output .csv file
def get_auctions(server, session, minutes):

    #set endtime for timer of function
    t_end = time.time() + 60 * minutes

    #open output file
    f = open('output.csv', 'a', encoding='utf-8')

    while (time.time() < t_end):
        url = server + 'hero_auction.php'
        text = session.get(url)
        auction_soup = BeautifulSoup(text.content, "html.parser")
        type(auction_soup)

        table = auction_soup.find('table')

        name = ''
        silver = ''
        timer = ''

        #search table for tr and td tags
        for row in table.findAll('tr'):
            cells = row.findAll('td')
            timer_element = row.find('span' , { 'class' : 'c0 t' })
            if (timer_element != None):
                #For each "tr", assign each "td" to a variable.
                if len(cells) == 6:
                    name = str(cells[1].find(text=True))
                    silver = str(cells[3].findAll(text=True))
                    silver = silver[:-8][10:]
                    timer = str(cells[4].find(text=True))

                    write_to_file = name + ";" + silver + ";" + timer + "\n"
                    print(write_to_file)
                    f.write(write_to_file)

        #timeout to prevent identical entries - 5 seconds
        time.sleep(5)

    #close file
    f.close()