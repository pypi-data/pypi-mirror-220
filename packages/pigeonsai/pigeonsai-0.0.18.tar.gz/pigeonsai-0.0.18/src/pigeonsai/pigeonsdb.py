import requests
import json
import warnings
from tenacity import retry, wait_exponential, stop_after_attempt
from tqdm import tqdm

warnings.filterwarnings("ignore")

API_URL = "http://test-search-1248249294.us-east-2.elb.amazonaws.com:8080/search"
API_URL_TEST = "http://172.30.36.170:3000/api/v1"
GET_DB_INFO_API = "https://api.pigeonsai.com/api/v1/sdk/get-db-info"
ADD_API_URL = "http://add-dev-177401989.us-east-2.elb.amazonaws.com:8080/add_documents"
DELETE_API_URL = "http://add-dev-177401989.us-east-2.elb.amazonaws.com:8080/delete_documents"


class PigeonsDBError(Exception):
    pass


class PigeonsDB:
    __connection = None
    __index_p = None

    @staticmethod
    def init(API_KEY, dbname):
        if not API_KEY:
            raise ValueError("Missing API_KEY")
        if not dbname:
            raise ValueError("Missing dbname")
        index_p, connect = _get_db_info(api_key=API_KEY, dbname=dbname)
        if connect:
            PigeonsDB.__connection = connect
            PigeonsDB.__index_p = index_p
        else:
            raise PigeonsDBError("API key or DB name not found")

    @staticmethod
    def search(query_text,
               namespace="documents",
               k=5,
               metadata_filters=None,
               keywords=None,
               rerank=False):

        if not query_text:
            print("Missing query_text")
            return

        url = API_URL #
        headers = {"Content-Type": "application/json"}
        data = {
            "connection": PigeonsDB.__connection,
            "index_path": PigeonsDB.__index_p,
            "query_text": query_text,
            "k": k,
            "namespace": namespace,
            "metadata_filters": metadata_filters,
            "keywords": keywords,
            "rerank": rerank
        }

        response = requests.post(url, headers=headers, data=json.dumps(data))
        res = json.loads(response.text)
        return res

    @staticmethod
    @retry(wait=wait_exponential(multiplier=1, min=2, max=60), stop=stop_after_attempt(3))
    def add(documents: list,
            metadata_list: list = None,
            namespace: str = "documents"):

        if not documents:
            raise PigeonsDBError("Missing documents.")

        if not isinstance(documents, list):
            raise ValueError(f'documents is expected to be a list, found {type(documents)}')
        if metadata_list is not None and not isinstance(metadata_list, list):
            raise ValueError(f'metadata_list is expected to be a list, found {type(metadata_list)}')

        chunk_size = 100
        chunks = [documents[i:i + chunk_size] for i in range(0, len(documents), chunk_size)]

        url = ADD_API_URL
        headers = {"Content-Type": "application/json"}
        for chunk in tqdm(chunks):
            data = {
                "connection": PigeonsDB.__connection,
                "index_path": PigeonsDB.__index_p,
                "documents": chunk,
                "namespace": namespace,
                "metadata_list": metadata_list
            }
            response = requests.post(url, headers=headers, data=json.dumps(data))
            if response.status_code == 200:
                print("\nSuccess: Documents added successfully.")
            else:
                print("\nERROR: Problem occurred while adding documents.")

    @staticmethod
    def delete_documents(object_ids: list):

        if not object_ids:
            print("Missing object_ids")
            return

        if not isinstance(object_ids, list):
            raise ValueError(f'documents is expected to be a list, found {type(object_ids)}')

        url = DELETE_API_URL
        headers = {"Content-Type": "application/json"}
        data = {
            "connection": PigeonsDB.__connection,
            "index_path": PigeonsDB.__index_p,
            "object_ids": object_ids
        }
        response = requests.post(url, headers=headers, data=json.dumps(data))
        print(response.json())

    @staticmethod
    def create_db_instance(dbname: str, instance_type: str):
        url = API_URL_TEST + "/create-db-instance"
        headers = {"Content-Type": "application/json"}
        data = {
            "api_key": PigeonsDB.__api_key,
            "dbname": dbname,
            "db_instance_class": instance_type
        }

        try:
            response = requests.post(url, headers=headers, data=json.dumps(data))
            status_code = response.status_code

            if status_code == 200:
                print(f"Successfully created a new db instance with dbname: {dbname}")
            else:
                print('Status code: ', status_code)
                response = response.json()
                print('Res:', response.get('Message'))
        except Exception as e:
            raise PigeonsDBError(f"Error occurred while creating a db instance")

    @staticmethod
    def delete_db_instance(dbname: str):
        url = API_URL_TEST + "/delete-db-instance"
        headers = {"Content-Type": "application/json"}
        data = {
            "api_key": PigeonsDB.__api_key,
            "dbname": dbname,
        }

        try:
            response = requests.post(url, headers=headers, data=json.dumps(data))
            status_code = response.status_code

            if status_code == 200:
                print(f"Successfully deleted a db instance with dbname: {dbname}")
            else:
                print('Status code: ', status_code)
                response = response.json()
                print('Res:', response.get('Message'))
        except Exception as e:
            raise PigeonsDBError(f"Error occurred while deleting a db instance.")



def _get_db_info(api_key: str, dbname: str):
    url = GET_DB_INFO_API
    headers = {"Content-Type": "application/json"}
    data = {"api_key": api_key, "dbname": dbname}
    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code != 200:
        raise PigeonsDBError("API_KEY or db_name doesn't match.")

    db_info = response.json().get('DB info', {})
    index_p = db_info.get('s3_identifier')
    keys = ['dbname', 'user', 'password', 'host']
    connect = {key: db_info.get(key) for key in keys}

    return index_p, connect



class SemanticChunking:

    def ada(text, min_tokens, max_tokens):
        # Tokenize the text into sentences
        sentences = sent_tokenize(text)
        print(sentences)
        # Convert sentences to embeddings using a pre-trained model
        embeddings = []
        for i in sentences:
            tensors = get_embedding(i)
            embeddings.append(tensors)
        embeddings = np.array((embeddings))
        # Calculate the number of clusters based on the desired token count
        total_tokens = sum([len(word_tokenize(sentence)) for sentence in sentences])
        num_clusters = max(1, int(total_tokens / max_tokens))

        # Train the k-means model on the embeddings
        kmeans = faiss.Kmeans(embeddings.shape[1], num_clusters, niter=20, verbose=False)
        kmeans.train(embeddings.astype(np.float32))

        # Cluster the sentences based on the k-means model
        _, cluster_assignments = kmeans.index.search(embeddings.astype(np.float32), 1)
        clusters = [[] for _ in range(num_clusters)]
        for i, assignment in enumerate(cluster_assignments):
            clusters[assignment[0]].append(sentences[i])

        # Create chunks based on the clusters and the desired token count
        chunks = []
        for cluster in clusters:
            chunk = []
            tokens_in_chunk = 0
            for sentence in cluster:
                tokens = word_tokenize(sentence)
                num_tokens = len(tokens)
                if tokens_in_chunk + num_tokens > max_tokens:
                    chunks.append(' '.join(chunk))
                    chunk = [sentence]
                    tokens_in_chunk = num_tokens
                elif tokens_in_chunk + num_tokens < min_tokens:
                    chunk.append(sentence)
                    tokens_in_chunk += num_tokens
                else:
                    chunk.append(sentence)
                    chunks.append(' '.join(chunk))
                    chunk = []
                    tokens_in_chunk = 0
            if chunk:
                chunks.append(' '.join(chunk))

        return chunks
    
