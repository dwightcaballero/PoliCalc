class get:

    def senators(self):

        sen_list = []
        with open('senators.txt', 'r') as senators:
            for sen in senators:
                sen = sen.split('\n')[0]
                sen_list.append(sen)
        return sen_list

    def concerns(self):

        con_list = []
        with open('final_concerns.txt', 'r') as concerns:
            for con in concerns:
                con = con.split('\n')[0]
                con_list.append(con)
        return con_list
