import grpc
import sys

sys.path.insert(1, '/workspaces/tensornlp')

#import grpcDir.file_pb2 as file_pb2
from grpcDir import file_pb2
#import grpcDir.file_pb2_grpc as file_pb2_grpc
from grpcDir import file_pb2_grpc
import time

class Client:
    def __init__(self, host) -> None:
        channel = grpc.insecure_channel(host)
        self.stub = file_pb2_grpc.FileServiceStub(channel)
        
    def GetFile(self, filename):
        print("Getting file")
        
        # by_name_selector = file_pb2.FileSelector.ByName(name=filename)
        # print(by_name_selector)
        # selector_ = file_pb2.FileSelector(by_name=by_name_selector)
        # print(selector_)
        selector_ = file_pb2.FileSelector(id=filename)
        GFR = file_pb2.GetFileRequest(selector=selector_)
        
        file_response = self.stub.GetFile(GFR)
        file = file_response.file
        file_name = file.name
        file_data = file.data_chunk
        
        # write the file to the local storage
        with open("my_file.txt", "wb") as f:
            f.write(file_data)
            
        return file
    
    def CreateFile(self, filename):
        print("Creating file")
        
        file_data = b''
        file_meta = file_pb2.CreateFileMeta()
        
        try:
            with open(filename, "rb") as f:
                file_data = f.read()
                file_meta = file_pb2.CreateFileMeta(parent_id = filename+"xyx",name=filename)
        except:
            print("Error opening file "+filename)
            return
        
        CFR = [file_pb2.CreateFileRequest(meta = file_meta, data_chunk=file_data)]
        
        return self.stub.CreateFile(CFR.__iter__())
                
if __name__ == '__main__':    
    tc = Client('localhost:50051')
    # Call GetFile
    tc.CreateFile("pluto.txt")
    tc.GetFile("dummy.txt")
    #tc.GetFile(file_pb2.FileRequest(name="test.txt"))