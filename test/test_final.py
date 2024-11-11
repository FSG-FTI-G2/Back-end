import os
from app.models.file_schema import FileSchema, FileType
from app.providers import qdrant_client
from io import BytesIO
import unittest
from app.utils.prompt_template import get_prompt_by_role
from app.providers import llm, embedder
from app.controllers.extraction_controller import extraction_features, extraction_file_content
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from sentence_transformers import SentenceTransformer

folder_path = os.path.join(os.getcwd(), 'temp')


def add_documents_to_vectordb(folder_path):
    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)
        file_name = os.path.basename(file_path).split('.')[0]
        file_type = os.path.splitext(file_path)[-1][1:]

        if file_name.endswith('.txt'):
            file_type = FileType.TXT
        elif file_name.endswith('.docx'):
            file_type = FileType.DOCX
        elif file_name.endswith('.pdf'):
            file_type = FileType.PDF

        with open(file_path, 'rb') as f:
            file_content = BytesIO(f.read())
            content = extraction_file_content(file_type, file_content)
            print(f"Extracted content from {file_name}: {content[:100]}...")

        file_schema = FileSchema(
            user_id="user_id",
            type=file_type,
            file_name=file_name,
            file_path=file_path,
        )
        file_schema.create()

        extraction_features(content, file_schema)


def generate(question_input, role_input, llm_model):
    role_prompt = get_prompt_by_role(role_input)

    vector_search_question = qdrant_client.search_vector(question_input)

    content_retrieve = vector_search_question[0].payload['content']

    response = llm.response(
        question=question_input + content_retrieve,
        role=role_prompt,
        model_name=llm_model
    )

    return response


def compute_similarity(text1, text2):
    embedding1 = embedder.embed(text1)
    embedding2 = embedder.embed(text2)

    similarity_score = cosine_similarity([embedding1], [embedding2])

    return similarity_score[0][0]


class TestApp(unittest.TestCase):
    #     def test_add_documents_to_vectordb(self):
    #         folder_path = test_folder_path
    #         try:
    #             add_documents_to_vectordb(folder_path)
    #             self.assertTrue(True)
    #         except Exception as e:
    #             self.fail(f"add_documents_to_vectordb failed with exception {e}")
    add_documents_to_vectordb(folder_path)
    # lst = qdrant_client.search_vector("What is AI?")[0].payload['content']

    # # for i, ans in enumerate(lst):
    # #     print(f"Answer {i+1}: {ans}")
    # print(lst)

# def test_generate(self):
#     question_input = "What is AI?"
#     role_input = "student"
#     llm_model = "gemini"

#     try:
#         response = generate(question_input, role_input, llm_model)
#         self.assertIsInstance(response, str)
#         self.assertGreater(
#             len(response), 0, "Response length should be greater than 0")
#     except Exception as e:
#         self.fail(f"generate failed with exception {e}")

# def test_similarity_on_dataframe(self):
#     df = pd.read_csv('transformer_questions_answers.csv')
#     sim_lst = []

#     for i in range(len(df)):
#         question = df['Question'][i]
#         answer_llm = generate(question_input=question,
#                               role_input="student", llm_model="gemini")
#         answer_origin = df['Answer'][i]
#         similarity_score = compute_similarity(answer_llm, answer_origin)
#         sim_lst.append(similarity_score)

#     mean_similarity = np.mean(sim_lst)
#     self.assertGreaterEqual(mean_similarity, 0)
#     self.assertLessEqual(mean_similarity, 1)
