import asyncio


class TransferClient:
    """
    Transfer data endpoint
    assume that both sourse and destination 
    as access and refresh tokens already
    """
    
    def __init(self, source, destination):
        self._source = source
        self._destination = destination


class BoxToSmartsheet(TransferClient):
    async def transfer(self):
        folder = self._source.folder
        all_metadata = []
        for _file in  await folder.files:
            all_metadata.append(_file.get_metadata())
    
        all_metadata = await asyncio.gather(*all_metadata)
        
        
class SmartsheetToBox(TransferClient):
    async def transfer(self):
        raise NotImplementedError
