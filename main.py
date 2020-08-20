# https://developers.google.com/sheets/api/quickstart/python
# might have to enable the api and get credentials and install package^

# make desktop icon: https://www.hackster.io/kamal-khan/desktop-shortcut-for-python-script-on-raspberry-pi-fd1c63


from sheet_reader import SheetReader
from datetime import date
import calendar
import pygame as pg


def main():
    display()


def display():
    pg.init()
    window = pg.display.set_mode((0, 0), pg.FULLSCREEN)

    # create a font object.
    # 1st parameter is the font file
    # which is present in pygame.
    # 2nd parameter is size of the font
    date_font = pg.font.Font(r'/home/pi/chalk_daily/chawp.ttf', 32)
    quote_font = pg.font.Font(r'/home/pi/chalk_daily/chawp.ttf', 50)
    event_font = pg.font.Font(r'/home/pi/chalk_daily/chawp.ttf', 28)


    # set the pygame window name
    pg.display.set_caption('Chalk Daily')

    # create a surface object, image is drawn on it.
    chalkboard = pg.image.load(r'/home/pi/chalk_daily/green_chalkboard.jpg')

    # copying the image surface object
    # to the display surface object at
    # (0, 0) coordinate.
    window.blit(chalkboard, (0, 0))

    white = (255, 255, 255)

    done = False
    while not done:
        today = date.today()
        day_name = calendar.day_name[today.weekday()]
        date_str = day_name + ", " + today.strftime("%B %d, %Y")

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

        info_dict = what_data(date_str)
        if info_dict['quote'] == '':
            info_dict['quote'] = 'Add quotes from people you respect! - Brennan'
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
        week_header_text = event_font.render("WEEK VIEW", True, white)
        event_font.set_underline(False)
        window.blit(week_header_text, (4.95 * w // 8, (1 * h // 8)))

        week_view_text = []
        for line in info_dict['week_events']:
            week_view_text.append(event_font.render(line, True, white))
        for line in range(len(week_view_text)):
            window.blit(week_view_text[line], (4.5 * w // 8, (1.1 * h // 8) + (line+1)*event_font.get_linesize()))
            bottom_of_week_events = (1.1 * h // 8) + (line+1)*event_font.get_linesize()

        event_font.set_underline(True)
        upcoming_header_text = event_font.render("COMING UP", True, white)
        event_font.set_underline(False)
        window.blit(upcoming_header_text, (4.95 * w // 8, (bottom_of_week_events + h // 8)))

        upcoming_view_text = []
        for line in info_dict['important_events']:
            upcoming_view_text.append(event_font.render(line, True, white))
        for line in range(len(upcoming_view_text)):
            window.blit(upcoming_view_text[line], (4.5 * w // 8, (bottom_of_week_events + (1.1*h // 8) + (line+1)*event_font.get_linesize())))

        pg.display.flip()

        pg.time.wait(100)  # ms

    pg.display.quit()
    pg.quit()


def what_data(date_str):
    # The ID and range of a sample spreadsheet.
    spreadsheet_id = '1aXGSYveChtyNhKcAhia9CTPUJ4Nsqq0jbhbMe6hEJqA'
    sheet_range = 'the input calendar!A3:F'

    sheet_reader = SheetReader(spreadsheet_id, sheet_range)
    values = sheet_reader.download_data()
    if not values:
        print('No data found.')

    ret_struct = {'date': date_str}
    ret_struct['week_events'] = []

    todays_index = None
    for i in range(len(values)):
        try:
            test = values[i][0][0]
        except IndexError:
            values[i][0] = 'TBD,TBD'

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


if __name__ == '__main__':
    main()
