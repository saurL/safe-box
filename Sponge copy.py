from SHA import SHA256
class Sponge:
    def __init__(self, bitrate, capacity, rounds):
        self.bitrate = bitrate
        self.capacity = capacity
        self.bytesrate = bitrate//8
        self.capacity_bytes = capacity//8
        self.rounds = rounds
        self.reset()
    def reset(self):
        self.state = bytearray(self.bytesrate + self.capacity_bytes)  


    def absorb(self, input_data):
        if isinstance(input_data, str):
            input_bytes = bytearray(input_data, 'utf-8')
        elif isinstance(input_data, (bytes, bytearray)):
            input_bytes = bytearray(input_data)
        else:
            raise TypeError("Input data must be of type str, bytes, or bytearray")

        while input_bytes:
            block = input_bytes[:self.bytesrate]
            input_bytes = input_bytes[self.bytesrate:]

            for i in range(len(block)):
              self.state[i] ^= block[i]
            
            self._permutation()

    def squeeze(self, output_length):
        output_length=output_length//8
        output = bytearray()
        while len(output) < output_length:
            output.extend(self.state[:self.bytesrate])
            self._permutation()
        return bytes(output[:output_length])

    def _permutation(self):
        temp_state = self.state[:]
        for r in range(self.rounds):
            for i in range(len(self.state)-4):
                if temp_state[i:i+4]==b'\x00\x00\x00\x00':
                    continue
                combined = int.from_bytes(temp_state[i:i+4], 'big')
                rotated = self._right_rotate(combined,(i+1)%32, size=32)
                self.state[i:i+4] = rotated.to_bytes(4, 'big')

        

    
    def _right_rotate(self ,value, shift, size=8):
       return ((value >> shift) | (value << (size - shift))& ((1 << size) - 1))
    """ & ((1 << size) - 1)"""
