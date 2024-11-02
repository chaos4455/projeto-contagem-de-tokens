import grpc
import proto.vector_service_pb2 as vector_service_pb2
import proto.vector_service_pb2_grpc as vector_service_pb2_grpc

def get_vector(stub, id):
    request = vector_service_pb2.VectorRequest(id=id)
    try:
        response = stub.GetVector(request)
        print(f"ID: {response.id}")
        print(f"Palavra: {response.word}")
        print(f"Vetor: {response.vector[:5]}...")  # Mostra primeiros 5 elementos
    except grpc.RpcError as e:
        print(f"Erro: {e.details()}")

def main():
    channel = grpc.insecure_channel('localhost:50051')
    stub = vector_service_pb2_grpc.VectorServiceStub(channel)
    
    # Teste com ID específico
    get_vector(stub, 1)
    
    # Listar todos os vetores
    print("\nListando todos os vetores:")
    for vector in stub.ListVectors(vector_service_pb2.ListVectorsRequest()):
        print(f"ID: {vector.id}, Palavra: {vector.word}")

if __name__ == '__main__':
    main()
