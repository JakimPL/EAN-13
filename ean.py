import matplotlib.pyplot as plot
import matplotlib.patches as patches


class EAN:
    encoding_raw_table = [
        '000000222222', '001011222222', '001101222222', '001110222222', '010011222222',
        '011001222222', '011100222222', '010101222222', '010110222222', '011010222222']
    ean_raw_tables = [
        ['0001101', '0011001', '0010011', '0111101', '0100011', '0110001', '0101111', '0111011', '0110111', '0001011'],
        ['0100111', '0110011', '0011011', '0100001', '0011101', '0111001', '0000101', '0010001', '0001001', '0010111'],
        ['1110010', '1100110', '1101100', '1000010', '1011100', '1001110', '1010000', '1000100', '1001000', '1110100']]

    encoding_table = [
        [0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2], [0, 0, 1, 0, 1, 1, 2, 2, 2, 2, 2, 2],
        [0, 0, 1, 1, 0, 1, 2, 2, 2, 2, 2, 2], [0, 0, 1, 1, 1, 0, 2, 2, 2, 2, 2, 2],
        [0, 1, 0, 0, 1, 1, 2, 2, 2, 2, 2, 2], [0, 1, 1, 0, 0, 1, 2, 2, 2, 2, 2, 2],
        [0, 1, 1, 1, 0, 0, 2, 2, 2, 2, 2, 2], [0, 1, 0, 1, 0, 1, 2, 2, 2, 2, 2, 2],
        [0, 1, 0, 1, 1, 0, 2, 2, 2, 2, 2, 2], [0, 1, 1, 0, 1, 0, 2, 2, 2, 2, 2, 2]]

    ean_tables: list[list[list[int]]] = [
        [[0, 0, 0, 1, 1, 0, 1], [0, 0, 1, 1, 0, 0, 1], [0, 0, 1, 0, 0, 1, 1],
         [0, 1, 1, 1, 1, 0, 1], [0, 1, 0, 0, 0, 1, 1], [0, 1, 1, 0, 0, 0, 1],
         [0, 1, 0, 1, 1, 1, 1], [0, 1, 1, 1, 0, 1, 1], [0, 1, 1, 0, 1, 1, 1], [0, 0, 0, 1, 0, 1, 1]],
        [[0, 1, 0, 0, 1, 1, 1], [0, 1, 1, 0, 0, 1, 1], [0, 0, 1, 1, 0, 1, 1],
         [0, 1, 0, 0, 0, 0, 1], [0, 0, 1, 1, 1, 0, 1], [0, 1, 1, 1, 0, 0, 1],
         [0, 0, 0, 0, 1, 0, 1], [0, 0, 1, 0, 0, 0, 1], [0, 0, 0, 1, 0, 0, 1], [0, 0, 1, 0, 1, 1, 1]],
        [[1, 1, 1, 0, 0, 1, 0], [1, 1, 0, 0, 1, 1, 0], [1, 1, 0, 1, 1, 0, 0],
         [1, 0, 0, 0, 0, 1, 0], [1, 0, 1, 1, 1, 0, 0], [1, 0, 0, 1, 1, 1, 0],
         [1, 0, 1, 0, 0, 0, 0], [1, 0, 0, 0, 1, 0, 0], [1, 0, 0, 1, 0, 0, 0], [1, 1, 1, 0, 1, 0, 0]]]

    number: int
    number_digits: list[int]
    binary_sequence: list[int]
    checksum: int

    def __init__(self, number):
        if isinstance(number, str):
            self.number_digits = self.get_number_digits(number)
        else:
            raise TypeError("a string expected")

        if len(self.number_digits) == 12:
            self.checksum = self.calculate_checksum()
            self.number_digits += [self.checksum]

        self.number = int(''.join(map(str, self.number_digits)))
        if not self.check_number():
            raise ValueError("a number has to be either a 12-digit code or a valid 13-digit code")

        self.generate_binary_sequence()

    def calculate_checksum(self):
        return (10 - (sum(self.number_digits[:13:2]) + 3 * sum(self.number_digits[1:13:2]))) % 10

    def check_number(self):
        if self.number < 0:
            return False

        n = len(self.number_digits)
        if n != 13:
            return False

        return self.calculate_checksum() == 0

    def generate_binary_sequence(self):
        encoder = EAN.encoding_table[self.number_digits[0]]

        binary_chain = []
        for i in range(13):
            binary_chain += EAN.ean_tables[encoder[i - 1]][self.number_digits[i]]

        suffix = [1, 0, 1]
        first_part = binary_chain[:7]
        second_part = binary_chain[7:]
        center = [0, 1, 0, 1, 0]

        self.binary_sequence = suffix + first_part + center + second_part + suffix

    def draw_barcode(self):
        n = len(self.binary_sequence)
        plot.figure()
        current_axis = plot.gca()
        for i in range(n):
            if self.binary_sequence[i] > 0:
                rectangle = patches.Rectangle((i, 0), 1, 1, color="black")
                current_axis.add_patch(rectangle)

        plot.xlim([0, n])
        plot.axis('off')
        plot.show()

    @staticmethod
    def convert_from_raw_data(data):
        return [list(map(int, list(data[i]))) for i in range(len(data))]

    @staticmethod
    def get_number_digits(number):
        return [int(digit) for digit in str(number)]
