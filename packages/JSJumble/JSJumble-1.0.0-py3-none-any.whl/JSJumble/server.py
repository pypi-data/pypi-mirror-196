from flask import Flask, request, render_template, jsonify, make_response
from waitress import serve
from os import path,makedirs,walk,remove
from pathlib import Path
from shutil import copyfile
import sys,hashlib, sqlite3

BASE_DIR = Path(__file__).resolve().parent


STATIC_DIR = None
STATIC_COMPRESSED_DIR = None
STATIC_CACHES_PATH = None

CACHE_CON = None
CACHE_CUR = None

ENGINE = None

JSONLY = True
DELETE_UNLISTED = True

flaskApi = Flask(__name__,
                    template_folder=path.join(BASE_DIR,"template"),
                    static_url_path='/static', 
                    static_folder=path.join(BASE_DIR,"static"),
                )

@flaskApi.route('/', methods=['GET'])
def home():
    return render_template("obfuscator.html")


@flaskApi.route('/get_change', methods=['GET'])
def get_change():
    result = []
    BUF_SIZE = 65536
    
    CACHE_CUR.execute("CREATE TABLE IF NOT EXISTS static (PATH TEXT, SHA512 TEXT);")
    CACHE_CUR.execute("CREATE TABLE IF NOT EXISTS static_compressed (PATH TEXT, SHA512 TEXT);")
    CACHE_CON.commit()
    for dir, subdirs, files in walk(path.join(STATIC_DIR)):
        for name in files:
            base_path = path.join(dir, name)
            print(base_path)
            rel_dir = path.relpath(base_path,path.join(STATIC_DIR))
            sha512 = hashlib.sha512()
            with open(base_path, 'rb') as f:
                while True:
                    data = f.read(BUF_SIZE)
                    if not data:
                        break
                    sha512.update(data)
            sha = sha512.hexdigest()
            compressed_path = path.join(STATIC_COMPRESSED_DIR,rel_dir)
            compressed_parent = path.join(path.split(compressed_path)[0])
            
            if path.splitext(base_path)[1] == ".js":
                def verify():
                    if path.exists(compressed_path):
                        CACHE_CUR.execute(f"SELECT SHA512 FROM static WHERE PATH = '{base_path}'")
                        caches_sha = CACHE_CUR.fetchone()
                        if caches_sha: caches_sha = caches_sha[0]
                        if caches_sha == sha:
                            sha512 = hashlib.sha512()
                            with open(compressed_path, 'rb') as f:
                                while True:
                                    data = f.read(BUF_SIZE)
                                    if not data:
                                        break
                                    sha512.update(data)
                            compressed_sha = sha512.hexdigest()
                            CACHE_CUR.execute(f"SELECT SHA512 FROM static_compressed WHERE PATH = '{compressed_path}'")
                            caches_compressed_sha = CACHE_CUR.fetchone()
                            if caches_compressed_sha: caches_compressed_sha = caches_compressed_sha[0]
                            if compressed_sha == caches_compressed_sha: return True
                            else: return False
                        else:
                            return False
                    else:
                        return False
                    
                if not verify():
                    result.append({
                            "rel_dir": rel_dir,
                            "base_path": base_path,
                            "sha": sha,
                        })
            elif not JSONLY:
                if path.exists(compressed_path):
                    compressed_sha512 = hashlib.sha512()
                    with open(compressed_path, 'rb') as f:
                        while True:
                            data = f.read(BUF_SIZE)
                            if not data:
                                break
                            compressed_sha512.update(data)
                    compressed_sha = compressed_sha512.hexdigest()
                    if sha != compressed_sha: 
                        remove(compressed_path)
                        if not path.exists(compressed_parent): makedirs(compressed_parent)
                        copyfile(base_path, compressed_path) 
                else:
                    if not path.exists(compressed_parent): makedirs(compressed_parent)
                    copyfile(base_path, compressed_path)
    
    data = {
        "engine": ENGINE,
        "data": result
        }
    return jsonify(data)

@flaskApi.route('/get_file', methods=['POST'])
def get_file():
    data = request.values
    dir = data["dir"]
    
    with open(dir,"r") as f:
        data = f.read()
        
    response = make_response(data, 200)
    response.mimetype = "text/plain"
    return response
    
@flaskApi.route('/save_compressed', methods=['POST'])
def save_compressed():
    BUF_SIZE = 65536
    data = request.values
    compressed_path = path.join(STATIC_COMPRESSED_DIR,data["rel_dir"])
    compressed_parent = path.join(path.split(compressed_path)[0])
    dir = data["dir"]
    sha = data["sha"]
    content = data["content"]
    
    # CACHES WRITE
    if not path.exists(compressed_parent): makedirs(compressed_parent)
    with open(compressed_path,"w") as f:
        f.write(content)    
    
    CACHE_CUR.execute(f'''SELECT COUNT(*) FROM static WHERE PATH = "{dir}";''')
    if CACHE_CUR.fetchone()[0]:
        CACHE_CUR.execute(f'''
                            UPDATE static
                            SET 
                                SHA512 = "{sha}"
                            WHERE
                                PATH = "{dir}"
                        ''')
    else:
        
        CACHE_CUR.execute(f'''
                            INSERT INTO static (PATH, SHA512) 
                            values ("{dir}", "{sha}");
                        ''')
    
    # CACHES COMPRESSED WRITE
    sha512 = hashlib.sha512()
    with open(compressed_path, 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            sha512.update(data)
    compressed_sha = sha512.hexdigest()
    
    CACHE_CUR.execute(f'''SELECT COUNT(*) FROM static_compressed WHERE PATH = "{compressed_path}";''')
    if CACHE_CUR.fetchone()[0]:
        CACHE_CUR.execute(f'''
                            UPDATE static_compressed
                            SET 
                                SHA512 = "{compressed_sha}"
                            WHERE
                                PATH = "{compressed_path}"
                        ''')
    else:
        
        CACHE_CUR.execute(f'''
                            INSERT INTO static_compressed (PATH, SHA512) 
                            values ("{compressed_path}", "{compressed_sha}");
                        ''')
    CACHE_CON.commit()
    return jsonify({"status":True})

@flaskApi.route('/delete_unlist', methods=['POST'])
def delete_unlist():
    from_path = Path(STATIC_DIR)
    to_path = Path(STATIC_COMPRESSED_DIR)

    difference = (set(map(lambda p: p.relative_to(to_path), to_path.rglob('*'))) -
                set(map(lambda p: p.relative_to(from_path), from_path.rglob('*'))))
    
    for i in difference:
        unlist_path = path.join(STATIC_DIR,i)
        CACHE_CUR.execute(f'''
                            DELETE FROM static
                            WHERE PATH = "{unlist_path}";
                        ''')
        if DELETE_UNLISTED:
            unlist_path = path.join(STATIC_COMPRESSED_DIR,i)
            if path.exists(unlist_path): remove(unlist_path)
            CACHE_CUR.execute(f'''
                                DELETE FROM static_compressed
                                WHERE PATH = "{unlist_path}";
                            ''')
    CACHE_CON.commit()
    if DELETE_UNLISTED:
        return jsonify({"result": len(difference)})
    else:
        return jsonify({"result": "ignored_compress"})

def start(host,port,static_dir,compress_dir,cache_dir,delete_unlisted, js_only, engine):
    global STATIC_DIR, STATIC_COMPRESSED_DIR, CACHE_CON, CACHE_CUR, DELETE_UNLISTED,JSONLY ,ENGINE
    
    STATIC_DIR = static_dir
    STATIC_COMPRESSED_DIR = compress_dir
    
    CACHE_CON = sqlite3.connect(cache_dir,check_same_thread=False)
    CACHE_CUR = CACHE_CON.cursor()
    JSONLY = js_only
    DELETE_UNLISTED = delete_unlisted
    ENGINE = engine
    
    if getattr(sys, 'frozen', False):
        serve(flaskApi, host=host, port=port)
    else:
        flaskApi.run(host=host,port=port, debug=True, use_reloader=False)
            

