from flask import Flask, jsonify
from flask_cors import CORS
import sqlite3
import numpy as np

app = Flask(__name__)
CORS(app)

DATABASE_PATH = 'vectors_continuo.db'

def get_vector_by_id(vector_id):
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, word, vector, palavra_origem, timestamp 
            FROM word_vectors 
            WHERE id = ?
        """, (vector_id,))
        
        result = cursor.fetchone()
        
        if result:
            id_, word, vector_blob, palavra_origem, timestamp = result
            vector_array = np.frombuffer(vector_blob)
            
            return {
                "id": id_,
                "word": word,
                "vector": vector_array.tolist(),
                "palavra_origem": palavra_origem,
                "timestamp": timestamp
            }
        else:
            return None
            
    except Exception as e:
        print(f"Erro ao consultar banco: {str(e)}")
        return None
    finally:
        conn.close()

@app.route('/vector/<int:vector_id>', methods=['GET'])
def get_vector(vector_id):
    result = get_vector_by_id(vector_id)
    
    if result:
        return jsonify({
            "status": "success",
            "data": result
        }), 200
    else:
        return jsonify({
            "status": "error",
            "message": "Vetor não encontrado"
        }), 404

@app.errorhandler(Exception)
def handle_error(error):
    return jsonify({
        "status": "error",
        "message": str(error)
    }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9777, debug=False)
