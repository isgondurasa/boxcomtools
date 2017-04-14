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
        return metadata
    
    async def transfer(self):
        # gather metadata
        folder = self._source.folder()
        all_metadata = []
        for _file in await folder.files:
            await _file.get()
            print(_file.__dict__)
            all_metadata.append({_file['name']: _file.get_metadata()})
        all_metadata = await asyncio.gather(*all_metadata)

        # parse_metadata
        parsed_metadata = await self.__parse_metadata(all_metadata)
        # create_sheet
        print(parsed_metadata)

        # fill rows


class SmartsheetToBox(TransferClient):
    async def transfer(self):
        raise NotImplementedError
