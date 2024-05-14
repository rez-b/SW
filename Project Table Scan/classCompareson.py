class Compareson:
    """сравнивает данные """
    def __init__(self, data_1, data_2,string_count, column_count):
        self.data_1 = data_1
        self.data_2 = data_2
        self.column_count = column_count
        self.string_count = string_count

    def get_matrix_data_sheet(self, out_data):
        """из листа с данными формирует матрицу (вложенный лист)"""
        self.out_data = out_data
        matrix = []
        row = []
        for i in range(self.string_count):
            for j in range(self.column_count):
                row.append(out_data[self.column_count * i + j])
            matrix.append(row)
            row = []
        return matrix
    
    def compare(self):
        """сравнивает матрицы и выдает номера неправильных ответов"""
        data_1 = self.get_matrix_data_sheet(self.data_1)
        data_2 = self.get_matrix_data_sheet(self.data_2)
        result = []
        wrong_answers = []
        for i in range(0, len(data_1)):
            for j in range(0, len(data_1[1])):
                if data_1[i][j] != data_2[i][j]:
                    result.append([j + 1, i + 1])
                    if (j + 1) not in wrong_answers:
                        wrong_answers.append(j + 1)
        str_wrong_answers = [str(n) for n in sorted(wrong_answers)]
        return str_wrong_answers
        
    def correct_answers_percentage(self):
        """вычисляет процент правильных ответов"""
        correct_answers_percent = round(
            (self.column_count- len(self.compare())) * 100 / (self.column_count))
        return correct_answers_percent
