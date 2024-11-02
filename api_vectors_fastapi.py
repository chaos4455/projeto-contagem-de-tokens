from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import sqlite3
import numpy as np
from datetime import datetime

app = FastAPI(title="API de Vetores Contínuos",
             description="API RESTful para gerenciar vetores de palavras")

# Configuração do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATABASE_PATH = 'vectors_continuo.db'

# Modelos Pydantic
class VectorBase(BaseModel):
    word: str
    vector: List[float]
    palavra_origem: Optional[str] = None

class VectorCreate(VectorBase):
    pass

class Vector(VectorBase):
    id: int
    timestamp: datetime
    
    class Config:
        from_attributes = True

# Funções auxiliares
def blob_to_array(blob):
    return np.frombuffer(blob).tolist()

def array_to_blob(array):
    return np.array(array, dtype=np.float32).tobytes()

# Rotas CRUD
@app.post("/vectors/", response_model=Vector, status_code=201)
async def create_vector(vector: VectorCreate):
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        vector_blob = array_to_blob(vector.vector)
        timestamp = datetime.now()
        
        cursor.execute("""
            INSERT INTO word_vectors (word, vector, palavra_origem, timestamp)
            VALUES (?, ?, ?, ?)
        """, (vector.word, vector_blob, vector.palavra_origem, timestamp))
        
        vector_id = cursor.lastrowid
        conn.commit()
        
        # Busca o vetor recém-criado
        cursor.execute("""
            SELECT id, word, vector, palavra_origem, timestamp
            FROM word_vectors WHERE id = ?
        """, (vector_id,))
        
        result = cursor.fetchone()
        conn.close()
        
        return {
            "id": result[0],
            "word": result[1],
            "vector": blob_to_array(result[2]),
            "palavra_origem": result[3],
            "timestamp": result[4]
        }
        
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Palavra já existe no banco de dados")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/vectors/", response_model=List[Vector])
async def read_vectors(skip: int = 0, limit: int = 100):
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, word, vector, palavra_origem, timestamp
            FROM word_vectors
            LIMIT ? OFFSET ?
        """, (limit, skip))
        
        results = cursor.fetchall()
        conn.close()
        
        return [{
            "id": row[0],
            "word": row[1],
            "vector": blob_to_array(row[2]),
            "palavra_origem": row[3],
            "timestamp": row[4]
        } for row in results]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/vectors/{vector_id}", response_model=Vector)
async def read_vector(vector_id: int):
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, word, vector, palavra_origem, timestamp
            FROM word_vectors WHERE id = ?
        """, (vector_id,))
        
        result = cursor.fetchone()
        conn.close()
        
        if result is None:
            raise HTTPException(status_code=404, detail="Vetor não encontrado")
            
        return {
            "id": result[0],
            "word": result[1],
            "vector": blob_to_array(result[2]),
            "palavra_origem": result[3],
            "timestamp": result[4]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/vectors/{vector_id}", response_model=Vector)
async def update_vector(vector_id: int, vector: VectorCreate):
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        vector_blob = array_to_blob(vector.vector)
        timestamp = datetime.now()
        
        cursor.execute("""
            UPDATE word_vectors
            SET word = ?, vector = ?, palavra_origem = ?, timestamp = ?
            WHERE id = ?
        """, (vector.word, vector_blob, vector.palavra_origem, timestamp, vector_id))
        
        if cursor.rowcount == 0:
            conn.close()
            raise HTTPException(status_code=404, detail="Vetor não encontrado")
            
        conn.commit()
        
        # Busca o vetor atualizado
        cursor.execute("""
            SELECT id, word, vector, palavra_origem, timestamp
            FROM word_vectors WHERE id = ?
        """, (vector_id,))
        
        result = cursor.fetchone()
        conn.close()
        
        return {
            "id": result[0],
            "word": result[1],
            "vector": blob_to_array(result[2]),
            "palavra_origem": result[3],
            "timestamp": result[4]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/vectors/{vector_id}")
async def delete_vector(vector_id: int):
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM word_vectors WHERE id = ?", (vector_id,))
        
        if cursor.rowcount == 0:
            conn.close()
            raise HTTPException(status_code=404, detail="Vetor não encontrado")
            
        conn.commit()
        conn.close()
        
        return {"message": "Vetor deletado com sucesso"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
