import os
import re
import socket

from langchain import PromptTemplate
from langchain.agents import create_spark_dataframe_agent
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import CSVLoader, TextLoader, JSONLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from pyspark.conf import SparkConf
from pyspark.sql import SparkSession


class RetriveQnA:

    def ingest_docs(self, file_path, jq_schema):
        if "csv" in file_path.split(".")[-1].lower():
            loader = CSVLoader(file_path)
        elif "txt" in file_path.split(".")[-1].lower():
            loader = TextLoader(file_path)
        elif "json" in file_path.split(".")[-1].lower():
            loader = JSONLoader(file_path, jq_schema=jq_schema)
        data = loader.load()
        print(f"original size of the document: {len(data)}")
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
        documents = text_splitter.split_documents(documents=data)
        print(f"after split the size of the document {len(documents)}")
        print(f"going to insert {len(documents)} chunks to FAISS")
        embeddings = OpenAIEmbeddings(
            deployment="text-embedding-ada-002",
            model="text-embedding-ada-002",
            openai_api_base='https://acc-test-openai.openai.azure.com/',
            openai_api_type="azure",
            chunk_size=1
        )
        vectorstore = FAISS.from_documents(documents, embeddings)
        os.makedirs(os.path.join(os.getcwd(), "vector_db"), exist_ok=True)
        vector_db_name = re.sub("\..*", "", file_path.split("/")[-1])
        vectorstore.save_local(os.path.join(os.getcwd(), "vector_db", vector_db_name))
        print(f"created vector_db {vector_db_name} locally")
        return vector_db_name

    def generate_qna_via_retrievalQA(self, file_path, query, jq_schema=None):
        if not (os.path.exists(os.path.join(os.getcwd(), "vector_db", re.sub("\..*", "", file_path.split("/")[-1])))):
            vector_db_name = self.ingest_docs(file_path, jq_schema=jq_schema)
        else:
            print("skipping vector db creation")
            vector_db_name = re.sub("\..*", "", file_path.split("/")[-1])
        embeddings = OpenAIEmbeddings()
        docsearch = FAISS.load_local(os.path.join("vector_db", vector_db_name), embeddings)
        llm = ChatOpenAI(engine='gpt-4')
        qa = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=docsearch.as_retriever(),
            return_source_documents=True,
        )
        return qa({"query": query})

    def create_spark_session(self, params={}):
        spark_conf = SparkConf()
        spark_conf.setAppName("gx-test")
        spark_conf.set("spark.master", 'k8s://https://kubernetes.default.svc.cluster.local:443')
        spark_conf.set("spark.kubernetes.namespace", "spark-operator")
        spark_conf.set("spark.driver.bindAddress", "0.0.0.0")
        spark_conf.set("spark.driver.host", str(socket.gethostbyname(socket.gethostname())))
        spark_conf.set("spark.driver.port", "50243")
        spark_conf.set("spark.executor.memory", params.get("spark.executor.memory", "2g"))
        spark_conf.set("spark.driver.memory", params.get("spark.driver.memory", "1g"))
        spark_conf.set("spark.executor.instances", params.get("spark.executor.instances", "3"))
        spark_conf.set("spark.executor.cores", params.get("spark.executor.cores", "3"))
        spark_conf.set("spark.kubernetes.container.image", 'crescendoimages.azurecr.io/gpt_test')
        spark_conf.set("spark.kubernetes.authenticate.driver.serviceAccountName", "default")
        self.spark = SparkSession.builder.config(conf=spark_conf).getOrCreate()
        return self.spark

    def read_file_from_blob(self, params):
        self.spark.conf.set(f"fs.azure.account.key.{params['storage_account_name']}.blob.core.windows.net",
                            params['storage_account_key'])
        blob_url = f"wasbs://{params['container_name']}@{params['storage_account_name']}.blob.core.windows.net/{params['blob_name']}"
        self.df = self.spark.read.csv(blob_url, header=True, inferSchema=True)

    def generate_qna_from_spark_df(self, prompt_template, input_variables, template_params):
        llm = ChatOpenAI(engine='gpt-4')
        agent = create_spark_dataframe_agent(llm=llm, df=self.df, verbose=True)
        prompt_template = PromptTemplate(
            template=prompt_template, input_variables=input_variables
        )
        try:
            response = agent.run(prompt_template.format_prompt(**template_params))
        except ValueError as e:
            try:
                response = agent.run(prompt_template.format_prompt(**template_params))
            except ValueError as e1:
                response = str(e1)
                if not response.startswith("Could not parse LLM output: `"):
                    raise e1
                response = response.removeprefix("Could not parse LLM output: `").removesuffix("`")
        return response

    def generate_qna_via_spark_agent(self, params, prompt_template, input_variables, template_params):
        self.create_spark_session(params=params)
        self.read_file_from_blob(params=params)
        response = self.generate_qna_from_spark_df(prompt_template, input_variables, template_params)
        return response


if __name__ == "__main__":
    print(RetriveQnA().generate_qna_via_retrievalQA("sensa_test_data.csv", '''As a financial analyst generate 5 qnA out of the dataset 
    and answers should be descriptive''')['result'])
