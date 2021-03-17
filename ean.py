import matplotlib.pyplot as plot
import matplotlib.patches as patches


class EAN:
    encoding_raw_table: list[str] = [
        '000000222222', '001011222222', '001101222222', '001110222222', '010011222222',
        '011001222222', '011100222222', '010101222222', '010110222222', '011010222222']
    ean_raw_tables: list[str] = [
        ['0001101', '0011001', '0010011', '0111101', '0100011', '0110001', '0101111', '0111011', '0110111', '0001011'],
        ['0100111', '0110011', '0011011', '0100001', '0011101', '0111001', '0000101', '0010001', '0001001', '0010111'],
        ['1110010', '1100110', '1101100', '1000010', '1011100', '1001110', '1010000', '1000100', '1001000', '1110100']]

    encoding_table: list[list[int]] = [
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

    __number: int
    __number_string: str
    __number_digits: list[int]
    __encoder: list[int]
    __binary_sequence: list[int]
    __checksum: int

    def __init__(self, code):
        self.__call__(code)

    def __call__(self, code):
        if isinstance(code, str):
            self.__number_digits = self.get_number_digits(code)
        else:
            raise TypeError("a string expected")

        if len(self.__number_digits) == 12:
            self.__checksum = self.calculate_checksum()
            self.__number_digits += [self.__checksum]

        self.__number_string = "".join(list(map(str, self.__number_digits)))
        self.__number = int(self.__number_string)
        if not self.check_number():
            raise ValueError("a number has to be either a 12-digit code or a valid 13-digit code")

        self.generate_binary_sequence()

    def calculate_checksum(self) -> int:
        return (10 - (sum(self.__number_digits[:13:2]) + 3 * sum(self.__number_digits[1:13:2]))) % 10

    def check_number(self) -> bool:
        if self.__number < 0:
            return False

        n = len(self.__number_digits)
        if n != 13:
            return False

        return self.calculate_checksum() == 0

    def generate_binary_sequence(self):
        self.__encoder = EAN.encoding_table[self.__number_digits[0]]

        binary_chain = []
        for i in range(1, 13):
            binary_chain += EAN.ean_tables[self.__encoder[i - 1]][self.__number_digits[i]]

        suffix = [1, 0, 1]
        first_part = binary_chain[:7]
        second_part = binary_chain[7:]
        center = [0, 1, 0, 1, 0]

        self.__binary_sequence = suffix + first_part + center + second_part + suffix

    def draw_barcode(self):
        n = len(self.__binary_sequence)
        plot.figure()
        current_axis = plot.gca()
        for i in range(n):
            if self.__binary_sequence[i] > 0:
                rectangle = patches.Rectangle((i, 0), 1, 1, color="black")
                current_axis.add_patch(rectangle)

        plot.xlim([0, n])
        plot.axis('off')
        plot.text(n / 2, -0.12, self.__number_string, ha='center', va='center', fontsize=30)
        plot.show()

    @staticmethod
    def convert_from_raw_data(data) -> list[list[int]]:
        return [list(map(int, list(data[i]))) for i in range(len(data))]

    @staticmethod
    def get_number_digits(number) -> list[int]:
        return [int(digit) for digit in str(number)]
