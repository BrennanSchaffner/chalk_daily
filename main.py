# https://developers.google.com/sheets/api/quickstart/python
# might have to enable the api and get credentials and install package^

# make desktop icon: https://www.hackster.io/kamal-khan/desktop-shortcut-for-python-script-on-raspberry-pi-fd1c63

from datetime import date
import calendar
import pygame as pg
import easygui
import sys
import os.path
import urllib

from sheet_reader import SheetReader

# this means debug lines that run on my windows laptop ->#######################################
# TODO: Rethink dates


def main():
    ss_id = get_sheet_url()
    if ss_id:
        display(ss_id)
    else:
        easygui.msgbox('I don\'t like that link for some reason - Brennan', 'The first shot does not beat you. - Chuck Daily')
        sys.exit()
    # test_display()


def internet_connected(host='http://google.com'):
    try:
        urllib.request.urlopen(host) #Python 3.x
        return True
    except:
        return False


def get_sheet_url():
    url = easygui.enterbox("Your Google sheet URL")
    if url == '' or url is None:
        sys.exit()

    try:
        after_d = url.split('/d/')[1]
        spreadsheet_id = after_d.split('/edit')[0]
    except:
        return 0

    # sheet_id = after_d.split('/edit#gid=')[1]

    return spreadsheet_id


def display(ss_id):
    successes, failures = pg.init()
    print("{0} successes and {1} failures".format(successes, failures))
    width, height = pg.display.Info().current_w, pg.display.Info().current_h
    window = pg.display.set_mode((width, height), pg.FULLSCREEN, pg.RESIZABLE)

    # create a font object.
    # 1st parameter is the font file
    # which is present in pygame.
    # 2nd parameter is size of the font
    if os.path.isfile('/home/pi/chalk_daily/chawp.ttf'):
        date_font = pg.font.Font(r'/home/pi/chalk_daily/chawp.ttf', 32)
        quote_font = pg.font.Font(r'/home/pi/chalk_daily/chawp.ttf', 50)
        event_font = pg.font.Font(r'/home/pi/chalk_daily/chawp.ttf', 28)
    else: ###############################
        date_font = pg.font.Font(r'.\chawp.ttf', 40)
        quote_font = pg.font.Font(r'.\chawp.ttf', 50)
        event_font = pg.font.Font(r'.\chawp.ttf', 34)

    # set the pygame window name
    pg.display.set_caption('Chalk Daily')

    # create a surface object, image is drawn on it.
    if os.path.isfile('/home/pi/chalk_daily/green_chalkboard.jpg'):
        chalkboard = pg.image.load(r'/home/pi/chalk_daily/green_chalkboard.jpg')
    else: #############################
        chalkboard = pg.image.load(r'.\green_chalkboard.jpg')

    # copying the image surface object
    # to the display surface object at
    # (0, 0) coordinate.
    window.blit(chalkboard, (0, 0))

    white = (255, 255, 255)

    done = False
    while not done:
        today = date.today()
        day_name = calendar.day_name[today.weekday()]
        date_str_no_year = day_name + ", " + today.strftime("%B %d")
        date_str = date_str_no_year + ", " + today.strftime("%Y")

        window.blit(chalkboard, (0, 0))

        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    done = True

        # create a text surface object,
        # on which text is drawn on it.
        date_text = date_font.render(date_str, True, white)

        # create a rectangular object for the
        # text surface object
        date_rect = date_text.get_rect()

        # set the center of the rectangular object.
        w, h = pg.display.get_surface().get_size()
        date_rect.bottomleft = (w // 8, 7 * h // 8)

        window.blit(date_text, date_rect)
        internet = True
        internet = internet_connected()
        try:
            info_dict = what_data(date_str, date_str_no_year, ss_id)
        except:
            internet = False

        if internet:
            if info_dict:
                if info_dict['quote'] == '':
                    info_dict['quote'] = 'Quotes from people you respect! - Brennan'
                if len(info_dict['quote']) <= 26:
                    quote_text = quote_font.render(info_dict['quote'], True, white)
                    quote_rect = quote_text.get_rect()
                    quote_rect.midleft = (w // 8, h // 2)
                    window.blit(quote_text, quote_rect)
                else:
                    quote_str = info_dict['quote']
                    quote_text = []
                    while len(quote_str) > 26:
                        last_space = quote_str.rfind(' ', 0, 26)
                        quote_text.append((quote_font.render(quote_str[:last_space], True, white)))
                        quote_str = quote_str[last_space:]
                    quote_text.append(quote_font.render(quote_str, True, white))
                    for line in range(len(quote_text)):
                        window.blit(quote_text[line], (w // 8, (h // 3) + line*quote_font.get_linesize()))

                event_font.set_underline(True)
                week_header_text = event_font.render(info_dict['week_header'], True, white)
                event_font.set_underline(False)
                window.blit(week_header_text, (5.7 * w // 8, (1 * h // 8)))

                week_view_text = []
                for line in info_dict['week_events']:
                    week_view_text.append(event_font.render(line, True, white))
                for line in range(len(week_view_text)):
                    window.blit(week_view_text[line], (5.25 * w // 8, (1.1 * h // 8) + (line+1)*(event_font.get_linesize() + 0.1//8)))
                    bottom_of_week_events = (1.1 * h // 8) + (line+1)*event_font.get_linesize()

                event_font.set_underline(True)
                upcoming_header_text = event_font.render(info_dict['future_header'], True, white)
                event_font.set_underline(False)
                window.blit(upcoming_header_text, (5.7 * w // 8, (bottom_of_week_events + h // 8)))

                upcoming_view_text = []
                for line in info_dict['important_events']:
                    upcoming_view_text.append(event_font.render(line, True, white))
                for line in range(len(upcoming_view_text)):
                    window.blit(upcoming_view_text[line], (5.25 * w // 8, (bottom_of_week_events + (1.1*h // 8) + (line+1)*(event_font.get_linesize() + 0.1//8))))
            else:
                quote_text = quote_font.render("I couldn't find today in your sheet", True, white)
                quote_rect = quote_text.get_rect()
                quote_rect.midleft = (w // 8, h // 2)
                window.blit(quote_text, quote_rect)
                quote_text = quote_font.render("- Brennan", True, white)
                quote_rect = quote_text.get_rect()
                quote_rect.midleft = (w // 8, h // 2 + quote_font.get_linesize() + 1//8)
                window.blit(quote_text, quote_rect)
        else:
            quote_text = quote_font.render("If I were connected to the internet,", True, white)
            quote_rect = quote_text.get_rect()
            quote_rect.midleft = (w // 8, h // 2)
            window.blit(quote_text, quote_rect)
            quote_text = quote_font.render("there would be a cool quote here.", True, white)
            quote_rect = quote_text.get_rect()
            quote_rect.midleft = (w // 8, h // 2 + quote_font.get_linesize() + 1 // 8)
            window.blit(quote_text, quote_rect)

        pg.display.flip()
        if not done:
            pg.time.wait(10)  # ms

    pg.display.quit()
    pg.quit()


def what_data(date_str, date_str_no_year, ss_id):
    # The ID and range of a sample spreadsheet.
    spreadsheet_id = ss_id
    sheet_range = 'A1:F'

    sheet_reader = SheetReader(spreadsheet_id, sheet_range)
    values = sheet_reader.download_data()
    if not values:
        print('No data found.')

    ret_struct = {'date': date_str}
    try:
        ret_struct['week_header'] = values[0][2]
    except IndexError:
        ret_struct['week_header'] = "WEEK VIEW"

    try:
        ret_struct['future_header'] = values[0][5]
    except IndexError:
        ret_struct['week_header'] = "COMING UP"

    ret_struct['week_events'] = []
    todays_index = None
    for i in range(1, len(values)):
        try:
            test = values[i][0][0]
        except IndexError:
            values[i][0] = 'TBD,TBD'

        if values[i][0] == date_str or values[i][0] == date_str_no_year:
            today = values[i]
            todays_index = i
            try:
                ret_struct['quote'] = today[1]
            except IndexError:
                ret_struct['quote'] = 'Your quote here!'

            for d in range(0, 7):
                try:
                    test = values[i+d][0][0]
                except IndexError:
                    values[i+d][0] = 'TBD,TBD'

                ret_struct['week_events'].append(values[i+d][0][:3].upper() + ': ')
                first_event_in_day = True
                if len(values[i+d]) > 2 and values[i+d][2] != '':
                    ret_struct['week_events'][len(ret_struct['week_events'])-1] += (values[i+d][2])
                    first_event_in_day = False

                if len(values[i+d]) > 4 and values[i+d][4] != '':
                    if first_event_in_day:
                        ret_struct['week_events'][len(ret_struct['week_events'])-1] += (values[i+d][4])
                        first_event_in_day = False
                    else:
                        ret_struct['week_events'].append('       '+values[i+d][4])
            break
    if todays_index is None:
        return 0

    ret_struct['important_events'] = []
    for row in values[todays_index+7:]:
        try:
            test = row[0][0]
        except IndexError:
            row[0] = 'TBD,TBD'

        if len(row) > 2 and row[2] != '':
            if (len(row) > 3) and (row[3] == '*') and (len(ret_struct['important_events']) < 8):
                ret_struct['important_events'].append(row[0].split(',')[1] + ': ' + row[2])
        if len(row) > 4 and row[4] != '':
            if (len(row) > 5) and (row[5] == '*') and (len(ret_struct['important_events']) < 8):
                ret_struct['important_events'].append(row[0].split(',')[1] + ': ' + row[4])

    return ret_struct


def test_display(): #####################
    import pygame
    successes, failures = pygame.init()
    print("{0} successes and {1} failures".format(successes, failures))

    screen = pygame.display.set_mode((720, 480), pg.RESIZABLE)
    clock = pygame.time.Clock()
    FPS = 60  # Frames per second.

    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    # RED = (255, 0, 0), GREEN = (0, 255, 0), BLUE = (0, 0, 255).

    rect = pygame.Rect((0, 0), (32, 32))
    image = pygame.Surface((32, 32))
    image.fill(WHITE)

    while True:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    rect.move_ip(0, -2)
                elif event.key == pygame.K_s:
                    rect.move_ip(0, 2)
                elif event.key == pygame.K_a:
                    rect.move_ip(-2, 0)
                elif event.key == pygame.K_d:
                    rect.move_ip(2, 0)

        screen.fill(BLACK)
        screen.blit(image, rect)
        pygame.display.update()  # Or pygame.display.flip()


if __name__ == '__main__':
    main()
