import string
string.ascii_uppercase
import copy
copy.deepcopy

class PlugLead():
    def __init__(self, plugs):
        self.encoded_letters = {}
        # disallow wrong entries
        if(type(plugs) == str and len(plugs) == 2 and plugs[0] != plugs[1] and plugs[0].isalpha() and plugs[1].isalpha()):
            plugs = plugs.upper()
            self.first_letter = plugs[0]
            self.second_letter = plugs[1]
            
            self.encoded_letters[self.first_letter] = self.second_letter
            self.encoded_letters[self.second_letter] = self.first_letter
            
        else:
            raise Exception("Wrong entry")
        
    def encode(self , plug):
        if(type(plug) == str and len(plug) == 1 and plug.isalpha() == True):
            plug = plug.upper()
        
            if(plug in self.encoded_letters.keys()):
                return self.encoded_letters[plug]
            else:
                return plug
        else:
            raise Exception("Wrong entry to encode")
            
#Aggregates the leads
class Plugboard():

    #should be able to encode using the (PlugLead's encoding)
    #Note: limit number of leads pluged to 10
    def __init__(self):
        #create an initial dictionary for encoding
        self._encoding_dictionary_ = self._init_encoding_dictionary_()
        self._plugged_leads_ = []
        self._plugged_letters_ = []
        self._current_leads_ = 0
        self._lead_limitation_ = 10
    
    
    def add(self, PlugLead):
        #check if added lead doesn't exceed max number of leads physically possible
        if(self._current_leads_ >= self._lead_limitation_): 
            raise Exception(f"Max number of leads  {self._lead_limitation_} exceeded, can't add more leads")
        
        first_plugged_letter = PlugLead.first_letter
        second_plugged_letter = PlugLead.encode(first_plugged_letter)
        
        #check if leads are not already plugged in
        if(first_plugged_letter not in self._plugged_letters_ and second_plugged_letter not in self._plugged_letters_):
            self._plugged_leads_.append(PlugLead)
            self._plugged_letters_.append(first_plugged_letter) 
            self._plugged_letters_.append(second_plugged_letter) 
            
            self._encoding_dictionary_[first_plugged_letter] = second_plugged_letter
            self._encoding_dictionary_[second_plugged_letter] = first_plugged_letter 
        else:
            raise Exception(f"Letters {first_plugged_letter} or {second_plugged_letter} already plugged in, unplug them first")
        
        self._current_leads_ += 1
        return self._encoding_dictionary_
    
    
    def encode(self, char):
        #should return the result of passing the character through the entire plugboard.
        for i,plug in enumerate(self._plugged_leads_):
            encoded_char = plug.encode(char)
            if(encoded_char != char):
                return encoded_char
        return encoded_char
            
        
    @staticmethod
    def _init_encoding_dictionary_():
        encoding_dictionary = {}
        for char in range(ord('A'), ord('Z')+1):
            alphabet_character = chr(char)
            encoding_dictionary[alphabet_character] = alphabet_character
        
        return encoding_dictionary
    
    


class Rotor:
    sorted_alphabet = list(string.ascii_uppercase)
    rotors_dict= {
        "Beta" : [["L","E","Y","J","V","C","N","I","X","W","P","B","Q","M","D","R","T","A","K","Z","G","F","U","H","O","S"], copy.deepcopy(sorted_alphabet)], 
        "Gamma" : [ ["F","S","O","K","A","N","U","E","R","H","M","B","T","I","Y","C","W","L","Q","P","Z","X","V","G","J","D"], copy.deepcopy(sorted_alphabet)],
        "I" : [ ["E","K","M","F","L","G","D","Q","V","Z","N","T","O","W","Y","H","X","U","S","P","A","I","B","R","C","J"], copy.deepcopy(sorted_alphabet)],
        "II" : [ ["A","J","D","K","S","I","R","U","X","B","L","H","W","T","M","C","Q","G","Z","N","P","Y","F","V","O","E"], copy.deepcopy(sorted_alphabet)],
        "III" : [ ["B","D","F","H","J","L","C","P","R","T","X","V","Z","N","Y","E","I","W","G","A","K","M","U","S","Q","O"], copy.deepcopy(sorted_alphabet)],
        "IV" : [ ["E","S","O","V","P","Z","J","A","Y","Q","U","I","R","H","X","L","N","F","T","G","K","D","C","M","W","B"], copy.deepcopy(sorted_alphabet)],
        "V" : [ ["V","Z","B","R","G","I","T","Y","U","P","S","D","N","H","L","X","A","W","M","J","Q","O","F","E","C","K"], copy.deepcopy(sorted_alphabet)],
        "A" :  [["E","J","M","Z","A","L","Y","X","V","B","W","F","C","R","Q","U","O","N","T","S","P","I","K","H","G","D"], copy.deepcopy(sorted_alphabet)],
        "B" :  [["Y","R","U","H","Q","S","L","D","P","X","N","G","O","K","M","I","E","B","F","Z","C","W","V","J","A","T"], copy.deepcopy(sorted_alphabet)],
        "C" :  [["F","V","P","J","I","A","O","Y","E","D","R","Z","X","W","G","C","T","K","U","Q","S","B","N","M","H","L"], copy.deepcopy(sorted_alphabet)]
    }
        
    notch_mapping = {
        "I"   : "Q",
        "II"  : "E",
        "III" : "V",
        "IV"  : "J",
        "V"   : "Z",
        "Beta" : False,
        "Gamma" : False  
        
    }
    

    def __init__(self, rotor_name):
        if rotor_name in Rotor.rotors_dict:
            self.rotor_name = rotor_name
            self.rotor_2d_list = copy.deepcopy(Rotor.rotors_dict[rotor_name])
        else:
            raise ValueError(f"{rotor_name} is not a valid rotor")
        
class Moving_Rotor(Rotor):
    
    def __init__ (self, rotor_name, starting_position='A',ring_setting=1):
        super().__init__(rotor_name)
        if starting_position.isupper() == False:
            raise ValueError('starting_position only accepts uppercase letters')
        else:
            self.current_position = starting_position
        if type(ring_setting) != int:
            raise TypeError('This enigma only takes numerical ring settings, please enter an int')
        
        if ring_setting < 1 or ring_setting > 26:
            raise ValueError(f'{ring_setting} is out of range, please choose a number between 1 and 26')
        else:
            self.ring_setting = ring_setting
            self.rotate_to_first_position(starting_position, ring_setting)
            self.notch = Rotor.notch_mapping[rotor_name]

    def rotate_to_first_position(self,starting_position, ring_setting):
        number_starting_position = string.ascii_uppercase.index(starting_position)+1        
        ring_setting_effect = ring_setting
        rotate_by= number_starting_position - ring_setting_effect
        if rotate_by < 0:
            rotate_by +=26

        self.rotate(rotate_by)        

    def rotate(self, number_of_rotations = 1):#this could be used as well for other rotations
        self.rotor_2d_list[0]= self.rotor_2d_list[0][number_of_rotations:] + self.rotor_2d_list[0][:number_of_rotations]
        self.rotor_2d_list[1]=self.rotor_2d_list[1][number_of_rotations:] + self.rotor_2d_list[1][:number_of_rotations]

        if number_of_rotations == 1:
            rotation_offset = string.ascii_uppercase.index(self.current_position) + number_of_rotations
            if rotation_offset >= 26:
                rotation_offset -= 26
        
            self.current_position = string.ascii_uppercase[rotation_offset]

    
    def encode_right_to_left(self,letter):
        letter_ascii_position = string.ascii_uppercase.index(letter)
        contact_letter = self.rotor_2d_list[0][letter_ascii_position]
        pin_position = self.rotor_2d_list[1].index(contact_letter)
        letter_to_return = string.ascii_uppercase[pin_position]
        return letter_to_return
    
    def encode_left_to_right(self,letter):
        letter_ascii_position = string.ascii_uppercase.index(letter)
        pin_letter = self.rotor_2d_list[1][letter_ascii_position]
        contact_position = self.rotor_2d_list[0].index(pin_letter)
        letter_to_return = string.ascii_uppercase[contact_position]
        return letter_to_return
    
class Reflector(Rotor):
    def __init__ (self,reflector_name):
        if reflector_name == 'A' or reflector_name == 'B' or reflector_name == 'C':
            super().__init__(reflector_name)
        else: 
            raise ValueError(f'{reflector_name} is not a reflector')
    
    def reflect(self,letter):
        reflector_pin_index = self.rotor_2d_list[1].index(letter)
        reflector_contact_letter=self.rotor_2d_list[0][reflector_pin_index]
        return reflector_contact_letter
    

              
class Rotor_Box:
    def __init__(self,array_of_rotors,array_of_starting_positions,array_of_ring_setting,reflector_name):
        if len(array_of_rotors) > 4 or len(array_of_rotors) <3:
            raise ValueError('This version of the enigma accepts a maximum of 4 rotors and a minimum of 3 rotors')

            
        else:    
            self.array_of_rotors = array_of_rotors
            self.array_of_starting_positions=array_of_starting_positions 
            self.array_of_ring_setting= array_of_ring_setting
            self.reflector = Reflector(reflector_name)
            self.rotor_list = []
            added_rotors = []
            for i, rotor_name in enumerate(array_of_rotors):
                if rotor_name in added_rotors:
                    raise ValueError("Can't add duplicate rotors of the same type")
                else:
                    current_rotor = Moving_Rotor(rotor_name,array_of_starting_positions[i],array_of_ring_setting[i])
                    self.rotor_list.append(current_rotor)
                    added_rotors.append(rotor_name)

    @staticmethod
    def rotate_on_notch(rotor_list):
        alphabet = string.ascii_uppercase
        rightmost_rotor_prev_position = alphabet.index(rotor_list[0].current_position) -1
        if(rightmost_rotor_prev_position < 1):
            rightmost_rotor_prev_position += 26
            
        if rotor_list[1].current_position == rotor_list[1].notch:
            rotor_list[1].rotate()
            rotor_list[2].rotate()
        elif rotor_list[0].notch != False and rightmost_rotor_prev_position == alphabet.index(rotor_list[0].notch) :
            rotor_list[1].rotate()
       
    
    def encode_and_reflect(self,letter): 
        self.rotor_list.reverse()
        #Rotate rightmost rotor
        self.rotor_list[0].rotate()
        self.rotate_on_notch(self.rotor_list)
    
        #encode_right_to_left
        number_of_rotors = len(self.rotor_list)
        
        #Dealing with the rotors from left to right
        letter_to_encode = letter
        for i, rotor in enumerate(self.rotor_list):
            current_encoding_rotor = rotor
            letter_to_encode = current_encoding_rotor.encode_right_to_left(letter_to_encode)        
           
        #reflect   
        letter_to_encode = self.reflector.reflect(letter_to_encode)
        
        #encode_left_to_right
        self.rotor_list.reverse()

        for i, rotor in enumerate(self.rotor_list):
            current_encoding_rotor = rotor
            letter_to_encode= current_encoding_rotor.encode_left_to_right(letter_to_encode)
        return letter_to_encode

    
    
class Enigma: 
    def __init__ (self, array_plug_leads, array_of_rotors, array_of_starting_positions, array_of_ring_settings, reflector):
        self.plugboard = Plugboard()
        for plug_lead_name in array_plug_leads:
            pluglead = PlugLead(plug_lead_name)
            self.plugboard.add(pluglead)
            
        self.rotor_box = Rotor_Box(array_of_rotors,array_of_starting_positions,array_of_ring_settings,reflector)

        
    def encrypt_decrypt(self, message):
        #handle small letters
        message_upper = message.upper()
        output = ''
        for letter in message_upper:
            plugboard_encryption_1=self.plugboard.encode(letter)
            rotor_box_encryption = self.rotor_box.encode_and_reflect(plugboard_encryption_1)
            output+= self.plugboard.encode(rotor_box_encryption)
            
        return output