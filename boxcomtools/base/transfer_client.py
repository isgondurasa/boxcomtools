#  transfer-client
import asyncio
from collections import defaultdict

from boxcomtools.smartsheet.sheet import Sheet


class TransferClient:
    """
    Transfer data endpoint
    assume that both source and destination
    as access and refresh tokens already
    """

    def __init__(self, source, destination):
        self._source = source
        self._destination = destination


class BoxToSmartsheet(TransferClient):

    def line(self, file_info):
        return {
            'name': file_info['name'],
            'path': [p['name'] for p in file_info['path_collection']['entries']],
            'created_at': file_info['created_at'],
            'modified_at': file_info['modified_at'],
        }

    def line_metafields(self, meta_file_info):
        for meta_file_line_info in meta_file_info:
            yield (
                meta_file_line_info['$template'],
                {k: v for k, v in meta_file_line_info.items() if not k.startswith("$")}
            )

    async def __parse_metadata(self, metadata):
        res = defaultdict(list)
        for file_info, meta_file_info in metadata:
            data = dict(self.line(file_info))
            for name, fields in self.line_metafields(meta_file_info):
                data['metafields'] = fields
                res[name].append(data)
        return res

    def sheet_template(self, name):
        return {
            'name': name,
            'columns': [
                {'title': 'Path', 'type': "TEXT_NUMBER"},
                {'title': 'Name', 'type': "TEXT_NUMBER", 'primary': True},
                {'title': 'Created At', 'type': 'DATE'}
            ]
        }

    def metafield_col_template(self, title, value_type=None):
        return {
            'title': title, 'type': 'TEXT_NUMBER'
        }

    def row_template(self):
        return {
            'toTop': True,
            'cells': []
        }
    
    async def transfer(self):
        """
        Gets all metadata from file, enterprise metadata templates
        and creates a list of sheets. One versus each template
        """
        # gather metadata
        folder = self._source.folder()
        all_metadata = []
        for _file in await folder.files:
            file_info = (_file.get(), _file.get_metadata())
            all_metadata.append(asyncio.gather(*file_info))
        all_metadata = await asyncio.gather(*all_metadata)

        # parse_metadata
        parsed_metadata = await self.__parse_metadata(all_metadata)

        # create sheets
        sheets = []
        for template_name, values in parsed_metadata.items():
            sheet = Sheet(self._destination)
            sheet_info = dict(self.sheet_template(template_name))
            for metafield, metavalue in values[0]['metafields'].items():  # TODO: get templates
                sheet_info['columns'].append(self.metafield_col_template(metafield))
            await sheet.create(sheet_info)
            await sheet.add_rows(values)
            sheets.append((sheet, values))

        # create_sheet
        # for sheet, values in sheets:
        #     await sheet.add_rows(values)
        # fill rows

        
        

class SmartsheetToBox(TransferClient):
    async def transfer(self):
        raise NotImplementedError
