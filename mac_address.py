import random
LIMIT = 12 ; REMAINING_BITS = LIMIT - 4 ; MAX_ADDRESS  = 3
char = ['A','B','C','D','E','F','G',0,1,2,3,4,5,6,7,8,9] ; _dict = {}

class Domain(object):
    def __init__(self, _id, name, mac_address):
        #TODO: type check _id type
        '''
        @param _id: undefined
        @param name: string
        @param mac_address: empty list
        '''
        if not isinstance(mac_address, list) or mac_address:
            raise Exception('mac_address incorrect format')
        if not isinstance(name, str):
            raise Exception('name is not string')

        self._id = _id
        self.name = name
        self.mac_addresses = mac_address

class MAC_Generator(Domain):
    def __init__(self, d_list):
        '''
        @param d_list: requires a list of Domain instances
        '''
        if not isinstance(d_list, list):
            raise Exception('MAC_Generator takes a list')

        self.d_list = d_list
        self.address_generator()

    # mac_address() returns a correctly formatted 12 character mac address 
    def mac_address(self, group):
        def give_me_colons(mac):
            s=''
            for i in range(0,LIMIT,2):
                s += mac[i:i+2] + ':'
            return s[:-1]

        # mac <- 4 characters based on Domain._id
        mac = self.d_list[group]._id

        # generate an unpadded 12 character string using the char array
        for i in range(0,REMAINING_BITS):
            # random number from 0 to (len(char)-1) -> endpoints included
            index = random.randint(0,len(char)-1)
            mac += str(char[index])

        return give_me_colons(mac)

    # generator() appends 10 mac addresses to each of the 3 domains
    def address_generator(self):
        for i in range(0,len(self.d_list)):
            for j in range(0, MAX_ADDRESS):
                self.d_list[i].mac_addresses.append(self.mac_address(i))

            print('Identifier: ' + str(self.d_list[i]._id) + ' -> ' + str(self.d_list[i].mac_addresses))

if __name__ == '__main__':

    # MAC_Generator takes one argument ; a list of unique Domain objects
    
    MAC_Generator( [    Domain('F52D','Kam',[]),
                        Domain('8GDF','Sam',[]),
                        Domain('3HG2','Yam',[]),
                        Domain('8K7G','Bam',[]),
                        Domain('KG3H','Qam',[]),
                        Domain('0GJ4','Tam',[])     ] )


