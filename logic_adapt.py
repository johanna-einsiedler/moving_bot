# -*- coding: utf-8 -*-
"""
Created on Sun May 24 10:56:03 2020

@author: hicom
"""


from chatterbot.logic import LogicAdapter


class MyLogicAdapter(LogicAdapter):
    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)
        
        import pandas as pd
        
        self.quest = 1
        self.mode = ''
        self.areas = ''
        self. uni = ''
        
    def can_process(self, statement):
        if self.quest != "x":
            return True
        else:
            return False
    
    def process(self, input_statement, additional_response_selection_parameters):
        from chatterbot.conversation import Statement
        import pandas as pd
        import os
        
        # get file path
        dirname = os.path.dirname(__file__)
        
        # get input statement and convert to all lower case
        input = input_statement.text.lower()
        
        uni_list = ['Goethe University Frankfurt',
                    'Frankfurt University of Music and Performing Arts',
                    'Provadis School of International Management & Technology Ltd',
                    'Hochschule fuer Bildende Kuenste - Staedelschule',
                    'Philosophisch-Theologische Hochschule Sankt Georgen',
                    'Frankfurt University of Applied Sciences',
                    'Frankfurt School of Finance & Management']
        
        error_message = Statement(text='Sorry, I did not understand. Can you maybe try writing it differently?')
        selected_statement = error_message

        #if(self.quest ==0):
           # selected_statement = Statement(text='Hi! Happy to hear that you are planning to move to Frankfurt! What university will you be attending?')

        # check university
        if (self.quest == 1):
            if any(x in input for x in ['goethe','göthe','Goethe','Göthe']):
                self.uni = uni_list[0]
                selected_statement = Statement(text = 'Thanks, that information will make it easier for me to find the perfect area for you! How do you plan to commute to uni? By car, bike or walking?')
            if any(x in input for x in ['music','musik','performing','arts','darstellend']):
                   self.uni = uni_list[1]
                   selected_statement = Statement(text = 'Thanks, that information will make it easier for me to find the perfect area for you! How do you plan to commute to uni? By car, bike or walking?')
            if any(x in input for x in ['provadis','international','technology','ltd']):
                   self.uni = uni_list[2] 
                   selected_statement = Statement(text = 'Thanks, that information will make it easier for me to find the perfect area for you! How do you plan to commute to uni? By car, bike or walking?')
            if any(x in input for x in ['bildende','staedel', "städel"]):
                   self.uni = uni_list[3]
                   selected_statement = Statement(text = 'Thanks, that information will make it easier for me to find the perfect area for you! How do you plan to commute to uni? By car, bike or walking?')
            if any(x in input for x in ['philosophisch','theologisch','philosophy','theology','sankt','georgen']):
                    self.uni = uni_list[4]
                    selected_statement = Statement(text = 'Thanks, that information will make it easier for me to find the perfect area for you! How do you plan to commute to uni? By car, bike or walking?')
            if any(x in input for x in ['applied','fachhochschule','angewandt']):
                    self.uni = uni_list[5]
                    selected_statement = Statement(text = 'Thanks, that information will make it easier for me to find the perfect area for you! How do you plan to commute to uni? By car, bike or walking?')
            if any(x in input for x in ['finance','finanz']):
                    self.uni = uni_list[6]
                    selected_statement = Statement(text = 'Thanks, that information will make it easier for me to find the perfect area for you! How do you plan to commute to uni? By car, bike or walking?')
  
        # check for commuting type    
        if (self.quest == 2):
            if any(x in input for x in ['car','auto','drive','driving']):
                self.mode = 'car'
                selected_statement = Statement(text='Alright. Got it. So you are going to '+ self.uni + ' and plan to commute by ' +self.mode+ '.  How long would you maximum be willing to commute?')
            if any(x in input for x in ['bike','rad','cycle']):
                self.mode = 'bike'
                selected_statement = Statement(text='Alright. Got it. So you are going to '+ self.uni + ' and plan to commute by ' +self.mode+ '.  How long would you maximum be willing to commute?')
            if any(x in input for x in ['walk','gehen','laufen','feet','foot']):
                self.mode = 'foot'
                selected_statement = Statement(text='Alright. Got it. So you are going to '+ self.uni + ' and plan to commute by ' +self.mode+ '.  How long would you maximum be willing to commute?')
           
        
        # check for commuting distance
        if(self.quest == 3 and any(char.isdigit() for char in input)):
            
            number = [int(s) for s in input if s.isdigit()]
            new_num= str()
            for i in range(0,len(number)):
                new_num = int(str(new_num) + str(number[i]))
            
            # get path to file with commuting distances
            commute_path = os.path.join(dirname, 'botdata/'+ self.mode +'.csv')
            commuting_times = pd.read_csv(commute_path, header =0, index_col=0)
            commuting_times = commuting_times[self.uni]
            mask = commuting_times<int(new_num) + 5
            names = commuting_times[mask].index
            self.areas = commuting_times[mask]
            
            if len(names)==0:
                return_string = 'Unfortunatley, there are no districts which are that close. Try a higher number!'
                self.quest = self.quest -1 
            else:
                return_string = 'The districts that are within this commuting distance: '
                for j in names:
                    return_string = return_string + j + ', '
            
                return_string = return_string[:-2] + '.'
                return_string = return_string +' What is more important to you: having a lake or river in your area or many green spaces?'
            selected_statement = Statement(text = return_string)
             
            
    
        # check preferences for water & green
        if(self.quest ==4):
            stats_path = os.path.join(dirname, 'botdata/'+ 'stats.csv')
            stats = pd.read_csv(stats_path, header =0, index_col=0, encoding = 'latin')
            areas = pd.concat([self.areas, stats],axis=1)
            if any(x in input for x in ['water','lake','river','see','wasser','fluss']):                
                com_sorted = areas.sort_values(['water'], ascending = 'False', axis = 0, na_position ='first')
                return_string = 'The districts within your desired commuting distance, that have the most water area: '
            
            if any(x in input for x in ['green','parc','park','grün']):
                com_sorted = areas.sort_values(['green'], ascending = 'False', axis = 0, na_position ='first')
                return_string = 'The districts within your desired commuting distance, that have the most green area: '
            
            maxs = com_sorted[len(com_sorted)-5:len(com_sorted)]
            for j in range(0,len(maxs)):
                return_string = return_string + maxs.index[j] + ', '
            return_string = return_string[:-2] + '.'
            return_string = return_string + ' I hope this information was helpful to you  - see you soon :)'
            selected_statement = Statement(text = return_string)
                
        self.quest = self.quest + 1
        
        if (selected_statement == error_message):
           self.quest = self.quest -1
           
        if self.quest == 5:
            self.quest = 1
           #selected_statement = Statement(text = str(self.quest))
        #if(self.last_ticket_referenced == 'car') and (int(input_statement)<1000):
         #  selected_statement = Statement(text = 'sucess')
        
        #self.last_ticket_referenced = 'uni'
        
        return (selected_statement)
    
