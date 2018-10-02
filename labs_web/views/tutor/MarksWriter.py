from abc import abstractmethod
import csv
import xml.etree.ElementTree as tree
import json


example_input_lst = [  # for testing purposes
    {'name': 'Alex Korienev',
     'marks': [8, 9, 6, 8, 'N\A', 'N\C']},
    {'name': 'John Doe',
     'marks': [10, 5, 'N\A', 'N\C', 8, 7]},
    {'name': 'Frederick Barbarossa',
     'marks': [10, 10, 10, 10, 10, 10]}
]


class MarksWriterFactoryMethod:
    @staticmethod
    def writer(out_format: str):
        if out_format == 'xml':
            return MarksWriterXML()
        if out_format == 'json':
            return MarksWriterJSON()
        if out_format == 'csv':
            return MarksWriterCSV()
        raise ValueError("given format doesn't match available variants. 'json', 'csv', 'xml' formats allowed")


class MarksWriter:
    @abstractmethod
    def write(self, marks_lst: list, outfile_path: str, *args, **kwargs):
        """
        saves marks table into selected format
        uses SQLAlchemy objects as
        :return:
        """
        pass


class MarksWriterXML(MarksWriter):
    """
    class to save marks in XML format
    format:
    <marksTable type="array">
        <marksRow>
            <name>Student_name</name>
                <marks type="array">
                    <mark>lab_1_mark</mark>
                    <mark>lab_2_mark</mark>
                    ...
                    <mark>lab_n_mark</mark>
                </marks>
        </marksRow>
    </marksTable>
    """
    def write(self, marks_lst: list, outfile_path: str, *args, **kwargs):
        marks_table = tree.Element('marksTable', {'type': 'array'})
        for row in marks_lst:
            marks_row = tree.SubElement(marks_table, 'marksRow')
            name = tree.SubElement(marks_row, 'name')
            name.text = row['name']
            marks = tree.SubElement(marks_row, 'marks', {'type': 'array'})
            for i in row['marks']:
                mark = tree.SubElement(marks, 'mark')
                mark.text = str(i)
        with open(outfile_path, 'w') as file:
            file.write(tree.tostring(marks_table, encoding='utf-8').decode())


class MarksWriterJSON(MarksWriter):
    """
    class to save marks in JSON format
    format:
    [{name: Student_name,
      marks: [lab_1_mark,
              lab_2_mark,
              ....
              lab_n_mark]
    }]
    """
    def write(self, marks_lst: list, outfile_path: str, *args, **kwargs):
        with open(outfile_path, 'w') as file:
            json.dump(marks_lst, file)


class MarksWriterCSV(MarksWriter):
    """
    class to save marks in CSV format
    format:
    Student_name,lab_1_mark,lab_2_mark ... ,lab_n_mark
    """
    def write(self, marks_lst: list, outfile_path: str, *args, **kwargs):
        with open(outfile_path, 'w') as file:
            w = csv.writer(file)
            w.writerow(['Name'] + ['lab_{}_mark'.format(i) for i in range(1, len(marks_lst[0]['marks']) + 1)])
            for row in marks_lst:
                tmp_lst = [row['name']] + row['marks']
                w.writerow(tmp_lst)

if __name__ == '__main__':  # for testing purposes
    writer = MarksWriterFactoryMethod.writer('csv')
    writer.write(marks_lst=example_input_lst,
                 outfile_path='tmp.csv')
    pass
