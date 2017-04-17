#  transfer-client
import asyncio


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

    async def __parse_metadata(self, metadata):

        res = []
        for file_info, meta_file_info in metadata:
            data = {
                'name': file_info['name'],
                'path': [p['name'] for p in file_info['path_collection']['entries']],
                'created_at': file_info['created_at'],
                'modified_at': file_info['modified_at']
            }

            data['metafields'] = []

            for meta_file_line_info in meta_file_info:
                data['metafields'].append({
                    'name': meta_file_line_info['$template'],
                    'values': {k:v for k,v in meta_file_line_info.items() if not k.startswith("$")}
                })
            res.append(data)
    
        return res
    
    async def transfer(self):
        # gather metadata
        folder = self._source.folder()
        all_metadata = []
        for _file in await folder.files:
            file_info = (_file.get(), _file.get_metadata())
            all_metadata.append(asyncio.gather(*file_info))
        all_metadata = await asyncio.gather(*all_metadata)

        # parse_metadata
        print("\nSTART: ===================\n")
        parsed_metadata = await self.__parse_metadata(all_metadata)
        # create_sheet
        print(parsed_metadata)
        print("\n END: =====================\n")
        # fill rows


class SmartsheetToBox(TransferClient):
    async def transfer(self):
        raise NotImplementedError
