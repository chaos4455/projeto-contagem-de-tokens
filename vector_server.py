import grpc
from concurrent import futures
import sqlite3
import numpy as np

# Importar os arquivos gerados pelo protobuf
import proto.vector_service_pb2 as vector_service_pb2
import proto.vector_service_pb2_grpc as vector_service_pb2_grpc

class VectorServicer(vector_service_pb2_grpc.VectorServiceServicer):
    def __init__(self):
        self.db_path = "vectors_continuo.db"

    def get_db_connection(self):
        return sqlite3.connect(self.db_path)

    def GetVector(self, request, context):
        with self.get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, word, vector 
                FROM vectors 
                WHERE id = ?
            """, (request.id,))
            
            row = cursor.fetchone()
            if not row:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details(f'Vector with id {request.id} not found')
                return vector_service_pb2.VectorResponse()

            id, word, vector_blob = row
            vector = np.frombuffer(vector_blob, dtype=np.float32)
            
            return vector_service_pb2.VectorResponse(
                id=id,
                word=word,
                vector=vector.tolist()
            )

    def ListVectors(self, request, context):
        with self.get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, word, vector FROM vectors")
            
            for row in cursor:
                id, word, vector_blob = row
                vector = np.frombuffer(vector_blob, dtype=np.float32)
                
                yield vector_service_pb2.VectorResponse(
                    id=id,
                    word=word,
                    vector=vector.tolist()
                )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    vector_service_pb2_grpc.add_VectorServiceServicer_to_server(
        VectorServicer(), server
    )
    server.add_insecure_port('[::]:50051')
    print("Servidor iniciado na porta 50051")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve() 