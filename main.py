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
    # print(ss_id)
    if ss_id:
        display(ss_id)
    else:
        easygui.msgbox('I don\'t like that link for some reason - Brennan', 'The first shot does not beat you. - Chuck Daily')
        sys.exit()
    # test_display()


def internet_connected(host='http://google.com'):
    try:
        if sys.version_info.major == 3:
            urllib.request.urlopen(host)  # Python 3.x
        else:
            urllib.urlopen(host)
        return True
    except:
        return False


def get_sheet_url():
    output = easygui.buttonbox("","Let's get that sheet URL", ['Enter new link with keyboard', 'Use same as last time'])
    if output == 'Enter new link with keyboard':
        url = get_sheet_url_by_link()
        with open("last_sheet_id.txt", "w") as f:
            print(url)
            f.write(url)
        return url
    elif output == 'Use same as last time':
        if os.path.isfile('/home/pi/chalk_daily/last_sheet_id.txt'):
            with open("/home/pi/chalk_daily/last_sheet_id.txt", "r") as f:
                url = f.readline().strip()
                print(url)
                return url
            # except FileNotFoundError:
            #     print("didnt find a previously used sheet.")
        elif os.path.isfile('.\last_sheet_id.txt'):
            with open('.\last_sheet_id.txt', "r") as f:
                url = f.readline().strip()
                print(url)
                return url
    else:
        return 0


def get_sheet_url_by_link():
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
        date_font = pg.font.Font(r'/home/pi/chalk_daily/chawp.ttf', 40)
        quote_font = pg.font.Font(r'/home/pi/chalk_daily/chawp.ttf', 52)
        event_font = pg.font.Font(r'/home/pi/chalk_daily/chawp.ttf', 35)
        error_font = pg.font.Font(r'/home/pi/chalk_daily/chawp.ttf', 20)
    else:  ###############################
        date_font = pg.font.Font(r'.\chawp.ttf', 40)
        quote_font = pg.font.Font(r'.\chawp.ttf', 50)
        event_font = pg.font.Font(r'.\chawp.ttf', 34)
        # error_font = pg.font.Font(r'\chawp.ttf', 20)

    # set the pygame window name
    pg.display.set_caption('Chalk Daily')

    # create a surface object, image is drawn on it.
    if os.path.isfile('/home/pi/chalk_daily/green_chalkboard.jpg'):
        chalkboard = pg.image.load(r'/home/pi/chalk_daily/green_chalkboard.jpg')
    else:  #############################
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
        day_of_month = today.strftime("%d").lstrip("0")
        date_str_no_year = day_name + ", " + today.strftime("%B") + " " + day_of_month
        date_str = date_str_no_year + ", " + today.strftime("%Y")
        # print(date_str)

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
        internet = internet_connected()

        info_dict = what_data(date_str, ss_id)
        # print(info_dict)
        if internet and info_dict is not "failed":
            if info_dict:
                quote_max_chars = 24
                if info_dict['quote'] == '':
                    info_dict['quote'] = 'Quotes from people you respect! - Brennan'
                if len(info_dict['quote']) <= quote_max_chars:
                    quote_text = quote_font.render(info_dict['quote'], True, white)
                    quote_rect = quote_text.get_rect()
                    quote_rect.midleft = (w // 8, h // 2)
                    window.blit(quote_text, quote_rect)
                else:
                    quote_str = info_dict['quote']
                    quote_text = []
                    while len(quote_str) > quote_max_chars:
                        last_space = quote_str.rfind(' ', 0, quote_max_chars)
                        quote_text.append((quote_font.render(quote_str[:last_space], True, white)))
                        quote_str = quote_str[last_space:]
                    quote_text.append(quote_font.render(quote_str, True, white))
                    for line in range(len(quote_text)):
                        window.blit(quote_text[line], (w // 20, (h // 5) + line*quote_font.get_linesize()))

                ### EVENTS
                text_x = 4.8 * w // 8
                text_x_indented = text_x + .45 * w // 8
                text_height = 0.5 * h // 8
                event_font.set_underline(True)
                week_header_text = event_font.render(info_dict['week_header'], True, white)
                event_font.set_underline(False)
                window.blit(week_header_text, (text_x_indented, text_height))

                week_view_text = []
                for line in info_dict['week_events']:
                    week_view_text.append(event_font.render(line, True, white))

                for line in range(len(week_view_text)):
                    if info_dict['week_events'][line].startswith(str(chr(27))):
                        text_height += (event_font.get_linesize() + 12)
                    else:
                        text_height += (event_font.get_linesize() + 0.1/8)
                    window.blit(week_view_text[line], (text_x, text_height))

                event_font.set_underline(True)
                upcoming_header_text = event_font.render(info_dict['future_header'], True, white)
                event_font.set_underline(False)
                text_height += 0.5*h // 8
                window.blit(upcoming_header_text, (text_x_indented, text_height))

                upcoming_view_text = []
                for line in info_dict['important_events']:
                    upcoming_view_text.append(event_font.render(line, True, white))
                for line in range(len(upcoming_view_text)):
                    if line is 0:
                       text_height += (event_font.get_linesize() + 12)
                    else:
                        text_height += (event_font.get_linesize() + 0.1 / 8)
                    window.blit(upcoming_view_text[line], (text_x, text_height))
            else:
                quote_text = error_font.render("I couldn't find today in your sheet. Or maybe I don't have permission to look at it.", True, white)
                quote_rect = quote_text.get_rect()
                quote_rect.midleft = (w // 8, h // 2)
                window.blit(quote_text, quote_rect)
                quote_text = error_font.render("- Brennan", True, white)
                quote_rect = quote_text.get_rect()
                quote_rect.midleft = (w // 8, h // 2 + quote_font.get_linesize() + 1//8)
                window.blit(quote_text, quote_rect)
        else:
            quote_text = error_font.render("If I were connected to the internet,", True, white)
            quote_rect = quote_text.get_rect()
            quote_rect.midleft = (w // 8, h // 2)
            window.blit(quote_text, quote_rect)
            quote_text = error_font.render("there would be a cool quote here.", True, white)
            quote_rect = quote_text.get_rect()
            quote_rect.midleft = (w // 8, h // 2 + quote_font.get_linesize() + 1 // 8)
            window.blit(quote_text, quote_rect)
            if info_dict is "failed":
                quote_text = error_font.render("Connect to the internet, and restart the program.", True, white)
                quote_rect = quote_text.get_rect()
                quote_rect.midleft = (w // 8, h // 2 + (quote_font.get_linesize() + 1 // 8) * 2)
                window.blit(quote_text, quote_rect)

        pg.display.flip()
        if not done:
            #pg.time.wait(1000*60*5)  # ms
            pg.time.wait(10)
        print("########################")
        print("info dict: ", info_dict)
        print("internet: ", internet)
        print("date: ", date_str)
        print("sheet: ", ss_id)
        print("done? ", done)

    pg.display.quit()
    pg.quit()


def what_data(date_str, ss_id):
    # The ID and range of a sample spreadsheet.
    spreadsheet_id = ss_id
    sheet_range = 'A1:F'

    sheet_reader = SheetReader(spreadsheet_id, sheet_range)
    try:
        values = sheet_reader.download_data()
    except:
        # print("failed to download data")
        return "failed"

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
        # print("i",i)
        # print("todays index", todays_index)
        # print("values", values)
        # print("values[i][0]", values[i][0])
        # print("date_str", date_str)
        # print("date_str_no_year", date_str_no_year)
        if values[i][0] == date_str:
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

                ret_struct['week_events'].append(chr(27) + values[i+d][0][:3].upper() + ': ')
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
       #  print("here ")
        return 0

    ret_struct['important_events'] = []
    for row in values[todays_index+7:]:
        try:
            test = row[0][0]
        except IndexError:
            if row:
                row[0] = 'TBD,TBD'
            else:
                row = ['TBD, TBD']

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
