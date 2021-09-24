def read_txt(value):
    with open("DATA_CURENT_USER.txt", "r") as file:
        for line in file:
            line = line.replace("\n", '')
            title_line = line.split(' ')
            # print(title_line)
            try:
                if title_line[0] in value:
                    value[title_line[0]] = title_line[1]
                elif '----------------------------------------------' in title_line[0]:
                    print("входит")
                    break
            except IndexError:
                print("Error: Values in DATA_CURENT_USER.txt specified incorrectly")
                exit()

def main():
    # print('Parsing_txt started work')
    # print('Started reading data from DATA_CURENT_USER.txt')
    value = {'Email=': '', 'Password=': '', 'Test_run=': '', 'Path_to_file=': '', 'List_name=': '',
             'Path_to_chrome_driver=': '', 'Only_today=': ''}
    read_txt(value)
    # print(value)
    print('Parsing_txt finishes work successfully')
    return value

# main()