from langchain_community.document_loaders import UnstructuredEmailLoader

doc = UnstructuredEmailLoader(file_path='localbin/users_space/1815124195/translated/work_Translated.eml', process_attachments=False).load()
print(doc[0].page_content)
